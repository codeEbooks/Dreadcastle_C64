"""Put the program on a 1541 disk image, as the reader gets it.

  python tools/make_disk.py [--vice PATH]

c1541, the disk tool of VICE (beside x64sc, or on the PATH), formats
game/build/dreadcastle.d64 (the disk's name DREADCASTLE, its id DC)
and writes game/build/dreadcastle.prg on it as DREADCASTLE: on a C64,
LOAD"DREADCASTLE",8,1 and RUN (or LOAD"*",8,1). Prints the directory
and the blocks the program takes. The image holds no date: the same
program makes the same bytes. Standard library only.
"""
import argparse
from pathlib import Path
import re
import shutil
import subprocess
import sys

PROJECT = Path(__file__).resolve().parents[1]
PRG = PROJECT / "game/build/dreadcastle.prg"
D64 = PROJECT / "game/build/dreadcastle.d64"
NAME = "dreadcastle"            # c1541 writes it in capitals


def c1541_beside(vice):
    """c1541 in the folder of x64sc, else on the PATH."""
    vice = Path(vice)
    for name in ("c1541.exe", "c1541"):
        found = vice.with_name(name)
        if found.exists():
            return str(found)
    found = shutil.which("c1541")
    if not found:
        raise SystemExit("c1541 (VICE's disk tool) not found beside "
                         f"{vice} or on the PATH")
    return found


def make(vice):
    """The image; returns c1541's directory listing and the blocks."""
    tool = c1541_beside(vice)
    if D64.exists():
        D64.unlink()
    listing = subprocess.run(
        [tool, "-format", "dreadcastle,dc", "d64", str(D64),
         "-write", str(PRG), NAME, "-dir"],
        capture_output=True, text=True, check=True).stdout
    blocks = int(re.search(rf'^(\d+)\s+"{NAME}"', listing,
                           re.M | re.I).group(1))
    return listing, blocks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vice", default=shutil.which("x64sc") or
                        "x64sc")
    args = parser.parse_args()
    if not PRG.exists():
        raise SystemExit(f"{PRG} not built")
    listing, blocks = make(args.vice)
    print(listing.strip())
    print(f"{D64.relative_to(PROJECT)}: {PRG.stat().st_size} bytes, "
          f"{blocks} blocks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
