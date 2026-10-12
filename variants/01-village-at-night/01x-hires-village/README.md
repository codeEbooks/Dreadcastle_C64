# The village in thin stripes

Step 01 (`chain/01-village-at-night`), where it breaks: a mistake made
on purpose.

The scroll value of the playfield without its multicolour bit.

## What changes

In `game/src/scroll.asm`:

```
        eor #%00010111          ; bit 4: multicolour
```

becomes

```
        eor #%00000111          ; bit 4: multicolour
```

## What you see

The village loses its colours: grey and white houses, roofs and street
in fine stripes. The HUD is right.

## Why

Bit 4 of $D016 turns multicolour on. `set_xscroll` keeps it in `xscroll`
with the 3 bits of the fine scroll; without it the top interrupt sets
the high-resolution mode: every byte of a character becomes 8 pixels of
one colour on the background, instead of 4 pixels of four colours, and
that colour is the whole value of its colour RAM, whose bit 3 (the
multicolour flag) makes it one of the light colours 8-15. The HUD's
interrupt writes its own value (`%00010000`), so the HUD is still in
multicolour.

## How the test stops it

The test of step 01 stops at "$d016 and $d018 from the frame before":
frame 1 (the village at night: nothing moves): 0xc7 0x03, model (23, 2).

The capture, 2 frames later: `hires-village.png` (in
`variants/01-village-at-night/evidence/01x-hires-village/`).

To repair it, undo the change above.
