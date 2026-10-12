"""Dreadcastle: compile the songs (score.py, boss.py, jingles.py).

Two songs: the theme of the game (score.py, song 0) and Tom
Darkfang's (boss.py, song 1); three jingles (jingles.py,
songs 2 to 4: through the gate, the victory, dawn), played once.
They share the instruments (score.py), the wavetable and the table of
patterns; each has its tempo and its three order lists. Writes
game/assets/generated/music.asm, included by data.asm (in the
program, under $4000):
  freq_lo, freq_hi   the SID frequency of notes 0-93 (C0 to A7), PAL
  ins_*              the instruments, one byte each in eight tables
  wave_ctrl,         the wavetable: for each row, a waveform (the
  wave_pitch         control register without the gate) and a pitch:
                     bit 7 set, an absolute note; clear, semitones
                     above the note played. $ff in wave_ctrl: jump to
                     the row in wave_pitch
  pattern_lo/hi      where each pattern starts, the songs' one after
                     the other
  order_lo/hi        where the order list of each voice starts: song
                     0's three, then song 1's, and on
  song_lists         each song's first order list: 3 a song
  tempo_table        frames of each step, in turn: song 0's four,
                     then song 1's, and on
  the theme's patterns and order lists
and music_high.asm, the other songs' patterns and order lists, which
data.asm puts under the KERNAL (Tom's; the jingles
too); returns a summary for assets.json.

Pattern bytes:
  $00-$5d  a note (0-93): played with the instrument and duration set
  $60      a rest: the gate off
  $80-$bf  duration: (byte AND $3f) + 1 steps, for what follows
  $c0-$df  instrument: byte AND $1f
  $ff      end of the pattern
Order lists: pairs (pattern, transposition: a signed byte), then
$fe and the pair to start again from; or, a song played
once (a jingle), $fd: the player stops.

Checked: every note, transposed, from 0 to 93; every voice exactly
as long as the others; at most 32 instruments, 256 wavetable rows.
"""

import re

import boss
import jingles
import score

NOTE_NAMES = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
HIGHEST = 93                        # A7: higher overflows 16 bits (PAL)
PAL_CLOCK = 985248
TEMPO = [5, 5, 5, 4]                # the theme: frames a step
SONGS = (score, boss,               # song 0, song 1,
         jingles.CLEAR, jingles.WON, jingles.DAWN)  # 2-4
SONG_NAMES = ("THEME", "BOSS", "CLEAR", "WON", "DAWN")
GATE_TICK = 2                       # gate off in the last 2 frames
REST, END, LOOP = 0x60, 0xFF, 0xFE
SONG_END = 0xFD                     # a jingle: stop

# Wavetables: rows of (waveform, pitch). Pitch: an int, semitones
# above the note; ("abs", note), a fixed note. The last row of each
# loops (jump) to the row given.
TRI, SAW, PULSE, NOISE = 0x10, 0x20, 0x40, 0x80
WAVES = {
    "square": [(PULSE, 0)],
    "saw": [(SAW, 0)],                  # the brass
    "arp_minor": [(PULSE, 0), (PULSE, 3), (PULSE, 7)],
    "arp_major": [(PULSE, 0), (PULSE, 4), (PULSE, 7)],
    "arp_dim": [(PULSE, 0), (PULSE, 3), (PULSE, 6)],
    "arp_dom7": [(PULSE, 0), (PULSE, 4), (PULSE, 10)],
    "kick": [(PULSE, ("abs", 48)), (TRI, ("abs", 36)),
             (TRI, ("abs", 30)), (TRI, ("abs", 26)),
             (TRI, ("abs", 22))],
    "snare": [(NOISE, ("abs", 84)), (PULSE, ("abs", 40)),
              (NOISE, ("abs", 76)), (NOISE, ("abs", 72))],
}
# Where each wavetable loops: the arpeggios from their first row,
# the others hold their last row.
LOOPS_TO_START = {"arp_minor", "arp_major", "arp_dim", "arp_dom7"}


def note_number(name):
    match = re.fullmatch(r"([A-G])([#b]?)(\d)", name)
    if not match:
        raise ValueError(f"not a note: {name}")
    letter, accidental, octave = match.groups()
    number = NOTE_NAMES[letter] + int(octave) * 12
    number += {"#": 1, "b": -1, "": 0}[accidental]
    return number


def frequency(note):
    """SID frequency register of a note, PAL: Hz * 2^24 / clock;
    A4 (note 57) is 440 Hz."""
    hertz = 440.0 * 2 ** ((note - 57) / 12)
    return round(hertz * 16777216 / PAL_CLOCK)


def parse(text, instruments):
    """Tokens of a pattern: [('ins', n) | ('note', n, steps) |
    ('rest', steps)]."""
    events = []
    for token in text.split():
        if token.startswith("i:"):
            events.append(("ins", instruments.index(token[2:])))
            continue
        name, steps = token.split("/")
        steps = int(steps)
        if not 1 <= steps <= 64:
            raise ValueError(f"{token}: 1-64 steps")
        if name == "--":
            events.append(("rest", steps))
        else:
            events.append(("note", note_number(name), steps))
    return events


def encode(events):
    data, duration = bytearray(), None
    for event in events:
        if event[0] == "ins":
            data.append(0xC0 | event[1])
            continue
        steps = event[-1]
        if steps != duration:
            data.append(0x80 | (steps - 1))
            duration = steps
        data.append(REST if event[0] == "rest" else event[1])
    data.append(END)
    return bytes(data)


def length(events):
    return sum(e[-1] for e in events if e[0] in ("note", "rest"))


def wavetable(instruments):
    """Rows (ctrl, pitch) of all the wavetables, and the first row
    of each instrument."""
    rows, start = [], {}
    for name, table in WAVES.items():
        start[name] = len(rows)
        for waveform, pitch in table:
            if isinstance(pitch, tuple):
                if not 0 <= pitch[1] <= HIGHEST:
                    raise ValueError(f"{name}: note {pitch[1]}")
                rows.append((waveform, 0x80 | pitch[1]))
            else:
                rows.append((waveform, pitch))
        back = start[name] if name in LOOPS_TO_START else len(rows) - 1
        rows.append((0xFF, back))
    if len(rows) > 256:
        raise ValueError("more than 256 wavetable rows")
    return rows, {ins: start[score.INSTRUMENTS[ins]["wave"]]
                  for ins in instruments}


def highest_offset(name):
    return max((p for _, p in WAVES[name] if isinstance(p, int)),
               default=0)


def tempo_of(module):
    """A song's frames a step: score.py's TEMPO here, boss.py's
    its own."""
    return TEMPO if module is score else module.TEMPO


def compile_music():
    """Both songs, as compile_song makes them; their patterns are
    numbered on, song 1's after song 0's."""
    songs, first, names = [], 0, set()
    for module in SONGS:
        song = compile_song(module)
        if names & set(song["names"]):
            raise ValueError("two songs with a pattern of one name")
        names |= set(song["names"])
        song["first_pattern"] = first
        first += len(song["names"])
        songs.append(song)
    return songs


def compile_score():
    """The theme of the game, song 0."""
    return compile_music()[0]


def compile_song(module):
    instruments = list(score.INSTRUMENTS)
    if len(instruments) > 32:
        raise ValueError("more than 32 instruments")
    tempo = tempo_of(module)
    if len(tempo) != len(TEMPO):
        raise ValueError("every song: as many steps of tempo")
    names = list(module.PATTERNS)
    parsed = {n: parse(module.PATTERNS[n], instruments) for n in names}
    voices, loops, seconds = [], [], None
    for order, loop in module.orders():
        total = 0
        for pattern, transpose in order:
            events, ins = parsed[pattern], None
            for event in events:
                if event[0] == "ins":
                    ins = instruments[event[1]]
                elif event[0] == "note":
                    wave = score.INSTRUMENTS[ins]["wave"]
                    top = event[1] + transpose + highest_offset(wave)
                    if not 0 <= event[1] + transpose or top > HIGHEST:
                        raise ValueError(f"{pattern}{transpose:+}: "
                                         f"note out of range")
            total += length(events)
        voices.append(total)
        loops.append(None if loop is None else
                     sum(length(parsed[p]) for p, _ in order[:loop]))
    if len(set(voices)) != 1 or len(set(loops)) != 1:
        raise ValueError(f"voices of {voices} steps, loops at {loops}")
    steps = voices[0]
    frames = sum(tempo[i % len(tempo)] for i in range(steps))
    loop_frames = (0 if loops[0] is None else
                   sum(tempo[i % len(tempo)]
                       for i in range(loops[0], steps)))
    seconds = frames / (PAL_CLOCK / 19656)
    rows, wave_start = wavetable(instruments)
    return {"instruments": instruments, "names": names,
            "data": {n: encode(parsed[n]) for n in names},
            "orders": module.orders(), "rows": rows, "tempo": tempo,
            "wave_start": wave_start, "steps": steps, "frames": frames,
            "loop_from_step": loops[0], "loop_frames": loop_frames,
            "seconds": seconds}


def byte_lines(label, values, per_line=8):
    lines = [f"{label}:"] if label else []
    values = list(values)
    for i in range(0, len(values), per_line):
        lines.append("        .byte " + ", ".join(
            f"${v & 0xFF:02x}" for v in values[i:i + per_line]))
    return lines


def assembler(songs):
    """music.asm (the tables, the theme's patterns and order lists)
    and music_high.asm (the other songs')."""
    first = songs[0]
    out = ["; Written by game/assets/music.py from score.py and",
           "; boss.py: do not edit.", ""]
    out.append(f"MUSIC_TEMPO_STEPS = {len(TEMPO)}")
    out.append(f"MUSIC_GATE_TICK = {GATE_TICK}")
    out.append(f"MUSIC_HIGHEST = {HIGHEST}")
    out.append(f"MUSIC_SONGS = {len(songs)}")
    for number, name in enumerate(SONG_NAMES):
        out.append(f"SONG_{name} = {number}")
        out.append(f"SONG_{name}_FRAMES = {songs[number]['frames']}")
    out.append(f"SONG_END = ${SONG_END:02x}")
    out.append("")
    freqs = [frequency(n) for n in range(HIGHEST + 1)]
    out += byte_lines("freq_lo", (f & 255 for f in freqs))
    out += byte_lines("freq_hi", (f >> 8 for f in freqs))
    out += byte_lines("tempo_table",
                      (v for song in songs for v in song["tempo"]))
    out += byte_lines("song_lists", (3 * n for n in range(len(songs))))
    ins = [score.INSTRUMENTS[i] for i in first["instruments"]]
    out += byte_lines("ins_ad", (i["ad"] for i in ins))
    out += byte_lines("ins_sr", (i["sr"] for i in ins))
    out += byte_lines("ins_wave", (first["wave_start"][n]
                                   for n in first["instruments"]))
    out += byte_lines("ins_pw_lo", (i["pw"] & 255 for i in ins))
    out += byte_lines("ins_pw_hi", (i["pw"] >> 8 for i in ins))
    out += byte_lines("ins_sweep", (i["sweep"] for i in ins))
    out += byte_lines("ins_vibrato", (i["vibrato"] for i in ins))
    out += byte_lines("wave_ctrl", (c for c, _ in first["rows"]))
    out += byte_lines("wave_pitch", (p for _, p in first["rows"]))
    total = sum(len(song["names"]) for song in songs)
    out.append("pattern_lo:")
    out += [f"        .byte <pat_{n}" for n in range(total)]
    out.append("pattern_hi:")
    out += [f"        .byte >pat_{n}" for n in range(total)]
    out.append("order_lo:")
    out += [f"        .byte <order_{v}" for v in range(3 * len(songs))]
    out.append("order_hi:")
    out += [f"        .byte >order_{v}" for v in range(3 * len(songs))]
    high = ["; Written by game/assets/music.py from boss.py and",
            "; jingles.py: do not edit. Under the KERNAL: song 1,",
            "; Tom's theme; songs 2-4, the jingles.",
            ""]
    for number, song in enumerate(songs):
        (high if number else out).extend(song_lines(song, number))
    return ["\n".join(out) + "\n", "\n".join(high) + "\n"]


def song_lines(song, number):
    """A song's patterns (numbered from its first) and its three
    order lists (order_<3 * song + voice>)."""
    out = []
    for at, name in enumerate(song["names"]):
        out.append(f"; pattern {song['first_pattern'] + at}: {name}")
        out += byte_lines(f"pat_{song['first_pattern'] + at}",
                          song["data"][name])
    for voice, (order, loop) in enumerate(song["orders"]):
        values = []
        for pattern, transpose in order:
            values += [song["first_pattern"]
                       + song["names"].index(pattern), transpose & 0xFF]
        values += [LOOP, loop] if loop is not None else [SONG_END]
        out += byte_lines(f"order_{3 * number + voice}", values)
    return out


def summary(song):
    tempo = song["tempo"]
    return {"steps": song["steps"], "frames": song["frames"],
            "seconds": round(song["seconds"], 3),
            "loop_from_step": song["loop_from_step"],
            "loop_frames": song["loop_frames"],
            "loop_seconds": round(song["loop_frames"]
                                  / (PAL_CLOCK / 19656), 3),
            "bpm": round(60 * (PAL_CLOCK / 19656)
                         / (sum(tempo) / len(tempo) * 4), 2),
            "patterns": len(song["names"]),
            "instruments": len(song["instruments"]),
            "wavetable_rows": len(song["rows"]),
            "pattern_bytes": sum(len(d) for d in song["data"].values())}
