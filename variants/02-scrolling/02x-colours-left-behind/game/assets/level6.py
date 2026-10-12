"""Level 6, THE FROZEN PASS: where everything is.

The plan of the eight levels gives the
level: 128 metatile columns in three tracts, high in the mountain,
in the snow and the ice. It has a set of characters of its own
(frost.py; one set for each level). Coordinates as in
level1.py:

  - x in multicolour pixels for the drawing (8 a metatile column),
    in level pixels for everything else (16 a metatile column);
  - y in lines, 0 at the top of the playfield; the path is line 144;
  - (column, row) of a metatile: 128 columns, 11 rows.

  A, the glacier (columns 0-41): two mounds of snow (h2), each before
     a slab of ice hanging over the path (solid, its top at h4, three
     metatiles free under it); under the slabs, the spikes of ice: the
     way goes over them, from the mound. The first heirloom, the
     candelabrum, on the path between the two slabs.
  B, the snow bridges (42-85): a chasm 5 metatiles wide with a block
     of ice wedged in it (h0): two jumps of 2, or the bat. The
     lantern. A chasm 3 wide: a hard jump, or the bat. The serac
     (solid, h2) and, high over it, the bridge of snow still standing
     (h6), on a column of ice behind. The second heirloom, the
     hourglass, on the bridge: only the bat gets there.
  C, the wall of ice (86-127): a block of ice (h2), the wall (solid,
     its top at h4), from the block a jump; past it the ledge (a slab,
     its top at h4, free under it) and a drift of snow (h2) before
     the col. From the wall the ledge is out of reach (5 metatiles
     between). The third heirloom, the book, on the ledge: up from the
     drift, back to the left. The way out: the col.

The picture: rocks and snow under the moon; the
spikes still and glinting (frost.py).
"""

import frost as m
import village as v

COLUMNS = 128
WIDTH = COLUMNS * 8                     # multicolour pixels
NAME = "THE FROZEN PASS"
ENVIRONMENT = "pass"
ENEMY_SETTING = "mountain"

START_X, START_Y = 28, v.GROUND_Y       # sensor in column 2

# Gameplay things, from the plan.
PITS = [(46, 50), (70, 72)]             # the two chasms
WATER = []
# Solid blocks: (first column, last column, first row, last row).
SOLIDS = [(11, 14, 5, 5),               # the first slab, its top h4
          (27, 30, 5, 5),               # the second slab
          (48, 48, 9, 10),              # the column of ice in the chasm
          (76, 80, 7, 8),               # the serac, h2
          (96, 97, 7, 8),               # a block of ice, h2
          (100, 108, 5, 8),             # the wall of ice, its top h4
          (114, 119, 5, 5)]             # the ledge, its top h4
# Hazards: (first column, last column, row): the spikes of ice.
HAZARDS = [(11, 14, 8), (27, 30, 8)]
MOUNDS = [(8, "mound 1"), (24, "mound 2"), (120, "drift")]
BRIDGE = (74, 82, 48)                   # columns, the line of its top
# Moths, in the black sky: (column, row) of the moth metatile.
MOTHS = [(24, 2), (48, 2), (60, 2), (96, 5), (116, 2)]
# Heirlooms: (column, line of the top of the 16 x 16 box, kind).
HEIRLOOMS = [(20, 120, "candelabrum"),  # on the path, between slabs
             (78, 24, "hourglass"),     # on the bridge of snow
             (116, 56, "book")]         # on the ledge
LANTERN = (64, 7)                       # (column, row) of its head
GATE_X = 976                            # the col: columns 122-125
DOOR = (123, 124, 6, 8)                 # the doorway
# The enemies of the mountain (the plan: a goat, an eagle, a werewolf
# of the band, an eagle, then in C a goat, a goat on the wall, a
# werewolf; here the werewolf first and the goat under the ledge: a
# werewolf jumping there would put its head into the ledge).
ENEMIES = [("patrol", 16, 23, 19, "street", "right"),      # A, a goat
           ("flyer", 31, 41, 36, 104, "left"),             # A, eagle
           ("jumper", 52, 58, 55, "street", "left"),       # B, a wolf
           ("flyer", 72, 84, 78, 104, "right"),            # B, eagle
           ("jumper", 86, 95, 90, "street", "left"),       # C, a wolf
           ("patrol", 100, 108, 104, 80, "right"),         # C, a goat
           ("patrol", 114, 119, 116, "street", "left")]    # C, a goat
# The peaks far away (their top: pixel, a multiple of 4; line, a
# multiple of 8).
PEAKS = [(40, 80), (168, 72), (336, 88), (472, 64), (560, 80),
         (720, 72)]


def stars_list():
    """Stars, as in the other levels, from another seed; all white."""
    found = []
    patterns = ("dot", "dot", "cross", "dot", "dot", "cross")
    seed, col = 389, 2
    for n in range(80):
        seed = (seed * 75 + 74) % 65537
        col += 2 + seed % 5
        if col >= COLUMNS * 2:
            break
        row = 2 + (seed // 7) % 6
        found.append((col, row, patterns[seed % len(patterns)], v.WHITE))
    return found


def draw(canvas, lit=False, open_door=False):
    """The picture of the level on `canvas` (WIDTH x 176), and its
    surfaces: [(name, {level x: line}, colours it stands on)]."""
    c = canvas
    surfaces = []
    # The ice: slabs, the column in the chasm, the serac, the block,
    # the wall, the ledge; the bridge of snow.
    for a, b, row, bottom in SOLIDS:
        under = bottom < 7
        m.ice_block(c, a * 8, b * 8 + 7, row * 16,
                    min(bottom * 16 + 15, 174), under=under)
        if under:
            m.icicles(c, a * 8 + 1, b * 8 + 6, bottom * 16 + 16)
    first, last, top = BRIDGE
    surfaces.append(("bridge", m.snow_bridge(c, first * 8, last * 8 + 7,
                                             top), {m.WHITE}))
    for col, name in MOUNDS:
        surfaces.append((name, m.heap(c, col * 8), {m.WHITE, m.ICE}))
    m.ground(c, [(a * 8, b * 8 + 7) for a, b in PITS])
    # Behind: the arch of the bridge, the peaks far away.
    m.arch(c, first * 8 + 1, last * 8 + 6, top + 16)
    for cx, peak_top in PEAKS:
        m.peak(c, cx, peak_top)
    surfaces.append(("lantern", v.lantern(c, LANTERN[0] * 8, lit),
                     {v.STONE}))
    m.pass_gate(c, GATE_X)
    if not open_door:
        m.gate_doors(c, GATE_X)
    m.sky(c)
    clear = [s for s in stars_list()
             if c.cell_colours(s[0], s[1]) == {v.BACKGROUND}
             and not near_moth(s[0], s[1])]
    v.stars(c, clear)
    street = {}
    for x in range(COLUMNS * 16):
        if not any(a * 16 <= x < (b + 1) * 16 for a, b in PITS):
            street[x] = v.GROUND_Y
    surfaces.insert(0, ("street", street, {m.WHITE}))
    return [(name, {x: y for x, y in line.items()
                    if 0 <= x < COLUMNS * 16}, colours)
            for name, line, colours in surfaces]


def near_moth(col, row):
    """A star cell inside a moth's metatile, or the next one: none."""
    return any(abs(col // 2 - mcol) <= 1 and row // 2 == mrow
               for mcol, mrow in MOTHS)
