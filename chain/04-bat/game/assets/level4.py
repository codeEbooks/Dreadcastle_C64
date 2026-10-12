"""Level 4, THE BLACK MIRE: where everything is.

The plan of the eight levels gives the
level: 128 metatile columns in three tracts, past the wood, the
second level of the forest. It has a set of characters of its own
(marsh.py): the forest's is full with the wood. Coordinates as in
level1.py:

  - x in multicolour pixels for the drawing (8 a metatile column),
    in level pixels for everything else (16 a metatile column);
  - y in lines, 0 at the top of the playfield; the path is line 144;
  - (column, row) of a metatile: 128 columns, 11 rows.

  A, the mire (columns 0-41): black water from column 6 to 36, with
     clods of peat on the line of the path, one or two metatiles wide:
     ten jumps of 2, or flights with a stop on a clod. The first
     heirloom, the candelabrum, on the big clod in the middle.
  B, the dead trees (42-85): broken dead trunks (solid, 2 metatiles
     high) and walkways of planks; the will-o'-the-wisps on the ground
     under the second walkway, a boardwalk with a step at each end:
     Oscar goes over them. The lantern between the second trunk and
     the boardwalk. The second heirloom, the hourglass, on the broken
     top of the great dead tree: only the bat reaches it.
  C, the bank of peat (86-127): a long step (h1); a dead tree fallen
     long ago across the path (the plan's "root": solid, its top at
     h4), the passage under it; a boulder (h2), one column further
     right than in the plan (at 118-119, under the tree's end, a jump
     could not climb it: the head stops under the tree). The third
     heirloom, the book, over the fallen tree, at its left end (column
     113, its top on line 40: lower, or at 114, a jump from the bank
     or from the boulder could reach it, tests/levels.py): from the
     boulder, a jump back to the left onto the tree, then a jump. The
     way out, between two dead posts: the path to the mountains.

The picture: mist and black water (marsh.py);
the wisps stay where they are and flicker.
"""

import marsh as m
import village as v

COLUMNS = 128
WIDTH = COLUMNS * 8                     # multicolour pixels
NAME = "THE BLACK MIRE"
ENVIRONMENT = "marsh"
ENEMY_SETTING = "forest"                # its enemies: the wood's

START_X, START_Y = 28, v.GROUND_Y       # sensor in column 2

# Gameplay things, from the plan.
PITS = []
WATER = [(6, 36)]                       # the mire
# The clods in it: (first column, last column), on the path's line.
CLODS = [(8, 8), (11, 11), (14, 14), (17, 18), (21, 21), (24, 24),
         (27, 27), (30, 31), (34, 34)]
# Solid blocks: (first column, last column, first row, last row).
SOLIDS = [(46, 48, 7, 8),               # a dead trunk, h2
          (58, 60, 7, 8),               # a dead trunk, h2
          (76, 78, 7, 8),               # the great dead tree's, h2
          (90, 110, 8, 8),              # the bank, h1
          (112, 117, 5, 5),             # the root, its top at h4
          (119, 120, 7, 8)]             # the boulder, h2
# Hazards: (first column, last column, row): the wisps.
HAZARDS = [(66, 72, 8)]
# The walkways: (first column, last column, line, name).
WALKWAYS = [(50, 56, 96, "walkway"),
            (63, 64, 112, "boardwalk 1"),
            (65, 72, 96, "boardwalk 2"),
            (73, 74, 112, "boardwalk 3")]
POSTS = [401, 417, 433, 449, 505, 521, 585, 593]    # pixels
# Moths, in the black sky: (column, row) of the moth metatile.
MOTHS = [(16, 3), (32, 3), (54, 1), (70, 1), (100, 3)]
# Heirlooms: (column, line of the top of the 16 x 16 box, kind).
HEIRLOOMS = [(18, 120, "candelabrum"),  # on the big clod
             (77, 16, "hourglass"),     # on the great dead tree, h7
             (113, 40, "book")]         # over the fallen tree
LANTERN = (62, 7)                       # (column, row) of its head
GATE_X = 976                            # the posts: columns 122-125
DOOR = (123, 124, 6, 8)                 # the doorway
TREE = 612                              # the great dead tree: x
# The enemies of the mire, the wood's (the plan: an owl over the
# water, a toad on the shore, a scout on the walkway, an owl by the
# great dead tree, a scout and a toad on the bank).
ENEMIES = [("flyer", 10, 34, 22, 104, "left"),           # A, an owl
           ("jumper", 37, 41, 39, "street", "left"),     # A, a toad
           ("patrol", 50, 56, 53, "walkway", "right"),   # B, a scout
           ("flyer", 70, 84, 77, 56, "right"),           # B, an owl
           ("patrol", 90, 108, 99, 128, "left"),         # C, a scout
           ("jumper", 96, 110, 104, 128, "right")]       # C, a toad
# The dead trees: (x, width, top line, foot line, limbs: x, line,
# angle, length, thickness, forks); the great one first.
SNAG = [(1, 84, -40, 22, 3, 1), (5, 72, 34, 18, 3, 1)]   # limbs
SNAGS = [(TREE - 2, 20, 32, v.GROUND_Y - 1,
          [(TREE + 2, 60, -50, 30, 4, 1), (TREE + 12, 46, 42, 26, 4, 1),
           (TREE + 6, 36, -12, 12, 3, 0)], 12, 3),
         (100, 7, 58, m.WATER_TOP,
          [(100 + d, y, a, n, t, f) for d, y, a, n, t, f in SNAG], 5, 1),
         (740, 7, 58, 127,
          [(740 + d, y, a, n, t, f) for d, y, a, n, t, f in SNAG], 5, 1)]
# The clumps of reeds: pixels.
REEDS = [8, 40, 296, 328, 360, 680, 712, 968, 1000]
def stars_list():
    """Stars, as in the other levels, from another seed; all white."""
    found = []
    patterns = ("dot", "dot", "cross", "dot", "dot", "cross")
    seed, col = 97, 3
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
    # Behind: the dead trees.
    for x0, width, top, foot, limbs, thin, flare in SNAGS:
        m.snag(c, x0, top, width, limbs, foot, thin, flare)
    # A, the mire: the clods.
    for first, last in CLODS:
        surfaces.append((f"clod {first}", m.clod(
            c, first * 8, (last - first + 1) * 8), {v.STONE, v.WOOD}))
    # B, the dead trunks, the walkways, the lantern.
    for first, last, row, bottom in SOLIDS[:2]:
        m.dead_stump(c, first * 8)
    m.fallen_log(c, SOLIDS[2][0] * 8)
    surfaces.append(("lantern", v.lantern(c, LANTERN[0] * 8, lit),
                     {v.STONE}))
    for x in POSTS:                             # under the planks
        m.post(c, x, 101 if x not in (505, 593) else 117,
               v.GROUND_Y - 1)
    for first, last, line, name in WALKWAYS:
        m.planks(c, first * 8, last * 8 + 7, line)
        surfaces.append((name, v.flat(first * 16, last * 16 + 15, line),
                         {v.WOOD}))
    # C, the bank, the root, the boulder, the way out.
    m.bank(c, 90 * 8, 110 * 8 + 7)
    m.fallen_tree(c, 112 * 8, 117 * 8 + 7, 80, 95,
                   [(900, v.GROUND_Y - 1), (946, v.GROUND_Y - 1)])
    m.boulder(c, 119 * 8)
    m.stile(c, GATE_X)
    if not open_door:
        m.stile_doors(c, GATE_X)
    # The path, the water, the mist, the reeds, the grass.
    m.ground(c, [(first * 8, last * 8 + 7) for first, last in WATER])
    for first, last in WATER:
        m.water(c, first * 8, last * 8 + 7)
        m.shore(c, first * 8 - 1, -1)
        m.shore(c, last * 8 + 8, 1)
    for first, last in CLODS:                   # again, on the water
        m.clod(c, first * 8, (last - first + 1) * 8)
    for x in REEDS:
        m.reeds(c, x)
    m.tufts(c, 0, 47)                           # not on the wisps
    m.tufts(c, 296, HAZARDS[0][0] * 8 - 1)
    m.tufts(c, HAZARDS[0][1] * 8 + 8, WIDTH - 1)
    for first, last in WATER:
        m.mist(c, first * 8, last * 8 + 7)
    m.sky(c)
    clear = [s for s in stars_list()
             if c.cell_colours(s[0], s[1]) == {v.BACKGROUND}
             and not near_moth(s[0], s[1])]
    v.stars(c, clear)
    street = {}
    for x in range(COLUMNS * 16):
        if not any(first * 16 <= x < (last + 1) * 16
                   for first, last in PITS + WATER):
            street[x] = v.GROUND_Y
    surfaces.insert(0, ("street", street, {v.STONE, v.WOOD}))
    return [(name, {x: y for x, y in line.items()
                    if 0 <= x < COLUMNS * 16}, colours)
            for name, line, colours in surfaces]


def near_moth(col, row):
    """A star cell inside a moth's metatile, or the next one: none."""
    return any(abs(col // 2 - mcol) <= 1 and row // 2 == mrow
               for mcol, mrow in MOTHS)
