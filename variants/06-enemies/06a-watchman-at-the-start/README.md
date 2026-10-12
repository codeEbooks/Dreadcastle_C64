# A watchman at the start

Step 06 (`chain/06-enemies`), a guided variant.

The first night watchman walks his round by the start, columns 1 to 7,
instead of beyond the trapdoor: the enemies are data.

## What changes

In `game/assets/level1.py`:

```
ENEMIES = [("patrol", 32, 40, 36, "street", "left"),      # A
```

becomes

```
ENEMIES = [("patrol", 1, 7, 5, "street", "left"),        # A
```

## Where

`game/assets/level1.py`, `ENEMIES`: for each enemy its kind, the first
and last metatile column of its stretch, the column where it starts,
what it stands on and where it faces.

## What you see

As soon as the level starts the watchman walks towards Oscar: a touch,
two notches of health, Oscar thrown back and blinking; the watchman
turns at the end of his stretch and comes back.

## Limits

A patrol's stretch must be on its surface; at most `MAX_ENEMIES` (8) in
a level, and four on the screen at once (sprites 3-6).

## What depends on it

`load_objects` copies the level's enemies; `reset_enemies` puts each at
its start.

## How it was proved

The test of step 06 (`tests/verify_game.py`) compared the program with
its model at every frame, on a route of its own
(`tests/routes/variant_06a.py`): PASS, 38 checks, 269 frames. Facts:

- a hit while Oscar waits: yes
- two notches of health: yes

To go back, undo the change above.
