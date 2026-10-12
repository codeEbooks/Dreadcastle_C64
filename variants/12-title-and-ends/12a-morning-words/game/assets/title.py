"""The title screen and the texts of the game's states.

The screens:
  - the title, the castle under the moon: the name in big letters
    (logo.py) over the walls of the castle, the moon and the blue
    night sky, Oscar in front of the door; under them the menu,
    MUSIC / SOUND FX / SILENT, and PRESS FIRE;
  - between two levels, the count of the level: LEVEL CLEAR, and what
    is left of the night going into the score, a step at a time;
  - the victory, in the arena: over the arena, after Tom has run
    away, the words of the end, the night left into the score; Fire,
    the title;
  - at dawn, the sun rises: the sky lighter, step by step, from
    blue to orange, Oscar gone in a puff of smoke, THE SUN HAS RISEN;
    Fire, the title.

The title shows the end of level 7, Dreadcastle Gate: its castle
door, with the camera as far right as it goes. The moon (sprite 6)
is put in the sky between the two towers, where it can be seen: in
the game it stays up on the right, behind the walls there.

The words over the playfield are a band of rows shown with the HUD's
characters (irq.asm): its first and last rows blank (code 0, blank
in every set), the words in the rows between. Each text: (row,
words); centred in screen columns 1-38. The HUD's colours are
hi-res, under 8.
"""

TITLE_LEVEL = 7                     # its number: 1-8
TITLE_X = 1972                      # Oscar, in front of the door
TITLE_MOON_X = 140                  # sprite 6's registers
TITLE_MOON_Y = 116
LOGO_X = 95                         # sprite 2's X register; 3-5 on
LOGO_Y = 56                         # 48 pixels each (stretched)
LOGO_STEP = 48

BLACK, WHITE, RED, CYAN, PURPLE, GREEN, BLUE, YELLOW = range(8)

# The menu: in the three rows of the HUD (22-24), one a choice; the
# chosen in white with the pointer before it, the others purple.
MENU_ROW = 22
MENU_COL = 12
POINTER_COL = MENU_COL - 2
CHOICES = ["MUSIC", "SOUND FX", "SILENT"]
CHOSEN, OTHER, POINTER = WHITE, PURPLE, YELLOW
PRESS = (23, 26, "PRESS FIRE")      # (row, column, words)
PRESS_ON, PRESS_OFF = CYAN, BLUE    # it blinks: 32 frames each

# The bands: (first row, rows, [(row, colour, words)]).
BANDS = {
    "clear": (2, 3, [(3, YELLOW, "LEVEL CLEAR!")]),
    "won": (3, 7, [(4, YELLOW, "TOM DARKFANG HAS FLED!"),
                   (5, WHITE, "DREADCASTLE IS SAFE,"),
                   (6, WHITE, "AND GRANDPA WILL NEVER KNOW!"),
                   (8, CYAN, "PRESS FIRE")]),
    "dawn": (2, 5, [(3, WHITE, "MORNING HAS COME!"),
                    (5, CYAN, "PRESS FIRE")]),
}
BAND_ORDER = ["clear", "won", "dawn"]

# Dawn: the playfield's background, a step every DAWN_FRAMES frames.
DAWN_COLOURS = [BLUE, PURPLE, 10, 8]        # light red, orange
DAWN_FRAMES = 25


def centred(words):
    """The column of words centred in screen columns 1-38."""
    if len(words) > 38:
        raise ValueError(f"{words!r}: longer than 38")
    return 1 + (38 - len(words)) // 2


def check():
    for name, (first, rows, texts) in BANDS.items():
        if first < 2 or first + rows > 21:
            raise ValueError(f"band {name}: rows 2-20")
        for row, colour, words in texts:
            if not first < row < first + rows - 1:
                raise ValueError(f"band {name}: row {row} at its edge")
            if colour > 7:
                raise ValueError("hi-res colours: under 8")
