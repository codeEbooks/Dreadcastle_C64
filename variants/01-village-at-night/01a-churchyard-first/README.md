# The churchyard first

Step 01 (`chain/01-village-at-night`), a guided variant.

The program starts in level 2, the Churchyard: the level is a number,
and everything else is data.

## What changes

In `game/src/main.asm`:

```
        lda #0                  ; level 1
```

becomes

```
        lda #1                  ; level 2
```

## Where

`game/src/main.asm`, at `entry`: the number given to `load_level` in
`level_no` (0 for level 1).

## What you see

The Churchyard at night, its graves and its chapel, with 2 THE
CHURCHYARD in the HUD. `load_level` takes the map, the setting and the
name of whatever level `level_no` says; the churchyard shares the
village's characters, so nothing else is needed.

## Limits

In this step the data of levels 1 to 3 are in memory (`plain.asm`): 0, 1
or 2. Level 3, the Wild Wood, needs characters of its own, which this
step does not copy into place yet (step 07 does).

## What depends on it

The test's model starts at the same level (`first_level`).

## How it was proved

The test of step 01 (`tests/verify_game.py`) compared the program with
its model at every frame, the model changed in the same way
(`game_model.Game.first_level = 1`), on the route of the step: PASS, 32
checks, 100 frames. Facts:

- level 2 on the screen: yes
- its name in the HUD's last row: yes

To go back, undo the change above.
