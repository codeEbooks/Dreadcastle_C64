"""Dreadcastle: the theme of the game, written for the SID.

An original tune for the night in the Village of Mortals: E minor,
about 158 beats a minute, three voices.
  voice 1  the melody (pulse wave, with vibrato on the long notes);
  voice 2  the bass, in octaves, in quavers;
  voice 3  the chords as fast arpeggios, with a soft kick and snare
           between them.

Form, 32 bars of 4/4: intro (4 bars), A (8), B (8), A again with a
new ending (8), bridge (4); then back to A: the intro is played only
once. A bar is 16 steps (semiquavers); a step lasts 5, 5, 5 and 4
frames in turn (music.py: TEMPO), 19 frames a beat.

Notation: a pattern is a string of tokens.
  E5/4    the note E in octave 5 for 4 steps (C0 is the lowest note)
  F#5 Bb4 sharps and flats
  --/4    a rest of 4 steps
  i:lead  the instrument for the notes that follow
An order list gives, bar after bar, a pattern and a transposition in
semitones; "loop" marks where the voice starts again.
"""

# Instruments: ADSR, wavetable, pulse width and sweep, vibrato delay
# (frames; 0: none). The wavetables are in music.py.
INSTRUMENTS = {
    "lead":  dict(ad=0x0A, sr=0xA8, wave="square", pw=0x0800,
                  sweep=0x18, vibrato=18),
    "bass":  dict(ad=0x06, sr=0xC4, wave="square", pw=0x0600,
                  sweep=0x00, vibrato=0),
    "minor": dict(ad=0x05, sr=0x00, wave="arp_minor", pw=0x0400,
                  sweep=0x10, vibrato=0),
    "major": dict(ad=0x05, sr=0x00, wave="arp_major", pw=0x0400,
                  sweep=0x10, vibrato=0),
    "dim":   dict(ad=0x05, sr=0x00, wave="arp_dim", pw=0x0400,
                  sweep=0x10, vibrato=0),
    "dom7":  dict(ad=0x05, sr=0x00, wave="arp_dom7", pw=0x0400,
                  sweep=0x10, vibrato=0),
    "kick":  dict(ad=0x05, sr=0x00, wave="kick", pw=0x0800,
                  sweep=0x00, vibrato=0),
    "snare": dict(ad=0x06, sr=0x00, wave="snare", pw=0x0800,
                  sweep=0x00, vibrato=0),
    # Tom's theme (boss.py): its melody, short and sharp, the
    # pulse width sweeping fast.
    "fury": dict(ad=0x08, sr=0xA6, wave="square", pw=0x0600,
                 sweep=0x30, vibrato=0),
    # The jingles (jingles.py): the fanfare's brass, a
    # sawtooth; the melody of dawn dying out, a low sustain and a long
    # release.
    "brass": dict(ad=0x29, sr=0x98, wave="saw", pw=0x0800,
                  sweep=0x00, vibrato=12),
    "fade": dict(ad=0x0A, sr=0x4A, wave="square", pw=0x0800,
                 sweep=0x10, vibrato=18),
}

PATTERNS = {
    # --- voice 1: the melody -------------------------------------
    "lead_intro": "--/64",
    "lead_a": """i:lead
        B4/4 E5/4 G5/2 F#5/2 E5/4
        D#5/2 E5/2 F#5/2 G5/2 B5/8
        C6/4 B5/2 A5/2 E5/4 C5/4
        B4/2 C5/2 E5/4 A4/8
        G5/4 E5/2 G5/2 C6/6 B5/2
        A5/2 G5/2 F#5/4 D#5/4 B4/4
        E5/2 F#5/2 G5/2 A5/2 B5/4 G5/4
        F#5/4 D#5/4 B4/8""",
    "lead_b": """i:lead
        D6/4 B5/2 G5/2 D6/4 E6/4
        F#6/4 E6/2 D6/2 A5/8
        G5/2 A5/2 B5/4 E6/4 B5/4
        C6/4 B5/2 A5/2 G5/4 E5/4
        A5/2 B5/2 C6/4 E6/4 C6/4
        D6/4 C6/2 B5/2 A5/4 F#5/4
        D#6/4 B5/4 F#5/4 D#5/4
        B5/12 --/4""",
    "lead_a2": """i:lead
        B4/4 E5/4 G5/2 F#5/2 E5/4
        D#5/2 E5/2 F#5/2 G5/2 B5/8
        C6/4 B5/2 A5/2 E5/4 C5/4
        B4/2 C5/2 E5/4 A4/8
        G5/4 E5/2 G5/2 C6/6 B5/2
        A5/2 G5/2 F#5/4 D#5/4 B4/4
        E5/2 F#5/2 G5/2 B5/2 E6/4 D#6/4
        E6/12 --/4""",
    "lead_bridge": """i:lead
        C5/4 E5/4 G5/4 C6/4
        B5/4 A5/4 E5/8
        F#5/4 A5/4 C6/4 D#6/4
        F#6/8 D#6/4 B5/4""",
    # --- voice 2: the bass, one bar, on E ------------------------
    "bass": """i:bass
        E2/2 E3/2 E2/2 E3/2 E2/2 E3/2 E2/2 E3/2""",
    # --- voice 3: chords and drums, one bar, on E ----------------
    "arps_minor": "i:minor E4/2 E4/2 E4/2 E4/2 E4/2 E4/2 E4/2 E4/2",
    "minor": ("i:kick E4/1 i:minor E4/3 i:snare E4/1 i:minor E4/3 "
              "i:kick E4/1 i:minor E4/3 i:snare E4/1 i:minor E4/3"),
    "major": ("i:kick E4/1 i:major E4/3 i:snare E4/1 i:major E4/3 "
              "i:kick E4/1 i:major E4/3 i:snare E4/1 i:major E4/3"),
    "dim":   ("i:kick E4/1 i:dim E4/3 i:snare E4/1 i:dim E4/3 "
              "i:kick E4/1 i:dim E4/3 i:snare E4/1 i:dim E4/3"),
    "dom7":  ("i:kick E4/1 i:dom7 E4/3 i:snare E4/1 i:dom7 E4/3 "
              "i:kick E4/1 i:dom7 E4/3 i:snare E4/1 i:dom7 E4/3"),
}

# The chords, bar by bar: (root's distance from E in semitones,
# quality). Bass and chords follow them.
EM, AM, C, B7, G, D, B, FS_DIM = ((0, "minor"), (5, "minor"),
                                  (-4, "major"), (7, "dom7"),
                                  (3, "major"), (-2, "major"),
                                  (7, "major"), (2, "dim"))
INTRO = [EM, EM, C, B7]
A = [EM, EM, AM, AM, C, B7, EM, B7]
B_PART = [G, D, EM, C, AM, D, B7, B7]
A2 = [EM, EM, AM, AM, C, B7, EM, EM]
BRIDGE = [C, AM, FS_DIM, B7]
SONG = INTRO + A + B_PART + A2 + BRIDGE          # 32 bars
LOOP_BAR = len(INTRO)                            # back to A


def orders():
    """The three order lists: [(pattern, transposition), ...] with
    the entry where each voice loops."""
    lead = [("lead_intro", 0), ("lead_a", 0), ("lead_b", 0),
            ("lead_a2", 0), ("lead_bridge", 0)]
    bass = [("bass", root) for root, _ in SONG]
    chords = [("arps_minor", root) for root, _ in INTRO[:2]]
    chords += [(quality, root) for root, quality in SONG[2:]]
    return [(lead, 1), (bass, LOOP_BAR), (chords, LOOP_BAR)]
