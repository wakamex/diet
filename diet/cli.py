"""diet CLI — entry point for the daily pipeline."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from diet import curate as curate_mod
from diet import discover as discover_mod
from diet import ingest as ingest_mod
from diet.export import serialize_solution, write_data_json
from diet.foods import build_foods_for_location, load_locations, load_prices, load_skus
from diet.solver import MODE_EXCLUDES, solve
from diet.supplements import build_supplement_foods, load_supplements
from diet.targets import load_targets

REPORTS_DIR = Path("reports")
SOLUTIONS_PATH = REPORTS_DIR / "solutions.json"


def cmd_discover(args: argparse.Namespace) -> int:
    n = discover_mod.discover(seed_location_id=args.seed_location)
    print(f"discover: wrote {n} candidates to data/sku_candidates.yaml")
    return 0


def cmd_curate(args: argparse.Namespace) -> int:
    n, problems = curate_mod.curate()
    print(f"curate: wrote {n} SKUs to data/skus.yaml")
    for p in problems:
        print(p)
    return 0 if n > 0 else 1


def cmd_ingest(args: argparse.Namespace) -> int:
    payload = ingest_mod.ingest()
    print(f"ingest: {len(payload['prices'])} prices, {len(payload['missing'])} missing")
    return 0


def cmd_solve(args: argparse.Namespace) -> int:
    """Solve every (mode × location × variant).

    Variant `food_only` uses just the Kroger food SKUs; `with_supplements`
    adds the Kroger-brand multivitamin/B12/calcium+D from data/supplements.yaml.
    Both variants are emitted so the website can toggle between them and show
    the cost delta (= the "supplement arbitrage").
    """
    targets = load_targets()
    skus = load_skus()
    locations = load_locations()
    prices = load_prices()

    supplements_path = Path("data/supplements.yaml")
    supps = load_supplements(supplements_path) if supplements_path.exists() else []

    solutions: list[dict] = []
    for loc in locations:
        food_foods = build_foods_for_location(skus, loc, prices, use_promo=True)
        if not food_foods:
            print(f"solve: no priced foods at {loc.region} ({loc.location_id}); skipping")
            continue
        supp_foods = build_supplement_foods(supps, loc, prices, use_promo=True)
        variants: list[tuple[str, list]] = [("food_only", food_foods)]
        if supp_foods:
            variants.append(("with_supplements", food_foods + supp_foods))

        for variant_name, foods in variants:
            for mode in MODE_EXCLUDES:
                sol = solve(foods, targets, mode=mode)
                solutions.append({
                    **serialize_solution(sol, mode=mode,
                                         location_region=loc.region,
                                         location_display=loc.display),
                    "variant": variant_name,
                })
                tag = f"{mode:11s} @ {loc.region:7s} [{variant_name}]"
                if sol.status == "optimal":
                    print(f"solve: {tag}: ${sol.cost_per_day:.2f}/day, {len(sol.basket)} items")
                else:
                    print(f"solve: {tag}: {sol.status}")

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    SOLUTIONS_PATH.write_text(json.dumps(solutions, indent=2) + "\n", encoding="utf-8")
    print(f"solve: wrote {SOLUTIONS_PATH}")
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    targets = load_targets()
    if not SOLUTIONS_PATH.exists():
        print(f"export: {SOLUTIONS_PATH} not found; run `diet solve` first", file=sys.stderr)
        return 1
    solutions = json.loads(SOLUTIONS_PATH.read_text(encoding="utf-8"))
    out = write_data_json(solutions, targets=targets)
    print(f"export: wrote {out}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    targets = load_targets()
    skus = load_skus()
    locations = load_locations()
    prices = load_prices() if Path("data/prices_current.json").exists() else {}

    errors: list[str] = []
    print(f"validate: {len(skus)} SKUs, {len(locations)} locations, {len(targets)} nutrients")

    for sku in skus:
        if not sku.product_id:
            errors.append(f"SKU missing product_id: {sku.name}")
        if sku.unit_grams <= 0:
            errors.append(f"SKU {sku.product_id} has non-positive unit_grams")
        if not sku.dietary_categories:
            errors.append(f"SKU {sku.product_id} ({sku.name}) has no dietary_categories")

    if prices:
        for loc in locations:
            for sku in skus:
                if (sku.product_id, loc.location_id) not in prices:
                    errors.append(f"missing price: {sku.product_id} @ {loc.region}")

    for line in errors[:50]:
        print(f"  ERROR  {line}")
    if len(errors) > 50:
        print(f"  ... and {len(errors) - 50} more")
    print(f"validate: {len(errors)} issue(s)")
    return 1 if errors else 0


def cmd_all(args: argparse.Namespace) -> int:
    rc = cmd_ingest(args) or cmd_solve(args) or cmd_export(args)
    return rc


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="diet", description="Stigler 2026 — daily diet LP")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("discover", help="search Kroger by terms → sku_candidates.yaml")
    sp.add_argument("--seed-location", required=True,
                    help="Kroger locationId to use as seed for discovery")
    sp.set_defaults(fn=cmd_discover)

    sp = sub.add_parser("curate", help="build skus.yaml from sku_candidates.yaml + FDC search")
    sp.set_defaults(fn=cmd_curate)

    sp = sub.add_parser("ingest", help="refresh Kroger prices for skus.yaml × locations.yaml")
    sp.set_defaults(fn=cmd_ingest)

    sp = sub.add_parser("solve", help="solve LP per (mode × location)")
    sp.set_defaults(fn=cmd_solve)

    sp = sub.add_parser("export", help="write site/data.json from reports/solutions.json")
    sp.set_defaults(fn=cmd_export)

    sp = sub.add_parser("validate", help="sanity checks")
    sp.set_defaults(fn=cmd_validate)

    sp = sub.add_parser("all", help="ingest → solve → export (the CI command)")
    sp.set_defaults(fn=cmd_all)

    args = p.parse_args(argv)
    return args.fn(args)
