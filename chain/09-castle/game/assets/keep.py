"""Dreadcastle from outside, under the moon: the pieces of level 7's
picture,
drawn a third time.

Level 7, DREADCASTLE GATE, has a set of characters of its own (as the
mountain's levels: one set for each level). The first two drawings
were grey and flat, too simple, the colours wrong; this one follows
the castle of the book's frontispiece and cover, and its sky is
night blue. So, as on
the cover:

  - the night is blue: the background of the playfield ($d021) is blue
    in the castle (the top interrupt sets it; the HUD stays black);
  - the stone is rough blocks of medium grey, dark grey in their
    shadow, black in their joints, moss at the foot of the walls;
    further back the stone is dark grey, its joints the blue of the
    night; in the dark (the postern, under the arches) black; far
    away the town is flat shapes;
  - violet clouds go by the moon; a dead tree stands black against
    the sky; across the moat, far away, the town on its hill, its
    windows lit, its clock;
  - red banners with the wolf's head of Tom's band; torches; lit
    windows; the keep's great gate, its portcullis down.

The colours: a cell has the blue of the night (bits 00), dark grey
($d022, bits 01), medium grey ($d023, bits 10: next_env sets it for
this setting) and one colour of its own, 0-7 (bits 11): black (the
joints, the outlines), green (moss), red (banners), yellow (windows,
flames), purple (clouds), white. Up where the moon is (lines 0-23,
MOON_BAND) what stands in front of the sky shows no blue and no dark
grey: the moon (a sprite behind the characters, moon.py) goes behind
medium grey and behind a cell's own colour (in_band).

A set holds 245 characters and 256 metatiles: every piece sits on the
grid of the cells (4 pixels by 8 lines), the stone repeats every 16
pixels and 16 lines, so pieces put at the same place in it share their
characters; the clouds, the stars, the windows and the spires sit on
the grid of the metatiles (8 pixels by 16 lines), so that alike they
share their metatiles too.
"""

import math

import village as v

OPEN_SKY = v.OPEN_SKY
BLACK, WHITE, RED, CYAN, PURPLE, GREEN, BLUE, YELLOW = 0, 1, 2, 3, 4, 5, \
    6, 7
SKY = BLUE                              # $d021 here: the night
GREY = 11                               # $d022: dark grey
STONE = 12                              # $d023 here: medium grey
SHARED = (SKY, GREY, STONE)             # $d021, $d022, $d023
GROUND_Y = v.GROUND_Y
flat = v.flat
PALETTE = {"b": SKY, "d": GREY, "m": STONE, "k": BLACK, "w": WHITE,
           "r": RED, "c": CYAN, "p": PURPLE, "g": GREEN, "y": YELLOW}
MOON_BAND = 24                  # lines 0-23: the moon (lines 2-22)


# --- tools -------------------------------------------------------------------
def put(c, x, y, letter, only_open=False):
    """A pixel of a letter of PALETTE; with only_open, only where
    nothing is drawn yet."""
    if 0 <= x < c.width and 0 <= y < c.height:
        if only_open and c.get(x, y) != OPEN_SKY:
            return
        c.plot(x, y, PALETTE[letter])


def paint(c, x0, y0, rows, only_open=False):
    """A drawing of letters; '.' leaves the canvas as it is."""
    for dy, row in enumerate(rows):
        for dx, letter in enumerate(row):
            if letter != ".":
                put(c, x0 + dx, y0 + dy, letter, only_open)


def fill(c, x0, y0, x1, y1, letter_at, only_open=False):
    """Pixels x0-x1, lines y0-y1: letter_at(x, y), or None to leave."""
    for y in range(max(y0, 0), min(y1, c.height - 1) + 1):
        for x in range(max(x0, 0), min(x1, c.width - 1) + 1):
            letter = letter_at(x, y)
            if letter:
                put(c, x, y, letter, only_open)


def in_band(letter, y):
    """A letter up where the moon is: what stands there hides it, so
    blue and dark grey become medium grey."""
    if y >= MOON_BAND:
        return letter
    return {"b": "m", "d": "m"}.get(letter, letter)


def settle(c, x0=0, x1=None):
    """Each cell keeps one colour of its own: where black meets another
    (moss, a flame, a banner), the black becomes dark grey (medium grey
    up where the moon is)."""
    x1 = c.width - 1 if x1 is None else x1
    for col in range(x0 // 4, x1 // 4 + 1):
        for row in range(c.height // 8):
            own = c.cell_colours(col, row) - set(SHARED) - {OPEN_SKY}
            if BLACK in own and len(own) > 1:
                to = "m" if row * 8 < MOON_BAND else "d"
                for y in range(row * 8, row * 8 + 8):
                    for x in range(col * 4, col * 4 + 4):
                        if c.get(x, y) == BLACK:
                            put(c, x, y, to)


def sky(c):
    """The open sky: the blue of the night."""
    for y in range(c.height):
        for x in range(c.width):
            if c.get(x, y) == OPEN_SKY:
                c.plot(x, y, SKY)


STAR_PATTERNS = v.STAR_PATTERNS


def stars(c, found):
    """Stars: (cell column, cell row, pattern), white hi-res cells of
    the open sky."""
    for col, row, pattern in found:
        if c.cell_colours(col, row) != {SKY}:
            raise ValueError(f"star at {col},{row} is not in clear sky")
        c.hires[(col, row)] = (STAR_PATTERNS[pattern], WHITE)


# --- the stone ---------------------------------------------------------------
# Rough blocks in courses of 8 lines (7 of stone, a joint), of uneven
# lengths; the pattern repeats every 16 pixels and two courses.
PERIOD = 16
JOINTS = ([0, 9], [4, 13])
SPECKS = [((2, 2), (3, 3)), ((-3, 2),), ((1, 4), (4, 1), (-2, 3)),
          ((2, 1),)]


def block_at(x, y):
    """(fx, ly, width of the face, which) of pixel (x, y): fx the pixel
    in the face of its block (-1: the joint), ly its line (7: the
    joint)."""
    course = (y // 8) % 2
    joints = JOINTS[course]
    px = x % PERIOD
    start = max((j for j in joints if j <= px), default=joints[-1] - PERIOD)
    after = [j for j in joints if j > start]
    end = after[0] if after else joints[0] + PERIOD
    which = (joints.index(start % PERIOD) if start >= 0 else
             len(joints) - 1) + len(joints) * course
    return px - start - 1, y % 8, end - start - 1, which


def ashlar(x, y, light="lit"):
    """The letter of the stone at pixel (x, y): "lit", near; "dim",
    further back (dark grey, the tops lit by the moon); "shade", in the
    dark (black, the tops dark grey)."""
    fx, ly, width, which = block_at(x, y)
    if ly == 7 or fx < 0:
        return "k"
    corner = (fx == 0 and ly == 0) or (fx == width - 1 and ly == 6)
    if corner:
        return "k"
    speck = any((sx if sx >= 0 else width + sx, sy) == (fx, ly)
                for sx, sy in SPECKS[which])
    if light == "shade":
        return shade(x, y)
    if light == "far":
        return far(x, y)
    if light == "dim":
        if ly == 0 and fx < width - 2:
            return "m"
        return "k" if speck or (fx == width - 1 and ly > 2) else "d"
    if ly == 6 or fx == width - 1:
        return "d"
    return "d" if speck else "m"


def shade(x, y):
    """Stone in the dark: black, the top of each course dark grey, a
    joint every 16 pixels."""
    if y % 8:
        return "k"
    return "k" if (x + 8 * ((y // 8) % 2)) % 16 == 0 else "d"


def far(x, y):
    """Stone further back, in the night: dark grey, its joints the blue
    of the night, a joint every 16 pixels."""
    if y % 8 == 7 or (x + 8 * ((y // 8) % 2)) % 16 == 0:
        return "b"
    return "d"


def small_block(x, y):
    """The small blocks of the arcade, 8 pixels by 8 lines: their
    pattern repeats every 8 pixels, so arches 8 pixels apart are
    alike."""
    bx, ly = (x + 4 * ((y // 8) % 2)) % 8, y % 8
    if ly == 7 or bx == 0:
        return "k"
    if ly == 6 or bx == 7:
        return "d"
    return "m"


def wall(c, x0, x1, y0, y1, light="lit", only_open=False):
    """Stone blocks from pixel x0 to x1, line y0 to y1."""
    fill(c, x0, y0, x1, y1,
         lambda x, y: in_band(ashlar(x, y, light), y), only_open)


MOSS = {"low": ["..g.......g.....",
                ".ggg.....ggg..g.",
                "gggg.g..gggggggg"]}


def moss(c, x0, y0, kind="low"):
    """Moss on the stone (the joints near the ground, the edges)."""
    paint(c, x0, y0, MOSS[kind])


# --- the ground --------------------------------------------------------------
def road(x, y):
    """Outside the walls: the old road, big paving stones seen from
    the side; earth under them."""
    dy = y - GROUND_Y
    if dy < 8:
        bx = x % 16
        if bx == 0:
            return "k"
        if dy == 0:
            return "m"
        if dy == 7:
            return "k"
        return "d" if bx == 15 or dy == 6 or (bx, dy) == (5, 3) else "m"
    if y == 175:
        return "k"
    return shade(x, y)


def pavement(x, y):
    """Inside the walls: the flags of the courtyard, their edges lit;
    under them the foundations going into the dark."""
    dy = y - GROUND_Y
    if dy < 8:
        bx = x % 16
        if dy == 0:
            return "m"
        if dy == 7:
            return "k"
        if bx == 0:
            return "k"
        if dy == 1:
            return "m"
        return "d" if bx == 15 or dy == 6 else "m"
    if y == 175:
        return "k"
    if dy < 16:
        return "k" if y % 8 == 7 or (x + 8) % 16 == 0 else "d"
    return shade(x, y)


def ground(c, x0, x1, kind="pavement"):
    """The ground from pixel x0 to x1: "pavement" or "road"."""
    letter_at = pavement if kind == "pavement" else road
    fill(c, x0, GROUND_Y, x1, c.height - 1, letter_at)


def grass(c, x0, x1):
    """Tufts of grass on the road's edge."""
    for x in range(x0, x1 + 1):
        if x % 16 in (1, 2, 3, 6, 7, 10, 11, 12, 13):
            put(c, x, GROUND_Y, "g")
        if x % 16 in (2, 11, 12):
            put(c, x, GROUND_Y + 1, "g")


# --- the moat ----------------------------------------------------------------
WATER_TOP = 152


def moat(c, x0, x1):
    """The moat from pixel x0 to x1: the far bank, in the dark; the
    black water, the blue of the sky in its ripples."""
    for y in range(GROUND_Y, c.height):
        for x in range(x0, x1 + 1):
            dy, px = (y - WATER_TOP) % 8, x % 16
            if y < WATER_TOP:
                letter = {GROUND_Y: "m", WATER_TOP - 1: "k"}.get(y, "d")
            elif y == c.height - 1:
                letter = "k"
            elif dy == 1 and px < 6:
                letter = "b"
            elif dy == 4 and 8 <= px < 13:
                letter = "b"
            elif dy == 6 and px in (3, 4):
                letter = "b"
            else:
                letter = "k"
            put(c, x, y, letter)
    for y in range(GROUND_Y, c.height - 1):          # the banks
        put(c, x0, y, "k")
        put(c, x1, y, "k")


# --- windows, slits, banners, torches ----------------------------------------
WINDOW = ["kkddddkk",
          "kddyyddk",
          "kdyyyydk",
          "dyyyyyyd",
          "dyyddyyd",
          "dyyddyyd",
          "dyyyyyyd",
          "dyyyyyyd",
          "dddddddd",
          "dyyddyyd",
          "dyyddyyd",
          "dyyyyyyd",
          "dyyyyyyd",
          "dyyddyyd",
          "dyyddyyd",
          "dyyyyyyd",
          "dyyyyyyd",
          "dddddddd",
          "dyyddyyd",
          "dyyyyyyd",
          "dyyyyyyd",
          "dddddddd",
          "mmmmmmmm",
          "dddddddd"]


def window(c, x0, y0):
    """A tall lit window, 8 pixels wide and 24 lines: its head round,
    a mullion and transoms of dark lead; its sill lit. It fills its
    cells, so its characters are the same on any wall."""
    paint(c, x0, y0, WINDOW)
    settle(c, x0, x0 + 7)


SLIT = ["kddk",
        "kbbk",
        "kbbk",
        "kbbk",
        "kbbk",
        "kbbk",
        "kbbk",
        "mmmm"]


def slit(c, x0, y0):
    """An arrow slit: the night through it."""
    paint(c, x0, y0, SLIT)


# The banner of Tom's band: red, the wolf's head dark on it, its eyes
# and its fangs; the pole across its top; 12 pixels wide, 40 lines,
# its foot cut in a swallow's tail.
BANNER = ["dmmmmmmmmmmd",
          "rrrrrrrrrrrr",
          "rrrrrrrrrrrr",
          "rrrrrrrrrrrr",
          "rrdrrrrrrdrr",
          "rrddrrrrddrr",
          "rrddddddddrr",
          "rddddddddddr",
          "rddrrddrrddr",
          "rddddddddddr",
          "rrddddddddrr",
          "rrrddddddrrr",
          "rrrddmmddrrr",
          "rrrrddddrrrr",
          "rrrrdmmdrrrr",
          "rrrrrddrrrrr",
          "rrrrrrrrrrrr",
          "rrrrrrrrrrrr",
          "rrrrrrrrrrrr",
          "rrrrrrrrrrrr",
          "rrrrrrrrrrrr",
          "rrrrrrrrrrrr",
          "rrrrrrrrrrrr",
          "rrrrrrrrrrrr",
          "rrrrrrrrrrrr",
          "rrrrrrrrrrrr",
          "rrrrrrrrrrrr",
          "rrrrrrrrrrrr",
          "rrrrrrrrrrrr",
          "rrrrrrrrrrrr",
          "rrrrrrrrrrrr",
          "rrrrrrrrrrrr",
          "rrrrrrrrrrrr",
          "rrrrrrrrrrrr",
          "rrrrr..rrrrr",
          "rrrr....rrrr",
          "rrr......rrr",
          "rr........rr",
          "r..........r",
          "............"]


def banner(c, x0, y0):
    paint(c, x0, y0, BANNER)
    settle(c, x0, x0 + 11)


# A torch in its iron bracket, on the soot it leaves on the wall: the
# tips of the flame red, the flame yellow (a cell each: one colour of
# their own), the cup and the bracket; three cells, the same on any
# wall (24 lines from y0, on the grid).
TORCH = ["drdd",
         "drdr",
         "rrdr",
         "rrrr",
         "drrr",
         "rrrd",
         "rrrr",
         "drrd",
         "dyyd",
         "yyyy",
         "yyyy",
         "yyyd",
         "dyyd",
         "dmmd",
         "ddmd",
         "ddmd",
         "kddk",
         "kdmk",
         "kkmk",
         "kkmk",
         "kmmk",
         "kkkk",
         "kddk",
         "kddk"]


def torch(c, x0, y0):
    paint(c, x0, y0, TORCH)


# --- the tops of the walls ---------------------------------------------------
# A merlon: a block 8 pixels by 8 lines, on the grid; in medium grey
# and black (it stands up where the moon is), or, further back, in dark
# grey and the blue of the night.
MERLON = {"lit": ["mmmmmmmk",
                  "mmmmmmmk",
                  "mmkmmmmk",
                  "mmmmmmmk",
                  "mmmmmmmk",
                  "mmmmkmmk",
                  "mmmmmmmk",
                  "kkkkkkkk"],
          "far": ["mmmmmmmb",
                  "dddddddb",
                  "dddddddb",
                  "dddddddb",
                  "dddddddb",
                  "dddddddb",
                  "dddddddb",
                  "bbbbbbbb"]}


def battlements(c, x0, x1, top, light="lit"):
    """Merlons every 16 pixels (on the stone's grid, wherever the wall
    starts), the night between them, from line top (8 lines); their
    characters are the same on every wall."""
    for x in range(x0, x1 + 1):
        if x % 16 < 8:
            for y in range(top, top + 8):
                put(c, x, y, MERLON[light][y - top][x % 8])


def machicolations(c, x0, x1, top):
    """Under the battlements, corbels every 8 pixels: the dark between
    them (16 lines from top)."""
    for x in range(x0, x1 + 1):
        bx = (x - x0) % 8
        for y in range(top, top + 8):
            dy = y - top
            if bx in (3, 4, 5, 6):
                letter = "k" if dy > 0 else "d"
            elif bx in (0, 2):
                letter = "d"
            else:
                letter = "m"
            put(c, x, y, in_band(letter, y))


# --- roofs -------------------------------------------------------------------
def slates(x, y, lit):
    """Slates of a roof: rows of 4 lines, joints shifted every row."""
    row = y // 4
    bx = (x + 2 * row) % 4
    if y % 4 == 3:
        return "k"
    if bx == 0:
        return "k" if y % 4 == 0 else "d"
    return ("m" if lit else "d") if y % 4 == 0 else "d"


def cone(c, cx, apex, base, only_open=False):
    """A spire of slates: its axis between pixels cx - 1 and cx (cx on
    the grid of the cells), from line apex (on the grid of the cell
    rows) down to line base; a pixel wider each side every 4 lines, so
    its edges repeat; the lit side on the right; its eaves dark; a
    spike on top."""
    for y in range(max(apex, 0), base + 1):
        half = 1 + (y - apex) // 4
        for x in range(cx - half, cx + half):
            if x == cx - half:
                letter = "k"
            elif x == cx + half - 1:
                letter = "m"
            else:
                letter = slates(x, y, x >= cx)
            if y >= base - 1:
                letter = "k" if y == base else "d"
            put(c, x, y, in_band(letter, y), only_open)
    for y in range(max(apex - 8, 0), apex):
        put(c, cx - 1, y, in_band("d", y), only_open)
        put(c, cx, y, in_band("m" if y > apex - 4 else "d", y),
            only_open)


def tower(c, x0, x1, top, bottom=GROUND_Y - 1, light="far"):
    """A tower or a building further back: its stone (in the night),
    its right edge lit by the moon, its left dark."""
    wall(c, x0, x1, top, bottom, light)
    for y in range(top, bottom + 1):
        put(c, x0, y, in_band("k", y))
        put(c, x1, y, in_band("m", y))
    for x in range(x0, x1 + 1):
        put(c, x, top, in_band("m", top))


def gable(c, x0, x1, top, bottom):
    """The roof of the great hall seen from its side: slates from line
    top to bottom, its ends sloping a pixel every 2 lines."""
    for y in range(top, bottom + 1):
        inset = (bottom - y) // 2
        for x in range(x0 + inset, x1 - inset + 1):
            if x == x0 + inset:
                letter = "k"
            elif x == x1 - inset:
                letter = "m"
            elif y == top:
                letter = "m"
            else:
                letter = slates(x, y, False)
            if y == bottom:
                letter = "k"
            put(c, x, y, in_band(letter, y))


# --- far away ----------------------------------------------------------------
# The town across the moat: houses and towers on its hill, flat dark
# shapes against the night, their windows lit; the clock tower. Roofs
# go a cell wider every cell row, so their edges repeat.
def house(c, x0, top, cells, windows=(), lit=False):
    """A house of the town: `cells` cells wide (4 pixels each), its
    wall from line top (on the grid) to 111, a pointed roof over it, a
    pixel narrower each side every 2 lines; windows at (cell, row of
    cells under top)."""
    x1 = x0 + 4 * cells - 1
    face = "m" if lit else "d"
    for y in range(top, 112):
        for x in range(x0, x1 + 1):
            put(c, x, y, face, only_open=True)
    k = 0
    while x0 + 4 * k <= x1 - 4 * k:
        for dy in range(8):
            y = top - 8 * k - 1 - dy
            inset = 4 * k + dy // 2
            for x in range(x0 + inset, x1 - inset + 1):
                put(c, x, y, face, only_open=True)
        k += 1
    for cell, row in windows:
        for y in range(top + 8 * row + 2, top + 8 * row + 6):
            for x in range(x0 + 4 * cell + 1, x0 + 4 * cell + 3):
                put(c, x, y, "y")


CLOCK = ["..dddd..",
         ".dyyyyd.",
         "dyykyyyd",
         "dyykyyyd",
         "dyykkkyd",
         "dyyyyyyd",
         ".dyyyyd.",
         "..dddd.."]


def town(c, x0):
    """The town far away on its hill, its windows lit, the clock tower
    with its yellow face (x0 to x0 + 95, lines 40-111)."""
    house(c, x0, 88, 3, windows=((1, 0),), lit=True)
    house(c, x0 + 12, 80, 4, windows=((1, 1), (2, 1)))
    house(c, x0 + 28, 48, 2, windows=((0, 3), (1, 5)), lit=True)
    paint(c, x0 + 28, 56, CLOCK)
    house(c, x0 + 36, 88, 4, windows=((1, 0), (2, 1)))
    house(c, x0 + 52, 72, 3, windows=((1, 1), (1, 3)), lit=True)
    house(c, x0 + 64, 96, 3, windows=((1, 0),))
    house(c, x0 + 76, 80, 4, windows=((2, 1),), lit=True)


def hill(c, x0, x1, top):
    """The town's hill, black, rising from the left a pixel every 2
    lines up to line top; its top edge dark grey."""
    for x in range(x0, x1 + 1):
        t = max(top, GROUND_Y - 1 - 2 * (x - x0))
        put(c, x, t, "d", only_open=True)
        for y in range(t + 1, GROUND_Y):
            put(c, x, y, "k", only_open=True)


def mountains(c, x0, x1, base, peaks):
    """Far mountains, black, their slopes lit dark grey on the right:
    peaks (x of the summit, line of the summit), a cell wider every
    4 lines down."""
    for x in range(x0, x1 + 1):
        top = base
        lit = False
        for px, py in peaks:
            t = py + 4 * (abs(x - px) // 2)
            if t < top:
                top, lit = t, x >= px
        for y in range(top, base + 1):
            letter = "d" if (y == top or (lit and y < top + 2)) else "k"
            put(c, x, y, letter, only_open=True)


# The dead tree, black against the night: a crown
# of bare branches (40 pixels by 24 lines), a trunk that twists down,
# a cell row at a time, to its roots on the road.
CROWN = [
    "k.......................k...............",
    ".k...........k.........k.........k......",
    ".k...k.......k........k.........k.......",
    "..k..k......k.........k........k....k...",
    "..kk..k.....k........k........kk...k....",
    "k..k..k....k.........k.......kk...k.....",
    ".k.kk..k...k........kk......kk...kk...k.",
    "..k.k..kk..k.......kk......kk...kk...k..",
    "..k..k..k.kk......kk......kk...kk...kk..",
    "...k.kk.kkk.......k......kk...kk...kk...",
    "...kk.kk.kk......kk.....kk...kk...kk....",
    "....k..kkkk.....kk.....kk...kkk..kk.....",
    "....kk..kkk....kk.....kk...kkkkkkk......",
    ".....kk.kkkk..kk.....kk...kkkk..........",
    "......kkkkkk.kk.....kkkkkkkk............",
    ".......kkkkkkk.....kkkkk................",
    "........kkkkkk...kkkk...................",
    ".........kkkkkkkkkk.....................",
    "..........kkkkkkk.......................",
    "..........kkkkkk........................",
    "..........kkkkk.........................",
    "...........kkkk.........................",
    "...........kkkk.........................",
    "..........kkkkk.........................",
]
TRUNK = ["..........kkkk..........",
         "..........kkkkk.........",
         "..........kkkkk.........",
         "...........kkkk.........",
         "...........kkkk.........",
         "..........kkkkk.........",
         "..........kkkk..........",
         "..........kkkk.........."]
ROOTS = [".........kkkkkk.........",
         "........kkkkkkkk........",
         ".......kk.kkk.kkk.......",
         "......kk..kkk...kk......"]


def tree(c, x0, y0):
    """The dead tree: its crown from y0 (on the grid), its trunk in
    cell rows down to its roots on the road (line 143)."""
    paint(c, x0, y0, CROWN)
    for y in range(y0 + len(CROWN), GROUND_Y - 4, 8):
        paint(c, x0, y, TRUNK)
    paint(c, x0, GROUND_Y - 4, ROOTS)


# --- clouds ------------------------------------------------------------------
# Violet clouds, lit by the moon on their tops, built of cells: each
# row of a cloud a rounded end, a body as long as wanted, a rounded
# end; the top row lit, the bottom row thinning.
CLOUD_CELLS = {
    "top": (["....", "....", "...m", "..mp", ".mpp", "mppp", "pppp",
             "pppp"],
            ["....", "....", "mmmm", "pppp", "pppp", "pppp", "pppp",
             "pppp"],
            ["....", "....", "m...", "pm..", "ppm.", "pppm", "pppp",
             "pppp"]),
    "mid": (["...p", "..pp", ".ppp", "pppp", "pppp", "pppp", ".ppp",
             "..pp"],
            ["pppp"] * 8,
            ["p...", "pp..", "ppp.", "pppp", "pppp", "pppp", "ppp.",
             "pp.."]),
    "bottom": (["..pp", "...p", "....", "....", "....", "....", "....",
                "...."],
               ["pppp", "pppp", "p.p.", "....", "....", "....", "....",
                "...."],
               ["pp..", "p...", "....", "....", "....", "....", "....",
                "...."]),
}


def cloud(c, x0, y0, rows):
    """A cloud from (x0, y0) on the grid: rows of cells (first cell,
    length) one under the other, the first lit, the last thinning."""
    for n, (first, length) in enumerate(rows):
        kind = "top" if n == 0 else (
            "bottom" if n == len(rows) - 1 else "mid")
        left, body, right = CLOUD_CELLS[kind]
        x, y = x0 + 4 * first, y0 + 8 * n
        paint(c, x, y, left, only_open=True)
        for k in range(1, length - 1):
            paint(c, x + 4 * k, y, body, only_open=True)
        paint(c, x + 4 * (length - 1), y, right, only_open=True)


# --- the postern ------------------------------------------------------
def tunnel(c, x0, x1):
    """The passage under the outer wall, lines 96-143: its vault and
    its walls in the dark, their tops dim; torches on them."""
    wall(c, x0, x1, 96, GROUND_Y - 1, "shade")
    for x in range(x0, x1 + 1):
        put(c, x, 96, "k")
        put(c, x, 97, "d" if x % 4 else "k")


def postern_mouth(c, x0):
    """The mouth of the postern: a round arch of big stones, 8 pixels
    deep, from line 96 down."""
    for y in range(96, GROUND_Y):
        for x in range(x0, x0 + 8):
            dx = x - x0
            if dx == 7:
                letter = "k"
            elif (y - 96) % 12 == 11:
                letter = "k"
            elif dx == 0:
                letter = "d"
            else:
                letter = "m" if dx < 5 else "d"
            put(c, x, y, letter)


def drawbridge(c, x0, top, bottom):
    """The drawbridge, raised in its recess: 32 pixels wide, planks of
    dark wood, iron bands, the chains to the wall."""
    for y in range(top - 8, top):
        for x in range(x0 - 4, x0 + 36):
            dx = x - x0 + 4
            put(c, x, y, "k" if (y - top + 8) > 2 and 3 < dx < 36 else
                in_band(ashlar(x, y), y))
    for y in range(top, bottom + 1):
        for x in range(x0, x0 + 32):
            dx, dy = x - x0, y - top
            if dx % 4 == 0:
                letter = "k"
            elif dy % 16 in (6, 7):
                letter = "m" if dx % 4 == 2 else "d"
            else:
                letter = "d"
            put(c, x, y, letter)
    for y in range(top - 8, top + 24):           # the chains
        for x in (x0 - 2, x0 + 33):
            put(c, x, y, "m" if y % 2 else "k")


# --- the courtyard -----------------------------------------------------------
# A barrel, 16 pixels by 16 lines: its staves, its hoops; two stacked
# are a solid block two metatiles high.
BARREL = ["kkkkkkkkkkkkkkkk",
          "kmmmmmmmmmmmmmmk",
          "kdkkkkkkkkkkkkdk",
          "kdmddmdddmddmddk",
          "kkkkkkkkkkkkkkkk",
          "kdmddmdddmddmddk",
          "kdmddmdddmddmddk",
          "kdmddmdddmddmddk",
          "kdmddmdddmddmddk",
          "kdmddmdddmddmddk",
          "kdmddmdddmddmddk",
          "kkkkkkkkkkkkkkkk",
          "kdmddmdddmddmddk",
          "kdmddmdddmddmddk",
          "kddddddddddddddk",
          "kkkkkkkkkkkkkkkk"]


def barrel(c, x0, top):
    """Two barrels, one on the other, two metatiles wide, from line
    top (on the grid) to the ground."""
    for y in range(top, GROUND_Y, 16):
        paint(c, x0, y, BARREL)


# A crate of planks, 8 pixels by 16 lines.
CRATE = ["kkkkkkkk",
         "kmmmmmmk",
         "kdkddkdk",
         "kddkkddk",
         "kdkddkdk",
         "kkddddkk",
         "kdkddkdk",
         "kddkkddk",
         "kdkddkdk",
         "kkddddkk",
         "kdkddkdk",
         "kddkkddk",
         "kdkddkdk",
         "kddddddk",
         "kddddddk",
         "kkkkkkkk"]


def cart(c, x0, top):
    """Four crates, two by two, two metatiles wide (where the cart was
    in the first drawing)."""
    for y in range(top, GROUND_Y, 16):
        for x in range(x0, x0 + 16, 8):
            paint(c, x, y, CRATE)


def turret(c, x0, x1, top):
    """The turret of the courtyard: a square tower of lit stone, its
    corners dark, a lit window; its top at line top."""
    wall(c, x0, x1, top, GROUND_Y - 1)
    for y in range(top, GROUND_Y):
        put(c, x0, y, "k")
        put(c, x1, y, "k")
        put(c, x1 - 1, y, "d")
    for x in range(x0, x1 + 1):
        put(c, x, top, "k")
        put(c, x, top + 1, "m")


def lantern(c, x0, lit):
    """The lantern of the checkpoint, as in the village (its head on
    line 112): an iron post and a head; dark, or lit (yellow)."""
    put_rect = c.rect
    put_rect(x0 + 3, 124, x0 + 4, GROUND_Y - 1, BLACK)
    put_rect(x0 + 2, 140, x0 + 5, GROUND_Y - 1, BLACK)
    put_rect(x0 + 2, 112, x0 + 5, 112, BLACK)
    put_rect(x0 + 1, 113, x0 + 6, 121, BLACK)
    put_rect(x0 + 2, 114, x0 + 5, 120, YELLOW if lit else GREY)
    put_rect(x0 + 1, 122, x0 + 6, 123, BLACK)
    return flat(2 * x0 + 4, 2 * x0 + 11, 112)


# --- the second wall ---------------------------------------------------------
def arch_top(x, left, right, spring, apex):
    """The line of a round arch's intrados at pixel x (or None)."""
    if not left <= x <= right:
        return None
    half = (right - left + 1) / 2
    centre = left + half - 0.5
    dx = abs(x - centre) / half
    rise = spring - apex
    return spring - int(rise * (1 - dx * dx) ** 0.5 + 0.5)


def wall_walk(c, x0, x1, deck, piers):
    """The wall walk on its arcade: a parapet with merlons, the deck
    (lines deck to deck + 15) of the walls' stone; under it the arcade
    of small blocks, round arches between the piers ((left, right)
    pixels), each ringed with voussoirs; the night under them (left
    open, for what is far away) down to a kerb (lines 141-143, as
    under the spikes)."""
    battlements(c, x0, x1, deck - 16)
    wall(c, x0, x1, deck - 8, deck + 15)
    for x in range(x0, x1 + 1):
        put(c, x, deck + 15, "k")
    left_end = min(p[0] for p in piers)
    right_end = max(p[1] for p in piers)
    fill(c, left_end, deck + 16, right_end, GROUND_Y - 1, small_block)
    for left, right in piers:
        for y in range(deck + 16, GROUND_Y):
            put(c, left, y, "k")
            put(c, right, y, "d")
    spans = [(a[1] + 1, b[0] - 1) for a, b in zip(piers, piers[1:])]
    for left, right in spans:
        for x in range(left, right + 1):
            top = arch_top(x, left, right, deck + 40, deck + 20)
            for y in range(top, GROUND_Y):
                put(c, x, y, shade(x, y))
            for y in range(top - 4, top):
                ring = "k" if y == top - 1 or (x - left) % 6 == 0 \
                    else "m"
                put(c, x, y, ring)


def pillar(c, x0, top):
    """A low pillar, 16 pixels, from line top to the ground."""
    wall(c, x0, x0 + 15, top, GROUND_Y - 1)
    for y in range(top, GROUND_Y):
        put(c, x0, y, "k")
        put(c, x0 + 15, y, "k")
    for x in range(x0, x0 + 16):
        put(c, x, top, "m")


def stair(c, x0):
    """The step (x0 - 8) and the two steps of the stair (x0, x0 + 8)."""
    for col, top in ((x0 - 8, 128), (x0, 96), (x0 + 8, 112)):
        wall(c, col, col + 7, top, GROUND_Y - 1)
        for x in range(col, col + 8):
            put(c, x, top, "m")
            put(c, x, top + 1, "m")
        for y in range(top, GROUND_Y):
            put(c, col + 7, y, "d")


# --- the keep ----------------------------------------------------------------
def keep_front(c, x0, x1, top=0):
    """The keep's front: lit stone from line top, its battlements."""
    wall(c, x0, x1, top + 8, GROUND_Y - 1)
    battlements(c, x0, x1, top)
    for y in range(top, GROUND_Y):
        put(c, x0, y, "k")


def castle_gate(c, x0):
    """The great gate of the keep, x0 to x0 + 31: its opening the
    door's two metatiles (x0 + 8 to x0 + 23, lines 96-143) under a
    round head (up to line 80), ringed with voussoirs, the keystone in
    the middle; the portcullis raised into the head."""
    cx = x0 + 16
    for y in range(72, 96):
        for x in range(x0 + 4, x0 + 28):
            dx, dy = x - cx + 0.5, 96 - y - 0.5
            inner = (dx / 8) ** 2 + (dy / 16) ** 2
            outer = (dx / 12) ** 2 + (dy / 24) ** 2
            if inner < 1:
                letter = portcullis(x, y, cx)
            elif outer < 1:
                angle = math.degrees(math.atan2(dy / 2, dx))
                if inner < 1.25 or outer > 0.82:
                    letter = "k"
                elif abs(angle - 90) < 9:
                    letter = "m" if abs(dx) < 1 else "k"
                elif abs(angle - 45) < 5 or abs(angle - 135) < 5:
                    letter = "k"
                else:
                    letter = "m" if dx > 0 else "d"
            else:
                continue
            put(c, x, y, letter)


def portcullis(x, y, cx):
    """The portcullis: iron bars, lit on their right, before the
    dark."""
    bx, by = (x - cx) % 4, y % 8
    if by == 4:
        return "d"
    if bx == 1:
        return "d"
    if bx == 2:
        return "m"
    return "k"


def gate_doors(c, x0):
    """The gate shut: the portcullis down to the ground (lines 96-143,
    the door's metatiles: x0 + 8 to x0 + 23), its spikes in the
    ground."""
    for y in range(96, GROUND_Y):
        for x in range(x0 + 8, x0 + 24):
            put(c, x, y, portcullis(x, y, x0 + 16))


def doorway(c, x0):
    """The gate open: the portcullis up in the head, its spikes over
    the dark passage."""
    for y in range(96, GROUND_Y):
        for x in range(x0 + 8, x0 + 24):
            bx = (x - x0 - 16) % 4
            letter = "k"
            if y < 100 and bx in (1, 2) and (y - 96) < 4 - (bx == 2):
                letter = "d" if bx == 1 else "m"
            put(c, x, y, letter)


# --- the spikes (the program draws them: FLICKER) ----------------------------
# Iron spikes standing in a row under the arches, before the dark wall
# (shade: their characters' own colour is black); the program changes
# their pictures: a glint runs up their edges, the moon's.
SPIKE = {"A": ["...d....",
               "..dmd...",
               "..dmd...",
               ".ddmd..d",
               ".ddmd.dm",
               ".ddmd.dm",
               "dddmdddm",
               "dddmdddm",
               "dddmdddm",
               "dddmdddm",
               "dddmdddm",
               "dddmdddm",
               "dddmdddm",
               "mmmmmmmm",
               "dddddddd",
               "kkkkkkkk"],
         "B": ["......d.",
               ".d...dmd",
               "dmd..dmd",
               "dmd.ddmd",
               "dmd.ddmd",
               "ddmdddmd",
               "ddmdddmd",
               "ddmddddm",
               "ddmddddm",
               "ddmddddm",
               "dddmdddm",
               "dddmdddm",
               "dddmdddm",
               "mmmmmmmm",
               "dddddddd",
               "kkkkkkkk"]}
SPIKE_KINDS = ("A", "B")
SPIKE_FRAMES = 4
SPIKE_COLOUR = BLACK


def spike_rows(kind, frame, x=None):
    """The picture `frame` of a metatile of spikes before the dark wall
    (its stone, shade(), behind them: kind A on a metatile 16 pixels
    from the wall's joints, B 8 from them): their edges dark grey, the
    glint medium grey, three lines high, from the foot (frame 0) up to
    the tips (frame 3)."""
    band = (9, 6, 3, 1)[frame]
    x0 = 0 if kind == "A" else 8
    rows = []
    for y, row in enumerate(SPIKE[kind]):
        line = []
        for dx, letter in enumerate(row):
            if letter == ".":
                letter = shade(x0 + dx, 128 + y)
            elif letter == "m" and y < 13 and not band <= y < band + 3:
                letter = "d"
            line.append(letter)
        rows.append("".join(line))
    return rows
