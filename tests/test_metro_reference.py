"""Metro and Food Basics unlocalized reference-price client tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from diet import cli
from diet.sources.metro_reference import (
    MetroReferenceClient,
    MetroReferenceError,
    MetroReferenceProductNotFound,
    MetroReferenceProtocolError,
    normalize_retailer,
)

FIXTURES = Path(__file__).parent / "fixtures" / "metro_reference"


class FixtureTransport:
    def __init__(self, fixture: str | bytes, *, status: int = 200):
        self.body = (FIXTURES / fixture).read_bytes() if isinstance(fixture, str) else fixture
        self.status = status
        self.calls: list[dict] = []

    def __call__(self, url, *, method, headers, data):
        self.calls.append({
            "url": url,
            "method": method,
            "headers": headers,
            "request": json.loads(data) if data else None,
        })
        return self.status, {"Content-Type": "text/html;charset=UTF-8"}, self.body


def test_normalizes_the_two_supported_banners():
    assert normalize_retailer("Metro") == "metro"
    assert normalize_retailer("Food Basics") == "foodbasics"
    with pytest.raises(ValueError, match="choose metro or foodbasics"):
        normalize_retailer("Superstore")


def test_metro_reference_quote_has_explicit_unlocalized_semantics():
    transport = FixtureTransport("metro.html")
    client = MetroReferenceClient("metro", transport=transport)

    quote = client.quote_product("059749930031")

    assert quote.retailer == "metro"
    assert quote.price_scope == "reference"
    assert quote.channel == "online_catalog"
    assert quote.product_id == "059749930031"
    assert quote.name == "Black Beans"
    assert quote.brand == "Selection"
    assert quote.package == "540 mL"
    assert quote.effective_price_cad == 1.69
    assert quote.regular_price_cad is None
    assert quote.promo_price_cad is None
    assert quote.unit_price_cad == 0.31
    assert quote.unit_quantity == 100
    assert quote.unit_measure == "ml"
    assert quote.is_weighted is False
    assert quote.source_url == (
        "https://www.metro.ca/en/online-grocery/aisles/pantry/canned-jarred/"
        "beans-legumes/black-beans/p/059749930031"
    )
    assert transport.calls[0] == {
        "url": "https://www.metro.ca/en/online-grocery/product/skus",
        "method": "POST",
        "headers": {
            "Accept": "text/html, */*",
            "Content-Type": "application/json",
        },
        "request": {"productIds": ["059749930031"]},
    }


def test_foodbasics_parses_promos_and_restores_requested_order():
    transport = FixtureTransport("foodbasics.html")
    client = MetroReferenceClient("Food Basics", transport=transport)

    result = client.quote_products(["055270846452", "739907000010", "missing"])

    assert result.retailer == "foodbasics"
    assert result.price_scope == "reference"
    assert [quote.product_id for quote in result.quotes] == [
        "055270846452",
        "739907000010",
    ]
    assert result.missing_product_ids == ("missing",)
    grace = result.quotes[0]
    assert grace.effective_price_cad == 3.99
    assert grace.regular_price_cad == 4.49
    assert grace.promo_price_cad == 3.99
    assert grace.unit_price_cad == 0.20
    assert grace.unit_quantity == 100
    assert grace.unit_measure == "g"
    assert transport.calls[0]["url"] == "https://www.foodbasics.ca/product/skus"


def test_search_uses_banner_specific_ranked_discovery_surface():
    transport = FixtureTransport("foodbasics.html")
    result = MetroReferenceClient(
        "foodbasics", transport=transport
    ).search_products("corn meal")

    assert result.query == "corn meal"
    assert [quote.product_id for quote in result.quotes] == [
        "739907000010",
        "055270846452",
    ]
    assert transport.calls[0] == {
        "url": (
            "https://www.foodbasics.ca/autocompleteSearchProducts?"
            "freeText=corn+meal&tabletMobile=false&previousSuggestion="
        ),
        "method": "POST",
        "headers": {
            "Accept": "text/html, */*",
            "X-Requested-With": "XMLHttpRequest",
        },
        "request": None,
    }


def test_weighted_quote_parses_implicit_one_kilogram_unit_price():
    quote = MetroReferenceClient(
        "foodbasics", transport=FixtureTransport("weighted.html")
    ).quote_product("201021")

    assert quote.is_weighted is True
    assert quote.effective_price_cad == 6.61
    assert quote.unit_price_cad == 18.89
    assert quote.unit_quantity == 1
    assert quote.unit_measure == "kg"


def test_exact_quote_fails_closed_when_sku_is_not_returned():
    client = MetroReferenceClient("metro", transport=FixtureTransport("metro.html"))
    with pytest.raises(MetroReferenceProductNotFound, match="not returned"):
        client.quote_product("000000000000")


def test_large_exact_lookup_is_split_into_bounded_batches():
    transport = FixtureTransport("metro.html")
    ids = ["059749930031", *(f"missing-{index}" for index in range(40))]
    result = MetroReferenceClient(
        "metro", transport=transport, batch_size=20
    ).quote_products(ids)

    assert len(transport.calls) == 3
    assert [len(call["request"]["productIds"]) for call in transport.calls] == [
        20, 20, 1,
    ]
    assert result.quotes[0].product_id == "059749930031"
    assert len(result.missing_product_ids) == 40


@pytest.mark.parametrize("product_ids", [[], [""], ["059749930031", " "]])
def test_rejects_empty_product_ids(product_ids):
    client = MetroReferenceClient("metro", transport=FixtureTransport("metro.html"))
    with pytest.raises(ValueError, match="non-empty product ID"):
        client.quote_products(product_ids)


def test_transport_and_protocol_failures_are_exposed():
    def failed_transport(*args, **kwargs):
        raise OSError("offline")

    with pytest.raises(MetroReferenceError, match="request failed: offline"):
        MetroReferenceClient("metro", transport=failed_transport).quote_product("1")

    client = MetroReferenceClient(
        "metro", transport=FixtureTransport("not html".encode(), status=503)
    )
    with pytest.raises(MetroReferenceError, match="HTTP 503"):
        client.quote_product("1")

    malformed = b'<div class="default-product-tile" data-product-code="1"></div>'
    client = MetroReferenceClient("metro", transport=FixtureTransport(malformed))
    with pytest.raises(MetroReferenceProtocolError, match="valid effective price"):
        client.quote_product("1")


def test_canada_reference_cli_emits_json_and_reports_missing(monkeypatch, capsys):
    def client(retailer):
        return MetroReferenceClient(retailer, transport=FixtureTransport("foodbasics.html"))

    monkeypatch.setattr(cli, "MetroReferenceClient", client)
    rc = cli.main([
        "canada-reference",
        "foodbasics",
        "055270846452",
        "not-found",
        "--json",
    ])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert rc == 1
    assert payload["price_scope"] == "reference"
    assert payload["quotes"][0]["product_id"] == "055270846452"
    assert payload["missing_product_ids"] == ["not-found"]
