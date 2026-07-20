"""Daily ingest: refresh prices for every (sku × location), write prices_current.json.

Routes each SKU to its source's API (Kroger Products API or Walmart.io Affiliate
Product Details) based on the SkuSpec.source field. Walmart Affiliate only has
national pricing, so the single `walmart_national` location pulls one price per
Walmart SKU.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from diet.foods import Location, SkuSpec, load_all_skus, load_locations
from diet.nutrition import (
    extract_fdc_branded_nutrition,
    extract_kroger_nutrition,
    load_sku_nutrients,
)
from diet.sources import fdc as fdc_mod
from diet.sources.kroger import KrogerClient, extract_price
from diet.sources.walmart import WalmartClient
from diet.supplements import as_sku_specs, load_supplements
from diet.util import write_json_atomic

DEFAULT_RAW_ROOT = Path("data/raw/kroger")
DEFAULT_WALMART_RAW_ROOT = Path("data/raw/walmart")
DEFAULT_OUT_PATH = Path("data/prices_current.json")
DEFAULT_NUTRIENTS_OUT_PATH = Path("data/nutrients_current.json")
DEFAULT_FDC_CACHE = Path("data/raw/fdc")
KROGER_BATCH_SIZE = 50


def _today_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _ingest_kroger(
    skus: list[SkuSpec],
    locations: list[Location],
    client: KrogerClient,
    raw_root: Path,
    today: str,
) -> tuple[list[dict], list[dict], list[dict], list[dict]]:
    """Existing Kroger path — batch productId lookup per location."""
    rows: list[dict] = []
    missing: list[dict] = []
    nutrient_rows: dict[tuple[str, str], dict] = {}
    nutrition_attempted: set[tuple[str, str]] = set()
    warnings: list[dict] = []
    for loc in locations:
        product_ids = [s.product_id for s in skus]
        merged_data: list[dict] = []
        for i in range(0, len(product_ids), KROGER_BATCH_SIZE):
            batch = product_ids[i:i + KROGER_BATCH_SIZE]
            payload = client.lookup_and_cache(
                batch, location_id=loc.location_id,
                cache_root=raw_root, date_str=today,
            )
            merged_data.extend(payload.get("data") or [])
        by_id = {p.get("productId"): p for p in merged_data if p.get("productId")}
        for sku in skus:
            product = by_id.get(sku.product_id)
            if product is None:
                missing.append({"product_id": sku.product_id, "name": sku.name,
                                "location_id": loc.location_id, "reason": "not returned"})
                continue
            nutrient_key = (sku.source, sku.product_id)
            if sku.fdc_id and nutrient_key not in nutrition_attempted:
                nutrition_attempted.add(nutrient_key)
                nutrition, issues = extract_kroger_nutrition(
                    product,
                    product_id=sku.product_id,
                    package_grams=sku.unit_grams,
                    fetched_at=today,
                )
                if nutrition:
                    nutrient_rows[nutrient_key] = nutrition
                for issue in issues:
                    warnings.append({
                        "product_id": sku.product_id,
                        "source": sku.source,
                        "warning": issue,
                    })
            regular, promo = extract_price(product)
            if regular is None and promo is None:
                missing.append({"product_id": sku.product_id, "name": sku.name,
                                "location_id": loc.location_id, "reason": "no price"})
                continue
            rows.append({"product_id": sku.product_id, "location_id": loc.location_id,
                         "regular": regular, "promo": promo, "fetched_at": today})
    return rows, missing, list(nutrient_rows.values()), warnings


def _ingest_walmart(
    skus: list[SkuSpec],
    locations: list[Location],
    client: WalmartClient,
    today: str,
    raw_root: Path,
    fdc_cache: Path,
) -> tuple[list[dict], list[dict], list[dict], list[dict]]:
    """Walmart Affiliate API — one product-details call per SKU and location.

    The synthetic ``walmart-national`` location omits storeId. Numeric Walmart
    location IDs are passed through so returned salePrice is store-scoped.
    """
    rows: list[dict] = []
    missing: list[dict] = []
    nutrient_rows: list[dict] = []
    warnings: list[dict] = []
    if not locations:
        return rows, missing, nutrient_rows, warnings
    for sku in skus:
        nutrition_attempted = False
        for loc in locations:
            store_id = None if loc.location_id == "walmart-national" else loc.location_id
            try:
                p = client.product_details(sku.product_id, store_id=store_id)
                write_json_atomic(
                    raw_root / today / loc.location_id / f"{sku.product_id}.json", p
                )
            except Exception as exc:
                missing.append({"product_id": sku.product_id, "name": sku.name,
                                "location_id": loc.location_id,
                                "reason": f"walmart {type(exc).__name__}: {exc}"})
                continue
            if sku.fdc_id and not nutrition_attempted:
                nutrition_attempted = True
                upc = str(p.get("upc") or "")
                if upc:
                    try:
                        branded = fdc_mod.search_branded_upc_cached(upc, fdc_cache)
                    except Exception as exc:
                        warnings.append({
                            "product_id": sku.product_id,
                            "source": sku.source,
                            "warning": f"USDA branded UPC lookup failed: {type(exc).__name__}: {exc}",
                        })
                    else:
                        if branded:
                            nutrition = extract_fdc_branded_nutrition(
                                branded,
                                product_id=sku.product_id,
                                source=sku.source,
                                upc=upc,
                                fetched_at=today,
                            )
                            if nutrition:
                                nutrient_rows.append(nutrition)
                            else:
                                warnings.append({
                                    "product_id": sku.product_id,
                                    "source": sku.source,
                                    "warning": "exact USDA Branded record has no mapped nutrients",
                                })
                        else:
                            warnings.append({
                                "product_id": sku.product_id,
                                "source": sku.source,
                                "warning": f"no exact USDA Branded match for UPC {upc}",
                            })
                else:
                    warnings.append({
                        "product_id": sku.product_id,
                        "source": sku.source,
                        "warning": "Walmart product has no UPC for exact USDA match",
                    })
            price = p.get("salePrice")
            if price is None:
                missing.append({"product_id": sku.product_id, "name": sku.name,
                                "location_id": loc.location_id,
                                "reason": "walmart no salePrice"})
                continue
            rows.append({"product_id": sku.product_id, "location_id": loc.location_id,
                         "regular": float(price), "promo": None, "fetched_at": today})
    return rows, missing, nutrient_rows, warnings


def ingest(
    *,
    skus: list[SkuSpec] | None = None,
    locations: list[Location] | None = None,
    kroger_client: KrogerClient | None = None,
    walmart_client: WalmartClient | None = None,
    raw_root: Path = DEFAULT_RAW_ROOT,
    walmart_raw_root: Path = DEFAULT_WALMART_RAW_ROOT,
    fdc_cache: Path = DEFAULT_FDC_CACHE,
    out_path: Path = DEFAULT_OUT_PATH,
    nutrients_out_path: Path = DEFAULT_NUTRIENTS_OUT_PATH,
) -> dict:
    skus = skus or load_all_skus()
    locations = locations or load_locations()
    supplements_path = Path("data/supplements.yaml")
    if supplements_path.exists():
        skus = list(skus) + as_sku_specs(load_supplements(supplements_path))
    today = _today_str()

    kroger_skus = [s for s in skus if s.source == "kroger"]
    walmart_skus = [s for s in skus if s.source == "walmart"]
    kroger_locs = [l for l in locations if l.source == "kroger"]
    walmart_locs = [l for l in locations if l.source == "walmart"]

    rows: list[dict] = []
    missing: list[dict] = []
    nutrient_rows: list[dict] = []
    nutrient_warnings: list[dict] = []

    if kroger_skus and kroger_locs:
        kroger_client = kroger_client or KrogerClient.from_env()
        r, m, n, w = _ingest_kroger(
            kroger_skus, kroger_locs, kroger_client, raw_root, today
        )
        rows += r; missing += m; nutrient_rows += n; nutrient_warnings += w
    if walmart_skus and walmart_locs:
        walmart_client = walmart_client or WalmartClient.from_env()
        r, m, n, w = _ingest_walmart(
            walmart_skus, walmart_locs, walmart_client, today,
            walmart_raw_root, fdc_cache,
        )
        rows += r; missing += m; nutrient_rows += n; nutrient_warnings += w

    payload = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "prices": rows,
        "missing": missing,
    }
    write_json_atomic(out_path, payload)
    # Nutrition changes much less often than price and a product API can be
    # transiently unavailable. Retain the last exact-SKU snapshot for still-
    # curated foods, then overlay every record refreshed successfully today.
    valid_nutrient_keys = {
        (sku.source, sku.product_id) for sku in skus if sku.fdc_id
    }
    effective_nutrients = {
        key: row for key, row in load_sku_nutrients(nutrients_out_path).items()
        if key in valid_nutrient_keys
    }
    for row in nutrient_rows:
        effective_nutrients[(row["source"], row["product_id"])] = row
    nutrition_payload = {
        "updated": payload["updated"],
        "nutrients": sorted(
            effective_nutrients.values(),
            key=lambda row: (row["source"], row["product_id"]),
        ),
        "warnings": nutrient_warnings,
    }
    write_json_atomic(nutrients_out_path, nutrition_payload)
    payload["nutrients"] = nutrition_payload["nutrients"]
    payload["nutrient_warnings"] = nutrient_warnings
    return payload
