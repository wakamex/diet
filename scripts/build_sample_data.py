#!/usr/bin/env python3
"""Generate sample site/data.json without Kroger or FDC API access.

Synthesizes realistic per-100 g nutrient profiles and Kroger-ish prices for the SKUs
in `data/skus.yaml`, runs the actual solver pipeline, and writes `site/data.json`. The
output is structurally identical to what the daily GitHub Action produces — the website
page can render against it immediately.

Re-run this whenever `data/skus.yaml` or the solver model changes (until the live
ingest takes over).
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from diet.export import serialize_solution, write_data_json  # noqa: E402
from diet.foods import build_foods_for_location, load_locations, load_skus  # noqa: E402
from diet.solver import MODE_EXCLUDES, solve  # noqa: E402
from diet.targets import load_targets  # noqa: E402
from diet.util import write_json_atomic  # noqa: E402

# Per-100 g nutrient profiles, USDA-style. Keys must match the FDC display names that
# diet.sources.fdc.FDC_NUTRIENT_MAP knows about.
NUTRITION_BY_FDC_ID: dict[int, dict[str, float]] = {
    168878: {  # 1% milk
        "Energy": 42, "Protein": 3.4, "Sodium, Na": 47, "Calcium, Ca": 125,
        "Vitamin B-12": 0.42, "Vitamin D (D2 + D3)": 1.2, "Iron, Fe": 0.03,
        "Magnesium, Mg": 11, "Potassium, K": 150, "Vitamin A, RAE": 58,
        "Folate, DFE": 5, "Vitamin C, total ascorbic acid": 0,
        "Zinc, Zn": 0.4, "Vitamin E (alpha-tocopherol)": 0.02,
        "Fiber, total dietary": 0, "PUFA 18:3 n-3 c,c,c (ALA)": 0.01,
    },
    173410: {  # Soy milk fortified
        "Energy": 45, "Protein": 3.0, "Sodium, Na": 38, "Calcium, Ca": 123,
        "Vitamin B-12": 1.2, "Vitamin D (D2 + D3)": 1.2, "Iron, Fe": 0.6,
        "Magnesium, Mg": 16, "Potassium, K": 122, "Vitamin A, RAE": 64,
        "Folate, DFE": 6, "Vitamin C, total ascorbic acid": 0,
        "Zinc, Zn": 0.3, "Vitamin E (alpha-tocopherol)": 0.1,
        "Fiber, total dietary": 0.4, "PUFA 18:3 n-3 c,c,c (ALA)": 0.2,
    },
    173430: {  # Eggs large
        "Energy": 155, "Protein": 13, "Sodium, Na": 124, "Calcium, Ca": 50,
        "Vitamin B-12": 1.1, "Vitamin D (D2 + D3)": 2.0, "Iron, Fe": 1.75,
        "Magnesium, Mg": 10, "Potassium, K": 126, "Vitamin A, RAE": 160,
        "Folate, DFE": 44, "Vitamin C, total ascorbic acid": 0,
        "Zinc, Zn": 1.05, "Vitamin E (alpha-tocopherol)": 1.05,
        "Fiber, total dietary": 0, "PUFA 18:3 n-3 c,c,c (ALA)": 0.04,
    },
    174270: {  # Tofu firm (calcium-set)
        "Energy": 144, "Protein": 17, "Sodium, Na": 14, "Calcium, Ca": 350,
        "Vitamin B-12": 0, "Vitamin D (D2 + D3)": 0, "Iron, Fe": 2.7,
        "Magnesium, Mg": 58, "Potassium, K": 121, "Vitamin A, RAE": 0,
        "Folate, DFE": 19, "Vitamin C, total ascorbic acid": 0.1,
        "Zinc, Zn": 1.6, "Vitamin E (alpha-tocopherol)": 0.01,
        "Fiber, total dietary": 2.3, "PUFA 18:3 n-3 c,c,c (ALA)": 0.6,
    },
    173735: {  # Chicken breast (also reused for "dried black beans" in seed — fix later)
        "Energy": 165, "Protein": 31, "Sodium, Na": 74, "Calcium, Ca": 15,
        "Vitamin B-12": 0.34, "Vitamin D (D2 + D3)": 0.1, "Iron, Fe": 1.0,
        "Magnesium, Mg": 29, "Potassium, K": 256, "Vitamin A, RAE": 9,
        "Folate, DFE": 4, "Vitamin C, total ascorbic acid": 0,
        "Zinc, Zn": 1.0, "Vitamin E (alpha-tocopherol)": 0.27,
        "Fiber, total dietary": 0, "PUFA 18:3 n-3 c,c,c (ALA)": 0.02,
    },
    174036: {  # Ground beef 80/20
        "Energy": 254, "Protein": 17, "Sodium, Na": 67, "Calcium, Ca": 18,
        "Vitamin B-12": 2.4, "Vitamin D (D2 + D3)": 0.1, "Iron, Fe": 1.94,
        "Magnesium, Mg": 17, "Potassium, K": 270, "Vitamin A, RAE": 0,
        "Folate, DFE": 7, "Vitamin C, total ascorbic acid": 0,
        "Zinc, Zn": 4.18, "Vitamin E (alpha-tocopherol)": 0.17,
        "Fiber, total dietary": 0, "PUFA 18:3 n-3 c,c,c (ALA)": 0.05,
    },
    175139: {  # Tuna canned in water
        "Energy": 116, "Protein": 25.5, "Sodium, Na": 247, "Calcium, Ca": 11,
        "Vitamin B-12": 9.4, "Vitamin D (D2 + D3)": 1.7, "Iron, Fe": 1.0,
        "Magnesium, Mg": 27, "Potassium, K": 237, "Vitamin A, RAE": 16,
        "Folate, DFE": 2, "Vitamin C, total ascorbic acid": 0,
        "Zinc, Zn": 0.65, "Vitamin E (alpha-tocopherol)": 0.4,
        "Fiber, total dietary": 0, "PUFA 18:3 n-3 c,c,c (ALA)": 0.01,
    },
    168880: {  # Long grain white rice (uncooked)
        "Energy": 365, "Protein": 7.1, "Sodium, Na": 5, "Calcium, Ca": 28,
        "Vitamin B-12": 0, "Vitamin D (D2 + D3)": 0, "Iron, Fe": 0.8,
        "Magnesium, Mg": 25, "Potassium, K": 115, "Vitamin A, RAE": 0,
        "Folate, DFE": 8, "Vitamin C, total ascorbic acid": 0,
        "Zinc, Zn": 1.09, "Vitamin E (alpha-tocopherol)": 0.11,
        "Fiber, total dietary": 1.6, "PUFA 18:3 n-3 c,c,c (ALA)": 0.03,
    },
    173905: {  # Old fashioned oats (dry)
        "Energy": 389, "Protein": 16.9, "Sodium, Na": 2, "Calcium, Ca": 54,
        "Vitamin B-12": 0, "Vitamin D (D2 + D3)": 0, "Iron, Fe": 4.7,
        "Magnesium, Mg": 177, "Potassium, K": 429, "Vitamin A, RAE": 0,
        "Folate, DFE": 56, "Vitamin C, total ascorbic acid": 0,
        "Zinc, Zn": 4.0, "Vitamin E (alpha-tocopherol)": 0.7,
        "Fiber, total dietary": 10.6, "PUFA 18:3 n-3 c,c,c (ALA)": 0.11,
    },
    172420: {  # Dried lentils
        "Energy": 352, "Protein": 24, "Sodium, Na": 6, "Calcium, Ca": 35,
        "Vitamin B-12": 0, "Vitamin D (D2 + D3)": 0, "Iron, Fe": 6.5,
        "Magnesium, Mg": 47, "Potassium, K": 677, "Vitamin A, RAE": 2,
        "Folate, DFE": 479, "Vitamin C, total ascorbic acid": 4.4,
        "Zinc, Zn": 4.78, "Vitamin E (alpha-tocopherol)": 0.5,
        "Fiber, total dietary": 11, "PUFA 18:3 n-3 c,c,c (ALA)": 0.11,
    },
    170417: {  # Frozen spinach
        "Energy": 28, "Protein": 3, "Sodium, Na": 124, "Calcium, Ca": 136,
        "Vitamin B-12": 0, "Vitamin D (D2 + D3)": 0, "Iron, Fe": 2.7,
        "Magnesium, Mg": 79, "Potassium, K": 469, "Vitamin A, RAE": 524,
        "Folate, DFE": 128, "Vitamin C, total ascorbic acid": 14,
        "Zinc, Zn": 0.53, "Vitamin E (alpha-tocopherol)": 2.0,
        "Fiber, total dietary": 2.5, "PUFA 18:3 n-3 c,c,c (ALA)": 0.14,
    },
    170026: {  # Russet potato (raw)
        "Energy": 79, "Protein": 2.1, "Sodium, Na": 6, "Calcium, Ca": 12,
        "Vitamin B-12": 0, "Vitamin D (D2 + D3)": 0, "Iron, Fe": 0.78,
        "Magnesium, Mg": 23, "Potassium, K": 417, "Vitamin A, RAE": 0,
        "Folate, DFE": 18, "Vitamin C, total ascorbic acid": 19.7,
        "Zinc, Zn": 0.36, "Vitamin E (alpha-tocopherol)": 0.01,
        "Fiber, total dietary": 1.3, "PUFA 18:3 n-3 c,c,c (ALA)": 0.02,
    },
    173944: {  # Peanut butter
        "Energy": 588, "Protein": 25, "Sodium, Na": 459, "Calcium, Ca": 43,
        "Vitamin B-12": 0, "Vitamin D (D2 + D3)": 0, "Iron, Fe": 1.9,
        "Magnesium, Mg": 168, "Potassium, K": 649, "Vitamin A, RAE": 0,
        "Folate, DFE": 87, "Vitamin C, total ascorbic acid": 0,
        "Zinc, Zn": 2.5, "Vitamin E (alpha-tocopherol)": 9.1,
        "Fiber, total dietary": 6, "PUFA 18:3 n-3 c,c,c (ALA)": 0.05,
    },
    173413: {  # Vegetable oil
        "Energy": 884, "Protein": 0, "Sodium, Na": 0, "Calcium, Ca": 0,
        "Vitamin B-12": 0, "Vitamin D (D2 + D3)": 0, "Iron, Fe": 0,
        "Magnesium, Mg": 0, "Potassium, K": 0, "Vitamin A, RAE": 0,
        "Folate, DFE": 0, "Vitamin C, total ascorbic acid": 0,
        "Zinc, Zn": 0, "Vitamin E (alpha-tocopherol)": 17.5,
        "Fiber, total dietary": 0, "PUFA 18:3 n-3 c,c,c (ALA)": 7.2,
    },
}

# Prices in $ per package, by region. Slight regional variance to make multi-location
# comparison interesting in the sample data.
PRICES_BY_REGION: dict[str, dict[str, float]] = {
    "midwest": {
        "0001111041700": 3.49, "0001111041800": 3.99, "0001111060601": 3.49,
        "0001111081640": 2.49, "0001111060710": 4.99, "0001111060810": 5.99,
        "0001111049010": 1.29, "0001111021010": 4.99, "0001111021050": 4.49,
        "0001111041100": 1.99, "0001111041110": 1.99, "0001111060100": 2.49,
        "0001111060200": 4.49, "0001111071100": 3.49, "0001111090100": 5.99,
    },
    "west": {
        "0001111041700": 4.29, "0001111041800": 4.49, "0001111060601": 4.99,
        "0001111081640": 2.99, "0001111060710": 5.99, "0001111060810": 7.99,
        "0001111049010": 1.49, "0001111021010": 5.99, "0001111021050": 4.99,
        "0001111041100": 2.29, "0001111041110": 2.29, "0001111060100": 2.99,
        "0001111060200": 5.49, "0001111071100": 3.99, "0001111090100": 6.99,
    },
    "south": {
        "0001111041700": 3.29, "0001111041800": 3.79, "0001111060601": 3.29,
        "0001111081640": 2.29, "0001111060710": 4.49, "0001111060810": 5.49,
        "0001111049010": 1.19, "0001111021010": 4.49, "0001111021050": 4.29,
        "0001111041100": 1.79, "0001111041110": 1.79, "0001111060100": 2.29,
        "0001111060200": 3.99, "0001111071100": 3.29, "0001111090100": 5.49,
    },
}


def main() -> int:
    skus = load_skus()
    locations = load_locations()
    targets = load_targets()

    # Stub the FDC cache from the inline nutrition data.
    fdc_cache = ROOT / "data" / "raw" / "fdc"
    fdc_cache.mkdir(parents=True, exist_ok=True)
    for fdc_id, nutrients in NUTRITION_BY_FDC_ID.items():
        payload = {
            "fdcId": fdc_id,
            "foodNutrients": [
                {"nutrient": {"name": n, "unitName": ""}, "amount": amt}
                for n, amt in nutrients.items()
            ],
        }
        write_json_atomic(fdc_cache / f"{fdc_id}.json", payload)

    # Synthesize prices_current.json.
    rows: list[dict] = []
    for loc in locations:
        prices = PRICES_BY_REGION.get(loc.region, {})
        for sku in skus:
            regular = prices.get(sku.product_id)
            if regular is None:
                continue
            rows.append({
                "product_id": sku.product_id,
                "location_id": loc.location_id,
                "regular": regular,
                "promo": None,
                "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            })
    prices_payload = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "prices": rows, "missing": [],
        "_note": "synthetic seed data — replaced by `diet ingest` in CI",
    }
    write_json_atomic(ROOT / "data" / "prices_current.json", prices_payload)

    # Reload and solve.
    from diet.foods import load_prices
    prices_loaded = load_prices(ROOT / "data" / "prices_current.json")

    solutions: list[dict] = []
    for loc in locations:
        foods = build_foods_for_location(skus, loc, prices_loaded,
                                         fdc_cache=fdc_cache, use_promo=True)
        for mode in MODE_EXCLUDES:
            sol = solve(foods, targets, mode=mode)
            solutions.append(serialize_solution(
                sol, mode=mode, location_region=loc.region,
                location_display=loc.display,
            ))
            tag = f"{mode:11s} @ {loc.region:7s}"
            if sol.status == "optimal":
                print(f"  {tag}: ${sol.cost_per_day:.2f}/day, {len(sol.basket)} foods")
            else:
                print(f"  {tag}: {sol.status}")

    out = write_data_json(solutions, targets=targets,
                          out_path=ROOT / "site" / "data.json")
    print(f"\nwrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
