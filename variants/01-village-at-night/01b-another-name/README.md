# Another name

Step 01 (`chain/01-village-at-night`), a guided variant.

The level's name in the HUD is data: THE SLEEPING VILLAGE instead of
VILLAGE OF MORTALS.

## What changes

In `game/assets/level1.py`:

```
NAME = "VILLAGE OF MORTALS"
```

becomes

```
NAME = "THE SLEEPING VILLAGE"
```

## Where

`game/assets/level1.py`, `NAME`; `build_assets.py` turns it into row 24
of the HUD (`name_row`): the level's number, the name in cyan, the
score.

## What you see

Row 24 of the HUD with the new name; `show_name` copies its 40
characters and 40 colours into both screens and the colour RAM.

## Limits

At most 30 characters, and only letters the HUD's font has (`font.py`);
the score keeps its place.

## What depends on it

Nothing else: the name is copied as it is.

## How it was proved

The test of step 01 (`tests/verify_game.py`) compared the program with
its model at every frame, on the route of the step: PASS, 32 checks, 100
frames. Facts:

- the new name in the HUD's last row: yes

To go back, undo the change above.
