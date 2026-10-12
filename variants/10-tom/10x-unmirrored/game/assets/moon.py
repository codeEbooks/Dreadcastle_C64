"""The moon of the wood and of the mire: a sprite, still in the sky
(and of the mountain and the castle).

The moon is always to be seen:
still in the sky, up on the right,
and well drawn.
A moon drawn in the level's characters
goes by with the level; a moon that stays where it is on the screen
is a sprite. Sprites 0-7 all have their work: in the wood, though,
the enemies are never more than three on the screen (tests/levels.py
checks it), so the program shows three there at most, on sprites
3-5, and sprite 6 is the moon. In the mire (mist and black water:
the night of the wood, the moon still up on
the right) the same. In the village (the setting without a moon)
sprite 6 is the fourth enemy, as before.

The full moon as it is seen from the north: the dark seas in light
grey on the white of the highlands, as they are on the moon itself
(the Sea of Showers and the Ocean of Storms up and down the left,
the Seas of Serenity and of Tranquillity on the right, the Sea of
Crises alone near its right edge, the Seas of Clouds and of Nectar
lower down, the crater Tycho in the bright south); its edge rounded
with light grey. One multicolour block, 11 pixels of the 12 (22
screen pixels) by 21 lines: round on the screen. Its colours:

  W  its own colour ($d02d): white
  G  shared colour 2 ($d026): light grey
  .  nothing (the sky)

In front of the level's characters (the stars and the moths pass
behind it, the crowns of the trees stay lower) and behind the other
sprites: Oscar, the bat, the staff, the enemies; the heirloom,
sprite 7, passes behind it.
"""

OWN_COLOUR = 1                      # white
SETTINGS = ("forest", "marsh", "crags", "pass", "keep",
            "hall")                         # where it is shown
# Where it goes behind the characters ($d01b): in the mountain,
# where the crag over level 5 shuts the sky, the moon is behind it;
# at the castle, behind its high walls (high walls hide the
# moon), and inside, behind the
# walls of the hall, seen in its windows.
BEHIND = ("crags", "keep", "hall")
X_REGISTER = 296                    # screen pixels 272-293
Y_REGISTER = 52                     # lines 2-22 of the playfield
PICTURE = ["....GWG.....",
           "...GWWWG....",
           "..WWWWWWW...",
           "..WGGWGGW...",
           ".GWGGGWWWG..",
           ".WGGGGWGGW..",
           ".GGGGGWGGW..",
           "GGGGGWWWWGW.",
           "WGGGWWGWWGW.",
           "WGGWWWGGGWW.",
           "WGGGWWGGGWW.",
           "WGGGWWWGGWW.",
           "WWGGWWWWGGW.",
           "WWGWGGWGGGW.",
           ".WGWGGWWWW..",
           ".WGGWWWWWW..",
           ".GWWWWWWWG..",
           "..WWGWGWW...",
           "..GWWWWWG...",
           "...GWWWG....",
           "....GWG....."]
BITS = {".": 0b00, "W": 0b10, "G": 0b11}


def block():
    """The sprite's 64 bytes: 21 lines of 3 bytes, multicolour."""
    data = bytearray()
    for row in PICTURE:
        value = 0
        for letter in row:
            value = (value << 2) | BITS[letter]
        data += value.to_bytes(3, "big")
    return bytes(data + b"\0")


def behind_mask(names):
    """For each setting (by name, in order): its bit of $d01b for the
    moon, %01000000 where it goes behind the characters, else 0."""
    return [0b01000000 if name in BEHIND else 0 for name in names]


def settings_mask(names):
    """For each setting (by name, in order): its bit of $d015 for the
    moon, %01000000 where the moon is, else 0."""
    return [0b01000000 if name in SETTINGS else 0 for name in names]
