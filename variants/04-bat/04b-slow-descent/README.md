# A slow descent

Step 04 (`chain/04-bat`), a guided variant.

Let go, the bat falls at 0.625 pixels a frame at most, instead of 1.25.

## What changes

In `game/src/bat.asm`:

```
BAT_FALL_MAX  = $0140           ; 1.25 pixels a frame, most
```

becomes

```
BAT_FALL_MAX  = $00a0           ; 0.625 pixels a frame, most
```

## Where

`game/src/bat.asm`, `BAT_FALL_MAX`: the top speed of the fall, let go
(with Down held the dive has its own, `BAT_DIVE_MAX`).

## What you see

From the top of the sky to the roof over the start the bat floats down
in 71 frames instead of 39; Down still dives as fast as before.

## Limits

Below `BAT_GRAVITY` ($0020) the speed would be reached in one frame and
the fall would look flat.

## What depends on it

Nothing else: perching, beats and energy are the same.

## How it was proved

The test of step 04 (`tests/verify_game.py`) compared the program with
its model at every frame, the model changed in the same way
(`numbers['BAT_FALL_MAX'] = 0x00a0`), on a route of its own
(`tests/routes/variant_04b.py`): PASS, 34 checks, 213 frames. Facts:

- down from the top in 71 frames: yes

To go back, undo the change above.
