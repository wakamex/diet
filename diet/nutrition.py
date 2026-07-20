"""Normalize and persist nutrition tied to an exact retail SKU.

Retail Nutrition Facts are authoritative for the nutrients they declare, but
they are intentionally incomplete for diet-optimization purposes.  This module
stores those declared values per gram plus per-nutrient provenance; foods.py
fills every undeclared nutrient from the curated generic USDA record.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from diet.sources.fdc import nutrients_per_g as fdc_nutrients_per_g
from diet.util import read_json

DEFAULT_NUTRIENTS_PATH = Path("data/nutrients_current.json")
DEFAULT_OVERRIDES_PATH = Path("data/nutrition_overrides.yaml")

# Prefer Kroger's stable nutrient codes, with display-name fallbacks for older
# or sparsely coded catalog records.
_KROGER_CODE_MAP = {
    "ENER-": "energy_kcal",
    "PRO-": "protein_g",
    "FIBTSW": "fiber_g",
    "VITA": "vit_a_mcg",
    "VITC": "vit_c_mg",
    "VITD": "vit_d_mcg",
    "TOCPHA": "vit_e_mg",
    "VITB12": "vit_b12_mcg",
    "FOLDFE": "folate_mcg",
    "CA": "calcium_mg",
    "FE": "iron_mg",
    "MG": "magnesium_mg",
    "K": "potassium_mg",
    "NA": "sodium_mg",
    "ZN": "zinc_mg",
}

_KROGER_NAME_MAP = {
    "calories": "energy_kcal",
    "energy": "energy_kcal",
    "protein": "protein_g",
    "dietary fiber": "fiber_g",
    "fiber": "fiber_g",
    "alpha-linolenic acid": "ala_g",
    "alpha-linolenic acid (ala)": "ala_g",
    "ala": "ala_g",
    "vitamin a": "vit_a_mcg",
    "vitamin c": "vit_c_mg",
    "vitamin d": "vit_d_mcg",
    "vitamin e": "vit_e_mg",
    "vitamin b12": "vit_b12_mcg",
    "vitamin b-12": "vit_b12_mcg",
    "folate": "folate_mcg",
    "folate, dfe": "folate_mcg",
    "calcium": "calcium_mg",
    "iron": "iron_mg",
    "magnesium": "magnesium_mg",
    "potassium": "potassium_mg",
    "sodium": "sodium_mg",
    "zinc": "zinc_mg",
}

_GRAM_UNITS = {"GRM", "G", "GRAM", "GRAMS"}
_MILLIGRAM_UNITS = {"MGM", "MG", "MILLIGRAM", "MILLIGRAMS"}
_MICROGRAM_UNITS = {"MC", "MCG", "UG", "MICROGRAM", "MICROGRAMS"}
_KCAL_UNITS = {"D70", "E14", "E15", "KCAL", "CAL", "CALORIE", "CALORIES"}

_CANONICAL_UNIT = {
    "energy_kcal": "kcal",
    "protein_g": "g",
    "fiber_g": "g",
    "ala_g": "g",
    "vit_a_mcg": "mcg",
    "vit_c_mg": "mg",
    "vit_d_mcg": "mcg",
    "vit_e_mg": "mg",
    "vit_b12_mcg": "mcg",
    "folate_mcg": "mcg",
    "calcium_mg": "mg",
    "iron_mg": "mg",
    "magnesium_mg": "mg",
    "potassium_mg": "mg",
    "sodium_mg": "mg",
    "zinc_mg": "mg",
}


def _unit_tokens(unit: dict[str, Any]) -> set[str]:
    return {
        str(unit.get("code") or "").strip().upper(),
        str(unit.get("name") or "").strip().upper(),
    }


def _amount_in_canonical_unit(
    nutrient: str,
    amount: float,
    unit: dict[str, Any],
) -> float | None:
    """Convert a label amount to the unit encoded in our canonical id."""
    tokens = _unit_tokens(unit)
    target = _CANONICAL_UNIT[nutrient]
    if target == "kcal":
        return amount if tokens & _KCAL_UNITS else None
    if target == "g":
        if tokens & _GRAM_UNITS:
            return amount
        if tokens & _MILLIGRAM_UNITS:
            return amount / 1_000.0
        if tokens & _MICROGRAM_UNITS:
            return amount / 1_000_000.0
        return None
    if target == "mg":
        if tokens & _MILLIGRAM_UNITS:
            return amount
        if tokens & _GRAM_UNITS:
            return amount * 1_000.0
        if tokens & _MICROGRAM_UNITS:
            return amount / 1_000.0
        return None
    if target == "mcg":
        if tokens & _MICROGRAM_UNITS:
            return amount
        if tokens & _MILLIGRAM_UNITS:
            return amount * 1_000.0
        # Vitamin D has an exact IU conversion. Vitamin A does not: its RAE
        # conversion depends on whether the source is retinol or carotenoids.
        if nutrient == "vit_d_mcg" and "IU" in tokens:
            return amount * 0.025
        return None
    return None


def _serving_grams(
    info: dict[str, Any],
    package_grams: float,
) -> tuple[float | None, str | None, list[str]]:
    warnings: list[str] = []
    serving = info.get("servingSize") or {}
    quantity = serving.get("quantity")
    unit = serving.get("unitOfMeasure") or {}
    tokens = _unit_tokens(unit)
    grams: float | None = None
    basis: str | None = None

    if quantity is not None and tokens & _GRAM_UNITS:
        grams = float(quantity)
        basis = "declared_grams"
    else:
        servings = info.get("servingsPerPackage") or {}
        count = servings.get("value")
        if count is None:
            count = servings.get("description")
        try:
            count_f = float(count)
        except (TypeError, ValueError):
            count_f = 0.0
        if count_f > 0 and package_grams > 0:
            grams = package_grams / count_f
            basis = "package_weight_divided_by_servings"

    if grams is None:
        return None, None, ["serving size cannot be converted to grams"]
    if grams <= 0 or grams > package_grams * 1.05:
        return None, None, [
            f"implausible serving size {grams:g} g for {package_grams:g} g package"
        ]

    servings = info.get("servingsPerPackage") or {}
    count = servings.get("value")
    if basis == "declared_grams" and count is not None:
        declared_total = grams * float(count)
        if package_grams > 0 and abs(declared_total - package_grams) / package_grams > 0.25:
            warnings.append(
                "serving count is inconsistent with package weight "
                f"({count} × {grams:g} g != {package_grams:g} g)"
            )
    return grams, basis, warnings


def extract_kroger_nutrition(
    product: dict[str, Any],
    *,
    product_id: str,
    package_grams: float,
    fetched_at: str,
) -> tuple[dict[str, Any] | None, list[str]]:
    """Extract the best usable Nutrition Facts panel from a Kroger product."""
    candidates: list[tuple[int, dict[str, Any], float, str, list[str]]] = []
    all_warnings: list[str] = []
    for info in product.get("nutritionInformation") or []:
        serving_g, basis, warnings = _serving_grams(info, package_grams)
        if serving_g is None or basis is None:
            all_warnings.extend(warnings)
            continue
        values: dict[str, float] = {}
        skipped_units: list[str] = []
        for entry in info.get("nutrients") or []:
            amount = entry.get("quantity")
            if amount is None:
                continue
            code = str(entry.get("code") or "").upper()
            display = str(entry.get("displayName") or "").strip().lower()
            nutrient = _KROGER_CODE_MAP.get(code) or _KROGER_NAME_MAP.get(display)
            if nutrient is None:
                continue
            converted = _amount_in_canonical_unit(
                nutrient, float(amount), entry.get("unitOfMeasure") or {}
            )
            if converted is None:
                skipped_units.append(entry.get("displayName") or code)
                continue
            if converted < 0:
                continue
            values.setdefault(nutrient, converted / serving_g)
        if skipped_units:
            warnings.append("unsupported label units for: " + ", ".join(skipped_units))
        if values:
            candidates.append((len(values), info, serving_g, basis, warnings))

    if not candidates:
        if not all_warnings:
            all_warnings.append("no usable structured Nutrition Facts panel")
        return None, all_warnings

    _, info, serving_g, basis, warnings = max(candidates, key=lambda row: row[0])
    values: dict[str, float] = {}
    for entry in info.get("nutrients") or []:
        amount = entry.get("quantity")
        if amount is None:
            continue
        code = str(entry.get("code") or "").upper()
        display = str(entry.get("displayName") or "").strip().lower()
        nutrient = _KROGER_CODE_MAP.get(code) or _KROGER_NAME_MAP.get(display)
        if nutrient is None:
            continue
        converted = _amount_in_canonical_unit(
            nutrient, float(amount), entry.get("unitOfMeasure") or {}
        )
        if converted is not None and converted >= 0:
            values.setdefault(nutrient, converted / serving_g)

    source_id = "kroger_label"
    row = {
        "product_id": product_id,
        "source": "kroger",
        "upc": str(product.get("upc") or product_id),
        "serving_size_g": round(serving_g, 6),
        "serving_basis": basis,
        "ingredients": info.get("ingredientStatement"),
        "nutrients_per_g": values,
        "nutrient_sources": {key: source_id for key in values},
        "source_details": {
            source_id: {"kind": "retailer_nutrition_facts", "fetched_at": fetched_at}
        },
    }
    return row, warnings


def extract_fdc_branded_nutrition(
    food: dict[str, Any],
    *,
    product_id: str,
    source: str,
    upc: str,
    fetched_at: str,
) -> dict[str, Any] | None:
    """Create an exact-SKU snapshot from a USDA Branded record matched by UPC."""
    values = fdc_nutrients_per_g(food)
    if not values:
        return None
    fdc_id = int(food["fdcId"])
    source_id = f"usda_branded_upc:{fdc_id}"
    serving_size = food.get("servingSize")
    serving_unit = str(food.get("servingSizeUnit") or "").upper()
    serving_g = float(serving_size) if serving_size is not None and serving_unit in _GRAM_UNITS else None
    return {
        "product_id": product_id,
        "source": source,
        "upc": upc,
        "serving_size_g": serving_g,
        "serving_basis": "usda_branded_record",
        "ingredients": food.get("ingredients"),
        "nutrients_per_g": values,
        "nutrient_sources": {key: source_id for key in values},
        "source_details": {
            source_id: {
                "kind": "usda_branded_exact_upc",
                "fdc_id": fdc_id,
                "publication_date": food.get("publicationDate"),
                "fetched_at": fetched_at,
            }
        },
    }


def load_nutrition_overrides(
    path: Path | str = DEFAULT_OVERRIDES_PATH,
) -> dict[tuple[str, str], dict[str, Any]]:
    """Load auditable manually sourced Nutrition Facts overrides."""
    path = Path(path)
    if not path.exists():
        return {}
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    out: dict[tuple[str, str], dict[str, Any]] = {}
    for entry in raw:
        serving_g = float(entry["serving_size_g"])
        if serving_g <= 0:
            raise ValueError(f"non-positive serving size in {path}: {entry['product_id']}")
        per_serving = entry.get("nutrients_per_serving") or {}
        values = {key: float(value) / serving_g for key, value in per_serving.items()}
        source_id = str(entry["source_id"])
        row = {
            "product_id": str(entry["product_id"]),
            "source": str(entry["source"]),
            "upc": str(entry.get("upc") or ""),
            "serving_size_g": serving_g,
            "serving_basis": str(entry["serving_basis"]),
            "ingredients": entry.get("ingredients"),
            "nutrients_per_g": values,
            "nutrient_sources": {key: source_id for key in values},
            "source_details": {
                source_id: {
                    "kind": "manufacturer_nutrition_facts",
                    "url": str(entry["source_url"]),
                    "title": str(entry["source_title"]),
                    "accessed": str(entry["accessed"]),
                    "derived_from_daily_value": list(
                        entry.get("derived_from_daily_value") or []
                    ),
                    "notes": list(entry.get("notes") or []),
                }
            },
        }
        out[(row["source"], row["product_id"])] = row
    return out


def load_sku_nutrients(
    path: Path | str = DEFAULT_NUTRIENTS_PATH,
    *,
    overrides_path: Path | str = DEFAULT_OVERRIDES_PATH,
) -> dict[tuple[str, str], dict[str, Any]]:
    path = Path(path)
    out: dict[tuple[str, str], dict[str, Any]] = {}
    if path.exists():
        payload = read_json(path)
        out.update({
            (str(row["source"]), str(row["product_id"])): row
            for row in payload.get("nutrients") or []
        })
    # Curated manufacturer labels deliberately take priority over automated
    # retailer/USDA records and retain their own per-nutrient provenance.
    out.update(load_nutrition_overrides(overrides_path))
    return out


def merge_with_usda_fallback(
    fallback: dict[str, float],
    *,
    fdc_id: int,
    sku_row: dict[str, Any] | None,
) -> tuple[dict[str, float], dict[str, str]]:
    """Overlay exact-SKU values and return effective values plus provenance."""
    values = dict(fallback)
    sources = {key: f"usda_reference:{fdc_id}" for key in fallback}
    if sku_row:
        exact = sku_row.get("nutrients_per_g") or {}
        exact_sources = sku_row.get("nutrient_sources") or {}
        for key, value in exact.items():
            values[key] = float(value)
            sources[key] = str(exact_sources.get(key) or "sku_label")
    return values, sources
