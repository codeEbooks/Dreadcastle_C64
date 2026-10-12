"""Variant 12b (the night worth more): from the title a game, taken to
the arena by the test; the fight, the victory, the night counted."""
from game_model import FIRE as F
from game_model import GO_ARENA, GO_NEXT, ST_WON


def route(v):
    return [
        ("the title", 30, 0, None, None),
        ("Fire: a new game", 1, F, None, None, dict(event="start")),
        ("the transition into level 1", 49, 0, "street", None),
        ("rest", 20, 0, "street", None),
        ("on to level 8, the staff in hand (the test writes it)", 1, 0,
         None, None, dict(poke={"level_no": 6, "trans": 50,
                                "trans_kind": GO_NEXT, "has_staff": 1})),
        ("the transition into level 8", 49, 0, None, None),
        ("into the arena (the test writes it)", 1, 0, None, None,
         dict(poke={"trans": 50, "trans_kind": GO_ARENA})),
        ("the transition into the arena", 49, 0, None, None),
        ("the fight until the victory", v.Until(
            lambda m: m.game_state == ST_WON, 6000, "the victory"),
         v.FIGHT_AGAIN, None, None),
        ("the night into the score", v.Until(
            lambda m: m.state_phase == 1, 400, "the night counted"), 0,
         None, "night-worth-more.png"),
    ]
