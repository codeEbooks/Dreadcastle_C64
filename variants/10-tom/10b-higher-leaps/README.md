# Higher leaps

Step 10 (`chain/10-tom`), a guided variant.

Tom leaps off the ground at 7 pixels a frame instead of 6.

## What changes

In `game/src/tom.asm`:

```
LEAP_VY       = $0600           ; 6 pixels a frame up
```

becomes

```
LEAP_VY       = $0700           ; 7 pixels a frame up
```

## Where

`game/src/tom.asm`, `LEAP_VY`: the speed up of his leap; `TOM_GRAVITY`
brings him down.

## What you see

Tom's leaps go higher and last longer: more time for Oscar to walk under
him, and he lands further on.

## Limits

The arena's ceiling: from the floor, (7 x 7) / (2 x gravity) lines up
must stay under the top of the playfield.

## What depends on it

The test's model leaps the same way; its fighter (`tests/fight.py`)
looks at the model, so it waits for the longer leap.

## How it was proved

The test of step 10 (`tests/verify_game.py`) compared the program with
its model at every frame, the model changed in the same way
(`numbers['LEAP_VY'] = 0x0700`), on a route of its own
(`tests/routes/variant_10.py`): PASS, 46 checks, 1437 frames. Facts:

- Tom beaten and gone: yes

To go back, undo the change above.
