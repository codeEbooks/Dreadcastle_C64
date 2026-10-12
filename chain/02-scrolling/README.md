# Dreadcastle, step 02 - The scrolling

Joystick 2 moves the camera over the village, both ways, two pixels a
frame, from one end of the level to the other, with the HUD still. The
scroll register moves the picture a pixel at a time; at every eighth
pixel the screen behind, made ready a slice a frame, comes to the front,
and the colour RAM moves in place before the beam reaches it.

New or changed: `scroll.asm` (the camera, the two screens, the colour
RAM); `main.asm` reads the joystick.

Not yet: oscar stands still: the joystick steers the camera.

## Build and play

`tools/run-game.ps1 -Mode Play` (Windows PowerShell) writes the data
(`game/assets/build_assets.py`), checks that no line of the sources is
longer than 60 characters, assembles `game/src/main.asm` with 64tass and
starts VICE (a PAL C64, SID 6581); joystick 2 is on the keypad: 4 and 6
move the camera. With other installations add `-Python`, `-Assembler`
and `-Vice`; `-Mode Build` only builds.

The program is `game/build/dreadcastle.prg`. This step is generated from
the source of the complete game (`tools/make_chain.py` in the project):
every file, routine and address here is the one of the finished game.
