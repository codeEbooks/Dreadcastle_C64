# A hard night

Step 06 (`chain/06-enemies`), a guided variant.

A touch takes four notches of health instead of two: two touches, and
Oscar is back at the lantern.

## What changes

In `game/src/enemies.asm`:

```
HIT_DAMAGE    = 2               ; a character of the bar
```

becomes

```
HIT_DAMAGE    = 4               ; two characters of the bar
```

## Where

`game/src/enemies.asm`, `HIT_DAMAGE`: what `hurt` takes from `health`
(8: the four characters of the bar, two notches each).

## What you see

In the churchyard the cat jumps at Oscar: half of the bar goes at once.

## Limits

`HEALTH_FULL` (8) should be a multiple of it, or the last touch leaves a
notch that only the next one takes.

## What depends on it

The brambles and the hazards of later steps hurt with the same `hurt`.

## How it was proved

The test of step 06 (`tests/verify_game.py`) compared the program with
its model at every frame, the model changed in the same way
(`numbers['HIT_DAMAGE'] = 4`), on a route of its own
(`tests/routes/variant_06b.py`): PASS, 40 checks, 404 frames. Facts:

- four notches at the first touch: yes

To go back, undo the change above.
