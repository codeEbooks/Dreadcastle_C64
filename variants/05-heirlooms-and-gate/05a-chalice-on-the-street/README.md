# The chalice on the street

Step 05 (`chain/05-heirlooms-and-gate`), a guided variant.

The first heirloom moved from the awning of the stall to the street by
the start: the objects are data.

## What changes

In `game/assets/level1.py`:

```
HEIRLOOMS = [(22, 80, "chalice"),       # on the awning, h3
```

becomes

```
HEIRLOOMS = [(6, 128, "chalice"),       # on the street
```

## Where

`game/assets/level1.py`, `HEIRLOOMS`: the metatile column of each, the
line of the top of its 16 x 16 box and its kind.

## What you see

The chalice bobs over the street a few steps from the start; Oscar takes
it walking, and the HUD counts 1/3.

## Limits

Its box must be where Oscar can reach it: on a surface, or within a jump
or a flight. Three heirlooms a level (`HEIRLOOM_COUNT`).

## What depends on it

`load_objects` copies the level's objects into `OBJECTS`: nothing in the
code changes.

## How it was proved

The test of step 05 (`tests/verify_game.py`) compared the program with
its model at every frame, on a route of its own
(`tests/routes/variant_05a.py`): PASS, 36 checks, 87 frames. Facts:

- taken by walking: yes

To go back, undo the change above.
