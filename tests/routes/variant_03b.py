"""Variant 03b (a faster walk): from the start, right to the crates."""
from game_model import GO_RIGHT as R


def route(v):
    return [
        ("rest at the start", 10, 0, "street", None),
        ("walk right to the crates", v.Until(
            lambda m: any(e == "blocked right" for _, e in m.events),
            200, "the crates"), R, "street", None),
        ("let go", 30, 0, "street", None),
    ]
