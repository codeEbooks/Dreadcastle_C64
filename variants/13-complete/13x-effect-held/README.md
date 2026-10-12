# An effect that does not end

Step 13 (`chain/13-complete`), where it breaks: a mistake made on
purpose.

At the end of a sound effect its gate bit is left on.

## What changes

In `game/src/effects.asm`:

```
        and #%11111110
        sta sid_shadow + 4,y
        jmp _next
```

becomes

```
        and #%11111111
        sta sid_shadow + 4,y
        jmp _next
```

## What you see

Heard, not seen: after the first effect its last sound hangs on in the
voice until another note.

## Why

A sound fades with its release only when the gate goes to 0:
`and #%11111110` clears it in the copy of the control register; with
`%11111111` nothing changes.

## How the test stops it

The test of step 13 stops at "music and (0.10.1) sound effects: the SID
registers": music frame 636: [218, 43, 216, 8, 64, 10, 168, 156, 69, 0,
8, 65, 0, 0, 103, 17, 64, 4, 64, 5, 0, 0, 0, 0, 15] model [218, 43, 216,
8, 64, 10, 168, 156, 69, 0, 8, 64, 0, 0, 103, 17, 64, 4, 64, 5, 0, 0, 0,
0, 15].

To repair it, undo the change above.
