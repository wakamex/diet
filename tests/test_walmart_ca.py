"""Walmart.ca unlocalized product-page reference-price tests."""

from pathlib import Path

import pytest

from diet.foods import Location, SkuSpec
from diet.ingest import _ingest_walmart_ca_reference
from diet.sources.walmart_ca import (
    WalmartCanadaClient,
    WalmartCanadaError,
    WalmartCanadaProtocolError,
)

FIXTURE = Path(__file__).parent / "fixtures" / "walmart_ca" / "product.html"


class FixtureTransport:
    def __init__(self, body: bytes | None = None, *, status: int = 200):
        self.body = body if body is not None else FIXTURE.read_bytes()
        self.status = status
        self.calls: list[dict] = []

    def __call__(self, url, *, method, headers, data):
        self.calls.append({
            "url": url,
            "method": method,
            "headers": headers,
            "data": data,
        })
        return self.status, {"Content-Type": "text/html"}, self.body


def test_quote_reads_current_cad_offer_from_json_ld():
    transport = FixtureTransport()
    quote = WalmartCanadaClient(transport=transport).quote_product("6000204673258")

    assert quote.product_id == "6000204673258"
    assert quote.name == "Equate Multivitamin, 250 Tablets, Value Size"
    assert quote.effective_price_cad == 17.57
    assert quote.currency == "CAD"
    assert quote.price_scope == "reference"
    assert quote.channel == "online_catalog"
    assert quote.source_url == (
        "https://www.walmart.ca/en/ip/"
        "equate-multivitamin-250-tablets-value-size-unisex/6000204673258"
    )
    assert transport.calls[0]["url"] == (
        "https://www.walmart.ca/en/ip/6000204673258"
    )


def test_quote_fails_closed_on_missing_or_non_cad_offer():
    missing = b'<html><script type="application/ld+json">{}</script></html>'
    with pytest.raises(WalmartCanadaProtocolError, match="product JSON-LD"):
        WalmartCanadaClient(
            transport=FixtureTransport(missing)
        ).quote_product("6000204673258")

    usd = FIXTURE.read_bytes().replace(b'"CAD"', b'"USD"')
    with pytest.raises(WalmartCanadaProtocolError, match="not priced in CAD"):
        WalmartCanadaClient(
            transport=FixtureTransport(usd)
        ).quote_product("6000204673258")


def test_transport_failure_is_exposed():
    with pytest.raises(WalmartCanadaError, match="HTTP 503"):
        WalmartCanadaClient(
            transport=FixtureTransport(status=503)
        ).quote_product("6000204673258")


def test_ingest_emits_reference_price_metadata(tmp_path):
    sku = SkuSpec(
        product_id="6000204673258",
        fdc_id=0,
        name="Equate Multivitamin",
        unit_grams=325,
        dietary_categories=frozenset({"supplement", "multivitamin"}),
        max_serving_g=1.3,
        source="walmart_ca",
        package_label="250 tablets",
    )
    location = Location(
        "walmart_ca_reference",
        "walmart-ca-reference",
        "Walmart.ca Reference",
        "walmart_ca",
        "CAD",
        "reference",
    )
    rows, missing = _ingest_walmart_ca_reference(
        [sku],
        location,
        WalmartCanadaClient(transport=FixtureTransport()),
        "2026-08-09",
        tmp_path,
    )

    assert missing == []
    assert rows == [{
        "product_id": "6000204673258",
        "location_id": "walmart-ca-reference",
        "regular": 17.57,
        "promo": None,
        "currency": "CAD",
        "price_scope": "reference",
        "channel": "online_catalog",
        "price_kind": "effective",
        "price_basis": "package",
        "package": "250 tablets",
        "source_url": (
            "https://www.walmart.ca/en/ip/"
            "equate-multivitamin-250-tablets-value-size-unisex/6000204673258"
        ),
        "observed_at": rows[0]["observed_at"],
        "fetched_at": "2026-08-09",
        "stale": False,
    }]
