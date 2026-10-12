# Slower wisps

Step 08 (`chain/08-packed-levels`), a guided variant.

The hazards that flicker take their next picture every 8 frames instead
of every 4.

## What changes

In `game/src/bat.asm`:

```
        lda turn_frame
        and #%00000011
        cmp #2
        bne _done
        lda turn_frame
        and #%00001100          ; picture * 4
        asl a                   ; * 64 bytes
        asl a
        asl a
        asl a

```

becomes

```
        lda turn_frame
        and #%00000111
        cmp #2
        bne _done
        lda turn_frame
        and #%00011000          ; picture * 8
        asl a                   ; * 64 bytes
        asl a
        asl a

```

## Where

`game/src/bat.asm`, `flicker_hazards`: the frames it acts on (bits 0-2
of the turn's frame, at 2) and the picture (bits 3-4, times 64 bytes:
three shifts).

## What you see

The will-o'-the-wisps of the mire drift twice as slowly.

## Limits

The mask and the shifts go together: with bits 3-4 for the picture, 3
shifts make 64 bytes. It must never act in the frame of the moths (bits
0-2 at 0).

## What depends on it

The test's model flickers at the same pace (`flicker_shift`).

## How it was proved

The test of step 08 (`tests/verify_game.py`) compared the program with
its model at every frame, the model changed in the same way
(`game_model.Game.flicker_shift = 3`), on a route of its own
(`tests/routes/variant_08.py`): PASS, 42 checks, 144 frames. Facts:

- the four pictures of the wisps: yes

To go back, undo the change above.
