"""Variant 04a (a tireless bat): the bat at the start, beats straight
up until the energy runs out."""
from game_model import FIRE as F, UP as U


def route(v):
    return [
        ("rest at the start", 10, 0, "street", None),
        ("Up and Fire: the bat", 1, U | F, "street", None,
         dict(form=1, event="to bat")),
        ("the smoke", 12, 0, "street", None),
        ("beats until the energy runs out", v.Until(
            lambda m: any(e == "out of energy" for _, e in m.events),
            3000, "out of energy"), v.Beats(0, 20), None, None),
        ("Oscar falls onto the roof", v.Until(
            lambda m: m.ground, 200, "down"), 0, "roof A1", None),
        ("rest", 20, 0, "roof A1", None),
    ]
