# Colours left behind

Step 02 (`chain/02-scrolling`), where it breaks: a mistake made on
purpose.

At a swap the colour RAM of rows 11-21 is not moved: the characters of
the lower half go on, their colours stay.

## What changes

In `game/src/scroll.asm`:

```
        jsr colour_half         ; rows 11-21

```

becomes

```

```

## What you see

Scrolling right, the top half of the street is right; in the bottom half
patches of the wrong colour appear on the walls, the windows and the
stalls, and change at every swap: the characters have moved on, their
paint has not.

## Why

Both screens have their own characters, but there is only one colour
RAM: at every swap `do_swap` moves it by a column, in place, the top
half (`colour_half` with the first routine) and the bottom half (the
second). Without the second, rows 11-21 keep the colours of the column
before, while their characters move one column at every swap.

## How the test stops it

The test of step 02 stops at "colour RAM equals the model": frame 24
(right: the street scrolls, 2 pixels a frame): column 0 row 15: 12
instead of 15.

The capture, 60 frames later: `colours-left-behind.png` (in
`variants/02-scrolling/evidence/02x-colours-left-behind/`).

To repair it, undo the change above.
