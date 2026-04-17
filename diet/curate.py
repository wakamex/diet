"""Curate `data/skus.yaml` from `data/sku_candidates.yaml`.

For each desired food (CURATE_PICKS below):
  1. Find candidates matching `term` in the candidates file.
  2. Filter by `include`/`exclude` substrings (case-insensitive).
  3. Take the first surviving candidate (already ranked store-brand-then-cheapest
     by `discover`).
  4. Resolve `unit_grams` from Kroger `size` + `net_weight` via diet.units.
  5. Resolve `fdc_id` via FDC search using `fdc_query`.
  6. Emit a row with product_id, fdc_id, name, unit_grams, dietary_categories.

Run with: `diet curate` (uses FDC_API_KEY for the FDC search step).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from diet.sources.fdc import best_match
from diet.units import resolve_unit_grams
from diet.util import write_text_atomic

DEFAULT_CANDIDATES_PATH = Path("data/sku_candidates.yaml")
DEFAULT_OUT_PATH = Path("data/skus.yaml")


@dataclass(frozen=True)
class Pick:
    """One desired food in the final basket."""
    term: str                                # key in sku_candidates.yaml
    include: tuple[str, ...] = ()           # all of these must be in description
    exclude: tuple[str, ...] = ()           # none of these may be in description
    fdc_query: str = ""                     # passed to FDC search
    dietary_categories: tuple[str, ...] = ()
    grams_per_count: float | None = None    # for "ct"-only sizes when FDC lookup fails


# Desired ~30 foods covering all 5 dietary modes + B12/D for vegan.
CURATE_PICKS: list[Pick] = [
    # Grains
    Pick("white rice", include=("white", "long grain"), exclude=("instant", "brown", "wild", "spanish", "minute"),
         fdc_query="rice white long grain raw enriched",
         dietary_categories=("grain",)),
    Pick("rolled oats", include=("oats",), exclude=("instant", "flavored", "quick", "steel"),
         fdc_query="oats whole grain rolled old fashioned",
         dietary_categories=("grain",)),
    Pick("whole wheat bread", include=("whole wheat", "bread"), exclude=("english muffin", "bagel", "tortilla"),
         fdc_query="bread whole wheat",
         dietary_categories=("grain",)),
    Pick("pasta", include=("pasta",), exclude=("sauce", "salad", "shells and"),
         fdc_query="pasta dry enriched",
         dietary_categories=("grain",)),
    Pick("all purpose flour", include=("flour",), exclude=("self rising", "almond", "coconut", "tortilla"),
         fdc_query="wheat flour white all-purpose enriched",
         dietary_categories=("grain",)),
    # Legumes / plant protein
    Pick("dried lentils", include=("lentil",), exclude=("soup",),
         fdc_query="lentils dry",
         dietary_categories=("legume",)),
    Pick("canned chickpeas", include=("garbanzo",), exclude=("hummus",),
         fdc_query="chickpeas garbanzo canned",
         dietary_categories=("legume",)),
    Pick("dried navy beans", include=("navy",),
         fdc_query="beans navy mature seeds raw",
         dietary_categories=("legume",)),
    Pick("tofu firm", include=("tofu",), exclude=("teriyaki", "smoked", "marinated", "baked"),
         fdc_query="tofu raw firm prepared with calcium sulfate",
         dietary_categories=("legume", "soy")),
    Pick("edamame frozen", include=("edamame",),
         fdc_query="edamame frozen unprepared",
         dietary_categories=("legume", "soy")),
    Pick("natural peanut butter", include=("peanut butter",), exclude=("powder", "cup", "filled"),
         fdc_query="peanut butter smooth",
         dietary_categories=("legume", "nut")),
    # Dairy
    Pick("low fat milk gallon", include=("1% lowfat", "milk"), exclude=("chocolate", "strawberry", "carbmaster"),
         fdc_query="milk lowfat fluid 1% milkfat with added vitamin a and vitamin d",
         dietary_categories=("dairy",)),
    Pick("plain greek yogurt", include=("plain", "greek yogurt"), exclude=("vanilla", "strawberry"),
         fdc_query="yogurt greek plain nonfat",
         dietary_categories=("dairy",)),
    Pick("cheddar cheese", include=("cheddar",), exclude=("macaroni", "snack", "shells", "popcorn", "puff"),
         fdc_query="cheese cheddar",
         dietary_categories=("dairy",)),
    # Eggs
    Pick("large eggs grade a", include=("large", "eggs"), exclude=("liquid", "white", "extra"),
         fdc_query="egg whole raw fresh",
         dietary_categories=("egg",), grams_per_count=50.0),
    # Meat
    Pick("chicken breast boneless", include=("boneless", "chicken breast"), exclude=("breaded", "marinated", "seasoned", "tenders"),
         fdc_query="chicken broiler or fryer breast meat only raw",
         dietary_categories=("meat_white",)),
    Pick("ground beef 80 20", include=("80/20", "ground beef"), exclude=("patties", "burger"),
         fdc_query="beef ground 80% lean 20% fat raw",
         dietary_categories=("meat_red",)),
    # Fish
    Pick("canned tuna in water", include=("tuna", "water"), exclude=("oil", "pouch", "salad"),
         fdc_query="fish tuna light canned in water drained solids",
         dietary_categories=("fish",)),
    Pick("canned sardines", include=("sardines",), exclude=("hot sauce", "tomato", "mustard"),
         fdc_query="fish sardine atlantic canned in oil drained solids with bone",
         dietary_categories=("fish",)),
    # Vegetables
    Pick("frozen broccoli", include=("broccoli",), exclude=("cheese", "rice", "alfredo", "with"),
         fdc_query="broccoli frozen unprepared",
         dietary_categories=("vegetable",)),
    Pick("frozen spinach", include=("spinach",), exclude=("creamed", "garlic"),
         fdc_query="spinach frozen chopped or leaf unprepared",
         dietary_categories=("vegetable",)),
    Pick("carrots", include=("carrots",), exclude=("baby food", "stage", "cake", "puree"),
         fdc_query="carrots raw",
         dietary_categories=("vegetable",)),
    # Fruit
    Pick("bananas", include=("bananas",),
         exclude=("yogurt", "smoothie", "carbmaster", "tubes", "chips", "puffs",
                  "dried", "freez", "pepper", "gelato"),
         fdc_query="bananas raw",
         dietary_categories=("fruit",), grams_per_count=118.0),
    Pick("frozen mixed berries", include=("frozen", "berry"),
         exclude=("smoothie", "yogurt", "ice cream", "bar", "popsicle", "kids",
                  "no sugar added", "protein"),
         fdc_query="strawberries frozen unsweetened",
         dietary_categories=("fruit",)),
    # Fortified for vegan B12/D
    Pick("fortified soy milk", include=("soy", "milk"), exclude=("coconut", "almond", "oat", "cashew", "rice"),
         fdc_query="soymilk soy milk original and vanilla unsweetened with added calcium vitamins a and d",
         dietary_categories=("plant_milk", "fortified_b12")),
    Pick("nutritional yeast", include=("nutritional yeast",),
         fdc_query="yeast extract spread",
         dietary_categories=("fortified_b12",)),
    # Fats
    Pick("olive oil", include=("olive oil",),
         exclude=("mayo", "spray", "spread", "anchovies", "dressing", "sauce",
                  "sun dried", "tomato", "tomatoes", "sardines", "halved",
                  "infused", "truffle", "garlic", "butter"),
         fdc_query="oil olive salad or cooking",
         dietary_categories=("fat",)),
    Pick("vegetable oil", include=("vegetable oil",), exclude=("spread", "spray", "buttery"),
         fdc_query="oil vegetable industrial soybean refined for cooking",
         dietary_categories=("fat",)),
]


def _matches(desc: str, include: tuple[str, ...], exclude: tuple[str, ...]) -> bool:
    d = (desc or "").lower()
    if not all(s.lower() in d for s in include):
        return False
    if any(s.lower() in d for s in exclude):
        return False
    return True


def _pick_candidate(rows: list[dict], pick: Pick) -> dict | None:
    for r in rows:
        if _matches(r.get("description", ""), pick.include, pick.exclude):
            return r
    return None


def curate(
    candidates_path: Path | str = DEFAULT_CANDIDATES_PATH,
    out_path: Path | str = DEFAULT_OUT_PATH,
) -> tuple[int, list[str]]:
    """Build skus.yaml from candidates. Returns (n_picked, problem_messages)."""
    candidates = yaml.safe_load(Path(candidates_path).read_text(encoding="utf-8")) or {}
    out_rows: list[dict] = []
    problems: list[str] = []

    for pick in CURATE_PICKS:
        rows = candidates.get(pick.term) or []
        if not rows:
            problems.append(f"  no candidates returned for term {pick.term!r}")
            continue
        picked = _pick_candidate(rows, pick)
        if picked is None:
            problems.append(f"  no candidate matched include/exclude for term {pick.term!r}")
            continue

        # Resolve FDC id (auto search).
        fdc = best_match(pick.fdc_query) if pick.fdc_query else None
        fdc_id = fdc["fdcId"] if fdc else None
        if not fdc_id:
            problems.append(f"  no FDC match for {pick.term!r} (query: {pick.fdc_query!r})")
            continue

        # Resolve unit_grams.
        size = picked.get("size")
        netw = picked.get("net_weight")
        ps = resolve_unit_grams(
            description=picked.get("description", ""),
            size=size,
            net_weight_str=netw,
            fdc_id=fdc_id,
        )
        unit_grams = ps.grams
        if unit_grams is None and pick.grams_per_count is not None:
            # Last-resort per-count override defined on the Pick itself.
            from diet.units import parse_size
            sz = parse_size(size)
            if sz and sz[1] == "count":
                unit_grams = sz[0] * pick.grams_per_count
                ps_note = f"override {pick.grams_per_count}g/each (manual)"
            else:
                ps_note = ps.note
        else:
            ps_note = ps.note

        if unit_grams is None:
            problems.append(f"  could not resolve unit_grams for {pick.term!r}: {ps_note}")
            continue

        out_rows.append({
            "product_id": picked["product_id"],
            "fdc_id": int(fdc_id),
            "name": picked.get("description"),
            "unit_grams": round(unit_grams, 1),
            "dietary_categories": list(pick.dietary_categories),
            # Provenance fields aren't load-bearing but help review.
            "_size": size,
            "_net_weight": netw,
            "_unit_source": ps.source,
            "_fdc_match": fdc.get("description") if fdc else None,
            "_fdc_dataType": fdc.get("dataType") if fdc else None,
            "_kroger_categories": picked.get("categories"),
        })

    # Header comment + YAML body.
    header = (
        "# Curated Kroger SKUs — generated by `diet curate` from data/sku_candidates.yaml.\n"
        "# Re-run after editing data/discovery_terms.yaml or diet/curate.py rules.\n"
        "# Underscore-prefixed fields are provenance only; the loader (diet/foods.py)\n"
        "# ignores them.\n\n"
    )
    body = yaml.safe_dump(out_rows, sort_keys=False, allow_unicode=True, width=120)
    write_text_atomic(Path(out_path), header + body)
    return len(out_rows), problems
