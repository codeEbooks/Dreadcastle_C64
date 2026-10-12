"""The memory of Dreadcastle as the finished program uses it.

Usage: python tools/memory_map.py [--root FOLDER] [--json FILE]

Reads a build of the finished game: FOLDER/game/build/dreadcastle.lbl
and .lst (FOLDER: the project, the default, or chain/13-complete) and
FOLDER/game/src/memory.asm. Lists the C64's memory from $0002 to $FFFF
once the program has started and move_high has put every block in its
place: each area, its first and last address, its bytes and what is
there, then the gaps that nothing uses, as free. The ends of the areas
come from the labels and from the listing: the bytes that each line
puts into the program, at the address where the program uses them
(the second address of a line, in a .logical block). With --json the
same table goes into FILE too. Standard library only.
"""
import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
LINE = re.compile(r"^[.>]([0-9a-f]{4})\t([0-9a-f]{4})?\t"
                  r"((?:[0-9a-f]{2} )*[0-9a-f]{2})")
ZERO_PAGE = re.compile(r"^(\w+)\s*=\s*\$([0-9a-f]{2})\b", re.M)


def labels(path):
    """The labels and constants of a build: name -> value."""
    found = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"al (?:C:)?([0-9a-fA-F]+) \.(\S+)", line.strip())
        if m:
            found[m.group(2)] = int(m.group(1), 16)
    return found


def emitted(path):
    """The address where the program uses each byte of the listing:
    address -> byte."""
    found = {}
    for line in path.read_text(encoding="utf-8",
                               errors="replace").splitlines():
        m = LINE.match(line)
        if m:
            at = int(m.group(2) or m.group(1), 16)
            for i, byte in enumerate(m.group(3).split()):
                found[at + i] = int(byte, 16)
    return found


def zero_page(memory_asm):
    """The names memory.asm gives to addresses of page zero."""
    text = memory_asm.read_text(encoding="utf-8")
    text = text[text.index("; Zero page."):]
    return [(name, int(value, 16))
            for name, value in ZERO_PAGE.findall(text)]


def build(folder):
    """The areas, in address order: dicts with first, last, bytes and
    what; free areas have what "free"."""
    build_dir = folder / "game/build"
    L = labels(build_dir / "dreadcastle.lbl")
    data = emitted(build_dir / "dreadcastle.lst")
    names = zero_page(folder / "game/src/memory.asm")

    def last_byte(first, limit):
        """The last address below limit that the program fills."""
        return max(a for a in data if first <= a < limit)

    zp_first = min(v for _, v in names)
    zp_last = max(v for _, v in names)
    areas = [
        (zp_first, zp_last, f"Page zero: {len(names)} names of "
         "memory.asm"),
        (0x0100, 0x01FF, "The stack"),
        (L["MIRROR"], L["MIRROR"] + 255,
         "MIRROR: every byte, its pairs of bits in reverse order"),
        (L["STATES"], L["SFX_VARS"] + L["SFX_BYTES"] - 1,
         "The states' bytes, then the sound effects'"),
        (L["STATE_CODE"], last_byte(L["STATE_CODE"], 0x0800),
         "The code of the states and the score"),
        (0x0801, last_byte(0x0801, L["SCREEN_A"]),
         "The BASIC line, the code, the tables, the theme"),
        (L["SCREEN_A"], L["SCREEN_B"] - 1, "Screen A"),
        (L["SCREEN_B"], L["CHARSET"] - 1, "Screen B"),
        (L["CHARSET"], L["HUD_CHARSET"] - 1, "The village's characters"),
        (L["HUD_CHARSET"], L["SET_SLOT"] - 1, "The HUD's characters"),
        (L["SET_SLOT"], L["SET_SLOT"] + L["SET_PAGES"] * 256 - 1,
         "SET_SLOT: the characters of the other settings"),
        (L["ENEMY_SPRITES"], L["ENEMY_END"] - 1,
         "Sprites: the enemies of the village and the wood"),
        (L["MOON_SPRITE"], L["SPRITES"] - 1,
         "Sprites: the moon, the title's name; then the HUD's rows "
         "and the moth's pictures"),
        (L["SPRITES"], L["SPRITES"] + L["SPRITE_BYTES"] - 1,
         "Sprites: Oscar, the bat, the smoke; the heirlooms"),
        (L["STAFF_SPRITES"], last_byte(L["STAFF_SPRITES"],
                                       L["ENEMY_SPRITES_2"]),
         "Sprites: the staff; where each profile starts"),
        (L["ENEMY_SPRITES_2"], L["ENEMY_SPRITES_2"] + L["ENEMIES_2"] - 1,
         "Sprites: the enemies of the mountain and the castle"),
        (L["TOM_SPRITES"], 0x7FFF, "Sprites: Tom's two pages"),
        (L["ENV_DATA"], last_byte(L["ENV_DATA"], L["LEVEL"]),
         "Packed: the maps of levels 1-3 and 5-8, the settings' "
         "tables and characters"),
        (L["LEVEL"], L["LEVEL"] + L["MAP_PAGES"] * 256 - 1,
         "The level being played, unpacked"),
        (L["OBJECTS"], L["ENV_TABLES"] - 1,
         "Its objects, its enemies as they move, Tom's bytes"),
        (L["ENV_TABLES"], L["ENV_TABLES"] + L["ENV_PAGES"] * 256 - 1,
         "The tables of its setting"),
        (0xD000, 0xDFFF, "I/O: VIC-II, SID, colour RAM, CIAs"),
        (L["HIGH_DATA"], L["HIGH_END"] - 1,
         "Packed: the castle's characters, the hall's tables and "
         "characters"),
        (L["HIGH_DATA_2"], L["HIGH_END_2"] - 1,
         "Packed: Tom's pictures, the map of level 4; the sound "
         "effects"),
        (L["TOM_PICS"], L["TOM_PICS"] + L["TOM_PAGES"] * 256 - 1,
         "Tom's pictures, unpacked when the arena starts"),
        (L["HIGH_DATA_3"], L["HIGH_END_3"] - 1,
         "mirror_to; Tom's theme and the jingles; the texts"),
        (0xFFFA, 0xFFFF, "The vectors: NMI and IRQ (reset unused)"),
    ]
    areas.sort()
    out, at = [], 0x0002
    for first, last, what in areas:
        if first < at:
            raise SystemExit(f"${first:04x}: {what} overlaps the area "
                             "before it")
        if first > at:
            out.append({"first": at, "last": first - 1,
                        "bytes": first - at, "what": "free"})
        out.append({"first": first, "last": last,
                    "bytes": last - first + 1, "what": what})
        at = last + 1
    if at != 0x10000:
        raise SystemExit("the areas do not reach $FFFF")
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--root", type=Path, default=ROOT,
                        help="the folder of the build (the project)")
    parser.add_argument("--json", type=Path,
                        help="write the table into this file too")
    args = parser.parse_args()
    areas = build(args.root.resolve())
    for area in areas:
        print(f"${area['first']:04X}-${area['last']:04X} "
              f"{area['bytes']:6d}  {area['what']}")
    free = [a for a in areas if a["what"] == "free"]
    print(f"free: {sum(a['bytes'] for a in free)} bytes in {len(free)} "
          "areas")
    if args.json:
        args.json.write_text(json.dumps(areas, indent=1) + "\n",
                             encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
