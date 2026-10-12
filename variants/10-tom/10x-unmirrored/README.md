# Tom not turned round

Step 10 (`chain/10-tom`), where it breaks: a mistake made on purpose.

Facing left, Tom's pictures are copied without the table that turns them
round.

## What changes

In `game/src/tom.asm`:

```
; mirrored into page 0
        tax
        lda MIRROR,x
```

becomes

```
; mirrored into page 0
        tax
        txa
```

## What you see

When Tom faces left his picture falls apart: each column of pixels is in
its place, but each byte still faces right, so the outline is cut into
slivers.

## Why

A sprite is turned round by reversing the order of its bytes in each row
and the pixels in each byte. `MIRROR` reverses the pixels of a byte (in
pairs, for multicolour); without it only the bytes change places.

## How the test stops it

The test of step 10 stops at "the page of Tom's sprites shown is his
picture": frame 25215 (the fight: up to Tom, a blow while he waits):
picture 6.

The capture, 10 frames later: `unmirrored.png` (in
`variants/10-tom/evidence/10x-unmirrored/`).

To repair it, undo the change above.
