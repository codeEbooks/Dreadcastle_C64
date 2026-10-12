"""The reference renderer: what the program must put on the screen.

Reads only the files written by game/assets/build_assets.py, and
computes from them, without the C64 program:
  - the screen and the colour RAM of the level seen from any camera
    position (eight levels, 128 metatile columns each; six
    settings, each with its set of characters and its tables:
    environment(); the HUD has a set of its own);
  - the 320 x 200 picture the VIC-II shows from them, in multicolour
    character mode, with Oscar's two sprites (or the bat's, or the
    smoke's), sprite 2 (the staff), sprites 3-6 (the enemies;
    where the moon is 3-5, and sprite 6 the moon) and sprite 7, the
    heirloom; each setting with its $d023, the mire's wisps and the
    spikes in their pictures, the moon behind the crag of level 5
    and the castle's walls; Tom's sprites, the title's name and the
    bands of words. The files given can
    carry the level as the model plays it (moths eaten, the lantern
    lit, the gate open), the character set with the moths' picture of
    the moment and the HUD as shown (game_model.py);
  - the 384 x 272 picture VICE exports, border included.
The test compares the C64's memory and VICE's capture with these.
"""

import json
from pathlib import Path
import re

PROJECT = Path(__file__).resolve().parents[1]
GENERATED = PROJECT / "game/assets/generated"

# VICE 3.10, internal palette, as RGB (measured from a capture).
PALETTE = ["000000", "ffffff", "af3c58", "7ef3d6", "aa40f5", "62d532",
           "2c3dec", "ffff46", "b7631e", "775300", "ee7b95", "626262",
           "949494", "b7ff86", "7385ff", "cdcdcd"]

PLAYFIELD_ROWS = 22                 # rows 22-24: the HUD
VISIBLE = 39                        # screen columns 0-38 can be seen
SPRITE_X_OFFSET = 31                # X register = level x - camera + 31


def constants():
    text = (GENERATED / "assets.inc").read_text(encoding="utf-8")
    return {name: int(value) for name, value in
            re.findall(r"^(\w+)\s*=\s*(\d+)", text, re.M)}


ENVIRONMENTS = ("village", "forest", "marsh", "crags", "pass", "keep",
                "hall")
CHARSETS = {name: "charset.bin" if name == "village" else
            f"charset_{name}.bin" for name in ENVIRONMENTS}


def environment(name):
    """A setting's set of characters and tables: its
    block of ENV_PAGES pages (build_assets.env_block) cut in its
    tables; its $d023; its $d021 and $d022."""
    block = (GENERATED / f"env_{name}.bin").read_bytes()
    index = ENVIRONMENTS.index(name)
    c = constants()
    return {"charset": (GENERATED / CHARSETS[name]).read_bytes(),
            "charcolour": block[0:256], "metaflags": block[256:512],
            "metashape": block[512:768], "metatiles": block[768:1792],
            "profiles": block[0x700:0x900], "env_block": block,
            "d021": c[f"ENV{index}_D021"],
            "d022": c[f"ENV{index}_D022"],
            "d023": c[f"ENV{index}_D023"],
            "moon_behind": bool(c["MOON_BEHIND"] >> index & 1)}


def load():
    """The files of the program; files["envs"] the settings, and the
    tables of the first (the village) also as files["charset"],
    files["metatiles"]... (env_files gives those of another)."""
    files = {}
    for name in ("hudset", "hud", "names", "sprites", "enemies",
                 "staff", "moon", "flicker", "tom", "mirror_to",
                 "logo"):
        files[name] = (GENERATED / f"{name}.bin").read_bytes()
    files["constants"] = constants()
    files["envs"] = [environment(name) for name in ENVIRONMENTS]
    files["staff_tables"] = json.loads(
        (GENERATED / "staff.json").read_text(encoding="utf-8"))
    files.update(files["envs"][0])
    count = files["constants"]["LEVEL_COUNT"]
    files["levels"] = [(GENERATED / f"level{n}.bin").read_bytes()
                       for n in range(1, count + 1)]
    files["level"] = files["levels"][0]
    # The packed data: {name: bytes} of the .lz files.
    files["packed"] = {path.name: path.read_bytes()
                       for path in sorted(GENERATED.glob("*.lz"))}
    files["texts"] = texts()
    return files


def texts():
    """The words of the title's menu and of the bands, from
    title.py (not from the program): {"menu": [(row, column,
    colour, codes)], "bands": [(first row, rows, [(row, column,
    colour, codes)])], "dawn": colours} with the HUD's codes
    (font.py)."""
    import sys
    sys.path.append(str(PROJECT / "game/assets"))
    import font
    import title

    def codes(words):
        return bytes(font.code(ch) for ch in words)

    menu = [(title.MENU_ROW + n, title.MENU_COL, title.OTHER,
             codes(words)) for n, words in enumerate(title.CHOICES)]
    row, column, words = title.PRESS
    menu.append((row, column, title.PRESS_ON, codes(words)))
    bands = []
    for name in title.BAND_ORDER:
        first, rows, items = title.BANDS[name]
        bands.append((first, rows, [
            (row, title.centred(words), colour, codes(words))
            for row, colour, words in items]))
    return {"menu": menu, "bands": bands,
            "dawn": list(title.DAWN_COLOURS)}


def mirror_byte(value):
    """A byte of a multicolour sprite, its four pixels the other way
    round (the table tom.asm makes)."""
    return ((value >> 6) | ((value >> 2) & 0x0C) | ((value << 2) & 0x30)
            | ((value << 6) & 0xC0))


def tom_picture(files, number):
    """The page of Tom's picture `number`: 0-4 facing right, as
    in tom.bin; 5-9 the same mirrored, facing left, as the program
    mirrors them (each row of six bytes, the left block's three and
    the right's, the other way round, each byte mirrored; as
    it copies them). The last byte of each block is not part of the
    picture: here 0, and the tests leave it out (shown_bytes)."""
    pictures = files["constants"]["TOM_PICTURES"]
    data = files["tom"][(number % pictures) * 256:][:256]
    if number < pictures:
        return bytes(data)
    out = bytearray(256)
    for half in (0, 128):
        for row in range(21):
            at = half + row * 3
            six = data[at:at + 3] + data[at + 64:at + 67]
            back = bytes(mirror_byte(b) for b in reversed(six))
            out[at:at + 3] = back[:3]
            out[at + 64:at + 67] = back[3:]
    return bytes(out)


def shown_bytes(page):
    """The bytes of a page of four sprite blocks the VIC-II shows: 63
    of each block."""
    return b"".join(page[at:at + 63] for at in range(0, 256, 64))


def env_files(files, env):
    """The files, with the tables of setting `env`."""
    view = dict(files)
    view.update(files["envs"][env])
    return view


def level_info(number=1):
    """levelN.json: the level's surfaces by name, solids, objects."""
    return json.loads((GENERATED / f"level{number}.json").read_text(
        encoding="utf-8"))


def objects(files, number=1):
    """A level's objects: the heirlooms, (level x of the sprite, top
    line of the box, kind number); the doors of the gate, (column,
    row, open tile); the lantern, (column, row) and its lit tile;
    the doorway, (first column, last column, top row); the
    enemies, (type number, x_min, x_max, x, line, facing) (the
    type, enemies.py TYPES: its behaviour is TYPEn_KIND); the
    staff, (x of its sprite, line under it) or None, and the
    setting."""
    info = level_info(number)
    kinds = info["heirloom_kinds"]
    return {"heirlooms": [(col * 16 - 4, top, kinds.index(kind))
                          for col, top, kind in info["heirlooms"]],
            "doors": [tuple(door) for door in info["doors"]],
            "lantern": tuple(info["lantern"]),
            "lantern_tile": info["lantern_tile"],
            "door": tuple(info["door"][:2] + info["door"][2:3]),
            "enemies": [(e["type"], e["x_min"], e["x_max"], e["x"],
                         e["line"], ("right", "left").index(e["facing"]))
                        for e in info.get("enemies", [])],
            "staff": ((info["staff"][0] | info["staff"][1] << 8,
                       info["staff"][2]) if info["staff"][2] else None),
            "env": info["env"]}


def corner(files, metatile, index):
    """Character of a metatile: index 0 top left, 1 top right,
    2 bottom left, 3 bottom right."""
    return files["metatiles"][index * 256 + metatile]


def level_column(files, world):
    """Character column `world` of the level: 22 codes."""
    metatile_column = files["level"][(world // 2) * 11:
                                     (world // 2) * 11 + 11]
    side = world % 2
    codes = []
    for metatile in metatile_column:
        codes += [corner(files, metatile, side),
                  corner(files, metatile, 2 + side)]
    return codes


def level_view(files, first):
    """Screen columns 0-38, rows 0-21, when level column `first`
    is in screen column 0: {(col, row): (code, colour)}."""
    view = {}
    for col in range(VISIBLE):
        for row, code in enumerate(level_column(files, first + col)):
            view[(col, row)] = (code, files["charcolour"][code])
    return view


def paint_cell(files, rows, x0, y0, code, colour, charset="charset"):
    c = files["constants"]
    d021 = files.get("d021", c["D021_SKY"])     # the setting's
    d022 = files.get("d022", c["D022_STONE"])
    d023 = files.get("d023", c["D023_WOOD"])
    if charset == "hudset":                     # the HUD: black
        d021 = c["D021_SKY"]
    colour &= 15
    for y in range(8):
        byte = files[charset][code * 8 + y]
        for x in range(8):
            if colour & 8:          # multicolour: pixel pairs
                bits = (byte >> (6 - (x // 2) * 2)) & 3
                pixel = (d021, d022, d023, colour & 7)[bits]
            elif byte & (0x80 >> x):
                pixel = colour
            else:
                pixel = d021
            rows[y0 + y][x0 + x] = pixel


def draw_oscar(files, rows, x_register, y_register, picture=0):
    """Oscar's two sprites over the picture: X and Y registers, and
    the picture (0-24: Oscar, the bat, the smoke; two blocks each,
    lines then colours)."""
    c = files["constants"]
    sprites = files["sprites"][picture * 128:picture * 128 + 128]
    x0 = x_register - 24
    y0 = y_register - 50
    multi = (None, c["SPRITE_SHARED_1"], c["OSCAR_COLOUR"],
             c["SPRITE_SHARED_2"])
    for y in range(21):
        paint = int.from_bytes(sprites[64 + y * 3:64 + y * 3 + 3], "big")
        line = int.from_bytes(sprites[y * 3:y * 3 + 3], "big")
        for x in range(24):
            bits = (paint >> (22 - (x // 2) * 2)) & 3
            if bits and 0 <= x0 + x < 320 and 0 <= y0 + y < 200:
                rows[y0 + y][x0 + x] = multi[bits]
            if (line & (0x800000 >> x) and 0 <= x0 + x < 320
                    and 0 <= y0 + y < 200):
                rows[y0 + y][x0 + x] = c["OSCAR_LINE_COLOUR"]


def draw_heirloom(files, rows, x_register, y_register, kind):
    """Sprite 7, multicolour: the heirloom of number `kind` (its
    block follows Oscar's 25 pictures)."""
    c = files["constants"]
    at = c["PICTURE_COUNT"] * 128 + kind * 64
    block = files["sprites"][at:at + 64]
    x0, y0 = x_register - 24, y_register - 50
    multi = (None, c["SPRITE_SHARED_1"], c["HEIRLOOM_COLOUR"],
             c["SPRITE_SHARED_2"])
    for y in range(21):
        paint = int.from_bytes(block[y * 3:y * 3 + 3], "big")
        for x in range(24):
            bits = (paint >> (22 - (x // 2) * 2)) & 3
            if bits and 0 <= x0 + x < 320 and 0 <= y0 + y < 200:
                rows[y0 + y][x0 + x] = multi[bits]


def draw_enemy(files, rows, x_register, y_register, block, colour,
               behind=None):
    """A multicolour sprite with its own colour `colour`: an enemy
    (or its puff), the staff, the moon; `block` its 64 bytes.
    `behind` (the moon behind the characters, $d01b): the
    playfield as the characters paint it and where they are in front
    (foreground: their colours of bits 10 and 11); there the sprite's
    pixel shows the characters, over a sprite of lower priority too
    (the VIC-II settles the sprites first, then the characters)."""
    c = files["constants"]
    x0, y0 = x_register - 24, y_register - 50
    multi = (None, c["SPRITE_SHARED_1"], colour, c["SPRITE_SHARED_2"])
    for y in range(21):
        paint = int.from_bytes(block[y * 3:y * 3 + 3], "big")
        for x in range(24):
            bits = (paint >> (22 - (x // 2) * 2)) & 3
            if bits and 0 <= x0 + x < 320 and 0 <= y0 + y < 200:
                pixel = multi[bits]
                if behind is not None:
                    screen, front = behind
                    if front(x0 + x, y0 + y):
                        pixel = screen[y0 + y][x0 + x]
                rows[y0 + y][x0 + x] = pixel


def background(files, x, y):
    """Is level pixel (x, y) of the playfield the background ($d021):
    a multicolour pixel of bits 00, a hi-res pixel not set."""
    code = level_column(files, x // 8)[y // 8]
    byte = files["charset"][code * 8 + y % 8]
    if files["charcolour"][code] & 8:
        return (byte >> (6 - (x % 8 // 2) * 2)) & 3 == 0
    return not byte & (0x80 >> (x % 8))


def foreground(files, world, x, y):
    """Is level pixel (x, y) of the playfield in front of a sprite
    behind the characters: a multicolour pixel of bits 10 or 11, a
    hi-res pixel set."""
    code = level_column(files, x // 8)[y // 8]
    byte = files["charset"][code * 8 + y % 8]
    if files["charcolour"][code] & 8:
        return (byte >> (6 - (x % 8 // 2) * 2)) & 2 == 2
    return bool(byte & (0x80 >> (x % 8)))


def world_picture(files):
    """The whole level, 176 lines high."""
    width = len(files["level"]) // 11 * 2
    rows = [[files.get("d021", files["constants"]["D021_SKY"])]
            * (width * 8) for _ in range(PLAYFIELD_ROWS * 8)]
    for world in range(width):
        for row, code in enumerate(level_column(files, world)):
            paint_cell(files, rows, world * 8, row * 8, code,
                       files["charcolour"][code])
    return rows


def scrolled_picture(files, camera, world=None, oscar=None,
                     heirloom=None, enemies=(), staff=None, moon=None,
                     tom=None, logo=None, band=None):
    """What the VIC-II shows with the camera at `camera`: screen
    pixel x (7-310, inside the 38-column border) of the playfield is
    level pixel camera + x - 7; the HUD does not scroll. `oscar`:
    (X register, Y register, picture), or None; `heirloom`: (X
    register, Y register, kind) of sprite 7, or None; `enemies`: for
    sprites 3, 4... (X register, Y register, block bytes, colour);
    `staff`: sprite 2, (X register, Y register, block bytes) or None;
    `moon`: sprite 6 in the wood, (X register, Y register) or None;
    `tom`: Tom's four sprites, 3, 4, 5 and 7 (X register, Y
    register, block bytes, colour each), or None. `logo`: the
    title's name, sprites 2-5 (X register, Y register, block bytes,
    colour each: hi-res, stretched both ways), or None; `band`: a band
    of words over the playfield, (first row, last row, {(column, row):
    (code, colour)}) of the screen shown, in the HUD's characters on
    the playfield's background ($d021: files["d021"]), or None.
    A sprite of a lower number is in front: Oscar, the staff (or the
    name), the enemies in their order (or Tom's 3, 4, 5), the moon,
    the heirloom (or Tom's 7)."""
    world = world or world_picture(files)
    rows = [[files["constants"]["D021_SKY"]] * 320 for _ in range(200)]
    for y in range(PLAYFIELD_ROWS * 8):
        for x in range(7, 311):
            rows[y][x] = world[y][camera + x - 7]
    # The playfield's last line (226): the HUD's interrupt has set the
    # background black in its left border (seen at dawn, where
    # the playfield's background is not black).
    last = PLAYFIELD_ROWS * 8 - 1
    for x in range(7, 311):
        if background(files, camera + x - 7, last):
            rows[last][x] = files["constants"]["D021_SKY"]
    if band is not None:
        paint_band(files, rows, camera, band)
    hud = files["hud"]
    for cell in range(120):
        paint_cell(files, rows, (cell % 40) * 8, 176 + (cell // 40) * 8,
                   hud[cell], hud[120 + cell], "hudset")
    screen = [list(line) for line in rows]      # no sprite yet
    if heirloom is not None:
        draw_heirloom(files, rows, *heirloom)
    if tom is not None:                         # sprite 7
        draw_enemy(files, rows, *tom[3])
    if moon is not None:
        behind = None
        if files.get("moon_behind"):
            behind = (screen, lambda x, y: (
                y < PLAYFIELD_ROWS * 8 and 7 <= x < 311
                and foreground(files, world, camera + x - 7, y)))
        if band is not None and behind is not None:
            behind = (screen, band_front(files, world, camera, band,
                                         behind[1]))
        draw_enemy(files, rows, *moon, files["moon"],
                   files["constants"]["MOON_COLOUR"], behind)
    for enemy in reversed(list(enemies)):
        draw_enemy(files, rows, *enemy)
    if tom is not None:                         # sprites 5, 4, 3
        for sprite in reversed(tom[:3]):
            draw_enemy(files, rows, *sprite)
    if logo is not None:                        # 5, 4, 3, 2
        for sprite in reversed(logo):
            draw_stretched(rows, *sprite)
    if staff is not None:
        draw_enemy(files, rows, *staff, c_staff(files))
    if oscar is not None:
        draw_oscar(files, rows, *oscar)
    return rows


def band_x(camera, column):
    """The screen x of a cell's first pixel: the characters
    scrolled as the playfield is (level x camera + x - 7)."""
    return column * 8 + 7 - (camera & 7)


def paint_band(files, rows, camera, band):
    """The band's rows in the HUD's characters: hi-res where the
    colour is under 8 (the words), on the playfield's background."""
    first, last, cells = band
    background = files.get("d021", files["constants"]["D021_SKY"])
    for (column, row), (code, colour) in cells.items():
        if not first <= row <= last:
            continue
        x0 = band_x(camera, column)
        for y in range(8):
            byte = files["hudset"][code * 8 + y]
            for x in range(8):
                if not 7 <= x0 + x < 311:
                    continue
                if colour & 8:
                    bits = (byte >> (6 - (x // 2) * 2)) & 3
                    pixel = (background, files["d022"], files["d023"],
                             colour & 7)[bits]
                else:
                    pixel = colour if byte & (0x80 >> x) else background
                rows[row * 8 + y][x0 + x] = pixel


def band_front(files, world, camera, band, level_front):
    """Where the characters are in front of a sprite behind
    them: in the band's rows its own characters (hi-res: set pixels),
    elsewhere the level's."""
    first, last, cells = band

    def front(x, y):
        row = y // 8
        if not first <= row <= last:
            return level_front(x, y)
        column = (x - 7 + (camera & 7)) // 8
        code, colour = cells.get((column, row), (0, 0))
        byte = files["hudset"][code * 8 + y % 8]
        offset = (x - 7 + (camera & 7)) % 8
        if colour & 8:
            return (byte >> (6 - (offset // 2) * 2)) & 2 == 2
        return bool(byte & (0x80 >> offset))
    return front


def draw_stretched(rows, x_register, y_register, block, colour):
    """A hi-res sprite stretched twice across and twice down
    ($d01d, $d017): 48 x 42 pixels."""
    x0, y0 = x_register - 24, y_register - 50
    for y in range(42):
        line = int.from_bytes(block[(y // 2) * 3:(y // 2) * 3 + 3],
                              "big")
        for x in range(48):
            if line & (0x800000 >> (x // 2)) and 0 <= x0 + x < 320 \
                    and 0 <= y0 + y < 200:
                rows[y0 + y][x0 + x] = colour


def c_staff(files):
    return files["constants"]["STAFF_COLOUR"]


def capture(rows, border=0):
    """VICE's export: 384 x 272, the screen at (32, 35); in 38-column
    mode the border covers 7 pixels on the left, 9 on the right."""
    full = [[border] * 384 for _ in range(272)]
    for y in range(200):
        for x in range(7, 311):
            full[35 + y][32 + x] = rows[y][x]
    return full


def rgb_rows(rows):
    return [[bytes.fromhex(PALETTE[c]) for c in line] for line in rows]
