from pathlib import Path

import yaml

from diet.foods import load_all_skus
from diet.supplements import load_supplements


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
    for retailer in ("metro", "foodbasics"):
        rows = [sku for sku in skus if sku.source == retailer]
        assert len({sku.product_id for sku in rows}) == len(rows)
        assert all(sku.unit_grams > 0 for sku in rows)
        assert all(sku.dietary_categories for sku in rows)


def test_canadian_supplements_use_exact_retailer_skus_and_label_profiles():
    supplements = {
        (supplement.product_id, supplement.source): supplement
        for supplement in load_supplements()
    }

    d3_metro = supplements[("064642052544", "metro")]
    d3_foodbasics = supplements[("064642052544", "foodbasics")]
    multivitamin = supplements[("064642098900", "metro")]
    calcium_d3 = supplements[("064642061164", "foodbasics")]

    assert d3_metro.count == d3_foodbasics.count == 240
    assert d3_metro.nutrients_per_tablet == {"vit_d_mcg": 25}
    assert multivitamin.count == 115
    assert multivitamin.nutrients_per_tablet["vit_a_mcg"] == 700
    assert multivitamin.nutrients_per_tablet["vit_d_mcg"] == 20
    assert multivitamin.nutrients_per_tablet["zinc_mg"] == 11
    assert calcium_d3.count == 90
    assert calcium_d3.nutrients_per_tablet == {
        "calcium_mg": 500,
        "vit_d_mcg": 25,
    }
