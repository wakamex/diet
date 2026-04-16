"""USDA FoodData Central API client.

Docs: https://fdc.nal.usda.gov/api-guide.html
We only need the food detail endpoint (returns nutrients per 100 g).
The free-tier API key is rate-limited but generous enough for our ~80-SKU pull.
"""

from __future__ import annotations

import os
from pathlib import Path

from diet.util import http_get_json, read_json, write_json_atomic

FDC_FOOD_URL = "https://api.nal.usda.gov/fdc/v1/food"

# Map FDC nutrient names → our internal nutrient ids (must match data/dri.json).
# FDC uses long display names; this dict maps any of them to a canonical id.
FDC_NUTRIENT_MAP: dict[str, str] = {
    "Energy":                                       "energy_kcal",
    "Energy (Atwater General Factors)":             "energy_kcal",
    "Energy (Atwater Specific Factors)":            "energy_kcal",
    "Protein":                                      "protein_g",
    "Fiber, total dietary":                         "fiber_g",
    "PUFA 18:3 n-3 c,c,c (ALA)":                    "ala_g",
    "Fatty acids, total polyunsaturated 18:3 n-3 c,c,c (ALA)": "ala_g",
    "Vitamin A, RAE":                               "vit_a_mcg",
    "Vitamin C, total ascorbic acid":               "vit_c_mg",
    "Vitamin D (D2 + D3)":                          "vit_d_mcg",
    "Vitamin E (alpha-tocopherol)":                 "vit_e_mg",
    "Vitamin B-12":                                 "vit_b12_mcg",
    "Folate, DFE":                                  "folate_mcg",
    "Calcium, Ca":                                  "calcium_mg",
    "Iron, Fe":                                     "iron_mg",
    "Magnesium, Mg":                                "magnesium_mg",
    "Potassium, K":                                 "potassium_mg",
    "Sodium, Na":                                   "sodium_mg",
    "Zinc, Zn":                                     "zinc_mg",
}


def _api_key() -> str:
    key = os.environ.get("FDC_API_KEY")
    if not key:
        raise RuntimeError("FDC_API_KEY must be set in env (https://api.data.gov/signup/)")
    return key


def fetch_food(fdc_id: int) -> dict:
    """Pull a single food's full record."""
    return http_get_json(
        f"{FDC_FOOD_URL}/{fdc_id}",
        params={"api_key": _api_key(), "format": "full", "nutrients": ""},
    )


def fetch_food_cached(fdc_id: int, cache_root: Path) -> dict:
    """Pull a food, caching the raw JSON under cache_root/<fdc_id>.json."""
    cache_path = cache_root / f"{fdc_id}.json"
    if cache_path.exists():
        return read_json(cache_path)
    payload = fetch_food(fdc_id)
    write_json_atomic(cache_path, payload)
    return payload


def nutrients_per_g(food_payload: dict) -> dict[str, float]:
    """Project an FDC food JSON onto our internal {nutrient_id: per-gram} dict.

    FDC returns nutrient amounts per 100 g; we convert to per-gram and apply the
    FDC_NUTRIENT_MAP. Nutrients we don't track are dropped silently.
    """
    out: dict[str, float] = {}
    for entry in food_payload.get("foodNutrients") or []:
        nutrient = entry.get("nutrient") or {}
        name = nutrient.get("name")
        amount = entry.get("amount")
        if name is None or amount is None:
            continue
        canonical = FDC_NUTRIENT_MAP.get(name)
        if not canonical:
            continue
        # Don't overwrite if multiple FDC names map to the same canonical (e.g. Energy):
        # take the first one we see.
        if canonical in out:
            continue
        out[canonical] = float(amount) / 100.0
    return out
