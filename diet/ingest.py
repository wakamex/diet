"""Daily ingest: refresh Kroger prices for every (sku × location), write prices_current.json."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from diet.foods import Location, SkuSpec, load_locations, load_skus
from diet.sources.kroger import KrogerClient, extract_price
from diet.util import write_json_atomic

DEFAULT_RAW_ROOT = Path("data/raw/kroger")
DEFAULT_OUT_PATH = Path("data/prices_current.json")
BATCH_SIZE = 50


def _today_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def ingest(
    *,
    skus: list[SkuSpec] | None = None,
    locations: list[Location] | None = None,
    client: KrogerClient | None = None,
    raw_root: Path = DEFAULT_RAW_ROOT,
    out_path: Path = DEFAULT_OUT_PATH,
) -> dict:
    """Pull current Kroger prices. Writes raw JSON per (date × location) and a flat
    `prices_current.json` consumed by the solver pipeline."""
    skus = skus or load_skus()
    locations = locations or load_locations()
    client = client or KrogerClient.from_env()

    today = _today_str()
    rows: list[dict] = []
    missing: list[dict] = []

    for loc in locations:
        # Batch productIds so we stay under Kroger's per-call lookup limit.
        product_ids = [s.product_id for s in skus]
        merged_data: list[dict] = []
        for i in range(0, len(product_ids), BATCH_SIZE):
            batch = product_ids[i:i + BATCH_SIZE]
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
            rows.append({
                "product_id": sku.product_id,
                "location_id": loc.location_id,
                "regular": regular,
                "promo": promo,
                "fetched_at": today,
            })

    payload = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "prices": rows,
        "missing": missing,
    }
    write_json_atomic(out_path, payload)
    return payload
