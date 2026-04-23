"""Walmart.io API client — RSA-SHA256 signed requests.

Walmart.io signs every request with an RSA-SHA256 signature over
  consumer_id + "\\n" + timestamp_ms + "\\n" + key_version + "\\n"
using the application's registered private key. The base64-encoded
signature + the other three fields go in the request headers.

Usage of this client is gated by Walmart's private-partnership approval
(submit at https://walmart.io/subscriptionrequest/OPD). Until approved,
requests will get back 401/403 from Walmart's API gateway.
"""

from __future__ import annotations

import base64
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from diet.util import http_request

WALMART_API_BASE = "https://developer.api.walmart.com/api-proxy/service"


@dataclass
class WalmartClient:
    consumer_id: str
    private_key_path: Path
    key_version: str = "1"
    _private_key: rsa.RSAPrivateKey | None = None

    @classmethod
    def from_env(cls) -> "WalmartClient":
        cid = os.environ.get("WALMART_CONSUMER_ID")
        key_path = os.environ.get("WALMART_PRIVATE_KEY_PATH")
        version = os.environ.get("WALMART_KEY_VERSION", "1")
        if not cid or not key_path:
            raise RuntimeError(
                "WALMART_CONSUMER_ID and WALMART_PRIVATE_KEY_PATH must be set"
            )
        return cls(
            consumer_id=cid,
            private_key_path=Path(key_path).expanduser(),
            key_version=version,
        )

    def _load_private_key(self) -> rsa.RSAPrivateKey:
        if self._private_key is None:
            data = self.private_key_path.read_bytes()
            key = serialization.load_pem_private_key(data, password=None)
            if not isinstance(key, rsa.RSAPrivateKey):
                raise TypeError(f"expected RSA private key, got {type(key).__name__}")
            object.__setattr__(self, "_private_key", key)
        assert self._private_key is not None
        return self._private_key

    def _signed_headers(self, extra: dict[str, str] | None = None) -> dict[str, str]:
        """Build the four auth headers. Timestamp is ms since epoch."""
        ts = str(int(time.time() * 1000))
        string_to_sign = f"{self.consumer_id}\n{ts}\n{self.key_version}\n"
        sig = self._load_private_key().sign(
            string_to_sign.encode("utf-8"),
            padding.PKCS1v15(),
            hashes.SHA256(),
        )
        headers = {
            "WM_CONSUMER.ID": self.consumer_id,
            "WM_CONSUMER.INTIMESTAMP": ts,
            "WM_SEC.AUTH_SIGNATURE": base64.b64encode(sig).decode("ascii"),
            "WM_SEC.KEY_VERSION": self.key_version,
            "Accept": "application/json",
        }
        if extra:
            headers.update(extra)
        return headers

    # --- low-level -----------------------------------------------------------

    def _request(self, method: str, url: str, *, params: dict | None = None,
                 body: dict | None = None) -> dict:
        if params:
            from urllib.parse import urlencode
            url = f"{url}?{urlencode(params, safe=',')}"
        headers = self._signed_headers(
            {"Content-Type": "application/json"} if body is not None else None
        )
        data = json.dumps(body).encode("utf-8") if body is not None else None
        status, _hdr, resp = http_request(url, method=method, headers=headers, data=data)
        if not resp:
            return {}
        return json.loads(resp)

    # --- endpoints -----------------------------------------------------------

    def search(self, query: str, *, num_items: int = 25,
               store_id: str | None = None) -> dict:
        """Affiliate Product Search — national product catalog + list price."""
        params: dict = {"query": query, "format": "json", "numItems": num_items}
        if store_id:
            params["storeId"] = store_id
        return self._request("GET", f"{WALMART_API_BASE}/affil/product/v2/search",
                             params=params)

    def product_details(self, item_id: str) -> dict:
        return self._request(
            "GET", f"{WALMART_API_BASE}/affil/product/v2/items/{item_id}"
        )

    def realtime_price(self, offer_ids: list[str], *,
                       store_id: str | None = None,
                       zip_code: str | None = None) -> dict:
        """OPD Realtime Pricing — store-level prices, up to 20 offerIds per call.

        Requires OPD partner approval; plain signup typically gets 401 here.
        """
        body: dict = {"offerIds": offer_ids[:20]}
        if store_id:
            body["storeIds"] = [store_id]
        if zip_code:
            body["zipCode"] = zip_code
        return self._request(
            "POST",
            f"{WALMART_API_BASE}/affil/catalog-api/v2/product/items/price-availability/",
            body=body,
        )
