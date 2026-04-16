# Stigler 2026 — Plan

A modern, automated, **truly daily** Stigler diet. Cheapest basket of real foods that
meets nutrient targets, filtered by dietary mode (omnivore / pescatarian / vegetarian /
ovo-lacto / vegan), priced from a real grocery store at a real location. Linear program.
Light enough to run in a GitHub Action and publish a `data.json` consumed by a static
page on the website.

Inspired by Stigler 1945 ("The Cost of Subsistence") and Garille & Gass 2001 ("Stigler's
Diet Problem Revisited"). Source corpus already extracted under `sources/`.

The framing — "the cheapest shoppable basket at *this Kroger* that hits your nutrients
today, by diet mode" — is honest, falsifiable (you can go to the store and buy it), and
genuinely new vs the BLS-national-average literature.

---

## Why this fits

- **LP is tiny:** ~80 foods × ~15 nutrients → milliseconds with `scipy.optimize.linprog`.
- **Kroger Public API is the unlock:** free, official, machine-readable, daily-fresh,
  per-location prices, 10,000 calls/day rate limit. Replaces BLS as the price source.
- **Output is one small JSON file** — perfect for `cdn.jsdelivr.net/gh/...` hosting like
  `cpudata`, then rendered by a static HTML page in the existing website.
- **Pipeline is deterministic given inputs** — Action is idempotent, no DB, no scraping.

---

## Scope (v1)

- **Kroger family stores only** (Kroger, Ralphs, King Soopers, Fred Meyer, Harris
  Teeter, Smith's, etc. — ~2,800 US locations).
- **Three locations** to start, one each from West / Midwest / South-or-East — sets up
  "price by location" honestly without explosion.
- One adult profile (male, 31–50, moderate activity) — DRI from NIH ODS.
- Five dietary modes: `omnivore`, `pescatarian`, `vegetarian`, `ovo_lacto`, `vegan`.
- ~80 staple SKUs, curated once via the discovery pass (below), refreshed quarterly.
- **True daily cron** — Kroger prices change daily (regular vs promo), so this is no
  longer theatrical.

Deferred to v2: more locations, more body profiles, EAT–Lancet planetary-bound overlay,
GHG/water co-objective, palatability bounds, halal/kosher tags, Open Prices fallback for
non-US comparison.

---

## Data sources

| Source | Use | License | Cadence |
|---|---|---|---|
| **Kroger Public Products API** (`/v1/products`) | per-SKU price (regular + promo) at a `locationId`, plus `categories` taxonomy | free for personal/dev use under Kroger ToS; OAuth2 client-credentials | **daily**; ~80 SKUs × 3 locations = ~6 batched calls/day, well under the 10k/day limit |
| **USDA FoodData Central** (Foundation + SR Legacy) | per-100g nutrient profile, joined to Kroger SKU by manual mapping (UPC → FDC ID in `data/skus.yaml`) | public domain | quarterly; cached |
| **NIH ODS Dietary Reference Intakes** | RDA / AI / UL targets per nutrient | public domain | ~yearly; vendored as `data/dri.json` |
| **EAT–Lancet 2.0 ranges** | optional comparison overlay (v2) | CC-BY | yearly; vendored |
| **Open Prices** (Open Food Facts) | optional v2 fallback for items Kroger doesn't carry, or for a EU comparison tier | ODbL | as-uploaded; pulled on demand |

Notably **dropped** from earlier draft: BLS APR (insufficient food coverage — no fish,
nuts, soy, leafy greens beyond romaine), Numbeo (ToS friction), commercial scraping APIs
(grey legality, redundant given Kroger).

---

## Discovery vs daily refresh

Kroger's API has **no full catalog dump** — only `filter.term` (fuzzy search) and
`filter.productId` (exact lookup). Pagination via `filter.start`/`filter.limit`, default
10 results, max raised by setting `filter.limit`.

Two-phase strategy:

### Discovery (one-off, re-run quarterly)

`diet discover` — semi-manual:

1. Read ~40 staple search terms from `data/discovery_terms.yaml` (`milk`, `eggs`,
   `chicken breast`, `ground beef`, `oats`, `lentils`, `tofu`, `spinach`, `sweet
   potato`, `peanut butter`, `sardines`, `nutritional yeast`, `fortified soy milk`, …).
2. For each term, paginate
   `GET /v1/products?filter.term=<term>&filter.locationId=<seed>&filter.limit=50&filter.start=0..200`
   → collect candidate SKUs (productId, UPC, description, brand, categories,
   regular price).
3. Auto-rank: prefer Kroger store brand + non-organic + largest pack size + lowest
   $/unit (proxy for "what a budget shopper buys").
4. Write `data/sku_candidates.yaml` for human review.
5. Operator picks ~80 SKUs and copies them into `data/skus.yaml` with manual fields:
   - `fdc_id` (USDA FoodData Central ID for nutrition lookup)
   - `unit_grams` (Kroger price is per-package; nutrients are per-100g — need this to
     translate)
   - `dietary_categories` (set; intersect with mode-exclusion to filter)

Discovery uses ~150 API calls; one-off cost. Dietary tagging is mostly automatic from
Kroger's `categories` field, with a small override file for edge cases.

### Daily refresh (in CI)

`diet ingest` — non-interactive:

1. Load `data/skus.yaml`.
2. For each (`location` × batch of `productId`s), call
   `GET /v1/products?filter.productId=<id1>,<id2>,...&filter.locationId=<loc>` (the API
   accepts comma-separated productId batches).
3. Cache today's response under `data/raw/kroger/<date>/<location>.json`.
4. Update `data/prices_current.json` with `{(sku, location): {regular, promo, source_date}}`.

API budget: 80 SKUs ÷ batch_size ~50 ≈ 2 calls × 3 locations = **~6 calls/day**.

---

## Model

Decision variables: `x_i ≥ 0`, grams/day of food `i`.

```
minimize    Σ price_per_g(i, location) * x_i
subject to  Σ nutrient(i, n) * x_i ≥ RDA(n)        for each nutrient n
            Σ nutrient(i, n) * x_i ≤ UL(n)         for nutrients with upper limits
            x_i = 0                                 for foods excluded by mode
            x_i ≤ max_serving(i)                    palatability cap (e.g. ≤ 500 g/day)
```

`price_per_g` uses promo when active, else regular.

Solver: `scipy.optimize.linprog(method="highs")`. No external solver needed.

Outputs per (mode × location):
- selected foods with grams/day, cost contribution, % of basket
- daily total cost
- nutrient delivery vs RDA (which constraints are binding)
- dual values → "shadow price" of each binding nutrient (= marginal $/unit)
- `infeasible: true` with diagnostic if a mode can't hit all RDAs (e.g. vegan B12
  without fortified options)

---

## Dietary mode tagging

Kroger returns a `categories` array per product (e.g. `["Dairy"]`,
`["Meat & Seafood"]`, `["Produce"]`, `["Pantry"]`). That alone covers ~80% of the work.

`data/skus.yaml`:

```yaml
- product_id: "0001111041600"
  fdc_id: 173441
  name: "Kroger 2% Reduced Fat Milk, 1 gal"
  unit_grams: 3784
  kroger_categories: [Dairy]
  dietary_categories: [dairy]
  modes_excluded: [vegan]

- product_id: "0001111060710"
  fdc_id: 174270
  name: "Simple Truth Organic Firm Tofu, 14 oz"
  unit_grams: 397
  kroger_categories: [Natural Foods]
  dietary_categories: [legume, soy]
  modes_excluded: []
```

Mode → excluded `dietary_categories` map lives in code:

```python
MODE_EXCLUDES = {
    "omnivore":      set(),
    "pescatarian":   {"meat_red", "meat_white", "meat_processed"},
    "vegetarian":    {"meat_red", "meat_white", "meat_processed", "fish"},
    "ovo_lacto":     {"meat_red", "meat_white", "meat_processed", "fish"},
    "vegan":         {"meat_red", "meat_white", "meat_processed", "fish", "dairy", "egg"},
}
```

---

## Repo layout (mirrors `/code/rb`)

```
/code/diet/
  diet/
    __init__.py
    cli.py              # discover, ingest, solve, export, validate, all
    sources/
      kroger.py         # OAuth2 client + product search/lookup + cache
      fdc.py            # USDA FoodData Central client + cache
    foods.py            # join skus.yaml + FDC nutrients + Kroger prices
    targets.py          # load DRI targets per profile
    solver.py           # build + solve LP per (mode × location)
    discover.py         # discovery pass — Kroger search & SKU candidates
    export.py           # write site/data.json
  data/
    discovery_terms.yaml      # ~40 staple search terms
    sku_candidates.yaml       # written by `discover`, hand-edited
    skus.yaml                 # the curated ~80, with fdc_id + unit_grams
    locations.yaml            # 3 Kroger locationIds: { west, midwest, south }
    dri.json                  # vendored RDAs/ULs
    prices_current.json       # written by `ingest`
    raw/
      kroger/<date>/          # cached daily responses
      fdc/                    # cached nutrient lookups (FDC ID -> nutrients)
  site/
    data.json                 # the published artifact (committed)
  sources/                    # research corpus (already populated)
  tests/
  .github/workflows/
    publish.yml               # daily cron → ingest → solve → commit
  pyproject.toml
  README.md
```

Mirror `/code/rb`'s conventions: `uv` for env, `cli.py` with subcommands, atomic writes,
cached raw data under `data/raw/`.

---

## CLI

```sh
diet discover              # one-off: search Kroger by terms → sku_candidates.yaml
diet ingest                # daily: refresh prices for skus.yaml × locations.yaml
diet solve                 # solve LP per (mode × location) → reports/solutions.json
diet export                # write site/data.json
diet validate              # sanity: every SKU has price, nutrients; mode feasibility
diet all                   # ingest → solve → export (the CI command)
```

---

## GitHub Action

`.github/workflows/publish.yml` — modeled on `/code/rb/.github/workflows/publish.yml`:

- Trigger: `schedule: cron: "0 13 * * *"` (13:00 UTC = 09:00 ET, after Kroger has
  rolled overnight pricing) + `workflow_dispatch`.
- Python 3.13 + `uv sync --locked`.
- Secrets: `KROGER_CLIENT_ID`, `KROGER_CLIENT_SECRET`, `FDC_API_KEY`.
- Run: `diet all`.
- Commit `site/data.json` only if `git diff --cached --quiet` returns non-zero (skips
  no-op days when prices haven't moved).
- Serve via `cdn.jsdelivr.net/gh/<user>/diet@main/site/data.json` like `cpudata` (no
  Cloudflare deploy step needed).

Light: whole job is well under 60 s. ~6 Kroger calls + cached FDC lookups + LP solve
+ one git commit.

---

## Website page

New static page at `/code/website/diet/index.html`, linked from the website index.
Same architecture as `/code/website/cpudata/index.html`:

```js
const CDN = 'https://cdn.jsdelivr.net/gh/<user>/diet@main/site';
fetch(`${CDN}/data.json`).then(r => r.json()).then(render);
```

UI:
- Header + one-line tagline.
- Two pill rows:
  - Mode: `omnivore | pescatarian | vegetarian | ovo-lacto | vegan`.
  - Location: `west | midwest | south` (store name + city shown beneath).
- Daily cost + "last updated" timestamp + "store" line ("Kroger #01400441 — Cincinnati,
  OH").
- Basket table: SKU name (link to product page via `productPageURI`), grams/day,
  $/unit, cost/day, % of basket. `tabular-nums`, right-aligned numbers.
- Nutrient delivery table: nutrient, RDA, delivered, status (binding / slack), shadow
  price ($/unit-of-nutrient).
- Infeasibility banner if a mode/location combo can't hit RDAs.
- Footer: data provenance, link to GitHub repo, Kroger attribution per their ToS.

### Style — strict adherence to `/code/cuminte/styles/based.md`

- Background `#040506`, surface `#0e0e10`, text `#e0e0e0` / `#b6aa99`.
- Single accent: `#ff9800` for the active pill, binding-constraint highlight, section
  rules.
- D2Coding everywhere (already loaded site-wide via `/D2CodingLigature.ttf`).
- `max-width: 760px`, centered, `padding: 0 24px`. 8 px spacing unit.
- `border-radius: 6px`, no shadows, borders do separation.
- Numeric columns: `font-variant-numeric: tabular-nums`, right-aligned, weight 700.
- Section headings: 1.1em, uppercase, `letter-spacing: 0.1em`, orange.
- Hover on rows: shift to `#0e0e10`. Focus: `box-shadow: 0 0 0 3px rgba(255,152,0,0.2)`.
- Fade-in on load, staggered. No other motion.
- No charts in v1 — the table *is* the visualization.

---

## What "modern" means here, vs Stigler 1945

| | 1945 | this |
|---|---|---|
| Solver | hand heuristic, off by $0.24/yr | HiGHS, exact, sub-second |
| Foods | 77, US 1939 | ~80 real Kroger SKUs |
| Nutrients | 9 | ~15 (incl. fiber, omega-3 ALA, B12, vit D) |
| Targets | NRC 1943 | NIH ODS DRIs, current |
| Cost | $39.93/yr (1939 $) | $/day at a real store, today |
| Constraints | nutrient floors only | floors + ULs + mode + palatability cap |
| Diet modes | none | 5 |
| Locations | none | 3 (v1), expandable |
| Output | a number | basket + shadow prices + nutrient slack, per (mode × loc) |
| Cadence | one-shot | true daily |

Genuinely new vs the literature:
- *Shadow price per binding nutrient* as first-class output ("the cheapest extra mcg of
  B12 in this basket would cost $X").
- *Actual shoppable SKUs at a named store* — falsifiable, not an abstraction.
- *Daily delta* — promo cycles become visible; you can see vegan being cheaper or more
  expensive than omnivore on a given Tuesday.

---

## Honest limits to disclose on the page

- Kroger only. If you don't shop there, this isn't your basket.
- Optimal ≠ palatable. The cap is a hack; 500 g/day of cabbage is allowed.
- Single adult profile in v1.
- Doesn't account for cooking, waste, bioavailability, or food synergies.
- Vegan B12 requires a fortified SKU in `skus.yaml` (Kroger sells fortified soy milk,
  nutritional yeast). If we omit it, vegan returns infeasible — we surface that
  honestly rather than hiding it.
- Promo prices may be loyalty-card-gated; we use the promo price the API returns,
  which may not be the price a shopper without a card actually pays.

---

## Phasing

- **v1 (2–3 days work):** discovery, ~80 SKUs, 3 Kroger locations, 5 modes, daily cron,
  page on website.
- **v2:** more locations (configurable from `locations.yaml`), more body profiles,
  EAT–Lancet overlay column, "what you'd save vs an unconstrained shopper" stat.
- **v3:** GHG/water as a second objective (ε-constraint method); palatability bounds
  per food; "show me three baskets near the optimum"; Open Prices EU tier.

---

## Open questions

- **Repo layout:** standalone `diet` repo (so jsDelivr can serve `data.json`), or live
  inside an existing one? Standalone matches `cpudata` pattern — recommend that.
- **Location selection:** which three Kroger locationIds to seed? Suggest a flagship in
  Cincinnati (Kroger HQ region), one in California (Ralphs), one in Texas — covers
  supply-chain and regional pricing variance. To be picked during discovery.
- **Promo handling:** always use promo when present? Or report both `cost_regular` and
  `cost_promo` so the page can show "today's deal vs sticker" diff? Recommend the
  latter — it's the only honest way to surface what daily means.
- **Kroger ToS attribution:** confirm the exact text/badge required on a public page
  using their data; bake into footer.
