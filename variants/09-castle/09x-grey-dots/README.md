# Grey dots over the HUD

Step 09 (`chain/09-castle`), where it breaks: a mistake made on purpose.

The HUD's interrupt no longer waits for line 226 before it changes the
registers.

## What changes

In `game/src/irq.asm`:

```
        lda #HUD_LINE           ; wait for line 226
-       cmp $d012
        bne -

```

becomes

```

```

## What you see

A row of grey dots along the last line of the playfield, just above the
HUD, in every level (in the castle, where the sky is blue, as in the
village).

## Why

The HUD's interrupt is set for line 225, the line before the HUD, to
have time: it must wait there for line 226 (`cmp $d012`) before it
writes $D021, $D016 and $D018. Without the wait the registers change
while the beam is still drawing line 225, and the rest of that line is
drawn with the HUD's characters.

## How the test stops it

The test of step 09 stops at "HUD interrupt on line 226": frame 1 (still
at the start): line 225.

The capture, 40 frames later: `grey-dots.png` (in
`variants/09-castle/evidence/09x-grey-dots/`).

To repair it, undo the change above.
