"""Unlocalized reference prices for Metro and Food Basics exact SKUs.

Both Metro Inc. banners expose the same read-only batch-SKU storefront surface,
with a banner-specific URL.  It returns server-rendered product tiles rather
than JSON.  The response has no store identity and must therefore be treated as
a reference catalog price, never as a local or chain-wide minimum price.
"""

from __future__ import annotations

import json
import math
import re
from collections.abc import Callable
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from typing import Any
from urllib.parse import urlencode, urljoin

from diet.util import http_request

METRO_REFERENCE_SOURCE = "metro_inc_reference_catalog"
REFERENCE_BATCH_SIZE = 20

_RETAILERS = {
    "metro": {
        "endpoint": "https://www.metro.ca/en/online-grocery/product/skus",
        "search_endpoint": "https://www.metro.ca/en/autocompleteSearchProducts",
        "base_url": "https://www.metro.ca",
    },
    "foodbasics": {
        "endpoint": "https://www.foodbasics.ca/product/skus",
        "search_endpoint": "https://www.foodbasics.ca/autocompleteSearchProducts",
        "base_url": "https://www.foodbasics.ca",
    },
}
_RETAILER_ALIASES = {
    "metro": "metro",
    "foodbasics": "foodbasics",
    "foodbasic": "foodbasics",
}
_PRICE = re.compile(r"\$\s*([0-9]+(?:\.[0-9]{1,2})?)")
_UNIT_PRICE = re.compile(
    r"\$\s*([0-9]+(?:\.[0-9]{1,2})?)\s*/\s*(?:([0-9.]+)\s*)?([A-Za-z]+)",
    re.IGNORECASE,
)
_VOID_TAGS = frozenset({
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
    "meta", "param", "source", "track", "wbr",
})

Transport = Callable[..., tuple[int, dict[str, str], bytes]]


class MetroReferenceError(RuntimeError):
    """Base error for reference-price transport or validation failures."""


class MetroReferenceProtocolError(MetroReferenceError):
    """The storefront response no longer matches the expected product tiles."""


class MetroReferenceProductNotFound(MetroReferenceError):
    """An exact requested product ID was absent from the response."""


def normalize_retailer(value: str) -> str:
    """Normalize a supported Metro Inc. banner name."""
    compact = re.sub(r"[^a-z]", "", value.lower())
    try:
        return _RETAILER_ALIASES[compact]
    except KeyError as exc:
        raise ValueError("unsupported retailer; choose metro or foodbasics") from exc


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _parse_price(text: str) -> float | None:
    match = _PRICE.search(text)
    return float(match.group(1)) if match else None


@dataclass(frozen=True)
class MetroReferenceQuote:
    retailer: str
    product_id: str
    name: str
    brand: str | None
    package: str | None
    effective_price_cad: float
    regular_price_cad: float | None
    promo_price_cad: float | None
    unit_price_cad: float | None
    unit_quantity: float | None
    unit_measure: str | None
    is_weighted: bool | None
    source_url: str | None
    image_url: str | None
    observed_at: str
    price_scope: str = "reference"
    channel: str = "online_catalog"
    source: str = METRO_REFERENCE_SOURCE

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MetroReferenceResult:
    retailer: str
    requested_product_ids: tuple[str, ...]
    quotes: tuple[MetroReferenceQuote, ...]
    missing_product_ids: tuple[str, ...]
    observed_at: str
    endpoint: str
    price_scope: str = "reference"
    source: str = METRO_REFERENCE_SOURCE

    def as_dict(self) -> dict[str, Any]:
        return {
            "retailer": self.retailer,
            "price_scope": self.price_scope,
            "source": self.source,
            "endpoint": self.endpoint,
            "observed_at": self.observed_at,
            "requested_product_ids": list(self.requested_product_ids),
            "quotes": [quote.as_dict() for quote in self.quotes],
            "missing_product_ids": list(self.missing_product_ids),
        }


@dataclass(frozen=True)
class MetroReferenceSearch:
    retailer: str
    query: str
    quotes: tuple[MetroReferenceQuote, ...]
    observed_at: str
    endpoint: str
    price_scope: str = "reference"
    source: str = METRO_REFERENCE_SOURCE

    def as_dict(self) -> dict[str, Any]:
        return {
            "retailer": self.retailer,
            "query": self.query,
            "price_scope": self.price_scope,
            "source": self.source,
            "endpoint": self.endpoint,
            "observed_at": self.observed_at,
            "quotes": [quote.as_dict() for quote in self.quotes],
        }


@dataclass
class _Tile:
    product_id: str
    name: str
    brand: str | None
    effective_price: float | None
    is_weighted: bool | None
    package: str | None = None
    regular_price: float | None = None
    unit_price_text: str | None = None
    product_url: str | None = None
    image_url: str | None = None


@dataclass
class _Capture:
    tag: str
    depth: int
    field: str
    chunks: list[str]


class _ProductTileParser(HTMLParser):
    """Parse only the stable semantic fields inside product tile fragments."""

    def __init__(self, *, base_url: str):
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.tiles: list[_Tile] = []
        self.tile: _Tile | None = None
        self.depth = 0
        self.captures: list[_Capture] = []

    @staticmethod
    def _classes(attrs: dict[str, str | None]) -> set[str]:
        return set((attrs.get("class") or "").split())

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = dict(attrs_list)
        classes = self._classes(attrs)
        if self.tile is None:
            product_id = (attrs.get("data-product-code") or "").strip()
            if tag == "div" and product_id and "default-product-tile" in classes:
                raw_price = attrs.get("data-main-price")
                raw_weighted = attrs.get("data-is-weighted")
                self.tile = _Tile(
                    product_id=product_id,
                    name=(attrs.get("data-product-name") or "").strip(),
                    brand=(attrs.get("data-product-brand") or "").strip() or None,
                    effective_price=float(raw_price) if raw_price else None,
                    is_weighted=(
                        raw_weighted.lower() == "true" if raw_weighted else None
                    ),
                )
                self.depth = 1
            return

        if tag not in _VOID_TAGS:
            self.depth += 1

        if tag == "div" and attrs.get("data-main-price"):
            try:
                self.tile.effective_price = float(attrs["data-main-price"] or "")
            except ValueError as exc:
                raise MetroReferenceProtocolError(
                    f"product {self.tile.product_id} has an invalid effective price"
                ) from exc

        capture_field = None
        if tag == "span" and "head__brand" in classes:
            capture_field = "brand"
        elif tag == "span" and "head__title" in classes:
            capture_field = "name"
        elif tag == "span" and "head__unit-details" in classes:
            capture_field = "package"
        elif tag == "div" and "pricing__before-price" in classes:
            capture_field = "regular_price"
        elif tag == "div" and "pricing__secondary-price" in classes:
            capture_field = "unit_price_text"
        if capture_field is not None:
            self.captures.append(_Capture(tag, self.depth, capture_field, []))

        if tag == "a" and "product-details-link" in classes and not self.tile.product_url:
            href = (attrs.get("href") or "").strip()
            if href:
                self.tile.product_url = urljoin(self.base_url, href)
        elif tag == "img" and not self.tile.image_url:
            src = (attrs.get("src") or "").strip()
            if src and "heart" not in src and "icon-" not in src:
                self.tile.image_url = urljoin(self.base_url, src)

    def handle_data(self, data: str) -> None:
        for capture in self.captures:
            capture.chunks.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self.tile is None:
            return

        finished = [
            capture
            for capture in self.captures
            if capture.tag == tag and capture.depth == self.depth
        ]
        for capture in finished:
            text = " ".join("".join(capture.chunks).split())
            if capture.field == "regular_price":
                self.tile.regular_price = _parse_price(text)
            else:
                setattr(self.tile, capture.field, text or None)
            self.captures.remove(capture)

        if tag == "div" and self.depth == 1:
            self.tiles.append(self.tile)
            self.tile = None
            self.captures.clear()
            self.depth = 0
        elif tag not in _VOID_TAGS:
            self.depth -= 1


def _quotes_from_html(
    body: bytes, *, retailer: str, base_url: str, observed_at: str
) -> list[MetroReferenceQuote]:
    try:
        text = body.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise MetroReferenceProtocolError("reference response was not UTF-8") from exc
    parser = _ProductTileParser(base_url=base_url)
    try:
        parser.feed(text)
        parser.close()
    except MetroReferenceProtocolError:
        raise
    except (TypeError, ValueError) as exc:
        raise MetroReferenceProtocolError("reference response contained invalid product data") from exc

    quotes: list[MetroReferenceQuote] = []
    for tile in parser.tiles:
        price = tile.effective_price
        if not tile.name or price is None or not math.isfinite(price) or price <= 0:
            raise MetroReferenceProtocolError(
                f"product {tile.product_id} is missing a name or valid effective price"
            )
        regular = tile.regular_price
        promo = price if regular is not None and price < regular else None
        unit_price = unit_quantity = None
        unit_measure = None
        if tile.unit_price_text:
            match = _UNIT_PRICE.search(tile.unit_price_text)
            if match:
                unit_price = float(match.group(1))
                unit_quantity = float(match.group(2) or 1)
                unit_measure = match.group(3).lower()
        quotes.append(MetroReferenceQuote(
            retailer=retailer,
            product_id=tile.product_id,
            name=tile.name,
            brand=tile.brand,
            package=tile.package,
            effective_price_cad=price,
            regular_price_cad=regular,
            promo_price_cad=promo,
            unit_price_cad=unit_price,
            unit_quantity=unit_quantity,
            unit_measure=unit_measure,
            is_weighted=tile.is_weighted,
            source_url=tile.product_url,
            image_url=tile.image_url,
            observed_at=observed_at,
        ))
    return quotes


@dataclass
class MetroReferenceClient:
    """Read exact SKU prices from one Metro Inc. banner's default catalog."""

    retailer: str
    transport: Transport = http_request
    batch_size: int = REFERENCE_BATCH_SIZE

    def __post_init__(self) -> None:
        self.retailer = normalize_retailer(self.retailer)
        if self.batch_size < 1:
            raise ValueError("batch_size must be positive")

    @property
    def endpoint(self) -> str:
        return _RETAILERS[self.retailer]["endpoint"]

    @property
    def search_endpoint(self) -> str:
        return _RETAILERS[self.retailer]["search_endpoint"]

    def _post(self, url: str, *, body: bytes | None = None) -> bytes:
        headers = {"Accept": "text/html, */*"}
        if body is None:
            body = b""
            headers["X-Requested-With"] = "XMLHttpRequest"
        else:
            headers["Content-Type"] = "application/json"
        try:
            status, _headers, response_body = self.transport(
                url,
                method="POST",
                headers=headers,
                data=body,
            )
        except (OSError, RuntimeError) as exc:
            raise MetroReferenceError(
                f"{self.retailer} reference request failed: {exc}"
            ) from exc
        if not 200 <= status < 300:
            raise MetroReferenceError(
                f"{self.retailer} reference request returned HTTP {status}"
            )
        return response_body

    def search_products(self, query: str) -> MetroReferenceSearch:
        """Return ranked default-catalog candidates for one discovery query."""
        query = str(query).strip()
        if not query:
            raise ValueError("a non-empty product search query is required")
        url = f"{self.search_endpoint}?{urlencode({
            'freeText': query,
            'tabletMobile': 'false',
            'previousSuggestion': '',
        })}"
        observed_at = _utc_now()
        body = self._post(url)
        quotes = _quotes_from_html(
            body,
            retailer=self.retailer,
            base_url=_RETAILERS[self.retailer]["base_url"],
            observed_at=observed_at,
        )
        return MetroReferenceSearch(
            retailer=self.retailer,
            query=query,
            quotes=tuple(quotes),
            observed_at=observed_at,
            endpoint=self.search_endpoint,
        )

    def quote_products(self, product_ids: list[str] | tuple[str, ...]) -> MetroReferenceResult:
        requested = tuple(dict.fromkeys(str(value).strip() for value in product_ids))
        if not requested or any(not value for value in requested):
            raise ValueError("at least one non-empty product ID is required")

        observed_at = _utc_now()
        parsed: list[MetroReferenceQuote] = []
        for offset in range(0, len(requested), self.batch_size):
            batch = requested[offset:offset + self.batch_size]
            request_body = json.dumps(
                {"productIds": list(batch)}, separators=(",", ":")
            ).encode("utf-8")
            body = self._post(self.endpoint, body=request_body)
            parsed.extend(_quotes_from_html(
                body,
                retailer=self.retailer,
                base_url=_RETAILERS[self.retailer]["base_url"],
                observed_at=observed_at,
            ))
        by_id = {quote.product_id: quote for quote in parsed}
        quotes = tuple(by_id[product_id] for product_id in requested if product_id in by_id)
        missing = tuple(product_id for product_id in requested if product_id not in by_id)
        return MetroReferenceResult(
            retailer=self.retailer,
            requested_product_ids=requested,
            quotes=quotes,
            missing_product_ids=missing,
            observed_at=observed_at,
            endpoint=self.endpoint,
        )

    def quote_product(self, product_id: str) -> MetroReferenceQuote:
        result = self.quote_products([product_id])
        if not result.quotes:
            raise MetroReferenceProductNotFound(
                f"{self.retailer} reference product {product_id!r} was not returned"
            )
        return result.quotes[0]
