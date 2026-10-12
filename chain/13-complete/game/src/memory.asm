; Where everything is. The VIC-II sees bank 1, $4000-$7fff:
; two screens, the characters of the levels and of the HUD,
; the sprites. Each setting has its tables, put in
; ENV_TABLES when a level of that setting starts. The
; village's set of characters stays at CHARSET; the others
; wait out of the VIC-II's bank and go to SET_SLOT when a
; level of their setting starts.
; The maps of the levels, the tables of the settings and
; those sets wait packed, from ENV_DATA on and under the
; KERNAL, and are unpacked where they are used
; (unpack.asm).

SCREEN_A    = $4000             ; two screens: one shown,
SCREEN_B    = $4400             ; one made ready behind
CHARSET     = $4800             ; characters: the village
SET_SLOT    = $5800             ; the other settings'
SPRITES     = $6800             ; sprite data, 64 bytes each
ENEMY_SPRITES = $6000           ; the enemies'
ENEMY_SPRITES_2 = $7900         ; more of them
STAFF_SPRITES = $7600           ; the staff's
PROFILE_INDEX = $78c0           ; where the profiles are
MOON_SPRITE = $6600             ; the moon
LOGO_SPRITE = $6640             ; the title's name
HUD_DATA    = $6740             ; the HUD's rows and more
ENV_DATA    = $8000             ; the packed data
HIGH_DATA   = $e000             ; more, under the KERNAL
HIGH_LOAD   = $c000             ; where the PRG brings them
TOM_SPRITES = $7e00             ; Tom's two pages
TOM_PICS    = $f500             ; his pictures, under the
                                ; KERNAL, facing right
HIGH_DATA_3 = TOM_PICS + TOM_PAGES * 256 ; after them:
                                ; mirror_to, the songs
MIRROR      = $0200             ; the table that mirrors:
                                ; the KERNAL's, it is out
COLOUR_RAM  = $d800             ; fixed by the C64: only one
HUD         = 880               ; first HUD cell: row 22
HUD_ROW     = 920               ; row 23: the bars
POINTERS    = $3f8              ; sprite pointers in it
LEVEL       = $c000             ; the level being played:
                                ; a copy, the program
                                ; changes it (1408 bytes)
OBJECTS     = $c600             ; its objects: a copy of
                                ; its block (objects.asm)
ENEMIES     = $c680             ; its enemies, as they move
ENV_TABLES  = $c700             ; the setting's tables: the
                                ; colour RAM value of each
                                ; character; each metatile's
                                ; flags, profile, chars;
                                ; the profiles (9 pages)
char_colour = ENV_TABLES
metaflags   = ENV_TABLES + $100
metashape   = ENV_TABLES + $200
meta_tl     = ENV_TABLES + $300
meta_tr     = ENV_TABLES + $400
meta_bl     = ENV_TABLES + $500
meta_br     = ENV_TABLES + $600
profiles    = ENV_TABLES + $700 ; 16 x PROFILE_STRIDE
        .cerror ENV_PAGES != 9, "nine pages"
        .cerror ENV_TABLES + ENV_PAGES * 256 > $d000, "env"
HUD_CHARSET = $5000             ; characters of the HUD

; $d018 for each screen: screen at bank + $0000 or + $0400,
; characters at bank + $0800.
D018_A      = %00000010
D018_B      = %00010010
; From line 226 the HUD: its own characters (screen A: the
; HUD rows are the same in both screens).
D018_HUD    = %00000100

; The sprite pointer counts 64-byte blocks from the start of
; the VIC-II bank. Oscar's pictures, the bat's and the
; smoke's: two blocks each, the lines, then the colours.
OSCAR_LINES = (SPRITES - $4000) / 64
; The enemies' pictures: four blocks a type (enemies.asm),
; the village's and the wood's at ENEMY_SPRITES, the
; others' at ENEMY_SPRITES_2 (type_block).
ENEMY_BLOCKS = (ENEMY_SPRITES - $4000) / 64
ENEMY_BLOCKS_2 = (ENEMY_SPRITES_2 - $4000) / 64
        .cerror ENEMY_BLOCKS_2 % 4 != 0, "a multiple of 4"
; The staff's: sprite 2 (staff.asm).
STAFF_BLOCKS = (STAFF_SPRITES - $4000) / 64
; The moon of the settings out of the village: sprite 6
; (enemies.asm, place_moon).
MOON_BLOCK  = (MOON_SPRITE - $4000) / 64
; The name on the title: sprites 2-5 (states.asm).
LOGO_BLOCK  = (LOGO_SPRITE - $4000) / 64

; Oscar's forms.
VAMPIRE     = 0
BAT         = 1

; The bottom of the playfield: feet there, Oscar has fallen.
BOTTOM      = 176

; Kinds of transition: back to the lantern (or the start)
; a new game from the title, level 1; the next level; into
; Tom's arena; the title, after the victory or dawn.
GO_BACK     = 0
GO_START    = 1                 ; from the title
GO_NEXT     = 2                 ; through the gate
GO_ARENA    = 3                 ; into Tom's arena
GO_TITLE    = 4                 ; the title
ARENA_LEVEL = LEVEL_COUNT - 1   ; its level: the last

; The game's states (states.asm): playing, the title, the
; count at the end of a level, the victory, dawn.
ST_PLAY     = 0
ST_TITLE    = 1
ST_TALLY    = 2
ST_WON      = 3
ST_DAWN     = 4
; The choices of the title's menu: sound_mode.
MUSIC       = 0
SOUND_FX    = 1
SILENT      = 2

; Raster lines of the two interrupts. On line 226, the
; last line of row 21, the street is black: the scroll
; can change there.
TOP_LINE    = 20                ; in the upper border
HUD_LINE    = 226               ; just before the HUD

; Directions: of the camera, and where Oscar looks.
RIGHT       = 0
LEFT        = 1

; Joystick bits in joy (pushed: 1).
JOY_UP      = %00000001
JOY_DOWN    = %00000010
JOY_LEFT    = %00000100
JOY_RIGHT   = %00001000
JOY_FIRE    = %00010000

; Zero page. Pointers and work bytes:
dst         = $02               ; screen address (2 bytes)
col_ptr     = $04               ; a column of the level (2)
top_tab     = $06               ; characters, upper half (2)
bottom_tab  = $08               ; characters, lower half (2)
vector      = $0a               ; a routine to call (2)
world       = $0c               ; a column of the level (2)
next        = $0e               ; where the camera goes (2)

; The state of the scrolling, together for the tests:
camera      = $10               ; level x at the left (2)
front       = $12               ; screen shown: 0 A, 1 B
prep_dir    = $13               ; back screen: for RIGHT
prep_stage  = $14               ; or LEFT; 0-2 work, 3 done
last_dir    = $15               ; where Oscar looks
swap        = $16               ; 1: show the back screen
shown_d018  = $17               ; for the top interrupt
xscroll     = $18               ; $d016 for the playfield
frame_count = $19               ; +1 at each top interrupt
hud_flag    = $1a               ; set by the HUD interrupt
joy         = $1b               ; joystick 2: bits set = on
speed       = $1c               ; camera: pixels this frame

; Work bytes of the camera and of the drawing:
col_screen  = $1d               ; its column on the screen
target_hi   = $1e               ; high byte of the screen
mrow        = $1f               ; metatile row, 0-10
below       = $20               ; the lower character
fine        = $21               ; the camera's fine part
edge_paint  = $22               ; 22 colours of the column

; The level being played, together for the tests.
health      = $e0               ; 0 to HEALTH_FULL
night       = $e1               ; steps of the night left
night_time  = $e2               ; frames left: the step (2)
got         = $e4               ; heirlooms taken
got_bits    = $e5               ; which: bit 0, 1, 2
lantern_lit = $e6               ; 1: lit, Oscar starts there
door_open   = $e7               ; 1 open; 2-7 opening
trans       = $e8               ; frames of the transition
trans_kind  = $e9               ; GO_BACK ... GO_TITLE
respawn_x   = $ea               ; where Oscar starts (2)
level_no    = $ec               ; the level: 0, 1 ...
protect     = $ed               ; frames of blinking
stun        = $ee               ; frames without joystick

; The staff, together for the tests.
has_staff   = $f0               ; 1: Oscar holds it
blow        = $f1               ; frames of the blow left
; The setting of the tables and its two values of $d018
; (screen A, screen B):
env         = $f2
d018_values = $f3               ; (2)
env_copy    = $f5               ; 1: copying a setting

; The objects of the level being played: the fields of
; its block, copied to OBJECTS when it starts (their
; offsets are in assets.inc).
heirloom_x_lo  = OBJECTS + OF_HEIRLOOM_X_LO
heirloom_x_hi  = OBJECTS + OF_HEIRLOOM_X_HI
heirloom_top   = OBJECTS + OF_HEIRLOOM_TOP
heirloom_block = OBJECTS + OF_HEIRLOOM_BLOCK
door_col       = OBJECTS + OF_DOOR_COL
door_row       = OBJECTS + OF_DOOR_ROW
door_tile      = OBJECTS + OF_DOOR_TILE
lantern_col    = OBJECTS + OF_LANTERN_COL
lantern_line   = OBJECTS + OF_LANTERN_LINE
lantern_row    = OBJECTS + OF_LANTERN_ROW
lantern_x      = OBJECTS + OF_LANTERN_X
lantern_tile   = OBJECTS + OF_LANTERN_TILE
door_first     = OBJECTS + OF_DOOR_FIRST
door_last      = OBJECTS + OF_DOOR_LAST
door_line      = OBJECTS + OF_DOOR_LINE
; Its enemies: how many, and MAX_ENEMIES of each field
; (enemies.asm).
enemy_count    = OBJECTS + OF_ENEMY_COUNT
en_kind        = OBJECTS + OF_EN_KIND
en_min_lo      = OBJECTS + OF_EN_MIN_LO
en_min_hi      = OBJECTS + OF_EN_MIN_HI
en_max_lo      = OBJECTS + OF_EN_MAX_LO
en_max_hi      = OBJECTS + OF_EN_MAX_HI
en_start_lo    = OBJECTS + OF_EN_START_LO
en_start_hi    = OBJECTS + OF_EN_START_HI
en_start_y     = OBJECTS + OF_EN_START_Y
en_start_dir   = OBJECTS + OF_EN_START_DIR
; The staff lying in the level: x of its sprite, the line
; under it (0: none here).
staff_x_lo     = OBJECTS + OF_STAFF_X_LO
staff_x_hi     = OBJECTS + OF_STAFF_X_HI
staff_line     = OBJECTS + OF_STAFF_LINE
        .cerror OBJECTS + OBJECT_BYTES > ENEMIES, "objects"
; The enemies as they move: MAX_ENEMIES of each, together
; for the tests. x and y in 1/256 pixel, the speeds too.
en_x_frac      = ENEMIES
en_x_lo        = ENEMIES + 8
en_x_hi        = ENEMIES + 16
en_y_frac      = ENEMIES + 24
en_y           = ENEMIES + 32   ; the line under its feet
en_vx_lo       = ENEMIES + 40   ; the cat's speeds
en_vx_hi       = ENEMIES + 48
en_vy_lo       = ENEMIES + 56
en_vy_hi       = ENEMIES + 64
en_dir         = ENEMIES + 72   ; RIGHT or LEFT
en_timer       = ENEMIES + 80   ; steps, wave, waiting
en_air         = ENEMIES + 88   ; the cat: 1 in the air
en_pic         = ENEMIES + 96   ; 0 or 1
en_gone        = ENEMIES + 104  ; struck: puff frames, $ff
        .cerror MAX_ENEMIES != 8, "8 of each"
        .cerror en_gone + 8 > ENV_TABLES, "enemies"

; Tom Darkfang and his arena (tom.asm), together for the
; tests: after the enemies, then after the objects.
TOM         = en_gone + 8
arena       = TOM               ; 1: in the arena
tom_state   = TOM + 1           ; TOM_WAIT ... TOM_GONE
tom_timer   = TOM + 2           ; frames: of the state
tom_x       = TOM + 3           ; level x, left edge (3)
tom_y       = TOM + 6           ; line under his feet (2)
tom_vx      = TOM + 8           ; speed across (2)
tom_vy      = TOM + 10          ; speed down (2)
tom_face    = TOM + 12          ; RIGHT or LEFT
tom_pic     = TOM + 13          ; his picture: 0-4
tom_hits    = TOM + 14          ; hits left: the bar
tom_flash   = TOM + 15          ; frames of the flash
        .cerror TOM + 16 != ENV_TABLES, "Tom's 16 bytes"
TOM_2       = OBJECTS + OBJECT_BYTES
tom_safe    = TOM_2             ; 1: struck, until he moves
tom_next    = TOM_2 + 1         ; his next move: 0 a leap
tom_shown   = TOM_2 + 2         ; the page shown: picture
tom_front   = TOM_2 + 3         ; and its page: 0 or 1
tom_reg     = TOM_2 + 4         ; his X register (2)
TOM_2_BYTES = 6
        .cerror TOM_2 + TOM_2_BYTES > ENEMIES, "the objects"

; Oscar's form and the energy of the flight, together for
; the tests.
osc_form    = $38               ; VAMPIRE or BAT
osc_puff    = $39               ; frames left of the smoke
energy      = $3a               ; in 1/256 of a unit (2)
osc_gnam    = $3c               ; frames left of the gnam
osc_flap    = $3d               ; frames flown: wing beats
moths_eaten = $3e               ; moths the bat has eaten

; Oscar, together for the tests. Positions and speeds in
; 1/256 pixel: the low byte is the fraction.
osc_x       = $40               ; level x, left edge (3)
osc_y       = $43               ; line under his feet (2)
osc_vx      = $45               ; speed across, signed (2)
osc_vy      = $47               ; speed down, signed (2)
osc_ground  = $49               ; 1: standing on a surface
osc_face    = $4a               ; RIGHT or LEFT
osc_anim    = $4b               ; distance walked (2)
osc_pic     = $4d               ; 0-5 right, 6-11 left
prev_joy    = $4e               ; joy of the frame before

; Work bytes of Oscar and of the camera:
sensor      = $50               ; level x under his feet (2)
old_feet    = $52               ; osc_y before the move
probe_top   = $53               ; find_surface looks from
probe_low   = $54               ; this line to this one
probe_row   = $55               ; the metatile row it reads
probe_last  = $56               ; the last row to read
probe_col   = $57               ; the level column (2)
probe_prof  = $59               ; profile table (2)
work        = $5b               ; a byte for a moment
screen_x    = $5c               ; Oscar's x on screen (2)

; The music player: only the top interrupt uses these (and
; music_start and music_stop, with the interrupts held).
mus_ptr     = $60               ; pattern, order list (2)
mus_tick    = $62               ; frames left in the step
mus_tempo   = $63               ; position in tempo_table
mus_frame   = $64               ; frames of music played (2)
mus_note    = $66               ; work: note of the frame
mus_freq    = $67               ; work: its frequency (2)
mus_work    = $69               ; work: a byte
mus_song    = $6a               ; the song: 0, 1 ...
mus_on      = $6b               ; 1: playing; 0: stopped
; Three bytes each, one a voice (X: 0, 1, 2):
v_order     = $70               ; entry of the order list
v_ptr_lo    = $73               ; where the pattern goes on
v_ptr_hi    = $76
v_trans     = $79               ; transposition, semitones
v_dur       = $7c               ; duration of the next note
v_ins       = $7f               ; instrument
v_left      = $82               ; steps left of the note
v_note      = $85               ; the note, transposed
v_wave      = $88               ; wavetable row
v_gate      = $8b               ; gate: 0 or 1
v_pw_lo     = $8e               ; pulse width (2 tables)
v_pw_hi     = $91
v_sweep     = $94               ; pulse sweep, signed
v_vib       = $97               ; frames before the vibrato
v_ctrl      = $9a               ; waveform of the frame
sid_shadow  = $a0               ; the 25 SID registers

; The unpacking (unpack.asm):
up_src      = $b9               ; the packed stream (2)
up_dst      = $bb               ; where the output goes (2)
up_from     = $bd               ; the run copied from (2)
up_run      = $bf               ; bytes left of the run

; Work bytes of the moves, of the bat, of the metatiles
; the program changes and of the transitions:
delta       = $c0               ; speed added this frame (2)
push        = $c2               ; joystick: 1, $ff or 0
tile_col    = $c3               ; a metatile's column
tile_row    = $c4               ; and its row
tile_at     = $c5               ; its screen column, signed
tile_line   = $c6               ; its row in a screen (2)
fill        = $c8               ; a character to write
new_tile    = $c9               ; set_tile: the metatile
corner      = $ca               ; and its corner, 0-3
height      = $cb               ; Oscar's body: lines
edge        = $cc               ; a level x (2)
row_last    = $ce               ; rows to look in: last
copy_src    = $d0               ; objects, name: from (2)
col_end     = $d4               ; draw_columns: the end
; Work bytes of the enemies:
en_i        = $d5               ; the enemy being moved
en_slot     = $d6               ; its sprite: 3 + en_slot
en_reg      = $d7               ; its X register (2)
en_line     = $d9               ; its feet before the move
en_dx       = $da               ; a distance across
; Work bytes of the blow: what it reaches.
st_x0       = $db               ; level x, from (2)
st_x1       = $dd               ; to (2)
st_top      = $df               ; lines: from
st_bottom   = $f6               ; to
flag_mask   = $f7               ; flag_column: SOLID, HAZARD
hurt_dir    = $f8               ; 0 thrown right, 2 left
; The frame of this turn: frame_count at its start, for
; the hazards that flicker at its end (the top interrupt
; may count on).
turn_frame  = $f9
; More of the unpacking:
up_n        = $fa               ; bytes copied now
up_on       = $fb               ; 1: a stream to unpack
up_pages    = $fc               ; unpack_pages: pages left
; The playfield's background, the setting's $d021, set by
; the top interrupt (the HUD's: black).
play_d021   = $fd

; The game's states, together for the tests: at STATES,
; out of the zero page and out of the PRG ($0300: BASIC's
; and the KERNAL's vectors, unused with both out); the
; program sets them before it uses them.
STATES      = $0300
game_state  = STATES            ; ST_PLAY ... ST_DAWN
sound_mode  = STATES + 1        ; MUSIC, SOUND_FX, SILENT
score       = STATES + 2        ; 6 BCD digits, low 1st (3)
score_new   = STATES + 5        ; 1: the HUD to write it
state_timer = STATES + 6        ; frames: of the phase
state_phase = STATES + 7        ; the state's phase
band_on     = STATES + 8        ; 1: a band of text shown
band_top    = STATES + 9        ; its raster lines: from
band_end    = STATES + 10       ; to
band_d018   = STATES + 11       ; the HUD's set, the screen
STATE_BYTES = 12
; The sound effects' (effects.asm), after them: for each
; voice, where its effect has got to in sfx_data (0:
; none), the frames left of its row, its frames a row; the
; voice the last one took; sfx_start's caller's X, Y.
SFX_VARS    = STATES + STATE_BYTES
sfx_pos     = SFX_VARS          ; 3
sfx_tick    = SFX_VARS + 3      ; 3
sfx_speed   = SFX_VARS + 6      ; 3
sfx_last    = SFX_VARS + 9      ; 0-2
sfx_keep    = SFX_VARS + 10     ; X and Y of the caller (2)
SFX_BYTES   = 12
STATE_CODE  = $0400             ; their code (data.asm)
        .cerror SFX_VARS + SFX_BYTES > STATE_CODE, "states"
