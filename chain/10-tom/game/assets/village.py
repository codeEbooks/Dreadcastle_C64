"""The Village of Mortals at midnight: the pieces of its picture.

Everything here is drawn for the game with simple shapes on a
multicolour canvas (canvas.py). A character cell has the background,
the two shared multicolours and one colour of its own (0-7).

The village is a level of 128 metatile columns, not a single
screen, and a set of characters holds only 192 for its picture: the
level is drawn from pieces that repeat. A piece is drawn at any place
of the canvas (x in multicolour pixels, y in lines), and two copies of
it share their characters when they stand on the same grid: walls,
windows and doors on the grid of the cells (x a multiple of 4, y of
8), whole houses on the grid of the metatiles (x a multiple of 8). The
patterns (bricks, tiles, cobbles, plaster, sky) repeat every cell or
every metatile wherever they are. The pieces of the first scene
are the same drawings as then, moved where the level wants them; the
new ones (stalls, crates, the loaded cart, the canal, the well, the
fountain, the lantern, the gate) follow their style.
"""

from canvas import CELL_H, CELL_W

# Colours of the village (C64 colour numbers).
BACKGROUND = 0      # $d021: the night sky, outlines and shadows
OPEN_SKY = 16       # not a C64 colour: sky still to be painted
SHARED_1 = 11       # $d022: dark grey, stone
SHARED_2 = 9        # $d023: brown, wood
BLUE, PURPLE, RED, YELLOW, WHITE, GREEN, CYAN = 6, 4, 2, 7, 1, 5, 3
SHARED = {BACKGROUND, SHARED_1, SHARED_2}

STONE, WOOD, SKY = SHARED_1, SHARED_2, BACKGROUND
GROUND_Y = 144      # the street: the first line of cell row 18


class Shifted:
    """A canvas seen from `dx` pixels further right: the drawings of
    the first scene, made for one screen, land anywhere in a level."""

    def __init__(self, canvas, dx):
        self.canvas, self.dx = canvas, dx

    def plot(self, x, y, colour):
        self.canvas.plot(x + self.dx, y, colour)

    def rect(self, x0, y0, x1, y1, colour):
        self.canvas.rect(x0 + self.dx, y0, x1 + self.dx, y1, colour)

    def hline(self, x0, x1, y, colour):
        self.rect(x0, y, x1, y, colour)

    def vline(self, x, y0, y1, colour):
        self.rect(x, y0, x, y1, colour)

    def ellipse(self, cx, cy, rx, ry, colour):
        self.canvas.ellipse(cx + self.dx, cy, rx, ry, colour)

    def blit(self, x0, y0, rows, palette):
        self.canvas.blit(x0 + self.dx, y0, rows, palette)


def own_colour_in(canvas, col, row):
    found = canvas.cell_colours(col, row) - SHARED - {OPEN_SKY}
    return next(iter(found)) if found else None


def sky(c):
    """The open sky: black, with blue light near the horizon, denser
    lower down. Only in cells without another colour of their own."""
    for y in range(c.height):
        for x in range(c.width):
            if c.get(x, y) != OPEN_SKY:
                continue
            c.plot(x, y, BACKGROUND)
            if y < 72 or own_colour_in(c, x // CELL_W, y // CELL_H) \
                    not in (None, BLUE):
                continue
            band = (y - 72) // 8
            if band == 0:
                on = y % 4 == 0 and (x + y // 4) % 4 == 0
            elif band == 1:
                on = y % 2 == 0 and x % 2 == 0
            elif band == 2:
                on = (x + y) % 2 == 0
            elif band == 3:
                on = not (x % 2 and y % 2)
            else:
                on = True
            if on:
                c.plot(x, y, BLUE)


def distant_roofs(c, x_from=0, x_to=None):
    """Houses far away, two shapes repeated every 16 pixels."""
    x_to = c.width if x_to is None else x_to
    for left in range(x_from, x_to, 16):
        for (x0, peak, window) in ((left, 100, True),
                                   (left + 8, 108, False)):
            wall = peak + 8
            for y in range(peak, wall):
                half = (y - peak) // 2
                c.hline(x0 + 3 - half, x0 + 4 + half, y, WOOD)
                c.plot(x0 + 3 - half, y, SKY)
                c.plot(x0 + 4 + half, y, SKY)
            c.rect(x0, wall, x0 + 7, 143, STONE)
            c.hline(x0, x0 + 7, wall, SKY)
            c.vline(x0 + 7, wall, 143, SKY)
            if window:
                c.rect(x0 + 3, 124, x0 + 4, 126, YELLOW)


def moon(c):
    """A full moon: 2 x 2 metatiles, white with grey seas."""
    c.ellipse(123, 15, 6, 13, WHITE)
    for (cx, cy, rx, ry) in ((121, 10, 1, 3), (126, 17, 1, 2),
                             (120, 21, 1, 2), (125, 7, 0, 1)):
        c.ellipse(cx, cy, rx, ry, STONE)


def roof(c, centre, base_y, half_base):
    """Red tiles: a 45-degree slope in multicolour pixels (one pixel
    each line), courses every 4 lines, joints every 4 pixels."""
    apex_y = base_y - half_base
    for y in range(apex_y, base_y + 1):
        half = y - apex_y
        left, right = centre - half, centre + 1 + half
        for x in range(left, right + 1):
            if y % 4 == 3 or (x + (y // 4) * 2) % 4 == 0:
                colour = SKY
            else:
                colour = RED
            c.plot(x, y, colour)
        c.plot(left, y, WOOD)
        c.plot(right, y, WOOD)
    c.rect(centre - half_base - 1, base_y + 1, centre + half_base + 2,
           base_y + 3, WOOD)


def timber_walls(c, x0, x1, top, posts, beams):
    """Plaster (purple) between posts and beams of wood."""
    c.rect(x0, top, x1, GROUND_Y - 1, PURPLE)
    for x in posts:
        c.rect(x, top, x + 1, GROUND_Y - 1, WOOD)
    for y in beams:
        c.rect(x0, y, x1, y + 2, WOOD)


def window(c, col, row, rows=2):
    """A lit window that fills whole cells: 2 cells wide."""
    x0, y0 = col * CELL_W, row * CELL_H
    x1, y1 = x0 + 2 * CELL_W - 1, y0 + rows * CELL_H - 1
    c.rect(x0, y0, x1, y1, WOOD)
    c.rect(x0 + 1, y0 + 2, x1 - 1, y1 - 2, YELLOW)
    c.vline((x0 + x1) // 2, y0 + 2, y1 - 2, SKY)
    c.hline(x0 + 1, x1 - 1, (y0 + y1) // 2, SKY)
    c.hline(x0, x1, y1, SKY)


def flower_box(c, col, row):
    x0, y0 = col * CELL_W, row * CELL_H
    c.rect(x0, y0, x0 + 7, y0 + 7, SKY)
    c.rect(x0, y0 + 3, x0 + 7, y0 + 6, WOOD)
    for x in range(x0, x0 + 8, 2):
        c.rect(x, y0 + 1, x, y0 + 2, GREEN)
        c.plot(x + 1, y0, GREEN)


def door(c, col, row, rows=3):
    """A wooden door, 2 cells wide, with a lit knob."""
    x0, y0 = col * CELL_W, row * CELL_H
    x1, y1 = x0 + 7, y0 + rows * CELL_H - 1
    c.rect(x0, y0, x1, y1, SKY)
    c.rect(x0 + 1, y0 + 3, x1 - 1, y1, WOOD)
    c.rect(x0 + 2, y0 + 1, x1 - 2, y0 + 2, WOOD)
    for x in range(x0 + 2, x1, 2):
        c.vline(x, y0 + 4, y1, SKY)
    c.plot(x1 - 2, (y0 + y1) // 2 + 2, YELLOW)


def chimney(c, col, top_row, rows):
    x0, y0 = col * CELL_W, top_row * CELL_H
    c.rect(x0, y0, x0 + 3, y0 + rows * CELL_H - 1, STONE)
    for y in range(y0 + 3, y0 + rows * CELL_H, 4):
        c.hline(x0, x0 + 3, y, SKY)
    c.rect(x0, y0, x0 + 3, y0 + 1, WOOD)


def left_house(c):
    """Cells 0-11: two floors, window boxes, a door."""
    timber_walls(c, 0, 47, 80, posts=(0, 22, 46), beams=(80, 112))
    chimney(c, 8, 7, 2)
    roof(c, 23, 79, 25)
    window(c, 2, 12)
    window(c, 7, 12)
    window(c, 1, 15)
    flower_box(c, 1, 17)
    door(c, 6, 15)
    window(c, 9, 15)
    flower_box(c, 9, 17)


def right_house(c):
    """Cells 26-39 and beyond: a balcony on the first floor."""
    timber_walls(c, 104, 159, 72, posts=(104, 126, 146),
                 beams=(72, 112))
    chimney(c, 36, 5, 3)
    roof(c, 131, 71, 29)
    for col in (28, 33, 37):
        window(c, col, 10)
    c.rect(104, 104, 143, 105, WOOD)        # the balcony rail
    for x in range(105, 143, 4):
        c.vline(x, 106, 111, WOOD)
    door(c, 30, 15)
    window(c, 34, 15)
    flower_box(c, 34, 17)
    window(c, 38, 15)


def tower(c):
    """The clock tower of the square, showing midnight."""
    x0, x1 = 66, 85
    c.rect(x0 - 2, 44, x1 + 2, GROUND_Y - 1, SKY)
    for y in range(44, GROUND_Y):          # bricks, 4 x 4 pixels
        for x in range(x0, x1 + 1):
            joint = y % 4 == 3 or (x + (y // 4) * 2) % 4 == 3
            c.plot(x, y, SKY if joint else STONE)
    c.rect(x0 - 2, 40, x1 + 2, 43, WOOD)   # cornice
    for y in range(15, 40):                 # spire of blue slate
        half = (y - 15) // 2
        for x in range(75 - half, 76 + half + 1):
            c.plot(x, y, SKY if y % 4 == 3 else BLUE)
        c.plot(75 - half, y, WOOD)
        c.plot(76 + half, y, WOOD)
    c.rect(75, 8, 76, 14, YELLOW)           # a golden bat on top
    c.blit(72, 3, ["y......y",
                   "yyy..yyy",
                   ".yyyyyy.",
                   "...yy..."], {"y": YELLOW})
    # the clock: midnight, both hands up
    c.ellipse(75, 63, 8, 16, WOOD)
    c.ellipse(75, 63, 7, 14, WHITE)
    for (x, y) in ((75, 51), (75, 75), (69, 63), (81, 63),
                   (72, 53), (78, 53), (72, 73), (78, 73)):
        c.plot(x, y, STONE)
    c.rect(75, 53, 75, 63, SKY)
    c.rect(76, 57, 76, 63, SKY)
    c.plot(75, 64, STONE)
    # a lit slit window, the door
    c.rect(74, 92, 77, 103, SKY)
    c.rect(75, 93, 76, 102, YELLOW)
    c.rect(70, 116, 81, GROUND_Y - 1, SKY)
    c.rect(71, 119, 80, GROUND_Y - 1, WOOD)
    c.rect(72, 117, 79, 118, WOOD)
    for x in range(72, 80, 2):
        c.vline(x, 121, GROUND_Y - 1, SKY)


def lamp(c):
    """The street lamp of the square: the lit lantern, on
    the grid of the metatiles (cells 24-25, a pixel to the left of
    first scene's lamp), so that the two share their characters."""
    lantern(c, 96, True)


def cart(c):
    """The merchant's cart, and the empty potato sack."""
    c.rect(47, 121, 63, 131, SKY)
    c.rect(48, 122, 62, 130, WOOD)
    for y in (124, 127):
        c.hline(48, 62, y, SKY)
    c.ellipse(53, 136, 4, 8, SKY)
    c.ellipse(53, 136, 3, 7, WOOD)
    c.ellipse(53, 136, 2, 5, SKY)
    c.vline(53, 130, 142, STONE)
    c.hline(51, 55, 136, STONE)
    # the sack, empty, lying on the cart
    c.ellipse(57, 115, 5, 7, SKY)
    c.ellipse(57, 115, 4, 6, WOOD)
    for (x, y) in ((55, 112), (58, 117), (56, 119), (59, 111),
                   (60, 114), (54, 116)):
        c.plot(x, y, STONE)
    c.rect(52, 107, 54, 110, SKY)
    c.rect(53, 108, 54, 109, WOOD)


def street(c):
    """The street: a kerb, then cobbles in courses of 8 lines; the
    pattern repeats every metatile (8 x 16 pixels)."""
    c.rect(0, GROUND_Y, c.width - 1, c.height - 1, SKY)
    for x in range(c.width):                # the kerb
        for y in range(GROUND_Y, GROUND_Y + 4):
            if x % 8 == 7:
                continue
            c.plot(x, y, BLUE if y == GROUND_Y else STONE)
    for y in range(GROUND_Y + 8, c.height):
        course = (y - GROUND_Y) // 8
        line = (y - GROUND_Y) % 8
        if line == 7:
            continue                        # mortar between courses
        for x in range(c.width):
            stone = x + (4 if course % 2 else 0)
            inside = stone % 8
            if inside == 7:
                continue                    # mortar between stones
            if line in (0, 6) and inside in (0, 6):
                continue                    # round corners
            colour = STONE
            if (stone // 8 + course) % 3 == 0:
                colour = WOOD               # an older, darker stone
            if line == 1 and 1 <= inside <= 3:
                colour = BLUE               # moonlight on the top
            c.plot(x, y, colour)


STAR_PATTERNS = {
    "dot": bytes([0, 0, 0, 0b00010000, 0, 0, 0, 0]),
    "cross": bytes([0, 0b00010000, 0b00010000, 0b01101100,
                    0b00010000, 0b00010000, 0, 0]),
}


def stars(c, stars_list):
    """Stars: (cell column, cell row, pattern, colour), hi-res cells
    of the open sky."""
    for col, row, pattern, colour in stars_list:
        if c.cell_colours(col, row) != {BACKGROUND}:
            raise ValueError(f"star at {col},{row} is not in clear sky")
        c.hires[(col, row)] = (STAR_PATTERNS[pattern], colour)


# The surfaces of the first scene, in screen pixels of
# that screen (0-319): the street, the lamp, the balcony, the two
# roofs and the spire. Each is {x: y}, y the first line of the
# object, where Oscar's feet go.
def roof_line(centre, base_y, half_base):
    """The top edge of roof(): one line up for each multicolour
    pixel towards the two pixels of the ridge."""
    apex_y = base_y - half_base
    line = {}
    for x in range(centre - half_base, centre + 2 + half_base):
        rise = centre - x if x <= centre else x - centre - 1
        for sx in (2 * x, 2 * x + 1):
            line[sx] = apex_y + rise
    return line


def spire_line():
    """The top edge of the spire of tower(): two lines a pixel."""
    line = {}
    for x in range(63, 89):
        half = 75 - x if x <= 75 else x - 76
        for sx in (2 * x, 2 * x + 1):
            line[sx] = 15 + 2 * half
    return line


def flat(x0, x1, y):
    return {sx: y for sx in range(x0, x1 + 1)}


def first_scene_surfaces():
    """The surfaces of left_house, right_house, tower and lamp, as
    in the first scene (the cart has its own, cart_surface)."""
    return [
        ("left roof", roof_line(23, 79, 25), {WOOD}),
        ("right roof", roof_line(131, 71, 29), {WOOD}),
        ("spire", spire_line(), {WOOD}),
        ("lamp", flat(196, 203, 112), {STONE}),
        ("balcony", flat(208, 287, 104), {WOOD}),
    ]


def cart_surface():
    return flat(96, 125, 122)


# --- New pieces for the level -------------------------------------
# x in multicolour pixels, y in lines; a metatile is 8 x 16.

def house(c, x0, width, top, windows=(), doors=(), boxes=(),
          chimney_at=None):
    """A timber house of `width` pixels (a multiple of 8) from x0,
    its wall from line `top` (a multiple of 8) to the street; posts
    at its two ends, beams at the top and on line 112. windows,
    doors, boxes: cell columns from x0 / 4 (and cell rows)."""
    x1 = x0 + width - 1
    timber_walls(c, x0, x1, top, posts=(x0, x1 - 1), beams=(top, 112))
    if chimney_at is not None:
        chimney(c, x0 // CELL_W + chimney_at[0], chimney_at[1],
                chimney_at[2])
    centre = x0 + width // 2 - 1
    roof(c, centre, top - 1, width // 2 + 1)
    base = x0 // CELL_W
    for col, row in windows:
        window(c, base + col, row)
    for col, row in doors:
        door(c, base + col, row)
    for col, row in boxes:
        flower_box(c, base + col, row)
    return roof_line(centre, top - 1, width // 2 + 1)


def stall(c, x0, width, goods):
    """A market stall, x0 and width multiples of 4: an awning in red
    and brown stripes (its top on line 96), dark inside, two posts,
    a counter with goods of the colour `goods`, one in each cell."""
    x1 = x0 + width - 1
    c.rect(x0, 96, x1, GROUND_Y - 1, SKY)
    for y in range(97, 104):                # the awning
        for x in range(x0, x1 + 1):
            c.plot(x, y, RED if x % 4 < 2 else WOOD)
    c.hline(x0, x1, 96, WOOD)
    for x in range(x0, x1 + 1, 4):          # its scalloped edge
        c.rect(x, 104, x + 1, 105, RED)
    for x in (x0 + 1, x1 - 1):              # the posts
        c.rect(x, 106, x, GROUND_Y - 1, WOOD)
    c.rect(x0, 120, x1, 122, WOOD)          # the counter
    for x in range(x0 + 4, x1 - 3, 4):      # goods on it
        c.rect(x + 1, 115, x + 2, 119, goods)
        c.rect(x, 117, x + 3, 118, goods)
    return flat(2 * x0, 2 * x1 + 1, 96)


def crate(c, x0, y0):
    """A wooden crate: a metatile, 8 x 16 pixels."""
    c.rect(x0, y0, x0 + 7, y0 + 15, SKY)
    c.rect(x0, y0, x0 + 6, y0 + 14, WOOD)
    for y in (y0 + 4, y0 + 9):
        c.hline(x0, x0 + 6, y, SKY)
    c.rect(x0 + 1, y0 + 1, x0 + 1, y0 + 13, STONE)
    c.rect(x0 + 5, y0 + 1, x0 + 5, y0 + 13, STONE)


def crates(c, x0, columns, rows):
    """A pile of crates, `columns` wide and `rows` high, standing on
    the street from x0 (a multiple of 8)."""
    for col in range(columns):
        for row in range(rows):
            crate(c, x0 + col * 8, GROUND_Y - 16 * (row + 1))


def hole(c, x0, width):
    """An open trapdoor in the street: black down to the bottom,
    a stone rim on its two sides."""
    c.rect(x0, GROUND_Y, x0 + width - 1, c.height - 1, SKY)
    c.rect(x0, GROUND_Y, x0, GROUND_Y + 3, STONE)
    c.rect(x0 + width - 1, GROUND_Y, x0 + width - 1, GROUND_Y + 3,
           STONE)


def canal(c, x0, width):
    """Running water, sunk below the street between two walls of
    stone: from line 152 to the bottom. Blue, with dark ripples and
    grey glints of the moon; the pattern repeats every cell."""
    x1 = x0 + width - 1
    c.rect(x0, GROUND_Y, x1, c.height - 1, SKY)
    for y in range(152, c.height - 1):      # the last line: black
        for x in range(x0, x1 + 1):
            ripple = (x + y // 2) % 4
            if y % 4 == 0 and ripple == 0:
                colour = STONE              # a glint of the moon
            elif y % 2 == 1 and ripple == 2:
                colour = SKY
            else:
                colour = BLUE
            c.plot(x, y, colour)
    c.rect(x0, GROUND_Y, x0, c.height - 2, STONE)
    c.rect(x1, GROUND_Y, x1, c.height - 2, STONE)


def well(c, x0):
    """A stone well: 2 x 2 metatiles from x0 (a multiple of 8), its
    rim of wood on line 112; the bricks of the tower."""
    for y in range(112, GROUND_Y):          # stones, 4 x 4
        for x in range(x0, x0 + 16):
            joint = y % 4 == 3 or (x + (y // 4) * 2) % 4 == 3
            c.plot(x, y, SKY if joint else STONE)
    c.rect(x0, 112, x0 + 15, 114, WOOD)
    c.hline(x0, x0 + 15, 115, SKY)


def fountain(c, x0):
    """A fountain: a stone basin (its rim on line 128) 2 metatiles
    wide, a jet of water above it."""
    c.rect(x0, 128, x0 + 15, GROUND_Y - 1, STONE)
    c.hline(x0, x0 + 15, 128, WOOD)
    c.rect(x0 + 1, 130, x0 + 14, 132, CYAN)
    for y in (133, 138):
        c.hline(x0, x0 + 15, y, SKY)
    c.rect(x0 + 7, 112, x0 + 8, 127, CYAN)  # the jet
    for (x, y) in ((x0 + 5, 116), (x0 + 10, 116), (x0 + 4, 121),
                   (x0 + 11, 121), (x0 + 6, 113), (x0 + 9, 113)):
        c.plot(x, y, CYAN)
    return flat(2 * x0, 2 * x0 + 31, 128)


def lantern(c, x0, lit):
    """The lantern of the checkpoint: a post and a head, like the
    street lamp; dark, or lit (yellow)."""
    c.rect(x0, 111, x0 + 7, 125, SKY)
    c.rect(x0 + 3, 124, x0 + 4, GROUND_Y - 1, STONE)
    c.rect(x0 + 2, 140, x0 + 5, GROUND_Y - 1, STONE)
    c.rect(x0 + 2, 112, x0 + 5, 112, STONE)
    c.rect(x0 + 1, 113, x0 + 6, 121, STONE)
    c.rect(x0 + 2, 114, x0 + 5, 120, YELLOW if lit else SKY)
    if not lit:
        c.rect(x0 + 3, 116, x0 + 4, 118, BLUE)
    c.rect(x0 + 1, 122, x0 + 6, 123, STONE)
    return flat(2 * x0 + 4, 2 * x0 + 11, 112)


def gate(c, x0):
    """The gate of the village: a stone gatehouse 4 metatiles wide
    (x0 to x0 + 31), its arch 2 metatiles wide in the middle, from
    line 96 to the street; a roof of tiles on top."""
    for y in range(64, GROUND_Y):           # stones
        for x in range(x0, x0 + 32):
            joint = y % 4 == 3 or (x + (y // 4) * 2) % 4 == 3
            c.plot(x, y, SKY if joint else STONE)
    roof(c, x0 + 15, 63, 17)
    c.rect(x0 + 8, 96, x0 + 23, GROUND_Y - 1, SKY)   # the arch
    for y in range(92, 96):
        c.hline(x0 + 8 + (95 - y), x0 + 23 - (95 - y), y, SKY)
    c.rect(x0 + 12, 74, x0 + 19, 85, SKY)   # a window above
    c.rect(x0 + 13, 76, x0 + 18, 84, YELLOW)
    c.vline(x0 + 15, 76, 84, SKY)
    c.vline(x0 + 16, 76, 84, SKY)
    return roof_line(x0 + 15, 63, 17)


def gate_doors(c, x0):
    """The two closed doors in the arch of gate(x0): planks of wood,
    iron bands."""
    c.rect(x0 + 8, 96, x0 + 23, GROUND_Y - 1, WOOD)
    for x in range(x0 + 9, x0 + 24, 2):
        c.vline(x, 98, GROUND_Y - 1, SKY)
    for y in (104, 120, 136):
        c.hline(x0 + 8, x0 + 23, y, STONE)


def balcony(c, x0, width, y):
    """A wooden balcony on a facade: rail on line y, bars under it
    for 8 lines."""
    c.rect(x0, y, x0 + width - 1, y + 1, WOOD)
    for x in range(x0 + 1, x0 + width - 1, 4):
        c.vline(x, y + 2, y + 7, WOOD)
    c.hline(x0, x0 + width - 1, y + 8, WOOD)
    return flat(2 * x0, 2 * (x0 + width) - 1, y)


# --- The churchyard (level 2) ------------------------------------------
# The same set of characters as the village (one set for the two
# levels of the village): the pieces reuse the bricks, the rims, the
# roofs, the windows and the doors of level 1, and add a few of their
# own. Behind them no distant houses: the open sky, with its blue
# light near the horizon.

def stone_wall(c, x0, x1, top, bottom=GROUND_Y - 1):
    """Stone bricks of 4 x 4 pixels, as the tower's and the well's:
    the pattern repeats every cell."""
    for y in range(top, bottom + 1):
        for x in range(x0, x1 + 1):
            joint = y % 4 == 3 or (x + (y // 4) * 2) % 4 == 3
            c.plot(x, y, SKY if joint else STONE)


def rim(c, x0, x1, y):
    """The wooden rim of the well, on line y (a multiple of 16)."""
    c.rect(x0, y, x1, y + 2, WOOD)
    c.hline(x0, x1, y + 3, SKY)


def stone_block(c, x0, width, top):
    """A block of stone with a rim on top: the well's picture, any
    width (a multiple of 8) and height (top a multiple of 16)."""
    stone_wall(c, x0, x0 + width - 1, top)
    rim(c, x0, x0 + width - 1, top)
    return flat(2 * x0, 2 * (x0 + width) - 1, top)


def plaque(c, x0, y0):
    """A dark plaque with a carved cross: one cell, on a stone
    block."""
    c.rect(x0, y0, x0 + 3, y0 + 7, SKY)
    c.vline(x0 + 1, y0 + 1, y0 + 6, STONE)
    c.vline(x0 + 2, y0 + 1, y0 + 6, STONE)
    c.hline(x0, x0 + 3, y0 + 3, STONE)


def church(c, x0, width, top, windows=(), doors=()):
    """The nave of the church: stone walls from line `top` to the
    street, a roof of tiles as the houses' (the same roof as a house
    of the same width), windows and doors in cell columns from x0 /
    4. Returns the roof's line."""
    x1 = x0 + width - 1
    stone_wall(c, x0, x1, top)
    centre = x0 + width // 2 - 1
    roof(c, centre, top - 1, width // 2 + 1)
    base = x0 // CELL_W
    for col, row in windows:
        window(c, base + col, row)
    for col, row in doors:
        door(c, base + col, row)
    return roof_line(centre, top - 1, width // 2 + 1)


def tombstone(c, x0):
    """A tombstone: a metatile of grey stone on the street (lines
    128-143), rounded on top, a cross carved in it."""
    c.blit(x0, 128, ["..SSSS..",
                     ".SSSSSS.",
                     ".SSSKSS.",
                     ".SSKKKS.",
                     ".SSSKSS.",
                     ".SSSKSS.",
                     ".SSSSSS.",
                     ".SSSSSS.",
                     ".SSSSSS.",
                     ".SSSSSS.",
                     ".SSSSSS.",
                     ".SSSSSS.",
                     "SSSSSSSS",
                     "SWWWWWWS",
                     "SSSSSSSS",
                     "KKKKKKKK"],
           {"S": STONE, "K": SKY, "W": WOOD})


def wooden_cross(c, x0):
    """A wooden cross on a grave, behind: one cell wide (x0 a
    multiple of 4), lines 124-143."""
    c.blit(x0, 124, [".WW.",
                     ".WW.",
                     "WWWW",
                     ".WW.",
                     ".WW.",
                     ".WW.",
                     ".WW.",
                     ".WW.",
                     ".WW.",
                     ".WW.",
                     ".WW.",
                     ".WW.",
                     ".WW.",
                     ".WW.",
                     ".WW.",
                     ".WW.",
                     "SWWS",
                     "SSSS",
                     "SSSS",
                     "KKKK"],
           {"W": WOOD, "S": STONE, "K": SKY})


def bell_cote(c, x0):
    """The bell-cote on the chapel's roof: a metatile wide (x0 a
    multiple of 8), stone from line 40 to 95, an arch with a golden
    bell, a slate cap from line 24."""
    stone_wall(c, x0, x0 + 7, 40, 95)
    c.rect(x0 + 2, 48, x0 + 5, 71, SKY)          # the arch
    c.hline(x0 + 3, x0 + 4, 47, SKY)
    c.blit(x0 + 2, 54, [".YY.",
                        "YYYY",
                        "YYYY",
                        "YYYY",
                        "YYYY",
                        "YYYY",
                        "..Y."],
           {"Y": YELLOW})
    c.vline(x0 + 3, 49, 53, WOOD)               # the rope
    for y in range(24, 40):                     # the cap, as the spire
        half = (y - 24) // 4
        for x in range(x0 + 3 - half, x0 + 5 + half):
            c.plot(x, y, SKY if y % 4 == 3 else BLUE)
        c.plot(x0 + 3 - half, y, WOOD)
        c.plot(x0 + 4 + half, y, WOOD)


def chapel(c, x0, width, windows=(), doors=()):
    """The chapel: a solid block of stone from line 96 (3 metatiles
    high), x0 and width multiples of 8, with the well's rim on top,
    lit windows and a door; the bell-cote in its middle."""
    stone_block(c, x0, width, 96)
    base = x0 // CELL_W
    for col, row in windows:
        window(c, base + col, row)
    for col, row in doors:
        door(c, base + col, row)
    bell_cote(c, x0 + width // 2 - 4)


def bridge_pile(c, x0):
    """A pile of the broken bridge, in the stream: 2 metatiles
    wide (x0 a multiple of 8), a deck of planks on line 144 and two
    posts down to the bottom."""
    for x in (x0 + 1, x0 + 12):
        c.rect(x, 148, x + 2, c.height - 2, WOOD)
        c.vline(x + 3, 148, c.height - 2, SKY)
    c.rect(x0, GROUND_Y, x0 + 15, GROUND_Y + 2, WOOD)
    c.hline(x0, x0 + 15, GROUND_Y + 3, SKY)
    for x in range(x0 + 3, x0 + 16, 4):
        c.vline(x, GROUND_Y + 1, GROUND_Y + 2, SKY)
    return flat(2 * x0, 2 * x0 + 31, GROUND_Y)


def angel(c, x0):
    """The statue of an angel on its pedestal: the pedestal is a
    stone block 2 metatiles wide (x0 a multiple of 8) from line 112;
    the angel, of grey stone, stands on it, wings open."""
    line = stone_block(c, x0, 16, 112)
    c.blit(x0 + 2, 76, ["....SS......",
                        "...SSSS.....",
                        "...SSSS.....",
                        "....SS......",
                        "S...SS.....S",
                        "SS.SSSS...SS",
                        "SSSSSSSS.SSS",
                        ".SSSSSSSSSS.",
                        "..SSSSSSSS..",
                        "...SSSSSS...",
                        "....SSSS....",
                        "....SSSS....",
                        "....SSSS....",
                        "....SSSS....",
                        "...SSSSSS...",
                        "...SSSSSS...",
                        "...SSSSSS...",
                        "..SSSSSSSS..",
                        "..SSSSSSSS..",
                        "..SSSSSSSS..",
                        "..SSSSSSSS..",
                        ".SSSSSSSSSS.",
                        ".SSSSSSSSSS.",
                        ".SSSSSSSSSS.",
                        "SSSSSSSSSSSS",
                        "SSSSSSSSSSSS",
                        "SSSSSSSSSSSS",
                        "SSSSSSSSSSSS",
                        "SSSSSSSSSSSS",
                        "SSSSSSSSSSSS",
                        "SSSSSSSSSSSS",
                        "SSSSSSSSSSSS",
                        "SSSSSSSSSSSS",
                        "SSSSSSSSSSSS",
                        "SSSSSSSSSSSS",
                        "KKKKKKKKKKKK"],
           {"S": STONE, "K": SKY})
    return line


def cemetery_wall(c, x0, width, top):
    """The wall round the churchyard: stone from line `top` (a
    multiple of 16) to the street, the rim on top. Oscar walks along
    its top, and in front of it on the street."""
    return stone_block(c, x0, width, top)
