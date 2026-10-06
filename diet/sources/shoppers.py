"""Shoppers Drug Mart online prices from the site's product API.

shoppersdrugmart.ca and api.shoppersdrugmart.ca sit behind Akamai Bot Manager,
which rejects plain HTTP clients and automated or headless-looking browsers.
A session is earned by loading one product page in a headless Chromium that
presents as an ordinary browser: a normal user agent, a screen size matching
its window, and no ``--enable-automation`` flag (which sets
``navigator.webdriver``).  The page's cookies, API key and client hints then
authorize direct product API calls made with a Chrome TLS fingerprint through
curl_cffi.  In testing on 2026-10-05 a session stayed valid for at least 30
minutes after the browser closed.

Prices are Shoppers' online prices for Ontario, not a particular store's.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
import time
import urllib.request
from collections.abc import Callable
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any

SHOPPERS_SOURCE = "shoppers_product_api"
API_HOST = "https://api.shoppersdrugmart.ca/beauty/"
API_ROOT = API_HOST + "v2/shoppersdrugmart/product/variantProduct/"
PRODUCT_PAGE_ROOT = "https://www.shoppersdrugmart.ca/p/BB_"


def product_page(product_id: str) -> str:
    # The short /p/BB_<code> page fetches only base-product data; with
    # variantCode it also calls the variant API whose prices the client reads.
    return f"{PRODUCT_PAGE_ROOT}{product_id}?variantCode={product_id}"
# Any current product page works; this one only earns the session.
SEED_PRODUCT = "057800273073"
PROVINCE = "ON"

# (url, headers, cookies) -> (status, body)
Transport = Callable[[str, dict[str, str], dict[str, str]], tuple[int, bytes]]


class ShoppersError(RuntimeError):
    """Base error for Shoppers session, transport or response failures."""


class ShoppersBlocked(ShoppersError):
    """Akamai refused the browser or the API call."""


class ShoppersProductNotFound(ShoppersError):
    """The product API does not know this product code."""


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


@dataclass(frozen=True)
class ShoppersSession:
    api_key: str
    cookies: dict[str, str]
    headers: dict[str, str]  # user agent and client hints of the browser that earned it
    earned_at: str


@dataclass(frozen=True)
class ShoppersQuote:
    product_id: str
    name: str
    brand: str | None
    regular_price_cad: float
    effective_price_cad: float
    promo_price_cad: float | None
    size: float | None
    in_stock: bool | None
    source_url: str
    observed_at: str
    price_scope: str = "reference"
    channel: str = "online_catalog"
    source: str = SHOPPERS_SOURCE

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _chromium_executable() -> str:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        path = p.chromium.executable_path
    if not os.path.exists(path):
        raise ShoppersError(
            f"Chromium not installed at {path}; run `uv run playwright install chromium`"
        )
    return path


def _wait_for_devtools(port: int, timeout_s: float) -> None:
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=1)
            return
        except OSError:
            time.sleep(0.25)
    raise ShoppersError("Chromium did not start")


def start_session(
    *, chromium: str | None = None, port: int = 9471, timeout_s: float = 60
) -> ShoppersSession:
    """Load one product page in a disguised headless Chromium and keep its session."""
    from playwright.sync_api import sync_playwright

    chromium = chromium or _chromium_executable()
    version = subprocess.run([chromium, "--version"], capture_output=True, text=True).stdout
    major = re.search(r"(\d+)\.\d+\.\d+", version)
    if not major:
        raise ShoppersError(f"cannot read the Chromium version from {version!r}")
    user_agent = (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
        f"Chrome/{major.group(1)}.0.0.0 Safari/537.36"
    )
    profile = tempfile.mkdtemp(prefix="diet-shoppers-")
    proc = subprocess.Popen(
        [
            chromium, "--headless=new", f"--user-agent={user_agent}",
            f"--remote-debugging-port={port}", f"--user-data-dir={profile}",
            "--no-first-run", "--no-default-browser-check", "--window-size=1300,900",
            "about:blank",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        _wait_for_devtools(port, timeout_s=15)
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{port}")
            context = browser.contexts[0]
            page = context.new_page()
            # Headless reports an 800x600 screen inside a larger window; Akamai
            # rejects that mismatch, so report a screen that fits the window.
            context.new_cdp_session(page).send("Emulation.setDeviceMetricsOverride", {
                "width": 1300, "height": 820, "deviceScaleFactor": 1, "mobile": False,
                "screenWidth": 1366, "screenHeight": 900,
            })
            api_requests = []
            # Every request to the product API carries the site's key.
            page.on("request", lambda r: api_requests.append(r) if r.url.startswith(API_HOST) else None)
            page.goto(product_page(SEED_PRODUCT), timeout=timeout_s * 1000)
            page.wait_for_timeout(8000)
            if not api_requests:
                title = page.title()
                if "access denied" in title.lower():
                    raise ShoppersBlocked("Akamai refused the browser session")
                raise ShoppersError(f"product page made no API call (title {title!r})")
            sent = next(
                (h for h in (r.all_headers() for r in api_requests) if h.get("x-apikey")), {}
            )
            api_key = sent.get("x-apikey")
            if not api_key:
                raise ShoppersError("product API call carried no x-apikey header")
            cookies = {c["name"]: c["value"] for c in context.cookies([API_ROOT])}
            headers = {
                k: v for k, v in sent.items()
                if k in ("user-agent", "sec-ch-ua", "sec-ch-ua-mobile", "sec-ch-ua-platform", "accept-language")
            }
            return ShoppersSession(api_key, cookies, headers, _utc_now())
    finally:
        proc.terminate()
        proc.wait()
        shutil.rmtree(profile, ignore_errors=True)


def _curl_cffi_transport(url: str, headers: dict[str, str], cookies: dict[str, str]) -> tuple[int, bytes]:
    from curl_cffi import requests as cffi

    response = cffi.get(
        url, headers=headers, cookies=cookies, impersonate="chrome",
        default_headers=False, timeout=30,
    )
    return response.status_code, response.content


def parse_product(product_id: str, payload: dict[str, Any]) -> ShoppersQuote:
    """Normalize one variantProduct/details response."""
    try:
        regular = float(payload["price"]["value"])
        effective = float((payload.get("effectivePrice") or payload["price"])["value"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ShoppersError(f"{product_id}: response has no usable price") from exc
    if effective <= 0 or regular <= 0:
        raise ShoppersError(f"{product_id}: non-positive price")
    name = str(payload.get("name") or "").strip()
    if not name:
        raise ShoppersError(f"{product_id}: response has no product name")
    size = payload.get("size")
    out_of_stock = payload.get("isOutOfStock")
    return ShoppersQuote(
        product_id=product_id,
        name=name,
        brand=payload.get("brandName"),
        regular_price_cad=regular,
        effective_price_cad=effective,
        promo_price_cad=effective if effective < regular else None,
        size=float(size) if size is not None else None,
        in_stock=None if out_of_stock is None else not out_of_stock,
        source_url=product_page(product_id),
        observed_at=_utc_now(),
    )


class ShoppersClient:
    """Quote Shoppers products, earning one browser session on first use."""

    def __init__(
        self,
        *,
        session_factory: Callable[[], ShoppersSession] = start_session,
        transport: Transport = _curl_cffi_transport,
    ):
        self.session_factory = session_factory
        self.transport = transport
        self._session: ShoppersSession | None = None

    def quote_product(self, product_id: str) -> ShoppersQuote:
        product_id = product_id.strip()
        if not product_id.isdigit():
            raise ValueError(f"Shoppers product codes are digits, got {product_id!r}")
        if self._session is None:
            self._session = self.session_factory()
        session = self._session
        headers = {
            **session.headers,
            "accept": "application/json, text/plain, */*",
            "x-apikey": session.api_key,
            "origin": "https://www.shoppersdrugmart.ca",
            "referer": "https://www.shoppersdrugmart.ca/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
        }
        try:
            status, body = self.transport(
                f"{API_ROOT}{product_id}/details?province={PROVINCE}", headers, session.cookies
            )
        except Exception as exc:
            raise ShoppersError(f"{product_id}: request failed: {exc}") from exc
        if status == 403:
            raise ShoppersBlocked(f"{product_id}: Akamai refused the API call")
        if status == 404:
            raise ShoppersProductNotFound(f"{product_id}: product code not found")
        if status != 200:
            raise ShoppersError(f"{product_id}: HTTP {status}")
        try:
            payload = json.loads(body)
        except ValueError as exc:
            raise ShoppersError(f"{product_id}: response is not JSON") from exc
        return parse_product(product_id, payload)
