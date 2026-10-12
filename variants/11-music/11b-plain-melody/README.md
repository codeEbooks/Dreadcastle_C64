# A plain melody

Step 11 (`chain/11-music`), a guided variant.

The lead instrument of the theme without its vibrato.

## What changes

In `game/assets/score.py`:

```
                  sweep=0x18, vibrato=18),
```

becomes

```
                  sweep=0x18, vibrato=0),
```

## Where

`game/assets/score.py`, `INSTRUMENTS['lead']`: `vibrato` is the delay,
in frames, before a long note starts to wobble; 0: never.

## What you see

The long notes of the melody stay flat; the rest of the theme is the
same.

## Limits

The vibrato's depth is a table of `player.asm` (`vibrato_table`), the
same for every instrument.

## What depends on it

The player reads the instrument's bytes as the compiled song gives them.

## How it was proved

The test of step 11 (`tests/verify_game.py`) compared the program with
its model at every frame, on a route of its own
(`tests/routes/variant_11.py`): PASS, 42 checks, 1200 frames. Facts:

- the theme played: yes

To go back, undo the change above.
