"""Supplements — label-sourced per-tablet nutrients, priced via the Kroger API.

Lives alongside `skus.yaml` in a separate file because the data model differs:
no FDC id (FDC is food-only), nutrients are declared inline, and pricing/size
math goes via tablet count and tablet weight rather than net package weight.
The loader materializes the same `SkuSpec` + `Food` types the rest of the
pipeline already understands, so the solver stays uniform.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from diet.foods import Location, SkuSpec
from diet.solver import Food

DEFAULT_SUPPLEMENTS_PATH = Path("data/supplements.yaml")


@dataclass(frozen=True)
class SupplementSpec:
    """Row from data/supplements.yaml after parsing."""
    product_id: str
    name: str
    count: int                                # tablets per package
    tablet_g: float                           # grams per tablet
    max_tablets_per_day: float
    dietary_categories: frozenset[str]
    nutrients_per_tablet: dict[str, float]    # keyed by our canonical nutrient ids
    source: str = "kroger"                    # "kroger" | "walmart" — routes ingest

    @property
    def unit_grams(self) -> float:
        """Net package weight = count × tablet_g — consistent with foods.py."""
        return self.count * self.tablet_g

    @property
    def max_serving_g(self) -> float:
        return self.max_tablets_per_day * self.tablet_g

    @property
    def nutrients_per_g(self) -> dict[str, float]:
        """Per-gram values, so the LP coefficients line up with foods."""
        return {k: v / self.tablet_g for k, v in self.nutrients_per_tablet.items()}


def load_supplements(path: Path | str = DEFAULT_SUPPLEMENTS_PATH) -> list[SupplementSpec]:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or []
    out: list[SupplementSpec] = []
    for r in raw:
        out.append(SupplementSpec(
            product_id=str(r["product_id"]),
            name=str(r["name"]),
            count=int(r["count"]),
            tablet_g=float(r["tablet_g"]),
            max_tablets_per_day=float(r["max_tablets_per_day"]),
            dietary_categories=frozenset(r.get("dietary_categories") or ["supplement"]),
            nutrients_per_tablet=dict(r.get("nutrients_per_tablet") or {}),
            source=r.get("source", "kroger"),
        ))
    return out


def as_sku_specs(supps: list[SupplementSpec]) -> list[SkuSpec]:
    """Adapter for reusing the shared ingest path (Kroger price fetch needs a
    product_id stream). `fdc_id=0` is a sentinel — foods.build_foods_for_location
    must be told to treat supplements specially."""
    return [SkuSpec(
        product_id=s.product_id, fdc_id=0, name=s.name,
        unit_grams=s.unit_grams,
        dietary_categories=s.dietary_categories,
        max_serving_g=s.max_serving_g,
        source=s.source,
    ) for s in supps]


def build_supplement_foods(
    supps: list[SupplementSpec],
    location: Location,
    prices: dict[tuple[str, str], dict],
    *,
    use_promo: bool = True,
) -> list[Food]:
    """Build Food records for supplements at one location. Skips any without a
    price at that location (same semantics as foods.build_foods_for_location)."""
    foods: list[Food] = []
    for s in supps:
        row = prices.get((s.product_id, location.location_id))
        if not row:
            continue
        regular = row.get("regular")
        promo = row.get("promo")
        chosen = promo if (use_promo and promo) else regular
        if chosen is None:
            continue
        price_per_g = float(chosen) / s.unit_grams
        foods.append(Food(
            sku_id=s.product_id,
            name=s.name,
            price_per_g=price_per_g,
            nutrients_per_g=s.nutrients_per_g,
            max_serving_g=s.max_serving_g,
            dietary_categories=s.dietary_categories,
            meta={
                "is_supplement": True,
                "count": s.count,
                "tablet_g": s.tablet_g,
                "max_tablets_per_day": s.max_tablets_per_day,
                "unit_grams": s.unit_grams,
                "price_regular": regular,
                "price_promo": promo,
                "price_used": chosen,
                "price_kind": "promo" if (use_promo and promo) else "regular",
                "location_id": location.location_id,
                "location_display": location.display,
            },
        ))
    return foods
