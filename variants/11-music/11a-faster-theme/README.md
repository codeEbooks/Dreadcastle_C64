# A faster theme

Step 11 (`chain/11-music`), a guided variant.

Every step of the theme lasts 4 frames: 16 frames a beat, about 188
beats a minute, instead of 19 (158).

## What changes

In `game/assets/music.py`:

```
TEMPO = [5, 5, 5, 4]                # the theme: frames a step
```

becomes

```
TEMPO = [4, 4, 4, 4]                # the theme: frames a step
```

## Where

`game/assets/music.py`, `TEMPO`: the frames of each step of the theme,
in turn; `music.py` compiles them into the song's tempo table.

## What you see

The same tune, faster; the player still plays one step of the song when
its count runs out.

## Limits

Frames are the unit: 4 frames a step is 187.5 beats a minute, 5 is 150;
the mix of 5, 5, 5, 4 gives 158.

## What depends on it

Tom's theme has its own `TEMPO` (in `boss.py`).

## How it was proved

The test of step 11 (`tests/verify_game.py`) compared the program with
its model at every frame, on a route of its own
(`tests/routes/variant_11.py`): PASS, 42 checks, 1200 frames. Facts:

- the theme shorter in frames: yes

To go back, undo the change above.
