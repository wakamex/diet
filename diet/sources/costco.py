"""Costco.ca online prices from its product pages.

costco.ca product pages answer a plain HTTP client, resolve by item number
alone, and carry the online price in JSON-LD. That is the costco.ca price,
which Costco notes may differ from the warehouse's; items sold only in the
warehouse (eggs, produce) have no online price. Buying at either needs a
Costco membership, which these prices do not include.

A current discount ("$3 OFF") is absent from the JSON-LD. The page's embedded
app data carries it as the item's `priceInfo.displayPrice`, whose
`deliveredPrice` is the online price after discounts.
"""

from __future__ import annotations

import json
import re

from diet.sources.product_page import ProductPageClient, Transport
from diet.util import http_request

COSTCO_PRODUCT_ROOT = "https://www.costco.ca/p/-/item/"
COSTCO_SOURCE = "costco_product_page"


class CostcoClient(ProductPageClient):
    def __init__(self, *, transport: Transport = http_request) -> None:
        super().__init__(COSTCO_PRODUCT_ROOT, COSTCO_SOURCE, transport=transport)

    def promo_price(self, page: str, product: dict, price_cad: float) -> float | None:
        sku = str(product.get("sku") or "")
        if not sku:
            return None
        # The app data is a JSON string inside a script, so its quotes are escaped.
        match = re.search(
            r'"priceInfo":\{"id":"' + re.escape(sku) + r'"[^{}]*"displayPrice":(\{[^{}]*\})',
            page.replace('\\"', '"'),
        )
        if not match:
            return None
        try:
            display = json.loads(match.group(1))
            online, delivered = float(display["onlinePrice"]), float(display["deliveredPrice"])
        except (KeyError, TypeError, ValueError):
            return None
        # Trust the discount only when it applies to the price JSON-LD reports.
        if abs(online - price_cad) > 0.005 or not 0 < delivered < online:
            return None
        return delivered
