"""Level 1, VILLAGE OF MORTALS: where everything is.

The plan of the eight levels gives
the level: 128 metatile columns in three tracts. Here the plan becomes
a picture and a list of things, in the coordinates of the level:

  - x in multicolour pixels for the drawing (8 a metatile column),
    in level pixels for everything else (16 a metatile column);
  - y in lines, 0 at the top of the playfield, 176 at its bottom;
    the street is line 144 (GROUND_Y);
  - (column, row) of a metatile: 128 columns, 11 rows.

  A, the market (columns 0-41): the merchant's cart with the empty
     sack at the start; crates and a loaded cart; two stalls; the open
     trapdoor of a cellar. The first heirloom, the chalice, on the
     awning of the second stall.
  B, the square of the tower (42-85): the first scene (without its
     cart, now at the start); the lantern of the checkpoint; a
     fountain. The second heirloom, the portrait, high in the sky
     over the square: only the bat reaches it.
  C, the canal and the gate (86-127): the canal, to fly over; the
     long balcony and the well. The third heirloom, the medallion, over
     the balcony (too high for a jump from the street: a jump from the
     balcony), reached from the well by going back. The gate of
     the village: the exit.
"""

import village as v

COLUMNS = 128
WIDTH = COLUMNS * 8                     # multicolour pixels
NAME = "VILLAGE OF MORTALS"

# Oscar at the start: the left edge of his sprite, his feet.
START_X, START_Y = 28, v.GROUND_Y       # sensor in column 2

# Gameplay things, from the plan.
PITS = [(30, 31)]                       # the trapdoor: no street
WATER = [(96, 103)]                     # the canal
# Solid blocks: (first column, last column, first row, last row).
SOLIDS = [(8, 9, 8, 8),                 # two crates, h1
          (16, 17, 7, 8),               # a pile of crates, h2
          (114, 115, 7, 8)]             # the well, h2
# Moths, in the black sky: (column, row) of the moth metatile.
MOTHS = [(68, 2), (80, 2), (98, 3), (102, 3)]
# Heirlooms: (column, line of the top of the 16 x 16 box, kind).
HEIRLOOMS = [(22, 80, "chalice"),       # on the awning, h3
             (74, 32, "portrait"),      # in the sky, h7
             (108, 56, "medallion")]    # over the balcony
LANTERN = (64, 7)                       # (column, row) of its head
GATE_X = 976                            # the gatehouse: columns
DOOR = (123, 124, 6, 8)                 # 122-125; the doorway
# The enemies, from the plan, only to be avoided here: (kind,
# first column, last column of its stretch, start column, where it is:
# the surface it stands on, or for the flyer the line of the middle of
# its wave, facing at the start).
ENEMIES = [("patrol", 1, 7, 5, "street", "left"),        # A
           ("jumper", 44, 53, 47, "left roof", "left"),   # B, roofs
           ("flyer", 72, 84, 78, 56, "right"),            # B, sky
           ("patrol", 104, 113, 108, "street", "right")]  # C

THE_SCENE = 44 * 8                      # the first scene from column 44


def stars_list():
    """Stars in the sky: (cell column, cell row, pattern, colour),
    spread over the level by a little random walk that always gives
    the same stars; draw() keeps those in clear sky."""
    found = []
    patterns = (("dot", v.WHITE), ("dot", v.WHITE), ("cross", v.YELLOW),
                ("dot", v.YELLOW), ("dot", v.WHITE), ("cross", v.WHITE),
                ("dot", v.CYAN))
    seed, col = 7, 1
    for n in range(80):
        seed = (seed * 75 + 74) % 65537
        col += 2 + seed % 5
        if col >= COLUMNS * 2:
            break
        row = (seed // 7) % 9
        pattern, colour = patterns[seed % len(patterns)]
        found.append((col, row, pattern, colour))
    return found


def draw(canvas, lit=False, open_door=False):
    """The picture of the level on `canvas` (WIDTH x 176), and its
    surfaces: [(name, {level x: line}, colours it stands on)]. With
    `lit` the lantern is lit; with `open_door` the gate is open."""
    c = canvas
    surfaces = []
    v.distant_roofs(c)
    # A, the market.
    surfaces.append(("roof A1", v.house(
        c, 0, 48, 80, windows=((2, 12), (7, 12), (1, 15), (9, 15)),
        doors=((6, 15),), boxes=((1, 17), (9, 17)),
        chimney_at=(8, 7, 2)), {v.WOOD}))
    surfaces.append(("roof A2", v.house(
        c, 64, 64, 72, windows=((2, 10), (7, 10), (12, 10), (2, 15)),
        doors=((5, 15),)), {v.WOOD}))
    surfaces.append(("roof A3", v.house(
        c, 144, 64, 80, windows=((2, 12), (7, 12), (12, 12))),
        {v.WOOD}))
    surfaces.append(("roof A4", v.house(
        c, 224, 48, 72, windows=((2, 10), (7, 10), (1, 15), (9, 15)),
        doors=((5, 15),), boxes=((1, 17), (9, 17))), {v.WOOD}))
    surfaces.append(("stall 1", v.stall(c, 96, 32, v.GREEN), {v.WOOD}))
    surfaces.append(("stall 2", v.stall(c, 160, 48, v.YELLOW), {v.WOOD}))
    v.crates(c, 64, 2, 1)
    v.crates(c, 128, 2, 2)
    shifted = v.Shifted(c, -16)             # the cart: columns 4-5
    v.cart(shifted)
    surfaces.append(("cart", {x - 32: y for x, y in
                              v.cart_surface().items()}, {v.WOOD, v.SKY}))
    # B, the square: the first scene, the lantern, the fountain.
    scene = v.Shifted(c, THE_SCENE)
    v.moon(scene)
    v.left_house(scene)
    v.right_house(scene)
    v.tower(scene)
    v.lamp(scene)
    for name, line, colours in v.first_scene_surfaces():
        surfaces.append((name, {x + 2 * THE_SCENE: y
                                for x, y in line.items()}, colours))
    surfaces.append(("lantern", v.lantern(c, LANTERN[0] * 8, lit),
                     {v.STONE}))
    surfaces.append(("fountain", v.fountain(c, 564), {v.WOOD}))
    # C, the canal, the balcony and the well, the gate.
    surfaces.append(("roof C1", v.house(
        c, 688, 80, 72, windows=((2, 10), (7, 10), (12, 10), (17, 10),
                                 (2, 15), (12, 15)),
        doors=((7, 15),), boxes=((2, 17), (12, 17))), {v.WOOD}))
    surfaces.append(("roof C2", v.house(
        c, 832, 64, 72, windows=((2, 10), (7, 10), (12, 10), (2, 15)),
        doors=((7, 15),)), {v.WOOD}))
    surfaces.append(("roof C3", v.house(
        c, 896, 80, 72, windows=((2, 10), (7, 10), (12, 10), (17, 10),
                                 (5, 15)),
        doors=((10, 15),)), {v.WOOD}))
    surfaces.append(("balcony C", v.balcony(c, 848, 96, 96), {v.WOOD}))
    v.well(c, 912)
    surfaces.append(("gate roof", v.gate(c, GATE_X), {v.WOOD}))
    if not open_door:
        v.gate_doors(c, GATE_X)
    v.street(c)
    for first, last in PITS:
        v.hole(c, first * 8, (last - first + 1) * 8)
    for first, last in WATER:
        v.canal(c, first * 8, (last - first + 1) * 8)
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
    # Two roofs side by side: the one drawn later covers the end of
    # the other, so its line wins where both have one.
    roofs = [i for i, (name, _, _) in enumerate(surfaces)
             if "roof" in name]
    for i in roofs:
        later = set()
        for j in roofs:
            if j > i:
                later |= set(surfaces[j][1])
        name, line, colours = surfaces[i]
        surfaces[i] = (name, {x: y for x, y in line.items()
                              if x not in later}, colours)
    return [(name, {x: y for x, y in line.items()
                    if 0 <= x < COLUMNS * 16}, colours)
            for name, line, colours in surfaces]


def near_moth(col, row):
    """A star cell inside a moth's metatile, or the next one: none."""
    return any(abs(col // 2 - mcol) <= 1 and row // 2 == mrow
               for mcol, mrow in MOTHS)
