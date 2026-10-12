"""Dreadcastle: the three jingles, written for the SID.

A gothic
fanfare. Three short tunes that do not loop: the player stops at
their end (music.py: SONG_END in the order lists).
  CLEAR  through the gate of a level (the count): a rising arpeggio
         in E minor that ends in E major (the Picardy third); about
         2 seconds at the theme's tempo.
  WON    the victory: the theme's first phrase in E major, slower,
         on a brass voice (`brass`, a sawtooth); about 5 seconds.
  DAWN   the sun rises: a line falling in the bass, the melody dying
         out (`fade`: a low sustain, a long release); about 3.4
         seconds.
They play with MUSIC and with SOUND FX
and not with SILENT (states.asm). The notation and the
instruments are score.py's (`brass` and `fade` are new there).
"""

from types import SimpleNamespace


def _song(tempo, patterns, lead, bass, chords):
    """A jingle: its tempo, its patterns and its three order lists,
    played once (no loop: None)."""
    return SimpleNamespace(
        TEMPO=tempo, PATTERNS=patterns,
        orders=lambda: [(lead, None), (bass, None), (chords, None)])


# Through the gate: E minor rising, B7, E major. 20 steps of 5, 5,
# 5 and 4 frames: 95 frames.
CLEAR = _song(
    [5, 5, 5, 4],
    {"clear_lead": "i:brass E5/2 G5/2 B5/2 E6/4 D#6/2 G#6/8",
     "clear_bass": "i:bass E2/2 E3/2 E2/2 E3/4 B1/2 E2/8",
     "clear_chords": ("i:kick E4/1 i:minor E4/9 i:snare E4/1 "
                      "i:dom7 B3/1 i:kick E4/1 i:major E4/7")},
    [("clear_lead", 0)], [("clear_bass", 0)], [("clear_chords", 0)])

# The victory: the theme's first two bars (score.py, lead_a) in E
# major, then E; over E, B7, E. 48 steps of 6, 5, 6 and 5 frames:
# 264 frames.
WON = _song(
    [6, 5, 6, 5],
    {"won_lead": """i:brass
        B4/4 E5/4 G#5/2 F#5/2 E5/4
        D#5/2 E5/2 F#5/2 G#5/2 B5/8
        E6/12 --/4""",
     "won_bass": """i:bass
        E2/4 E3/4 E2/4 E3/4
        B1/4 B2/4 B1/4 B2/4
        E2/12 --/4""",
     "won_major": "i:kick E4/1 i:major E4/7 i:snare E4/1 i:major E4/7",
     "won_dom7": "i:kick E4/1 i:dom7 E4/7 i:snare E4/1 i:dom7 E4/7",
     "won_end": "i:kick E4/1 i:major E4/11 --/4"},
    [("won_lead", 0)], [("won_bass", 0)],
    [("won_major", 0), ("won_dom7", 7), ("won_end", 0)])

# Dawn: the bass falls from E3 to E2 under Em, C, B7, Am, Em; the
# melody falls and fades. 28 steps of 6 frames: 168 frames.
DAWN = _song(
    [6, 6, 6, 6],
    {"dawn_lead": "i:lead B5/4 G5/4 E5/4 D#5/4 i:fade E5/4 B4/8",
     "dawn_bass": "i:bass E3/4 D3/4 C3/4 B2/4 A2/4 E2/8",
     "dawn_chords": ("i:minor E4/8 i:major C4/4 i:dom7 B3/4 "
                     "i:minor A3/4 i:minor E3/8")},
    [("dawn_lead", 0)], [("dawn_bass", 0)], [("dawn_chords", 0)])
