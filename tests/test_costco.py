"""costco.ca product-page prices and Costco catalog entries."""

from pathlib import Path

from diet.foods import Location, SkuSpec, load_all_skus
from diet.ingest import _ingest_product_page_reference
from diet.sources.costco import COSTCO_PRODUCT_ROOT, COSTCO_SOURCE, CostcoClient
from diet.supplements import load_supplements

PAGE = b"""<html><head><script type="application/ld+json">
{"@context":"https://schema.org","@type":"Product",
 "name":"Kirkland Signature Calcium Plus With Vitamin D3 & Minerals 600 mg | 800 IU, 500 Tablets",
 "sku":"462461",
 "offers":{"@type":"Offer",
   "url":"https://www.costco.ca/p/-/kirkland-signature-calcium-plus-with-vitamin-d3-minerals-600-mg-800-iu-500-tablets/100291275",
   "availability":"https://schema.org/OutOfStock","priceCurrency":"CAD","price":22.99}}
</script></head></html>"""


def test_quotes_an_item_number_from_its_product_page():
    urls = []

    def transport(url, **kwargs):
        urls.append(url)
        return 200, {}, PAGE

    quote = CostcoClient(transport=transport).quote_product("100291275")

    assert urls == [COSTCO_PRODUCT_ROOT + "100291275"]
    assert quote.effective_price_cad == 22.99
    assert quote.source == COSTCO_SOURCE
    assert quote.source_url.endswith("/100291275")


# A costco.ca page during a "$3 OFF" offer, cut down from item 1412124 on
# 2026-10-27: JSON-LD has the regular price, and the app data pushed in a
# script string (so with escaped quotes) has the item's price after discounts,
# next to a related item's own priceInfo.
SALE_PAGE = rb"""<html><head><script type="application/ld+json">
{"@context":"https://schema.org","@type":"Product","name":"Quaker Quick Oats, 2 \u00d7 2.58 kg","sku":"1412124",
 "offers":{"@type":"Offer","url":"https://www.costco.ca/p/-/quaker-quick-oats-2-258-kg/100570610",
   "availability":"https://schema.org/InStock","priceCurrency":"CAD","price":13.99}}
</script></head><body>
<script>self.__next_f.push([1,"{\"priceInfo\":{\"id\":\"9999999\",\"warehouseNumber\":\"894\",\"displayPrice\":{\"onlinePrice\":13.99,\"aggregatedDiscountAmt\":5,\"deliveredPrice\":8.99,\"currency\":\"CAD\"}},\"priceInfo\":{\"id\":\"1412124\",\"clientId\":\"e442e6e6-2602-4a39-937b-8b28b4457ed3\",\"warehouseNumber\":\"894\",\"locale\":\"en-ca\",\"displayPrice\":{\"onlinePrice\":13.99,\"aggregatedDiscountAmt\":3,\"deliveredPrice\":10.99,\"currency\":\"CAD\",\"warehouseNumber\":\"894\",\"uom\":null,\"factor\":0,\"tierPrices\":null}}}"])</script>
</body></html>"""


def _client(page):
    return CostcoClient(transport=lambda url, **kwargs: (200, {}, page))


def test_discount_from_the_app_data_becomes_the_promo_price():
    quote = _client(SALE_PAGE).quote_product("1412124")

    assert quote.effective_price_cad == 13.99
    assert quote.promo_price_cad == 10.99  # this item's discount, not the related item's


def test_no_promo_without_a_discount_or_when_prices_disagree():
    assert _client(PAGE).quote_product("100291275").promo_price_cad is None
    stale = SALE_PAGE.replace(b'"price":13.99', b'"price":12.99')
    assert _client(stale).quote_product("1412124").promo_price_cad is None


def test_ingest_records_the_promo_price(tmp_path):
    sku = SkuSpec(product_id="1412124", fdc_id=1, name="Quaker Quick Oats", unit_grams=5160,
                  dietary_categories=frozenset({"grain"}), max_serving_g=None, source="costco")
    location = Location(region="costco", location_id="costco-catalog", display="Costco", source="costco",
                        currency="CAD", price_scope="reference")

    rows, missing = _ingest_product_page_reference([sku], location, _client(SALE_PAGE), "2026-10-27", tmp_path)

    assert missing == []
    assert (rows[0]["regular"], rows[0]["promo"]) == (13.99, 10.99)


def test_costco_items_load_as_costco_products_and_pills():
    foods = {s.product_id for s in load_all_skus() if s.source == "costco"}
    pills = {s.product_id: s for s in load_supplements(Path("data/supplements.yaml")) if s.source == "costco"}

    assert {"4000339745", "100539558", "100559709"} <= foods
    assert pills["100291275"].nutrients_per_tablet == {"calcium_mg": 600, "vit_d_mcg": 20}
    assert pills["100322373"].count == 720
