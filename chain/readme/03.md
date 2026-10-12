# Dreadcastle, step 03 - Oscar

Oscar walks and jumps (Up held longer, higher) on the streets, the
roofs, the balconies and the carts of the village; the crates stop him;
the camera follows him. A fall into the trapdoor or the canal: the
screen goes off, and he is back at the start.

New or changed: `oscar.asm` (his moves, the surfaces, his pictures);
`objects.asm` begins with the fall and the transition.

Not yet: no bat, no heirlooms, no enemies yet.

## Build and play

`tools/run-game.ps1 -Mode Play` (Windows PowerShell) writes the data
(`game/assets/build_assets.py`), checks that no line of the sources is
longer than 60 characters, assembles `game/src/main.asm` with 64tass and
starts VICE (a PAL C64, SID 6581); joystick 2 is on the keypad: 4 left,
6 right, 8 up (the jump), 7 and 9 the jumps to the left and to the
right. With other installations add `-Python`, `-Assembler` and `-Vice`;
`-Mode Build` only builds.

The program is `game/build/dreadcastle.prg`. This step is generated from
the source of the complete game (`tools/make_chain.py` in the project):
every file, routine and address here is the one of the finished game.
