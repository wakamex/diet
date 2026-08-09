"""Write `site/data.json` from a list of solved (mode × location) solutions."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from diet.foods import (
    Location,
    build_foods_for_location,
    load_all_skus,
    load_locations,
    load_prices,
    price_locations_for,
)
from diet.solver import NutrientTarget, Solution, solve
from diet.supplements import build_supplement_foods, load_supplements
from diet.targets import load_targets
from diet.util import write_json_atomic
from diet.util import read_json

DEFAULT_OUT_PATH = Path("site/data.json")
DEFAULT_SUPPLEMENTS_PATH = Path("data/supplements.yaml")
DEFAULT_PRICES_PATH = Path("data/prices_current.json")
DEFAULT_FX_PATH = Path("data/fx_current.json")
VALUE_REGION = "walmart_national"
VALUE_MODE = "omnivore"
VALUE_VARIANT = "with_supplements"


def load_fx_rates(path: Path | str = DEFAULT_FX_PATH) -> dict[str, dict[str, Any]]:
    rates: dict[str, dict[str, Any]] = {
        "USD": {"currency": "USD", "to_usd": 1.0, "as_of": None}
    }
    path = Path(path)
    if path.exists():
        for currency, row in (read_json(path).get("rates") or {}).items():
            if isinstance(row, dict) and row.get("to_usd") is not None:
                rates[currency.upper()] = row
    return rates


def serialize_solution(
    s: Solution,
    *,
    mode: str,
    location_region: str,
    location_display: str,
    currency: str = "USD",
    price_scope: str = "store",
    fx_rate: dict[str, Any] | None = None,
) -> dict:
    fx_to_usd = float(fx_rate["to_usd"]) if fx_rate else None
    fetched_dates = [
        item.get("meta", {}).get("price_fetched_at")
        for item in s.basket
        if item.get("meta", {}).get("price_fetched_at")
    ]
    has_stale = any(
        item.get("meta", {}).get("price_stale", False) for item in s.basket
    )
    return {
        "mode": mode,
        "location_region": location_region,
        "location_display": location_display,
        "currency": currency,
        "price_scope": price_scope,
        "fx_to_usd": fx_to_usd,
        "fx_as_of": fx_rate.get("as_of") if fx_rate else None,
        "status": s.status,
        "message": s.message,
        "cost_per_day": s.cost_per_day,
        "cost_per_day_usd": (
            s.cost_per_day * fx_to_usd
            if s.cost_per_day is not None and fx_to_usd is not None
            else None
        ),
        "price_as_of": min(fetched_dates) if fetched_dates else None,
        "has_stale_prices": has_stale,
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


def _merge_prices(rows: list[dict], locations: list[Location]) -> dict:
    """Merge concept prices, choosing the best normalized composite quote.

    The selected cell retains the source SKU's package size so Kroger's 5 oz
    yogurt and Walmart's 32 oz tub normalize correctly even on one catalog row.
    """
    out: dict = {}
    for location in locations:
        candidates = [
            (row, row.get("prices_by_region", {}).get(location.region))
            for row in rows
            if row.get("prices_by_region", {}).get(location.region) is not None
        ]
        if not candidates:
            out[location.region] = None
            continue
        if location.member_regions:
            def normalized(candidate):
                row, value = candidate
                package_price = value["effective"]
                divisor = (
                    row.get("count")
                    if row.get("kind") == "supplement"
                    else row.get("unit_grams")
                )
                return package_price / divisor

            row, value = min(candidates, key=normalized)
        else:
            row, value = candidates[0]
        cell = {**value, "unit_grams": row["unit_grams"]}
        if location.member_regions:
            cell["retailer"] = row["source"]
            cell["product_id"] = row["product_id"]
        if row.get("kind") == "supplement":
            cell["count"] = row["count"]
            cell["tablet_g"] = row["tablet_g"]
        out[location.region] = cell
    return out


def _build_catalog(value_scores: dict[str, float] | None = None) -> tuple[list[dict], list[dict]]:
    """Build the catalog. SKUs sharing a food concept (same fdc_id for foods,
    same supplement category for pills) merge into one row whose
    prices_by_region spans every chain that carries that concept.
    """
    value_scores = value_scores or {}
    skus = load_all_skus()
    supps = load_supplements(DEFAULT_SUPPLEMENTS_PATH) if DEFAULT_SUPPLEMENTS_PATH.exists() else []
    locations = load_locations()
    prices = load_prices() if DEFAULT_PRICES_PATH.exists() else {}

    fx_rates = load_fx_rates()
    loc_payload = [{
        "region": l.region,
        "location_id": l.location_id,
        "display": l.display,
        "currency": l.currency,
        "price_scope": l.price_scope,
        "reference_store_name": l.reference_store_name,
        "reference_store_address": l.reference_store_address,
        "reference_store_basis": l.reference_store_basis,
        "member_regions": list(l.member_regions) or None,
        "fx_to_usd": (fx_rates.get(l.currency) or {}).get("to_usd"),
        "fx_as_of": (fx_rates.get(l.currency) or {}).get("as_of"),
    } for l in locations]
    price_locations = {
        location.region: price_locations_for(location, locations)
        for location in locations
    }

    # First, build per-SKU rows with prices_by_region.
    raw: list[dict] = []
    for sku in skus:
        prices_by_region: dict = {}
        for loc in locations:
            price_location = price_locations[loc.region].get(sku.source)
            row = (
                prices.get((sku.product_id, price_location.location_id))
                if price_location else None
            )
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
            "value_score": value_scores.get(sku.product_id),
            "prices_by_region": prices_by_region,
        })
    for s in supps:
        prices_by_region = {}
        for loc in locations:
            price_location = price_locations[loc.region].get(s.source)
            row = (
                prices.get((s.product_id, price_location.location_id))
                if price_location else None
            )
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
            "value_score": value_scores.get(s.product_id),
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
            "value_score": next(
                (m["value_score"] for m in members if m["value_score"] is not None),
                None,
            ),
            "prices_by_region": _merge_prices(members, locations),
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


def _build_value_scores(targets: list[NutrientTarget]) -> dict[str, float]:
    """Score the catalog in one fixed, serving-independent benchmark universe."""
    locations = load_locations()
    location = next((l for l in locations if l.region == VALUE_REGION), None)
    if location is None:
        return {}

    prices = load_prices() if DEFAULT_PRICES_PATH.exists() else {}
    foods = build_foods_for_location(load_all_skus(), location, prices, use_promo=True)
    supplements = (
        load_supplements(DEFAULT_SUPPLEMENTS_PATH)
        if DEFAULT_SUPPLEMENTS_PATH.exists()
        else []
    )
    foods += build_supplement_foods(supplements, location, prices, use_promo=True)
    if not foods:
        return {}

    solution = solve(foods, targets, mode=VALUE_MODE)
    return solution.value_scores if solution.status == "optimal" else {}


def write_data_json(
    solutions: list[dict],
    *,
    targets: list[NutrientTarget] | None = None,
    out_path: Path | str = DEFAULT_OUT_PATH,
    profile: str = "adult_male_31_50_moderate",
) -> Path:
    targets = targets or load_targets()
    value_scores = _build_value_scores(targets)
    catalog, locations = _build_catalog(value_scores)
    payload = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "profile": profile,
        "nutrient_targets": [
            {"nutrient": t.nutrient, "rda": t.rda, "ul": t.ul,
             "unit": t.unit, "label": t.label or t.nutrient}
            for t in targets
        ],
        "locations": locations,
        "value_benchmark": {
            "region": VALUE_REGION,
            "mode": VALUE_MODE,
            "variant": VALUE_VARIANT,
            "label": "Walmart national · omnivore · food + pills",
        },
        "catalog": catalog,
        "solutions": solutions,
    }
    out = Path(out_path)
    write_json_atomic(out, payload)
    return out
