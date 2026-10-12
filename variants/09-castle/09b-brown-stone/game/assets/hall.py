"""Inside Dreadcastle by torchlight: the pieces of level 8's picture
(drawn a third time).

Level 8, THE THRONE TOWER, has a set of characters of its own (as the
other levels from the wood on). The first two drawings were too
empty inside, then too striped; this one has
stone and torches, as outside: the stone of the walls
outside (keep.py), worked, with moss; tall arches and columns from the
floor to the vault; torches; the red banners of Tom's band. So:

  - every 32 pixels a column of stone rises from the floor to its
    capital (line 40), and from the capitals pointed arches of orange
    ribs meet under the vault: no band runs along the hall;
  - in each bay under its arch a tall lancet window, its glass the
    blue of the night (the moon shows through it, "Dietro le
    finestre", and the moths fly there); the vault over the arches in
    the dark;
  - the walls the rough blocks of outside, medium grey, their shadow
    the blue of the night, their joints black, the torches' light
    orange on them; moss at their foot;
  - torches on the columns, the banners of the band, the chandeliers,
    the armour, the chest, the great fireplace, the balcony, the door
    of the throne room.

The colours: a cell has the blue of the night (bits 00), medium grey
($d022 here: next_env sets it for this setting, the stone, as
outside), orange ($d023: the light of the torches and the fire, and
the wood) and one colour of its own (0-7): black (the joints, iron),
red (the banners), yellow (flames, gilt), green (moss). The moon is
behind orange and a cell's own colour, in front of blue and medium
grey: up on lines 0-23 (MOON_BAND) the hall shows the vault, black,
its ribs orange, and the glass of its windows.

Every piece sits on the grid of the cells; the stone repeats every 16
pixels and the bays every 32, so that their characters do: a set of
245 holds the level.
"""

import keep
import village as v

OPEN_SKY = v.OPEN_SKY
BLACK, WHITE, RED, CYAN, PURPLE, GREEN, BLUE, YELLOW = 0, 1, 2, 3, 4, 5, \
    6, 7
SKY = BLUE                              # $d021 here: the night
STONE = 9                               # $d022 here: brown
ORANGE = 8                              # $d023 here: the torches' light
SHARED = (SKY, STONE, ORANGE)           # $d021, $d022, $d023
GROUND_Y = v.GROUND_Y
MOON_BAND = 24                          # lines 0-23: the moon
CAPITALS = 40                           # the arches spring here
BAY = 32
flat = v.flat
PALETTE = {"b": SKY, "m": STONE, "o": ORANGE, "k": BLACK, "w": WHITE,
           "r": RED, "c": CYAN, "p": PURPLE, "g": GREEN, "y": YELLOW}


# --- tools -------------------------------------------------------------------
def put(c, x, y, letter, only_open=False):
    if 0 <= x < c.width and 0 <= y < c.height:
        if only_open and c.get(x, y) != OPEN_SKY:
            return
        c.plot(x, y, PALETTE[letter])


def paint(c, x0, y0, rows, only_open=False):
    for dy, row in enumerate(rows):
        for dx, letter in enumerate(row):
            if letter != ".":
                put(c, x0 + dx, y0 + dy, letter, only_open)


def fill(c, x0, y0, x1, y1, letter_at):
    for y in range(max(y0, 0), min(y1, c.height - 1) + 1):
        for x in range(max(x0, 0), min(x1, c.width - 1) + 1):
            letter = letter_at(x, y)
            if letter:
                put(c, x, y, letter)


def in_band(letter, y):
    """Up where the moon is, what stands there hides it: blue and
    medium grey become black (the dark of the vault)."""
    if y >= MOON_BAND:
        return letter
    return {"b": "k", "m": "k"}.get(letter, letter)


def settle(c, x0=0, x1=None):
    """Each cell keeps one colour of its own: where black meets another
    (a flame, a banner, moss), the black becomes medium grey (orange up
    where the moon is)."""
    x1 = c.width - 1 if x1 is None else x1
    for col in range(x0 // 4, x1 // 4 + 1):
        for row in range(c.height // 8):
            own = c.cell_colours(col, row) - set(SHARED) - {OPEN_SKY}
            if BLACK in own and len(own) > 1:
                to = "o" if row * 8 < MOON_BAND else "m"
                for y in range(row * 8, row * 8 + 8):
                    for x in range(col * 4, col * 4 + 4):
                        if c.get(x, y) == BLACK:
                            put(c, x, y, to)


def dark(c):
    """What is left open: the blue of the night (the windows' glass)."""
    for y in range(c.height):
        for x in range(c.width):
            if c.get(x, y) == OPEN_SKY:
                c.plot(x, y, SKY)


# --- the stone ---------------------------------------------------------------
def ashlar(x, y):
    """The stone of outside (keep.ashlar's blocks), inside: medium grey,
    its joints and its shadow under it black."""
    letter = keep.ashlar(x, y)
    fx, ly, width, _ = keep.block_at(x, y)
    if letter == "d":
        return "k" if ly == 6 and fx > 1 else "m"
    return letter


def wall(c, x0, x1, y0, y1):
    fill(c, x0, y0, x1, y1, lambda x, y: in_band(ashlar(x, y), y))


def glow(c, cx, cy, radius=10):
    """The light of a torch at (cx, cy) on the stone around it: the
    tops and left edges of the blocks orange."""
    for y in range(cy - radius * 2, cy + radius * 2 + 1):
        for x in range(cx - radius, cx + radius + 1):
            if ((x - cx) / radius) ** 2 + ((y - cy) / (2 * radius)) ** 2 \
                    > 1 or not (0 <= x < c.width and MOON_BAND <= y <
                                c.height):
                continue
            fx, ly, width, _ = keep.block_at(x, y)
            near = ((x - cx) / radius) ** 2 + ((y - cy) / (
                2 * radius)) ** 2 < 0.4
            if c.get(x, y) == STONE and (ly == 0 or fx == 0 or (
                    near and (x + y) % 2)):
                put(c, x, y, "o")


# --- the bays: columns, arches, windows --------------------------------------
def arch_line(bx):
    """The line of the intrados of a bay's pointed arch at pixel bx of
    the bay (8-31: between its columns), from the capitals (line
    CAPITALS) up to its point (line 4) in the middle."""
    d = abs(bx - 19.5)                  # 0.5 in the middle, 11.5 out
    return 4 + int(36 * (d / 12) ** 1.6)


def bay_letter(bx, y, window=True):
    """The letter of a bay at pixel bx (0-31) and line y, over the wall
    behind: None to leave the wall; the column (0-7), its capital, the
    arch's rib, the vault over it, the window's glass and frame."""
    if bx < 8:                                      # the column
        if y < CAPITALS - 8:
            return "k"                              # the vault
        if y < CAPITALS:                            # its capital
            dy = y - CAPITALS + 8
            if dy == 7:
                return "k"
            return "o" if dy == 0 or bx in (2, 3, 4, 5) else "m"
        if y >= GROUND_Y - 12:                      # its base
            if y == GROUND_Y - 12 or bx == 0:
                return "k"
            return "o" if y == GROUND_Y - 11 else "m"
        return "k" if bx in (0, 7) else ("o" if bx == 6 else "m")
    top = arch_line(bx)
    if y < top - 4:
        return "k"                                  # the vault
    if y < top:
        return "k" if y in (top - 4, top - 1) else "o"  # the rib
    if not window:
        return None
    if 16 <= bx <= 23 and y < 80:                   # the glass
        head = 12 + int(8 * (abs(bx - 19.5) / 4) ** 2)
        if y >= head:
            return "glass" if y < 76 else None
        if y >= head - 2:
            return "o"
        return None
    if bx in (15, 24) and 12 <= y < 76:
        return "k"
    if 13 <= bx <= 26 and 76 <= y < 80:
        return "o" if y == 76 else ("k" if y == 79 else "m")
    return None


def bays(c, x0, x1, windows=True):
    """The bays of the hall from pixel x0 to x1: the stone of the walls,
    the columns every 32 pixels, the arches, the vault, the windows."""
    wall(c, x0, x1, 0, GROUND_Y - 1)
    for y in range(GROUND_Y):
        for x in range(x0, x1 + 1):
            letter = bay_letter(x % BAY, y, windows)
            if letter == "glass":
                put(c, x, y, "b")               # the night, the moon
            elif letter:
                put(c, x, y, in_band(letter, y))


def moss(c, x0, x1):
    """Moss at the foot of the walls, in the joints."""
    for x in range(x0, x1 + 1):
        if x % BAY >= 8 and x % 16 in (1, 2, 5, 9, 10, 11):
            put(c, x, GROUND_Y - 1, "g")
        if x % BAY >= 8 and x % 16 in (2, 10):
            put(c, x, GROUND_Y - 2, "g")
    settle(c, x0, x1)


# --- torches and banners -----------------------------------------------------
TORCH = ["oyyo",
         "yyyo",
         "oyyy",
         "yyyo",
         "oyyo",
         "ooyo",
         "mkkm",
         "okkm",
         "okmm",
         "oomm",
         "omkm",
         "okkm",
         "oomm",
         "okmm",
         "omkm",
         "omkm"]


def torch(c, x0, y0):
    """A torch on the face of a column, its flame yellow on its orange
    light (16 lines from y0, on the grid)."""
    paint(c, x0, y0, TORCH)


# The banner of Tom's band, as outside: red, the wolf's head on it in
# the orange of the torchlight.
BANNER = [row.replace("d", "o") for row in keep.BANNER]


def banner(c, x0, y0):
    paint(c, x0, y0, BANNER)
    settle(c, x0, x0 + 11)


# --- the floor ---------------------------------------------------------------
def floor(c, x0, x1):
    """The floor: big flags lit orange on their edges, the blue of the
    shadow under them, the foundations dark."""
    for y in range(GROUND_Y, c.height):
        for x in range(x0, x1 + 1):
            dy, bx = y - GROUND_Y, x % 16
            if dy == 0:
                letter = "o"
            elif y == c.height - 1:
                letter = "k"
            elif dy < 8:
                letter = "k" if bx == 0 or dy in (6, 7) else "m"
            elif dy < 16:
                letter = "k" if (bx + 8) % 16 == 0 or dy in (14, 15) \
                    else "m"
            else:
                letter = "k" if y % 8 else ("m" if (
                    x + 8 * (y // 8 % 2)) % 16 in range(2, 14) else "k")
            put(c, x, y, letter)


# --- the furniture -----------------------------------------------------------
def chandelier(c, x0, y):
    """A chandelier two metatiles wide (pixels x0 to x0 + 15), its ring
    on line y, hung on its chain from the vault: candles lit, the
    ring's arms of iron."""
    for cy in range(CAPITALS - 8, y - 12):           # the chain
        put(c, x0 + 7, cy, "o" if cy % 4 < 2 else "k")
        put(c, x0 + 8, cy, "k" if cy % 4 < 2 else "o")
    rows = ["..y..y....y..y..",
            ".yy.yy...yy.yy..",
            ".yy.yy...yy.yy..",
            "..o..o....o..o..",
            "..o..o....o..o..",
            "..o..o....o..o..",
            "..k..k.kk.k..k..",
            "...kkkkkkkkkk...",
            "......kook......",
            "..o..o.oo.o..o..",
            "..o..o....o..o..",
            ".kkkkkkkkkkkkkkk",
            ".oooooooooooooo.",
            "kooooooooooooook",
            ".kkkkkkkkkkkkkk.",
            "....kkkkkkk.....",
            ".....kooook.....",
            "......kook......",
            ".......o........"]
    paint(c, x0, y - 12, rows)
    settle(c, x0, x0 + 15)
    return flat(2 * x0 + 2, 2 * x0 + 29, y)


def armour(c, x0, top):
    """A suit of armour on its plinth, two metatiles high (16 pixels,
    32 lines from `top`): steel, orange where the torches shine on it;
    the plinth of stone."""
    rows = ["....kkkkkkk.....",
            "...kmmmmmmkk....",
            "...kmkkkkkkk....",
            "...kmmmmmokk....",
            "..kkkmmmkkkkk...",
            ".kmmkkkkkkkmok..",
            ".kmkkmmmmkkkmkk.",
            ".kmkkmmmmokkmkk.",
            ".kmkkmmmkkkkkmkk",
            ".kkkkkkkkkkkkkk.",
            ".kkkmmmmkkkkkkk.",
            "...kmmkkmmkkk...",
            "...kmmkkmokkk...",
            "...kmkkkmkkkk...",
            "..kmmkkkmmkkkk..",
            "..kkkkkkkkkkkk..",
            "oooooooooooooooo",
            "kmmmmmmmmmmmmmok",
            "kmkkkkkkkkkkkmok",
            "kmkmmmmmmmmmkmok",
            "kmkmmmmmmmmmkmok",
            "kmkmmmmmmmmmkmok",
            "kmkkkkkkkkkkkmok",
            "kmmmmmmmmmmmmmok",
            "kkkkkkkkkkkkkkkk",
            "kmmmmmmmmmmmmmok",
            "kmmmmmmmmmmmmmok",
            "kmmmmmmmmmmmmmok",
            "kmmmmmmmmmmmmmok",
            "kkkkkkkkkkkkkkkk",
            "kmmmmmmmmmmmmmok",
            "kkkkkkkkkkkkkkkk"]
    paint(c, x0, top, rows)


def chest(c, x0, top):
    """A chest of wood, a metatile high, two wide: orange planks, iron
    bands."""
    rows = [".kkkkkkkkkkkkkk.",
            "kooooooooooooook",
            "kobbbbbbbbbbbbok",
            "kooooooooooooook",
            "kkkkkkkkkkkkkkkk",
            "kokkoooooooookok",
            "kokkoookkooookok",
            "kokkoookkooookok",
            "kokkoooooooookok",
            "kokkoooooooookok",
            "kbkkbbbbbbbbkkbk",
            "kokkoooooooookok",
            "kokkoooooooookok",
            "kokkoooooooookok",
            "kbbbbbbbbbbbbbbk",
            "kkkkkkkkkkkkkkkk"]
    paint(c, x0, top, rows)


def stool(c, x0, top):
    """A stool of wood, a metatile high, two wide."""
    rows = ["oooooooooooooooo",
            "kbbbbbbbbbbbbbbk",
            "kkkkkkkkkkkkkkkk",
            ".kok........kok.",
            ".kok........kok.",
            ".kok........kok.",
            ".kok........kok.",
            ".kokkkkkkkkkkok.",
            ".kok........kok.",
            ".kok........kok.",
            ".kok........kok.",
            ".kok........kok.",
            ".kok........kok.",
            ".kok........kok.",
            ".kbk........kbk.",
            ".kkk........kkk."]
    paint(c, x0, top, rows)


def pedestal(c, x0, top):
    """An empty pedestal of stone two metatiles wide, its top on line
    `top` (a surface Oscar stands on, or passes in front of)."""
    height = GROUND_Y - top
    for y in range(top, GROUND_Y):
        dy = y - top
        inset = 0 if dy < 6 or dy >= height - 6 else 2
        for x in range(x0 + inset, x0 + 16 - inset):
            dx = x - x0
            if dy == 0:
                letter = "o" if 1 <= dx <= 14 else "k"
            elif dy in (5, height - 7) or dx in (inset, 15 - inset):
                letter = "k"
            elif dx == 14 - inset:
                letter = "o"
            else:
                letter = "m"
            put(c, x, y, letter)
    return flat(2 * x0 + 2, 2 * x0 + 29, top)


def pier(c, x0, x1, foot):
    """A pier of the gallery: the wall, solid from the vault to line
    foot - 1, its edges dark; a lintel of wood over the passage."""
    wall(c, x0, x1, 0, foot - 1)
    for y in range(0, foot):
        put(c, x0, y, "k")
        put(c, x1, y, "k")
    for y in range(foot - 8, foot):
        for x in range(x0, x1 + 1):
            dy = y - foot + 8
            if dy in (0, 7) or x in (x0, x1):
                letter = "k"
            elif dy == 1:
                letter = "o"
            elif (x - x0) % 12 == 6:
                letter = "k"
            else:
                letter = "o" if dy in (2, 6) or (x - x0) % 3 else "k"
            put(c, x, y, letter)


def lantern(c, x0, lit):
    """The lantern of the checkpoint (its head on line 112): an iron
    post and a head; dark, or lit (yellow)."""
    c.rect(x0 + 3, 124, x0 + 4, GROUND_Y - 1, BLACK)
    c.rect(x0 + 2, 140, x0 + 5, GROUND_Y - 1, BLACK)
    c.rect(x0 + 2, 112, x0 + 5, 112, BLACK)
    c.rect(x0 + 1, 113, x0 + 6, 121, BLACK)
    c.rect(x0 + 2, 114, x0 + 5, 120, YELLOW if lit else STONE)
    c.rect(x0 + 1, 122, x0 + 6, 123, BLACK)
    if lit:
        settle(c, x0, x0 + 7)
    return flat(2 * x0 + 4, 2 * x0 + 11, 112)


SHIELD = ["..kkkkkkkkkkkk..",
          ".krrrrrrrrrrrrk.",
          ".krrorrrrrrorrk.",
          ".krroorrrroorrk.",
          ".krroooooooorrk.",
          ".kroooooooooork.",
          ".kroorooooroork.",
          ".kroooooooooork.",
          ".krroooooooorrk.",
          ".krrroommoorrrk.",
          "..krrroooorrrk..",
          "..krrrroorrrrk..",
          "...krrrrrrrrk...",
          "....krrrrrrk....",
          ".....krrrrk.....",
          "......kkkk......"]


def fireplace(c, x0, mantel, hood_top):
    """The great fireplace, five metatiles wide from pixel x0: its hood
    of stone from line `hood_top` (its top a surface: the hourglass
    there) down to the mantel (line `mantel`, a metatile high, solid),
    the wolf of the band on its shield; its jambs; the hearth under
    the mantel, glowing (the fire itself is the program's: FIRE)."""
    x1 = x0 + 39
    for y in range(hood_top, mantel):                   # the hood
        inset = 6 if y < mantel - 24 else 6 - (y - mantel + 24) // 4
        for x in range(x0 + inset, x1 - inset + 1):
            if y == hood_top:
                letter = "o"
            elif x == x0 + inset:
                letter = "k"
            elif x == x1 - inset:
                letter = "o"
            else:
                letter = ashlar(x, y)
            put(c, x, y, in_band(letter, y))
    paint(c, x0 + 12, 48, SHIELD)
    settle(c, x0 + 12, x0 + 27)
    for y in range(mantel, mantel + 16):                # the mantel
        for x in range(x0, x1 + 1):
            dy = y - mantel
            if dy == 0:
                letter = "o"
            elif dy == 15 or x in (x0, x1):
                letter = "k"
            elif dy in (1, 2):
                letter = "m"
            elif dy == 3:
                letter = "k"
            else:
                letter = "o" if (x - x0) % 8 == 4 and 6 <= dy <= 11 \
                    else "m"
            put(c, x, y, letter)
    for jx in (x0, x1 - 7):                             # the jambs
        for y in range(mantel + 16, GROUND_Y):
            for x in range(jx, jx + 8):
                dx = x - jx
                letter = "k" if dx in (0, 7) else (
                    "o" if dx == 6 else ashlar(x, y))
                put(c, x, y, letter)
    for y in range(mantel + 16, GROUND_Y):              # the hearth
        for x in range(x0 + 8, x1 - 7):
            dy = y - mantel - 16
            if y >= GROUND_Y - 16:
                letter = "b"                            # the fire's
            elif dy < 4:
                letter = "k"
            elif dy < 10:
                letter = "o" if (x + dy) % (4 if dy < 7 else 2) == 0 \
                    else "k"
            else:
                letter = "o"
            put(c, x, y, letter)


def balcony(c, x0, x1, top):
    """The balcony, pixels x0 to x1, its floor of wood on line `top`
    (solid, a metatile thick): an orange rail, a carved front, corbels
    of stone under it."""
    for y in range(top, top + 16):
        for x in range(x0, x1 + 1):
            dy, px = y - top, (x - x0) % 16
            if dy == 0:
                letter = "o"
            elif dy in (1, 15):
                letter = "k"
            elif dy == 2:
                letter = "k"
            elif px in (0, 15) or dy in (3, 14):
                letter = "k"
            elif px in (1, 14) or dy in (4, 13):
                letter = "o"
            else:
                letter = "k"
            put(c, x, y, letter)
    for x in range(x0 + 8, x1 - 7, 32):                 # the corbels
        for y in range(top + 16, top + 32):
            dy = y - top - 16
            for dx in range(8):
                if dx < dy // 2 - 1:
                    continue
                letter = "k" if dx == dy // 2 - 1 or dy == 15 else (
                    "o" if dx == 7 else "m")
                put(c, x + dx - 4, y, letter)


def throne_wall(c, x0, x1, door_x0):
    """The wall of the throne room (pixels x0 to x1), solid from the
    vault down to the floor right of its door; over the door a round
    arch of voussoirs (lines 72-95, the same shut and open)."""
    wall(c, x0, x1, 0, GROUND_Y - 1)
    for y in range(0, GROUND_Y):
        put(c, x0, y, "k")
        put(c, x1, y, "k")
    for y in range(72, 96):                             # the arch
        for x in range(door_x0 - 4, door_x0 + 20):
            dx, dy = x - door_x0 - 7.5, 96 - y - 0.5
            inner = (dx / 8) ** 2 + (dy / 16) ** 2
            outer = (dx / 12) ** 2 + (dy / 24) ** 2
            if inner < 1:
                letter = "k"
            elif outer < 1:
                letter = "k" if inner < 1.25 or outer > 0.82 else (
                    "o" if dx > 0 else "m")
            else:
                continue
            put(c, x, y, letter)


def throne_doors(c, door_x0):
    """The door of the throne room, shut (pixels door_x0 to door_x0 +
    15, lines 96-143): two leaves of wood, iron bands and studs."""
    rows = []
    for dy in range(48):
        if dy % 16 == 4:
            row = "kkkkkkkkkkkkkkkk"
        elif dy % 16 == 5:
            row = "kokokokokokokoko"
        else:
            row = "koooooomkooooook"
        rows.append(row)
    paint(c, door_x0, 96, rows)


def throne(c, x0):
    """The throne, empty, three metatiles wide from pixel x0, lines
    80-111 (on its dais): a tall back of red velvet in a gilt frame
    (orange), the seat, the arms."""
    rows = ["..........oo............",
            ".........oooo...........",
            "........oorroo..........",
            ".......oorrrroo.........",
            "......oorrrrrroo........",
            ".....oorrrrrrrroo.......",
            "....oorrrrrrrrrroo......",
            "....orrrrrrrrrrrro......",
            "....orrrroorrrrrro......",
            "....orrroooorrrrro......",
            "....orrrroorrrrrro......",
            "....orrrrrrrrrrrro......",
            "....orrrrrrrrrrrro......",
            "....orrrrrrrrrrrro......",
            "....orrrrrrrrrrrro......",
            "....orrrrrrrrrrrro......",
            "oooooorrrrrrrrrroooooo..",
            "orrrrorrrrrrrrrrorrrro..",
            "oooooorrrrrrrrrroooooo..",
            "..mo.orrrrrrrrrro.om....",
            "..mo.oooooooooooo.om....",
            "..mo.orrrrrrrrrro.om....",
            "..mooooooooooooooooom...",
            "..mobbbbbbbbbbbbbbbom...",
            "..mobbbbbbbbbbbbbbbom...",
            "..mooooooooooooooooom...",
            "..mom.............mom...",
            "..mom.............mom...",
            "..mom.............mom...",
            "..mom.............mom...",
            "..mom.............mom...",
            "..mmm.............mmm..."]
    paint(c, x0, 80, rows)


def dais(c, x0, top):
    """A dais of stone, two steps, under the throne."""
    for y in range(top, GROUND_Y):
        dy = y - top
        for x in range(x0 - 8, x0 + 32):
            if dy < 16 and not (x0 <= x < x0 + 24):
                continue
            letter = "o" if dy % 16 == 0 else (
                "k" if dy % 16 == 15 else "m")
            put(c, x, y, letter)


# --- the fire on the hearth (the program draws it: FLICKER) ------------------
# A metatile of fire on the hearth, two kinds, four pictures each: the
# flames yellow, a log under them; behind them the hearth glowing
# orange.
FIRE = {"A": [["........",
               "........",
               "...y....",
               "...y....",
               "..yo...y",
               "..yo..yo",
               ".yoo..yo",
               ".yoo.yoo",
               "yyooyyoo",
               "yoooyooo",
               "yoooooo.",
               ".ooooo..",
               "mmmmmmmm",
               "momymomy",
               "mmmmmmmm",
               "........"]],
        "B": [["........",
               "........",
               "......y.",
               ".....yo.",
               ".y...yo.",
               ".yo..yoo",
               "yyo.yyoo",
               "yoo.yooo",
               "yooyyooo",
               "yooyoooo",
               ".oooooo.",
               "..oooo..",
               "mmmmmmmm",
               "ommommom",
               "mmmmmmmm",
               "........"]]}
FIRE_KINDS = ("A", "B")
FIRE_FRAMES = 4


def fire_rows(kind, frame):
    """The picture `frame` of a metatile of fire: its flames shift a
    pixel up and down, their tips flicker; the hearth behind them
    glowing."""
    rows = [list(row.replace(".", "o")) for row in FIRE[kind][0]]
    shift = (0, 1, 0, 2)[frame]
    flames = [["o" if ch == "o" else ch for ch in row]
              for row in rows[:12]]
    flames = flames[shift:] + [["o"] * 8] * shift
    if frame % 2:
        flames = [row[1:] + row[:1] for row in flames]
    return ["".join(row) for row in flames + rows[12:]]
