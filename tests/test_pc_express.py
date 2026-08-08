"""PC Express MCP client tests using sanitized live-response fixtures."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from diet import cli
from diet.sources.pc_express import (
    PCExpressClient,
    PCExpressError,
    PCExpressProductNotFound,
    PCExpressProtocolError,
    normalize_banner,
    normalize_postal_code,
)

FIXTURES = Path(__file__).parent / "fixtures" / "pc_express"


class FixtureTransport:
    def __init__(self, fixture: str | bytes):
        self.body = (
            (FIXTURES / fixture).read_bytes()
            if isinstance(fixture, str)
            else fixture
        )
        self.calls: list[dict] = []

    def __call__(self, url, *, method, headers, data):
        self.calls.append({
            "url": url,
            "method": method,
            "headers": headers,
            "request": json.loads(data),
        })
        return 200, {"Content-Type": "text/event-stream"}, self.body


def test_normalizes_canadian_postal_code_and_banner_aliases():
    assert normalize_postal_code("k1s-5b6") == "K1S 5B6"
    assert normalize_banner("Loblaws") == "loblaw"
    assert normalize_banner("Real Canadian Superstore") == "superstore"
    assert normalize_banner("No Frills") == "nofrills"


@pytest.mark.parametrize("value", ["", "K1S", "123456", "K1S 5B"])
def test_rejects_invalid_postal_codes(value):
    with pytest.raises(ValueError, match="invalid Canadian postal code"):
        normalize_postal_code(value)


def test_store_search_returns_normalized_ottawa_stores():
    transport = FixtureTransport("stores.sse")
    client = PCExpressClient(transport=transport)

    stores = client.search_stores("k1s5b6")

    assert [store.store_id for store in stores] == ["8999", "1095", "1009"]
    assert [store.banner for store in stores] == ["nofrills", "loblaw", "superstore"]
    assert stores[2].postal_code == "K1Z 6W6"
    request = transport.calls[0]["request"]
    assert request["method"] == "tools/call"
    assert request["params"] == {
        "name": "search_for_stores",
        "arguments": {"postal_code": "K1S 5B6"},
    }


def test_product_search_returns_effective_prices_without_package_claims():
    transport = FixtureTransport("products.sse")
    client = PCExpressClient(transport=transport)

    result = client.search_products(
        store_id="1009",
        banner="Real Canadian Superstore",
        terms="long grain rice",
        postal_code="K1S5B6",
        num_results=25,
    )

    assert result.store_id == "1009"
    assert result.banner == "superstore"
    assert result.channel == "pickup"
    assert result.observed_at.endswith("Z")
    assert result.terms == ("long grain rice",)
    assert result.products[0].product_id == "20069589_EA"
    assert result.products[0].effective_price_cad == 5.0
    assert result.products[0].in_stock is True
    assert result.products[1].in_stock is False
    assert "package_quantity" not in result.products[0].as_dict()
    arguments = transport.calls[0]["request"]["params"]["arguments"]
    assert arguments == {
        "store_id": "1009",
        "banner": "SUPERSTORE",
        "term": ["long grain rice"],
        "num_results": 25,
        "postal_code": "K1S 5B6",
    }


def test_quote_product_requires_an_exact_curated_liam():
    client = PCExpressClient(transport=FixtureTransport("products.sse"))
    product = client.quote_product(
        product_id="20069589_EA",
        query="long grain rice",
        store_id="1009",
        banner="superstore",
    )
    assert product.name == "Long Grain White Rice"
    assert product.store_id == "1009"
    assert product.banner == "superstore"
    assert product.channel == "pickup"
    assert product.regular_price_cad is None
    assert product.promo_price_cad is None

    client = PCExpressClient(transport=FixtureTransport("products.sse"))
    with pytest.raises(PCExpressProductNotFound, match="NOT_RETURNED_EA"):
        client.quote_product(
            product_id="NOT_RETURNED_EA",
            query="long grain rice",
            store_id="1009",
            banner="superstore",
        )


def test_json_rpc_errors_are_exposed_without_retrying_as_data():
    body = b'{"jsonrpc":"2.0","id":1,"error":{"code":-32000,"message":"nope"}}'
    client = PCExpressClient(transport=FixtureTransport(body))
    with pytest.raises(PCExpressError, match="nope"):
        client.search_stores("K1S 5B6")


def test_transport_failures_are_exposed_as_pc_express_errors():
    def failed_transport(*args, **kwargs):
        raise OSError("offline")

    client = PCExpressClient(transport=failed_transport)
    with pytest.raises(PCExpressError, match="request failed: offline"):
        client.search_stores("K1S 5B6")


def test_malformed_success_is_rejected():
    body = b'{"jsonrpc":"2.0","id":1,"result":{"structuredContent":{}}}'
    client = PCExpressClient(transport=FixtureTransport(body))
    with pytest.raises(PCExpressProtocolError, match="no stores array"):
        client.search_stores("K1S 5B6")


def test_client_rejects_cart_mutation_tools():
    client = PCExpressClient(transport=FixtureTransport("stores.sse"))
    with pytest.raises(ValueError, match="not allowed"):
        client._call_tool("clear_cart", {"cart_id": "unused"})


def test_pcx_stores_cli_emits_normalized_json(monkeypatch, capsys):
    transport = FixtureTransport("stores.sse")
    monkeypatch.setattr(cli, "PCExpressClient", lambda: PCExpressClient(transport=transport))

    assert cli.main(["pcx", "stores", "K1S5B6", "--json"]) == 0

    output = json.loads(capsys.readouterr().out)
    assert output[0]["store_id"] == "8999"
    assert output[0]["source"] == "pc_express_mcp"


def test_pcx_cli_reports_exact_id_miss_without_traceback(monkeypatch, capsys):
    transport = FixtureTransport("products.sse")
    monkeypatch.setattr(cli, "PCExpressClient", lambda: PCExpressClient(transport=transport))

    rc = cli.main([
        "pcx", "search", "long grain rice",
        "--store-id", "1009",
        "--banner", "superstore",
        "--product-id", "NOT_RETURNED_EA",
    ])

    captured = capsys.readouterr()
    assert rc == 1
    assert "pcx: PC Express product 'NOT_RETURNED_EA'" in captured.err
    assert "Traceback" not in captured.err
