"""Discovery pass: search Kroger by staple terms, write candidates for human review.

Run quarterly. Outputs `data/sku_candidates.yaml` ranked by `$/oz` ascending,
preferring Kroger store brands.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from diet.sources.kroger import KrogerClient, extract_price
from diet.util import write_text_atomic

DEFAULT_TERMS_PATH = Path("data/discovery_terms.yaml")
DEFAULT_OUT_PATH = Path("data/sku_candidates.yaml")
PAGES_PER_TERM = 3       # 3 × 50 = 150 results per term
LIMIT_PER_PAGE = 50

# Substrings that almost always indicate a snack / candy / processed-meal
# variant we don't want for a Stigler basket. Filtered case-insensitively against
# the product description. A candidate is kept if it contains any noise word
# only when that word also appears in the search term itself (e.g. don't drop
# "potato chip" results when the user explicitly searched for "potato chips").
NOISE_SUBSTRINGS: tuple[str, ...] = (
    "chip", "candy", "ropes", "spray", "snack kit", "snack pack",
    "soda", "zero sugar", "flavored", "coleslaw", "sushi",
    "ice cream", "sherbet", "cracker", "biscuit", "syrup",
    "dressing", "stuffing", "meal kit", "lunchable",
    "cake", "cookie", "muffin", "pastry", "pie", "donut",
    "pretzel", "puffs", "popcorn",
    "drink mix", "energy", "sport drink",
    "frozen entree", "frozen dinner", "tv dinner", "instant", "ready to eat",
    # Pet food — Kroger carries hundreds of SKUs and our term-based fuzzy
    # search has matched them as legumes/meat/fish more than once.
    "dog", "cat food", "kitten", "puppy", "canine", "feline",
    "kibble", "rawhide", "pet food", "pet treat", "dog treat", "cat treat",
    "wet food", "dry food", "nutrish", "rachael ray",
)


def _is_noise(description: str, term: str) -> bool:
    d = (description or "").lower()
    t = (term or "").lower()
    for s in NOISE_SUBSTRINGS:
        if s in d and s not in t:
            return True
    return False


def _kroger_brand_score(brand: str | None) -> int:
    if not brand:
        return 1
    b = brand.lower()
    # Lower numbers rank earlier. Store brands first.
    if b in {"kroger", "simple truth", "simple truth organic", "private selection",
             "ralphs", "king soopers", "fred meyer", "smith's", "harris teeter"}:
        return 0
    return 1


def discover(
    terms_path: Path | str = DEFAULT_TERMS_PATH,
    out_path: Path | str = DEFAULT_OUT_PATH,
    *,
    seed_location_id: str,
    client: KrogerClient | None = None,
    pages_per_term: int = PAGES_PER_TERM,
) -> int:
    """Search Kroger for each staple term; write ranked candidates. Returns count."""
    client = client or KrogerClient.from_env()
    terms = yaml.safe_load(Path(terms_path).read_text(encoding="utf-8")) or []

    candidates_by_term: dict[str, list[dict]] = {}
    seen_ids: set[str] = set()

    for term in terms:
        term_str = term if isinstance(term, str) else term.get("term", "")
        if not term_str:
            continue
        rows: list[dict] = []
        for page in range(pages_per_term):
            payload = client.search(
                term_str,
                location_id=seed_location_id,
                limit=LIMIT_PER_PAGE,
                start=page * LIMIT_PER_PAGE,
            )
            data = payload.get("data") or []
            if not data:
                break
            for product in data:
                pid = product.get("productId")
                if not pid or pid in seen_ids:
                    continue
                description = product.get("description") or ""
                if _is_noise(description, term_str):
                    continue
                regular, promo = extract_price(product)
                if regular is None and promo is None:
                    # Kroger sometimes returns SKUs without prices at this location
                    # — useless for ingest, drop them from candidates.
                    continue
                seen_ids.add(pid)
                item = (product.get("items") or [{}])[0]
                rows.append({
                    "product_id": pid,
                    "upc": product.get("upc"),
                    "brand": product.get("brand"),
                    "description": description,
                    "categories": product.get("categories"),
                    "regular_price": regular,
                    "promo_price": promo,
                    "size": item.get("size") if (item := (product.get("items") or [{}])[0]) else None,
                    "net_weight": (product.get("itemInformation") or {}).get("netWeight"),
                    "_brand_score": _kroger_brand_score(product.get("brand")),
                })
            if len(data) < LIMIT_PER_PAGE:
                break

        # Rank: store brand first, then cheapest regular price (None → last).
        rows.sort(key=lambda r: (r["_brand_score"],
                                 r["regular_price"] if r["regular_price"] is not None else 1e9))
        # Keep top 10 per term.
        candidates_by_term[term_str] = rows[:10]

    # Strip private fields and emit YAML.
    out_payload: dict[str, list[dict]] = {}
    for term_str, rows in candidates_by_term.items():
        out_payload[term_str] = [{k: v for k, v in r.items() if not k.startswith("_")}
                                 for r in rows]

    write_text_atomic(Path(out_path), yaml.safe_dump(out_payload, sort_keys=False,
                                                    allow_unicode=True))
    return sum(len(v) for v in out_payload.values())
