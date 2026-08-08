"""Read-only client for the first-party PC Express MCP shopping endpoint.

PC Express powers several Loblaw banners, including Loblaws, Real Canadian
Superstore, and No Frills.  Its MCP endpoint does not require customer
credentials.  Product search may create an anonymous empty cart internally, but
this client intentionally exposes no cart mutation operations.

The product response supplies a current effective price but not package size or
a regular/promo split.  Callers must keep package size in separately verified
curated metadata before using a quote to calculate price per gram.
"""

from __future__ import annotations

import json
import math
import re
from collections.abc import Callable, Sequence
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

from diet.util import http_request

PC_EXPRESS_MCP_URL = "https://api.pcexpress.ca/v1/agents/mcp"
PC_EXPRESS_SOURCE = "pc_express_mcp"

_POSTAL_CODE = re.compile(r"^[A-Z]\d[A-Z]\d[A-Z]\d$")
_BANNER_ALIASES = {
    "loblaw": "loblaw",
    "loblaws": "loblaw",
    "superstore": "superstore",
    "realcanadiansuperstore": "superstore",
    "nofrills": "nofrills",
    "fortinos": "fortinos",
    "maxi": "maxi",
    "independent": "independent",
    "yourindependentgrocer": "independent",
    "valumart": "valumart",
    "zehrs": "zehrs",
    "rass": "rass",
    "realatlanticsuperstore": "rass",
    "provigo": "provigo",
    "independentcitymarket": "independentcitymarket",
    "dominion": "dominion",
    "wholesaleclub": "wholesaleclub",
}
_READ_ONLY_TOOLS = frozenset({"search_for_stores", "search_for_products"})

Transport = Callable[..., tuple[int, dict[str, str], bytes]]


class PCExpressError(RuntimeError):
    """Base error for PC Express transport, protocol, or validation failures."""


class PCExpressProtocolError(PCExpressError):
    """The endpoint returned a response that does not match the expected MCP shape."""


class PCExpressProductNotFound(PCExpressError):
    """A curated LIAM product ID was absent from a search response."""


def normalize_postal_code(value: str) -> str:
    """Validate and format a Canadian postal code as ``A1A 1A1``."""
    compact = re.sub(r"[\s-]+", "", value).upper()
    if not _POSTAL_CODE.fullmatch(compact):
        raise ValueError(f"invalid Canadian postal code: {value!r}")
    return f"{compact[:3]} {compact[3:]}"


def normalize_banner(value: str) -> str:
    """Return the canonical lowercase PC Express banner key."""
    compact = re.sub(r"[^a-z0-9]", "", value.lower())
    try:
        return _BANNER_ALIASES[compact]
    except KeyError as exc:
        choices = ", ".join(sorted(set(_BANNER_ALIASES.values())))
        raise ValueError(f"unsupported PC Express banner {value!r}; choose from {choices}") from exc


@dataclass(frozen=True)
class PCExpressStore:
    store_id: str
    name: str
    banner: str
    service_type: str
    postal_code: str
    address: str
    city: str
    province: str
    country: str
    source: str = PC_EXPRESS_SOURCE

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> "PCExpressStore":
        store_id = str(payload.get("store_id") or "").strip()
        name = str(payload.get("store_name") or "").strip()
        if not store_id or not name:
            raise PCExpressProtocolError("store response is missing store_id or store_name")
        postal = str(payload.get("postalCode") or "").strip()
        if postal:
            postal = normalize_postal_code(postal)
        return cls(
            store_id=store_id,
            name=name,
            banner=normalize_banner(str(payload.get("banner") or "")),
            service_type=str(payload.get("serviceType") or "unknown").lower(),
            postal_code=postal,
            address=str(payload.get("address") or "").strip(),
            city=str(payload.get("city") or "").strip(),
            province=str(payload.get("province") or "").strip(),
            country=str(payload.get("country") or "").strip(),
        )

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PCExpressProduct:
    product_id: str
    name: str
    brand: str | None
    effective_price_cad: float
    in_stock: bool | None
    image_url: str | None
    source: str = PC_EXPRESS_SOURCE

    @property
    def liam(self) -> str:
        """PC Express's stable line-item identifier."""
        return self.product_id

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> "PCExpressProduct":
        product_id = str(payload.get("liam") or "").strip()
        name = str(payload.get("name") or "").strip()
        price = payload.get("price")
        if not product_id or not name:
            raise PCExpressProtocolError("product response is missing liam or name")
        if isinstance(price, bool) or not isinstance(price, (int, float)):
            raise PCExpressProtocolError(f"product {product_id} has an invalid price")
        price = float(price)
        if not math.isfinite(price) or price <= 0:
            raise PCExpressProtocolError(f"product {product_id} has a non-positive price")
        stock = payload.get("in_stock")
        return cls(
            product_id=product_id,
            name=name,
            brand=(str(payload["brand"]).strip() if payload.get("brand") else None),
            effective_price_cad=price,
            in_stock=stock if isinstance(stock, bool) else None,
            image_url=(
                str(payload["image_url"]).strip() if payload.get("image_url") else None
            ),
        )

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PCExpressProductSearch:
    store_id: str
    banner: str
    terms: tuple[str, ...]
    products: tuple[PCExpressProduct, ...]
    observed_at: str
    channel: str = "pickup"
    source: str = PC_EXPRESS_SOURCE

    def as_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "store_id": self.store_id,
            "banner": self.banner,
            "channel": self.channel,
            "observed_at": self.observed_at,
            "terms": list(self.terms),
            "products": [product.as_dict() for product in self.products],
        }


@dataclass(frozen=True)
class PCExpressQuote:
    store_id: str
    banner: str
    product_id: str
    name: str
    brand: str | None
    effective_price_cad: float
    in_stock: bool | None
    image_url: str | None
    observed_at: str
    regular_price_cad: float | None = None
    promo_price_cad: float | None = None
    channel: str = "pickup"
    source: str = PC_EXPRESS_SOURCE
    source_url: str = PC_EXPRESS_MCP_URL

    @classmethod
    def from_search(
        cls, search: PCExpressProductSearch, product: PCExpressProduct
    ) -> "PCExpressQuote":
        return cls(
            store_id=search.store_id,
            banner=search.banner,
            product_id=product.product_id,
            name=product.name,
            brand=product.brand,
            effective_price_cad=product.effective_price_cad,
            in_stock=product.in_stock,
            image_url=product.image_url,
            observed_at=search.observed_at,
        )

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z")
    )


def _decode_sse_or_json(body: bytes) -> dict[str, Any]:
    """Decode either a plain JSON-RPC response or an SSE ``data:`` event."""
    try:
        text = body.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise PCExpressProtocolError("PC Express response was not UTF-8") from exc

    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        payload = None
    if isinstance(payload, dict):
        return payload

    events: list[dict[str, Any]] = []
    data_lines: list[str] = []

    def flush() -> None:
        if not data_lines:
            return
        event_data = "\n".join(data_lines)
        data_lines.clear()
        if event_data == "[DONE]":
            return
        try:
            event = json.loads(event_data)
        except json.JSONDecodeError as exc:
            raise PCExpressProtocolError("PC Express returned malformed SSE JSON") from exc
        if isinstance(event, dict):
            events.append(event)

    for line in text.splitlines():
        if not line:
            flush()
        elif line.startswith("data:"):
            data_lines.append(line[5:].lstrip())
    flush()

    if not events:
        raise PCExpressProtocolError("PC Express returned no JSON-RPC event")
    return events[-1]


def _structured_content(result: dict[str, Any]) -> dict[str, Any]:
    structured = result.get("structuredContent")
    if isinstance(structured, dict):
        return structured
    for item in result.get("content") or []:
        if not isinstance(item, dict) or item.get("type") != "text":
            continue
        try:
            parsed = json.loads(item.get("text") or "")
        except (TypeError, json.JSONDecodeError):
            continue
        if isinstance(parsed, dict):
            return parsed
    raise PCExpressProtocolError("PC Express result has no structured content")


@dataclass
class PCExpressClient:
    """Minimal MCP client exposing catalog reads but no cart mutations."""

    endpoint: str = PC_EXPRESS_MCP_URL
    transport: Transport = http_request
    _request_id: int = field(default=0, init=False, repr=False)

    def _rpc(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        self._request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self._request_id,
            "method": method,
            "params": params,
        }
        try:
            status, _headers, body = self.transport(
                self.endpoint,
                method="POST",
                headers={
                    "Accept": "application/json, text/event-stream",
                    "Content-Type": "application/json",
                },
                data=json.dumps(request, separators=(",", ":")).encode("utf-8"),
            )
        except (OSError, RuntimeError) as exc:
            raise PCExpressError(f"PC Express request failed: {exc}") from exc
        if not 200 <= status < 300:
            raise PCExpressError(f"PC Express request returned HTTP {status}")
        response = _decode_sse_or_json(body)
        if response.get("id") not in (None, self._request_id):
            raise PCExpressProtocolError(
                f"PC Express response id {response.get('id')!r} did not match request"
            )
        if "error" in response:
            error = response["error"]
            if isinstance(error, dict):
                message = error.get("message") or json.dumps(error, sort_keys=True)
            else:
                message = str(error)
            raise PCExpressError(f"PC Express MCP error: {message}")
        result = response.get("result")
        if not isinstance(result, dict):
            raise PCExpressProtocolError("PC Express response has no result object")
        if result.get("isError"):
            raise PCExpressError("PC Express tool reported an error")
        return result

    def _call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if name not in _READ_ONLY_TOOLS:
            raise ValueError(f"PC Express tool is not allowed by this client: {name}")
        result = self._rpc("tools/call", {"name": name, "arguments": arguments})
        return _structured_content(result)

    def search_stores(self, postal_code: str) -> list[PCExpressStore]:
        postal_code = normalize_postal_code(postal_code)
        payload = self._call_tool(
            "search_for_stores", {"postal_code": postal_code}
        )
        rows = payload.get("stores")
        if not isinstance(rows, list):
            widget = payload.get("_widget")
            rows = widget.get("stores") if isinstance(widget, dict) else None
        if not isinstance(rows, list):
            raise PCExpressProtocolError("store search result has no stores array")
        return [PCExpressStore.from_payload(row) for row in rows]

    def search_products(
        self,
        *,
        store_id: str,
        banner: str,
        terms: str | Sequence[str],
        postal_code: str | None = None,
        num_results: int = 10,
    ) -> PCExpressProductSearch:
        store_id = str(store_id).strip()
        if not store_id:
            raise ValueError("store_id must be non-empty")
        banner = normalize_banner(banner)
        if isinstance(terms, str):
            normalized_terms = (terms.strip(),)
        else:
            normalized_terms = tuple(str(term).strip() for term in terms)
        if not normalized_terms or any(not term for term in normalized_terms):
            raise ValueError("at least one non-empty product search term is required")
        if not 1 <= num_results <= 100:
            raise ValueError("num_results must be between 1 and 100")

        arguments: dict[str, Any] = {
            "store_id": store_id,
            "banner": banner.upper(),
            "term": list(normalized_terms),
            "num_results": num_results,
        }
        if postal_code is not None:
            arguments["postal_code"] = normalize_postal_code(postal_code)
        payload = self._call_tool("search_for_products", arguments)
        widget = payload.get("_widget")
        rows = widget.get("products") if isinstance(widget, dict) else None
        if not isinstance(rows, list):
            rows = payload.get("products")
        if not isinstance(rows, list):
            raise PCExpressProtocolError("product search result has no products array")
        return PCExpressProductSearch(
            store_id=store_id,
            banner=banner,
            terms=normalized_terms,
            products=tuple(PCExpressProduct.from_payload(row) for row in rows),
            observed_at=_utc_now(),
        )

    def quote_product(
        self,
        *,
        product_id: str,
        query: str,
        store_id: str,
        banner: str,
        postal_code: str | None = None,
        num_results: int = 100,
    ) -> PCExpressQuote:
        """Search and return only an exact curated LIAM product ID."""
        product_id = str(product_id).strip()
        if not product_id:
            raise ValueError("product_id must be non-empty")
        result = self.search_products(
            store_id=store_id,
            banner=banner,
            terms=query,
            postal_code=postal_code,
            num_results=num_results,
        )
        for product in result.products:
            if product.product_id == product_id:
                return PCExpressQuote.from_search(result, product)
        raise PCExpressProductNotFound(
            f"PC Express product {product_id!r} was not returned for query {query!r} "
            f"at store {store_id}"
        )
