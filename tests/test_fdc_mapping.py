"""Tests for the FDC nutrient projection — purely a mapping function."""

import pytest

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


def test_missing_amount_skipped():
    payload = {"foodNutrients": [
        {"nutrient": {"name": "Protein"}, "amount": None},
    ]}
    assert nutrients_per_g(payload) == {}
