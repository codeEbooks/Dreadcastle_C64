# Enemies of one screen

Step 06 (`chain/06-enemies`), where it breaks: a mistake made on
purpose.

The enemies' sprite pointers are written in screen A only.

## What changes

In `game/src/enemies.asm`:

```
        sta SCREEN_B + POINTERS + 3,y

```

becomes

```

```

## What you see

Scrolling, the enemies vanish whenever screen B is in front (in the
capture, the watchman by the trapdoor is missing), and come back with
screen A.

## Why

The sprite pointers are the last 8 bytes of the screen the VIC-II shows:
with two screens, two sets. `place_enemy` must write both, as
`place_oscar` does; in screen B the enemies' pointers keep whatever was
there, here a block with nothing visible in it.

## How the test stops it

The test of step 06 stops at "sprites 3-6, the enemies, equal the
model": frame 645 (walk right to the trapdoor): slot 0: (86, 173, 130,
0, 8).

The capture, 2 frames later: `pointers-of-one-screen.png` (in
`variants/06-enemies/evidence/06x-pointers-of-one-screen/`).

To repair it, undo the change above.
