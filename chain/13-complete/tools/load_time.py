"""How long the program takes to load from a 1541, and that it
starts from the disk.

  python tools/load_time.py [--vice PATH]

After tools/load_time.py of volume 2 (Cryptmorrow). tools/make_disk.py
writes game/build/dreadcastle.d64. VICE then starts with a 1541 on
unit 8, true drive emulation on, the image attached and no autostart;
through the text monitor the keyboard buffer receives
LOAD"DREADCASTLE",8,1 and RETURN, as a user would type it. The monitor
holds the machine from its start (-initbreak ready), so every run
types at the same emulated moment and the disk turns the same way; the
machine stops where BASIC's LOAD calls the KERNAL (JSR $FFD5 at $E175)
and where that call returns ($E178): the load time is the difference
of the two CPU clocks the monitor prints there, in cycles of the PAL
C64 (985 248 a second). $AE/$AF must then hold the end of the file.
Then RUN: the program must reach its main loop (joy_ready, from
game/build/dreadcastle.lbl) on the title, MUSIC chosen ($0300, $0301).
Warp mode only makes the run faster: the clocks count emulated cycles.
Writes evidence/load-time.json; exit code 1 if a check fails. Standard
library only.
"""
import argparse
import json
from pathlib import Path
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "tools"))
import make_disk  # noqa: E402

PAL_CLOCK = 985248
CALL, BACK = 0xE175, 0xE178         # JSR $FFD5 in BASIC's LOAD, after it
STATES = 0x0300                     # game_state, sound_mode (states.asm)
ST_TITLE, MUSIC = 1, 0
REPORT = PROJECT / "evidence/load-time.json"


class TextMonitor:
    """One link to VICE's text monitor, kept open for the whole
    measurement: closing a link lets the machine run on."""

    def __init__(self, port):
        self.link = socket.create_connection(("127.0.0.1", port),
                                             timeout=5)
        self.link.settimeout(0.5)

    def send(self, command, wait=10, until=None):
        """The answer, up to the monitor's prompt (and, with `until`,
        a line matching it: an answer may come late)."""
        self.link.sendall((command + "\n").encode())
        answer, deadline = bytearray(), time.monotonic() + wait
        while time.monotonic() < deadline:
            try:
                chunk = self.link.recv(4096)
            except (TimeoutError, OSError):
                chunk = b""
            answer.extend(chunk)
            text = bytes(answer)
            if re.search(rb"\(C:\$[0-9a-f]{4}\) $", text) and (
                    until is None or re.search(until.encode(), text)):
                break
        return answer.decode(errors="replace")

    def close(self):
        self.link.close()


def free_port():
    with socket.socket() as reserve:
        reserve.bind(("127.0.0.1", 0))
        return reserve.getsockname()[1]


def clock(answer, address):
    """The CPU clock printed with the stop at address."""
    line = next(l for l in answer.splitlines()
                if l.startswith(f".C:{address:04x}"))
    return int(line.split()[-1])


def joy_ready():
    text = (PROJECT / "game/build/dreadcastle.lbl").read_text()
    found = re.search(r"^al\s+C?:?([0-9a-fA-F]+)\s+\.joy_ready\s*$",
                      text, re.M)
    if not found:
        raise SystemExit("joy_ready not in game/build/dreadcastle.lbl")
    return int(found.group(1), 16)


def load_and_run(vice, image, scratch):
    port = free_port()
    log = open(Path(scratch) / "vice.log", "w")
    process = subprocess.Popen(
        [str(vice), "-default", "-pal", "-sound", "-sounddev", "dummy",
         "-warp", "-drive8type", "1541", "-drive8truedrive", "-8",
         str(image), "-initbreak", "ready", "-remotemonitor",
         "-remotemonitoraddress", f"127.0.0.1:{port}"], stdout=log,
        stderr=subprocess.STDOUT)
    try:
        deadline = time.monotonic() + 30
        while True:
            try:
                socket.create_connection(("127.0.0.1", port), 1).close()
                break
            except OSError:
                if time.monotonic() > deadline:
                    raise RuntimeError("VICE's monitor did not answer")
                time.sleep(0.2)
        text = TextMonitor(port)
        text.send("r", until=r"\.;")            # held at the start
        text.send(f'keybuf load\\"{make_disk.NAME}\\",8,1\\n')
        text.send(f"break {CALL:04x}")
        start = clock(text.send("g", wait=120, until=rf"\.C:{CALL:04x}"),
                      CALL)
        text.send("del")
        text.send(f"break {BACK:04x}")
        end = clock(text.send("g", wait=300, until=rf"\.C:{BACK:04x}"),
                    BACK)
        shown = text.send("m ae af", until=r">C:00ae")
        low, high = re.search(r">C:00ae\s+([0-9a-f]{2})\s+([0-9a-f]{2})",
                              shown).groups()
        text.send("del")
        loop = joy_ready()
        text.send("keybuf run\\n")
        text.send(f"break {loop:04x}")
        reached = text.send("g", wait=120, until=rf"\.C:{loop:04x}")
        at_loop = f".C:{loop:04x}" in reached
        states = text.send(f"m {STATES:04x} {STATES + 1:04x}",
                           until=rf">C:{STATES:04x}")
        found = re.search(rf">C:{STATES:04x}\s+([0-9a-f]{{2}})\s+"
                          r"([0-9a-f]{2})", states)
        state = [int(found.group(n), 16) for n in (1, 2)] if found \
            else None
        text.send("del")
        text.link.sendall(b"quit\n")
        time.sleep(1)
        text.close()
    finally:
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.terminate()
            process.wait(timeout=10)
        log.close()
    return end - start, int(high + low, 16), at_loop, state


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vice", default=shutil.which("x64sc") or
                        "x64sc")
    args = parser.parse_args()
    _, blocks = make_disk.make(args.vice)
    data = make_disk.PRG.read_bytes()
    with tempfile.TemporaryDirectory() as scratch:
        cycles, end, at_loop, state = load_and_run(
            args.vice, make_disk.D64, scratch)
    expected = (data[0] | data[1] << 8) + len(data) - 2
    checks = {
        "loaded to its end": end == expected,
        "RUN: the main loop reached": at_loop,
        "on the title, MUSIC chosen": state == [ST_TITLE, MUSIC],
    }
    result = "PASS" if all(checks.values()) else "FAIL"
    report = {
        "method": "LOAD\"DREADCASTLE\",8,1 typed through the monitor's "
                  "keyboard buffer; 1541, true drive emulation; clocks "
                  "at $E175 and $E178; then RUN, to joy_ready",
        "image": str(make_disk.D64.relative_to(PROJECT)),
        "bytes": len(data), "blocks": blocks, "load_cycles": cycles,
        "load_seconds": round(cycles / PAL_CLOCK, 2),
        "bytes_per_second": round(len(data) / (cycles / PAL_CLOCK)),
        "end_address": f"${end:04x}", "expected_end": f"${expected:04x}",
        "states_after_run": state, "checks": checks, "result": result}
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=1) + "\n",
                      encoding="utf-8")
    print(json.dumps(report, indent=1))
    return 0 if result == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
