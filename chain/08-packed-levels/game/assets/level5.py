"""Level 5, THE GREY CRAGS: where everything is.

The plan of the eight levels gives the
level: 128 metatile columns in three tracts, the first level of the
mountain. It has a set of characters of its own (crags.py;
one set for each level). Coordinates as in level1.py:

  - x in multicolour pixels for the drawing (8 a metatile column),
    in level pixels for everything else (16 a metatile column);
  - y in lines, 0 at the top of the playfield; the path is line 144;
  - (column, row) of a metatile: 128 columns, 11 rows.

  A, the mountain path (columns 0-41): a low ledge (h2), a boulder to
     stand on (h2: Oscar passes in front of it), the high ledge (its
     top at h4) over the path, a rock (h2). The first heirloom, the
     chalice, on the high ledge: off the path, up from the boulder
     (column 24, not at the ledge's far end, 30: from the rock a jump
     took it there).
  B, the crevasse (42-85): 16 metatiles of nothing, three stones
     standing out of it (h0) and the pinnacle in the middle, solid
     from the bottom to h6: it is passed only by the bat, from the
     stone before it. The second heirloom, the portrait, on top of the
     pinnacle: only the bat gets there. The lantern after the
     crevasse.
  C, under the crag (86-127): the crag, solid from h6 up, shuts the
     sky; under it two cracks 3 metatiles wide, hard jumps (or a low
     flight). The third heirloom, the medallion, on the path between
     the cracks. The way out, between two cairns: the mouth of the
     pass.

The picture: rocks and snow under the moon
(crags.py).
"""

import crags as m
import village as v

COLUMNS = 128
WIDTH = COLUMNS * 8                     # multicolour pixels
NAME = "THE GREY CRAGS"
ENVIRONMENT = "crags"
ENEMY_SETTING = "mountain"

START_X, START_Y = 28, v.GROUND_Y       # sensor in column 2

# Gameplay things, from the plan.
PITS = [(46, 61), (94, 96), (106, 108)]  # the crevasse, two cracks
WATER = []
# Solid blocks: (first column, last column, first row, last row).
SOLIDS = [(8, 14, 7, 8),                # the low ledge, h2
          (20, 30, 5, 5),               # the high ledge, its top h4
          (32, 33, 7, 8),               # a rock, h2
          (49, 49, 9, 10),              # the stones of the crevasse,
          (52, 52, 9, 10),              # h0
          (55, 55, 3, 10),              # the pinnacle, its top h6
          (58, 58, 9, 10),
          (86, 117, 0, 3)]              # the crag over C, from h6 up
BOULDER = (16, 112)                     # (column, line of its top)
# Moths, in the black sky: (column, row) of the moth metatile.
MOTHS = [(18, 2), (50, 2), (60, 2), (74, 2), (92, 5)]
# Heirlooms: (column, line of the top of the 16 x 16 box, kind).
HEIRLOOMS = [(24, 56, "chalice"),       # on the high ledge
             (55, 24, "portrait"),      # on the pinnacle
             (100, 120, "medallion")]   # between the cracks
LANTERN = (66, 7)                       # (column, row) of its head
GATE_X = 976                            # the cairns: columns 122-125
DOOR = (123, 124, 6, 8)                 # the doorway
# The enemies of the mountain (the plan: a goat on the low ledge, a
# werewolf of the band, an eagle over the crevasse, a goat, an eagle
# under the crag, a goat between the cracks, a werewolf).
ENEMIES = [("patrol", 8, 14, 11, 112, "right"),            # A, a goat
           ("jumper", 35, 41, 38, "street", "left"),       # A, a wolf
           ("flyer", 44, 58, 50, 104, "left"),             # B, eagle
           ("patrol", 72, 84, 78, "street", "right"),      # B, a goat
           ("flyer", 88, 104, 96, 100, "right"),           # C, eagle
           ("patrol", 97, 105, 101, "street", "left"),     # C, a goat
           ("jumper", 110, 120, 115, "street", "left")]    # C, a wolf
# The pines (pixels, on the grid of 4) and the peaks far away (their
# top: pixel, a multiple of 4; line, a multiple of 8).
PINES = [36, 108, 284, 500, 612, 656]
PEAKS = [(64, 88), (344, 80), (480, 96), (600, 88)]


def stars_list():
    """Stars, as in the other levels, from another seed; all white;
    none in the lines of the moon (it goes behind the crag here)."""
    found = []
    patterns = ("dot", "dot", "cross", "dot", "dot", "cross")
    seed, col = 211, 3
    for n in range(80):
        seed = (seed * 75 + 74) % 65537
        col += 2 + seed % 5
        if col >= COLUMNS * 2:
            break
        row = 3 + (seed // 7) % 5
        found.append((col, row, patterns[seed % len(patterns)], v.WHITE))
    return found


def draw(canvas, lit=False, open_door=False):
    """The picture of the level on `canvas` (WIDTH x 176), and its
    surfaces: [(name, {level x: line}, colours it stands on)]."""
    c = canvas
    surfaces = []
    # Far behind: the peaks; behind: the pines.
    for cx, top in PEAKS:
        m.peak(c, cx, top)
    for x in PINES:
        m.pine(c, x)
    m.back_face(c, 20 * 8 + 2, 30 * 8 + 5, 96, v.GROUND_Y - 1)
    x, top = BOULDER
    surfaces.append(("boulder", m.boulder(c, x * 8, top), {m.WHITE}))
    m.ground(c, [(first * 8, last * 8 + 7) for first, last in PITS])
    # The rock: ledges, the rock, the stones, the pinnacle, the crag.
    for first, last, row, bottom in SOLIDS:
        if first == 86:
            continue
        if first == last:                   # stones, the pinnacle
            m.pillar(c, first * 8, row * 16, 174)
            continue
        m.rock_block(c, first * 8, last * 8 + 7, row * 16,
                     bottom * 16 + 15, under=bottom < 7)
        if bottom < 7:
            m.icicles(c, first * 8 + 1, last * 8 + 6, bottom * 16 + 16)
    m.crag(c, 86 * 8, 117 * 8 + 7, 63)
    m.back_face(c, 46 * 8, 61 * 8 + 7, v.GROUND_Y, 174, fade=True)
    surfaces.append(("lantern", v.lantern(c, LANTERN[0] * 8, lit),
                     {v.STONE}))
    m.pass_mouth(c, GATE_X)
    if not open_door:
        m.barricade(c, GATE_X)
    m.sky(c)
    clear = [s for s in stars_list()
             if c.cell_colours(s[0], s[1]) == {v.BACKGROUND}
             and not near_moth(s[0], s[1])]
    v.stars(c, clear)
    street = {}
    for x in range(COLUMNS * 16):
        if not any(first * 16 <= x < (last + 1) * 16
                   for first, last in PITS):
            street[x] = v.GROUND_Y
    surfaces.insert(0, ("street", street, {m.WHITE, m.STONE}))
    return [(name, {x: y for x, y in line.items()
                    if 0 <= x < COLUMNS * 16}, colours)
            for name, line, colours in surfaces]


def near_moth(col, row):
    """A star cell inside a moth's metatile, or the next one: none."""
    return any(abs(col // 2 - mcol) <= 1 and row // 2 == mrow
               for mcol, mrow in MOTHS)
