#!/usr/bin/env python3
"""Build a seed data/walmart_skus.yaml by searching Walmart for each Kroger
curated SKU's food category. One-off; re-run quarterly like Kroger curate.

Strategy:
  For each Kroger SKU in data/skus.yaml, take its dietary_categories and
  a search term derived from its name. Call walmart.search() for that term,
  pick the first matching candidate whose description is not obvious noise
  (baby food, dog treats, candy), then walmart.product_details() to get the
  UPC + a name we can parse for size. Size → unit_grams via diet.units.
  FDC id reuses the Kroger SKU's fdc_id (same food type — cheaper than
  re-running FDC search).

Run with WALMART_CONSUMER_ID + WALMART_PRIVATE_KEY_PATH in env.
"""

from __future__ import annotations

import re
import sys
import time
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from diet.foods import load_skus  # noqa: E402
from diet.sources.walmart import WalmartClient  # noqa: E402
from diet.units import resolve_unit_grams  # noqa: E402

NOISE = (
    "baby food", "dog", "cat food", "puppy", "kitten", "kibble", "treat",
    "candy", "chocolate", "cookie", "cake", "ice cream", "soda", "drink mix",
    "subscription", "bundle",
)


def _derive_search_term(sku_name: str) -> str:
    """Strip brands and trademark noise from the Kroger name for a clean search."""
    name = re.sub(r"[®™]", "", sku_name)
    name = re.sub(r"^(Kroger|Simple Truth( Organic)?|Private Selection|Heritage Farm|"
                  r"Butcher's Prime|Grace|Quaker|Morrell|Goya|La Preferida|"
                  r"Nature's Bounty|Nature Made|Silk|Planet Oat|Almond Breeze|"
                  r"Bob's Red Mill|Wyman's|Kretschmer|Maizena|Grandma's|"
                  r"Pet|Snow's|KROGER|BIG DEAL!|\s)+",
                  "", name, flags=re.IGNORECASE).strip()
    name = re.sub(r"\s+x\s*\d+\s*$", "", name)  # "x 2" packs
    name = re.sub(r"\b(with|Rack|Pouches?|Cup|Tub|Bag|Bottle|Package|Roll|Can|Cans)\b.*$",
                  "", name, flags=re.IGNORECASE).strip()
    return name[:60]


def _size_from_walmart_name(name: str) -> str | None:
    """Pull a size token out of a Walmart product name. Uses the same unit parser
    we built for Kroger's `size` field — Walmart embeds sizes in the name itself."""
    # Simple strategy: run parse_size directly — it scans the whole string.
    return name  # resolve_unit_grams handles the full description


def _is_noisy(desc: str) -> bool:
    d = (desc or "").lower()
    return any(n in d for n in NOISE)


def main() -> int:
    client = WalmartClient.from_env()
    kroger_skus = load_skus()
    print(f"Bootstrapping Walmart SKUs from {len(kroger_skus)} Kroger entries...")

    out_rows: list[dict] = []
    seen_item_ids: set[str] = set()

    for i, sku in enumerate(kroger_skus, 1):
        term = _derive_search_term(sku.name)
        if len(term) < 3:
            continue
        try:
            resp = client.search(term, num_items=10)
        except Exception as exc:
            print(f"  [{i}/{len(kroger_skus)}] search fail for {term!r}: {exc}")
            continue

        items = resp.get("items") or []
        picked = None
        for item in items:
            desc = item.get("name") or ""
            if _is_noisy(desc):
                continue
            if item.get("salePrice") is None:
                continue
            if str(item.get("itemId")) in seen_item_ids:
                continue
            picked = item
            break

        if picked is None:
            print(f"  [{i}/{len(kroger_skus)}] no clean match for {term!r}")
            continue

        item_id = str(picked["itemId"])
        seen_item_ids.add(item_id)
        name = picked.get("name", "")
        ps = resolve_unit_grams(description=name, size=name, net_weight_str=None,
                                fdc_id=sku.fdc_id)
        if ps.grams is None:
            print(f"  [{i}/{len(kroger_skus)}] no size in {name!r}; skipping")
            continue

        out_rows.append({
            "product_id": item_id,
            "fdc_id": sku.fdc_id,
            "name": name,
            "unit_grams": round(ps.grams, 1),
            "dietary_categories": sorted(sku.dietary_categories),
            "source": "walmart",
            "_upc": picked.get("upc"),
            "_sale_price": picked.get("salePrice"),
            "_kroger_source": sku.name,
        })
        print(f"  [{i}/{len(kroger_skus)}] ✓  {item_id}  ${picked.get('salePrice')}  "
              f"{name[:55]}")
        time.sleep(0.25)  # be polite

    Path("data/walmart_skus.yaml").write_text(
        "# Bootstrapped from Kroger skus via walmart.search + product_details.\n"
        "# Underscore fields are provenance only; ignored by the loader.\n"
        "# Regenerate with scripts/bootstrap_walmart_skus.py.\n\n"
        + yaml.safe_dump(out_rows, sort_keys=False, allow_unicode=True, width=120)
    )
    print(f"\nwrote data/walmart_skus.yaml with {len(out_rows)} entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
