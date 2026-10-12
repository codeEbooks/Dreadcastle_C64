"""Variants 09a and 09b (the colours of the castle): on to Dreadcastle
Gate, then to the Throne Tower."""
from game_model import GO_NEXT


def route(v):
    return [
        ("on to the castle (the test writes it)", 1, 0, None, None,
         dict(poke={"level_no": 5, "trans": 50, "trans_kind": GO_NEXT})),
        ("the transition into level 7", 49, 0, None, None),
        ("rest at Dreadcastle Gate", 40, 0, None, "castle-gate.png"),
        ("on to the tower (the test writes it)", 1, 0, None, None,
         dict(poke={"trans": 50, "trans_kind": GO_NEXT})),
        ("the transition into level 8", 49, 0, None, None),
        ("rest in the Throne Tower", 40, 0, None, "throne-tower.png"),
    ]
