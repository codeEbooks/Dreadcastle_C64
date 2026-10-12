"""Variant 12a (other words at dawn): from the title a game; the test
takes the night to its end: dawn and its words."""
from game_model import FIRE as F, UP as U


def route(v):
    return [
        ("the title", 30, 0, None, None),
        ("Fire: a new game", 1, F, None, None, dict(event="start")),
        ("the transition into level 1", 49, 0, "street", None),
        ("a jump at the start", 1, U, None, None),
        ("he lands", 45, 0, "street", None),
        ("the night near its end (the test writes it)", 1, 0, None, None,
         dict(poke={"night": 1, "night_time": 40})),
        ("dawn: the game stops", 39, 0, None, None, dict(event="dawn")),
        ("the sky lighter, step by step; Oscar in a puff of smoke",
         v.Until(lambda m: m.state_phase > m.c["DAWN_STEPS"], 300,
                 "Oscar gone"), 0, None, None),
        ("the words of dawn", 10, 0, None, "dawn-words.png"),
    ]
