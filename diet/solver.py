"""Linear program for the Stigler diet.

Decision variables: grams/day of each food.
Objective: minimize daily cost.
Constraints: nutrient RDAs (lower bounds) and ULs (upper bounds), mode exclusions,
per-food palatability caps, non-negativity.

Solver: scipy.optimize.linprog with HiGHS. Dual values are read off the marginals to
produce shadow prices for binding nutrient constraints.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Literal

import numpy as np
from scipy.optimize import linprog

EPSILON_G = 1e-3  # foods below this gram count are treated as not in the basket


@dataclass(frozen=True)
class Food:
    """A single SKU after price + nutrient join."""

    sku_id: str
    name: str
    price_per_g: float                           # $ per gram
    nutrients_per_g: dict[str, float]            # nutrient name -> amount per gram
    max_serving_g: float                         # palatability cap
    dietary_categories: frozenset[str] = frozenset()
    meta: dict = field(default_factory=dict)     # arbitrary, passed through to output


@dataclass(frozen=True)
class NutrientTarget:
    """RDA (lower bound) and/or UL (upper bound) for one nutrient."""

    nutrient: str
    rda: float | None = None
    ul: float | None = None
    unit: str = ""


@dataclass(frozen=True)
class Solution:
    status: Literal["optimal", "infeasible", "unbounded", "error"]
    message: str
    cost_per_day: float | None
    basket: list[dict]                           # selected foods
    nutrients: list[dict]                        # delivery + shadow prices


# Mode → excluded dietary_categories. Single source of truth.
MODE_EXCLUDES: dict[str, frozenset[str]] = {
    "omnivore":    frozenset(),
    "pescatarian": frozenset({"meat_red", "meat_white", "meat_processed"}),
    "vegetarian":  frozenset({"meat_red", "meat_white", "meat_processed", "fish"}),
    "ovo_lacto":   frozenset({"meat_red", "meat_white", "meat_processed", "fish"}),
    "vegan":       frozenset({"meat_red", "meat_white", "meat_processed", "fish",
                              "dairy", "egg"}),
}


def solve(
    foods: list[Food],
    targets: list[NutrientTarget],
    mode: str = "omnivore",
) -> Solution:
    """Solve the LP for one (foods, targets, mode) combination.

    Foods excluded by mode are dropped from the formulation entirely (rather than
    bounded to zero) to keep the LP small and improve solver conditioning.
    """
    if mode not in MODE_EXCLUDES:
        raise ValueError(f"unknown mode: {mode!r}; known: {sorted(MODE_EXCLUDES)}")

    excluded = MODE_EXCLUDES[mode]
    eligible = [f for f in foods if not (f.dietary_categories & excluded)]
    if not eligible:
        return Solution("infeasible", f"no foods eligible for mode {mode!r}",
                        None, [], [])

    n_foods = len(eligible)
    nutrient_names = [t.nutrient for t in targets]

    # Objective: cost per gram per food
    c = np.array([f.price_per_g for f in eligible], dtype=float)

    # Per-food bounds
    bounds = [(0.0, f.max_serving_g) for f in eligible]

    # Build A_ub (≤) rows. Lower-bound (RDA) constraints become -A x ≤ -rda.
    rows: list[np.ndarray] = []
    rhs: list[float] = []
    constraint_meta: list[dict] = []  # parallel to rows, for shadow-price reporting

    for t in targets:
        nutrient_vec = np.array(
            [f.nutrients_per_g.get(t.nutrient, 0.0) for f in eligible], dtype=float
        )
        if t.rda is not None:
            rows.append(-nutrient_vec)
            rhs.append(-t.rda)
            constraint_meta.append({"nutrient": t.nutrient, "kind": "rda",
                                    "target": t.rda, "unit": t.unit})
        if t.ul is not None:
            rows.append(nutrient_vec)
            rhs.append(t.ul)
            constraint_meta.append({"nutrient": t.nutrient, "kind": "ul",
                                    "target": t.ul, "unit": t.unit})

    if not rows:
        return Solution("error", "no nutrient targets supplied", None, [], [])

    A_ub = np.vstack(rows)
    b_ub = np.array(rhs, dtype=float)

    res = linprog(c=c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")

    if not res.success:
        # status: 0 success, 1 iteration limit, 2 infeasible, 3 unbounded, 4 numerical
        if res.status == 2:
            return Solution("infeasible", res.message, None, [], _empty_nutrients(targets))
        if res.status == 3:
            return Solution("unbounded", res.message, None, [], _empty_nutrients(targets))
        return Solution("error", res.message, None, [], _empty_nutrients(targets))

    x = res.x
    cost = float(res.fun)

    # Basket: foods with grams above epsilon
    basket: list[dict] = []
    for f, grams in zip(eligible, x):
        if grams < EPSILON_G:
            continue
        food_cost = float(grams * f.price_per_g)
        basket.append({
            "sku_id": f.sku_id,
            "name": f.name,
            "grams_per_day": round(float(grams), 2),
            "cost_per_day": round(food_cost, 4),
            "pct_of_basket": round(food_cost / cost * 100, 1) if cost > 0 else 0.0,
            "meta": f.meta,
        })
    basket.sort(key=lambda b: -b["cost_per_day"])

    # Nutrient delivery + shadow prices
    delivered_per_nutrient: dict[str, float] = {}
    for name in nutrient_names:
        nutrient_vec = np.array(
            [f.nutrients_per_g.get(name, 0.0) for f in eligible], dtype=float
        )
        delivered_per_nutrient[name] = float(nutrient_vec @ x)

    # HiGHS marginals on inequality constraints (one per A_ub row, same order).
    # ineqlin.marginals[i] is dCost/d(b_ub[i]) at the optimum, ≤ 0 for binding,
    # 0 for slack. For an RDA row (-A x ≤ -rda), tightening RDA = decreasing b_ub by 1
    # increases cost by -marginal. So shadow_price(rda) = -marginal.
    # For a UL row (A x ≤ ul), relaxing UL by 1 decreases cost by -marginal.
    marginals = getattr(res, "ineqlin", None)
    margs = list(marginals.marginals) if marginals is not None else [0.0] * len(rows)

    nutrient_rows: list[dict] = []
    seen: set[str] = set()
    for cm, marg in zip(constraint_meta, margs):
        name = cm["nutrient"]
        delivered = delivered_per_nutrient[name]
        target = cm["target"]
        kind = cm["kind"]
        if kind == "rda":
            slack = delivered - target
            binding = abs(slack) < max(1e-6, 1e-4 * abs(target))
            shadow = -float(marg)  # $/unit-of-nutrient at the optimum
        else:  # ul
            slack = target - delivered
            binding = abs(slack) < max(1e-6, 1e-4 * abs(target))
            shadow = -float(marg)
        # If both RDA and UL exist for a nutrient, emit both rows distinctly.
        nutrient_rows.append({
            "nutrient": name,
            "kind": kind,
            "target": target,
            "delivered": round(delivered, 4),
            "unit": cm["unit"],
            "binding": bool(binding),
            "shadow_price_per_unit": round(shadow, 6),
        })
        seen.add(name)

    return Solution("optimal", "optimal solution found", round(cost, 4),
                    basket, nutrient_rows)


def _empty_nutrients(targets: Iterable[NutrientTarget]) -> list[dict]:
    return [
        {"nutrient": t.nutrient, "kind": "rda" if t.rda is not None else "ul",
         "target": t.rda if t.rda is not None else t.ul,
         "delivered": 0.0, "unit": t.unit, "binding": False,
         "shadow_price_per_unit": 0.0}
        for t in targets
    ]
