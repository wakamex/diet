from pathlib import Path

import yaml

from diet.foods import Location, load_all_skus, load_locations
from diet.supplements import build_supplement_foods, load_supplements


def test_initial_canadian_pass_accounts_for_every_food_concept():
    skus = load_all_skus()
    concepts = {
        sku.fdc_id for sku in skus if sku.source in {"kroger", "walmart"}
    }
    misses = yaml.safe_load(Path("data/canada_missing.yaml").read_text())

    assert len(concepts) == 85
    for retailer in ("metro", "foodbasics"):
        mapped = {sku.fdc_id for sku in skus if sku.source == retailer}
        explicit_misses = {
            int(row["fdc_id"])
            for row in misses
            if retailer in row["retailers"]
        }
        assert mapped.isdisjoint(explicit_misses)
        assert mapped | explicit_misses == concepts


def test_canadian_mappings_have_unique_positive_exact_skus_per_retailer():
    skus = load_all_skus()
    for retailer in ("metro", "foodbasics", "superstore", "nofrills"):
        rows = [sku for sku in skus if sku.source == retailer]
        assert len({sku.product_id for sku in rows}) == len(rows)
        assert all(sku.unit_grams > 0 for sku in rows)
        assert all(sku.dietary_categories for sku in rows)

    pcx_required = {
        169103, 169287, 169697, 172370, 172428, 173744,
        173884, 174266, 175186, 2257046, 2644283,
    }
    for retailer in ("superstore", "nofrills"):
        assert {sku.fdc_id for sku in skus if sku.source == retailer} == pcx_required


def test_canadian_supplements_use_exact_retailer_skus_and_label_profiles():
    supplements = {
        (supplement.product_id, supplement.source): supplement
        for supplement in load_supplements()
    }

    d3_metro = supplements[("064642052544", "metro")]
    d3_foodbasics = supplements[("064642052544", "foodbasics")]
    multivitamin = supplements[("064642098900", "metro")]
    foodbasics_multivitamin = supplements[("625273031867", "foodbasics")]
    metro_calcium = supplements[("064642026743", "metro")]
    foodbasics_calcium = supplements[("064642079619", "foodbasics")]
    superstore_multivitamin = supplements[("21589918_EA", "superstore")]
    nofrills_multivitamin = supplements[("21589918_EA", "nofrills")]
    superstore_calcium = supplements[("20316359001_EA", "superstore")]
    nofrills_d3 = supplements[("20299993_EA", "nofrills")]

    assert d3_metro.count == d3_foodbasics.count == 240
    assert d3_metro.nutrients_per_tablet == {"vit_d_mcg": 25}
    assert multivitamin.count == 115
    assert multivitamin.nutrients_per_tablet["vit_a_mcg"] == 700
    assert multivitamin.nutrients_per_tablet["vit_d_mcg"] == 20
    assert multivitamin.nutrients_per_tablet["zinc_mg"] == 11
    assert foodbasics_multivitamin.count == 90
    assert foodbasics_multivitamin.nutrients_per_tablet["vit_a_mcg"] == 750
    assert foodbasics_multivitamin.nutrients_per_tablet["vit_e_mg"] == 20
    assert foodbasics_multivitamin.nutrients_per_tablet["folate_mcg"] == 500
    assert foodbasics_multivitamin.nutrients_per_tablet["zinc_mg"] == 10
    assert metro_calcium.count == 200
    assert metro_calcium.max_tablets_per_day == 3
    assert metro_calcium.nutrients_per_tablet == {
        "calcium_mg": 333,
        "magnesium_mg": 167,
        "vit_d_mcg": 5,
    }
    assert foodbasics_calcium.count == 250
    assert foodbasics_calcium.max_tablets_per_day == 2
    assert foodbasics_calcium.nutrients_per_tablet == {
        "calcium_mg": 650,
        "vit_d_mcg": 10,
    }
    assert superstore_multivitamin.count == nofrills_multivitamin.count == 115
    assert superstore_multivitamin.nutrients_per_tablet == multivitamin.nutrients_per_tablet
    assert superstore_calcium.count == 200
    assert superstore_calcium.nutrients_per_tablet == metro_calcium.nutrients_per_tablet
    assert nofrills_d3.count == 240
    assert nofrills_d3.nutrients_per_tablet == {"vit_d_mcg": 25}


def test_pc_express_effective_price_semantics_reach_solution_metadata():
    supplement = next(
        item for item in load_supplements()
        if item.source == "superstore" and item.product_id == "21589918_EA"
    )
    location = Location(
        "superstore_reference", "1033", "Superstore Reference",
        "superstore", "CAD", "reference",
    )
    foods = build_supplement_foods(
        [supplement],
        location,
        {(supplement.product_id, "1033"): {
            "regular": 22.99,
            "promo": None,
            "price_kind": "effective",
            "channel": "pickup",
        }},
    )

    assert foods[0].meta["price_kind"] == "effective"
    assert foods[0].meta["price_channel"] == "pickup"


def test_composite_canada_supplements_keep_cheapest_duplicate_with_retailer():
    locations = load_locations()
    composite = next(item for item in locations if item.region == "canada_reference")
    supplements = [
        item for item in load_supplements()
        if item.product_id == "21589918_EA"
    ]
    prices = {
        ("21589918_EA", "1033"): {"regular": 22.99, "promo": None},
        ("21589918_EA", "3787"): {"regular": 20.99, "promo": None},
    }

    foods = build_supplement_foods(
        supplements, composite, prices, locations=locations
    )

    assert len(foods) == 1
    assert foods[0].sku_id == "nofrills:21589918_EA"
    assert foods[0].meta["price_retailer"] == "nofrills"
    assert foods[0].meta["location_id"] == "3787"
