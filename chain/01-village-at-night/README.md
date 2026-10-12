# Dreadcastle, step 01 - The village at night

The Village of Mortals at night: its map of metatiles drawn in
multicolour characters, the HUD under it in characters of its own, the
level's name, and Oscar standing at the start. Two raster interrupts a
frame keep the playfield's characters above line 226 and the HUD's below
it. Nothing moves yet: the main loop only waits for the frame.

New or changed: every file: `main.asm`, `memory.asm`, `vic.asm`,
`irq.asm`, `level.asm` (the map, the columns, the HUD), `data.asm` (the
level's data as it is, at `$8000`), `scroll.asm` (the scroll register),
`oscar.asm` (his sprite), `unpack.asm` (the data copied where they are
used, a page at a time).

Not yet: no joystick yet: close VICE to finish.

## Build and play

`tools/run-game.ps1 -Mode Play` (Windows PowerShell) writes the data
(`game/assets/build_assets.py`), checks that no line of the sources is
longer than 60 characters, assembles `game/src/main.asm` with 64tass and
starts VICE (a PAL C64, SID 6581). With other installations add
`-Python`, `-Assembler` and `-Vice`; `-Mode Build` only builds.

The program is `game/build/dreadcastle.prg`. This step is generated from
the source of the complete game (`tools/make_chain.py` in the project):
every file, routine and address here is the one of the finished game.
