from diet.curate import CURATE_PICKS, _matches


def test_walnut_pick_rejects_cosmetics_and_accepts_food():
    pick = next(p for p in CURATE_PICKS if p.term == "walnuts")

    assert not _matches(
        "e.l.f. Cosmetics Hydrating Satin Camo Concealer Tan Walnut",
        pick.include,
        pick.exclude,
    )
    assert _matches(
        "Kroger Gluten Free Vegan Halves and Pieces Walnuts",
        pick.include,
        pick.exclude,
    )
