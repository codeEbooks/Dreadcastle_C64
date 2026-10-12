"""Variant 07b (the moon on the left): on to the wood; the moon."""
from game_model import GO_NEXT


def route(v):
    return [
        ("on to the wood (the test writes it)", 1, 0, None, None,
         dict(poke={"level_no": 1, "trans": 50, "trans_kind": GO_NEXT})),
        ("the transition into level 3", 49, 0, "street", None),
        ("rest in the wood: the moon", 40, 0, "street", "moon-left.png"),
    ]
