"""Dreadcastle: every level can be finished.

The plan of the eight levels asks of every level, shown without
playing it on the C64:
  1. from the start, the three heirlooms and then the exit;
  2. from the checkpoint (the lantern), every heirloom, those of tract
     A too, and the exit; and from the far side of every flight, back;
  3. the jumps on foot within the measures of section 1.3, measured on
     the game's model (game_model.py), not written by hand;
  4. every flight the level asks for done with the bar full and no
     moth, within the limits of 1.3 (about 20 metatiles across, 7 up);
  5. the rule of the space to turn back into a vampire (1.4);
  6. three heirlooms, one a tract, at least 21 columns apart; the
     checkpoint in tract B; the exit shut at the start;
  7. at most 4 enemies in every window of 19 columns and the margin;
     none within 6 columns of the start and of the checkpoint;
and every heirloom of the kind the plan gives it (1.2): within reach,
off the path, or in flight.

How. Body is game_model.Game without the screens: it moves Oscar with
the model's own code (Game.move_oscar and what it calls), a frame at a
time, and finds what he touches with Game.touch_heirlooms,
touch_lantern and touch_gate. The level is played without its moths.
A search starts where Oscar starts and where he comes back to (the
lantern). From every place where he stands still it jumps (Up held
1, 8, 16 or 28 frames; straight up, steering on, letting go, turning
back) and runs both ways; running at full speed it jumps every 4
frames, from the last frame before every edge and against every
block; from one place in every FLY_EVERY pixels and metatile of
height it flies (the bat keeps a height, and every GLIDE_EVERY pixels
across glides down to a perch, where Oscar comes back). Where he
stops, little steps of the joystick bring him to a pixel on a grid of
GRID, and he waits for the bar to be full: so the places are few, and
a place reached two ways is the same in everything the moves depend
on. Every move is a list of joystick frames played on the model: what
the search finds can be done. The ways it finds (the witnesses) are
played again in the whole model (game_model.Game: the camera, the
screens, the night), from the start and from the lantern (there with
the night full): the heirlooms taken, the gate open, through the gate
before dawn, with Oscar where the search said after every move.
The enemies are left out of the search and of the witnesses
played again: in levels 1 and 2 they are only to be avoided (the
plan), and a wait for one to walk away is not a way the search
needs to find; in level 3 they can be struck, but no passage asks for
it (the VICE test, verify_game.py, plays the levels with them). A
hazard in Oscar's body (level 3's brambles) is a fall for the
search: no way goes through one. The staff is something to touch
(STAFF_BIT), left where it is. Section 4.7 is checked on where the
enemies move: the enemies the program can show at once, for every
camera (the window of place_enemies: 19 columns and the margin, 344
pixels), at most 4;
their stretches at least 6 columns from the start and from the
lantern; and, as the plan gives them (section 3), their kind and
stretch; the watchman's street under the whole of his stretch, and
no block in his way (he turns only at its ends).
The door of the throne room, level 8's exit, leads into the
arena: the witnesses of level 8 go on in the whole model through the
transition into it, and the fighter (fight.py) plays the fight: Tom
beaten, Oscar never without health, before dawn, then the
victory. The
arena is checked too: closed on the left by the wall of the throne
room and on the right by the end of the level, the camera still at the
end; its two pedestals reached from its floor with a jump (Tom held
aside); no enemy of the level in its window.
What the search does not find is no proof that it cannot be done. For
that (an heirloom out of reach on foot) the check is a bound: how high
and how far a jump, the highest the model makes, can take Oscar's feet
and his middle from any surface (bound_touch).
Every level of PLAN is checked, each on its own, with the tables of
its setting; the measures of 1.3 once. Level 2 and the others are
reached in the whole model as the C64 reaches them: from the
title, a new game, then through the gates of the levels before. The
way (section 3 of the plan) is the street, the blocks on it and the
surfaces PLAN names for a level (level 3's stones); a block over the
street (level 3's hollow oak) is not on it.

Usage: python tests/levels.py [--level N]
(after build_assets.py and the assembly). Writes
evidence/levels-check.json; exit code 1 if a check fails.
"""

import argparse
from collections import deque
import heapq
import json
import math
import sys
import time

import fight
import game_model
import reference
import vicemon

PROJECT = reference.PROJECT
LABELS = PROJECT / "game/build/dreadcastle.lbl"
EVIDENCE = PROJECT / "evidence/levels-check.json"

UP, DOWN, FIRE = game_model.UP, game_model.DOWN, game_model.FIRE
R, L = game_model.GO_RIGHT, game_model.GO_LEFT
VAMPIRE, BAT = game_model.VAMPIRE, game_model.BAT
OPPOSITE = {R: L, L: R}
METATILE = 16

# What the plan (section 3) gives each level: its tracts, the kind of
# each heirloom, where the checkpoint and the exit are.
# The passages one way on foot (a gap flown, a step down of more than
# 2 metatiles), by the last column; what can be touched on foot from
# the start and from beyond each of them.
PLAN = {1: {"name": "VILLAGE OF MORTALS",
            "tracts": ((0, 41), (42, 85), (86, 127)),
            "kinds": ("within reach", "in flight", "off the path"),
            "checkpoint": (62, 66), "exit": (122, 125),
            "moths": (4, 5),
            "one_way": (("the canal", 103),),
            "on_foot": {"the start": {0, 3}, "the canal": {2, 4}},
            "enemies": (("patrol", 32, 40), ("jumper", 44, 53),
                        ("flyer", 72, 84), ("patrol", 104, 113))},
        2: {"name": "THE CHURCHYARD",
            "tracts": ((0, 41), (42, 85), (86, 127)),
            "kinds": ("within reach", "in flight", "off the path"),
            "checkpoint": (62, 66), "exit": (122, 125),
            "moths": (4, 5),
            "one_way": (("the landslide", 59), ("the chapel", 80)),
            "on_foot": {"the start": {0}, "the landslide": {2, 3, 4},
                        "the chapel": {2, 4}},
            "enemies": (("jumper", 16, 26), ("flyer", 30, 40),
                        ("patrol", 42, 51), ("flyer", 90, 102),
                        ("jumper", 108, 120))},
        3: {"name": "THE WILD WOOD",
            "tracts": ((0, 41), (42, 85), (86, 127)),
            "kinds": ("within reach", "in flight", "off the path"),
            "checkpoint": (62, 66), "exit": (122, 125),
            "moths": (4, 5),
            "one_way": (("the roots", 121),),
            "way": ("stone",),
            "hazards": ((54, 55), (60, 61)),
            "on_foot": {"the start": {0, 2, 3, 4, 5},
                        "the roots": {4}},
            "enemies": (("jumper", 16, 26), ("patrol", 32, 40),
                        ("patrol", 45, 53), ("flyer", 72, 84),
                        ("flyer", 92, 108), ("jumper", 110, 117))},
        4: {"name": "THE BLACK MIRE",
            "tracts": ((0, 41), (42, 85), (86, 127)),
            "kinds": ("within reach", "in flight", "off the path"),
            "checkpoint": (62, 66), "exit": (122, 125),
            "moths": (4, 5),
            "one_way": (),
            "way": ("clod", "boardwalk"),
            "hazards": ((66, 72),),
            "on_foot": {"the start": {0, 2, 3, 4}},
            "enemies": (("flyer", 10, 34), ("jumper", 37, 41),
                        ("patrol", 50, 56), ("flyer", 70, 84),
                        ("patrol", 90, 108), ("jumper", 96, 110))},
        5: {"name": "THE GREY CRAGS",
            "tracts": ((0, 41), (42, 85), (86, 127)),
            "kinds": ("off the path", "in flight", "within reach"),
            "checkpoint": (62, 66), "exit": (122, 125),
            "moths": (4, 5),
            "one_way": (("the pinnacle", 57),),
            "on_foot": {"the start": {0}, "the pinnacle": {2, 3, 4}},
            "enemies": (("patrol", 8, 14), ("jumper", 35, 41),
                        ("flyer", 44, 58), ("patrol", 72, 84),
                        ("flyer", 88, 104), ("patrol", 97, 105),
                        ("jumper", 110, 120))},
        6: {"name": "THE FROZEN PASS",
            "tracts": ((0, 41), (42, 85), (86, 127)),
            "kinds": ("within reach", "in flight", "off the path"),
            "checkpoint": (62, 66), "exit": (122, 125),
            "moths": (4, 5),
            "one_way": (("the first slab", 14), ("the second slab", 30),
                        ("the wall", 108)),
            "way": ("mound",),
            "over": ((10, 14), (26, 30), (98, 99)),
            "hazards": ((11, 14), (27, 30)),
            "on_foot": {"the start": {0, 2, 3, 4},
                        "the first slab": {0, 2, 3, 4},
                        "the second slab": {2, 3, 4},
                        "the wall": {2, 4}},
            "enemies": (("patrol", 16, 23), ("flyer", 31, 41),
                        ("jumper", 52, 58), ("flyer", 72, 84),
                        ("jumper", 86, 95), ("patrol", 100, 108),
                        ("patrol", 114, 119))},
        7: {"name": "DREADCASTLE GATE",
            "tracts": ((0, 41), (42, 85), (86, 127)),
            "kinds": ("within reach", "in flight", "off the path"),
            "checkpoint": (62, 66), "exit": (122, 125),
            "moths": (4, 5),
            "one_way": (("the moat", 21), ("the turret", 76)),
            "hazards": ((94, 95), (108, 109)),
            "on_foot": {"the start": set(), "the moat": {0, 2, 3, 4},
                        "the turret": {2, 4}},
            "enemies": (("flyer", 10, 21), ("patrol", 26, 41),
                        ("patrol", 46, 57), ("jumper", 77, 84),
                        ("flyer", 72, 82), ("patrol", 92, 113),
                        ("jumper", 118, 121), ("flyer", 106, 121))},
        8: {"name": "THE THRONE TOWER",
            "tracts": ((0, 41), (42, 85), (86, 127)),
            "kinds": ("within reach", "in flight", "off the path"),
            "checkpoint": (62, 66), "exit": (104, 105),
            "moths": (4, 5),
            "one_way": (("the mantel", 76),),
            "over": ((72, 76),),
            "hazards": ((73, 75),),
            "on_foot": {"the start": {0, 2, 3, 4}, "the mantel": {2, 4}},
            "enemies": (("patrol", 16, 28), ("flyer", 24, 40),
                        ("patrol", 44, 58), ("flyer", 72, 84),
                        ("jumper", 78, 87), ("patrol", 90, 100))}}

# The rules of section 1.3 and 1.4, in metatiles.
RULES = {"rise": 2,                 # a step on foot, at most
         "gap": 3,                  # a gap on foot, at most
         "across": 20,              # a flight asked for, across
         "up": 7,                   # and up
         "apart": 21,               # columns between heirlooms
         "space": 2,                # surface to solid block above
         "enemies": (4, 8),         # a level's enemies (levels 1-7)
         "on_screen": 4,            # enemies the program can show
                                    # (three where the moon is)
         "enemy_away": 6}           # columns from start, checkpoint
# The plan's measures, measured on the model.
PLAN_MEASURES = {"rise": 47, "long_jump": 69, "long_jump_up_2": 57,
                 "tap_rise": 20, "tap_length": 35, "climb_beats": 12,
                 "cruise_metatiles": 60, "glide_metatiles": 10,
                 "recharge_seconds": 15}

# The search.
HOLDS = (1, 8, 16, 28)              # frames of Up held
TAKE_EVERY = 4                      # at full speed: a take-off
STOP_EVERY = 20                     # every 4 frames, a stop every 20
AIR = 600                           # frames in the air, at most
RUN = 4000                          # frames of a run, at most
FLY_EVERY = 48                      # pixels: a flight from each
GLIDE_EVERY = 32                    # pixels across: a glide from each
MAX_SPAN = 24 * METATILE            # a flight: pixels across at most
BEAT_EVERY = 12                     # frames between two beats
HEIGHTS = 24                        # lines: heights the bat keeps
PUSH = 8                            # pixels: a push out of a block
PROFILE_FROM = 64                   # line: the highest jump measured
MAX_TRIES = 60                      # witnesses looked for again
GRID = 4                            # pixels: where he stops
FLIGHT_COST = 600                   # frames: ways on foot first

TOUCH_NAMES = ("heirloom 0", "heirloom 1", "heirloom 2", "lantern",
               "gate", "staff")
LANTERN_BIT, GATE_BIT, STAFF_BIT = 8, 16, 32


def nudge(delta):
    """Joystick frames that move Oscar, standing, by delta/256 pixel
    (a multiple of 8): Right one frame and let go, +16; Left then
    Right, +8 (the skid); and the other way round."""
    eighths = delta // 8
    joys = []
    if eighths % 2:
        joys += [L, R, 0] if eighths > 0 else [R, L, 0]
        eighths -= 1 if eighths > 0 else -1
    joys += ([R, 0] if eighths > 0 else [L, 0]) * abs(eighths // 2)
    return joys


class Tape:
    """Joystick frames: [[joy, frames], ...]."""

    def __init__(self):
        self.runs = []

    def add(self, joy, frames=1):
        if self.runs and self.runs[-1][0] == joy:
            self.runs[-1][1] += frames
        else:
            self.runs.append([joy, frames])

    def extend(self, other):
        for joy, frames in other.runs:
            self.add(joy, frames)

    def frames(self):
        return sum(frames for _, frames in self.runs)


class Body(game_model.Game):
    """Oscar alone, moved by the model's code, without the screens."""

    def __init__(self, game, level, number=1):
        self.k, self.c = game.k, game.c
        self.env = game.level_env[number - 1]
        env = game.all_files["envs"][self.env]
        self.files = dict(game.files)
        self.files.update(env)
        self.level = bytearray(level)
        self.files["level"] = self.level
        self.surfaces = game_model.Surfaces(self.level, env)
        self.level_no = number - 1
        self.objects = game.all_objects[number - 1]
        self.moves = game.moves
        self.x_max = game.x_max
        self.events, self.landed, self.taken = [], [], []
        self.frame = self.joy = self.moths_eaten = 0
        self.stun = self.protect = 0        # never hit here
        self.has_staff = self.blow = 0      # nor striking
        self.hazard = 0                     # frames in a hazard
        self.score = self.score_new = 0     # not counted here
        self.fx_calls = []                  # nor the sounds
        self.respawn_x = self.c["START_X"]
        self.fell = self.through = False
        self.frames = 0                     # frames played
        self.pushed = 0                     # the longest pushed frame

    # What ends a life or a level does not happen here: noted.
    def fallen(self):
        self.fell = True

    def start_transition(self, kind):
        self.through = True

    def start_tally(self):
        """Through a gate: the count would follow."""
        self.through = True

    def set_tile(self, col, row, tile):
        """The lantern lit: the same surfaces (checked)."""

    def get(self):
        return (self.x, self.y, self.vx, self.vy, self.ground,
                self.face, self.form, self.puff, self.flap, self.gnam,
                self.energy, self.prev_joy)

    def put(self, state):
        (self.x, self.y, self.vx, self.vy, self.ground, self.face,
         self.form, self.puff, self.flap, self.gnam, self.energy,
         self.prev_joy) = state
        self.sensor = (self.x >> 8) + self.k["SENSOR_X"]
        self.height = game_model.BODY_HEIGHTS[self.form]
        self.fell = False

    def step(self, joy):
        """A frame, as Game.turn plays it; what Oscar touches: bits
        0-2 the heirlooms, LANTERN_BIT, GATE_BIT (the doorway),
        STAFF_BIT (the staff, which he does not take here). A hazard
        in his body (the brambles) is a fall: no way through them."""
        self.frames += 1
        del self.events[:], self.landed[:], self.taken[:]
        self.joy = joy
        before = self.x
        self.move_oscar()
        if any(what.startswith("blocked") for _, what in self.events):
            self.pushed = max(self.pushed, abs(self.x - before) / 256)
        if not self.fell and self.in_hazard() is not None:
            self.hazard += 1
            self.fell = True
        if self.fell:
            return 0
        self.got = self.got_bits = 0
        self.touch_staff()
        if self.has_staff:
            self.has_staff = 0
            self.got_bits |= STAFF_BIT
        self.touch_heirlooms()
        self.lantern_lit = 0
        self.touch_lantern()
        self.door_open, self.through = 1, False
        self.touch_gate()
        return (self.got_bits | (LANTERN_BIT if self.lantern_lit else 0)
                | (GATE_BIT if self.through else 0))


def standing_state(body, x, line):
    """Oscar standing at x (left edge of his sprite) on `line`, as
    respawn leaves him: still, a vampire, the bar full."""
    return (x << 8, line << 8, 0, 0, 1, game_model.RIGHT, VAMPIRE, 0,
            0, 0, body.k["ENERGY_FULL"] << 8, 0)


# --- the measures of section 1.3, on the model ----------------------
def plain_columns(body):
    """A column with the street only, and one with nothing."""
    s, street, empty = body.surfaces, None, None
    line = body.c["START_Y"]
    for col in range(body.c["LEVEL_WIDTH"]):
        lines = {(row, s.line_at(x, row))
                 for x in range(col * 16, col * 16 + 16)
                 for row in range(11)}
        lines = {item for item in lines if item[1] is not None}
        if s.solid(col, 0, 10):
            continue
        if street is None and lines == {(line >> 4, line)}:
            street = col
        if empty is None and not lines:
            empty = col
    return street, empty


def flat_body(game, body, col):
    width = body.c["LEVEL_WIDTH"]
    column = bytes(body.level[col * 11:col * 11 + 11])
    return Body(game, column * width, body.level_no + 1)


def follow(body, state, joys, until):
    """Play `joys` (a function of the frame) from `state` until
    until(body) or a fall; the feet and the sensor of every frame."""
    body.put(state)
    track = []
    for frame in range(AIR * 4):
        body.step(joys(frame))
        if body.fell:
            break
        track.append((body.sensor, body.y >> 8, body.energy >> 8))
        if until(body):
            break
    return track


def measures(game, body):
    """The numbers of section 1.3, on a level of street only."""
    k, c = body.k, body.c
    street, empty = plain_columns(body)
    flat = flat_body(game, body, street)
    line = c["START_Y"]
    start = standing_state(flat, 200, line)
    found = {}

    def landed(b):
        return b.ground

    # The jump held: from standing, Up held until he lands.
    track = follow(flat, start, lambda f: UP, landed)
    found["rise"] = line - min(feet for _, feet, _ in track)
    # Running at full speed, then the jump held, or a tap.
    flat.put(start)
    while flat.vx < k["WALK_MAX"]:
        flat.step(R)
    running = flat.get()
    for name, hold in (("long_jump", AIR), ("tap", 1)):
        take_off = (running[0] >> 8) + k["SENSOR_X"]
        track = follow(flat, running,
                       lambda f, h=hold: R | (UP if f < h else 0),
                       landed)
        top = min(feet for _, feet, _ in track)
        if name == "tap":
            found["tap_rise"] = line - top
            found["tap_length"] = track[-1][0] - take_off
            continue
        found["long_jump"] = track[-1][0] - take_off
        apex = [feet for _, feet, _ in track].index(top)
        found["long_jump_up_2"] = next(
            sensor for sensor, feet, _ in track[apex:]
            if feet >= line - 2 * METATILE) - take_off
    # The highest a jump takes the feet, frame by frame, with nothing
    # to land on (the bound for what cannot be reached on foot): from
    # line PROFILE_FROM, so that he falls long enough to reach
    # FALL_MAX; after that he falls FALL_MAX a frame.
    nothing = flat_body(game, body, empty)
    track = follow(nothing, standing_state(nothing, 200, PROFILE_FROM),
                   lambda f: UP, lambda b: False)
    found["jump_profile"] = [PROFILE_FROM - feet for _, feet, _ in track]
    found["profile_ends_at_fall_max"] = nothing.vy == k["FALL_MAX"]
    # The bat: from the street, beats every 12 frames up to the top.
    flat.put(start)
    flat.step(UP | FIRE)
    for _ in range(k["PUFF_FRAMES"]):
        flat.step(0)
    perched = flat.get()
    track = follow(flat, perched,
                   lambda f: UP if f % BEAT_EVERY == 0 else 0,
                   lambda b: b.y >> 8 <= k["BAT_TOP"])
    found["climb_beats"] = (len(track) - 1) // BEAT_EVERY + 1
    found["climb_frames"] = len(track)
    top = list(flat.get())
    top[10] = k["ENERGY_FULL"] << 8             # the bar full again
    top = tuple(top)
    # Across at the top, the bar full: a beat every 28 frames, Right
    # held, until the energy is out; and gliding down from the top.
    track = follow(flat, top,
                   lambda f: R | (UP if f % 28 == 0 else 0),
                   lambda b: b.energy >> 8 < k["FLAP_COST"])
    found["cruise_metatiles"] = round((track[-1][0] - track[0][0])
                                      / METATILE, 1)
    found["cruise_lowest"] = max(feet for _, feet, _ in track)
    track = follow(flat, top, lambda f: R, landed)
    found["glide_metatiles"] = round((track[-1][0] - track[0][0])
                                     / METATILE, 1)
    # The bar from empty to full, standing.
    found["recharge_seconds"] = round(
        k["ENERGY_FULL"] * 256 / k["RECHARGE"] / 50, 1)
    return found


# --- the search -------------------------------------------------------
class Search:
    """Places where Oscar stands still ('stop') or runs ('run'), and
    the moves between them: (to, touched, tape, how, flight)."""

    def __init__(self, body, flights=True):
        self.body = body
        self.flights = flights
        self.states, self.kinds, self.out = [], [], []
        self.index = {}
        self.todo = deque()
        self.flown = set()
        self.took = set()

    @staticmethod
    def key(state, kind):
        """What the moves depend on: one place for each. (Where he
        faces, the wings and the mouth do not move him.)"""
        x, y, vx, vy, ground, _, form, puff, _, _, energy, joy = state
        return kind, x, y, vx, vy, ground, form, puff, energy, joy

    def node(self, state, kind):
        key = self.key(state, kind)
        number = self.index.get(key)
        if number is not None:
            return number, False
        number = len(self.states)
        self.index[key] = number
        self.states.append(state)
        self.kinds.append(kind)
        self.out.append([])
        if kind == "stop":
            self.todo.append(number)
        return number, True

    def edge(self, start, to, touched, tape, how, flight=None):
        self.out[start].append((to, touched, tape.runs, how, flight))

    def explore(self, seeds):
        firsts = [self.node(state, "stop")[0] for state in seeds]
        while self.todo:
            number = self.todo.popleft()
            self.stand(number)
        return firsts

    # Oscar still lets go: until he stands still again (or falls).
    def settle(self, start, tape, touched, how, flight=None):
        b = self.body
        for _ in range(AIR):
            if (b.ground and b.vx == 0 and b.form == VAMPIRE
                    and not b.puff and b.prev_joy == 0):
                touched = self.even_up(tape, touched)
                to, _ = self.node(b.get(), "stop")
                self.edge(start, to, touched, tape, how, flight)
                return to
            touched |= b.step(0)
            tape.add(0)
            if b.fell:
                break
        self.edge(start, None, touched, tape, how, flight)
        return None

    def even_up(self, tape, touched):
        """Standing still: little steps to a pixel that is a multiple
        of GRID (or, if he would walk off, to a whole pixel), the
        fraction 0 or 4/256 (the bat's speeds are multiples of 4, the
        vampire's of 8); then the bar full again, waiting. So the
        places where he stops are few, and the runs from them the
        same."""
        k, b = self.body.k, self.body
        kept = b.get()
        base = b.x & 7
        for grid in (GRID, 1):
            whole = ((b.x >> 8) + grid // 2) // grid * grid
            delta = (whole << 8 | base) - b.x
            if not delta:
                break
            steps, more = Tape(), 0
            for joy in nudge(delta):
                more |= b.step(joy)
                steps.add(joy)
                if b.fell:
                    break
            if (not b.fell and b.ground and b.vx == 0
                    and b.x == (whole << 8 | base) and b.prev_joy == 0):
                tape.extend(steps)
                touched |= more
                break
            b.put(kept)
        while b.energy >> 8 < k["ENERGY_FULL"]:
            touched |= b.step(0)
            tape.add(0)
        return touched

    def stand(self, number):
        """The moves from a place where Oscar stands still."""
        for first, after in ((UP, 0), (UP, R), (UP, L),
                             (UP | R, R), (UP | L, L)):
            for hold in HOLDS:
                self.jump(number, first, hold, after)
        for direction in (R, L):
            self.run(number, direction)
        state = self.states[number]
        bucket = (state[0] >> 8) // FLY_EVERY, state[1] >> 12
        if self.flights and bucket not in self.flown:
            self.flown.add(bucket)
            self.fly(number)

    def jump(self, number, first, hold, after):
        b = self.body
        b.put(self.states[number])
        tape, touched = Tape(), 0
        for frame in range(AIR):
            joy = first if frame < hold else after
            touched |= b.step(joy)
            tape.add(joy)
            if b.fell or b.ground:
                break
        if frame == 0 and b.ground:
            return                          # no jump
        if not b.fell:
            self.settle(number, tape, touched, "foot")
        else:
            self.edge(number, None, touched, tape, "foot")

    def run(self, number, direction):
        """Right or Left held: a 'run' place every frame on the
        ground; at full speed, take-offs and stops every few frames;
        from the last place before an edge, a take-off; against a
        block, a take-off and a stop."""
        k, b = self.body.k, self.body
        state, last = self.states[number], number
        tape, touched = Tape(), 0
        count = 0
        for _ in range(RUN):
            b.put(state)
            touched |= b.step(direction)
            tape.add(direction)
            if b.fell:
                self.edge(last, None, touched, tape, "foot")
                return
            state = b.get()
            if not b.ground:
                if tape.frames() == 1 and last != number:
                    self.take_offs(last, direction)  # the edge
                continue
            to, new = self.node(state, "run")
            self.edge(last, to, touched, tape, "foot")
            tape, touched = Tape(), 0
            if not new:
                return
            last = to
            blocked = state[2] == 0
            if abs(state[2]) == k["WALK_MAX"]:
                count += 1
            if blocked or count % TAKE_EVERY == 1:
                self.take_offs(to, direction)
            if blocked or count % STOP_EVERY == 1:
                b.put(state)
                self.settle(to, Tape(), 0, "foot")
                if blocked:
                    return

    def take_offs(self, number, direction):
        if number in self.took:
            return
        self.took.add(number)
        for after in (direction, 0, OPPOSITE[direction]):
            for hold in HOLDS:
                self.jump(number, direction | UP, hold, after)

    # --- the bat --------------------------------------------------
    def fly(self, number):
        """From standing: the bar full again (waiting), into a bat;
        Right or Left, beats to keep the feet up to a height (every
        HEIGHTS lines from the top to just over the surface), across; at
        every GLIDE_EVERY pixels, a glide (holding on, or letting go)
        down to a perch, and there a vampire again."""
        k, b = self.body.k, self.body
        b.put(self.states[number])
        tape = Tape()
        while b.energy >> 8 < k["ENERGY_FULL"]:
            b.step(0)
            tape.add(0)
        b.step(UP | FIRE)
        tape.add(UP | FIRE)
        for _ in range(k["PUFF_FRAMES"]):
            b.step(0)
            tape.add(0)
        if b.form != BAT:
            return
        perched = b.get()
        line = perched[1] >> 8
        for direction in (R, L):
            for height in range(k["BAT_TOP"], line - 8, HEIGHTS):
                self.cruise(number, perched, tape, direction, height)

    def cruise(self, number, perched, start_tape, direction, height):
        k, b = self.body.k, self.body
        b.put(perched)
        x0, line = perched[0] >> 8, perched[1] >> 8
        tape, touched = Tape(), 0
        tape.extend(start_tape)
        since, beats, highest, glided = BEAT_EVERY, 0, line, 0
        for _ in range(AIR * 2):
            beat = (b.y >> 8 > height and since >= BEAT_EVERY
                    and b.energy >> 8 >= k["FLAP_COST"])
            joy = direction | (UP if beat else 0)
            touched |= b.step(joy)
            tape.add(joy)
            since = 0 if beat else since + 1
            beats += beat
            if b.fell:
                self.edge(number, None, touched, tape, "flight")
                return
            highest = min(highest, b.y >> 8)
            span = abs((b.x >> 8) - x0)
            if b.ground:
                self.perch(number, tape, touched,
                           (span, line - highest, beats))
                return
            if span >= MAX_SPAN:
                return
            if span >= glided + GLIDE_EVERY:
                glided = span - span % GLIDE_EVERY
                state = b.get()
                for glide in (direction, 0):
                    self.glide(number, state, tape, touched, glide,
                               (x0, line, highest, beats))
                b.put(state)

    def glide(self, number, state, tape_so_far, touched, joy, so_far):
        b = self.body
        x0, line, highest, beats = so_far
        b.put(state)
        tape = Tape()
        tape.extend(tape_so_far)
        for _ in range(AIR):
            touched |= b.step(joy)
            tape.add(joy)
            if b.fell:
                self.edge(number, None, touched, tape, "flight")
                return
            if b.ground:
                span = abs((b.x >> 8) - x0)
                self.perch(number, tape, touched,
                           (span, line - highest, beats))
                return

    def perch(self, number, tape, touched, flight):
        """Perched: Down and Fire, the smoke, a vampire again."""
        b = self.body
        span, climb, beats = flight
        flight = {"across": span, "up": max(climb, 0), "beats": beats,
                  "energy_left": b.energy >> 8}
        touched |= b.step(DOWN | FIRE)
        tape.add(DOWN | FIRE)
        if b.form == BAT and not b.puff:
            self.edge(number, None, touched, tape, "flight", flight)
            return
        self.settle(number, tape, touched, "flight", flight)

    # --- ways through the places ------------------------------------
    def ways(self, starts, allowed=lambda edge: True):
        """Dijkstra in frames from `starts` (a place or a list), a
        flight counting FLIGHT_COST frames more: {place: (frames,
        came)}, came = (from, edge)."""
        starts = starts if isinstance(starts, list) else [starts]
        best = {start: (0, None) for start in starts}
        queue = [(0, start) for start in starts]
        while queue:
            frames, here = heapq.heappop(queue)
            if frames > best[here][0]:
                continue
            for edge in self.out[here]:
                to = edge[0]
                if to is None or not allowed(edge):
                    continue
                cost = frames + sum(n for _, n in edge[2])
                if edge[3] == "flight":
                    cost += FLIGHT_COST         # on foot if he can
                if to not in best or cost < best[to][0]:
                    best[to] = (cost, (here, edge))
                    heapq.heappush(queue, (cost, to))
        return best

    def touched(self, best, allowed=lambda edge: True):
        """What can be touched from the places of `best`: {bit:
        (frames, place, edge)}, the quickest."""
        found = {}
        for here, (frames, _) in best.items():
            for edge in self.out[here]:
                if not edge[1] or not allowed(edge):
                    continue
                cost = frames + sum(n for _, n in edge[2])
                for bit in range(len(TOUCH_NAMES)):
                    if edge[1] & 1 << bit and (
                            bit not in found or cost < found[bit][0]):
                        found[bit] = (cost, here, edge)
        return found

    def witness(self, start, goals, allowed=lambda edge: True):
        """A way from `start` (a place or a list) that touches the
        goals (bits; any order, the nearest first; the gate last):
        [(from, edge), ...]."""
        way, here, left = [], start, list(goals)
        while left:
            gate_only = [bit for bit in left if bit != 4] or left
            best = self.ways(here, allowed)
            found = self.touched(best, allowed)
            near = [(found[bit][0], bit) for bit in gate_only
                    if bit in found and found[bit][2][0] is not None]
            if not near:
                return None, left
            _, bit = min(near)
            _, place, edge = found[bit]
            way += self.back(best, place) + [(place, edge)]
            here = edge[0]
            left = [item for item in left if not edge[1] & 1 << item]
        return way, []

    def close(self, state, number):
        """Oscar where the search put place `number`: the same in
        everything the moves depend on."""
        kind = self.kinds[number]
        return self.key(state, kind) == self.key(self.states[number],
                                                 kind)

    def play(self, way):
        """The way again on the model, from the exact state of its
        first place: (what it touches, the first move that ends
        elsewhere or in a fall, or None)."""
        b = self.body
        b.put(self.states[way[0][0]])
        touched = 0
        for number, (_, edge) in enumerate(way):
            for joy, frames in edge[2]:
                for _ in range(frames):
                    touched |= b.step(joy)
                    if b.fell:
                        return touched, number
            if edge[0] is not None and not self.close(b.get(),
                                                      edge[0]):
                return touched, number
        return touched, None

    def proven(self, start, goals, allowed=lambda edge: True):
        """A witness that, played again, touches every goal (should a
        move end elsewhere, it is left out and the way looked for
        again: it does not happen, the places being exact). (way or
        None, goals missing, moves left out)."""
        banned = set()

        def fine(edge):
            return id(edge) not in banned and allowed(edge)

        for _ in range(MAX_TRIES):
            way, left = self.witness(start, goals, fine)
            if way is None:
                return None, left, len(banned)
            touched, wrong = self.play(way)
            missing = [bit for bit in goals if not touched & 1 << bit]
            if wrong is None and not missing:
                return way, [], len(banned)
            if wrong is None:
                wrong = next(n for n, (_, edge) in enumerate(way)
                             if edge[1] & 1 << missing[0])
            banned.add(id(way[wrong][1]))
        return None, goals, len(banned)

    def touch_where(self, number, edge, bit):
        """The move played again: when it first touches `bit`,
        (on the ground?, (sensor, line)); None if it does not."""
        b = self.body
        b.put(self.states[number])
        for joy, frames in edge[2]:
            for _ in range(frames):
                if b.step(joy) & 1 << bit:
                    return bool(b.ground), (b.sensor, b.y >> 8)
                if b.fell:
                    return None
        return None

    @staticmethod
    def back(best, place):
        steps = []
        while best[place][1] is not None:
            came = best[place][1]
            steps.append(came)
            place = came[0]
        return steps[::-1]


# --- what the plan asks -----------------------------------------------
def limited(edge):
    """A flight within the limits of 1.3 (moves on foot: all)."""
    flight = edge[4]
    if edge[3] != "flight":
        return True
    if flight is None:
        return False
    return (flight["across"] <= RULES["across"] * METATILE
            and flight["up"] <= RULES["up"] * METATILE)


def on_foot(edge):
    return edge[3] == "foot"


def reach_box(heirloom, k):
    """Where Oscar's sensor and feet touch an heirloom (vampire):
    |sensor - middle| < TOUCH, top < feet < top + 16 + 20."""
    x, top, _ = heirloom
    return x + 12, top, top + k["HEIRLOOM_BOX"] + 20


def bound_touch(points, heirloom, k, profile, blocks):
    """Can a jump from a surface point touch the heirloom? The bound:
    after t frames his sensor has moved at most 1.5 t + 1 pixels (the
    fraction of his x), plus PUSH for each solid block between the
    point and the heirloom: a push out of a block (push_out) moves him
    at once, by the depth of his body in the block's column plus one,
    7 pixels at most (his sensor is out of that column, or he would
    stand on the block); the search measures the longest frame with a
    push;
    his feet are at most profile[t - 1] lines over the surface (the
    held jump: the highest at every frame, whatever he does with the
    joystick), and past the end of the profile FALL_MAX a frame lower.
    Touching needs feet - 20 < top + 16. The closest it comes:
    [margin in lines, point] (margin > 0: it cannot be touched)."""
    middle, top, below = reach_box(heirloom, k)
    speed, fall = k["WALK_MAX"] / 256, k["FALL_MAX"] / 256
    best = None
    for sensor, line in points:
        low, high = min(sensor, middle) - 32, max(sensor, middle) + 32
        push = PUSH * sum(1 for first, last, _, _ in blocks
                          if first * 16 <= high and (last + 1) * 16 >= low)
        far = max(abs(sensor - middle) - (k["TOUCH"] - 1) - push - 1, 0)
        index = max(math.ceil(far / speed) - 1, 0)
        if index < len(profile):
            highest = max(profile[index:])
        else:
            highest = profile[-1] - fall * (index - len(profile) + 1)
        # the feet at line - highest or lower; touching: feet < below
        margin = (line - highest) - (below - 1)
        if best is None or margin < best[0]:
            best = [margin, [sensor, line]]
    return best


def all_points(body):
    """Every (sensor, line) where a surface holds Oscar up, from the
    metatiles of the level, as Surfaces finds them."""
    s = body.surfaces
    return [(x, line) for x in range(body.c["LEVEL_WIDTH"] * 16)
            for row in range(11)
            for line in [s.line_at(x, row)] if line is not None]


def path_profile(body, info, way=(), over=()):
    """The way the plan calls obligatory (the street, the blocks on
    it and the surfaces whose names start with one in `way`: level
    3's stones in the river), column by column: the line of its top,
    or None (a gap). A block over the street, not on it (level 3's
    hollow oak), is not on the way: the way goes under it; but where
    the plan says the way goes over (`over`, stretches of columns:
    level 6's slabs over the spikes), it is the blocks over the
    street, and where there are none a leap (a gap): from level 6's
    mound onto the slab, from the block onto the wall."""
    s, line = body.surfaces, body.c["START_Y"]
    on_street = (line >> 4) - 1             # a block's lowest row
    tops = {}
    for item in info["surfaces"]:
        if item["name"].startswith(tuple(way)) and way:
            for x, y in item["points"]:
                tops[x // 16] = min(tops.get(x // 16, y), y)
    profile = []
    for col in range(body.c["LEVEL_WIDTH"]):
        top = tops.get(col)
        for first, last, row, bottom in info["solids"]:
            if first <= col <= last and bottom == on_street:
                top = row * METATILE if top is None else min(
                    top, row * METATILE)
        if top is None and all(s.line_at(x, line >> 4) == line
                               for x in range(col * 16, col * 16 + 16)):
            top = line
        if any(first <= col <= last for first, last in over):
            top = None
            for first, last, row, bottom in info["solids"]:
                if first <= col <= last:
                    top = row * METATILE if top is None else min(
                        top, row * METATILE)
        profile.append(top)
    return profile


def check_path(profile, start_col, end_col, water):
    """The steps and gaps of the way, against the rules."""
    steps, gaps = [], []
    col, last = start_col, profile[start_col]
    while col < end_col:
        col += 1
        if profile[col] is None:
            first = col
            while profile[col] is None:
                col += 1
            width = col - first
            wet = any(a <= first <= b for a, b in water)
            gaps.append({"columns": [first, col - 1], "width": width,
                         "water": wet,
                         "on_foot": width <= RULES["gap"],
                         "difference": (last - profile[col])
                         // METATILE})
        rise = (last - profile[col]) // METATILE
        if rise:
            steps.append({"column": col, "metatiles": rise})
        last = profile[col]
    return steps, gaps


def space_rule(body, points):
    """For every point where Oscar can stand (his body clear of solid
    blocks): lines up to the first solid block over him."""
    k, s = body.k, body.surfaces
    closest, under = None, 0
    for sensor, line in points:
        x = sensor - k["SENSOR_X"]
        cols = range((x + k["BODY_LEFT"]) >> 4,
                     min((x + k["BODY_RIGHT"]) >> 4,
                         body.c["LEVEL_WIDTH"] - 1) + 1)
        rows = range(max(line - 20, 0) >> 4, ((line - 1) >> 4) + 1)
        if any(s.solid(col, row, row) for col in cols for row in rows):
            continue
        for row in range((line - 1) >> 4, -1, -1):
            if any(s.solid(col, row, row) for col in cols):
                gap = line - (row + 1) * METATILE
                under += 1
                if closest is None or gap < closest[0]:
                    closest = [gap, [sensor, line]]
                break
    return closest, under


def replay(game_files, labels, start, way, search, number,
           lantern=None):
    """The witness in the whole model, on level `number`, reached as
    the C64 reaches it (through the gates of the levels before it):
    from the start, or (lantern: its column) as after a fall with the
    lantern lit. Oscar where the search said after every move; what
    happened (the frames counted from the start of the way)."""
    game = game_model.Game(game_files, labels)
    # The enemies left out (only to be avoided, section 1.7).
    game.all_objects = [dict(objects, enemies=[])
                        for objects in game.all_objects]
    game.objects = game.all_objects[0]
    game.reset_enemies()
    count = 0

    def transition(kind):
        nonlocal count
        game.start_transition(kind)
        for _ in range(game.k["TRANS_FRAMES"]):
            count += 1
            game.turn(0, count & 255)

    transition(game_model.GO_START)     # from the title
    for _ in range(number - 1):
        transition(game_model.GO_NEXT)
    if lantern is not None:         # back at the lantern, as after a
        game.respawn_x = lantern * 16 + 8 - 12      # fall there
        game.lantern_lit = 1
        transition(game_model.GO_BACK)
    setup = count
    del game.events[:]
    body_keys = ("x", "y", "vx", "vy", "ground", "face", "form",
                 "puff", "flap", "gnam", "energy", "prev_joy")
    same = (game.level_no == number - 1
            and all(getattr(game, key) == value for key, value in
                    zip(body_keys, search.states[start])))
    moves = elsewhere = 0
    through = False
    joys = []                   # the joystick, a frame at a time
    for _, edge in way:
        for joy, frames in edge[2]:
            for _ in range(frames):
                count += 1
                game.turn(joy, count & 255)
                joys.append(joy)
                if any(what == "through the gate"
                       for _, what in game.events[-3:]):
                    through = True
                    break
            if through:
                break
        if through:
            break
        moves += 1
        state = tuple(getattr(game, key) for key in body_keys)
        if edge[0] is not None and not search.close(state, edge[0]):
            elsewhere += 1
    frames = count - setup
    arena = None
    if through and game.trans_kind == game_model.GO_ARENA:
        night_before = game.night, game.night_time
        game.has_staff = 1      # (from level 3 on, in the game)
        for _ in range(game.trans):
            count += 1
            game.turn(0, count & 255)
        came = {"x": game.x >> 8, "camera": game.camera,
                "arena": game.arena}
        before = len(game.events)
        joys, count = fight.play(game, count)
        after = [what for _, what in game.events[before:]]
        night = game.k["NIGHT_STEP"]
        arena = {"came_in": came, "fight_frames": len(joys),
                 "struck": after.count("tom struck"),
                 "beaten": "tom beaten" in after,
                 "gone": "tom gone" in after,
                 "hits_on_oscar": after.count("hit"),
                 "fallen": after.count("fallen"),
                 "dawn": "dawn" in after,
                 "won": game.game_state == game_model.ST_WON,
                 "night_at_the_door": (night_before[0] - 1) * night
                 + night_before[1],
                 "night_left": (game.night - 1) * night
                 + game.night_time}
        del game.events[before:]            # (the witness's events)
    events = [what for _, what in game.events]
    marks = ("to bat", "to vampire", "heirloom", "lantern", "gate",
             "through", "fallen", "dawn", "moth")
    return {"frames": frames, "moves_of_the_search": moves,
            "events": [[frame, what] for frame, what in game.events
                       if what.startswith(marks)],
            "start_as_searched": same, "elsewhere": elsewhere,
            "heirlooms": sorted(what for what in events
                                if what.startswith("heirloom")),
            "lantern": "lantern" in events or lantern is not None,
            "gate_open": "gate open" in events,
            "through_the_gate": through,
            "fallen": events.count("fallen"),
            "dawn": "dawn" in events,
            "moths": sum(what.startswith("moth") for what in events),
            "arena": arena, "joystick": runs(joys)}


def runs(joys):
    """[[joystick, frames], ...]: a frame list in runs."""
    out = []
    for joy in joys:
        if out and out[-1][0] == joy:
            out[-1][1] += 1
        else:
            out.append([joy, 1])
    return out


def flights_of(way):
    return [dict(edge[4]) for _, edge in way
            if edge[3] == "flight" and edge[4]]


def without_moths(files):
    """The levels without their moths: a flight must not need them.
    (files, {level number: moth count})."""
    c = files["constants"]
    levels, moths = [], {}
    for number, start_map in enumerate(files["levels"], 1):
        level = bytearray(start_map)
        found = [i for i, tile in enumerate(level)
                 if tile == c["MOTH_TILE"]]
        for i in found:
            level[i] = c["EMPTY_SKY"]
        levels.append(bytes(level))
        moths[number] = len(found)
    no_moths = dict(files)
    no_moths["levels"] = levels
    no_moths["level"] = levels[0]
    return no_moths, moths


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level", type=int, choices=sorted(PLAN),
                        help="one level only (default: all)")
    args = parser.parse_args()
    began = time.time()
    labels = vicemon.load_labels(LABELS)
    files = reference.load()
    no_moths, moths = without_moths(files)
    game = game_model.Game(no_moths, labels)
    report = {"levels": [], "checks": []}
    failures = []

    def check(name, ok, **detail):
        report["checks"].append({"check": name, "pass": bool(ok),
                                 **detail})
        if not ok:
            failures.append(name)
        print(f"  {'PASS' if ok else 'FAIL'}  {name}"
              + (f": {detail}" if detail else ""))

    print("3. The measures of 1.3, on the model")
    body = Body(game, no_moths["levels"][0])
    found = measures(game, body)
    profile = found.pop("jump_profile")
    report["measures"] = found
    report["plan_measures"] = PLAN_MEASURES
    for name, value in PLAN_MEASURES.items():
        print(f"        {name:18s} plan {value:5}  model {found[name]}")
    check("a jump climbs 2 metatiles, not 3",
          2 * METATILE <= found["rise"] < 3 * METATILE,
          rise=found["rise"])
    check("the highest jump measured to the fastest fall (the bound)",
          found["profile_ends_at_fall_max"])
    check("a long jump clears a gap of 3 metatiles",
          found["long_jump"] > 3 * METATILE,
          length=found["long_jump"])

    numbers = [args.level] if args.level else sorted(PLAN)
    for number in numbers:
        level_report = {"level": number, "name": PLAN[number]["name"]}
        report["levels"].append(level_report)

        def level_check(name, ok, **detail):
            check(f"level {number}: {name}", ok, **detail)

        check_level(number, files, no_moths, moths[number], labels,
                    profile, level_check, level_report)

    report["seconds"] = round(time.time() - began, 1)
    report["result"] = "PASS" if not failures else "FAIL"
    report["failures"] = failures
    EVIDENCE.parent.mkdir(exist_ok=True)
    EVIDENCE.write_text(json.dumps(report, indent=2) + "\n",
                        encoding="utf-8")
    print(f"{report['result']}: {len(report['checks'])} checks, "
          f"{report['seconds']} s; {EVIDENCE.name}")
    return 0 if not failures else 1


def check_enemies(info, plan, body, objects, check):
    """Section 4.7, on where the enemies of the level move."""
    k, c = body.k, body.c
    found = info["enemies"]
    print("7. The enemies")
    low, high = RULES["enemies"]
    check(f"{low} to {high} enemies", low <= len(found) <= high,
          enemies=len(found))
    check("the enemies the plan gives (section 3): kind, stretch",
          tuple((e["kind"], e["first"], e["last"]) for e in found)
          == plan["enemies"])
    # place_enemies shows an enemy whose sprite's X register would be
    # 0-343: x from camera - 31 to camera + 312. Wherever the camera
    # is, the enemies that can be in that window.
    most = max(sum(e["x_min"] <= camera + 312 and e["x_max"] >=
                   camera - 31 for e in found)
               for camera in range(c["CAMERA_MAX"] + 1))
    # In a setting with a moon (the wood) sprite 6 is the moon: the
    # program shows three enemies at most there (moon.py).
    limit = RULES["on_screen"] - (c["MOON_SETTINGS"] >> info["env"] & 1)
    check(f"at most {limit} enemies in a window of 19 columns and the "
          "margin (344 pixels)", most <= limit, most=most)
    start_col = (c["START_X"] + k["SENSOR_X"]) // METATILE
    lantern_col = objects["lantern"][0]

    def away(col, e):
        return max(e["first"] - col, col - e["last"], 0)
    closest = min(min(away(start_col, e), away(lantern_col, e))
                  for e in found)
    check(f"none within {RULES['enemy_away']} columns of the start "
          "and of the checkpoint", closest >= RULES["enemy_away"],
          closest=closest)
    points = {}
    for item in info["surfaces"]:
        points.setdefault(item["name"], set()).update(
            map(tuple, item["points"]))
    # A patrol given a line, not a surface (level 4's on the bank):
    # its street is the tops of the solid blocks.
    points[None] = {(x, top * METATILE) for first, last, top, _
                    in info["solids"]
                    for x in range(first * METATILE,
                                   (last + 1) * METATILE)}
    walks = []
    for e in found:
        if e["kind"] != "patrol":
            continue
        cols = range(e["first"], e["last"] + 1)
        under = all((x, e["line"]) in points[e["on"]]
                    for x in range(cols[0] * METATILE,
                                   (cols[-1] + 1) * METATILE))
        top = e["line"] - 21
        walls = [s for s in info["solids"]
                 if s[0] <= cols[-1] and s[1] >= cols[0]
                 and s[2] * METATILE < e["line"]
                 and (s[3] + 1) * METATILE > top]
        walks.append(under and not walls)
    check("the watchmen: their street under the whole stretch, no "
          "block in their way", all(walks), watchmen=len(walks))


def arena_game(files, labels):
    """A model in the arena: the last level, as the C64 reaches
    it, then the transition through the door of the throne room."""
    game = game_model.Game(files, labels)
    count = 0
    for kind in ([game_model.GO_START]          # the title
                 + [game_model.GO_NEXT] * (len(files["levels"]) - 1)
                 + [game_model.GO_ARENA]):
        game.start_transition(kind)
        for _ in range(game.k["TRANS_FRAMES"]):
            count += 1
            game.turn(0, count & 255)
    return game, count


def check_arena(files, labels, info, check, report):
    """The arena: closed, its pedestals reached, no enemy."""
    print("The arena (0.9)")
    c = reference.constants()
    found = {}
    # Closed: Oscar walks left, then right, Tom held aside (gone, his
    # moment long: he does not touch Oscar, nor end the level).
    for way, joy in (("left", game_model.GO_LEFT),
                     ("right", game_model.GO_RIGHT)):
        game, count = arena_game(files, labels)
        game.tom_state, game.tom_timer = game.k["TS_GONE"], 255
        cameras = set()
        for _ in range(250):
            count += 1
            game.turn(joy, count & 255)
            game.tom_timer = 255
            cameras.add(game.camera)
        found[way] = {"x": game.x >> 8, "cameras": sorted(cameras)}
    left_wall = c["TOM_MIN_X"] - game.k["BODY_LEFT"]
    check("closed: on the left the wall of the throne room, on the "
          "right the end of the level; the camera still",
          found["left"]["x"] == left_wall
          and found["right"]["x"] == game.x_max
          and found["left"]["cameras"] == found["right"]["cameras"]
          == [c["CAMERA_MAX"]], **found)
    # The pedestals: from the floor, a run and a jump onto each.
    pedestals = {}
    for item in info["surfaces"]:
        if item["name"].startswith("pedestal ") and \
                item["name"] != "pedestal":
            pedestals[item["name"]] = {tuple(p) for p in item["points"]}
    reached = {}
    for name, points in sorted(pedestals.items()):
        first = min(x for x, _ in points)
        reached[name] = None
        for run in range(0, 160, 4):
            for hold in (8, 16, 28):
                game, count = arena_game(files, labels)
                game.tom_state, game.tom_timer = game.k["TS_GONE"], 255
                start = len(game.landed)
                for joy, frames in ((game_model.GO_RIGHT, run),
                                    (game_model.GO_RIGHT
                                     | game_model.UP, hold),
                                    (game_model.GO_RIGHT, 40)):
                    for _ in range(frames):
                        count += 1
                        game.turn(joy, count & 255)
                        game.tom_timer = 255
                landed = [(x, y) for _, x, y, who, _ in
                          game.landed[start:] if who == "vampire"]
                if any(spot in points for spot in landed):
                    reached[name] = {"run": run, "up_held": hold,
                                     "from_x": first}
                    break
            if reached[name]:
                break
    check("its two pedestals reached from its floor with a jump",
          len(pedestals) == 2 and all(reached.values()), **reached)
    window = (c["CAMERA_MAX"] - 31, c["CAMERA_MAX"] + 312)
    near = [e for e in info["enemies"]
            if e["x_max"] >= window[0] and e["x_min"] <= window[1]]
    check("no enemy of the level in the arena's window (Tom is "
          "four sprites)", not near, enemies=len(near))
    report["arena"] = {"walls": found, "pedestals": reached}


def check_level(number, files, no_moths, moth_count, labels, profile,
                check, report):
    """The checks of section 4 on level `number`."""
    plan = PLAN[number]
    info = game_model.level_info(number)
    start_map = files["levels"][number - 1]
    game = game_model.Game(no_moths, labels)
    body = Body(game, no_moths["levels"][number - 1], number)
    k, c = body.k, body.c
    objects = body.objects
    names = [kind for _, _, kind in info["heirlooms"]]
    print(f"Level {number}, {plan['name']}")
    check("the name in the HUD", info["name"] == plan["name"],
          level_name=info["name"])

    print("6. The things of the level")
    tracts = plan["tracts"]
    cols = [x // 16 + 1 for x, _, _ in objects["heirlooms"]]
    in_tracts = [next((n for n, (a, b) in enumerate(tracts)
                       if a <= col <= b), None) for col in cols]
    check("three heirlooms, one a tract", len(cols) == 3
          and in_tracts == [0, 1, 2], columns=cols)
    apart = min(b - a for a, b in zip(cols, cols[1:]))
    check("heirlooms at least 21 columns apart",
          apart >= RULES["apart"], closest=apart)
    lantern_col, lantern_row = objects["lantern"]
    low, high = plan["checkpoint"]
    check(f"the checkpoint in tract B, columns {low}-{high}",
          low <= lantern_col <= high, column=lantern_col)
    low, high = plan["exit"]
    doors = objects["doors"]
    check(f"the exit at columns {low}-{high}, shut at the start",
          all(low <= col <= high for col, _, _ in doors)
          and all(start_map[col * 11 + row] != tile
                  for col, row, tile in doors),
          doors=sorted({col for col, _, _ in doors}))
    low, high = plan["moths"]
    check(f"{low} to {high} moths", low <= moth_count <= high,
          moths=moth_count)
    env = files["envs"][body.env]
    shape, flags = env["metashape"], env["metaflags"]
    lantern_tile = start_map[lantern_col * 11 + lantern_row]
    same = [(shape[a], flags[a]) == (shape[b], flags[b]) for a, b in
            [(lantern_tile, objects["lantern_tile"])]
            + [(start_map[col * 11 + row], tile)
               for col, row, tile in doors]]
    check("the lantern lit and the gate open change no surface and "
          "no block", all(same))
    check_enemies(info, plan, body, objects, check)

    print("3. The way, against the measures of 1.3")
    path = path_profile(body, info, plan.get("way", ()),
                        plan.get("over", ()))
    start_col = (c["START_X"] + k["SENSOR_X"]) // 16
    steps, gaps = check_path(path, start_col, objects["door"][0],
                             info["water"])
    report["path"] = {"steps": steps, "gaps": gaps}
    check("the way: no step up over 2 metatiles",
          all(s["metatiles"] <= RULES["rise"] for s in steps),
          steps=[[s["column"], s["metatiles"]] for s in steps])
    check("the way: gaps on foot up to 3 metatiles, the others "
          "flights up to 20, level",
          all(g["on_foot"] or (g["width"] <= RULES["across"]
                               and abs(g["difference"]) <= RULES["up"])
              for g in gaps),
          gaps=[[*g["columns"], "water" if g["water"] else "pit"]
                for g in gaps])
    # One way on foot: the gaps flown, and the steps down of more
    # than 2 metatiles (back, a climb the bat does).
    # The hazards (level 3's brambles, level 4's wisps): on the
    # street; jumped on foot, at most 3 columns, or with the
    # way over them all along (level 4's boardwalk). The search goes
    # through none of them.
    hazards = info.get("hazards", [])
    street_row = c["START_Y"] // METATILE - 1
    check("the hazards: on the street, at most "
          f"{RULES['gap']} columns or under the way, as the plan "
          "gives them",
          all(row == street_row and (
              last - first + 1 <= RULES["gap"]
              or all(path[col] is not None
                     and path[col] < c["START_Y"]
                     for col in range(first, last + 1)))
              for first, last, row in hazards)
          and tuple((first, last) for first, last, _ in hazards)
          == plan.get("hazards", ()),
          hazards=hazards)
    one_way = sorted([g["columns"][1] for g in gaps if not g["on_foot"]]
                     + [s["column"] - 1 for s in steps
                        if s["metatiles"] < -RULES["rise"]])
    check("the way: one way on foot only where the plan says",
          one_way == [last for _, last in plan["one_way"]],
          one_way=one_way,
          plan=[[name, last] for name, last in plan["one_way"]])

    print("5. The space to turn back")
    points = game_model.surface_names(number)
    for first, last, top, bottom in info["solids"]:
        if bottom != street_row:            # over the street: off
            for x in range(first * 16, (last + 1) * 16):    # the way
                points[(x, top * 16)] = "block over the street"
    closest, under = space_rule(body, points)
    check("2 metatiles between a surface and a block over it",
          closest is None or closest[0] >= RULES["space"] * METATILE,
          surfaces_under_blocks=under, closest=closest)
    report["space"] = {"points_under_blocks": under,
                       "closest": closest}

    print("Search (the model, no moths) ...")
    search = Search(body)
    lantern_x = lantern_col * 16 + 8 - 12
    starts = [standing_state(body, c["START_X"], c["START_Y"]),
              standing_state(body, lantern_x, c["START_Y"])]
    start, lantern = search.explore(starts)
    check("a frame with a push out of a block moves him less than PUSH",
          body.pushed < PUSH, longest=body.pushed, push=PUSH)
    report["search"] = {
        "longest_frame_with_a_push": body.pushed,
        "places": len(search.states),
        "standing": search.kinds.count("stop"),
        "moves": sum(len(out) for out in search.out),
        "flights_from": len(search.flown),
        "model_frames": body.frames}
    print(f"        {report['search']}")

    if number == len(files["levels"]):
        check_arena(no_moths, labels, info, check, report)

    print("1, 2, 4. From the start and from the lantern")
    goals = [0, 1, 2, 4]
    report["witness"] = {}
    night = k["NIGHT_STEPS"] * k["NIGHT_STEP"]
    report["night_frames"] = night
    for name, here, at in (("start", start, None),
                           ("lantern", lantern, lantern_col)):
        best = search.ways(here, limited)
        touched = search.touched(best, limited)
        reached = [TOUCH_NAMES[bit] for bit in sorted(touched)]
        check(f"from the {name}: the three heirlooms and the gate, "
              "flights within the limits",
              all(bit in touched for bit in goals), reached=reached)
        way, left, banned = search.proven(here, goals, limited)
        if way is None:
            check(f"from the {name}: a witness", False,
                  missing=[TOUCH_NAMES[bit] for bit in left])
            continue
        result = replay(no_moths, labels, here, way, search, number, at)
        result["flights"] = flights_of(way)
        report["witness"][name] = result
        check(f"from the {name}: the witness in the whole model",
              result["start_as_searched"] and not result["elsewhere"]
              and len(result["heirlooms"]) == 3
              and result["gate_open"] and result["through_the_gate"]
              and not result["fallen"] and not result["dawn"]
              and not result["moths"] and result["frames"] < night,
              frames=result["frames"], left_out=banned,
              flights=[[f["across"] // METATILE, f["up"] // METATILE]
                       for f in result["flights"]])
        arena = result["arena"]
        if number == len(files["levels"]):          # Tom
            came = (arena or {}).get("came_in", {})
            check(f"from the {name}: through the door of the throne "
                  "room into the arena, Oscar at ARENA_X, the camera at "
                  "the end of the level",
                  arena is not None and came == {
                      "x": c["ARENA_X"], "camera": c["CAMERA_MAX"],
                      "arena": 1}, came_in=came)
            if arena is not None:
                check(f"from the {name}: Tom beaten by the fighter "
                      f"({k['HITS_FULL']} blows), gone, then (0.10) "
                      "the victory; Oscar never without health; "
                      "before dawn",
                      arena["struck"] == k["HITS_FULL"]
                      and arena["beaten"] and arena["gone"]
                      and arena["won"] and not arena["fallen"]
                      and not arena["dawn"],
                      **{key: arena[key] for key in (
                          "fight_frames", "hits_on_oscar",
                          "night_at_the_door", "night_left")})

    # The places beyond the passages one way: the nearest place on
    # the street where he stands still, past the passage.
    reached = search.ways(start, limited)
    beyond = {}
    for passage, last in plan["one_way"]:
        far = [n for n in reached
               if search.kinds[n] == "stop"
               and search.states[n][1] >> 8 == c["START_Y"]
               and (search.states[n][0] >> 8) + k["SENSOR_X"]
               >= (last + 1) * 16]
        beyond[passage] = (min(far, key=lambda n: search.states[n][0])
                           if far else None)

    # On foot alone, from the start and from beyond each passage: the
    # flights are needed where the plan says, the rest is on foot.
    report["on_foot"] = {}
    for passage, expected in plan["on_foot"].items():
        here = start if passage == "the start" else beyond[passage]
        if here is None:
            check(f"on foot from beyond {passage}", False, place=None)
            continue
        foot = search.touched(search.ways(here, on_foot), on_foot)
        reached = [TOUCH_NAMES[bit] for bit in sorted(foot)]
        report["on_foot"][passage] = reached
        where = (passage if passage == "the start"
                 else f"beyond {passage}")
        check(f"on foot from {where}: "
              + ", ".join(TOUCH_NAMES[bit] for bit in sorted(expected))
              + ", nothing else", set(foot) == expected,
              reached=reached)

    # Back from the lantern to tract A: on foot if no passage one way
    # is in between (between its heirloom and the lantern: level 6's
    # second slab), else with flights within the limits.
    between = [name for name, last in plan["one_way"]
               if cols[0] < last < lantern_col]
    allowed, how = ((limited, "flights within the limits") if between
                    else (on_foot, "on foot"))
    way, left, banned = search.proven(lantern, [0], allowed)
    check(f"from the lantern back to tract A, {how}: the {names[0]}",
          way is not None, over=between,
          missing=[TOUCH_NAMES[bit] for bit in left])

    # Back over every passage one way.
    report["back"] = {}
    for passage, _ in plan["one_way"]:
        far = beyond[passage]
        if far is None:
            check(f"from beyond {passage}, back", False, beyond=0)
            continue
        way, left, banned = search.proven(far, [3, 0, 1, 2], limited)
        report["back"][passage] = {
            "from_x": search.states[far][0] >> 8,
            "frames": sum(sum(n for _, n in edge[2])
                          for _, edge in way or []),
            "flights": flights_of(way or [])}
        check(f"from beyond {passage}, back: the lantern and every "
              "heirloom", way is not None,
              from_x=search.states[far][0] >> 8,
              missing=[TOUCH_NAMES[bit] for bit in left])

    print("The kinds of the heirlooms (1.2)")
    path_names = ("street", "solid block") + tuple(
        name for name in set(points.values())
        if name.startswith(tuple(plan.get("way", ()))) and plan.get("way"))
    every_point = all_points(body)

    def where(place):
        state = search.states[place]
        return points.get(((state[0] >> 8) + k["SENSOR_X"],
                           state[1] >> 8))

    path_points = [p for p in every_point
                   if points.get(p) in path_names]
    # The places he reaches on foot, from the start, the lantern
    # and beyond each passage one way: "in flight" is where only the bat
    # gets (1.2), so no jump from these may touch it (a surface only the
    # bat reaches, the top of level 5's pinnacle, does not count).
    foot_places = search.ways(
        [start, lantern] + [n for n in beyond.values() if n is not None],
        on_foot)
    foot_points = sorted({((search.states[n][0] >> 8) + k["SENSOR_X"],
                           search.states[n][1] >> 8)
                          for n in foot_places
                          if search.kinds[n] == "stop"})
    report["heirlooms"] = []
    for index, heirloom in enumerate(objects["heirlooms"]):
        bit = 1 << index
        kind, tract = plan["kinds"][index], tracts[index]
        # Jumps from the way, from any surface (the bound).
        from_path = bound_touch(path_points, heirloom, k, profile,
                                info["solids"])
        from_any = bound_touch(every_point, heirloom, k, profile,
                               info["solids"])
        from_foot = bound_touch(foot_points, heirloom, k, profile,
                                info["solids"])
        # On foot from the way of its tract (the search).
        seeds = [n for n in range(len(search.states))
                 if where(n) in path_names
                 and tract[0] * 16 <= (search.states[n][0] >> 8)
                 + k["SENSOR_X"] < (tract[1] + 1) * 16]
        way = None
        if seeds:
            way, _, _ = search.proven(seeds, [index], on_foot)
        on_foot_reach = way is not None
        # A move from the way that touches it in the air, or standing
        # on the way (not after landing somewhere else).
        from_the_way = False
        for here in seeds:
            for edge in search.out[here]:
                if edge[3] != "foot" or not edge[1] & bit:
                    continue
                found_at = search.touch_where(here, edge, index)
                if found_at and (not found_at[0]
                                 or points.get(found_at[1])
                                 in path_names):
                    from_the_way = True
                    break
            if from_the_way:
                break
        flight = any(edge[3] == "flight" and edge[1] & bit
                     for out in search.out for edge in out)
        if kind == "within reach":
            ok = from_the_way
        elif kind == "off the path":
            ok = on_foot_reach and from_path[0] > 0
        else:
            ok = flight and from_foot[0] > 0
        report["heirlooms"].append({
            "heirloom": index, "name": names[index],
            "column": cols[index], "top": heirloom[1], "kind": kind,
            "on_foot_in_its_tract": on_foot_reach,
            "jump_from_the_way": from_the_way,
            "bound_from_the_way": from_path,
            "bound_from_any_surface": from_any,
            "bound_from_where_he_walks": from_foot,
            "by_the_bat": flight})
        check(f"heirloom {index}, the {names[index]} (column "
              f"{cols[index]}): {kind}", ok,
              on_foot=on_foot_reach, from_the_way=from_the_way,
              bound_way=from_path[0], bound_any=from_any[0],
              bound_foot=from_foot[0], bat=flight)


if __name__ == "__main__":
    sys.exit(main())
