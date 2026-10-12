# A purple night over the castle

Step 09 (`chain/09-castle`), a guided variant.

Dreadcastle Gate under a purple sky instead of a blue one.

## What changes

In `game/assets/keep.py`:

```
SKY = BLUE                              # $d021 here: the night
```

becomes

```
SKY = PURPLE                            # $d021 here: the night
```

## Where

`game/assets/keep.py`, `SKY`: the colour of the keep's background, $D021
of its setting (`env_d021`).

## What you see

The sky of level 7 purple; the HUD stays black, because its interrupt
sets its own $D021 at line 226.

## Limits

$D021 is the background of every character: it must be a colour the
pictures of the keep do not use as one of their own.

## What depends on it

The top interrupt writes `play_d021`, set from `env_d021` when the level
starts.

## How it was proved

The test of step 09 (`tests/verify_game.py`) compared the program with
its model at every frame, on a route of its own
(`tests/routes/variant_09.py`): PASS, 43 checks, 180 frames. Facts:

- the gate's sky purple: yes

To go back, undo the change above.
