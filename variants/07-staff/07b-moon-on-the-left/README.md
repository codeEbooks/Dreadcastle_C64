# The moon on the left

Step 07 (`chain/07-staff`), a guided variant.

The moon of the wood high on the left of the sky instead of on the
right.

## What changes

In `game/assets/moon.py`:

```
X_REGISTER = 296                    # screen pixels 272-293
```

becomes

```
X_REGISTER = 72                     # screen pixels 48-69
```

## Where

`game/assets/moon.py`, `X_REGISTER`: the moon's X in the sprite
registers (the screen's left edge is 24).

## What you see

The moon on the left of the wood's sky, still while the level scrolls; X
under 256 needs no ninth bit in $D010.

## Limits

The moon is a sprite behind the characters ($D01B): trees and hills
cover it wherever it is.

## What depends on it

Sprite 6 is the moon's only in the settings with a moon; `place_enemies`
leaves its bits alone.

## How it was proved

The test of step 07 (`tests/verify_game.py`) compared the program with
its model at every frame, on a route of its own
(`tests/routes/variant_07b.py`): PASS, 41 checks, 90 frames. Facts:

- the moon at X 72: yes

To go back, undo the change above.
