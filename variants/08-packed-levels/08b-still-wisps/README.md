# Still wisps

Step 08 (`chain/08-packed-levels`), a guided variant.

The mire left out of the settings that flicker: its wisps keep their
first picture.

## What changes

In `game/assets/build_assets.py`:

```
FLICKER = {"marsh": "wisps", "pass": "spikes", "keep": "spikes",
```

becomes

```
FLICKER = {"pass": "spikes", "keep": "spikes",
```

## Where

`game/assets/build_assets.py`, `FLICKER`: the settings whose hazards
flicker and the pictures they use; `env_flicker` gets a 0 for the
others.

## What you see

The wisps hang still over the pools; they hurt as before: a hazard is a
flag of its metatile, not a picture.

## Limits

One page of pictures for each setting in the table.

## What depends on it

`flicker_hazards` reads `env_flicker` and does nothing where it is 0.

## How it was proved

The test of step 08 (`tests/verify_game.py`) compared the program with
its model at every frame, on a route of its own
(`tests/routes/variant_08.py`): PASS, 41 checks, 144 frames. Facts:

- no picture of the mire's wisps changed: yes

To go back, undo the change above.
