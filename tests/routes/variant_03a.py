"""Variant 03a (a higher jump): Oscar jumps where he starts, Up held
up to the top of the jump, and lands."""
from game_model import UP as U


def route(v):
    return [
        ("rest at the start", 10, 0, "street", None),
        ("Up held: up to the top of the jump", v.Until(
            lambda m: m.vy >= 0 and not m.ground, 80, "the top"), U,
         None, "higher-jump.png"),
        ("let go: he lands", v.Until(lambda m: m.ground, 80, "down"), 0,
         "street", None),
        ("rest", 20, 0, "street", None),
    ]
