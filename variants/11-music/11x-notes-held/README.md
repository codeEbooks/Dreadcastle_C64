# Notes that never let go

Step 11 (`chain/11-music`), where it breaks: a mistake made on purpose.

Before a note the player no longer clears its gate bit.

## What changes

In `game/src/player.asm`:

```
        bcs +
        lda #0
        sta v_gate,x
```

becomes

```
        bcs +
        lda #1
        sta v_gate,x
```

## What you see

Heard, not seen: the notes of each voice run into one another, without
attack, a smear of sound.

## Why

The SID starts a note's envelope when the gate bit goes from 0 to 1.
Left at 1, the next note only changes the pitch: no new attack.

## How the test stops it

The test of step 11 stops at "music and (0.10.1) sound effects: the SID
registers": music frame 9: [23, 1, 0, 0, 64, 10, 168, 123, 5, 0, 6, 65,
6, 196, 218, 32, 144, 4, 65, 5, 0, 0, 0, 0, 15] model [23, 1, 0, 0, 64,
10, 168, 123, 5, 0, 6, 64, 6, 196, 218, 32, 144, 4, 64, 5, 0, 0, 0, 0,
15].

To repair it, undo the change above.
