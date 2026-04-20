"""Load nutrient targets (RDAs / ULs) from a vendored DRI JSON file."""

from __future__ import annotations

import json
from pathlib import Path

from diet.solver import NutrientTarget

DEFAULT_DRI_PATH = Path("data/dri.json")


def load_targets(path: Path | str = DEFAULT_DRI_PATH) -> list[NutrientTarget]:
    """Read the DRI JSON file and return a list of NutrientTarget."""
    p = Path(path)
    payload = json.loads(p.read_text(encoding="utf-8"))
    targets: list[NutrientTarget] = []
    for entry in payload["nutrients"]:
        targets.append(NutrientTarget(
            nutrient=entry["nutrient"],
            rda=entry.get("rda"),
            ul=entry.get("ul"),
            unit=entry.get("unit", ""),
            label=entry.get("label", entry["nutrient"]),
        ))
    return targets


def nutrient_label(targets: list[NutrientTarget], nutrient_id: str) -> str:
    """Pretty label for output. Falls back to the id if not in targets."""
    for t in targets:
        if t.nutrient == nutrient_id:
            return t.unit  # caller can format
    return nutrient_id
