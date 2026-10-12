"""The moth, the bat's food: drawn for the game.

A moth is two multicolour characters side by side (8 x 8 pixels two
screen pixels wide), in the upper half of its metatile. It has two
pictures, wings open and wings raised: the program copies one or the
other over the two characters of the character set every 8 frames,
so all the moths on the screen flutter together.

  W  its own colour: white, the wings
  G  shared colour 1 ($d022): dark grey, the spots
  B  shared colour 2 ($d023): brown, the body and the feelers
"""

OWN_COLOUR = 1                      # white
FRAMES = [
    ["..B..B..",
     "WW.BB.WW",
     "WWWBBWWW",
     "WGWBBWGW",
     ".WWBBWW.",
     "..W..W..",
     "........",
     "........"],
    ["..B..B..",
     ".W.BB.W.",
     ".WWBBWW.",
     ".WWBBWW.",
     "..GBBG..",
     "...BB...",
     "........",
     "........"],
]
BITS = {".": 0b00, "G": 0b01, "B": 0b10, "W": 0b11}


def characters(frame):
    """The 16 bytes of one picture: the left character, then the
    right one."""
    rows = FRAMES[frame]
    if len(rows) != 8 or any(len(row) != 8 for row in rows):
        raise ValueError("a moth is 8 x 8")
    data = bytearray()
    for half in (0, 4):
        for row in rows:
            value = 0
            for letter in row[half:half + 4]:
                value = (value << 2) | BITS[letter]
            data.append(value)
    return bytes(data)


def frames():
    """Both pictures, 32 bytes: what the program copies from."""
    return characters(0) + characters(1)
