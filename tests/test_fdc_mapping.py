"""Tests for the FDC nutrient projection — purely a mapping function."""

import pytest

from diet.sources import fdc
from diet.sources.fdc import nutrients_per_g


def test_nutrients_per_g_converts_per_100g_to_per_g():
    payload = {"foodNutrients": [
        {"nutrient": {"name": "Energy"},                      "amount": 130.0},
        {"nutrient": {"name": "Protein"},                     "amount": 2.7},
        {"nutrient": {"name": "Vitamin C, total ascorbic acid"}, "amount": 4.6},
        {"nutrient": {"name": "Sodium, Na"},                  "amount": 5.0},
        {"nutrient": {"name": "Some Random Nutrient"},        "amount": 99.0},
    ]}
    out = nutrients_per_g(payload)
    assert out["energy_kcal"] == pytest.approx(1.3)
    assert out["protein_g"] == pytest.approx(0.027)
    assert out["vit_c_mg"] == pytest.approx(0.046)
    assert out["sodium_mg"] == pytest.approx(0.05)
    assert "Some Random Nutrient" not in out  # unmapped names dropped


def test_first_match_wins_for_duplicate_canonicals():
    payload = {"foodNutrients": [
        {"nutrient": {"name": "Energy"},                          "amount": 100.0},
        {"nutrient": {"name": "Energy (Atwater General Factors)"}, "amount": 200.0},
    ]}
    out = nutrients_per_g(payload)
    assert out["energy_kcal"] == pytest.approx(1.0)  # first one wins


def test_generic_ala_is_fallback_for_legacy_records():
    payload = {"foodNutrients": [
        {"nutrient": {"name": "PUFA 18:3"}, "amount": 9.08},
    ]}
    assert nutrients_per_g(payload)["ala_g"] == pytest.approx(0.0908)


def test_explicit_ala_takes_priority_over_generic_value():
    payload = {"foodNutrients": [
        {"nutrient": {"name": "PUFA 18:3"}, "amount": 1.2},
        {"nutrient": {"name": "PUFA 18:3 n-3 c,c,c (ALA)"}, "amount": 1.1},
    ]}
    assert nutrients_per_g(payload)["ala_g"] == pytest.approx(0.011)


def test_missing_amount_skipped():
    payload = {"foodNutrients": [
        {"nutrient": {"name": "Protein"}, "amount": None},
    ]}
    assert nutrients_per_g(payload) == {}


def test_branded_upc_cache_requires_exact_normalized_gtin(tmp_path, monkeypatch):
    hits = [
        {"fdcId": 1, "gtinUpc": "999999999999"},
        {"fdcId": 2, "gtinUpc": "001234567890"},
    ]
    monkeypatch.setattr(fdc, "search_foods", lambda *args, **kwargs: hits)
    monkeypatch.setattr(
        fdc, "fetch_food_cached",
        lambda fdc_id, cache_root: {"fdcId": fdc_id},
    )
    assert fdc.search_branded_upc_cached("01234567890", tmp_path) == {"fdcId": 2}
    # The search response, including misses, is persisted for later ingests.
    assert (tmp_path / "upc" / "01234567890.json").exists()
