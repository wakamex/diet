"""Join curated SKUs with USDA FDC nutrients and current Kroger prices.

Returns a list of `Food` records (the solver's input dataclass), one per
(sku × location), with `meta` carrying display info for the eventual `data.json`.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from diet.solver import Food
from diet.nutrition import (
    DEFAULT_NUTRIENTS_PATH,
    load_sku_nutrients,
    merge_with_usda_fallback,
)
from diet.sources import fdc as fdc_mod
from diet.util import read_json

DEFAULT_SKUS_PATH = Path("data/skus.yaml")
DEFAULT_WALMART_SKUS_PATH = Path("data/walmart_skus.yaml")
DEFAULT_CANADA_PRODUCT_MAP_PATH = Path("data/canada_product_map.yaml")
DEFAULT_LOCATIONS_PATH = Path("data/locations.yaml")
DEFAULT_PRICES_PATH = Path("data/prices_current.json")
DEFAULT_FDC_CACHE = Path("data/raw/fdc")
# None = no per-food palatability cap (Stigler-pure LP). A food's `max_serving_g`
# can still be set explicitly in skus.yaml to restrict a specific item.
DEFAULT_MAX_SERVING_G: float | None = None


@dataclass(frozen=True)
class SkuSpec:
    """A row from data/skus.yaml (or walmart_skus.yaml) after parsing."""

    product_id: str
    fdc_id: int
    name: str
    unit_grams: float
    dietary_categories: frozenset[str]
    max_serving_g: float | None
    source: str = "kroger"   # retailer/source key — routes ingest
    package_label: str | None = None
    search_query: str | None = None


@dataclass(frozen=True)
class Location:
    """A row from data/locations.yaml."""

    region: str           # short key, e.g. "midwest"
    location_id: str      # Kroger locationId or synthetic for walmart
    display: str          # human label
    source: str = "kroger"
    currency: str = "USD"
    price_scope: str = "store"
    reference_store_name: str | None = None
    reference_store_address: str | None = None
    reference_store_basis: str | None = None
    member_regions: tuple[str, ...] = ()


def load_skus(path: Path | str = DEFAULT_SKUS_PATH,
              *, source: str = "kroger") -> list[SkuSpec]:
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
            source=r.get("source", source),
            package_label=r.get("_package"),
            search_query=r.get("query"),
        ))
    return out


def load_all_skus() -> list[SkuSpec]:
    """Load every configured retailer SKU file."""
    skus = load_skus(DEFAULT_SKUS_PATH, source="kroger")
    if DEFAULT_WALMART_SKUS_PATH.exists():
        skus += load_skus(DEFAULT_WALMART_SKUS_PATH, source="walmart")
    if DEFAULT_CANADA_PRODUCT_MAP_PATH.exists():
        skus += load_canada_skus(skus, DEFAULT_CANADA_PRODUCT_MAP_PATH)
    return skus


def load_canada_skus(
    base_skus: list[SkuSpec],
    path: Path | str = DEFAULT_CANADA_PRODUCT_MAP_PATH,
) -> list[SkuSpec]:
    """Expand curated Canadian UPC mappings and inherit concept nutrition tags."""
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or []
    concepts: dict[int, SkuSpec] = {}
    for sku in base_skus:
        concepts.setdefault(sku.fdc_id, sku)
    out: list[SkuSpec] = []
    for row in raw:
        fdc_id = int(row["fdc_id"])
        concept = concepts.get(fdc_id)
        if concept is None:
            raise ValueError(f"Canadian mapping references unknown FDC concept {fdc_id}")
        sources = row.get("sources") or [row.get("source")]
        if not sources or any(
            source not in {"metro", "foodbasics", "superstore", "nofrills"}
            for source in sources
        ):
            raise ValueError(
                f"Canadian mapping {row.get('product_id')!r} has invalid sources"
            )
        for source in sources:
            out.append(SkuSpec(
                product_id=str(row["product_id"]),
                fdc_id=fdc_id,
                name=str(row["name"]),
                unit_grams=float(row["unit_grams"]),
                dietary_categories=concept.dietary_categories,
                max_serving_g=concept.max_serving_g,
                source=source,
                package_label=row.get("package"),
                search_query=row.get("query"),
            ))
    return out


def load_locations(path: Path | str = DEFAULT_LOCATIONS_PATH) -> list[Location]:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or []
    return [Location(region=r["region"], location_id=str(r["location_id"]),
                     display=r.get("display", r["location_id"]),
                     source=r.get("source", "kroger"),
                     currency=r.get("currency", "USD").upper(),
                     price_scope=r.get("price_scope", "store"),
                     reference_store_name=r.get("reference_store_name"),
                     reference_store_address=r.get("reference_store_address"),
                     reference_store_basis=r.get("reference_store_basis"),
                     member_regions=tuple(r.get("member_regions") or ())) for r in raw]


def price_locations_for(
    location: Location,
    locations: list[Location] | None = None,
) -> dict[str, Location]:
    """Map retailer source keys to the concrete locations supplying prices."""
    if not location.member_regions:
        return {location.source: location}
    configured = locations or load_locations()
    by_region = {item.region: item for item in configured}
    missing = [region for region in location.member_regions if region not in by_region]
    if missing:
        raise ValueError(
            f"composite location {location.region!r} has unknown members: {missing}"
        )
    members = [by_region[region] for region in location.member_regions]
    sources = {member.source: member for member in members}
    if len(sources) != len(members):
        raise ValueError(
            f"composite location {location.region!r} has duplicate retailer sources"
        )
    if any(member.currency != location.currency for member in members):
        raise ValueError(
            f"composite location {location.region!r} mixes currencies"
        )
    return sources


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
    nutrients_path: Path | str = DEFAULT_NUTRIENTS_PATH,
    use_promo: bool = True,
    locations: list[Location] | None = None,
) -> list[Food]:
    """Materialize Food records for every SKU that has a price at this location.

    SKUs without a price entry are skipped silently — they'll show up in the
    `validate` report instead.
    """
    foods: list[Food] = []
    sku_nutrients = load_sku_nutrients(nutrients_path)
    price_locations = price_locations_for(location, locations)
    for sku in skus:
        price_location = price_locations.get(sku.source)
        if price_location is None:
            continue
        price_row = prices.get((sku.product_id, price_location.location_id))
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
        fallback = fdc_mod.nutrients_per_g(fdc_payload)
        sku_row = sku_nutrients.get((sku.source, sku.product_id))
        nutrients, nutrient_sources = merge_with_usda_fallback(
            fallback, fdc_id=sku.fdc_id, sku_row=sku_row
        )

        foods.append(Food(
            sku_id=(
                f"{sku.source}:{sku.product_id}"
                if location.member_regions else sku.product_id
            ),
            name=sku.name,
            price_per_g=price_per_g,
            nutrients_per_g=nutrients,
            max_serving_g=sku.max_serving_g,
            dietary_categories=sku.dietary_categories,
            meta={
                "fdc_id": sku.fdc_id,
                "nutrient_sources": nutrient_sources,
                "sku_nutrition": ({
                    "upc": sku_row.get("upc"),
                    "serving_size_g": sku_row.get("serving_size_g"),
                    "serving_basis": sku_row.get("serving_basis"),
                    "source_details": sku_row.get("source_details") or {},
                } if sku_row else None),
                "unit_grams": sku.unit_grams,
                "price_regular": regular,
                "price_promo": promo,
                "price_used": chosen,
                "price_kind": (
                    "promo" if (use_promo and promo)
                    else price_row.get("price_kind", "regular")
                ),
                "location_id": price_location.location_id,
                "location_display": price_location.display,
                **({
                    "price_retailer": sku.source,
                    "solution_location_id": location.location_id,
                    "solution_location_display": location.display,
                } if location.member_regions else {}),
                "currency": location.currency,
                "price_scope": location.price_scope,
                "price_channel": price_row.get("channel"),
                "price_fetched_at": price_row.get("fetched_at"),
                "price_observed_at": price_row.get("observed_at"),
                "price_stale": bool(price_row.get("stale", False)),
                "price_source_url": price_row.get("source_url"),
            },
        ))
    return foods
