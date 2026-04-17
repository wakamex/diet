"""USDA FoodData Central API client.

Docs: https://fdc.nal.usda.gov/api-guide.html
We only need the food detail endpoint (returns nutrients per 100 g).
The free-tier API key is rate-limited but generous enough for our ~80-SKU pull.
"""

from __future__ import annotations

import os
import urllib.error
from pathlib import Path

from diet.util import http_get_json, read_json, write_json_atomic

FDC_FOOD_URL = "https://api.nal.usda.gov/fdc/v1/food"
FDC_SEARCH_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"

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


def search_foods(query: str, *, page_size: int = 5,
                 data_types: tuple[str, ...] = ("Foundation", "SR Legacy")) -> list[dict]:
    """Find candidate foods for a free-text query.

    Foundation/SR Legacy foods are preferred — they're per-100g unprocessed
    reference entries, vs Branded which are per-package and noisier. Returns
    the API's `foods` array (already ranked by relevance).
    """
    payload = http_get_json(
        FDC_SEARCH_URL,
        params={
            "api_key": _api_key(),
            "query": query,
            "dataType": ",".join(data_types),
            "pageSize": page_size,
        },
    )
    return payload.get("foods") or []


def best_match(query: str) -> dict | None:
    """Return the top-ranked Foundation/SR Legacy food for a query, or None.

    FDC's search endpoint can return Foundation IDs that 404 on /v1/food/{id}
    (observed for ~5 of 28 picks in our basket — apparently "experimental
    Foundation" entries that made it into search but not the food endpoint).
    We verify each candidate via fetch_food and fall back to the next hit on
    HTTP 404. The top tier is "Foundation entries about the same first-word
    topic as the top hit" (avoids preferring a Foundation 'Carrots, frozen' over
    an SR Legacy 'Broccoli, frozen' just because Foundation outranked SR Legacy).
    """
    hits = search_foods(query)
    if not hits:
        return None
    top = hits[0]
    top_first_word = top.get("description", "").split(",")[0].strip().lower()
    same_topic = lambda f: (f.get("description", "").split(",")[0].strip().lower()
                            == top_first_word)
    foundation_same_topic = [f for f in hits
                             if f.get("dataType") == "Foundation" and same_topic(f)]
    rest = [f for f in hits if f not in foundation_same_topic]
    ordered = foundation_same_topic + rest
    for candidate in ordered:
        fdc_id = candidate.get("fdcId")
        if not fdc_id:
            continue
        try:
            fetch_food(int(fdc_id))
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                continue
            raise
        except RuntimeError:
            # http_request wraps repeated failures; skip and try the next hit.
            continue
        return candidate
    return None


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
