from diet.foods import Location, SkuSpec
from diet.ingest import _ingest_walmart


class FakeWalmartClient:
    def __init__(self):
        self.calls = []

    def product_details(self, item_id, *, store_id=None):
        self.calls.append((item_id, store_id))
        return {
            "itemId": int(item_id),
            "salePrice": 11.0 if store_id == "3478" else 8.98,
        }


class SearchFallbackWalmartClient:
    def __init__(self):
        self.search_calls = []

    def product_details(self, item_id, *, store_id=None):
        raise RuntimeError("details unavailable")

    def search(self, query, *, num_items=25, store_id=None):
        self.search_calls.append((query, num_items, store_id))
        return {
            "items": [
                {"itemId": 999, "salePrice": 1.0},
                {"itemId": 123, "salePrice": 2.5, "upc": "00123"},
            ]
        }


def test_walmart_ingest_routes_numeric_location_as_store_id(tmp_path):
    sku = SkuSpec(
        product_id="123", fdc_id=0, name="Cashews", unit_grams=100,
        dietary_categories=frozenset({"nut"}), max_serving_g=None,
        source="walmart",
    )
    locations = [
        Location("walmart_national", "walmart-national", "National", "walmart"),
        Location("hawaii", "3478", "Honolulu", "walmart"),
    ]
    client = FakeWalmartClient()
    rows, missing, nutrients, warnings = _ingest_walmart(
        [sku], locations, client, "2026-07-20", tmp_path / "raw", tmp_path / "fdc"
    )
    assert client.calls == [("123", None), ("123", "3478")]
    assert [(row["location_id"], row["regular"]) for row in rows] == [
        ("walmart-national", 8.98),
        ("3478", 11.0),
    ]
    assert missing == []
    assert nutrients == []
    assert warnings == []
    assert (tmp_path / "raw" / "2026-07-20" / "3478" / "123.json").exists()


def test_walmart_ingest_falls_back_to_exact_search_item(tmp_path):
    sku = SkuSpec(
        product_id="123", fdc_id=0, name="Exact Product", unit_grams=100,
        dietary_categories=frozenset(), max_serving_g=None, source="walmart",
    )
    location = Location(
        "walmart_national", "walmart-national", "National", "walmart"
    )
    client = SearchFallbackWalmartClient()

    rows, missing, nutrients, warnings = _ingest_walmart(
        [sku], [location], client, "2026-08-02", tmp_path / "raw", tmp_path / "fdc"
    )

    assert client.search_calls == [("Exact Product", 25, None)]
    assert rows == [{
        "product_id": "123", "location_id": "walmart-national",
        "regular": 2.5, "promo": None, "fetched_at": "2026-08-02",
    }]
    assert missing == []
    assert nutrients == []
    assert warnings == []
