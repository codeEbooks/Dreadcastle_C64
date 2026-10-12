"""Record a song as the emulated SID plays it, then measure it.

  python tools/record_music.py [--vice PATH] [--model 6581|8580]
                               [--song theme|boss|clear|won|dawn|sfx]

--song boss: Tom's theme, from game/build/dreadcastle-boss.prg,
the program assembled with -D RECORD_SONG=1 (it plays Tom's theme from
the start; tools/run-game.ps1 -Mode Record makes it): WAV, report and
MP3 named dreadcastle-boss-<model>, music-recording-boss-<model>.
--song clear, won, dawn: the three jingles, from
dreadcastle-clear.prg, -won.prg, -dawn.prg (-D RECORD_SONG=2, 3, 4),
with a second more for their last notes to fade; --song sfx: the sound
effects one after the other, 0.6 seconds each, from
dreadcastle-sfx.prg (-D RECORD_SFX=1). A jingle passes if it is never
clipped and never quiet while it plays; the effects, if never
clipped and loud enough (a peak over 2000): between them the SID is
silent.

VICE runs the game in real time (warp off: in warp mode it makes no
sound) with its "wav" sound device, for the song's first time through
(intro and one loop) plus the start-up. The script cuts the song from
its first sound into evidence/dreadcastle-theme-<model>.wav and writes
evidence/music-recording-<model>.json: duration, peak, loudness per
second, clipped samples, silent gaps; with numpy and librosa installed,
also the tempo and the key it hears. With ffmpeg on the PATH it also
writes an MP3 of the recording in game/build, to listen to.
Standard library otherwise. Only the VICE process started here runs.

On Windows VICE 3.10 does not always quit by itself at the cycle limit
(seen on the development PC): the script closes it as soon as
VICE has finished the WAV file (its RIFF header holds the real size).
"""
import argparse
import array
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
import wave

ROOT = Path(__file__).resolve().parents[1]
PAL_CLOCK = 985248
ENGINE = {"6581": "256", "8580": "257"}      # reSID with that chip
START_UP_SECONDS = 6
# The songs: their summary in assets.json, the program that plays
# them from the start, the names of the files written.
SONGS = {"theme": ("music", "game/build/dreadcastle.prg", "theme",
                   "music-recording"),
         "boss": ("music_boss", "game/build/dreadcastle-boss.prg",
                  "boss", "music-recording-boss")}
for _jingle in ("clear", "won", "dawn"):
    SONGS[_jingle] = (f"music_{_jingle}",
                      f"game/build/dreadcastle-{_jingle}.prg", _jingle,
                      f"music-recording-{_jingle}")
SONGS["sfx"] = ("sfx", "game/build/dreadcastle-sfx.prg", "sfx",
                "sfx-recording")
TAIL = {"clear": 1.0, "won": 1.0, "dawn": 1.0}  # the release, after


def analyse(samples, rate):
    peak = max(abs(s) for s in samples)
    clipped = sum(1 for s in samples if abs(s) >= 32767)
    per_second = []
    for start in range(0, len(samples) - rate + 1, rate):
        block = samples[start:start + rate]
        per_second.append(round((sum(s * s for s in block) /
                                 len(block)) ** 0.5))
    quiet, longest = 0, 0
    for s in samples:
        quiet = quiet + 1 if abs(s) < 64 else 0
        longest = max(longest, quiet)
    result = {"seconds": round(len(samples) / rate, 3), "peak": peak,
              "clipped_samples": clipped,
              "rms_per_second_min": min(per_second),
              "rms_per_second_max": max(per_second),
              "longest_quiet_gap_seconds": round(longest / rate, 3)}
    try:
        import numpy as np
        import librosa
    except ImportError:
        result["tempo_and_key"] = "numpy/librosa not installed: skipped"
        return result
    y = np.array(samples, dtype=np.float32) / 32768.0
    tempo, _ = librosa.beat.beat_track(y=y, sr=rate)
    chroma = librosa.feature.chroma_cqt(y=y, sr=rate).mean(axis=1)
    minor = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75,
                      3.98, 2.69, 3.34, 3.17])
    major = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19,
                      2.39, 3.66, 2.29, 2.88])
    names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#",
             "B"]
    scores = []
    for shift in range(12):
        scores.append((np.corrcoef(np.roll(major, shift), chroma)[0, 1],
                       names[shift] + " major"))
        scores.append((np.corrcoef(np.roll(minor, shift), chroma)[0, 1],
                       names[shift] + " minor"))
    scores.sort(reverse=True)
    result["tempo_bpm_estimate"] = round(float(np.atleast_1d(tempo)[0]), 1)
    result["key_estimates"] = [[k, round(float(v), 3)]
                               for v, k in scores[:3]]
    return result


def closed(path):
    """True when VICE has closed the WAV file: while it writes, the
    size in the RIFF header is a placeholder; at the end, the real
    one."""
    try:
        size = path.stat().st_size
        with open(path, "rb") as file:
            head = file.read(8)
    except OSError:
        return False
    return (size > 1000 and head[:4] == b"RIFF"
            and int.from_bytes(head[4:8], "little") == size - 8)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vice", default=shutil.which("x64sc") or "x64sc")
    parser.add_argument("--model", choices=ENGINE, default="6581")
    parser.add_argument("--song", choices=SONGS, default="theme")
    args = parser.parse_args()
    key, prg, name, report_name = SONGS[args.song]
    song = json.loads((ROOT / "game/assets/generated/assets.json")
                      .read_text(encoding="utf-8"))[key]
    played = song["reel_seconds"] if args.song == "sfx" \
        else song["seconds"]
    seconds = played + TAIL.get(args.song, 0)
    if not (ROOT / prg).exists():
        print(f"Recording FAILED: no {prg}", file=sys.stderr)
        return 1
    raw = ROOT / "game/build" / f"{name}-{args.model}-raw.wav"
    if raw.exists():
        raw.unlink()
    cycles = int((seconds + START_UP_SECONDS) * PAL_CLOCK)
    command = [str(args.vice), "-default", "-pal",
               "-sidenginemodel", ENGINE[args.model], "+warp", "-sound",
               "-sounddev", "wav", "-soundarg", str(raw),
               "-soundrate", "44100", "-limitcycles", str(cycles),
               "-autostartprgmode", "1", "-autostart", str(ROOT / prg)]
    print(f"Recording {seconds + START_UP_SECONDS:.0f} s of real time "
          f"from the {args.model} SID...", flush=True)
    started = time.monotonic()
    startup = None
    if sys.platform == "win32":                 # no window while recording
        startup = subprocess.STARTUPINFO()
        startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startup.wShowWindow = 0
    with open(ROOT / "game/build" / f"record-{name}-{args.model}"
              "-vice.log",
              "w") as log:
        process = subprocess.Popen(command, cwd=ROOT, stdout=log,
                                   stderr=subprocess.STDOUT,
                                   startupinfo=startup)
        limit = time.monotonic() + seconds + START_UP_SECONDS + 120
        while process.poll() is None and time.monotonic() < limit:
            if closed(raw):             # the WAV is whole: VICE may
                time.sleep(1)           # not quit by itself
                break
            time.sleep(0.5)
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
    if not closed(raw):
        print("Recording FAILED: VICE did not finish the WAV file",
              file=sys.stderr)
        return 1
    with wave.open(str(raw)) as source:
        rate = source.getframerate()
        channels = source.getnchannels()
        samples = array.array("h", source.readframes(source.getnframes()))
    raw.unlink()                                # the song is kept below
    if channels == 2:
        samples = samples[::2]
    first = next((i for i, s in enumerate(samples) if abs(s) > 256), None)
    if first is None:
        print("Recording FAILED: only silence", file=sys.stderr)
        return 1
    count = round(seconds * rate)
    take = samples[first:first + count]
    if len(take) < count:
        print("Recording FAILED: shorter than the song", file=sys.stderr)
        return 1
    out = ROOT / "evidence" / f"dreadcastle-{name}-{args.model}.wav"
    out.parent.mkdir(exist_ok=True)
    with wave.open(str(out), "wb") as target:
        target.setnchannels(1)
        target.setsampwidth(2)
        target.setframerate(rate)
        target.writeframes(take.tobytes())
    report = {"file": str(out.relative_to(ROOT)).replace("\\", "/"),
              "source": f"VICE reSID {args.model}, 'wav' sound device, "
                        "the song's first time through, from its first "
                        "sound",
              "sample_rate": rate, "seconds_expected": seconds,
              "first_sound_seconds": round(first / rate, 3),
              "wall_seconds": round(time.monotonic() - started, 1)}
    report.update(analyse(list(take), rate))
    if args.song == "sfx":                      # the effects
        good = report["peak"] > 2000
    elif args.song in TAIL:                     # a jingle: while it
        playing = take[:round(played * rate)]   # plays (the tail fades)
        report["while_playing"] = analyse(list(playing), rate)
        good = report["while_playing"]["rms_per_second_min"] > 100
    else:
        good = report["rms_per_second_min"] > 100
    report["result"] = "PASS" if (report["clipped_samples"] == 0
                                  and good) else "CHECK"
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:
        mp3 = ROOT / "game/build" / f"dreadcastle-{name}-{args.model}.mp3"
        subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-i", str(out),
                        "-b:a", "192k", str(mp3)], check=False)
        if mp3.exists():
            report["listen"] = str(mp3.relative_to(ROOT)).replace("\\", "/")
    with open(ROOT / "evidence" / f"{report_name}-{args.model}.json",
              "w", encoding="utf-8", newline="\n") as file:
        file.write(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if report["result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
