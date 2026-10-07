"""Costco.ca online prices from its product pages.

costco.ca product pages answer a plain HTTP client, resolve by item number
alone, and carry the online price in JSON-LD. That is the costco.ca price,
which Costco notes may differ from the warehouse's; items sold only in the
warehouse (eggs, produce) have no online price. Buying at either needs a
Costco membership, which these prices do not include.
"""

from __future__ import annotations

from diet.sources.product_page import ProductPageClient, Transport
from diet.util import http_request

COSTCO_PRODUCT_ROOT = "https://www.costco.ca/p/-/item/"
COSTCO_SOURCE = "costco_product_page"


class CostcoClient(ProductPageClient):
    def __init__(self, *, transport: Transport = http_request) -> None:
        super().__init__(COSTCO_PRODUCT_ROOT, COSTCO_SOURCE, transport=transport)
