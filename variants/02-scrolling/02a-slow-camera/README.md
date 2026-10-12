# A slow camera

Step 02 (`chain/02-scrolling`), a guided variant.

The camera moves one pixel a frame instead of two.

## What changes

In `game/src/scroll.asm`:

```
        lda #2
        sta speed
```

becomes

```
        lda #1
        sta speed
```

## Where

`game/src/scroll.asm`, `steer_camera`: the speed given to `camera_right`
and `camera_left`.

## What you see

The street glides twice as slowly; a new column every 8 frames, and the
back screen, ready in 3, never makes the camera wait.

## Limits

From 1 to 8 pixels a frame (more would skip a column). From step 03 the
camera follows Oscar and this speed is his.

## What depends on it

The test's model moves its camera by the same speed (`camera_speed`);
its route takes twice the frames.

## How it was proved

The test of step 02 (`tests/verify_game.py`) compared the program with
its model at every frame, the model changed in the same way
(`game_model.Game.camera_speed = 1`), on a route of its own
(`tests/routes/variant_02a.py`): PASS, 37 checks, 4170 frames. Facts:

- one pixel a frame: yes
- the camera never waits going one way: yes

To go back, undo the change above.
