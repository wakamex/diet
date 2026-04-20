"""Write `site/data.json` from a list of solved (mode × location) solutions."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from diet.solver import NutrientTarget, Solution
from diet.targets import load_targets
from diet.util import write_json_atomic

DEFAULT_OUT_PATH = Path("site/data.json")


def serialize_solution(s: Solution, *, mode: str, location_region: str,
                       location_display: str) -> dict:
    return {
        "mode": mode,
        "location_region": location_region,
        "location_display": location_display,
        "status": s.status,
        "message": s.message,
        "cost_per_day": s.cost_per_day,
        "basket": s.basket,
        "nutrients": s.nutrients,
        "diagnosis": s.diagnosis,
    }


def write_data_json(
    solutions: list[dict],
    *,
    targets: list[NutrientTarget] | None = None,
    out_path: Path | str = DEFAULT_OUT_PATH,
    profile: str = "adult_male_31_50_moderate",
) -> Path:
    targets = targets or load_targets()
    payload = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "profile": profile,
        "nutrient_targets": [
            {"nutrient": t.nutrient, "rda": t.rda, "ul": t.ul,
             "unit": t.unit, "label": t.label or t.nutrient}
            for t in targets
        ],
        "solutions": solutions,
    }
    out = Path(out_path)
    write_json_atomic(out, payload)
    return out
