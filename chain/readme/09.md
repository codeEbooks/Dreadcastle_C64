# Dreadcastle, step 09 - The castle

Levels 7 and 8, Dreadcastle Gate and the Throne Tower: stone and lit
windows on a blue night, the spikes of iron and the fire. The top
interrupt sets the castle's sky, the HUD's sets black again.

New or changed: `irq.asm` (the castle's sky, black again under the HUD);
`level.asm` (the colour of the stone).

Not yet: eight levels: through the door of the throne room, level 1
again. No Tom yet.

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
