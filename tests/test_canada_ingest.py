from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from diet.foods import Location, SkuSpec
from diet.ingest import _ingest_metro_reference, _retain_reference_prices
from diet.sources.metro_reference import MetroReferenceClient

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
