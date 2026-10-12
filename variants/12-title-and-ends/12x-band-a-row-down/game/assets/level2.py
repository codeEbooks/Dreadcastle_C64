"""Level 2, THE CHURCHYARD: where everything is.

The plan of the eight levels gives the
level: 128 metatile columns in three tracts, out of the houses, in the
churchyard of the church. It shares the set of characters and the
metatiles of level 1 (one set for the two levels of the village), so
it is drawn with the same pieces, and a few of its own (village.py,
"The churchyard"). Coordinates as in level1.py:

  - x in multicolour pixels for the drawing (8 a metatile column),
    in level pixels for everything else (16 a metatile column);
  - y in lines, 0 at the top of the playfield; the street (here the
    path of the churchyard) is line 144;
  - (column, row) of a metatile: 128 columns, 11 rows.

  A, the church and the tombs (columns 0-41): the start before the
     door of the church (the door of its tower, the clock tower of the
     village's square); tombstones, two open graves, the family tomb.
     The first heirloom, the candelabrum, on the family tomb.
  B, the meadow of the crosses (42-85): a tombstone, the landslide (a
     gap of 6 metatiles, to fly over), the lantern of the checkpoint,
     the sarcophagus and the chapel (solid, 3 metatiles high: one
     climbs the sarcophagus first). The second heirloom, the
     hourglass, over the bell-cote of the chapel: only the bat
     reaches it.
  C, the stream and the wall (86-127): the stream, with the piles of
     the broken bridge (on foot from pile to pile, or flying); the
     angel on its pedestal and the wall of the churchyard, walked on.
     The third heirloom, the book, over the wall: from the pedestal
     up onto the wall, then a jump. The gate of the churchyard (the
     village's gatehouse, here a lych-gate): the exit.
"""

import village as v

COLUMNS = 128
WIDTH = COLUMNS * 8                     # multicolour pixels
NAME = "THE CHURCHYARD"

# Oscar at the start: as in level 1, before the door of the tower.
START_X, START_Y = 28, v.GROUND_Y       # sensor in column 2

# Gameplay things, from the plan.
PITS = [(28, 29), (34, 35),             # two open graves
        (54, 59)]                       # the landslide
WATER = [(92, 101)]                     # the stream
# Solid blocks: (first column, last column, first row, last row).
SOLIDS = [(18, 18, 8, 8), (22, 22, 8, 8), (26, 26, 8, 8),  # h1
          (36, 39, 7, 8),               # the family tomb, h2
          (52, 52, 8, 8), (53, 53, 8, 8),   # two tombstones, h1
          (70, 71, 7, 8),               # the sarcophagus, h2
          (72, 80, 6, 8)]               # the chapel, h3
# Moths, in the black sky: (column, row) of the moth metatile.
MOTHS = [(40, 2), (56, 3), (74, 2), (96, 3), (116, 2)]
# Heirlooms: (column, line of the top of the 16 x 16 box, kind).
HEIRLOOMS = [(38, 96, "candelabrum"),   # on the family tomb, h2
             (76, 8, "hourglass"),      # over the bell-cote, h8
             (112, 56, "book")]         # over the wall
LANTERN = (66, 7)                       # (column, row) of its head
GATE_X = 976                            # the gatehouse: columns
DOOR = (123, 124, 6, 8)                 # 122-125; the doorway
PILES = [94, 98]                        # the bridge: 2 columns each
# The enemies, from the plan, only to be avoided here (as in
# level1.py).
ENEMIES = [("jumper", 16, 26, 20, "street", "left"),      # A, tombs
           ("flyer", 30, 40, 35, 100, "left"),            # A, graves
           ("patrol", 42, 51, 46, "street", "right"),     # B
           ("flyer", 90, 102, 96, 104, "right"),          # C, stream
           ("jumper", 108, 120, 116, "wall", "left")]     # C, wall

THE_TOWER = -64                         # the clock tower: columns 0-2
THE_MOON = 44 * 8                       # where it is in level 1


def stars_list():
    """Stars in the sky, as in level 1 but from another seed."""
    found = []
    patterns = (("dot", v.WHITE), ("cross", v.WHITE), ("dot", v.YELLOW),
                ("dot", v.WHITE), ("cross", v.YELLOW), ("dot", v.CYAN),
                ("dot", v.WHITE))
    seed, col = 23, 3
    for n in range(80):
        seed = (seed * 75 + 74) % 65537
        col += 2 + seed % 5
        if col >= COLUMNS * 2:
            break
        row = (seed // 7) % 9
        pattern, colour = patterns[seed % len(patterns)]
        found.append((col, row, pattern, colour))
    return found


CROSSES = [108, 124, 140,               # A: before the tombstones
           244, 260,                    # between the graves
           340, 356, 372, 388, 404,     # B: the meadow
           484, 500, 548,               # by the lantern
           652, 668, 684,               # after the chapel
           700, 716, 732]               # C: before the stream


def draw(canvas, lit=False, open_door=False):
    """The picture of the level on `canvas` (WIDTH x 176), and its
    surfaces: [(name, {level x: line}, colours it stands on)]. With
    `lit` the lantern is lit; with `open_door` the gate is open."""
    c = canvas
    surfaces = []
    # A, the church and the tombs.
    surfaces.append(("church roof", v.church(
        c, 24, 80, 72,
        windows=((2, 11), (7, 11), (12, 11), (17, 11),
                 (2, 15), (7, 15), (12, 15), (17, 15))), {v.WOOD}))
    tower = v.Shifted(c, THE_TOWER)
    v.tower(tower)                          # in front of the roof's end
    name, line, colours = surfaces[0]
    surfaces[0] = (name, {x: y for x, y in line.items() if x >= 48},
                   colours)
    for name, line, colours in v.first_scene_surfaces():
        if name == "spire":
            surfaces.append((name, {x + 2 * THE_TOWER: y
                                    for x, y in line.items()}, colours))
    v.moon(v.Shifted(c, THE_MOON))
    for x in CROSSES:
        v.wooden_cross(c, x)
    for first, last, top, bottom in SOLIDS:
        if (first, last) in ((36, 39), (70, 71)):
            continue
        if top == 8:
            for col in range(first, last + 1):
                v.tombstone(c, col * 8)
    v.stone_block(c, 288, 32, 112)          # the family tomb
    v.plaque(c, 300, 120)
    v.plaque(c, 308, 120)
    # B, the meadow: the lantern, the sarcophagus, the chapel.
    surfaces.append(("lantern", v.lantern(c, LANTERN[0] * 8, lit),
                     {v.STONE}))
    v.stone_block(c, 560, 16, 112)          # the sarcophagus
    v.plaque(c, 566, 120)
    v.chapel(c, 576, 72, windows=((2, 13), (5, 13), (12, 13),
                                  (15, 13)), doors=((8, 15),))
    # C, the stream, the angel, the wall, the gate.
    surfaces.append(("pedestal", v.angel(c, 832), {v.WOOD}))
    surfaces.append(("wall", v.cemetery_wall(c, 848, 128, 80),
                     {v.WOOD}))
    surfaces.append(("gate roof", v.gate(c, GATE_X), {v.WOOD}))
    if not open_door:
        v.gate_doors(c, GATE_X)
    v.street(c)
    for first, last in PITS:
        v.hole(c, first * 8, (last - first + 1) * 8)
    for first, last in WATER:
        v.canal(c, first * 8, (last - first + 1) * 8)
    for number, col in enumerate(PILES, 1):
        surfaces.append((f"pile {number}", v.bridge_pile(c, col * 8),
                         {v.WOOD}))
    v.sky(c)
    clear = [s for s in stars_list()
             if c.cell_colours(s[0], s[1]) == {v.BACKGROUND}
             and not near_moth(s[0], s[1])]
    v.stars(c, clear)
    street = {}
    for x in range(COLUMNS * 16):
        if not any(first * 16 <= x < (last + 1) * 16
                   for first, last in PITS + WATER):
            street[x] = v.GROUND_Y
    surfaces.insert(0, ("street", street, {v.BLUE, v.STONE, v.SKY}))
    return [(name, {x: y for x, y in line.items()
                    if 0 <= x < COLUMNS * 16}, colours)
            for name, line, colours in surfaces]


def near_moth(col, row):
    """A star cell inside a moth's metatile, or the next one: none."""
    return any(abs(col // 2 - mcol) <= 1 and row // 2 == mrow
               for mcol, mrow in MOTHS)
