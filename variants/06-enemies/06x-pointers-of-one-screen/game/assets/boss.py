"""Dreadcastle: the theme of Tom Darkfang, written for the SID.

Tense and fast, more frantic than the theme of the game. A first
theme for Tom, a heavy march of 120 beats a minute, was made and
heard, and set aside for this one.
It plays in the arena, from when Oscar comes in
until Tom is beaten.

An original tune, E minor
like the game's theme, faster: about 177 beats a minute (the theme:
158), three voices:
  voice 1  the melody, high (octaves 5 and 6), in jerks: short notes
           and leaps, a pulse wave that sweeps fast (`fury`);
  voice 2  the bass, hammering: semiquavers on the root, its octave on
           the off-beats (the theme's `bass`);
  voice 3  a kick on beats 1 and 3, a snare on 2 and 4 and two more
           at the end of the bar (a roll of three), the chords as
           arpeggios between them (the theme's instruments);
           diminished chords for the tension.

Form, 18 bars of 4/4: intro (2 bars: the bass and the drums), A (8),
B (8); then back to A. A bar is 16 steps; a step lasts 4, 4, 4 and 5
frames in turn (TEMPO), 17 frames a beat. The notation is score.py's;
the instruments are score.py's too.
"""

TEMPO = [4, 4, 4, 5]                # frames a step, in turn: 177 bpm

PATTERNS = {
    # --- voice 1: the melody -------------------------------------
    "boss_lead_intro": "--/32",
    "boss_lead_a": """i:fury
        E5/2 --/1 E5/1 G5/2 E5/2 B5/2 A5/2 G5/2 F#5/2
        E5/2 --/1 E5/1 G5/2 B5/2 E6/4 D#6/4
        E6/2 --/1 E6/1 D6/2 C6/2 B5/2 C6/2 B5/2 G5/2
        F#5/2 --/1 F#5/1 A5/2 C6/2 D#6/4 B5/4
        E5/2 --/1 E5/1 G5/2 E5/2 B5/2 A5/2 G5/2 F#5/2
        G5/2 A5/2 B5/2 E6/2 G6/4 F#6/4
        F6/2 E6/2 C6/2 A5/2 F5/2 A5/2 C6/2 E6/2
        D#6/4 B5/2 F#5/2 D#5/4 B4/4""",
    "boss_lead_b": """i:fury
        A5/2 --/1 A5/1 C6/2 A5/2 E6/2 D6/2 C6/2 B5/2
        A5/2 C6/2 E6/2 A6/2 G6/4 E6/4
        G6/2 --/1 G6/1 F#6/2 E6/2 B5/2 E6/2 D#6/2 B5/2
        E6/8 --/4 B5/2 C6/2
        C6/2 --/1 C6/1 E6/2 G6/2 F#6/2 E6/2 D6/2 C6/2
        A6/2 --/1 A6/1 F#6/2 C6/2 D#6/4 F#6/4
        B5/2 D#6/2 F#6/2 A6/2 B6/4 A6/4
        F#6/4 D#6/4 B5/4 --/4""",
    # --- voice 2: the bass, one bar, on E ------------------------
    "boss_bass": """i:bass
        E2/1 E2/1 E3/1 E2/1 E2/1 E2/1 E3/1 E2/1
        E2/1 E2/1 E3/1 E2/1 E2/1 E3/1 E2/1 E3/1""",
    # --- voice 3: drums and chords, one bar, on E ----------------
    "boss_minor": ("i:kick E4/1 i:minor E4/3 i:snare E4/1 i:minor E4/3 "
                   "i:kick E4/1 i:minor E4/3 i:snare E4/1 i:minor E4/1 "
                   "i:snare E4/1 E4/1"),
    "boss_major": ("i:kick E4/1 i:major E4/3 i:snare E4/1 i:major E4/3 "
                   "i:kick E4/1 i:major E4/3 i:snare E4/1 i:major E4/1 "
                   "i:snare E4/1 E4/1"),
    "boss_dom7": ("i:kick E4/1 i:dom7 E4/3 i:snare E4/1 i:dom7 E4/3 "
                  "i:kick E4/1 i:dom7 E4/3 i:snare E4/1 i:dom7 E4/1 "
                  "i:snare E4/1 E4/1"),
    "boss_dim": ("i:kick E4/1 i:dim E4/3 i:snare E4/1 i:dim E4/3 "
                 "i:kick E4/1 i:dim E4/3 i:snare E4/1 i:dim E4/1 "
                 "i:snare E4/1 E4/1"),
}

# The chords, bar by bar: (root's distance from E, quality).
EM, AM, C, F, B7, FS_DIM, DS_DIM = ((0, "minor"), (5, "minor"),
                                    (-4, "major"), (1, "major"),
                                    (7, "dom7"), (2, "dim"),
                                    (-1, "dim"))
INTRO = [EM, DS_DIM]
A = [EM, EM, C, B7, EM, EM, F, B7]
B_PART = [AM, AM, EM, EM, C, FS_DIM, B7, B7]
SONG = INTRO + A + B_PART                       # 18 bars
LOOP_BAR = len(INTRO)                           # back to A


def orders():
    """The three order lists: [(pattern, transposition), ...] with
    the entry where each voice loops."""
    lead = [("boss_lead_intro", 0), ("boss_lead_a", 0),
            ("boss_lead_b", 0)]
    bass = [("boss_bass", root) for root, _ in SONG]
    chords = [("boss_" + quality, root) for root, quality in SONG]
    return [(lead, 1), (bass, LOOP_BAR), (chords, LOOP_BAR)]
