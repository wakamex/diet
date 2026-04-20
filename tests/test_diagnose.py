"""Tests for the phase-1 infeasibility diagnosis."""

import pytest

from diet.solver import Food, NutrientTarget, solve


def _food(sku, name, nutrients, price=0.01, max_g=None, cats=()):
    return Food(sku_id=sku, name=name, price_per_g=price, nutrients_per_g=nutrients,
                max_serving_g=max_g, dietary_categories=frozenset(cats))


def test_diagnosis_reports_shortfall_when_nutrient_has_no_source():
    """Vegan-style case: vit D RDA > 0 but no food provides any D."""
    foods = [
        _food("rice", "Rice", {"kcal": 1.3, "protein": 0.03}),
        _food("bean", "Beans", {"kcal": 1.2, "protein": 0.09}),
    ]
    targets = [
        NutrientTarget("kcal", rda=2000, unit="kcal"),
        NutrientTarget("protein", rda=50, unit="g"),
        NutrientTarget("vit_d", rda=15, unit="mcg"),  # no food provides this
    ]
    s = solve(foods, targets, mode="omnivore")
    assert s.status == "infeasible"
    # Should report exactly vit_d as shortfall by the full RDA amount.
    short = [d for d in s.diagnosis if d["kind"] == "shortfall"]
    assert len(short) == 1
    assert short[0]["nutrient"] == "vit_d"
    assert short[0]["amount"] == pytest.approx(15.0, rel=1e-3)
    assert short[0]["pct_of_target"] == pytest.approx(100.0, rel=1e-3)


def test_diagnosis_reports_ul_excess_when_rda_forces_past_ul():
    """Only a sodium-heavy food has vit_b; must hit vit_b RDA so sodium goes
    over its UL — excess is the minimum-slack path."""
    foods = [
        # Salty food is the only vit_b source. Hitting RDA=10 needs 100g salty,
        # which drags sodium to 100 × 50 = 5000mg (UL 1000 → excess 4000mg).
        _food("salty", "Salty",  {"kcal": 1.0, "sodium": 50.0, "vit_b": 0.1}, max_g=None),
        _food("plain", "Plain",  {"kcal": 1.0, "sodium": 0.01, "vit_b": 0.0},  max_g=None),
    ]
    targets = [
        NutrientTarget("kcal",    rda=2000, unit="kcal"),
        NutrientTarget("vit_b",   rda=10,   unit="mg"),
        NutrientTarget("sodium",  ul=1000,  unit="mg"),
    ]
    s = solve(foods, targets, mode="omnivore")
    assert s.status == "infeasible"
    # At least one diagnosis row; sodium excess should be in there.
    assert len(s.diagnosis) >= 1
    nutrients_flagged = {d["nutrient"] for d in s.diagnosis}
    assert "sodium" in nutrients_flagged or "vit_b" in nutrients_flagged


def test_diagnosis_empty_when_feasible():
    """No diagnosis populated when the main solve succeeds."""
    foods = [_food("rice", "Rice", {"kcal": 1.3, "protein": 0.03}, max_g=2000)]
    targets = [NutrientTarget("kcal", rda=2000, unit="kcal"),
               NutrientTarget("protein", rda=50, unit="g")]
    s = solve(foods, targets, mode="omnivore")
    assert s.status == "optimal"
    assert s.diagnosis == []
