"""Tests for Kroger client helper functions (no live API calls)."""

from diet.sources.kroger import effective_price, extract_price


def test_extract_price_returns_regular_and_promo():
    product = {"items": [{"price": {"regular": 3.99, "promo": 2.99}}]}
    assert extract_price(product) == (3.99, 2.99)


def test_extract_price_handles_missing_promo():
    product = {"items": [{"price": {"regular": 1.49}}]}
    assert extract_price(product) == (1.49, None)


def test_extract_price_handles_no_items():
    assert extract_price({}) == (None, None)
    assert extract_price({"items": []}) == (None, None)


def test_extract_price_treats_zero_promo_as_none():
    product = {"items": [{"price": {"regular": 3.99, "promo": 0}}]}
    _, promo = extract_price(product)
    assert promo is None


def test_effective_price_prefers_promo():
    assert effective_price(3.99, 2.99) == 2.99
    assert effective_price(3.99, None) == 3.99
    assert effective_price(None, 2.99) == 2.99
    assert effective_price(None, None) is None
