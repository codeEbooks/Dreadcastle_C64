# A higher jump

Step 03 (`chain/03-oscar`), a guided variant.

Oscar leaves the ground at 4 pixels a frame instead of 3.47: Up held, he
rises 62 lines instead of 47.

## What changes

In `game/src/oscar.asm`:

```
JUMP_SPEED    = $0378           ; 3.47 pixels a frame up;
```

becomes

```
JUMP_SPEED    = $0400           ; 4 pixels a frame up;
```

## Where

`game/src/oscar.asm`, `JUMP_SPEED`: the speed up when he leaves the
ground, in 1/256 of a pixel a frame.

## What you see

The jump goes higher and lasts longer; with Up let go early it is still
short, because `GRAVITY` (let go) is stronger than `GRAVITY_HOLD`
(held).

## Limits

The height grows with the square of the speed: (speed in pixels)^2 / (2
x 0.125). The levels are drawn for a jump of 2 metatiles, never 3: with
this one he climbs 3, and places meant for the bat or for a longer way
round may come within a jump.

## What depends on it

The test's model jumps with the same number (`numbers['JUMP_SPEED']`).

## How it was proved

The test of step 03 (`tests/verify_game.py`) compared the program with
its model at every frame, the model changed in the same way
(`numbers['JUMP_SPEED'] = 0x0400`), on a route of its own
(`tests/routes/variant_03a.py`): PASS, 32 checks, 84 frames. Facts:

- 62 lines up, Up held: yes

To go back, undo the change above.
