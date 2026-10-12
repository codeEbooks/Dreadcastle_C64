; The data, made by game/assets/build_assets.py.

        .cerror LEVEL_WIDTH != 128, "128 columns"

; Each level: its map, its objects, its name; its setting
; the types of enemy; the staff.
        .include "../assets/generated/level_maps.asm"
        .include "../assets/generated/objects.asm"
        .include "../assets/generated/level_names.asm"
        .include "../assets/generated/tables.asm"
        .include "../assets/generated/env_flicker.asm"
        .include "../assets/generated/types.asm"
        .include "../assets/generated/staff_tables.asm"
level_names:
        .binary "../assets/generated/names.bin"
NAME_ROWS = LEVEL_COUNT + 1     ; the levels', then Tom's
        .cerror * - level_names != NAME_ROWS * 80, "names"

; The pictures of the hazards that flicker: a page for
; each setting with them (the mire's wisps, the spikes of
; the pass and of the castle, its fire), FLICKER_FRAMES of
; 64 bytes, the 8 characters from FLICKER_CHAR
; (flicker_hazards).
        .align 256
flicker_pictures:
        .binary "../assets/generated/flicker.bin"
FLICKER_END = flicker_pictures + FLICKER_PAGES * 256
        .cerror * != FLICKER_END, "a page a setting"
        .cerror FLICKER_FRAMES * 64 != 256, "a page"

; Where each column of the level being played starts in
; its copy at LEVEL: a page of its own, after the hazards'
; pictures.
level_lo:
        .byte <(LEVEL + range(LEVEL_WIDTH) * 11)
level_hi:
        .byte >(LEVEL + range(LEVEL_WIDTH) * 11)
        .cerror (level_lo & $ff) != 0, "a page"

; The theme, compiled from score.py by music.py, and the
; tables of all the songs.
        .include "../assets/generated/music.asm"

        .cerror * > SCREEN_A, "code reaches the screens"

; Still more for under the KERNAL: in the PRG at SCREEN_A
; (the screens are drawn after the move), moved by
; move_high to HIGH_DATA_3, after Tom's pictures: where
; each byte of a picture of Tom goes, mirrored (tom.py),
; and Tom's theme (music_high.asm, from boss.py, and the
; jingles, from jingles.py); the texts of the states.
        * = SCREEN_A
        .logical HIGH_DATA_3
mirror_to:
        .binary "../assets/generated/mirror_to.bin"
        .cerror * - mirror_to != 256, "a page"
        .include "../assets/generated/music_high.asm"
; The texts of the title's menu and of the bands
; (title.py), for states.asm.
        .include "../assets/generated/texts.asm"
HIGH_END_3 = *
        .here
HIGH_PAGES_3 = (HIGH_END_3 - HIGH_DATA_3 + 255) / 256
        .cerror HIGH_END_3 > $fffa, "the vectors"
        .cerror (mirror_to & $ff) != 0, "mirror_to: a page"

; The game's states, the title, the score (states.asm) and
; their texts: in the PRG after the third block for under
; the KERNAL, in the screens too, moved by move_high to
; STATE_CODE ($0400, the KERNAL's screen, unused: the
; VIC-II sees bank 1).
STATE_LOAD = SCREEN_A + HIGH_PAGES_3 * 256
        * = STATE_LOAD
        .logical STATE_CODE
        .include "states.asm"
STATE_END = *
        .here
STATE_PAGES = (STATE_END - STATE_CODE + 255) / 256
        .cerror STATE_END > $0800, "under the program"
        .cerror HIGH_PAGES_3 + STATE_PAGES > 8, "screens"

        * = CHARSET
        .binary "../assets/generated/charset.bin"
; The HUD's characters. The codes after its glyphs must
; stay empty: the HUD's interrupt shows them on the last
; line of the playfield (irq.asm).
        * = HUD_CHARSET
        .binary "../assets/generated/hudset.bin"

; More packed data for under the KERNAL: in the PRG at
; SET_SLOT (empty until a setting's set is unpacked there),
; moved by move_high to HIGH_DATA_2, after the others:
; Tom's pictures and the map of level 4 (packed_mid.asm,
; from build_assets.py); the sound effects (sfx.asm, from
; sfx.py).
        * = SET_SLOT
        .logical HIGH_DATA_2
tom_packed:
        .binary "../assets/generated/tom.lz"
        .include "../assets/generated/packed_mid.asm"
        .include "../assets/generated/sfx.asm"
HIGH_END_2 = *
        .here
HIGH_PAGES_2 = (HIGH_END_2 - HIGH_DATA_2 + 255) / 256
        .cerror HIGH_PAGES_2 >= SET_PAGES, "the moth"
        .cerror HIGH_END_2 > TOM_PICS, "Tom's pictures"
        .cerror sfx_data + 256 < HIGH_END_2, "256 bytes"
; SET_SLOT: empty in the program; start_set and unpack_page
; fill it.

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
        * = LOGO_SPRITE         ; the title's name
        .binary "../assets/generated/logo.bin"
        .cerror * != LOGO_SPRITE + LOGO_SPRITES * 64, "4"
        .cerror * > SPRITES, "the name: under the sprites"
        .cerror LOGO_SPRITE < MOON_SPRITE + 64, "the moon"
        .cerror * != HUD_DATA, "the HUD's rows next"
; The HUD's rows 22 and 23, after the name: in the VIC-II's
; bank, but not seen there.
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

; The enemies of the mountain and of the castle: after
; the staff.
        * = ENEMY_SPRITES_2
        .binary ENEMY_FILE, ENEMIES_1
ENEMIES_2 = (ENEMY_TYPES - ENEMY_TYPES_1) * 256
        .cerror * - ENEMY_SPRITES_2 != ENEMIES_2, "4 a type"
        .cerror * > $8000, "sprites past the VIC-II bank"

; Out of the VIC-II's bank, packed (pack.py): each level's
; map, each setting's tables, the sets of characters of
; the settings but the village's (packed.asm, written by
; build_assets.py). Unpacked by start_map, start_tables,
; start_set and unpack_page.
        * = ENV_DATA
        .include "../assets/generated/packed.asm"
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

; The packed data under the KERNAL: in the PRG at
; HIGH_LOAD (where the level goes, later), moved to
; HIGH_DATA by the program when it starts (move_high).
        * = HIGH_LOAD
        .logical HIGH_DATA
        .include "../assets/generated/packed_high.asm"
HIGH_END = *
        .here
HIGH_PAGES = (HIGH_END - HIGH_DATA + 255) / 256
HIGH_STOP = HIGH_LOAD + HIGH_PAGES * 256
HIGH_DATA_2 = HIGH_DATA + HIGH_PAGES * 256
        .cerror HIGH_STOP > $d000, "the I/O"
        .cerror HIGH_END > $fffa, "the vectors"
