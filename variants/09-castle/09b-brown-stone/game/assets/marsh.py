"""The black mire under the moon: the pieces of its picture.

Level 4, THE BLACK MIRE, has a set of characters of its own (the
forest's is full with the wood). Its look, mist and black water:
the moonlit night of the wood
over a mire: the moon still in the sky up on the right (a sprite,
moon.py); black water with the glints of the moon; clods of peat;
dead trees, grey and bare; walkways of planks; a low greenish mist on
the water. And the will-o'-the-wisps, still and flickering: flames
that stay where they are and flicker (their characters change while
the level is played: WISP_FRAMES).

The same canvas and the same shared colours as the village and the
wood (village.py): a cell has the black background, dark grey
($d022), brown ($d023) and one colour of its own (0-7). Dead wood is
dark grey and brown, lit white by the moon on its right side (the
moon is up on the right); the mist is green, the wisps cyan.

The pieces repeat on the grid of the cells and of the metatiles, so
that a set holds the level: the water, the mist, the peat and the
planks repeat every 8, 16 or 32 pixels; the clods, the stumps and
the reeds are one drawing each, put on the grid of the metatiles.
"""

import math

import village as v

BACKGROUND, OPEN_SKY = v.BACKGROUND, v.OPEN_SKY
GREY, WOOD, SKY = v.SHARED_1, v.SHARED_2, v.BACKGROUND
GREEN, CYAN, WHITE, YELLOW = v.GREEN, v.CYAN, v.WHITE, v.YELLOW
GROUND_Y = v.GROUND_Y
flat = v.flat
PALETTE = {"k": SKY, "d": GREY, "b": WOOD, "g": GREEN, "c": CYAN,
           "w": WHITE, "y": YELLOW}
LX, LY = 0.55, -0.83                # the moon: up and to the right
WATER_TOP = 148                     # the line of the water


def own(c, x, y):
    """The colour of its own of the cell of pixel (x, y), or None."""
    return v.own_colour_in(c, x // 4, y // 8)


def put(c, x, y, colour):
    """A pixel of a colour of its own, where its cell has no other:
    else dark grey."""
    if colour not in (SKY, GREY, WOOD):
        here = own(c, x, y)
        if here is not None and here != colour:
            colour = GREY
    c.plot(x, y, colour)


def sky(c):
    """The open sky: black."""
    for y in range(c.height):
        for x in range(c.width):
            if c.get(x, y) == OPEN_SKY:
                c.plot(x, y, BACKGROUND)


# --- the ground: peat --------------------------------------------------
# The peat of the path, a metatile (8 x 16 pixels) repeating: a wet
# dark edge, then layers of brown and black, roots of dark grey.
PEAT = ["dbdddbdd",
        "bbdbbbbd",
        "bbbbbbkb",
        "bdbbbbbb",
        "bbbbkbbb",
        "kbbbbbbd",
        "bbbdbbbb",
        "bbbbbbkb",
        "bkbbbbbb",
        "bbbbbdbb",
        "dbbbbbbb",
        "bbbkbbbb",
        "bbbbbbdk",
        "bdbbbbbb",
        "bbbbkbbb",
        "kbbbbbbb"]


def peat(c, x0, x1, top=GROUND_Y, bottom=None):
    """Peat from pixel x0 to x1, from line `top` to `bottom` (the
    playfield's last line but one), the pattern on the grid of the
    metatiles."""
    bottom = c.height - 2 if bottom is None else bottom
    for y in range(top, bottom + 1):
        row = PEAT[(y - GROUND_Y) % 16]
        for x in range(x0, x1 + 1):
            c.plot(x, y, PALETTE[row[x % 8]])
    c.hline(x0, x1, c.height - 1, SKY)


def ground(c, gaps):
    """The path: peat everywhere but in the gaps (pixel x0, x1)."""
    c.rect(0, GROUND_Y, c.width - 1, c.height - 1, SKY)
    x = 0
    for a, b in sorted(gaps) + [(c.width, c.width)]:
        if a > x:
            peat(c, x, a - 1)
        x = b + 1


# Tufts of grass on the peat, 16 pixels repeating: (x, height).
TUFTS = [(1, 3), (2, 2), (9, 2), (10, 4), (11, 2)]


def tufts(c, x0, x1, base=GROUND_Y):
    """Tufts of grass over the edge of the peat (line `base`), from
    pixel x0 to x1, in the cells with nothing else in them."""
    for x in range(x0, x1 + 1):
        for dx, h in TUFTS:
            if x % 16 != dx:
                continue
            for i in range(1, h + 1):
                y = base - i
                if c.get(x, y) in (OPEN_SKY, SKY) and own(c, x, y) in (
                        None, GREEN):
                    c.plot(x, y, GREEN)


# --- the water, the mist ----------------------------------------------
# The glints of the moon on the black water, 16 pixels repeating: the
# lines from WATER_TOP down (the last line of the playfield black).
GLINTS = [".dd...ddd...d.dd",
          "................",
          "...........dd...",
          "..ww............",
          ".........www....",
          "................",
          "....ddd.........",
          "............w...",
          ".www............",
          "................",
          ".......dd.......",
          "...........ww...",
          "................",
          "..d.............",
          ".......w........",
          "................",
          "............d...",
          "...dd...........",
          "................",
          "........d.......",
          "..............w.",
          "................",
          "....d.........d.",
          "................",
          ".........d......",
          "................",
          "................",
          "................"]


def water(c, x0, x1):
    """Black water from pixel x0 to x1, from the path's line down: its
    line at WATER_TOP (ripples of dark grey), the glints of the moon
    under it, white, fewer and dark grey deeper down."""
    c.rect(x0, GROUND_Y, x1, c.height - 1, SKY)
    for y in range(WATER_TOP, c.height - 1):
        row = GLINTS[y - WATER_TOP]
        for x in range(x0, x1 + 1):
            if row[x % 16] != ".":
                c.plot(x, y, PALETTE[row[x % 16]])


# The mist: 16 pixels repeating, from line MIST_TOP to the water;
# thin streaks high up, thicker down to the water.
MIST_TOP = 130
MIST = ["................",
        "..........g.....",
        "................",
        "...g............",
        "................",
        "................",
        ".........gg.....",
        "................",
        "..gg............",
        "................",
        "...........gg...",
        "....g...........",
        "................",
        "gg.......g......",
        "..........gg....",
        "....gg..........",
        ".............gg.",
        "g.....gg........"]


def mist(c, x0, x1):
    """A low mist from pixel x0 to x1, over the water: green streaks
    (16 pixels repeating), in the black only: what stands in it stays
    in front."""
    for y, row in enumerate(MIST, MIST_TOP):
        for x in range(x0, x1 + 1):
            if row[x % 16] == "g" and c.get(x, y) in (OPEN_SKY, SKY):
                put(c, x, y, GREEN)


# --- clods of peat in the water ------------------------------------------
# A clod: grass on it, its top on the path's line (the sixth row of
# the drawing), its sides in the water.
CLOD_8 = ["...g....",
          ".g.g.g..",
          ".gg.gg.g",
          "g.ggg.gg",
          "gggbggg.",
          "dbdbbdbd",
          "kbbkbbdk",
          "kbdbbkbk",
          ".kbbbbk.",
          "..kkkk..",
          "..d..d.."]

def clod(c, x0, width):
    """A clod of peat in the water, `width` pixels (8, or 16: two
    tussocks; x0 a multiple of 8), its top on the path's line, grass
    on it."""
    for x in range(x0, x0 + width, 8):
        c.blit(x, GROUND_Y - 5, CLOD_8, PALETTE)
    return flat(2 * x0, 2 * (x0 + width) - 1, GROUND_Y)


def shore(c, x, inward):
    """The edge of the peat at pixel x where the water starts, rounded
    into the water; inward: -1 for the peat on the left of the water,
    1 for the peat on its right."""
    for i, top in enumerate((GROUND_Y + 1, GROUND_Y + 3, GROUND_Y + 6)):
        px = x + inward * i
        for y in range(top, c.height - 1):
            c.plot(px, y, SKY)
        c.plot(px, top - 1, GREY)


# --- reeds -------------------------------------------------------------
# A clump of reeds: stems (x at the foot, lean, height, a cattail?).
REEDS = [(1, 1, 26, True), (3, -1, 20, False), (4, 1, 30, True),
         (6, 2, 18, False), (2, -2, 14, False)]


def reeds(c, x0, base=GROUND_Y - 1):
    """A clump of reeds standing at pixel x0 (a multiple of 4), from
    line `base` up: green stems, brown cattails; behind what is
    drawn."""
    for fx, lean, height, cattail in REEDS:
        for i in range(height):
            y = base - i
            x = x0 + fx + (lean * i * i) // (height * height)
            if c.get(x, y) == OPEN_SKY:
                put(c, x, y, GREEN)
        if cattail:
            x = x0 + fx + lean
            for i in range(height - 9, height - 3):
                y = base - i
                if c.get(x, y) in (OPEN_SKY, GREEN):
                    c.plot(x, y, WOOD)
                if i in (height - 8, height - 6) and \
                        c.get(x + 1, y) == OPEN_SKY:
                    c.plot(x + 1, y, GREY)


# --- dead wood ---------------------------------------------------------
def fissure(x, y):
    """Whether pixel x is in one of the long cracks of dead wood at
    line y: two cracks every 8 pixels that step a pixel and break, 16
    lines repeating."""
    x, y = x % 8, y % 16
    if x == (1 if 4 <= y < 11 else 2) and y != 13:
        return True
    return x == (5 if 2 <= y < 9 else 6) and y not in (14, 15)


def dead_bark(x, y, x0, x1):
    """Dead wood of a round trunk from x0 to x1, lit by the moon from
    the right: white on its edge, then brown; dark grey; on its left
    the shade; long black cracks. Away from its edges it depends only
    on x and y, so trunks of other widths share their characters."""
    w = x1 - x0 + 1
    left, right = x - x0, x1 - x
    y %= 16                                     # 16 lines repeating
    if left <= 0 or right <= 0:
        return SKY
    if w <= 8:                                  # a thin one
        if right == 1:
            return WHITE if y % 8 else GREY
        if right == 2 and w > 4:
            return WOOD if (y // 4) % 2 else GREY
        return SKY if left == 1 and y % 8 < 3 else GREY
    crack = fissure(x, y)
    if right == 1:
        return WHITE
    if right == 2:
        return WHITE if y in (3, 4, 11) else WOOD
    if right <= 4:
        return GREY if crack else (WOOD if (y + 3 * x) % 7 else GREY)
    if left == 1:
        return SKY if y in (2, 3, 9) else GREY
    return SKY if crack else GREY


def trunk(c, x0, x1, y0, y1):
    """A dead trunk from x0 to x1, lines y0 to y1."""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            put(c, x, y, dead_bark(x, y, x0, x1))


def roots(c, x0, x1, bottom=GROUND_Y - 1, rows=6, spread=3):
    """Roots at the foot of a dead trunk (x0 to x1): its last `rows`
    lines spread `spread` pixels each side, dark between the roots."""
    for i in range(rows):
        y = bottom - rows + 1 + i
        s = (i * spread + rows // 2) // (rows - 1)
        a, b = x0 - s, x1 + s
        for x in range(a, b + 1):
            put(c, x, y, dead_bark(x - a + x0, y, x0, x0 + (b - a)))
        if i >= rows - 3:
            third = (x1 - x0) // 3
            for gx in (x0 + 1, x0 + third, x1 - third, x1 - 1):
                if i >= rows - 2 or gx in (x0 + 1, x1 - 1):
                    c.plot(gx, y, SKY)
    c.hline(x0 - spread, x1 + spread, bottom, SKY)


# The broken top of a dead trunk: how far each of its columns rises
# over the line it stands on (20 columns).
SPLINTERS = [1, 3, 6, 9, 12, 11, 7, 4, 2, 1, 1, 2, 4, 7, 10, 8, 5, 3, 2, 1]


def dead_stump(c, x0, top=112):
    """A broken dead trunk on 3 metatiles (x0 a multiple of 8), solid
    from line `top` to the path: 20 pixels wide, its roots spreading
    to 24; splintered over its top, the hollow inside it dark."""
    a, b = x0 + 2, x0 + 21
    trunk(c, a, b, top, GROUND_Y - 1)
    roots(c, a, b, spread=2)
    for i, rise in enumerate(SPLINTERS):
        x = a + i
        for y in range(top - rise, top):
            put(c, x, y, dead_bark(x, y + 16, a, b))
        c.plot(x, top - rise - 1, SKY)
        if 0 < i < 19 and SPLINTERS[i + 1] < rise:      # lit edge
            put(c, x, top - rise, WHITE)
    for i in range(3, 17):                      # the hollow inside
        if SPLINTERS[i] <= 3:
            c.plot(a + i, top - SPLINTERS[i], SKY)
            c.plot(a + i, top + 1 - SPLINTERS[i], WOOD)


def fallen_log(c, x0, top=112):
    """A dead log fallen at the foot of the great tree, on 3 metatiles
    (x0 a multiple of 8), from line `top` to the path: its bark lying
    (8 pixels repeating), lit from above; its broken end on the right
    showing its rings."""
    bottom = GROUND_Y - 1
    end = x0 + 16
    for y in range(top, bottom + 1):
        for x in range(x0, end):
            put(c, x, y, lying_bark(x, y, top, bottom))
    c.vline(x0, top, bottom, SKY)
    cx, cy = end + 3.5, (top + bottom + 1) / 2
    for y in range(top, bottom + 1):            # its broken end
        for x in range(end - 2, x0 + 24):
            u, w = (x + 0.5 - cx) / 4.2, (y + 0.5 - cy) / 16.5
            d = (u * u + w * w) ** 0.5
            if d > 1:
                continue
            ring = int(d * 5) % 2
            colour = SKY if d > 0.88 else (WOOD if ring else GREY)
            if d <= 0.88 and u > 0.3 and w < 0.2:
                colour = WHITE if ring else WOOD
            put(c, x, y, colour)


def limb(c, x, y, angle, length, thick, depth, turns):
    """A bare bough from (x, y), x in screen pixels (half pixels of
    the canvas), at `angle` degrees from up (positive: to the right),
    `length` lines long, `thick` at its start, thinner to its end,
    bending by `turns`; `depth` times it forks in two. Dark grey, the
    moon white on its top, black under it."""
    points = []
    a = angle
    for k in range(int(length)):
        a += turns[(depth * 7 + k) % len(turns)] * 2.5
        x += math.sin(math.radians(a))
        y -= math.cos(math.radians(a))
        points.append((x, y, max(1.0, thick * (1 - 0.55 * k / length))))
    for px, py, th in points:
        mx, my = int(px // 2), int(round(py))
        for dy in range(-int(th / 2), int(th / 2) + 1):
            for dx in (0,) if th < 2.5 else (-1, 0):
                if c.get(mx + dx, my + dy) == OPEN_SKY:
                    put(c, mx + dx, my + dy, GREY)
    for px, py, th in points:
        mx, my = int(px // 2), int(round(py))
        top = my - int(th / 2) - 1
        if c.get(mx, top) == OPEN_SKY:
            put(c, mx, top, WHITE if th > 1.6 else GREY)
        bottom = my + int(th / 2) + 1
        if c.get(mx, bottom) == OPEN_SKY:
            c.plot(mx, bottom, SKY)
    if depth > 0:
        ex, ey, th = points[-1]
        spread = 26 + 6 * depth
        limb(c, ex, ey, a - spread, length * 0.62, th, depth - 1, turns)
        limb(c, ex, ey, a + spread * 0.8, length * 0.55, th, depth - 1,
             turns[3:] + turns[:3])


TURNS = [0.3, -0.5, 0.8, -0.2, 0.1, -0.9, 0.6, 0.0, -0.4, 0.7, -0.6, 0.2]


def snag(c, x0, top, width, limbs, foot=GROUND_Y - 1, thin=None,
         flare=2):
    """A dead tree standing behind the path: its trunk `width` pixels
    from x0 at its foot, `thin` at its broken top (line `top`), down
    to line `foot`: straight on its right, thinner on its left a pixel
    every 16 lines; its roots spreading `flare` pixels each side; its
    limbs (x in pixels, line, angle, length, thickness, forks)."""
    thin = width if thin is None else thin
    x1 = x0 + width - 1
    for n, (lx, ly, angle, length, thick, forks) in enumerate(limbs):
        limb(c, 2 * lx + 1, ly, angle, length, thick, forks,
             TURNS[n * 5 % 12:] + TURNS[:n * 5 % 12])
    for y in range(top, foot + 1):
        w = max(thin, min(width, thin + 2 * ((y - top) // 16)))
        a = x1 - w + 1
        for x in range(a, x1 + 1):
            put(c, x, y, dead_bark(x, y, a, x1))
    roots(c, x0, x1, bottom=foot, rows=5, spread=flare)
    a = x1 - thin + 1
    for i in range(3):                          # its broken top
        for x in range(a + 1 + i, x1 - i):
            if (x - a + i) % 3 != 2:
                put(c, x, top - 1 - i, dead_bark(x, top - 1 - i, a, x1))


# --- planks ------------------------------------------------------------
def planks(c, x0, x1, y):
    """Planks from pixel x0 to x1 on line y, 6 lines: brown, the grain
    dark grey, their ends black every 8 pixels, a beam dark under."""
    rows = ((WOOD, WOOD), (WOOD, GREY), (WOOD, WOOD), (GREY, SKY),
            (GREY, GREY), (SKY, SKY))
    for x in range(x0, x1 + 1):
        for dy, (colour, grain) in enumerate(rows):
            if x % 8 == 7 and dy in (1, 2):
                colour = SKY
            elif x % 8 in (2, 3, 5) and dy in (1, 3):
                colour = grain
            c.plot(x, y + dy, colour)
    c.vline(x0, y + 1, y + 4, SKY)
    c.vline(x1, y + 1, y + 4, SKY)


def post(c, x, y0, y1):
    """A post of the walkways, 2 pixels wide, lines y0 to y1: brown on
    the side of the moon, dark grey on the other, black rings."""
    for y in range(y0, y1 + 1):
        ring = y % 12 == 5
        c.plot(x, y, SKY if ring else GREY)
        c.plot(x + 1, y, SKY if ring else WOOD)


# --- the will-o'-the-wisps ----------------------------------------------
# A wisp: a flame on the ground, cyan, a halo of dark grey: one
# metatile (8 x 16 pixels), four pictures that follow one another as
# it flickers. Two kinds, A and B, in turn along the ground.
WISPS = {
    "A": [["........",
           "........",
           "........",
           "....d...",
           "...dcd..",
           "...dc...",
           "..dccd..",
           "..dccd..",
           ".dcccd..",
           ".dccccd.",
           ".dcccd..",
           "..dccd..",
           "..dcd...",
           "...d....",
           "........",
           "........"],
          ["........",
           "........",
           "...d....",
           "..dcd...",
           "..dc....",
           "..dccd..",
           "...ccd..",
           "..dcccd.",
           ".dccccd.",
           ".dcccd..",
           ".dccccd.",
           "..dccd..",
           "...cd...",
           "...d....",
           "........",
           "........"],
          ["........",
           "........",
           "........",
           "........",
           ".....d..",
           "....dc..",
           "...dcd..",
           "..dccd..",
           "..dcccd.",
           ".dccccd.",
           ".dcccd..",
           "..dccd..",
           "..dcd...",
           "...d....",
           "........",
           "........"],
          ["........",
           "....d...",
           "....c...",
           "...dcd..",
           "...dc...",
           "..dccd..",
           "..dcc...",
           ".dcccd..",
           ".dccccd.",
           ".dccccd.",
           "..dcccd.",
           "..dccd..",
           "...cd...",
           "...d....",
           "........",
           "........"]],
    "B": [["........",
           "........",
           "........",
           "........",
           "........",
           "...d....",
           "..dcd...",
           "..dc....",
           ".dccd...",
           ".dcccd..",
           ".dccd...",
           "..dcd...",
           "...d....",
           "........",
           "........",
           "........"],
          ["........",
           "........",
           "........",
           "........",
           "..d.....",
           "..cd....",
           "..dcd...",
           ".dccd...",
           ".dcccd..",
           ".dcccd..",
           "..dccd..",
           "..dcd...",
           "...d....",
           "........",
           "........",
           "........"],
          ["........",
           "........",
           "........",
           "...d....",
           "..dcd...",
           "..dcd...",
           "..dc....",
           ".dccd...",
           ".dcccd..",
           ".dccd...",
           ".dcccd..",
           "..dcd...",
           "...d....",
           "........",
           "........",
           "........"],
          ["........",
           "........",
           "........",
           "........",
           "........",
           "........",
           "...d....",
           "..dcd...",
           ".dccd...",
           ".dcccd..",
           ".dccd...",
           "..dcd...",
           "...d....",
           "........",
           "........",
           "........"]]}
WISP_KINDS = ("A", "B")
WISP_FRAMES = 4


def wisp(c, x0, kind, frame=0):
    """A wisp's picture `frame` in the metatile at pixel x0, row 8
    (lines 128-143)."""
    c.blit(x0, 128, WISPS[kind][frame], PALETTE)


# --- the bank, the boulder, the root, the way out ----------------------
def bank(c, x0, x1, top=128):
    """The bank of peat, a long step from pixel x0 to x1 (whole
    metatiles), its top on line `top`: the peat of the path, a lip of
    grass over its edge, its ends rounded."""
    peat(c, x0, x1, top, GROUND_Y - 1)
    for x in range(x0, x1 + 1):                 # 8 pixels repeating
        c.plot(x, top, GREY if x % 4 else WOOD)
        c.plot(x, top + 1, SKY if x % 8 in (2, 6) else GREEN)
        if x % 8 in (0, 5):
            c.plot(x, top + 2, GREEN)
    for x, inward in ((x0, 1), (x1, -1)):
        for i, depth in enumerate((6, 3, 1)):
            for y in range(top, top + depth):
                c.plot(x + inward * i, y, SKY)
        c.vline(x, top, GROUND_Y - 1, SKY)
    tufts(c, x0 + 3, x1 - 3, top)


# A boulder 2 metatiles wide, 2 high: round, the moon on its top and
# on its right.
BOULDER = ["....kkkkkkkk....",
           "..kkddddddwwkk..",
           ".kdddddddddwwwk.",
           "kdddkddddddddwwk",
           "kddddddkdddddwwk",
           "kdkdddddddddddwk",
           "kddddddddkdddwwk",
           "kdddkdddddddddwk",
           "kddddddkdddddddk",
           "kkdddddddkddddwk",
           "kddddkddddddddwk",
           "kddddddddkdddddk",
           "kdkddddddddddddk",
           "kddddkdddddkddwk",
           "kdddddddkddddddk",
           "kddkdddddddddddk",
           "kdddddkdddkddddk",
           "kddddddddddddkdk",
           "kdkdddddkddddddk",
           "kddddkdddddddddk",
           "kdddddddddkddddk",
           "kddkdddddddddkdk",
           "kddddddkdddddddk",
           "kdkdddddddddkddk",
           "kddddkdddddddddk",
           "kdddddddkddddddk",
           "kddkddddddddkddk",
           "kddddddkdddddddk",
           ".kdddddddddkddk.",
           "kkkddkddddddkkkk",
           "kbkkkkkkkkkkkkbk",
           "kkkkkkkkkkkkkkkk"]


def boulder(c, x0, top=112):
    """A boulder from pixel x0 (a multiple of 8), 16 pixels wide, from
    line `top` to the path: its top, its middle 8 lines repeating,
    its foot."""
    for y in range(top, GROUND_Y):
        k = y - top
        row = BOULDER[k if k < 8 or k >= 24 else 8 + k % 8]
        c.blit(x0, y, [row], PALETTE)


def fallen_tree(c, x0, x1, top, bottom, props):
    """A dead tree fallen long ago across the path, solid from pixel x0
    to x1, lines `top` to `bottom`, broken at both ends; broken limbs
    prop it up: (x, the line of their foot). Under it, the passage."""
    for y in range(top, bottom + 1):
        for x in range(x0, x1 + 1):
            put(c, x, y, lying_bark(x, y, top, bottom))
    for i in range(4):                          # broken on the right
        for y in range(top + i // 2, bottom + 1 - i // 2):
            if i == 0 or (y + i) % 4 == 0:
                c.plot(x1 - i, y, SKY)
    cx, cy = x0 + 2.5, (top + bottom + 1) / 2   # cut on the left:
    for y in range(top, bottom + 1):            # its rings
        for x in range(x0 - 2, x0 + 6):
            u, w = (x + 0.5 - cx) / 3.2, (y + 0.5 - cy) / 8.5
            d = (u * u + w * w) ** 0.5
            if d <= 1:
                ring = int(d * 4) % 2
                colour = SKY if d > 0.85 else (WOOD if ring else GREY)
                if d <= 0.85 and u < -0.2 and w < 0.3:
                    colour = WOOD if ring else GREY
                put(c, x, y, colour)
    c.blit(x1 - 7, top - 3, ["......k.k.", "...k.kwkdk",
                             "..kwkddddk"], PALETTE)
    for x, foot in props:                       # straight down
        for y in range(bottom + 1, foot + 1):
            c.blit(x - 1, y, ["kddbk"], PALETTE)
        c.hline(x - 3, x + 4, foot, SKY)
    for x, rise in ((x0 + 14, 9), (x0 + 31, 6)):  # broken limbs on it
        for i in range(rise):
            c.blit(x + i // 2, top - 1 - i, ["kdwk"], PALETTE)


def lying_bark(x, y, top, bottom):
    """The bark of a trunk lying down, 8 pixels repeating: lit on top,
    its cracks along it."""
    h = (y - top) / (bottom - top)
    x %= 8                                      # 8 pixels repeating
    crack = (y + x // 4) % 5 == 0 and x not in (3, 4)
    if y in (top, bottom):
        return SKY
    if y == top + 1:
        return WHITE if (x + y) % 3 else WOOD
    if crack:
        return SKY
    if h < 0.55:
        return WOOD if (x // 2 + y) % 4 else GREY
    if h < 0.85:
        return GREY
    return SKY if (x + y) % 2 else GREY


def stile(c, x0):
    """The way out of the mire: two dead posts on the metatiles at x0
    and x0 + 24, a beam over the doorway between them (line 88)."""
    for px in (x0 + 1, x0 + 25):
        trunk(c, px, px + 5, 82, GROUND_Y - 1)
        roots(c, px, px + 5, rows=4, spread=1)
        c.blit(px, 78, ["..k...", ".kdk..", ".kddk.", "kdddwk"],
               PALETTE)
    planks(c, x0, x0 + 31, 88)


def stile_doors(c, x0):
    """The doorway of stile(x0) shut: a gate of rough planks, two bands
    of dark wood."""
    for y in range(96, GROUND_Y):
        for x in range(x0 + 8, x0 + 24):
            i = x - x0 - 8
            if i % 4 == 3:
                colour = SKY
            elif y in (104, 105, 130, 131):
                colour = GREY if y % 2 == 0 else SKY
            else:
                colour = WOOD if (i % 4 != 1 or y % 5) else GREY
            c.plot(x, y, colour)
