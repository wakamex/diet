"""Write `site/data.json` from a list of solved (mode × location) solutions."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from diet.foods import load_locations, load_prices, load_skus
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


def _build_catalog() -> tuple[list[dict], list[dict]]:
    """Build the all-SKUs-with-per-location-prices catalog for the page.

    Returns (catalog, locations). Each catalog row has:
      product_id, name, kind ("food" or "supplement"), dietary_categories,
      unit_display (e.g. "16 oz (454g)" or "240 tab"),
      prices_by_region: {region: {regular, promo, effective} | null}
    """
    skus = load_skus()
    supps = load_supplements(DEFAULT_SUPPLEMENTS_PATH) if DEFAULT_SUPPLEMENTS_PATH.exists() else []
    locations = load_locations()
    prices = load_prices() if DEFAULT_PRICES_PATH.exists() else {}

    loc_payload = [{"region": l.region, "location_id": l.location_id,
                    "display": l.display} for l in locations]

    catalog: list[dict] = []

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
                    "regular": regular, "promo": promo,
                    "effective": effective,
                }
        catalog.append({
            "product_id": sku.product_id,
            "name": sku.name,
            "kind": "food",
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
                    "regular": regular, "promo": promo,
                    "effective": effective,
                }
        catalog.append({
            "product_id": s.product_id,
            "name": s.name,
            "kind": "supplement",
            "dietary_categories": sorted(s.dietary_categories),
            "unit_grams": round(s.unit_grams, 1),
            "tablet_g": s.tablet_g,
            "count": s.count,
            "max_tablets_per_day": s.max_tablets_per_day,
            "prices_by_region": prices_by_region,
        })

    # Stable sort: foods before supplements, then by first category then by name.
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
