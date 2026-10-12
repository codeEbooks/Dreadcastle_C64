"""The title of Dreadcastle: the name in big letters, sprites.

The title screen, the castle under the moon:
the name DREADCASTLE in big letters over the walls of
the castle, the moon and the blue night sky, Oscar in front of the
door; the menu under them. The big letters are four hi-res sprites
(2-5) of three letters each, stretched twice across and twice down
($d01d, $d017): a letter of 8 pixels by 21 lines is 16 by 42 on the
screen. The letters are drawn for the game, bold, 7 pixels and a gap,
14 lines tall; under them they drip (a fairy tale more than a horror
story: the drips of a ghost story's title), each letter its own drips,
so that the two Ds, the two As and the two Es are not the same.

Their colour: LOGO_COLOUR, one for all four (each sprite's own
colour register).
"""

LETTER_LINES = 14                   # the letter; then its drips
LINES = 21                          # a sprite block's
WIDTH = 8                           # a letter, its gap included
LOGO_COLOUR = 7                     # yellow, as the windows
WORD = "DREADCASTLE"
SPRITES = 4                         # three letters each

LETTERS = {
    "D": ["#####...",
          "######..",
          "##..###.",
          "##...##.",
          "##...##.",
          "##...##.",
          "##...##.",
          "##...##.",
          "##...##.",
          "##...##.",
          "##...##.",
          "##..###.",
          "######..",
          "#####..."],
    "R": ["#####...",
          "######..",
          "##..###.",
          "##...##.",
          "##...##.",
          "##..###.",
          "######..",
          "#####...",
          "##.###..",
          "##..##..",
          "##..###.",
          "##...##.",
          "##...##.",
          "##...##."],
    "E": ["#######.",
          "#######.",
          "##......",
          "##......",
          "##......",
          "##......",
          "######..",
          "######..",
          "##......",
          "##......",
          "##......",
          "##......",
          "#######.",
          "#######."],
    "A": ["..###...",
          ".#####..",
          "###.###.",
          "##...##.",
          "##...##.",
          "##...##.",
          "#######.",
          "#######.",
          "##...##.",
          "##...##.",
          "##...##.",
          "##...##.",
          "##...##.",
          "##...##."],
    "C": ["..####..",
          ".######.",
          "###..##.",
          "##......",
          "##......",
          "##......",
          "##......",
          "##......",
          "##......",
          "##......",
          "##......",
          "###..##.",
          ".######.",
          "..####.."],
    "S": [".#####..",
          "#######.",
          "##...##.",
          "##......",
          "###.....",
          ".####...",
          "..####..",
          "....###.",
          ".....##.",
          ".....##.",
          "##...##.",
          "##...##.",
          "#######.",
          ".#####.."],
    "T": ["#######.",
          "#######.",
          "..###...",
          "..###...",
          "..###...",
          "..###...",
          "..###...",
          "..###...",
          "..###...",
          "..###...",
          "..###...",
          "..###...",
          "..###...",
          "..###..."],
    "L": ["##......",
          "##......",
          "##......",
          "##......",
          "##......",
          "##......",
          "##......",
          "##......",
          "##......",
          "##......",
          "##......",
          "##......",
          "#######.",
          "#######."],
}

# The drips of each letter of WORD, in its order: (column, lines).
# A drip runs down from the letter's last line, a pixel wide, and ends
# in a drop two pixels wide and two lines tall.
DRIPS = [[(1, 4)],                  # D
         [(5, 5)],                  # R
         [(4, 4)],                  # E
         [(5, 6)],                  # A
         [(0, 3), (3, 5)],          # D
         [(3, 5)],                  # C
         [(1, 4)],                  # A
         [(5, 3)],                  # S
         [(3, 7)],                  # T
         [(5, 4)],                  # L
         [(2, 5), (5, 3)]]          # E


def letter_rows(index):
    """The 21 rows of the letter of WORD at `index`, with its drips."""
    rows = [list(line) for line in LETTERS[WORD[index]]]
    rows += [list("." * WIDTH) for _ in range(LINES - LETTER_LINES)]
    for column, length in DRIPS[index]:
        if not 2 <= length <= LINES - LETTER_LINES:
            raise ValueError(f"drip of {length} lines")
        if rows[LETTER_LINES - 1][column] != "#":
            raise ValueError(f"{WORD[index]}: a drip from nothing")
        last = LETTER_LINES + length - 1
        for line in range(LETTER_LINES, last + 1):
            rows[line][column] = "#"
        for line in (last - 1, last):           # the drop
            rows[line][column + 1] = "#"
    return ["".join(row) for row in rows]


def sprite_rows(number):
    """Sprite `number` (0-3): three letters side by side, 24 pixels
    by 21 lines; the last has two."""
    letters = [letter_rows(i) for i in
               range(number * 3, min(number * 3 + 3, len(WORD)))]
    return ["".join(letter[line] for letter in letters).ljust(24, ".")
            for line in range(LINES)]


def blocks():
    """The four sprite blocks, 64 bytes each (63 and a 0)."""
    data = bytearray()
    for number in range(SPRITES):
        for line in sprite_rows(number):
            bits = int(line.replace("#", "1").replace(".", "0"), 2)
            data += bits.to_bytes(3, "big")
        data.append(0)
    if len(WORD) > SPRITES * 3 or len(WORD) <= (SPRITES - 1) * 3:
        raise ValueError("the word in four sprites")
    return bytes(data)


if __name__ == "__main__":
    for number in range(SPRITES):
        print("\n".join(sprite_rows(number)))
        print()
