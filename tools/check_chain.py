"""Static checks of the chain of the book against its master source.

Usage: python tools/check_chain.py

For every step but the last (tools/make_chain.py), on the lines that
step has:

1. anonymous labels: a branch to + or - lands on the line of the
   master where it lands in the complete game or, if the step has not
   got that line, on the first line after it that the step has;
2. falling through: the code before each label falls into it (it is
   not a jmp, rts or rti, nor data) in the step exactly when it does
   in the complete game.

Only the files that each step includes are read.

Lines of the earlier steps only (;|) that branch to + or - are listed
as seams, to be read. Exit status 1 if a check fails. Standard library
only.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import make_chain as chain  # noqa: E402

SOURCE = ROOT / "game/src"
# Differences read and meant (the seams of the chain), by master line.
KNOWN = {
    ("main.asm", 200): "steps 01-11: the start falls into the main "
                       "loop (from step 12 it goes to the title)",
    ("objects.asm", 658): "step 10: jmp _on where the game falls into "
                          "it after level_theme: the same",
    ("player.asm", 205): "steps 11-12: no jingles, the end of an order "
                         "list goes on into the pattern",
}
LABEL = re.compile(r"^([A-Za-z_]\w*|[+-]+)(?::|\s|$)")
BRANCH = re.compile(r"^\s+(b[a-z]{2}|jmp|jsr)\s+([+-]+)\s*(;.*)?$")


def indexed(text, step):
    """The lines of a file in a step (as make_chain.step_lines), each
    with its line number in the master and whether it is a ;| line."""
    out, blocks = [], [(1, chain.LAST)]
    for number, line in enumerate(text.splitlines(), 1):
        if line == ";{}":
            blocks.pop()
            continue
        block = chain.BLOCK.match(line)
        if block:
            low, high = chain.parse(*block.groups())
            outer = blocks[-1]
            blocks.append((max(low, outer[0]), min(high, outer[1])))
            continue
        low, high = blocks[-1]
        earlier = line.startswith(";|")
        if earlier:
            line = line[2:]
        tag = chain.TAG.search(line)
        if tag:
            first, second = chain.parse(*tag.groups())
            low, high = max(low, first), min(high, second)
            line = line[:tag.start()].rstrip()
            if line.endswith(";") and line.strip() != ";":
                line = line[:-1].rstrip()
        if low <= step <= high:
            out.append((number, line, earlier))
    return out


def code(line):
    text = line.split(";")[0].rstrip()
    return text if text.strip() else None


def anonymous_targets(lines):
    """{index of a branching line: index of its target or None}"""
    result = {}
    for i, (_, line, _) in enumerate(lines):
        branch = BRANCH.match(line)
        if not branch:
            continue
        sign = branch.group(2)
        span = (range(i + 1, len(lines)) if sign[0] == "+"
                else range(i, -1, -1))
        result[i] = next((j for j in span
                          for found in [LABEL.match(lines[j][1])]
                          if found and found.group(1) == sign), None)
    return result


def falls(line):
    """Whether a line of code goes on to the next one."""
    if line is None:
        return False
    words = code(line).split()
    if words and not line.startswith(" "):
        words = words[1:]               # the label in front of it
    if not words:                       # a label alone: on
        return True
    if words[0][0] in ".#*":            # data, a macro's rts, * =
        return False
    return not (words and words[0] in ("jmp", "rts", "rti"))


def before_labels(lines):
    """{master number of a label: the code line before it, or None}"""
    result, last = {}, None
    for number, line, _ in lines:
        label = LABEL.match(line)
        text = code(line)
        constant = re.match(r"^\S+\s*=", line)
        if label and not line.startswith(" ") and not constant:
            result[number] = last
        if label and not line.startswith(" ") and not constant:
            last = line                 # a label: goes on to the next
        elif text:
            body = (re.sub(r"^\S+\s*", "", text)
                    if not text.startswith(" ") else text)
            if body.strip() and not body.strip().startswith("="):
                last = line
    return result


def included(texts, step):
    """The files the step assembles, from main.asm on."""
    todo, done = ["main.asm"], []
    while todo:
        name = todo.pop(0)
        if name in done or name not in texts:
            continue
        done.append(name)
        todo += [m.group(1) for _, line, _ in indexed(texts[name], step)
                 for m in [re.match(r'\s+\.include "([a-z_]+\.asm)"',
                                    line)] if m]
    return done


def main():
    files = sorted(path.name for path in SOURCE.glob("*.asm"))
    texts = {name: (SOURCE / name).read_text(encoding="utf-8")
             for name in files}
    game = {name: indexed(texts[name], chain.LAST) for name in files}
    problems, seams = [], []
    for step in sorted(chain.STEPS)[:-1]:
        for name in included(texts, step):
            lines = indexed(texts[name], step)
            if not lines:
                continue
            numbers = [n for n, _, _ in game[name]]
            game_targets = {numbers[i]: (numbers[j] if j is not None
                                         else None)
                            for i, j in anonymous_targets(
                                game[name]).items()}
            have = [n for n, _, _ in lines]
            for i, j in anonymous_targets(lines).items():
                number, line, earlier = lines[i]
                target = lines[j][0] if j is not None else None
                where = f"step {step} {name}:{number} {line.strip()}"
                wanted = game_targets.get(number)
                if wanted is not None:          # or the next it has
                    wanted = next((n for n in have if n >= wanted), None)
                if earlier:
                    seams.append(f"{where} -> line {target}")
                elif wanted != target:
                    problems.append(f"{where}: to line {target}, in the "
                                    f"game {game_targets.get(number)}")
            in_game, in_step = before_labels(game[name]), \
                before_labels(lines)
            for number, before in in_step.items():
                if number in in_game and \
                        falls(before) != falls(in_game[number]):
                    if (name, number) in KNOWN:
                        seams.append(f"step {step} {name}:{number}: "
                                     f"{KNOWN[name, number]}")
                        continue
                    only = "step" if falls(before) else "game"
                    problems.append(f"step {step} {name}:{number}: "
                                    f"reached by falling through in "
                                    f"the {only} only")
    for seam in seams:
        print("seam:", seam)
    for problem in problems:
        print("PROBLEM:", problem)
    print(f"{len(problems)} problems, {len(seams)} seams")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
