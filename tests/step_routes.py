"""The routes of the first steps of the book's chain.

tests/verify_game.py --step N plays, in the program of step N
(chain/NN-name, tools/make_chain.py), a route: a list of entries as
verify_game.ROUTE has them (what, frames, joystick, where Oscar
stands at the end or None, a capture at the end or None, and what must
be true at the end). Steps 6-11 play the first game of the complete
game's route, from level 1 (verify_game.game_route); step 3 takes
level 1 of it as far as the left roof. Here: step 1 (nothing moves),
step 2 (the joystick moves the camera), the end of step 3, steps 4
and 5. Steps 4 and 5 play the ways through levels 1 and 2 that
tests/levels.py found (its witnesses, tests/routes/witnesses.json:
the joystick, from the start of a level to its gate, the enemies left
out, in runs [joystick, frames]). An entry's frames ("until", test,
most): until test(model) holds (verify_game.Until).
"""
import json
from pathlib import Path

from game_model import DOWN as D, FIRE as F, GO_LEFT as L
from game_model import GO_RIGHT as R, UP as U

HERE = Path(__file__).resolve().parent
WITNESSES = HERE / "routes/witnesses.json"
TRANS_FRAMES = 50                   # objects.asm: a transition

STEP_1 = [
    ("the village at night: nothing moves", 60, 0, None,
     "village-at-night.png"),
    ("still the village at night", 40, 0, None, None),
]

STEP_2 = [
    ("still: the back screen made ready", 20, 0, None,
     "scrolling-still.png"),
    ("right: the street scrolls, 2 pixels a frame", 160, R, None,
     "scrolling-right.png"),
    ("let go: the camera stops", 10, 0, None, None),
    ("left: the back screen made again, the other way", 40, L, None,
     None),
    ("right again", 30, R, None, None),
    ("right to the end of the level", 900, R, None,
     "scrolling-end.png"),
    ("at the end: no more to the right", 20, R, None, None),
    ("left, all the way back", 920, L, None, "scrolling-start.png"),
    ("at the start: no more to the left", 20, L, None, None),
]


def witness(level, start="start"):
    """The joystick of the way tests/levels.py found through `level`,
    from its start (or from the lantern): [[joystick, frames], ...]."""
    found = json.loads(WITNESSES.read_text(encoding="utf-8"))
    return found[str(level)][start]


def witness_route(level, title, last=None):
    """The witness of `level` as entries of a route, a run of the
    joystick each; the last one's expectation `last`."""
    runs = witness(level)
    route = []
    for number, (joy, frames) in enumerate(runs, 1):
        entry = (f"{title}: the way of levels.py, move {number}",
                 frames, joy, None, None)
        if number == len(runs) and last:
            entry += (last,)
        route.append(entry)
    return route


def event(name, what):
    """Until the model's event `name` happens (from the entry's start),
    for verify_game.Until."""
    seen = {}

    def test(model):
        seen.setdefault("from", len(model.events))
        return any(e == name for _, e in model.events[seen["from"]:])
    test.what = what
    return test


def step_3_end():
    """Step 3, after the complete game's route as far as the left
    roof: over it and down, and right along the street into the
    canal: back at the start (from step 5: at the lantern, lit on the
    way)."""
    return [
        ("over the roof, left, and down", 100, L, "street", None),
        ("walk right, into the canal", ("until", event(
            "fallen", "the canal"), 800), R, None, None,
         dict(event="fallen")),
        ("Oscar falls: back where he starts", TRANS_FRAMES, 0, "street",
         None),
        ("back where he starts", 20, 0, "street", "oscar-back.png"),
    ]


def step_4(v):
    """Step 4: step 3's route; the way of levels.py through level 1
    (the bat, its flights; no heirlooms yet, no gate: on to the end of
    the level); then the bat up to the top, a dive, beats until the
    energy runs out, a change refused; the moths (step_4_moths)."""
    beats = v.Beats
    return (v.game_route(3) + step_3_end()
            + witness_route(1, "level 1") + [
                ("let go", 16, 0, None, None),
                ("Up and Fire: the bat", 1, U | F, None, None,
                 dict(form=1, event="to bat")),
                ("the smoke", 12, 0, None, None),
                ("fast beats up to the top", ("until", event(
                    "top", "the top"), 300), beats(0, 5), None, None,
                 dict(event="top")),
                ("a dive", ("until", event("dive", "a dive"), 40), D,
                 None, None),
                ("the dive on, onto the gate's roof", 40, D, "gate roof",
                 None),
                ("beats left until the energy runs out", ("until", event(
                    "out of energy", "the energy out"), 600),
                 beats(L, 10), None, None, dict(form=0)),
                ("Oscar falls", 50, 0, "roof C3", None),
                ("Up and Fire: not enough energy (Up: a jump)", 1, U | F,
                 None, None, dict(form=0, event="refused")),
                ("he lands", 30, 0, "roof C3", "bat-refused.png"),
                ("rest: the energy comes back", 200, 0, "roof C3", None),
            ] + step_4_moths(v))


def step_4_moths(v):
    """The end of step 4: the bat over the canal of level 1 eats its
    two moths, one each way, and perches facing left."""
    beats = v.Beats
    return [
        ("rest on, until the energy is full", 510, 0, "roof C3", None),
        ("walk left over the roofs, near the end of roof C2", 156, L,
         "roof C2", None),
        ("let go", 16, 0, "roof C2", None),
        ("Up and Fire: the bat", 1, U | F, "roof C2", None,
         dict(form=1, event="to bat")),
        ("the smoke", 12, 0, "roof C2", None),
        ("perched on the roof, facing left", 10, 0, "roof C2",
         "bat-perched.png"),
        ("slow beats left (every 34 frames): a moth", 38, beats(L, 34),
         None, None, dict(moths=1)),
        ("faster beats left, the moth in its mouth", 8, beats(L, 26),
         None, "bat-moth.png"),
        ("faster beats left: over the other moth, over the street", 69,
         beats(L, 26, 18), None, None),
        ("slow beats right: the other moth", 61, beats(R, 34), None,
         None, dict(moths=2)),
        ("beats right", 10, beats(R, 34), None, None),
        ("Right held: the bat glides down onto the street", 87, R,
         "street", None),
        ("Down and Fire: Oscar", 1, D | F, "street", None,
         dict(form=0, event="to vampire")),
        ("the smoke", 14, 0, "street", None),
    ]


def step_5(v):
    """Step 5: level 1 by the way of levels.py (the three heirlooms,
    the gate), level 2 likewise, its gate: level 1 again; there step
    3's route (the chalice, the trapdoor: back at the start; the
    lantern lit on the way to the canal: back at the lantern); then
    the test writes the night's last step: dawn, level 1 again."""
    return (witness_route(1, "level 1", dict(event="through the gate"))
            + [("the transition: level 2", TRANS_FRAMES, 0, "street",
                None),
               ("at the start of the churchyard", 30, 0, "street",
                "churchyard-start.png", dict(got=0))]
            + witness_route(2, "level 2", dict(event="through the gate"))
            + [("the transition: level 1 again (the last level of the "
                "step)", TRANS_FRAMES, 0, "street", None)]
            + v.game_route(5) + step_3_end()
            + [("the night near its end (the test writes it)", 1, 0,
                "street", None,
                dict(poke={"night": 1, "night_time": 40})),
               ("until dawn: level 1 again", ("until", event(
                   "start", "dawn"), 60), 0, None, None,
                dict(event="start")),
               ("the transition: level 1 from its start", TRANS_FRAMES,
                0, "street", None),
               ("level 1 again, the night full", 30, 0, "street",
                "dawn-level-1.png", dict(got=0))])


def route(step, v):
    """The route of step `step` (1-5); v: verify_game."""
    if step == 1:
        return STEP_1
    if step == 2:
        return STEP_2
    if step == 3:
        return v.game_route(3) + step_3_end()
    if step == 4:
        return step_4(v)
    return step_5(v)
