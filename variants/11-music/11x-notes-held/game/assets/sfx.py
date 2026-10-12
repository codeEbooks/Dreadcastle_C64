"""Dreadcastle: the sound effects, for the SID.

Classic
and short: noise for the staff and the smoke, a pulse wave rising for
the jump and the wings, a bright arpeggio for the heirloom; each under
0.3 seconds); fifteen of them (the ten of the game's design,
three for Tom and the menu's click; the wings' beat is the jump's
sound, shorter). They play only with SOUND FX (player.asm: sfx_start).

An effect is a header and rows. The header: frames a row, attack and
decay, sustain and release, the pulse width (its high byte). A row is
a waveform (the control register, the gate on) and a note (music.py's
numbers: the frequency table is the music's); each lasts the effect's
frames a row. After the last row the gate goes off: the release.
Writes game/assets/generated/sfx.asm: FX_* (the effects' numbers),
sfx_first (where each starts in sfx_data) and sfx_data (at most 256
bytes: one byte says where an effect is).
"""

import music

GATE = 1
TRI, SAW, PULSE, NOISE = (music.TRI | GATE, music.SAW | GATE,
                          music.PULSE | GATE, music.NOISE | GATE)
HEADER = 4                          # frames a row, AD, SR, pulse
REEL_FRAMES = 30                    # the recording: one each 0.6 s
WAVE_NAMES = {TRI: "tri", SAW: "saw", PULSE: "pulse", NOISE: "noise"}


def rows(wave, notes):
    return [(wave, note) for note in notes.split()]


# name: (frames a row, AD, SR, pulse width high, rows); in the order
# of their numbers (FX_<NAME>).
EFFECTS = {
    # Oscar: the jump, a pulse wave rising; the bat's beat, shorter.
    "jump": (1, 0x08, 0x84, 0x08, rows(PULSE, "C4 D4 F4 A4 C5 F5")),
    "flap": (1, 0x06, 0x63, 0x06, rows(PULSE, "G3 C4 G4")),
    # The staff's blow: noise, falling.
    "blow": (1, 0x05, 0x83, 0x08, rows(NOISE, "C7 A6 F6 D6 A5")),
    # A moth eaten: a bite, two notes.
    "moth": (2, 0x04, 0x63, 0x08, rows(TRI, "E6 A6")),
    # An enemy struck: a crack of noise, then a pulse falling.
    "struck": (1, 0x05, 0x84, 0x04,
               rows(NOISE, "C5") + rows(PULSE, "G3 F3 E3 D3")),
    # Oscar hurt: a sawtooth falling.
    "hurt": (1, 0x06, 0x94, 0x08, rows(SAW, "E5 C5 A4 F4 D4 B3 G3")),
    # The change (vampire, bat): a puff of noise, up and down.
    "change": (2, 0x05, 0x84, 0x08, rows(NOISE, "C4 E4 G4 C5 G4 E4 C4")),
    # An heirloom: a bright arpeggio, E major up two octaves.
    "heirloom": (2, 0x04, 0xA6, 0x04,
                 rows(PULSE, "E5 G#5 B5 E6 G#6 B6 E7")),
    # The lantern lit: a chime of two notes.
    "lantern": (6, 0x04, 0x6A, 0x08, rows(TRI, "B5 E6")),
    # The gate opening: a low rumble of noise.
    "gate": (3, 0x08, 0xA6, 0x08, rows(NOISE, "C2 D2 C2 D2 C2")),
    # The night nearly over: a bell tolls (the last two steps).
    "toll": (15, 0x09, 0x0B, 0x08, rows(TRI, "G3")),
    # Tom: the growl, a low sawtooth wavering; struck, a crack and a
    # fall; landing from a leap, a thud.
    "growl": (2, 0x18, 0xA6, 0x08, rows(SAW, "E2 F2 E2 D#2 E2 F2")),
    "tom_hit": (1, 0x05, 0x85, 0x04,
                rows(NOISE, "A5") + rows(PULSE, "C4 B3 A#3")),
    "tom_land": (1, 0x05, 0x84, 0x08, rows(NOISE, "C3 A2 F2")),
    # The menu: a click, one frame.
    "click": (1, 0x00, 0x00, 0x08, rows(PULSE, "C6")),
}


def compile_effects():
    """[(name, header, [(control, note number)])], the data and where
    each effect starts in it."""
    effects, data, first = [], bytearray(), []
    for name, (speed, ad, sr, pulse, effect_rows) in EFFECTS.items():
        notes = [(wave, music.note_number(note))
                 for wave, note in effect_rows]
        for wave, note in notes:
            if not 0 <= note <= music.HIGHEST:
                raise ValueError(f"{name}: note {note}")
        if not 1 <= speed <= 255 or not notes:
            raise ValueError(f"{name}: frames a row, rows")
        first.append(len(data))
        data += bytes([speed, ad, sr, pulse])
        for wave, note in notes:
            data += bytes([wave, note])
        data.append(0)
        effects.append((name, (speed, ad, sr, pulse), notes))
    if len(data) > 256:
        raise ValueError(f"sfx_data: {len(data)} bytes, more than 256")
    return effects, bytes(data), first


def assembler():
    effects, data, first = compile_effects()
    out = ["; Written by game/assets/sfx.py: do not edit.", ""]
    for number, (name, _, _) in enumerate(effects):
        out.append(f"FX_{name.upper()} = {number}")
    out.append(f"FX_COUNT = {len(effects)}")
    out.append(f"FX_HEADER = {HEADER}")
    out.append(f"FX_REEL_FRAMES = {REEL_FRAMES}")
    out.append("")
    out += music.byte_lines("sfx_first", first)
    for number, (name, _, notes) in enumerate(effects):
        start = first[number]
        out.append(f"; {number}: {name}")
        out += music.byte_lines("sfx_data" if number == 0 else "",
                                data[start:start + HEADER + 2 * len(notes)
                                     + 1], per_line=9)
    return "\n".join(out) + "\n"


def summary():
    effects, data, _ = compile_effects()
    return {"effects": len(effects), "bytes": len(data),
            "reel_seconds": round(len(effects) * REEL_FRAMES
                                  / (985248 / 19656), 3),
            "frames": {name: header[0] * len(notes)
                       for name, header, notes in effects}}
