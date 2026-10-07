"""Bulk Barn online catalog prices and online-order sales."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
import yaml

from diet.foods import Location, SkuSpec, load_all_skus
from diet.ingest import _ingest_bulkbarn_reference
from diet.sources.bulkbarn import (
    BulkBarnError,
    fetch_catalog,
    parse_catalog,
)

LOCATION = Location(
    region="bulkbarn", location_id="bulkbarn-catalog", display="Bulk Barn", source="bulkbarn",
    currency="CAD", price_scope="reference",
)
# Two items in the shape of product_data.js (trimmed), plus a packaged item
# with no per-100 g price.
CATALOG = """\
localStorage.setItem("timeStamp", "October 06 2026 09:06");
var products = [
{
	"Product_name_EN" 	: "Gluten Flour, Vital Wheat Gluten",
	"BBPLU" 		 	: "342",
	"Retail_Price" 		: "18.95",
	"Retail_Price_100g" 	: "1.895",
	"Sale_Price" 		: "",
	"Sale_Start_Date" 		: "08/06/2020 0:01",
	"Sale_End_Date" 		: "12/31/3020 23:59"
},
{
	"Product_name_EN" 	: "Dates, Loose Pack, Pits Removed",
	"BBPLU" 		 	: "1711",
	"Retail_Price_100g" 	: "0.958",
	"Sale_Price" 		: "7.18",
	"Sale_Start_Date" 		: "2026-10-01 00:01",
	"Sale_End_Date" 		: "2026-10-14 23:59"
},
{
	"Product_name_EN" 	: "Jamieson Lecithin 1,200 mg, 100 Capsules",
	"BBPLU" 		 	: "101646",
	"Retail_Price_100g" 	: ""
}
];
"""
def sku(plu: str) -> SkuSpec:
    return SkuSpec(product_id=plu, fdc_id=0, name=f"bin {plu}", unit_grams=100,
                   dietary_categories=frozenset(), max_serving_g=None, source="bulkbarn")


def catalog_fetch():
    return fetch_catalog(lambda url: (200, {}, CATALOG.encode()))


def test_catalog_gives_regular_price_per_100g_by_bin():
    items, updated = catalog_fetch()

    assert updated == "October 06 2026 09:06"
    assert set(items) == {"342", "1711"}
    assert items["342"].regular == 1.895
    assert items["342"].name == "Gluten Flour, Vital Wheat Gluten"


def test_sale_applies_only_between_its_dates_like_the_order_form():
    dates = catalog_fetch()[0]["1711"]

    assert dates.sale == pytest.approx(0.718)  # Sale_Price is per kg
    assert dates.sale_on(date(2026, 10, 1)) == pytest.approx(0.718)
    assert dates.sale_on(date(2026, 10, 14)) == pytest.approx(0.718)
    assert dates.sale_on(date(2026, 10, 15)) is None


def test_unrecognizable_catalog_is_an_error():
    with pytest.raises(BulkBarnError, match="format"):
        parse_catalog("<html>maintenance</html>")
    with pytest.raises(BulkBarnError, match="HTTP 503"):
        fetch_catalog(lambda url: (503, {}, b""))


def test_ingest_prices_bins_from_the_catalog_with_online_order_sales(tmp_path):
    rows, missing = _ingest_bulkbarn_reference(
        [sku("342"), sku("1711"), sku("999")], LOCATION, catalog_fetch, "2026-10-10", tmp_path / "raw",
    )

    by_id = {r["product_id"]: r for r in rows}
    assert by_id["342"]["regular"] == 1.895
    assert by_id["342"]["promo"] is None
    assert by_id["1711"]["promo"] == pytest.approx(0.718)
    assert by_id["1711"]["price_basis"] == "per_100g"
    assert [m["product_id"] for m in missing] == ["999"]
    assert (tmp_path / "raw" / "2026-10-10" / "bulkbarn.json").exists()


def test_failed_catalog_marks_every_bin_missing(tmp_path):
    def down():
        raise BulkBarnError("catalog request failed: timeout")

    rows, missing = _ingest_bulkbarn_reference(
        [sku("342"), sku("1711")], LOCATION, down, "2026-10-10", tmp_path,
    )

    assert rows == []
    assert len(missing) == 2


def test_mapped_bins_are_priced_per_100g():
    mapped = [
        row for row in yaml.safe_load(Path("data/canada_product_map.yaml").read_text())
        if row.get("sources") == ["bulkbarn"]
    ]

    assert mapped
    assert all(row["unit_grams"] == 100 for row in mapped)
    assert {s.product_id for s in load_all_skus() if s.source == "bulkbarn"} == {
        str(row["product_id"]) for row in mapped
    }
