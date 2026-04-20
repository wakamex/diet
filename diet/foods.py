"""Join curated SKUs with USDA FDC nutrients and current Kroger prices.

Returns a list of `Food` records (the solver's input dataclass), one per
(sku × location), with `meta` carrying display info for the eventual `data.json`.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from diet.solver import Food
from diet.sources import fdc as fdc_mod
from diet.util import read_json

DEFAULT_SKUS_PATH = Path("data/skus.yaml")
DEFAULT_LOCATIONS_PATH = Path("data/locations.yaml")
DEFAULT_PRICES_PATH = Path("data/prices_current.json")
DEFAULT_FDC_CACHE = Path("data/raw/fdc")
# None = no per-food palatability cap (Stigler-pure LP). A food's `max_serving_g`
# can still be set explicitly in skus.yaml to restrict a specific item.
DEFAULT_MAX_SERVING_G: float | None = None


@dataclass(frozen=True)
class SkuSpec:
    """A row from data/skus.yaml after parsing."""

    product_id: str
    fdc_id: int
    name: str
    unit_grams: float
    dietary_categories: frozenset[str]
    max_serving_g: float | None


@dataclass(frozen=True)
class Location:
    """A row from data/locations.yaml."""

    region: str           # short key, e.g. "midwest"
    location_id: str      # Kroger locationId
    display: str          # human label, e.g. "Kroger #01400441 — Cincinnati, OH"


def load_skus(path: Path | str = DEFAULT_SKUS_PATH) -> list[SkuSpec]:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or []
    out: list[SkuSpec] = []
    for r in raw:
        cap = r.get("max_serving_g")
        out.append(SkuSpec(
            product_id=str(r["product_id"]),
            fdc_id=int(r["fdc_id"]),
            name=str(r["name"]),
            unit_grams=float(r["unit_grams"]),
            dietary_categories=frozenset(r.get("dietary_categories") or []),
            max_serving_g=float(cap) if cap is not None else DEFAULT_MAX_SERVING_G,
        ))
    return out


def load_locations(path: Path | str = DEFAULT_LOCATIONS_PATH) -> list[Location]:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or []
    return [Location(region=r["region"], location_id=str(r["location_id"]),
                     display=r.get("display", r["location_id"])) for r in raw]


def load_prices(path: Path | str = DEFAULT_PRICES_PATH) -> dict[tuple[str, str], dict]:
    """`prices_current.json` shape: [{product_id, location_id, regular, promo, ...}, ...]"""
    payload = read_json(Path(path))
    out: dict[tuple[str, str], dict] = {}
    for entry in payload.get("prices", []):
        out[(entry["product_id"], entry["location_id"])] = entry
    return out


def build_foods_for_location(
    skus: list[SkuSpec],
    location: Location,
    prices: dict[tuple[str, str], dict],
    *,
    fdc_cache: Path = DEFAULT_FDC_CACHE,
    use_promo: bool = True,
) -> list[Food]:
    """Materialize Food records for every SKU that has a price at this location.

    SKUs without a price entry are skipped silently — they'll show up in the
    `validate` report instead.
    """
    foods: list[Food] = []
    for sku in skus:
        price_row = prices.get((sku.product_id, location.location_id))
        if not price_row:
            continue
        regular = price_row.get("regular")
        promo = price_row.get("promo")
        chosen = promo if (use_promo and promo) else regular
        if chosen is None:
            continue
        # Convert package $ → $/g. Nutrients come from FDC per-100g, normalized to per-g.
        price_per_g = float(chosen) / sku.unit_grams

        fdc_payload = fdc_mod.fetch_food_cached(sku.fdc_id, fdc_cache)
        nutrients = fdc_mod.nutrients_per_g(fdc_payload)

        foods.append(Food(
            sku_id=sku.product_id,
            name=sku.name,
            price_per_g=price_per_g,
            nutrients_per_g=nutrients,
            max_serving_g=sku.max_serving_g,
            dietary_categories=sku.dietary_categories,
            meta={
                "fdc_id": sku.fdc_id,
                "unit_grams": sku.unit_grams,
                "price_regular": regular,
                "price_promo": promo,
                "price_used": chosen,
                "price_kind": "promo" if (use_promo and promo) else "regular",
                "location_id": location.location_id,
                "location_display": location.display,
            },
        ))
    return foods
