"""Oscar, drawn for the game: two sprites one over the other.

The colour layer is a multicolour sprite, 12 x 21 pixels two screen
pixels wide:
  P  his own colour ($d028): purple, the cape
  R  shared colour 1 ($d025): red, the lining of the cape, cheeks
  S  shared colour 2 ($d026): light grey, skin and shirt
The line layer is a hi-res sprite, 24 x 21 pixels, in black, drawn
over the colour layer: hair, eyes, mouth and legs (OSCAR_LINES), and
an outline computed from the colour layer (outlined).

Oscar has six pictures, facing right; those facing left are
the same, mirrored:
  stand, walk_a, walk_b, walk_c (the walk: a, b, c, b), jump, fall.
In walk_a and walk_c, the steps, the body is one line lower and
only the shoes show. His black hair has a purple sheen on its edge
(HAIR_SHINE), so that it shows against the night sky.

Oscar turns into a bat: a chubby bat with his colours, his
tuft of black hair with its purple sheen and his fangs. Five pictures,
facing right, then mirrored: fly_a, fly_b, fly_c (wings up, level,
down: the flight goes a, b, c, b), perch (wings folded, like his
cape) and gnam (a moth in his mouth). The bat's claws are on the
last row: the line under them is the line under his feet, as for
Oscar. Three pictures of a puff of smoke
(puff_a, puff_b, puff_c) hide the change: grey clouds with a purple
heart, without an outline; the same both ways.
"""

OSCAR_COLOUR = [
    "............",
    "............",
    "............",
    "............",
    ".....S......",
    ".PSSSSSSSSP.",
    "RPSSSSSSSSPR",
    "RSSSSSSSSSSR",
    "RSSSSSSSSSSR",
    "RSSSSSSSRSSR",
    "RRSSSSSSSSRR",
    ".RRSSSSSSRR.",
    ".PRRSSSSRRP.",
    "PPPRRSSRRPPP",
    "PPRPPSSPPRPP",
    ".PRPPPPPPRP.",
    ".PRPPPPPPRP.",
    "PPRPPPPPPRPP",
    "PRRRRRRRRRRP",
    "P..........P",
    "............",
]

OSCAR_LINES = [
    "......############......",
    "....################....",
    "..####################..",
    "..####################..",
    "..########..##########..",
    "...##......#..#....##...",
    "........................",
    "...........##...##......",
    "...........##...##......",
    "...........#....#.......",
    "........................",
    ".............####.......",
    "..............#.#.......",
    "........................",
    "..........#.............",
    "...........#..#.........",
    "........................",
    "...........#..#.........",
    "........................",
    "........................",
    "........................",
]

# The hair, rows 0-4: '#' black, 'P' the purple sheen (in pairs of
# screen pixels: one multicolour pixel), '.' nothing.
HAIR_SHINE = [
    "......PPPPPPPPPPPP......",
    "....PP############PP....",
    "..PP################PP..",
    "..PP################PP..",
    "..PP######..########PP..",
]

# The legs, rows 19 and 20 of the line layer, for each picture;
# `low`: the body one line lower (only row 20 of the legs shows);
# `hem`: row 19 of the colour layer, the corners of the cape.
PICTURES = {
    "stand":  dict(legs=("##......####.#####....##",
                         ".......###...###........"),
                   low=False, hem="P..........P"),
    "walk_a": dict(legs=("##......####.#####....##",
                         ".....####.......####...."),
                   low=True, hem="P..........P"),
    "walk_b": dict(legs=("##.......######.......##",
                         ".........#####.........."),
                   low=False, hem="P..........P"),
    "walk_c": dict(legs=("##......####.#####....##",
                         "......####....####......"),
                   low=True, hem="P..........P"),
    "jump":   dict(legs=("##......##########....##",
                         "........................"),
                   low=False, hem="PP........PP"),
    "fall":   dict(legs=("##........######......##",
                         ".........###.###........"),
                   low=False, hem="PP........PP"),
}
PICTURE_ORDER = ["stand", "walk_a", "walk_b", "walk_c", "jump", "fall"]

COLOUR_BITS = {".": 0b00, "R": 0b01, "P": 0b10, "S": 0b11}


def sprite_block(rows, bits_per_pixel, codes):
    """64 bytes of a sprite: 21 rows of 3 bytes, then a pad byte."""
    width = 24 // bits_per_pixel
    data = bytearray()
    if len(rows) != 21:
        raise ValueError(f"a sprite has 21 rows, not {len(rows)}")
    for line in rows:
        if len(line) != width:
            raise ValueError(f"row {line!r}: {width} pixels expected")
        value = 0
        for letter in line:
            value = (value << bits_per_pixel) | codes[letter]
        data += value.to_bytes(3, "big")
    return bytes(data + b"\0")


def outlined(details, colour_rows, shine=()):
    """The line layer: the details drawn by hand, plus an outline:
    every screen pixel of the colour layer that touches, left, right,
    above or below, a pixel with neither colour nor detail (or the
    edge of the sprite). The pixels of the sheen get no outline."""
    def solid(x, y):
        return (0 <= x < 24 and 0 <= y < 21
                and (colour_rows[y][x // 2] != "."
                     or details[y][x] == "#"))
    rows = []
    for y in range(21):
        line = ""
        for x in range(24):
            own = colour_rows[y][x // 2] != "." and (x, y) not in shine
            edge = own and not all(
                solid(x + dx, y + dy)
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            line += "#" if edge or details[y][x] == "#" else "."
        rows.append(line)
    return rows


def picture(name):
    """(colour rows, line rows) of one picture, facing right."""
    spec = PICTURES[name]
    colour = list(OSCAR_COLOUR)
    details = list(OSCAR_LINES)
    shine = set()
    for y, row in enumerate(HAIR_SHINE):
        c, d = list(colour[y]), list(details[y])
        for x, letter in enumerate(row):
            if letter == "P":
                if row[x ^ 1] != "P":
                    raise ValueError(f"sheen row {y}: pixel {x} alone")
                c[x // 2] = "P"
                shine.add((x, y))
            d[x] = "#" if letter == "#" else "."
        colour[y], details[y] = "".join(c), "".join(d)
    colour[19] = spec["hem"]
    lines = outlined(details, colour, shine)
    lines[19], lines[20] = spec["legs"]
    if spec["low"]:
        colour = ["." * 12] + colour[:19] + [colour[20]]
        lines = ["." * 24] + lines[:19] + [spec["legs"][1]]
    return colour, lines


def mirrored(colour, lines):
    return [row[::-1] for row in colour], [row[::-1] for row in lines]


def oscar_pictures():
    """The twelve pictures: six facing right, then the same six
    facing left. Each: (colour rows, line rows)."""
    right = [picture(name) for name in PICTURE_ORDER]
    return right + [mirrored(*p) for p in right]


def oscar_blocks():
    """Two blocks for each picture: line layer (hi-res) first, then
    colours. 24 blocks, 1536 bytes."""
    data = bytearray()
    for colour, lines in oscar_pictures():
        data += sprite_block(lines, 1, {".": 0, "#": 1})
        data += sprite_block(colour, 2, COLOUR_BITS)
    return bytes(data)


# The bat. The head, from the tips of the ears: big grey ears, the
# tuft (purple sheen over black), the eyes, the mouth and the fangs.
BAT_HEAD = ["...S....S...",
            "...SSPPSS...",
            "...SPPPPS...",
            "...SSSSSS...",
            "...SSSSSS...",
            "...SSSSSS...",
            "...SSSSSS...",
            "...SSSSSS...",
            "....SSSS...."]
BAT_FACE = ["........................",
            "........................",
            ".........######.........",
            "........................",
            "..........##..##........",
            "..........##..##........",
            "........................",
            "..........######........",
            "..........#.##.#........"]
# gnam: the eyes half shut, the mouth wide open (rows of BAT_FACE).
BAT_GNAM = {4: "........................",
            5: "..........##..##........",
            6: "..........######........",
            7: "..........######........",
            8: "...........####........."}
BAT_BODY = ["...PPPPPP...",
            "...PPPPPP...",
            "....PPPP...."]
BAT_CLAWS = [".........#....#.........",
             "........#.#..#.#........"]
# Perched: the wings folded round him, red inside, like his cape.
BAT_FOLDED = [".PPPPPPPPPP.",
              ".PRPPPPPPRP.",
              ".PRPPPPPPRP.",
              "..PRPPPPRP..",
              "..PP.PP.PP.."]
BAT_FOLDED_CLAWS = [".........#....#........."]
BAT_FOLDED_TIPS = {7: ".P........P.", 8: ".PP......PP."}
# The wings: the first row, counted from the tips of the ears, and
# the rows (the head and the body are drawn over them).
BAT_WINGS = {
    "up": (-4, ["P..........P", "PP........PP", "PRP......PRP",
                "PRR......RRP", "PRR......RRP", ".PRR....RRP.",
                ".PRR....RRP.", "..PRP..PRP..", "..PRP..PRP..",
                "..PRPPPPRP..", "...PP..PP..."]),
    "level": (3, ["PP........PP", "PRP......PRP", "PRRP....PRRP",
                  "PRRR....RRRP", "PRRR....RRRP", ".PRRPPPPRRP.",
                  ".P.PPPPPP.P."]),
    "down": (5, [".P........P.", "PRP......PRP", "PRR......RRP",
                 "PRRP....PRRP", "PRRPPPPPPRRP", "PR.P....P.RP",
                 "P..........P"]),
}
BAT_PICTURES = {"fly_a": "up", "fly_b": "level", "fly_c": "down",
                "perch": None, "gnam": "level"}
BAT_ORDER = ["fly_a", "fly_b", "fly_c", "perch", "gnam"]


def _over(base, top):
    """Row `top` drawn over row `base`: its '.' leave base."""
    return "".join(t if t != "." else b for b, t in zip(base, top))


def bat_picture(name):
    """(colour rows, line rows) of one picture of the bat, facing
    right. The ears' tips are on row 7 in flight, row 6 perched: the
    claws end on row 20."""
    perch = name == "perch"
    top = 6 if perch else 7
    colour = ["." * 12] * 21
    details = ["." * 24] * 21
    wings = BAT_PICTURES[name]
    if wings:
        first, rows = BAT_WINGS[wings]
        for i, row in enumerate(rows):
            colour[top + first + i] = row
    face = dict(enumerate(BAT_FACE))
    if name == "gnam":
        face.update(BAT_GNAM)
    for i, row in enumerate(BAT_HEAD):
        colour[top + i] = _over(colour[top + i], row)
        details[top + i] = face[i]
    body = BAT_FOLDED if perch else BAT_BODY
    claws = BAT_FOLDED_CLAWS if perch else BAT_CLAWS
    for i, row in enumerate(body):
        colour[top + 9 + i] = _over(colour[top + 9 + i], row)
    for i, row in enumerate(claws):
        details[top + 9 + len(body) + i] = row
    if perch:
        for i, row in BAT_FOLDED_TIPS.items():
            colour[top + i] = _over(colour[top + i], row)
    shine = {(x, y) for y in (top + 1, top + 2) for x in range(24)
             if colour[y][x // 2] == "P" and details[y][x] == "."}
    if "#" not in details[20]:
        raise ValueError(f"bat {name}: the claws are not on row 20")
    return colour, outlined(details, colour, shine)


def puff_rows(circles, hearts):
    """A cloud: the wide pixels whose centre is in one of `circles`
    (x, y, radius in screen pixels), grey; in `hearts` (letter,
    circles) another colour on top."""
    rows = [["."] * 12 for _ in range(21)]
    for letter, group in [("S", circles)] + hearts:
        for cx, cy, radius in group:
            for y in range(21):
                for wide in range(12):
                    x = wide * 2 + 1
                    if (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2:
                        rows[y][wide] = letter
    return ["".join(row) for row in rows]


PUFFS = {
    "puff_a": ([(12, 13, 4.5), (8, 15, 3), (16, 15, 3)],
               [("P", [(12, 14, 2.2)])]),
    "puff_b": ([(12, 11, 6.5), (6, 14, 4.5), (18, 14, 4.5),
                (8, 7, 3.5), (16, 6, 3.5), (12, 17, 4)],
               [("P", [(12, 11, 3.8)]), ("R", [(12, 11, 1.8)])]),
    "puff_c": ([(5, 6, 3.6), (19, 5, 3.4), (4, 15, 3.4), (20, 14, 3.6),
                (12, 18, 3.2), (12, 9, 2.4)],
               [("P", [(19, 5, 1.4), (12, 9, 1.2)])]),
}
PUFF_ORDER = ["puff_a", "puff_b", "puff_c"]


def all_pictures():
    """The 25 pictures, in the order of their numbers in the program:
    0-5 Oscar facing right, 6-11 facing left; 12-16 the bat facing
    right, 17-21 facing left; 22-24 the puff."""
    oscar = oscar_pictures()
    bat = [bat_picture(name) for name in BAT_ORDER]
    bat += [mirrored(*p) for p in bat]
    puffs = [(puff_rows(*PUFFS[name]), ["." * 24] * 21)
             for name in PUFF_ORDER]
    return oscar + bat + puffs


def sprite_blocks():
    """Two blocks for each of the 25 pictures: line layer (hi-res)
    first, then colours. 50 blocks, 3200 bytes."""
    data = bytearray()
    for colour, lines in all_pictures():
        data += sprite_block(lines, 1, {".": 0, "#": 1})
        data += sprite_block(colour, 2, COLOUR_BITS)
    return bytes(data)
