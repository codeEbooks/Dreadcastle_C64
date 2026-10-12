"""The frozen pass under the moon: the pieces of its picture.

Level 6, THE FROZEN PASS, has a set of characters of its own (one
for each level of the mountain and the castle). Its look, rocks and
snow under the moon: the moonlit night, the
moon still in the sky up on the right (a sprite, moon.py); white snow,
blue ice, slabs of ice, a serac, icicles; the peaks far away. And the
spikes of ice, still and glinting: they stay where they are, and a
glint runs over them (their characters change while the level is
played: SPIKE_FRAMES, as the wisps of the mire).

The colours: a cell has the black background, dark grey ($d022, as in
every setting), light blue ($d023: next_env sets it for this setting)
and one colour of its own (0-7): white in the snow, blue in the ice.
The snow lies in layers, white and light blue; the ice stands in
columns, light blue where the moon lights them (it is up on the
right), blue in their shade, dark grey in the grooves between them.

The pieces repeat on the grid of the cells and of the metatiles, so
that a set holds the level: the snow under the path every 32 pixels,
the ice every 16 pixels and 16 lines; the heaps of snow, the peaks,
the bridge are one drawing each.
"""

import crags
import village as v

BACKGROUND, OPEN_SKY = v.BACKGROUND, v.OPEN_SKY
SKY, GREY = v.BACKGROUND, v.SHARED_1        # black, dark grey
ICE = 14                                    # $d023 here: light blue
WHITE, BLUE = v.WHITE, v.BLUE
SHARED = (SKY, GREY, ICE)                   # $d021, $d022, $d023
GROUND_Y = v.GROUND_Y
flat = v.flat
PALETTE = {"k": SKY, "d": GREY, "a": ICE, "w": WHITE, "u": BLUE,
           "m": ICE}                        # the crags' grey: here blue


def own(c, x, y):
    """The colour of its own of the cell of pixel (x, y), or None."""
    found = c.cell_colours(x // 4, y // 8) - set(SHARED) - {OPEN_SKY}
    return next(iter(found)) if found else None


def put(c, x, y, colour):
    """A pixel of a colour of its own, where its cell has no other:
    else light blue."""
    if colour not in SHARED:
        here = own(c, x, y)
        if here is not None and here != colour:
            colour = ICE
    c.plot(x, y, colour)


def sky(c):
    """The open sky: black."""
    for y in range(c.height):
        for x in range(c.width):
            if c.get(x, y) == OPEN_SKY:
                c.plot(x, y, BACKGROUND)


# --- the snow under the path --------------------------------------------
# The path is deep snow in layers, 32 pixels repeating, from its top
# (line 144) to the last line of the playfield: fresh snow, white,
# rippled by the wind; older snow, its layers light blue and dark
# grey; at the bottom ice, blue. The last line is black.
LAYERS = ["wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
          "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
          "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
          "wwwwwwwwwwaaaawwwwwwwwwwwwwwwwww",
          "wwwwwaaaaawwwwwwwwwwwwwwwwaaaaww",
          "aaaaawwwwwwwwwwwwwwwaaaaaawwwwwa",
          "wwwwwwwwwwwwwwwaaaaawwwwwwwwwwww",
          "wwwwwwwwwwaaaaawwwwwwwwwwwwwwwww",
          "aaawwwwaaawwwwwwwwwwwwwwwaaaaaaa",
          "aaaaaaaaaaaaawwwwwwwaaaaaaaaaaaa",
          "ddaaaaaaaaaaaaaaaaaaaaaaaaaadddd",
          "aaddddaaaaaaaaaaaaaaaaaddddaaaaa",
          "aaaaaaddddddaaaaaaaddddaaaaaaaaa",
          "wwaaaaaaaaaaddddddddaaaaaaaawwww",
          "wwwwwwaaaaaaaaaaaaaaaaaawwwwwwww",
          "aaawwwwwwwwwwaaaaaaawwwwwwwwaaaa",
          "aaaaaaawwwwwwwwwwwwwwwwaaaaaaaaa",
          "aaaaaaaaaaaaawwwwwaaaaaaaaaaaaaa",
          "ddaaaaaaaaaaaaaaaaaaaaaaaaaaaadd",
          "aaddddddaaaaaaaaaaaaaaaaddddddaa",
          "aaaaaaaaddddddddaaaaddddaaaaaaaa",
          "aaaaaaaaaaaaaaaaddddaaaaaaaaaaaa",
          "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
          "uuaaaaaaaaaaaaaaaaaaaaaaaaaauuuu",
          "uuuuuuaaaaaaaaaaaaaaaaaauuuuuuuu",
          "uuuuuuuuuuuaaaaaaaauuuuuuuuuuuuu",
          "dduuuuuuuuuuuuuuuuuuuuuuuuuuuddd",
          "uuddduuuuuuuuuuuuuuuuuuuudddduuu",
          "uuuuuddddduuuuuuuuuuddddduuuuuuu",
          "uuuuuuuuuuddddddddddduuuuuuuuuuu",
          "uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu",
          "kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk"]


def snowfield(c, x0, x1, left=True, right=True):
    """The path from pixel x0 to x1: the layers of snow from line
    GROUND_Y down; where it ends at a chasm, its side: black at the
    edge, lit light blue on its right end (the moon), dark grey on its
    left end."""
    for y in range(GROUND_Y, c.height):
        row = LAYERS[y - GROUND_Y]
        for x in range(x0, x1 + 1):
            c.plot(x, y, PALETTE[row[x % 32]])
    for y in range(GROUND_Y + 3, c.height):
        if left:
            c.plot(x0, y, SKY)
            c.plot(x0 + 1, y, GREY)
        if right:
            c.plot(x1, y, SKY)
            if y >= GROUND_Y + 8:
                c.plot(x1 - 1, y, ICE)


def ground(c, gaps):
    """The path everywhere but in the gaps (pixel x0, x1)."""
    x = 0
    for a, b in sorted(gaps) + [(c.width, c.width)]:
        if a > x:
            snowfield(c, x, a - 1, left=x > 0, right=a < c.width)
        x = b + 1
    c.hline(0, c.width - 1, c.height - 1, SKY)


# --- the ice ----------------------------------------------------------------
# The ice, 16 pixels and 16 lines repeating: columns of ice, light blue
# where the moon lights them, blue in their shade, dark grey (or black,
# deep) in the grooves between them.
ICE_FACE = ["duuaaaduaaakduaa",
            "duuaaaduaaakduaa",
            "duaaaadduaaakdua",
            "duaaaaaduaaakdua",
            "kduaaaaduuaakdua",
            "kduaaaadduaaakdu",
            "kduaaaaaduaaakdu",
            "kduuaaaaduaaaadu",
            "duuaaaaaduuaaadu",
            "duuaaaaakduaaadu",
            "duaaaaaakduaaaad",
            "duaaaaaakduuaaad",
            "duuaaaaadduaaaud",
            "duuaaaaadduaaaud",
            "duuuaaaaduaaaakd",
            "duuaaaaaduaaaakd"]


def ice(x, y):
    return PALETTE[ICE_FACE[y % 16][x % 16]]


# Snow on the ice, 16 pixels repeating, a cell row high: white, its
# foot light blue; under it the ice starts.
SNOW_CAP = ["wwwwwwwwwwwwwwww",
            "wwwwwwwwwwwwwwww",
            "wwwwwwwwwwwwwwww",
            "wwwawwwwwwwwwaww",
            "waaaawwwwwwaaaaw",
            "aaaaaawwwwaaaaaa",
            "aadaaaaaaaaaadaa",
            "dddddaddaddddddd"]


# A slab's ice, under its snow (a cell row, 16 pixels repeating): lit
# light blue at its top, blue, dark grey at its foot; then its
# underside, dark (ice_block).
SLAB_ICE = ["aaaaauaaaaaaauaa",
            "uaaauuuaaaauuuaa",
            "uuauuuuuaauuuuua",
            "uuuuuduuuuuuduuu",
            "uuuudduuuuuudduu",
            "dduddddudddddddu"]


def ice_block(c, x0, x1, y0, y1, under=False):
    """A block of ice, pixels x0 to x1, lines y0 to y1 (y0 on the grid
    of the cells): snow on its top, a cell row, then the ice; black
    edges, its right edge lit, its left in shade, its top corners
    round; `under`: its underside dark (a slab hanging)."""
    for y in range(y0, y1 + 1):
        k = y - y0
        for x in range(x0, x1 + 1):
            if k < len(SNOW_CAP):
                colour = PALETTE[SNOW_CAP[k][x % 16]]
            elif under and k - len(SNOW_CAP) < len(SLAB_ICE):
                colour = PALETTE[SLAB_ICE[k - len(SNOW_CAP)][x % 16]]
            else:
                colour = ice(x, y)
            c.plot(x, y, colour)
    for y in range(y0 + 1, y1 + 1):
        c.plot(x0, y, SKY)
        c.plot(x1, y, SKY)
        if y >= y0 + len(SNOW_CAP):
            c.plot(x0 + 1, y, GREY)
            c.plot(x1 - 1, y, ICE)
    c.plot(x0, y0, OPEN_SKY)
    c.plot(x1, y0, OPEN_SKY)
    if under:
        c.hline(x0, x1, y1, SKY)
        for x in range(x0 + 1, x1):
            c.plot(x, y1 - 1, GREY if x % 4 else SKY)


# Icicles under a slab, 16 pixels repeating: (x, length).
ICICLES = [(1, 4), (3, 7), (6, 3), (9, 6), (11, 2), (13, 5)]


def icicles(c, x0, x1, y):
    """Icicles hanging from line y, pixels x0 to x1: white, their tips
    light blue."""
    for x in range(x0, x1 + 1):
        for dx, length in ICICLES:
            if x % 16 == dx:
                for i in range(length):
                    put(c, x, y + i, WHITE if i < length - 2 else ICE)


# --- the heaps of snow ------------------------------------------------------
def heap(c, x0, top=112, foot=GROUND_Y - 1, rx=12.0, p=2.0):
    """A heap of snow on the metatiles from pixel x0 (2 wide), its top
    on line `top`, round, its foot a little wider (rx pixels from its
    middle) on the path: lit from up on the right, white; light blue,
    then dark grey, in its shade (dithered between). Its surface: its
    top line."""
    cx = x0 + 7.5
    ry = foot - top + 4.0
    inside = {}
    for y in range(top, foot + 1):
        h = (foot + 1 - y) / ry                 # 1 over the top
        half = rx * (1 - h ** p) ** (1 / p)
        for x in range(int(cx - rx) - 2, int(cx + rx) + 3):
            if abs(x - cx) > half + 0.5:
                continue
            nx = (x - cx) / rx
            ny = -h * 0.8
            nz = max(0.0, 1 - nx * nx - ny * ny) ** 0.5
            norm = (nx * nx + ny * ny + nz * nz) ** 0.5
            inside[(x, y)] = (nx * 0.55 - ny * 0.75 + nz * 0.45) / norm
    for (x, y), light in inside.items():
        odd = (x + y) % 2
        if light > 0.8:
            colour = WHITE
        elif light > 0.66:
            colour = WHITE if odd else ICE
        elif light > 0.35:
            colour = ICE
        elif light > 0.18:
            colour = ICE if odd else GREY
        else:
            colour = GREY
        c.plot(x, y, colour)
    for x, y in list(inside):
        for q in ((x - 1, y), (x + 1, y), (x, y - 1)):
            if q not in inside and y < foot - 1 and \
                    c.get(*q) in (OPEN_SKY, SKY):
                c.plot(q[0], q[1], SKY)
    on = sorted(x for x, y in inside if y == top)
    return flat(2 * on[0], 2 * on[-1] + 1, top)


# --- the spikes of ice -------------------------------------------------------
# Two kinds of spikes, a metatile each (8 x 16 pixels): crystals of
# ice, light blue where the moon lights them, dark grey in their
# shade, on a foot of ice; and four pictures of each: a glint (white)
# running up their right edges. The colour of their own is white.
SPIKE_KINDS = ("A", "B")
SPIKE_FRAMES = 4
SPIKE = {"A": ["........",
               "...a....",
               "...a....",
               "..da....",
               "..da....",
               "..daa...",
               "..daa...",
               ".ddaa...",
               ".ddaa...",
               ".ddaaa.a",
               ".dddaa.a",
               "dddaaa.a",
               "dddaaada",
               "ddddaada",
               "dddaaada",
               "dddddddd"],
         "B": ["........",
               "........",
               "......a.",
               "......a.",
               ".....da.",
               ".a...da.",
               ".a...daa",
               "da...daa",
               "da..ddaa",
               "da..ddaa",
               "daa.ddaa",
               "daa.ddaa",
               "ddaaddda",
               "ddaaddaa",
               "ddaaddda",
               "dddddddd"]}


def spike_rows(kind, frame):
    """The picture `frame` of a metatile of spikes, black around them:
    on the light blue of their right edges (the moon) the glint,
    white, three lines high, from the foot (frame 0) up to the tips
    (frame 3)."""
    band = (11, 8, 5, 2)[frame]
    rows = [list(row.replace(".", "k")) for row in SPIKE[kind]]
    for y in range(band, band + 3):
        for x in range(8):
            if rows[y][x] == "a" and (x == 7 or rows[y][x + 1] in "kd"):
                rows[y][x] = "w"
    return ["".join(row) for row in rows]


def spike(c, x0, kind, frame=0):
    """A spike's picture `frame` in the metatile at pixel x0, row 8
    (lines 128-143)."""
    c.blit(x0, 128, spike_rows(kind, frame), PALETTE)


# --- the peaks far away ------------------------------------------------------
def peak(c, cx, top, base=GROUND_Y - 1, snow=20):
    """A peak far away: its top at pixel cx (a multiple of 4), line
    `top` (a multiple of 8), its sides falling a pixel every two lines
    (a cell every cell row: the same characters all the way down) to
    line `base`, where nothing nearer is drawn (draw it after them).
    Snow on its top, light
    blue in its shade; under the snow dark grey on the left, on the
    right, where the moon lights it, dark grey and light blue
    dithered."""
    for y in range(top, base + 1):
        k = y - top
        half = k // 2
        ridge = cx - k // 8
        for x in range(cx - half - 1, cx + half + 2):
            if c.get(x, y) != OPEN_SKY:
                continue
            if x in (cx - half - 1, cx + half + 1):
                colour = SKY
            elif k < snow - (x * 5 % 7) // 2:
                colour = WHITE if x > ridge - 1 else ICE
            elif x > ridge:
                colour = ICE if (x + y) % 2 else GREY
            else:
                colour = GREY
            put(c, x, y, colour)


# --- the bridge of snow ------------------------------------------------------
def snow_bridge(c, x0, x1, top):
    """The bridge of snow still standing, pixels x0 to x1, its top on
    line `top` (on the grid of the cells): snow, a cell row, then the
    ice under it, its underside dark, icicles; its ends broken off.
    It stands on an arch of ice in the dark, behind (arch). Its
    surface: its top, but its broken ends."""
    for y in range(top, top + 16):
        k = y - top
        for x in range(x0, x1 + 1):
            if k < len(SNOW_CAP):
                colour = PALETTE[SNOW_CAP[k][x % 16]]
            elif k < 14:
                colour = ice(x, y)
            elif k == 14:
                colour = GREY if x % 4 else SKY
            else:
                colour = SKY
            c.plot(x, y, colour)
    for x, step in ((x0, 1), (x1, -1)):        # broken ends
        for i, depth in enumerate((14, 10, 6, 3)):
            for y in range(top + 16 - depth, top + 16):
                c.plot(x + step * i, y, OPEN_SKY)
        c.vline(x, top + 1, top + 2, SKY)
        c.plot(x, top, OPEN_SKY)
    icicles(c, x0 + 4, x1 - 4, top + 16)
    return flat(2 * x0 + 2, 2 * x1 - 1, top)


def arch(c, x0, x1, top, foot=GROUND_Y - 1, leg=8):
    """An arch of ice in the dark, behind, from pixel x0 to x1, from
    line `top` down to `foot`: its opening between its legs (`leg`
    pixels wide at the foot) half an ellipse, from the foot up to a
    cell row under `top`. Not solid: it holds nothing."""
    middle = (x0 + x1) / 2
    wide = (x1 - x0) / 2 - leg + 0.5
    high = foot - (top + 8)
    for y in range(top, foot + 1):
        up = (foot - y) / high
        for x in range(x0, x1 + 1):
            across = (x - middle) / wide
            if up < 1 and across * across + up * up < 1:
                continue                    # the opening
            back_pixel(c, x, y, x0, x1)


def back_pixel(c, x, y, x0, x1):
    """A pixel of the ice in the dark, behind, where nothing is drawn
    yet (draw it after the things in front): dark grey, streaks of
    light blue every 8 pixels (the moon on its ridges), black at its
    sides."""
    if c.get(x, y) != OPEN_SKY:
        return
    if x in (x0, x1):
        colour = SKY
    elif x % 8 == 5 or (x % 8 == 6 and y % 4 < 2):
        colour = ICE
    else:
        colour = GREY
    c.plot(x, y, colour)


def back_ice(c, x0, x1, y0, y1):
    """A column of ice in the dark, behind, pixels x0 to x1, lines y0
    to y1 (back_pixel)."""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            back_pixel(c, x, y, x0, x1)


# --- a column of ice in a chasm ----------------------------------------------
def ice_column(c, x0, top, foot):
    """A column of ice a metatile wide from pixel x0, rising from the
    bottom of a chasm (line `foot`) to line `top`: snow on it, then
    the ice (ice_block)."""
    ice_block(c, x0, x0 + 7, top, foot)


# --- the way out: the col ----------------------------------------------------
def pass_gate(c, x0):
    """The way out, the col: two pillars of the crags, white with snow
    and blue, a beam over the doorway between them (line 88)."""
    for px in (x0, x0 + 24):
        for y in range(72, GROUND_Y):
            k = y - 72
            row = crags.PILLAR_TOP[k] if k < len(crags.PILLAR_TOP) else \
                crags.PILLAR[(k - len(crags.PILLAR_TOP)) % len(
                    crags.PILLAR)]
            c.blit(px, y, [row], PALETTE)
    for y in range(88, 94):
        for x in range(x0 + 7, x0 + 25):
            colour = SKY if y in (88, 93) or x in (x0 + 7, x0 + 24) \
                else WHITE if y in (89, 90) else GREY if x % 4 else ICE
            put(c, x, y, colour)


def gate_doors(c, x0):
    """The doorway of pass_gate(x0) shut: logs across, frozen."""
    for y in range(96, GROUND_Y):
        for x in range(x0 + 8, x0 + 24):
            k = (y - 96) % 6
            if k == 5:
                colour = SKY
            elif k == 0:
                colour = WHITE if x % 4 else ICE
            else:
                colour = GREY if (x + 2 * k) % 8 else SKY
            if x in (x0 + 11, x0 + 20) and k != 5:
                colour = ICE
            put(c, x, y, colour)
