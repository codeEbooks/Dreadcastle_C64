# A step to the left, 256 pixels to the right

Step 03 (`chain/03-oscar`), where it breaks: a mistake made on purpose.

Moving left, the speed is added to his position without its sign in the
top byte.

## What changes

In `game/src/oscar.asm`:

```
        lda osc_vx + 1
        bpl +
        dex

```

becomes

```
        lda osc_vx + 1
        bpl +
        nop

```

## What you see

Oscar walks left from the start and, at the first frame, is 256 pixels
further right; the camera runs after him.

## Why

Positions have three bytes (fraction, pixels, 256s of pixels), speeds
two. A speed to the left is negative: $FFF0 is -16. Added to three
bytes, its third byte must be $FF, the sign carried on (`dex` makes X
$FF); with 0 the carry out of the second byte is not cancelled, and the
third byte goes up by one: 256 pixels.

## How the test stops it

The test of step 03 stops at "Oscar's variables equal the model": frame
36 (walk left to the end of the level): [240, 27, 1, 0, 144, 240, 255,
0, 0, 1, 1, 16, 0, 7, 4] model [240, 27, 0, 0, 144, 240, 255, 0, 0, 1,
1, 16, 0, 7, 4].

The capture, 30 frames later: `sign-lost.png` (in
`variants/03-oscar/evidence/03x-sign-lost/`).

To repair it, undo the change above.
