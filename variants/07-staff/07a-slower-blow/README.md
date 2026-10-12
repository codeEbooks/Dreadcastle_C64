# A slower blow

Step 07 (`chain/07-staff`), a guided variant.

The staff is raised for 7 frames instead of 3 before it swings: a blow
of 14 frames instead of 10.

## What changes

In `game/assets/staff.py`:

```
BLOW_FRAMES = 10
BLOW = {10: (8, 0, "raise"), 9: (8, 0, "raise"), 8: (8, 0, "raise"),
```

becomes

```
BLOW_FRAMES = 14
BLOW = {14: (8, 0, "raise"), 13: (8, 0, "raise"), 12: (8, 0, "raise"),
        11: (8, 0, "raise"), 10: (8, 0, "raise"), 9: (8, 0, "raise"),
        8: (8, 0, "raise"),
```

## Where

`game/assets/staff.py`, `BLOW_FRAMES` and `BLOW`: the frames of a blow
and, for each frame left, where the staff is and which of its pictures;
`staff_tables` has an entry for each.

## What you see

Fire, and the staff stays up longer before the swing; 11 frames after
Fire the blow is still going on, where a blow of 10 has ended.

## Limits

The frames that strike are counted from the end (`STRIKE_FIRST`,
`STRIKE_LAST`: 7 to 4 left): the swing hits 4 frames later after Fire,
and an enemy has 4 more frames to come close. Fire is not heard again
until the blow ends.

## What depends on it

`BLOW_FRAMES` is a number of the data: the program and the test's model
read it from there, and the staff's table from `staff_tables`.

## How it was proved

The test of step 07 (`tests/verify_game.py`) compared the program with
its model at every frame, on a route of its own
(`tests/routes/variant_07a.py`): PASS, 42 checks, 102 frames. Facts:

- still in the blow 12 frames after Fire: yes

To go back, undo the change above.
