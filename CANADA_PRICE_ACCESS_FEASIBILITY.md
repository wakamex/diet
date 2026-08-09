# Canada grocery-price access: feasibility and proposed design

Status: Metro/Food Basics and PC Express reference venues integrated into daily optimizer/site
Target geography: Ottawa, Ontario
Retailers: Loblaws, Real Canadian Superstore, No Frills, Metro, Food Basics, Farm Boy, Costco
Observed: 2026-08-08

## Implemented PC Express surface

The first phase is implemented in
[`diet/sources/pc_express.py`](diet/sources/pc_express.py). It exposes normalized
store lookup, product search, and exact-LIAM quote matching. It deliberately
does not expose PC Express's add, remove, update, or clear-cart tools.

```sh
# Nearby stores, normalized as JSON
uv run diet pcx stores "K1S 5B6" --json

# Products and effective prices at an explicitly selected store
uv run diet pcx search "long grain rice" \
  --store-id 1009 --banner superstore --postal-code "K1S 5B6" --json

# Fail unless the curated LIAM is present in the search response
uv run diet pcx search "long grain rice" \
  --store-id 1009 --banner superstore --postal-code "K1S 5B6" \
  --product-id 20069589_EA --json
```

The client returns effective package price and stock state. Package size must
still be verified and stored in curated SKU metadata before a quote can affect
the solver.

Superstore and No Frills are connected to the optimizer through explicit banner
reference stores, rather than through an ambiguous storeless quote. Inspection
of each storefront's loaded app configuration found that `defaultStoreId`,
`masterStoreId`, and `highAssortmentStoreId` currently agree:

| Banner | Configured store ID | Reference store |
| --- | --- | --- |
| Real Canadian Superstore | `1033` | Dufferin & Steeles, 51 Gerry Fitzgerald Dr, Toronto |
| No Frills | `3787` | Chris & Tanya's, 680 O'Brien Rd, Renfrew |

Those IDs are declared in `data/locations.yaml`, passed explicitly on every MCP
product search, and persisted with the raw response and normalized price. They
are useful stable banner references, not national averages, chain minima, or
Ottawa prices. Curated exact LIAMs cover the inexpensive staples needed to
produce feasible baskets plus three Canadian-label Jamieson supplements.

## Implemented Metro and Food Basics reference surface

[`diet/sources/metro_reference.py`](diet/sources/metro_reference.py) implements
the common exact-SKU storefront contract used by both Metro Inc. banners. The
hosts and paths differ, but both accept a JSON `productIds` array and return HTML
product tiles. The client normalizes package, effective price, regular/promo
split, unit price, weighted-item status, source URL, and observation time.

```sh
# One exact Metro UPC
uv run diet canada-reference metro 059749930031 --json

# Batch exact Food Basics UPCs
uv run diet canada-reference foodbasics 055270846452 739907000010 --json
```

The endpoint has no store identity and does not calculate a chain-wide minimum.
Every result is therefore marked `price_scope: reference` and
`channel: online_catalog`. Missing requested UPCs are reported explicitly, and
the CLI exits nonzero if any are missing. This surface is useful for approximate
optimizer inputs and retailer comparisons, but it is not an Ottawa-store quote.

### Main-site integration

Metro Reference and Food Basics Reference are first-class daily locations in
`data/locations.yaml`. The initial discovery pass queried all 85 existing food
concepts at both banners. Curated exact mappings cover 73 concepts at Metro and
75 at Food Basics; `data/canada_missing.yaml` accounts explicitly for every
remaining concept/retailer pair. Both also have an exact Jamieson B12 SKU for the
food-plus-pills universe.

The daily ingest uses batches of at most 20 UPCs because a large-request
counterfactual showed that the storefront silently truncates results. A missing
batch result falls back to the ranked autocomplete surface using the curated
query, then accepts only the exact expected UPC. Expected package labels are
checked before promotion. Weighted products use the storefront's per-kilogram
price, while every volume-to-mass estimate is recorded in the curated mapping.

Solutions remain in native CAD. The site additionally shows a USD comparison
using the latest daily `FXUSDCAD` observation from the Bank of Canada Valet API;
the FX rate and date are persisted in `data/fx_current.json`. A uniform exchange
rate cannot change the LP basket. Failed Canadian refreshes retain the last good
quote with its original price date and a visible stale marker.

`All Canada Reference` is a derived fifth optimizer view over the four Canadian
reference venues. It does not ingest or manufacture prices: each food and
supplement retains the member chain and concrete quote it came from, and the LP
may mix retailers to minimize total daily cost. Identical physical supplements
are collapsed to their cheapest chain quote so duplicate retailer listings
cannot multiply a label dosage cap. The view is explicitly a multi-stop
mathematical basket, not a basket available from one store.

## Decision

We can build a useful API-equivalent price service for this project, but we
cannot honestly promise one uniform, complete feed for all six retailers.

The defensible scope is a **curated-SKU quote service**, not a daily scrape of
every retailer's full catalog:

- Loblaws, Superstore, and No Frills can share one PC Express connector. A
  first-party PC Express MCP endpoint currently provides Ottawa store lookup and
  product search with item IDs, current effective prices, and stock status.
- Metro and Food Basics share a batch exact-SKU storefront pattern that exposes
  package description, regular/sale price, unit price, URL, and image in
  server-rendered HTML. It is implemented as an explicitly unlocalized
  reference-price source. Store selection still must be used and proven before
  calling either banner's result an Ottawa price.
- Farm Boy does not publish a full Ottawa store catalog. Its official site says
  Farm Boy stores do not offer delivery and points users to Voilà for a subset of
  Farm Boy private-label products. That is not the same thing as Farm Boy store
  pricing.
- Costco Same-Day exposes a shoppable delivery catalog, but it is powered by
  Instacart, carries a markup over warehouse prices, and Instacart expressly
  prohibits unapproved scraping. Costco warehouse prices therefore require an
  approved feed or receipt/price-tag observations; Same-Day prices require
  approved Instacart developer access.

The client layer covers PC Express local store lookup, two explicit PC Express
banner references, and Metro/Food Basics catalog references. Exact Farm Boy and Costco
**in-store** coverage is not currently feasible through a supported public API.

## What “price” means

Every quote must carry a channel. These are different economic quantities and
must never be silently mixed:

| Channel | Meaning |
| --- | --- |
| `pickup` | Price quoted for an order collected from a named store |
| `retailer_delivery` | Price on a retailer-operated delivery storefront |
| `marketplace_delivery` | Price on Instacart or another marketplace; may include item markup |
| `warehouse` | Physical shelf/register price, especially important for Costco |
| `flyer` | Advertised promotion only; absence does not imply that an item is unavailable |
| `receipt` | Price actually paid at a store and time |

The diet solver can compare sources only within a declared universe. A sensible
Ottawa default would be `pickup` plus `retailer_delivery`. Costco Same-Day could
be a separate location/channel; it must not be labelled “Costco warehouse.”

## Retailer-by-retailer assessment

Difficulty is implementation and maintenance difficulty on a 1–5 scale. Policy
risk is separate from technical difficulty.

| Retailer | Proposed source | Technical feasibility | Difficulty | Main limitation |
| --- | --- | ---: | ---: | --- |
| Loblaws | PC Express first-party MCP | High for curated SKUs | 2/5 | Package size and regular-vs-promo split are absent |
| Superstore | Same PC Express connector | High for curated SKUs | 2/5 | Same limitation |
| No Frills | Same PC Express connector | High for curated SKUs | 2/5 | Same limitation |
| Metro | Internal exact-SKU storefront endpoint | High for reference prices | 2/5 | Unlocalized; not a minimum or store quote |
| Food Basics | Same Metro Inc. endpoint pattern | High for reference prices | 2/5 | Unlocalized; not a minimum or store quote |
| Farm Boy | Official flyer plus receipt/Open Prices fallback | Low for regular catalog; medium for promos | 4/5 | No full Ottawa online store catalog |
| Costco | Approved Instacart access for Same-Day; receipts for warehouse | Medium for delivery, low for warehouse | 4/5–5/5 | Marketplace markup, approval, and no supported warehouse feed |

### PC Express: Loblaws, Superstore, and No Frills

The best discovery is a first-party endpoint at
[`https://api.pcexpress.ca/v1/agents/mcp`](https://api.pcexpress.ca/v1/agents/mcp).
It is an MCP Streamable HTTP server. A direct, unauthenticated protocol probe on
2026-08-05 returned `PCExpressMCPServer` version `3.4.2` and advertised these
relevant tools:

- `search_for_stores(postal_code)`
- `search_for_products(store_id, banner, term, postal_code, ...)`

The store lookup returned real Ottawa IDs for all three requested banners,
including Superstore Richmond Road (`1009`), Loblaws Isabella Street (`1095`),
and No Frills Alta Vista (`8999`). A product lookup at store `1009` returned a
stable LIAM item identifier, name, brand, current price, image, and stock state.
For example, `20069589_EA` was returned as No Name Long Grain White Rice at
`$5.00`.

This is materially better than copying a browser API key from PC Express's older
private product endpoint. It is first-party, is explicitly shaped for agent
access, supports named locations, and requires no customer credential. However,
it is not yet documented on a public PC Express developer page, so “publicly
reachable” should not be equated with permission for bulk collection or
redistribution. Loblaw's general site terms limit use to personal,
non-commercial use and restrict copying site material for commercial use
([Loblaw legal terms](https://www.loblaw.ca/en/legal/)). We should ask Loblaw for
written confirmation before making scheduled collection or raw quote
redistribution a public service.

There are also data-shape limitations:

- The MCP result gives an effective price, not separate regular and promo
  prices.
- It does not include package size or unit price.
- Search creates or retrieves an anonymous cart and returns its ID, even though
  it does not add products to the cart.
- Search ranking is not an exact-ID lookup, so the connector must match the
  returned LIAM against a curated mapping instead of trusting the first result.

For this repository those limitations are manageable. Package size is stable
metadata that can be manually verified when a SKU is curated, while the daily
job needs only LIAM, price, and stock. Reject a quote if the expected LIAM is not
in the response.

Protocol probe, reproducible without credentials:

```sh
curl -sS \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  --data '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' \
  https://api.pcexpress.ca/v1/agents/mcp
```

Use a truthful project user-agent, make a small number of requests, cache raw
responses, and never invoke the cart mutation tools.

### Metro and Food Basics

Metro has no documented consumer product-price API, but both Metro and Food
Basics expose an internal read-only endpoint used by their storefronts:

- `POST https://www.metro.ca/en/online-grocery/product/skus`
- `POST https://www.foodbasics.ca/product/skus`
- JSON body: `{"productIds":["059749930031"]}`

Both return server-rendered HTML product tiles rather than JSON. Live
counterfactuals showed that the endpoint ignores a selected favourite-store
session: Metro returned the same implicit price while the store-specific search
surface returned different prices at different Ottawa stores. The implementation
therefore deliberately calls these **Metro Reference** and **Food Basics
Reference**, never local or national prices.

For a local-price adapter, use the separate store flow: enumerate stores, select
one in an anonymous session, call the banner's `autocompleteSearchProducts`
surface with a curated query, and accept only the exact expected UPC. A controlled
test found Metro black beans at `$1.99` at Merivale and `$1.69` at Glebe, and Food
Basics chickpea flour at `$7.49` at Kirkwood and `$6.49` at Heron. Those results
falsify any assumption that a single implicit quote represents every store.

Metro's `robots.txt` allows product detail URLs but disallows parameterized
search/filter URLs. Its terms limit the site to personal, non-commercial use and
prohibit unauthorized reproduction of site content
([website terms](https://www.metro.ca/en/terms-of-use),
[e-commerce terms](https://www.metro.ca/en/online-grocery-policy)). A public,
scheduled data product should therefore get written permission. Technical
access alone is not sufficient authorization.

### Farm Boy

Farm Boy is the weakest target for regular prices. Its official customer-care
page says it does not offer delivery from Farm Boy stores and instead points to
Voilà, which carries hundreds of Farm Boy private-label products in some Ontario
regions ([Farm Boy delivery FAQ](https://www.farmboy.ca/contact-us/)). A Farm Boy
store page may link to Voilà, but a Voilà SKU is a Voilà delivery quote—not a
quote from the nearby Farm Boy store
([Train Yards example](https://www.farmboy.ca/stores/train-yards/)).

Supported options are therefore:

- Parse Farm Boy's own weekly flyer for promotion discovery. This is incomplete
  by definition and should use the `flyer` channel.
- Collect Ottawa receipt or price-tag observations for the fixed high-value SKU
  list.
- Ask Farm Boy/Empire for a product feed.
- Use Voilà only when the intended universe is Voilà delivery and preserve that
  banner/channel honestly.

Do not manufacture regular Farm Boy prices from the last observed sale or from
another Empire banner.

### Costco

There are three different Costco price surfaces:

1. `costco.ca` shipped products: incomplete grocery assortment and online price.
2. Costco Same-Day: a local delivery assortment powered by Instacart.
3. The physical warehouse: the member shelf/register price.

Costco explicitly says Same-Day item prices are marked up above the local
warehouse price
([Costco Same-Day help](https://www.costco.ca/f/-/sameday-grocery-help?langId=-24)).
Therefore Same-Day is usable only as `marketplace_delivery`, not as a proxy for
warehouse cost.

Scraping Same-Day is not a defensible route. Instacart's current terms prohibit
scraping, crawling, data mining, reverse engineering storefront behavior, and
unapproved automated access
([Instacart terms](https://www.instacart.com/terms.aspx)). Its official Developer
Platform does support Canada, nearby-retailer lookup, and shopping integrations,
but the default public product endpoint generates an Instacart-hosted shopping
page rather than returning the matched catalog and prices to the caller. The
official FAQ explicitly says public API developers cannot access Instacart data
([Developer Platform overview and FAQ](https://company.instacart.com/business/developers)).

Applying for advanced/partner access is still worthwhile. Instacart describes
real-time inventory and pricing as a supported developer use case, but access is
scoped and approval-dependent; its documentation estimates roughly 30–40 days
from access request to demo approval and a production key
([getting started](https://docs.instacart.com/developer_platform_api/get_started/overview)).
The application should explicitly ask whether item-level search results and
prices may be stored, used in optimization, and displayed publicly. Without
that grant, the official API is useful for checkout links but not for this
price-ingestion pipeline.

For warehouse prices, the practical supported fallback is receipt/price-tag
collection. Costco item numbers can be mapped to curated foods, but observed
prices must retain warehouse ID and date.

## Third-party and open alternatives

### Open Prices

[Open Prices](https://prices.openfoodfacts.org/api/docs) is the best lawful
fallback for receipt and price-tag observations. It exposes products, locations,
prices, proofs, and receipt items through an open API. Contributors are asked to
attach a receipt or price-tag photo as evidence
([Open Food Facts price documentation](https://openfoodfacts.github.io/openfoodfacts-server/api/tutorials/product-prices/)).
The data is ODbL, so attribution, share-alike obligations for a derived database,
and contribution rules must be reviewed before mixing it into this repository.

Coverage in Ottawa is likely sparse, so it is a collection mechanism rather than
a ready-made complete feed. It is especially appropriate for Farm Boy and Costco
warehouse observations that have no supported online equivalent.

### GroceryPulse

[GroceryPulse](https://www.grocerypulse.ca/api/docs) already offers a commercial
Canadian price API with Ottawa and all requested banners except Costco. It is a
useful benchmark or validation source, not a drop-in solution for the diet
solver: its price panel covers a fixed 50-item basket, is weekly, excludes
Costco, and licenses per-item observations for internal use unless redistribution
is negotiated.

### Flyers and Flipp

Flyers are useful for sale discovery but cannot support a cheapest-basket solver
by themselves because non-promoted items disappear. Unofficial Flipp endpoints
would also introduce another private interface and another set of terms. Prefer
the retailer's own flyer where available, store the validity interval, and label
the quote `flyer`.

### Commercial “scraping APIs”

These services can hide Cloudflare and browser maintenance, but they do not grant
rights to collect or redistribute retailer data. They also add cost, supply-chain
surface, and an opaque dependency. They should not be the default architecture.

## Proposed API-equivalent interface

Normalize all sources behind a small quote interface. Search is for curation;
exact tracked IDs are for recurring ingestion.

```python
class CanadianPriceSource(Protocol):
    def stores(self, postal_code: str) -> list[Store]: ...
    def discover(self, store: Store, term: str) -> list[ProductCandidate]: ...
    def quote(self, store: Store, tracked: list[TrackedSku]) -> list[PriceQuote]: ...
```

Minimum normalized quote:

```json
{
  "source": "pc_express_mcp",
  "retailer": "superstore",
  "store_id": "1009",
  "store_name": "Real Canadian Superstore Richmond Road",
  "channel": "pickup",
  "product_id": "20069589_EA",
  "upc": null,
  "name": "Long Grain White Rice",
  "brand": "No Name",
  "package_quantity": 2,
  "package_unit": "kg",
  "regular_price_cad": null,
  "promo_price_cad": null,
  "effective_price_cad": 5.0,
  "in_stock": true,
  "observed_at": "2026-08-05T00:00:00-04:00",
  "source_url": "https://api.pcexpress.ca/v1/agents/mcp",
  "raw_sha256": "..."
}
```

`effective_price_cad` is mandatory. Regular and promo may be null when a source
does not distinguish them. Package quantity and unit come from separately
verified curated metadata when the live source omits them.

## Repository shape

An incremental implementation can fit the existing source-client design:

```text
diet/sources/ca/
  base.py              normalized Store, TrackedSku, and PriceQuote
  pc_express_mcp.py    first-party MCP adapter
  metro_pages.py       known-page parser
  open_prices.py       receipt/price-tag fallback
data/
  locations.yaml
  canada_product_map.yaml
  canada_missing.yaml
  prices_current.json
  fx_current.json
  raw/metro_reference/YYYY-MM-DD/<retailer>.json
```

No browser automation is required for the PC Express or Metro Inc. connectors.
Use the standard-library HTTP layer already present in this project, bounded
timeouts, a truthful user-agent, retries with jitter, and source-specific rate
limits. Avoid adding Playwright, Selenium, rotating proxies, CAPTCHA services,
or copied mobile-app credentials.

Each tracked SKU should record:

- source and banner
- immutable source product ID (LIAM, SKU, UPC, or Costco item number)
- expected normalized name and brand
- package quantity and unit, with evidence URL/date
- allowed store IDs and channel
- last successful response hash
- whether the quote can be displayed publicly under the source's permission or
  licence

Discovery can run manually or quarterly. Daily/weekly ingestion should quote
only the curated list. This makes load, breakage, and accidental product
substitution much smaller than a catalog crawler.

## Validation and promotion gates

Before any connector affects optimizer output:

1. **Identity:** Returned product ID must exactly match the curated ID. Search
   rank alone is never sufficient.
2. **Package:** Manually verify package quantity for every new ID. Quarantine a
   changed package rather than silently changing price per gram.
3. **Location/scope:** For a local quote, persist store ID, banner, channel,
   postal code, and the store name actually returned/rendered. For an
   unlocalized quote, persist `price_scope: reference` and never manufacture a
   store identity.
4. **Price counterfactual:** Compare at least 20 quotes with the consumer
   storefront on the same date. Include a sale, an out-of-stock product, and a
   weighted item.
5. **Metro Inc. store test:** The exact-SKU endpoint failed the two-store
   counterfactual and is permanently classified as reference scope. Any future
   local adapter must independently prove the selected store in fresh sessions.
6. **Channel test:** For Costco, compare Same-Day and a same-day warehouse receipt
   and verify they remain separate records.
7. **Raw evidence:** Save the exact response, retrieval time, effective loaded
   configuration, parser version, and SHA-256 hash.
8. **Failure behavior:** Stale or structurally changed data must retain the last
   good quote with a visible age; it must not become zero, disappear silently, or
   trigger automatic SKU replacement.

## Effort estimate

For one developer familiar with this repository:

| Work | Estimate | External gate |
| --- | ---: | --- |
| PC Express proof, adapter, and two reference venues | Implemented | Clarify permitted scheduled/public use |
| Metro/Food Basics reference parser | Implemented | Clarify permitted scheduled/public use |
| Metro location counterfactual and hardening | 2–3 days | Must prove store attribution |
| Canadian normalized schema and ingest integration | Implemented | None |
| Open Prices receipt workflow | 2–3 days | ODbL design review |
| Tests, fixtures, daily workflow, and site labels | Implemented | None |
| Instacart production integration | engineering is modest | Approximately 30–40 days approval path |
| Farm Boy or Costco first-party feed | unknown | Retailer agreement required |

The Metro Inc. path and the Superstore/No Frills reference-store paths are
implemented through the main site. Six-banner delivery and warehouse coverage
remains an external-data partnership project, not merely a scraping task.

## Recommended sequence

1. Ask Loblaw whether the PC Express MCP endpoint may be used for a low-rate,
   non-commercial daily price optimizer and whether effective prices may be
   displayed publicly.
2. Expand the exact PC Express LIAM set only when package size has been
   independently verified; its current MCP search does not provide that field.
3. Build a separate store-selected Metro Inc. adapter only if local quotes are
   required; it must pass a fresh two-store counterfactual.
4. Apply to Instacart for item-level product/price access and explicit storage,
   optimization, and display rights.
5. Use Open Prices receipt proofs for Farm Boy and Costco warehouse items while
   pursuing retailer feeds.

The stop condition is important: if a source cannot prove product identity,
package size, price scope, channel, and observation time, it does not enter the
solver. A store identity is additionally required before a quote may be called
local.
