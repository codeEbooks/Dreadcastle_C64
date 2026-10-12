# A camera faster than the back screen

Step 02 (`chain/02-scrolling`), a guided variant.

The camera moves four pixels a frame: faster than the back screen can be
made ready.

## What changes

In `game/src/scroll.asm`:

```
        lda #2
        sta speed
```

becomes

```
        lda #4
        sta speed
```

## Where

`game/src/scroll.asm`, `steer_camera`: the speed.

## What you see

A new column every 2 frames, but the back screen needs 3 more after a
swap (two to move the rows, one for the new column): at the edge of each
column the camera waits (`_hold`) until it is ready. The street moves in
jerks and, on average, no faster than at two pixels a frame: 8 pixels in
4 frames is all the back screen allows. That is why `steer_camera` says
2.

## Limits

The cure would be a back screen made in fewer stages, at the price of a
longer frame.

## What depends on it

The test's model waits the same way (`holds`).

## How it was proved

The test of step 02 (`tests/verify_game.py`) compared the program with
its model at every frame, the model changed in the same way
(`game_model.Game.camera_speed = 4`), on the route of the step: PASS, 38
checks, 2120 frames. Facts:

- the camera waits at the edge of its columns: yes
- no faster than two pixels a frame: yes

To go back, undo the change above.
