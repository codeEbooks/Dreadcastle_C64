"""The grey crags under the moon: the pieces of their picture.

Level 5, THE GREY CRAGS, has a set of characters of its own (one
for each level of the mountain and the castle). Its look, rocks and
snow under the moon: the moonlit night of the
wood and the mire, the moon still in the sky up on the right (a
sprite, moon.py); grey crags in layers, with cracks; ledges with snow
on them; a few dark pines; the crevasse; the crag that shuts the sky.

The colours: a cell has the black background, dark grey ($d022, as in
every setting), medium grey ($d023: in the mountain the second shared
colour is grey, not brown: next_env sets it) and one colour of its own
(0-7): white for the snow and the edges the moon lights (it is up on
the right), green for the pines. The rock is medium grey, its shadows
dark grey, its cracks black.

The pieces repeat on the grid of the cells and of the metatiles, so
that a set holds the level: the rock repeats every 32 pixels across
and 16 lines down, the snow every 16 pixels; the pines, the peaks, the
boulder are one drawing each.
"""

import village as v

BACKGROUND, OPEN_SKY = v.BACKGROUND, v.OPEN_SKY
SKY, GREY = v.BACKGROUND, v.SHARED_1        # black, dark grey
STONE = 12                                  # $d023 here: medium grey
WHITE, GREEN, BLUE, CYAN = v.WHITE, v.GREEN, v.BLUE, v.CYAN
SHARED = (SKY, GREY, STONE)                 # $d021, $d022, $d023
GROUND_Y = v.GROUND_Y
flat = v.flat
PALETTE = {"k": SKY, "d": GREY, "m": STONE, "w": WHITE, "g": GREEN,
           "u": BLUE, "c": CYAN}


def own(c, x, y):
    """The colour of its own of the cell of pixel (x, y), or None."""
    found = c.cell_colours(x // 4, y // 8) - set(SHARED) - {OPEN_SKY}
    return next(iter(found)) if found else None


def put(c, x, y, colour):
    """A pixel of a colour of its own, where its cell has no other:
    else the grey of the rock."""
    if colour not in SHARED:
        here = own(c, x, y)
        if here is not None and here != colour:
            colour = STONE
    c.plot(x, y, colour)


def sky(c):
    """The open sky: black."""
    for y in range(c.height):
        for x in range(c.width):
            if c.get(x, y) == OPEN_SKY:
                c.plot(x, y, BACKGROUND)


# --- the rock -----------------------------------------------------------
# The rock face, 32 pixels across and 32 lines down, repeating: facets
# of grey between black cracks; the edge of a facet under a crack lit
# white (the moon is up on the right), the edge over a crack and the
# one on its left in shadow; some facets darker.
ROCK = ["dmmwkdmmmmmmmmmwkwmmmmmmmmmmmdmm",
        "mmmmkdddmmmmmmmmkdmmmmmmmmmmmmmm",
        "mdmmkdddddmmmmmdkdmmmmmmmmmmmmdm",
        "mmddwkkkdddmmmmdkdmmmmmmmmmmmmmm",
        "ddddkkmmkkddmmmkwmmmddmmmmmmmmmd",
        "ddkkmmddmmkdddmkdddddddmmmmmmmmd",
        "kkmmddddddkkdddkddddkkdddmmmmmdd",
        "mmddddddddkwkkdkkkkkwwkdddmmmddk",
        "ddddddddddkdwwkkwwwwmmwkkddmddkm",
        "ddddddddddkdmmwwmmmdmmmwwkdddkmd",
        "dddddddddkwmmmmmmmmmmmmmdkkdkmdd",
        "dddddddddkdmmmmmmmmmdmmmkmmkmddd",
        "dddddddddkdmmmmmmmmmmmmdkddmdddd",
        "dddddddddkdmmmmmmmmmmdddkddddddd",
        "dddddddddkdmmmmmmmmmmmdkmddddddd",
        "dddddddddmkdmmmmmmmmmwkmdddddddd",
        "ddddddddddkdmmmmmmmmmmkddddddddd",
        "ddddddddddkdmmmmmmmmmmkddddddddd",
        "ddddddddddmkdmmmmmmmmwkddddddddd",
        "ddddkkkddddkdmmmmmddmmkddddddddd",
        "dddkkkwkdddkdmmmdddddmkddddddddd",
        "dkkwkwmwkdkmkdddddkkddwkdddddddd",
        "kkwkwmmmwkkdkdddkkwwkddkdddddddk",
        "wwdkdmmmmwwkwdkkwkdmwkdkdddddkkk",
        "mmdkdmmmmmmwkkwwmwkdmwkkdddkkkww",
        "mmkwmmmmmmmmwwmmmmkdmmwwkdkkwwmm",
        "mmkdmmmmmmmmmdmmmmkdmmmmwkwwmmmm",
        "mwkdmmmmmmmmmmmmmmwkdmmmmwmmdmmm",
        "mmwkdmmmmmmmmmdmmmdkdmmmmmmmmmmm",
        "dmmkdmmmmmmmmmmmmdkwmmmmmmmmmdmm",
        "mmwkdmmmmmmmmmmdddkdmmmmmmmmmmmm",
        "mdmwkdmmmmmmmmmmdkwmmmmmmmmmmmdm"]


def rock(x, y, top=0):
    """The rock face at pixel (x, y): the same everywhere, so that the
    blocks of rock share their characters."""
    return PALETTE[ROCK[y % 32][x % 32]]


# The snow lying on a ledge, 16 pixels repeating: how deep it is under
# its top (0-3 lines more), white, its foot grey.
SNOW = [2, 2, 3, 3, 2, 1, 1, 2, 2, 3, 2, 2, 1, 2, 3, 2]


def snow_cap(c, x0, x1, top):
    """Snow on the top of a rock from pixel x0 to x1, from line `top`:
    white down to its depth, then the grey of its foot."""
    for x in range(x0, x1 + 1):
        depth = SNOW[x % 16]
        for i in range(depth + 1):
            put(c, x, top + i, WHITE)
        c.plot(x, top + depth + 1, STONE)


def rock_block(c, x0, x1, y0, y1, snow=True, left=True, right=True,
               under=False, joints=0):
    """A block of rock, pixels x0 to x1, lines y0 to y1: the rock face
    (its layers from line `joints`), a black edge on its sides, lit
    white on its right; snow on its top (from line y0); `under`: its
    underside dark."""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            c.plot(x, y, rock(x, y, joints))
    edge = y0 + (4 if snow else 0)
    if left:
        c.vline(x0, edge, y1, SKY)
        for y in range(edge, y1 + 1):
            if rock(x0 + 1, y, joints) == STONE:
                c.plot(x0 + 1, y, GREY)
    if right:
        c.vline(x1, edge, y1, SKY)
        for y in range(edge, y1 + 1):
            if rock(x1 - 1, y, joints) != SKY:
                put(c, x1 - 1, y, WHITE if (y // 2) % 3 else STONE)
    if under:
        c.hline(x0, x1, y1, SKY)
        for x in range(x0, x1 + 1):
            if c.get(x, y1 - 1) != SKY:
                c.plot(x, y1 - 1, GREY)
    if snow:
        snow_cap(c, x0, x1, y0)


# The face of the mountain in the dark, behind: under the high ledge,
# a wall of dark grey, its ends ragged; down in the crevasse its far
# side, dark grey fading into the black of the depth.
def back_face(c, x0, x1, y0, y1, fade=False):
    """The face of the mountain in the dark, from pixel x0 to x1, lines
    y0 to y1, where nothing else is drawn yet: dark grey; `fade`: from
    its top into black, dithered."""
    for y in range(y0, y1 + 1):
        k = y - y0
        ragged = (0, 1, 2, 1)[(y // 4) % 4] if not fade else 0
        for x in range(x0 + ragged, x1 - ragged + 1):
            if c.get(x, y) not in (OPEN_SKY, SKY):
                continue
            if fade and (k >= 16 or (k >= 8 and (x + y) % 2)):
                colour = SKY
            else:
                colour = GREY
            c.plot(x, y, colour)


# The top of the crag, where the moon can be behind it (lines 0-23):
# snow on its top, and down the gullies of its grey face; only these
# two colours, so that the moon (behind the characters here, $d01b) is
# hidden by all of it. 32 pixels repeating.
CRAG_FACE = ["wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
             "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
             "wwwwmmwwwwwwwwwwwmmwwwwwwwwwmwww",
             "wwwmmmmwwwwwwwwwmmmmwwwwwwwmmmww",
             "wwmmmmmmwwwwwwwmmmmmmwwwwwmmmmmw",
             "wmmmmmmmmwwwwwmmmmmmmmwwwwmmmmmm",
             "mmmmmmmmmwwwwmmmmmmmmmwwwmmmmmmm",
             "mmmmmmmmmmwwmmmmmmmmmmmwwmmmmmmm",
             "mmmmmmmmmmwwmmmmmmmmmmmwwmmmmmmm",
             "mmmmmmmmmmwwwmmmmmmmmmmwmmmmmmmm",
             "mmmmmmmmmmmwwmmmmmmmmmmwmmmmmmmm",
             "mmmmmmmmmmmwwmmmmmmmmmwwmmmmmmmm",
             "mmmmmmmmmmmmwmmmmmmmmmwmmmmmmmmm",
             "mmmmmmmmmmmmwwmmmmmmmmwmmmmmmmmm",
             "wmmmmmmmmmmmmwmmmmmmmmwwmmmmmmmw",
             "wwmmmmmmmmmmmwmmmmmmmmmwmmmmmmww",
             "mwwmmmmmmmmmmwwmmmmmmmmwmmmmmwwm",
             "mmwmmmmmmmmmmmwmmmmmmmmwwmmmmwmm",
             "mmwwmmmmmmmmmmwmmmmmmmmmwmmmwwmm",
             "mmmwmmmmmmmmmmmwmmmmmmmmwmmmwmmm",
             "mmmwwmmmmmmmmmmwmmmmmmmmwwmmwmmm",
             "mmmmwmmmmmmmmmmmwmmmmmmmmwmwwmmm",
             "mmmmwmmmmmmmmmmmwmmmmmmmmwmwmmmm",
             "mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm"]


def crag(c, x0, x1, bottom):
    """The crag that shuts the sky, pixels x0 to x1, from the top of
    the playfield down to line `bottom`: its upper face grey and white
    (the moon goes behind it), then the rock, its underside dark,
    icicles under it; its ends slanting in."""
    for y in range(0, bottom + 1):
        for x in range(x0, x1 + 1):
            colour = PALETTE[CRAG_FACE[y][x % 32]] if y < 24 \
                else rock(x, y)
            c.plot(x, y, colour)
    for y in range(24, bottom + 1):             # the ends slant in
        cut = (y - 24) // 8
        for i in range(cut):
            c.plot(x0 + i, y, OPEN_SKY)
            c.plot(x1 - i, y, OPEN_SKY)
        c.plot(x0 + cut, y, SKY)
        c.plot(x1 - cut, y, SKY)
        put(c, x1 - cut - 1, y, WHITE)
    c.hline(x0, x1, bottom, SKY)
    for x in range(x0, x1 + 1):
        if c.get(x, bottom - 1) not in (SKY, OPEN_SKY):
            c.plot(x, bottom - 1, GREY)
    icicles(c, x0 + 8, x1 - 8, bottom + 1)


# A pillar of rock 8 pixels wide: its top, with snow; then 16 lines
# repeating down to its foot. The stones of the crevasse, the
# pinnacle and the cairns of the way out are all this drawing.
PILLAR_TOP = ["..kkkk..",
              ".kwwwwk.",
              "kwwwwwwk",
              "kmmwwwwk",
              "kdmmmwwk",
              "kddmmmwk"]
PILLAR = ["kddmmmwk",
          "kddmmmwk",
          "kdkkmmmk",
          "kkwwkkwk",
          "kdmmwwmk",
          "kddmmmwk",
          "kddmmmmk",
          "kdddmmwk",
          "kddmkkwk",
          "kdkkwwkk",
          "kkwmmmwk",
          "kdmmmmwk",
          "kddmmmmk",
          "kddmmmwk",
          "kdddmmwk",
          "kddmmmmk"]


def pillar(c, x0, top, foot):
    """A pillar of rock from pixel x0 (a metatile's), line `top` (a
    multiple of 8) to line `foot`."""
    for y in range(top, foot + 1):
        k = y - top
        row = PILLAR_TOP[k] if k < len(PILLAR_TOP) else \
            PILLAR[(k - len(PILLAR_TOP)) % len(PILLAR)]
        c.blit(x0, y, [row], PALETTE)


# --- the path -----------------------------------------------------------
def ground(c, gaps):
    """The path of rock, its top on GROUND_Y, everywhere but in the
    gaps (pixel x0, x1), and the last line black. A gap's sides are
    the rock going down (pit_wall)."""
    c.rect(0, GROUND_Y, c.width - 1, c.height - 1, SKY)
    x = 0
    for a, b in sorted(gaps) + [(c.width, c.width)]:
        if a > x:
            rock_block(c, x, a - 1, GROUND_Y, c.height - 2,
                       left=x > 0, right=a < c.width, joints=GROUND_Y)
        x = b + 1
    c.hline(0, c.width - 1, c.height - 1, SKY)


# --- icicles --------------------------------------------------------------
# Icicles under a ledge, 16 pixels repeating: (x, length).
ICICLES = [(2, 5), (5, 3), (9, 7), (12, 2), (14, 4)]


def icicles(c, x0, x1, y):
    """Icicles hanging from line y, pixels x0 to x1: white, thinner
    down to their point."""
    for x in range(x0, x1 + 1):
        for dx, length in ICICLES:
            if x % 16 == dx:
                for i in range(length):
                    put(c, x, y + i, WHITE if i < length - 1 else CYAN
                        if own(c, x, y + i) in (None, CYAN) else WHITE)


# --- the pines -------------------------------------------------------------
# A dark pine, 16 pixels wide, 36 lines: four tiers, dark grey and
# black, their needles green where the moon lights them (on the
# right), snow on their tops grey; the trunk.
PINE = [".......kk.......",
        "......kmmk......",
        "......kmgk......",
        ".....kmmggk.....",
        ".....kddggk.....",
        "....kmddgggk....",
        "....kdgggdgk....",
        "...kkkkgdkkkk...",
        ".....kmmggk.....",
        "....kmmggggk....",
        "....kkggdggk....",
        "...kmdddggdgk...",
        "...kddgggdggk...",
        "..kmkgdgdggdgk..",
        "..kdddgdggdggk..",
        ".kkkkkdggdkkkkk.",
        "....kmmmdgggk...",
        "...kmmdgggdggk..",
        "...kkdgdgdgggk..",
        "..kmdddgdggdggk.",
        "..kddkgdggdgggk.",
        ".kmkdgdggdggdgk.",
        ".kddddggdggdgggk",
        "kkkkkkddggdkkkkk",
        "...kmmmdgdggggk.",
        "..kmmkdgdggdgggk",
        "..kkddgdggdggggk",
        ".kmddgdggdggdggk",
        ".kddkdggdggdgggk",
        "kmkddgddggdggdgk",
        "kdddgdgggdggdggk",
        "kkkkkkkgdkkkkkkk",
        ".......kdk......",
        ".......kdk......",
        ".......kdk......",
        "......kddk......"]


def pine(c, x0, foot=GROUND_Y - 1):
    """A pine from pixel x0 (on the grid of 4), standing on line
    `foot` (whose cell row it fills down to its last line)."""
    c.blit(x0, foot - len(PINE) + 1, PINE, PALETTE)


# --- the peaks far away ------------------------------------------------------
def peak(c, cx, top, base=GROUND_Y - 1, snow=20):
    """A peak far away: its top at pixel cx (a multiple of 4), line
    `top` (a multiple of 8), its sides falling a pixel every two lines
    (a cell every cell row: the same characters all the way down) to
    line `base`. Dark grey on the left, grey on its right where the
    moon lights it; snow on its top, `snow` lines down."""
    for y in range(top, base + 1):
        k = y - top
        half = k // 2
        ridge = cx - k // 8
        for x in range(cx - half - 1, cx + half + 2):
            if c.get(x, y) not in (OPEN_SKY, SKY):
                continue
            if x in (cx - half - 1, cx + half + 1):
                colour = SKY
            elif k < snow - (x * 5 % 7) // 2:
                colour = WHITE
            elif x > ridge:
                colour = STONE
            else:
                colour = GREY
            c.plot(x, y, colour)


# --- the boulder ------------------------------------------------------------
BOULDER = [".....kkkkkk.....",
           "...kkwwwwwwkk...",
           "..kwwwwwwwwwwk..",
           ".kwwwwwmwwwwwwk.",
           ".kmwwmmmmwwwwmk.",
           "kmmmmmmmmmmmwmmk",
           "kdmmmmmmmmmmmmwk",
           "kdmmmmmmmmmmmmwk",
           "kddmmmmmmmmmmmwk",
           "kddmmmmmmmmmmmmk",
           "kdddmmmmmmdmmmwk",
           "kdddmmmmmdkmmmwk",
           "kddddmmmdkwmmmwk",
           "kddddmmdkwmmmmmk",
           "kdddddmkwmmmmmwk",
           "kddddddkmmmmmmwk",
           "kdddddkwmmmmmmwk",
           "kddddkdwmmmmmmmk",
           "kdddkddmmmmmmmwk",
           "kddddddddmmmmmwk",
           ".kdddddddmmmmmwk",
           ".kdkdddddddmmmk.",
           ".kddddddddddmmk.",
           "..kdkdddddddmmk.",
           "..kkddddddddmk..",
           "...kddddddddmk..",
           "..kkkddddddddkk.",
           ".kkdddddddddddkk",
           "kkkkkkkkkkkkkkkk",
           "kkkkkkkkkkkkkkkk"]


def boulder(c, x0, top=112):
    """A boulder 2 metatiles wide from pixel x0: the snow on its top
    from line `top` (its outline on the line above) down to the path
    (its middle longer if it is taller)."""
    rows = BOULDER[:-1]
    need = GROUND_Y - (top - 1)
    while len(rows) < need:
        rows = rows[:12] + [rows[12]] + rows[12:]
    c.blit(x0, top - 1, rows[-need:] if len(rows) > need else rows,
           PALETTE)
    on = [x for x in range(x0, x0 + 16) if c.get(x, top) == WHITE]
    return flat(2 * on[0], 2 * on[-1] + 1, top)


# --- the way out: the mouth of the pass --------------------------------------
def pass_mouth(c, x0):
    """The way out: two pillars of rock on the metatiles at x0 and
    x0 + 24, from line 72; a beam of rough timber over the doorway
    between them (lines 88-93)."""
    for px in (x0, x0 + 24):
        pillar(c, px, 72, GROUND_Y - 1)
    for y in range(88, 94):
        for x in range(x0 + 7, x0 + 25):
            colour = SKY if y in (88, 93) or x in (x0 + 7, x0 + 24) \
                else WHITE if y == 89 else GREY if (x + y) % 5 else STONE
            put(c, x, y, colour)


def barricade(c, x0):
    """The doorway of pass_mouth(x0) shut: logs across, lashed."""
    for y in range(96, GROUND_Y):
        for x in range(x0 + 8, x0 + 24):
            k = (y - 96) % 6
            if k == 5:
                colour = SKY
            elif k == 0:
                colour = STONE if x % 3 else GREY
            else:
                colour = GREY if (x + k) % 7 else SKY
            if x in (x0 + 11, x0 + 20) and k != 5:
                colour = STONE
            c.plot(x, y, colour)
