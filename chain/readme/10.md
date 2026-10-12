# Dreadcastle, step 10 - Tom Darkfang

The door of the throne room leads to Tom's arena: he growls, leaps and
charges; struck eight times with the staff he runs away through the
window. His pictures are turned round by a table, under the KERNAL.

New or changed: `tom.asm` (new); `objects.asm` leads into the arena;
`unpack.asm` moves Tom's data.

Not yet: tom gone, level 1 again. No music yet.

## Build and play

`tools/run-game.ps1 -Mode Play` (Windows PowerShell) writes the data
(`game/assets/build_assets.py`), checks that no line of the sources is
longer than 60 characters, assembles `game/src/main.asm` with 64tass and
starts VICE (a PAL C64, SID 6581); joystick 2 is on the keypad: 4 left,
6 right, 8 up (the jump), 7 and 9 the jumps to the left and to the
right; 8 and 0 together: the bat, which beats its wings with 8 and dives
with 2; 2 and 0 together: Oscar again; 0 alone, with the staff: a blow.
With other installations add `-Python`, `-Assembler` and `-Vice`;
`-Mode Build` only builds.

The program is `game/build/dreadcastle.prg`. This step is generated from
the source of the complete game (`tools/make_chain.py` in the project):
every file, routine and address here is the one of the finished game.
