import json

import pytest

from diet.foods import Location, SkuSpec, build_foods_for_location
from diet.nutrition import (
    extract_fdc_branded_nutrition,
    extract_kroger_nutrition,
    load_nutrition_overrides,
    merge_with_usda_fallback,
)


def _kroger_product(serving, nutrients, *, servings=10):
    return {
        "upc": "001234567890",
        "nutritionInformation": [{
            "servingSize": serving,
            "servingsPerPackage": {"value": servings},
            "ingredientStatement": "Peanuts, salt.",
            "nutrients": nutrients,
        }],
    }


def test_kroger_label_normalizes_declared_gram_serving():
    product = _kroger_product(
        {"quantity": 32, "unitOfMeasure": {"code": "GRM"}},
        [
            {"code": "ENER-", "displayName": "Calories", "quantity": 180,
             "unitOfMeasure": {"code": "D70", "name": "Calorie - International Table (IT)"}},
            {"code": "PRO-", "displayName": "Protein", "quantity": 7,
             "unitOfMeasure": {"code": "GRM"}},
            {"code": "NA", "displayName": "Sodium", "quantity": 150,
             "unitOfMeasure": {"code": "MGM"}},
        ],
        servings=14,
    )
    row, warnings = extract_kroger_nutrition(
        product, product_id="sku", package_grams=453.6, fetched_at="2026-07-20"
    )
    assert row is not None
    assert row["serving_size_g"] == 32
    assert row["nutrients_per_g"]["energy_kcal"] == pytest.approx(180 / 32)
    assert row["nutrients_per_g"]["protein_g"] == pytest.approx(7 / 32)
    assert row["nutrients_per_g"]["sodium_mg"] == pytest.approx(150 / 32)
    assert row["nutrient_sources"]["protein_g"] == "kroger_label"
    assert warnings == []


def test_kroger_label_infers_household_serving_from_package_count():
    product = _kroger_product(
        {"quantity": 0.25, "unitOfMeasure": {"code": "G21", "name": "Cup US"}},
        [{"code": "PRO-", "displayName": "Protein", "quantity": 6,
          "unitOfMeasure": {"code": "GRM"}}],
        servings=15,
    )
    row, _ = extract_kroger_nutrition(
        product, product_id="sku", package_grams=453.6, fetched_at="2026-07-20"
    )
    assert row is not None
    assert row["serving_basis"] == "package_weight_divided_by_servings"
    assert row["serving_size_g"] == pytest.approx(30.24)
    assert row["nutrients_per_g"]["protein_g"] == pytest.approx(6 / 30.24)


def test_kroger_label_flags_package_serving_count_mismatch_but_keeps_gram_basis():
    product = _kroger_product(
        {"quantity": 30, "unitOfMeasure": {"code": "GRM"}},
        [{"code": "PRO-", "displayName": "Protein", "quantity": 6,
          "unitOfMeasure": {"code": "GRM"}}],
        servings=4,
    )
    row, warnings = extract_kroger_nutrition(
        product, product_id="sku", package_grams=907.2, fetched_at="2026-07-20"
    )
    assert row is not None
    assert row["serving_size_g"] == 30
    assert "inconsistent with package weight" in warnings[0]


def test_merge_uses_exact_values_and_usda_only_for_missing_nutrients():
    exact = {
        "nutrients_per_g": {"energy_kcal": 5.625, "protein_g": 0.21875},
        "nutrient_sources": {
            "energy_kcal": "kroger_label",
            "protein_g": "kroger_label",
        },
    }
    values, sources = merge_with_usda_fallback(
        {"energy_kcal": 5.88, "protein_g": 0.22, "ala_g": 0.001},
        fdc_id=123,
        sku_row=exact,
    )
    assert values == {"energy_kcal": 5.625, "protein_g": 0.21875, "ala_g": 0.001}
    assert sources == {
        "energy_kcal": "kroger_label",
        "protein_g": "kroger_label",
        "ala_g": "usda_reference:123",
    }


def test_fdc_branded_snapshot_records_exact_upc_provenance():
    food = {
        "fdcId": 456,
        "description": "EXACT PRODUCT",
        "servingSize": 28,
        "servingSizeUnit": "GRM",
        "foodNutrients": [
            {"nutrient": {"name": "Protein"}, "amount": 20},
        ],
    }
    row = extract_fdc_branded_nutrition(
        food, product_id="item", source="walmart", upc="0123",
        fetched_at="2026-07-20",
    )
    assert row is not None
    assert row["nutrients_per_g"]["protein_g"] == pytest.approx(0.2)
    assert row["nutrient_sources"]["protein_g"] == "usda_branded_upc:456"
    assert row["source_details"]["usda_branded_upc:456"]["fdc_id"] == 456


def test_food_builder_overlays_sku_snapshot_and_exposes_provenance(
    tmp_path, monkeypatch
):
    snapshot = {
        "nutrients": [{
            "source": "kroger",
            "product_id": "sku",
            "nutrients_per_g": {"protein_g": 0.25},
            "nutrient_sources": {"protein_g": "kroger_label"},
            "upc": "00123",
            "serving_size_g": 20,
            "serving_basis": "declared_grams",
            "source_details": {"kroger_label": {"kind": "retailer_nutrition_facts"}},
        }]
    }
    path = tmp_path / "nutrients.json"
    path.write_text(json.dumps(snapshot))
    monkeypatch.setattr(
        "diet.foods.fdc_mod.fetch_food_cached",
        lambda *args, **kwargs: {"foodNutrients": [
            {"nutrient": {"name": "Protein"}, "amount": 10},
            {"nutrient": {"name": "PUFA 18:3"}, "amount": 1},
        ]},
    )
    sku = SkuSpec(
        product_id="sku", fdc_id=123, name="Food", unit_grams=100,
        dietary_categories=frozenset({"nut"}), max_serving_g=None,
    )
    location = Location(region="test", location_id="loc", display="Test")
    foods = build_foods_for_location(
        [sku], location,
        {("sku", "loc"): {"regular": 2.0, "promo": None}},
        nutrients_path=path,
    )
    assert foods[0].nutrients_per_g["protein_g"] == 0.25
    assert foods[0].nutrients_per_g["ala_g"] == pytest.approx(0.01)
    assert foods[0].meta["nutrient_sources"] == {
        "protein_g": "kroger_label",
        "ala_g": "usda_reference:123",
    }


def test_manual_override_normalizes_serving_and_preserves_source(tmp_path):
    path = tmp_path / "overrides.yaml"
    path.write_text("""
- source: walmart
  product_id: "123"
  serving_size_g: 40
  serving_basis: "manufacturer label"
  source_id: "manufacturer:test"
  source_url: "https://example.test/label"
  source_title: "Test label"
  accessed: "2026-07-20"
  derived_from_daily_value: [zinc_mg]
  nutrients_per_serving:
    protein_g: 5
    zinc_mg: 2
""")
    row = load_nutrition_overrides(path)[("walmart", "123")]
    assert row["nutrients_per_g"] == {"protein_g": 0.125, "zinc_mg": 0.05}
    assert row["nutrient_sources"]["zinc_mg"] == "manufacturer:test"
    details = row["source_details"]["manufacturer:test"]
    assert details["url"] == "https://example.test/label"
    assert details["derived_from_daily_value"] == ["zinc_mg"]
