# Dreadcastle, step 13 - The complete game

The jingles at the gates, at the victory and at dawn, the sound
effects with SOUND FX, and the disk: Dreadcastle 1.0, byte for byte
(SHA-256 `2479d57d...4126`).

New or changed: `effects.asm` (new); `states.asm` plays the jingles;
`objects.asm` tolls the bell in the last steps of the night; the disk:
`tools/make_disk.py` and `tools/load_time.py`.

## Build and play

`tools/run-game.ps1 -Mode Play` (Windows PowerShell) writes the data
(`game/assets/build_assets.py`), checks that no line of the sources is
longer than 60 characters, assembles `game/src/main.asm` with 64tass and
starts VICE (a PAL C64, SID 6581); on the title 8 and 2 choose MUSIC,
SOUND FX or SILENT and 0 starts; in the game joystick 2 is on the
keypad: 4 left, 6 right, 8 up (the jump; for the bat, a beat), 2 down, 0
fire (with the staff, a blow); 8 and 0 together: the bat; 2 and 0: Oscar
again. With other installations add `-Python`, `-Assembler` and `-Vice`;
`-Mode Build` only builds. `-Mode Disk` makes `game/build/dreadcastle.d64`
(the program on a 1541 disk) and starts VICE with it on a 1541 at the
real speed: about two minutes of loading, then the title.

The program is `game/build/dreadcastle.prg`. This step is generated from
the source of the complete game (`tools/make_chain.py` in the project):
every file, routine and address here is the one of the finished game.
