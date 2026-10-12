# A faster walk

Step 03 (`chain/03-oscar`), a guided variant.

Oscar walks at 2.25 pixels a frame at most, instead of 1.5.

## What changes

In `game/src/oscar.asm`:

```
WALK_MAX      = $0180           ; 1.5 pixels a frame
```

becomes

```
WALK_MAX      = $0240           ; 2.25 pixels a frame
```

## Where

`game/src/oscar.asm`, `WALK_MAX`: the top speed of the walk;
`WALK_ACCEL` takes him there, 1/16 of a pixel more each frame.

## What you see

He reaches the crates in 55 frames instead of 67, and takes longer to
stop (`WALK_FRICTION`).

## Limits

The camera follows him at his speed: above 8 pixels a frame it would
skip columns, and above 2 the back screen is not ready in time (see step
02): the camera waits, and he gets ahead of it.

## What depends on it

The jumps are longer too: their length is the speed across times the
time in the air.

## How it was proved

The test of step 03 (`tests/verify_game.py`) compared the program with
its model at every frame, the model changed in the same way
(`numbers['WALK_MAX'] = 0x0240`), on a route of its own
(`tests/routes/variant_03b.py`): PASS, 31 checks, 95 frames. Facts:

- at the crates in 55 frames: yes

To go back, undo the change above.
