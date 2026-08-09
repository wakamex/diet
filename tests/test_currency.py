import json

import pytest

from diet.export import _merge_prices, load_fx_rates, serialize_solution
from diet.foods import Location, load_locations, price_locations_for
from diet.solver import Solution


def test_canadian_locations_are_native_cad_reference_scopes():
    locations = {location.region: location for location in load_locations()}
    for region in (
        "metro_reference",
        "foodbasics_reference",
        "superstore_reference",
        "nofrills_reference",
        "canada_reference",
    ):
        assert locations[region].currency == "CAD"
        assert locations[region].price_scope == "reference"

    assert locations["superstore_reference"].location_id == "1033"
    assert locations["nofrills_reference"].location_id == "3787"
    assert "defaultStoreId/masterStoreId" in (
        locations["superstore_reference"].reference_store_basis or ""
    )
    composite = locations["canada_reference"]
    assert composite.member_regions == (
        "metro_reference",
        "foodbasics_reference",
        "superstore_reference",
        "nofrills_reference",
    )
    assert {
        source: location.region
        for source, location in price_locations_for(
            composite, list(locations.values())
        ).items()
    } == {
        "metro": "metro_reference",
        "foodbasics": "foodbasics_reference",
        "superstore": "superstore_reference",
        "nofrills": "nofrills_reference",
    }


def test_load_fx_rates_keeps_usd_identity_and_reads_cad(tmp_path):
    path = tmp_path / "fx.json"
    path.write_text(json.dumps({
        "rates": {"CAD": {"to_usd": 0.72, "as_of": "2026-08-07"}}
    }))
    rates = load_fx_rates(path)
    assert rates["USD"]["to_usd"] == 1
    assert rates["CAD"]["to_usd"] == 0.72


def test_serialized_solution_keeps_native_cost_and_adds_usd_comparison():
    solution = Solution(
        status="optimal",
        message="ok",
        cost_per_day=10.0,
        basket=[{
            "meta": {"price_fetched_at": "2026-08-07", "price_stale": True}
        }],
        nutrients=[],
    )
    payload = serialize_solution(
        solution,
        mode="vegan",
        location_region="metro_reference",
        location_display="Metro Reference",
        currency="CAD",
        price_scope="reference",
        fx_rate={"to_usd": 0.72, "as_of": "2026-08-07"},
    )
    assert payload["cost_per_day"] == 10
    assert payload["cost_per_day_usd"] == pytest.approx(7.2)
    assert payload["currency"] == "CAD"
    assert payload["fx_as_of"] == "2026-08-07"
    assert payload["price_as_of"] == "2026-08-07"
    assert payload["has_stale_prices"] is True


def test_composite_catalog_cell_chooses_lowest_normalized_price():
    composite = Location(
        "canada_reference",
        "canada-reference",
        "All Canada Reference",
        "canada",
        "CAD",
        "reference",
        member_regions=("metro_reference", "foodbasics_reference"),
    )
    rows = [{
        "product_id": "large-package",
        "source": "metro",
        "kind": "food",
        "unit_grams": 1000,
        "prices_by_region": {
            "canada_reference": {
                "regular": 4.0, "promo": None, "effective": 4.0,
            },
        },
    }, {
        "product_id": "small-package",
        "source": "foodbasics",
        "kind": "food",
        "unit_grams": 500,
        "prices_by_region": {
            "canada_reference": {
                "regular": 3.0, "promo": None, "effective": 3.0,
            },
        },
    }]

    cell = _merge_prices(rows, [composite])["canada_reference"]

    assert cell["product_id"] == "large-package"
    assert cell["retailer"] == "metro"
    assert cell["unit_grams"] == 1000
