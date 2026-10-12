# Dreadcastle, step 06 - The enemies

The night watchman walks to and fro, the crow flies on a wave, the cat
jumps at Oscar. A touch takes two notches of health and throws him back;
he blinks, safe, for a moment; with no health left, back at the lantern.

New or changed: `enemies.asm` (new); `data.asm` adds the enemies'
sprites.

Not yet: oscar cannot strike back yet.

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
