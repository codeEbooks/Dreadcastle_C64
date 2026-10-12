# A tireless bat

Step 04 (`chain/04-bat`), a guided variant.

A beat costs 4 units of energy instead of 8: 48 beats in a full bar
instead of 24.

## What changes

In `game/src/bat.asm`:

```
FLAP_COST     = 8               ; a beat: 24 beats in a bar
```

becomes

```
FLAP_COST     = 4               ; a beat: 48 beats in a bar
```

## Where

`game/src/bat.asm`, `FLAP_COST`: what a beat takes from `energy` (in
256ths: 192 is the full bar).

## What you see

The bat climbs and hovers twice as long before it turns back into the
vampire and falls; the bar of the energy goes down by half a character a
beat.

## Limits

The levels are planned for 24 beats: over the canal or the moat the bat
now has energy to spare. A cost of 0 would never run out.

## What depends on it

The energy comes back on a surface (`RECHARGE`) and with a moth
(`MOTH_ENERGY`) as before.

## How it was proved

The test of step 04 (`tests/verify_game.py`) compared the program with
its model at every frame, the model changed in the same way
(`numbers['FLAP_COST'] = 4`), on a route of its own
(`tests/routes/variant_04a.py`): PASS, 33 checks, 1032 frames. Facts:

- 48 beats before the energy runs out: yes

To go back, undo the change above.
