"""Dreadcastle: build the data of the program from the drawings.

  python game/assets/build_assets.py

Reads the drawings (village.py, forest.py, marsh.py, crags.py,
frost.py, level1.py to level6.py, moth.py, heirloom.py, enemies.py,
staff.py, moon.py, sprites.py, font.py),
checks the rules of the C64 and writes, in game/assets/generated:
  charset.bin     the village's set: 256 characters x 8 bytes, at
                  $4800 in the program: 0 the blank, from 1 the
                  pictures of levels 1 and 2 (one set for the two
                  levels of the village), MOTH_CHAR and the next the
                  moth's two
  charset_forest.bin, charset_marsh.bin, charset_crags.bin,
  charset_pass.bin
                  the wood's set: level 3; the mire's:
                  level 4, its will-o'-the-wisps at FLICKER_CHAR to
                  FLICKER_CHAR + 7; the crags': level 5; the
                  pass's: level 6, its spikes of ice at FLICKER_CHAR;
                  kept out of the VIC-II's bank and unpacked into
                  SET_SLOT ($5800) when a level of their setting
                  starts
  env_village.bin ... env_pass.bin
                  the tables of each setting, ENV_PAGES pages,
                  copied to ENV_TABLES: the colour RAM value of each
                  character; for each metatile its flags (bit 0
                  solid, bit 1 hazard) and its profile (0, none); the
                  four tables of its characters (top left, top right,
                  bottom left, bottom right); the profiles of the
                  surfaces, 16 tables of PROFILE_STRIDE bytes: table i
                  gives, for each profile, the line (0-15) Oscar
                  stands on in pixel column i of the metatile, or $ff
  hudset.bin      the HUD's set: 256 characters, at
                  $5000: the font and the icons, the rest blank
  level1.bin to level6.bin
                  each level as it starts: LEVEL_WIDTH columns of 11
                  metatiles, column after column, with its moths
  level1.lz ..., env_village.lz ..., charset_forest.lz ...
                  the same, packed (pack.py): the maps
                  followed by zeros up to MAP_PAGES pages; the
                  settings' tables; the sets of characters out of the
                  VIC-II's bank. In the program they are unpacked a
                  page at a time where they are used (unpack.asm)
  packed.asm      the packed data in the program, with where
                  each map, each setting's tables and set are
  plain.asm       for steps 01-07 of the book's chain only: the data
                  of the levels of the village and the wood as they
                  are, not packed, with the same labels
  objects.asm     for each level: where its map is, its heirlooms,
                  lantern, doors, enemies and
                  the staff (OBJECT_BYTES bytes, copied to OBJECTS
                  when it starts)
  tables.asm      the setting of each level; for each setting
                  the enemies it shows at most and its moon's bit; the
                  tables of the types of enemy; where the staff is
                  held
  names.bin       the name of each level for the HUD; then the
                  row of Tom's arena: his name, his bar
  moth.bin        the moth's two pictures: 16 bytes each, its two
                  characters (MOTH_CHAR and the next)
  flicker.bin     the pictures of the hazards that flicker, a page
                  for each setting with them (the mire's
                  will-o'-the-wisps; the pass's spikes of ice):
                  four pictures of 64 bytes, the 8 characters of the
                  two kinds (FLICKER_CHAR to FLICKER_CHAR + 7)
  hud.bin         the three HUD rows: 120 characters, 120 colours
  sprites.bin     25 pictures of Oscar, the bat and the smoke (two
                  blocks each: lines, then colours), then one block for
                  each heirloom
  enemies.bin     the enemies' sprites: four blocks a type
                  (enemies.py), at ENEMY_SPRITES
  staff.bin       the staff's sprites, at STAFF_SPRITES
  tom.bin         Tom Darkfang's five pictures facing right, a
                  page each (tom.py), and an empty page: tom.lz,
                  packed, under the KERNAL (data.asm)
  mirror_to.bin   where each byte of a picture of Tom goes
                  mirrored (tom.py), under the KERNAL
  moon.bin        the moon of the wood: sprite 6,
                  one block, at MOON_SPRITE
  music.asm       the theme (score.py), compiled by music.py, with
                  the tables of all the songs
  music_high.asm  Tom's theme (boss.py) and the three
                  jingles (jingles.py), under the KERNAL
  sfx.asm         the sound effects (sfx.py), under the
                  KERNAL
  level1.json to level6.json
                  each level for the tests and levels.py: name,
                  setting, surfaces by name, solid blocks, hazards,
                  pits, water, moths, heirlooms, lantern, gate, start,
                  enemies, the staff
  staff.json      the staff's tables, for the tests
  assets.inc      the numbers above as 64tass constants
  preview.png     the picture at the start, for the eye (the tests
                  compute their own: tests/reference.py)
  level1.png to level6.png
                  the whole levels, for the eye

Each level is drawn twice: as it starts, and with the lantern lit and
the gate open. The metatiles where the two differ (and only those:
checked) give the tiles the program puts in their place.

Rules checked: at most one colour of its own per multicolour cell,
and from 0-7; the characters of the picture fit after the font;
metatile indexes in a byte; surfaces on the pixels of their objects,
one at most in a pixel column of a metatile; solid blocks on the
grid of the metatiles, with no surface drawn inside them; moths on
empty sky; the last line of the playfield black (the HUD's scroll
register is written there).
Text files are written with LF line ends on every system.
"""

import hashlib
import json
from pathlib import Path
import struct
import sys
import zlib

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from canvas import INK, Canvas  # noqa: E402
import crags         # noqa: E402
import font          # noqa: E402
import frost         # noqa: E402
import hall          # noqa: E402
import enemies       # noqa: E402
import heirloom      # noqa: E402
import level1        # noqa: E402
import level2        # noqa: E402
import level3        # noqa: E402
import level4        # noqa: E402
import level5        # noqa: E402
import level6        # noqa: E402
import level7        # noqa: E402
import level8        # noqa: E402
import logo          # noqa: E402
import keep          # noqa: E402
import marsh         # noqa: E402
import moon          # noqa: E402
import moth          # noqa: E402
import music         # noqa: E402
import pack          # noqa: E402
import sfx           # noqa: E402
import sprites       # noqa: E402
import staff         # noqa: E402
import title         # noqa: E402
import tom           # noqa: E402
import village       # noqa: E402

OUT = HERE / "generated"
COLUMNS, ROWS = 40, 22              # the screen's playfield, in cells
LEVEL_ROWS = 11                     # metatile rows
LEVELS = [level1, level2, level3, level4, level5,  # as they are played
          level6, level7, level8]
# The settings: each has its own set of characters and its own
# tables of metatiles, for its levels. Their sets: the village's at
# $4800 (CHARSET); the others out of the VIC-II's bank, each
# put in $5800 (SET_SLOT) when one of its levels starts: the wood's
# (level 3), the mire's (level 4); the crags' (level 5), the
# pass's (level 6); the keep's (level 7, the castle from
# outside), the hall's (level 8, inside).
ENVIRONMENTS = [("village", [level1, level2]), ("forest", [level3]),
                ("marsh", [level4]), ("crags", [level5]),
                ("pass", [level6]), ("keep", [level7]),
                ("hall", [level8])]
# Each setting's second shared colour ($d023, next_env): brown in the
# village, the wood and the mire; in the mountain grey in the
# crags (crags.py), light blue in the pass (frost.py); in the castle
# medium grey outside (keep.py), orange inside, the light of
# the torches (hall.py). The first ($d022): ENV_D022, below.
ENV_D023 = {"village": village.SHARED_2, "forest": village.SHARED_2,
            "marsh": village.SHARED_2, "crags": crags.STONE,
            "pass": frost.ICE, "keep": keep.STONE, "hall": hall.ORANGE}
# The background ($d021) and the first shared
# colour ($d022) of each setting: black and dark grey, but in the
# castle the night is blue, as on the cover of the book (night
# blue): the top interrupt sets the playfield's
# $d021 (play_d021), the HUD's sets black again; inside (hall.py) the
# first shared colour is medium grey, the stone, as outside (keep.py's
# second), the second orange, the light of the torches.
ENV_D021 = {name: village.BACKGROUND for name, _ in ENVIRONMENTS}
ENV_D021.update(keep=keep.SKY, hall=hall.SKY)
ENV_D022 = {name: village.SHARED_1 for name, _ in ENVIRONMENTS}
ENV_D022.update(keep=keep.GREY, hall=hall.STONE)
# The settings whose hazards flicker: their 8 characters, two kinds of
# 4, at FLICKER_CHAR, their picture changed by the program (the
# mire's will-o'-the-wisps; the pass's spikes of ice, a glint
# running over them; the keep's spikes of iron, a glint too, the
# fire on the hearth of the hall). For each: the name of its hazards.
FLICKER = {"marsh": "wisps", "pass": "spikes", "keep": "spikes",
           "hall": "fire"}
FLICKER_CHAR = 246                  # 246-253
FLICKER_FRAMES = 4                  # pictures, in turn
ENV_PAGES = 9                       # an environment's tables, in pages
# Packed (pack.py): each map is unpacked as MAP_PAGES whole pages
# (the level, then zeros), each set of characters as SET_PAGES.
MAP_PAGES = 6
SET_PAGES = 8
PROFILE_STRIDE = 32                 # profiles: room for 32
FIRST_SCENE_CHAR = 1                # 0: the blank
MOTH_CHAR = 254                     # 254-255: the moth
EMPTY_SKY = 0                       # metatile 0: four blank cells
SOLID = 1                           # bits of metaflags: solid,
HAZARD = 2                          # a hazard (brambles)
NO_SURFACE = (0xFF,) * 16

# The HUD: three rows under the playfield, hi-res characters.
WHITE, RED, CYAN, PURPLE, BLUE, YELLOW = 1, 2, 3, 4, 6, 7
HUD_ROWS = [
    # row 22: a purple rule across the screen
    [("rule", PURPLE)] * COLUMNS,
    # row 23: health, flight, heirlooms, the night until dawn
    ([(" ", WHITE)] + [("heart", RED)] + [("bar2", RED)] * 4
     + [(" ", WHITE)] + [("bat", PURPLE)] + [("bar2", PURPLE)] * 3
     + [(" ", WHITE)] + [("chalice", YELLOW)]
     + [(ch, WHITE) for ch in "0/3"] + [(" ", WHITE)] * 2
     + [("moon", WHITE)] + [("bar2", BLUE)] * 8 + [("sun", YELLOW)]
     + [(" ", WHITE)] * 12),
    # row 24: the level and the score (name_row: each level's)
]


def name_row(number, name):
    """Row 24 of the HUD: the number and the name of the level, the
    score."""
    return ([(" ", WHITE), (str(number), YELLOW), (" ", WHITE)]
            + [(ch, CYAN) for ch in name]
            + [(" ", WHITE)] * (40 - 3 - len(name) - 7)
            + [(ch, WHITE) for ch in "000000"]
            + [(" ", WHITE)])


def score_column():
    """The score's first cell in row 24, the same in each
    level's row and in Tom's."""
    rows = [name_row(n + 1, level.NAME) for n, level in
            enumerate(LEVELS)] + [tom_row()]
    columns = {[name for name, _ in row].index("0", 3) for row in rows}
    if len(columns) != 1:
        raise ValueError("the score: one place")
    return columns.pop()


# Row 24 in the arena: Tom's name and his bar (from cell TOM_BAR,
# two hits a character, as Oscar's health), the score.
TOM_NAME = "TOM DARKFANG"
TOM_BAR = 1 + len(TOM_NAME) + 1
TOM_BAR_CELLS = 4


def tom_row():
    """Row 24 of the HUD in Tom's arena."""
    return ([(" ", WHITE)] + [(ch, YELLOW) for ch in TOM_NAME]
            + [(" ", WHITE)] + [("bar2", RED)] * TOM_BAR_CELLS
            + [(" ", WHITE)] * (40 - TOM_BAR - TOM_BAR_CELLS - 7)
            + [(ch, WHITE) for ch in "000000"]
            + [(" ", WHITE)])

# The camera: the level pixel at the left edge of the playfield
# (38 columns: screen pixel 7). A sprite X register is level x -
# camera + 31. Oscar's screen x (his sprite's left edge) at a new
# start: SCREEN_START.
SPRITE_X_OFFSET = 31
SCREEN_START = 120
SPRITE_SHARED_1, SPRITE_SHARED_2 = 2, 15    # $d025, $d026
OSCAR_LINE_COLOUR, OSCAR_COLOUR = 0, 4       # $d027, $d028

# VICE 3.10, internal palette (measured from a VICE capture).
PALETTE = ["000000", "ffffff", "af3c58", "7ef3d6", "aa40f5", "62d532",
           "2c3dec", "ffff46", "b7631e", "775300", "ee7b95", "626262",
           "949494", "b7ff86", "7385ff", "cdcdcd"]


def shared_of(name):
    """A setting's three shared colours: $d021, $d022, $d023."""
    return (ENV_D021[name], ENV_D022[name], ENV_D023[name])


def encode_cell(canvas, col, row, shared=None):
    """The 8 bytes and the colour RAM value of one playfield cell, with
    the shared colours of its setting (the village's if not given)."""
    if (col, row) in canvas.hires:
        data, colour = canvas.hires[(col, row)]
        return bytes(data), colour              # bit 3 clear: hi-res
    d021, d022, d023 = shared or shared_of("village")
    pixels = [canvas.pixels[row * 8 + y][col * 4 + x]
              for y in range(8) for x in range(4)]
    own = set(pixels) - {d021, d022, d023}
    if len(own) > 1 or any(colour > 7 and colour != INK
                           for colour in own):
        raise ValueError(f"cell {col},{row}: colours {sorted(own)}")
    own_colour = own.pop() if own else 0
    if own_colour == INK:                       # black, bits 11
        own_colour = 0
    bits = {d021: 0b00, d022: 0b01, d023: 0b10}
    data = bytearray()
    for y in range(8):
        value = 0
        for x in range(4):
            pixel = pixels[y * 4 + x]
            value = (value << 2) | bits.get(pixel, 0b11)
        data.append(value)
    if not any(data):
        return bytes(8), 8                       # the empty cell
    return bytes(data), 8 | own_colour          # bit 3 set: multicolour


def draw_level(level, lit=False, open_door=False):
    canvas = Canvas(village.OPEN_SKY, width=level.WIDTH)
    surfaces = level.draw(canvas, lit, open_door)
    if any(canvas.pixels[ROWS * 8 - 1][x] not in (village.BACKGROUND,
                                                  INK)
           for x in range(canvas.width)) or any(
               row == ROWS - 1 for _, row in canvas.hires):
        raise ValueError("the last line of the playfield is not black")
    return canvas, surfaces


class Characters:
    """A setting's character set: the blank, then the pictures'
    characters as they are met, the first level first, up to `limit`
    (the moth's, or the flickering hazards')."""

    def __init__(self, limit=MOTH_CHAR, shared=None):
        self.shared = shared
        self.charset = bytearray(256 * 8)
        self.colours = bytearray(256)
        self.colours[0] = 8                     # the blank: multicolour
        self.codes = {}                         # (bytes, colour) -> code
        self.limit = limit

    def code(self, data, colour):
        if not any(data):
            return 0                            # the blank glyph
        key = (data, colour)
        if key not in self.codes:
            code = FIRST_SCENE_CHAR + len(self.codes)
            if code >= self.limit:
                raise ValueError("the picture reaches the moth's "
                                 "(or the hazards') characters")
            self.codes[key] = code
            self.charset[code * 8:code * 8 + 8] = data
            self.colours[code] = colour
        return self.codes[key]

    def cells(self, canvas, columns=None):
        """{(col, row): code} of the canvas (or of some cell columns)."""
        found = {}
        for col in columns if columns is not None else \
                range(canvas.width // 4):
            for row in range(ROWS):
                found[(col, row)] = self.code(*encode_cell(
                    canvas, col, row, self.shared))
        return found


def hud_set():
    """The HUD's character set: the font and the icons from code 0,
    the rest blank (row 21 of the playfield is read through it in
    the last line before the HUD: blank, so black)."""
    charset = bytearray(256 * 8)
    for index, name in enumerate(font.GLYPH_ORDER):
        charset[index * 8:index * 8 + 8] = font.glyph_bytes(name)
    return bytes(charset)


def surface_shapes(level, canvas, surfaces):
    """{(metatile column, metatile row): 16 lines}: for each pixel
    column of the metatile, the line (0-15) of the surface in it, or
    $ff; from the surfaces of the drawing and the tops of the solid
    blocks."""
    shapes = {}

    def put(name, x, y):
        key = (x // 16, y // 16)
        shape = list(shapes.get(key, NO_SURFACE))
        if shape[x % 16] != 0xFF:
            raise ValueError(f"{name}: two surfaces at ({x}, {y})")
        shape[x % 16] = y % 16
        shapes[key] = tuple(shape)

    for name, line, allowed in surfaces:
        for x, y in line.items():
            if canvas.pixels[y][x // 2] not in allowed:
                raise ValueError(f"{name}: ({x}, {y}) is not on it")
            if solid_at(level, x // 16, y // 16):
                raise ValueError(f"{name}: ({x}, {y}) in a solid block")
            put(name, x, y)
    for first, last, top, bottom in level.SOLIDS:
        for x in range(first * 16, (last + 1) * 16):
            put("solid block", x, top * 16)
    return shapes


def solid_at(level, col, row):
    return any(first <= col <= last and top <= row <= bottom
               for first, last, top, bottom in level.SOLIDS)


def hazard_at(level, col, row):
    return any(first <= col <= last and row == at
               for first, last, at in getattr(level, "HAZARDS", ()))


def environment_of(level):
    return getattr(level, "ENVIRONMENT", "village")


def build():
    """The levels, setting by setting: each setting has one set of
    characters and one table of metatiles for its levels (the village:
    levels 1 and 2, level 1 first, its characters in their first order;
    the forest: level 3)."""
    numbers = {level: n for n, level in enumerate(LEVELS, 1)}
    envs = []
    for env_number, (name, env_levels) in enumerate(ENVIRONMENTS):
        flicker = name in FLICKER
        chars = Characters(FLICKER_CHAR if flicker else MOTH_CHAR,
                           shared_of(name))
        keys = [((0, 0, 0, 0), NO_SURFACE, 0)]  # metatile 0: empty sky
        # The moth: the last two characters, a metatile of its own.
        chars.charset[MOTH_CHAR * 8:MOTH_CHAR * 8 + 16] = \
            moth.characters(0)
        chars.colours[MOTH_CHAR:MOTH_CHAR + 2] = bytes(
            [8 | moth.OWN_COLOUR] * 2)
        keys.append(((MOTH_CHAR, MOTH_CHAR + 1, 0, 0), NO_SURFACE, 0))
        moth_tile = 1
        flicker_tiles = None
        if flicker:                 # their first picture, two metatiles
            kinds, _, _, colour = flicker_source(name)
            chars.charset[FLICKER_CHAR * 8:FLICKER_CHAR * 8 + 64] = \
                flicker_frames(name)[:64]
            chars.colours[FLICKER_CHAR:FLICKER_CHAR + 8] = bytes(
                [8 | colour] * 8)
            flicker_tiles = []
            for kind in range(len(kinds)):
                first = FLICKER_CHAR + 4 * kind
                flicker_tiles.append(len(keys))
                keys.append((tuple(range(first, first + 4)), NO_SURFACE,
                             HAZARD))
        built = []
        for level in env_levels:
            if environment_of(level) != name:
                raise ValueError(f"{level.NAME}: not of {name}")
            entry = build_level(numbers[level], level, chars, keys,
                                moth_tile, flicker_tiles)
            entry["env"] = env_number
            built.append(entry)
        if len(keys) > 256:
            raise ValueError(f"{name}: more than 256 metatiles")
        profiles = [NO_SURFACE] + sorted({shape for _, shape, _ in keys
                                          if shape != NO_SURFACE})
        if len(profiles) > PROFILE_STRIDE:
            raise ValueError(f"{name}: more than {PROFILE_STRIDE} "
                             "profiles")
        envs.append({
            "name": name, "charset": bytes(chars.charset),
            "d021": ENV_D021[name], "d022": ENV_D022[name],
            "d023": ENV_D023[name],
            "colours": bytes(chars.colours),
            "metatiles": [quad for quad, _, _ in keys],
            "metashape": bytes(profiles.index(shape)
                               for _, shape, _ in keys),
            "metaflags": bytes(flags for _, _, flags in keys),
            "profiles": profiles,
            "levels": built, "scene_chars": len(chars.codes),
            "limit": chars.limit, "moth_tile": moth_tile,
            "flicker_tiles": flicker_tiles})
    levels = sorted((e for env in envs for e in env["levels"]),
                    key=lambda e: e["number"])
    if [e["module"] for e in levels] != LEVELS:
        raise ValueError("every level in one setting")
    if len({lv.START_X for lv in LEVELS}) != 1 or \
            len({lv.COLUMNS for lv in LEVELS}) != 1:
        raise ValueError("the levels start alike, and are as wide")
    hud_chars, hud_colours = bytearray(), bytearray()
    for line in HUD_ROWS + [name_row(1, level1.NAME)]:
        if len(line) != COLUMNS:
            raise ValueError(f"HUD row of {len(line)} cells")
        for name, colour in line:
            hud_chars.append(font.code(name))
            hud_colours.append(colour)
    names = bytearray()
    for number, level in enumerate(LEVELS, 1):
        row = name_row(number, level.NAME)
        if len(row) != COLUMNS:
            raise ValueError(f"name of level {number}: {len(row)} cells")
        names += bytes(font.code(name) for name, _ in row)
        names += bytes(colour for _, colour in row)
    row = tom_row()
    if len(row) != COLUMNS:
        raise ValueError(f"Tom's row: {len(row)} cells")
    names += bytes(font.code(name) for name, _ in row)
    names += bytes(colour for _, colour in row)
    return {
        "envs": envs, "hudset": hud_set(),
        "levels": levels,
        "hud": bytes(hud_chars + hud_colours), "names": bytes(names),
        "sprites": sprites.sprite_blocks(),
        "heirlooms": b"".join(heirloom.block(kind)
                              for kind in heirloom.KINDS),
        "enemies": enemies.blocks(), "staff": staff.blocks(),
        "tom": tom.pages() + bytes(256),
        "moon": moon.block(),
        "moth_char": MOTH_CHAR, "moth_tile": 1,
        "moth": moth.frames(),
        "flicker": b"".join(flicker_frames(name) for name, _
                            in ENVIRONMENTS if name in FLICKER),
    }


def flicker_source(name):
    """A setting's hazards that flicker: their kinds, their pictures
    (kind, picture) -> rows, the palette of the rows, their colour of
    their own. The mire's wisps (marsh.py), the pass's spikes
    (frost.py)."""
    if name == "marsh":
        return (marsh.WISP_KINDS, lambda kind, n: marsh.WISPS[kind][n],
                marsh.PALETTE, marsh.CYAN)
    if name == "pass":
        return (frost.SPIKE_KINDS, frost.spike_rows, frost.PALETTE,
                frost.WHITE)
    if name == "keep":
        return (keep.SPIKE_KINDS, keep.spike_rows, keep.PALETTE,
                keep.SPIKE_COLOUR)
    if name == "hall":
        return (hall.FIRE_KINDS, hall.fire_rows, hall.PALETTE,
                hall.YELLOW)
    raise ValueError(f"{name}: no hazards that flicker")


def flicker_frames(name):
    """A setting's flickering hazards' pictures, a page: for each of
    FLICKER_FRAMES, the 8 characters of the two kinds, 4 each (top
    left, top right, bottom left, bottom right): 64 bytes a picture.
    Kind B is two pictures behind kind A, so the two do not change
    together."""
    kinds, picture, palette, own_colour = flicker_source(name)
    if len(kinds) != 2 or {marsh.WISP_FRAMES, frost.SPIKE_FRAMES,
                           keep.SPIKE_FRAMES, hall.FIRE_FRAMES} != {
            FLICKER_FRAMES}:
        raise ValueError("two kinds, FLICKER_FRAMES pictures")
    out = bytearray()
    for frame in range(FLICKER_FRAMES):
        for number, kind in enumerate(kinds):
            rows = picture(kind, (frame + 2 * number) % FLICKER_FRAMES)
            canvas = Canvas(ENV_D021[name], width=8, height=16)
            canvas.blit(0, 0, rows, palette)
            for dy, dx in ((0, 0), (0, 1), (1, 0), (1, 1)):
                data, colour = encode_cell(canvas, dx, dy,
                                           shared_of(name))
                if colour not in (8, 8 | own_colour):
                    raise ValueError(f"{name} {kind}: colour {colour}")
                out += data
    return bytes(out)


def env_block(env):
    """The tables of a setting, as the program copies them to
    ENV_TABLES (ENV_PAGES pages): the colour RAM value of each
    character; for each metatile its flags, its profile and its four
    characters (256 each); the profiles, 16 tables of PROFILE_STRIDE
    bytes."""
    out = bytearray(ENV_PAGES * 256)
    count = len(env["metatiles"])
    out[0:256] = env["colours"]
    out[256:256 + count] = env["metaflags"]
    out[512:512 + count] = env["metashape"]
    for i in range(4):
        out[768 + 256 * i:768 + 256 * i + count] = bytes(
            quad[i] for quad in env["metatiles"])
    for column in range(16):
        for index, profile in enumerate(env["profiles"]):
            out[0x700 + column * PROFILE_STRIDE + index] = profile[column]
    return bytes(out)


def build_level(number, level, chars, keys, moth_tile,
                flicker_tiles=None):
    """One level: its map, its characters and metatiles added to the
    shared ones, its lantern's and doors' tiles; in a setting whose
    hazards flicker (flicker_tiles: their two metatiles) its hazards
    are those, the two kinds in turn, on metatiles left blank in the
    picture."""
    canvas, surfaces = draw_level(level)
    other, _ = draw_level(level, lit=True, open_door=True)
    first_new = len(chars.codes)
    cells = chars.cells(canvas)
    shapes = surface_shapes(level, canvas, surfaces)
    special = {}
    for first, last, row in (getattr(level, "HAZARDS", ())
                             if flicker_tiles else ()):
        for mcol in range(first, last + 1):
            if any(cells[(mcol * 2 + dx, row * 2 + dy)]
                   for dx in (0, 1) for dy in (0, 1)):
                raise ValueError(f"level {number}: hazard at {mcol},"
                                 f"{row}: not on blank cells")
            special[(mcol, row)] = flicker_tiles[mcol % 2]

    def tile(quad, mcol, mrow):
        if (mcol, mrow) in special:
            return special[(mcol, mrow)]
        key = (quad, shapes.get((mcol, mrow), NO_SURFACE),
               (SOLID if solid_at(level, mcol, mrow) else 0)
               | (HAZARD if hazard_at(level, mcol, mrow) else 0))
        if key not in keys:
            keys.append(key)
        return keys.index(key)

    def quad_of(found, mcol, mrow):
        return tuple(found[(mcol * 2 + dx, mrow * 2 + dy)]
                     for dy in (0, 1) for dx in (0, 1))

    tiles_before = len(keys)
    columns = [[tile(quad_of(cells, mcol, mrow), mcol, mrow)
                for mrow in range(LEVEL_ROWS)]
               for mcol in range(level.COLUMNS)]
    # The other picture: only the lantern's head and the doors.
    changes = {}
    other_cells = chars.cells(other)
    for mcol in range(level.COLUMNS):
        for mrow in range(LEVEL_ROWS):
            if quad_of(other_cells, mcol, mrow) != quad_of(cells, mcol,
                                                           mrow):
                changes[(mcol, mrow)] = tile(
                    quad_of(other_cells, mcol, mrow), mcol, mrow)
    lantern = level.LANTERN
    first, last, top, bottom = level.DOOR
    doors = [(c, r) for c in range(first, last + 1)
             for r in range(top, bottom + 1)]
    if set(changes) != {lantern} | set(doors):
        raise ValueError(f"level {number}, lit and open: changes at "
                         f"{sorted(changes)}")
    for col, row in level.MOTHS:
        if columns[col][row] != EMPTY_SKY:
            raise ValueError(f"level {number}: moth at {col},{row}: not "
                             "on empty sky")
        columns[col][row] = moth_tile
    return {
        "module": level, "number": number, "canvas": canvas,
        "surfaces": surfaces, "level": columns,
        "lantern_lit": changes[lantern],
        "doors": [(c, r, changes[(c, r)]) for c, r in doors],
        "new_chars": len(chars.codes) - first_new,
        "new_tiles": len(keys) - tiles_before,
    }


def camera_for(x, width):
    """The camera that shows Oscar (sprite's left edge at level x)
    at SCREEN_START on the screen, within the level."""
    camera_max = width * 16 - 305
    return max(0, min(x + 7 - SCREEN_START, camera_max))


# What a level's block of objects holds, in this order (bytes).
OBJECT_FIELDS = [("heirloom_x_lo", 3), ("heirloom_x_hi", 3),
                 ("heirloom_top", 3), ("heirloom_block", 3),
                 ("door_col", 6), ("door_row", 6), ("door_tile", 6),
                 ("lantern_col", 1), ("lantern_line", 1),
                 ("lantern_row", 1), ("lantern_x", 2),
                 ("lantern_tile", 1), ("door_first", 1),
                 ("door_last", 1), ("door_line", 1),
                 # the enemies: how many, and MAX_ENEMIES of
                 # each field: kind, the ends of its stretch (x of
                 # its sprite), where it starts, facing
                 ("enemy_count", 1), ("en_kind", 8),
                 ("en_min_lo", 8), ("en_min_hi", 8),
                 ("en_max_lo", 8), ("en_max_hi", 8),
                 ("en_start_lo", 8), ("en_start_hi", 8),
                 ("en_start_y", 8), ("en_start_dir", 8),
                 # the Count's staff, lying in the level: x of
                 # its sprite, the line under it (0: none here)
                 ("staff_x_lo", 1), ("staff_x_hi", 1),
                 ("staff_line", 1)]
OBJECT_BYTES = sum(size for _, size in OBJECT_FIELDS)
MAX_ENEMIES = 8


def enemy_list(entry):
    """A level's enemies (the module's ENEMIES): for each, its kind,
    stretch and start; x of the left edge of its sprite: from x_min to
    x_max its box stays in the columns of its stretch; it starts in
    the middle of its start column, on the line of the surface named
    (or, the flyer, on the line given)."""
    level = entry["module"]
    surfaces = {name: line for name, line, _ in entry["surfaces"]}
    found = []
    setting = getattr(level, "ENEMY_SETTING", environment_of(level))
    for kind, first, last, start, where, facing in level.ENEMIES:
        type_ = enemies.type_index(setting, kind)
        name = enemies.TYPES[type_][0]
        left, right, _, _ = enemies.BOXES[name]
        x_min = first * 16 - left
        x_max = (last + 1) * 16 - 1 - right
        x = start * 16 + 8 - 12
        if isinstance(where, str):
            line = surfaces[where].get(x + 12)
            if line is None:
                raise ValueError(f"{kind} at {start}: not on {where}")
        else:
            line = where
        if not (x_min <= x <= x_max and first <= start <= last
                and facing in ("right", "left")):
            raise ValueError(f"{kind} at {start}: outside its stretch")
        found.append({"kind": kind, "type": type_, "name": name,
                      "first": first, "last": last,
                      "start": start, "x_min": x_min, "x_max": x_max,
                      "x": x, "line": line, "on": where
                      if isinstance(where, str) else None,
                      "facing": facing})
    if len(found) > MAX_ENEMIES:
        raise ValueError(f"more than {MAX_ENEMIES} enemies")
    return found


def object_bytes(entry):
    """A level's block of objects (OBJECT_FIELDS)."""
    level = entry["module"]
    kinds = list(heirloom.KINDS)
    xs = [col * 16 - 4 for col, _, _ in level.HEIRLOOMS]
    col, row = level.LANTERN
    first, last, top, _ = level.DOOR
    lantern_x = col * 16 + 8 - 12
    data = ([x & 255 for x in xs] + [x >> 8 for x in xs]
            + [top_ for _, top_, _ in level.HEIRLOOMS]
            + [kinds.index(kind) for _, _, kind in level.HEIRLOOMS]
            + [door[0] for door in entry["doors"]]
            + [door[1] for door in entry["doors"]]
            + [door[2] for door in entry["doors"]]
            + [col, row * 16, row, lantern_x & 255, lantern_x >> 8,
               entry["lantern_lit"], first, last, top * 16 + 1])
    found = enemy_list(entry)

    def field(values):
        values = list(values)
        return values + [0] * (MAX_ENEMIES - len(values))

    data += [len(found)]
    data += field(e["type"] for e in found)
    for key in ("x_min", "x_max", "x"):
        data += field(e[key] & 255 for e in found)
        data += field(e[key] >> 8 for e in found)
    data += field(e["line"] for e in found)
    data += field(("right", "left").index(e["facing"]) for e in found)
    data += list(staff_place(level))
    if len(data) != OBJECT_BYTES:
        raise ValueError("a block of objects of the wrong size")
    return data


def type_constants():
    """For each type of enemy (enemies.TYPES): its behaviour, its box
    (left pixel, top and bottom over its feet), its colour."""
    found = {}
    for index, ((name, _, kind), (left, up, down)) in enumerate(
            zip(enemies.TYPES, enemies.boxes())):
        found[f"TYPE{index}_KIND"] = enemies.KINDS.index(kind)
        found[f"TYPE{index}_LEFT"] = left
        found[f"TYPE{index}_UP"] = up
        found[f"TYPE{index}_DOWN"] = down
        found[f"TYPE{index}_COLOUR"] = enemies.OWN_COLOURS[name]
    return found


ENEMY_TYPES_1 = 6                   # the types at ENEMY_SPRITES


def type_block(index):
    """Where the four blocks of type `index` start (a 64tass
    expression)."""
    if index < ENEMY_TYPES_1:
        return f"ENEMY_BLOCKS + {4 * index}"
    return f"ENEMY_BLOCKS_2 + {4 * (index - ENEMY_TYPES_1)}"


def staff_place(level):
    """Where the staff lies in a level: (x lo, x hi, line under it);
    (0, 0, 0) where it is not. Its sprite's left edge 4 pixels into
    its column."""
    col = getattr(level, "STAFF", None)
    if col is None:
        return (0, 0, 0)
    x = col * 16 - 4
    return (x & 255, x >> 8, level.START_Y)


def flicker_pages():
    """For each setting, 64tass: the page of its flickering hazards'
    pictures (flicker_pictures, a page each in the order of the
    settings), or 0."""
    found, page = [], 0
    for name, _ in ENVIRONMENTS:
        if name in FLICKER:
            found.append(f">flicker_pictures + {256 * page}")
            page += 1
        else:
            found.append("0")
    return found


HEADER = "; Written by game/assets/build_assets.py: do not edit."


def tables_asm(data):
    """The tables of the settings and of the types: tables.asm, the
    setting of each level and each setting's sprites and colours;
    env_flicker.asm, the pages of the hazards that flicker;
    types.asm, the types of enemy (their behaviour, box, colour,
    pictures); staff_tables.asm, where the staff is drawn. Four files,
    one after the other in the program (data.asm), for the steps of
    the book's chain."""
    settings = [name for name, _ in ENVIRONMENTS]
    tables = [HEADER,
              "; The setting of each level: its set of characters and",
              "; its tables (0: the village, 1: the forest, 2: the",
              "; mire, 3: the crags, 4: the pass, 5: the keep, 6: the",
              "; hall).",
              "level_env:",
              "        .byte " + ", ".join(
                  str(e["env"]) for e in data["levels"]),
              "; For each setting: the enemies it shows at most (in",
              "; the wood three: sprite 6 is the moon); its moon's",
              "; bit in $d015 (moon.py), or 0.",
              "env_slots:",
              "        .byte " + ", ".join(
                  "3" if mask else "4"
                  for mask in moon.settings_mask(settings)),
              "env_moon:",
              "        .byte " + ", ".join(
                  f"%{mask:08b}" for mask in moon.settings_mask(settings)),
              "; Its moon behind the characters: its bit of $d01b; its",
              "; second shared colour, $d023.",
              "env_behind:",
              "        .byte " + ", ".join(
                  f"%{mask:08b}" for mask in moon.behind_mask(settings)),
              "env_d023:",
              "        .byte " + ", ".join(
                  str(ENV_D023[name]) for name in settings),
              "; Its background, $d021 of the playfield (the top",
              "; interrupt's), and its first shared colour.",
              "env_d021:",
              "        .byte " + ", ".join(
                  str(ENV_D021[name]) for name in settings),
              "env_d022:",
              "        .byte " + ", ".join(
                  str(ENV_D022[name]) for name in settings)]
    flicker = [HEADER,
               "; For each setting whose hazards flicker: the page of",
               "; their pictures (flicker.bin); else 0.",
               "env_flicker:",
               "        .byte " + ", ".join(flicker_pages())]
    count = range(len(enemies.TYPES))
    types = [HEADER,
             "; The types of enemy (enemies.py: TYPES): behaviour;",
             "; box: BODY_RIGHT less its left pixel, its top and",
             "; bottom over its feet; colour.",
             "type_kind:",
             "        .byte " + ", ".join(f"TYPE{i}_KIND" for i in count),
             "type_reach:",
             "        .byte " + ", ".join(
                 f"BODY_RIGHT - TYPE{i}_LEFT" for i in count),
             "type_left:",
             "        .byte " + ", ".join(f"TYPE{i}_LEFT" for i in count),
             "type_up:",
             "        .byte " + ", ".join(f"TYPE{i}_UP" for i in count),
             "type_down:",
             "        .byte " + ", ".join(f"TYPE{i}_DOWN" for i in count),
             "type_colour:",
             "        .byte " + ", ".join(
                 f"TYPE{i}_COLOUR" for i in count),
             "; Its first block: the village's and the wood's at",
             "; ENEMY_SPRITES, the others' at ENEMY_SPRITES_2; four",
             "; each, on a multiple of 4.",
             "type_block:",
             "        .byte " + ", ".join(type_block(i) for i in count)]
    held, blow = staff.held_table(), staff.blow_table()
    staff_lines = [HEADER,
                   "; The staff in his hand, for each of Oscar's 12",
                   "; pictures: X, Y from his sprite's, its block.",
                   "held_dx:",
                   "        .byte " + ", ".join(
                       str(dx & 255) for dx, _, _ in held),
                   "held_dy:",
                   "        .byte " + ", ".join(
                       str(dy) for _, dy, _ in held),
                   "held_block:",
                   "        .byte " + ", ".join(
                       f"STAFF_BLOCKS + {pic}" for _, _, pic in held),
                   "; The blow, by its frames left (1-10), facing right,",
                   "; then left.",
                   "blow_dx:",
                   "        .byte " + ", ".join(
                       str(dx & 255) for dx, _, _ in blow),
                   "blow_dy:",
                   "        .byte " + ", ".join(
                       str(dy) for _, dy, _ in blow),
                   "blow_block:",
                   "        .byte " + ", ".join(
                       f"STAFF_BLOCKS + {pic}" for _, _, pic in blow)]
    return {name: "\n".join(lines) + "\n" for name, lines in (
        ("tables.asm", tables), ("env_flicker.asm", flicker),
        ("types.asm", types), ("staff_tables.asm", staff_lines))}


def objects_asm(data):
    """Where each level's map is (level_maps.asm); its block of
    objects (objects.asm: the heirloom blocks as HEIRLOOM_BLOCKS +
    kind); where its name is (level_names.asm). Three files, one after
    the other in the program (data.asm), for the steps of the book's
    chain."""
    numbers = range(1, len(LEVELS) + 1)
    maps = [HEADER,
            "; The maps of the levels, as they start.",
            "level_maps_lo:",
            "        .byte " + ", ".join(f"<level_map_{n}" for n in numbers),
            "level_maps_hi:",
            "        .byte " + ", ".join(f">level_map_{n}" for n in numbers)]
    objects = [HEADER,
               "; Each level's objects: copied to OBJECTS when it",
               "; starts (see the fields in assets.inc).",
               "level_objects_lo:",
               "        .byte " + ", ".join(
                   f"<objects_{n}" for n in numbers),
               "level_objects_hi:",
               "        .byte " + ", ".join(
                   f">objects_{n}" for n in numbers)]
    heirloom_at = sum(size for name, size in OBJECT_FIELDS
                      if name in ("heirloom_x_lo", "heirloom_x_hi",
                                  "heirloom_top"))
    for entry in data["levels"]:
        block = object_bytes(entry)
        objects.append(f"objects_{entry['number']}:")
        for start in range(0, OBJECT_BYTES, 9):
            part = []
            for index in range(start, min(start + 9, OBJECT_BYTES)):
                value = str(block[index])
                if heirloom_at <= index < heirloom_at + 3:
                    value = f"HEIRLOOM_BLOCKS + {value}"
                part.append(value)
            objects.append("        .byte " + ", ".join(part))
    rows = range(len(LEVELS) + 1)
    names = [HEADER,
             "; Each level's row 24 of the HUD: 40 characters,",
             "; 40 colours; then Tom's, in the arena.",
             "level_names_lo:",
             "        .byte " + ", ".join(
                 f"<(level_names + {i * 80})" for i in rows),
             "level_names_hi:",
             "        .byte " + ", ".join(
                 f">(level_names + {i * 80})" for i in rows)]
    return {name: "\n".join(lines) + "\n" for name, lines in (
        ("level_maps.asm", maps), ("objects.asm", objects),
        ("level_names.asm", names))}


def paint_cell(data, picture, x0, y0, code, colour, charset="charset"):
    """One character cell into the picture, at pixel (x0, y0); `data`
    a setting (its d023) or the HUD's data."""
    d021, d022, d023 = (data.get("d021", village.BACKGROUND),
                        data.get("d022", village.SHARED_1),
                        data.get("d023", village.SHARED_2))
    if charset == "hudset":                     # the HUD: black
        d021 = village.BACKGROUND
    colour &= 15
    for y in range(8):
        byte = data[charset][code * 8 + y]
        line = picture[y0 + y]
        if colour & 8:
            for x in range(4):
                bits = (byte >> (6 - 2 * x)) & 3
                pixel = (d021, d022, d023, colour & 7)[bits]
                line[x0 + 2 * x] = pixel
                line[x0 + 2 * x + 1] = pixel
        else:
            for x in range(8):
                if byte & (0x80 >> x):
                    line[x0 + x] = colour


def level_picture(data, entry):
    """The whole level (its map), 16 pixels per metatile column, 176
    lines, with the characters of its setting."""
    env = data["envs"][entry["env"]]
    level = entry["level"]
    tables = env["metatiles"]
    width = len(level) * 16
    picture = [[env["d021"]] * width for _ in range(ROWS * 8)]
    for mcol, column in enumerate(level):
        for mrow, tile in enumerate(column):
            for i, (dx, dy) in enumerate(((0, 0), (1, 0), (0, 1),
                                          (1, 1))):
                code = tables[tile][i]
                paint_cell(env, picture, mcol * 16 + dx * 8,
                           mrow * 16 + dy * 8, code,
                           env["colours"][code])
    return picture


def draw_sprites(picture, blocks, x_reg, y_reg):
    """Oscar over the picture: colour layer, then the line layer
    (sprite 0 has priority over sprite 1). Screen pixel = register
    - 24 across, - 50 down."""
    lines, colour_layer = blocks[:64], blocks[64:128]
    x0, y0 = x_reg - 24, y_reg - 50
    shared = (None, SPRITE_SHARED_1, OSCAR_COLOUR, SPRITE_SHARED_2)
    for y in range(21):
        row = int.from_bytes(colour_layer[y * 3:y * 3 + 3], "big")
        for x in range(12):
            bits = (row >> (22 - 2 * x)) & 3
            if bits:
                for dx in (0, 1):
                    _plot(picture, x0 + 2 * x + dx, y0 + y, shared[bits])
        row = int.from_bytes(lines[y * 3:y * 3 + 3], "big")
        for x in range(24):
            if row & (0x800000 >> x):
                _plot(picture, x0 + x, y0 + y, OSCAR_LINE_COLOUR)


def _plot(picture, x, y, colour):
    if 0 <= x < 320 and 0 <= y < 200:
        picture[y][x] = colour


def start_picture(data):
    """The screen at the start: the level from the camera, the HUD,
    Oscar standing; 320 x 200."""
    world = level_picture(data, data["levels"][0])
    camera = camera_for(level1.START_X, level1.COLUMNS)
    picture = [[village.BACKGROUND] * 320 for _ in range(200)]
    for y in range(ROWS * 8):
        for x in range(7, 311):
            picture[y][x] = world[y][camera + x - 7]
    for cell in range(120):
        paint_cell(data, picture, (cell % 40) * 8, 176 + (cell // 40) * 8,
                   data["hud"][cell], data["hud"][120 + cell], "hudset")
    draw_sprites(picture, data["sprites"],
                 level1.START_X - camera + SPRITE_X_OFFSET,
                 level1.START_Y + 29)
    return picture


def capture_of(picture, border=0, left=7, right=9):
    """The 384 x 272 picture VICE exports: the screen at (32, 35);
    in 38-column mode the border covers `left` and `right` pixels."""
    full = [[border] * 384 for _ in range(272)]
    for y in range(200):
        for x in range(left, 320 - right):
            full[35 + y][32 + x] = picture[y][x]
    return full


def save_png(rows, path):
    """A PNG of colour numbers, with the standard library only."""
    height, width = len(rows), len(rows[0])
    raw = bytearray()
    for line in rows:
        raw.append(0)                       # no filter
        for colour in line:
            raw += bytes.fromhex(PALETTE[colour])

    def chunk(kind, body):
        return (struct.pack(">I", len(body)) + kind + body
                + struct.pack(">I", zlib.crc32(kind + body)))
    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    Path(path).write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header)
                           + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
                           + chunk(b"IEND", b""))


def hud_offset(name, after=0):
    """The screen offset (row 23) of a HUD cell: the first `name`,
    plus `after`."""
    row = [cell for cell, _ in HUD_ROWS[1]]
    return 880 + 40 + row.index(name) + after


def level_json(entry):
    """A level for the tests and for levels.py."""
    level = entry["module"]
    return {
        "number": entry["number"], "name": level.NAME,
        "columns": level.COLUMNS,
        "start": [level.START_X, level.START_Y],
        "surfaces": [{"name": name,
                      "points": [[x, y] for x, y in sorted(line.items())]}
                     for name, line, _ in entry["surfaces"]],
        "environment": environment_of(level), "env": entry["env"],
        "solids": level.SOLIDS, "pits": level.PITS,
        "hazards": [list(h) for h in getattr(level, "HAZARDS", ())],
        "staff": list(staff_place(level)),
        "water": level.WATER, "moths": level.MOTHS,
        "heirlooms": [list(h) for h in level.HEIRLOOMS],
        "lantern": list(level.LANTERN), "door": list(level.DOOR),
        "lantern_tile": entry["lantern_lit"],
        "heirloom_kinds": list(heirloom.KINDS),
        "doors": [list(door) for door in entry["doors"]],
        "enemies": enemy_list(entry),
        "enemy_kinds": list(enemies.KINDS),
        "enemy_types": [name for name, _, _ in enemies.TYPES],
    }


def packed_files(data, files):
    """The packed data: {name.lz: bytes}. A map is packed with
    zeros after it, to MAP_PAGES pages; a set of characters out of the
    VIC-II's bank (not the village's) as its SET_PAGES pages."""
    packed = {}
    for entry in data["levels"]:
        name = f"level{entry['number']}"
        level = files[name + ".bin"]
        if len(level) > MAP_PAGES * 256:
            raise ValueError(f"{name}: more than {MAP_PAGES} pages")
        padded = level + bytes(MAP_PAGES * 256 - len(level))
        packed[name + ".lz"] = pack.pack(padded)
    for env in data["envs"]:
        name = env["name"]
        packed[f"env_{name}.lz"] = pack.pack(files[f"env_{name}.bin"])
        if name != "village":
            charset = files[f"charset_{name}.bin"]
            if len(charset) != SET_PAGES * 256:
                raise ValueError(f"{name}: a set of {SET_PAGES} pages")
            packed[f"charset_{name}.lz"] = pack.pack(charset)
    packed["tom.lz"] = pack.pack(files["tom.bin"])
    return packed


# The packed streams kept under the KERNAL: the PRG brings them
# at HIGH_LOAD ($c000, before the level is copied there) and the program
# moves them to HIGH_DATA ($e000) when it starts. Those of PACKED_MID
# come with Tom's pictures in the PRG at SET_SLOT and go under the
# KERNAL too, after the others (once level 4's and level 8's map
# were after the program's code, where Tom's code is now; level 8's is
# with the others again). The others at ENV_DATA ($8000).
PACKED_HIGH = ("charset_keep", "charset_hall", "env_hall")
PACKED_MID = ("level4",)


def packed_asm(data, where="low"):
    """packed.asm: the packed data, where the program keeps
    them (data.asm includes this file at ENV_DATA), and the tables of
    where they are: each level's map; each setting's tables and its
    set of characters (0, none: the village's stays at CHARSET).
    packed_high.asm ("high"): the streams of PACKED_HIGH, which
    data.asm puts at HIGH_DATA; packed_mid.asm ("mid"): those of
    PACKED_MID, at SET_SLOT, then under the KERNAL."""
    lines = ["; Written by game/assets/build_assets.py: do not edit.",
             "; The packed data (pack.py): each level's map, then each",
             "; setting's tables and set of characters" +
             {"low": ".", "high": " (those under the KERNAL).",
              "mid": " (those after Tom's, under the KERNAL)."}[where]]

    def stream(label, file_name):
        name = file_name.rsplit(".", 1)[0]
        place = ("high" if name in PACKED_HIGH else
                 "mid" if name in PACKED_MID else "low")
        if place == where:
            lines.extend([f"{label}:", f'        .binary "{file_name}"'])

    for entry in data["levels"]:
        n = entry["number"]
        stream(f"level_map_{n}", f"level{n}.lz")
    names = [env["name"] for env in data["envs"]]
    for name in names:
        stream(f"env_packed_{name}", f"env_{name}.lz")
        if name != "village":
            stream(f"set_packed_{name}", f"charset_{name}.lz")
    if where != "low":
        return "\n".join(lines) + "\n"
    lines.append("; Where each setting's tables and set are.")
    for table, label in (("env_packed", "env_packed_{}"),
                         ("set_packed", "set_packed_{}")):
        for half, op in (("lo", "<"), ("hi", ">")):
            values = ["0" if table == "set_packed" and name == "village"
                      else op + label.format(name) for name in names]
            lines.append(f"{table}_{half}:")
            lines.append("        .byte " + ", ".join(values))
    return "\n".join(lines) + "\n"


# The book's chain (tools/make_chain.py): steps 01-07 play the levels
# of the first two settings, with the data as they are, not packed.
PLAIN_SETTINGS = ("village", "forest")


def plain_asm(data):
    """plain.asm, for steps 01-07 of the book's chain only (the game
    includes packed.asm): the maps of the levels of PLAIN_SETTINGS
    and those settings' tables and sets, as they are; each map with
    zeros after it to MAP_PAGES pages, as it is unpacked. The same
    labels and tables as packed.asm: 0 for what these steps have
    not got (unpack.asm copies a page at a time in these steps)."""
    names = [env["name"] for env in data["envs"]]
    plain = [n for n in names if n in PLAIN_SETTINGS]
    lines = ["; Written by game/assets/build_assets.py: do not edit.",
             "; For steps 01-07 of the book's chain: the data of the",
             "; first levels as they are, not packed (from step 08",
             "; packed.asm packs them all); each map with zeros",
             "; after it, to MAP_PAGES pages."]
    for entry in data["levels"]:
        n = entry["number"]
        if names[entry["env"]] in plain:
            size = len(entry["level"]) * len(entry["level"][0])
            lines += [f"level_map_{n}:",
                      f'        .binary "level{n}.bin"',
                      f"        .fill {MAP_PAGES * 256 - size}"]
        else:
            lines.append(f"level_map_{n} = 0{' ' * 15}; not yet")
    for name in plain:
        lines += [f"env_packed_{name}:",
                  f'        .binary "env_{name}.bin"']
        if name != "village":
            lines += [f"set_packed_{name}:",
                      f'        .binary "charset_{name}.bin"']
    lines.append("; Where each setting's tables and set are (0: not yet).")
    for table, label in (("env_packed", "env_packed_{}"),
                         ("set_packed", "set_packed_{}")):
        for half, op in (("lo", "<"), ("hi", ">")):
            values = ["0" if name not in plain or (
                table == "set_packed" and name == "village")
                else op + label.format(name) for name in names]
            lines.append(f"{table}_{half}:")
            lines.append("        .byte " + ", ".join(values))
    return "\n".join(lines) + "\n"


def text_record(row, column, colour, words):
    """A text for put_texts (states.asm): its row, its column, its
    colour, how many characters, the characters (the HUD's codes)."""
    codes = [font.code(ch) for ch in words]
    if column + len(codes) > 40 or not 0 <= row <= 24:
        raise ValueError(f"{words!r} out of the screen")
    return [row, column, colour, len(codes)] + codes


def texts_asm():
    """The texts of the title's menu and of the bands
    (title.py), for states.asm: records of put_texts, $ff after the
    last."""
    title.check()

    def lines(label, records):
        out = [f"{label}:"]
        for record in records:
            out.append("        .byte " + ", ".join(map(str, record)))
        out.append("        .byte $ff")
        return out

    text = ["; Written by game/assets/build_assets.py: do not edit.",
            "; The texts of the title and of the bands",
            "; (title.py): a row, a column, a colour, a length,",
            "; the characters (the HUD's codes); $ff: no more."]
    menu = [text_record(title.MENU_ROW + n, title.MENU_COL, title.OTHER,
                        words) for n, words in enumerate(title.CHOICES)]
    menu.append(text_record(*title.PRESS[:2], title.PRESS_ON,
                            title.PRESS[2]))
    text += lines("menu_texts", menu)
    for name in title.BAND_ORDER:
        _, _, texts = title.BANDS[name]
        text += lines(f"texts_{name}", [
            text_record(row, title.centred(words), colour, words)
            for row, colour, words in texts])
    order = title.BAND_ORDER
    text += ["; Each band: its first row, how many rows, its texts.",
             "band_first:",
             "        .byte " + ", ".join(
                 str(title.BANDS[n][0]) for n in order),
             "band_rows:",
             "        .byte " + ", ".join(
                 str(title.BANDS[n][1]) for n in order),
             "band_texts_lo:",
             "        .byte " + ", ".join(f"<texts_{n}" for n in order),
             "band_texts_hi:",
             "        .byte " + ", ".join(f">texts_{n}" for n in order),
             "; Dawn: the playfield's background, step by step.",
             "dawn_colours:",
             "        .byte " + ", ".join(map(str, title.DAWN_COLOURS))]
    return "\n".join(text) + "\n"


def write(data):
    OUT.mkdir(exist_ok=True)
    files = {}
    for env in data["envs"]:
        name = env["name"]
        files["charset.bin" if name == "village" else
              f"charset_{name}.bin"] = env["charset"]
        files[f"env_{name}.bin"] = env_block(env)
    files.update({
        "hudset.bin": data["hudset"],
        "hud.bin": data["hud"],
        "names.bin": data["names"],
        "sprites.bin": data["sprites"] + data["heirlooms"],
        "enemies.bin": data["enemies"],
        "staff.bin": data["staff"],
        "tom.bin": data["tom"],
        "mirror_to.bin": tom.mirror_to(),
        "moon.bin": data["moon"],
        "moth.bin": data["moth"],
        "flicker.bin": data["flicker"],
        "logo.bin": logo.blocks()})
    for entry in data["levels"]:
        files[f"level{entry['number']}.bin"] = bytes(
            tile for column in entry["level"] for tile in column)
    packed = packed_files(data, files)
    for name, content in {**files, **packed}.items():
        (OUT / name).write_bytes(content)
    write_text(OUT / "packed.asm", packed_asm(data))
    write_text(OUT / "packed_high.asm", packed_asm(data, "high"))
    write_text(OUT / "packed_mid.asm", packed_asm(data, "mid"))
    write_text(OUT / "plain.asm", plain_asm(data))     # the chain
    write_text(OUT / "texts.asm", texts_asm())
    constants = {
        "FIRST_SCENE_CHAR": FIRST_SCENE_CHAR,
        "LEVEL_COUNT": len(LEVELS),
        "ENV_COUNT": len(ENVIRONMENTS),
        "ENV_PAGES": ENV_PAGES,
        "PROFILE_STRIDE": PROFILE_STRIDE,
        "D021_SKY": village.BACKGROUND,
        "D022_STONE": village.SHARED_1,
        "D023_WOOD": village.SHARED_2,
        "SPRITE_SHARED_1": SPRITE_SHARED_1,
        "SPRITE_SHARED_2": SPRITE_SHARED_2,
        "OSCAR_LINE_COLOUR": OSCAR_LINE_COLOUR,
        "OSCAR_COLOUR": OSCAR_COLOUR,
        "HEIRLOOM_COLOUR": heirloom.OWN_COLOUR,
        "STAFF_COLOUR": staff.OWN_COLOUR,
        "STAFF_PICTURES": len(data["staff"]) // 64,
        "STAFF_LYING": staff.LYING,
        "BLOW_FRAMES": staff.BLOW_FRAMES,
        "STRIKE_FIRST": staff.STRIKE_FIRST,
        "STRIKE_LAST": staff.STRIKE_LAST,
        "STRIKE_REACH": staff.STRIKE_REACH,
        "STRIKE_UP": staff.STRIKE_UP,
        "STRIKE_DOWN": staff.STRIKE_DOWN,
        "MOON_X": moon.X_REGISTER,
        "MOON_Y": moon.Y_REGISTER,
        "MOON_COLOUR": moon.OWN_COLOUR,
        "MOON_BEHIND": sum(1 << i for i, mask in enumerate(
            moon.behind_mask([name for name, _ in ENVIRONMENTS]))
            if mask),
        **{f"ENV{i}_D023": ENV_D023[name]
           for i, (name, _) in enumerate(ENVIRONMENTS)},
        **{f"ENV{i}_D021": ENV_D021[name]
           for i, (name, _) in enumerate(ENVIRONMENTS)},
        **{f"ENV{i}_D022": ENV_D022[name]
           for i, (name, _) in enumerate(ENVIRONMENTS)},
        "MOON_SETTINGS": sum(1 << i for i, mask in enumerate(
            moon.settings_mask([name for name, _ in ENVIRONMENTS]))
            if mask),
        "MIN_MATCH": pack.MIN_MATCH,
        "MAP_PAGES": MAP_PAGES,
        "SET_PAGES": SET_PAGES,
        "LEVEL_WIDTH": level1.COLUMNS,
        "CAMERA_MAX": level1.COLUMNS * 16 - 305,
        "SCREEN_START": SCREEN_START,
        "START_X": level1.START_X,
        "START_Y": level1.START_Y,
        "EMPTY_SKY": EMPTY_SKY,
        "SOLID": SOLID,
        "HAZARD": HAZARD,
        "MOTH_TILE": data["moth_tile"],
        "MOTH_CHAR": data["moth_char"],
        "FLICKER_CHAR": FLICKER_CHAR,
        "FLICKER_FRAMES": FLICKER_FRAMES,
        "FLICKER_SETTINGS": sum(1 << i for i, (name, _) in enumerate(
            ENVIRONMENTS) if name in FLICKER),
        "FLICKER_PAGES": len(FLICKER),
        "PICTURE_COUNT": len(data["sprites"]) // 128,
        "HEIRLOOM_COUNT": 3,
        "HEIRLOOM_KINDS": len(heirloom.KINDS),
        "DOOR_COUNT": len(data["levels"][0]["doors"]),
        "OBJECT_BYTES": OBJECT_BYTES,
        "MAX_ENEMIES": MAX_ENEMIES,
        "ENEMY_KINDS": len(enemies.KINDS),
        "ENEMY_TYPES": len(enemies.TYPES),
        "ENEMY_TYPES_1": ENEMY_TYPES_1,
        **type_constants(),
        "BAR_EMPTY": font.code("bar0"),
        "DIGIT_0": font.code("0"),
        "HEALTH_BAR": hud_offset("heart", 1),
        "ENERGY_BAR": hud_offset("bat", 1),
        "HEIRLOOM_DIGIT": hud_offset("chalice", 1),
        "NIGHT_BAR": hud_offset("moon", 1),
        # Tom Darkfang (tom.py) and his arena (level8.py).
        "HUD_GLYPHS": len(font.GLYPH_ORDER),
        "TOM_BAR": 880 + 80 + TOM_BAR,         # row 24
        "TOM_PICTURES": len(tom.NAMES),
        "TOM_PAGES": len(data["tom"]) // 256,
        "TOM_COLOUR": tom.OWN_COLOUR,
        "TOM_FLASH_COLOUR": tom.FLASH_COLOUR,
        "TOM_BOX_LEFT": tom.box()[0],
        "TOM_BOX_UP": tom.box()[2],
        "ARENA_X": level8.ARENA_X,
        "TOM_START_X": level8.TOM_START_X,
        "TOM_MIN_X": level8.TOM_MIN_X,
        "TOM_MAX_X": level8.TOM_MAX_X,
        "THRONE_X": level8.THRONE_X,
        "DAIS_TOP": level8.DAIS_TOP,
        # The title (title.py, logo.py) and the states.
        "TITLE_LEVEL": title.TITLE_LEVEL - 1,
        "TITLE_X": title.TITLE_X,
        "TITLE_MOON_X": title.TITLE_MOON_X,
        "TITLE_MOON_Y": title.TITLE_MOON_Y,
        "LOGO_X": title.LOGO_X,
        "LOGO_Y": title.LOGO_Y,
        "LOGO_STEP": title.LOGO_STEP,
        "LOGO_COLOUR": logo.LOGO_COLOUR,
        "LOGO_SPRITES": logo.SPRITES,
        "MENU_ROW": title.MENU_ROW,
        "MENU_COL": title.MENU_COL,
        "POINTER_COL": title.POINTER_COL,
        "MENU_CHOICES": len(title.CHOICES),
        "CHOSEN_COLOUR": title.CHOSEN,
        "POINTER_CODE": font.code(">"),
        "POINTER_COLOUR": title.POINTER,
        "PRESS_CELL": title.PRESS[0] * 40 + title.PRESS[1],
        "PRESS_LENGTH": len(title.PRESS[2]),
        "PRESS_ON": title.PRESS_ON,
        "PRESS_OFF": title.PRESS_OFF,
        "BANDS": len(title.BANDS),
        **{f"BAND_{name.upper()}": index
           for index, name in enumerate(title.BAND_ORDER)},
        "SCORE_CELL": 880 + 80 + score_column(),
        "DAWN_STEPS": len(title.DAWN_COLOURS),
        "DAWN_FRAMES": title.DAWN_FRAMES,
    }
    if any(len(entry["doors"]) != constants["DOOR_COUNT"]
           or len(entry["module"].HEIRLOOMS) != 3
           for entry in data["levels"]):
        raise ValueError("every level: three heirlooms, the same doors")
    if any(env["moth_tile"] != data["moth_tile"] for env in data["envs"]):
        raise ValueError("the moth: the same metatile in every setting")
    offset = 0
    for name, size in OBJECT_FIELDS:            # where each field is
        constants[f"OF_{name.upper()}"] = offset
        offset += size
    text = ["; Written by game/assets/build_assets.py: do not edit."]
    text += [f"{name:<18} = {value}" for name, value in constants.items()]
    write_text(OUT / "assets.inc", "\n".join(text) + "\n")
    for name, text in {**objects_asm(data), **tables_asm(data)}.items():
        write_text(OUT / name, text)
    write_text(OUT / "staff.json", json.dumps({
        "held": staff.held_table(), "blow": staff.blow_table()},
        indent=1) + "\n")
    save_png(capture_of(start_picture(data)), OUT / "preview.png")
    for entry in data["levels"]:
        save_png(level_picture(data, entry),
                 OUT / f"level{entry['number']}.png")
        write_text(OUT / f"level{entry['number']}.json",
                   json.dumps(level_json(entry), indent=1) + "\n")
    summary = {name: {"bytes": len(content),
                      "sha256": hashlib.sha256(content).hexdigest()}
               for name, content in files.items()}
    summary["packed"] = {
        name: {"bytes": len(content), "runs": pack.runs(content),
               "sha256": hashlib.sha256(content).hexdigest()}
        for name, content in packed.items()}
    summary["counts"] = {
        "settings": {
            env["name"]: {
                "scene_characters": env["scene_chars"],
                "per_level_new_characters": [
                    e["new_chars"] for e in env["levels"]],
                "free_characters": env["limit"] - FIRST_SCENE_CHAR
                - env["scene_chars"],
                "metatiles": len(env["metatiles"]),
                "per_level_new_metatiles": [
                    e["new_tiles"] for e in env["levels"]],
                "profiles": len(env["profiles"])}
            for env in data["envs"]},
        "moth_characters": 2,
        "moths": [len(e["module"].MOTHS) for e in data["levels"]],
        "sprite_pictures": len(data["sprites"]) // 128,
        "heirloom_kinds": len(heirloom.KINDS),
        "enemy_types": len(enemies.TYPES),
        "staff_pictures": len(data["staff"]) // 64,
        "level_columns": [len(e["level"]) for e in data["levels"]]}
    songs = music.compile_music()
    theme, high = music.assembler(songs)
    write_text(OUT / "music.asm", theme)
    write_text(OUT / "music_high.asm", high)
    summary["music"] = music.summary(songs[0])
    summary["music_boss"] = music.summary(songs[1])
    for number, name in enumerate(("clear", "won", "dawn"), 2):
        summary[f"music_{name}"] = music.summary(songs[number])
    write_text(OUT / "sfx.asm", sfx.assembler())
    summary["sfx"] = sfx.summary()
    write_text(OUT / "assets.json", json.dumps(summary, indent=2) + "\n")
    return summary


def write_text(path, text):
    """UTF-8 with LF line ends, on Windows too: the files are the
    same bytes on every system."""
    with open(path, "w", encoding="utf-8", newline="\n") as file:
        file.write(text)


def main():
    data = build()
    summary = write(data)
    counts = summary["counts"]
    parts = []
    for name, env in counts["settings"].items():
        parts.append(
            f"{name}: {env['scene_characters']} characters (levels "
            f"{' + '.join(map(str, env['per_level_new_characters']))}"
            f"; {env['free_characters']} free), {env['metatiles']} "
            f"metatiles")
    print("Assets written: " + "; ".join(parts) + f"; {len(LEVELS)} "
          f"levels of {counts['level_columns'][0]} columns.")


if __name__ == "__main__":
    main()
