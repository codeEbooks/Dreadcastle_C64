; The data, made by game/assets/build_assets.py.

        .cerror LEVEL_WIDTH != 128, "128 columns"

; Each level: its map, its objects, its name; its setting
; the types of enemy; the staff.
        .include "../assets/generated/level_maps.asm"
        .include "../assets/generated/objects.asm"
        .include "../assets/generated/level_names.asm"
        .include "../assets/generated/tables.asm"
        .include "../assets/generated/types.asm"
        .include "../assets/generated/staff_tables.asm"
level_names:
        .binary "../assets/generated/names.bin"
NAME_ROWS = LEVEL_COUNT + 1     ; the levels', then Tom's
        .cerror * - level_names != NAME_ROWS * 80, "names"

; Where each column of the level being played starts in
; its copy at LEVEL: a page of its own.
        .align 256
level_lo:
        .byte <(LEVEL + range(LEVEL_WIDTH) * 11)
level_hi:
        .byte >(LEVEL + range(LEVEL_WIDTH) * 11)
        .cerror (level_lo & $ff) != 0, "a page"

        .cerror * > SCREEN_A, "code reaches the screens"

        * = CHARSET
        .binary "../assets/generated/charset.bin"
; The HUD's characters. The codes after its glyphs must
; stay empty: the HUD's interrupt shows them on the last
; line of the playfield (irq.asm).
        * = HUD_CHARSET
        .binary "../assets/generated/hudset.bin"

; Sprites: Oscar's pictures, the bat's and the smoke's, two
; blocks each, then a block for each kind of heirloom.
HEIRLOOM_BLOCKS = OSCAR_LINES + PICTURE_COUNT * 2
SPRITE_BYTES = PICTURE_COUNT * 128 + HEIRLOOM_KINDS * 64

ENEMY_END = ENEMY_SPRITES + ENEMY_TYPES_1 * 256
        * = ENEMY_SPRITES
ENEMY_FILE = "../assets/generated/enemies.bin"
ENEMIES_1 = ENEMY_TYPES_1 * 256 ; the village's, the wood's
        .binary ENEMY_FILE, 0, ENEMIES_1
        .cerror * != ENEMY_END, "4"
        .cerror * > SPRITES, "enemies: under the sprites"

        * = MOON_SPRITE         ; the moon
        .binary "../assets/generated/moon.bin"
        .cerror * != MOON_SPRITE + 64, "the moon: a block"
        .cerror * > SPRITES, "the moon: under the sprites"
        .cerror MOON_SPRITE < ENEMY_END, "the moon: enemies"
; The HUD's rows 22 and 23: in the VIC-II's bank, but not
; seen there.
        * = HUD_DATA
hud_chars:                      ; rows 22 and 23
        .binary "../assets/generated/hud.bin", 0, 80
hud_colours:
        .binary "../assets/generated/hud.bin", 120, 80
; The moth's two pictures: 16 bytes each, for its two
; characters.
moth_frames:
        .binary "../assets/generated/moth.bin"
        .cerror * - moth_frames != 32, "moth.bin"
        .cerror * > SPRITES, "the HUD: under the sprites"

        * = SPRITES
        .binary "../assets/generated/sprites.bin"
        .cerror * - SPRITES != SPRITE_BYTES, "sprites"
        .cerror * > STAFF_SPRITES, "under the staff"

        * = STAFF_SPRITES
        .binary "../assets/generated/staff.bin"
STAFF_BYTES = STAFF_PICTURES * 64
        .cerror * - STAFF_SPRITES != STAFF_BYTES, "staff"
        .cerror * != PROFILE_INDEX, "the profiles next"
; The profiles of the surfaces, in ENV_TABLES: for each
; pixel column of a metatile, a table of PROFILE_STRIDE
; bytes: the line of each profile in that column, or $ff.
; Where the tables are: after the staff's sprites.
profile_lo:
        .byte <(profiles + range(16) * PROFILE_STRIDE)
profile_hi:
        .byte >(profiles + range(16) * PROFILE_STRIDE)
        .cerror * > ENEMY_SPRITES_2, "the profiles: under"

; Out of the VIC-II's bank, as they are (plain.asm,
; written by build_assets.py): the maps of levels 1-3,
; the tables of their settings and the wood's set of
; characters. Copied by start_map, start_tables, start_set
; and unpack_page.
        * = ENV_DATA
        .include "../assets/generated/plain.asm"
        .cerror ENV_COUNT != 7, "seven settings"
        .cerror LEVEL_COUNT != 8, "eight levels"
; Each setting's $d018 for screen A, screen B: the
; characters at CHARSET (the village) or SET_SLOT.
env_d018_a:     .byte D018_A, D018_A | %100, D018_A | %100
                .byte D018_A | %100, D018_A | %100
                .byte D018_A | %100, D018_A | %100
env_d018_b:     .byte D018_B, D018_B | %100, D018_B | %100
                .byte D018_B | %100, D018_B | %100
                .byte D018_B | %100, D018_B | %100
        .cerror * - env_d018_b != ENV_COUNT, "one a setting"
        .cerror SET_SLOT - CHARSET != $1000, "+ $1000"
        .cerror * > LEVEL, "the data reach the level"
