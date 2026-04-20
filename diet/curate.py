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
    Pick("brown rice", include=("brown rice",),
         exclude=("instant", "minute", "pilaf", "seasoned", "flavored", "chip",
                  "cake", "cracker", "spanish", "blend", "wild", "vegetable",
                  "cauliflower", "fried", "sushi"),
         fdc_query="rice brown long-grain raw",
         dietary_categories=("grain",)),
    # Pearled barley — try both bare and pearled terms; Kroger often lists it
    # without the "pearled" qualifier. First term with a match wins at LP time.
    Pick("barley", include=("barley",),
         exclude=("soup", "juice", "malt", "beer", "drink", "malted", "energy",
                  "grass", "wheat grass", "dog", "cat", "pet", "wet food",
                  "quinoa", "brown rice", "bowl", "beef and", "beef with",
                  "oatmeal", "toddler", "baby", "stage", "freshly", "cereal"),
         fdc_query="barley pearled raw",
         dietary_categories=("grain",)),
    Pick("wheat germ", include=("wheat germ",),
         exclude=("oil", "bread", "cookie", "cracker", "bar", "mix", "muffin"),
         fdc_query="wheat germ crude",
         dietary_categories=("grain",)),
    Pick("cornstarch", include=("starch",),
         exclude=("mix", "pudding", "recipe", "sauce", "dessert", "tapioca", "arrowroot"),
         fdc_query="cornstarch",
         dietary_categories=("grain",)),
    Pick("cheerios", include=("cheerios",),
         exclude=("bar", "treat", "snack mix", "clusters"),
         fdc_query="cereals ready-to-eat general mills cheerios",
         dietary_categories=("grain", "fortified_b12")),
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
    Pick("dried black beans", include=("black beans",),
         exclude=("refried", "soup", "seasoning", "sauce", "chili", "rice",
                  "blackeye", "black-eye"),
         fdc_query="beans black turtle mature seeds raw",
         dietary_categories=("legume",)),
    Pick("canned black beans", include=("black beans",),
         exclude=("refried", "soup", "dried", "seasoning", "sauce", "chili", "rice",
                  "blackeye", "black-eye"),
         fdc_query="beans black turtle mature seeds canned",
         dietary_categories=("legume",)),
    Pick("dried pinto beans", include=("pinto",),
         exclude=("refried", "soup", "seasoning", "sauce", "rice"),
         fdc_query="beans pinto mature seeds raw",
         dietary_categories=("legume",)),
    Pick("canned pinto beans", include=("pinto",),
         exclude=("refried", "soup", "dried", "seasoning", "sauce", "rice"),
         fdc_query="beans pinto mature seeds canned",
         dietary_categories=("legume",)),
    Pick("dried kidney beans", include=("kidney",),
         exclude=("refried", "soup", "seasoning", "sauce", "rice", "chili"),
         fdc_query="beans kidney red mature seeds raw",
         dietary_categories=("legume",)),
    Pick("canned kidney beans", include=("kidney",),
         exclude=("refried", "soup", "dried", "seasoning", "sauce", "rice", "chili"),
         fdc_query="beans kidney red mature seeds canned",
         dietary_categories=("legume",)),
    Pick("dried split peas", include=("split peas",),
         exclude=("soup", "seasoning", "sauce"),
         fdc_query="peas split mature seeds raw",
         dietary_categories=("legume",)),
    Pick("dried black-eyed peas", include=("black",),
         exclude=("refried", "soup", "seasoning", "sauce", "canned"),
         fdc_query="cowpeas black-eyed mature seeds raw",
         dietary_categories=("legume",)),
    Pick("canned great northern beans", include=("great northern",),
         exclude=("soup", "dried", "seasoning"),
         fdc_query="beans great northern mature seeds canned",
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
    Pick("walnuts", include=("walnut",),
         exclude=("candy", "sugar", "salted", "chocolate", "coated", "honey",
                  "glazed", "praline", "cookie", "brittle", "brownie", "cake",
                  "ice cream", "cereal", "baby", "stage", "puree", "toddler",
                  "salad", "kit", "chicken", "bowl", "wrap", "sandwich"),
         fdc_query="nuts walnuts english",
         dietary_categories=("nut",)),
    Pick("ground flaxseed", include=("flax",),
         exclude=("oil", "capsule", "supplement", "bread", "tablet", "softgel",
                  "bar", "crackers"),
         fdc_query="seeds flaxseed",
         dietary_categories=("seed",)),
    Pick("chia", include=("chia",),
         exclude=("pudding", "bar", "drink", "bottle", "lemonade", "yogurt",
                  "tea", "smoothie", "cracker", "oatmeal", "cookie", "bread",
                  "muffin", "kombucha", "granola"),
         fdc_query="seeds chia seeds dried",
         dietary_categories=("seed",)),
    # Kroger Cincinnati doesn't stock dried mature soybeans under any searchable
    # term; we already cover soy via tofu, soy milk, and edamame. Pick omitted.
    # Bob's Red Mill is the only vital wheat gluten SKU at Kroger ("wheat gluten"
    # search surfaces it; "vital wheat gluten" search returns nothing). The
    # Bob's product is 22oz, ~75% protein by weight — meat-level protein density
    # as a plant food.
    Pick("wheat gluten", include=("gluten",),
         exclude=("free", "gluten-free", "bread", "cracker", "pasta", "cookie",
                  "mix", "shampoo", "haircare", "protein shampoo", "sprouted",
                  "whole wheat flour", "organic foods organic"),
         fdc_query="wheat flour whole-grain",
         dietary_categories=("grain",)),
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
    Pick("instant nonfat dry milk", include=("dry milk",),
         exclude=("coconut", "almond", "goat", "soy", "oat", "cashew",
                  "buttermilk", "espresso", "cocoa", "chocolate", "formula",
                  "baby", "infant", "starter"),
         fdc_query="milk dry nonfat regular without added vitamin a and vitamin d",
         dietary_categories=("dairy",)),
    # Eggs
    Pick("large eggs grade a", include=("large", "eggs"), exclude=("liquid", "white", "extra"),
         fdc_query="egg whole raw fresh",
         dietary_categories=("egg",), grams_per_count=50.0),
    # Meat
    Pick("chicken breast boneless", include=("boneless", "chicken breast"), exclude=("breaded", "marinated", "seasoned", "tenders"),
         fdc_query="chicken broiler or fryer breast meat only raw",
         dietary_categories=("meat_white",)),
    Pick("whole chicken", include=("whole", "chicken"),
         exclude=("breast", "wing", "thigh", "leg", "quarter", "ground",
                  "tender", "strip", "nugget", "patty", "sausage", "meatball",
                  "boneless", "soup", "broth", "rotisserie", "cooked",
                  "marinated", "seasoned"),
         fdc_query="chicken broilers or fryers whole meat and skin raw",
         dietary_categories=("meat_white",)),
    Pick("chicken leg quarters", include=("leg",),
         exclude=("breast", "wing", "tender", "strip", "nugget", "patty",
                  "sausage", "meatball", "ground", "marinated", "sauce",
                  "soup", "broth", "boneless", "bbq", "dog", "cat"),
         # seasoned leg quarters accepted — extra salt rides the sodium UL
         fdc_query="chicken broilers or fryers leg meat and skin raw",
         dietary_categories=("meat_white",)),
    Pick("ground beef 80 20", include=("80/20", "ground beef"), exclude=("patties", "burger"),
         fdc_query="beef ground 80% lean 20% fat raw",
         dietary_categories=("meat_red",)),
    Pick("pork shoulder", include=("pork", "shoulder"),
         exclude=("sausage", "ground", "bbq", "marinated", "seasoned",
                  "pre-cooked", "cooked", "steamed", "bites", "ham"),
         fdc_query="pork fresh shoulder separable lean and fat raw",
         dietary_categories=("meat_red",)),
    # Fish
    Pick("canned tuna in water", include=("tuna", "water"), exclude=("oil", "pouch", "salad"),
         fdc_query="fish tuna light canned in water drained solids",
         dietary_categories=("fish",)),
    Pick("canned sardines", include=("sardines",), exclude=("hot sauce", "tomato", "mustard"),
         fdc_query="fish sardine atlantic canned in oil drained solids with bone",
         dietary_categories=("fish",)),
    Pick("canned salmon", include=("salmon",),
         exclude=("smoked", "cream cheese", "patty", "cake", "burger", "jerky",
                  "teriyaki", "sauce", "fresh", "frozen", "fillet", "steak",
                  "nugget", "sushi", "lox"),
         fdc_query="fish salmon pink canned drained solids with bone",
         dietary_categories=("fish",)),
    Pick("canned mackerel", include=("mackerel",),
         # Kroger's mackerel at Cincinnati is "Grace Jack Mackerel in Tomato
         # Sauce" — tomato sauce is normal packing for canned mackerel, not a
         # flavored product. Keep the exclude list small.
         exclude=("smoked", "fresh", "frozen", "fillet", "steak", "jerky", "pickled"),
         fdc_query="fish mackerel jack canned drained solids",
         dietary_categories=("fish",)),
    Pick("canned clams", include=("clams",),
         exclude=("chowder", "sauce", "dip", "stuffed", "smoked", "cake", "strip",
                  "fried", "pasta"),
         fdc_query="mollusks clam mixed species canned drained solids",
         dietary_categories=("fish",)),
    Pick("chicken liver", include=("liver",),
         exclude=("dog", "cat", "pet", "treat", "kibble", "feline", "canine",
                  "pate", "paste", "duck", "beef", "pork", "snack",
                  "fancy feast", "temptations", "purina", "pedigree", "friskies",
                  "wellness", "nutro", "iams", "hills", "rachael ray", "meow mix",
                  "wet food", "dry food", "cat food", "dog food"),
         fdc_query="chicken liver all classes raw",
         dietary_categories=("meat_white",)),
    # Vegetables
    Pick("frozen broccoli", include=("broccoli",), exclude=("cheese", "rice", "alfredo", "with"),
         fdc_query="broccoli frozen unprepared",
         dietary_categories=("vegetable",)),
    Pick("frozen spinach", include=("spinach",),
         exclude=("creamed", "garlic", "sausage", "bite", "meatball", "dip",
                  "quiche", "pie", "ravioli", "lasagna", "artichoke"),
         fdc_query="spinach frozen chopped or leaf unprepared",
         dietary_categories=("vegetable",)),
    Pick("carrots", include=("carrots",), exclude=("baby food", "stage", "cake", "puree"),
         fdc_query="carrots raw",
         dietary_categories=("vegetable",)),
    Pick("fresh cabbage", include=("cabbage",),
         exclude=("coleslaw", "slaw", "shredded", "angel hair", "kimchi",
                  "sauerkraut", "roll", "stuffed", "soup"),
         fdc_query="cabbage raw",
         dietary_categories=("vegetable",)),
    Pick("whole potato", include=("potato",),
         exclude=("chips", "fries", "fried", "mashed", "hash", "cake", "instant",
                  "scalloped", "salad", "pancake", "tot", "stuffed", "wedge",
                  "au gratin", "sweet", "soup"),
         fdc_query="potatoes white flesh and skin raw",
         dietary_categories=("vegetable",)),
    Pick("sweet potato", include=("sweet potato",),
         exclude=("baby food", "stage", "puree", "pie", "chips", "fries", "puff",
                  "cereal", "dessert", "sauce", "casserole", "cracker", "cookie",
                  "bar", "cake", "muffin", "bread", "tot", "waffle", "frozen meal"),
         fdc_query="sweet potato raw unprepared",
         dietary_categories=("vegetable",)),
    Pick("canned tomatoes", include=("tomato",),
         exclude=("paste", "sauce", "soup", "ketchup", "juice", "rotel", "salsa",
                  "pico", "seasoned", "flavored", "dried", "sun dried", "green",
                  "hot", "chili", "stewed with", "paste"),
         fdc_query="tomatoes red ripe canned packed in tomato juice no salt added",
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
    # Frozen concentrate wasn't available at Cincinnati Kroger — plain orange
    # juice (refrigerated) carries the same vit C per gram at the same FDC match.
    Pick("orange juice", include=("orange juice",),
         exclude=("mandarin", "cups", "drink", "light", "cocktail", "punch",
                  "lemonade", "smoothie", "kids", "pop", "strawberry", "bar",
                  "blend"),
         fdc_query="orange juice raw",
         dietary_categories=("fruit",)),
    Pick("raisins", include=("raisin",),
         exclude=("bread", "oatmeal", "cookie", "cereal", "bar", "muffin",
                  "granola", "trail mix", "yogurt", "bran", "chocolate", "cake",
                  "scone", "bagel"),
         fdc_query="raisins",
         dietary_categories=("fruit",)),
    # Fortified for vegan B12/D
    Pick("fortified soy milk", include=("soy", "milk"),
         exclude=("coconut", "almond", "oat", "cashew", "rice",
                  "yogurt", "ice cream", "creamer", "cheese", "protein powder",
                  "chocolate", "strawberry", "vanilla"),
         fdc_query="soymilk soy milk original and vanilla unsweetened with added calcium vitamins a and d",
         dietary_categories=("plant_milk", "fortified_b12")),
    # Additional plant milks — typically fortified with vit D + B12 + calcium.
    # All tag as plant_milk so vegan mode accepts them. Nutrient profiles
    # differ (almond has ~0 protein, pea milk has ~3g/100g like soy), so
    # the LP may mix them: soy/pea for protein, almond for cheap vit D
    # delivery.
    Pick("almond milk unsweetened", include=("almond", "milk"),
         exclude=("soy", "oat", "cashew", "coconut", "rice", "yogurt",
                  "ice cream", "creamer", "cheese", "chocolate", "vanilla",
                  "strawberry", "original"),
         fdc_query="almond milk unsweetened shelf stable",
         dietary_categories=("plant_milk", "fortified_b12")),
    Pick("oat milk", include=("oat", "milk"),
         exclude=("soy", "almond", "cashew", "coconut", "rice", "yogurt",
                  "ice cream", "creamer", "cheese", "chocolate", "vanilla",
                  "strawberry"),
         fdc_query="beverages oat milk unsweetened plain refrigerated",
         dietary_categories=("plant_milk", "fortified_b12")),
    # Pea milk and cashew milk: Kroger Cincinnati doesn't stock clean versions.
    # "pea milk" surfaces peanut butter + dog treats + yogurt (confounded by the
    # substring "pea" in too many descriptions); "cashew milk" surfaces frozen
    # dessert + chocolate bars. Fortified soy/almond/oat already cover the
    # plant-milk niche for the LP. Picks omitted.
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
    # Classical Stigler staples — reintroduced to align with the 1939/1947/2001
    # optimal baskets (cabbage + navy beans + wheat flour + evaporated milk +
    # beef liver dominated those solutions).
    Pick("evaporated milk", include=("evaporated",),
         exclude=("condensed", "sweetened"),
         fdc_query="milk canned evaporated without added vitamin a",
         dietary_categories=("dairy",)),
    Pick("beef liver", include=("beef", "liver"),
         exclude=("chicken", "pork", "calf", "pate", "paste",
                  "dog", "cat", "pet", "treat", "kibble", "wet food", "dry food"),
         fdc_query="beef variety meats and by-products liver raw",
         dietary_categories=("meat_red",)),
    Pick("corn meal", include=("corn meal",),
         exclude=("mix", "muffin", "bread", "chowder", "soup", "flakes",
                  "tortilla", "chips", "dog", "cat", "batter", "breading",
                  "self rising", "self-rising"),
         fdc_query="cornmeal whole grain yellow",
         dietary_categories=("grain",)),
    Pick("lard", include=("lard",),
         exclude=("substitute", "vegetable", "plant", "shortening"),
         fdc_query="lard",
         # meat_red gets lard excluded from pescatarian/vegetarian/ovo_lacto/vegan
         # via MODE_EXCLUDES — semantically fuzzy (lard isn't red meat) but
         # functionally correct for dietary-mode filtering.
         dietary_categories=("fat", "meat_red")),
    # Kroger's product catalog doesn't return hits for the bare term "molasses";
    # only "grandma molasses" (the common brand) surfaces the real bottle.
    Pick("grandma molasses", include=("molasses",),
         exclude=("cookie", "glaze", "ham", "barbecue", "marinade", "ginger",
                  "candy", "bread"),
         fdc_query="molasses",
         dietary_categories=("fruit",)),
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
