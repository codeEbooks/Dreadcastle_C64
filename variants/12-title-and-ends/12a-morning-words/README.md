# Other words at dawn

Step 12 (`chain/12-title-and-ends`), a guided variant.

At dawn the band says MORNING HAS COME! instead of THE SUN HAS RISEN!

## What changes

In `game/assets/title.py`:

```
"dawn": (2, 5, [(3, WHITE, "THE SUN HAS RISEN!"),
```

becomes

```
"dawn": (2, 5, [(3, WHITE, "MORNING HAS COME!"),
```

## Where

`game/assets/title.py`, `BANDS`: each band's first row, its rows and its
words (row, colour, text).

## What you see

The band of dawn over the village with the new words.

## Limits

The letters of the HUD's font (`font.py`): no J, Q or X; 40 characters a
row.

## What depends on it

`show_band` copies the band as it is.

## How it was proved

The test of step 12 (`tests/verify_game.py`) compared the program with
its model at every frame, on a route of its own
(`tests/routes/variant_12a.py`): PASS, 52 checks, 288 frames. Facts:

- dawn reached: yes

To go back, undo the change above.
