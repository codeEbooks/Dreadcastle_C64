# The chapters and their folders

The book builds the game in thirteen steps. Each chapter works on one
step of `chain/` (two chapters may share one); its experiments are in
`variants/`, in the folder of the same step. A variant is the step
with one change: a guided variant ("Make it yours") shows what a value
or a table does, a "Where it breaks" version makes on purpose a
mistake the chapter explains, and its test must fail.

| Chapter | Title | Step | Experiments | Tools |
|---|---|---|---|---|
| 1 | Your workshop | `chain/01-village-at-night` | | `tools/run-game.ps1`, `tools/check_lines.py` |
| 2 | Memory and the VIC-II | `chain/01-village-at-night` | | |
| 3 | The level on screen | `chain/01-village-at-night` | `01a-churchyard-first` | |
| 4 | The raster and the HUD | `chain/01-village-at-night` | `01b-another-name`, `01x-hires-village` | |
| 5 | Smooth scrolling | `chain/02-scrolling` | `02a-slow-camera`, `02b-fast-camera`, `02x-colours-left-behind` | |
| 6 | Oscar walks | `chain/03-oscar` | `03b-faster-walk`, `03x-sign-lost` | |
| 7 | Jumps and solid ground | `chain/03-oscar` | `03a-higher-jump` | |
| 8 | The bat | `chain/04-bat` | `04a-tireless-bat`, `04b-slow-descent`, `04x-endless-energy` | |
| 9 | Heirlooms, the gate and the night | `chain/05-heirlooms-and-gate` | `05a-chalice-on-the-street`, `05b-short-night`, `05x-taken-again` | |
| 10 | The enemies | `chain/06-enemies` | `06a-watchman-at-the-start`, `06b-hard-night`, `06x-pointers-of-one-screen` | |
| 11 | The Count's staff | `chain/07-staff` | `07a-slower-blow`, `07b-moon-on-the-left`, `07x-endless-puff` | |
| 12 | Packed levels and the castle | `chain/08-packed-levels`, `chain/09-castle` | `08a-slower-wisps`, `08b-still-wisps`, `08x-repeat-too-near`, `09a-purple-night`, `09b-brown-stone`, `09x-grey-dots` | |
| 13 | Tom Darkfang | `chain/10-tom` | `10b-higher-leaps`, `10x-unmirrored` | |
| 14 | The fight with Tom | `chain/10-tom` | `10a-four-blows` | `tests/fight.py` |
| 15 | The SID and the music | `chain/11-music` | `11a-faster-theme`, `11b-plain-melody`, `11x-notes-held` | |
| 16 | States, title and menu | `chain/12-title-and-ends` | | |
| 17 | The tally, dawn and victory | `chain/12-title-and-ends` | `12a-morning-words`, `12b-night-worth-more`, `12x-band-a-row-down` | |
| 18 | Effects, jingles and the disk | `chain/13-complete` | `13x-effect-held` | `tools/make_disk.py`, `tools/load_time.py`, `tools/record_music.py` |
| 19 | Reading and checking the game | `chain/13-complete`, `game` | | `tests/`, `tools/memory_map.py`, `tools/load_time.py`, `tools/check_lines.py` |
| 20 | Glossary and index | | | |

Step 13 is the complete game, Dreadcastle 1.0, byte for byte; `game/`
holds its master source, from which `tools/make_chain.py` makes the
thirteen steps.

## The experiments

| Folder | Chapter | Kind | Title | Its test |
|---|---|---|---|---|
| `variants/01-village-at-night/01a-churchyard-first` | 3 | variant | The churchyard first | PASS |
| `variants/01-village-at-night/01b-another-name` | 4 | variant | Another name | PASS |
| `variants/01-village-at-night/01x-hires-village` | 4 | where it breaks | The village in thin stripes | FAIL, as it must |
| `variants/02-scrolling/02a-slow-camera` | 5 | variant | A slow camera | PASS |
| `variants/02-scrolling/02b-fast-camera` | 5 | variant | A camera faster than the back screen | PASS |
| `variants/02-scrolling/02x-colours-left-behind` | 5 | where it breaks | Colours left behind | FAIL, as it must |
| `variants/03-oscar/03b-faster-walk` | 6 | variant | A faster walk | PASS |
| `variants/03-oscar/03x-sign-lost` | 6 | where it breaks | A step to the left, 256 pixels to the right | FAIL, as it must |
| `variants/03-oscar/03a-higher-jump` | 7 | variant | A higher jump | PASS |
| `variants/04-bat/04a-tireless-bat` | 8 | variant | A tireless bat | PASS |
| `variants/04-bat/04b-slow-descent` | 8 | variant | A slow descent | PASS |
| `variants/04-bat/04x-endless-energy` | 8 | where it breaks | Endless energy | FAIL, as it must |
| `variants/05-heirlooms-and-gate/05a-chalice-on-the-street` | 9 | variant | The chalice on the street | PASS |
| `variants/05-heirlooms-and-gate/05b-short-night` | 9 | variant | A night of one minute | PASS |
| `variants/05-heirlooms-and-gate/05x-taken-again` | 9 | where it breaks | The same heirloom three times | FAIL, as it must |
| `variants/06-enemies/06a-watchman-at-the-start` | 10 | variant | A watchman at the start | PASS |
| `variants/06-enemies/06b-hard-night` | 10 | variant | A hard night | PASS |
| `variants/06-enemies/06x-pointers-of-one-screen` | 10 | where it breaks | Enemies of one screen | FAIL, as it must |
| `variants/07-staff/07a-slower-blow` | 11 | variant | A slower blow | PASS |
| `variants/07-staff/07b-moon-on-the-left` | 11 | variant | The moon on the left | PASS |
| `variants/07-staff/07x-endless-puff` | 11 | where it breaks | A puff that never ends | FAIL, as it must |
| `variants/08-packed-levels/08a-slower-wisps` | 12 | variant | Slower wisps | PASS |
| `variants/08-packed-levels/08b-still-wisps` | 12 | variant | Still wisps | PASS |
| `variants/08-packed-levels/08x-repeat-too-near` | 12 | where it breaks | A repeat from one byte nearer | FAIL, as it must |
| `variants/09-castle/09a-purple-night` | 12 | variant | A purple night over the castle | PASS |
| `variants/09-castle/09b-brown-stone` | 12 | variant | A hall of brown stone | PASS |
| `variants/09-castle/09x-grey-dots` | 12 | where it breaks | Grey dots over the HUD | FAIL, as it must |
| `variants/10-tom/10b-higher-leaps` | 13 | variant | Higher leaps | PASS |
| `variants/10-tom/10x-unmirrored` | 13 | where it breaks | Tom not turned round | FAIL, as it must |
| `variants/10-tom/10a-four-blows` | 14 | variant | Four blows for Tom | PASS |
| `variants/11-music/11a-faster-theme` | 15 | variant | A faster theme | PASS |
| `variants/11-music/11b-plain-melody` | 15 | variant | A plain melody | PASS |
| `variants/11-music/11x-notes-held` | 15 | where it breaks | Notes that never let go | FAIL, as it must |
| `variants/12-title-and-ends/12a-morning-words` | 17 | variant | Other words at dawn | PASS |
| `variants/12-title-and-ends/12b-night-worth-more` | 17 | variant | A night worth more | PASS |
| `variants/12-title-and-ends/12x-band-a-row-down` | 17 | where it breaks | The band a row down | FAIL, as it must |
| `variants/13-complete/13x-effect-held` | 18 | where it breaks | An effect that does not end | FAIL, as it must |

Every folder has a README: where the change is, the lines before and
after, what you will see, the limits, what else depends on it, how it
was proved and how to go back to the step. The reports of the tests
and their captures are in `variants/NN-name/evidence/ID/`.

## The tools

| File | What it does |
|---|---|
| `tools/run-game.ps1` | Builds a step, a variant or the complete game and starts it in VICE (chapter 1); every folder has a copy |
| `tools/check_lines.py` | Stops the build if a source line is longer than 60 characters, the width of the book's listings |
| `tools/make_chain.py` | Makes the steps of `chain/` from the master source `game/src` and its step tags, with the READMEs of `chain/readme` |
| `tools/check_chain.py` | Checks each step against the master: a branch to an anonymous label lands where it does in the complete game, and the code falls into each label as it does there; lists the seams, the lines of earlier steps only |
| `tools/make_variants.py`, `tools/variants.py` | Make `variants/` again from the steps and the list of changes. Each folder is made from nothing; `--test` runs the tests and writes the reports again, `--readme` only the READMEs |
| `tools/verify-step.ps1`, `tools/verify-variants.ps1` | On Windows: build a step and run its test; build and prove every variant |
| `tools/make_disk.py` | Puts the complete game on a 1541 disk image with VICE's `c1541` (chapter 18) |
| `tools/load_time.py` | Times the loading of the program from that image in an emulated 1541, then starts it (chapter 18) |
| `tools/record_music.py` | Records the theme, Tom's theme, the jingles and the sound effects from the SID of VICE into WAV files (chapter 18) |
| `tools/memory_map.py` | The memory of the complete game, area by area, and the free gaps (chapter 19) |

`tests/` holds the tests themselves: `verify_game.py`, which plays a
step or the complete game in VICE and compares every frame with the
model of the game (`game_model.py`, with `player_model.py` for the
music and `fight.py`, the player of the fight with Tom); `reference.py`,
which draws the screens again from the data files; `step_routes.py`
and `routes/`, the routes of the steps and of the variants that have
their own; `levels.py`, which shows on the model that every level can
be finished; `mutate_steps.py` and `mutate_game.py`, which put
one-line faults into copies and check that the tests stop them; and
`vicemon.py`, which drives VICE through its monitor.
