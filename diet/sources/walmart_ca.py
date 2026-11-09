"""Walmart.ca reference prices from its product pages.

Walmart.ca product pages, including third-party marketplace listings, answer a
plain HTTP client sending a Firefox user agent. Requesting a few dozen pages
back to back gets the client's address redirected to a "Verify Your Identity"
page for a while, so requests are spaced WALMART_CA_MIN_INTERVAL seconds apart.
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
WALMART_CA_MIN_INTERVAL = 4.0

__all__ = ["WalmartCanadaClient", "WalmartCanadaError", "WalmartCanadaProtocolError"]


class WalmartCanadaClient(ProductPageClient):
    def __init__(self, *, transport: Transport = http_request, **pacing) -> None:
        pacing.setdefault("min_interval", WALMART_CA_MIN_INTERVAL)
        super().__init__(WALMART_CA_PRODUCT_ROOT, WALMART_CA_SOURCE, transport=transport, **pacing)

    def check_page(self, page: str) -> None:
        if "<title>Verify Your Identity" in page:
            raise WalmartCanadaError("blocked by Walmart's bot check (Verify Your Identity page)")
