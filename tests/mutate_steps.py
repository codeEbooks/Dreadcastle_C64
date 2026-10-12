"""Does the test of each step of the chain see faults in its code?

  python tests/mutate_steps.py [--vice PATH] [--jobs N] [--step N]
                               [--check] [--resume]

Three faults of one line for each of steps 1-12, in the code that
the step adds (the complete game, step 13, has the 215 of
tests/mutate_game.py). Most are faults of mutate_game.py, put into
the step where their code first appears (their texts are the
master's: in a step, without the step tags); the others are written
here. Each mutation changes a copy of the step (chain/NN-name, in a
temporary folder: the chain is not touched), assembles it and runs
tests/verify_game.py --step N --root on it. The test must fail, in
the check named for that mutation. --check: only that each text is
in its step once; --resume: an interrupted run goes on. Writes
chain/evidence/mutations.json (all of them only: with --step it
writes nothing).

Tried and set aside, in step 2: the camera let past CAMERA_MAX, which
is equivalent (the hold at the last column stops the camera there
anyway, since CAMERA_MAX is the last pixel of a column); the joystick
read without its eor #$ff, which the test cannot see: it writes the
joystick byte itself, at joy_ready, after read_joystick (the reading
of $DC00 is proved by the hand test).
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

PROJECT = Path(__file__).resolve().parents[1]
ASSEMBLER = shutil.which("64tass") or "64tass"
REPORT = PROJECT / "chain/evidence/mutations.json"
PARTIAL = PROJECT / "chain/evidence/mutations-partial.jsonl"
LINE_LIMIT = 60
# A step tag at the end of a line of the master (tools/make_chain.py).
TAG = re.compile(r"\s*\{(\d*)(-?)(\d*)\}$")

# (step, name, file, text, replacement, a check that must fail);
# GAME: the mutation of mutate_game.py with that name.
GAME = "mutate_game.py"
STEP_MUTATIONS = [
    (1, "the HUD with the level's characters (no $d018 at line 226)",
     GAME),
    (1, "show_name: the level's name only in screen A", GAME),
    (1, "the name's colours a row too high",
     "game/src/level.asm",
     "        sta COLOUR_RAM + NAME_ROW - 40,y",
     "        sta COLOUR_RAM + NAME_ROW - 80,y",
     "the HUD in both screens equals the model"),
    (2, "the new column in screen column 37 instead of 38", GAME),
    (2, "a swap that never shows the back screen",
     "game/src/scroll.asm",
     "        lda d018_values,x\n        sta shown_d018\n"
     "        lda prep_dir            ; 0 right, 1 left",
     "        lda d018_values,x\n"
     "        lda prep_dir            ; 0 right, 1 left",
     "$d016 and $d018 from the frame before"),
    (2, "turning, the back screen is not started again",
     "game/src/scroll.asm",
     "        sta prep_dir            ; the other way: start again\n"
     "        lda #0\n"
     "        sta prep_stage\n",
     "        sta prep_dir            ; the other way: start again\n",
     "a ready back screen = the level one column over"),
    (3, "the jump as high with Up let go: no lighter gravity", GAME),
    (3, "STEP = 1: the slopes are too steep for him", GAME,
     "Oscar's variables equal the model"),
    (3, "the screen stays on in a transition", GAME),
    (4, "Up alone turns him into the bat (Fire not needed)", GAME),
    (4, "a beat costs no energy", GAME),
    (4, "the moths do not flutter", GAME),
    (5, "the gate opens with two heirlooms", GAME),
    (5, "the heirloom does not bob", GAME),
    (5, "the night of 4 minutes again (NIGHT_STEP 750)", GAME),
    (6, "the crow flies straight, without its wave", GAME),
    (6, "a hit takes one notch of health, not two", GAME),
    (6, "every enemy in the watchman's colour", GAME),
    (7, "Fire strikes without the staff", GAME),
    (7, "the staff lying moves with the camera", GAME),
    (7, "the moon moves with the camera", GAME),
    (8, "unpack: a repeat one byte short", GAME),
    (8, "the hazards do not flicker", GAME),
    (8, "move_high: a page short", GAME),
    (9, "the castle's night black: the top interrupt never sets "
        "$d021", GAME),
    (9, "$d022 never changed: the hall's stone dark grey", GAME),
    (9, "the HUD blue in the castle: its interrupt never sets black",
     GAME),
    (10, "Tom's touch never hurts", GAME),
    (10, "Tom's leap: a lighter gravity", GAME,
     "Tom's bytes (0.9) equal the model"),
    (10, "Tom facing left: the pictures facing right", GAME),
    (11, "music: the vibrato the other way round", GAME),
    (11, "every song at the theme's tempo", GAME),
    (11, "Tom's theme never starts in the arena", GAME),
    (12, "the title: Down does not change the choice", GAME),
    (12, "PRESS FIRE never blinks", GAME),
    (12, "a step of the night 60 points", GAME),
]


def game_mutations():
    spec = importlib.util.spec_from_file_location(
        "mutate_game", PROJECT / "tests/mutate_game.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return {m[0]: m for m in module.MUTATIONS}


def untagged(text):
    """A text of the master as a step has it: without its step tags,
    as tools/make_chain.py writes the step."""
    lines = []
    for line in text.split("\n"):
        tag = TAG.search(line)
        if tag:
            line = line[:tag.start()].rstrip()
            if line.endswith(";") and line.strip() != ";":
                line = line[:-1].rstrip()
        lines.append(line)
    return "\n".join(lines)


def mutations():
    """(step, name, file, text, replacement, must_fail), all."""
    game = game_mutations()
    result = []
    for entry in STEP_MUTATIONS:
        if entry[2] == GAME:
            _, file, text, replacement, must_fail = game[entry[1]]
            if len(entry) > 3:          # another check in this step
                must_fail = entry[3]
            entry = (entry[0], entry[1], file, untagged(text),
                     untagged(replacement), must_fail)
        result.append(entry)
    return result


def step_root(step):
    found = sorted((PROJECT / "chain").glob(f"{step:02d}-*"))
    if len(found) != 1:
        raise SystemExit(f"step {step} not in chain/")
    return found[0]


def assemble(copy):
    (copy / "game/build").mkdir(exist_ok=True)
    built = subprocess.run(
        [ASSEMBLER, "--cbm-prg", "-Wall", "-Werror",
         "--vice-labels-numeric", "-l", "game/build/dreadcastle.lbl",
         "-o", "game/build/dreadcastle.prg", "game/src/main.asm"],
        cwd=copy, capture_output=True, text=True)
    return built.returncode == 0, built.stdout + built.stderr


def run_one(mutation, vice):
    """One mutation in its own copy of its step: the test's result."""
    step, name, file, text, replacement, must_fail = mutation
    root = step_root(step)
    with tempfile.TemporaryDirectory() as folder:
        copy = Path(folder) / root.name
        for part in ("game/src", "game/assets"):
            shutil.copytree(root / part, copy / part,
                            ignore=shutil.ignore_patterns("__pycache__"))
        source = copy / file
        content = source.read_text(encoding="utf-8")
        source.write_text(content.replace(text, replacement),
                          encoding="utf-8", newline="\n")
        ok, output = assemble(copy)
        if not ok:
            raise SystemExit(f"{name}: 64tass failed\n{output}")
        run = subprocess.run(
            [sys.executable, str(PROJECT / "tests/verify_game.py"),
             "--vice", vice, "--step", str(step), "--root", str(copy),
             "--stop-at", must_fail],
            cwd=PROJECT, capture_output=True, text=True)
        written = copy / "evidence/step-test.json"
        if not written.exists():    # the test itself broke
            print(f"MISSED step {step}: {name} (the test broke)",
                  flush=True)
            return {"step": step, "mutation": name, "file": file,
                    "test_result": "BROKEN", "must_fail": must_fail,
                    "failed_checks": [], "caught": False,
                    "error": run.stderr[-2000:]}
        report = json.loads(written.read_text(encoding="utf-8"))
    failed = [item["check"] for item in report["checks"]
              if not item["pass"]]
    caught = (run.returncode == 1 and
              any(check.startswith(must_fail) or must_fail in check
                  for check in failed))
    print(("CAUGHT" if caught else "MISSED") + f" step {step}: {name}",
          flush=True)
    return {"step": step, "mutation": name, "file": file,
            "test_result": report["result"], "must_fail": must_fail,
            "failed_checks": failed, "caught": caught}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vice", default=shutil.which("x64sc") or "x64sc")
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--step", type=int, default=None)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--resume", action="store_true",
                        help="keep the results of an interrupted run")
    args = parser.parse_args()
    chosen = [m for m in mutations()
              if args.step is None or m[0] == args.step]
    for step, name, file, text, replacement, _ in chosen:
        found = (step_root(step) / file).read_text(
            encoding="utf-8").count(text)
        if found != 1:
            raise SystemExit(f"step {step}: {name}: the text is there "
                             f"{found} times")
        long = [line for line in replacement.splitlines()
                if len(line.expandtabs(8)) > LINE_LIMIT]
        if long:
            raise SystemExit(f"step {step}: {name}: a line over "
                             f"{LINE_LIMIT}")
    if args.check:
        print(f"{len(chosen)} mutations, each text once in its step")
        return 0
    done = {}
    if args.resume and PARTIAL.exists():    # results kept so far
        for line in PARTIAL.read_text(encoding="utf-8").splitlines():
            result = json.loads(line)
            done[(result["step"], result["mutation"])] = result
    elif args.step is None:
        PARTIAL.parent.mkdir(parents=True, exist_ok=True)
        PARTIAL.write_text("", encoding="utf-8")

    def one(mutation):
        if (mutation[0], mutation[1]) in done:
            return done[(mutation[0], mutation[1])]
        result = run_one(mutation, args.vice)
        if args.step is None:
            with open(PARTIAL, "a", encoding="utf-8", newline="\n") as out:
                out.write(json.dumps(result) + "\n")
        return result

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(one, chosen))
    if args.step is None:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        with open(REPORT, "w", encoding="utf-8", newline="\n") as out:
            out.write(json.dumps({"mutations": results}, indent=2)
                      + "\n")
    missed = [r for r in results if not r["caught"]]
    print(f"{len(results) - len(missed)} of {len(results)} mutations "
          "caught" + ("" if args.step else
                      f"; report {REPORT.relative_to(PROJECT)}"))
    for r in missed:
        print(f"  missed: step {r['step']}: {r['mutation']}")
    return 1 if missed else 0


if __name__ == "__main__":
    sys.exit(main())
