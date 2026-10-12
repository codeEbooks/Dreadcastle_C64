# The band a row down

Step 12 (`chain/12-title-and-ends`), where it breaks: a mistake made on
purpose.

The band's raster line 8 lines lower than its rows.

## What changes

In `game/src/states.asm`:

```
BAND_LINE     = 53
```

becomes

```
BAND_LINE     = 61
```

## What you see

LEVEL CLEAR! half drawn: the top lines of its letters are missing, so
that L looks like C and E like C.

## Why

The band is drawn with characters of its own: an interrupt at
`BAND_LINE` switches $D018 to them and another switches back. 8 lines
lower, the top of the band's row is still drawn with the playfield's
set, where those character codes are empty sky.

## How the test stops it

The test of step 12 stops at "dreadcastle-clear.png": 224 pixels differ.

The capture, 0 frames later: `dreadcastle-clear.png` (in
`variants/12-title-and-ends/evidence/12x-band-a-row-down/`).

To repair it, undo the change above.
