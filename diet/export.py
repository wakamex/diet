"""Write `site/data.json` from a list of solved (mode × location) solutions."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from diet.foods import load_all_skus, load_locations, load_prices
from diet.solver import NutrientTarget, Solution
from diet.supplements import load_supplements
from diet.targets import load_targets
from diet.util import write_json_atomic

DEFAULT_OUT_PATH = Path("site/data.json")
DEFAULT_SUPPLEMENTS_PATH = Path("data/supplements.yaml")
DEFAULT_PRICES_PATH = Path("data/prices_current.json")


def serialize_solution(s: Solution, *, mode: str, location_region: str,
                       location_display: str) -> dict:
    return {
        "mode": mode,
        "location_region": location_region,
        "location_display": location_display,
        "status": s.status,
        "message": s.message,
        "cost_per_day": s.cost_per_day,
        "basket": s.basket,
        "nutrients": s.nutrients,
        "diagnosis": s.diagnosis,
    }


_BRAND_PREFIXES = (
    "kroger®", "kroger", "simple truth organic®", "simple truth organic",
    "simple truth™", "simple truth®", "simple truth", "private selection™",
    "private selection®", "private selection", "heritage farm®", "heritage farm",
    "great value", "freshness guaranteed", "foster farms", "starkist",
    "chicken of the sea", "deming's", "snow's®", "snow's", "skylark®", "skylark",
    "butcher's prime", "grace®", "grace", "quaker®", "quaker", "kretschmer®",
    "kretschmer", "morrell", "john morrell®", "maizena®", "maizena",
    "grandma's®", "grandma's", "wyman's®", "wyman's", "manitoba harvest®",
    "manitoba harvest", "silk®", "silk", "planet oat®", "planet oat",
    "almond breeze", "bob's red mill", "general mills", "post",
    "la preferida®", "la preferida", "bush's", "del monte", "tropicana",
    "libby's", "goya®", "goya", "carnation", "nestle", "pet®", "pet",
    "spring valley", "equate®", "equate", "nature made®", "nature made",
    "nature's bounty", "kroger's®",
)


def _strip_brand(name: str) -> str:
    """Drop a leading brand prefix and trailing trademark/size noise so two
    different store-brand SKUs of the same food collapse to the same display
    name. Order of prefix list matters — longer/more-specific entries first."""
    s = (name or "").strip()
    low = s.lower()
    # repeatedly strip leading brand prefixes (some names have stacked brands)
    changed = True
    while changed:
        changed = False
        for p in _BRAND_PREFIXES:
            if low.startswith(p + " "):
                s = s[len(p):].lstrip(" ®™()-:,")
                low = s.lower()
                changed = True
                break
    return s.strip(" ®™") or name


def _merge_prices(rows: list[dict], regions: list[str]) -> dict:
    """Cell-level merge: for each region, take the first non-null price across
    the input rows. In practice each region only has prices from one source
    (Kroger regions vs walmart_national), so this is a non-overlapping union."""
    out: dict = {}
    for r in regions:
        out[r] = None
        for row in rows:
            v = row.get("prices_by_region", {}).get(r)
            if v is not None:
                out[r] = v
                break
    return out


def _build_catalog() -> tuple[list[dict], list[dict]]:
    """Build the catalog. SKUs sharing a food concept (same fdc_id for foods,
    same supplement category for pills) merge into one row whose
    prices_by_region spans every chain that carries that concept.
    """
    skus = load_all_skus()
    supps = load_supplements(DEFAULT_SUPPLEMENTS_PATH) if DEFAULT_SUPPLEMENTS_PATH.exists() else []
    locations = load_locations()
    prices = load_prices() if DEFAULT_PRICES_PATH.exists() else {}

    loc_payload = [{"region": l.region, "location_id": l.location_id,
                    "display": l.display} for l in locations]
    region_keys = [l.region for l in locations]

    # First, build per-SKU rows with prices_by_region.
    raw: list[dict] = []
    for sku in skus:
        prices_by_region: dict = {}
        for loc in locations:
            row = prices.get((sku.product_id, loc.location_id))
            if row is None:
                prices_by_region[loc.region] = None
            else:
                regular = row.get("regular")
                promo = row.get("promo")
                effective = promo if (promo and promo > 0) else regular
                prices_by_region[loc.region] = {
                    "regular": regular, "promo": promo, "effective": effective,
                }
        raw.append({
            "product_id": sku.product_id,
            "name": sku.name,
            "kind": "food",
            "source": sku.source,
            "fdc_id": sku.fdc_id,
            "dietary_categories": sorted(sku.dietary_categories),
            "unit_grams": round(sku.unit_grams, 1),
            "prices_by_region": prices_by_region,
        })
    for s in supps:
        prices_by_region = {}
        for loc in locations:
            row = prices.get((s.product_id, loc.location_id))
            if row is None:
                prices_by_region[loc.region] = None
            else:
                regular = row.get("regular")
                promo = row.get("promo")
                effective = promo if (promo and promo > 0) else regular
                prices_by_region[loc.region] = {
                    "regular": regular, "promo": promo, "effective": effective,
                }
        raw.append({
            "product_id": s.product_id,
            "name": s.name,
            "kind": "supplement",
            "source": s.source,
            "fdc_id": 0,
            "dietary_categories": sorted(s.dietary_categories),
            "unit_grams": round(s.unit_grams, 1),
            "tablet_g": s.tablet_g,
            "count": s.count,
            "max_tablets_per_day": s.max_tablets_per_day,
            "prices_by_region": prices_by_region,
        })

    # Group into food concepts. Foods share an fdc_id (Walmart bootstrap reused
    # the Kroger SKU's fdc_id, so cross-chain pairs match). Supplements share
    # the non-`supplement` part of their dietary_categories tuple
    # (multivitamin / b12 / calcium / omega_3).
    def dedupe_key(r: dict) -> tuple:
        if r["kind"] == "food":
            return ("food", r["fdc_id"])
        non_supp = tuple(c for c in r["dietary_categories"] if c != "supplement")
        return ("supplement", non_supp or (r["product_id"],))

    groups: dict[tuple, list[dict]] = {}
    for r in raw:
        groups.setdefault(dedupe_key(r), []).append(r)

    catalog: list[dict] = []
    for key, members in groups.items():
        # Kroger first (more descriptive names), then Walmart.
        members.sort(key=lambda r: (r["source"] != "kroger", r["name"].lower()))
        primary = members[0]
        display_name = _strip_brand(primary["name"])
        catalog.append({
            "name": display_name,
            "kind": primary["kind"],
            "fdc_id": primary["fdc_id"],
            "dietary_categories": sorted({c for r in members for c in r["dietary_categories"]}),
            "unit_grams": primary["unit_grams"],
            **({"tablet_g": primary["tablet_g"], "count": primary["count"],
                "max_tablets_per_day": primary["max_tablets_per_day"]}
               if primary["kind"] == "supplement" else {}),
            "prices_by_region": _merge_prices(members, region_keys),
            "variants": [
                {"source": m["source"], "product_id": m["product_id"],
                 "name": m["name"], "unit_grams": m["unit_grams"]}
                for m in members
            ],
        })

    catalog.sort(key=lambda c: (c["kind"] == "supplement",
                                (c["dietary_categories"] or [""])[0],
                                c["name"].lower()))
    return catalog, loc_payload


def write_data_json(
    solutions: list[dict],
    *,
    targets: list[NutrientTarget] | None = None,
    out_path: Path | str = DEFAULT_OUT_PATH,
    profile: str = "adult_male_31_50_moderate",
) -> Path:
    targets = targets or load_targets()
    catalog, locations = _build_catalog()
    payload = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "profile": profile,
        "nutrient_targets": [
            {"nutrient": t.nutrient, "rda": t.rda, "ul": t.ul,
             "unit": t.unit, "label": t.label or t.nutrient}
            for t in targets
        ],
        "locations": locations,
        "catalog": catalog,
        "solutions": solutions,
    }
    out = Path(out_path)
    write_json_atomic(out, payload)
    return out
