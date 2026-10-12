"""Dreadcastle, a frame at a time, in Python.

A model of one turn of the main loop of the C64 program, written from
the comments of game/src (oscar.asm, bat.asm, objects.asm, level.asm,
scroll.asm): Oscar's walk and jump in fixed point, the surfaces he
stands on and the solid blocks that push him out; the puff of smoke, the
bat's flight, its energy and the moths it eats; the heirlooms, the
lantern, the gate, the health, the night; the transitions after a fall,
at dawn and through the gate (to the next level: the first two on one
set of characters); the enemies (the patrol, the flyer, the jumper:
enemies.asm), their touch that takes health, the jump back and the
blinking that follows; the settings (each its set of characters and its
tables), the Count's staff (taken, held, the blow that strikes the
enemies), the hazards (brambles), the head under a solid block and the
room to turn back from the bat; the mire of level 4, its set of
characters copied into the slot of the VIC-II's bank (SET_SLOT) as the
wood's is, and its will-o'-the-wisps that flicker; the maps, tables and
sets unpacked a page a frame in the transition (pack.py), the mountain's
two settings (the crags of level 5, the pass of level 6, whose spikes of
ice glint as the wisps flicker); the camera that follows him, the two
screens and the colour RAM; the castle, its keep and its hall; the arena
and Tom Darkfang (tom.asm): the way in through the door of the throne
room, his pictures unpacked in the transition (mirrored as they are
copied into the page shown), his moves, the blow that strikes him, his
touch, his four sprites and the page of them shown, his bar, his flight;
which song plays and whether it plays (the theme, Tom's from the arena
shown until he is beaten; the player itself is player_model.py); the
game's states (states.asm): the title at the start (level 7 at its door,
the name, the moon, the menu and its choices), a new game, the count at
a gate, the victory, dawn; the bands of words in the screens; the score.
The numbers (speeds, gravity, energy, the night...) are read from the
program's labels, so model and program share them; the level, its
metatiles and its objects come from the files of game/assets/generated.
The model plays its own copy of the level, as the program does.

The test runs the model next to the C64 and compares, after every
frame, Oscar's variables, the level's, the staff's, the camera's, the
enemies', the sprite registers and the memory of the two screens, of
the colour RAM, of the level, of the setting's tables, of the moths'
and the flickering hazards' characters and of the HUD.
"""

from pathlib import Path
import sys

import reference

sys.path.append(str(Path(__file__).resolve().parents[1]  # after
                    / "game/assets"))   # a variant's (verify_game.py)
import music         # noqa: E402
import sfx           # noqa: E402

RIGHT, LEFT = 0, 1
D018 = (0x02, 0x12)                 # screen A, screen B (the village)
# + the setting's characters: the village's at CHARSET, the others'
# in SET_SLOT.
CHAR_BITS = (0x00, 0x04)         # the village's set; the others'
# The hazards by setting (the event of a touch): the wood's brambles,
# the mire's wisps, the pass's spikes of ice, the keep's
# spikes of iron and the fire on the hall's hearth.
HAZARD_NAMES = {"marsh": "wisps", "pass": "spikes", "keep": "spikes",
                "hall": "fire"}
UP, DOWN, GO_LEFT, GO_RIGHT, FIRE = 0x01, 0x02, 0x04, 0x08, 0x10
ROWS = reference.PLAYFIELD_ROWS
STAND, WALK_A, WALK_B, WALK_C, JUMP, FALL = range(6)
WALK_CYCLE = (WALK_A, WALK_B, WALK_C, WALK_B)
VAMPIRE, BAT = 0, 1
FLY_A, FLY_B, FLY_C, PERCH, GNAM = range(5)
BEAT_CYCLE = (FLY_C, FLY_B, FLY_A, FLY_B)       # after a beat
CHANGE_KEYS = (UP | FIRE, DOWN | FIRE)          # vampire, bat
GO_BACK, GO_START, GO_NEXT, GO_ARENA, GO_TITLE = 0, 1, 2, 3, 4
# The game's states (states.asm), and the menu's choices.
ST_PLAY, ST_TITLE, ST_TALLY, ST_WON, ST_DAWN = range(5)
MUSIC, SOUND_FX, SILENT = range(3)
# The sound effects' numbers (sfx.py: FX_JUMP is 0), the
# jingles' songs.
FX = {name: number for number, name in enumerate(sfx.EFFECTS)}
SONG_CLEAR, SONG_WON, SONG_DAWN = 2, 3, 4
JINGLE_FRAMES = {number: song["frames"] for number, song
                 in enumerate(music.compile_music())}
BODY_HEIGHTS = (20, 12)                         # the vampire, the bat
# The steps of a transition (objects.asm, trans_steps), by trans from
# 0 up: 8 the level, the next or the same again, whose map is
# unpacked in the next MAP_PAGES frames (2: a page of the stream); 9
# the setting's tables, if another (ENV_PAGES frames); 10 the screen
# off and, if another setting, env and the setting's characters into
# SET_SLOT (if another set: SET_PAGES frames, the first here); 7 the
# level's things and Oscar; 3-6 screen A drawn again; 1 the screen
# on.
TRANS_STEPS = ((0, 1, 2, 2, 2, 6, 5, 4, 3, 7, 2, 2, 2, 2, 10)
               + (0,) * 18 + (2,) * 9 + (9,) + (2,) * 6 + (8,))
DRAWN = {3: (0, 10), 4: (10, 20), 5: (20, 30), 6: (30, 39)}
PHYSICS = ("WALK_MAX", "WALK_ACCEL", "WALK_SKID", "WALK_FRICTION",
           "JUMP_SPEED", "GRAVITY_HOLD", "GRAVITY", "FALL_MAX", "STEP",
           "CEILING", "SENSOR_X", "ZONE_LEFT", "ZONE_RIGHT",
           "PUFF_FRAMES", "PUFF", "FLAP_SPEED", "BAT_GRAVITY",
           "BAT_FALL_MAX", "BAT_DIVE", "BAT_DIVE_MAX", "FLY_MAX_X",
           "FLY_ACCEL", "FLY_TURN", "FLY_DRAG", "BAT_TOP", "BAT_MIDDLE",
           "BEAT_FRAMES", "ENERGY_FULL", "ENERGY_STEP", "FLAP_COST",
           "RECHARGE", "MOTH_ENERGY", "GNAM_FRAMES", "BAT_PICTURES",
           "BODY_LEFT", "BODY_RIGHT", "BOTTOM", "HEALTH_FULL",
           "NIGHT_STEPS", "NIGHT_STEP", "HEIRLOOM_BOX", "TOUCH",
           "TRANS_FRAMES", "BLANK_AT", "SHOW_AT", "HEIRLOOM_BLOCKS",
           "PATROL_SPEED", "FLYER_SPEED", "CAT_JUMP", "CAT_VX",
           "CAT_GRAVITY", "CAT_WAIT", "CAT_REACH", "HIT_DAMAGE",
           "PROTECT_FRAMES", "KNOCK_FRAMES", "ENEMY_BLOCKS",
           "ENEMY_BLOCKS_2", "MAX_ENEMIES", "OSCAR_LINES", "STAFF_BLOCKS",
           "ENEMY_PUFF", "STAFF_TOUCH", "MOON_BLOCK",
           # Tom (tom.asm)
           "HITS_FULL", "HITS_FAST", "WAIT_FRAMES", "GROWL_FRAMES",
           "GROWL_FAST", "LAND_FRAMES", "DAZED_FRAMES", "DAZED_FAST",
           "LEAP_VY", "TOM_GRAVITY", "LEAP_REACH", "CHARGE_ACCEL",
           "CHARGE_MAX", "CHARGE_FAST", "FLASH_FRAMES", "YELP_FRAMES",
           "FLEE_SPEED", "HOP_VY", "PAUSE_FRAMES", "UP_SPEED",
           "GONE_FRAMES", "TOM_BLOCKS", "TOUCH_SPAN", "MIDDLES",
           "TS_WAIT", "TS_GROWL", "TS_LEAP", "TS_LAND", "TS_CHARGE",
           "TS_DAZED", "TS_YELP", "TS_RUN", "TS_HOP", "TS_PAUSE",
           "TS_UP", "TS_GONE", "T_STAND", "T_GROWL", "T_RUN_A",
           "T_RUN_B", "T_DAZED",
           # the states (states.asm)
           "TALLY_WAIT", "TALLY_TICK", "TALLY_END", "WON_WAIT",
           "BAND_LINE", "LOGO_BLOCK", "STATES", "STATE_BYTES",
           # the sound
           "TOLL_STEPS", "SFX_VARS", "SFX_BYTES")
PATROL, FLYER, JUMPER = 0, 1, 2
# The steps of the book's chain (tools/make_chain.py): the first step
# of each part of the game. A model of step N (Game(..., step=N)) has
# the parts of the steps up to N, and the seams of that step: in steps
# 1-11 the program starts in level 1 (no title); step 1 only shows it;
# in step 2 the joystick moves the camera (steer_camera); in steps 3-4
# a transition only takes Oscar back after a fall; in steps 5-9 the
# gate of the last level of the step leads to level 1 (STEP_LEVELS);
# in steps 5-11 dawn starts level 1 again (GO_START), and (7-11) takes
# the staff; in steps 10-11 Tom gone starts level 1 again too; in step
# 11 the theme always plays (no menu).
FIRST = {"scroll": 2, "oscar": 3, "bat": 4, "objects": 5, "enemies": 6,
         "staff": 7, "packed": 8, "castle": 9, "tom": 10, "music": 11,
         "states": 12, "sound": 13}
STEP_LEVELS = {5: 2, 6: 2, 7: 3, 8: 6, 9: 8}
GONE = 0xFF                         # an enemy struck, after its puff
KNOCK_X = (0x0200, 0x0180)          # the jump back: the vampire, the bat
KNOCK_Y = (0x0200, 0x0100)
# The flyer's wave: 64 lines up and down, a sine of 12.
WAVE = [round(12 * __import__("math").sin(i * 2 * 3.141592653589793
                                           / 64)) for i in range(64)]


def flicker_page(c, env):
    """The page of setting env's flickering hazards' pictures in
    flicker.bin: one for each setting with them, in their order."""
    return bin(c["FLICKER_SETTINGS"] & ((1 << env) - 1)).count("1")


def signed(value):
    """A 16-bit two's complement number as a Python integer."""
    return value - 0x10000 if value & 0x8000 else value


class Surfaces:
    """The lines Oscar stands on, from the tables of the setting
    (metashape, metaflags, profiles: reference.environment), looked
    up the way the program does, in a level (the model's copy)."""

    def __init__(self, level, env):
        self.level = level
        self.use(env)

    def use(self, env):
        """The tables of a setting (env: reference.environment)."""
        self.shape = env["metashape"]
        self.flags = env["metaflags"]
        self.profiles = env["profiles"]
        self.count = len(self.profiles) // 16

    def line_at(self, x, row):
        """The surface in metatile row `row` at level pixel column x,
        as a line of the playfield, or None."""
        if not 0 <= row < 11:
            return None
        metatile = self.level[(x >> 4) * 11 + row]
        profile = self.shape[metatile]
        if profile == 0:
            return None
        offset = self.profiles[(x & 15) * self.count + profile]
        return None if offset == 0xFF else row * 16 + offset

    def find(self, x, top, bottom):
        """The highest surface at column x with top <= line <=
        bottom, or None: the program looks in the metatile rows of
        top and of bottom (never more than 16 lines apart)."""
        for row in range(top >> 4, (bottom >> 4) + 1):
            line = self.line_at(x, row)
            if line is not None and top <= line <= bottom:
                return line
        return None

    def solid(self, col, first, last, flag=1):
        """A solid metatile (or one with `flag`: 2, a hazard) in
        column col, rows first to last."""
        return any(self.flags[self.level[col * 11 + row]] & flag
                   for row in range(first, last + 1))


class Game:
    chain_step = 13                 # the complete game (see FIRST)
    enemy_slots = 0                 # slots of ENEMIES reset so far
    camera_speed = 2                # step 2: steer_camera's speed
    first_level = 0                 # steps 1-11: the level at entry
    flicker_shift = 2               # the hazards: every 4 frames
    night_points = 50               # a step of the night

    def __init__(self, files, labels, step=13):
        """labels: the complete game's (the numbers; the same in every
        step); step: the step of the chain (13: the complete game)."""
        c = files["constants"]
        self.c = c
        self.chain_step = step
        self.k = k = {name: labels[name] for name in PHYSICS}
        self.all_files = files
        self.files = dict(files)
        self.level_maps = [bytes(m) for m in files["levels"]]
        self.level_no = 0
        self.level = bytearray(self.level_maps[0])  # LEVEL, the copy
        self.files["level"] = self.level
        self.env = 0                        # the setting's tables
        self.surfaces = Surfaces(self.level, files["envs"][0])
        self.all_objects = [reference.objects(files, n + 1)
                            for n in range(len(self.level_maps))]
        self.level_env = [objects["env"] for objects in self.all_objects]
        self.objects = self.all_objects[0]
        self.names = files["names"]
        self.moves = {   # speeding up, turning, slowing down, top
            "walk": (k["WALK_ACCEL"], k["WALK_SKID"],
                     k["WALK_FRICTION"], k["WALK_MAX"]),
            "across": (k["FLY_ACCEL"], k["FLY_TURN"], k["FLY_DRAG"],
                       k["FLY_MAX_X"])}
        self.moth_frame = 0                 # the moths' picture
        self.moth_pictures = (reference.GENERATED
                              / "moth.bin").read_bytes()
        # SET_SLOT: the setting whose characters are in it (None:
        # none yet), its moth's picture and its flickering hazards'
        # (they change there, not where the set waits).
        self.slot_env = None
        self.slot_moth = self.slot_flicker = 0
        # Steps 7-11: until the first moth is written there, SET_SLOT
        # holds what was in memory (from step 12 the game starts on
        # the title, SET_SLOT as LOAD left it).
        self.slot_moth_known = self.has("states")
        self.flicker_pictures = files["flicker"]
        self.env_copy = False
        self.events = []                    # (frame, what)
        self.landed = []                    # (frame, x, line, who)
        self.taken = []                     # (frame, heirloom)
        self.x_max = c["LEVEL_WIDTH"] * 16 - 24
        self.camera_max = c["CAMERA_MAX"]
        self.frame = 0
        self.joy = 0
        self.height = None                  # push_out, respawn
        self.sensor = None                  # move_x, respawn
        self.holds = [0, 0]
        self.swaps = 0
        self.screens = [{}, {}]
        self.colours = {}
        self.edge = [0] * ROWS
        self.edge_paints = 0                # set_tile into edge
        self.hud_bytes = bytearray(files["hud"][:120])
        self.hud_colours = bytearray(files["hud"][120:240])
        self.trans, self.trans_kind = 0, None
        self.display_on = True
        self.sprites_on = 3                 # $d015
        self.d010 = 0
        self.sprite7 = None                 # (X, Y, block, kind)
        self.enemy_sprites = []             # [(X, Y, block, colour)]
        # The table of the enemies: MAX_ENEMIES places, as in the
        # C64; a level uses the first, as many as it has (the others
        # keep what was there).
        places = k["MAX_ENEMIES"]
        self.en_x, self.en_y = [0] * places, [0] * places
        self.en_vx, self.en_vy = [0] * places, [0] * places
        self.en_dir, self.en_timer = [0] * places, [0] * places
        self.en_air, self.en_pic = [0] * places, [0] * places
        self.en_gone = [0] * places         # 0, puff frames, GONE
        self.protect = self.stun = 0
        self.hit_by = []            # (frame, type; -1 a hazard)
        self.struck = []                # (frame, type, face, ground)
        self.has_staff = 0                  # 1: Oscar holds it
        self.blow = 0                       # frames of the blow left
        self.staff_sprite = None            # (X, Y, block)
        self.moon_sprite = None             # (X, Y, block): the wood
        self.d018_values = self.d018_of(0)
        self.shown = None                   # the heirloom shown
        self.anim = 0
        self.swapped = False
        # Tom: init_tom, at the start: his bytes all 0.
        self.arena = 0
        self.tom_state = self.tom_timer = 0
        self.tom_x = self.tom_y = self.tom_vx = self.tom_vy = 0
        self.tom_face = self.tom_pic = self.tom_hits = 0
        self.tom_flash = self.tom_safe = self.tom_next = 0
        self.tom_shown = self.tom_front = self.tom_reg = 0
        # The music: music_init, the theme, playing.
        self.mus_song, self.mus_on = 0, 1
        self.calls = []                     # music_start, music_stop
        self.fx_calls = []                  # sfx_start
        self.counted = 0                    # night steps counted
        # The game's states: the title first, MUSIC, the score
        # 0, no band; the title's sprites (2-5 the name, stretched,
        # hi-res); the background of dawn, if it has come.
        self.game_state, self.sound_mode = ST_TITLE, MUSIC
        self.score = self.score_new = 0
        self.state_timer = self.state_phase = 0
        self.band_on = self.band_top = self.band_end = 0
        self.band_d018 = 0
        self.dawn_d021 = None
        self.logo_on = False
        self.texts = files["texts"]
        self.menu_blink = None              # PRESS FIRE's colour
        self.tom_sprites = []               # [(X, Y, block, colour)]
        self.tom_pages = [None, None]       # TOM_SPRITES: what is there
        self.tom_page_frame = -99           # when the page changed
        self.tom_struck = []                # (frame, hits left)
        self.tom_seen = set()               # (state, picture, face)
        # The program's start (main.asm, entry; load_level):
        # the title, level 7 with its setting (its set unpacked into
        # SET_SLOT), Oscar at its door, the menu; the name, the moon.
        # Steps 1-11: level 1, Oscar at its start, the HUD; no music
        # before step 11 (from it the theme, playing).
        self.stream = None
        if not self.has("states"):
            self.start_level_1()
            return
        self.level_no = c["TITLE_LEVEL"]
        self.level[:] = self.level_maps[self.level_no]
        self.load_env(self.level_env[self.level_no])
        self.slot_env = self.env
        self.restart()
        self.title_place()
        self.draw_columns(0, 39)
        self.title_sprites()

    def has(self, part):
        """The step has this part of the game (FIRST)."""
        return self.chain_step >= FIRST[part]

    def start_level_1(self):
        """Steps 1-11 (main.asm, entry): level 1 with its setting, the
        village's (no set into SET_SLOT), Oscar at its start, screen A
        drawn, the HUD and the level's name; the enemies at their
        start (6-11); Oscar's sprites on."""
        self.game_state = ST_PLAY
        self.level_no = first = self.first_level
        self.level[:] = self.level_maps[first]
        self.load_env(self.level_env[first])
        self.restart()
        self.respawn()
        self.draw_columns(0, 39)
        self.show_name()
        self.init_sprites()
        if self.has("enemies"):
            self.reset_enemies()
        self.place_oscar()
        self.mus_on = int(self.has("music"))

    # --- one turn -------------------------------------------------
    def turn(self, joy, frame_count):
        """One turn; frame_count: the C64's at joy_ready."""
        self.frame += 1
        self.joy = joy
        self.swapped = False
        if not self.has("scroll"):          # step 1: nothing moves
            self.joy = 0
            return
        if not self.has("oscar"):           # step 2: steer_camera
            self.steer_camera()
            return
        if self.trans:
            self.transition()
            return
        if self.game_state != ST_PLAY:          # a state's turn
            self.turn_frame = frame_count
            (self.title_turn, self.tally_turn, self.won_turn,
             self.dawn_turn)[self.game_state - 1]()
            return
        # flutter_moths: every 8 frames the picture of bit 3, in both
        # sets the VIC-II sees (step 4; SET_SLOT's from step 7).
        if frame_count & 7 == 0 and self.has("bat"):
            self.moth_frame = (frame_count >> 3) & 1
            if self.has("staff"):
                self.slot_moth = self.moth_frame
                self.slot_moth_known = True
        self.move_oscar()
        if self.trans:                              # fallen
            self.show_hud()
            return
        self.animate()
        self.follow()
        self.place_oscar()
        if self.has("staff"):
            self.place_staff()
        if self.swap:
            self.do_swap()
        else:
            self.prepare_back()
        # The enemies after the colour RAM (it must be moved before
        # the raster reaches it); in the arena Tom instead of
        # them and of the level's things.
        if self.arena:
            self.fight_tom()
            if self.trans:                          # no health left
                self.show_hud()
                return
            self.place_tom()
            self.tick_night()
            self.show_hud()
            self.flicker(frame_count)
            return
        if self.has("enemies"):
            self.move_enemies()
            self.hit_enemies()
            if self.trans:                          # no health left
                self.show_hud()
                return
            self.place_enemies()
        if self.has("objects"):
            self.touch_things()
            self.tick_night()
        self.show_hud()
        if self.has("objects"):
            self.place_heirloom()
        self.flicker(frame_count)

    def steer_camera(self):
        """Step 2 (scroll.asm, steer_camera): the joystick moves the
        camera, 2 pixels a frame; the back screen for that way."""
        self.swap = 0
        if self.joy & GO_RIGHT:
            self.last_dir = RIGHT
            self.move_camera(RIGHT, self.camera_speed)
        elif self.joy & GO_LEFT:
            self.last_dir = LEFT
            self.move_camera(LEFT, self.camera_speed)
        if self.swap:
            self.do_swap()
        else:
            self.prepare_back()

    def flicker(self, frame_count):
        """flicker_hazards: in a setting whose hazards
        flicker, every 4 frames (at 2 of 4) the picture of bits 2-3."""
        shift = self.flicker_shift
        if self.c["FLICKER_SETTINGS"] >> self.env & 1 and \
                frame_count & ((1 << shift) - 1) == 2:
            self.slot_flicker = (frame_count >> shift) & 3

    # --- the level: restart, respawn, transitions -----------------
    def restart(self):
        """restart: the level's things from the start, its objects (its
        name: in the last step, trans_on)."""
        self.objects = self.all_objects[self.level_no]
        self.got = self.got_bits = 0
        self.lantern_lit = self.door_open = 0
        self.moths_eaten = 0
        self.arena = 0                      # not in the arena
        self.night = self.k["NIGHT_STEPS"]
        self.night_time = self.k["NIGHT_STEP"]
        self.respawn_x = self.c["START_X"]

    def start_stream(self, kind):
        """A packed stream to unpack: "map", "tables" or
        "set", a page a frame."""
        self.stream = [kind, 0]

    def unpack_page(self):
        """A page of the stream: of the map, into the level's copy; of
        the set, into SET_SLOT, whose moth and flickering hazards (in
        the last page) are then the set's as it waits, in their first
        pictures."""
        if self.stream is None:
            return
        kind, page = self.stream
        if kind == "map":
            new = self.level_maps[self.level_no]
            low, high = page * 256, min((page + 1) * 256, len(new))
            if low < high:
                self.level[low:high] = new[low:high]
        elif kind == "tom":                 # under the KERNAL
            pass
        elif kind == "set" and page == self.c["SET_PAGES"] - 1:
            self.slot_env = self.env
            self.slot_moth = self.slot_flicker = 0
            self.slot_moth_known = True
        self.stream[1] = page + 1

    def respawn(self):
        k, c = self.k, self.c
        self.x = self.respawn_x << 8
        self.sensor = self.respawn_x + k["SENSOR_X"]
        self.height = BODY_HEIGHTS[VAMPIRE]
        self.y = c["START_Y"] << 8
        self.vx = self.vy = 0
        self.anim = 0
        self.form, self.puff, self.gnam, self.flap = VAMPIRE, 0, 0, 0
        self.energy = k["ENERGY_FULL"] << 8
        self.front, self.prep_stage, self.swap = 0, 0, 0
        self.prev_joy = self.joy
        self.health = k["HEALTH_FULL"]
        self.ground = 1
        self.face = self.prep_dir = self.last_dir = RIGHT
        self.picture = STAND
        self.shown_d018 = self.d018_values[0]
        camera = self.respawn_x - (c["SCREEN_START"] - 7)
        self.camera = max(0, min(camera, self.camera_max))
        if self.arena:                      # the end
            self.camera = self.camera_max
        self.set_xscroll()
        self.protect = self.stun = self.blow = 0

    def d018_of(self, env):
        """$d018 for screens A and B with the characters of setting
        `env`."""
        return tuple(value | (CHAR_BITS[0] if env == 0 else CHAR_BITS[1])
                     for value in D018)

    def load_env(self, env):
        """The tables of setting `env` in use (ENV_TABLES), its set of
        characters shown."""
        self.env = env
        self.files.update(self.all_files["envs"][env])
        self.files["level"] = self.level
        self.surfaces.use(self.all_files["envs"][env])
        self.d018_values = self.d018_of(env)

    def start_transition(self, kind):
        self.trans_kind = kind
        self.trans = self.k["TRANS_FRAMES"]
        self.events.append((self.frame, ("back", "start", "next",
                                         "arena", "title")[kind]))

    def fallen(self):
        self.health = 0
        self.sprites_on &= 0x40 if self.moon_here() else 0
        self.events.append((self.frame, "fallen"))
        self.start_transition(GO_BACK)

    def transition(self):
        self.trans -= 1
        step = TRANS_STEPS[self.trans]
        if not self.has("objects") and step in (2, 8, 9):
            return                      # steps 3-4: trans_none
        if step == 8:                   # the level
            self.env_copy = False
            self.stream = None
            if self.trans_kind == GO_BACK:
                return
            if self.trans_kind == GO_ARENA:     # Tom's pictures
                self.start_stream("tom")
                if self.has("music"):
                    self.music_stop()
                return
            if self.trans_kind == GO_NEXT:
                self.level_no += 1
                if self.level_no == STEP_LEVELS.get(self.chain_step):
                    self.level_no = 0           # steps 5-9: level 1
            elif self.trans_kind == GO_START:   # a new game
                self.level_no = 0
            else:                               # the title
                self.level_no = self.c["TITLE_LEVEL"]
            self.env_copy = self.level_env[self.level_no] != self.env
            self.start_stream("map")
        elif step == 2:
            if self.stream is not None:
                self.unpack_page()
        elif step == 9:                 # the setting's tables
            self.stream = None
            if self.env_copy:
                self.start_stream("tables")
        elif step == 10:                # the screen off; the setting
            self.display_on = False
            self.sprites_on = 0
            self.stream = None
            self.band_on = 0                    # no band
            self.dawn_d021 = None       # next_env, always
            if self.env_copy:
                self.load_env(self.level_env[self.level_no])
                if self.env != 0:
                    self.start_stream("set")
                    self.unpack_page()
        elif step == 7:
            if self.trans_kind == GO_ARENA:
                self.arena = 1
                self.respawn_x = self.c["ARENA_X"]
            elif self.trans_kind != GO_BACK:
                if self.trans_kind == GO_START:
                    if self.has("states"):
                        self.new_game()
                    else:
                        self.has_staff = 0      # steps 7-11
                self.restart()
                if self.trans_kind == GO_TITLE:
                    self.title_place()
                    return
            if self.arena:
                self.reset_tom()
            self.respawn()
            self.show_hud()
        elif step in DRAWN:
            self.draw_columns(*DRAWN[step])
        elif step == 1:                 # the lightest step
            if self.trans_kind == GO_TITLE:     # the title
                self.title_sprites()
                self.game_state = ST_TITLE
                self.title_music()
                self.events.append((self.frame, "the title"))
                self.display_on = True
                return
            if self.trans_kind == GO_START and self.has("states"):
                self.init_sprites()             # init_sprites
            self.show_name()
            if self.has("enemies"):
                self.reset_enemies()    # at their start
            self.place_oscar()
            if self.has("staff"):
                self.place_staff()
            if self.has("enemies"):
                self.place_enemies()
            if self.has("objects"):
                self.place_heirloom()
            self.game_state = ST_PLAY
            if self.arena:
                self.place_tom()
                if (self.has("music") and self.sound_mode == MUSIC
                        and self.mus_song != 1):
                    self.music_start(1)         # boss_theme
                    self.events.append((self.frame, "boss theme"))
            elif self.trans_kind != GO_BACK:    # level_theme
                if self.has("music") and self.sound_mode == MUSIC:
                    self.music_start(0)
                    self.events.append((self.frame, "theme"))
            self.sprites_on |= 3
            self.display_on = True

    def music_start(self, song):
        """music_start: `song` from its start, playing."""
        self.mus_song, self.mus_on = song, 1
        self.calls.append(("start", song))

    def music_stop(self):
        self.mus_on = 0
        self.calls.append(("stop",))

    def sfx(self, name):
        """sfx_start: the program calls it where the thing
        happens, whatever the menu said (sfx_start decides); the test
        compares the calls, in their order. (From step 13.)"""
        if self.has("sound"):
            self.fx_calls.append((self.frame, FX[name]))

    def jingle(self, song):
        """The jingles: not with SILENT. (From step 13.)"""
        if self.has("sound") and self.sound_mode != SILENT:
            self.music_start(song)

    def draw_columns(self, first, end):
        for col in range(first, end):
            self.draw_column((self.camera >> 3) + col, col, 0)
            self.paint(col, range(ROWS))

    # --- Oscar ----------------------------------------------------
    def move_oscar(self):
        if self.stun:                   # thrown back: no joystick
            self.stun -= 1
            self.joy = 0
        if self.blow:                   # the blow goes on
            self.blow -= 1
        k, joy = self.k, self.joy
        both = CHANGE_KEYS[self.form]
        pushed = (joy & both == both and self.prev_joy & both != both
                  and self.has("bat"))          # step 3: no change
        if self.puff:
            self.puff -= 1                          # in the smoke
        elif pushed and self.form == BAT and self.no_room():
            self.events.append((self.frame, "refused"))
            self.move_bat()
        elif pushed and (self.form == BAT
                         or self.energy >> 8 >= k["ENERGY_STEP"]):
            self.transform()
        elif pushed:
            self.events.append((self.frame, "refused"))
            self.move_vampire()
        elif self.form == VAMPIRE:
            if (self.has_staff and not self.blow and joy & FIRE
                    and not self.prev_joy & FIRE):
                self.blow = self.c["BLOW_FRAMES"]   # the blow
                self.sfx("blow")
                self.events.append((self.frame, "blow"))
            self.move_vampire()
        else:
            self.move_bat()
        if self.y >> 8 >= k["BOTTOM"]:              # oscar_done
            self.fallen()
        if self.ground and self.has("bat"):
            if self.energy >> 8 < k["ENERGY_FULL"]:
                self.energy += k["RECHARGE"]
                if self.energy >> 8 >= k["ENERGY_FULL"]:
                    self.energy = k["ENERGY_FULL"] << 8
        self.prev_joy = joy

    def no_room(self):
        """The bat cannot turn back: a solid block in the rows of the
        vampire's body (his feet up 20 lines), in the column of one of
        his edges."""
        k = self.k
        feet = self.y >> 8
        first = max(feet - BODY_HEIGHTS[VAMPIRE], 0) >> 4
        last = (feet - 1) >> 4
        x = self.x >> 8
        return any(self.surfaces.solid((x + edge) >> 4, first, last)
                   for edge in (k["BODY_RIGHT"], k["BODY_LEFT"]))

    def bump_head(self):
        """Going up: his head in a solid block (in the column of one of
        his edges) stops him just under it."""
        k = self.k
        head = (self.y >> 8) - self.height
        if head < 0:
            return
        row = head >> 4
        x = self.x >> 8
        if any(self.surfaces.solid((x + edge) >> 4, row, row)
               for edge in (k["BODY_RIGHT"], k["BODY_LEFT"])):
            self.y = ((row + 1) * 16 + self.height) << 8
            self.vy = 0
            self.events.append((self.frame, "head"))

    def transform(self):
        self.sfx("change")
        self.form ^= 1
        self.blow = 0
        self.puff = self.k["PUFF_FRAMES"]
        self.flap = self.k["BEAT_FRAMES"]           # gliding
        self.vx = self.vy = self.gnam = 0
        self.events.append((self.frame, ("to bat", "to vampire")
                            [self.form == VAMPIRE]))

    @staticmethod
    def speed_step(v, push, move):
        """speed_step: push 1, -1 or 0; move: (accel, turn, slow,
        top)."""
        accel, turn, slow, top = move
        if push == 0:
            if v > 0:
                v = max(v - slow, 0)
            elif v < 0:
                v = min(v + slow, 0)
        elif push > 0:
            v += turn if v < 0 else accel
            if v >= 0:
                v = min(v, top)
        else:
            v -= turn if v > 0 else accel
            if v < 0:
                v = max(v, -top)
        return v

    def push_across(self):
        joy = self.joy
        if self.blow and self.ground and self.form == VAMPIRE:
            return 0                    # a blow on the ground: still
        push = 1 if joy & GO_RIGHT else -1 if joy & GO_LEFT else 0
        if push:
            self.face = RIGHT if push > 0 else LEFT
        return push

    def move_x(self):
        self.x += self.vx
        if self.x < 0:
            self.x, self.vx = 0, 0
        elif self.x >> 8 > self.x_max:
            self.x, self.vx = self.x_max << 8, 0
        self.push_out()
        self.sensor = (self.x >> 8) + self.k["SENSOR_X"]
        return self.sensor, self.y >> 8

    def push_out(self):
        """His body in a solid block: out of it, and he stops."""
        k = self.k
        self.height = BODY_HEIGHTS[self.form]
        feet = self.y >> 8
        first = max(feet - self.height, 0) >> 4
        last = (feet - 1) >> 4
        edge = (self.x >> 8) + k["BODY_RIGHT"]
        if self.surfaces.solid(edge >> 4, first, last):
            self.x = ((edge & 0xFFF0) - k["BODY_RIGHT"] - 1) << 8
            self.vx = 0
            self.events.append((self.frame, "blocked right"))
            return
        edge = (self.x >> 8) + k["BODY_LEFT"]
        if self.surfaces.solid(edge >> 4, first, last):
            self.x = ((edge | 15) - (k["BODY_LEFT"] - 1)) << 8
            self.vx = 0
            self.events.append((self.frame, "blocked left"))

    def land(self, sensor, feet, who):
        line = self.surfaces.find(sensor, feet, self.y >> 8)
        if line is not None:
            self.y, self.vy, self.ground = line << 8, 0, 1
            self.landed.append((self.frame, sensor, line, who,
                                self.level_no + 1))

    def move_vampire(self):
        k, joy = self.k, self.joy
        self.vx = self.speed_step(self.vx, self.push_across(),
                                  self.moves["walk"])
        sensor, feet = self.move_x()
        if self.ground:
            if joy & UP and not self.prev_joy & UP and not self.blow:
                self.vy = -k["JUMP_SPEED"]          # the jump
                self.sfx("jump")
                self.ground = 0
            else:
                line = self.surfaces.find(sensor, feet - k["STEP"],
                                          feet + k["STEP"])
                if line is not None:
                    self.y = line << 8              # still standing
                else:
                    self.ground, self.vy = 0, 0     # walked off
        if not self.ground:
            rising_held = self.vy < 0 and joy & UP
            self.vy += k["GRAVITY_HOLD"] if rising_held else k["GRAVITY"]
            self.vy = min(self.vy, k["FALL_MAX"])
            self.y += self.vy
            if self.vy < 0:
                if self.y >> 8 < k["CEILING"]:
                    self.y, self.vy = k["CEILING"] << 8, 0
                else:
                    self.bump_head()
            else:
                self.land(sensor, feet, "vampire")

    def move_bat(self):
        k, joy = self.k, self.joy
        if joy & UP and not self.prev_joy & UP:     # a beat
            if (self.energy >> 8) < k["FLAP_COST"]:
                self.events.append((self.frame, "out of energy"))
                self.transform()
                return
            self.energy -= k["FLAP_COST"] << 8
            self.vy = -k["FLAP_SPEED"]
            self.ground = self.flap = 0
            self.sfx("flap")
            self.events.append((self.frame, "beat"))
        if self.ground:                             # perched
            self.push_across()
            self.eat_moth()
            return
        self.vx = self.speed_step(self.vx, self.push_across(),
                                  self.moves["across"])
        sensor, feet = self.move_x()
        dive = bool(joy & DOWN)
        self.vy += k["BAT_DIVE"] if dive else k["BAT_GRAVITY"]
        if self.vy >= 0:
            self.vy = min(self.vy, k["BAT_DIVE_MAX"] if dive
                          else k["BAT_FALL_MAX"])
            if dive:
                self.events.append((self.frame, "dive"))
        self.y += self.vy
        if self.y >> 8 < k["BAT_TOP"]:
            self.y, self.vy = k["BAT_TOP"] << 8, 0
            self.events.append((self.frame, "top"))
        elif self.vy < 0:
            self.bump_head()
        elif self.vy > 0:
            self.land(sensor, feet, "bat")
            if self.ground:
                self.vx = 0
        self.eat_moth()

    def eat_moth(self):
        k, c = self.k, self.c
        sensor = (self.x >> 8) + k["SENSOR_X"]
        col = sensor >> 4
        row = (((self.y >> 8) - k["BAT_MIDDLE"]) & 255) >> 4
        if self.level[col * 11 + row] != c["MOTH_TILE"]:
            return
        self.moths_eaten += 1
        self.add_score(10)
        self.sfx("moth")
        self.gnam = k["GNAM_FRAMES"]
        whole = (self.energy >> 8) + k["MOTH_ENERGY"]
        if whole >= k["ENERGY_FULL"]:
            self.energy = k["ENERGY_FULL"] << 8
        else:
            self.energy = (whole << 8) | (self.energy & 255)
        self.events.append((self.frame, f"moth {col},{row}"))
        self.set_tile(col, row, c["EMPTY_SKY"])

    def set_tile(self, col, row, tile):
        """A metatile into the level and onto the screens: front,
        colour RAM, back (one column over; edge_paint if that is the
        column just drawn)."""
        self.level[col * 11 + row] = tile
        at = (col * 2 - (self.camera >> 3)) & 255
        shift = -1 if self.prep_dir == RIGHT else 1
        edge_column = 38 if self.prep_dir == RIGHT else 0
        for corner in (3, 2, 1, 0):
            code = reference.corner(self.files, tile, corner)
            dx, dy = corner & 1, corner >> 1
            cell_row = row * 2 + dy
            column = (dx + at) & 255
            if column < 39:
                self.screens[self.front][(column, cell_row)] = code
                self.colours[(column, cell_row)] = \
                    self.files["charcolour"][code]
            column = (dx + at + shift) & 255
            if column < 39:
                if column == edge_column and self.prep_stage == 3:
                    self.edge[cell_row] = self.files["charcolour"][code]
                    self.edge_paints += 1
                self.screens[1 - self.front][(column, cell_row)] = code

    def animate(self):
        k = self.k
        if self.puff:
            self.picture = k["PUFF"] + (k["PUFF_FRAMES"] - self.puff) // 4
            return
        if self.form == BAT:
            if self.flap < k["BEAT_FRAMES"]:
                self.flap += 1
            if self.gnam:
                self.gnam -= 1
                picture = GNAM
            elif self.ground:
                picture = PERCH
            elif self.flap >= k["BEAT_FRAMES"]:
                picture = FLY_B                     # gliding
            else:
                picture = BEAT_CYCLE[self.flap >> 2]
            self.picture = k["BAT_PICTURES"] + picture + 5 * self.face
            return
        if not self.ground:
            picture = JUMP if self.vy < 0 else FALL
        elif self.vx == 0:
            picture = STAND
        else:
            self.anim = (self.anim + abs(self.vx)) & 0xFFFF
            picture = WALK_CYCLE[(self.anim >> 11) & 3]
        self.picture = self.face * 6 + picture

    # --- the heirlooms, the lantern, the gate, the night ----------
    def touch_things(self):
        self.open_door()
        self.touch_staff()
        self.touch_heirlooms()
        self.touch_lantern()
        self.touch_gate()

    def touch_staff(self):
        """The staff lying in the level: his middle (the sensor) within
        STAFF_TOUCH pixels of its middle, his feet on its line or
        lower and his head above it: he takes it."""
        place = self.objects["staff"]
        if self.has_staff or place is None:
            return
        x, line = place
        if abs(self.sensor - x - 12) >= self.k["STAFF_TOUCH"]:
            return
        feet = self.y >> 8
        if feet < line or feet - self.height >= line:
            return
        self.has_staff = 1
        self.events.append((self.frame, "staff"))

    def touch_heirlooms(self):
        k = self.k
        feet = self.y >> 8
        for index in (2, 1, 0):
            x, top, block = self.objects["heirlooms"][index]
            if self.got_bits & (1 << index):
                continue
            if abs(self.sensor - x - 12) >= k["TOUCH"]:
                continue
            if top >= feet:
                continue
            head = feet - self.height
            if head >= 0 and head >= top + k["HEIRLOOM_BOX"]:
                continue
            self.got_bits |= 1 << index
            self.got += 1
            self.add_score(500)
            self.sfx("heirloom")
            self.taken.append((self.frame, index))
            self.events.append((self.frame, f"heirloom {index}"))
            if self.got == len(self.objects["heirlooms"]):
                self.open_gate()

    def touch_lantern(self):
        col, row = self.objects["lantern"]
        if self.lantern_lit or self.sensor >> 4 != col:
            return
        if self.y >> 8 < row * 16:
            return
        self.lantern_lit = 1
        self.sfx("lantern")
        self.respawn_x = col * 16 + 8 - 12
        self.events.append((self.frame, "lantern"))
        self.set_tile(col, row, self.objects["lantern_tile"])

    def open_gate(self):
        """The gate opens: touch_gate lets him through at once; its
        doors become their open tiles one a frame, from the next
        (open_door), the last first."""
        self.sfx("gate")
        self.door_open = len(self.objects["doors"]) + 1
        self.events.append((self.frame, "gate open"))

    def open_door(self):
        """door_open: the doors left to open, plus 1; 1: open."""
        if self.door_open < 2:
            return
        self.door_open -= 1
        col, row, tile = self.objects["doors"][self.door_open - 1]
        self.set_tile(col, row, tile)

    def touch_gate(self):
        first, last, top = self.objects["door"]
        if not self.door_open:
            return
        if not first <= self.sensor >> 4 <= last:
            return
        if self.y >> 8 < top * 16 + 1:
            return
        self.events.append((self.frame, "through the gate"))
        if (self.level_no == self.c["LEVEL_COUNT"] - 1
                and self.has("tom")):
            self.start_transition(GO_ARENA)
        elif self.has("states"):
            self.start_tally()
        else:
            self.start_transition(GO_NEXT)  # steps 5-11

    def tick_night(self):
        if self.game_state != ST_PLAY:      # stopped this turn
            return
        self.night_time -= 1
        if self.night_time:
            return
        self.night_time = self.k["NIGHT_STEP"]
        self.night -= 1
        if self.night == 0:
            self.events.append((self.frame, "dawn"))
            if self.has("states"):
                self.start_dawn()
            else:
                self.start_transition(GO_START)     # steps 5-11
        elif (self.has("sound")             # step 13
              and self.night <= self.k["TOLL_STEPS"]):
            self.sfx("toll")                # the bell
            self.events.append((self.frame, "toll"))

    def show_hud(self):
        """show_hud: the bars and the heirlooms taken, in the HUD
        rows (the same in both screens)."""
        c = self.c
        bars = [(self.health, 4, c["HEALTH_BAR"])]
        if self.has("bat"):
            bars.append(((self.energy >> 8) >> 5, 3, c["ENERGY_BAR"]))
        if self.has("objects"):
            bars.append((self.night, 8, c["NIGHT_BAR"]))
        for value, count, at in bars:
            for i in range(count):
                self.hud_bytes[at - 880 + i] = c["BAR_EMPTY"] + min(value, 2)
                value = max(value - 2, 0)
        if self.has("objects"):
            self.hud_bytes[c["HEIRLOOM_DIGIT"] - 880] = \
                c["DIGIT_0"] + self.got
        if self.score_new and self.has("states"):   # the score
            self.write_score()
        if self.arena:                      # Tom's bar
            value = self.tom_hits
            for i in range(4):
                self.hud_bytes[c["TOM_BAR"] - 880 + i] = \
                    c["BAR_EMPTY"] + min(value, 2)
                value = max(value - 2, 0)

    def show_name(self):
        """show_name: row 24, the level's number and name; in the
        arena, Tom's."""
        at = (self.c["LEVEL_COUNT"] if self.arena else self.level_no) * 80
        self.hud_bytes[80:120] = self.names[at:at + 40]
        self.hud_colours[80:120] = self.names[at + 40:at + 80]
        if self.has("states"):
            self.write_score()

    def hud(self):
        """The HUD's 240 bytes (characters, colours) as shown."""
        return bytes(self.hud_bytes) + bytes(self.hud_colours)

    def place_heirloom(self):
        """Sprite 7: the heirloom on the screen, if any."""
        for index in (2, 1, 0):
            x, top, block = self.objects["heirlooms"][index]
            if self.got_bits & (1 << index):
                continue
            register = x - self.camera + 31
            if not 0 <= register < 344:
                continue
            bob = 1 if self.night_time & 16 else 0
            self.sprite7 = (register, top + 50 + bob,
                            self.k["HEIRLOOM_BLOCKS"] + block, block)
            self.d010 = (self.d010 & 0x7F) | (0x80 if register > 255
                                              else 0)
            self.sprites_on |= 0x80
            self.shown = index
            return
        self.sprites_on &= 0x7F
        self.shown = None

    def charset(self, env=None):
        """A character set (the setting's, by default) as the VIC-II
        sees it now: the village's at CHARSET with the moths' picture of
        now; another's in SET_SLOT with the pictures of its moth and of
        its flickering hazards there."""
        env = self.env if env is None else env
        charset = bytearray(self.all_files["envs"][env]["charset"])
        at = self.c["MOTH_CHAR"] * 8
        moth = self.moth_frame if env == 0 else self.slot_moth
        charset[at:at + 16] = self.moth_pictures[moth * 16:moth * 16 + 16]
        if env and self.c["FLICKER_SETTINGS"] >> env & 1:
            at = self.c["FLICKER_CHAR"] * 8
            first = flicker_page(self.c, env) * 256 + self.slot_flicker * 64
            charset[at:at + 64] = self.flicker_pictures[first:first + 64]
        return bytes(charset)

    def slot(self):
        """SET_SLOT's 2048 bytes: the set of slot_env (zeros before the
        first is copied, but for the moth)."""
        if self.slot_env is not None:
            return self.charset(self.slot_env)
        slot = bytearray(2048)
        at = self.c["MOTH_CHAR"] * 8
        moth = self.slot_moth
        slot[at:at + 16] = self.moth_pictures[moth * 16:moth * 16 + 16]
        return bytes(slot)

    def only(self, values, parts):
        """values, with None (any byte) where the step has not got the
        part that byte is of (parts: one name of FIRST, or None, for
        each)."""
        return [value if part is None or self.has(part) else None
                for value, part in zip(values, parts)]

    def form_state(self):
        """$38-$3e: form, puff, energy (2), gnam, flap, moths."""
        return [self.form, self.puff, self.energy & 255,
                self.energy >> 8, self.gnam, self.flap,
                self.moths_eaten]

    def level_state(self):
        """$e0-$ee: health ... respawn_x, level_no, protect, stun."""
        return self.only(
            [self.health, self.night, self.night_time & 255,
             self.night_time >> 8, self.got, self.got_bits,
             self.lantern_lit, self.door_open, self.trans,
             self.trans_kind if self.trans_kind is not None else None,
             self.respawn_x & 255, self.respawn_x >> 8,
             self.level_no, self.protect, self.stun],
            ["oscar"] + ["objects"] * 7 + ["oscar", "oscar", None, None,
                                           None, "enemies", "enemies"])

    def staff_state(self):
        """$f0-$f2: the staff held, the blow, the setting."""
        return self.only([self.has_staff, self.blow, self.env],
                         ["staff", "staff", None])

    def oscar_screen_x(self):
        return (self.x >> 8) - self.camera + 7

    # --- the camera -----------------------------------------------
    def follow(self):
        """The camera keeps Oscar between ZONE_LEFT and ZONE_RIGHT
        (screen x of his left edge), 2 pixels a frame at most."""
        k = self.k
        self.last_dir = self.face
        self.swap = 0
        if self.arena:                      # the camera stays
            return
        sx = self.oscar_screen_x()
        if sx > k["ZONE_RIGHT"]:
            self.move_camera(RIGHT, min(sx - k["ZONE_RIGHT"], 2))
        elif sx < k["ZONE_LEFT"]:
            self.move_camera(LEFT, min(k["ZONE_LEFT"] - sx, 2))

    def move_camera(self, direction, step):
        if direction == RIGHT:
            nxt = min(self.camera + step, self.camera_max)
            if nxt & 7 < self.camera & 7:          # next column
                if self.prep_dir == RIGHT and self.prep_stage == 3:
                    self.swap = 1
                else:
                    nxt = self.camera | 7
                    self.holds[RIGHT] += 1
        else:
            nxt = max(self.camera - step, 0)
            if nxt & 7 > self.camera & 7:          # column before
                if self.prep_dir == LEFT and self.prep_stage == 3:
                    self.swap = 1
                else:
                    nxt = self.camera & ~7
                    self.holds[LEFT] += 1
        self.camera = nxt
        self.set_xscroll()

    def set_xscroll(self):
        self.xscroll = 0x10 | ((self.camera & 7) ^ 7)

    def place_staff(self):
        """Sprite 2: the staff in his hand (not the bat's, not in the
        smoke; blinking with him), its place and picture from his
        picture or from the blow; or lying in the level, on the
        screen; or nothing."""
        k = self.k
        files = self.all_files
        self.d010 &= 0xFB
        self.staff_sprite = None
        if self.has_staff:
            if self.form != VAMPIRE or self.puff:
                self.sprites_on &= 0xFB
                return
            tables = files["staff_tables"]
            if self.blow:
                dx, dy, block = tables["blow"][self.face * 10
                                               + self.blow - 1]
            else:
                dx, dy, block = tables["held"][self.picture]
            register = (self.sprite_x + dx) & 0x1FF
            y = (self.sprite_y + dy) & 255
            if self.protect & 4:
                self.sprites_on &= 0xFB
            else:
                self.sprites_on |= 0x04
        else:
            place = self.objects["staff"]
            if place is None:
                self.sprites_on &= 0xFB
                return
            register = place[0] - self.camera + 31
            if not 0 <= register < 344:
                self.sprites_on &= 0xFB
                return
            y = (place[1] + 29) & 255
            block = self.c["STAFF_LYING"]
            self.sprites_on |= 0x04
        if register > 255:
            self.d010 |= 0x04
        self.staff_sprite = (register, y, k["STAFF_BLOCKS"] + block)

    def place_oscar(self):
        self.sprite_x = (self.x >> 8) - self.camera + 31
        self.sprite_y = (self.y >> 8) + 29
        self.placed = self.picture
        # the others' ninth bits kept (the moon's, in a fall)
        self.d010 = (self.d010 & 0xFC) | (3 if self.sprite_x > 255 else 0)
        if self.protect & 4:            # blinking, after a hit
            self.sprites_on &= 0xFC
        else:
            self.sprites_on |= 3

    # --- the enemies (enemies.asm) --------------------------------
    def kind_of(self, type_):
        """The behaviour of a type of enemy (TYPEn_KIND)."""
        return self.c[f"TYPE{type_}_KIND"]

    def reset_enemies(self):
        """Each enemy of the level at its start (and back, if
        struck)."""
        for i in range(len(self.objects["enemies"])):
            self.reset_enemy(i)

    def move_enemies(self):
        k = self.k
        for i, (type_, x_min, x_max, _, line, _) in enumerate(
                self.objects["enemies"]):
            if self.en_gone[i]:         # struck: its puff, then gone
                if self.en_gone[i] != GONE:
                    self.en_gone[i] -= 1
                    if self.en_gone[i] == 0:
                        self.en_gone[i] = GONE
                continue
            kind = self.kind_of(type_)
            if kind == JUMPER:
                self.move_jumper(i, x_min, x_max)
                continue
            step = k["PATROL_SPEED"] if kind == PATROL else k["FLYER_SPEED"]
            if self.en_dir[i] == RIGHT:
                self.en_x[i] += step
                if self.en_x[i] >> 8 >= x_max:
                    self.en_x[i], self.en_dir[i] = x_max << 8, LEFT
            else:
                self.en_x[i] -= step
                if self.en_x[i] >> 8 <= x_min:
                    self.en_x[i], self.en_dir[i] = x_min << 8, RIGHT
            if kind == PATROL:
                self.en_timer[i] = (self.en_timer[i] + 1) & 255
            else:
                self.en_timer[i] = (self.en_timer[i] + 1) & 63
                self.en_y[i] = (line + WAVE[self.en_timer[i]]) << 8
            self.en_pic[i] = (self.en_timer[i] >> 3) & 1

    def move_jumper(self, i, x_min, x_max):
        """The cat, the toad: sitting, it looks at Oscar and waits;
        then, if he is near, it jumps at him; in the air it falls onto
        the first surface under it."""
        k = self.k
        ex, ox = self.en_x[i] >> 8, self.x >> 8
        if not self.en_air[i]:
            self.en_dir[i] = LEFT if ox < ex else RIGHT
            if self.en_timer[i]:
                self.en_timer[i] -= 1
                return
            self.en_timer[i] = k["CAT_WAIT"]
            if abs(ox - ex) >= k["CAT_REACH"]:
                return
            self.en_vy[i] = -k["CAT_JUMP"]
            self.en_vx[i] = (k["CAT_VX"] if self.en_dir[i] == RIGHT
                             else -k["CAT_VX"])
            self.en_air[i] = self.en_pic[i] = 1
            self.events.append((self.frame, "cat jumps"))
            return
        self.en_x[i] += self.en_vx[i]
        if self.en_vx[i] >= 0:
            if self.en_x[i] >> 8 >= x_max:
                self.en_x[i], self.en_vx[i] = x_max << 8, 0
        elif self.en_x[i] >> 8 <= x_min:
            self.en_x[i], self.en_vx[i] = x_min << 8, 0
        old = self.en_y[i] >> 8
        self.en_vy[i] = min(self.en_vy[i] + k["CAT_GRAVITY"], k["FALL_MAX"])
        self.en_y[i] += self.en_vy[i]
        if self.en_vy[i] >= 0:
            line = self.surfaces.find((self.en_x[i] >> 8) + 12, old,
                                      self.en_y[i] >> 8)
            if line is not None:
                self.en_y[i] = line << 8
                self.en_vx[i] = self.en_vy[i] = 0
                self.en_air[i] = self.en_pic[i] = 0
                self.en_timer[i] = k["CAT_WAIT"]
                self.events.append((self.frame, "cat lands"))
        if self.en_y[i] >> 8 >= k["BOTTOM"]:
            self.reset_enemy(i)

    def reset_enemy(self, i):
        _, _, _, x, line, face = self.objects["enemies"][i]
        self.en_x[i], self.en_y[i] = x << 8, line << 8
        self.en_vx[i] = self.en_vy[i] = 0
        self.en_dir[i], self.en_timer[i] = face, 0
        self.en_air[i] = self.en_pic[i] = self.en_gone[i] = 0
        self.enemy_slots = max(self.enemy_slots, i + 1)

    def enemy_box(self, i):
        """An enemy's box: (left x, right x, top line, bottom line);
        its top not above line 0, its bottom a byte (as strike)."""
        c = self.c
        type_ = self.objects["enemies"][i][0]
        ex, ey = self.en_x[i] >> 8, self.en_y[i] >> 8
        left = c[f"TYPE{type_}_LEFT"]
        return (ex + left, ex + 23 - left,
                max(ey - c[f"TYPE{type_}_UP"], 0),
                (ey - c[f"TYPE{type_}_DOWN"]) & 255)

    def hit_enemies(self):
        """The blow strikes first: the enemies whose box meets the
        staff's reach, in the frames that strike. Then, unless he is
        still blinking from the last time: a hazard in his body, or
        an enemy's box over it: he is hit."""
        k, c = self.k, self.c
        feet, ox = self.y >> 8, self.x >> 8
        if (self.form == VAMPIRE and not self.puff and
                c["STRIKE_LAST"] <= self.blow <= c["STRIKE_FIRST"]):
            if self.face == RIGHT:
                x0 = ox + k["BODY_RIGHT"] + 1
                x1 = ox + k["BODY_RIGHT"] + c["STRIKE_REACH"]
            else:
                x0 = max(ox + k["BODY_LEFT"] - c["STRIKE_REACH"], 0)
                x1 = ox + k["BODY_LEFT"] - 1
            top = max(feet - c["STRIKE_UP"], 0)
            bottom = (feet - c["STRIKE_DOWN"]) & 255
            # The program goes through them from the last.
            for i in reversed(range(len(self.objects["enemies"]))):
                if self.en_gone[i]:
                    continue
                left, right, etop, ebottom = self.enemy_box(i)
                if left <= x1 and right >= x0 and etop <= bottom \
                        and ebottom >= top:
                    self.en_gone[i] = k["ENEMY_PUFF"]
                    self.add_score(100)
                    self.sfx("struck")
                    self.struck.append((self.frame,
                                        self.objects["enemies"][i][0],
                                        self.face, self.ground))
                    self.events.append((self.frame, "struck"))
        if self.protect:
            self.protect -= 1
            return
        hazard = self.in_hazard()
        if hazard is not None:
            self.hit(hazard, -1)
            return
        enemies = list(enumerate(self.objects["enemies"]))
        for i, (type_, *_) in reversed(enemies):   # from the last
            if self.en_gone[i]:
                continue
            # Boxes the same from both sides (Oscar's too): touching
            # across is |x - his x| up to his right edge less its left.
            ex = self.en_x[i] >> 8
            if abs(ex - ox) > k["BODY_RIGHT"] - c[f"TYPE{type_}_LEFT"]:
                continue
            dy = (self.en_y[i] >> 8) - feet
            if (dy > c[f"TYPE{type_}_UP"] - 1
                    or dy < c[f"TYPE{type_}_DOWN"] - self.height):
                continue
            self.hit(ex > ox, type_)
            return

    def in_hazard(self):
        """A hazard in his body: in the column of his right edge
        (True: he is thrown left), else of his left edge (False);
        None if none."""
        k = self.k
        feet, ox = self.y >> 8, self.x >> 8
        first = max(feet - self.height, 0) >> 4
        last = (feet - 1) >> 4
        for edge, from_right in ((k["BODY_RIGHT"], True),
                                 (k["BODY_LEFT"], False)):
            if self.surfaces.solid((ox + edge) >> 4, first, last,
                                   self.c["HAZARD"]):
                return from_right
        return None

    def hit(self, from_right, kind):
        """A touch: HIT_DAMAGE of the health, PROTECT_FRAMES of
        blinking; out of the smoke, a jump back, away from the enemy
        (or the hazard), and KNOCK_FRAMES without the joystick. No
        health left: back at the lantern (or the start), as after a
        fall. `kind`: the enemy's type, or -1 for a hazard."""
        k = self.k
        self.sfx("hurt")
        self.health = max(self.health - k["HIT_DAMAGE"], 0)
        self.protect = k["PROTECT_FRAMES"]
        self.hit_by.append((self.frame, kind))
        hazard = HAZARD_NAMES.get(reference.ENVIRONMENTS[self.env],
                                  "brambles")
        self.events.append((self.frame, "hit" if kind >= 0 else hazard))
        if not self.puff:
            knock = KNOCK_X[self.form]
            self.vx = -knock if from_right else knock
            self.vy = -KNOCK_Y[self.form]
            self.ground = 0
            self.stun = k["KNOCK_FRAMES"]
        if self.health == 0:
            self.events.append((self.frame, "no health"))
            self.fallen()

    # --- the game's states (states.asm) ---------------------------
    def states_bytes(self):
        """STATES: game_state, sound_mode, score (3, BCD, low first),
        score_new, state_timer, state_phase, band_on, band_top,
        band_end, band_d018."""
        digits = f"{self.score % 1000000:06d}"
        bcd = [int(digits[4:6], 16), int(digits[2:4], 16),
               int(digits[0:2], 16)]
        return ([self.game_state, self.sound_mode] + bcd
                + [self.score_new, self.state_timer & 255,
                   self.state_phase, self.band_on, self.band_top,
                   self.band_end, self.band_d018])

    def add_score(self, points):
        self.score += points
        self.score_new = 1

    def write_score(self):
        """Row 24, from SCORE_CELL: six digits."""
        at = self.c["SCORE_CELL"] - 880
        digits = f"{self.score % 1000000:06d}"
        for i, digit in enumerate(digits):
            self.hud_bytes[at + i] = self.c["DIGIT_0"] + int(digit)
        self.score_new = 0

    def new_keys(self):
        """The keys pushed now and not in the frame before."""
        pushed = self.joy & ~self.prev_joy & 255
        self.prev_joy = self.joy
        return pushed

    def put_texts(self, records):
        """Into both screens (rows 0-21 here; the HUD's rows into
        hud_bytes), their colours into the colour RAM (hud_colours)."""
        for row, column, colour, codes in records:
            for i, code in enumerate(codes):
                col = column + i
                if row >= ROWS:
                    at = (row - ROWS) * 40 + col
                    self.hud_bytes[at] = code
                    self.hud_colours[at] = colour
                elif col < reference.VISIBLE:
                    self.screens[0][(col, row)] = code
                    self.screens[1][(col, row)] = code
                    self.colours[(col, row)] = colour

    def clear_rows(self, first, rows):
        """Blank, in both screens; the colour RAM black."""
        for row in range(first, first + rows):
            if row >= ROWS:
                at = (row - ROWS) * 40
                self.hud_bytes[at:at + 40] = bytes(40)
                self.hud_colours[at:at + 40] = bytes(40)
                continue
            for col in range(reference.VISIBLE):
                self.screens[0][(col, row)] = 0
                self.screens[1][(col, row)] = 0
                self.colours[(col, row)] = 0

    def show_band(self, number):
        """Band `number`: its rows blank in both screens, its words;
        the lines of its interrupts; the HUD's set, the screen
        shown."""
        first, rows, records = self.texts["bands"][number]
        self.band_top = first * 8 + self.k["BAND_LINE"]
        self.band_end = self.band_top + (rows - 1) * 8
        self.clear_rows(first, rows)
        self.put_texts(records)
        self.band_d018 = (self.shown_d018 & 0xF0) | 0x04
        self.band_on = 1
        self.events.append((self.frame, f"band {number}"))

    def show_menu(self):
        c = self.c
        self.clear_rows(c["MENU_ROW"], c["MENU_CHOICES"])
        self.put_texts(self.texts["menu"])
        at = (c["MENU_ROW"] + self.sound_mode - ROWS) * 40
        self.hud_bytes[at + c["POINTER_COL"]] = c["POINTER_CODE"]
        self.hud_colours[at + c["POINTER_COL"]] = c["POINTER_COLOUR"]
        for col in range(c["MENU_COL"], c["MENU_COL"] + 8):
            self.hud_colours[at + col] = c["CHOSEN_COLOUR"]

    def title_place(self):
        """Oscar at the castle's door of level 7, the camera as far
        right as it goes; the menu."""
        self.respawn_x = self.c["TITLE_X"]
        self.respawn()
        self.show_menu()

    def title_sprites(self):
        """Oscar; the name (sprites 2-5); the moon between the towers;
        sprite 7 off."""
        c = self.c
        self.place_oscar()
        self.logo_on = True
        self.enemy_sprites = []
        self.staff_sprite = None
        self.moon_sprite = (c["TITLE_MOON_X"], c["TITLE_MOON_Y"],
                            self.k["MOON_BLOCK"])
        self.d010 &= 0x03
        self.sprites_on = (self.sprites_on & 0x03) | 0x7C

    def init_sprites(self):
        """init_sprites (vic.asm), after the title: no stretching,
        multicolour, sprites 0 and 1 on."""
        self.logo_on = False
        self.sprites_on = 0x03

    def title_music(self):
        if self.sound_mode != MUSIC:
            if self.mus_on:
                self.events.append((self.frame, "silence"))
            self.music_stop()
        elif not (self.mus_on and self.mus_song == 0):
            self.music_start(0)
            self.events.append((self.frame, "theme"))

    def title_turn(self):
        pushed = self.new_keys()
        c = self.c
        if pushed & FIRE:
            self.start_transition(GO_START)
            return
        chosen = self.sound_mode
        if pushed & UP:
            chosen = max(chosen - 1, 0)
        elif pushed & DOWN:
            chosen = min(chosen + 1, c["MENU_CHOICES"] - 1)
        if chosen != self.sound_mode:
            self.sound_mode = chosen
            self.show_menu()
            self.title_music()
            self.sfx("click")
            self.events.append((self.frame, f"menu {chosen}"))
        colour = c["PRESS_OFF"] if self.turn_frame & 32 else c["PRESS_ON"]
        at = c["PRESS_CELL"] - 880
        for i in range(c["PRESS_LENGTH"]):
            self.hud_colours[at + i] = colour

    def new_game(self):
        """A new game: the score 0, no staff, the HUD's rows 22-23."""
        self.score = 0
        self.has_staff = 0
        self.hud_bytes[:80] = self.all_files["hud"][:80]
        self.hud_colours[:80] = self.all_files["hud"][120:200]

    def start_tally(self):
        self.game_state, self.state_phase = ST_TALLY, 0
        self.state_timer = self.k["TALLY_WAIT"]
        self.jingle(SONG_CLEAR)
        self.show_band(self.c["BAND_CLEAR"])

    def count_night(self):
        """A step of the night into the score (50); False: none."""
        if not self.night:
            return False
        self.night -= 1
        self.add_score(self.night_points)
        self.counted += 1
        self.show_hud()
        return True

    def tally_turn(self):
        k = self.k
        self.state_timer -= 1
        if self.state_timer:
            return
        if self.state_phase:
            self.start_transition(GO_NEXT)
            return
        if self.count_night():
            self.state_timer = k["TALLY_TICK"]
        else:
            self.state_phase = 1
            self.state_timer = k["TALLY_END"]

    def start_won(self):
        self.game_state, self.state_phase = ST_WON, 0
        self.state_timer = self.k["WON_WAIT"]
        self.jingle(SONG_WON)
        self.events.append((self.frame, "victory"))
        self.show_band(self.c["BAND_WON"])

    def won_turn(self):
        pushed = self.new_keys()
        if self.state_phase:
            self.fire_title(pushed)
            return
        self.state_timer -= 1
        if self.state_timer:
            return
        counted = self.count_night()
        self.state_timer = self.k["TALLY_TICK"]
        if not counted:
            self.state_phase = 1

    def fire_title(self, pushed):
        if pushed & FIRE:
            self.start_transition(GO_TITLE)

    def start_dawn(self):
        self.game_state, self.state_phase = ST_DAWN, 0
        self.state_timer = self.c["DAWN_FRAMES"]
        self.jingle(SONG_DAWN)

    def dawn_turn(self):
        k, c = self.k, self.c
        pushed = self.new_keys()
        phase = self.state_phase
        if phase > c["DAWN_STEPS"]:
            self.fire_title(pushed)
        elif phase == c["DAWN_STEPS"]:          # the puff
            self.puff -= 1
            if self.puff:
                self.animate()
                self.place_oscar()
                self.place_staff()
                return
            self.sprites_on &= 0xF8
            self.state_phase += 1
            self.show_band(self.c["BAND_DAWN"])
        else:
            self.state_timer -= 1
            if self.state_timer:
                return
            self.dawn_d021 = self.texts["dawn"][phase]
            self.state_phase += 1
            self.state_timer = c["DAWN_FRAMES"]
            if phase == c["DAWN_STEPS"] - 1:
                self.puff = k["PUFF_FRAMES"]
                self.events.append((self.frame, "sunrise"))

    def setting_registers(self, top=False):
        """$d021, $d022, $d023 and $d01b as next_env leaves them for the
        setting: black, the setting's shared colours (in the castle
        its first too, medium grey in the hall); the moon (sprite 6)
        behind the characters where the setting puts it there (the
        crags). $d021: black after the HUD's interrupt; after
        the top one (`top`) the playfield's, the setting's (blue in the
        castle)."""
        c = self.c
        d021 = self.play_d021() if top else c["D021_SKY"]
        return (d021, c[f"ENV{self.env}_D022"], c[f"ENV{self.env}_D023"],
                0x40 if c["MOON_BEHIND"] >> self.env & 1 else 0)

    def play_d021(self):
        """play_d021: the background next_env leaves for the
        top interrupt, the setting's; at dawn, its colour."""
        if self.dawn_d021 is not None:
            return self.dawn_d021
        return self.c[f"ENV{self.env}_D021"]

    def moon_here(self):
        """A setting with a moon (moon.py: the wood)."""
        return bool(self.c["MOON_SETTINGS"] >> self.env & 1)

    def place_enemies(self):
        """Sprites 3-6: the enemies on the screen, in their order,
        four at most, three where the moon is (sprite 6); struck, its
        puff (the smoke's pictures, in its colour), then nothing. Then
        the moon."""
        k, c = self.k, self.c
        self.d010 &= 0x87
        self.sprites_on &= 0x87
        self.enemy_sprites = []
        slots = 3 if self.moon_here() else 4
        for i, (type_, *_) in enumerate(self.objects["enemies"]):
            if len(self.enemy_sprites) == slots:
                break
            if self.en_gone[i] == GONE:
                continue
            register = (self.en_x[i] >> 8) - self.camera + 31
            if not 0 <= register < 344:
                continue
            slot = len(self.enemy_sprites)
            if self.en_gone[i]:
                puff = (k["ENEMY_PUFF"] - self.en_gone[i]) >> 2
                block = k["OSCAR_LINES"] + (k["PUFF"] + puff) * 2 + 1
            else:
                block = (self.type_block(type_)
                         + self.en_dir[i] * 2 + self.en_pic[i])
            self.enemy_sprites.append(
                (register, ((self.en_y[i] >> 8) + 29) & 255, block,
                 c[f"TYPE{type_}_COLOUR"], type_, block))
            if register > 255:
                self.d010 |= 8 << slot
            self.sprites_on |= 8 << slot
        self.place_moon()

    def type_block(self, type_):
        """The first of the four blocks of a type of enemy (type_block):
        the village's and the wood's at ENEMY_BLOCKS, the
        others' at ENEMY_BLOCKS_2."""
        first = self.c["ENEMY_TYPES_1"]
        if type_ < first:
            return self.k["ENEMY_BLOCKS"] + 4 * type_
        return self.k["ENEMY_BLOCKS_2"] + 4 * (type_ - first)

    def place_moon(self):
        """Sprite 6 where the moon is (the wood): still on the screen,
        up on the right, whatever the camera."""
        c = self.c
        if not self.moon_here():
            self.moon_sprite = None
            return
        self.moon_sprite = (c["MOON_X"], c["MOON_Y"], self.k["MOON_BLOCK"])
        self.sprites_on |= 0x40
        if c["MOON_X"] > 255:
            self.d010 |= 0x40

    # --- Tom Darkfang (tom.asm) ------------------------------------
    def reset_tom(self):
        """reset_tom: in front of his throne, facing left, all his
        hits, waiting; nothing shown (the page to copy into next: the
        second)."""
        k, c = self.k, self.c
        self.tom_front = 0
        self.tom_x = c["TOM_START_X"] << 8
        self.tom_y = c["START_Y"] << 8
        self.tom_vx = self.tom_vy = 0
        self.tom_flash = self.tom_safe = self.tom_next = 0
        self.tom_state, self.tom_timer = k["TS_WAIT"], k["WAIT_FRAMES"]
        self.tom_face, self.tom_pic = LEFT, k["T_STAND"]
        self.tom_hits = k["HITS_FULL"]
        self.tom_shown = 0xFF

    def tom_to(self, state, timer, picture):
        self.tom_state, self.tom_timer, self.tom_pic = \
            state, timer, picture

    def tom_fast(self):
        """With half his hits gone (or more) he is faster."""
        return self.tom_hits <= self.k["HITS_FAST"]

    def fight_tom(self):
        """A frame of the fight: he moves; the blow strikes him; while
        Oscar blinks nothing counts, else Tom's touch."""
        k = self.k
        if self.tom_flash:
            self.tom_flash -= 1
        moves = {k["TS_WAIT"]: self.tom_wait,
                 k["TS_GROWL"]: self.tom_growl,
                 k["TS_LEAP"]: self.tom_leap,
                 k["TS_LAND"]: self.tom_land,
                 k["TS_CHARGE"]: self.tom_charge,
                 k["TS_DAZED"]: self.tom_dazed,
                 k["TS_YELP"]: self.tom_yelp,
                 k["TS_RUN"]: self.tom_run,
                 k["TS_HOP"]: self.tom_hop,
                 k["TS_PAUSE"]: self.tom_pause,
                 k["TS_UP"]: self.tom_up,
                 k["TS_GONE"]: self.tom_gone}
        moves[self.tom_state]()
        self.strike_tom()
        if self.protect:
            self.protect -= 1
            return
        self.touch_tom()

    def face_oscar(self):
        """Left if Oscar's middle is left of Tom's (x + 12, x + 24)."""
        d = (self.x >> 8) - (self.tom_x >> 8)
        self.tom_face = LEFT if d < 12 else RIGHT

    def tom_wait(self):
        self.face_oscar()
        self.tom_timer -= 1
        if not self.tom_timer:
            self.growl()

    def tom_growl(self):
        self.face_oscar()
        self.tom_timer -= 1
        if self.tom_timer:
            return
        self.tom_safe = 0
        self.tom_next ^= 1
        if self.tom_next:               # it was 0: a leap
            self.leap()
        else:
            self.charge()

    def growl(self):
        k = self.k
        self.sfx("growl")
        self.tom_to(k["TS_GROWL"], k["GROWL_FAST"] if self.tom_fast()
                    else k["GROWL_FRAMES"], k["T_GROWL"])
        self.events.append((self.frame, "tom growls"))

    def leap(self):
        """At where Tom's middle is under Oscar's (Oscar's x - 12), in
        the arena, at most LEAP_REACH away: a 32nd of the way a
        frame."""
        k, c = self.k, self.c
        there = min(max((self.x >> 8) - 12, c["TOM_MIN_X"]),
                    c["TOM_MAX_X"])
        dx = there - (self.tom_x >> 8)
        dx = max(min(dx, k["LEAP_REACH"]), -k["LEAP_REACH"])
        self.tom_vx = (dx * 8) & 0xFFFF
        self.tom_vy = -k["LEAP_VY"] & 0xFFFF
        self.tom_to(k["TS_LEAP"], 0, k["T_RUN_B"])
        self.events.append((self.frame, "tom leaps"))

    def tom_across(self):
        """x + vx (24 bits, signed); out of the arena: at its edge,
        still across."""
        c = self.c
        self.tom_x = (self.tom_x + signed(self.tom_vx)) & 0xFFFFFF
        if self.tom_x >> 8 < c["TOM_MIN_X"]:
            self.tom_x, self.tom_vx = c["TOM_MIN_X"] << 8, 0
        elif self.tom_x >> 8 > c["TOM_MAX_X"]:
            self.tom_x, self.tom_vx = c["TOM_MAX_X"] << 8, 0

    def tom_fall(self, line):
        """vy + gravity, y + vy; falling onto `line` or past it:
        there, still (True)."""
        self.tom_vy = (self.tom_vy + self.k["TOM_GRAVITY"]) & 0xFFFF
        self.tom_y = (self.tom_y + self.tom_vy) & 0xFFFF
        if self.tom_vy & 0x8000 or self.tom_y >> 8 < line:
            return False
        self.tom_y = line << 8
        self.tom_vx = self.tom_vy = 0
        return True

    def tom_leap(self):
        k = self.k
        self.tom_across()
        if self.tom_fall(self.c["START_Y"]):
            self.sfx("tom_land")
            self.tom_to(k["TS_LAND"], k["LAND_FRAMES"], k["T_STAND"])
            self.events.append((self.frame, "tom lands"))

    def tom_land(self):
        self.tom_timer -= 1
        if not self.tom_timer:
            self.growl()

    def charge(self):
        k = self.k
        self.tom_vx = 0
        self.tom_to(k["TS_CHARGE"], 0, k["T_RUN_A"])
        self.events.append((self.frame, "tom charges"))

    def stride(self):
        self.tom_timer = (self.tom_timer + 1) & 255
        self.tom_pic = self.k["T_RUN_A"] + ((self.tom_timer >> 2) & 1)

    def tom_run_on(self, target_left, target_right):
        """Running at tom_vx the way he faces, to target_right (facing
        right) or target_left: there or past it, there, still (True)."""
        if self.tom_face == RIGHT:
            self.tom_x = (self.tom_x + self.tom_vx) & 0xFFFFFF
            if self.tom_x >> 8 >= target_right:
                self.tom_x, self.tom_vx = target_right << 8, 0
                return True
        else:
            self.tom_x = (self.tom_x - self.tom_vx) & 0xFFFFFF
            if self.tom_x >> 8 <= target_left:
                self.tom_x, self.tom_vx = target_left << 8, 0
                return True
        return False

    def tom_charge(self):
        k, c = self.k, self.c
        self.stride()
        self.tom_vx = (self.tom_vx + k["CHARGE_ACCEL"]) & 0xFFFF
        most = k["CHARGE_FAST"] if self.tom_fast() else k["CHARGE_MAX"]
        if self.tom_vx >> 8 >= most >> 8:
            self.tom_vx = most
        if self.tom_run_on(c["TOM_MIN_X"], c["TOM_MAX_X"]):
            self.tom_to(k["TS_DAZED"], k["DAZED_FAST"] if self.tom_fast()
                        else k["DAZED_FRAMES"], k["T_DAZED"])
            self.events.append((self.frame, "tom dazed"))

    def tom_dazed(self):
        self.tom_timer -= 1
        if not self.tom_timer:
            self.growl()

    def tom_yelp(self):
        k, c = self.k, self.c
        self.tom_timer -= 1
        if self.tom_timer:
            return
        self.tom_vx = k["FLEE_SPEED"]
        self.tom_face = RIGHT if self.tom_x >> 8 < c["THRONE_X"] else LEFT
        self.tom_to(k["TS_RUN"], 0, k["T_RUN_A"])

    def tom_run(self):
        k, c = self.k, self.c
        self.stride()
        throne = c["THRONE_X"]
        if self.tom_run_on(throne, throne):
            self.tom_vy = -k["HOP_VY"] & 0xFFFF
            self.tom_to(k["TS_HOP"], 0, k["T_RUN_B"])

    def tom_hop(self):
        k = self.k
        if self.tom_fall(self.c["DAIS_TOP"]):
            self.tom_to(k["TS_PAUSE"], k["PAUSE_FRAMES"], k["T_STAND"])

    def tom_pause(self):
        k = self.k
        self.tom_timer -= 1
        if not self.tom_timer:
            self.tom_to(k["TS_UP"], 0, k["T_GROWL"])
            self.events.append((self.frame, "tom flees"))

    def tom_up(self):
        k = self.k
        line = (self.tom_y >> 8) - k["UP_SPEED"]
        self.tom_y = (line & 255) << 8 | (self.tom_y & 255)
        if line < 0:
            self.tom_to(k["TS_GONE"], k["GONE_FRAMES"], k["T_STAND"])
            self.events.append((self.frame, "tom gone"))

    def tom_gone(self):
        self.tom_timer -= 1
        if not self.tom_timer:
            if self.has("states"):
                self.start_won()            # the victory
            else:
                self.start_transition(GO_START)     # steps 10-11

    def tom_box(self):
        """His box: left x, right x, top line, bottom line (bytes)."""
        c = self.c
        tx, ty = self.tom_x >> 8, self.tom_y >> 8
        return (tx + c["TOM_BOX_LEFT"], tx + 47 - c["TOM_BOX_LEFT"],
                (ty - c["TOM_BOX_UP"]) & 255, (ty - 1) & 255)

    def blow_box(self):
        """The box of the blow in the frames that strike (x0, x1, top,
        bottom), or None."""
        k, c = self.k, self.c
        if not (self.form == VAMPIRE and not self.puff and
                c["STRIKE_LAST"] <= self.blow <= c["STRIKE_FIRST"]):
            return None
        feet, ox = self.y >> 8, self.x >> 8
        if self.face == RIGHT:
            x0 = ox + k["BODY_RIGHT"] + 1
            x1 = ox + k["BODY_RIGHT"] + c["STRIKE_REACH"]
        else:
            x0 = max(ox + k["BODY_LEFT"] - c["STRIKE_REACH"], 0)
            x1 = ox + k["BODY_LEFT"] - 1
        return (x0, x1, max(feet - c["STRIKE_UP"], 0),
                (feet - c["STRIKE_DOWN"]) & 255)

    def strike_tom(self):
        """Still (waiting, growling, landed, dazed), not struck since
        his last move: the blow meets his box, a hit; he flashes; no
        hits left, beaten."""
        k = self.k
        still = (k["TS_WAIT"], k["TS_GROWL"], k["TS_LAND"], k["TS_DAZED"])
        if self.tom_safe or self.tom_state not in still:
            return
        blow = self.blow_box()
        if blow is None:
            return
        x0, x1, top, bottom = blow
        left, right, ttop, tbottom = self.tom_box()
        if not (left <= x1 and right >= x0 and ttop <= bottom
                and tbottom >= top):
            return
        self.sfx("tom_hit")
        self.tom_safe = 1
        self.tom_flash = k["FLASH_FRAMES"]
        self.tom_hits -= 1
        self.tom_struck.append((self.frame, self.tom_hits))
        self.events.append((self.frame, "tom struck"))
        if not self.tom_hits:
            self.add_score(5000)
            if self.has("music"):
                self.music_stop()           # his theme stops
            self.tom_to(k["TS_YELP"], k["YELP_FRAMES"], k["T_GROWL"])
            self.events.append((self.frame, "tom beaten"))

    def touch_tom(self):
        """Fighting (not beaten): his box over Oscar's body, as an
        enemy's: a hit, thrown away from Tom's middle."""
        k, c = self.k, self.c
        if self.tom_state >= k["TS_YELP"]:
            return
        d = ((self.x >> 8) - (self.tom_x >> 8)
             + k["BODY_RIGHT"] - c["TOM_BOX_LEFT"])
        if not 0 <= d <= k["TOUCH_SPAN"]:
            return
        feet, ty = self.y >> 8, self.tom_y >> 8
        if ty >= feet:
            if ty - feet >= c["TOM_BOX_UP"]:
                return
        elif feet - ty > self.height - 1:
            return
        self.hit(d < k["MIDDLES"], c["ENEMY_TYPES"])

    def place_tom(self):
        """Sprites 3, 4, 5, 7: Tom, the four blocks of the page shown;
        his colour, white two frames of four when struck; gone, off.
        Then the moon."""
        k, c = self.k, self.c
        self.tom_sprites = []
        if self.tom_state == k["TS_GONE"]:
            self.sprites_on &= 0x47
            self.place_moon()
            return
        self.tom_page()
        self.tom_reg = ((self.tom_x >> 8) - self.camera + 31) & 0xFFFF
        x = self.tom_reg
        self.d010 = (self.d010 & 0x47) | (0x28 if x > 255 else 0)
        if x + 24 > 255:
            self.d010 |= 0x90
        top = ((self.tom_y >> 8) + 8) & 255
        bottom = (top + 21) & 255
        block = k["TOM_BLOCKS"] + self.tom_front * 4
        colour = (c["TOM_FLASH_COLOUR"] if self.tom_flash & 2
                  else c["TOM_COLOUR"])
        self.tom_sprites = [(x, top, block, colour),
                            (x + 24, top, block + 1, colour),
                            (x, bottom, block + 2, colour),
                            (x + 24, bottom, block + 3, colour)]
        self.sprites_on |= 0xB8
        self.tom_seen.add((self.tom_state, self.tom_pic, self.tom_face))
        self.place_moon()

    def tom_page(self):
        """The picture (tom_pic, facing tom_face) into the page not
        shown, which is shown from now on, when it is not the one
        shown."""
        number = self.tom_pic + (self.c["TOM_PICTURES"]
                                 if self.tom_face == LEFT else 0)
        if number == self.tom_shown:
            return
        self.tom_shown = number
        self.tom_front ^= 1
        self.tom_pages[self.tom_front] = number
        self.tom_page_frame = self.frame

    def tom_state_bytes(self):
        """TOM: arena ... tom_flash (16 bytes); then TOM_2: tom_safe,
        tom_next, tom_shown, tom_front, tom_reg (2 bytes)."""
        vx, vy = self.tom_vx & 0xFFFF, self.tom_vy & 0xFFFF
        return ([self.arena, self.tom_state, self.tom_timer & 255,
                 self.tom_x & 255, (self.tom_x >> 8) & 255,
                 self.tom_x >> 16, self.tom_y & 255, self.tom_y >> 8,
                 vx & 255, vx >> 8, vy & 255, vy >> 8,
                 self.tom_face, self.tom_pic, self.tom_hits,
                 self.tom_flash],
                [self.tom_safe, self.tom_next, self.tom_shown,
                 self.tom_front, self.tom_reg & 255,
                 self.tom_reg >> 8])

    def enemy_state(self, places=None):
        """The table at ENEMIES: 14 arrays of MAX_ENEMIES bytes, the
        first `places` of each (see enemies.asm); by default as many
        as the level has."""
        if places is None:
            places = len(self.objects["enemies"])
        x, y = self.en_x[:places], self.en_y[:places]
        vx, vy = self.en_vx[:places], self.en_vy[:places]
        return [[v & 255 for v in x], [(v >> 8) & 255 for v in x],
                [v >> 16 for v in x],
                [v & 255 for v in y], [(v >> 8) & 255 for v in y],
                [v & 255 for v in vx], [(v >> 8) & 255 for v in vx],
                [v & 255 for v in vy], [(v >> 8) & 255 for v in vy],
                self.en_dir[:places], self.en_timer[:places],
                self.en_air[:places], self.en_pic[:places],
                self.en_gone[:places]]

    # --- the screens -------------------------------------------------
    def do_swap(self):
        self.swapped = True
        self.swaps += 1
        self.front ^= 1
        self.shown_d018 = self.d018_values[self.front]
        edge = 38 if self.prep_dir == RIGHT else 0
        for half in (range(0, 11), range(11, 22)):
            self.move(self.colours, self.colours, half)
            self.paint(edge, half)
        self.prep_stage = 0

    def prepare_back(self):
        if self.last_dir != self.prep_dir:
            self.prep_dir = self.last_dir
            self.prep_stage = 0
        if self.prep_dir == RIGHT and self.camera >= self.camera_max - 7:
            return
        if self.prep_dir == LEFT and self.camera < 8:
            return
        front, back = self.screens[self.front], self.screens[1 - self.front]
        if self.prep_stage < 2:
            half = range(0, 11) if self.prep_stage == 0 else range(11, 22)
            self.move(front, back, half)
            self.prep_stage += 1
        elif self.prep_stage == 2:
            if self.prep_dir == RIGHT:
                world, col = (self.camera >> 3) + 39, 38
            else:
                world, col = (self.camera >> 3) - 1, 0
            self.draw_column(world, col, 1 - self.front)
            self.prep_stage = 3

    def move(self, source, target, rows):
        if self.prep_dir == RIGHT:
            order, step = range(0, 38), 1
        else:
            order, step = range(38, 0, -1), -1
        for x in order:
            for row in rows:
                target[(x, row)] = source.get((x + step, row))

    def draw_column(self, world, col, screen):
        width = len(self.level) // 11 * 2
        assert 0 <= world < width, f"level column {world}"
        for row, code in enumerate(reference.level_column(self.files,
                                                          world)):
            self.screens[screen][(col, row)] = code
            self.edge[row] = self.files["charcolour"][code]

    def paint(self, col, rows):
        for row in rows:
            self.colours[(col, row)] = self.edge[row]

    # --- what the C64 holds ---------------------------------------
    def oscar_state(self):
        """Oscar's bytes in the program's order (see oscar.asm)."""
        vx, vy = self.vx & 0xFFFF, self.vy & 0xFFFF
        return self.only(
            [self.x & 255, (self.x >> 8) & 255, self.x >> 16,
             self.y & 255, self.y >> 8,
             vx & 255, vx >> 8, vy & 255, vy >> 8,
             self.ground, self.face, self.anim & 255, self.anim >> 8,
             self.picture, self.prev_joy],
            [None] * 5 + ["oscar"] * 8 + [None, "oscar"])

    def scroll_state(self):
        """camera ... xscroll, then joy ($10-$18, $1b)."""
        return self.only(
            [self.camera & 255, self.camera >> 8, self.front,
             self.prep_dir, self.prep_stage, self.last_dir,
             self.swap, self.shown_d018, self.xscroll, self.joy],
            [None, None, None, "scroll", "scroll", "scroll", "scroll",
             None, None, "scroll"])

    @staticmethod
    def cells(memory):
        return {(col, row): memory[row * 40 + col]
                for row in range(ROWS) for col in range(reference.VISIBLE)}

    def view(self, first):
        view = reference.level_view(self.files, first)
        return ({k: v[0] for k, v in view.items()},
                {k: v[1] for k, v in view.items()})


def level_info(number=1):
    """levelN.json: surfaces by name, solids, objects."""
    return reference.level_info(number)


def surface_names(number=1):
    """{(level x, line): name} of the drawn surfaces of a level; the
    tops of the solid blocks are 'solid block'."""
    info = level_info(number)
    names = {(x, y): item["name"] for item in info["surfaces"]
             for x, y in item["points"]}
    for first, last, top, _ in info["solids"]:
        for x in range(first * 16, (last + 1) * 16):
            names[(x, top * 16)] = "solid block"
    return names
