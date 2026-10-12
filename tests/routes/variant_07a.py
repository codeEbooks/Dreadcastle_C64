"""Variant 07a (a longer blow): on to the wood with the staff; a
blow."""
from game_model import FIRE as F
from game_model import GO_NEXT


def route(v):
    return [
        ("on to the wood with the staff (the test writes it)", 1, 0,
         None, None, dict(poke={"level_no": 1, "trans": 50,
                                "trans_kind": GO_NEXT, "has_staff": 1})),
        ("the transition into level 3", 49, 0, "street", None),
        ("rest", 20, 0, "street", None),
        ("Fire: a blow", 1, F, "street", None, dict(event="blow")),
        ("the blow, 11 frames on", 11, 0, "street", "longer-blow.png"),
        ("the blow over", 20, 0, "street", None),
    ]
