"""Walmart.ca reference prices from its product pages.

Walmart.ca product pages, including third-party marketplace listings, answer a
plain HTTP client sending a Firefox user agent.
"""

from __future__ import annotations

from diet.sources.product_page import (
    ProductPageClient,
    ProductPageError as WalmartCanadaError,
    ProductPageProtocolError as WalmartCanadaProtocolError,
    Transport,
)
from diet.util import http_request

WALMART_CA_PRODUCT_ROOT = "https://www.walmart.ca/en/ip/"
WALMART_CA_SOURCE = "walmart_ca_product_page"

__all__ = ["WalmartCanadaClient", "WalmartCanadaError", "WalmartCanadaProtocolError"]


class WalmartCanadaClient(ProductPageClient):
    def __init__(self, *, transport: Transport = http_request) -> None:
        super().__init__(WALMART_CA_PRODUCT_ROOT, WALMART_CA_SOURCE, transport=transport)
