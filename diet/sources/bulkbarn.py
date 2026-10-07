"""Bulk Barn prices from its online-ordering catalog.

The online-ordering page (bulkbarn.ca/ecomm/product_search.html) loads every
item from one script, product_data.js, refreshed daily. Each item carries its
bin number (BBPLU) and regular price per 100 g; these matched 46 of 49 shelf
labels photographed in an Ottawa store on 2026-10-06 (the three misses were
stone-ground flours). Prices are reference prices, not a particular store's.

Sales are the online-order prices. The order form shows, and its cart
charges, an item's Sale_Price (per kg) whenever today falls between its sale
start and end dates; at pickup only the weight changes. Those sales are not
in-store sales: they matched all five sale tags in those photos, but also
cover 22 photographed bins whose tags showed none, so a sale here is the price
for ordering online and picking up, not for buying at the bin.
"""

from __future__ import annotations

import html
import re
from collections.abc import Callable
from dataclasses import dataclass
from datetime import date, datetime

from diet.util import http_request

CATALOG_URL = "https://www.bulkbarn.ca/ecomm/product_data.js"
BULKBARN_SOURCE = "bulkbarn_online_catalog"

# url -> (status, headers, body)
Transport = Callable[..., tuple[int, dict[str, str], bytes]]

_ITEM = re.compile(r"\{[^{}]*\}")
_FIELD = re.compile(r'"(\w+)"\s*:\s*"([^"]*)"')


class BulkBarnError(RuntimeError):
    """The catalog could not be fetched or parsed."""


@dataclass(frozen=True)
class CatalogItem:
    plu: str
    name: str
    regular: float  # CAD per 100 g
    sale: float | None = None  # CAD per 100 g, for online orders
    sale_start: date | None = None
    sale_end: date | None = None

    def sale_on(self, today: date) -> float | None:
        """The online-order sale price in effect on `today`, as the order form decides it."""
        if self.sale is None or self.sale_start is None or self.sale_end is None:
            return None
        if not self.sale_start <= today <= self.sale_end or self.sale >= self.regular:
            return None
        return self.sale


def _sale_date(text: str | None) -> date | None:
    for fmt in ("%m/%d/%Y %H:%M", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime((text or "").strip(), fmt).date()
        except ValueError:
            continue
    return None


def parse_catalog(text: str) -> dict[str, CatalogItem]:
    items: dict[str, CatalogItem] = {}
    for block in _ITEM.findall(text):
        fields = dict(_FIELD.findall(block))
        plu, price = fields.get("BBPLU"), fields.get("Retail_Price_100g")
        if not plu or not price:
            continue
        try:
            regular = float(price)
        except ValueError:
            continue
        if regular <= 0:
            continue
        try:
            sale = round(float(fields.get("Sale_Price") or 0) / 10, 4)  # per kg, as every priced bin is sold
        except ValueError:
            sale = 0
        items[plu] = CatalogItem(
            plu,
            html.unescape(fields.get("Product_name_EN", "")),
            regular,
            sale=sale if sale > 0 else None,
            sale_start=_sale_date(fields.get("Sale_Start_Date")),
            sale_end=_sale_date(fields.get("Sale_End_Date")),
        )
    if not items:
        raise BulkBarnError("catalog has no priced items; its format may have changed")
    return items


def fetch_catalog(transport: Transport = http_request) -> tuple[dict[str, CatalogItem], str]:
    """The priced items and the catalog's own update stamp."""
    try:
        status, _, body = transport(CATALOG_URL)
    except Exception as exc:
        raise BulkBarnError(f"catalog request failed: {exc}") from exc
    if status != 200:
        raise BulkBarnError(f"catalog request returned HTTP {status}")
    text = body.decode("utf-8", errors="replace")
    stamp = re.search(r'"timeStamp",\s*"([^"]+)"', text)
    return parse_catalog(text), stamp.group(1) if stamp else ""
