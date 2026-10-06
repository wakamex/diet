"""Shoppers Drug Mart product API client and ingest tests."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from diet.foods import Location, SkuSpec
from diet.ingest import _ingest_shoppers_reference
from diet.sources.shoppers import (
    ShoppersBlocked,
    ShoppersClient,
    ShoppersProductNotFound,
    ShoppersSession,
    parse_product,
)
from diet.supplements import load_supplements

# A real variantProduct/details response (2026-10-05), trimmed to the fields
# the parser reads.
VITAMIN_D = json.loads(
    (Path(__file__).parent / "fixtures" / "shoppers" / "vitamin_d3_057800840138.json").read_text()
)
SESSION = ShoppersSession(
    api_key="test-key",
    cookies={"_abck": "cookie"},
    headers={"user-agent": "Mozilla/5.0 Chrome/153.0.0.0", "sec-ch-ua": '"Chromium";v="153"'},
    earned_at="2026-10-05T00:00:00Z",
)
LOCATION = Location(
    region="shoppers", location_id="shoppers-catalog", display="Shoppers", source="shoppers",
    currency="CAD", price_scope="reference",
)


class FakeTransport:
    def __init__(self, responses: dict[str, tuple[int, bytes]]):
        self.responses = responses
        self.calls: list[tuple[str, dict, dict]] = []

    def __call__(self, url, headers, cookies):
        self.calls.append((url, headers, cookies))
        code = url.split("/")[-2]
        return self.responses[code]


def client_for(responses):
    sessions = []

    def factory():
        sessions.append(SESSION)
        return SESSION

    transport = FakeTransport(responses)
    return ShoppersClient(session_factory=factory, transport=transport), transport, sessions


def test_parses_regular_price_size_and_stock():
    quote = parse_product("057800840138", VITAMIN_D)

    assert quote.name == "Vitamin D3 1000  IU"
    assert quote.brand == "Life Brand"
    assert quote.regular_price_cad == 8.49
    assert quote.effective_price_cad == 8.49
    assert quote.promo_price_cad is None
    assert quote.size == 100.0
    assert quote.in_stock is True


def test_lower_effective_price_is_a_sale():
    on_sale = copy.deepcopy(VITAMIN_D)
    on_sale["effectivePrice"]["value"] = 6.79

    quote = parse_product("057800840138", on_sale)

    assert quote.regular_price_cad == 8.49
    assert quote.promo_price_cad == 6.79


def test_one_session_signs_every_call():
    body = json.dumps(VITAMIN_D).encode()
    client, transport, sessions = client_for({"057800840138": (200, body), "057800840244": (200, body)})

    client.quote_product("057800840138")
    client.quote_product("057800840244")

    assert len(sessions) == 1
    url, headers, cookies = transport.calls[0]
    assert url.endswith("/variantProduct/057800840138/details?province=ON")
    assert headers["x-apikey"] == "test-key"
    assert headers["user-agent"] == SESSION.headers["user-agent"]
    assert headers["sec-ch-ua"] == SESSION.headers["sec-ch-ua"]
    assert cookies == {"_abck": "cookie"}


def test_refusal_and_unknown_codes_raise_distinct_errors():
    client, _, _ = client_for({
        "1": (403, b"<HTML><TITLE>Access Denied</TITLE></HTML>"),
        "2": (404, b'{"errors":[{"message":"Product code 2 not found"}]}'),
    })

    with pytest.raises(ShoppersBlocked):
        client.quote_product("1")
    with pytest.raises(ShoppersProductNotFound):
        client.quote_product("2")
    with pytest.raises(ValueError, match="digits"):
        client.quote_product("BB_057800840138")


def test_ingest_stops_calling_after_a_refusal(tmp_path):
    client, transport, _ = client_for({"1": (403, b"Access Denied")})
    skus = [
        SkuSpec(product_id=code, fdc_id=0, name=f"pill {code}", unit_grams=20,
                dietary_categories=frozenset(), max_serving_g=None, source="shoppers")
        for code in ("1", "2", "3")
    ]

    rows, missing = _ingest_shoppers_reference(skus, LOCATION, client, "2026-10-05", tmp_path)

    assert rows == []
    assert [m["product_id"] for m in missing] == ["1", "2", "3"]
    assert len(transport.calls) == 1


def test_ingest_records_regular_and_sale_prices(tmp_path):
    on_sale = copy.deepcopy(VITAMIN_D)
    on_sale["effectivePrice"]["value"] = 6.79
    client, _, _ = client_for({"057800840138": (200, json.dumps(on_sale).encode())})
    sku = SkuSpec(product_id="057800840138", fdc_id=0, name="D3", unit_grams=20,
                  dietary_categories=frozenset(), max_serving_g=None, source="shoppers")

    rows, missing = _ingest_shoppers_reference([sku], LOCATION, client, "2026-10-05", tmp_path)

    assert missing == []
    assert rows[0]["regular"] == 8.49
    assert rows[0]["promo"] == 6.79
    assert rows[0]["in_stock"] is True
    assert (tmp_path / "2026-10-05" / "shoppers.json").exists()


def test_shoppers_supplements_carry_label_doses():
    pills = {s.product_id: s for s in load_supplements() if s.source == "shoppers"}

    assert pills["057800840138"].nutrients_per_tablet == {"vit_d_mcg": 25}
    assert pills["057800270461"].max_tablets_per_day == 3
    assert pills["057800273073"].nutrients_per_tablet["choline_mg"] == 50
