"""Verify Dreadcastle in a private VICE: the complete game, or a step.

  python tests/verify_game.py [--step N] [--root FOLDER] [--vice PATH]
      [--set STATEMENT] [--route FILE] [--no-shows] [--coverage]
      [--stop-at TEXT] [--stop-after N] [--stop-shot NAME]

Without --step it tests the complete game (step 13, at the root of
the package) in four games, one run of VICE: the first with SOUND
FX, won with the joystick only; the second with MUSIC (the theme
through its loop in level 1, then, helped by the test, level 8, the
arena, Tom's theme and the victory); the third with SOUND FX, lost
with the joystick only (dawn in the village, the bell, the jingle);
the fourth with SILENT, helped (dawn in level 7, no jingle). With
--step N it plays the route of step N (tests/step_routes.py) on
chain/NN-name, built first, or on the folder given by --root (a
variant); its report goes to chain/evidence/NN-name/. The route of
the first game is the one told here.

The program is started in VICE (x64sc, PAL), driven through its binary
monitor (tests/vicemon.py). On the title it moves in the menu
(Down to SOUND FX and SILENT, Down again at the end, Up back to
MUSIC), then Fire: a new game. The test plays level 1 on the joystick
(ROUTE): Oscar walks to the left end, into the crates and the pile of
crates (blocked on both sides), climbs them, jumps to the awning of a
stall and takes the chalice, falls into the trapdoor and starts again
at the start; waits for the night watchman to walk away and jumps over
the trapdoor and over him; on to the square (the lamp, the
balcony, the roofs, the spire); on the left roof the black cat jumps
at him: a hit, thrown back, blinking; he lights the lantern; turns
into the bat on the fountain, eats a moth, takes the portrait in the
sky, waits for the crow (a hit), eats another moth; flies to the top,
dives onto a roof; walks off it into the canal and starts again at the
lantern; flies until the energy runs out, is refused a change, rests;
flies over the canal eating two more moths; walks into the second
watchman four times, each time once the blinking is over, until no
health is left: back at the lantern; the test fills the night again;
over the canal again, the watchman walks into him, and blinking he
walks past; into the well, to the end of the level past the shut gate
and back, climbs the well and the balcony and takes the medallion over
it with a jump: the gate opens; through the gate, level 2, the
churchyard: over the tombstones into a grave and back at its start;
over the tombstones and the graves onto the family tomb (the
candelabrum), past its cat and its watchman; the bat over the
landslide (a moth), the lantern; onto the sarcophagus and the chapel,
the bat from the chapel (a moth, the hourglass), past the crows; over
the stream on the piles of the broken bridge; onto the pedestal and
the wall; the bat over the book and the cat and back, down onto the
wall left of the book, with the camera where the gate's left column is
the one the back screen is drawing: walking right Oscar takes the
book, and the gate opens, a door a frame, one of them in that
column too (set_tile, edge_paint);
through the gate, level 3, the wild wood (its own characters and
tables): Fire does nothing yet; he takes the staff lying on the path;
strikes the toad that jumps at him; over the stump to the chalice;
over the scout, turns, and strikes him facing left; the other scout
walks into him (a hit), and blinking over, he strikes it; into the
brambles (a hit, thrown back), then over them; the lantern; from the
stump onto the low branch of the great oak, a jump and a blow in the
air: the owl; Fire, then Up with Fire held: the bat, the blow cut
short; the portrait; down by the river, over the five stones; strikes
the toad under the hollow oak; a jump under the oak (his head on it),
the bat against it (its head too), and no room there to turn back;
up the roots onto the oak, the medallion; through the gap in the
hedge, level 4, the black mire (its characters copied into
SET_SLOT): over the clods of peat in the water, the candelabrum on
the big clod; the owl over the water struck with a jump and a blow;
the toad of the shore struck in a jump at it; onto the dead trunks,
under the walkway, the lantern; into the will-o'-the-wisps (a hit,
thrown back), then up the boardwalk over them; onto the log at the
foot of the great dead tree, the bat straight up to the hourglass on
its top, a glide and a dive; onto the bank, the scout and the toad
on it struck; under the fallen tree, onto the boulder, up onto the
tree, the book; down through the way out, level 5, the grey crags
(the maps, tables and sets unpacked in the transitions; the
second shared colour grey; the moon behind the crag): onto the low
ledge, where the goat walks into him (a hit), then struck from
behind; the boulder, the high ledge, the chalice; onto the rock, the
werewolf of the band jumps at him, a leap over it and away while it
jumps after him; over the crevasse on two stones, the bat up to the
portrait on the pinnacle, a moth, a dive to the lantern; a goat
struck; under the crag, over a crack, the medallion; a goat and a
werewolf struck, over the other crack, through the mouth of the
pass, level 6, the frozen pass (the second shared colour light
blue): onto the mound and the slab, down off it and back into the
spikes of ice (a hit, thrown back), the glint running over them; a
goat struck, the candelabrum; the second mound and slab; over the
chasm on the column of ice; a werewolf struck, the lantern; a long
jump; the eagle struck with a jump and a blow; onto the serac, the
bat straight up and right to the hourglass, perched on the bridge of
snow, Oscar again on it; a werewolf struck; onto the block of ice, a
leap onto the wall, its goat struck; another goat struck under the
ledge; past the drift, up onto it and onto the ledge, the book;
through the col, level 7, Dreadcastle Gate (its packed set
moved under the KERNAL; the moon behind its high walls): the bat over
the moat into the postern, the chalice, the guard struck in it; onto
a barrel, the guard of the courtyard struck; onto the cart, the
lantern; the barrel and the turret, Tom's crow struck with a jump and
a blow, the bat up and right to the portrait on the top of the roof,
Oscar again on the turret; the werewolf of the band struck in a jump
down; the pillar, into the spikes of iron (a hit, thrown back), over
them; the second pillar and the spikes; the step, the stair, up left
onto the wall walk, its guard struck, the medallion; down onto the
stair, Tom's crow and the werewolf struck from it; through the door
of the castle, level 8, the Throne Tower (inside: the second shared
colour orange; the moon behind the walls, seen in the high
windows): onto the armour, the bat perched on a chandelier, Oscar
again on it; onto the chest, the guard struck in a jump down, the
candelabrum; the guard of the gallery walks into him (a hit), then
struck under the columns; the lantern; the stool, the mantel, the bat
up and right to the hourglass on the hood; off the mantel, back into
the fire on the hearth (a hit, thrown back); the werewolf struck;
onto the pedestal and the balcony, its guard struck, the book;
through the door of the throne room: the arena, Tom's pictures
unpacked under the KERNAL and mirrored in the transition, Oscar at
the left of the throne room, the camera at the end of the level; Tom
waits by his throne. The fight is played by the fighter
(tests/fight.py), who looks at the model before every frame as a
player at the screen: Tom growls, leaps and charges in turn, is
struck eight times, faster from the fifth, hits Oscar, is dazed
against both walls; beaten, he runs back to his throne, hops onto
its dais and away through the high window; then the victory:
the words over the arena, the night counted into the score; Fire, the
title; Fire, a new game: level 1, the score 0, no staff; the test
takes the program to level 7 with the staff in hand and sets the
night near its end: dawn, the sky through its colours, Oscar gone in
a puff, THE SUN HAS RISEN; Fire, the title again, its sky blue. At
every gate of levels 1-7, LEVEL CLEAR and the count; the test
then plays the next level from the frame after its start it played
before the count was there, with frame_count as it was then (the
moths' wings, the waits of the captures). At
every frame it stops at joy_ready and writes the joystick byte, then
stops at frame_done and compares with
the model (tests/game_model.py) and the reference
(tests/reference.py):
  - Oscar's variables, his form and energy, the level's (health,
    night, heirlooms, lantern, gate, transition, where he starts
    again, his protection and his stun after a hit), the camera's;
    the staff (his, the blow) and the setting; Tom's bytes
    (the arena, his state, place, speeds, picture, hits, flash; the
    page shown, his X register), his four sprites (3, 4, 5, 7:
    registers, pointers, colours) and the page of TOM_SPRITES shown,
    his picture (facing left, mirrored as it was copied); his
    pictures under the KERNAL, unpacked, and the table that mirrors,
    when the fight starts; which song plays and whether it
    plays; $d021-$d023
    and $d01b as the setting wants them ($d021 black after
    the HUD's interrupt, the setting's after the top one, blue in the
    castle; play_d021 the setting's); the enemies' table at
    $c680 (where each is, its speed, its way, its timer, its picture,
    struck); the sprite registers (Oscar's, blinking while protected;
    sprite 2 of the staff, held or lying; sprites 3-6 of the enemies,
    in their order, their puffs; where the moon is (the wood, the
    mire, the mountain) sprites 3-5, and sprite 6 the moon, still
    whatever the camera (and in the middle of the turn:
    place_enemies leaves it on, with its ninth bit); sprite 7
    of the heirlooms), the screen on or off;
  - the two screens and the colour RAM, rows 0-21, columns 0-38:
    equal to the model, and, while the game is played, the screen in
    front equal to the level seen from the camera; the level in
    memory (its copy at $c000), the setting's tables at $c700, the
    moths' two characters in both character sets the VIC-II sees
    ($4800 and SET_SLOT, $5800), the eight of the hazards that
    flicker in SET_SLOT (the wisps; the spikes;
    the keep's spikes, the hall's fire),
    the HUD in both screens; at the end of every step, the whole of
    SET_SLOT;
  - the HUD interrupt on line 226, with the scroll and the screen of
    the frame before, then the HUD's characters; the colour RAM moved
    in time;
  - one turn of the main loop a frame, never late, transitions
    included;
  - the route: at the end of a step, Oscar stands where he should,
    in the form he should, with the moths eaten and the heirlooms
    taken so far (ROUTE); the surfaces landed on in the eight
    levels; every picture and every heirloom shown; hits by the three
    kinds of enemy, by one of the wood, of the mountain, of the
    castle, by the brambles, the wisps, the spikes and the fire, the
    blinking; the 44 pictures of the enemies, two to four of them on
    the screen together; every enemy of the wood, the mountain and
    the castle struck, facing both ways, on the ground and in the
    air; the eleven pictures of the staff;
  - VICE captures at the rests of the route, pixel by pixel equal to
    the reference picture (the moon behind the crag where it
    is in front of it; behind the castle's high walls and in
    the windows of the hall);
  - the music: after every frame of music (music_done, in the top
    interrupt) the copy of the SID registers and the state of the three
    voices equal the model (tests/player_model.py); the copy
    also as it goes into the SID (music_play), where an effect just
    started has its gate off; the cycles of a
    frame of music; the theme plays through its loop; the data of
    both songs in memory are those music.py compiled (Tom's
    under the KERNAL, with mirror_to); where the program
    starts a song or stops (music_start, music_stop) the model of the
    player does the same; Tom's theme from the arena shown until he
    is beaten, then silence; the theme from its start in every
    level, stopped at every gate and at dawn, on the title as the menu
    says: the program's calls as the model's;
  - the game's state, the menu's choice, the score and the band
    of words ($0300) equal the model at every frame; the title's
    sprites (the name: hi-res, stretched, its colour), not stretched
    and multicolour out of it; the score at the victory as the points
    of what happened; the count's frames as states.asm sets them.
It writes evidence/game-test.json and the captures in evidence/.
Only the VICE process started here is controlled and closed.
"""

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import struct
import sys
import zlib

sys.path.insert(0, str(Path(__file__).resolve().parent))
# The data's Python of the program tested: with --root, that
# folder's (a variant may change the songs, the words, the tables).
ASSETS = Path(__file__).resolve().parents[1] / "game/assets"
if "--root" in sys.argv[:-1]:
    ASSETS = (Path(sys.argv[sys.argv.index("--root") + 1]).resolve()
              / "game/assets")
sys.path.insert(0, str(ASSETS))
import fight         # noqa: E402
import game_model    # noqa: E402
import pack          # noqa: E402
import player_model  # noqa: E402
import reference     # noqa: E402
import step_routes   # noqa: E402
import vicemon       # noqa: E402

PROJECT = vicemon.PROJECT
PRG = PROJECT / "game/build/dreadcastle.prg"
LABELS = PROJECT / "game/build/dreadcastle.lbl"
REPORT = PROJECT / "evidence/game-test.json"

R, L, U = game_model.GO_RIGHT, game_model.GO_LEFT, game_model.UP
D, F = game_model.DOWN, game_model.FIRE
V, B = game_model.VAMPIRE, game_model.BAT


class Beats:
    """A joystick that beats the bat's wings: Up pushed for one
    frame every `every` frames, from frame `first`; `hold` all
    the time."""

    def __init__(self, hold, every, first=0):
        self.hold, self.every, self.first = hold, every, first

    def at(self, frame):
        beat = frame >= self.first and \
            (frame - self.first) % self.every == 0
        return self.hold | (U if beat else 0)

    def __str__(self):
        return (f"{self.hold} and Up every {self.every} frames "
                f"from frame {self.first}")

    def __repr__(self):
        return f"Beats({self.hold}, {self.every}, {self.first})"


class Until:
    """The frames of a step: until `test(model)` holds, at most
    `most` frames (more: the route fails)."""

    def __init__(self, test, most, text):
        self.test, self.most, self.text = test, most, text

    def __str__(self):
        return f"until {self.text}"


# The joystick of the fight: the fighter of fight.py, on the
# model of the test (main puts it in the place of FIGHT).
FIGHT = "the fighter"
FIGHT_AGAIN = "the fighter, a new fight"
# The frames of a transition into the next level, and as many
# more as the step through the gate went on after Oscar passed it
# (the count of the night came in between): the next level is then
# played from the same frame after its start as without the count,
# with
# the enemies where the route found them.
NEXT_LEVEL = "the transition, then as many frames as before"
# A capture is taken in the last SHOT_WINDOW frames of its step,
# at the first frame whose picture holds (steady); else as soon as one
# holds while the route goes on, at most SHOT_LATE frames later. The
# capture adds no frames: the route is the same joystick, whatever
# the moths' wings and the hazards are doing.
SHOT_WINDOW, SHOT_LATE = 8, 40


def since(event, frames):
    """Until `frames` frames after the model's last `event`
    (a jingle to its end)."""
    def test(model):
        at = [f for f, e in model.events if e == event]
        return bool(at) and model.frame - at[-1] >= frames
    return test


def happens(event):
    """Until `event` happens, counted from the step's start (an
    earlier one does not count)."""
    seen = {}

    def test(model):
        if "from" not in seen:
            seen["from"] = len(model.events)
        return any(e == event for _, e in model.events[seen["from"]:])
    return test


def tom_is(state, timer=None):
    """Until Tom is in `state` (TS_..., a label), its timer at
    `timer` if given."""
    def test(model):
        k = model.k
        return model.tom_state == k[state] and (
            timer is None or model.tom_timer == timer(k))
    return test


def joystick(joy, frame):
    """The joystick byte of a step at its frame `frame`."""
    return joy.at(frame) if hasattr(joy, "at") else joy


# The route: (what, frames, joystick, where Oscar stands at the end
# of it or None (in the air, or not checked), capture at the end,
# and what must be true at the end: his form, the moths eaten, the
# heirlooms taken, something that happened in the step; and "poke":
# values the test writes into the C64 and the model before the step).
ROUTE = [
    # The title: the name over the castle's door, the menu.
    ('the title: the name, the castle, the moon, the menu', 30, 0, None,
     'dreadcastle-title.png'),
    ('the menu: Down, SOUND FX', 1, D, None, None, dict(event='menu 1')),
    ('let go: no music', 5, 0, None, None),
    ('the menu: Down, SILENT', 1, D, None, None, dict(event='menu 2')),
    ('let go', 20, 0, None, 'dreadcastle-silent.png'),
    ('the menu: Down again, nothing below', 1, D, None, None),
    ('let go, Down held', 5, D, None, None),
    # The first game with SOUND FX, won with the joystick only:
    # from here to the victory the test writes nothing into the C64.
    ('the menu: Up, SOUND FX', 1, U, None, None, dict(event='menu 1')),
    ('let go: PRESS FIRE blinks', 46, 0, None, None),
    ('Fire: a new game', 1, F, None, None, dict(event='start')),
    ('the transition into level 1, Fire held', 49, F, 'street', None),
    ('still at the start', 35, 0, 'street', 'dreadcastle-start.png'),
    ('walk left to the end of the level', 30, L, 'street', None),
    ('walk right into the crates', 97, R, 'street', None,
     dict(event='blocked right')),
    ('let go', 3, 0, 'street', None),
    ('a short jump right', 6, R | U, None, None),
    ('onto the crates', 18, R, 'solid block', None),
    ('rest on the crates', 25, 0, 'solid block', None),
    ('walk right, off the crates', 29, R, 'street', None),
    ('walk on', 37, R, 'street', None),
    ('walk left into the crates', 67, L, 'street', None,
     dict(event='blocked left')),
    ('right to the pile of crates', 75, R, 'street', None),
    ('jump right onto the pile', 38, R | U, 'solid block', None),
    ('a run and a jump right: on', 1, R, None, None),
    ('a run and a jump right: Up held 14 frames', 14, R | U, None, None),
    ('a run and a jump right: onto the stall 2', 18, R, 'stall 2', None),
    ('let go on the awning', 16, 0, 'stall 2', None),
    ('rest on the awning: the chalice', 23, 0, 'stall 2',
     'dreadcastle-chalice.png'),
    ('walk right on the awning: the chalice', 23, R, 'stall 2', None,
     dict(event='heirloom 0', got=1)),
    ('on, off the awning to the street', 62, R, 'street', None),
    ('walk right to the trapdoor', 38, R, None, None, dict(event='fallen')),
    ('Oscar falls: back at the start', 50, 0, 'street', None),
    ('back at the start', 42, 0, 'street', 'dreadcastle-back-at-start.png'),
    ('walk right to the crates again', 67, R, 'street', None),
    ('a jump: Up held 3 frames', 3, R | U, None, None),
    ('a jump: onto the solid block', 17, R, 'solid block', None),
    ('off the crates, to the pile', 95, R, 'street', None),
    ('up: Up held 13 frames', 13, R | U, None, None),
    ('up: onto the solid block', 13, R, 'solid block', None),
    ('over the pile, down', 36, R, 'street', None),
    ('to the trapdoor', 107, R, 'street', None),
    ('let go', 16, 0, 'street', None),
    ('wait: the watchman walks away, right', 100, 0, 'street', None),
    ('a jump over the trapdoor: on', 7, R, None, None),
    ('a jump over the trapdoor: Up held 28 frames', 28, R | U, None, None),
    ('a jump over the trapdoor: onto the street', 18, R, 'street', None),
    ('let go', 16, 0, 'street', None),
    ('a jump over the watchman: on', 36, R, None, None),
    ('a jump over the watchman: Up held 26 frames', 26, R | U, None, None),
    ('a jump over the watchman: over it, onto the street', 19, R, 'street',
     None),
    ('a jump over the watchman: on, away from it', 30, R, None, None),
    ('walk right, under the lamp', 136, R, 'street', None),
    ('let go', 16, 0, 'street', None),
    ('jump up onto the lamp: Up held 8 frames', 8, U, None, None),
    ('jump up onto the lamp: onto the lamp', 8, 0, 'lamp', None),
    ('a hop right to the balcony: Up held 1 frames', 1, R | U, None, None),
    ('a hop right to the balcony: onto the balcony', 19, R, 'balcony', None),
    ('let go', 14, 0, 'balcony', None),
    ('jump up through the roof: Up held 14 frames', 14, U, None, None),
    ('jump up through the roof: onto the right roof', 6, 0, 'right roof',
     None),
    ('rest on the roof', 12, 0, 'right roof', 'dreadcastle-roof.png'),
    ('jump left onto the spire: Up held 26 frames', 26, L | U, None, None),
    ('jump left onto the spire: onto the spire', 13, L, 'spire', None),
    ('over the top of the spire', 6, L, 'spire', None),
    ('jump left onto the roof: on', 17, L, None, None),
    ('jump left onto the roof: Up held 1 frames', 1, L | U, None, None),
    ('jump left onto the roof: onto the left roof', 29, L, 'left roof', None),
    ('over the roof: the cat jumps at him, a hit', 36, L, None, None,
     dict(event='hit')),
    ('thrown back, he lands', 14, 0, None, None),
    ('blinking, down to the street', 83, L, 'street', None),
    ('walk right to the lantern: it lights up', 264, R, 'street', None,
     dict(event='lantern')),
    ('let go', 16, 0, 'street', None),
    ('rest by the lantern', 30, 0, 'street', 'dreadcastle-lantern.png'),
    ('walk right, to the fountain', 62, R, 'street', None),
    ('a hop onto the fountain: Up held 1 frames', 1, R | U, None, None),
    ('a hop onto the fountain: onto the fountain', 15, R, 'fountain', None),
    ('let go', 16, 0, 'fountain', None),
    ('Up and Fire: the bat', 1, U | F, 'fountain', None, dict(form=B,
     event='to bat')),
    ('the smoke', 12, U | F, 'fountain', None),
    ('perched on the fountain: the portrait above', 21, 0, 'fountain',
     'dreadcastle-bat-fountain.png', dict(form=B)),
    ('beats: up', 81, Beats(0, 12), None, None, dict(event='beat')),
    ('beats left, at that height: a moth', 48, Beats(L, 28), None, None,
     dict(moths=1)),
    ('beats right: the portrait (the crow about)', 88, Beats(R, 28), None,
     None, dict(got=2)),
    ('the bat waits for the crow: a hit', 24, 0, None, None,
     dict(event='hit')),
    ('beats right: the next moth', 96, Beats(R, 28), None, None,
     dict(moths=2)),
    ('fast beats up to the top', 27, Beats(R, 6), None, None),
    ('beats right, over the house', 74, Beats(R, 28, 6), None, None),
    ('a dive onto the roof', 8, D, 'roof C1', None, dict(event='dive')),
    ('perched on the roof', 34, 0, 'roof C1', 'dreadcastle-bat-roof.png'),
    ('Down and Fire: Oscar, on the roof', 1, D | F, 'roof C1', None,
     dict(form=V, event='to vampire')),
    ('the smoke', 14, 0, 'roof C1', None),
    ('walk right down the roof, off its end: the canal', 109, R, None, None,
     dict(event='fallen')),
    ('Oscar falls: back at the lantern', 50, 0, 'street', None),
    ('back at the lantern', 20, 0, 'street',
     'dreadcastle-back-at-lantern.png'),
    ('Up and Fire: the bat', 1, U | F, 'street', None, dict(form=B,
     event='to bat')),
    ('the smoke', 14, 0, 'street', None),
    ('Up held: a single beat', 20, U, None, None, dict(event='beat')),
    ('beats right, until the energy runs out', 217, Beats(R, 9), None, None,
     dict(form=V, event='out of energy')),
    ('Oscar falls', 50, 0, None, None),
    ('Up and Fire: not enough energy (Up: a jump)', 1, U | F, None, None,
     dict(form=V, event='refused')),
    ('he lands', 22, 0, None, None),
    ('rest: the energy comes back', 300, 0, None, None),
    ('walk right, to the canal', 126, R, 'street', None),
    ('let go at its edge', 16, 0, 'street', None),
    ('Up and Fire: the bat', 1, U | F, 'street', None, dict(form=B,
     event='to bat')),
    ('the smoke', 12, U | F, 'street', None),
    ('beats: up', 90, Beats(0, 12), None, None),
    ('beats right over the canal: a moth', 45, Beats(R, 28), None, None,
     dict(moths=3)),
    ('beats right: the other moth', 43, Beats(R, 28, 12), None, None,
     dict(moths=4)),
    ('down onto the street', 38, R | D, 'street', None),
    ('perched on the street', 20, 0, 'street',
     'dreadcastle-over-the-canal.png'),
    ('Down and Fire: Oscar', 1, D | F, None, None, dict(form=V,
     event='to vampire')),
    ('the smoke', 14, 0, None, None),
    ('he walks into the watchman: a hit', 4, R, None, None, dict(event='hit')),
    ('blinking: he waits', 75, 0, None, None),
    ('he walks into the watchman: a hit', 40, R, None, None,
     dict(event='hit')),
    ('blinking: he waits', 75, 0, None, None),
    ('he walks into the watchman: a hit', 76, R, None, None,
     dict(event='hit')),
    ('blinking: he waits', 75, 0, None, None),
    ('he walks into the watchman: a hit', 43, L, None, None,
     dict(event='hit')),
    ('no health left: back at the lantern', 50, 0, 'street', None),
    ('rest at the lantern, the health full again', 20, 0, 'street',
     None),
    ('walk right, to the canal (2)', 325, R, 'street', None),
    ('let go at its edge (2)', 16, 0, 'street', None),
    ('Up and Fire: the bat (2)', 1, U | F, 'street', None, dict(form=B,
     event='to bat')),
    ('the smoke (2)', 12, U | F, 'street', None),
    ('beats: up (2)', 90, Beats(0, 12), None, None),
    ('beats right over the canal (2)', 75, Beats(R, 28), None, None),
    ('glide right, down onto the street', 69, R, 'street', None),
    ('Down and Fire: Oscar', 1, D | F, 'street', None, dict(form=V,
     event='to vampire')),
    ('the smoke', 14, 0, 'street', None),
    ('the watchman walks into him: a hit', 4, 0, None, None,
     dict(event='hit')),
    ('thrown back, he lands', 12, 0, 'street', None),
    ('blinking, he walks past the watchman into the well', 106, R, 'street',
     None),
    ('jump up onto the well: Up held 13 frames', 13, R | U, None, None),
    ('jump up onto the well: onto the solid block', 13, R, 'solid block',
     None),
    ('walk right, off the well', 36, R, 'street', None),
    ('walk right past the shut gate, to the end', 118, R, 'street', None),
    ('rest at the end of the level', 20, 0, 'street',
     'dreadcastle-gate-shut.png'),
    ('walk back left into the well', 134, L, 'street', None,
     dict(event='blocked left')),
    ('jump up onto the well: Up held 13 frames', 13, L | U, None, None),
    ('jump up onto the well: onto the solid block', 13, L, 'solid block',
     None),
    ('let go', 10, 0, 'solid block', None),
    ('jump up through the balcony: Up held 1 frames', 1, U, None, None),
    ('jump up through the balcony: onto the balcony C', 15, 0, 'balcony C',
     None),
    ('walk left on the balcony, under the medallion', 85, L, 'balcony C',
     None),
    ('let go', 16, 0, 'balcony C', None),
    ('a jump: the medallion', 2, U, None, None, dict(got=3,
     event='gate open')),
    ('he lands on the balcony', 22, 0, 'balcony C', None),
    ('walk right along the balcony, down to the street', 134, R, 'street',
     None),
    ('walk right to the gate', 26, R, 'street', None),
    ('let go', 16, 0, 'street', None),
    ('the gate is open', 25, 0, 'street', 'dreadcastle-gate-open.png'),
    ('through the gate', 11, R, None, None, dict(event='through the gate')),
    # LEVEL CLEAR: the night left into the score.
    ('LEVEL CLEAR, the night counted', 55, 0, None,
     'dreadcastle-clear.png'),
    ('the rest of the night into the score', Until(
        lambda m: m.trans > 0, 400, "the transition"), 0,
     None, None, dict(event='next')),
    ('the next level: the churchyard', NEXT_LEVEL, 0, 'street', None),
    ('at the start of the churchyard: nothing taken', 35, 0, 'street',
     'dreadcastle-churchyard.png', dict(got=0, moths=0)),
    ('walk right, to the tombstones (1)', 113, R, 'street', None),
    ('let go', 16, 0, 'street', None),
    ('a run and a jump onto the tombstone: on', 26, R, None, None),
    ('a run and a jump onto the tombstone: Up held 27 frames', 27, R | U, None,
     None),
    ('a run and a jump onto the tombstone: onto the solid block', 15, R,
     'solid block', None),
    ('a run and a jump onto the second tombstone: Up held 23 frames', 23,
     R | U, None, None),
    ('a run and a jump onto the second tombstone: onto the solid block', 20, R,
     'solid block', None),
    ('a run and a jump onto the third tombstone: Up held 23 frames', 23, R | U,
     None, None),
    ('a run and a jump onto the third tombstone: onto the solid block', 20, R,
     'solid block', None),
    ('walk right, off it, into the first grave', 44, R, None, None,
     dict(event='fallen')),
    ('Oscar falls: back at the start of the churchyard', 50, 0, 'street',
     None),
    ('walk right, to the tombstones (2)', 113, R, 'street', None),
    ('let go', 16, 0, 'street', None),
    ('the tombstones, and the cat: wait', 24, 0, None, None),
    ('a run and a jump onto the tombstone: on', 26, R, None, None),
    ('a run and a jump onto the tombstone: Up held 27 frames', 27, R | U, None,
     None),
    ('a run and a jump onto the tombstone: onto the solid block', 15, R,
     'solid block', None),
    ('a run and a jump onto the second tombstone: Up held 23 frames', 23,
     R | U, None, None),
    ('a run and a jump onto the second tombstone: onto the solid block', 20, R,
     'solid block', None),
    ('a run and a jump onto the third tombstone: Up held 23 frames', 23, R | U,
     None, None),
    ('a run and a jump onto the third tombstone: onto the solid block', 20, R,
     'solid block', None),
    ('walk right, off it, to the grave', 19, R, 'street', None),
    ('a jump over the grave: Up held 14 frames', 14, R | U, None, None),
    ('a jump over the grave: onto the street', 22, R, 'street', None),
    ('walk right to the second grave', 30, R, 'street', None),
    ('a jump over the grave onto the family tomb: Up held 20 frames', 20,
     R | U, None, None),
    ('a jump over the grave onto the family tomb: onto the solid block', 12, R,
     'solid block', None),
    ('walk right on the tomb: the candelabrum', 19, R, 'solid block', None,
     dict(got=1, event='heirloom 0')),
    ('let go on the tomb', 16, 0, 'solid block', None),
    ('rest on the family tomb', 12, 0, 'solid block',
     'dreadcastle-candelabrum.png'),
    ('walk right, off the tomb', 41, R, 'street', None),
    ('a jump over the watchman: wait', 40, 0, None, None),
    ('a jump over the watchman: on', 36, R, None, None),
    ('a jump over the watchman: Up held 26 frames', 26, R | U, None, None),
    ('a jump over the watchman: over it, onto the street', 19, R, 'street',
     None),
    ('a jump over the watchman: on, away from it', 30, R, None, None),
    ('walk right to the tombstones', 22, R, 'street', None),
    ('a jump onto the tombstones: Up held 1 frames', 1, R | U, None, None),
    ('a jump onto the tombstones: onto the solid block', 15, R, 'solid block',
     None),
    ('walk right to their end', 15, R, 'solid block', None),
    ('let go at the edge of the landslide', 16, 0, 'solid block', None),
    ('Up and Fire: the bat', 1, U | F, 'solid block', None, dict(form=B,
     event='to bat')),
    ('the smoke', 12, U | F, 'solid block', None),
    ('beats: up', 77, Beats(0, 12), None, None),
    ('beats right over the landslide: a moth', 31, Beats(R, 28), None, None,
     dict(moths=1)),
    ('beats right, past the landslide', 71, Beats(R, 28), None, None),
    ('down onto the street', 37, D, 'street', None),
    ('Down and Fire: Oscar', 1, D | F, 'street', None, dict(form=V,
     event='to vampire')),
    ('the smoke', 14, 0, 'street', None),
    ('walk right to the lantern: it lights up', 32, R, 'street', None,
     dict(event='lantern')),
    ('walk right into the sarcophagus', 43, R, 'street', None),
    ('a jump onto the sarcophagus: Up held 10 frames', 10, R | U, None, None),
    ('a jump onto the sarcophagus: onto the solid block', 12, R, 'solid block',
     None),
    ('let go', 10, 0, 'solid block', None),
    ('a jump onto the chapel: Up held 13 frames', 13, R | U, None, None),
    ('a jump onto the chapel: onto the solid block', 18, R, 'solid block',
     None),
    ('walk right on the chapel, by the bell-cote', 16, R, 'solid block', None),
    ('let go', 16, 0, 'solid block', None),
    ('Up and Fire: the bat, on the chapel', 1, U | F, 'solid block', None,
     dict(form=B, event='to bat')),
    ('the smoke', 12, U | F, 'solid block', None),
    ('perched on the chapel: the hourglass above', 24, 0, 'solid block',
     'dreadcastle-chapel.png', dict(form=B)),
    ('beats up: a moth', 39, Beats(0, 12), None, None, dict(moths=2)),
    ('beats right, up: the hourglass', 26, Beats(R, 10), None, None,
     dict(got=2)),
    ('glide right, past the chapel', 79, R, None, None),
    ('a dive to the street', 14, D, 'street', None),
    ('Down and Fire: Oscar', 1, D | F, 'street', None, dict(form=V,
     event='to vampire')),
    ('the smoke', 14, 0, 'street', None),
    ('walk right to the stream', 81, R, 'street', None),
    ('a jump onto the first pile: on', 3, R, None, None),
    ('a jump onto the first pile: Up held 10 frames', 10, R | U, None, None),
    ('a jump onto the first pile: onto the pile 1', 22, R, 'pile 1', None),
    ('let go on the pile', 16, 0, 'pile 1', None),
    ('on the broken bridge', 15, 0, 'pile 1', 'dreadcastle-bridge.png'),
    ('a jump onto the second pile: Up held 27 frames', 27, R | U, None, None),
    ('a jump onto the second pile: onto the pile 2', 19, R, 'pile 2', None),
    ('let go', 16, 0, 'pile 2', None),
    ('a jump onto the far bank: on', 24, R, None, None),
    ('a jump onto the far bank: Up held 1 frames', 1, R | U, None, None),
    ('a jump onto the far bank: onto the street', 22, R, 'street', None),
    ('walk right, under the angel', 13, R, 'street', None),
    ('let go', 16, 0, 'street', None),
    ('a jump onto the pedestal: Up held 8 frames', 8, R | U, None, None),
    ('a jump onto the pedestal: onto the pedestal', 8, R, 'pedestal', None),
    ('let go', 11, 0, 'pedestal', None),
    ('a jump onto the wall: Up held 12 frames', 12, R | U, None, None),
    ('a jump onto the wall: onto the wall', 13, R, 'wall', None),
    ('let go on the wall', 16, 0, 'wall', None),
    ('Up and Fire: the bat, on the wall', 1, U | F, 'wall', None, dict(form=B,
     event='to bat')),
    ('the smoke', 12, U | F, 'wall', None),
    ("beats: up to the top, over the cat's jumps", 65, Beats(0, 10), None,
     None),
    ('beats right, over the book: the camera on', 98, Beats(R, 16), None,
     None),
    ('beats left, back over the book', 56, Beats(L, 20), None, None),
    ('glide down onto the wall, left of the book', 50, 0, 'wall', None),
    ('Down and Fire: Oscar', 1, D | F, 'wall', None, dict(form=V,
     event='to vampire')),
    ('the smoke', 14, 0, 'wall', None),
    ('walk right on the wall: the book', 22, R, 'wall', None, dict(got=3,
     event='gate open')),
    ('walk on: the doors open, one a frame, at the edge', 6, R, 'wall', None),
    ('walk on: the open gate comes onto the screen', 42, R, 'wall', None),
    ('let go on the wall', 16, 0, 'wall', None),
    ('on the wall: the gate is open', 20, 0, 'wall', 'dreadcastle-wall.png'),
    ('walk right, off the wall, through the gate', 75, R, None, None,
     dict(event='through the gate')),
    ('LEVEL CLEAR: the night into the score', Until(
        lambda m: m.trans > 0, 400, "the transition"), 0,
     None, None, dict(event='next')),
    ('the next level: the wild wood', NEXT_LEVEL, 0, 'street', None),
    ('at the edge of the wood: the staff on the path', 34, 0, 'street',
     'dreadcastle-wood.png', dict(got=0, moths=0)),
    ('Fire: no staff yet, no blow', 6, F, 'street', None),
    ('a run and a jump over the staff, onto the trunk: on', 50, R, None, None),
    ('a run and a jump over the staff, onto the trunk: Up held 27 frames', 27,
     R | U, None, None),
    ('a run and a jump over the staff, onto the trunk: onto the solid block',
     15, R, 'solid block', None),
    ('walk on right: the camera moves, the staff lying with the level', 39, R,
     'street', None),
    ('let go (camera)', 10, 0, 'street', None),
    ('walk back left into the trunk', 23, L, 'street', None),
    ('a jump back onto the trunk: Up held 3 frames', 3, L | U, None, None),
    ('a jump back onto the trunk: onto the solid block', 17, L, 'solid block',
     None),
    ('walk back left, off the trunk, to the staff: he takes it', 40, L,
     'street', None, dict(event='staff')),
    ('let go', 10, 0, 'street', None),
    ("the Count's staff in his hand", 26, 0, 'street',
     'dreadcastle-staff.png'),
    ('Fire: a blow', 1, F, 'street', None, dict(event='blow')),
    ('Up in the blow: no jump', 6, U, 'street', None),
    ('let go: the blow ends', 4, 0, 'street', None),
    ('Fire and Right held: one blow, still while it lasts, then he walks', 16,
     R | F, 'street', None),
    ('let go (staff)', 4, 0, 'street', None),
    ('walk right into the fallen trunk', 21, R, 'street', None),
    ('a jump onto the trunk: Up held 1 frames', 1, R | U, None, None),
    ('a jump onto the trunk: onto the solid block', 15, R, 'solid block',
     None),
    ('let go on the trunk', 10, 0, 'solid block', None),
    ('walk right, off the trunk', 40, R, 'street', None),
    ('a jump over the toad: wait', 36, 0, None, None),
    ('a jump over the toad: on', 38, R, None, None),
    ('a jump over the toad: Up held 28 frames', 28, R | U, None, None),
    ('a jump over the toad: over it, onto the street', 18, R, 'street', None),
    ('a jump over the toad: on, away from it', 4, R, None, None),
    ('let go past it', 16, 0, 'street', None),
    ('Left: he turns; the toad jumps at him: a blow: on', 12, L, None, None),
    ('Left: he turns; the toad jumps at him: a blow: wait', 26, 0, None, None),
    ('Left: he turns; the toad jumps at him: a blow: Fire, the blow', 1, F,
     None, None, dict(event='blow')),
    ('Left: he turns; the toad jumps at him: a blow: struck', 5, 0, None, None,
     dict(event='struck')),
    ('its puff, then nothing', 12, 0, None, None),
    ('walk right into the stump', 56, R, 'street', None),
    ('a jump onto the stump: Up held 10 frames', 10, R | U, None, None),
    ('a jump onto the stump: onto the solid block', 12, R, 'solid block',
     None),
    ('walk right, off the stump: the chalice', 75, R, None, None,
     dict(event='heirloom 0', got=1)),
    ('let go in the clearing', 16, 0, 'street', None),
    ('a jump over the scout: wait', 24, 0, None, None),
    ('a jump over the scout: on', 36, R, None, None),
    ('a jump over the scout: Up held 26 frames', 26, R | U, None, None),
    ('a jump over the scout: over it, onto the street', 19, R, 'street', None),
    ('a jump over the scout: on, away from it', 10, R, None, None),
    ('let go past him', 16, 0, 'street', None),
    ('Left: he turns; the scout comes back: a blow: on', 1, L, None, None),
    ('Left: he turns; the scout comes back: a blow: wait', 126, 0, None, None),
    ('Left: he turns; the scout comes back: a blow: Fire, the blow', 1, F,
     None, None, dict(event='blow')),
    ('Left: he turns; the scout comes back: a blow: struck', 6, 0, None, None,
     dict(event='struck')),
    ("the scout's puff, then nothing", 12, 0, None, None),
    ('walk right into the stump', 69, R, 'street', None),
    ('a jump onto the stump: Up held 1 frames', 1, R | U, None, None),
    ('a jump onto the stump: onto the solid block', 15, R, 'solid block',
     None),
    ('let go on it', 10, 0, 'solid block', None),
    ('right: the other scout walks into him, a hit', 81, R, None, None,
     dict(event='hit')),
    ('thrown back, he lands', 12, 0, None, None),
    ('blinking, he waits', 63, 0, None, None),
    ('the scout comes: a blow: wait', 50, 0, None, None),
    ('the scout comes: a blow: Fire, the blow', 1, F, None, None,
     dict(event='blow')),
    ('the scout comes: a blow: struck', 6, 0, None, None,
     dict(event='struck')),
    ('its puff, then nothing', 12, 0, None, None),
    ('walk right into the brambles: thrown back', 67, R, None, None,
     dict(event='brambles')),
    ('thrown back, he lands', 12, 0, 'street', None),
    ('blinking by the brambles', 15, 0, 'street', 'dreadcastle-brambles.png'),
    ('blinking: he waits', 48, 0, 'street', None),
    ('a run and a jump over the brambles: on', 12, R, None, None),
    ('a run and a jump over the brambles: Up held 26 frames', 26, R | U, None,
     None),
    ('a run and a jump over the brambles: onto the street', 19, R, 'street',
     None),
    ('let go between the brambles', 16, 0, 'street', None),
    ('a jump over the other brambles: on', 22, R, None, None),
    ('a jump over the other brambles: Up held 27 frames', 27, R | U, None,
     None),
    ('a jump over the other brambles: onto the street', 18, R, 'street', None),
    ('walk right to the lantern: it lights up', 15, R, 'street', None,
     dict(event='lantern')),
    ('let go', 16, 0, 'street', None),
    ('walk right into the stump by the oak', 68, R, 'street', None),
    ('a jump onto the stump (3): Up held 10 frames', 10, R | U, None, None),
    ('a jump onto the stump (3): onto the solid block', 12, R, 'solid block',
     None),
    ('let go on the stump', 10, 0, 'solid block', None),
    ('a run and a jump onto the low branch: wait', 20, 0, None, None),
    ('a run and a jump onto the low branch: on', 14, R, None, None),
    ('a run and a jump onto the low branch: Up held 29 frames', 29, R | U,
     None, None),
    ('a run and a jump onto the low branch: onto the low branch', 9, R,
     'low branch', None),
    ('let go on the low branch', 16, 0, 'low branch', None),
    ('the owl: a jump and a blow: Up held 1 frames', 1, U, None, None),
    ('the owl: a jump and a blow: Fire, the blow', 1, F, None, None,
     dict(event='blow')),
    ('the owl: a jump and a blow: struck', 3, 0, None, None,
     dict(event='struck')),
    ('the owl: a jump and a blow: he lands', 18, 0, 'low branch', None),
    ('on the low branch of the great oak', 18, 0, 'low branch',
     'dreadcastle-oak.png'),
    ('Fire: a blow', 2, F, 'low branch', None, dict(event='blow')),
    ('Up, Fire held: the bat (the blow cut short)', 1, U | F, 'low branch',
     None, dict(form=B, event='to bat')),
    ('the smoke', 12, U | F, 'low branch', None),
    ('beats up and right: the portrait', 118, Beats(R, 12), None, None,
     dict(got=2)),
    ('glide right, to the river', 47, R, None, None),
    ('a dive to the street', 25, D, 'street', None),
    ('Down and Fire: Oscar', 1, D | F, 'street', None, dict(form=V,
     event='to vampire')),
    ('the smoke', 14, 0, 'street', None),
    ('walk right to the river', 21, R, 'street', None),
    ('let go at the bank', 14, 0, 'street', None),
    ('a jump onto stone 1: on', 2, R, None, None),
    ('a jump onto stone 1: Up held 27 frames', 27, R | U, None, None),
    ('a jump onto stone 1: onto the stone 1', 14, R, 'stone 1', None),
    ('a jump onto stone 1: let go', 16, 0, 'stone 1', None),
    ('a jump onto stone 2: Up held 15 frames', 15, R | U, None, None),
    ('a jump onto stone 2: onto the stone 2', 22, R, 'stone 2', None),
    ('a jump onto stone 2: let go', 16, 0, 'stone 2', None),
    ('a jump onto stone 3: Up held 13 frames', 13, R | U, None, None),
    ('a jump onto stone 3: onto the stone 3', 22, R, 'stone 3', None),
    ('a jump onto stone 3: let go', 16, 0, 'stone 3', None),
    ('on a stone in the river', 22, 0, 'stone 3', 'dreadcastle-river.png'),
    ('a jump onto stone 4: Up held 15 frames', 15, R | U, None, None),
    ('a jump onto stone 4: onto the stone 4', 22, R, 'stone 4', None),
    ('a jump onto stone 4: let go', 16, 0, 'stone 4', None),
    ('a jump onto stone 5: wait', 8, 0, None, None),
    ('a jump onto stone 5: Up held 13 frames', 13, R | U, None, None),
    ('a jump onto stone 5: onto the stone 5', 22, R, 'stone 5', None),
    ('a jump onto stone 5: let go', 16, 0, 'stone 5', None),
    ('a jump onto the far bank: Up held 11 frames', 11, R | U, None, None),
    ('a jump onto the far bank: onto the street', 26, R, 'street', None),
    ('a jump onto the far bank: let go', 16, 0, 'street', None),
    ('the toad under the oak: a blow: wait', 72, 0, None, None),
    ('the toad under the oak: a blow: Fire, the blow', 1, F, None, None,
     dict(event='blow')),
    ('the toad under the oak: a blow: struck', 6, 0, None, None,
     dict(event='struck')),
    ('its puff, then nothing (2)', 12, 0, None, None),
    ('walk right, under the hollow oak', 62, R, 'street', None),
    ('let go under the oak', 16, 0, 'street', None),
    ('a jump: his head on the oak', 11, U, None, None, dict(event='head')),
    ('he lands', 13, 0, 'street', None),
    ('Up and Fire: the bat, under the oak', 1, U | F, 'street', None,
     dict(form=B, event='to bat')),
    ('the smoke (3)', 12, U | F, 'street', None),
    ('a beat: up against the oak', 50, Beats(0, 12), None, None,
     dict(event='head')),
    ('Down and Fire: no room for Oscar', 1, D | F, None, None, dict(form=B,
     event='refused')),
    ('the bat glides down to the street', 32, 0, 'street', None),
    ('Down and Fire: Oscar (room now)', 1, D | F, 'street', None, dict(form=V,
     event='to vampire')),
    ('the smoke (4)', 14, 0, 'street', None),
    ('walk right into the roots', 42, R, 'street', None),
    ('a jump onto the roots: Up held 1 frames', 1, R | U, None, None),
    ('a jump onto the roots: onto the solid block', 15, R, 'solid block',
     None),
    ('let go on the roots', 10, 0, 'solid block', None),
    ('a jump onto the high roots: on', 4, R, None, None),
    ('a jump onto the high roots: Up held 14 frames', 14, R | U, None, None),
    ('a jump onto the high roots: onto the solid block', 13, R, 'solid block',
     None),
    ('let go on the high roots', 16, 0, 'solid block', None),
    ('a jump up left, onto the oak: on', 4, L, None, None),
    ('a jump up left, onto the oak: Up held 28 frames', 28, L | U, None, None),
    ('a jump up left, onto the oak: onto the solid block', 10, L,
     'solid block', None),
    ('walk left on the oak: the medallion', 50, L, 'solid block', None,
     dict(got=3, event='gate open')),
    ('let go on the oak', 16, 0, 'solid block', None),
    ('on the hollow oak: the gap in the hedge open', 22, 0, 'solid block',
     'dreadcastle-hollow-oak.png'),
    ('walk right on the oak', 57, R, 'solid block', None),
    ('a jump right, onto the high roots: Up held 5 frames', 5, R | U, None,
     None),
    ('a jump right, onto the high roots: onto the solid block', 30, R,
     'solid block', None),
    ('walk right, off the roots, through the gap', 42, R, None, None,
     dict(event='through the gate')),
    ('LEVEL CLEAR: the night into the score', Until(
        lambda m: m.trans > 0, 400, "the transition"), 0,
     None, None, dict(event='next')),
    ('the next level: the black mire', NEXT_LEVEL, 0, 'street', None),
    ('at the edge of the mire', 31, 0, 'street', 'dreadcastle-mire.png',
     dict(got=0, moths=0)),
    ('walk right to the water', 30, R, 'street', None),
    ('let go at the water', 16, 0, 'street', None),
    ('a jump onto clod 8: on', 2, R, None, None),
    ('a jump onto clod 8: Up held 25 frames', 25, R | U, None, None),
    ('a jump onto clod 8: on, in the air', 15, R, None, None),
    ('a jump onto clod 8: onto the clod 8', 16, 0, 'clod 8', None),
    ('a jump onto clod 11: on', 2, R, None, None),
    ('a jump onto clod 11: Up held 16 frames', 16, R | U, None, None),
    ('a jump onto clod 11: on, in the air', 18, R, None, None),
    ('a jump onto clod 11: onto the clod 11', 16, 0, 'clod 11', None),
    ('a jump onto clod 14: wait', 20, 0, None, None),
    ('a jump onto clod 14: on', 12, R, None, None),
    ('a jump onto clod 14: Up held 7 frames', 7, R | U, None, None),
    ('a jump onto clod 14: on, in the air', 18, R, None, None),
    ('a jump onto clod 14: onto the clod 14', 16, 0, 'clod 14', None),
    ('a jump onto the big clod: wait', 20, 0, None, None),
    ('a jump onto the big clod: on', 4, R, None, None),
    ('a jump onto the big clod: Up held 13 frames', 13, R | U, None, None),
    ('a jump onto the big clod: on, in the air', 24, R, None, None),
    ('a jump onto the big clod: onto the clod 17', 16, 0, 'clod 17', None,
     dict(event='heirloom 0', got=1)),
    ('on the big clod, the candelabrum taken', 14, 0, 'clod 17',
     'dreadcastle-clods.png'),
    ('the owl: a jump and a blow: Right', 1, R, 'clod 17', None),
    ('the owl: a jump and a blow: wait', 436, 0, 'clod 17', None),
    ('the owl: a jump and a blow: Up held 12 frames', 12, U, None, None),
    ('the owl: a jump and a blow: up', 1, 0, None, None),
    ('the owl: a jump and a blow: Fire, the blow', 1, F, None, None,
     dict(event='blow')),
    ('the owl: a jump and a blow: struck, he lands', 20, 0, 'clod 17', None,
     dict(event='struck')),
    ('a jump onto clod 21: on', 4, R, None, None),
    ('a jump onto clod 21: Up held 19 frames', 19, R | U, None, None),
    ('a jump onto clod 21: on, in the air', 18, R, None, None),
    ('a jump onto clod 21: onto the clod 21', 16, 0, 'clod 21', None),
    ('a jump onto clod 24: on', 2, R, None, None),
    ('a jump onto clod 24: Up held 16 frames', 16, R | U, None, None),
    ('a jump onto clod 24: on, in the air', 18, R, None, None),
    ('a jump onto clod 24: onto the clod 24', 16, 0, 'clod 24', None),
    ('a jump onto clod 27: on', 2, R, None, None),
    ('a jump onto clod 27: Up held 16 frames', 16, R | U, None, None),
    ('a jump onto clod 27: on, in the air', 18, R, None, None),
    ('a jump onto clod 27: onto the clod 27', 16, 0, 'clod 27', None),
    ('a jump onto clod 30: on', 4, R, None, None),
    ('a jump onto clod 30: Up held 13 frames', 13, R | U, None, None),
    ('a jump onto clod 30: on, in the air', 24, R, None, None),
    ('a jump onto clod 30: onto the clod 30', 16, 0, 'clod 30', None),
    ('a jump onto clod 34: on', 2, R, None, None),
    ('a jump onto clod 34: Up held 22 frames', 22, R | U, None, None),
    ('a jump onto clod 34: on, in the air', 18, R, None, None),
    ('a jump onto clod 34: onto the clod 34', 16, 0, 'clod 34', None),
    ('the toad on the shore: a jump at it: Up held', 20, R | U, None, None),
    ('the toad on the shore: a jump at it: on, in the air', 2, R, None, None),
    ('the toad on the shore: a jump at it: Fire, the blow', 1, R | F, None,
     None, dict(event='blow')),
    ('the toad on the shore: a jump at it: on, in the air', 9, R, None, None),
    ('the toad on the shore: a jump at it: he lands', 16, 0, 'street', None),
    ('walk right into the dead trunk', 103, R, 'street', None),
    ('a jump onto the dead trunk: on', 4, R, None, None),
    ('a jump onto the dead trunk: Up held 13 frames', 13, R | U, None, None),
    ('a jump onto the dead trunk: on, in the air', 6, R, None, None),
    ('a jump onto the dead trunk: onto the solid block', 8, 0, 'solid block',
     None),
    ('let go on the trunk', 10, 0, 'solid block', None),
    ('walk right, off the trunk, under the walkway, into the next trunk', 148,
     R, 'street', None),
    ('a jump onto the second trunk: on', 4, R, None, None),
    ('a jump onto the second trunk: Up held 13 frames', 13, R | U, None, None),
    ('a jump onto the second trunk: on, in the air', 6, R, None, None),
    ('a jump onto the second trunk: onto the solid block', 8, 0,
     'solid block', None),
    ('let go on it', 10, 0, 'solid block', None),
    ('walk right, off the trunk, to the lantern: it lights up', 69, R,
     'street', None, dict(event='lantern')),
    ('let go by the lantern', 16, 0, 'street', None),
    ('walk right into the wisps: thrown back', 41, R, None, None,
     dict(event='wisps')),
    ('thrown back, he lands', 14, 0, 'street', None),
    ('blinking by the wisps', 10, 0, 'street', None),
    ('blinking: he waits', 40, 0, 'street', None),
    ('a jump onto the boardwalk: Up held 10 frames', 10, R | U, None, None),
    ('a jump onto the boardwalk: onto the boardwalk 1', 11, 0, 'boardwalk 1',
     None),
    ('a jump up onto the boardwalk over the wisps: Up held 1 frames', 1,
     R | U, None, None),
    ('a jump up onto the boardwalk over the wisps: on, in the air', 9, R,
     None, None),
    ('a jump up onto the boardwalk over the wisps: onto the boardwalk 2', 7,
     0, 'boardwalk 2', None),
    ('walk right on the boardwalk, over the wisps', 40, R, 'boardwalk 2',
     None),
    ('let go over the wisps', 16, 0, 'boardwalk 2', None),
    ('on the boardwalk over the wisps', 12, 0, 'boardwalk 2',
     'dreadcastle-wisps.png'),
    ('walk right, down onto the step at its end', 71, R, 'boardwalk 3', None),
    ('let go on the step', 12, 0, 'boardwalk 3', None),
    ('a jump onto the fallen log: on', 2, R, None, None),
    ('a jump onto the fallen log: Up held 1 frames', 1, R | U, None, None),
    ('a jump onto the fallen log: on, in the air', 12, R, None, None),
    ('a jump onto the fallen log: onto the solid block', 14, 0, 'solid block',
     None),
    ('let go on the log', 12, 0, 'solid block', None),
    ('walk right on the log, under the hourglass', 23, R, 'solid block', None),
    ('let go under the hourglass', 12, 0, 'solid block', None),
    ('on the log, under the great dead tree', 17, 0, 'solid block',
     'dreadcastle-dead-tree.png'),
    ('Up and Fire: the bat', 1, U | F, 'solid block', None,
     dict(form=B, event='to bat')),
    ('the smoke', 12, U | F, 'solid block', None),
    ('beats straight up: the hourglass', 73, Beats(0, 10), None, None,
     dict(got=2)),
    ('glide right', 20, R, None, None),
    ('a dive to the street', 36, D, 'street', None),
    ('Down and Fire: Oscar', 1, D | F, 'street', None,
     dict(form=V, event='to vampire')),
    ('the smoke', 14, 0, 'street', None),
    ('walk right into the bank', 112, R, 'street', None),
    ('a jump onto the bank: Up held 4 frames', 4, R | U, None, None),
    ('a jump onto the bank: on, in the air', 9, R, None, None),
    ('a jump onto the bank: onto the solid block', 9, 0, 'solid block', None),
    ('let go on the bank', 10, 0, 'solid block', None),
    ('the scout on the bank: Right', 1, R, 'solid block', None),
    ('the scout on the bank: wait', 220, 0, 'solid block', None),
    ('the scout on the bank: Fire, the blow', 1, F, 'solid block', None,
     dict(event='blow')),
    ('the scout on the bank: struck', 11, 0, 'solid block', None,
     dict(event='struck')),
    ('walk right on the bank', 110, R, 'solid block', None),
    ('the toad on the bank: a jump and a blow: Right', 1, R, 'solid block',
     None),
    ('the toad on the bank: a jump and a blow: wait', 44, 0, 'solid block',
     None),
    ('the toad on the bank: a jump and a blow: Up held 6 frames', 6, U, None,
     None),
    ('the toad on the bank: a jump and a blow: up', 8, 0, None, None),
    ('the toad on the bank: a jump and a blow: Fire, the blow', 1, F, None,
     None, dict(event='blow')),
    ('the toad on the bank: a jump and a blow: struck, he lands', 13, 0,
     'solid block', None, dict(event='struck')),
    ('walk right, off the bank, under the fallen tree', 214, R, 'street',
     None),
    ('let go by the boulder', 12, 0, 'street', None),
    ('a jump onto the boulder: on', 4, R, None, None),
    ('a jump onto the boulder: Up held 13 frames', 13, R | U, None, None),
    ('a jump onto the boulder: on, in the air', 6, R, None, None),
    ('a jump onto the boulder: onto the solid block', 8, 0, 'solid block',
     None),
    ('let go on the boulder', 12, 0, 'solid block', None),
    ('a jump up left, onto the fallen tree: on', 2, L, None, None),
    ('a jump up left, onto the fallen tree: Up held 13 frames', 13, L | U,
     None, None),
    ('a jump up left, onto the fallen tree: on, in the air', 3, L, None, None),
    ('a jump up left, onto the fallen tree: onto the solid block', 12, 0,
     'solid block', None),
    ('let go on the fallen tree', 12, 0, 'solid block', None),
    ('walk left on the fallen tree', 44, L, 'solid block', None),
    ('a jump: the book', 1, U, None, None),
    ('a jump: the book: he lands', 22, 0, 'solid block', None,
     dict(got=3, event='gate open')),
    ('let go on the fallen tree', 16, 0, 'solid block', None),
    ('on the fallen tree: the way out open', 33, 0, 'solid block',
     'dreadcastle-fallen-tree.png'),
    ('a jump right, down onto the boulder: on', 12, R, None, None),
    ('a jump right, down onto the boulder: Up held 25 frames', 25, R | U,
     None, None),
    ('a jump right, down onto the boulder: on, in the air', 21, R, None, None),
    ('a jump right, down onto the boulder: onto the solid block', 16, 0,
     'solid block', None),
    ('walk right, off the boulder, through the way out', 64, R, None, None,
     dict(event='through the gate')),
    ('LEVEL CLEAR: the night into the score', Until(
        lambda m: m.trans > 0, 400, "the transition"), 0,
     None, None, dict(event='next')),
    ('the next level: the grey crags', NEXT_LEVEL, 0, 'street', None),
    ('at the foot of the crags', 43, 0, 'street', 'dreadcastle-crags.png',
     dict(got=0, moths=0)),
    ('walk right into the low ledge', 67, R, 'street', None,
     dict(event='blocked right')),
    ('a jump onto the low ledge: Up held 13 frames', 13, R | U, None, None),
    ('a jump onto the low ledge: on, in the air', 12, R, None, None),
    ('on the ledge, the goat walks into him: a hit', 38, 0, None, None,
     dict(event='hit')),
    ('thrown back', 9, 0, None, None),
    ('blinking, then he waits for the goat to go right', 53, 0, 'street',
     None),
    ('a jump onto the low ledge again: Up held 13 frames', 13, R | U, None,
     None),
    ('a jump onto the low ledge again: on, in the air', 12, R, 'solid block',
     None),
    ('walk right on the ledge behind the goat', 42, R, 'solid block', None),
    ('the goat: Fire, the blow', 1, F, 'solid block', None,
     dict(event='blow')),
    ('the goat struck', 20, 0, 'solid block', None, dict(event='struck')),
    ('a jump onto the boulder: on', 12, R, None, None),
    ('a jump onto the boulder: Up held 25 frames', 25, R | U, None, None),
    ('a jump onto the boulder: on, in the air', 9, R, None, None),
    ('a jump onto the boulder: onto the boulder', 16, 0, 'boulder', None),
    ('let go on the boulder', 10, 0, 'boulder', None),
    ('a jump onto the high ledge: on', 12, R, None, None),
    ('a jump onto the high ledge: Up held 28 frames', 28, R | U, None, None),
    ('a jump onto the high ledge: onto the solid block', 16, 0, 'solid block',
     None),
    ('let go on the high ledge', 10, 0, 'solid block', None),
    ('walk right on the high ledge: the chalice', 53, R, 'solid block', None,
     dict(event='heirloom 0', got=1)),
    ('let go on the high ledge', 16, 0, 'solid block', None),
    ('on the high ledge, the chalice taken', 17, 0, 'solid block',
     'dreadcastle-high-ledge.png'),
    ('walk right, off the high ledge, into the rock', 101, R, 'street', None),
    ('a jump onto the rock: on', 4, R, None, None),
    ('a jump onto the rock: Up held 13 frames', 13, R | U, None, None),
    ('a jump onto the rock: on, in the air', 6, R, None, None),
    ('a jump onto the rock: onto the solid block', 8, 0, 'solid block', None),
    ('walk right on the rock', 22, R, 'solid block', None),
    ('on the rock: the werewolf jumps at him', 80, 0, 'solid block', None),
    ('a leap over the werewolf: Up held 28 frames', 28, R | U, None, None),
    ('a leap over the werewolf: on, in the air', 20, R, None, None),
    ('a leap over the werewolf: onto the street', 16, 0, 'street', None),
    ('run right, away from the werewolf, to the crevasse', 78, R, 'street',
     None),
    ('let go at the edge of the crevasse', 16, 0, 'street', None),
    ('a jump onto the first stone: on', 21, R, None, None),
    ('a jump onto the first stone: Up held 22 frames', 22, R | U, None, None),
    ('a jump onto the first stone: on, in the air', 8, R, None, None),
    ('a jump onto the first stone: onto the solid block', 16, 0,
     'solid block', None),
    ('a jump onto the second stone: on', 4, R, None, None),
    ('a jump onto the second stone: Up held 28 frames', 28, R | U, None, None),
    ('a jump onto the second stone: on, in the air', 4, R, None, None),
    ('a jump onto the second stone: onto the solid block', 16, 0,
     'solid block', None),
    ('on the second stone, under the pinnacle', 20, 0, 'solid block', None),
    ('Up and Fire: the bat', 1, U | F, 'solid block', None,
     dict(form=B, event='to bat')),
    ('the smoke', 12, U | F, 'solid block', None),
    ('beats up and right: the portrait on the pinnacle', 136, Beats(R, 14),
     None, None, dict(got=2)),
    ('beats right, slower: a moth', 60, Beats(R, 30), None, None,
     dict(moths=1)),
    ('glide right', 52, R, None, None),
    ('a dive to the street: the lantern', 12, D, 'street', None,
     dict(event='lantern')),
    ('Down and Fire: Oscar', 1, D | F, 'street', None,
     dict(form=V, event='to vampire')),
    ('the smoke', 14, 0, 'street', None),
    ('by the lantern, the crevasse behind', 13, 0, 'street',
     'dreadcastle-crevasse.png'),
    ('walk right to the goat', 119, R, 'street', None),
    ('the goat: Fire, the blow', 1, F, 'street', None, dict(event='blow')),
    ('the goat struck', 29, 0, 'street', None, dict(event='struck')),
    ('walk right under the crag, to the first crack', 186, R, 'street', None),
    ('let go at the crack', 16, 0, 'street', None),
    ('a jump over the first crack: wait', 75, 0, None, None),
    ('a jump over the first crack: on', 6, R, None, None),
    ('a jump over the first crack: Up held 28 frames', 28, R | U, None, None),
    ('a jump over the first crack: on, in the air', 5, R, None, None),
    ('a jump over the first crack: onto the street', 16, 0, 'street', None),
    ('walk right: the medallion, the way out open', 41, R, 'street', None,
     dict(event='gate open', got=3)),
    ('let go under the crag', 16, 0, 'street', None),
    ('under the crag, the moon behind it', 16, 0, 'street',
     'dreadcastle-under-the-crag.png'),
    ('the goat between the cracks: walk right', 11, R, 'street', None),
    ('the goat: Fire, the blow', 1, F, 'street', None, dict(event='blow')),
    ('the goat struck', 29, 0, 'street', None, dict(event='struck')),
    ('walk right to the second crack', 56, R, 'street', None),
    ('let go at the crack', 16, 0, 'street', None),
    ('a jump over the second crack: on', 6, R, None, None),
    ('a jump over the second crack: Up held 28 frames', 28, R | U, None, None),
    ('a jump over the second crack: on, in the air', 5, R, None, None),
    ('a jump over the second crack: onto the street', 16, 0, 'street', None),
    ('the werewolf by the way out: wait', 21, 0, 'street', None),
    ('the werewolf by the way out: walk right', 52, R, 'street', None),
    ('the werewolf: Fire, the blow', 1, F, 'street', None, dict(event='blow')),
    ('the werewolf struck', 39, 0, 'street', None, dict(event='struck')),
    ('walk right through the mouth of the pass', 114, R, None, None,
     dict(event='through the gate')),
    ('LEVEL CLEAR: the night into the score', Until(
        lambda m: m.trans > 0, 400, "the transition"), 0,
     None, None, dict(event='next')),
    ('the next level: the frozen pass', NEXT_LEVEL, 0, 'street', None),
    ('at the foot of the pass', 42, 0, 'street', 'dreadcastle-pass.png',
     dict(got=0, moths=0)),
    ('walk right to the first mound', 47, R, 'street', None),
    ('let go by the mound', 16, 0, 'street', None),
    ('a jump onto the mound: on', 8, R, None, None),
    ('a jump onto the mound: Up held 16 frames', 16, R | U, None, None),
    ('a jump onto the mound: onto the mound 1', 16, 0, 'mound 1', None),
    ('let go on the mound', 10, 0, 'mound 1', None),
    ('a jump onto the first slab: on', 8, R, None, None),
    ('a jump onto the first slab: Up held 22 frames', 22, R | U, None, None),
    ('a jump onto the first slab: on, in the air', 3, R, None, None),
    ('a jump onto the first slab: onto the solid block', 16, 0, 'solid block',
     None),
    ('let go on the slab', 10, 0, 'solid block', None),
    ('walk right, off the slab, down to the path', 74, R, 'street', None),
    ('let go past the slab', 12, 0, 'street', None),
    ('walk left into the spikes of ice: thrown back', 23, L, None, None,
     dict(event='spikes')),
    ('thrown back, he lands', 22, 0, 'street', None),
    ('blinking by the spikes', 10, 0, 'street', None),
    ('by the spikes of ice, glinting', 31, 0, 'street',
     'dreadcastle-spikes.png'),
    ('the goat on the path: walk right', 32, R, 'street', None),
    ('the goat: Fire, the blow', 1, F, 'street', None, dict(event='blow')),
    ('the goat struck', 29, 0, 'street', None, dict(event='struck')),
    ('walk right: the candelabrum', 17, R, 'street', None,
     dict(event='heirloom 0', got=1)),
    ('walk right to the second mound', 24, R, 'street', None),
    ('let go by the mound', 16, 0, 'street', None),
    ('a jump onto the second mound: on', 4, R, None, None),
    ('a jump onto the second mound: Up held 19 frames', 19, R | U, None, None),
    ('a jump onto the second mound: onto the mound 2', 16, 0, 'mound 2', None),
    ('let go on the mound', 10, 0, 'mound 2', None),
    ('a jump onto the second slab: on', 10, R, None, None),
    ('a jump onto the second slab: Up held 22 frames', 22, R | U, None, None),
    ('a jump onto the second slab: onto the solid block', 16, 0,
     'solid block', None),
    ('let go on the slab', 10, 0, 'solid block', None),
    ('walk right, off the slab, down to the path', 75, R, 'street', None),
    ('let go past the slab', 12, 0, 'street', None),
    ('walk right to the chasm', 127, R, 'street', None),
    ('let go at the chasm', 16, 0, 'street', None),
    ('a jump onto the column of ice: on', 15, R, None, None),
    ('a jump onto the column of ice: Up held 22 frames', 22, R | U, None,
     None),
    ('a jump onto the column of ice: on, in the air', 12, R, None, None),
    ('a jump onto the column of ice: onto the solid block', 16, 0,
     'solid block', None),
    ('let go on the column', 10, 0, 'solid block', None),
    ('a jump over the rest of the chasm: Up held 25 frames', 25, R | U, None,
     None),
    ('a jump over the rest of the chasm: on, in the air', 12, R, None, None),
    ('a jump over the rest of the chasm: onto the street', 16, 0, 'street',
     None),
    ('the werewolf jumps at him: wait', 28, 0, 'street', None),
    ('the werewolf: walk right', 12, R, 'street', None),
    ('the werewolf: Fire, the blow', 1, F, 'street', None, dict(event='blow')),
    ('the werewolf struck', 39, 0, 'street', None, dict(event='struck')),
    ('walk right to the lantern: it lights up', 147, R, 'street', None,
     dict(event='lantern')),
    ('walk right to the second chasm', 50, R, 'street', None),
    ('let go at the chasm', 16, 0, 'street', None),
    ('a long jump over the second chasm: on', 6, R, None, None),
    ('a long jump over the second chasm: Up held 28 frames', 28, R | U, None,
     None),
    ('a long jump over the second chasm: on, in the air', 4, R, None, None),
    ('a long jump over the second chasm: onto the street', 16, 0, 'street',
     None),
    ('walk right to the serac', 30, R, 'street', None),
    ('let go by the serac', 16, 0, 'street', None),
    ('the eagle by the serac: turn left', 1, L, 'street', None),
    ('the eagle by the serac: wait', 6, 0, 'street', None),
    ('the eagle: a jump and a blow: Up held 16 frames', 16, U, None, None),
    ('the eagle: a jump and a blow: Fire, the blow', 1, F, None, None,
     dict(event='blow')),
    ('the eagle: a jump and a blow: struck, he lands', 20, 0, 'street', None,
     dict(event='struck')),
    ('a jump onto the serac: Up held 16 frames', 16, R | U, None, None),
    ('a jump onto the serac: on, in the air', 6, R, None, None),
    ('a jump onto the serac: onto the solid block', 8, 0, 'solid block', None),
    ('let go on the serac', 10, 0, 'solid block', None),
    ('Up and Fire: the bat', 1, U | F, 'solid block', None,
     dict(form=B, event='to bat')),
    ('the smoke', 12, U | F, 'solid block', None),
    ('beats straight up, under the bridge of snow', 38, Beats(0, 10), None,
     None),
    ('beats right: the hourglass on the bridge', 33, Beats(R, 14), None, None,
     dict(got=2)),
    ('glide right: onto the bridge', 6, R, None, None),
    ('let go on the bridge', 10, 0, 'bridge', None),
    ('Down and Fire: Oscar', 1, D | F, 'bridge', None,
     dict(form=V, event='to vampire')),
    ('the smoke', 14, 0, 'bridge', None),
    ('on the bridge of snow', 16, 0, 'bridge', 'dreadcastle-snow-bridge.png'),
    ('walk right, off the bridge, down to the path', 78, R, 'street', None),
    ('let go under the bridge', 16, 0, 'street', None),
    ('the werewolf: walk right', 9, R, 'street', None),
    ('the werewolf: Fire, the blow', 1, F, 'street', None, dict(event='blow')),
    ('the werewolf struck', 39, 0, 'street', None, dict(event='struck')),
    ('walk right into the block of ice', 109, R, 'street', None,
     dict(event='blocked right')),
    ('a jump onto the block of ice: on', 4, R, None, None),
    ('a jump onto the block of ice: Up held 13 frames', 13, R | U, None, None),
    ('a jump onto the block of ice: on, in the air', 6, R, None, None),
    ('a jump onto the block of ice: onto the solid block', 8, 0,
     'solid block', None),
    ('let go on the block', 10, 0, 'solid block', None),
    ('a leap onto the wall of ice: on', 16, R, 'solid block', None),
    ('a leap onto the wall of ice: Up held 28 frames', 28, R | U, None, None),
    ('a leap onto the wall of ice: on, in the air', 15, R, None, None),
    ('a leap onto the wall of ice: onto the wall', 15, 0, 'solid block', None),
    ('the goat on the wall: Fire, the blow', 1, F, 'solid block', None,
     dict(event='blow')),
    ('the goat on the wall struck', 29, 0, 'solid block', None,
     dict(event='struck')),
    ('walk right on the wall, off its end, down to the path', 116, R,
     'street', None),
    ('let go under the wall', 12, 0, 'street', None),
    ('the goat under the ledge: walk right', 73, R, 'street', None),
    ('the goat: Fire, the blow', 1, F, 'street', None, dict(event='blow')),
    ('the goat struck', 29, 0, 'street', None, dict(event='struck')),
    ('walk right under the ledge, to the drift', 26, R, 'street', None),
    ('let go by the drift', 16, 0, 'street', None),
    ('walk right past the drift, to the shut way out', 51, R, 'street', None),
    ('let go by the way out', 16, 0, 'street', None),
    ('a jump up left onto the drift: on', 2, L, None, None),
    ('a jump up left onto the drift: Up held 19 frames', 19, L | U, None,
     None),
    ('a jump up left onto the drift: on, in the air', 3, L, None, None),
    ('a jump up left onto the drift: onto the drift', 16, 0, 'drift', None),
    ('let go on the drift', 10, 0, 'drift', None),
    ('a jump up left onto the ledge: Up held 19 frames', 19, L | U, None,
     None),
    ('a jump up left onto the ledge: on, in the air', 3, L, None, None),
    ('a jump up left onto the ledge: onto the solid block', 15, 0,
     'solid block', None),
    ('let go on the ledge', 10, 0, 'solid block', None),
    ('walk left on the ledge: the book, the way out open', 42, L,
     'solid block', None, dict(event='gate open', got=3)),
    ('let go on the ledge', 16, 0, 'solid block', None),
    ('on the ledge, the col open', 20, 0, 'solid block',
     'dreadcastle-ledge.png'),
    ('walk right, off the ledge and the drift, through the col', 96, R, None,
     None, dict(event='through the gate')),
    ('LEVEL CLEAR: the night into the score', Until(
        lambda m: m.trans > 0, 400, "the transition"), 0,
     None, None, dict(event='next')),
    ('the next level: dreadcastle gate', NEXT_LEVEL, 0, 'street', None),
    ('at the castle, the drawbridge up', 30, 0, 'street',
     'dreadcastle-gate.png', dict(got=0, moths=0)),
    ('walk right to the moat', 105, R, 'street', None),
    ('let go by the moat', 16, 0, 'street', None),
    ('Up and Fire: the bat', 1, U | F, 'street', None,
     dict(form=B, event='to bat')),
    ('the smoke', 12, U | F, 'street', None),
    ('beats right over the moat', 110, Beats(R, 16), None, None),
    ('glide right into the postern', 58, R, 'street', None),
    ('Down and Fire: Oscar', 1, D | F, 'street', None,
     dict(form=V, event='to vampire')),
    ('the smoke', 14, 0, 'street', None),
    ('the guard in the postern: walk right', 178, R, 'street', None),
    ('the guard in the postern: Fire, the blow', 1, F, 'street', None,
     dict(event='blow')),
    ('the guard in the postern struck', 29, 0, 'street', None,
     dict(event='struck')),
    ('walk right out of the postern, to the barrel', 47, R, 'street', None),
    ('let go by the barrel', 12, 0, 'street', None),
    ('a jump onto the barrel: on', 4, R, None, None),
    ('a jump onto the barrel: Up held 13 frames', 13, R | U, None, None),
    ('a jump onto the barrel: on, in the air', 6, R, None, None),
    ('a jump onto the barrel: onto the solid block', 8, 0, 'solid block',
     None),
    ('let go on the barrel', 10, 0, 'solid block', None),
    ('walk right, off the barrel', 46, R, 'street', None),
    ('the guard in the courtyard: walk right', 23, R, 'street', None),
    ('the guard in the courtyard: Fire, the blow', 1, F, 'street', None,
     dict(event='blow')),
    ('the guard in the courtyard struck', 29, 0, 'street', None,
     dict(event='struck')),
    ('walk right to the cart', 98, R, 'street', None),
    ('let go by the cart', 12, 0, 'street', None),
    ('a jump onto the cart: on', 4, R, None, None),
    ('a jump onto the cart: Up held 13 frames', 13, R | U, None, None),
    ('a jump onto the cart: on, in the air', 6, R, None, None),
    ('a jump onto the cart: onto the solid block', 8, 0, 'solid block', None),
    ('let go on the cart', 10, 0, 'solid block', None),
    ('walk right, off the cart', 46, R, 'street', None),
    ('walk right to the lantern: it lights up', 62, R, 'street', None,
     dict(event='lantern')),
    ('walk right to the barrel', 33, R, 'street', None),
    ('let go by the barrel', 12, 0, 'street', None),
    ('a jump onto the barrel: on', 4, R, None, None),
    ('a jump onto the barrel: Up held 13 frames', 13, R | U, None, None),
    ('a jump onto the barrel: on, in the air', 6, R, None, None),
    ('a jump onto the barrel: onto the solid block', 8, 0, 'solid block',
     None),
    ('let go on the barrel', 10, 0, 'solid block', None),
    ('a jump onto the turret: on', 4, R, None, None),
    ('a jump onto the turret: Up held 16 frames', 16, R | U, None, None),
    ('a jump onto the turret: on, in the air', 6, R, None, None),
    ('a jump onto the turret: onto the solid block', 16, 0, 'solid block',
     None),
    ('let go on the turret', 10, 0, 'solid block', None),
    ("Tom's crow by the turret: turn right", 1, R, 'solid block', None),
    ("Tom's crow by the turret: a jump and a blow: Up held 4 frames", 4, U,
     None, None),
    ("Tom's crow by the turret: a jump and a blow: Fire, the blow", 1, F,
     None, None, dict(event='blow')),
    ("Tom's crow by the turret: a jump and a blow: struck, he lands", 21, 0,
     'solid block', None, dict(event='struck')),
    ('let go on the turret', 10, 0, 'solid block', None),
    ('Up and Fire: the bat', 1, U | F, 'solid block', None,
     dict(form=B, event='to bat')),
    ('the smoke', 12, U | F, 'solid block', None),
    ('beats straight up, by the roof', 60, Beats(0, 10), None, None),
    ('beats right: the portrait on the top of the roof', 28, Beats(R, 8),
     None, None, dict(got=2, event='heirloom 1')),
    ('let go: down onto the turret', 72, 0, 'solid block', None),
    ('Down and Fire: Oscar', 1, D | F, 'solid block', None,
     dict(form=V, event='to vampire')),
    ('the smoke', 14, 0, 'solid block', None),
    ('on the turret, the moon behind the castle', 15, 0, 'solid block',
     'dreadcastle-turret.png'),
    ('the werewolf of the band: a jump', 1, R | U, None, None),
    ('the werewolf of the band: on', 27, R, None, None),
    ('the werewolf of the band: let go', 8, 0, None, None),
    ('the werewolf of the band: Fire, the blow', 1, F, None, None,
     dict(event='blow')),
    ('the werewolf of the band: struck', 10, 0, 'street', None,
     dict(event='struck')),
    ('walk right to the low pillar', 116, R, 'street', None),
    ('let go by the pillar', 12, 0, 'street', None),
    ('a jump onto the pillar: Up held 4 frames', 4, R | U, None, None),
    ('a jump onto the pillar: on, in the air', 9, R, None, None),
    ('a jump onto the pillar: onto the solid block', 9, 0, 'solid block',
     None),
    ('let go on the pillar', 10, 0, 'solid block', None),
    ('walk right, off the pillar', 40, R, 'street', None),
    ('walk right into the spikes of iron: thrown back', 43, R, None, None,
     dict(event='spikes')),
    ('thrown back, he lands', 12, 0, 'street', None),
    ('blinking by the spikes', 10, 0, 'street', None),
    ('by the spikes of iron, glinting', 15, 0, 'street',
     'dreadcastle-iron-spikes.png'),
    ('a jump over the spikes: on', 24, R, None, None),
    ('a jump over the spikes: Up held 17 frames', 17, R | U, None, None),
    ('a jump over the spikes: on, in the air', 6, R, None, None),
    ('a jump over the spikes: onto the street', 16, 0, 'street', None),
    ('walk right to the second pillar', 40, R, 'street', None),
    ('let go by the pillar', 12, 0, 'street', None),
    ('a jump onto the pillar: Up held 4 frames', 4, R | U, None, None),
    ('a jump onto the pillar: on, in the air', 9, R, None, None),
    ('a jump onto the pillar: onto the solid block', 9, 0, 'solid block',
     None),
    ('let go on the pillar', 10, 0, 'solid block', None),
    ('walk right, off the pillar', 40, R, 'street', None),
    ('walk right to the spikes', 39, R, 'street', None),
    ('let go by the spikes', 12, 0, 'street', None),
    ('a jump over the spikes: on', 16, R, None, None),
    ('a jump over the spikes: Up held 19 frames', 19, R | U, None, None),
    ('a jump over the spikes: on, in the air', 15, R, None, None),
    ('a jump over the spikes: onto the street', 16, 0, 'street', None),
    ('walk right to the step', 46, R, 'street', None),
    ('let go by the step', 12, 0, 'street', None),
    ('a jump onto the step: Up held 4 frames', 4, R | U, None, None),
    ('a jump onto the step: on, in the air', 9, R, None, None),
    ('a jump onto the step: onto the solid block', 9, 0, 'solid block', None),
    ('let go on the step', 10, 0, 'solid block', None),
    ('a jump onto the stair of the guard tower: Up held 13 frames', 13, R | U,
     None, None),
    ('a jump onto the stair of the guard tower: on, in the air', 3, R, None,
     None),
    ('a jump onto the stair of the guard tower: onto the solid block', 11, 0,
     'solid block', None),
    ('let go on the stair', 10, 0, 'solid block', None),
    ('a jump up left onto the wall walk: Up held 25 frames', 25, L | U, None,
     None),
    ('a jump up left onto the wall walk: on, in the air', 3, L, None, None),
    ('a jump up left onto the wall walk: onto the solid block', 16, 0,
     'solid block', None),
    ('let go on the wall walk', 10, 0, 'solid block', None),
    ('the guard on the wall walk: walk left', 93, L, 'solid block', None),
    ('the guard on the wall walk: Fire, the blow', 1, F, 'solid block', None,
     dict(event='blow')),
    ('the guard on the wall walk struck', 29, 0, 'solid block', None,
     dict(event='struck')),
    ('walk left on the wall walk: the medallion, the door open', 99, L,
     'solid block', None, dict(event='gate open', got=3)),
    ('let go on the wall walk', 16, 0, 'solid block', None),
    ('on the wall walk, the door open', 13, 0, 'solid block',
     'dreadcastle-wall-walk.png'),
    ('walk right to the end of the wall walk', 184, R, 'solid block', None),
    ('let go at its end', 12, 0, 'solid block', None),
    ('a jump down right onto the stair: Up held 10 frames', 10, R | U, None,
     None),
    ('a jump down right onto the stair: on, in the air', 18, R, None, None),
    ('a jump down right onto the stair: onto the solid block', 16, 0,
     'solid block', None),
    ('let go on the stair', 10, 0, 'solid block', None),
    ("Tom's crow by the door: turn right", 1, R, 'solid block', None),
    ("Tom's crow by the door: wait", 32, 0, 'solid block', None),
    ("Tom's crow by the door: a jump and a blow: Up held 12 frames", 12, U,
     None, None),
    ("Tom's crow by the door: a jump and a blow: Fire, the blow", 1, F, None,
     None, dict(event='blow')),
    ("Tom's crow by the door: a jump and a blow: struck, he lands", 21, 0,
     'solid block', None, dict(event='struck')),
    ('walk right, down the stair', 31, R, 'solid block', None),
    ('the werewolf by the door: wait', 68, 0, 'solid block', None),
    ('the werewolf by the door: walk right', 6, R, 'solid block', None),
    ('the werewolf by the door: Fire, the blow', 1, F, 'solid block', None,
     dict(event='blow')),
    ('the werewolf by the door struck', 29, 0, 'solid block', None,
     dict(event='struck')),
    ('walk right, down to the path, through the door of the castle', 78, R,
     None, None, dict(event='through the gate')),
    ('LEVEL CLEAR: the night into the score', Until(
        lambda m: m.trans > 0, 400, "the transition"), 0,
     None, None, dict(event='next')),
    ('the next level: the throne tower', NEXT_LEVEL, 0, 'street', None),
    ('in the throne tower', 44, 0, 'street', 'dreadcastle-hall.png',
     dict(got=0, moths=0)),
    ('walk right to the suit of armour', 40, R, 'street', None),
    ('let go by the armour', 12, 0, 'street', None),
    ('a jump onto the armour: on', 4, R, None, None),
    ('a jump onto the armour: Up held 13 frames', 13, R | U, None, None),
    ('a jump onto the armour: on, in the air', 6, R, None, None),
    ('a jump onto the armour: onto the solid block', 8, 0, 'solid block',
     None),
    ('let go on the armour', 10, 0, 'solid block', None),
    ('Up and Fire: the bat', 1, U | F, 'solid block', None,
     dict(form=B, event='to bat')),
    ('the smoke', 12, U | F, 'solid block', None),
    ('beats right, up to the chandelier', 42, Beats(R, 10), None, None),
    ('glide right over it', 12, R, None, None),
    ('let go: the bat perches on the chandelier', 14, 0, 'chandelier 1', None),
    ('Down and Fire: Oscar', 1, D | F, 'chandelier 1', None,
     dict(form=V, event='to vampire')),
    ('the smoke', 14, 0, 'chandelier 1', None),
    ('on the chandelier', 10, 0, 'chandelier 1', None),
    ('walk right, off the chandelier, down to the floor', 50, R, 'street',
     None),
    ('let go by the chest', 12, 0, 'street', None),
    ('a jump onto the chest: Up held 4 frames', 4, R | U, None, None),
    ('a jump onto the chest: on, in the air', 12, R, None, None),
    ('a jump onto the chest: onto the solid block', 8, 0, 'solid block', None),
    ('let go on the chest', 8, 0, 'solid block', None),
    ('the guard of the armoury: run', 4, R, None, None),
    ('the guard of the armoury: a jump', 12, R | U, None, None),
    ('the guard of the armoury: on', 18, R, None, None),
    ('the guard of the armoury: let go', 5, 0, None, None),
    ('the guard of the armoury: Fire, the blow', 1, F, None, None,
     dict(event='blow')),
    ('the guard of the armoury: struck', 10, 0, 'street', None,
     dict(event='struck')),
    ('walk right: the candelabrum', 65, R, 'street', None,
     dict(event='heirloom 0', got=1)),
    ('walk right into the gallery: the guard walks into him, a hit', 270, R,
     None, None, dict(event='hit')),
    ('thrown back, he lands', 14, 0, 'street', None),
    ('the guard in the gallery: walk right', 5, R, 'street', None),
    ('the guard in the gallery: Fire, the blow', 1, F, 'street', None,
     dict(event='blow')),
    ('the guard in the gallery struck', 29, 0, 'street', None,
     dict(event='struck')),
    ('in the gallery of the portraits', 10, 0, 'street',
     'dreadcastle-gallery.png'),
    ('walk right through the gallery to the lantern: it lights up', 205, R,
     'street', None, dict(event='lantern')),
    ('walk right to the stool', 54, R, 'street', None),
    ('let go by the stool', 12, 0, 'street', None),
    ('a jump onto the stool: Up held 4 frames', 4, R | U, None, None),
    ('a jump onto the stool: on, in the air', 9, R, None, None),
    ('a jump onto the stool: onto the solid block', 9, 0, 'solid block', None),
    ('let go on the stool', 10, 0, 'solid block', None),
    ('a jump onto the mantel: on', 2, R, None, None),
    ('a jump onto the mantel: Up held 22 frames', 22, R | U, None, None),
    ('a jump onto the mantel: onto the solid block', 16, 0, 'solid block',
     None),
    ('let go on the mantel', 10, 0, 'solid block', None),
    ('Up and Fire: the bat', 1, U | F, 'solid block', None,
     dict(form=B, event='to bat')),
    ('the smoke', 12, U | F, 'solid block', None),
    ('beats straight up, by the hood of the fireplace', 24, Beats(0, 10),
     None, None),
    ('beats right: the hourglass on the hood', 36, Beats(R, 8), None, None,
     dict(got=2, event='heirloom 1')),
    ('let go: down onto the mantel', 72, 0, 'solid block', None),
    ('Down and Fire: Oscar', 1, D | F, 'solid block', None,
     dict(form=V, event='to vampire')),
    ('the smoke', 14, 0, 'solid block', None),
    ('walk right, off the mantel, down to the floor', 39, R, 'street', None),
    ('let go past the fireplace', 12, 0, 'street', None),
    ('walk left into the fire on the hearth: thrown back', 31, L, None, None,
     dict(event='fire')),
    ('thrown back, he lands', 12, 0, 'street', None),
    ('blinking by the fire', 10, 0, 'street', None),
    ('by the fire on the hearth, burning', 14, 0, 'street',
     'dreadcastle-fire.png'),
    ('the werewolf of the band: wait', 35, 0, 'street', None),
    ('the werewolf of the band: walk right', 58, R, 'street', None),
    ('the werewolf of the band: Fire, the blow', 1, F, 'street', None,
     dict(event='blow')),
    ('the werewolf of the band struck', 29, 0, 'street', None,
     dict(event='struck')),
    ('walk right to the pedestal', 55, R, 'street', None),
    ('let go by the pedestal', 12, 0, 'street', None),
    ('a jump onto the pedestal: Up held 10 frames', 10, R | U, None, None),
    ('a jump onto the pedestal: onto the pedestal', 11, 0, 'pedestal', None),
    ('let go on the pedestal', 10, 0, 'pedestal', None),
    ('a jump onto the balcony: on', 2, R, None, None),
    ('a jump onto the balcony: Up held 22 frames', 22, R | U, None, None),
    ('a jump onto the balcony: onto the solid block', 16, 0, 'solid block',
     None),
    ('let go on the balcony', 10, 0, 'solid block', None),
    ('the guard on the balcony: walk right', 54, R, 'solid block', None),
    ('the guard on the balcony: Fire, the blow', 1, F, 'solid block', None,
     dict(event='blow')),
    ('the guard on the balcony struck', 29, 0, 'solid block', None,
     dict(event='struck')),
    ('walk right on the balcony: the book, the door open', 23, R,
     'solid block', None, dict(event='gate open', got=3)),
    ('let go on the balcony', 16, 0, 'solid block', None),
    ('on the balcony, the door of the throne room open', 14, 0, 'solid block',
     'dreadcastle-balcony.png'),
    ('walk right, off the balcony, through the door of the throne room', 103,
     R, None, None, dict(event='arena')),
    # Tom Darkfang.
    ('into the arena: Tom unpacked and mirrored', 50, 0, 'street', None),
    ('in the throne room: Tom waits by his throne', 15, 0, 'street',
     'dreadcastle-arena.png', dict(got=3)),
    ('the fight: up to Tom, a blow while he waits', Until(
        tom_is("TS_GROWL", lambda k: k["GROWL_FRAMES"] - 6), 300,
        "Tom growls"), FIGHT, None, None),
    ('Tom growls, his arms up', 2, FIGHT, None,
     'dreadcastle-growl.png'),
    ('the fight: Tom leaps at Oscar', Until(
        lambda m: m.tom_state == m.k["TS_LEAP"] and m.tom_y >> 8 < 112,
        300, "Tom high in his leap"), FIGHT, None, None),
    ('Tom in the air', 1, FIGHT, None, 'dreadcastle-leap.png'),
    ('the fight: Tom charges, Oscar over him; Tom dazed', Until(
        tom_is("TS_DAZED", lambda k: k["DAZED_FRAMES"] - 4), 600,
        "Tom dazed"), FIGHT, None, None, dict(event='tom charges')),
    ('Tom dazed against the wall', 1, FIGHT, None,
     'dreadcastle-dazed.png'),
    ('the fight: on to the end, Tom beaten', Until(
        tom_is("TS_PAUSE", lambda k: k["PAUSE_FRAMES"] - 6), 4000,
        "Tom on the dais"), FIGHT, None, None,
     dict(event='tom beaten')),
    ('Tom on the dais of his throne, beaten', 1, FIGHT, None,
     'dreadcastle-beaten.png'),
    ('away through the high window', Until(
        tom_is("TS_GONE", lambda k: k["GONE_FRAMES"] - 30), 200,
        "Tom gone"), FIGHT, None, None, dict(event='tom gone')),
    ('the throne room without Tom', 1, FIGHT, None,
     'dreadcastle-gone.png'),
    # The victory, the title, a new game, dawn.
    ('a moment, then the victory', Until(
        lambda m: m.game_state == game_model.ST_WON, 200, "the victory"),
     0, None, None, dict(event='band 1')),
    ('the words over the arena; the night into the score', Until(
        lambda m: m.state_phase == 1, 300, "the night counted"), 0,
     None, None),
    ('the victory', 10, 0, None, 'dreadcastle-won.png'),
    ('(0.10.1) its jingle to the end', Until(since(
        'victory', game_model.JINGLE_FRAMES[game_model.SONG_WON] + 2),
        400, "the jingle over"), 0, None, None),
    ('Fire: the title', 1, F, None, None, dict(event='title')),
    ('the transition to the title', 49, 0, None, None,
     dict(event='the title')),
    ('the title again', 20, 0, None, 'dreadcastle-title-again.png'),
    # The second game with MUSIC: the theme from its start on the
    # title, in level 1 through its loop. Then the test takes the
    # program to level 8 and into the arena (it writes the level, the
    # transition and the staff: the help of this game), for Tom's theme
    # and the fight to the end, and the victory with MUSIC.
    ('the menu: Up, MUSIC: the theme from its start', 1, U, None, None,
     dict(event='menu 0')),
    ('let go', 10, 0, None, None),
    ('Fire: a new game', 1, F, None, None, dict(event='start')),
    ('the transition into level 1', 49, 0, 'street', None),
    ('in the village again: nothing taken, no staff, the score 0', 30, 0,
     'street', 'dreadcastle-again.png', dict(got=0, moths=0)),
    ('Oscar still: the theme through its loop', 2450, 0, 'street', None),
    ('on to level 8, the staff in hand (the test writes it)', 1, 0, None,
     None, dict(poke={'level_no': 6, 'trans': 50,
                      'trans_kind': game_model.GO_NEXT, 'has_staff': 1})),
    ('the transition into level 8: the theme from its start', 49, 0,
     None, None),
    ('into the arena (the test writes it)', 1, 0, None, None, dict(poke={
        'trans': 50, 'trans_kind': game_model.GO_ARENA})),
    ('the transition into the arena', 49, 0, None, None),
    ("the fight with MUSIC: Tom's theme until he is beaten", Until(
        lambda m: m.game_state == game_model.ST_WON, 4000,
        "the victory"), FIGHT_AGAIN, None, None, dict(event='tom beaten')),
    ('the words over the arena; the night into the score', Until(
        lambda m: m.state_phase == 1, 300, "the night counted"), 0,
     None, None),
    ('the victory with MUSIC: its jingle to the end', Until(since(
        'victory', game_model.JINGLE_FRAMES[game_model.SONG_WON] + 2),
        400, "the jingle over"), 0, None, None),
    ('Fire: the title, the theme', 1, F, None, None, dict(event='title')),
    ('the transition to the title', 49, 0, None, None),
    ('on the title with MUSIC', 20, 0, None, None),
    # The third game with SOUND FX, lost with the joystick only:
    # Oscar waits in the village until dawn; the bell in the last two
    # steps of the night, dawn's jingle; Fire, the title.
    ('the menu: Down, SOUND FX: silence, a click', 1, D, None, None,
     dict(event='menu 1')),
    ('let go', 10, 0, None, None),
    ('Fire: a new game', 1, F, None, None, dict(event='start')),
    ('the transition into level 1', 49, 0, 'street', None),
    ('a jump at the start', 1, U, None, None),
    ('he lands', 45, 0, 'street', None),
    ('the night goes by: the bell tolls', Until(happens('toll'), 6200,
     "the bell"), 0, 'street', None, dict(event='toll')),
    ('on to dawn: the game stops', Until(happens('dawn'), 800, "dawn"), 0,
     'street', None, dict(event='dawn')),
    ('the sky lighter, step by step; Oscar in a puff of smoke', Until(
        lambda m: m.state_phase > m.c["DAWN_STEPS"], 300,
        "Oscar gone"), 0, None, None, dict(event='band 2')),
    ('the sun has risen over the village', 10, 0, None,
     'dreadcastle-dawn-village.png'),
    ('its jingle to the end', Until(since(
        'dawn', game_model.JINGLE_FRAMES[game_model.SONG_DAWN] + 2),
        400, "the jingle over"), 0, None, None),
    ('Fire: the title', 1, F, None, None, dict(event='title')),
    ('the transition to the title', 49, 0, None, None),
    ('on the title', 20, 0, None, None),
    # The fourth game with SILENT: the test takes the program to
    # level 7 and to the end of its night (it writes the level, the
    # transition and the night: the help of this game), for dawn in
    # the title's own setting, with no jingle.
    ('the menu: Down, SILENT', 1, D, None, None, dict(event='menu 2')),
    ('let go', 10, 0, None, None),
    ('Fire: a new game', 1, F, None, None, dict(event='start')),
    ('the transition into level 1', 49, 0, 'street', None),
    ('a jump at the start, unheard', 1, U, None, None),
    ('he lands', 45, 0, 'street', None),
    ('on to level 7 (the test writes it)', 1, 0, None, None, dict(poke={
        'level_no': 5, 'trans': 50, 'trans_kind': game_model.GO_NEXT})),
    ('the transition into level 7', 49, 0, None, None),
    ('the night nearly over (the test writes it)', 1, 0, None, None,
     dict(poke={'night': 2, 'night_time': 30})),
    ('the bell, unheard', 35, 0, None, None, dict(event='toll')),
    ('the night near its end (the test writes it)', 1, 0, None, None,
     dict(poke={'night_time': 40})),
    ('dawn: the game stops, no jingle', 39, 0, None, None,
     dict(event='dawn')),
    ('the sky lighter, step by step; Oscar in a puff of smoke', Until(
        lambda m: m.state_phase > m.c["DAWN_STEPS"], 300,
        "Oscar gone"), 0, None, None, dict(event='band 2')),
    ('the sun has risen', 10, 0, None, 'dreadcastle-dawn.png'),
    ('silence where the jingle would be', Until(since(
        'dawn', game_model.JINGLE_FRAMES[game_model.SONG_DAWN] + 2),
        400, "as long as the jingle"), 0, None, None),
    ('Fire: the title', 1, F, None, None, dict(event='title')),
    ('the transition to the title', 49, 0, None, None),
    ('rest on the title', 120, 0, None, None),
]
SURFACES = {1: ["street", "solid block", "stall 2", "lamp", "balcony",
                "right roof", "spire", "left roof", "fountain",
                "balcony C"],
            2: ["street", "solid block", "pile 1", "pile 2",
                "pedestal", "wall"],
            3: ["street", "solid block", "low branch", "stone 1",
                "stone 2", "stone 3", "stone 4", "stone 5"],
            4: ["street", "solid block", "clod 8", "clod 11", "clod 14",
                "clod 17", "clod 21", "clod 24", "clod 27", "clod 30",
                "clod 34", "boardwalk 1", "boardwalk 2", "boardwalk 3"],
            5: ["street", "solid block", "boulder"],
            6: ["street", "solid block", "mound 1", "mound 2", "drift"],
            7: ["street", "solid block"],
            8: ["street", "solid block", "pedestal"]}
PERCHES = ["roof C1", "street", "bridge", "chandelier 1"]
EVENTS = ["to bat", "to vampire", "refused", "out of energy", "top",
          "beat", "dive", "blocked right", "blocked left", "fallen",
          "back", "start", "next", "lantern", "heirloom 0",
          "heirloom 1", "heirloom 2", "gate open", "through the gate",
          "dawn", "hit", "no health", "cat jumps", "cat lands",
          "staff", "blow", "struck", "brambles", "head", "wisps",
          "spikes", "fire",
          # Tom
          "arena", "tom growls", "tom leaps", "tom lands", "tom charges",
          "tom dazed", "tom struck", "tom beaten", "tom flees", "tom gone",
          # the songs
          "boss theme", "theme",
          # the states
          "title", "the title", "menu 1", "menu 2", "menu 0", "silence",
          "band 0", "band 1", "band 2", "victory", "sunrise"]
OSCAR, OSCAR_BYTES = 0x40, 15
FORM, FORM_BYTES = 0x38, 7          # form ... moths eaten
GAME, GAME_BYTES = 0xE0, 15         # health ... protect, stun
STAFF, STAFF_BYTES = 0xF0, 3        # has_staff, blow, env
ENEMIES = 0xC680                    # the enemies: 14 arrays of 8
ENEMY_ARRAYS = 14
ENV_TABLES, ENV_BYTES = 0xC700, 9 * 256     # the setting's tables
SET_SLOT = 0x5800                   # the setting's characters
STATE = 0x10                        # camera ... speed: 13 bytes
FRAME_COUNT = 0x19
PLAY_D021 = 0xFD                    # the playfield's $d021
LEVEL = 0xC000                      # the level being played
FIRST_ROW_LINE = 51                 # badline of row 0
ROW_11_LINE = 51 + 8 * 11
POKES = {"night": (0xE1, 1), "night_time": (0xE2, 2),
         "frame_count": (0x19, 1),          # as at the old start
         "level_no": (0xEC, 1), "trans": (0xE8, 1),     # on to
         "trans_kind": (0xE9, 1), "has_staff": (0xF0, 1),   # a level
         "sound_mode": (0x0301, 1)}         # the menu's choice
LEAP_FRAMES, LEAP_RISE = 31, 45     # tom.asm: a leap
# states.asm: the count's frames (LEVEL CLEAR, a step of the
# night, after it), the victory's before its count.
COUNT_FRAMES = {"TALLY_WAIT": 40, "TALLY_TICK": 3, "TALLY_END": 60,
                "WON_WAIT": 50}                 # TALLY_END
TOM_BYTES, TOM_2_BYTES = 16, 6      # arena ... tom_flash; tom_safe
TOM_SPRITES = 0x7E00                # ... tom_reg; Tom's two pages
STATES = 0x0300                     # game_state ... band_d018
SFX_VARS = 0x030C                   # sfx_pos ... sfx_last


def read_png(path):
    """Rows of RGB bytes from a PNG with 8-bit RGB or RGBA pixels."""
    data = Path(path).read_bytes()
    position, chunks = 8, {}
    while position < len(data):
        length, kind = struct.unpack(">I4s", data[position:position + 8])
        body = data[position + 8:position + 8 + length]
        chunks.setdefault(kind, []).append(body)
        position += 12 + length
    width, height, depth, colour_type = struct.unpack(
        ">IIBB", chunks[b"IHDR"][0][:10])
    vicemon.require(depth == 8 and colour_type in (2, 6),
                    f"unexpected PNG format {depth}/{colour_type}")
    size = 3 if colour_type == 2 else 4
    raw = zlib.decompress(b"".join(chunks[b"IDAT"]))
    stride = width * size
    rows, previous = [], bytearray(stride)
    for y in range(height):
        kind = raw[y * (stride + 1)]
        line = bytearray(raw[y * (stride + 1) + 1:(y + 1) * (stride + 1)])
        for i in range(stride):
            left = line[i - size] if i >= size else 0
            up = previous[i]
            corner = previous[i - size] if i >= size else 0
            if kind == 1:
                line[i] = (line[i] + left) & 255
            elif kind == 2:
                line[i] = (line[i] + up) & 255
            elif kind == 3:
                line[i] = (line[i] + (left + up) // 2) & 255
            elif kind == 4:
                guess = left + up - corner
                best = min((abs(guess - left), 0), (abs(guess - up), 1),
                           (abs(guess - corner), 2))[1]
                line[i] = (line[i] + (left, up, corner)[best]) & 255
        rows.append([bytes(line[x * size:x * size + 3])
                     for x in range(width)])
        previous = line
    return rows


class Checks:
    def __init__(self):
        self.items = []

    def add(self, name, ok, detail=""):
        self.items.append({"check": name, "pass": bool(ok),
                           "detail": detail})
        print(("PASS " if ok else "FAIL ") + name +
              (f": {detail}" if detail and not ok else ""))

    def passed(self):
        return all(item["pass"] for item in self.items)


class Stopped(Exception):
    """--stop-at: the check named failed; the route stops."""


class Tally:
    """A check made at every frame: passes if it never failed; keeps
    the first failure."""
    stop_at = None                  # --stop-at TEXT
    stop_after = 0                  # --stop-after N: N frames more
    stopping = None                 # [the tally, frames left]

    def __init__(self, name):
        self.name, self.count, self.failures, self.first = name, 0, 0, ""

    def __call__(self, ok, where, detail=""):
        self.count += 1
        if not ok:
            self.failures += 1
            if not self.first:
                self.first = f"{where}: {detail}"
                stop = Tally.stop_at
                if stop and (self.name.startswith(stop)
                             or stop in self.name):
                    if not Tally.stop_after:
                        raise Stopped(self)
                    Tally.stopping = [self, Tally.stop_after]

    def report(self, checks):
        checks.add(f"{self.name} ({self.count} times)", not self.failures,
                   f"{self.failures} failures; first at {self.first}")


def difference(actual, expected):
    for key in sorted(expected):
        if actual[key] != expected[key]:
            col, row = key
            return (f"column {col} row {row}: {actual[key]} instead of "
                    f"{expected[key]}")
    return ""


def position(count, start, line):
    """Raster line relative to the frame after the turn's start:
    negative while still in the frame of the turn."""
    if count == start:
        return line if line < 226 else line - 312
    return line + 312 * (count - start - 1)


def clock(count, start, registers):
    return (position(count, start, registers["LIN"]) *
            vicemon.PAL_LINE_CYCLES + registers["CYC"])


# The steps of a transition (objects.asm, trans_steps), by number.
STEP_NAMES = ("none", "on", "page", "draw 0", "draw 1", "draw 2",
              "draw 3", "second", "level", "tables", "off")


def stream_of(model, kind):
    """(label, file) of the packed stream of `kind` being unpacked:
    the map of the level; the tables of its setting; the set
    of the setting (env already the new one: trans_off)."""
    if kind == "map":
        number = model.level_no + 1
        return f"level_map_{number}", f"level{number}.lz"
    if kind == "tables":
        name = reference.ENVIRONMENTS[model.level_env[model.level_no]]
        return f"env_packed_{name}", f"env_{name}.lz"
    if kind == "tom":
        return "tom_packed", "tom.lz"
    name = reference.ENVIRONMENTS[model.env]
    return f"set_packed_{name}", f"charset_{name}.lz"


def steady(model, count):
    """A picture that holds for a capture: the moths' wings the same
    from 3 frames before to 4 after (count AND 7 from 3 to 5), where
    the hazards flicker their pictures too (count AND 3 is
    0 or 1, they change at 2), the heirloom's bob too (the night's
    frames AND 15 from 4 to 11), and the bars of the energy and of the
    night."""
    if model.game_state != game_model.ST_PLAY:
        return True                 # stopped: nothing moves
    if not 3 <= count & 7 <= 5 and model.has("bat"):
        return False                # (the moths: from step 4)
    mask = (1 << model.flicker_shift) - 1   # a variant's speed
    if model.c["FLICKER_SETTINGS"] >> model.env & 1 and \
            (count - 2) & mask < 2:
        return False
    k = model.k
    if model.has("objects") and not (
            4 <= model.night_time & 15 <= 11
            and 8 < model.night_time < k["NIGHT_STEP"] - 8):
        return False                # (the night: from step 5)
    if model.arena and (model.tom_flash or
                        model.frame - model.tom_page_frame < 2):
        return False                # Tom: no flash, his page held
    full = k["ENERGY_FULL"] << 8
    if model.ground and model.energy < full:   # coming back
        before = model.energy - 3 * k["RECHARGE"]
        after = min(model.energy + 3 * k["RECHARGE"], full)
        return before >> 13 == after >> 13     # whole steps
    return True


def shown(model):
    """What a frame drawn with the registers of now shows (for the
    captures): the camera, the sprites on, the level, the setting
    and its characters with the moths' picture, the HUD."""
    on = model.sprites_on
    return {"camera": model.camera,
            "oscar": ([model.sprite_x, model.sprite_y, model.placed]
                      if on & 3 else None),
            "heirloom": (list(model.sprite7[:2]) + [model.sprite7[3]]
                         if on & 0x80 and not model.arena else None),
            "enemies": [[x, y, block, colour] for
                        x, y, block, colour, _, _
                        in model.enemy_sprites],
            "staff": (list(model.staff_sprite)
                      if on & 4 and model.staff_sprite else None),
            "moon": (list(model.moon_sprite[:2])
                     if on & 0x40 and model.moon_sprite else None),
            "tom": ([list(sprite) for sprite in model.tom_sprites]
                    + [model.tom_pages[model.tom_front]]
                    if model.arena and on & 0xB8 == 0xB8
                    and model.tom_sprites else None),
            "env": model.env,
            "level": bytes(model.level), "charset": model.charset(),
            "hud": model.hud(),
            # the name on the title; a band of words; dawn
            "logo": model.logo_on and on & 0x3C == 0x3C,
            "band": band_cells(model) if model.band_on else None,
            "d021": model.play_d021()}


def band_cells(model):
    """The band shown: its first and last rows, and the cells of
    the screen in front in them, (code, colour)."""
    first = (model.band_top - model.k["BAND_LINE"]) // 8
    last = (model.band_end - model.k["BAND_LINE"]) // 8
    screen = model.screens[model.front]
    return [first, last, {f"{col},{row}": [screen.get((col, row), 0),
                                           model.colours.get((col, row),
                                                             0)]
                          for row in range(first, last + 1)
                          for col in range(reference.VISIBLE)}]


def tom_sprites(files, tom):
    """Tom's four sprites for the reference, as shown: (X, Y,
    the block's 64 bytes, colour), top left, top right, bottom left,
    bottom right; or None."""
    if not tom:
        return None
    *sprites, number = tom
    page = reference.tom_picture(files, number)
    return [(x, y, page[n * 64:n * 64 + 64], colour)
            for n, (x, y, _, colour) in enumerate(sprites)]


def logo_sprites(files, c, k):
    """The title's name for the reference: sprites 2-5."""
    return [(c["LOGO_X"] + n * c["LOGO_STEP"], c["LOGO_Y"],
             files["logo"][n * 64:n * 64 + 64], c["LOGO_COLOUR"])
            for n in range(c["LOGO_SPRITES"])]


def band_of(band):
    """A band as shown() keeps it, for the reference."""
    if band is None:
        return None
    first, last, cells = band
    return (first, last, {tuple(map(int, key.split(","))): tuple(value)
                          for key, value in cells.items()})


def check_kernal(monitor, files, c, labels):
    """Tom's pictures under the KERNAL once the transition into
    the arena is over: facing right at TOM_PICS as tom.bin; the table
    that mirrors at MIRROR (the pictures facing left are made
    from them as they are copied). A text: what is wrong, or "ok"."""
    pictures = c["TOM_PICTURES"]
    pics, mirror = labels["TOM_PICS"], labels["MIRROR"]
    wrong = []
    if monitor.memory(pics, pictures * 256) != \
            files["tom"][:pictures * 256]:
        wrong.append("facing right")
    table = bytes(reference.mirror_byte(b) for b in range(256))
    if monitor.memory(mirror, 256) != table:
        wrong.append("the table")
    return ", ".join(wrong) or "ok"


def sprite_bytes(files, k, block):
    """The 64 bytes of a VIC-II sprite block of the program: an
    enemy's (the mountain's at ENEMY_BLOCKS_2), Oscar's (the
    smoke's colours for an enemy's puff), the staff's."""
    first_types = files["constants"]["ENEMY_TYPES_1"] * 256
    for first, data in ((k["ENEMY_BLOCKS"],
                         files["enemies"][:first_types]),
                        (k["ENEMY_BLOCKS_2"],
                         files["enemies"][first_types:]),
                        (k["OSCAR_LINES"], files["sprites"]),
                        (k["STAFF_BLOCKS"], files["staff"])):
        at = (block - first) * 64
        if 0 <= at < len(data):
            return data[at:at + 64]
    raise ValueError(f"block {block}")


LAST_STEP = 13                      # the book's chain: the whole game
TRANS_FRAMES = 50                   # objects.asm: a transition
# What each step of the chain lacks, for what a route expects at the
# end of an entry: the expectation's key, or its event's first words,
# and the step that has it.
EXPECTED_FROM = {"form": 4, "moths": 4, "got": 5,
                 "to bat": 4, "to vampire": 4, "refused": 4, "beat": 4,
                 "out of energy": 4, "dive": 4, "heirloom": 5,
                 "lantern": 5, "gate open": 5, "through the gate": 5,
                 "next": 5, "hit": 6, "staff": 7, "blow": 7,
                 "struck": 7, "arena": 10, "tom": 10, "band": 12,
                 "title": 12, "start": 12, "menu": 12}


def expected_in(step, expect):
    """What the step has of an entry's expectations."""
    kept = {}
    for key, value in expect.items():
        what = value if key == "event" else key
        first = max([s for name, s in EXPECTED_FROM.items()
                     if str(what).startswith(name)], default=1)
        if step >= first:
            kept[key] = value
    return kept


def game_route(step):
    """Steps 3 and 6-11: the complete game's route from level 1's
    start ("still at the start", after the title), as far as the step
    goes: without the count at the gates (states.asm, step 12): the
    next level's entry then plays the transition, TRANS_FRAMES frames
    (the frames of the level after it as before); what the step has
    not got left out of the expectations."""
    first = next(i for i, e in enumerate(ROUTE)
                 if e[0] == "still at the start")
    gates = [i for i, e in enumerate(ROUTE[:1000]) if len(e) > 5
             and e[5].get("event") in ("through the gate", "arena")]
    levels = {6: 2, 7: 3, 8: 6, 9: 8, 10: 8, 11: 8}.get(step)
    if step < 6:                    # level 1, to the left roof
        end = next(i for i, e in enumerate(ROUTE) if e[0] ==
                   "jump left onto the roof: onto the left roof") + 1
    elif step >= 10:                # the arena: Tom gone
        end = next(i for i, e in enumerate(ROUTE) if e[0] ==
                   "the throne room without Tom") + 1
    else:
        end = gates[levels - 1] + 1
    route = []
    for entry in ROUTE[first:end]:
        what, frames = entry[0], entry[1]
        if what.startswith(("LEVEL CLEAR", "the rest of the night")):
            continue
        if frames == NEXT_LEVEL:
            frames = TRANS_FRAMES
        expect = expected_in(step, dict(entry[5]) if len(entry) > 5
                             else {})
        if step == 9 and expect.get("event") == "arena":
            expect["event"] = "next"        # step 9: level 1 again
        route.append((what, frames) + tuple(entry[2:5]) + (expect,))
    return route


def step_route(step):
    """The route of step `step` (1-11); in step_routes.py, ("until",
    test, most) for an Until."""
    return [(entry[0], Until(entry[1][1], entry[1][2],
                             entry[1][1].what)) + tuple(entry[2:])
            if isinstance(entry[1], tuple) else entry
            for entry in route_of(step)]


def step_12_route():
    """Step 12: the complete game's route; the bell of the last two
    steps of the night comes with step 13 (its sound): in the third
    game the night goes by to dawn."""
    route = []
    for entry in ROUTE:
        if entry[0] == "the night goes by: the bell tolls":
            route.append(("the night goes by to dawn (no bell yet)",
                          Until(happens("dawn"), 7000, "dawn"), 0,
                          "street", None, dict(event="dawn")))
        elif entry[0] == "on to dawn: the game stops":
            continue
        elif entry[0] == "the bell, unheard":
            route.append(("the night's last steps", ) + entry[1:5])
        else:
            route.append(entry)
    return route


def own_route(path):
    """A route of its own (a variant's): route(v) of a Python file;
    ("until", test, most) for an Until, as in step_routes.py."""
    spec = importlib.util.spec_from_file_location("own_route", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return [(entry[0], Until(entry[1][1], entry[1][2],
                             entry[1][1].what)) + tuple(entry[2:])
            if isinstance(entry[1], tuple) else entry
            for entry in module.route(sys.modules[__name__])]


def route_of(step):
    if step <= 5:
        return step_routes.route(step, sys.modules[__name__])
    route = game_route(step)
    if step <= 9:                   # the last level's gate: level 1
        route += [("the transition: level 1 again", TRANS_FRAMES, 0,
                   "street", None),
                  ("level 1 again, from its start", 35, 0, "street",
                   None, dict(got=0))]
    else:                           # Tom gone: level 1 again
        route += [("a moment, then level 1 again", Until(
                      happens("start"), 200, "level 1 again"), 0,
                   None, None),
                  ("the transition into level 1", TRANS_FRAMES, 0,
                   "street", None),
                  ("level 1 again, from its start", 35, 0, "street",
                   None, dict(got=0))]
    return route


def step_root(step):
    """The folder of a step of the book's chain, chain/NN-name
    (tools/make_chain.py); the project itself for the complete game."""
    if step == LAST_STEP:
        return PROJECT
    found = sorted((PROJECT / "chain").glob(f"{step:02d}-*"))
    vicemon.require(len(found) == 1, f"step {step} not in chain/")
    return found[0]


INSTRUCTION = re.compile(r"^\.([0-9a-f]{4})\t(?:([0-9a-f]{4})\t)?\t*"
                         r"((?:[0-9a-f]{2} )*[0-9a-f]{2})\t+([a-z]{3})\b")


def instructions(listing):
    """The address of every instruction of a 64tass listing (of
    code moved elsewhere to run, .logical, the address where it
    runs)."""
    found = set()
    for line in listing.read_text(encoding="utf-8",
                                  errors="replace").splitlines():
        match = INSTRUCTION.match(line)
        if match:
            found.add(int(match.group(2) or match.group(1), 16))
    return sorted(found)


def report_path(path):
    """A path for the report: in the project, from its folder."""
    return (str(path.relative_to(PROJECT)) if path.is_relative_to(PROJECT)
            else str(path))


def same(found, expected):
    """found equals expected but where expected has None (a byte the
    step has not got: any value)."""
    return len(found) == len(expected) and all(
        e is None or f == e for f, e in zip(found, expected))


def restart(monitor, prg, entry):
    """Steps 1-11: the PRG written again into memory, as LOAD leaves
    it, and the program run from its entry, the interrupts held: from
    now on every frame is the test's (the program has run on its own
    since VICE started it, and before the title of step 12 there is no
    still start to wait at)."""
    data = prg.read_bytes()
    start = data[0] | data[1] << 8
    body = data[2:]
    for offset in range(0, len(body), 0x8000):
        part = body[offset:offset + 0x8000]
        monitor.poke(start + offset, part)
    registers = monitor.read_registers()
    flags = registers.get("FL", 0) | 0x04          # I: held
    monitor.command(0x32, struct.pack("<BH", 0, 2)
                    + struct.pack("<BBH", 3, monitor.registers["FL"],
                                  flags)
                    + struct.pack("<BBH", 3, monitor.registers["PC"],
                                  entry))


def step_checks(step, model, seen, checks, c, files, music, player):
    """What steps 1-11 of the chain must show, on their routes (the
    program compared with the model of the step at every frame)."""
    happened = [what for _, what in model.events]
    events = seen["events"] | set(happened)

    def has(part):
        return step >= game_model.FIRST[part]

    if step == 1:
        checks.add("step 1: the village at night, still: the camera at "
                   "0, Oscar at the start, standing",
                   seen["camera"] == {0} and seen["x"] == {c["START_X"]}
                   and seen["pictures"] == {game_model.STAND},
                   f"cameras {sorted(seen['camera'])}, x "
                   f"{sorted(seen['x'])}")
        return
    if step == 2:
        checks.add("step 2: the camera from one end of the level to the "
                   "other, both ways, a back screen shown at every "
                   "column; it waits for the back screen when it turns",
                   {0, c["CAMERA_MAX"]} <= seen["camera"]
                   and model.swaps > 2 * c["CAMERA_MAX"] // 8 - 8
                   and model.holds[0] > 0 and model.holds[1] > 0,
                   f"cameras {min(seen['camera'])}-"
                   f"{max(seen['camera'])}, {model.swaps} swaps, "
                   f"waits {model.holds}")
        return
    # From step 3: Oscar.
    landed = {name for n, name in seen["surfaces"] if n == 1}
    wanted = {"street", "solid block", "stall 2", "lamp", "balcony",
              "right roof", "spire", "left roof"}
    checks.add("Oscar walks and jumps: he lands on the street, the "
               "crates, the stall, the lamp, the balcony, the roofs and "
               "the spire of level 1",
               wanted <= landed, f"never on {sorted(wanted - landed)}")
    walk = set(range(12))
    checks.add("his twelve pictures, both ways (standing, walking, "
               "jumping, falling)", walk <= seen["pictures"],
               f"never {sorted(walk - seen['pictures'])}")
    falls = {"blocked right", "blocked left", "fallen", "back"}
    checks.add("the crates stop him both ways; he falls into the "
               "trapdoor and the transition takes him back",
               falls <= events, f"never {sorted(falls - events)}")
    checks.add("the screen off in the transition, then on",
               seen["blank"] > 0, f"{seen['blank']} frames off")
    # Step 5's route flies the bat only along the ways of levels.py
    # (right, no dive, no moth): the bat's checks are step 4's, and
    # come back from step 6 with the complete game's route.
    if has("bat") and step != 5:
        bat = {"to bat", "to vampire", "beat", "dive", "out of energy",
               "refused"}
        checks.add("the bat: the change both ways, beats, a dive, out "
                   "of energy, a change refused",
                   bat <= events, f"never {sorted(bat - events)}")
        pictures = set(range(c["PICTURE_COUNT"]))
        checks.add(f"all {c['PICTURE_COUNT']} pictures of Oscar, the "
                   "bat and the smoke", pictures <= seen["pictures"],
                   f"never {sorted(pictures - seen['pictures'])}")
        checks.add("the bat eats moths", sum(seen["moths"].values()) > 0,
                   f"{seen['moths']}")
    if has("objects"):
        wanted = {1, 2} if step < 7 else set(range(
            1, game_model.STEP_LEVELS.get(step, 8) + 1))
        checks.add(f"the levels of the step played (by the model and "
                   f"by the program): {sorted(wanted)}; then level 1 "
                   "again", wanted == seen["levels"] == seen["c64_levels"]
                   and model.level_no == 0
                   and seen.get("c64_level_no") == 0,
                   f"levels {sorted(seen['levels'])}, the program's "
                   f"{sorted(seen['c64_levels'])}")
        level = {"heirloom 0", "heirloom 1", "heirloom 2", "lantern",
                 "gate open", "through the gate", "next"}
        checks.add("the three heirlooms, the lantern, the gate open and "
                   "passed", level <= events,
                   f"never {sorted(level - events)}")
        kinds = set(range(c["HEIRLOOM_KINDS"])) if step >= 6 else \
            {0, 1, 2, 3, 4, 5}
        shown = seen["heirlooms_shown"]
        checks.add("the heirlooms shown (sprite 7)", kinds <= shown,
                   f"never {sorted(kinds - shown)}")
    if step == 5:
        checks.add("dawn: level 1 again (the night over)",
                   "dawn" in events and happened.count("start") >= 1,
                   f"{sorted(events)}")
    if has("enemies"):
        checks.add("Oscar hit by the three kinds of enemy (the "
                   "watchman, the crow, the cat); he blinks; no health "
                   "left: back at the lantern",
                   {0, 1, 2} <= seen["hit_by"] and seen["blinking"] > 0
                   and "no health" in events,
                   f"by {sorted(seen['hit_by'])}, blinking "
                   f"{seen['blinking']}")
        types = {0, 1, 2} if step == 6 else set()
        shown = {t for t, _ in seen["enemy_pictures"]}
        checks.add("the enemies of the village shown, four pictures "
                   "each", all((k, n) in seen["enemy_pictures"]
                               for k in (0, 1, 2) for n in range(4)),
                   f"{sorted(shown | types)}")
    if has("staff"):
        staff = {"staff", "blow", "struck", "brambles", "head"}
        checks.add("the staff taken, blows, enemies struck, the "
                   "brambles, his head under a block",
                   staff <= events, f"never {sorted(staff - events)}")
        checks.add("the moon in the wood, at every frame of the screen "
                   "on", seen["moon_frames"].get(1, 0) > 0
                   and seen["moon_missing"] == 0,
                   f"{seen['moon_frames']}, {seen['moon_missing']} "
                   "without it")
    if has("packed"):
        streams = seen["streams"]
        checks.add("the packed streams unpacked in the transitions: the "
                   "maps, the settings' tables and sets",
                   streams["map"] >= 5 and streams["tables"] >= 4
                   and streams["set"] >= 4, f"{streams}")
        flicker = {n: sorted(p) for n, p in
                   seen["flicker_pictures"].items()}
        wanted = [n for n in ((2, 4) if step == 8 else (2, 4, 5, 6))
                  if c["FLICKER_SETTINGS"] >> n & 1]  # the data
        checks.add("the hazards that flicker: their four pictures",
                   all(flicker.get(n) == [0, 1, 2, 3] for n in wanted),
                   f"{flicker}")
    if has("castle"):
        blue = {c[f"ENV{n}_D021"] for n in range(len(files["envs"]))}
        checks.add("the castle's sky blue, the HUD black: $d021 as the "
                   "setting wants it", blue <= seen["d021"],
                   f"{sorted(seen['d021'])}")
    if has("tom"):
        k = model.k
        checks.add("Tom: into the arena, struck eight times, beaten, "
                   "gone; then level 1 again",
                   len(model.tom_struck) >= k["HITS_FULL"]
                   and {"tom beaten", "tom gone"} <= events,
                   f"{len(model.tom_struck)} hits")
    if has("music"):
        calls = model.calls
        checks.add("the music: the theme from the start and in every "
                   "level, Tom's from the arena until he is beaten",
                   ("start", 1) in calls and ("stop",) in calls
                   and music["frames_of"][0] > 0
                   and music["frames_of"][1] > 0, f"{calls}")


def standing_on(model, names):
    """The name of the surface under Oscar's feet, or None."""
    if not model.ground:
        return None
    sensor = (model.x >> 8) + model.k["SENSOR_X"]
    return names.get((sensor, model.y >> 8), "?")


def main():
    global PRG, LABELS, REPORT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vice", default=str(vicemon.DEFAULT_VICE))
    parser.add_argument("--stop-at", metavar="TEXT", help="stop "
                        "at the first failure of the check whose name "
                        "has TEXT (mutate_game.py: the fault caught)")
    parser.add_argument("--step", type=int, default=LAST_STEP,
                        help="a step of the book's chain, 1-13 "
                        "(chain/NN-name, assembled; 13: the game)")
    parser.add_argument("--root", type=Path, help="the step's folder "
                        "(a variant of it: variants/...)")
    parser.add_argument("--set", action="append", default=[],
                        metavar="STATEMENT", help="Python run "
                        "before the model is made: a variant's change "
                        "in the model (numbers['NAME'] = value, ...)")
    parser.add_argument("--route", type=Path, help="a route of its "
                        "own: a Python file with route(v)")
    parser.add_argument("--no-shows", action="store_true", help=""
                        "not what the step must show on its own route "
                        "(a variant's route of its own)")
    parser.add_argument("--stop-after", type=int, default=0,
                        metavar="N", help="with --stop-at: N frames "
                        "more after the failure, then a capture")
    parser.add_argument("--stop-shot", default="stopped.png",
                        help="the name of that capture")
    parser.add_argument("--coverage", action="store_true",
                        help="a checkpoint on every instruction "
                        "of the listing, taken away when it is first "
                        "executed; those never executed go into the "
                        "report")
    args = parser.parse_args()
    Tally.stop_at = args.stop_at
    Tally.stop_after = args.stop_after if args.stop_at else 0
    step = args.step
    vicemon.require(1 <= step <= LAST_STEP, "steps 1-13")

    def has(part):
        """The step has this part of the game (game_model.FIRST)."""
        return step >= game_model.FIRST[part]

    root = args.root.resolve() if args.root else step_root(step)
    evidence = "evidence"
    if root != PROJECT:
        PRG = root / "game/build/dreadcastle.prg"
        LABELS = root / "game/build/dreadcastle.lbl"
        evidence = (str(root.relative_to(PROJECT).parent / "evidence"
                        / root.name)
                    if root.is_relative_to(PROJECT)
                    else str(root / "evidence"))
        REPORT = PROJECT / evidence / "step-test.json"
        (PROJECT / evidence).mkdir(parents=True, exist_ok=True)
        reference.GENERATED = root / "game/assets/generated"
    if args.coverage:           # its own report
        REPORT = REPORT.with_name("coverage-test.json")
    # The numbers of the game (speeds, frames...) and the places of
    # its variables are the same in every step: the complete game's.
    # So the complete game must be built, at the root, as the step.
    complete = PROJECT / "game/build/dreadcastle.lbl"
    for needed, folder in ((LABELS, root), (complete, PROJECT)):
        if not needed.is_file():
            raise SystemExit(f"{needed} is missing: build {folder} "
                             "first (tools/run-game.ps1 -Mode Build)")
    labels = vicemon.load_labels(LABELS)    # the step's addresses
    numbers = vicemon.load_labels(complete)
    files = reference.load()
    for statement in args.set:      # a variant: the model changed
        exec(statement, {"numbers": numbers, "files": files,  # as the
                         "game_model": game_model,            # program
                         "reference": reference, "fight": fight})
    model = game_model.Game(files, numbers, step=step)
    TOM, TOM_2 = numbers["arena"], numbers["tom_safe"]
    names = {n: game_model.surface_names(n)
             for n in range(1, files["constants"]["LEVEL_COUNT"] + 1)}
    checks = Checks()
    tallies = {name: Tally(text) for name, text in (
        ("order", "stops in the expected order"),
        ("hud", "HUD interrupt on line 226"),
        ("registers", "$d016 and $d018 from the frame before"),
        ("hudset", "the HUD's characters from line 226 ($d018)"),
        ("frames", "frame_count +1 at each frame, turn on time"),
        ("oscar", "Oscar's variables equal the model"),
        ("state", "the camera's variables equal the model"),
        ("game", "the level's variables equal the model"),
        ("sprites", "sprite registers and pointers equal the model"),
        ("heirloom", "sprite 7, the heirloom, equals the model"),
        ("enemies", "the enemies' variables equal the model"),
        ("enemy sprites", "sprites 3-6, the enemies, equal the model"),
        ("staff", "the staff, the blow, the setting equal the model"),
        ("staff sprite", "sprite 2, the staff, equals the model "
                         "(0.10.1: its colour too)"),
        ("moon", "sprite 6, the moon of the wood, the mire and the "
                 "mountain, equals the model: still, up on the right"),
        ("moon kept", "the moon (0.10.2): in a setting with it, "
                      "place_enemies leaves its bits of $d015 and "
                      "$d010 as they were (in 0.10.1 it flickered)"),
        ("setting", "$d021, $d022, $d023 and $d01b (the moon behind) "
                    "as the setting wants them (0.8.1); (0.8.2) "
                    "$d021 black after the HUD, the setting's (blue "
                    "in the castle) after the top interrupt"),
        ("env", "the setting's tables at $c700 equal the model's"),
        ("display", "the screen on or off, the sprites on, as the model"),
        ("screens", "screens A and B equal the model"),
        ("colours", "colour RAM equals the model"),
        # these three on the C64's own variables, not the model's
        ("front", "screen in front = the level from camera / 8"),
        ("paint", "colour RAM = the level's colours from camera / 8"),
        ("back", "a ready back screen = the level one column over"),
        ("top", "colour rows 0-10 moved before line 51"),
        ("bottom", "colour rows 11-21 moved before line 139"),
        ("route", "Oscar stands where the route says"),
        ("form", "Oscar's form, smoke, energy, moths equal the model"),
        ("level", "the level in memory equals the model's"),
        ("moths", "the moths' characters: the picture of the model"),
        ("flicker", "the flickering hazards' characters in SET_SLOT "
         "(the wisps, the spikes): the picture of the model (0.8)"),
        ("slot", "SET_SLOT holds the set unpacked last, its moth's and "
         "its hazards' pictures (0.8)"),
        ("unpack", "a packed stream unpacked to its very end, a page "
         "a frame (0.8.1: up_src after its last byte)"),
        ("bar", "the HUD in both screens equals the model"),
        ("expect", "form, moths, heirlooms and events where the route says"),
        ("sid", "music and (0.10.1) sound effects: the SID registers "
                "(copy) equal the model, after a frame of music and "
                "(0.10.1) as they go into the SID"),
        ("effects", "the sound effects' voices (0.10.1) equal the "
                    "model"),
        ("silence", "(1.0) no note left on: with no song and no effect "
                    "playing, the three gates of the SID off"),
        ("tom", "Tom's bytes (0.9) equal the model"),
        ("tom sprites", "sprites 3, 4, 5, 7, Tom (0.9), equal the model"),
        ("tom page", "the page of Tom's sprites shown is his picture "
                     "(0.9)"),
        ("voices", "music: the three voices equal the model"),
        ("song", "music: the song and whether it plays (0.9.1) equal "
                 "the model"),
        ("states", "the game's state, the menu's choice, the score, "
                   "the band of words (0.10) equal the model"),
        ("title sprites", "sprites 2-5 (0.10): on the title the name "
                          "(hi-res, stretched, its colour), else not "
                          "stretched and multicolour"),
    )}
    player = player_model.Player()
    song = player.song
    moon = {"before": None, "on": 0}       # place_enemies
    music = {"start": None, "cycles": [], "synced_at": None,
             "frames_of": [0] * len(player.songs), "silent": 0,
             "calls": [],
             "fx": [], "fx_by_mode": {}}
    cycles = {"turn": [], "swap_turn": [], "transition": [],
              "arena_turn": []}                     # Tom
    cycle_log = []                  # (cycles, kind, where)
    steps_cost = {}                 # the transition's steps: the most
    seen = {"surfaces": set(), "x_register_max": 0, "camera": set(),
            "x": set(), "pictures": set(), "perches": set(),
            "events": set(), "heirlooms_shown": set(), "blank": 0,
            "moths": {}, "levels": set(), "hit_by": set(),
            "c64_levels": set(),        # the program's own
            "enemy_pictures": set(), "together": 0, "blinking": 0,
            "puffs": 0, "staff_pictures": set(), "struck": set(),
            "envs": set(), "strikes": set(), "moon_cameras": set(),
            "moon_missing": 0, "d021": set(),
            "press": set(), "play_d021": set(),
            "tom_pictures": set(), "tom_states": set(),
            "tom_flash": 0, "tom_fast": 0, "tom_kernal": None,
            "leaps": set(), "leap_now": None,
            "moon_frames": {n: 0 for n in range(len(files["envs"]))},
            "flicker_pictures": {},
            "streams": {"map": 0, "tables": 0, "set": 0, "tom": 0},
            "lines": {"top_painted": -999, "bottom_painted": -999}}
    c = files["constants"]
    (PROJECT / "evidence").mkdir(exist_ok=True)
    vice = vicemon.Vice(args.vice, PRG, PRG.parent / "game-test-vice.log",
                        evidence=evidence)
    shots, snaps, route_log = [], [], []
    stopped, start_state = None, {}
    run = {"turn": 0, "count_before": None, "shown": shown(model),
           "previous": (model.xscroll, model.shown_d018), "stream": None}
    STREAM_PAGES = {"map": c["MAP_PAGES"], "tables": c["ENV_PAGES"],
                    "set": c["SET_PAGES"], "tom": c["TOM_PAGES"]}
    try:
        monitor = vice.connect(settle=2.0)
        stops = {labels[name]: name for name in (
            "hud_write", "joy_ready", "top_painted", "bottom_painted",
            "frame_done") if name in labels}
        for address in stops:
            monitor.checkpoint(address)
        for name in ("music_play", "music_done", "music_start",
                     "music_stop", "sfx_start",
                     "place_enemies", "moon_kept"):
            if name in labels:                  # (the chain's steps)
                monitor.checkpoint(labels[name])
        patterns = ([labels[f"pat_{n}"]
                     for n in range(len(player.patterns))]
                    if has("music") else [])
        monitor.run_to(labels["frame_done"])        # the program runs
        pending = []
        cover, executed = {}, set()     # --coverage
        if args.coverage:   # every instruction, from the entry again
            taken = set(stops) | {labels[name] for name in (
                "music_play", "music_done", "music_start", "music_stop",
                "sfx_start", "place_enemies", "moon_kept")
                if name in labels}
            for address in instructions(LABELS.with_suffix(".lst")):
                if address not in taken:
                    cover[address] = monitor.checkpoint(address)
            restart(monitor, PRG, labels["entry"])
            while True:
                pc = monitor.run_until_stop()
                if pc in cover:
                    executed.add(pc)
                    monitor.delete_checkpoint(cover.pop(pc))
                elif pc == labels["frame_done"]:
                    break
        if not has("states"):       # steps 1-11: from the entry again
            restart(monitor, PRG, labels["entry"])
            while True:             # past the coverage's stops
                pc = monitor.run_until_stop()
                if pc in cover:
                    executed.add(pc)
                    monitor.delete_checkpoint(cover.pop(pc))
                elif pc == labels["hud_write"]:
                    break
            pending.append(labels["hud_write"])
        # The program has run on its own since it started: the night
        # has gone on. The test writes the model's night into the C64
        # (nothing else has changed: no joystick yet); the moths may
        # have fluttered: the model takes their picture of the moment.
        # (Steps 1-11 start again from the entry: nothing to write.)
        wings = monitor.memory(0x4800 + c["MOTH_CHAR"] * 8, 16)
        model.moth_frame = int(wings == model.moth_pictures[16:32])
        if has("staff"):
            model.slot_moth = model.moth_frame  # (both sets)
        game = monitor.memory(GAME, GAME_BYTES)
        start_state = {"night": game[1],
                       "night_time": game[2] | game[3] << 8,
                       "transition": game[8]}
        if has("states"):
            found = {name: labels[name] for name in COUNT_FRAMES}
            checks.add("the count (0.10): LEVEL CLEAR 40 frames, a step "
                       "of the night every 3, 50 after; the victory 50 "
                       "before", found == COUNT_FRAMES, f"{found}")
            states = list(monitor.memory(STATES, 12))
            checks.add("at the first stop: (0.10) the title, MUSIC, the "
                       "score 0, no band; no transition",
                       game[8] == 0 and states == model.states_bytes(),
                       f"{list(game)} states {states}")
            monitor.poke(GAME + 1, bytes([model.night,
                                          model.night_time & 255,
                                          model.night_time >> 8]))
            # The enemies have moved too, on their own (Oscar far
            # away, still): the test writes the model's into the C64.
            # And the frames counted, from 0: the frames the captures
            # wait for a picture that holds (steady) are then those of
            # the route as it was made on the model, and the enemies
            # where it found them.
            # All the places of the table, the unused ones too (in RAM
            # they hold whatever was there; in the model, 0).
            state = model.enemy_state(model.k["MAX_ENEMIES"])
            for number, values in enumerate(state):
                monitor.poke(ENEMIES + number * 8, bytes(values))
            monitor.poke(FRAME_COUNT, bytes([0]))
        vic = monitor.memory(0xD000, 0x2F)
        bank = monitor.memory(0xDD00, 1)[0] & 3
        checks.add("VIC-II bank 1 ($4000)", bank == 0b10, f"{bank:02b}")
        if has("objects"):
            checks.add("sprites 0, 1 multicolour 1 and 7, sprite 7 "
                       "yellow", vic[0x1C] & 0x83 == 0x82 and
                       vic[0x2E] & 15 == c["HEIRLOOM_COLOUR"],
                       f"$d01c={vic[0x1C]:#04x} $d02e={vic[0x2E]:#04x}")
        else:
            checks.add("sprites 0 and 1: 1 multicolour", vic[0x1C] & 3
                       == 2, f"$d01c={vic[0x1C]:#04x}")
        if has("states"):
            logo = [b & 15 for b in vic[0x29:0x2D]]
            checks.add("(0.10) the title: sprites 2-5 the name, hi-res, "
                       "stretched both ways, in its colour; sprite 6, "
                       "the moon, multicolour",
                       vic[0x1C] & 0x7C == 0x40 and vic[0x17] & 0x3C
                       == 0x3C and vic[0x1D] & 0x3C == 0x3C
                       and logo == [c["LOGO_COLOUR"]] * 4,
                       f"$d01c={vic[0x1C]:#04x} $d017={vic[0x17]:#04x} "
                       f"$d01d={vic[0x1D]:#04x} colours {logo}")
        first_types = c["ENEMY_TYPES_1"] * 256
        if has("enemies"):
            places = [(0x6000, files["enemies"][:first_types],
                       "the enemies' pictures at $6000")]
            if has("staff"):
                places.append((0x7600, files["staff"],
                               "the staff's at $7600"))
            if has("packed"):
                places.append((0x7900, files["enemies"][first_types:],
                               "the mountain's and the castle's at "
                               "$7900"))
            checks.add(", ".join(text for _, _, text in places)
                       + ": enemies.bin, staff.bin",
                       all(monitor.memory(at, len(data)) == data
                           for at, data, _ in places))
        moth = c["MOTH_CHAR"] * 8
        village = monitor.memory(0x4800, 2048)
        slot = monitor.memory(SET_SLOT, 2048)
        if has("states"):
            checks.add("the village's characters at $4800 are "
                       "charset.bin (the moth apart); (0.10) SET_SLOT "
                       "($5800) holds the set of the title's setting, "
                       "the keep's, unpacked at the start",
                       village[:moth] == files["envs"][0]["charset"][:moth]
                       and slot == model.slot() and model.slot_env == 5)
        else:
            checks.add("the village's characters at $4800 are "
                       "charset.bin (the moth apart)",
                       village[:moth] == files["envs"][0]["charset"][:moth])
        if has("packed"):
            # The packed data: in memory as written, and each
            # unpacks to its file (the maps with zeros after them).
            packed, wrong = files["packed"], []
            streams = [(f"level_map_{n}", f"level{n}.lz",
                        level + bytes(c["MAP_PAGES"] * 256 - len(level)))
                       for n, level in enumerate(files["levels"], 1)]
            for name, env in zip(reference.ENVIRONMENTS, files["envs"]):
                streams.append((f"env_packed_{name}", f"env_{name}.lz",
                                env["env_block"]))
                if name != "village":
                    streams.append((f"set_packed_{name}",
                                    f"charset_{name}.lz", env["charset"]))
            if has("tom"):
                streams.append(("tom_packed", "tom.lz", files["tom"]))
            for label, file, unpacked in streams:
                data = packed[file]
                if monitor.memory(labels[label], len(data)) != data:
                    wrong.append(f"{label} is not {file}")
                elif pack.unpack(data, len(unpacked)) != unpacked:
                    wrong.append(f"{file} does not unpack to its file")
            checks.add("the packed data in memory (0.8.1) are the .lz "
                       "files (the maps, the settings' tables, the sets "
                       "of the wood, the mire, the crags, the pass, the "
                       "keep and the hall; 0.8.2: some moved under the "
                       "KERNAL; 0.9: Tom's pictures), and each unpacks "
                       "to its file (level1.bin..., env_*.bin, "
                       "charset_*.bin, tom.bin)",
                       not wrong and len(streams) == len(packed)
                       - (0 if has("tom") else 1), ", ".join(wrong))
        else:
            # Steps 1-7 (plain.asm): the data of the first levels as
            # they are, the maps with zeros after them.
            wrong = []
            plain = [(f"level_map_{n}",
                      level + bytes(c["MAP_PAGES"] * 256 - len(level)))
                     for n, level in enumerate(files["levels"], 1)
                     if model.level_env[n - 1] < 2]
            for name, env in zip(reference.ENVIRONMENTS[:2],
                                 files["envs"]):
                plain.append((f"env_packed_{name}", env["env_block"]))
                if name != "village":
                    plain.append((f"set_packed_{name}", env["charset"]))
            for label, data in plain:
                if monitor.memory(labels[label], len(data)) != data:
                    wrong.append(label)
            checks.add("the data of levels 1-3 in memory as they are "
                       "(plain.asm): the maps with zeros after them, "
                       "the tables of the village and of the wood, the "
                       "wood's set of characters", not wrong,
                       ", ".join(wrong))
        port = monitor.read_registers()["01"]
        checks.add("$01 = $35: I/O in, BASIC and KERNAL out",
                   port & 7 == 5, f"{port:#04x}")
        sprite_data = monitor.memory(0x6800, len(files["sprites"]))
        checks.add(f"the {c['PICTURE_COUNT']} pictures and the "
                   f"{c['HEIRLOOM_KINDS']} heirlooms at $6800",
                   sprite_data == files["sprites"])
        glyphs = c["HUD_GLYPHS"] * 8
        hud_set = monitor.memory(0x5000, len(files["hudset"]))
        checks.add("the HUD's characters at $5000 are hudset.bin, its "
                   "glyphs and nothing after them (0.9: the HUD's "
                   "interrupt shows them on line 175)",
                   hud_set == files["hudset"]
                   and not any(files["hudset"][glyphs:]))
        if has("objects"):
            night = labels["NIGHT_STEPS"] * labels["NIGHT_STEP"]
            model_night = numbers["NIGHT_STEPS"] * numbers["NIGHT_STEP"]
            if model_night == 6000:
                checks.add("the night: 2 minutes (16 steps of 375 "
                           "frames, 6000 at 50 a second)", night == 6000,
                           f"{night} frames")
            else:                       # a variant's night
                checks.add(f"the night: {model_night} frames, as the "
                           "model's", night == model_night,
                           f"{night} frames")
        if has("music"):
            wrong = [f"pattern {number}"
                     for number, data in enumerate(player.patterns)
                     if monitor.memory(labels[f"pat_{number}"],
                                       len(data)) != data]
            wrong += [f"order list {number}"
                      for number, data in enumerate(player.orders)
                      if monitor.memory(labels[f"order_{number}"],
                                        len(data)) != bytes(data)]
            tempo = [v for each in player.songs for v in each["tempo"]]
            if monitor.memory(labels["tempo_table"], len(tempo)) != \
                    bytes(tempo):
                wrong.append("tempo")
            lists = bytes(3 * n for n in range(len(player.songs)))
            if monitor.memory(labels["song_lists"], len(lists)) != lists:
                wrong.append("song_lists")
            for name, values in (
                    ("ad", [i["ad"] for i in player.ins]),
                    ("sr", [i["sr"] for i in player.ins]),
                    ("wave", player.ins_wave),
                    ("pw_lo", [i["pw"] & 255 for i in player.ins]),
                    ("pw_hi", [i["pw"] >> 8 for i in player.ins]),
                    ("sweep", [i["sweep"] & 255 for i in player.ins]),
                    ("vibrato", [i["vibrato"] for i in player.ins])):
                if monitor.memory(labels[f"ins_{name}"],
                                  len(values)) != bytes(values):
                    wrong.append(f"ins_{name}")
            rows = song["rows"]
            tables = (monitor.memory(labels["wave_ctrl"], len(rows))
                      == bytes(c for c, _ in rows) and
                      monitor.memory(labels["wave_pitch"], len(rows))
                      == bytes(p for _, p in rows))
            checks.add("the songs in memory are the ones music.py "
                       "compiled (0.9.1: the theme and, under the "
                       "KERNAL, Tom's; 0.10.1: and the three jingles)",
                       not wrong and tables, f"{wrong}")
        if has("sound"):
            first = bytes(player.sfx_first)
            checks.add("the sound effects in memory, under the KERNAL, "
                       "are the ones sfx.py compiled (0.10.1): "
                       "sfx_first, sfx_data",
                       monitor.memory(labels["sfx_first"], len(first))
                       == first and
                       monitor.memory(labels["sfx_data"], len(
                           player.sfx_data)) == player.sfx_data, "")
        if has("tom"):
            checks.add("mirror_to under the KERNAL (0.9.1) is "
                       "mirror_to.bin (tom.py)",
                       monitor.memory(labels["mirror_to"], 256)
                       == files["mirror_to"], "")

        def raw_stop():
            while True:
                pc = (pending.pop() if pending
                      else monitor.run_until_stop())
                if pc in cover:         # first time: away
                    executed.add(pc)
                    monitor.delete_checkpoint(cover.pop(pc))
                    continue
                if args.coverage:
                    executed.add(pc)
                return pc

        def next_stop():
            """The next stop of the main loop or of the HUD interrupt;
            the frames of music met on the way are checked here."""
            while True:
                pc = raw_stop()
                if pc == labels.get("music_play"):
                    count = monitor.memory(FRAME_COUNT, 1)[0]
                    music["start"] = (count, monitor.read_registers())
                    if music["synced_at"] is not None:
                        shadow = list(monitor.memory(0xA0, 25))
                        tallies["sid"](
                            shadow == player.shadow,
                            f"into the SID, turn {run['turn']}",
                            f"{shadow} model {player.shadow}")
                    continue
                if pc == labels.get("music_start"):
                    number = monitor.read_registers()["A"]
                    music["calls"].append((run["turn"], "start", number))
                    if music["synced_at"] is not None:
                        player.start(number)
                    continue
                if pc == labels.get("music_stop"):
                    music["calls"].append((run["turn"], "stop"))
                    if music["synced_at"] is not None:
                        player.stop()
                    continue
                if pc == labels.get("place_enemies"):
                    moon["before"] = (monitor.memory(0xD010, 1)[0],
                                      monitor.memory(0xD015, 1)[0])
                    continue
                if pc == labels.get("moon_kept"):
                    env = monitor.memory(labels["env"], 1)[0]
                    bit = monitor.memory(labels["env_moon"] + env, 1)[0]
                    after = (monitor.memory(0xD010, 1)[0],
                             monitor.memory(0xD015, 1)[0])
                    if bit:
                        before = moon["before"]
                        tallies["moon kept"](
                            [b & bit for b in before]
                            == [a & bit for a in after],
                            f"turn {run['turn']}",
                            f"$d010, $d015 {before} then {after}")
                        moon["on"] += bool(before[1] & bit)
                    continue
                if pc == labels.get("sfx_start"):
                    effect = monitor.read_registers()["A"]
                    mode = monitor.memory(STATES + 1, 1)[0]
                    music["fx"].append((run["turn"], effect))
                    sounded = (music["synced_at"] is not None
                               and player.sfx_start(effect, mode))
                    tally = music["fx_by_mode"].setdefault(mode, [0, 0])
                    tally[0] += 1
                    tally[1] += bool(sounded)
                    continue
                if pc != labels.get("music_done"):
                    return pc
                count = monitor.memory(FRAME_COUNT, 1)[0]
                registers = monitor.read_registers()
                if music["start"] is not None:
                    begun, at = music["start"]
                    music["cycles"].append(
                        (position(count, begun, registers["LIN"]) * 63
                         + registers["CYC"]) -
                        (position(begun, begun, at["LIN"]) * 63
                         + at["CYC"]))
                frame = int.from_bytes(monitor.memory(0x64, 2), "little")
                if music["synced_at"] is None:
                    music["synced_at"] = frame
                    for _ in range(frame):
                        player.play()
                else:
                    player.play()
                if player.on:
                    music["frames_of"][player.number] += 1
                else:
                    music["silent"] += 1
                where = f"music frame {frame}"
                shadow = list(monitor.memory(0xA0, 25))
                tallies["sid"](shadow == player.shadow, where,
                               f"{shadow} model {player.shadow}")
                state = (list(monitor.memory(0x62, 4)),
                         list(monitor.memory(0x6A, 2)),
                         list(monitor.memory(0x70, 45)))
                tallies["voices"](state == player.state(patterns), where,
                                  f"{state} model {player.state(patterns)}")
                if not player.on and not any(       # silence
                        fx["pos"] for fx in player.fx):
                    gates = [shadow[4], shadow[11], shadow[18]]
                    tallies["silence"](not any(g & 1 for g in gates),
                                       where, f"controls {gates}")
                effects = list(monitor.memory(SFX_VARS, 10))
                if has("sound"):
                    tallies["effects"](
                        effects == player.sfx_state(), where,
                        f"{effects} model {player.sfx_state()}")
        moth_char, hazard_char = c["MOTH_CHAR"] * 8, c["FLICKER_CHAR"] * 8

        def one_frame(what, joy):
            """One turn of the main loop, checked."""
            if Tally.stopping:      # --stop-after: the capture
                if Tally.stopping[1] == 0:
                    take(args.stop_shot)
                    raise Stopped(Tally.stopping[0])
                Tally.stopping[1] -= 1
            run["turn"] += 1
            where = f"frame {run['turn']} ({what})"
            pc = next_stop()
            tallies["order"](stops.get(pc) == "hud_write", where,
                             stops.get(pc, hex(pc)))
            registers = monitor.read_registers()
            tallies["hud"](registers["LIN"] == 226, where,
                           f"line {registers['LIN']}")
            d016, d018 = monitor.memory(0xD016, 3)[0::2]
            if not model.trans:     # (a transition can end late)
                tallies["registers"](
                    (d016 & 0x1F, d018 & 0xFE) == run["previous"], where,
                    f"{d016:#04x} {d018:#04x}, model {run['previous']}")
            if "joy_ready" in labels:       # (step 1: no joystick)
                pc = next_stop()
                tallies["order"](stops.get(pc) == "joy_ready", where,
                                 stops.get(pc, hex(pc)))
            start = monitor.memory(FRAME_COUNT, 1)[0]
            registers = monitor.read_registers()
            began = clock(start, start, registers)
            if "joy_ready" in labels:
                d018 = monitor.memory(0xD018, 1)[0]
                tallies["hudset"](d018 & 0xFE == 0x04, where,
                                  f"$d018 {d018:#04x}")
            before = run["count_before"]
            tallies["frames"](
                start == (1 if before is None else (before + 1) & 255)
                and 226 <= registers["LIN"] <= 229, where,
                f"count {start} after {before}, "
                f"line {registers['LIN']}")
            run["count_before"] = start
            if "joy_ready" in labels:
                monitor.poke(STATE + 11, bytes([joy]))
            in_transition = model.trans > 0
            step = (STEP_NAMES[game_model.TRANS_STEPS[model.trans - 1]]
                    if in_transition else None)
            if step == "page" and model.stream is not None:
                step = "page of the " + model.stream[0]
            run["shown"] = shown(model)     # what VICE shows next
            env_before = model.env      # for $d021
            model.turn(joy, start)
            if model.swapped:
                for name in ("top_painted", "bottom_painted"):
                    pc = next_stop()
                    tallies["order"](stops.get(pc) == name, where,
                                     stops.get(pc, hex(pc)))
                    count = monitor.memory(FRAME_COUNT, 1)[0]
                    at = position(count, start,
                                  monitor.read_registers()["LIN"])
                    limit = (FIRST_ROW_LINE if name == "top_painted"
                             else ROW_11_LINE)
                    seen["lines"][name] = max(seen["lines"][name], at)
                    tallies["top" if name == "top_painted"
                            else "bottom"](at < limit, where,
                                           f"line {at}")
            pc = next_stop()
            tallies["order"](stops.get(pc) == "frame_done", where,
                             stops.get(pc, hex(pc)))
            if "joy_ready" not in labels:   # step 1: the HUD's set now
                d018 = monitor.memory(0xD018, 1)[0]
                tallies["hudset"](d018 & 0xFE == 0x04, where,
                                  f"$d018 {d018:#04x}")
            count = monitor.memory(FRAME_COUNT, 1)[0]
            registers = monitor.read_registers()
            at = position(count, start, registers["LIN"])
            kind = ("transition" if in_transition else
                    "swap_turn" if model.swapped else "turn")
            spent = clock(count, start, registers) - began
            cycles[kind].append(spent)
            if model.arena and not in_transition:
                cycles["arena_turn"].append(spent)
            if step is not None:            # by step
                steps_cost[step] = max(steps_cost.get(step, 0), spent)
            cycle_log.append((spent, kind, where))
            tallies["frames"](at < 226, where,
                              f"turn ends on line {at}")
            oscar = list(monitor.memory(OSCAR, OSCAR_BYTES))
            tallies["oscar"](same(oscar, model.oscar_state()), where,
                             f"{oscar} model {model.oscar_state()}")
            if has("bat"):
                form = list(monitor.memory(FORM, FORM_BYTES))
                tallies["form"](form == model.form_state(), where,
                                f"{form} model {model.form_state()}")
            game = list(monitor.memory(GAME, GAME_BYTES))
            expected = model.level_state()
            if expected[9] is None:                 # never set yet
                expected[9] = game[9]
            tallies["game"](same(game, expected), where,
                            f"{game} model {expected}")
            seen["c64_levels"].add(game[12] + 1)   # its level_no
            seen["c64_level_no"] = game[12]
            staff = list(monitor.memory(STAFF, STAFF_BYTES))
            tallies["staff"](same(staff, model.staff_state()), where,
                             f"{staff} model {model.staff_state()}")
            seen["envs"].add(model.env)
            stream = model.stream           # the unpacking
            if stream is not None and stream is not run["stream"] and \
                    stream[1] == STREAM_PAGES[stream[0]] and \
                    has("packed"):
                run["stream"] = stream
                label, file = stream_of(model, stream[0])
                end = labels[label] + len(files["packed"][file])
                found = int.from_bytes(monitor.memory(labels["up_src"], 2),
                                       "little")
                tallies["unpack"](found == end, where,
                                  f"{file}: {found:#06x}, end {end:#06x}")
                seen["streams"][stream[0]] += 1
            memory = monitor.memory(STATE, 13)
            actual = list(memory[0:9]) + [memory[11]]
            tallies["state"](same(actual, model.scroll_state()), where,
                             f"{actual} model {model.scroll_state()}")
            vic = monitor.memory(0xD000, 0x16)
            d011 = monitor.memory(0xD011, 1)[0]
            pointers = (tuple(monitor.memory(0x43F8, 8)),
                        tuple(monitor.memory(0x47F8, 8)))
            display = (bool(d011 & 0x10), vic[0x15])
            tallies["display"](display == (model.display_on,
                                           model.sprites_on), where,
                               f"{display} model "
                               f"{(model.display_on, model.sprites_on)}")
            registers = tuple(b & 15 for b in monitor.memory(0xD021, 3))
            registers += (monitor.memory(0xD01B, 1)[0],)
            # $d021: black if the top interrupt has not come
            # yet in this turn; else the setting's, the one before if
            # the setting changed in the turn (next_env may come
            # before or after the interrupt); play_d021 the setting's.
            top = count != start
            wanted = [model.setting_registers(top)]
            if top and env_before != model.env:
                wanted.append((c[f"ENV{env_before}_D021"],)
                              + wanted[0][1:])
            play = monitor.memory(PLAY_D021, 1)[0]
            if not has("castle"):       # play_d021: from step 9
                play = model.play_d021()
            tallies["setting"](registers in wanted
                               and play == model.play_d021(), where,
                               f"{registers} play_d021 {play} model "
                               f"{wanted} {model.play_d021()}")
            seen["d021"].add(registers[0])
            seen["play_d021"].add(play)         # dawn's too
            if not model.display_on:
                seen["blank"] += 1
            lines_block = 160 + model.placed * 2
            expected = (model.sprite_x & 255, model.sprite_y,
                        3 if model.sprite_x > 255 else 0,
                        ((lines_block, lines_block + 1),) * 2)
            found = (vic[0], vic[1], vic[0x10] & 3,
                     (pointers[0][:2], pointers[1][:2]))
            tallies["sprites"](found == expected and vic[2] == vic[0]
                               and vic[3] == vic[1], where,
                               f"{found} model {expected}")
            in_memory = monitor.memory(ENEMIES, ENEMY_ARRAYS * 8)
            places = model.k["MAX_ENEMIES"]     # all, used or not
            found = [list(in_memory[n * 8:n * 8 + places])
                     for n in range(ENEMY_ARRAYS)]
            expected = model.enemy_state(places)
            if not has("states"):
                # Steps 6-11: the table is not cleared before the
                # first level; a slot no level has reset yet holds
                # what was in memory (any value).
                expected = [[v if n < model.enemy_slots else None
                             for n, v in enumerate(row)]
                            for row in expected]
            if not has("staff"):        # en_gone: from step 7
                found, expected = found[:-1], expected[:-1]
            if has("enemies"):
                tallies["enemies"](
                    len(found) == len(expected)
                    and all(same(f, e) for f, e in zip(found, expected)),
                    where, f"{found} model {expected}")
            colours = monitor.memory(0xD02A, 4)
            wrong = []
            if vic[0x10] & 0x78 != model.d010 & 0x78 and \
                    has("enemies"):
                wrong.append(f"$d010 {vic[0x10]:#04x}")
            for slot, (x, y, block, colour, type_, _) in enumerate(
                    model.enemy_sprites):
                found = (vic[6 + 2 * slot], vic[7 + 2 * slot],
                         pointers[0][3 + slot], pointers[1][3 + slot],
                         colours[slot] & 15)
                if found != (x & 255, y, block, block, colour):
                    wrong.append(f"slot {slot}: {found}")
                picture = block - model.type_block(type_)
                if 0 <= picture < 4:
                    seen["enemy_pictures"].add((type_, picture))
                else:
                    seen["puffs"] += 1
            seen["together"] = max(seen["together"],
                                   len(model.enemy_sprites))
            if has("enemies"):
                tallies["enemy sprites"](not wrong, where,
                                         ", ".join(wrong))
            # The game's states; the title's sprites.
            if model.game_state == game_model.ST_TITLE:
                seen["press"].add(model.hud_colours[c["PRESS_CELL"]
                                                    - 880])
            if has("states"):
                found = list(monitor.memory(STATES, 12))
                tallies["states"](found == model.states_bytes(), where,
                                  f"{found} model "
                                  f"{model.states_bytes()}")
            if model.logo_on:
                k = model.k
                wanted = [(c["LOGO_X"] + n * c["LOGO_STEP"], c["LOGO_Y"],
                           k["LOGO_BLOCK"] + n, c["LOGO_COLOUR"])
                          for n in range(c["LOGO_SPRITES"])]
                colours = [b & 15 for b in monitor.memory(0xD029, 4)]
                expanded = monitor.memory(0xD017, 7)
                found = [(vic[4 + 2 * n], vic[5 + 2 * n],
                          pointers[0][2 + n], colours[n])
                         for n in range(4)]
                good = (found == wanted
                        and pointers[0][2:6] == pointers[1][2:6]
                        and vic[0x10] & 0x3C == 0
                        and expanded[0] & 0x3C == 0x3C
                        and expanded[6] & 0x3C == 0x3C
                        and expanded[5] & 0x3C == 0)
            else:
                expanded = monitor.memory(0xD017, 7)
                good = (expanded[0] & 0x3C == 0 and expanded[6] & 0x3C
                        == 0 and expanded[5] & 0x7C == 0x7C)
                found = list(expanded)
            tallies["title sprites"](good, where, f"{found}")
            if model.sprites_on & 4 and not model.logo_on:
                x, y, block = model.staff_sprite
                expected = (x & 255, y, 4 if x > 255 else 0,
                            (block, block), c["STAFF_COLOUR"])
                found = (vic[4], vic[5], vic[0x10] & 4,
                         (pointers[0][2], pointers[1][2]),
                         monitor.memory(0xD029, 1)[0] & 15)
                tallies["staff sprite"](found == expected, where,
                                        f"{found} model {expected}")
                seen["staff_pictures"].add(
                    block - model.k["STAFF_BLOCKS"])
            seen["struck"].update(t for _, t, _, _ in model.struck)
            seen["strikes"].update((face, ground)
                                   for _, _, face, ground in model.struck)
            if not model.trans and model.protect and not (
                    model.sprites_on & 3):
                seen["blinking"] += 1
            seen["hit_by"].update(kind for _, kind in model.hit_by)
            if model.sprites_on & 0x80 and not model.arena:
                x, y, block, kind_shown = model.sprite7
                expected = (x & 255, y, 0x80 if x > 255 else 0,
                            (block, block))
                found = (vic[0x0E], vic[0x0F], vic[0x10] & 0x80,
                         (pointers[0][7], pointers[1][7]))
                tallies["heirloom"](found == expected, where,
                                    f"{found} model {expected}")
                seen["heirlooms_shown"].add(kind_shown)
            if model.moon_sprite is not None and model.sprites_on & 0x40:
                x, y, block = model.moon_sprite
                colour = monitor.memory(0xD02D, 1)[0] & 15
                expected = (x & 255, y, 0x40 if x > 255 else 0,
                            (block, block), c["MOON_COLOUR"])
                found = (vic[0x0C], vic[0x0D], vic[0x10] & 0x40,
                         (pointers[0][6], pointers[1][6]), colour)
                tallies["moon"](found == expected, where,
                                f"{found} model {expected}")
                seen["moon_cameras"].add(model.camera)
                seen["moon_frames"][model.env] += 1
            if (model.display_on and model.moon_here()
                    and not model.sprites_on & 0x40):
                seen["moon_missing"] += 1
            # Tom's leaps, measured: their frames (his state
            # a leap at the frame's end) and how high he goes.
            if model.arena:
                if model.tom_state == model.k["TS_LEAP"]:
                    leap = seen["leap_now"] or [0, 0]
                    leap[0] += 1
                    leap[1] = max(leap[1], model.c["START_Y"]
                                  - (model.tom_y >> 8))
                    seen["leap_now"] = leap
                elif seen["leap_now"]:
                    if model.tom_state == model.k["TS_LAND"]:
                        seen["leaps"].add(tuple(seen["leap_now"]))
                    seen["leap_now"] = None
            # The song, and whether it plays; a
            # jingle stops by itself, at its end: whether it plays is
            # then the player model's (it follows the program's calls
            # and counts the frames of music).
            found = list(monitor.memory(0x6A, 2))
            on = (model.mus_on if model.mus_song < game_model.SONG_CLEAR
                  else player.on)
            if has("music"):
                tallies["song"](found == [model.mus_song, on],
                                where, f"{found} model "
                                f"{[model.mus_song, on]}")
            # Tom: his bytes; his sprites and the page shown.
            found = (list(monitor.memory(TOM, TOM_BYTES)),
                     list(monitor.memory(TOM_2, TOM_2_BYTES)))
            expected = model.tom_state_bytes()
            if has("tom"):
                tallies["tom"](found == expected, where,
                               f"{found} model {expected}")
            if model.arena and model.tom_sprites and \
                    model.sprites_on & 0xB8 == 0xB8:
                tom_colours = monitor.memory(0xD02A, 5)
                wrong = []
                for (x, y, block, colour), slot in zip(
                        model.tom_sprites, (3, 4, 5, 7)):
                    found = (vic[2 * slot] if slot < 7 else vic[0x0E],
                             vic[2 * slot + 1] if slot < 7
                             else vic[0x0F],
                             vic[0x10] >> slot & 1,
                             pointers[0][slot], pointers[1][slot],
                             tom_colours[slot - 3] & 15)
                    if found != (x & 255, y, x >> 8, block, block,
                                 colour):
                        wrong.append(f"sprite {slot}: {found}")
                tallies["tom sprites"](not wrong, where, ", ".join(wrong))
                page = monitor.memory(TOM_SPRITES + model.tom_front * 256,
                                      256)
                picture = reference.tom_picture(
                    files, model.tom_pages[model.tom_front])
                tallies["tom page"](
                    reference.shown_bytes(page)
                    == reference.shown_bytes(picture), where,
                    f"picture {model.tom_pages[model.tom_front]}")
                seen["tom_pictures"].add(model.tom_pages[model.tom_front])
                seen["tom_states"].add(model.tom_state)
                if model.tom_flash & 2:
                    seen["tom_flash"] += 1
                if model.tom_fast():
                    seen["tom_fast"] += 1
                if not seen["tom_kernal"]:
                    seen["tom_kernal"] = check_kernal(monitor, files, c,
                                                      labels)
            seen["x_register_max"] = max(seen["x_register_max"],
                                         model.sprite_x)
            seen["camera"].add(model.camera)
            seen["x"].add(model.x >> 8)
            seen["pictures"].add(model.picture)
            level = model.level_no + 1
            seen["levels"].add(level)
            if not model.trans:     # the count is the level's
                seen["moths"][level] = max(seen["moths"].get(level, 0),
                                           model.moths_eaten)
            screens = [model.cells(monitor.memory(base, 880))
                       for base in (0x4000, 0x4400)]
            colours = model.cells(bytes(
                b & 15 for b in monitor.memory(0xD800, 880)))
            for index in (0, 1):
                found = difference(screens[index],
                                   model.screens[index])
                tallies["screens"](not found, where,
                                   f"screen {'AB'[index]}: {found}")
            found = difference(colours, model.colours)
            tallies["colours"](not found, where, found)
            in_memory = monitor.memory(LEVEL, len(model.level))
            tallies["level"](in_memory == bytes(model.level), where,
                             "the level differs")
            if not model.trans and model.game_state in (
                    game_model.ST_PLAY, game_model.ST_TITLE):
                camera, front = memory[0] | memory[1] << 8, memory[2]
                prep_dir, prep_stage = memory[3], memory[4]
                cells, paint = model.view(camera >> 3)
                found = difference(screens[front & 1], cells)
                tallies["front"](not found, where, found)
                found = difference(colours, paint)
                tallies["paint"](not found, where, found)
                if prep_stage == 3:
                    step = 1 if prep_dir == game_model.RIGHT else -1
                    cells, _ = model.view((camera >> 3) + step)
                    found = difference(screens[1 - (front & 1)], cells)
                    tallies["back"](not found, where, found)
            wings = monitor.memory(0x4800 + moth_char, 16)
            tallies["moths"](wings == model.charset(0)[
                moth_char:moth_char + 16], where,
                f"picture {model.moth_frame} expected at $4800")
            slot = model.slot()         # SET_SLOT: its moth,
            wings = monitor.memory(SET_SLOT + moth_char, 16)
            if has("staff") and model.slot_moth_known:  # (from 7)
                tallies["moths"](wings == slot[moth_char:moth_char + 16],
                                 where, f"picture {model.slot_moth} "
                                 "expected in SET_SLOT")
            if model.slot_env is not None and \
                    c["FLICKER_SETTINGS"] >> model.slot_env & 1:
                found = monitor.memory(SET_SLOT + hazard_char, 64)
                tallies["flicker"](
                    found == slot[hazard_char:hazard_char + 64], where,
                    f"picture {model.slot_flicker} expected")
                if model.env == model.slot_env and not model.trans:
                    seen["flicker_pictures"].setdefault(
                        model.env, set()).add(model.slot_flicker)
            huds = (monitor.memory(0x4370, 120),
                    monitor.memory(0x4770, 120),
                    bytes(b & 15 for b in monitor.memory(0xDB70, 120)))
            hud = model.hud()
            tallies["bar"](huds == (hud[:120], hud[:120], hud[120:]),
                           where, "the HUD differs")
            run["previous"] = (model.xscroll, model.shown_d018)

        fighter = fight.Fighter(model)      # the fight
        def take(shot):
            """A capture now, the frame just drawn."""
            # VICE's capture is the last whole frame: drawn with what
            # the turn before this one left (measured).
            before = run["shown"]
            taken = vice.screenshot(shot)
            taken.update({key: before[key] for key in (
                "camera", "oscar", "heirloom", "enemies", "staff",
                "moon", "env", "tom", "logo", "band", "d021")})
            taken["turn"] = run["turn"]
            shots.append(taken)
            snaps.append(dict(reference.env_files(files, before["env"]),
                              level=before["level"],
                              charset=before["charset"],
                              hud=before["hud"], d021=before["d021"]))
            pc = monitor.read_registers()["PC"]
            if pc != labels["frame_done"]:
                pending.append(pc)

        def late_shot():
            """A capture that waits for a picture that holds,
            while the route goes on."""
            if run["due"] is None:
                return
            name, since, step = run["due"]
            if steady(model, run["count_before"]):
                take(name)
                run["due"] = None
            elif model.trans or model.frame - since > SHOT_LATE:
                tallies["route"](False, f"capture after '{step}'",
                                 f"no picture that holds for {name}")
                run["due"] = None

        run["due"] = None
        route = ((ROUTE if has("sound") else step_12_route())
                 if has("states") else step_route(step))
        if args.route:                  # a variant's own route
            route = own_route(args.route)
        for entry in route:
            what, frames, joy, where_end, shot = entry[:5]
            if joy is FIGHT_AGAIN:          # a new fight
                fighter = fight.Fighter(model)
                joy = FIGHT
            if joy is FIGHT:
                joy = fighter
            expect = dict(entry[5]) if len(entry) > 5 else {}
            for name, value in expect.pop("poke", {}).items():
                address, size = POKES[name]
                monitor.poke(address, value.to_bytes(size, "little"))
                if name == "frame_count":   # the count goes on
                    run["count_before"] = value
                else:
                    setattr(model, name, value)
            if frames == NEXT_LEVEL:
                if "gate_rest" not in run:  # no gate passed: the
                    tallies["route"](False, f"'{what}'",  # route
                                     "no gate before")    # is lost
                    run["gate_rest"] = 0
                    run["gate_frame"] = model.frame
                    run["count_before"] = run["count_before"] or 0
                frames = model.k["TRANS_FRAMES"] + run["gate_rest"]
                # frame_count is no longer written: the moths'
                # wings and the hazards' pictures (only pictures) as
                # the count leaves them.
            camera_from, x_from = model.camera, model.x >> 8
            landed_from, events_from = len(model.landed), len(model.events)
            if isinstance(frames, Until):   # until something
                until, frames = frames, 0
                while not until.test(model):
                    if frames == until.most:
                        tallies["route"](False, f"'{what}'",
                                         f"not {until} in {frames}")
                        break
                    one_frame(what, joystick(joy, frames))
                    late_shot()
                    frames += 1
            else:
                for frame in range(frames):
                    one_frame(what, joystick(joy, frame))
                    late_shot()
                    if (shot and frame >= frames - SHOT_WINDOW
                            and steady(model, run["count_before"])):
                        take(shot)          # in the step's end
                        shot = None
            if shot:                        # later, as soon as
                run["due"] = (shot, model.frame, what)  # it holds
            standing = standing_on(model, names[model.level_no + 1])
            tallies["route"](where_end is None or standing == where_end,
                             f"end of '{what}'",
                             f"on {standing}, not {where_end}")
            events = [e for _, e in model.events[events_from:]]
            if (model.game_state == game_model.ST_WON
                    and model.state_phase == 1
                    and "score_won" not in seen):
                happened = [e for _, e in model.events]
                seen["score_won"] = {
                    "score": model.score,
                    "struck": happened.count("struck"),
                    "heirlooms": sum(e.startswith("heirloom ")
                                     for e in happened),
                    "moths": sum(e.startswith("moth ")
                                 for e in happened),
                    "tom": happened.count("tom beaten"),
                    "night_steps": model.counted}
            if what.startswith("in the village again"):
                seen["new_game"] = {"level": model.level_no + 1,
                                    "score": model.score,
                                    "staff": model.has_staff,
                                    "hud": bytes(model.hud_bytes[:80])
                                    == files["hud"][:80]}
            gate = [f for f, e in model.events[events_from:]
                    if e == "through the gate"]
            if gate:                        # see NEXT_LEVEL
                run["gate_rest"] = model.frame - gate[-1]
                run["gate_frame"] = gate[-1]
            wrong = []
            if "form" in expect and model.form != expect["form"]:
                wrong.append(f"form {model.form}")
            if "moths" in expect and model.moths_eaten != expect["moths"]:
                wrong.append(f"moths {model.moths_eaten}")
            if "got" in expect and model.got != expect["got"]:
                wrong.append(f"heirlooms {model.got}")
            if "event" in expect and expect["event"] not in events:
                wrong.append(f"events {events}")
            if expect:
                tallies["expect"](not wrong, f"end of '{what}'",
                                  ", ".join(wrong))
            if not model.trans:     # the tables of the setting
                tables = monitor.memory(ENV_TABLES, ENV_BYTES)
                tallies["env"](tables == files["envs"][model.env]
                               ["env_block"], f"end of '{what}'",
                               f"setting {model.env}")
                in_slot = monitor.memory(SET_SLOT, 2048)  # and
                if model.slot_env is not None or has("states"):
                    tallies["slot"](in_slot == model.slot(),  # SET_SLOT
                                    f"end of '{what}'",
                                    f"the set of setting "
                                    f"{model.slot_env}")
            landings = [(names[n].get((x, y), "?"), who, n)
                        for _, x, y, who, n in model.landed[landed_from:]]
            seen["surfaces"].update((n, name) for name, who, n in landings
                                    if who == "vampire")
            seen["perches"].update(name for name, who, _ in landings
                                   if who == "bat")
            seen["events"].update(events)
            route_log.append({
                "what": what, "frames": frames,
                "joystick": joy if isinstance(joy, int) else str(joy),
                "tom": ({"state": model.tom_state,
                         "hits_left": model.tom_hits,
                         "x": model.tom_x >> 8}
                        if model.arena else None),
                "x_from": x_from, "x_to": model.x >> 8,
                "feet": model.y >> 8, "standing_on": standing,
                "level": model.level_no + 1,
                "landed_on": [name for name, _, _ in landings],
                "form": ("vampire", "bat")[model.form],
                "energy": round(model.energy / 256, 2),
                "moths_eaten": model.moths_eaten,
                "heirlooms": model.got,
                "events": {e: events.count(e) for e in dict.fromkeys(events)},
                "camera_from": camera_from, "camera_to": model.camera,
                "camera_waits": sum(model.holds),
                # for the facts of the variants
                "frame": model.frame, "health": model.health,
                "protect": model.protect,
                "night": getattr(model, "night", None),
                "night_time": getattr(model, "night_time", None),
                "score": model.score,
                "staff": model.has_staff,
                "enemy_x": [x >> 8 for x in model.en_x[
                    :len(model.objects["enemies"])]],
                "picture": model.picture, "blow": model.blow})
        # the HUD's rows as the program left them, for the facts
        run["hud_end"] = list(monitor.memory(0x4370, 120))
    except RuntimeError as error:   # the C64 stopped answering
        stopped = f"{error} (frame {run['turn']})"
    except Stopped as early:        # --stop-at: caught; no more
        tally = early.args[0]
        report = {"program": report_path(PRG),
                  "stopped_at": run["turn"],
                  "screenshots": shots,           # --stop-after
                  "checks": [{"check": f"{tally.name} (the route "
                              f"stopped at its first failure)",
                              "pass": False, "detail": tally.first}],
                  "result": "FAIL"}
        with open(REPORT, "w", encoding="utf-8", newline="\n") as file:
            file.write(json.dumps(report, indent=2) + "\n")
        print(f"FAIL {tally.name}: {tally.first} (stopped)")
        return 1
    finally:
        vice.close()
    turn = run["turn"]
    checks.add("the program ran the whole route: every stop reached",
               stopped is None, stopped or "")
    for tally in tallies.values():
        if tally.count or step == LAST_STEP:    # those of the step
            tally.report(checks)
    if args.no_shows:           # a route of its own
        pass
    elif has("states"):        # the game: its title, its four games
        checks.add("the theme played through its loop (every voice back "
                   "to its loop entry)", min(player.loops[0]) >= 1,
                   f"loops {player.loops}")
        # Tom's theme: started when the arena is shown, stopped
        # when Tom is beaten; the theme from its start in every
        # level, stopped at every gate (the count), on the title as the
        # menu says; the program's calls as the model's.
        calls = [call[1:] for call in music["calls"]]
        clear, won, dawn = (game_model.SONG_CLEAR, game_model.SONG_WON,
                            game_model.SONG_DAWN)
        # The first game with SOUND FX: the menu, the seven gates,
        # the arena, Tom beaten, the victory, the title; the second with
        # MUSIC: the menu, level 1, level 8, the arena, Tom's theme, the
        # victory, the title; the third with SOUND FX: the menu, dawn,
        # the title; the fourth with SILENT: the menu, the title.
        wanted = ([("stop",)] * 3                       # SOUND FX ...
                  + [("start", clear)] * 7              # the seven gates
                  + [("stop",), ("stop",)]              # door, Tom beaten
                  + [("start", won), ("stop",)]         # victory, title
                  + [("start", 0)] * 3                  # MUSIC, 1, 8
                  + [("stop",), ("start", 1), ("stop",)]    # Tom's
                  + [("start", won), ("start", 0)]      # victory, title
                  + [("stop",), ("start", dawn), ("stop",)]     # SOUND FX
                  + [("stop",), ("stop",)])             # SILENT
        if not has("sound"):            # step 12: no jingles yet
            wanted = [call for call in wanted
                      if call not in (("start", clear), ("start", won),
                                      ("start", dawn))]
        checks.add("the songs: (0.10) the menu's choices (no music with "
                   "SOUND FX and SILENT, the theme again with MUSIC), the "
                   "theme from its start in a level with MUSIC; Tom's from "
                   "the arena shown until he is beaten; (0.10.1) the "
                   "jingles at the gates, at the victory and at dawn with "
                   "MUSIC and SOUND FX, none with SILENT (1.0: dawn in the "
                   "fourth game): the program's calls, the model's",
                   calls == model.calls == wanted
                   and {"boss theme", "tom beaten", "theme", "silence"}
                   <= seen["events"]
                   and music["frames_of"][1] > 0 and music["silent"] > 0,
                   f"calls {calls}, model {model.calls}, frames "
                   f"{music['frames_of']}, silent {music['silent']}")
        jingles = [clear] * 7 + [won, won, dawn] if has("sound") else []
        checks.add("(0.10.1) the jingles play to their end and the player "
                   "stops by itself (SONG_END): (1.0) seven of the gate, "
                   "the victory's twice, dawn's; their frames as music.py "
                   "counts them",
                   player.ended == jingles
                   and all(music["frames_of"][n]
                           >= jingles.count(n) * player.songs[n]["frames"]
                           for n in (clear, won, dawn)),
                   f"ended {player.ended}, frames {music['frames_of']}")
        fx = [effect for _, effect in music["fx"]]
        model_fx = [effect for _, effect in model.fx_calls]
        every = set(range(len(game_model.FX)))
        by_mode = music["fx_by_mode"]
        if has("sound"):
            checks.add(
                "(0.10.1) the sound effects: the program calls "
                "sfx_start where the model does, in the same order; all "
                "fifteen sound with SOUND FX ((1.0) the first game, the "
                "third); called with MUSIC and SILENT, none sounds",
                fx == model_fx and set(player.fx_started) == every
                and by_mode.get(game_model.SOUND_FX, [0, 0])[1] > 0
                and by_mode.get(game_model.MUSIC, [0, 1])[0] > 0
                and by_mode.get(game_model.MUSIC, [0, 1])[1] == 0
                and by_mode.get(game_model.SILENT, [0, 1])[0] > 0
                and by_mode.get(game_model.SILENT, [0, 1])[1] == 0,
                f"{len(fx)} calls (model {len(model_fx)}), sounded "
                f"{sorted(set(player.fx_started))}, by mode {by_mode}")
        checks.add("a frame of music under 2500 cycles",
                   max(music["cycles"], default=0) < 2500,
                   f"{max(music['cycles'], default=0)}")
        missing = [(n, name) for n, names_of in SURFACES.items()
                   for name in names_of if (n, name) not in seen["surfaces"]]
        checks.add("Oscar lands on the surfaces of the route, in the eight "
                   "levels", not missing, f"never on {missing}")
        count = c["LEVEL_COUNT"]
        every = set(range(1, count + 1))
        checks.add(f"the {count} levels played: through the gate of each "
                   "(0.8.2: by the model and by the program); (0.10) at the "
                   "end the title, level 7's door",
                   seen["levels"] == every == seen["c64_levels"]
                   and model.level_no == c["TITLE_LEVEL"]
                   and seen.get("c64_level_no") == c["TITLE_LEVEL"]
                   and seen["events"] >= {"next"},
                   f"levels {sorted(seen['levels'])}, the program's "
                   f"{sorted(seen['c64_levels'])}")
        moons = [n for n in range(len(files["envs"]))
                 if c["MOON_SETTINGS"] >> n & 1]
        checks.add("the moon: in the wood, the mire, the crags, the pass, "
                   "at the castle and in it at every frame of the screen "
                   "on, still whatever the camera; never in the village",
                   seen["moon_missing"] == 0 and seen["moon_frames"][0] == 0
                   and moons == [1, 2, 3, 4, 5, 6]
                   and all(seen["moon_frames"][n] > 0 for n in moons)
                   and len(seen["moon_cameras"]) >= 100,
                   f"{seen['moon_frames']} frames, "
                   f"{len(seen['moon_cameras'])} cameras, "
                   f"{seen['moon_missing']} without it")
        checks.add("the moon (0.10.2): place_enemies met with the moon on "
                   "in more than a thousand turns",
                   moon["on"] > 1000, f"{moon['on']} turns")
        checks.add("the seven settings: the village's tables and "
                   "characters, the wood's, the mire's, the crags', the "
                   "pass's, the keep's, the hall's (their sets unpacked "
                   "into SET_SLOT)",
                   seen["envs"] == set(range(len(files["envs"]))),
                   f"settings {sorted(seen['envs'])}")
        blue = {c[f"ENV{n}_D021"] for n in range(len(files["envs"]))}
        dawn = set(files["texts"]["dawn"])
        checks.add("the night of the castle blue, the HUD black (0.8.2): "
                   "$d021 seen black after the HUD's interrupt and the "
                   "settings' after the top one, blue among them; (0.10) "
                   "and at dawn its colours (play_d021, for the top "
                   "interrupt)",
                   blue | {c["D021_SKY"]} <= seen["d021"]
                   <= blue | {c["D021_SKY"]} | dawn and len(blue) > 1
                   and seen["play_d021"] == blue | dawn,
                   f"$d021 seen {sorted(seen['d021'])}, play_d021 "
                   f"{sorted(seen['play_d021'])}, settings {sorted(blue)}")
        flicker = {n: sorted(p) for n, p in seen["flicker_pictures"].items()}
        checks.add("the hazards that flicker: their four pictures in "
                   "SET_SLOT, the wisps in the mire (0.8), the spikes in "
                   "the pass (0.8.1), the spikes of the keep and the fire "
                   "of the hall (0.8.2)",
                   flicker == {n: [0, 1, 2, 3] for n in (2, 4, 5, 6)},
                   f"pictures {flicker}")
        streams = seen["streams"]
        checks.add("the packed streams unpacked in the transitions (0.8.1):"
                   " the maps of the levels played, the settings' tables "
                   "and sets (the wood's, the mire's, the crags', the "
                   "pass's; 0.8.2: the keep's, the hall's, under the "
                   "KERNAL)",
                   streams["map"] >= len(files["levels"]) and
                   streams["tables"] >= 6 and streams["set"] >= 6,
                   f"{streams}")
        missing = [name for name in PERCHES if name not in seen["perches"]]
        checks.add("the bat perches on a roof, on the street, on the "
                   "bridge of snow and on a chandelier", not missing,
                   f"never on {missing}")
        x_max = c["LEVEL_WIDTH"] * 16 - 24
        checks.add("both ends of the level: x 0 and x X_MAX, camera 0 and "
                   "CAMERA_MAX", {0, x_max} <= seen["x"] and
                   {0, c["CAMERA_MAX"]} <= seen["camera"])
        checks.add("the ninth bit of X used (X register over 255)",
                   seen["x_register_max"] > 255,
                   f"at most {seen['x_register_max']}")
        moths = {n: len(reference.level_info(n)["moths"])
                 for n in seen["moths"]}
        checks.add("the bat eats every moth of level 1, and moths of "
                   "level 2", seen["moths"].get(1) == moths.get(1)
                   and seen["moths"].get(2, 0) >= 2,
                   f"eaten {seen['moths']} of {moths}")
        missing = [e for e in EVENTS if e not in seen["events"]]
        checks.add("everything happens: changes both ways, refused, out of "
                   "energy, top, beats, a dive, blocked both ways, falls, "
                   "back, the lantern, the three heirlooms, the gate "
                   "open and passed, dawn; the staff taken, blows, enemies "
                   "struck, the brambles, a head on a block, the wisps, "
                   "the spikes of ice; (0.10) the title, the menu's "
                   "choices, the bands of words, a new game, the victory, "
                   "the sunrise", not missing, f"never {missing}")
        checks.add("set_tile into edge_paint: a door of the gate of level "
                   "2 opened in the column the back screen had just drawn",
                   model.edge_paints >= 2, f"{model.edge_paints} cells")
        missing = sorted(set(range(c["PICTURE_COUNT"])) - seen["pictures"])
        checks.add(f"all {c['PICTURE_COUNT']} pictures shown", not missing,
                   f"never {missing}")
        missing = sorted(set(range(c["HEIRLOOM_KINDS"]))
                         - seen["heirlooms_shown"])
        checks.add(f"all {c['HEIRLOOM_KINDS']} heirlooms shown (sprite 7)",
                   not missing, f"never {missing}")
        checks.add("the screen off during the transitions, then on",
                   seen["blank"] > 0, f"{seen['blank']} frames off")
        types = c["ENEMY_TYPES"]
        names = ("the watchman", "the crow", "the cat", "the scout",
                 "the owl", "the toad", "the goat", "the eagle",
                 "the werewolf of the band", "the werewolf of the guard",
                 "Tom's crow", "Tom Darkfang")[:types + 1]
        hit = sorted(seen["hit_by"])
        checks.add("Oscar hit by the three kinds of enemy (the watchman, "
                   "the crow, the cat), by one of the wood, by one of the "
                   "mountain, by one of the castle and by the hazards (the "
                   "brambles, the wisps, the spikes, the fire)",
                   {0, 1, 2} <= seen["hit_by"]
                   and any(3 <= kind < 6 for kind in hit)
                   and any(6 <= kind < 9 for kind in hit)
                   and any(9 <= kind < types for kind in hit)
                   and -1 in seen["hit_by"],
                   f"by {[names[k] if k >= 0 else 'a hazard' for k in hit]}")
        checks.add("the staff strikes every enemy of the wood (scout, owl, "
                   "toad), (0.8.1) of the mountain (goat, eagle, werewolf "
                   "of the band) and (0.8.2) of the castle (werewolf of the "
                   "guard, Tom's crow)",
                   seen["struck"] == set(range(3, types)),
                   f"struck {[names[k] for k in sorted(seen['struck'])]}")
        ways = {(game_model.RIGHT, 1), (game_model.LEFT, 1)}
        checks.add("blows facing right and left, on the ground, and one "
                   "in the air", ways <= seen["strikes"]
                   and any(not ground for _, ground in seen["strikes"]),
                   f"(facing, on the ground) {sorted(seen['strikes'])}")
        missing = sorted(set(range(c["STAFF_PICTURES"]))
                         - seen["staff_pictures"])
        checks.add(f"all {c['STAFF_PICTURES']} pictures of the staff shown "
                   "(sprite 2: held, in a jump, the blow, lying)",
                   not missing, f"never {missing}")
        checks.add("the struck enemies' puffs shown (sprites 3-6)",
                   seen["puffs"] > 0, f"{seen['puffs']} sprites")
        checks.add("after a hit Oscar blinks (his sprites off, then on)",
                   seen["blinking"] > 0, f"{seen['blinking']} frames off")
        missing = sorted(set((k, p) for k in range(types)
                             for p in range(4)) - seen["enemy_pictures"])
        checks.add(f"all {types * 4} pictures of the enemies shown "
                   "(sprites 3-6)", not missing, f"never {missing}")
        checks.add("enemies on the screen together: up to 4",
                   2 <= seen["together"] <= 4, f"at most {seen['together']}")
        # Tom Darkfang.
        checks.add("into the arena through the door of the throne room "
                   "(0.9): Tom's five pictures under the KERNAL as tom.bin, "
                   "the table that mirrors",
                   seen["tom_kernal"] == "ok", f"{seen['tom_kernal']}")
        pictures = c["TOM_PICTURES"]
        checks.add(f"Tom's {pictures * 2} pictures shown, facing both ways "
                   "(the page of TOM_SPRITES shown)",
                   seen["tom_pictures"] == set(range(pictures * 2)),
                   f"{sorted(seen['tom_pictures'])}")
        k = model.k
        states = {k[f"TS_{name}"] for name in (
            "WAIT", "GROWL", "LEAP", "LAND", "CHARGE", "DAZED", "YELP",
            "RUN", "HOP", "PAUSE", "UP")}
        checks.add("every move of Tom's on the screen: waiting, growling, "
                   "leaping, landed, charging, dazed; beaten: yelping, "
                   "running back, hopping onto the dais, still there, up "
                   "and away", seen["tom_states"] >= states,
                   f"{sorted(seen['tom_states'])}")
        checks.add(f"Tom struck {k['HITS_FULL']} times, flashing; faster "
                   f"with {k['HITS_FAST']} hits left; beaten, gone, and "
                   "(0.10) the victory",
                   len(model.tom_struck) >= k["HITS_FULL"]
                   and seen["tom_flash"] > 0 and seen["tom_fast"] > 0
                   and {"tom beaten", "tom gone"} <= seen["events"],
                   f"{len(model.tom_struck)} hits, {seen['tom_flash']} "
                   f"frames flashing, {seen['tom_fast']} faster")
        # The states and the score.
        happened = [e for _, e in model.events]
        checks.add("the title (0.10): at the start, (1.0) after the two "
                   "victories and the two dawns; the menu's three choices, "
                   "Up and Down; PRESS FIRE blinking",
                   happened.count("the title") == 4
                   and {"menu 0", "menu 1", "menu 2"} <= seen["events"]
                   and seen["press"] == {c["PRESS_ON"], c["PRESS_OFF"]},
                   f"titles {happened.count('the title') + 1}, colours "
                   f"{sorted(seen['press'])}")
        checks.add("at the gate of each level from 1 to 7, LEVEL CLEAR "
                   "and the count (0.10): the night left into the score, "
                   "then the next level", happened.count("band 0")
                   == c["LEVEL_COUNT"] - 1, f"{happened.count('band 0')}")
        won = seen.get("score_won", {})
        expected = (100 * won.get("struck", 0) + 500 * won.get("heirlooms", 0)
                    + 10 * won.get("moths", 0) + 5000 * won.get("tom", 0)
                    + 50 * won.get("night_steps", 0))
        checks.add("the score at the victory (0.10): 100 an enemy struck, "
                   "500 an heirloom, 10 a moth, 5000 Tom, 50 a step of the "
                   "night counted (the program's as the model's at every "
                   "frame)", won and won["score"] == expected
                   and won["heirlooms"] == 3 * c["LEVEL_COUNT"]
                   and won["tom"] == 1, f"{won}, expected {expected}")
        checks.add("the victory (0.10): Tom gone, the words over the arena, "
                   "the night counted; Fire: the title",
                   {"victory", "band 1"} <= seen["events"], "")
        checks.add("dawn (0.10): the game stops, the sky through the "
                   "colours of dawn, Oscar gone in a puff of smoke, THE SUN "
                   "HAS RISEN; Fire: the title",
                   {"dawn", "sunrise", "band 2"} <= seen["events"]
                   and dawn <= seen["play_d021"], "")
        fresh = seen.get("new_game", {})
        checks.add("a new game after the title (0.10): level 1, the score "
                   "0, no staff, the HUD's rows again",
                   fresh == {"level": 1, "score": 0, "staff": 0, "hud": True},
                   f"{fresh}")
        checks.add("Oscar hit by Tom (0.9)", types in seen["hit_by"],
                   f"by {sorted(seen['hit_by'])}")
        # The model reads LEAP_VY and TOM_GRAVITY from the program's
        # labels: with other numbers both would leap alike. The leap
        # tom.asm means: LEAP_FRAMES frames, LEAP_RISE lines high.
        checks.add(f"Tom's leaps (0.9): {LEAP_FRAMES} frames, "
                   f"{LEAP_RISE} lines high, every one",
                   seen["leaps"] == {(LEAP_FRAMES, LEAP_RISE)},
                   f"{sorted(seen['leaps'])} (frames, lines)")
    else:                       # steps 1-11 of the chain
        step_checks(step, model, seen, checks, c, files, music,
                    player)
    for taken, snap in zip(shots, snaps):
        actual = read_png(PROJECT / taken["file"])
        heirloom, oscar = taken["heirloom"], taken["oscar"]
        k = model.k
        staff = taken["staff"]
        expected = reference.rgb_rows(reference.capture(
            reference.scrolled_picture(
                snap, taken["camera"], reference.world_picture(snap),
                tuple(oscar) if oscar else None,
                tuple(heirloom) if heirloom else None,
                [(x, y, sprite_bytes(files, k, block), colour)
                 for x, y, block, colour in taken["enemies"]],
                (staff[0], staff[1], sprite_bytes(files, k, staff[2]))
                if staff else None,
                tuple(taken["moon"]) if taken["moon"] else None,
                tom_sprites(files, taken["tom"]),
                logo_sprites(files, c, k) if taken["logo"] else None,
                band_of(taken["band"]))))
        different = sum(1 for y in range(272) for x in range(384)
                        if actual[y][x] != expected[y][x])
        taken["pixels_different"] = different
        checks.add(f"{taken['file']} (camera {taken['camera']}) equals "
                   "the reference, pixel by pixel", different == 0,
                   f"{different} pixels differ")
    report = {
        "program": report_path(PRG),
        "prg_bytes": PRG.stat().st_size,
        "prg_sha256": hashlib.sha256(PRG.read_bytes()).hexdigest(),
        "vice": str(args.vice),
        "frames": turn,
        "start": start_state,
        "route": route_log,
        "surfaces_landed_on": sorted(f"{n}: {name}"
                                     for n, name in seen["surfaces"]),
        "bat": {"perched_on": sorted(seen["perches"]),
                "moths_eaten": seen["moths"],
                "pictures_shown": len(seen["pictures"])},
        "events": sorted(seen["events"]),
        "frames_screen_off": seen["blank"],
        "colour_moved_by_line": seen["lines"],
        "camera_waits": {"going_right": model.holds[0],
                         "going_left": model.holds[1]},
        "swaps": model.swaps,
        "cycles_from_joy_ready_max": {name: max(values, default=0)
                                      for name, values in cycles.items()},
        "cycles_most": [list(item) for item in
                        sorted(cycle_log, reverse=True)[:12]],
        "transition_steps_max": dict(sorted(steps_cost.items())),
        "music": {"frames_checked": len(music["cycles"]),
                  "synced_at_music_frame": music["synced_at"],
                  "last_music_frame": player.frame,
                  "song_frames": song["frames"],
                  "boss_song_frames": player.songs[1]["frames"],
                  "frames_played": {"theme": music["frames_of"][0],
                                    "boss": music["frames_of"][1],
                                    "clear": music["frames_of"][2],
                                    "won": music["frames_of"][3],
                                    "dawn": music["frames_of"][4],
                                    "stopped": music["silent"]},
                  "loops": player.loops,
                  "calls": music["calls"],
                  "jingles_ended": player.ended,
                  "effects_called": music["fx"],
                  "effects_sounded": player.fx_started,
                  "effects_by_mode": {str(k): v for k, v in
                                      music["fx_by_mode"].items()},
                  "cycles_max": max(music["cycles"], default=0),
                  "cycles_mean": round(sum(music["cycles"])
                                       / max(len(music["cycles"]), 1))},
        "frame_cycles": vicemon.PAL_FRAME_CYCLES,
        "screenshots": shots,
        "hud_end": run.get("hud_end"),
        "coverage": ({"instructions": len(executed) + len(cover),
                      "never": sorted(cover)}
                     if args.coverage else None),
        "flicker_pictures": {str(n): sorted(p) for n, p in
                             seen["flicker_pictures"].items()},
        "checks": checks.items,
        "result": "PASS" if checks.passed() else "FAIL",
    }
    with open(REPORT, "w", encoding="utf-8", newline="\n") as file:
        file.write(json.dumps(report, indent=2) + "\n")
    print(f"{report['result']}: {len(checks.items)} checks, {turn} "
          f"frames, report {report_path(REPORT)}")
    return 0 if checks.passed() else 1


if __name__ == "__main__":
    sys.exit(main())
