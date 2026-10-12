# What was tested, and the limits

Everything here ran in VICE, the emulator. Nothing was run on a real
Commodore 64, and nothing on an NTSC machine. Chapter 19 of the book
("How this book was checked") tells how the tests work; this page gives
the results, the versions and what the repository cannot repeat.

## The versions

| Program | Versions used |
|---|---|
| 64tass | 1.60.3243 |
| VICE, `x64sc` | 3.10 |
| Python | 3.10 and 3.11, standard library only |
| PowerShell | 7.4 on Linux for this version of `run-game.ps1`; the early versions of the game were built and played on Windows with an earlier one |

Every test used a PAL C64 with the 6581 SID. The tests ran on Linux;
seven early versions of the game, tested on Windows too, gave the same
programs and captures there.

## The results printed in the book

| Check | Result |
|---|---|
| The tests of the steps (`tests/verify_game.py --step N`) | See the table below: all PASS, every capture equal to the reference picture |
| The test of the complete game | 40 341 frames, 160 checks: PASS; 57 captures, each equal to the reference |
| Its route | 1 025 moves, four games: the eight levels and Tom with SOUND FX, won with the joystick only; Tom again with MUSIC; a dawn, lost with the joystick only; a game with SILENT |
| One-line faults put in on purpose | Steps 01 to 12: 36 of 36 stopped (`tests/mutate_steps.py`); the complete game: 215 of 215 (`tests/mutate_game.py`) |
| Variants and "Where it breaks" versions | 24 PASS; 13 stopped by their test, as they must be |
| Every level can be finished (`tests/levels.py`) | 248 checks: PASS |
| Figures of the book | 49 captures of the tests, made twice: identical |
| Instructions run by the test of the complete game (`--coverage`) | 4 833 of 4 921 |
| Work of a turn, at most | 17 740 cycles of the 19 656 of a frame, 90 %, just before the victory; every turn on time |
| The disk, loaded by an emulated 1541 (`tools/load_time.py`) | 127.14 seconds, then the title: PASS |
| Listings of the book | 280, each compared with its source; no line over 60 characters |

The tests of the steps:

| Step | Frames | Checks | Captures | Result |
|---|---|---|---|---|
| `01-village-at-night` | 100 | 32 | 1 | PASS |
| `02-scrolling` | 2 120 | 38 | 4 | PASS |
| `03-oscar` | 2 518 | 43 | 5 | PASS |
| `04-bat` | 5 942 | 50 | 8 | PASS |
| `05-heirlooms-and-gate` | 6 782 | 52 | 7 | PASS |
| `06-enemies` | 8 636 | 68 | 16 | PASS |
| `07-staff` | 11 896 | 80 | 22 | PASS |
| `08-packed-levels` | 20 193 | 97 | 35 | PASS |
| `09-castle` | 25 200 | 106 | 43 | PASS |
| `10-tom` | 27 483 | 117 | 49 | PASS |
| `11-music` | 27 483 | 123 | 49 | PASS |
| `12-title-and-ends` | 40 341 | 157 | 57 | PASS |
| `13-complete`, the complete game | 40 341 | 160 | 57 | PASS |

The 88 instructions that the test of the complete game never runs are
defences, for a change of the maps or of the speeds, and moves of the
fight that the test's fights never bring about; chapter 19 lists them
(Table 5), and `tests/verify_game.py --coverage` finds them again.

## Checked again for this repository

On 12 October 2026 the repository was checked from clean copies of
this folder, on Linux, with 64tass 1.60.3243, VICE 3.10 (`x64sc`),
Python 3.11 and PowerShell 7.4:

| Check | Result |
|---|---|
| `python verify.py` | the 7 428 files of `SHA256SUMS.txt` unchanged; the complete game, the 13 steps and the 37 variants built again, each identical to its reference; the 37 reports of the variants' tests name those programs; the disk image holds the release byte for byte: PASS |
| The tests of the thirteen steps and of the complete game, built as the README says | 13 of 13 PASS: the frames, checks and captures of the table above, and every capture byte for byte the one of the project's run. Two measures of steps 12 and 13 depend on the moment VICE starts the title music and change from run to run: the frame where the test meets the music, and the longest step of a transition (15 652 cycles in the book's run of the complete game, 15 648 and 15 644 in two runs here); the turn's 17 740 cycles did not change, and no number printed in the book depends on them |
| `tools/make_chain.py --out` another folder | the thirteen steps and `chain/coverage.csv` identical to `chain/` |
| `tools/make_variants.py`, then `--readme` | the 37 folders, their READMEs, `variants/README.md` and `variants/variants.json` identical; the 37 programs identical to `reference/variants` |
| `tools/check_chain.py` | 0 problems, 22 seams |
| `tools/run-game.ps1 -Mode Build` | in `chain/03-oscar` and at the root, the reference programs; `-Mode Verify` and `-Mode Disk` in a step stop and say where they work |
| `tools/make_disk.py`, `tools/load_time.py` | the disk image identical to `releases/dreadcastle-1.0.d64`; loaded by an emulated 1541 in 127.14 seconds, then the title: PASS |
| `tools/memory_map.py` | the map of chapter 19 |
| `tests/levels.py` | 248 checks: PASS |
| `tests/mutate_steps.py` | 36 of 36 stopped, each in the check meant for it, with the same failed checks as the project's run |
| `tests/mutate_game.py` | its 215 mutated programs are byte for byte those that the test stopped at version 1.0 (215 of 215); 33 of them run again here in VICE, 20 with texts brought to today's master source: 33 of 33 stopped, with the failed checks of 1.0 |
| The listings and file names of the book | the 280 listings, each identical to its lines here; every file name printed in the book is here, or is written by a build (`game/build`, `.prg`, `.lst`, `.lbl`) |
| A Git checkout | `git add` of the folder: 7 429 files, the sources with LF line ends, nothing ignored; a clone made with `core.autocrlf=true` and a `git archive` both agree with `SHA256SUMS.txt` |

Not repeated here: the tests of the variants (`tools/make_variants.py
--test`, several hours; their reports are those of the book, and
`verify.py` checks that they name the programs of this repository),
and `run-game.ps1`, `verify-step.ps1` and `verify-variants.ps1` in this
form under Windows PowerShell 5.1.

## What the repository cannot repeat

- **The figures of the book.** They were captured by an editorial tool
  that is not part of the repository, from the same tests; the
  captures of the tests are written again into `evidence/` when they
  run, and those of the "Where it breaks" versions are in their
  `evidence/` folders.
- **The reports of the tests of the steps and of the complete game.**
  They are not included: running a test writes its report again, in
  `chain/evidence/NN-name/` or `evidence/`. The reports of the
  variants' tests are in their folders.
- **Playing by hand.** The author played the game by hand in VICE;
  that cannot be in a repository.

## Limits

- A test compares the program with a model written in Python for this
  purpose. A model could be wrong in the same way as the program; the
  reference renderer (`tests/reference.py`), written again from the
  data rather than from the assembly, and the faults above, which the
  tests had to stop, are there to make that unlikely, not impossible.
- A route is one way through the game. It enters every level, takes
  every heirloom, meets every kind of enemy and fights Tom, but it
  cannot try every timing.
- `verify.py` proves that the programs are built byte for byte as in
  the book. After your own changes it will report differences, as it
  should; only playing and testing tell whether a change works.
- The 8580 SID of `run-game.ps1 -Model 8580` was used only to record
  the music, not by the tests.
