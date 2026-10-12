# A repeat from one byte nearer

Step 08 (`chain/08-packed-levels`), where it breaks: a mistake made on
purpose.

In `unpack`, a repeat copies from one byte nearer than the stream says.

## What changes

In `game/src/unpack.asm`:

```
        eor #$ff                ; - (D + 1) is $ff00 + ~D
        clc
```

becomes

```
        eor #$ff                ; - (D + 1) is $ff00 + ~D
        sec
```

## What you see

From the very start the village is a jumble: pieces of roofs and windows
scattered over the sky, walls in the wrong colours. From this step every
level, the first too, comes out of `unpack`.

## Why

A repeat copies earlier output from D + 1 bytes back; `eor #$ff` and
`clc` then `adc` make the low byte of - (D + 1). With `sec` the sum is
one more: D bytes back, a byte too near, and every repeat copies the
wrong bytes: the map, the setting's tables and its characters are all
wrong.

## How the test stops it

The test of step 08 stops at "the level in memory equals the model's":
frame 1 (still at the start): the level differs.

The capture, 60 frames later: `repeat-too-near.png` (in
`variants/08-packed-levels/evidence/08x-repeat-too-near/`).

To repair it, undo the change above.
