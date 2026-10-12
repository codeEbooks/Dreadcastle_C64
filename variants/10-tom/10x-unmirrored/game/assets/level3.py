"""Level 3, THE WILD WOOD: where everything is.

The plan of the eight levels gives the
level: 128 metatile columns in three tracts, in the first wood of the
wild lands. It has the forest's set of characters (forest.py), not
the village's. Coordinates as in level1.py:

  - x in multicolour pixels for the drawing (8 a metatile column),
    in level pixels for everything else (16 a metatile column);
  - y in lines, 0 at the top of the playfield; the path is line 144;
  - (column, row) of a metatile: 128 columns, 11 rows.

  A, the edge of the wood (columns 0-41): the Count's staff on the
     path just after the start (column 8): Oscar takes it walking over
     it, and from then on Fire strikes. A fallen trunk, a branch, a
     stump; the first heirloom, the chalice, in the clearing, on the
     path.
  B, the deep wood (42-85): a stump and a branch; brambles across the
     path, to jump; the lantern of the checkpoint; the great oak, with
     a stump at its foot, a low branch and a high one. The second
     heirloom, the portrait, on the high branch: from the low branch
     only the bat reaches it.
  C, the river and the hollow oak (86-127): the river (water, 17
     metatiles) with five stepping stones; the hollow oak, a huge oak
     fallen long ago, solid, with the passage under it, 3 metatiles
     high; its roots, sawn off, make steps. The third heirloom, the
     medallion, on top of the hollow oak, at its left end: up the
     roots, then back to the left (at column 114 a jump from the roots
     could reach it, tests/levels.py). The way out of the wood, a gap
     in the hedge: the exit.

The picture (forest.py) is the second drawing of the wood, with
better trees and bushes.
"""

import forest as f
import village as v

COLUMNS = 128
WIDTH = COLUMNS * 8                     # multicolour pixels
NAME = "THE WILD WOOD"
ENVIRONMENT = "forest"

START_X, START_Y = 28, v.GROUND_Y       # sensor in column 2

# Gameplay things, from the plan.
PITS = []
WATER = [(92, 108)]                     # the river
# Solid blocks: (first column, last column, first row, last row).
SOLIDS = [(10, 11, 8, 8),               # the fallen trunk, h1
          (24, 25, 7, 8),               # a stump, h2
          (44, 44, 8, 8),               # a stump, h1
          (70, 71, 7, 8),               # the stump by the oak, h2
          (112, 117, 4, 5),             # the hollow oak, h5 to h3
          (118, 119, 8, 8),             # its roots: h1
          (120, 121, 6, 8)]             # and h3
# Hazards: (first column, last column, row): the brambles.
HAZARDS = [(54, 55, 8), (60, 61, 8)]
# Moths, in the black sky: (column, row) of the moth metatile.
MOTHS = [(36, 1), (56, 1), (68, 1), (98, 2), (104, 2)]
# Heirlooms: (column, line of the top of the 16 x 16 box, kind).
HEIRLOOMS = [(30, 120, "chalice"),      # in the clearing, on the path
             (84, 16, "portrait"),      # by the high branch, h7
             (112, 48, "medallion")]    # on top of the hollow oak
LANTERN = (64, 7)                       # (column, row) of its head
GATE_X = 976                            # the hedge: columns 122-125
DOOR = (123, 124, 6, 8)                 # the gap
STAFF = 8                               # the column of the staff
STONES = [94, 97, 100, 103, 106]        # the stepping stones, h1
BRANCHES = [(14, 17, 96, "branch A"),   # (columns, line, name)
            (46, 51, 96, "branch B")]
OAK = 72                                # the great oak: its trunk
LOW_BRANCH, HIGH_BRANCH = (80, 78), (32, 86)     # (line, last column)
# The enemies of the wood (the plan: werewolf scouts, owls, giant
# toads); with the staff they can be struck.
ENEMIES = [("jumper", 16, 26, 20, "street", "left"),      # A, a toad
           ("patrol", 32, 40, 36, "street", "right"),     # A, a scout
           ("patrol", 45, 53, 49, "street", "left"),      # B, a scout
           ("flyer", 72, 84, 78, 56, "right"),            # B, an owl
           ("flyer", 92, 108, 100, 104, "left"),          # C, an owl
           ("jumper", 110, 117, 114, "street", "right")]  # C, a toad

# The wood behind the path: trees, all of one drawing (cell column of
# the trunk, a multiple of 4: the bushes repeat every 4 cells; the row
# of the crown); the trees at columns 36 and 104 hold branches A and
# B, the great oak is at OAK. The bushes from pixel x to x (whole
# cells). The crowns stay under the moon's lines: the moon is a
# sprite, still in the sky (moon.py).
TREES = [(8, 4), (36, 4), (60, 5), (80, 4), (104, 4), (132, 5)]
UNDERGROWTH = [(0, 735), (872, 895)]


def stars_list():
    """Stars, as in the levels of the village, from another seed; all
    white (the forest's set has few characters to spare)."""
    found = []
    patterns = ("dot", "dot", "cross", "dot", "dot", "cross")
    seed, col = 41, 2
    for n in range(80):
        seed = (seed * 75 + 74) % 65537
        col += 2 + seed % 5
        if col >= COLUMNS * 2:
            break
        row = (seed // 7) % 7
        found.append((col, row, patterns[seed % len(patterns)], v.WHITE))
    return found


def draw(canvas, lit=False, open_door=False):
    """The picture of the level on `canvas` (WIDTH x 176), and its
    surfaces: [(name, {level x: line}, colours it stands on)]."""
    c = canvas
    surfaces = []
    for col, crown_row in TREES:                # the wood behind
        f.tree(c, col, crown_row)
    # A, the edge of the wood.
    f.log(c, 80)
    for first, last, line, name in BRANCHES:
        surfaces.append((name, f.branch(c, first * 8, last * 8 + 7,
                                        line), {v.WOOD, v.STONE}))
    f.stump(c, 192, 16, 112)
    # B, the deep wood.
    f.stump(c, 352, 8, 128)
    for first, last, row in HAZARDS:
        f.thorns(c, first, last - first + 1)
    surfaces.append(("lantern", v.lantern(c, LANTERN[0] * 8, lit),
                     {v.STONE}))
    f.stump(c, 560, 16, 112)
    low = f.big_oak(c, OAK, LOW_BRANCH[0], HIGH_BRANCH[0],
                    LOW_BRANCH[1] * 8 + 7, HIGH_BRANCH[1] * 8 + 7)
    surfaces.append(("low branch", low, {v.WOOD, v.STONE}))
    # The high branch is drawn, not walked on: on it the portrait
    # could be reached by a jump (the plan: only in flight).
    # C, the river, the hollow oak, the hedge.
    f.hollow_oak(c, 112, 6, 64, 95)
    f.oak_roots(c, 944, 128, 96)
    f.hedge_gate(c, GATE_X)
    if not open_door:
        f.hedge_doors(c, GATE_X)
    f.hedge(c, GATE_X + 32, WIDTH - 1, 64)
    f.ground(c)
    for first, last in WATER:
        f.river(c, first * 8, (last - first + 1) * 8)
    for number, col in enumerate(STONES, 1):
        surfaces.append((f"stone {number}", f.stone(c, col * 8),
                         {v.STONE}))
    for x0, x1 in UNDERGROWTH:                  # last: in free cells
        f.undergrowth(c, x0, x1)
    f.sky(c)
    clear = [s for s in stars_list()
             if c.cell_colours(s[0], s[1]) == {v.BACKGROUND}
             and not near_moth(s[0], s[1])]
    v.stars(c, clear)
    street = {}
    for x in range(COLUMNS * 16):
        if not any(first * 16 <= x < (last + 1) * 16
                   for first, last in PITS + WATER):
            street[x] = v.GROUND_Y
    surfaces.insert(0, ("street", street, {f.GREEN}))
    return [(name, {x: y for x, y in line.items()
                    if 0 <= x < COLUMNS * 16}, colours)
            for name, line, colours in surfaces]


def near_moth(col, row):
    """A star cell inside a moth's metatile, or the next one: none."""
    return any(abs(col // 2 - mcol) <= 1 and row // 2 == mrow
               for mcol, mrow in MOTHS)
