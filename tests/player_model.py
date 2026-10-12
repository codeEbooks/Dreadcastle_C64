"""The music player of Dreadcastle, a frame at a time, in Python.

A model of game/src/player.asm, written from its comments: the same
steps, events, order lists, wavetables, vibrato and pulse sweep, on the
songs compiled by game/assets/music.py from score.py, boss.py
and jingles.py (the same bytes the program carries); and
of the sound effects' player, game/src/effects.asm, on the
effects of sfx.py. After every frame of music the test compares the
model's copy of the SID registers and the state of the three voices
(and of the effects) with those of the C64. start() and stop()
are music_start and music_stop, sfx_start() is sfx_start:
the test calls them where the program does, as it meets them.
"""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]  # after
                    / "game/assets"))   # a variant's (verify_game.py)
import music         # noqa: E402
import score         # noqa: E402
import sfx           # noqa: E402

PW_LOW, PW_HIGH = 0x0200, 0x0E00
REST, END, LOOP = music.REST, music.END, music.LOOP
SONG_END = music.SONG_END
SOUND_FX = 1                                # the menu's choice
VIBRATO = (0, 1, 2, 1, 0, -1, -2, -1)


class Player:
    def __init__(self, songs=None):
        self.songs = songs or music.compile_music()
        self.song = self.songs[0]           # the theme
        s = self.song
        self.freq = [music.frequency(n) for n in range(music.HIGHEST + 1)]
        self.ins = [score.INSTRUMENTS[name] for name in s["instruments"]]
        self.ins_wave = [s["wave_start"][name] for name in s["instruments"]]
        self.rows = s["rows"]
        self.patterns = [song["data"][name] for song in self.songs
                         for name in song["names"]]
        self.orders = []                    # song 0's three, song 1's
        for song in self.songs:
            for order, loop in song["orders"]:
                values = []
                for pattern, transpose in order:
                    values += [song["first_pattern"]
                               + song["names"].index(pattern),
                               transpose & 0xFF]
                self.orders.append(values + ([LOOP, loop]
                                             if loop is not None
                                             else [SONG_END]))
        # The effects: their data, and each voice's state.
        _, self.sfx_data, self.sfx_first = sfx.compile_effects()
        self.fx = [dict(pos=0, tick=0, speed=0) for _ in range(3)]
        self.fx_last = 0
        self.fx_started = []                # the effects that sounded
        self.ended = []                     # the jingles to their end
        # music_init
        self.loops = [[0, 0, 0] for _ in self.songs]    # back to loop
        self.shadow = [0] * 25
        self.shadow[24] = 0x0F
        self.frame, self.number = 0, 0
        self.start_song()

    def start_song(self):
        """Every voice at the start of its order list of the song;
        playing."""
        self.tick, self.on, self.tempo = 1, 1, 0
        self.v = []
        for voice in range(3):
            self.v.append(dict(order=0, ins=0, note=0, gate=0, wave=0,
                               ctrl=0, pw=0, sweep=0, vib=0, dur=1,
                               left=1, trans=0, pattern=0, offset=0))
        for voice in (2, 1, 0):
            self.load_order(voice)

    def gates_off(self):
        for voice in range(3):
            self.shadow[voice * 7 + 4] &= 0xFE

    def start(self, number):
        """music_start: song `number` from its start;
        the effects stop."""
        self.number = number
        self.gates_off()
        self.start_song()
        for voice in self.fx:
            voice["pos"] = 0

    def stop(self):
        """music_stop: the notes let go, the player stops;
        only if it plays."""
        if not self.on:
            return
        self.on = 0
        self.gates_off()

    def sfx_start(self, effect, sound_mode):
        """sfx_start: effect `effect`, with SOUND FX and no
        music playing, on the voice after the last one's."""
        if sound_mode != SOUND_FX or self.on:
            return False
        self.fx_started.append(effect)
        voice = self.fx_last + 1
        if voice == 3:
            voice = 0
        self.fx_last = voice
        at = self.sfx_first[effect]
        speed, ad, sr, pulse = self.sfx_data[at:at + sfx.HEADER]
        self.fx[voice] = dict(pos=at + sfx.HEADER, tick=1, speed=speed)
        base = voice * 7
        self.shadow[base + 5] = ad
        self.shadow[base + 6] = sr
        self.shadow[base + 3] = pulse
        self.shadow[base + 2] = 0
        self.shadow[base + 4] = 0
        return True

    def sfx_play(self):
        """A frame of the effects, after the music's: not
        while music plays."""
        if self.on:
            return
        for voice in (2, 1, 0):
            fx = self.fx[voice]
            if not fx["pos"]:
                continue
            fx["tick"] = (fx["tick"] - 1) & 0xFF
            if fx["tick"]:
                continue
            fx["tick"] = fx["speed"]
            wave = self.sfx_data[fx["pos"]]
            base = voice * 7
            if not wave:
                fx["pos"] = 0
                self.shadow[base + 4] &= 0xFE
                continue
            freq = self.freq[self.sfx_data[fx["pos"] + 1]]
            self.shadow[base] = freq & 255
            self.shadow[base + 1] = freq >> 8
            self.shadow[base + 4] = wave
            fx["pos"] = (fx["pos"] + 2) & 0xFF

    def sfx_state(self):
        """sfx_pos, sfx_tick, sfx_speed (three each) and
        sfx_last, as at SFX_VARS."""
        return ([f["pos"] for f in self.fx] + [f["tick"] for f in self.fx]
                + [f["speed"] for f in self.fx] + [self.fx_last])

    @property
    def tempo_table(self):
        return self.songs[self.number]["tempo"]

    def load_order(self, voice):
        """The voice's next pattern; at a jingle's end, the
        gate off and the player stopped: True."""
        v = self.v[voice]
        order = self.orders[voice + 3 * self.number]
        position = v["order"]
        if order[position * 2] == LOOP:
            v["order"] = position = order[position * 2 + 1]
            self.loops[self.number][voice] += 1
        if order[position * 2] == SONG_END:
            if self.on:
                self.ended.append(self.number)
            v["gate"] = 0
            self.on = 0
            return True
        v["pattern"] = order[position * 2]
        v["trans"] = order[position * 2 + 1]
        v["offset"] = 0
        return False

    def play(self):
        """One frame: music_play (stopped: only the copy), then
        sfx_play."""
        self.music_play()
        self.sfx_play()

    def music_play(self):
        if not self.on:
            return
        self.frame = (self.frame + 1) & 0xFFFF
        self.tick = (self.tick - 1) & 0xFF
        if self.tick == 0:
            self.tick = self.tempo_table[self.tempo]
            self.tempo = (self.tempo + 1) & 3
            for voice in (2, 1, 0):
                v = self.v[voice]
                v["left"] = (v["left"] - 1) & 0xFF
                if v["left"] == 0:
                    self.read_events(voice)
        for voice in (2, 1, 0):
            self.voice_frame(voice)

    def read_events(self, voice):
        v = self.v[voice]
        while True:
            byte = self.patterns[v["pattern"]][v["offset"]]
            v["offset"] += 1
            if byte == END:
                v["order"] = (v["order"] + 1) & 0xFF
                if self.load_order(voice):  # the end: the
                    v["offset"] -= 1        # pointer still at $ff
                    return
            elif byte >= 0xC0:
                v["ins"] = byte & 0x1F
            elif byte >= 0x80:
                v["dur"] = (byte & 0x3F) + 1
            else:
                v["left"] = v["dur"]
                if byte == REST:
                    v["gate"] = 0
                    return
                v["note"] = (byte + v["trans"]) & 0xFF
                v["gate"] = 1
                i = v["ins"]
                v["wave"] = self.ins_wave[i]
                v["pw"] = self.ins[i]["pw"]
                v["sweep"] = self.ins[i]["sweep"] & 0xFF
                v["vib"] = self.ins[i]["vibrato"]
                return

    def voice_frame(self, voice):
        v = self.v[voice]
        if v["left"] == 1 and self.tick <= music.GATE_TICK:
            v["gate"] = 0
        row = v["wave"]
        if self.rows[row][0] == 0xFF:
            row = self.rows[row][1]
        v["ctrl"], pitch = self.rows[row]
        note = pitch & 0x7F if pitch & 0x80 else (pitch + v["note"]) & 0xFF
        v["wave"] = (row + 1) & 0xFF
        freq = self.freq[note]
        if self.ins[v["ins"]]["vibrato"]:
            if v["vib"]:
                v["vib"] -= 1
            else:
                step = freq >> 8
                freq = (freq + VIBRATO[self.frame & 7] * step) & 0xFFFF
        sweep = v["sweep"]
        if sweep:
            if sweep < 0x80:
                v["pw"] = (v["pw"] + sweep) & 0xFFFF
                turn = v["pw"] >> 8 >= PW_HIGH >> 8
                limit = PW_HIGH
            else:
                v["pw"] = (v["pw"] + sweep - 0x100) & 0xFFFF
                turn = v["pw"] >> 8 < PW_LOW >> 8
                limit = PW_LOW
            if turn:
                v["pw"] = limit
                v["sweep"] = (-sweep) & 0xFF
        ins = self.ins[v["ins"]]
        base = voice * 7
        self.shadow[base:base + 7] = [
            freq & 255, freq >> 8, v["pw"] & 255, v["pw"] >> 8,
            v["ctrl"] | v["gate"], ins["ad"], ins["sr"]]

    def state(self, pattern_addresses):
        """The bytes of $62-$65, $6a-$6b (mus_song, mus_on) and
        $70-$9c, in the program's order; pattern_addresses: where each
        pattern is in memory."""
        tables = {name: [] for name in (
            "order", "ptr_lo", "ptr_hi", "trans", "dur", "ins", "left",
            "note", "wave", "gate", "pw_lo", "pw_hi", "sweep", "vib",
            "ctrl")}
        for v in self.v:
            address = pattern_addresses[v["pattern"]] + v["offset"]
            values = dict(order=v["order"], ptr_lo=address & 255,
                          ptr_hi=address >> 8, trans=v["trans"],
                          dur=v["dur"], ins=v["ins"], left=v["left"],
                          note=v["note"], wave=v["wave"], gate=v["gate"],
                          pw_lo=v["pw"] & 255, pw_hi=v["pw"] >> 8,
                          sweep=v["sweep"], vib=v["vib"], ctrl=v["ctrl"])
            for name in tables:
                tables[name].append(values[name])
        voices = [b for name in tables for b in tables[name]]
        return ([self.tick, self.tempo, self.frame & 255, self.frame >> 8],
                [self.number, self.on], voices)
