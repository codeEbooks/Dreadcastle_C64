"""Level 7, DREADCASTLE GATE: where everything is.

The plan of the eight levels gives the
level: 128 metatile columns in three tracts, the castle held by Tom
Darkfang's band. The drawbridge is up: the way in is in flight, over
the moat, and through the postern. It has a set of characters of its
own (keep.py). Coordinates as in level1.py:

  - x in multicolour pixels for the drawing (8 a metatile column),
    in level pixels for everything else (16 a metatile column);
  - y in lines, 0 at the top of the playfield; the path is line 144;
  - (column, row) of a metatile: 128 columns, 11 rows.

  A, the moat and the postern (columns 0-41): the moat (water, 12-21),
     to be crossed in flight; the outer wall (22-41), solid from the
     postern up to the top: the postern, a passage 3 metatiles high
     at its foot, is the only way through, and a werewolf guards it
     (too low to jump over him: he must be struck). The first
     heirloom, the chalice, in the postern.
  B, the courtyard (42-85): a barrel (h2), a cart (h2), the lantern,
     another barrel (h2) and the turret (solid, its top at h3) with
     its pointed roof; past it, down to the courtyard: one way on
     foot. The second heirloom, the portrait, on the top of the roof
     (h8): only the bat gets there.
  C, the second wall (86-127): low pillars (h1) with spikes after
     each; over them the wall walk (its top at h5, four metatiles
     free under it: room to jump over the spikes), too high from the
     pillars; a step (h1) and the stair of the guard tower (solid,
     h3, then h2) before the castle's door. The third heirloom, the medallion,
     on the wall walk: up from the stair, back to the left. The way
     out: the castle's door.

The picture: stone and lit windows; the
spikes still, the fire burning; drawn a third time after the castle
of the book's frontispiece and cover, under a blue night:
keep.py.
"""

import keep as m
import village as v

COLUMNS = 128
WIDTH = COLUMNS * 8                     # multicolour pixels
NAME = "DREADCASTLE GATE"
ENVIRONMENT = "keep"
ENEMY_SETTING = "castle"

START_X, START_Y = 28, v.GROUND_Y       # sensor in column 2

# Gameplay things, from the plan.
PITS = []
WATER = [(12, 21)]                      # the moat
# Solid blocks: (first column, last column, first row, last row).
SOLIDS = [(22, 41, 0, 5),               # the outer wall, over the
                                        # postern
          (44, 45, 7, 8),               # a barrel, h2
          (58, 59, 7, 8),               # the cart (crates), h2
          (70, 71, 7, 8),               # a barrel, h2
          (72, 76, 6, 8),               # the turret, its top h3
          (88, 89, 8, 8),               # a low pillar, h1
          (92, 113, 4, 4),              # the wall walk, its top h5
          (100, 101, 8, 8),             # a low pillar, h1
          (115, 115, 8, 8),             # a step, h1
          (116, 116, 6, 8),             # the stair of the guard
          (117, 117, 7, 8)]             # tower, h3, h2
# Hazards: (first column, last column, row): the spikes.
HAZARDS = [(94, 95, 8), (108, 109, 8)]
# Moths, in the black sky: (column, row) of the moth metatile.
MOTHS = [(14, 2), (20, 2), (54, 2), (70, 2), (100, 2)]
# Heirlooms: (column, line of the top of the 16 x 16 box, kind).
HEIRLOOMS = [(32, 128, "chalice"),      # in the postern
             (74, 8, "portrait"),       # on the top of the roof
             (96, 40, "medallion")]     # on the wall walk
LANTERN = (66, 7)                       # (column, row) of its head
GATE_X = 976                            # the door: columns 122-125
DOOR = (123, 124, 6, 8)                 # the doorway
TURRET = (72, 76)
# The enemies of the castle (the plan: Tom's crow over the moat, a
# guard in the postern, a guard in the courtyard, a werewolf of the
# band and a crow by the turret, a guard on the wall walk, a werewolf
# and a crow before the door).
ENEMIES = [("flyer", 10, 21, 16, 104, "left"),             # A, crow
           ("patrol", 26, 41, 36, "street", "left"),       # A, guard
           ("patrol", 46, 57, 52, "street", "right"),      # B, guard
           ("jumper", 77, 84, 81, "street", "left"),       # B, a wolf
           ("flyer", 72, 82, 77, 56, "right"),             # B, crow
           ("patrol", 92, 113, 104, 64, "left"),           # C, guard
           ("jumper", 118, 121, 120, "street", "left"),    # C, a wolf
           ("flyer", 106, 121, 112, 40, "left")]           # C, crow

def stars_list():
    """A few stars between the clouds: (cell column, cell row,
    pattern), each the first cell of its metatile."""
    found = []
    patterns = ("dot", "dot", "cross", "dot")
    seed, col = 577, 2
    for n in range(60):
        seed = (seed * 75 + 74) % 65537
        col += 4 + seed % 9
        if col >= COLUMNS * 2:
            break
        row = 2 * ((seed // 7) % 4)
        found.append((col & ~1, row, patterns[seed % len(patterns)]))
    return found


# The clouds: (x, line, rows of cells (first cell, length)).
# On the grid of the metatiles (x by 8, lines by 16), so that clouds
# alike are alike in their metatiles too.
BIG = ((2, 4), (0, 9), (3, 5))
SMALL = ((1, 3), (0, 6))
CLOUDS = [(16, 0, BIG), (136, 48, SMALL), (264, 16, SMALL),
          (400, 0, BIG), (608, 32, SMALL), (712, 0, BIG),
          (896, 16, SMALL)]


def far_away(c):
    """Seen at the start, across the moat: the town on its hill, its
    clock tower."""
    m.town(c, 52)
    m.hill(c, 32, 175, 112)


def outer_wall(c):
    """The outer wall over the postern (columns 22-41): battlements
    over machicolations, two banners of the band, lit windows, arrow
    slits, moss at its foot; under it the postern, a dark passage with
    torches."""
    x0, x1 = 22 * 8, 42 * 8 - 1
    m.wall(c, x0, x1, 8, 95)
    m.machicolations(c, x0, x1, 16)
    m.battlements(c, x0, x1, 0)
    for x in (24 * 8, 36 * 8):
        m.banner(c, x, 32)
    for x in (29 * 8, 33 * 8):
        m.window(c, x, 48)
    for x in (27 * 8, 31 * 8 + 2, 35 * 8 + 4):
        m.slit(c, x, 72)
    for y in range(24, 96):
        m.put(c, x0, y, "k")
    m.tunnel(c, x0, x1)
    m.postern_mouth(c, x0)
    for x in (26 * 8, 38 * 8):
        m.torch(c, x, 104)
    for x in range(x0 + 8, x1 - 8, 32):
        m.moss(c, x, 93)


def courtyard(c):
    """Behind the courtyard, further back in the night: the inner wall
    and its battlements; towers under spires, the great hall under
    its roof, their windows lit; a banner and torches on the wall.
    Windows and spires on the grid of the metatiles, so that alike
    they share their metatiles."""
    m.tower(c, 42 * 8, 91 * 8 - 1, 88)
    m.battlements(c, 42 * 8, 91 * 8 - 1, 80, "far")
    m.tower(c, 43 * 8, 46 * 8 - 1, 72)
    m.cone(c, 44 * 8 + 4, 8, 71)
    m.window(c, 44 * 8, 80)
    m.tower(c, 49 * 8, 59 * 8 - 1, 72)
    m.gable(c, 49 * 8, 59 * 8 - 1, 48, 71)
    for x in (51 * 8, 56 * 8):
        m.window(c, x, 80)
    m.tower(c, 60 * 8, 64 * 8 - 1, 88)
    m.cone(c, 62 * 8, 24, 87)
    m.banner(c, 61 * 8, 96)
    for x in (65 * 8, 69 * 8):
        m.torch(c, x, 96)
    m.tower(c, 81 * 8, 84 * 8 - 1, 56)
    m.cone(c, 82 * 8 + 4, -8, 55)
    m.window(c, 82 * 8, 80)


def draw(canvas, lit=False, open_door=False):
    """The picture of the level on `canvas` (WIDTH x 176), and its
    surfaces: [(name, {level x: line}, colours it stands on)]."""
    c = canvas
    surfaces = []
    # Further back first, then what stands in front of it.
    courtyard(c)
    m.barrel(c, 44 * 8, 112)
    m.cart(c, 58 * 8, 112)
    m.barrel(c, 70 * 8, 112)
    m.turret(c, TURRET[0] * 8, TURRET[1] * 8 + 7, 96)
    m.machicolations(c, TURRET[0] * 8, TURRET[1] * 8 + 7, 88)
    m.cone(c, 74 * 8 + 4, 24, 87)
    m.wall_walk(c, 92 * 8, 114 * 8 - 1, 64,
                [(91 * 8, 92 * 8 - 1), (98 * 8, 99 * 8 - 1),
                 (105 * 8, 106 * 8 - 1), (112 * 8, 114 * 8 - 1)])
    for col in (88, 100):
        m.pillar(c, col * 8, 128)
    m.stair(c, 116 * 8)
    outer_wall(c)
    m.keep_front(c, 118 * 8, 128 * 8 - 1)
    m.window(c, 119 * 8, 32)
    m.banner(c, 120 * 8, 32)
    m.window(c, 126 * 8, 32)
    m.castle_gate(c, GATE_X)
    if open_door:
        m.doorway(c, GATE_X)
    else:
        m.gate_doors(c, GATE_X)
    for x in (121 * 8, 126 * 8 + 4):
        m.torch(c, x, 88)
    m.ground(c, 0, 12 * 8 - 1, "road")
    m.grass(c, 0, 12 * 8 - 1)
    m.ground(c, 22 * 8, 128 * 8 - 1, "pavement")
    for a, b in WATER:
        m.moat(c, a * 8, b * 8 + 7)
    surfaces.append(("lantern", m.lantern(c, LANTERN[0] * 8, lit),
                     {m.BLACK, m.GREY}))
    m.tree(c, 0, 56)
    for x, y, rows in CLOUDS:
        m.cloud(c, x, y, rows)
    far_away(c)
    m.settle(c)
    for first, last, row in HAZARDS:        # the program's spikes
        c.rect(first * 8, row * 16, last * 8 + 7, row * 16 + 15, m.SKY)
    m.sky(c)
    m.stars(c, [s for s in stars_list()
                if c.cell_colours(s[0], s[1]) == {m.SKY}
                and not near_moth(s[0], s[1])])
    street = {}
    for x in range(COLUMNS * 16):
        if not any(a * 16 <= x < (b + 1) * 16 for a, b in WATER):
            street[x] = v.GROUND_Y
    surfaces.insert(0, ("street", street, {m.STONE, m.GREEN, m.BLACK,
                                           m.GREY}))
    return [(name, {x: y for x, y in line.items()
                    if 0 <= x < COLUMNS * 16}, colours)
            for name, line, colours in surfaces]


def near_moth(col, row):
    """A star cell inside a moth's metatile, or the next one: none."""
    return any(abs(col // 2 - mcol) <= 1 and row // 2 == mrow
               for mcol, mrow in MOTHS)
