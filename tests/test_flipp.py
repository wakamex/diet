"""Flipp regional flyer snapshot tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from diet.sources.flipp import (
    FLIPP_BASE,
    FlippClient,
    FlippError,
    normalize_item,
    pull_flyers,
    select_flyers,
)

FIXTURES = Path(__file__).parent / "fixtures" / "flipp"
CREAM_CHEESE, PRETZELS, TROPICANA = json.loads(
    (FIXTURES / "items.json").read_text(encoding="utf-8")
)

FLYERS = [
    {"id": 8164401, "merchant": "Loblaws", "categories": ["Groceries"],
     "valid_from": "2026-10-01T04:00:00+00:00", "valid_to": "2026-10-08T03:59:59+00:00"},
    {"id": 8165258, "merchant": "Metro", "categories": ["Groceries"],
     "valid_from": "2026-10-01T04:00:00+00:00", "valid_to": "2026-10-08T03:59:59+00:00"},
    {"id": 1, "merchant": "Loblaws", "categories": ["Pharmacy"],
     "valid_from": "2026-10-01T04:00:00+00:00", "valid_to": "2026-10-08T03:59:59+00:00"},
]


class RouteTransport:
    """Serve exact Flipp URLs and reject anything else."""

    def __init__(self, routes: dict[str, object]):
        self.routes = {f"{FLIPP_BASE}/{path}": body for path, body in routes.items()}
        self.calls: list[str] = []

    def __call__(self, url, *, method, headers, data):
        assert method == "GET" and data is None
        self.calls.append(url)
        if url not in self.routes:
            raise AssertionError(f"unexpected request {url}")
        return 200, {}, json.dumps(self.routes[url]).encode()


def _routes() -> dict[str, object]:
    return {
        "flyers?locale=en-ca&postal_code=K1S5B6": {"flyers": FLYERS},
        "flyers/8164401?locale=en-ca": {
            "items": [{"id": CREAM_CHEESE["id"]}, {"id": PRETZELS["id"]}]
        },
        "flyers/8165258?locale=en-ca": {"items": [{"id": TROPICANA["id"]}]},
        **{f"items/{item['id']}": {"item": item}
           for item in (CREAM_CHEESE, PRETZELS, TROPICANA)},
    }


def test_multi_buy_terms_and_trusted_product_id():
    item = normalize_item(CREAM_CHEESE)

    assert item["price_prefix"] == "2/"
    assert item["price"] == 7.5
    assert item["price_suffix"] == "or $3.99 EA."
    assert item["multi_buy_quantity"] == 2
    assert item["multi_buy_unit_price"] == 3.75
    assert item["member_only"] is False
    assert item["product_id"] == "20308105001_EA"


def test_member_price_is_flagged():
    item = normalize_item(PRETZELS)

    assert item["member_only"] is True
    assert item["multi_buy_quantity"] is None
    assert item["sale_story"] == "Members save $2.50"


def test_ad_wrapped_link_is_a_hint_not_a_product_id():
    item = normalize_item(TROPICANA)

    assert item["url"].startswith("https://www.metro.ca/")
    assert item["link_product_id"] == "059749896078"
    assert item["product_id"] is None


def test_select_flyers_keeps_named_grocery_flyers():
    assert [f["id"] for f in select_flyers(FLYERS, ["loblaws"])] == [8164401]
    assert [f["id"] for f in select_flyers(FLYERS, None)] == [8164401, 8165258]


def test_pull_caches_each_flyer(tmp_path):
    transport = RouteTransport(_routes())
    client = FlippClient(transport=transport, workers=2)

    snapshot = pull_flyers(
        "k1s 5b6", merchants=["Loblaws", "Metro"], cache_root=tmp_path, client=client
    )

    assert snapshot["postal_code"] == "K1S 5B6"
    assert [f["item_count"] for f in snapshot["flyers"]] == [2, 1]
    assert [i["item_id"] for i in snapshot["items"]] == [
        CREAM_CHEESE["id"], PRETZELS["id"], TROPICANA["id"]
    ]
    assert (tmp_path / "flyers" / "8164401.json").exists()

    transport.calls.clear()
    again = pull_flyers(
        "K1S5B6", merchants=["Loblaws", "Metro"], cache_root=tmp_path, client=client
    )
    assert transport.calls == [f"{FLIPP_BASE}/flyers?locale=en-ca&postal_code=K1S5B6"]
    assert again["items"] == snapshot["items"]


def test_schema_change_raises():
    transport = RouteTransport({"flyers?locale=en-ca&postal_code=K1S5B6": {"x": 1}})

    with pytest.raises(FlippError, match="no flyers array"):
        FlippClient(transport=transport).list_flyers("K1S 5B6")
