# Dreadcastle

The code of **Dreadcastle**, Volume 3 of the C64 Game Manual Series
(CODE & BOOKS) by Eric A. Norton: a complete game for the Commodore 64,
written in assembly language for its 6510 processor, and every step of
it as the book builds it.

Oscar, a young vampire, must get home before dawn. He crosses eight
levels, seen from the side on a screen that scrolls smoothly both
ways: the Village of Mortals and its churchyard, the Wild Wood and the
Black Mire, the Grey Crags and the Frozen Pass, Dreadcastle Gate and
the Throne Tower. In each he takes three heirlooms of his family to
open its gate. He walks and jumps, turns into a bat that flies while
its energy lasts and eats moths to win it back, and from the wood on
he strikes with the Count's staff. At the top of the Throne Tower Tom
Darkfang, the leader of the werewolves, waits for him. The title
offers music, sound effects or silence; every game ends in victory or
at dawn.

The repository is the companion of the book. Every listing printed in
the book is a part of a file here, line for line, and every program
here can be rebuilt and compared byte for byte (`verify.py`).

## Play without building

`releases/dreadcastle-1.0.prg` is the complete game, Dreadcastle 1.0,
50 793 bytes. `releases/dreadcastle-1.0.d64` holds the same
program on a 1541 disk image. Start either in VICE:

```text
x64sc -pal -autostartprgmode 1 -joydev2 1 -autostart releases/dreadcastle-1.0.prg
```

`-autostartprgmode 1` puts the program straight into memory; without
it VICE loads it through its emulated 1541, which takes about two
minutes, as on a real C64. With the disk image, attach it to drive 8
and type `LOAD"DREADCASTLE",8,1`, then `RUN`.

- Joystick in port 2. `-joydev2 1` puts it on the numeric keypad: 4
  left, 6 right, 8 up, 2 down, 0 Fire; 7, 9, 1 and 3 the diagonals.
- On the title, Up and Down choose MUSIC, SOUND FX or SILENT; Fire
  starts a game.
- Up jumps, higher while it is held. Up and Fire together turn Oscar
  into the bat: each push of Up is a beat of its wings, Down dives,
  Down and Fire turn it back into Oscar. Once he has found the staff,
  Fire strikes.
- After the victory or at dawn, Fire goes back to the title.

The game is written for a PAL C64 and was tested in VICE's PAL C64
with a 6581 SID. It was not tested on a real C64 or on an NTSC machine.

SHA-256 of the PRG:
`2479d57d001c093b6b58b5c295994ababda7dcf623029357f2ccadd72a654126`

## What is here

```text
game/          the complete game, 1.0: the master source (game/src),
               whose comments also say in which steps each line exists,
               and the tools and data of its graphics, levels and sound
               (game/assets)
chain/         the thirteen steps of the book, 01 to 13: each folder
               has its own copy of every source and tool it needs and
               builds on its own
variants/      37 experiments of the book, each a step with one change:
               24 guided variants and 13 "Where it breaks" versions,
               with a README, and the report of its test in the
               evidence/ folder of its step
tests/         the tests the book relies on (chapter 19)
tools/         run-game.ps1, which builds and plays, and the tools
               named in the book
reference/     the reference programs of the steps and variants
releases/      the complete game, as a PRG and as a D64 disk image
verify.py      builds everything again and compares it byte for byte
CHAPTERS.md    chapter by chapter: its step, experiments and tools
TESTING.md     what was tested, with which versions, and the limits
SHA256SUMS.txt the SHA-256 of every file
LICENSE        MIT
```

## What you need

None of these programs is included; download them from their sites.

- **64tass** 1.60.3243, the assembler (tass64.sourceforge.net). Another
  version may give other bytes.
- **VICE** 3.10, the emulator, whose `x64sc` is the C64
  (vice-emu.sourceforge.io; for Windows, GTK3VICE).
- **Python** 3.10 or later (python.org). Everything uses its standard
  library only.
- On Windows, PowerShell, which comes with Windows, for
  `tools/run-game.ps1`.

`run-game.ps1` and `verify.py` look for `64tass`, `x64sc` and `python`
on the PATH.

## Build and play a step

Open PowerShell in a step folder, for example
`chain/01-village-at-night`, and type:

```text
.\tools\run-game.ps1 -Mode Build
.\tools\run-game.ps1 -Mode Play
```

`Build` writes the data (`game/assets/build_assets.py`), checks that no
source line is longer than 60 characters (`tools/check_lines.py`) and
assembles `game/src/main.asm` into `game/build/dreadcastle.prg`, with
the listing (`.lst`) and the labels for VICE's monitor (`.lbl`). `Play`
builds, then starts `x64sc` as a PAL C64 with a 6581 SID
(`-Model 8580` for the other SID). If a program is not on the PATH, give
its full path with `-Assembler`, `-Vice` or `-Python`. If PowerShell
refuses the script, run it for this one command:

```text
powershell -ExecutionPolicy Bypass -File tools\run-game.ps1 -Mode Play
```

The same script works in every folder of `chain` and `variants`, and at
the root of the repository, where it builds `game/`, the complete game.
There `-Mode Disk` also makes the disk image and loads it from an
emulated 1541 (step 13 has it too), `-Mode Verify` runs the test of
the game, the check of the levels and the timing of the disk, and
`-Mode Record` records the music and the sound effects; in a folder
without the files a mode needs, the script says so.

Without PowerShell, on Linux for example, the same stages by hand, in
the step folder:

```text
python3 game/assets/build_assets.py
python3 tools/check_lines.py
mkdir -p game/build
64tass --cbm-prg -Wall -Werror --vice-labels-numeric \
    -l game/build/dreadcastle.lbl -L game/build/dreadcastle.lst \
    -o game/build/dreadcastle.prg game/src/main.asm
x64sc -pal -autostart game/build/dreadcastle.prg
```

Work on a copy of a step, not on the step itself (chapter 1): the book
and `verify.py` compare your programs with the steps as they are.

## Check that you build the book's programs

```text
python verify.py
```

`verify.py` checks every file against `SHA256SUMS.txt`, builds the
complete game, the thirteen steps and the 37 variants again in a
temporary folder, and compares every program, byte for byte, with the
one in `reference/` or `releases/`; it also reads the program back
from the disk image. A file you changed on purpose is reported as
changed. It takes a few minutes; `python verify.py chain/03` builds
only what matches.

The programs of the steps:

| Step | Bytes | SHA-256 |
|---|---|---|
| `chain/01-village-at-night` | 42 027 | `8bb018bee3b2201ab36913951fa2d2aa33c5fe12cae1446afe26d63cb03b0cd0` |
| `chain/02-scrolling` | 42 027 | `136f509eb68051c41833365784faa9e8fc18e30a6e7ac6519b3e1796e771c0c1` |
| `chain/03-oscar` | 42 027 | `0893b753ad8d80348541b22206bda340d4c734e545280e2e8cf70281ae2cc936` |
| `chain/04-bat` | 42 027 | `9d6c9090cbe4841d5483809a0299ddae2a110682601f9340b440bd4f945cf22d` |
| `chain/05-heirlooms-and-gate` | 42 027 | `560482ab5d530e048c287b5777349939a824c6f4fcaf87f265303dead8bf6804` |
| `chain/06-enemies` | 42 027 | `ca36fd683541bb767c837144a8d225e4dbe445c6548d8336d37a24fff7acb859` |
| `chain/07-staff` | 42 027 | `4452258d3fa4d34a59aa39b72e4a6d1009321956535ad97901dc95fc00d70a48` |
| `chain/08-packed-levels` | 50 793 | `ff88c7740ade2c95fcdd1e5f45061eb832f8eb08901f20c9b7f02170518b8e78` |
| `chain/09-castle` | 50 793 | `ec4346f528fce21d1863e1938d74862670911cd6ef2c73051e44399a129f57dd` |
| `chain/10-tom` | 50 793 | `27adec53b3be78ca7b891646ba30054d36ee3eb2e29e8b473ed87ca8a1a28c0c` |
| `chain/11-music` | 50 793 | `b7fcc5ef3357551d1ea923c5074cd64fdaadc070d38be5a7da9507e57c3921bd` |
| `chain/12-title-and-ends` | 50 793 | `fa69048422ebad1482286fb2f7a35b5b5f5b1d621ec855c275baf64f5339f79c` |
| `chain/13-complete` | 50 793 | `2479d57d001c093b6b58b5c295994ababda7dcf623029357f2ccadd72a654126` |

## Run the tests

```text
python tests/verify_game.py --step 3 --vice PATH
python tests/verify_game.py --vice PATH
```

`verify_game.py` checks a step, or with no `--step` the complete game;
it starts VICE itself, plays a planned route with the joystick and
compares every frame with a model written in Python. `PATH` is the
full path of `x64sc`. Build the complete game first, at the root, and
then the step (`-Mode Build` in its folder): a test reads the
programs and labels of `game/build`, and every test takes the numbers
of the game, its speeds, its frames and the places of its variables,
from the labels of the complete game. The report of a step goes to
`chain/evidence/NN-name/`, that of the complete game to `evidence/`.
On Windows, `tools/verify-step.ps1 -Step 3` builds what is needed and
runs the test of a step. On
Linux without a display, start the tests and the tools that run VICE
under `xvfb-run`. [TESTING.md](TESTING.md) tells what was checked, and
how.

## Rights

The contents of this repository, source code, data, tools, tests and
programs, including the graphics, levels, font, sprites, music and
sound effects in `game/assets`, are released under the MIT License:
see [LICENSE](LICENSE). Copyright (c) 2026 Eric A. Norton.

The book is not part of this repository and is not covered by this
license: its text, figures, layout and cover are copyright (c) 2026
Eric A. Norton, all rights reserved. Book by Eric A. Norton; music and
history edited by Jorah Sallow.

Everything in the game was made for it: graphics, levels, font,
sprites, music and sound effects. No ROM, emulator or assembler is
included. Commodore 64 and the other product names are used to
identify the machine and the tools; this is an independent project,
not affiliated with or endorsed by their owners.
