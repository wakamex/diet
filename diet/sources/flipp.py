"""Regional grocery flyer items from Flipp's public app backend.

Flipp aggregates the weekly flyers of most Canadian grocery chains by postal
code.  The flyer listing and per-flyer item lists carry only a name and price;
each item's detail record adds the promotion terms (multi-buy prefix such as
``2/``, suffix such as ``or $3.99 EA.``, member-only price, sale story, PC
Optimum offers) and a click-through link to the retailer's online store.

``product_id`` is set only when the item's ``sku`` equals the product ID in
that link, as on Loblaw-banner and Walmart items.  Metro Inc. flyers use
internal ad codes as ``sku`` and their links often point at an unrelated
product (Tropicana juice linking to eggs), so their ``link_product_id`` is a
hint, not an identity.

Flyer items are promotions only.  An item's absence says nothing about a
product's shelf price, and a ``SELECTED VARIETIES`` item's product ID names a
single representative product.
"""

from __future__ import annotations

import json
import re
from collections.abc import Callable, Iterable
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from diet.sources.pc_express import normalize_postal_code
from diet.util import http_request, read_json, write_json_atomic

FLIPP_SOURCE = "flipp_flyers"
FLIPP_BASE = "https://backflipp.wishabi.com/flipp"
GROCERY_CATEGORY = "Groceries"
DEFAULT_MERCHANTS = (
    "Loblaws",
    "No Frills",
    "Real Canadian Superstore",
    "Metro",
    "Food Basics",
    "Walmart",
)

_MULTI_BUY = re.compile(r"^\s*(\d+)\s*/")
_MEMBER = re.compile(r"member|membre", re.IGNORECASE)
_PRODUCT_ID = re.compile(r"/(?:p|ip/[^/?]+)/([0-9A-Za-z_]+)")

Transport = Callable[..., tuple[int, dict[str, str], bytes]]


class FlippError(RuntimeError):
    """Transport or schema failure while reading Flipp."""


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _text(value: Any) -> str | None:
    text = " ".join(str(value).split()) if value is not None else ""
    return text or None


def _retailer_url(url: str | None) -> str | None:
    """Strip ad-tracker wrappers that embed the retailer URL after ``?``."""
    if not url:
        return None
    _, sep, inner = url.partition("?https://")
    return f"https://{inner}" if sep else url


def normalize_item(raw: dict[str, Any]) -> dict[str, Any]:
    """Flatten one Flipp item detail record into the snapshot schema."""
    price = _float(raw.get("current_price"))
    prefix = _text(raw.get("pre_price_text"))
    multi = _MULTI_BUY.match(prefix or "")
    quantity = int(multi.group(1)) if multi else None
    url = _retailer_url(raw.get("ttm_url"))
    link = _PRODUCT_ID.search(url or "")
    link_product_id = link.group(1) if link else None
    sku = _text(raw.get("sku"))
    return {
        "item_id": raw["id"],
        "flyer_id": raw["flyer_id"],
        "merchant": raw.get("merchant"),
        "name": _text(raw.get("name")),
        "brand": _text(raw.get("brand")),
        "description": _text(raw.get("description")),
        "product_id": link_product_id if sku and sku == link_product_id else None,
        "link_product_id": link_product_id,
        "price": price,
        "price_prefix": prefix,
        "price_suffix": _text(raw.get("price_text")),
        "original_price": _float(raw.get("original_price")),
        "sale_story": _text(raw.get("sale_story")),
        "multi_buy_quantity": quantity,
        "multi_buy_unit_price": (
            round(price / quantity, 2) if price is not None and quantity else None
        ),
        "member_only": bool(prefix and _MEMBER.search(prefix)),
        "in_store_only": bool(raw.get("in_store_only")),
        "disclaimer": _text(raw.get("disclaimer_text")),
        "valid_from": raw.get("valid_from"),
        "valid_to": raw.get("valid_to"),
        "url": url,
    }


class FlippClient:
    def __init__(self, *, transport: Transport = http_request, workers: int = 8):
        self.transport = transport
        self.workers = workers

    def _get(self, path: str) -> Any:
        url = f"{FLIPP_BASE}/{path}"
        try:
            status, _, body = self.transport(
                url, method="GET", headers={"Accept": "application/json"}, data=None
            )
        except Exception as exc:
            raise FlippError(f"GET {url} failed: {exc}") from exc
        if status != 200:
            raise FlippError(f"GET {url} returned HTTP {status}")
        try:
            return json.loads(body)
        except ValueError as exc:
            raise FlippError(f"GET {url} returned invalid JSON") from exc

    def list_flyers(self, postal_code: str) -> list[dict[str, Any]]:
        compact = normalize_postal_code(postal_code).replace(" ", "")
        payload = self._get(f"flyers?locale=en-ca&postal_code={compact}")
        flyers = payload.get("flyers") if isinstance(payload, dict) else None
        if not isinstance(flyers, list):
            raise FlippError("flyer listing has no flyers array")
        return flyers

    def flyer_items(self, flyer_id: int) -> list[dict[str, Any]]:
        """Return the detail record of every item in one flyer."""
        payload = self._get(f"flyers/{flyer_id}?locale=en-ca")
        items = payload.get("items") if isinstance(payload, dict) else None
        if not isinstance(items, list):
            raise FlippError(f"flyer {flyer_id} has no items array")
        with ThreadPoolExecutor(self.workers) as pool:
            return list(pool.map(self._item, (item["id"] for item in items)))

    def _item(self, item_id: int) -> dict[str, Any]:
        payload = self._get(f"items/{item_id}")
        item = payload.get("item") if isinstance(payload, dict) else None
        if not isinstance(item, dict):
            raise FlippError(f"item {item_id} has no item record")
        return item


def select_flyers(
    flyers: Iterable[dict[str, Any]], merchants: Iterable[str] | None
) -> list[dict[str, Any]]:
    """Keep grocery flyers, optionally only those of the named merchants."""
    wanted = {m.casefold() for m in merchants} if merchants else None
    return [
        flyer
        for flyer in flyers
        if GROCERY_CATEGORY in (flyer.get("categories") or [])
        and (wanted is None or str(flyer.get("merchant", "")).casefold() in wanted)
    ]


def pull_flyers(
    postal_code: str,
    *,
    merchants: Iterable[str] | None = DEFAULT_MERCHANTS,
    cache_root: Path,
    client: FlippClient | None = None,
) -> dict[str, Any]:
    """Snapshot every current grocery flyer item for a postal code.

    A flyer's items do not change once published, so each flyer's detail
    records are cached under ``cache_root/flyers/<id>.json`` and later pulls
    fetch only flyers they have not seen.
    """
    client = client or FlippClient()
    postal_code = normalize_postal_code(postal_code)
    observed_at = _utc_now()
    flyers = select_flyers(client.list_flyers(postal_code), merchants)

    flyer_rows: list[dict[str, Any]] = []
    items: list[dict[str, Any]] = []
    for flyer in flyers:
        cache = cache_root / "flyers" / f"{flyer['id']}.json"
        if cache.exists():
            raw_items = read_json(cache)
        else:
            raw_items = client.flyer_items(flyer["id"])
            write_json_atomic(cache, raw_items)
        flyer_rows.append({
            "flyer_id": flyer["id"],
            "merchant": flyer.get("merchant"),
            "valid_from": flyer.get("valid_from"),
            "valid_to": flyer.get("valid_to"),
            "item_count": len(raw_items),
        })
        items.extend(normalize_item(raw) for raw in raw_items)

    return {
        "source": FLIPP_SOURCE,
        "postal_code": postal_code,
        "observed_at": observed_at,
        "merchants": sorted(merchants) if merchants else None,
        "flyers": flyer_rows,
        "items": items,
    }
