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
