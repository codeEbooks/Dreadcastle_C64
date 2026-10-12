# Endless energy

Step 04 (`chain/04-bat`), where it breaks: a mistake made on purpose.

A beat no longer checks that there is energy for it.

## What changes

In `game/src/bat.asm`:

```
        bcs +
        jsr transform           ; not enough: a vampire
```

becomes

```
        jmp +
        jsr transform           ; not enough: a vampire
```

## What you see

When the bar is empty the bat beats on, and the bar is full again: the
bat never has to come down.

## Why

`sbc #FLAP_COST` leaves the carry clear when the energy is less than the
cost: the subtraction has borrowed. `bcs` keeps the beat only without a
borrow; with `jmp` the result, 8 less than a small number, wraps round
to near 256, more than the full bar (192).

## How the test stops it

The test of step 04 stops at "Oscar's form, smoke, energy, moths equal
the model": frame 4668 (beats left until the energy runs out): [1, 0,
64, 254, 0, 1, 0] model [0, 12, 64, 6, 0, 16, 0].

The capture, 20 frames later: `endless-energy.png` (in
`variants/04-bat/evidence/04x-endless-energy/`).

To repair it, undo the change above.
