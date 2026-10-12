"""The wild wood under the moon: the pieces of its picture.

The forest has a set of characters of its own:
levels 3 and 4. Its look, a moonlit night, dark green:
the night of the village in a wood: the
black sky with the moon and the stars, brown trunks, dark green
leaves. A first drawing was redrawn with better
trees and bushes: this is the second. The
moon is not here: it stays still in the sky, up on the right, a
sprite (moon.py).

The same canvas and the same shared colours as the village
(village.py): a cell has the black background, dark grey ($d022) and
brown ($d023), and one colour of its own (0-7). The dark green of the
leaves is the C64's green with dark grey and black: a crown is a heap
of round lobes, each lit by the moon (up and to the left) on its own
and the whole heap lit too; the leaves are a pattern of small leaves
(LEAVES, 8 x 8 pixels) that turns green where the light is, dark grey
and black in the shade. Bark has long grooves; cut wood shows pale
(yellow) with its rings.

A set holds 253 characters for the pictures of its levels, so the
pieces repeat: every tree is the same drawing on the same grid of the
cells, and the bark, the bushes, the hedge and the middle of the
boughs repeat every 8 or 16 pixels. The bushes behind the path are
drawn only in cells with nothing else in them: what stands in front
of them keeps its own characters, and a black edge round it.
"""

import village as v

BACKGROUND, OPEN_SKY = v.BACKGROUND, v.OPEN_SKY
GREY, WOOD, SKY = v.SHARED_1, v.SHARED_2, v.BACKGROUND
GREEN, RED, BLUE, YELLOW, WHITE = v.GREEN, v.RED, v.BLUE, v.YELLOW, \
    v.WHITE
GROUND_Y = v.GROUND_Y
flat = v.flat
PALETTE = {"k": SKY, "d": GREY, "b": WOOD, "g": GREEN, "r": RED,
           "l": BLUE, "y": YELLOW, "w": WHITE}
LX, LY = -0.55, -0.83               # the moon: up and to the left


# --- leaves -----------------------------------------------------------
def leaf_map():
    """8 x 8 thresholds: four small leaves, each lit first at its
    middle and on its side towards the moon; the gaps between them
    last."""
    leaves = ((1.5, 1.5), (5.5, 1.5), (3.5, 5.5), (7.5, 5.5))
    order = []
    for y in range(8):
        for x in range(8):
            best = None
            for cx, cy in leaves:
                for ox in (-8, 0, 8):
                    for oy in (-8, 0, 8):
                        du = (x + 0.5 - cx - ox) / 2.1
                        dw = (y + 0.5 - cy - oy) / 2.6
                        d = du * du + dw * dw
                        if best is None or d < best[0]:
                            best = (d, du, dw)
            d, du, dw = best
            h = (1 - min(d, 1.5)) * 0.55 + (du * LX + dw * LY) * 0.45
            order.append((-h, (x * 5 + y * 3) % 7, x, y))
    order.sort()
    table = [[0.0] * 8 for _ in range(8)]
    for i, (_, _, x, y) in enumerate(order):
        table[y][x] = (i + 0.5) / 64
    return table


LEAVES = leaf_map()


def leaf_colour(x, y, light, grey=0.25):
    """The leaves at (x, y) for a light from 0 (none) to 1: green,
    dark grey or black."""
    t = LEAVES[y % 8][x % 8]
    if light > t:
        return GREEN
    return GREY if light > t - grey else SKY


def foliage(c, lobes, base=0.45, gain=0.55, macro=(0.2, 0.3),
            cap=0.86, outline=0.4, behind=False, bottom=None,
            left=None, right=None, frame=None, free_cells=False):
    """Leaves: lobes (cx, cy, r), back to front, each r lines high and
    r / 2 pixels wide (the pixels are two screen pixels wide). Each
    lobe is lit on its own and the whole heap is lit from the moon
    (macro: across and down, in `frame`, by default the heap's own
    box); a lobe in front has a black edge on the heap behind it, on
    its side in the shade (`outline`). Nothing below `bottom`, nor out
    of pixels `left` to `right`; `behind`: only where nothing is drawn
    yet; `free_cells`: only in cells with nothing drawn yet. In a cell
    with another colour of its own the green turns dark grey."""
    owner = {}
    for i, (cx, cy, r) in enumerate(lobes):
        rx = r / 2
        for y in range(int(cy - r) - 1, int(cy + r) + 2):
            if bottom is not None and y > bottom:
                continue
            for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
                if (left is not None and x < left) or \
                        (right is not None and x > right):
                    continue
                u, w = (x + 0.5 - cx) / rx, (y + 0.5 - cy) / r
                if u * u + w * w <= 1:
                    owner[(x, y)] = (i, u, w)
    if not owner:
        return
    if frame is None:
        xs = [x for x, _ in owner]
        ys = [y for _, y in owner]
        frame = (min(xs), min(ys), max(xs), max(ys))
    fx0, fy0, fx1, fy1 = frame
    mx, my = (fx0 + fx1) / 2, (fy0 + fy1) / 2
    hw, hh = (fx1 - fx0) / 2 + 1, (fy1 - fy0) / 2 + 1
    inside = [p for p in owner
              if 0 <= p[0] < c.width and 0 <= p[1] < c.height]
    taken = set()
    if free_cells:
        taken = {(x // 4, y // 8) for (x, y) in inside
                 if c.get(x, y) != OPEN_SKY}
    others = {}
    for x, y in inside:
        i, u, w = owner[(x, y)]
        if behind and c.get(x, y) != OPEN_SKY:
            continue
        key = (x // 4, y // 8)
        if key in taken:
            continue
        if key not in others:
            others[key] = v.own_colour_in(c, *key) not in (None, GREEN)
        lit = u * LX + w * LY
        edge = any(owner.get((x + dx, y + dy), (99,))[0] < i
                   for dx, dy in ((1, 0), (0, 1), (1, 1), (-1, 1)))
        if outline is not None and edge and lit < outline:
            c.plot(x, y, SKY)
            continue
        light = base + gain * lit + macro[0] * (x - mx) / hw * LX + \
            macro[1] * (y - my) / hh * LY
        colour = leaf_colour(x, y, min(light, cap))
        c.plot(x, y, GREY if colour == GREEN and others[key] else colour)


# --- bark -------------------------------------------------------------
def groove(x, y, period=16):
    """The grooves of bark, 8 pixels and 16 lines repeating (or 8):
    two long cracks that wander a pixel."""
    y = y % period * 16 // period
    a = 1 if y < 6 or y >= 12 else 2
    b = 5 if y < 4 or y >= 10 else 6
    return x % 8 == a or (x % 8 == b and y not in (8, 9))


def bark_colour(x, y, x0, x1, shade=3, period=16):
    """Bark of a round trunk from x0 to x1: black edges, the grooves
    dark grey on the lit side and black in the shade (the last `shade`
    pixels before the right edge, a pixel of half shade first)."""
    if x in (x0, x1):
        return SKY
    if x > x1 - shade:
        return SKY if groove(x, y, period) and x < x1 - 1 else GREY
    if x == x1 - shade:
        return GREY if y % 2 else WOOD
    return GREY if groove(x, y, period) else WOOD


def bark(c, x0, x1, y0, y1, shade=3, period=16):
    """A trunk's bark from x0 to x1, lines y0 to y1."""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            c.plot(x, y, bark_colour(x, y, x0, x1, shade, period))


def flare(c, x0, x1, bottom=GROUND_Y - 1):
    """Roots at the foot of a trunk from x0 to x1: its last 8 lines
    spread 3 pixels each side and split into roots."""
    width = x1 - x0 + 1
    for i in range(8):
        y = bottom - 7 + i
        spread = (i * 3) // 7
        a, b = x0 - spread, x1 + spread
        for x in range(a, b + 1):
            c.plot(x, y, bark_colour(x - a + x0, y, x0, x0 + (b - a),
                                     shade=max(3, width // 4)))
        if i >= 4:                              # between the roots
            for gx in (x0 + 1, x0 + width // 2, x1 - 1):
                if i >= 5 or gx != x0 + width // 2:
                    c.plot(gx, y, SKY)
    c.hline(x0 - 3, x1 + 3, bottom, SKY)


# --- trees ------------------------------------------------------------
# The crown of a tree: lobes (dx, dy, r) round its middle, back to
# front.
CROWN = [(-2, -27, 9), (7, -22, 8), (-9, -18, 8), (12, -11, 8),
         (-14, -7, 8), (2, -14, 11), (-5, -4, 10), (8, -2, 10),
         (-14, 4, 7), (14, 5, 6), (-7, 10, 8), (5, 11, 8),
         (0, 2, 9)]
TRUNK = 8                           # pixels wide: 2 cells


def crown(c, cx, cy):
    """The crown of a tree round (cx, cy): cx a multiple of 8 plus 4,
    cy of 8 plus 2, for its characters to be those of every tree."""
    foliage(c, [(cx + dx, cy + dy, r) for dx, dy, r in CROWN])


def tree(c, col, crown_row=4):
    """A tree behind the path: its trunk 2 cells wide from cell column
    `col` (a multiple of 4), its crown round line crown_row * 8 + 34,
    two boughs into it from the top of the trunk; its roots on the
    path."""
    x0 = col * 4
    cy = crown_row * 8 + 34
    for i in range(14):                         # the boughs
        y = cy + 10 - i
        c.blit(x0 - 1 - i // 3, y, ["kbbk"], PALETTE)
        c.blit(x0 + 5 + i // 3, y, ["kbdk"], PALETTE)
    bark(c, x0, x0 + TRUNK - 1, cy + 6, GROUND_Y - 9, shade=TRUNK // 4)
    flare(c, x0, x0 + TRUNK - 1)
    crown(c, x0 + TRUNK // 2, cy)


def branch(c, x0, x1, y, root="right"):
    """A bough to walk on, from x0 to x1 (whole cells) on line y (a
    multiple of 8), growing from a trunk on the `root` side: bark 6
    lines thick, lit on top, thicker where it leaves the trunk,
    thinner at its tip, where a tuft of leaves grows. Its middle
    repeats every 8 pixels."""
    for x in range(x0, x1 + 1):
        near = (x1 - x) if root == "right" else (x - x0)   # the trunk
        far = (x - x0) if root == "right" else (x1 - x)    # the tip
        thick = 6
        if near < 6:
            thick = 6 + (6 - near) // 2             # the collar: to 9
        if far < 8:
            thick = 3 + far * 3 // 8                # the tip: from 3
        for dy in range(thick + 1):
            if dy == thick:
                colour = SKY
            elif dy == thick - 1:
                colour = GREY
            elif dy == 2:
                colour = GREY if x % 8 in (0, 1, 2, 5) else WOOD
            elif dy == thick - 2 and dy > 2:
                colour = GREY if x % 2 else WOOD
            else:
                colour = WOOD
            c.plot(x, y + dy, colour)
    side = -1 if root == "right" else 1
    tip = x0 if root == "right" else x1
    foliage(c, [(tip + side, y + 1, 8), (tip - side * 4, y + 8, 8),
                (tip + side * 4, y + 9, 7)],
            behind=True, outline=None, base=0.5)
    return flat(2 * x0, 2 * x1 + 1, y)


def big_oak(c, col, low, high, low_x1, high_x1):
    """The great oak: a tree whose trunk stands at metatile column
    `col`, its crown high, under the moon's lines (moon.py); a low
    bough on line `low` and a high one on line `high`, to the right,
    to low_x1 and high_x1 (pixels); the high one holds up more of its
    crown. Returns the low bough's surface."""
    x0 = col * 8
    branch(c, x0 + TRUNK, high_x1, high, root="left")
    crown(c, x0 + 68, 58)
    tree(c, x0 // 4, 3)
    return branch(c, x0 + TRUNK, low_x1, low, root="left")


# --- the bushes, the sky ------------------------------------------------
# The bushes behind the path: lobes (dx, cy, r) repeating every 16
# pixels, darker than the crowns.
UNDER = [(-1, 136, 8), (8, 130, 10), (3, 137, 9), (13, 137, 9),
         (7, 141, 7), (15, 142, 6), (0, 142, 6)]
UNDER_PERIOD = 16


def undergrowth(c, x0, x1):
    """The bushes behind the path from pixel x0 to x1 (whole cells),
    in the cells with nothing drawn in them yet."""
    lobes = []
    for b0 in range(x0 - x0 % UNDER_PERIOD - UNDER_PERIOD,
                    x1 + UNDER_PERIOD, UNDER_PERIOD):
        lobes += [(b0 + dx, cy, r) for dx, cy, r in UNDER]
    foliage(c, lobes, base=0.32, macro=(0, 0.35), bottom=GROUND_Y - 1,
            left=x0, right=x1, frame=(0, 120, 100, 143),
            free_cells=True)


def sky(c):
    """The open sky: black."""
    for y in range(c.height):
        for x in range(c.width):
            if c.get(x, y) == OPEN_SKY:
                c.plot(x, y, BACKGROUND)


# --- the path, the river, the stones ------------------------------------
def ground(c):
    """The path through the wood: a green edge of grass, tufts of it
    on the earth below, brown with dark grey stones; the pattern
    repeats every metatile (8 x 16 pixels)."""
    c.rect(0, GROUND_Y, c.width - 1, c.height - 1, SKY)
    for x in range(c.width):
        for y in range(GROUND_Y, c.height - 1):
            inside_x, inside_y = x % 8, (y - GROUND_Y) % 16
            if y == GROUND_Y:
                colour = GREEN
            elif y < GROUND_Y + 3:
                blade = (x * 3 + y) % 4
                colour = GREEN if blade == 0 else \
                    SKY if blade == 2 and y == GROUND_Y + 1 else WOOD
            else:
                stone = (inside_x in (1, 2) and inside_y in (7, 8)) or \
                    (inside_x in (5, 6) and inside_y in (12, 13)) or \
                    (inside_x == 4 and inside_y == 9)
                shadow = (inside_x in (1, 2) and inside_y == 9) or \
                    (inside_x in (5, 6) and inside_y == 14)
                colour = GREY if stone else SKY if shadow else WOOD
            c.plot(x, y, colour)


def river(c, x0, width):
    """The river: running water below the path's level, from line
    152 to the bottom; banks of earth. Blue, dark ripples, grey
    glints of the moon; the pattern repeats every cell."""
    x1 = x0 + width - 1
    c.rect(x0, GROUND_Y, x1, c.height - 1, SKY)
    for y in range(152, c.height - 1):          # the last line: black
        for x in range(x0, x1 + 1):
            ripple = (x + y // 2) % 4
            if y % 4 == 0 and ripple == 0:
                colour = GREY
            elif y % 2 == 1 and ripple == 2:
                colour = SKY
            else:
                colour = BLUE
            c.plot(x, y, colour)
    for x in (x0, x1):
        c.vline(x, GROUND_Y, c.height - 2, WOOD)


# A stepping stone: a rock, the moon shining on it (white).
STONE = ["dddddddd",
         "wwwdddkd",
         "dwwdddkd",
         "dwdddddk",
         "ddddkddk",
         "dddddkdk",
         "dddddddk",
         "kddkddkk",
         "dddddddk",
         "dddddkdk",
         "kdddddkk",
         "ddkdddkk",
         "kddddkdk",
         "dddkdddk",
         "kdkdddkk",
         "ddddkdkk",
         "kddkdkkk",
         "kkddkdkk",
         "kdkdkkk.",
         ".kkkkkk."]


def stone(c, x0):
    """A stepping stone in the river: a metatile wide (x0 a multiple
    of 8), its flat top on line 128, down to the water."""
    c.blit(x0, 128, STONE, PALETTE)
    return flat(2 * x0, 2 * x0 + 15, 128)


# --- wood to stand on -------------------------------------------------
# The sawn tops of stumps: pale new wood (yellow), a ring and the
# heart brown, the rim black against the night; their bark below.
FACE_16 = ["...kkkkkkkkkk...",
           ".kkyyyyyyyyyykk.",
           "kyyyybbbbbbyyyyk",
           "kyyybyybbyybyyyk",
           "kbyyybbbbbbyyydk",
           "kbbyyyyyyyyyyddk",
           "kbbbbbbbbbbbbddk"]
FACE_8 = [".kkkkkk.",
          "kyyyyyyk",
          "kyybbyyk",
          "kbyyyydk",
          "kbbbbddk"]


def stump(c, x0, width, top):
    """A sawn stump `width` pixels wide (8 or 16; x0 a multiple of 8),
    from line `top` (a multiple of 8) to the path: its cut on top, the
    rings showing; bark; its roots spreading at its foot."""
    x1 = x0 + width - 1
    face = FACE_16 if width == 16 else FACE_8
    bark(c, x0, x1, top + len(face), GROUND_Y - 9,
         shade=max(2, width // 5))
    flare(c, x0, x1)
    c.blit(x0, top, face, PALETTE)
    return flat(2 * x0, 2 * x1 + 1, top)


# A fallen trunk, 2 metatiles long: moss on it, broken off at both
# ends, hollow: its dark heart shows at the right end.
LOG = ["..g...g.g.......",
       ".ggg.gggggg.....",
       "kgdggggdgggkkkk.",
       "kbbgbbbbbgkbbbbk",
       "kbbbbbbbbbkbkkdk",
       "kbdbbbdbbkbkkkkd",
       "kbbbbbbbbkbkkkkd",
       "kbbbdbbbbkdkkkkd",
       "kbbbbbbdbkbkkkkd",
       "kdbbbbbbbkdkkkkd",
       "kbbbdbbbbkdkkkkd",
       "kbbbbbbbbkbkkkkd",
       "kddbddbddkdkkkdk",
       "kdddddddddkdkkdk",
       "kkddkdddkdkdddk.",
       "kdkkdkkdkkkkkkk.",
       ".kkkkkkkkkk....."]


def log(c, x0):
    """The fallen trunk on the path, from x0 (a multiple of 8), lines
    128-143 (and its moss above)."""
    c.blit(x0, 126, LOG, PALETTE)


# Brambles: canes arching (from x, to x, height) over 16 pixels.
CANES = [(-3, 7, 13), (3, 13, 15), (8, 18, 12), (0, 9, 8), (10, 16, 7)]


def thorns(c, col, columns):
    """Brambles across the path from metatile column `col`, lines
    128-143: red canes arching, grey thorns all along them, the stems
    brown at their foot; nothing green in their cells. They hurt like
    an enemy (metaflags: HAZARD)."""
    for i in range(0, columns * 8, 16):
        x0 = col * 8 + i
        cane, spikes = set(), set()
        for xa, xb, h in CANES:
            steps = 3 * (xb - xa) + 2 * h
            for k in range(steps + 1):
                t = k / steps
                x = x0 + round(xa + (xb - xa) * t)
                y = GROUND_Y - 1 - round(h * 4 * t * (1 - t))
                if x0 <= x < x0 + 16 and y >= 128:
                    cane.add((x, y))
                    if k % 3 == 1:
                        sx = -1 if t < 0.4 else 1 if t > 0.6 else 0
                        spikes.add((x + sx, y - 1))
        for x, y in spikes:
            if (x, y) not in cane and x0 <= x < x0 + 16 and y >= 128:
                c.plot(x, y, GREY)
        for x, y in cane:
            c.plot(x, y, WOOD if y >= 140 else RED)
            if (x, y + 1) not in cane and y + 1 < GROUND_Y:
                c.plot(x, y + 1, SKY)
        c.hline(x0, x0 + 15, GROUND_Y - 1, SKY)


# --- the hollow oak, its roots, the hedge -------------------------------
def log_band(y, top, bottom):
    """The bark of a trunk lying down, by line from `top` to `bottom`:
    lit on top, dark below: (its colour, the colour of its cracks)."""
    h = (y - top) / (bottom - top)
    if y in (top, bottom):
        return SKY, SKY
    if h < 0.3:
        return WOOD, GREY
    if h < 0.7:
        return WOOD, SKY
    if h < 0.85:
        return GREY, SKY
    return SKY, GREY


def hollow_oak(c, col, columns, top, bottom):
    """The hollow oak: a huge oak fallen long ago, lying from metatile
    column `col` for `columns` metatiles, solid from line `top` to
    `bottom`: cracks along its bark, moss on top; broken off on the
    left, where it is hollow; it rests on a bough on the left and on
    its roots on the right (oak_roots); under it, the passage. Its
    bark repeats every 8 pixels."""
    x0, x1 = col * 8, col * 8 + 8 * columns - 1
    for y in range(top, bottom + 1):
        base, line = log_band(y, top, bottom)
        k = (y - top) % 8
        for x in range(x0, x1 + 1):
            crack = (k == 3 and x % 8 not in (0, 5)) or \
                (k == 6 and x % 8 in (2, 3, 4)) or \
                (k == 1 and x % 8 == 6)
            c.plot(x, y, line if crack else base)
    for x in range(x0 + 6, x1 + 1):             # moss on top
        if "gg.ggg.g"[x % 8] == "g":
            c.plot(x, top, GREEN)
        if "g...gg.."[x % 8] == "g":
            c.plot(x, top - 1, GREEN)
        if x % 8 == 4:
            c.plot(x, top + 1, GREEN)
    cx, cy = x0 + 5.5, (top + bottom + 1) / 2   # the broken end
    for y in range(top - 4, bottom + 2):
        for x in range(x0 - 4, x0 + 12):
            u, w = (x + 0.5 - cx) / 7.0, (y + 0.5 - cy) / 17.5
            d = (u * u + w * w) ** 0.5
            if d > 1:
                continue
            if d > 0.9:
                colour = SKY
            elif d > 0.62:
                colour = WOOD if (y + x) % 5 else GREY
            elif d > 0.52:
                colour = GREY
            else:
                colour = SKY                    # the hollow
            c.plot(x, y, colour)
    c.blit(x0 - 4, top - 6, ["..k.....k.",
                             ".kbk...kbk",
                             "kbbdk.kbdk"], PALETTE)   # splinters
    for i in range(GROUND_Y - bottom - 1):      # the bough under it
        x = x0 + 2 - i // 4
        c.blit(x - 2, bottom + 1 + i, ["kbbbddk"], PALETTE)
    c.blit(x0 - 14, GROUND_Y - 4, ["...kbbk..",
                                   "..kbbbdk.",
                                   ".kbbkbddk",
                                   "kkkk.kkkk"], PALETTE)


def oak_roots(c, x0, top_low, top_high, top=64, bottom=95):
    """The right end of the fallen oak (its trunk from `top` to
    `bottom`) and its roots, sawn off, that make steps: a low one from
    x0 (16 pixels wide) at line `top_low`, a high one from x0 + 16 at
    `top_high`."""
    stump(c, x0 + 16, 16, top_high)
    stump(c, x0, 16, top_low)
    for y in range(top, bottom + 1):            # the trunk's end
        for x in range(x0, x0 + 6):
            u = (x - x0) / 6
            w = (y - top) / (bottom - top)
            e = (u * 1.2) ** 2 + ((w - 0.5) * 2) ** 2
            if e <= 1.05:
                band, _ = log_band(y, top, bottom)
                c.plot(x, y, SKY if x == x0 + 5 or e > 0.8 else band)


def hedge(c, x0, x1, top, gap=None):
    """A hedge from line `top` to the path, x0 to x1 (whole cells):
    leaves thick all through, bumps of leaves along its top, darker at
    its foot; `gap`: (x, x, line), a gap cut through it."""
    lobes = [(x, top + 6, 8) for x in range(x0, x1 + 8, 8)]
    foliage(c, lobes, base=0.55, macro=(0, 0), outline=None,
            left=x0, right=x1, frame=(0, 0, 1, 1))
    for y in range(top + 8, GROUND_Y):
        for x in range(x0, x1 + 1):
            c.plot(x, y, leaf_colour(x, y, 0.42 if y < GROUND_Y - 8
                                     else 0.3))
    sides = [x0] if gap is None else [x0, gap[0] - 1, gap[1] + 1]
    for side in sides:
        for y in range(top + 6, GROUND_Y):
            if y % 8 in (0, 1, 4):
                c.plot(side, y, SKY)
    if gap is not None:
        c.rect(gap[0], gap[2], gap[1], GROUND_Y - 1, SKY)


def hedge_gate(c, x0):
    """The way out of the wood: a hedge 4 metatiles wide (x0 to
    x0 + 31) with a gap 2 metatiles wide in the middle, from line 96
    to the path, under a bough."""
    hedge(c, x0, x0 + 31, 64, gap=(x0 + 8, x0 + 23, 96))
    c.blit(x0 + 6, 88, ["kkkkkkkkkkkkkkkkkkkk",
                        "bbbbbbbbbbbbbbbbbbbb",
                        "dbbdbbbbdbbbbdbbbbdb",
                        "kddkdddddkdddddkddkk"], PALETTE)


def hedge_doors(c, x0):
    """The gap of hedge_gate(x0) shut: a gate of rough planks, bands
    of dark iron."""
    for y in range(96, GROUND_Y):
        for x in range(x0 + 8, x0 + 24):
            i = x - x0 - 8
            if i % 4 == 3:
                colour = SKY
            elif y in (104, 105, 128, 129):
                colour = GREY if y % 2 == 0 else SKY
            else:
                colour = WOOD if (i % 4 != 2 or y % 3) else GREY
            c.plot(x, y, colour)
