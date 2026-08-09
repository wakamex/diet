"""Unlocalized Walmart.ca product-page reference prices.

Walmart.ca exposes the current online offer in server-rendered JSON-LD on each
product page.  The page has no explicit store context, so quotes from this
client are reference catalog prices rather than local or national prices.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from typing import Any
from urllib.parse import quote

from diet.util import http_request

WALMART_CA_PRODUCT_ROOT = "https://www.walmart.ca/en/ip/"
WALMART_CA_SOURCE = "walmart_ca_product_page"

Transport = Callable[..., tuple[int, dict[str, str], bytes]]


class WalmartCanadaError(RuntimeError):
    """The product page could not be fetched or validated."""


class WalmartCanadaProtocolError(WalmartCanadaError):
    """The product page no longer contains the expected structured offer."""


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace(
        "+00:00", "Z"
    )


class _JsonLdParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._capturing = False
        self._chunks: list[str] = []
        self.documents: list[Any] = []

    def handle_starttag(
        self, tag: str, attrs_list: list[tuple[str, str | None]]
    ) -> None:
        attrs = dict(attrs_list)
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self._capturing = True
            self._chunks = []

    def handle_data(self, data: str) -> None:
        if self._capturing:
            self._chunks.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag != "script" or not self._capturing:
            return
        self._capturing = False
        try:
            self.documents.append(json.loads("".join(self._chunks)))
        except json.JSONDecodeError:
            pass


def _objects(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from _objects(child)


@dataclass(frozen=True)
class WalmartCanadaQuote:
    product_id: str
    name: str
    effective_price_cad: float
    source_url: str
    observed_at: str
    availability: str | None = None
    currency: str = "CAD"
    price_scope: str = "reference"
    channel: str = "online_catalog"
    source: str = WALMART_CA_SOURCE

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class WalmartCanadaClient:
    def __init__(self, *, transport: Transport = http_request) -> None:
        self.transport = transport

    def quote_product(self, product_id: str) -> WalmartCanadaQuote:
        product_id = product_id.strip()
        if not product_id:
            raise ValueError("product ID must be non-empty")
        source_url = WALMART_CA_PRODUCT_ROOT + quote(product_id, safe="")
        try:
            status, _, body = self.transport(
                source_url,
                method="GET",
                headers={
                    "Accept": "text/html,application/xhtml+xml",
                    "Accept-Language": "en-CA,en;q=0.9",
                    "User-Agent": (
                        "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) "
                        "Gecko/20100101 Firefox/128.0"
                    ),
                },
                data=None,
            )
        except Exception as exc:
            raise WalmartCanadaError(f"request failed: {exc}") from exc
        if status != 200:
            raise WalmartCanadaError(f"HTTP {status}")

        parser = _JsonLdParser()
        parser.feed(body.decode("utf-8", errors="replace"))
        product = next(
            (
                item
                for document in parser.documents
                for item in _objects(document)
                if item.get("@type") == "Product"
            ),
            None,
        )
        if product is None:
            raise WalmartCanadaProtocolError("product JSON-LD not found")

        offers = product.get("offers")
        if isinstance(offers, dict):
            offers = [offers]
        offer = next(
            (
                item
                for item in (offers or [])
                if isinstance(item, dict) and item.get("price") is not None
            ),
            None,
        )
        if offer is None:
            raise WalmartCanadaProtocolError("current product offer not found")
        if str(offer.get("priceCurrency", "")).upper() != "CAD":
            raise WalmartCanadaProtocolError("product offer is not priced in CAD")
        try:
            price_cad = float(offer["price"])
        except (TypeError, ValueError) as exc:
            raise WalmartCanadaProtocolError("product offer has an invalid price") from exc
        if price_cad <= 0:
            raise WalmartCanadaProtocolError("product offer has a non-positive price")

        name = str(product.get("name") or "").strip()
        if not name:
            raise WalmartCanadaProtocolError("product JSON-LD has no name")
        return WalmartCanadaQuote(
            product_id=product_id,
            name=name,
            effective_price_cad=price_cad,
            source_url=str(offer.get("url") or source_url).split("?")[0],
            observed_at=_utc_now(),
            availability=offer.get("availability"),
        )
