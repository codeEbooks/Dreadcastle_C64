"""Variant 06b (a hard night: a hit takes four notches): on to the
churchyard, right into its cat."""
from game_model import GO_NEXT
from game_model import GO_RIGHT as R


def route(v):
    return [
        ("on to the churchyard (the test writes it)", 1, 0, None, None,
         dict(poke={"trans": 50, "trans_kind": GO_NEXT})),
        ("the transition into level 2", 49, 0, "street", None),
        ("walk right until the cat jumps at him", v.Until(
            lambda m: any(e == "hit" for _, e in m.events), 400,
            "a hit"), R, None, None, dict(event="hit")),
        ("thrown back, blinking", 30, 0, None, "hard-night.png"),
        ("wait", 100, 0, None, None),
    ]
