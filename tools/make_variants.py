"""Build, prove and describe the variants and breaks of the chain.

Usage: python tools/make_variants.py [--test | --readme] [--jobs N]
           [--assembler PATH] [--vice PATH] [ID ...]

After tools/make_variants.py of volume 2. For each entry of
tools/variants.py (all, or those whose id starts with one of ID):
variants/NN-name/ID/ is the step chain/NN-name/ with the entry's
edits (each old text there exactly once), its data rebuilt if the
edits touch game/assets, assembled with 64tass (-Wall -Werror) and
its lines checked (60 characters at most). With --test it is
proved: a variant must pass the test of its step
(tests/verify_game.py --step N --root ..., with the entry's --set,
--route and --no-shows) and show its facts; a break must fail, in
the check the entry names, and is photographed `after` frames later
(--stop-at, --stop-after, --stop-shot). The reports go to
variants/NN-name/evidence/ID/. Then it writes the README.md of each
one, variants/README.md and variants/variants.json; it exits with an
error if one is not proved. --readme writes only the READMEs and the
index again, from variants.json. Standard library only.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import textwrap

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "tools"), str(ROOT / "game/assets")]
import make_chain  # noqa: E402
import variants as catalogue  # noqa: E402

OUT = ROOT / "variants"
PYTHON = sys.executable
TOOLS = {"assembler": shutil.which("64tass") or "64tass",
         "vice": shutil.which("x64sc") or "x64sc"}


def from_game(entries):
    """A break given as a mutation of tests/mutate_game.py (`game`):
    its edit and the check that stops it."""
    spec = importlib.util.spec_from_file_location(
        "mutate_game", ROOT / "tests/mutate_game.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for entry in entries:
        if "game" not in entry:
            continue
        found = [m for m in module.MUTATIONS
                 if m[0].startswith(entry["game"])]
        if len(found) != 1:
            raise SystemExit(f"{entry['id']}: mutation not found once")
        _, file, text, replacement, must_fail = found[0]
        entry.setdefault("edits", [(file, text, replacement)])
        entry.setdefault("fails", must_fail)
    return entries


def folder(entry):
    return OUT / make_chain.STEPS[entry["step"]] / entry["id"]


def evidence(entry):
    return OUT / make_chain.STEPS[entry["step"]] / "evidence" / entry["id"]


def build(entry):
    """The variant's folder: the step, the edits, built."""
    step = ROOT / "chain" / make_chain.STEPS[entry["step"]]
    target = folder(entry)
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    for part in ("game/src", "game/assets", "tools"):
        shutil.copytree(step / part, target / part,
                        ignore=shutil.ignore_patterns("__pycache__"))
    assets = False
    for file, old, new in entry["edits"]:
        path = target / file
        text = path.read_text(encoding="utf-8")
        if text.count(old) != 1:
            raise SystemExit(f"{entry['id']}: {file}: the old text is "
                             f"there {text.count(old)} times")
        path.write_text(text.replace(old, new), encoding="utf-8",
                        newline="\n")
        assets |= file.startswith("game/assets/")
    if assets:
        built = subprocess.run([PYTHON, "game/assets/build_assets.py"],
                               cwd=target, capture_output=True, text=True,
                               env=dict(os.environ,
                                        PYTHONDONTWRITEBYTECODE="1"))
        if built.returncode:
            raise SystemExit(f"{entry['id']}: build_assets.py failed\n"
                             f"{built.stdout}{built.stderr}")
    return make_chain.assemble(target, TOOLS["assembler"])


def command(entry):
    """The test of the step, on the variant."""
    line = [PYTHON, str(ROOT / "tests/verify_game.py"), "--step",
            str(entry["step"]), "--root", str(folder(entry)),
            "--vice", TOOLS["vice"]]
    for statement in entry.get("model", []):
        line += ["--set", statement]
    if entry.get("route"):
        line += ["--route", str(ROOT / "tests/routes" / entry["route"]),
                 "--no-shows"]
    if entry["kind"] == "break" and entry.get("stop", True):
        line += ["--stop-at", entry["fails"], "--stop-after",
                 str(entry.get("after", 0)), "--stop-shot",
                 entry.get("shot") or "stopped.png"]
    return line


def glyphs():
    import font
    return {code: char for code, char in enumerate(font.GLYPH_ORDER)}


def hud_text(report):
    """The HUD's three rows at the end, as text."""
    table = glyphs()
    cells = report.get("hud_end") or []
    rows = [cells[n:n + 40] for n in range(0, len(cells), 40)]
    return ["".join(table.get(c, "?") if isinstance(table.get(c), str)
                    and len(table.get(c)) == 1 else "?" for c in row)
            for row in rows]


def entry_of(report):
    def find(text):
        for step in report.get("route", []):
            if step["what"].startswith(text):
                return step
        raise KeyError(text)
    return find


def prove(entry):
    """Run the test; the result as variants.json keeps it."""
    run = subprocess.run(command(entry), cwd=ROOT, capture_output=True,
                         text=True)
    report_file = evidence(entry) / "step-test.json"
    result = {"id": entry["id"], "step": entry["step"],
              "kind": entry["kind"], "title": entry["title"],
              "proved": False}
    if not report_file.exists():
        result["error"] = run.stdout[-1500:] + run.stderr[-1500:]
        return result
    report = json.loads(report_file.read_text(encoding="utf-8"))
    result["prg_sha256"] = report.get("prg_sha256")
    if entry["kind"] == "variant":
        facts = []
        names = {"r": report, "entry": lambda r, text: entry_of(r)(text),
                 "hud": hud_text}
        for text, test in entry.get("expect", []):
            try:
                ok = bool(eval(test, names))
            except Exception as error:      # noqa: BLE001
                ok = False
                text += f" ({type(error).__name__}: {error})"
            facts.append({"fact": text, "true": ok})
        failed = [c["check"] for c in report["checks"] if not c["pass"]]
        result.update(test=report["result"], frames=report["frames"],
                      checks=len(report["checks"]), failed=failed,
                      facts=facts,
                      proved=report["result"] == "PASS"
                      and all(f["true"] for f in facts))
    elif not entry.get("stop", True):   # failed at the end
        failed = [c for c in report["checks"] if not c["pass"]]
        named = [c for c in failed if entry["fails"] in c["check"]]
        shots = [s["file"] for s in report.get("screenshots", [])
                 if Path(s["file"]).name == entry.get("shot")]
        result.update(test=report["result"],
                      stopped_by=named[0]["check"] if named else None,
                      detail=named[0]["detail"] if named else "",
                      failed=[c["check"] for c in failed], shots=shots,
                      proved=report["result"] == "FAIL" and bool(named)
                      and (not entry.get("shot") or bool(shots)))
    else:
        check = report["checks"][0]
        shots = [s["file"] for s in report.get("screenshots", [])
                 if Path(s["file"]).name == entry.get("shot")]
        result.update(test=report["result"],
                      stopped_by=check["check"], detail=check["detail"],
                      stopped_at=report.get("stopped_at"), shots=shots,
                      proved=report["result"] == "FAIL"
                      and entry["fails"] in check["check"]
                      and (not entry.get("shot") or bool(shots)))
    return result


def readme(entry, result):
    """The variant's README.md, in English."""
    step = make_chain.STEPS[entry["step"]]
    lines = [f"# {entry['title']}", "",
             f"Step {entry['step']:02d} (`chain/{step}`), "
             + ("a guided variant." if entry["kind"] == "variant" else
                "where it breaks: a mistake made on purpose."), "",
             entry["summary"], ""]
    lines += ["## What changes", ""]
    for file, old, new in entry["edits"]:
        lines += [f"In `{file}`:", "", "```", old, "```", "",
                  "becomes", "", "```", new, "```", ""]
    if entry["kind"] == "variant":
        for title, key in (("Where", "where"), ("What you see", "see"),
                           ("Limits", "limits"),
                           ("What depends on it", "depends")):
            lines += [f"## {title}", "", entry[key], ""]
        lines += ["## How it was proved", ""]
        how = (f"The test of step {entry['step']:02d} "
               "(`tests/verify_game.py`) compared the program with its "
               "model at every frame")
        if entry.get("model"):
            how += (", the model changed in the same way ("
                    + "; ".join(f"`{m}`" for m in entry["model"]) + ")")
        where = (f"a route of its own (`tests/routes/{entry['route']}`)"
                 if entry.get("route") else "the route of the step")
        how += (f", on {where}: {result.get('test')}, "
                f"{result.get('checks')} checks, "
                f"{result.get('frames')} frames. Facts:")
        lines += [how, ""]
        lines += [f"- {f['fact']}: {'yes' if f['true'] else 'NO'}"
                  for f in result.get("facts", [])]
        lines += ["", "To go back, undo the change above.", ""]
    else:
        lines += ["## What you see", "", entry["symptom"], "",
                  "## Why", "", entry["cause"], "",
                  "## How the test stops it", "",
                  f"The test of step {entry['step']:02d} stops at "
                  f"\"{entry['fails']}\": {result.get('detail', '')}.",
                  ""]
        if result.get("shots"):
            lines += [f"The capture, {entry.get('after', 0)} frames "
                      f"later: `{Path(result['shots'][0]).name}` (in "
                      f"`variants/{step}/evidence/{entry['id']}/`).", ""]
        lines += ["To repair it, undo the change above.", ""]
    (folder(entry) / "README.md").write_text(
        wrapped("\n".join(lines)), encoding="utf-8", newline="\n")


def wrapped(text, width=72):
    """Paragraphs and list items filled to `width`, a `code` span never
    cut; headings and ``` blocks as they are."""
    out, block = [], False
    for line in text.split("\n"):
        if line.startswith("```"):
            block = not block
        if block or line.startswith(("```", "#")) or len(line) <= width:
            out.append(line)
            continue
        joined = re.sub(r"`[^`]*`",
                        lambda m: m.group(0).replace(" ", "\0"), line)
        lead = "  " if line.startswith("- ") else ""
        out += [part.replace("\0", " ") for part in textwrap.wrap(
            joined, width, subsequent_indent=lead,
            break_long_words=False, break_on_hyphens=False)]
    return "\n".join(out)


def write_index(results):
    """variants/README.md: every variant and break, with its result."""
    by_id = {e["id"]: e for e in catalogue.VARIANTS}
    lines = ["# Variants and breaks of the chain", "",
             "Each folder is a step of `chain/` with one change. A "
             "guided variant (a, b) changes one idea and is proved by "
             "the test of its step, its model changed in the same way; "
             "a break (x) is a classic mistake that the test of its "
             "step stops. Built and proved by `tools/make_variants.py "
             "--test`; results in `variants.json`, reports and "
             "captures in `NN-name/evidence/`.", "",
             "| Step | Folder | Kind | What | Proved |",
             "|---|---|---|---|---|"]
    for result in results:
        entry = by_id[result["id"]]
        step = make_chain.STEPS[entry["step"]]
        kind = "variant" if entry["kind"] == "variant" else "break"
        lines.append(f"| {entry['step']:02d} | `{step}/{entry['id']}` | "
                     f"{kind} | {entry['title']} | "
                     f"{'yes' if result['proved'] else 'NO'} |")
    (OUT / "README.md").write_text("\n".join(lines) + "\n",
                                   encoding="utf-8", newline="\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ids", nargs="*")
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--assembler", default=TOOLS["assembler"])
    parser.add_argument("--vice", default=TOOLS["vice"])
    parser.add_argument("--readme", action="store_true",
                        help="only the READMEs and the index, from "
                        "variants.json (no build, no test)")
    args = parser.parse_args()
    TOOLS.update(assembler=args.assembler, vice=args.vice)
    chosen = [e for e in from_game(catalogue.VARIANTS)
              if not args.ids or any(e["id"].startswith(i)
                                     for i in args.ids)]
    if args.readme:
        store = OUT / "variants.json"
        known = {r["id"]: r for r in json.loads(store.read_text(
            encoding="utf-8"))["results"]}
        for entry in chosen:
            if entry["id"] in known and folder(entry).exists():
                readme(entry, known[entry["id"]])
        write_index([known[e["id"]] for e in catalogue.VARIANTS
                     if e["id"] in known])
        return 0
    for entry in chosen:
        size = build(entry)
        print(f"{entry['id']}: built, PRG {size} bytes", flush=True)
    if not args.test:
        return 0
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(prove, chosen))
    for entry, result in zip(chosen, results):
        readme(entry, result)
        print(("PROVED " if result["proved"] else "NOT PROVED ")
              + entry["id"] + ("" if result["proved"] else
                               f": {json.dumps(result)[:600]}"),
              flush=True)
    store = OUT / "variants.json"
    known = {}
    if store.exists():
        known = {r["id"]: r for r in json.loads(store.read_text(
            encoding="utf-8"))["results"]}
    known.update({r["id"]: r for r in results})
    order = [e["id"] for e in catalogue.VARIANTS]
    ordered = [known[i] for i in order if i in known]
    store.write_text(json.dumps({"results": ordered}, indent=2) + "\n",
                     encoding="utf-8")
    write_index(ordered)
    return 0 if all(r["proved"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
