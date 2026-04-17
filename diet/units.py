"""Deterministic unit parser for Kroger package sizes.

Two paths into grams:
  1. `itemInformation.netWeight` (e.g. "2.0 [lb_av]") — authoritative for weight-
     sold items. Always used when present and self-consistent with `size`.
  2. `items[].size` (e.g. "32 oz", "1 gal", "8 ct / 26 oz") — parsed via UCUM-ish
     unit table, with optional density for fl oz of liquids.

For count-only sizes ("18 ct", "12 ct") — netWeight from Kroger is unreliable
(observed: 0.13 lb returned for 18 ct eggs which is per-egg with shell, not pkg).
Fall back to `grams_per_unit` lookup keyed by FDC id when known, else surface a
warning and require manual override.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

OZ_TO_G = 28.3495231
LB_TO_G = 453.59237
GAL_TO_ML = 3785.4118
QT_TO_ML = 946.353
PT_TO_ML = 473.176
CUP_TO_ML = 236.588
FLOZ_TO_ML = 29.5735

# Density g/mL for liquids commonly sold by fl oz / gallon. Defaults to 1.0
# (water) when unknown — log via DensityWarning so callers can decide.
DENSITY_G_PER_ML: dict[str, float] = {
    "water":     1.000,
    "milk":      1.030,   # whole milk
    "soy milk":  1.030,
    "almond milk": 1.020,
    "juice":     1.045,
    "olive oil": 0.918,
    "vegetable oil": 0.920,
    "canola oil": 0.917,
    "honey":     1.420,
    "syrup":     1.330,
}

# Per-unit grams for things sold by "ct" where Kroger netWeight is per-egg
# / per-can / per-piece (not the package). Override by FDC id when possible.
GRAMS_PER_COUNT_BY_FDC: dict[int, float] = {
    748967:  50.0,   # Eggs, Grade A, Large, egg whole — per egg (FDC 748967)
    747997:  33.0,   # Eggs, Grade A, Large, egg white
    748236:  17.0,   # Eggs, Grade A, Large, egg yolk
}

# Some banner shorthand we expect to see in `size`.
_SIZE_RE = re.compile(
    r"""
    (?:(?P<frac_n>\d+)\s*/\s*(?P<frac_d>\d+)\s+)?    # optional leading fraction "1/2 "
    (?P<num>\d+(?:\.\d+)?)?
    \s*
    (?P<unit>oz|fl\s*oz|lb|gal|qt|pt|cup|ml|l|g|kg|ct|each|ea)
    """,
    re.IGNORECASE | re.VERBOSE,
)
_NETWEIGHT_RE = re.compile(r"(?P<num>\d+(?:\.\d+)?)\s*\[(?P<unit>\w+)\]")


@dataclass(frozen=True)
class ParsedSize:
    grams: float | None
    source: str            # "netWeight" | "size:weight" | "size:volume" | "size:count" | "fallback"
    note: str = ""


def parse_kroger_netweight(s: str | None) -> float | None:
    """Parse strings like '2.0 [lb_av]' or '907 [g]' to grams."""
    if not s:
        return None
    m = _NETWEIGHT_RE.search(s)
    if not m:
        return None
    n = float(m["num"])
    u = m["unit"].lower()
    if u in ("lb_av", "lb"):
        return n * LB_TO_G
    if u in ("oz_av", "oz"):
        return n * OZ_TO_G
    if u == "g":
        return n
    if u == "kg":
        return n * 1000.0
    return None


def parse_size(size_str: str | None) -> tuple[float, str] | None:
    """Parse 'size' string. Prefers the larger (weight) part of '8 ct / 26 oz'.

    Returns (grams, kind) where kind is 'weight' (oz/lb/g/kg), 'volume' (fl oz/
    gal/etc; needs density to finalize), or 'count' (ct/each).
    """
    if not size_str:
        return None
    matches = list(_SIZE_RE.finditer(size_str))
    if not matches:
        return None

    # Prefer weight unit > volume unit > count when multiple are present.
    rank = {"weight": 0, "volume": 1, "count": 2}
    best: tuple[float, str] | None = None

    for m in matches:
        # Handle leading fractions like "1/2 gal" → 0.5 gal.
        if m["frac_n"] and m["frac_d"]:
            n = float(m["frac_n"]) / float(m["frac_d"])
        elif m["num"]:
            n = float(m["num"])
        else:
            continue
        u = m["unit"].lower().replace(" ", "")
        if u in ("oz",):
            kind, g = "weight", n * OZ_TO_G
        elif u == "lb":
            kind, g = "weight", n * LB_TO_G
        elif u == "g":
            kind, g = "weight", n
        elif u == "kg":
            kind, g = "weight", n * 1000.0
        elif u == "floz":
            kind, g = "volume", n * FLOZ_TO_ML       # caller multiplies by density
        elif u == "gal":
            kind, g = "volume", n * GAL_TO_ML
        elif u == "qt":
            kind, g = "volume", n * QT_TO_ML
        elif u == "pt":
            kind, g = "volume", n * PT_TO_ML
        elif u == "cup":
            kind, g = "volume", n * CUP_TO_ML
        elif u == "ml":
            kind, g = "volume", n
        elif u == "l":
            kind, g = "volume", n * 1000.0
        elif u in ("ct", "each", "ea"):
            kind, g = "count", n
        else:
            continue

        if best is None or rank[kind] < rank[best[1]]:
            best = (g, kind)

    return best


def density_for(description: str) -> tuple[float, str]:
    """Pick a density g/mL based on description keywords. Returns (density, key)."""
    d = description.lower()
    for key, dens in DENSITY_G_PER_ML.items():
        if key in d:
            return dens, key
    return 1.0, "default-water"


def resolve_unit_grams(
    *,
    description: str,
    size: str | None,
    net_weight_str: str | None,
    fdc_id: int | None = None,
) -> ParsedSize:
    """Combine Kroger netWeight + size into a final per-package gram weight.

    Strategy (in order):
      1. If netWeight is present AND size parses as a weight AND they agree
         within ±5%, return netWeight (most reliable).
      2. If size is a weight, return that.
      3. If size is a volume, multiply by best-guess density.
      4. If size is a count and we have a known grams-per-count for the FDC id,
         return count × per_unit.
      5. Otherwise, return None with a note.
    """
    nw = parse_kroger_netweight(net_weight_str)
    sz = parse_size(size)

    if nw and sz and sz[1] == "weight":
        if abs(nw - sz[0]) / max(nw, 1.0) < 0.05:
            return ParsedSize(grams=nw, source="netWeight",
                              note=f"agrees with size {size}")
        # netWeight and size disagree: prefer size (often netWeight is per-unit).
        return ParsedSize(grams=sz[0], source="size:weight",
                          note=f"netWeight {nw:.0f}g disagreed with size {size}")

    if sz and sz[1] == "weight":
        return ParsedSize(grams=sz[0], source="size:weight")

    if sz and sz[1] == "volume":
        dens, key = density_for(description)
        return ParsedSize(grams=sz[0] * dens, source="size:volume",
                          note=f"density {dens:g} g/mL ({key})")

    if sz and sz[1] == "count":
        per = GRAMS_PER_COUNT_BY_FDC.get(fdc_id) if fdc_id else None
        if per is not None:
            return ParsedSize(grams=sz[0] * per, source="size:count",
                              note=f"{per:g} g/each (FDC {fdc_id})")
        # Last resort: use Kroger netWeight × count if both present and netWeight
        # looks like per-unit weight (well below the implied total).
        if nw and nw < sz[0] * 200:  # 200 g/unit = generous upper bound for "per unit"
            return ParsedSize(grams=sz[0] * nw, source="size:count",
                              note=f"interpreted Kroger netWeight {nw:.0f}g as per-unit")
        return ParsedSize(grams=None, source="fallback",
                          note=f"count-only size {size}; need grams/unit override")

    return ParsedSize(grams=nw, source="netWeight" if nw else "fallback",
                      note=f"could not parse size {size!r}")
