import json

import pytest

from diet.export import load_fx_rates, serialize_solution
from diet.foods import load_locations
from diet.solver import Solution


def test_canadian_locations_are_native_cad_reference_scopes():
    locations = {location.region: location for location in load_locations()}
    for region in ("metro_reference", "foodbasics_reference"):
        assert locations[region].currency == "CAD"
        assert locations[region].price_scope == "reference"


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
