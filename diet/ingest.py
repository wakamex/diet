"""Daily ingest: refresh prices for every (SKU × location), write current data.

Routes each SKU to its source's API (Kroger Products API, Walmart.io Affiliate
Product Details, Metro Inc. reference catalogs, or PC Express reference stores) based on the
``SkuSpec.source`` field.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from diet.foods import Location, SkuSpec, load_all_skus, load_locations
from diet.nutrition import (
    extract_fdc_branded_nutrition,
    extract_kroger_nutrition,
    load_nutrition_overrides,
    load_sku_nutrients,
)
from diet.sources import fdc as fdc_mod
from diet.sources.bank_of_canada import BankOfCanadaClient, BankOfCanadaError
from diet.sources.kroger import KrogerClient, extract_price
from diet.sources.metro_reference import (
    MetroReferenceClient,
    MetroReferenceError,
    MetroReferenceQuote,
)
from diet.sources.pc_express import (
    PC_EXPRESS_MCP_URL,
    PCExpressClient,
    PCExpressError,
    PCExpressQuote,
)
from diet.sources.walmart import WalmartClient
from diet.sources.walmart_ca import WalmartCanadaClient, WalmartCanadaError
from diet.supplements import as_sku_specs, load_supplements
from diet.util import read_json, write_json_atomic

DEFAULT_RAW_ROOT = Path("data/raw/kroger")
DEFAULT_WALMART_RAW_ROOT = Path("data/raw/walmart")
DEFAULT_METRO_RAW_ROOT = Path("data/raw/metro_reference")
DEFAULT_PC_EXPRESS_RAW_ROOT = Path("data/raw/pc_express")
DEFAULT_WALMART_CA_RAW_ROOT = Path("data/raw/walmart_ca")
DEFAULT_OUT_PATH = Path("data/prices_current.json")
DEFAULT_NUTRIENTS_OUT_PATH = Path("data/nutrients_current.json")
DEFAULT_FX_OUT_PATH = Path("data/fx_current.json")
DEFAULT_FDC_CACHE = Path("data/raw/fdc")
KROGER_BATCH_SIZE = 50


def _today_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _ingest_kroger(
    skus: list[SkuSpec],
    locations: list[Location],
    client: KrogerClient,
    raw_root: Path,
    today: str,
) -> tuple[list[dict], list[dict], list[dict], list[dict]]:
    """Existing Kroger path — batch productId lookup per location."""
    rows: list[dict] = []
    missing: list[dict] = []
    nutrient_rows: dict[tuple[str, str], dict] = {}
    nutrition_attempted: set[tuple[str, str]] = set()
    warnings: list[dict] = []
    for loc in locations:
        product_ids = [s.product_id for s in skus]
        merged_data: list[dict] = []
        for i in range(0, len(product_ids), KROGER_BATCH_SIZE):
            batch = product_ids[i:i + KROGER_BATCH_SIZE]
            payload = client.lookup_and_cache(
                batch, location_id=loc.location_id,
                cache_root=raw_root, date_str=today,
            )
            merged_data.extend(payload.get("data") or [])
        by_id = {p.get("productId"): p for p in merged_data if p.get("productId")}
        for sku in skus:
            product = by_id.get(sku.product_id)
            if product is None:
                missing.append({"product_id": sku.product_id, "name": sku.name,
                                "location_id": loc.location_id, "reason": "not returned"})
                continue
            nutrient_key = (sku.source, sku.product_id)
            if sku.fdc_id and nutrient_key not in nutrition_attempted:
                nutrition_attempted.add(nutrient_key)
                nutrition, issues = extract_kroger_nutrition(
                    product,
                    product_id=sku.product_id,
                    package_grams=sku.unit_grams,
                    fetched_at=today,
                )
                if nutrition:
                    nutrient_rows[nutrient_key] = nutrition
                for issue in issues:
                    warnings.append({
                        "product_id": sku.product_id,
                        "source": sku.source,
                        "warning": issue,
                    })
            regular, promo = extract_price(product)
            if regular is None and promo is None:
                missing.append({"product_id": sku.product_id, "name": sku.name,
                                "location_id": loc.location_id, "reason": "no price"})
                continue
            rows.append({"product_id": sku.product_id, "location_id": loc.location_id,
                         "regular": regular, "promo": promo, "fetched_at": today})
    return rows, missing, list(nutrient_rows.values()), warnings


def _ingest_walmart(
    skus: list[SkuSpec],
    locations: list[Location],
    client: WalmartClient,
    today: str,
    raw_root: Path,
    fdc_cache: Path,
) -> tuple[list[dict], list[dict], list[dict], list[dict]]:
    """Walmart Affiliate API — one product-details call per SKU and location.

    The synthetic ``walmart-national`` location omits storeId. Numeric Walmart
    location IDs are passed through so returned salePrice is store-scoped.
    """
    rows: list[dict] = []
    missing: list[dict] = []
    nutrient_rows: list[dict] = []
    warnings: list[dict] = []
    if not locations:
        return rows, missing, nutrient_rows, warnings
    for sku in skus:
        nutrition_attempted = False
        for loc in locations:
            store_id = None if loc.location_id == "walmart-national" else loc.location_id
            search_item = None
            search_exc = None
            try:
                search = client.search(sku.name, num_items=25, store_id=store_id)
                search_item = next(
                    item for item in (search.get("items") or [])
                    if str(item.get("itemId")) == sku.product_id
                )
            except Exception as exc:
                search_exc = exc

            # Search results are offer-specific, whereas item details can pick
            # an unrelated marketplace seller for the same item ID. Prefer an
            # exact Walmart-sold search offer; otherwise retain details as a
            # fallback for products search does not return.
            if search_item is not None and not search_item.get("marketplace", False):
                p = search_item
            else:
                try:
                    details = client.product_details(sku.product_id, store_id=store_id)
                except Exception as details_exc:
                    if search_item is not None:
                        p = search_item
                    else:
                        missing.append({
                            "product_id": sku.product_id,
                            "name": sku.name,
                            "location_id": loc.location_id,
                            "reason": (
                                f"walmart exact search "
                                f"{type(search_exc).__name__}: {search_exc}; "
                                f"details {type(details_exc).__name__}: {details_exc}"
                            ),
                        })
                        continue
                else:
                    p = (
                        details
                        if not details.get("marketplace", False)
                        else search_item or details
                    )
                if not p:
                    missing.append({
                        "product_id": sku.product_id,
                        "name": sku.name,
                        "location_id": loc.location_id,
                        "reason": "walmart search/details returned no item",
                    })
                    continue
            write_json_atomic(
                raw_root / today / loc.location_id / f"{sku.product_id}.json", p
            )
            if sku.fdc_id and not nutrition_attempted:
                nutrition_attempted = True
                upc = str(p.get("upc") or "")
                if upc:
                    try:
                        branded = fdc_mod.search_branded_upc_cached(upc, fdc_cache)
                    except Exception as exc:
                        warnings.append({
                            "product_id": sku.product_id,
                            "source": sku.source,
                            "warning": f"USDA branded UPC lookup failed: {type(exc).__name__}: {exc}",
                        })
                    else:
                        if branded:
                            nutrition = extract_fdc_branded_nutrition(
                                branded,
                                product_id=sku.product_id,
                                source=sku.source,
                                upc=upc,
                                fetched_at=today,
                            )
                            if nutrition:
                                nutrient_rows.append(nutrition)
                            else:
                                warnings.append({
                                    "product_id": sku.product_id,
                                    "source": sku.source,
                                    "warning": "exact USDA Branded record has no mapped nutrients",
                                })
                        else:
                            warnings.append({
                                "product_id": sku.product_id,
                                "source": sku.source,
                                "warning": f"no exact USDA Branded match for UPC {upc}",
                            })
                else:
                    warnings.append({
                        "product_id": sku.product_id,
                        "source": sku.source,
                        "warning": "Walmart product has no UPC for exact USDA match",
                    })
            price = p.get("salePrice")
            if price is None:
                missing.append({"product_id": sku.product_id, "name": sku.name,
                                "location_id": loc.location_id,
                                "reason": "walmart no salePrice"})
                continue
            rows.append({"product_id": sku.product_id, "location_id": loc.location_id,
                         "regular": float(price), "promo": None, "fetched_at": today})
    return rows, missing, nutrient_rows, warnings


def _weighted_reference_price(
    sku: SkuSpec, quote: MetroReferenceQuote
) -> tuple[float, float | None] | None:
    """Return a synthetic unit-price package matching the curated gram basis."""
    if (
        quote.unit_price_cad is None
        or quote.unit_quantity is None
        or quote.unit_measure is None
    ):
        return None
    if quote.unit_measure == "g":
        basis_g = quote.unit_quantity
    elif quote.unit_measure == "kg":
        basis_g = quote.unit_quantity * 1000
    else:
        return None
    if abs(basis_g - sku.unit_grams) > max(0.1, basis_g * 0.001):
        return None
    return quote.unit_price_cad, None


def _ingest_metro_reference(
    skus: list[SkuSpec],
    location: Location,
    client: MetroReferenceClient,
    today: str,
    raw_root: Path,
) -> tuple[list[dict], list[dict]]:
    """Batch exact curated UPCs from one unlocalized Metro Inc. catalog."""
    try:
        result = client.quote_products([sku.product_id for sku in skus])
    except MetroReferenceError as exc:
        return [], [{
            "product_id": sku.product_id,
            "name": sku.name,
            "location_id": location.location_id,
            "reason": f"reference request failed: {exc}",
        } for sku in skus]

    quotes = {quote.product_id: quote for quote in result.quotes}
    fallback_searches: list[dict] = []
    for sku in skus:
        if sku.product_id in quotes or not sku.search_query:
            continue
        try:
            search = client.search_products(sku.search_query)
        except MetroReferenceError:
            continue
        fallback_searches.append(search.as_dict())
        exact = next(
            (quote for quote in search.quotes if quote.product_id == sku.product_id),
            None,
        )
        if exact is not None:
            quotes[sku.product_id] = exact
    raw_payload = result.as_dict()
    raw_payload["search_fallbacks"] = fallback_searches
    write_json_atomic(
        raw_root / today / f"{location.source}.json", raw_payload
    )
    rows: list[dict] = []
    missing: list[dict] = []
    for sku in skus:
        quote = quotes.get(sku.product_id)
        reason = None
        if quote is None:
            reason = "not returned"
        elif sku.package_label and quote.package != sku.package_label:
            reason = (
                f"package changed: expected {sku.package_label!r}, "
                f"received {quote.package!r}"
            )
        if reason:
            missing.append({
                "product_id": sku.product_id,
                "name": sku.name,
                "location_id": location.location_id,
                "reason": reason,
            })
            continue

        if quote.is_weighted:
            prices = _weighted_reference_price(sku, quote)
            if prices is None:
                missing.append({
                    "product_id": sku.product_id,
                    "name": sku.name,
                    "location_id": location.location_id,
                    "reason": "weighted item has no matching unit-price gram basis",
                })
                continue
            regular, promo = prices
            price_basis = "storefront_unit_price"
        else:
            regular = quote.regular_price_cad or quote.effective_price_cad
            promo = quote.promo_price_cad
            price_basis = "package"
        rows.append({
            "product_id": sku.product_id,
            "location_id": location.location_id,
            "regular": regular,
            "promo": promo,
            "currency": "CAD",
            "price_scope": "reference",
            "price_basis": price_basis,
            "package": quote.package,
            "source_url": quote.source_url,
            "observed_at": quote.observed_at,
            "fetched_at": today,
            "stale": False,
        })
    return rows, missing


_PC_EXPRESS_PRODUCT_ROOTS = {
    "superstore": "https://www.realcanadiansuperstore.ca/en/p/",
    "nofrills": "https://www.nofrills.ca/en/p/",
}


def _ingest_pc_express_reference(
    skus: list[SkuSpec],
    location: Location,
    client: PCExpressClient,
    today: str,
    raw_root: Path,
) -> tuple[list[dict], list[dict]]:
    """Search exact curated LIAMs at an explicit PC Express reference store."""
    rows: list[dict] = []
    missing: list[dict] = []
    searches: list[dict] = []
    for sku in skus:
        if not sku.search_query:
            missing.append({
                "product_id": sku.product_id,
                "name": sku.name,
                "location_id": location.location_id,
                "reason": "curated PC Express SKU has no search query",
            })
            continue
        try:
            search = client.search_products(
                store_id=location.location_id,
                banner=location.source,
                terms=sku.search_query,
                num_results=100,
            )
        except (PCExpressError, ValueError) as exc:
            missing.append({
                "product_id": sku.product_id,
                "name": sku.name,
                "location_id": location.location_id,
                "reason": f"reference request failed: {exc}",
            })
            continue
        searches.append(search.as_dict())
        product = next(
            (item for item in search.products if item.product_id == sku.product_id),
            None,
        )
        if product is None:
            reason = "exact LIAM not returned"
        elif product.in_stock is False:
            reason = "out of stock at reference store"
        else:
            reason = None
        if reason:
            missing.append({
                "product_id": sku.product_id,
                "name": sku.name,
                "location_id": location.location_id,
                "reason": reason,
            })
            continue

        quote = PCExpressQuote.from_search(search, product)
        rows.append({
            "product_id": sku.product_id,
            "location_id": location.location_id,
            # MCP exposes one current effective price, without a regular/promo split.
            "regular": quote.effective_price_cad,
            "promo": None,
            "currency": "CAD",
            "price_scope": "reference",
            "channel": quote.channel,
            "price_kind": "effective",
            "price_basis": "package",
            "package": sku.package_label,
            "source_url": _PC_EXPRESS_PRODUCT_ROOTS[location.source] + sku.product_id,
            "api_source_url": PC_EXPRESS_MCP_URL,
            "observed_at": quote.observed_at,
            "fetched_at": today,
            "stale": False,
            "banner": quote.banner,
            "store_id": quote.store_id,
            "reference_store_name": location.reference_store_name,
            "reference_store_address": location.reference_store_address,
            "reference_store_basis": location.reference_store_basis,
        })
    write_json_atomic(
        raw_root / today / f"{location.source}-{location.location_id}.json",
        {
            "source": "pc_express_mcp",
            "source_url": PC_EXPRESS_MCP_URL,
            "banner": location.source,
            "store_id": location.location_id,
            "reference_store_name": location.reference_store_name,
            "reference_store_address": location.reference_store_address,
            "reference_store_basis": location.reference_store_basis,
            "searches": searches,
        },
    )
    return rows, missing


def _ingest_walmart_ca_reference(
    skus: list[SkuSpec],
    location: Location,
    client: WalmartCanadaClient,
    today: str,
    raw_root: Path,
) -> tuple[list[dict], list[dict]]:
    """Read exact Walmart.ca SKUs from their unlocalized product pages."""
    rows: list[dict] = []
    missing: list[dict] = []
    quotes: list[dict] = []
    for sku in skus:
        try:
            quote = client.quote_product(sku.product_id)
        except (WalmartCanadaError, ValueError) as exc:
            missing.append({
                "product_id": sku.product_id,
                "name": sku.name,
                "location_id": location.location_id,
                "reason": f"reference request failed: {exc}",
            })
            continue
        quotes.append(quote.as_dict())
        rows.append({
            "product_id": sku.product_id,
            "location_id": location.location_id,
            # JSON-LD exposes the current offer, without a regular/promo split.
            "regular": quote.effective_price_cad,
            "promo": None,
            "currency": "CAD",
            "price_scope": "reference",
            "channel": quote.channel,
            "price_kind": "effective",
            "price_basis": "package",
            "package": sku.package_label,
            "source_url": quote.source_url,
            "observed_at": quote.observed_at,
            "fetched_at": today,
            "stale": False,
        })
    write_json_atomic(
        raw_root / today / f"{location.source}.json",
        {
            "source": "walmart_ca_product_page",
            "price_scope": "reference",
            "quotes": quotes,
        },
    )
    return rows, missing


def _retain_reference_prices(
    rows: list[dict],
    previous_rows: list[dict],
    *,
    skus: list[SkuSpec],
    locations: list[Location],
    retained_at: str,
) -> list[dict]:
    """Keep the last good Canadian quote when today's exact lookup misses."""
    reference_locations = {
        location.location_id: location.source
        for location in locations
        if location.price_scope == "reference"
    }
    valid = {
        (sku.product_id, location_id)
        for location_id, source in reference_locations.items()
        for sku in skus
        if sku.source == source
    }
    fresh = {(row["product_id"], row["location_id"]) for row in rows}
    retained: list[dict] = []
    for row in previous_rows:
        key = (row.get("product_id"), row.get("location_id"))
        if key not in valid or key in fresh:
            continue
        retained.append({
            **row,
            "stale": True,
            "retained_at": retained_at,
        })
    return rows + retained


def _refresh_fx(
    client: BankOfCanadaClient,
    path: Path,
    updated: str,
) -> tuple[dict | None, str | None]:
    try:
        cad = client.cad_to_usd()
    except BankOfCanadaError as exc:
        if path.exists():
            return read_json(path), str(exc)
        return None, str(exc)
    payload = {
        "updated": updated,
        "rates": {
            "USD": {
                "currency": "USD",
                "to_usd": 1.0,
                "as_of": cad.as_of,
                "source": cad.source,
                "source_url": cad.source_url,
            },
            "CAD": cad.as_dict(),
        },
    }
    write_json_atomic(path, payload)
    return payload, None


def ingest(
    *,
    skus: list[SkuSpec] | None = None,
    locations: list[Location] | None = None,
    kroger_client: KrogerClient | None = None,
    walmart_client: WalmartClient | None = None,
    metro_clients: dict[str, MetroReferenceClient] | None = None,
    pc_express_clients: dict[str, PCExpressClient] | None = None,
    walmart_ca_client: WalmartCanadaClient | None = None,
    fx_client: BankOfCanadaClient | None = None,
    raw_root: Path = DEFAULT_RAW_ROOT,
    walmart_raw_root: Path = DEFAULT_WALMART_RAW_ROOT,
    metro_raw_root: Path = DEFAULT_METRO_RAW_ROOT,
    pc_express_raw_root: Path = DEFAULT_PC_EXPRESS_RAW_ROOT,
    walmart_ca_raw_root: Path = DEFAULT_WALMART_CA_RAW_ROOT,
    fdc_cache: Path = DEFAULT_FDC_CACHE,
    out_path: Path = DEFAULT_OUT_PATH,
    nutrients_out_path: Path = DEFAULT_NUTRIENTS_OUT_PATH,
    fx_out_path: Path = DEFAULT_FX_OUT_PATH,
) -> dict:
    skus = skus or load_all_skus()
    locations = locations or load_locations()
    supplements_path = Path("data/supplements.yaml")
    if supplements_path.exists():
        skus = list(skus) + as_sku_specs(load_supplements(supplements_path))
    today = _today_str()

    kroger_skus = [s for s in skus if s.source == "kroger"]
    walmart_skus = [s for s in skus if s.source == "walmart"]
    kroger_locs = [l for l in locations if l.source == "kroger"]
    walmart_locs = [l for l in locations if l.source == "walmart"]
    metro_reference_locs = [
        l for l in locations if l.source in {"metro", "foodbasics"}
    ]
    pc_express_reference_locs = [
        l for l in locations if l.source in {"superstore", "nofrills"}
    ]
    walmart_ca_reference_locs = [
        l for l in locations if l.source == "walmart_ca"
    ]

    rows: list[dict] = []
    missing: list[dict] = []
    nutrient_rows: list[dict] = []
    nutrient_warnings: list[dict] = []

    if kroger_skus and kroger_locs:
        kroger_client = kroger_client or KrogerClient.from_env()
        r, m, n, w = _ingest_kroger(
            kroger_skus, kroger_locs, kroger_client, raw_root, today
        )
        rows += r; missing += m; nutrient_rows += n; nutrient_warnings += w
    if walmart_skus and walmart_locs:
        walmart_client = walmart_client or WalmartClient.from_env()
        r, m, n, w = _ingest_walmart(
            walmart_skus, walmart_locs, walmart_client, today,
            walmart_raw_root, fdc_cache,
        )
        rows += r; missing += m; nutrient_rows += n; nutrient_warnings += w

    metro_clients = metro_clients or {}
    for loc in metro_reference_locs:
        retailer_skus = [sku for sku in skus if sku.source == loc.source]
        if not retailer_skus:
            continue
        client = metro_clients.get(loc.source) or MetroReferenceClient(loc.source)
        r, m = _ingest_metro_reference(
            retailer_skus, loc, client, today, metro_raw_root
        )
        rows += r
        missing += m

    pc_express_clients = pc_express_clients or {}
    for loc in pc_express_reference_locs:
        retailer_skus = [sku for sku in skus if sku.source == loc.source]
        if not retailer_skus:
            continue
        client = pc_express_clients.get(loc.source) or PCExpressClient()
        r, m = _ingest_pc_express_reference(
            retailer_skus, loc, client, today, pc_express_raw_root
        )
        rows += r
        missing += m

    for loc in walmart_ca_reference_locs:
        retailer_skus = [sku for sku in skus if sku.source == loc.source]
        if not retailer_skus:
            continue
        r, m = _ingest_walmart_ca_reference(
            retailer_skus,
            loc,
            walmart_ca_client or WalmartCanadaClient(),
            today,
            walmart_ca_raw_root,
        )
        rows += r
        missing += m

    updated = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    previous_rows = []
    if out_path.exists():
        previous_rows = (read_json(out_path).get("prices") or [])
    rows = _retain_reference_prices(
        rows,
        previous_rows,
        skus=skus,
        locations=locations,
        retained_at=updated,
    )
    payload = {
        "updated": updated,
        "prices": rows,
        "missing": missing,
    }
    if any(location.currency == "CAD" for location in locations):
        fx, fx_warning = _refresh_fx(
            fx_client or BankOfCanadaClient(), fx_out_path, updated
        )
        payload["fx"] = fx
        if fx_warning:
            payload["fx_warning"] = fx_warning
    write_json_atomic(out_path, payload)
    # Nutrition changes much less often than price and a product API can be
    # transiently unavailable. Retain the last exact-SKU snapshot for still-
    # curated foods, then overlay every record refreshed successfully today.
    valid_nutrient_keys = {
        (sku.source, sku.product_id) for sku in skus if sku.fdc_id
    }
    effective_nutrients = {
        key: row for key, row in load_sku_nutrients(nutrients_out_path).items()
        if key in valid_nutrient_keys
    }
    for row in nutrient_rows:
        effective_nutrients[(row["source"], row["product_id"])] = row
    for key, row in load_nutrition_overrides().items():
        if key in valid_nutrient_keys:
            effective_nutrients[key] = row
    nutrition_payload = {
        "updated": payload["updated"],
        "nutrients": sorted(
            effective_nutrients.values(),
            key=lambda row: (row["source"], row["product_id"]),
        ),
        "warnings": nutrient_warnings,
    }
    write_json_atomic(nutrients_out_path, nutrition_payload)
    payload["nutrients"] = nutrition_payload["nutrients"]
    payload["nutrient_warnings"] = nutrient_warnings
    return payload
