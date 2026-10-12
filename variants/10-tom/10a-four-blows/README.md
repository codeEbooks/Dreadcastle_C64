# Four blows for Tom

Step 10 (`chain/10-tom`), a guided variant.

Tom is beaten after four blows of the staff instead of eight.

## What changes

In `game/src/tom.asm`:

```
HITS_FULL      = 8               ; the staff's hits: his bar
```

becomes

```
HITS_FULL      = 4               ; the staff's hits: his bar
```

## Where

`game/src/tom.asm`, `HITS_FULL`: the blows Tom takes; `HITS_FAST` (half
of it) is when he gets faster.

## What you see

A shorter fight: Tom gets faster after two blows and runs away after
four.

## Limits

His bar in the HUD shows the hits left: with fewer, a shorter bar.

## What depends on it

The test's model counts the same hits (`HITS_FULL`, `HITS_FAST`).

## How it was proved

The test of step 10 (`tests/verify_game.py`) compared the program with
its model at every frame, the model changed in the same way
(`numbers['HITS_FULL'] = 4`; `numbers['HITS_FAST'] = 2`), on a route of
its own (`tests/routes/variant_10.py`): PASS, 46 checks, 747 frames.
Facts:

- beaten after four blows: yes

To go back, undo the change above.
