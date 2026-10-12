# Dreadcastle, step 04 - The bat

Up and Fire together turn Oscar into a bat in a puff of smoke, Down and
Fire back. The bat beats its wings with Up, falls when let go, dives
with Down and perches on what it meets; its flight uses up the energy of
the HUD, which comes back on the ground, and the moths of the sky give
some back when eaten.

New or changed: `bat.asm` (new); `oscar.asm` changes form; `level.asm`
changes a metatile in the level and on both screens (a moth eaten).

Not yet: no heirlooms, no gate: the level just ends.

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
