# Dreadcastle, step 12 - The title and the ends

The title over the castle's door, with its menu (MUSIC, SOUND FX,
SILENT); LEVEL CLEAR and the count of the night left at each gate; the
victory in the arena; dawn, when a night is over: the game is over. The
score; a new game from the title.

New or changed: `states.asm` (new); `irq.asm` (the band of LEVEL CLEAR);
`main.asm` runs the states.

Not yet: no sound effects, no jingles yet.

## Build and play

`tools/run-game.ps1 -Mode Play` (Windows PowerShell) writes the data
(`game/assets/build_assets.py`), checks that no line of the sources is
longer than 60 characters, assembles `game/src/main.asm` with 64tass and
starts VICE (a PAL C64, SID 6581); on the title 8 and 2 choose MUSIC,
SOUND FX or SILENT and 0 starts; in the game joystick 2 is on the
keypad: 4 left, 6 right, 8 up (the jump; for the bat, a beat), 2 down, 0
fire (with the staff, a blow); 8 and 0 together: the bat; 2 and 0: Oscar
again. With other installations add `-Python`, `-Assembler` and `-Vice`;
`-Mode Build` only builds.

The program is `game/build/dreadcastle.prg`. This step is generated from
the source of the complete game (`tools/make_chain.py` in the project):
every file, routine and address here is the one of the finished game.
