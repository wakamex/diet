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
from diet.sources.kroger import KrogerClient, extract_price
from diet.sources.walmart import WalmartClient
from diet.supplements import as_sku_specs, load_supplements
from diet.util import write_json_atomic

DEFAULT_RAW_ROOT = Path("data/raw/kroger")
DEFAULT_WALMART_RAW_ROOT = Path("data/raw/walmart")
DEFAULT_OUT_PATH = Path("data/prices_current.json")
KROGER_BATCH_SIZE = 50


def _today_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _ingest_kroger(
    skus: list[SkuSpec],
    locations: list[Location],
    client: KrogerClient,
    raw_root: Path,
    today: str,
) -> tuple[list[dict], list[dict]]:
    """Existing Kroger path — batch productId lookup per location."""
    rows: list[dict] = []
    missing: list[dict] = []
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
            regular, promo = extract_price(product)
            if regular is None and promo is None:
                missing.append({"product_id": sku.product_id, "name": sku.name,
                                "location_id": loc.location_id, "reason": "no price"})
                continue
            rows.append({"product_id": sku.product_id, "location_id": loc.location_id,
                         "regular": regular, "promo": promo, "fetched_at": today})
    return rows, missing


def _ingest_walmart(
    skus: list[SkuSpec],
    locations: list[Location],
    client: WalmartClient,
    today: str,
) -> tuple[list[dict], list[dict]]:
    """Walmart Affiliate API — one product_details call per itemId. Affiliate
    returns national salePrice only (no per-store pricing without OPD approval)."""
    rows: list[dict] = []
    missing: list[dict] = []
    if not locations:
        return rows, missing
    # Walmart Affiliate has no location concept; one national price per SKU,
    # broadcast to every walmart-flagged location.
    for sku in skus:
        try:
            p = client.product_details(sku.product_id)
        except Exception as exc:
            for loc in locations:
                missing.append({"product_id": sku.product_id, "name": sku.name,
                                "location_id": loc.location_id,
                                "reason": f"walmart {type(exc).__name__}: {exc}"})
            continue
        price = p.get("salePrice")
        if price is None:
            for loc in locations:
                missing.append({"product_id": sku.product_id, "name": sku.name,
                                "location_id": loc.location_id,
                                "reason": "walmart no salePrice"})
            continue
        for loc in locations:
            rows.append({"product_id": sku.product_id, "location_id": loc.location_id,
                         "regular": float(price), "promo": None, "fetched_at": today})
    return rows, missing


def ingest(
    *,
    skus: list[SkuSpec] | None = None,
    locations: list[Location] | None = None,
    kroger_client: KrogerClient | None = None,
    walmart_client: WalmartClient | None = None,
    raw_root: Path = DEFAULT_RAW_ROOT,
    out_path: Path = DEFAULT_OUT_PATH,
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

    if kroger_skus and kroger_locs:
        kroger_client = kroger_client or KrogerClient.from_env()
        r, m = _ingest_kroger(kroger_skus, kroger_locs, kroger_client, raw_root, today)
        rows += r; missing += m
    if walmart_skus and walmart_locs:
        walmart_client = walmart_client or WalmartClient.from_env()
        r, m = _ingest_walmart(walmart_skus, walmart_locs, walmart_client, today)
        rows += r; missing += m

    payload = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "prices": rows,
        "missing": missing,
    }
    write_json_atomic(out_path, payload)
    return payload
