"""costco.ca product-page prices and Costco catalog entries."""

from pathlib import Path

from diet.foods import load_all_skus
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


def test_costco_items_load_as_costco_products_and_pills():
    foods = {s.product_id for s in load_all_skus() if s.source == "costco"}
    pills = {s.product_id: s for s in load_supplements(Path("data/supplements.yaml")) if s.source == "costco"}

    assert {"4000339745", "100539558", "100559709"} <= foods
    assert pills["100291275"].nutrients_per_tablet == {"calcium_mg": 600, "vit_d_mcg": 20}
    assert pills["100322373"].count == 720
