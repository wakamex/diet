import pytest

from diet.targets import default_profile, load_profiles, load_targets


def _bounds(targets):
    return {t.nutrient: (t.rda, t.ul) for t in targets}


def test_default_profile_matches_nutrient_rows():
    assert _bounds(load_targets(profile=default_profile())) == _bounds(load_targets())


def test_every_profile_bounds_the_same_nutrients():
    # Planners that rescale one model per profile rely on the same rows existing.
    shape = {n: (rda is not None, ul is not None) for n, (rda, ul) in _bounds(load_targets()).items()}
    for profile in load_profiles():
        bounds = _bounds(load_targets(profile=profile))
        assert {n: (rda is not None, ul is not None) for n, (rda, ul) in bounds.items()} == shape, profile


def test_profile_values_differ_by_sex_and_age():
    woman = _bounds(load_targets(profile="female_19_30"))
    older = _bounds(load_targets(profile="female_51_70"))
    assert woman["iron_mg"] == (18, 45)
    assert older["iron_mg"] == (8, 45)
    assert older["calcium_mg"] == (1200, 2000)


def test_unknown_profile_is_rejected():
    with pytest.raises(ValueError, match="unknown DRI profile"):
        load_targets(profile="child")
