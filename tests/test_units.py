"""Tests for the deterministic unit parser."""

import pytest

from diet.units import (
    LB_TO_G,
    OZ_TO_G,
    parse_kroger_netweight,
    parse_size,
    resolve_unit_grams,
)


def test_netweight_lb_av():
    assert parse_kroger_netweight("2.0 [lb_av]") == pytest.approx(907.18, rel=1e-3)


def test_netweight_grams():
    assert parse_kroger_netweight("907 [g]") == 907


def test_netweight_none_for_missing_or_bad():
    assert parse_kroger_netweight(None) is None
    assert parse_kroger_netweight("") is None
    assert parse_kroger_netweight("about 5 lb") is None  # no brackets


def test_parse_size_weight():
    assert parse_size("32 oz") == (32 * OZ_TO_G, "weight")
    assert parse_size("5 lb") == (5 * LB_TO_G, "weight")


def test_parse_size_volume():
    g, kind = parse_size("1 gal")
    assert kind == "volume"
    assert g == pytest.approx(3785.41, rel=1e-3)


def test_parse_size_count():
    assert parse_size("18 ct") == (18.0, "count")
    assert parse_size("12 each") == (12.0, "count")


def test_parse_size_handles_leading_fraction():
    """'1/2 gal' must be 0.5 gal, not 2 gal — earlier regex was greedy."""
    g, kind = parse_size("1/2 gal")
    assert kind == "volume"
    assert g == pytest.approx(0.5 * 3785.4118, rel=1e-3)
    g2, _ = parse_size("3/4 lb")
    assert g2 == pytest.approx(0.75 * LB_TO_G, rel=1e-3)


def test_parse_size_prefers_weight_over_count():
    # "8 ct / 26 oz" — picks the weight component.
    g, kind = parse_size("8 ct / 26 oz")
    assert kind == "weight"
    assert g == pytest.approx(26 * OZ_TO_G, rel=1e-3)


def test_resolve_uses_netweight_when_consistent_with_size():
    p = resolve_unit_grams(
        description="Kroger Long Grain White Rice",
        size="32 oz",
        net_weight_str="2.0 [lb_av]",
    )
    assert p.source == "netWeight"
    assert p.grams == pytest.approx(907.18, rel=1e-3)


def test_resolve_falls_back_to_size_when_netweight_disagrees():
    # Eggs case: 18 ct package, Kroger reports per-egg netWeight 0.13 lb.
    p = resolve_unit_grams(
        description="Kroger Grade A Large White Eggs",
        size="18 ct",
        net_weight_str="0.13 [lb_av]",
    )
    # Without a known fdc_id we'd hit the per-unit fallback path.
    assert p.grams == pytest.approx(18 * 0.13 * LB_TO_G, rel=1e-2)
    assert "per-unit" in p.note


def test_resolve_uses_per_count_when_fdc_known():
    p = resolve_unit_grams(
        description="Kroger Grade A Large White Eggs",
        size="18 ct",
        net_weight_str=None,
        fdc_id=748967,
    )
    assert p.grams == pytest.approx(18 * 50.0, rel=0)
    assert "FDC" in p.note


def test_resolve_volume_with_milk_density():
    p = resolve_unit_grams(
        description="Kroger Whole Milk",
        size="1 gal",
        net_weight_str=None,
    )
    # 1 gal = 3785.41 mL × 1.030 g/mL = 3899 g
    assert p.grams == pytest.approx(3785.41 * 1.030, rel=1e-3)
    assert "1.03" in p.note


def test_resolve_returns_none_for_count_only_unknown():
    p = resolve_unit_grams(
        description="Mystery Snack",
        size="3 ct",
        net_weight_str=None,
    )
    assert p.grams is None
    assert "override" in p.note
