# The same heirloom three times

Step 05 (`chain/05-heirlooms-and-gate`), where it breaks: a mistake made
on purpose.

Taking an heirloom no longer sets its bit in `got_bits`.

## What changes

In `game/src/objects.asm`:

```
        lda got_bits
        ora heirloom_bit,x
        sta got_bits

```

becomes

```
        lda got_bits
        sta got_bits

```

## What you see

Oscar touches the chalice: it stays where it is, and the HUD counts on
past 3/3 (6/3 in the capture) while he stands by it; at 3 the gate
opened.

## Why

`touch_heirlooms` skips an heirloom whose bit is set in `got_bits`.
Without the `ora`, the bit is never set: in every frame that Oscar
touches the chalice it is taken again, `got` goes on counting, and at 3
`open_gate` runs. The chalice is still drawn: for `place_heirloom` it
has not been taken.

## How the test stops it

The test of step 05 stops at "the level's variables equal the model":
frame 277 (level 1: the way of levels.py, move 11): [8, 16, 98, 0, 1, 0,
0, 0, 0, 134, 28, 0, 0, 135, 135] model [8, 16, 98, 0, 1, 1, 0, 0, 0,
134, 28, 0, 0, None, None].

The capture, 30 frames later: `taken-again.png` (in
`variants/05-heirlooms-and-gate/evidence/05x-taken-again/`).

To repair it, undo the change above.
