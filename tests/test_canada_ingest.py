from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from diet.foods import Location, SkuSpec
from diet.ingest import (
    _ingest_metro_reference,
    _ingest_pc_express_reference,
    _retain_reference_prices,
)
from diet.sources.metro_reference import MetroReferenceClient
from diet.sources.pc_express import PCExpressProduct, PCExpressProductSearch

FIXTURE = (
    Path(__file__).parent
    / "fixtures"
    / "metro_reference"
    / "foodbasics.html"
).read_bytes()


def fixture_transport(url, **kwargs):
    return 200, {"Content-Type": "text/html"}, FIXTURE


def fallback_transport(url, **kwargs):
    body = FIXTURE if "autocompleteSearchProducts" in url else b""
    return 200, {"Content-Type": "text/html"}, body


def _sku(package="2 kg"):
    return SkuSpec(
        product_id="055270846452",
        fdc_id=169697,
        name="Grace Corn Meal",
        unit_grams=2000,
        dietary_categories=frozenset({"grain"}),
        max_serving_g=None,
        source="foodbasics",
        package_label=package,
    )


def test_reference_ingest_normalizes_promo_and_provenance(tmp_path):
    location = Location(
        "foodbasics_reference",
        "foodbasics-reference",
        "Food Basics Reference",
        "foodbasics",
        "CAD",
        "reference",
    )
    client = MetroReferenceClient("foodbasics", transport=fixture_transport)

    rows, missing = _ingest_metro_reference(
        [_sku()], location, client, "2026-08-08", tmp_path
    )

    assert missing == []
    assert rows == [{
        "product_id": "055270846452",
        "location_id": "foodbasics-reference",
        "regular": 4.49,
        "promo": 3.99,
        "currency": "CAD",
        "price_scope": "reference",
        "price_basis": "package",
        "package": "2 kg",
        "source_url": (
            "https://www.foodbasics.ca/aisles/pantry/baking-ingredients/"
            "flour-baking-essentials/corn-meal/p/055270846452"
        ),
        "observed_at": rows[0]["observed_at"],
        "fetched_at": "2026-08-08",
        "stale": False,
    }]
    assert (tmp_path / "2026-08-08" / "foodbasics.json").exists()


def test_reference_ingest_rejects_changed_package(tmp_path):
    location = Location(
        "foodbasics_reference", "foodbasics-reference", "Reference",
        "foodbasics", "CAD", "reference",
    )
    rows, missing = _ingest_metro_reference(
        [_sku("1 kg")],
        location,
        MetroReferenceClient("foodbasics", transport=fixture_transport),
        "2026-08-08",
        tmp_path,
    )
    assert rows == []
    assert "package changed" in missing[0]["reason"]


def test_reference_ingest_falls_back_to_curated_search_and_exact_upc(tmp_path):
    location = Location(
        "foodbasics_reference", "foodbasics-reference", "Reference",
        "foodbasics", "CAD", "reference",
    )
    sku = replace(_sku(), search_query="corn meal")
    rows, missing = _ingest_metro_reference(
        [sku],
        location,
        MetroReferenceClient("foodbasics", transport=fallback_transport),
        "2026-08-08",
        tmp_path,
    )
    assert missing == []
    assert rows[0]["product_id"] == "055270846452"


def test_retains_only_still_curated_missing_reference_quotes():
    location = Location(
        "foodbasics_reference", "foodbasics-reference", "Reference",
        "foodbasics", "CAD", "reference",
    )
    previous = [{
        "product_id": "055270846452",
        "location_id": "foodbasics-reference",
        "regular": 3.99,
        "fetched_at": "2026-08-07",
    }, {
        "product_id": "removed",
        "location_id": "foodbasics-reference",
        "regular": 1.0,
    }]
    rows = _retain_reference_prices(
        [], previous, skus=[_sku()], locations=[location],
        retained_at="2026-08-08T12:00:00Z",
    )
    assert rows == [{
        "product_id": "055270846452",
        "location_id": "foodbasics-reference",
        "regular": 3.99,
        "fetched_at": "2026-08-07",
        "stale": True,
        "retained_at": "2026-08-08T12:00:00Z",
    }]


class FakePCExpressClient:
    def __init__(self, *, in_stock=True, include_exact=True):
        self.in_stock = in_stock
        self.include_exact = include_exact
        self.calls = []

    def search_products(self, **kwargs):
        self.calls.append(kwargs)
        products = ()
        if self.include_exact:
            products = (PCExpressProduct(
                product_id="20602161_EA",
                name="Grace Cornmeal",
                brand="Grace",
                effective_price_cad=3.99,
                in_stock=self.in_stock,
                image_url=None,
            ),)
        return PCExpressProductSearch(
            store_id=kwargs["store_id"],
            banner=kwargs["banner"],
            terms=(kwargs["terms"],),
            products=products,
            observed_at="2026-08-08T12:34:56Z",
        )


def _pcx_location():
    return Location(
        region="superstore_reference",
        location_id="1033",
        display="Superstore Reference — Dufferin & Steeles, Toronto",
        source="superstore",
        currency="CAD",
        price_scope="reference",
        reference_store_name="Real Canadian Superstore — Dufferin & Steeles",
        reference_store_address="51 Gerry Fitzgerald Dr, Toronto, ON M3J 3N4",
        reference_store_basis="PC Express storefront defaultStoreId/masterStoreId",
    )


def _pcx_sku():
    return SkuSpec(
        product_id="20602161_EA",
        fdc_id=169697,
        name="Grace Cornmeal",
        unit_grams=2000,
        dietary_categories=frozenset({"grain"}),
        max_serving_g=None,
        source="superstore",
        package_label="2 kg",
        search_query="Grace cornmeal",
    )


def test_pc_express_ingest_uses_explicit_reference_store_and_exact_liam(tmp_path):
    client = FakePCExpressClient()
    rows, missing = _ingest_pc_express_reference(
        [_pcx_sku()], _pcx_location(), client, "2026-08-08", tmp_path
    )

    assert missing == []
    assert client.calls == [{
        "store_id": "1033",
        "banner": "superstore",
        "terms": "Grace cornmeal",
        "num_results": 100,
    }]
    assert rows == [{
        "product_id": "20602161_EA",
        "location_id": "1033",
        "regular": 3.99,
        "promo": None,
        "currency": "CAD",
        "price_scope": "reference",
        "channel": "pickup",
        "price_kind": "effective",
        "price_basis": "package",
        "package": "2 kg",
        "source_url": "https://www.realcanadiansuperstore.ca/en/p/20602161_EA",
        "api_source_url": "https://api.pcexpress.ca/v1/agents/mcp",
        "observed_at": "2026-08-08T12:34:56Z",
        "fetched_at": "2026-08-08",
        "stale": False,
        "banner": "superstore",
        "store_id": "1033",
        "reference_store_name": "Real Canadian Superstore — Dufferin & Steeles",
        "reference_store_address": "51 Gerry Fitzgerald Dr, Toronto, ON M3J 3N4",
        "reference_store_basis": "PC Express storefront defaultStoreId/masterStoreId",
    }]
    assert (
        tmp_path / "2026-08-08" / "superstore-1033.json"
    ).exists()


def test_pc_express_ingest_rejects_missing_or_out_of_stock_exact_liam(tmp_path):
    for client, reason in (
        (FakePCExpressClient(include_exact=False), "exact LIAM not returned"),
        (FakePCExpressClient(in_stock=False), "out of stock"),
    ):
        rows, missing = _ingest_pc_express_reference(
            [_pcx_sku()], _pcx_location(), client, "2026-08-08", tmp_path
        )
        assert rows == []
        assert reason in missing[0]["reason"]
