# A puff that never ends

Step 07 (`chain/07-staff`), where it breaks: a mistake made on purpose.

The frames of a struck enemy's puff are never counted down.

## What changes

In `game/src/enemies.asm`:

```
        dec en_gone,x           ; the puff

```

becomes

```

```

## What you see

A struck enemy turns into a puff of smoke, and stays a puff: it never
goes, and never comes back.

## Why

`en_gone` counts the puff's frames down to the end, when the enemy is
gone; without the `dec`, the count stays where it started.

## How the test stops it

The test of step 07 stops at "the enemies' variables equal the model":
frame 9204 (its puff, then nothing): [[0, 64, 128, 0, 0, 0, 255, 255],
[18, 254, 74, 193, 225, 28, 255, 255], [1, 1, 3, 4, 5, 7, 191, 255],
[224, 0, 0, 0, 0, 0, 255, 255], [130, 144, 144, 62, 110, 144, 255, 255],
[0, 0, 0, 0, 0, 0, 255, 255], [1, 0, 0, 0, 0, 0, 255, 255], [160, 0, 0,
0, 0, 0, 255, 255], [253, 0, 0, 0, 0, 0, 255, 255], [0, 1, 0, 1, 1, 1,
255, 255], [60, 91, 91, 27, 27, 7, 255, 255], [1, 0, 0, 0, 0, 0, 255,
255], [1, 1, 1, 1, 1, 0, 255, 255], [12, 0, 0, 0, 0, 0, 255, 255]] model
[[0, 64, 128, 0, 0, 0, None, None], [18, 254, 74, 193, 225, 28, None,
None], [1, 1, 3, 4, 5, 7, None, None], [224, 0, 0, 0, 0, 0, None, None],
[130, 144, 144, 62, 110, 144, None, None], [0, 0, 0, 0, 0, 0, None,
None], [1, 0, 0, 0, 0, 0, None, None], [160, 0, 0, 0, 0, 0, None, None],
[253, 0, 0, 0, 0, 0, None, None], [0, 1, 0, 1, 1, 1, None, None], [60,
91, 91, 27, 27, 7, None, None], [1, 0, 0, 0, 0, 0, None, None], [1, 1,
1, 1, 1, 0, None, None], [11, 0, 0, 0, 0, 0, None, None]].

The capture, 30 frames later: `endless-puff.png` (in
`variants/07-staff/evidence/07x-endless-puff/`).

To repair it, undo the change above.
