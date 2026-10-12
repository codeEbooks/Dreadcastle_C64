# A night of one minute

Step 05 (`chain/05-heirlooms-and-gate`), a guided variant.

A step of the night lasts 188 frames instead of 375: the 16 steps of the
bar go by in one minute.

## What changes

In `game/src/objects.asm`:

```
NIGHT_STEP    = 375             ; frames: 7.5 s, 2 minutes
```

becomes

```
NIGHT_STEP    = 188             ; frames: 3.76 s, 1 minute
```

## Where

`game/src/objects.asm`, `NIGHT_STEP`: the frames of one of the 16 steps
of the bar of the night.

## What you see

The bar of the night empties twice as fast; at dawn the level starts
again, its heirlooms back in place.

## Limits

`NIGHT_STEP` is a 16-bit count (`night_time`); `NIGHT_STEPS` stays 16:
the bar has 8 characters of 2 steps (a `.cerror` says so).

## What depends on it

In step 12 the steps left at the gate become points: a shorter night
gives fewer.

## How it was proved

The test of step 05 (`tests/verify_game.py`) compared the program with
its model at every frame, the model changed in the same way
(`numbers['NIGHT_STEP'] = 188`), on a route of its own
(`tests/routes/variant_05b.py`): PASS, 34 checks, 3088 frames. Facts:

- dawn after 16 x 188 frames: yes

To go back, undo the change above.
