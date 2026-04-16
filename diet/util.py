"""Shared utilities: atomic writes, HTTP, paths."""

from __future__ import annotations

import json
import os
import ssl
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

import certifi

USER_AGENT = "diet/0.1"


def write_text_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def write_json_atomic(path: Path, obj: Any, *, indent: int = 2) -> None:
    write_text_atomic(path, json.dumps(obj, indent=indent, sort_keys=False) + "\n")


def read_json(path: Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _ssl_ctx() -> ssl.SSLContext:
    return ssl.create_default_context(cafile=certifi.where())


def http_request(
    url: str,
    *,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    data: bytes | None = None,
    timeout_s: int = 60,
    retries: int = 3,
) -> tuple[int, dict[str, str], bytes]:
    """Minimal HTTP wrapper with retries on transient failures."""
    hdrs = {"User-Agent": USER_AGENT}
    if headers:
        hdrs.update(headers)

    last_err: Exception | None = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=hdrs, data=data, method=method)
            ctx = _ssl_ctx() if url.startswith("https://") else None
            with urllib.request.urlopen(req, timeout=timeout_s, context=ctx) as resp:
                status = getattr(resp, "status", 200)
                resp_headers = {k: v for k, v in resp.headers.items()}
                body = resp.read()
                return status, resp_headers, body
        except urllib.error.HTTPError as exc:
            # Don't retry 4xx (except 429) — they won't get better.
            if 400 <= exc.code < 500 and exc.code != 429:
                raise
            last_err = exc
        except (urllib.error.URLError, TimeoutError) as exc:
            last_err = exc
        if attempt < retries - 1:
            time.sleep(1.5 * (attempt + 1))

    raise RuntimeError(f"http_request failed after {retries} attempts: {last_err}")


def http_get_json(url: str, *, params: dict | None = None, **kwargs) -> Any:
    if params:
        url = f"{url}?{urlencode(params, safe=',')}"
    _, _, body = http_request(url, method="GET", **kwargs)
    return json.loads(body)


def http_post_form_json(url: str, *, form: dict, headers: dict[str, str] | None = None,
                       **kwargs) -> Any:
    body_bytes = urlencode(form).encode("utf-8")
    hdrs = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"}
    if headers:
        hdrs.update(headers)
    _, _, body = http_request(url, method="POST", headers=hdrs, data=body_bytes, **kwargs)
    return json.loads(body)
