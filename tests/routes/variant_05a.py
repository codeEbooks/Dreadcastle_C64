"""Variant 05a (the chalice on the street): from the start, right to
the chalice."""
from game_model import GO_RIGHT as R


def route(v):
    return [
        ("rest at the start", 10, 0, "street", "chalice-on-street.png"),
        ("walk right to the chalice", v.Until(
            lambda m: m.got == 1, 200, "the chalice"), R, "street",
         None, dict(got=1)),
        ("let go", 30, 0, "street", None),
    ]
