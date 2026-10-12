"""Tom Darkfang: drawn for the game.

The leader of the band of werewolves that holds Dreadcastle waits for
Oscar in the throne room, the arena at the end of level 8: the big
hunched werewolf of the book's frontispiece and cover,
brown fur, the
muzzle, the chest and the claws light grey, the eyes and the mouth
red; bigger than the werewolves of his band.

Tom is four multicolour sprites, two across and two down: 48 x 42
screen pixels, twice Oscar's size (sprites 3-6
in the fight, no other enemy; the program uses 3, 4, 5 and 7, so that
the moon stays sprite 6). A picture is 24 pixels two screen pixels
wide by 42 rows, standing on its last row: like Oscar, Tom's y is the
line under his feet. Colours:

  O  his own colour ($d02a-$d02c, $d02e): brown
  R  shared colour 1 ($d025): red, as for Oscar
  G  shared colour 2 ($d026): light grey, as for Oscar
  .  nothing: what is behind

Five pictures, facing right; the program mirrors them, facing left,
as it copies them into the page shown (tom.asm, tom_page;
keeping them mirrored would take 1 280 bytes). In memory a
picture is four blocks of 64 bytes, top left, top right, bottom left,
bottom right: a page. MIRROR_TO gives, for each byte of a picture,
where it goes mirrored (mirror_to.bin, under the KERNAL).

BOX gives the part of him that touches Oscar and that the staff
strikes: from screen pixel `left` to `right` across the picture (0-47,
the same from both sides: left + right = 47), from `up` lines over his
feet down to his feet. Up to 32: Oscar standing on a pedestal (two
metatiles high) is over it.
"""

OWN_COLOUR = 9                      # brown
FLASH_COLOUR = 1                    # white: struck, he flashes
NAMES = ("stand", "growl", "run_a", "run_b", "dazed")
BOX = (8, 39, 32)                   # left, right, lines up
BITS = {".": 0b00, "R": 0b01, "O": 0b10, "G": 0b11}

PICTURES = {
    # Standing, hunched, his arms hanging, the claws out; the fangs
    # over his lip.
    "stand": [
        "...........O....O.......",
        "...........OO...OO......",
        "...........OOO..OOO.....",
        "..........OOOOOOOOO.....",
        ".........OOOOOOOOOOO....",
        "........OOOOOOOORROO....",
        ".......OOOOOOOOOOOOOOO..",
        "......OOOOOOOOOOOOOOOOOO",
        ".....OOOOOOOOOOOOOGGGGO.",
        "....OOOOOOOOOOOOOGRGRGR.",
        "...O.OOOOOOOOOOOGRRRRR..",
        "...OOOOOOOOOOOOOGGGGG...",
        "..O.OOOOOOOOOOOGGGGG....",
        "..OOOOOOOOOOOOGGGGGO....",
        "...OOOOOOOOOOGGGGGOOO...",
        "..OOOOOOOOOOOGGGGGOOOO..",
        "...OOOOOOOOOOGGGGG.OOOO.",
        "....OOOOOOOOOGGGG...OOO.",
        "....OOOOOOOOOOGG....OOO.",
        "....OOOOOOOOOOOO....OOO.",
        ".....OOOOOOOOOOOO...OOO.",
        ".....OOOOOOOOOOOO...OOOO",
        ".....OOOOOOOOOOGOG.GOOOG",
        "......OOOOOOOOOG.G.G.G.G",
        "......OOOOOOOOOOO.......",
        ".....OOOOOOOOOOOOO......",
        ".....OOOOOO..OOOOOO.....",
        "....OOOOOO....OOOOO.....",
        "....OOOOO......OOOOO....",
        "....OOOOO.......OOOO....",
        ".....OOOO.......OOOO....",
        ".....OOOO.......OOOO....",
        "......OOO......OOOO.....",
        "......OOO......OOO......",
        ".......OO......OOO......",
        ".......OO......OOO......",
        ".......OO.......OO......",
        "......OOO.......OOO.....",
        ".....OOOO.......OOOO....",
        "....OOOOO.......OOOOO...",
        "...GOGOG.........GOGOG..",
        "...G.G.G.........G.G.G.."],
    # The growl: his head thrown back, the jaws wide, both arms up,
    # the claws spread. Also his yelp, beaten, and his leap up and away.
    "growl": [
        ".G.G.G....O.......OGG...",
        ".GOGOG....OO.....OOOGG..",
        "..OOOO....OOO...OOOOOG..",
        "..OOO....OOOOOOOOOOOO...",
        "..OOO...OOOOOOORROOR....",
        "...OOO.OOOOOOOOOORRRR...",
        "...OOOOOOOOOOOOORRRRRR..",
        "....OOOOOOOOOOOOGRRRRG..",
        "....OOOOOOOOOOOOGGRRRG..",
        "...OOOOOOOOOOOOGGGGGG...",
        "...O.OOOOOOOOOGGGG......",
        "..O.OOOOOOOOOGGGGG...G.G",
        "..OOOOOOOOOOGGGGGO...GOG",
        "...OOOOOOOOOGGGGGOO.OOOG",
        "..OOOOOOOOOOGGGGGOOOOOO.",
        "...OOOOOOOOOGGGGG.OOOO..",
        "....OOOOOOOOOGGGG.......",
        "....OOOOOOOOOOGG........",
        "....OOOOOOOOOOOO........",
        ".....OOOOOOOOOOOO.......",
        ".....OOOOOOOOOOOO.......",
        ".....OOOOOOOOOOOO.......",
        "......OOOOOOOOOOO.......",
        "......OOOOOOOOOOO.......",
        "......OOOOOOOOOOO.......",
        ".....OOOOOOOOOOOOO......",
        ".....OOOOOO..OOOOOO.....",
        "....OOOOOO....OOOOO.....",
        "....OOOOO......OOOOO....",
        "....OOOOO.......OOOO....",
        ".....OOOO.......OOOO....",
        ".....OOOO.......OOOO....",
        "......OOO......OOOO.....",
        "......OOO......OOO......",
        ".......OO......OOO......",
        ".......OO......OOO......",
        ".......OO.......OO......",
        "......OOO.......OOO.....",
        ".....OOOO.......OOOO....",
        "....OOOOO.......OOOOO...",
        "...GOGOG.........GOGOG..",
        "...G.G.G.........G.G.G.."],
    # Running: a stride, leaning forward, the near arm reaching.
    "run_a": [
        "........................",
        "........................",
        "........................",
        "........................",
        "........................",
        "........................",
        "........................",
        "........................",
        "..............O...O.....",
        "..............OO..OO....",
        "..............OOOOOO....",
        ".............OOOOOOOO...",
        "......O.O...OOOOOOROO...",
        ".....OOOOOOOOOOOOOOOOOO.",
        "....OOOOOOOOOOOOOOOOOOOO",
        "...O.OOOOOOOOOOOOOGGGGO.",
        "..O.OOOOOOOOOOOOOGRGRGR.",
        "..OOOOOOOOOOOOOOGRRRRR..",
        "...OOOOOOOOOOOOOGGGGG...",
        "..OOOOOOOOOOOOOGGGGG....",
        "...OOOOOOOOOOOGGGGGOO...",
        "...OOOOOOOOOOGGGGGOOOO..",
        "....OOOOOOOOOGGGGG.OOOOO",
        "....OOOOOOOOOGGGG...GOOG",
        ".....OOOOOOOOOGG....G.G.",
        ".....OOOOOOOOOOO........",
        "......OOOOOOOOOO........",
        "......OOOOOOOOOOO.......",
        ".....OOOOOOOOOOOOO......",
        "....OOOOOO..OOOOOOO.....",
        "...OOOOOO.....OOOOOO....",
        "..OOOOO........OOOOOO...",
        ".OOOOO..........OOOOO...",
        "OOOO.............OOOO...",
        "OOO..............OOO....",
        "GOG.............OOOO....",
        "G.G............OOOO.....",
        "..............OOOO......",
        "..............OOO.......",
        ".............OOOO.......",
        "............GOGOG.......",
        "............G.G.G......."],
    # Running, the other stride: in the air, stretched out, the arms
    # forward. Also his leap at Oscar.
    "run_b": [
        "........................",
        "........................",
        "........................",
        "........................",
        "........................",
        "........................",
        "..............O...O.....",
        "..............OO..OO....",
        ".............OOOOOOO....",
        "......O.O...OOOOOOOROO..",
        ".....OOOOOOOOOOOOOOOOOO.",
        "....OOOOOOOOOOOOOOOOOOOO",
        "...O.OOOOOOOOOOOOOGGGGO.",
        "..O.OOOOOOOOOOOOOGRGRGR.",
        ".OOOOOOOOOOOOOOOGRRRRR..",
        "..OOOOOOOOOOOOOOGGGGG...",
        ".OOOOOOOOOOOOOOGGGGGOOOG",
        "..OOOOOOOOOOOOGGGGOOOOOG",
        "...OOOOOOOOOOOGGGG..OOGG",
        "...OOOOOOOOOOOOOG.......",
        "....OOOOOOOOOOOOOO......",
        "...OOOOOOOOOOOOOOOO.....",
        "..OOOOOO.......OOOOO....",
        ".OOOOO..........OOOOO...",
        "OOOO.............OOOOO..",
        "OOO...............OOOO..",
        "GOG................OOO..",
        "G.G...............GOGOG.",
        "..................G.G.G.",
        "........................",
        "........................",
        "........................",
        "........................",
        "........................",
        "........................",
        "........................",
        "........................",
        "........................",
        "........................",
        "........................",
        "........................",
        "........................"],
    # Dazed, against the wall: sitting, his head down, the tongue out,
    # stars round his head.
    "dazed": [
        "........................",
        "........................",
        "..........G.............",
        "........G.G.G...G.......",
        ".........GGG...G.G......",
        "........G.G.G...G.......",
        "..........G.............",
        "..............G.........",
        ".............GGG........",
        "..............G.........",
        "........................",
        "............O...O.......",
        "............OO..OO......",
        "...........OOOOOOOO.....",
        "..........OOOOOOOOOO....",
        ".........OOOOOOGOGOO....",
        "........OOOOOOOOGOOOOO..",
        ".......OOOOOOOOGOGOOOOO.",
        "......OOOOOOOOOOOOOGGGO.",
        ".....OOOOOOOOOOOOOGGGGG.",
        "....O.OOOOOOOOOOOGGRRG..",
        "....OOOOOOOOOOOOGGGRR...",
        "...O.OOOOOOOOOOGGGGRR...",
        "...OOOOOOOOOOOGGGGG.R...",
        "...OOOOOOOOOOOGGGGG.....",
        "...OOOOOOOOOOOGGGGO.....",
        "....OOOOOOOOOOOGGOOO....",
        "....OOOOOOOOOOOOOOOOO...",
        "....OOOOOOOOOOOOO.OOOO..",
        "...OOOOOOOOOOOOOO..OOOO.",
        "..OOOOOOOOOOOOOOO...GOG.",
        "..OOOOOOOOOOOOOOOO..G.G.",
        "..OOOOOOOOOOOOOOOOO.....",
        ".OOOOOOOOOOOOOOOOOOO....",
        ".OOOOOOOO....OOOOOOOO...",
        ".OOOOOOO.......OOOOOOO..",
        "..OOOOO..........OOOOOO.",
        "...OOOO...........OOOOO.",
        "....OOO............OOOO.",
        "....GOGO...........OOOO.",
        "....G.G.G.........GOGOG.",
        "..................G.G.G."],
}


def rows_of(name, left=False):
    """The 42 rows of a picture, facing right or (left) mirrored."""
    rows = PICTURES[name]
    if len(rows) != 42 or any(len(row) != 24 for row in rows):
        raise ValueError(f"{name}: 42 rows of 24 pixels")
    if set("".join(rows)) - set(BITS):
        raise ValueError(f"{name}: letters . R O G only")
    return [row[::-1] for row in rows] if left else list(rows)


def page(rows):
    """A picture's four blocks: top left, top right, bottom left,
    bottom right; 21 rows of 3 bytes and a byte unused each."""
    data = bytearray()
    for top, left in ((0, 0), (0, 12), (21, 0), (21, 12)):
        for row in rows[top:top + 21]:
            value = 0
            for letter in row[left:left + 12]:
                value = (value << 2) | BITS[letter]
            data += value.to_bytes(3, "big")
        data += b"\0"
    return bytes(data)


def pages(left=False):
    """The five pictures, a page each, in the order of NAMES."""
    return b"".join(page(rows_of(name, left)) for name in NAMES)


def box():
    left, right, up = BOX
    if left + right != 47 or not 0 < up <= 42:
        raise ValueError("Tom's box: the same from both sides")
    return BOX


def mirror_byte(value):
    """A byte of a multicolour sprite, its four pixels the other way
    round (what the program's table holds)."""
    return ((value >> 6) | ((value >> 2) & 0x0C) | ((value << 2) & 0x30)
            | ((value << 6) & 0xC0))


def mirror_to():
    """For each of the 256 bytes of a page facing right, where it
    goes in the page facing left: the left block's three bytes of a
    row go to the right block's, the other way round, and the right
    block's to the left's; the 64th byte of each block (not shown) to
    the other's 64th. The program copies byte Y of the picture,
    through the table that mirrors a byte, to byte mirror_to[Y]."""
    out = bytearray(256)
    for half in (0, 128):
        for row in range(21):
            for b in range(3):
                left, right = half + row * 3 + b, half + 64 + row * 3 + b
                out[left] = half + 64 + row * 3 + 2 - b
                out[right] = half + row * 3 + 2 - b
        out[half + 63], out[half + 127] = half + 127, half + 63
    if sorted(out) != list(range(256)):
        raise ValueError("mirror_to: every byte once")
    return bytes(out)


def mirrored(data):
    """A page facing right, mirrored as the program mirrors it: each
    row of six bytes (the left block's three, the right's three) the
    other way round, each byte mirrored."""
    out = bytearray(256)
    for half in (0, 128):
        for row in range(21):
            at = half + row * 3
            six = data[at:at + 3] + data[at + 64:at + 67]
            back = bytes(mirror_byte(b) for b in reversed(six))
            out[at:at + 3] = back[:3]
            out[at + 64:at + 67] = back[3:]
    return bytes(out)
