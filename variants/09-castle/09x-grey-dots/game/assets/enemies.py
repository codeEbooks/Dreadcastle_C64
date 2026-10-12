"""The enemies: drawn for the game.

Three behaviours, each
with the look of its setting (TYPES):

  the patrol   walks to and fro along its stretch of street: in the
               village the night watchman with his lantern; in the
               wood a werewolf scout of Tom Darkfang's band; in the
               mountain a mountain goat;
  the flyer    flies to and fro across its stretch, up and down on a
               wave, through everything: the crow; the owl; the
               eagle;
  the jumper   sits, and every so often jumps towards Oscar, if he is
               near: the black cat; the giant toad; a werewolf of the
               band, crouching.

Each enemy is one multicolour sprite (sprites 3-6, four on the screen
at most), 12 x 21 pixels two screen pixels wide, standing on its last
row: like Oscar, the enemy's y is the line under its feet. Two
pictures each, facing right; the program has them mirrored too, for
facing left: four blocks a type, at ENEMY_SPRITES, in the order of
TYPES. Colours:

  O  its own colour ($d02a-$d02d, by type): OWN_COLOURS
  R  shared colour 1 ($d025): red, as for Oscar
  G  shared colour 2 ($d026): light grey, as for Oscar
  .  nothing: what is behind

BOXES gives, for each type, the part of its sprite that touches
Oscar: from screen pixel `left` to `right` across the sprite (0-23;
the same from both sides, so that a mirrored picture has the same
box: left + right = 23), from row `top` to row `bottom` (0-20).
"""

KINDS = ("patrol", "flyer", "jumper")
# The types, in the order of their blocks: (name, setting, behaviour).
TYPES = (("watchman", "village", "patrol"),
         ("crow", "village", "flyer"),
         ("cat", "village", "jumper"),
         ("scout", "forest", "patrol"),
         ("owl", "forest", "flyer"),
         ("toad", "forest", "jumper"),
         ("goat", "mountain", "patrol"),
         ("eagle", "mountain", "flyer"),
         ("gangwolf", "mountain", "jumper"),
         ("guard", "castle", "patrol"),
         ("tomcrow", "castle", "flyer"))
# A type that two settings share: in the castle the jumper is
# the werewolf of the band, as in the mountain (the design of the game:
# the band's werewolves are the castle's enemies).
SHARED_TYPES = {("castle", "jumper"): "gangwolf"}
# Their own colours: the watchman orange; the crow and the cat dark
# grey, the black of the night that shows on the black sky and on the
# blue of the low sky (a blue cat did not, in the churchyard). In the
# wood: the werewolf grey, the owl orange, the toad light green.
# In the mountain: the goat white, the eagle brown with a light
# grey head, the werewolf of the band orange-brown. In the castle:
# the werewolf of the guard brown, in a red tabard, a light
# grey helmet and halberd; Tom's crow purple, a red collar.
OWN_COLOURS = {"watchman": 8, "crow": 11, "cat": 11,
               "scout": 12, "owl": 8, "toad": 13,
               "goat": 1, "eagle": 9, "gangwolf": 8,
               "guard": 9, "tomcrow": 4}
BOXES = {"watchman": (6, 17, 1, 20), "crow": (2, 21, 11, 17),
         "cat": (3, 20, 10, 20),
         "scout": (5, 18, 2, 20), "owl": (4, 19, 10, 17),
         "toad": (3, 20, 11, 20),
         "goat": (2, 21, 7, 20), "eagle": (2, 21, 7, 16),
         "gangwolf": (1, 22, 8, 20),
         "guard": (5, 18, 1, 20), "tomcrow": (2, 21, 11, 17)}

PICTURES = {
    # The night watchman: a cap, a big nose, a coat to the knees;
    # the lantern held out in front. Two steps.
    "watchman": [[
        "............",
        "....OOO.....",
        "...OOOOO....",
        "..OOOOOOOO..",
        "...GGGG.....",
        "...G.GGG....",
        "...GGGGRR...",
        "....GGG.....",
        "...OOOOO....",
        "..OOOOOOO...",
        "..OOOOOOGG..",
        "..OOOOOO.GG.",
        "..OOOOOO.RR.",
        "..OOOOOO.RR.",
        "..OOOOOO.GG.",
        "..OOOOOO....",
        "...OOOO.....",
        "...OO.OO....",
        "...OO.OO....",
        "..GGG.GGG...",
        "..GGG.GGG..."], [
        "............",
        "....OOO.....",
        "...OOOOO....",
        "..OOOOOOOO..",
        "...GGGG.....",
        "...G.GGG....",
        "...GGGGRR...",
        "....GGG.....",
        "...OOOOO....",
        "..OOOOOOO...",
        "..OOOOOOGG..",
        "..OOOOOO.GG.",
        "..OOOOOO.RR.",
        "..OOOOOO.RR.",
        "..OOOOOO.GG.",
        "..OOOOOO....",
        "..OOOOOO....",
        "..OO..OO....",
        ".OO....OO...",
        "GGG....GGG..",
        "GGG.....GG.."]],
    # The crow: wings up, wings down; a light grey eye, a red beak.
    "crow": [[
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "...OO.......",
        "....OOO.....",
        ".....OOO....",
        ".....OOOO...",
        "......OOOOO.",
        ".....OOOOGOR",
        "OO..OOOOOORR",
        ".OOOOOOOOO..",
        "..OOOOOOO...",
        "...OOOOO....",
        "....R.R.....",
        "............",
        "............",
        "............"], [
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "......OOOOO.",
        ".....OOOOGOR",
        "OO..OOOOOORR",
        ".OOOOOOOOO..",
        "..OOOOOOOO..",
        "...OOOOOO...",
        "....OOOO....",
        "....OOO.....",
        "....OO......",
        "....O......."]],
    # The black cat: sitting, tail up; jumping, stretched out.
    "cat": [[
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "........O.O.",
        "..O.....OOO.",
        ".O......GOG.",
        ".O......OROO",
        ".O.....OOOO.",
        "..O...OOOOO.",
        "..O..OOOOOO.",
        "...OOOOOOOO.",
        "...OOOOOOOO.",
        "....OOOOOO..",
        "....OOOOOO..",
        "....GG..GG.."], [
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "..........O.",
        "........OOOO",
        "........GOGO",
        "O......OOORO",
        ".O...OOOOOO.",
        "..OOOOOOOOO.",
        "...OOOOOOO..",
        "...OOOOOO...",
        "..OO....OO..",
        ".GG......GG.",
        "............",
        "............"]],
    # The werewolf scout of the band: on two legs, ears up, a red
    # eye, light grey teeth and claws. Two steps.
    "scout": [[
        "............",
        "...O..O.....",
        "...OO.OO....",
        "...OOOOOO...",
        "...OOOROOOO.",
        "...OOOOOOGGO",
        "....OOOOOR..",
        "....OOOO....",
        "..OOOOOOO...",
        ".OOGGGGOOO..",
        ".OO.GGGG.OO.",
        ".OO.GGGG..OG",
        "OO..OOOO..G.",
        "G...OOOO....",
        "....OOOO....",
        "...OOOOOO...",
        "...OO..OO...",
        "...OO...OO..",
        "..OO.....OO.",
        "..GG.....GG.",
        ".GGG....GGG."], [
        "............",
        "...O..O.....",
        "...OO.OO....",
        "...OOOOOO...",
        "...OOOROOOO.",
        "...OOOOOOGGO",
        "....OOOOOR..",
        "....OOOO....",
        "..OOOOOOO...",
        ".OOGGGGOOO..",
        ".OO.GGGG.OO.",
        "OO..GGGG..OG",
        "G...OOOO..G.",
        "....OOOO....",
        "....OOOO....",
        "...OOOOOO...",
        "...OO.OO....",
        "....OOO.....",
        "....OO.O....",
        "...GG..GG...",
        "..GGG.GGG..."]],
    # The owl: big light grey eyes with red pupils, wings up, wings
    # down.
    "owl": [[
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "O..........O",
        "OO.O....O.OO",
        "OOOOO..OOOOO",
        ".OOOOOOOOOO.",
        "..OGGOOGGO..",
        "..OGROORGO..",
        "..OOGORGOO..",
        "...OOROOO...",
        "...OGOGOO...",
        "....OOOO....",
        "....R..R....",
        "............",
        "............",
        "............"], [
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "...O....O...",
        "...OOOOOO...",
        "..OOOOOOOO..",
        ".OOGGOOGGOO.",
        "OOOGROORGOOO",
        "OO.OGRRGO.OO",
        "O..OOOOOO..O",
        "...OGOGOO...",
        "....OOOO....",
        "....R..R....",
        "............",
        "............",
        "............"]],
    # The giant toad: sitting, red eyes up, a light grey belly;
    # jumping, stretched out.
    "toad": [[
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "....OO..OO..",
        "...OROOOORO.",
        "..OOOOOOOOOO",
        ".OOOOOOOOOOO",
        ".OOGGGGGGGGO",
        "OOOOOOOOOOO.",
        "OOOGGGGGOOO.",
        "OOGGGGGGGOO.",
        ".OOGGGGGOOO.",
        "GG.OO..OO.GG"], [
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        ".........OO.",
        "........OROO",
        "......OOOOOO",
        "....OOOOOOOO",
        "..OOOOOOGGG.",
        ".OOOOOGGGG..",
        "OOOGGGGGG...",
        "OO.OO.......",
        "G...OO......",
        "G....GG.....",
        "............",
        "............",
        "............"]],
    # The mountain goat: white, curved horns and a beard of
    # light grey, its hooves light grey; walking, two steps.
    "goat": [[
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "........G...",
        ".......G.G..",
        ".......GOO..",
        "......OOOOO.",
        "......OROOOO",
        ".......OOGG.",
        "..OOOOOOOG..",
        ".OOOOOOOOO..",
        "GOOOOOOOOO..",
        ".OOOOOOOOO..",
        "..OOGGGGO...",
        "..OO...OO...",
        "..O.O..O.O..",
        ".O..O..O..O.",
        ".G..G..G..G."], [
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "........G...",
        ".......G.G..",
        ".......GOO..",
        "......OOOOO.",
        "......OROOOO",
        ".......OOGG.",
        "..OOOOOOOG..",
        ".OOOOOOOOO..",
        "GOOOOOOOOO..",
        ".OOOOOOOOO..",
        "..OOGGGGO...",
        "..OO...OO...",
        "..OO...OO...",
        "..OO...OO...",
        "..GG...GG..."]],
    # The eagle: brown, its head light grey, a red beak and red
    # talons; wings up, wings down.
    "eagle": [[
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "OO..........",
        ".OOO........",
        "..OOOO......",
        "...OOOOO....",
        "....OOOOOGG.",
        "...OOOOOOGGR",
        "OOOOOOOOOG..",
        ".OOOOOOOO...",
        "...OO.......",
        "...R.R......",
        "............",
        "............",
        "............",
        "............"], [
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "......OOOGG.",
        "....OOOOOGGR",
        "OOOOOOOOOG..",
        ".OOOOOOOO...",
        "..OOOOOO....",
        "...OOOOO....",
        "....OOOO....",
        ".....OOO....",
        ".....R.R....",
        "............",
        "............"]],
    # A werewolf of the band: crouching, red eyes, light grey teeth,
    # belly and claws; leaping.
    "gangwolf": [[
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "...O...O....",
        "...OO.OO....",
        "...OOOOOO...",
        "...OROOOOO..",
        "...OOOOOOGG.",
        "....OOOOGGG.",
        "...OOOOOO...",
        "..OOOOOOOO..",
        ".OOOGGGGOOO.",
        ".OOOGGGGOOO.",
        "OOO.OOOO.OOO",
        "OO..OO.OO.OO",
        "GG.GGG..GGGG"], [
        "............",
        "............",
        "............",
        "............",
        "............",
        "........O..O",
        "........OOOO",
        ".......OROOO",
        "......OOOOGG",
        ".....OOOOGGG",
        "...OOOOOOO..",
        "..OOOOGGOO..",
        ".OOOGGGGO...",
        "OOOOGGGOOO..",
        "OO.OOOO..OO.",
        "G...OO....GG",
        "....GG......",
        "............",
        "............",
        "............",
        "............"]],
    # The werewolf of the guard: upright, a helmet, a red
    # tabard with a light grey cross; his halberd held up in front.
    # Two steps.
    "guard": [[
        "..........G.",
        "....GG...GG.",
        "...GGGG..GGG",
        "..GGGGGG..G.",
        "...OOROOO.G.",
        "...OOOOOGGG.",
        "....OOOOR.G.",
        "....OOOO..G.",
        "..RRRRRRR.G.",
        ".ORRRGRRRRG.",
        ".ORRGGGRROGG",
        ".OORRGRRR.G.",
        ".OORRRRRR.G.",
        "OO..RRRR..G.",
        "G...OOOO..G.",
        "...OOOOOO.G.",
        "...OO..OO.G.",
        "...OO...OOG.",
        "..OO.....OO.",
        "..GG.....GG.",
        ".GGG....GGG."], [
        "..........G.",
        "....GG...GG.",
        "...GGGG..GGG",
        "..GGGGGG..G.",
        "...OOROOO.G.",
        "...OOOOOGGG.",
        "....OOOOR.G.",
        "....OOOO..G.",
        "..RRRRRRR.G.",
        ".ORRRGRRRRG.",
        ".ORRGGGRROGG",
        "OORRRGRRR.G.",
        "G.RRRRRRR.G.",
        "...RRRRR..G.",
        "...OOOOO..G.",
        "...OOOOO..G.",
        "...OO.OO..G.",
        "....OOO...G.",
        "....OO.O..G.",
        "...GG..GG...",
        "..GGG.GGG..."]],
    # Tom Darkfang's crow: the crow of the village, tamed, a
    # red collar round its neck. Two beats of its wings.
    "tomcrow": [[
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "...OO.......",
        "....OOO.....",
        ".....OOO....",
        ".....OOOO...",
        "......OOOOO.",
        ".....OORROGR",
        ".....OOOOORR",
        "OO..OOOOOOO.",
        ".OOOOOOOOO..",
        "..OOOOOOO...",
        "...OOOOO....",
        "....R.R.....",
        "............",
        "............",
        "............"], [
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "......OOOOO.",
        ".....OORROGR",
        ".....OOOOORR",
        "OO..OOOOOOO.",
        ".OOOOOOOOO..",
        "..OOOOOOOO..",
        "...OOOOOO...",
        "....OOOO....",
        "....OOO.....",
        "....OO......",
        "....O......."]]
}

BITS = {".": 0b00, "R": 0b01, "O": 0b10, "G": 0b11}


def kind_of(name):
    """The behaviour of a type."""
    return next(kind for type_, _, kind in TYPES if type_ == name)


def type_index(setting, kind):
    """The type of a behaviour in a setting: its index in TYPES (or of
    the type it shares, SHARED_TYPES)."""
    shared = SHARED_TYPES.get((setting, kind))
    if shared is not None:
        return next(i for i, (name, _, _) in enumerate(TYPES)
                    if name == shared)
    return next(i for i, (_, where, k) in enumerate(TYPES)
                if where == setting and k == kind)


def rows_of(name, picture, left=False):
    """The 21 rows of a picture, facing right or (left) mirrored."""
    rows = PICTURES[name][picture]
    if len(rows) != 21 or any(len(row) != 12 for row in rows):
        raise ValueError(f"{name} {picture}: 21 rows of 12 pixels")
    return [row[::-1] for row in rows] if left else list(rows)


def block(rows):
    """The 64 bytes of a sprite."""
    data = bytearray()
    for row in rows:
        value = 0
        for letter in row:
            value = (value << 2) | BITS[letter]
        data += value.to_bytes(3, "big")
    return bytes(data + b"\0")


def boxes():
    """For each type, in the order of TYPES: its box as its left
    pixel and the lines above its feet of its top and of its bottom."""
    found = []
    for name, _, _ in TYPES:
        left, right, top, bottom = BOXES[name]
        if left + right != 23 or not 0 <= top <= bottom <= 20:
            raise ValueError(f"{name}: a box the same from both sides")
        found.append((left, 21 - top, 21 - bottom))
    return found


def blocks():
    """Four blocks a type, in the order of TYPES: the two pictures
    facing right, then the two facing left."""
    data = bytearray()
    for name, _, _ in TYPES:
        for left in (False, True):
            for picture in (0, 1):
                data += block(rows_of(name, picture, left))
    return bytes(data)
