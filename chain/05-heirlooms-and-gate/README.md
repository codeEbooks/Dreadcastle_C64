# Dreadcastle, step 05 - Heirlooms and the gate

The Village of Mortals and the Churchyard: three heirlooms to take in
each, the lantern of the checkpoint, the gate that opens with all three
and leads to the next level. Two minutes of night a level; at dawn,
level 1 again.

New or changed: `objects.asm` (the heirlooms, the lantern, the gate, the
night); `level.asm` loads the objects of a level.

Not yet: two levels: through the churchyard's gate, level 1 again. No
enemies yet.

## Build and play

`tools/run-game.ps1 -Mode Play` (Windows PowerShell) writes the data
(`game/assets/build_assets.py`), checks that no line of the sources is
longer than 60 characters, assembles `game/src/main.asm` with 64tass and
starts VICE (a PAL C64, SID 6581); joystick 2 is on the keypad: 4 left,
6 right, 8 up (the jump), 7 and 9 the jumps to the left and to the
right; 8 and 0 together: the bat, which beats its wings with 8 and dives
with 2; 2 and 0 together: Oscar again. With other installations add
`-Python`, `-Assembler` and `-Vice`; `-Mode Build` only builds.

The program is `game/build/dreadcastle.prg`. This step is generated from
the source of the complete game (`tools/make_chain.py` in the project):
every file, routine and address here is the one of the finished game.
