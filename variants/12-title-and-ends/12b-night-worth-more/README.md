# A night worth more

Step 12 (`chain/12-title-and-ends`), a guided variant.

A step of the night left counts 75 points instead of 50.

## What changes

In `game/src/states.asm`:

```
NIGHT_POINTS  = $50             ; a step of the night: 50
```

becomes

```
NIGHT_POINTS  = $75             ; a step of the night: 75
```

## Where

`game/src/states.asm`, `NIGHT_POINTS`: in BCD, two decimal digits in a
byte ($75 is 75).

## What you see

At the victory (and at every gate) each step of the night left adds 75
to the score.

## Limits

BCD: the decimal flag (`sed`) makes `adc` add decimal digits; `$7A`
would not be a number.

## What depends on it

The test's model adds the same points (`night_points`).

## How it was proved

The test of step 12 (`tests/verify_game.py`) compared the program with
its model at every frame, the model changed in the same way
(`game_model.Game.night_points = 75`), on a route of its own
(`tests/routes/variant_12b.py`): PASS, 56 checks, 2013 frames. Facts:

- the score a multiple of 75 more than Tom's 5000: yes

To go back, undo the change above.
