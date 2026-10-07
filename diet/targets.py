"""Load nutrient targets (RDAs / ULs) from a vendored DRI JSON file."""

from __future__ import annotations

import json
from pathlib import Path

from diet.solver import NutrientTarget

DEFAULT_DRI_PATH = Path("data/dri.json")


def load_profiles(path: Path | str = DEFAULT_DRI_PATH) -> dict[str, str]:
    """Profile id -> label for every age and sex group in the DRI file."""
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return {key: p["label"] for key, p in payload.get("profiles", {}).items()}


def default_profile(path: Path | str = DEFAULT_DRI_PATH) -> str:
    """The profile whose values the file's `nutrients` rows hold."""
    return json.loads(Path(path).read_text(encoding="utf-8"))["profile"]


def load_targets(
    path: Path | str = DEFAULT_DRI_PATH, profile: str | None = None
) -> list[NutrientTarget]:
    """Read the DRI JSON file and return a list of NutrientTarget.

    `profile` picks an age and sex group from the file's `profiles`; by default
    the values in `nutrients` (the file's default profile) apply.
    """
    p = Path(path)
    payload = json.loads(p.read_text(encoding="utf-8"))
    values = None
    if profile is not None:
        profiles = payload.get("profiles", {})
        if profile not in profiles:
            raise ValueError(f"unknown DRI profile {profile!r}; choose from {sorted(profiles)}")
        values = profiles[profile]
    targets: list[NutrientTarget] = []
    for entry in payload["nutrients"]:
        nutrient = entry["nutrient"]
        targets.append(NutrientTarget(
            nutrient=nutrient,
            rda=values["rda"].get(nutrient) if values else entry.get("rda"),
            ul=values["ul"].get(nutrient) if values else entry.get("ul"),
            unit=entry.get("unit", ""),
            label=entry.get("label", nutrient),
        ))
    return targets


def nutrient_label(targets: list[NutrientTarget], nutrient_id: str) -> str:
    """Pretty label for output. Falls back to the id if not in targets."""
    for t in targets:
        if t.nutrient == nutrient_id:
            return t.unit  # caller can format
    return nutrient_id
