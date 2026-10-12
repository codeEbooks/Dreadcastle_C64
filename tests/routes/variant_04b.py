"""Variant 04b (a slow descent): the bat up to the top, then let go
until it perches on the roof over the start."""
from game_model import FIRE as F, UP as U


def route(v):
    return [
        ("rest at the start", 10, 0, "street", None),
        ("Up and Fire: the bat", 1, U | F, "street", None,
         dict(form=1, event="to bat")),
        ("the smoke", 12, 0, "street", None),
        ("fast beats up to the top", v.Until(
            lambda m: any(e == "top" for _, e in m.events), 300,
            "the top"), v.Beats(0, 6), None, None),
        ("let go: down onto the roof", v.Until(
            lambda m: m.ground, 400, "perched"), 0, "roof A1", None),
        ("perched", 20, 0, "roof A1", "slow-descent.png"),
    ]
