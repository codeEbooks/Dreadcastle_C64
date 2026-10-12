# A hall of brown stone

Step 09 (`chain/09-castle`), a guided variant.

The stone of the Throne Tower brown instead of grey.

## What changes

In `game/assets/hall.py`:

```
STONE = 12                              # $d022 here: medium grey
```

becomes

```
STONE = 9                               # $d022 here: brown
```

## Where

`game/assets/hall.py`, `STONE`: $D022 of the hall's setting, the first
shared colour of its characters.

## What you see

Every stone of level 8 brown: one register, all the characters that use
it.

## Limits

A shared colour is shared: all the hall's pixels of that colour change
together.

## What depends on it

`level.asm` writes $D022 from `env_d022` when the setting changes.

## How it was proved

The test of step 09 (`tests/verify_game.py`) compared the program with
its model at every frame, on a route of its own
(`tests/routes/variant_09.py`): PASS, 43 checks, 180 frames. Facts:

- the captures of the castle as the reference: yes

To go back, undo the change above.
