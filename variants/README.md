# Variants and breaks of the chain

Each folder is a step of `chain/` with one change. A guided variant (a, b) changes one idea and is proved by the test of its step, its model changed in the same way; a break (x) is a classic mistake that the test of its step stops. Built and proved by `tools/make_variants.py --test`; results in `variants.json`, reports and captures in `NN-name/evidence/`.

| Step | Folder | Kind | What | Proved |
|---|---|---|---|---|
| 01 | `01-village-at-night/01a-churchyard-first` | variant | The churchyard first | yes |
| 01 | `01-village-at-night/01b-another-name` | variant | Another name | yes |
| 01 | `01-village-at-night/01x-hires-village` | break | The village in thin stripes | yes |
| 02 | `02-scrolling/02a-slow-camera` | variant | A slow camera | yes |
| 02 | `02-scrolling/02b-fast-camera` | variant | A camera faster than the back screen | yes |
| 02 | `02-scrolling/02x-colours-left-behind` | break | Colours left behind | yes |
| 03 | `03-oscar/03a-higher-jump` | variant | A higher jump | yes |
| 03 | `03-oscar/03b-faster-walk` | variant | A faster walk | yes |
| 03 | `03-oscar/03x-sign-lost` | break | A step to the left, 256 pixels to the right | yes |
| 04 | `04-bat/04a-tireless-bat` | variant | A tireless bat | yes |
| 04 | `04-bat/04b-slow-descent` | variant | A slow descent | yes |
| 04 | `04-bat/04x-endless-energy` | break | Endless energy | yes |
| 05 | `05-heirlooms-and-gate/05a-chalice-on-the-street` | variant | The chalice on the street | yes |
| 05 | `05-heirlooms-and-gate/05b-short-night` | variant | A night of one minute | yes |
| 05 | `05-heirlooms-and-gate/05x-taken-again` | break | The same heirloom three times | yes |
| 06 | `06-enemies/06a-watchman-at-the-start` | variant | A watchman at the start | yes |
| 06 | `06-enemies/06b-hard-night` | variant | A hard night | yes |
| 06 | `06-enemies/06x-pointers-of-one-screen` | break | Enemies of one screen | yes |
| 07 | `07-staff/07a-slower-blow` | variant | A slower blow | yes |
| 07 | `07-staff/07b-moon-on-the-left` | variant | The moon on the left | yes |
| 07 | `07-staff/07x-endless-puff` | break | A puff that never ends | yes |
| 08 | `08-packed-levels/08a-slower-wisps` | variant | Slower wisps | yes |
| 08 | `08-packed-levels/08b-still-wisps` | variant | Still wisps | yes |
| 08 | `08-packed-levels/08x-repeat-too-near` | break | A repeat from one byte nearer | yes |
| 09 | `09-castle/09a-purple-night` | variant | A purple night over the castle | yes |
| 09 | `09-castle/09b-brown-stone` | variant | A hall of brown stone | yes |
| 09 | `09-castle/09x-grey-dots` | break | Grey dots over the HUD | yes |
| 10 | `10-tom/10a-four-blows` | variant | Four blows for Tom | yes |
| 10 | `10-tom/10b-higher-leaps` | variant | Higher leaps | yes |
| 10 | `10-tom/10x-unmirrored` | break | Tom not turned round | yes |
| 11 | `11-music/11a-faster-theme` | variant | A faster theme | yes |
| 11 | `11-music/11b-plain-melody` | variant | A plain melody | yes |
| 11 | `11-music/11x-notes-held` | break | Notes that never let go | yes |
| 12 | `12-title-and-ends/12a-morning-words` | variant | Other words at dawn | yes |
| 12 | `12-title-and-ends/12b-night-worth-more` | variant | A night worth more | yes |
| 12 | `12-title-and-ends/12x-band-a-row-down` | break | The band a row down | yes |
| 13 | `13-complete/13x-effect-held` | break | An effect that does not end | yes |
