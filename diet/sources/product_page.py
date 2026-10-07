"""Reference prices from retailers' product pages.

Walmart.ca and costco.ca expose the current online offer in server-rendered
JSON-LD on each product page, reachable by product ID alone.  The pages have
no explicit store context, so quotes from this client are reference catalog
prices rather than local or national prices.
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


Transport = Callable[..., tuple[int, dict[str, str], bytes]]


class ProductPageError(RuntimeError):
    """The product page could not be fetched or validated."""


class ProductPageProtocolError(ProductPageError):
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
class ProductPageQuote:
    product_id: str
    name: str
    effective_price_cad: float
    source_url: str
    observed_at: str
    source: str
    availability: str | None = None
    currency: str = "CAD"
    price_scope: str = "reference"
    channel: str = "online_catalog"

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class ProductPageClient:
    """Quote a retailer's products from their pages at `product_root` + product ID."""

    def __init__(self, product_root: str, source: str, *, transport: Transport = http_request) -> None:
        self.product_root = product_root
        self.source = source
        self.transport = transport

    def quote_product(self, product_id: str) -> ProductPageQuote:
        product_id = product_id.strip()
        if not product_id:
            raise ValueError("product ID must be non-empty")
        source_url = self.product_root + quote(product_id, safe="")
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
            raise ProductPageError(f"request failed: {exc}") from exc
        if status != 200:
            raise ProductPageError(f"HTTP {status}")

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
            raise ProductPageProtocolError("product JSON-LD not found")

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
            raise ProductPageProtocolError("current product offer not found")
        if str(offer.get("priceCurrency", "")).upper() != "CAD":
            raise ProductPageProtocolError("product offer is not priced in CAD")
        try:
            price_cad = float(offer["price"])
        except (TypeError, ValueError) as exc:
            raise ProductPageProtocolError("product offer has an invalid price") from exc
        if price_cad <= 0:
            raise ProductPageProtocolError("product offer has a non-positive price")

        name = str(product.get("name") or "").strip()
        if not name:
            raise ProductPageProtocolError("product JSON-LD has no name")
        return ProductPageQuote(
            product_id=product_id,
            name=name,
            effective_price_cad=price_cad,
            source_url=str(offer.get("url") or source_url).split("?")[0],
            observed_at=_utc_now(),
            availability=offer.get("availability"),
            source=self.source,
        )
