"""Variants 08a and 08b (the wisps of the mire): on to the mire; the
wisps over its pools."""
from game_model import GO_NEXT


def route(v):
    return [
        ("on to the mire (the test writes it)", 1, 0, None, None,
         dict(poke={"level_no": 2, "trans": 50, "trans_kind": GO_NEXT})),
        ("the transition into level 4: unpacked, a page a frame", 49, 0,
         None, None),
        ("rest in the mire: the wisps over the pool ahead", 94, 0,
         "street", "wisps.png"),
    ]
