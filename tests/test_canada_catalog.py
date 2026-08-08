from pathlib import Path

import yaml

from diet.foods import load_all_skus


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
