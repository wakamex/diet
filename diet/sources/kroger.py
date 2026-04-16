"""Kroger Public Products API client.

Auth: OAuth2 client_credentials (scope `product.compact`).
Rate limit: 10,000 calls/day across the `/products` endpoint.
Docs: https://developer.kroger.com/documentation/api-products/public/products/overview
"""

from __future__ import annotations

import base64
import os
import time
from dataclasses import dataclass
from pathlib import Path

from diet.util import http_get_json, http_post_form_json, write_json_atomic

KROGER_BASE = "https://api.kroger.com"
TOKEN_URL = f"{KROGER_BASE}/v1/connect/oauth2/token"
PRODUCTS_URL = f"{KROGER_BASE}/v1/products"

DEFAULT_SCOPE = "product.compact"
TOKEN_REFRESH_BUFFER_S = 60        # refresh if <= this much time remains


@dataclass
class KrogerClient:
    """Stateful client. Re-uses the OAuth token until it expires."""

    client_id: str
    client_secret: str
    scope: str = DEFAULT_SCOPE
    cache_dir: Path | None = None  # if set, cached token persists between runs

    _token: str | None = None
    _token_expires_at: float = 0.0  # epoch seconds

    @classmethod
    def from_env(cls, cache_dir: Path | None = None) -> "KrogerClient":
        cid = os.environ.get("KROGER_CLIENT_ID")
        secret = os.environ.get("KROGER_CLIENT_SECRET")
        if not cid or not secret:
            raise RuntimeError(
                "KROGER_CLIENT_ID / KROGER_CLIENT_SECRET must be set in env"
            )
        return cls(client_id=cid, client_secret=secret, cache_dir=cache_dir)

    # ---- auth ----------------------------------------------------------------

    def _basic_auth_header(self) -> str:
        creds = f"{self.client_id}:{self.client_secret}".encode()
        return "Basic " + base64.b64encode(creds).decode()

    def _refresh_token(self) -> None:
        payload = http_post_form_json(
            TOKEN_URL,
            form={"grant_type": "client_credentials", "scope": self.scope},
            headers={"Authorization": self._basic_auth_header()},
        )
        self._token = payload["access_token"]
        self._token_expires_at = time.time() + int(payload.get("expires_in", 1800))

    def _bearer(self) -> str:
        if self._token is None or time.time() + TOKEN_REFRESH_BUFFER_S >= self._token_expires_at:
            self._refresh_token()
        return f"Bearer {self._token}"

    # ---- API ----------------------------------------------------------------

    def _get(self, params: dict) -> dict:
        return http_get_json(
            PRODUCTS_URL,
            params=params,
            headers={"Accept": "application/json", "Authorization": self._bearer()},
        )

    def search(
        self,
        term: str,
        *,
        location_id: str | None = None,
        limit: int = 50,
        start: int = 0,
    ) -> dict:
        """Fuzzy term search. Order is non-deterministic across requests."""
        params: dict = {"filter.term": term, "filter.limit": limit, "filter.start": start}
        if location_id:
            params["filter.locationId"] = location_id
        return self._get(params)

    def lookup(
        self,
        product_ids: list[str],
        *,
        location_id: str | None = None,
    ) -> dict:
        """Exact lookup by productId. Up to 50 ids per call (API soft limit)."""
        if not product_ids:
            raise ValueError("product_ids must be non-empty")
        if len(product_ids) > 50:
            raise ValueError(f"too many product_ids ({len(product_ids)}); max 50")
        params: dict = {
            "filter.productId": ",".join(product_ids),
            "filter.limit": len(product_ids),
        }
        if location_id:
            params["filter.locationId"] = location_id
        return self._get(params)

    # ---- caching helpers ----------------------------------------------------

    def lookup_and_cache(
        self,
        product_ids: list[str],
        *,
        location_id: str,
        cache_root: Path,
        date_str: str,
    ) -> dict:
        """Fetch a batch and persist the raw JSON under cache_root/<date>/<loc>.json."""
        payload = self.lookup(product_ids, location_id=location_id)
        out = cache_root / date_str / f"{location_id}.json"
        write_json_atomic(out, payload)
        return payload


def extract_price(product: dict, *, prefer_promo: bool = True) -> tuple[float | None, float | None]:
    """Return (regular, promo) prices in $ from a product entry. None if unavailable."""
    items = product.get("items") or []
    if not items:
        return (None, None)
    price = (items[0].get("price") or {})
    regular = price.get("regular")
    promo = price.get("promo")
    if not promo:
        promo = None
    return (
        float(regular) if regular is not None else None,
        float(promo) if promo is not None else None,
    )


def effective_price(regular: float | None, promo: float | None) -> float | None:
    """Use promo when present and non-zero, else regular."""
    if promo is not None and promo > 0:
        return promo
    return regular
