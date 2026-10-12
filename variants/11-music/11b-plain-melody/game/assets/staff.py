"""The Count's staff: drawn for the game.

The Count's walking stick, used as a club: a shaft of dark wood with
a silver knob. Oscar finds it in level 3, lying on the path; from then
on he holds it, always in his hand,
and Fire strikes with it.

The staff is sprite 2, one multicolour block, behind Oscar's two
sprites (a sprite with a lower number is in front): so his cape and
his outline cover the part of the staff in his hand. Its colours:

  O  its own colour ($d029): brown, the wood
  R  shared colour 1 ($d025): red, the ferrule at its foot
  G  shared colour 2 ($d026): light grey, the silver knob
  .  nothing

Pictures, facing right; the program has them mirrored for facing
left (the blocks: the pictures facing right, then facing left):

  held     upright in his hand, at his front
  air      tilted forward, in a jump or a fall
  raise    the blow, first: raised behind his head
  swing    the blow: straight forward at the height of his hand
  down     the blow, last: forward and down
  lying    on the path, before he takes it (one block, after the
           others: it is never mirrored); its top edge light grey,
           the moon on it, so that it shows on the dark wood

Each picture of Oscar holding it has its place against his sprite
(HELD: dx, dy, picture); the blow's ten frames theirs (BLOW). dx is
for facing right; facing left the staff is at -dx (the mirrored
picture), dy the same.
"""

OWN_COLOUR = 9                      # brown
PICTURES = {
    "held": [
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        ".GG.........",
        "GGGG........",
        ".GG.........",
        ".O..........",
        ".O..........",
        ".O..........",
        ".O..........",
        ".O..........",
        ".O..........",
        ".O..........",
        ".O..........",
        ".O..........",
        ".O..........",
        ".O..........",
        ".R.........."],
    "air": [
        "............",
        "............",
        "............",
        "............",
        "..GG........",
        ".GGGG.......",
        "..GG........",
        "..O.........",
        "..O.........",
        "..O.........",
        "...O........",
        "...O........",
        "...O........",
        "....O.......",
        "....O.......",
        "....O.......",
        ".....R......",
        "............",
        "............",
        "............",
        "............"],
    "raise": [
        "..GG........",
        ".GGGG.......",
        "..GGO.......",
        "....O.......",
        ".....O......",
        ".....O......",
        "......O.....",
        "......O.....",
        ".......O....",
        ".......O....",
        "........O...",
        "........R...",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............"],
    "swing": [
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "..........GG",
        ".........GGG",
        "OOOOOOOOOGGG",
        "..........GG",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............"],
    "down": [
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "OO..........",
        "..OO........",
        "....OO......",
        "......OO....",
        "........OO..",
        "..........GG",
        "..........GG",
        "............",
        "............",
        "............",
        "............",
        "............"],
    "lying": [
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
        "............",
        "............",
        "............",
        "............",
        "............",
        ".GG.........",
        "GGGG........",
        "GGGGGGGGGGG.",
        "GGOOOOOOOOOO",
        ".GOOOOOOOOOR"],
}
ORDER = ["held", "air", "raise", "swing", "down"]
LYING = 2 * len(ORDER)              # its block, after the others

# Oscar's twelve pictures (sprites.py: stand, walk_a, walk_b, walk_c,
# jump, fall; then the same facing left): where the staff is. Its
# shaft just clear of his cape (at 20 the cape hid it). walk_a and
# walk_c: his body one line lower.
HELD = [(22, 0, "held"), (22, 1, "held"), (22, 0, "held"),
        (22, 1, "held"), (20, 0, "air"), (20, 0, "air")]
# The blow, BLOW_FRAMES frames, by the frames left (10 down to 1).
BLOW_FRAMES = 10
BLOW = {10: (8, 0, "raise"), 9: (8, 0, "raise"), 8: (8, 0, "raise"),
        7: (16, 0, "swing"), 6: (16, 0, "swing"), 5: (16, 0, "swing"),
        4: (16, 0, "swing"), 3: (16, 0, "down"), 2: (16, 0, "down"),
        1: (16, 0, "down")}
# The frames of the blow that strike, and what they reach: from his
# body's front edge (BODY_RIGHT facing right) STRIKE_REACH pixels on;
# from STRIKE_UP to STRIKE_DOWN lines over his feet.
STRIKE_FIRST, STRIKE_LAST = 7, 4
STRIKE_REACH = 18
STRIKE_UP, STRIKE_DOWN = 16, 6
BITS = {".": 0b00, "R": 0b01, "O": 0b10, "G": 0b11}


def rows_of(name, left=False):
    rows = PICTURES[name]
    if len(rows) != 21 or any(len(row) != 12 for row in rows):
        raise ValueError(f"{name}: 21 rows of 12 pixels")
    return [row[::-1] for row in rows] if left else list(rows)


def block(rows):
    data = bytearray()
    for row in rows:
        value = 0
        for letter in row:
            value = (value << 2) | BITS[letter]
        data += value.to_bytes(3, "big")
    return bytes(data + b"\0")


def blocks():
    """The pictures facing right, then facing left, then lying."""
    data = bytearray()
    for left in (False, True):
        for name in ORDER:
            data += block(rows_of(name, left))
    return bytes(data + block(rows_of("lying")))


def picture_index(name, left):
    return ORDER.index(name) + (len(ORDER) if left else 0)


def held_table():
    """For each of Oscar's 12 pictures: (dx, dy, picture index)."""
    found = []
    for left in (False, True):
        for dx, dy, name in HELD:
            found.append((-dx if left else dx, dy,
                          picture_index(name, left)))
    return found


def blow_table():
    """For frames left 1..BLOW_FRAMES, facing right then left:
    (dx, dy, picture index)."""
    found = []
    for left in (False, True):
        for frames in range(1, BLOW_FRAMES + 1):
            dx, dy, name = BLOW[frames]
            found.append((-dx if left else dx, dy,
                          picture_index(name, left)))
    return found
