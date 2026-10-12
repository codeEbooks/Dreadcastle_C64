; The data, made by game/assets/build_assets.py.

        .cerror LEVEL_WIDTH != 128, "128 columns"

; Each level: its map, its name; its setting. {-4}
; Each level: its map, its objects, its name; its setting. {5-5}
; Each level: its map, its objects, its name; its setting; {6}
; the types of enemy. {6-6}
; the types of enemy; the staff. {7}
        .include "../assets/generated/level_maps.asm"
        .include "../assets/generated/objects.asm" ; {5}
        .include "../assets/generated/level_names.asm"
        .include "../assets/generated/tables.asm"
        .include "../assets/generated/env_flicker.asm" ; {8}
        .include "../assets/generated/types.asm" ; {6}
        .include "../assets/generated/staff_tables.asm" ; {7}
level_names:
        .binary "../assets/generated/names.bin"
NAME_ROWS = LEVEL_COUNT + 1     ; the levels', then Tom's
        .cerror * - level_names != NAME_ROWS * 80, "names"

; The pictures of the hazards that flicker: a page for {8}
; each setting with them (the mire's wisps, the spikes of {8}
; the pass and of the castle, its fire), FLICKER_FRAMES of {8}
; 64 bytes, the 8 characters from FLICKER_CHAR {8}
; (flicker_hazards). {8}
        .align 256 ; {8}
flicker_pictures: ; {8}
        .binary "../assets/generated/flicker.bin" ; {8}
FLICKER_END = flicker_pictures + FLICKER_PAGES * 256 ; {8}
        .cerror * != FLICKER_END, "a page a setting" ; {8}
        .cerror FLICKER_FRAMES * 64 != 256, "a page" ; {8}

; Where each column of the level being played starts in {-7}
; its copy at LEVEL: a page of its own. {-7}
;|        .align 256 ; {-7}
; Where each column of the level being played starts in {8}
; its copy at LEVEL: a page of its own, after the hazards' {8}
; pictures. {8}
level_lo:
        .byte <(LEVEL + range(LEVEL_WIDTH) * 11)
level_hi:
        .byte >(LEVEL + range(LEVEL_WIDTH) * 11)
        .cerror (level_lo & $ff) != 0, "a page"

; The theme, compiled from score.py by music.py, and the {11}
; tables of all the songs. {11}
        .include "../assets/generated/music.asm" ; {11}

        .cerror * > SCREEN_A, "code reaches the screens"

;{10}
; Still more for under the KERNAL: in the PRG at SCREEN_A
; (the screens are drawn after the move), moved by
; move_high to HIGH_DATA_3, after Tom's pictures: where
; each byte of a picture of Tom goes, mirrored (tom.py). {10-10}
; each byte of a picture of Tom goes, mirrored (tom.py), {11}
; and Tom's theme (music_high.asm, from boss.py, and the {11}
; jingles, from jingles.py). {11-11}
; jingles, from jingles.py); the texts of the states. {12}
        * = SCREEN_A
        .logical HIGH_DATA_3
mirror_to:
        .binary "../assets/generated/mirror_to.bin"
        .cerror * - mirror_to != 256, "a page"
        .include "../assets/generated/music_high.asm" ; {11}
; The texts of the title's menu and of the bands {12}
; (title.py), for states.asm. {12}
        .include "../assets/generated/texts.asm" ; {12}
HIGH_END_3 = *
        .here
HIGH_PAGES_3 = (HIGH_END_3 - HIGH_DATA_3 + 255) / 256
        .cerror HIGH_END_3 > $fffa, "the vectors"
        .cerror (mirror_to & $ff) != 0, "mirror_to: a page"
;{}

;{12}
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
;{}

        * = CHARSET
        .binary "../assets/generated/charset.bin"
; The HUD's characters. The codes after its glyphs must
; stay empty: the HUD's interrupt shows them on the last
; line of the playfield (irq.asm).
        * = HUD_CHARSET
        .binary "../assets/generated/hudset.bin"

;{8}
; More packed data for under the KERNAL: in the PRG at
; SET_SLOT (empty until a setting's set is unpacked there),
; moved by move_high to HIGH_DATA_2, after the others: {8-9}
; the map of level 4 (packed_mid.asm, from {8-9}
; build_assets.py). {8-9}
; moved by move_high to HIGH_DATA_2, after the others: {10}
; Tom's pictures and the map of level 4 (packed_mid.asm, {10}
; from build_assets.py). {10-12}
; from build_assets.py); the sound effects (sfx.asm, from {13}
; sfx.py). {13}
        * = SET_SLOT
        .logical HIGH_DATA_2
tom_packed: ; {10}
        .binary "../assets/generated/tom.lz" ; {10}
        .include "../assets/generated/packed_mid.asm"
        .include "../assets/generated/sfx.asm" ; {13}
HIGH_END_2 = *
        .here
HIGH_PAGES_2 = (HIGH_END_2 - HIGH_DATA_2 + 255) / 256
        .cerror HIGH_PAGES_2 >= SET_PAGES, "the moth"
        .cerror HIGH_END_2 > TOM_PICS, "Tom's pictures" ; {10}
        .cerror sfx_data + 256 < HIGH_END_2, "256 bytes" ; {13}
; SET_SLOT: empty in the program; start_set and unpack_page
; fill it.
;{}

; Sprites: Oscar's pictures, the bat's and the smoke's, two
; blocks each, then a block for each kind of heirloom.
HEIRLOOM_BLOCKS = OSCAR_LINES + PICTURE_COUNT * 2 ; {5}
SPRITE_BYTES = PICTURE_COUNT * 128 + HEIRLOOM_KINDS * 64

;{6}
ENEMY_END = ENEMY_SPRITES + ENEMY_TYPES_1 * 256
        * = ENEMY_SPRITES
ENEMY_FILE = "../assets/generated/enemies.bin"
ENEMIES_1 = ENEMY_TYPES_1 * 256 ; the village's, the wood's
        .binary ENEMY_FILE, 0, ENEMIES_1
        .cerror * != ENEMY_END, "4"
        .cerror * > SPRITES, "enemies: under the sprites"
;{}

;{7}
        * = MOON_SPRITE         ; the moon
        .binary "../assets/generated/moon.bin"
        .cerror * != MOON_SPRITE + 64, "the moon: a block"
        .cerror * > SPRITES, "the moon: under the sprites"
        .cerror MOON_SPRITE < ENEMY_END, "the moon: enemies"
;{}
;{12}
        * = LOGO_SPRITE         ; the title's name
        .binary "../assets/generated/logo.bin"
        .cerror * != LOGO_SPRITE + LOGO_SPRITES * 64, "4"
        .cerror * > SPRITES, "the name: under the sprites"
        .cerror LOGO_SPRITE < MOON_SPRITE + 64, "the moon"
        .cerror * != HUD_DATA, "the HUD's rows next"
;{}
; The HUD's rows 22 and 23: in the VIC-II's bank, but not {-11}
; seen there. {-11}
;|        * = HUD_DATA ; {-11}
; The HUD's rows 22 and 23, after the name: in the VIC-II's {12}
; bank, but not seen there. {12}
hud_chars:                      ; rows 22 and 23
        .binary "../assets/generated/hud.bin", 0, 80
hud_colours:
        .binary "../assets/generated/hud.bin", 120, 80
; The moth's two pictures: 16 bytes each, for its two {4}
; characters. {4}
moth_frames: ; {4}
        .binary "../assets/generated/moth.bin" ; {4}
        .cerror * - moth_frames != 32, "moth.bin" ; {4}
        .cerror * > SPRITES, "the HUD: under the sprites"

        * = SPRITES
        .binary "../assets/generated/sprites.bin"
        .cerror * - SPRITES != SPRITE_BYTES, "sprites"
        .cerror * > STAFF_SPRITES, "under the staff" ; {7}
        .cerror * > PROFILE_INDEX, "under the profiles" ; {3-6}

;{7}
        * = STAFF_SPRITES
        .binary "../assets/generated/staff.bin"
STAFF_BYTES = STAFF_PICTURES * 64
        .cerror * - STAFF_SPRITES != STAFF_BYTES, "staff"
        .cerror * != PROFILE_INDEX, "the profiles next"
;{}
; The profiles of the surfaces, in ENV_TABLES: for each {3}
; pixel column of a metatile, a table of PROFILE_STRIDE {3}
; bytes: the line of each profile in that column, or $ff. {3}
; Where the tables are: at PROFILE_INDEX. {3-6}
;|        * = PROFILE_INDEX ; {3-6}
; Where the tables are: after the staff's sprites. {7}
profile_lo: ; {3}
        .byte <(profiles + range(16) * PROFILE_STRIDE) ; {3}
profile_hi: ; {3}
        .byte >(profiles + range(16) * PROFILE_STRIDE) ; {3}
        .cerror * > ENEMY_SPRITES_2, "the profiles: under" ; {6}

;{8}
; The enemies of the mountain and of the castle: after
; the staff.
        * = ENEMY_SPRITES_2
        .binary ENEMY_FILE, ENEMIES_1
ENEMIES_2 = (ENEMY_TYPES - ENEMY_TYPES_1) * 256
        .cerror * - ENEMY_SPRITES_2 != ENEMIES_2, "4 a type"
        .cerror * > $8000, "sprites past the VIC-II bank"
;{}

; Out of the VIC-II's bank, as they are (plain.asm, {-7}
; written by build_assets.py): the maps of levels 1-3, {-7}
; the tables of their settings and the wood's set of {-7}
; characters. Copied by start_map, start_tables, start_set {-7}
; and unpack_page. {-7}
;|        * = ENV_DATA ; {-7}
;|        .include "../assets/generated/plain.asm" ; {-7}
; Out of the VIC-II's bank, packed (pack.py): each level's {8}
; map, each setting's tables, the sets of characters of {8}
; the settings but the village's (packed.asm, written by {8}
; build_assets.py). Unpacked by start_map, start_tables, {8}
; start_set and unpack_page. {8}
        * = ENV_DATA ; {8}
        .include "../assets/generated/packed.asm" ; {8}
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
        .cerror SET_SLOT - CHARSET != $1000, "+ $1000" ; {7}
        .cerror * > LEVEL, "the data reach the level"

;{8}
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
;{}
