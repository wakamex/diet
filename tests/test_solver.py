"""Tests for the LP solver.

These tests use small, hand-built food universes so the optimum is easy to verify
analytically. They guard against regressions in the constraint construction, mode
filtering, and shadow-price reporting.
"""

from __future__ import annotations

import pytest

from diet.solver import (
    EPSILON_G,
    MODE_EXCLUDES,
    Food,
    NutrientTarget,
    solve,
)


def _food(sku, name, price, nutrients, max_g=2000.0, cats=()):
    return Food(sku_id=sku, name=name, price_per_g=price, nutrients_per_g=nutrients,
                max_serving_g=max_g, dietary_categories=frozenset(cats))


# Three foods, two nutrients. With max_g=2000 (generous), rice alone can satisfy
# both kcal and protein for vegetarian/vegan. Beef enters only if it's worth its cost.
FOODS = [
    _food("rice", "Rice", price=0.002, nutrients={"kcal": 1.3, "protein": 0.026}),
    _food("bean", "Beans", price=0.005, nutrients={"kcal": 1.2, "protein": 0.090}),
    _food("beef", "Beef", price=0.020, nutrients={"kcal": 2.5, "protein": 0.260},
          cats=("meat_red",)),
]

KCAL = NutrientTarget("kcal", rda=2000, unit="kcal")
PROTEIN = NutrientTarget("protein", rda=50, unit="g")


def test_optimal_omnivore_picks_cheapest_per_kcal():
    # Cost per kcal: rice $0.00154, bean $0.00417, beef $0.0080. Rice wins.
    # Need 2000 kcal: 2000/1.3 ≈ 1538 g rice. Cost ≈ $3.08. Protein 1538 * 0.026 ≈ 40 g — short of 50.
    # So mix in beans to make up protein. Beans add 0.09 g protein per gram, more than rice's 0.026.
    # Solver should land somewhere between $3.08 (kcal-bound) and $9.50 (max-mix).
    s = solve(FOODS, [KCAL, PROTEIN], mode="omnivore")
    assert s.status == "optimal"
    assert 3.0 <= s.cost_per_day <= 4.5, f"unexpected cost {s.cost_per_day}"


def test_vegetarian_excludes_beef():
    s = solve(FOODS, [KCAL, PROTEIN], mode="vegetarian")
    assert s.status == "optimal"
    skus = {b["sku_id"] for b in s.basket}
    assert "beef" not in skus


def test_vegan_same_as_vegetarian_when_no_dairy_or_eggs_present():
    """Our small food universe has no dairy/egg items, so vegan ≡ vegetarian here."""
    s_v = solve(FOODS, [KCAL, PROTEIN], mode="vegetarian")
    s_g = solve(FOODS, [KCAL, PROTEIN], mode="vegan")
    assert s_v.status == s_g.status == "optimal"
    assert s_v.cost_per_day == pytest.approx(s_g.cost_per_day)


def test_infeasible_when_serving_caps_too_tight():
    """With 100g caps, no diet can hit 2000 kcal from these three foods."""
    tight_foods = [
        _food("rice", "Rice", price=0.002, nutrients={"kcal": 1.3, "protein": 0.026}, max_g=100),
        _food("bean", "Beans", price=0.005, nutrients={"kcal": 1.2, "protein": 0.090}, max_g=100),
    ]
    s = solve(tight_foods, [KCAL, PROTEIN], mode="vegan")
    assert s.status == "infeasible"
    assert s.cost_per_day is None


def test_basket_grams_above_epsilon_only():
    s = solve(FOODS, [KCAL, PROTEIN], mode="omnivore")
    assert s.status == "optimal"
    for b in s.basket:
        assert b["grams_per_day"] >= EPSILON_G


def test_shadow_price_matches_marginal_food():
    """With only kcal binding, shadow price = $/kcal of the cheapest-per-kcal food."""
    s = solve(FOODS, [KCAL], mode="omnivore")
    assert s.status == "optimal"
    [n] = s.nutrients
    assert n["binding"] is True
    expected = 0.002 / 1.3  # rice $/kcal
    assert n["shadow_price_per_unit"] == pytest.approx(expected, rel=0.05)


def test_upper_bound_blocks_excess_sodium():
    """Salt water is cheapest per kcal but exceeds sodium UL — solver must dilute."""
    foods = [
        _food("salt", "Salt water", price=0.001,
              nutrients={"kcal": 1.0, "sodium_mg": 100.0}, max_g=3000),
        _food("plain", "Plain food", price=0.010,
              nutrients={"kcal": 1.0, "sodium_mg": 0.5}, max_g=3000),
    ]
    targets = [
        NutrientTarget("kcal", rda=2000, unit="kcal"),
        NutrientTarget("sodium_mg", ul=2300, unit="mg"),
    ]
    s = solve(foods, targets, mode="omnivore")
    assert s.status == "optimal"
    sodium_total = sum(b["grams_per_day"] * (100.0 if b["sku_id"] == "salt" else 0.5)
                       for b in s.basket)
    # Tolerance accounts for the 2-decimal rounding applied to basket gram values.
    assert sodium_total <= 2301.0
    # And the UL row should be binding.
    ul_row = next(n for n in s.nutrients if n["nutrient"] == "sodium_mg" and n["kind"] == "ul")
    assert ul_row["binding"] is True


def test_unknown_mode_raises():
    with pytest.raises(ValueError):
        solve(FOODS, [KCAL], mode="carnivore")


def test_no_targets_returns_error():
    s = solve(FOODS, [], mode="omnivore")
    assert s.status == "error"


def test_mode_excludes_table_is_consistent():
    """omnivore ⊆ pescatarian ⊆ vegetarian ⊆ vegan in terms of excluded categories."""
    om = MODE_EXCLUDES["omnivore"]
    pe = MODE_EXCLUDES["pescatarian"]
    ve = MODE_EXCLUDES["vegetarian"]
    vg = MODE_EXCLUDES["vegan"]
    assert om <= pe <= ve <= vg
