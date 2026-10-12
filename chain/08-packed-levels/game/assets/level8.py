"""Level 8, THE THRONE TOWER: where everything is.

The plan of the eight levels gives the
level: 128 metatile columns in three tracts, inside the castle up to
the throne room, where Tom Darkfang waits. The door at the end of
the level is not its way out:
it leads into the throne room, the
arena, where Oscar fights Tom (tom.asm). It has a set of characters of
its own (hall.py). Coordinates as in level1.py:

  - x in multicolour pixels for the drawing (8 a metatile column),
    in level pixels for everything else (16 a metatile column);
  - y in lines, 0 at the top of the playfield; the floor is line 144;
  - (column, row) of a metatile: 128 columns, 11 rows.

  A, the armoury (columns 0-41): a suit of armour on its plinth (h2)
     and a chest (h1); four chandeliers (h4, two wide), where the bat
     perches. The first heirloom, the candelabrum, on the floor.
  B, the gallery of the portraits (42-85): two rows of columns,
     solid up to the top, a passage 3 metatiles high under each (a
     guard walks there: he must be struck). The lantern. The great
     fireplace: the fire on the hearth, the mantel over it (solid, its
     top at h3), up from a stool (h1). The second heirloom, the
     hourglass, on the top of the fireplace's hood: only the bat gets
     there.
  C, the antechamber and the throne room (86-127): an empty pedestal
     (h2: Oscar passes in front of it, or stands on it) and the
     balcony (solid, its top at h4). The third heirloom, the book, on
     the balcony: up from the pedestal. The door of the throne room
     opens with the three heirlooms; behind it the throne room
     (109-127): the throne on its dais, two pedestals (h2). Through
     the door Oscar is in the throne room, the camera at the
     end of the level, and the door shut behind him: the arena.

The picture: stone and lit windows, the
moon behind the windows; the fire burning; drawn a
third time with the stone and the torches of outside:
hall.py.
"""

import hall as m
import village as v

COLUMNS = 128
WIDTH = COLUMNS * 8                     # multicolour pixels
NAME = "THE THRONE TOWER"
ENVIRONMENT = "hall"
ENEMY_SETTING = "castle"

START_X, START_Y = 28, v.GROUND_Y       # sensor in column 2

# Gameplay things, from the plan.
PITS = []
WATER = []
# Solid blocks: (first column, last column, first row, last row).
SOLIDS = [(6, 7, 7, 8),                 # the suit of armour, h2
          (14, 15, 8, 8),               # the chest, h1
          (46, 50, 0, 5),               # the columns, over a passage
          (56, 60, 0, 5),               # the columns, over a passage
          (70, 71, 8, 8),               # the stool, h1
          (72, 76, 6, 6),               # the mantel, its top h3
          (90, 100, 5, 5),              # the balcony, its top h4
          (104, 108, 0, 5),             # the wall of the throne room,
          (106, 108, 6, 8)]             # its door at 104-105
# Hazards: (first column, last column, row): the fire on the hearth.
HAZARDS = [(73, 75, 8)]
CHANDELIERS = [10, 18, 26, 34]          # their first column; line 80
PEDESTAL = (88, 112)                    # (column, line of its top)
HOOD_TOP = 24                           # the top of the fireplace
# Moths, in the windows: (column, row) of the moth metatile.
MOTHS = [(30, 2), (54, 2), (66, 2), (86, 2)]
# Heirlooms: (column, line of the top of the 16 x 16 box, kind).
HEIRLOOMS = [(22, 128, "candelabrum"),  # on the floor
             (74, 8, "hourglass"),      # on the top of the hood
             (96, 56, "book")]          # on the balcony
LANTERN = (64, 7)                       # (column, row) of its head
GATE_X = 104 * 8                        # the door of the throne room
DOOR = (104, 105, 6, 8)                 # the doorway
# The arena: the throne room, columns 109-127, the whole screen
# with the camera at the end of the level. Oscar comes in at ARENA_X
# (his sprite's left edge, level pixels); Tom waits in front of his
# throne (TOM_START_X, his left edge), runs and leaps between TOM_MIN_X
# and TOM_MAX_X; beaten, he runs back to the throne (THRONE_X), up
# onto its dais (its top DAIS_TOP) and away through the high window
# over it. Two pedestals (h2, two wide), between the banners (the plan
# had them at 112 and 122, under the banners).
ARENA_X = 109 * 16
TOM_START_X = 116 * 16
TOM_MIN_X, TOM_MAX_X = 109 * 16, COLUMNS * 16 - 48
THRONE_X = 117 * 16
DAIS_TOP = 112
ARENA_PEDESTALS = (111, 124)            # their first column
# The bays (32 pixels from a column) with a banner of the band under
# their window; torches on the columns (the column's number).
BANNERS = [3, 5, 8, 10, 17, 20, 25, 28, 30]
TORCHES = [1, 3, 5, 7, 9, 11, 16, 20, 22, 24, 27, 29, 31]
# Stars seen through the windows: (bay, cell row), away from the
# moths.
STARS = [(0, 6), (3, 4), (6, 7), (9, 5), (12, 6), (17, 4), (19, 7),
         (24, 5), (27, 4), (30, 6)]
# The enemies of the castle (the plan: a guard and Tom's crow in A, a
# guard in the gallery and a crow by the fireplace in B, a werewolf of
# the band and a guard on the balcony in C; the werewolf here after
# the fireplace, not under the balcony, where he would put his head
# into it).
ENEMIES = [("patrol", 16, 28, 20, "street", "right"),      # A, guard
           ("flyer", 24, 40, 32, 72, "left"),              # A, crow
           ("patrol", 44, 58, 53, "street", "left"),       # B, guard
           ("flyer", 72, 84, 80, 64, "right"),             # B, crow
           ("jumper", 78, 87, 84, "street", "left"),       # C, a wolf
           ("patrol", 90, 100, 95, 80, "right")]           # C, guard


def draw(canvas, lit=False, open_door=False):
    """The picture of the level on `canvas` (WIDTH x 176), and its
    surfaces: [(name, {level x: line}, colours it stands on)]."""
    c = canvas
    surfaces = []
    # The hall in bays, the whole length; then what stands in it.
    m.bays(c, 0, WIDTH - 1)
    for n in TORCHES:
        m.glow(c, n * m.BAY + 6, 76)
    for n in BANNERS:
        m.banner(c, n * m.BAY + 14, 88)
    for n in TORCHES:
        m.torch(c, n * m.BAY + 4, 72)
    m.floor(c, 0, WIDTH - 1)
    m.moss(c, 0, WIDTH - 1)
    m.armour(c, 6 * 8, 112)
    m.chest(c, 14 * 8, 128)
    for first, last in ((46, 50), (56, 60)):
        m.pier(c, first * 8, last * 8 + 7, 96)
    m.stool(c, 70 * 8, 128)
    m.fireplace(c, 72 * 8, 96, HOOD_TOP)
    surfaces.append(("hood", m.flat(2 * (72 * 8 + 6), 2 * (77 * 8 - 6)
                                    - 1, HOOD_TOP), {m.ORANGE}))
    m.balcony(c, 90 * 8, 101 * 8 - 1, 80)
    surfaces.append(("pedestal", m.pedestal(c, PEDESTAL[0] * 8,
                                            PEDESTAL[1]), {m.ORANGE}))
    m.throne_wall(c, 104 * 8, 109 * 8 - 1, GATE_X)
    if not open_door:
        m.throne_doors(c, GATE_X)
    else:
        c.rect(GATE_X, 96, GATE_X + 15, v.GROUND_Y - 1, m.BLACK)
    for n, col in enumerate(CHANDELIERS, 1):
        surfaces.append((f"chandelier {n}",
                         m.chandelier(c, col * 8, 80), {m.ORANGE}))
    surfaces.append(("lantern", m.lantern(c, LANTERN[0] * 8, lit),
                     {m.BLACK, m.STONE}))
    # The throne room: the throne on its dais; the two pedestals.
    m.dais(c, 116 * 8, DAIS_TOP)
    m.throne(c, 116 * 8)
    for n, col in enumerate(ARENA_PEDESTALS, 2):
        top = m.pedestal(c, col * 8, PEDESTAL[1])
        surfaces.append((f"pedestal {n}", top, {m.ORANGE}))
    m.settle(c)
    m.dark(c)
    for bay, row in STARS:                  # in the windows' glass
        cell = (bay * 8 + 4 + (row % 2), row)
        if c.cell_colours(*cell) == {m.SKY}:
            c.hires[cell] = (v.STAR_PATTERNS["dot" if row % 3
                                             else "cross"], m.WHITE)
    street = {x: v.GROUND_Y for x in range(COLUMNS * 16)}
    surfaces.insert(0, ("street", street, {m.ORANGE}))
    return [(name, {x: y for x, y in line.items()
                    if 0 <= x < COLUMNS * 16}, colours)
            for name, line, colours in surfaces]
