; Where everything is. The VIC-II sees bank 1, $4000-$7fff:
; two screens, the characters of the levels and of the HUD,
; the sprites. Each setting has its tables, put in
; ENV_TABLES when a level of that setting starts. {-6}
; ENV_TABLES when a level of that setting starts. The {7}
; village's set of characters stays at CHARSET; the others {7}
; wait out of the VIC-II's bank and go to SET_SLOT when a {7}
; level of their setting starts. {7}
; The maps of the levels and the tables of the settings {-7}
; wait at ENV_DATA as they are; a level's are copied where {-7}
; they are used when it starts (unpack.asm). {-7}
; The maps of the levels, the tables of the settings and {8}
; those sets wait packed, from ENV_DATA on and under the {8}
; KERNAL, and are unpacked where they are used {8}
; (unpack.asm). {8}

SCREEN_A    = $4000             ; two screens: one shown,
SCREEN_B    = $4400             ; one made ready behind
CHARSET     = $4800             ; characters: the village
SET_SLOT    = $5800             ; the other settings' {7}
SPRITES     = $6800             ; sprite data, 64 bytes each
ENEMY_SPRITES = $6000           ; the enemies' {6}
ENEMY_SPRITES_2 = $7900         ; more of them {6}
STAFF_SPRITES = $7600           ; the staff's {7}
PROFILE_INDEX = $78c0           ; where the profiles are {3}
MOON_SPRITE = $6600             ; the moon {7}
LOGO_SPRITE = $6640             ; the title's name {12}
HUD_DATA    = $6740             ; the HUD's rows and more
;|ENV_DATA    = $8000             ; the data of the levels {-7}
ENV_DATA    = $8000             ; the packed data {8}
HIGH_DATA   = $e000             ; more, under the KERNAL {8}
HIGH_LOAD   = $c000             ; where the PRG brings them {8}
TOM_SPRITES = $7e00             ; Tom's two pages {10}
TOM_PICS    = $f500             ; his pictures, under the {10}
                                ; KERNAL, facing right {10}
HIGH_DATA_3 = TOM_PICS + TOM_PAGES * 256 ; after them: {10}
                                ; mirror_to, the songs {10}
MIRROR      = $0200             ; the table that mirrors: {10}
                                ; the KERNAL's, it is out {10}
COLOUR_RAM  = $d800             ; fixed by the C64: only one
HUD         = 880               ; first HUD cell: row 22
HUD_ROW     = 920               ; row 23: the bars {3}
POINTERS    = $3f8              ; sprite pointers in it
LEVEL       = $c000             ; the level being played:
                                ; a copy, made when it {-3}
                                ; starts {-3}
                                ; a copy, the program {4}
                                ; changes it (1408 bytes) {4}
OBJECTS     = $c600             ; its objects: a copy of {5}
                                ; its block (objects.asm) {5}
ENEMIES     = $c680             ; its enemies, as they move {6}
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
; the VIC-II bank. Oscar's pictures: two blocks each, the {-3}
; lines, then the colours. {-3}
; the VIC-II bank. Oscar's pictures, the bat's and the {4}
; smoke's: two blocks each, the lines, then the colours. {4}
OSCAR_LINES = (SPRITES - $4000) / 64
; The enemies' pictures: four blocks a type (enemies.asm), {6}
; the village's and the wood's at ENEMY_SPRITES, the {6}
; others' at ENEMY_SPRITES_2 (type_block). {6}
ENEMY_BLOCKS = (ENEMY_SPRITES - $4000) / 64 ; {6}
ENEMY_BLOCKS_2 = (ENEMY_SPRITES_2 - $4000) / 64 ; {6}
        .cerror ENEMY_BLOCKS_2 % 4 != 0, "a multiple of 4" ; {6}
; The staff's: sprite 2 (staff.asm). {7}
STAFF_BLOCKS = (STAFF_SPRITES - $4000) / 64 ; {7}
; The moon of the settings out of the village: sprite 6 {7}
; (enemies.asm, place_moon). {7}
MOON_BLOCK  = (MOON_SPRITE - $4000) / 64 ; {7}
; The name on the title: sprites 2-5 (states.asm). {12}
LOGO_BLOCK  = (LOGO_SPRITE - $4000) / 64 ; {12}

; Oscar's forms. {4}
VAMPIRE     = 0 ; {4}
BAT         = 1 ; {4}

; The bottom of the playfield: feet there, Oscar has fallen. {3}
BOTTOM      = 176 ; {3}

; A kind of transition: back at the start, after a fall. {3-4}
; Kinds of transition: back to the lantern (or the start) {5-11}
; after a fall; level 1 again, at dawn; the next level, {5-9}
; through the gate. {5-9}
; after a fall; level 1 again, at dawn or after Tom; the {10-11}
; next level, through the gate; into Tom's arena. {10-11}
; Kinds of transition: back to the lantern (or the start); {12}
; a new game from the title, level 1; the next level; into {12}
; Tom's arena; the title, after the victory or dawn. {12}
GO_BACK     = 0 ; {3}
;|GO_START    = 1                 ; level 1 again {5-11}
GO_START    = 1                 ; from the title {12}
GO_NEXT     = 2                 ; through the gate {5}
GO_ARENA    = 3                 ; into Tom's arena {10}
GO_TITLE    = 4                 ; the title {12}
ARENA_LEVEL = LEVEL_COUNT - 1   ; its level: the last {10}

; The game's states (states.asm): playing, the title, the {12}
; count at the end of a level, the victory, dawn. {12}
ST_PLAY     = 0 ; {12}
ST_TITLE    = 1 ; {12}
ST_TALLY    = 2 ; {12}
ST_WON      = 3 ; {12}
ST_DAWN     = 4 ; {12}
; The choices of the title's menu: sound_mode. {12}
MUSIC       = 0 ; {12}
SOUND_FX    = 1 ; {12}
SILENT      = 2 ; {12}

; Raster lines of the two interrupts. On line 226, the
; last line of row 21, the street is black: the scroll
; can change there.
TOP_LINE    = 20                ; in the upper border
HUD_LINE    = 226               ; just before the HUD

; Directions: of the camera, of the back screen. {2-2}
; Directions: of the camera, and where Oscar looks. {3}
RIGHT       = 0 ; {2}
LEFT        = 1 ; {2}

; Joystick bits in joy (pushed: 1). {2}
JOY_UP      = %00000001 ; {2}
JOY_DOWN    = %00000010 ; {2}
JOY_LEFT    = %00000100 ; {2}
JOY_RIGHT   = %00001000 ; {2}
JOY_FIRE    = %00010000 ; {2}

; Zero page. Pointers and work bytes:
dst         = $02               ; screen address (2 bytes)
col_ptr     = $04               ; a column of the level (2)
top_tab     = $06               ; characters, upper half (2)
bottom_tab  = $08               ; characters, lower half (2)
vector      = $0a               ; a routine to call (2) {2}
world       = $0c               ; a column of the level (2)
next        = $0e               ; where the camera goes (2) {2}

; The state of the scrolling, together for the tests:
camera      = $10               ; level x at the left (2)
front       = $12               ; screen shown: 0 A, 1 B
prep_dir    = $13               ; back screen: for RIGHT {2}
prep_stage  = $14               ; or LEFT; 0-2 work, 3 done {2}
;|last_dir    = $15               ; where the camera goes {2-2}
last_dir    = $15               ; where Oscar looks {3}
swap        = $16               ; 1: show the back screen {2}
shown_d018  = $17               ; for the top interrupt
xscroll     = $18               ; $d016 for the playfield
frame_count = $19               ; +1 at each top interrupt
hud_flag    = $1a               ; set by the HUD interrupt
joy         = $1b               ; joystick 2: bits set = on {2}
speed       = $1c               ; camera: pixels this frame {2}

; Work bytes of the camera and of the drawing:
col_screen  = $1d               ; its column on the screen
target_hi   = $1e               ; high byte of the screen
mrow        = $1f               ; metatile row, 0-10
below       = $20               ; the lower character
fine        = $21               ; the camera's fine part {2}
edge_paint  = $22               ; 22 colours of the column

; The level being played. {1-2}
; The level being played, together for the tests. {3}
health      = $e0               ; 0 to HEALTH_FULL {3}
night       = $e1               ; steps of the night left {5}
night_time  = $e2               ; frames left: the step (2) {5}
got         = $e4               ; heirlooms taken {5}
got_bits    = $e5               ; which: bit 0, 1, 2 {5}
lantern_lit = $e6               ; 1: lit, Oscar starts there {5}
door_open   = $e7               ; 1 open; 2-7 opening {5}
trans       = $e8               ; frames of the transition {3}
;|trans_kind  = $e9               ; GO_BACK {3-4}
;|trans_kind  = $e9               ; GO_BACK, GO_START, GO_NEXT {5-9}
;|trans_kind  = $e9               ; GO_BACK ... GO_ARENA {10-11}
trans_kind  = $e9               ; GO_BACK ... GO_TITLE {12}
respawn_x   = $ea               ; where Oscar starts (2)
;|level_no    = $ec               ; the level: 0 {1-4}
level_no    = $ec               ; the level: 0, 1 ... {5}
protect     = $ed               ; frames of blinking {6}
stun        = $ee               ; frames without joystick {6}

; The staff, together for the tests. {7}
has_staff   = $f0               ; 1: Oscar holds it {7}
blow        = $f1               ; frames of the blow left {7}
; The setting of the tables and its two values of $d018
; (screen A, screen B):
env         = $f2
d018_values = $f3               ; (2)
env_copy    = $f5               ; 1: copying a setting {7}

; The objects of the level being played: the fields of {5}
; its block, copied to OBJECTS when it starts (their {5}
; offsets are in assets.inc). {5}
heirloom_x_lo  = OBJECTS + OF_HEIRLOOM_X_LO ; {5}
heirloom_x_hi  = OBJECTS + OF_HEIRLOOM_X_HI ; {5}
heirloom_top   = OBJECTS + OF_HEIRLOOM_TOP ; {5}
heirloom_block = OBJECTS + OF_HEIRLOOM_BLOCK ; {5}
door_col       = OBJECTS + OF_DOOR_COL ; {5}
door_row       = OBJECTS + OF_DOOR_ROW ; {5}
door_tile      = OBJECTS + OF_DOOR_TILE ; {5}
lantern_col    = OBJECTS + OF_LANTERN_COL ; {5}
lantern_line   = OBJECTS + OF_LANTERN_LINE ; {5}
lantern_row    = OBJECTS + OF_LANTERN_ROW ; {5}
lantern_x      = OBJECTS + OF_LANTERN_X ; {5}
lantern_tile   = OBJECTS + OF_LANTERN_TILE ; {5}
door_first     = OBJECTS + OF_DOOR_FIRST ; {5}
door_last      = OBJECTS + OF_DOOR_LAST ; {5}
door_line      = OBJECTS + OF_DOOR_LINE ; {5}
; Its enemies: how many, and MAX_ENEMIES of each field {6}
; (enemies.asm). {6}
enemy_count    = OBJECTS + OF_ENEMY_COUNT ; {6}
en_kind        = OBJECTS + OF_EN_KIND ; {6}
en_min_lo      = OBJECTS + OF_EN_MIN_LO ; {6}
en_min_hi      = OBJECTS + OF_EN_MIN_HI ; {6}
en_max_lo      = OBJECTS + OF_EN_MAX_LO ; {6}
en_max_hi      = OBJECTS + OF_EN_MAX_HI ; {6}
en_start_lo    = OBJECTS + OF_EN_START_LO ; {6}
en_start_hi    = OBJECTS + OF_EN_START_HI ; {6}
en_start_y     = OBJECTS + OF_EN_START_Y ; {6}
en_start_dir   = OBJECTS + OF_EN_START_DIR ; {6}
; The staff lying in the level: x of its sprite, the line {7}
; under it (0: none here). {7}
staff_x_lo     = OBJECTS + OF_STAFF_X_LO ; {7}
staff_x_hi     = OBJECTS + OF_STAFF_X_HI ; {7}
staff_line     = OBJECTS + OF_STAFF_LINE ; {7}
        .cerror OBJECTS + OBJECT_BYTES > ENEMIES, "objects" ; {6}
; The enemies as they move: MAX_ENEMIES of each, together {6}
; for the tests. x and y in 1/256 pixel, the speeds too. {6}
en_x_frac      = ENEMIES ; {6}
en_x_lo        = ENEMIES + 8 ; {6}
en_x_hi        = ENEMIES + 16 ; {6}
en_y_frac      = ENEMIES + 24 ; {6}
en_y           = ENEMIES + 32   ; the line under its feet {6}
en_vx_lo       = ENEMIES + 40   ; the cat's speeds {6}
en_vx_hi       = ENEMIES + 48 ; {6}
en_vy_lo       = ENEMIES + 56 ; {6}
en_vy_hi       = ENEMIES + 64 ; {6}
en_dir         = ENEMIES + 72   ; RIGHT or LEFT {6}
en_timer       = ENEMIES + 80   ; steps, wave, waiting {6}
en_air         = ENEMIES + 88   ; the cat: 1 in the air {6}
en_pic         = ENEMIES + 96   ; 0 or 1 {6}
en_gone        = ENEMIES + 104  ; struck: puff frames, $ff {7}
        .cerror MAX_ENEMIES != 8, "8 of each" ; {6}
        .cerror en_gone + 8 > ENV_TABLES, "enemies" ; {7}

; Tom Darkfang and his arena (tom.asm), together for the {10}
; tests: after the enemies, then after the objects. {10}
TOM         = en_gone + 8 ; {10}
arena       = TOM               ; 1: in the arena {10}
tom_state   = TOM + 1           ; TOM_WAIT ... TOM_GONE {10}
tom_timer   = TOM + 2           ; frames: of the state {10}
tom_x       = TOM + 3           ; level x, left edge (3) {10}
tom_y       = TOM + 6           ; line under his feet (2) {10}
tom_vx      = TOM + 8           ; speed across (2) {10}
tom_vy      = TOM + 10          ; speed down (2) {10}
tom_face    = TOM + 12          ; RIGHT or LEFT {10}
tom_pic     = TOM + 13          ; his picture: 0-4 {10}
tom_hits    = TOM + 14          ; hits left: the bar {10}
tom_flash   = TOM + 15          ; frames of the flash {10}
        .cerror TOM + 16 != ENV_TABLES, "Tom's 16 bytes" ; {10}
TOM_2       = OBJECTS + OBJECT_BYTES ; {10}
tom_safe    = TOM_2             ; 1: struck, until he moves {10}
tom_next    = TOM_2 + 1         ; his next move: 0 a leap {10}
tom_shown   = TOM_2 + 2         ; the page shown: picture {10}
tom_front   = TOM_2 + 3         ; and its page: 0 or 1 {10}
tom_reg     = TOM_2 + 4         ; his X register (2) {10}
TOM_2_BYTES = 6 ; {10}
        .cerror TOM_2 + TOM_2_BYTES > ENEMIES, "the objects" ; {10}

; Oscar's form and the energy of the flight, together for {4}
; the tests. {4}
osc_form    = $38               ; VAMPIRE or BAT {4}
osc_puff    = $39               ; frames left of the smoke {4}
energy      = $3a               ; in 1/256 of a unit (2) {4}
osc_gnam    = $3c               ; frames left of the gnam {4}
osc_flap    = $3d               ; frames flown: wing beats {4}
moths_eaten = $3e               ; moths the bat has eaten {4}

; Oscar. Positions in 1/256 pixel: the low byte is the {1-2}
; fraction. {1-2}
; Oscar, together for the tests. Positions and speeds in {3}
; 1/256 pixel: the low byte is the fraction. {3}
osc_x       = $40               ; level x, left edge (3)
osc_y       = $43               ; line under his feet (2)
osc_vx      = $45               ; speed across, signed (2) {3}
osc_vy      = $47               ; speed down, signed (2) {3}
osc_ground  = $49               ; 1: standing on a surface {3}
osc_face    = $4a               ; RIGHT or LEFT {3}
osc_anim    = $4b               ; distance walked (2) {3}
;|osc_pic     = $4d               ; his picture {1-2}
osc_pic     = $4d               ; 0-5 right, 6-11 left {3}
prev_joy    = $4e               ; joy of the frame before {3}

; A work byte: {1-2}
; Work bytes of Oscar and of the camera: {3}
sensor      = $50               ; level x under his feet (2) {3}
old_feet    = $52               ; osc_y before the move {3}
probe_top   = $53               ; find_surface looks from {3}
probe_low   = $54               ; this line to this one {3}
probe_row   = $55               ; the metatile row it reads {3}
probe_last  = $56               ; the last row to read {3}
probe_col   = $57               ; the level column (2) {3}
probe_prof  = $59               ; profile table (2) {3}
work        = $5b               ; a byte for a moment
screen_x    = $5c               ; Oscar's x on screen (2) {3}

; The music player: only the top interrupt uses these (and {11}
; music_start and music_stop, with the interrupts held). {11}
mus_ptr     = $60               ; pattern, order list (2) {11}
mus_tick    = $62               ; frames left in the step {11}
mus_tempo   = $63               ; position in tempo_table {11}
mus_frame   = $64               ; frames of music played (2) {11}
mus_note    = $66               ; work: note of the frame {11}
mus_freq    = $67               ; work: its frequency (2) {11}
mus_work    = $69               ; work: a byte {11}
mus_song    = $6a               ; the song: 0, 1 ... {11}
mus_on      = $6b               ; 1: playing; 0: stopped {11}
; Three bytes each, one a voice (X: 0, 1, 2): {11}
v_order     = $70               ; entry of the order list {11}
v_ptr_lo    = $73               ; where the pattern goes on {11}
v_ptr_hi    = $76 ; {11}
v_trans     = $79               ; transposition, semitones {11}
v_dur       = $7c               ; duration of the next note {11}
v_ins       = $7f               ; instrument {11}
v_left      = $82               ; steps left of the note {11}
v_note      = $85               ; the note, transposed {11}
v_wave      = $88               ; wavetable row {11}
v_gate      = $8b               ; gate: 0 or 1 {11}
v_pw_lo     = $8e               ; pulse width (2 tables) {11}
v_pw_hi     = $91 ; {11}
v_sweep     = $94               ; pulse sweep, signed {11}
v_vib       = $97               ; frames before the vibrato {11}
v_ctrl      = $9a               ; waveform of the frame {11}
sid_shadow  = $a0               ; the 25 SID registers {11}

; The copy of the data (unpack.asm): {-7}
; The unpacking (unpack.asm): {8}
;|up_src      = $b9               ; the data copied (2) {-7}
up_src      = $b9               ; the packed stream (2) {8}
up_dst      = $bb               ; where the output goes (2)
up_from     = $bd               ; the run copied from (2) {8}
up_run      = $bf               ; bytes left of the run {8}

; Work bytes: {1-2}
; Work bytes of the moves and of the transitions: {3-3}
; Work bytes of the moves, of the bat, of the metatiles {4}
; the program changes and of the transitions: {4}
delta       = $c0               ; speed added this frame (2) {3}
push        = $c2               ; joystick: 1, $ff or 0 {3}
tile_col    = $c3               ; a metatile's column {4}
tile_row    = $c4               ; and its row {4}
tile_at     = $c5               ; its screen column, signed {4}
tile_line   = $c6               ; its row in a screen (2) {4}
fill        = $c8               ; a character to write {4}
new_tile    = $c9               ; set_tile: the metatile {4}
corner      = $ca               ; and its corner, 0-3 {4}
height      = $cb               ; Oscar's body: lines {3}
edge        = $cc               ; a level x (2) {3}
row_last    = $ce               ; rows to look in: last {3}
copy_src    = $d0               ; objects, name: from (2)
col_end     = $d4               ; draw_columns: the end
; Work bytes of the enemies: {6}
en_i        = $d5               ; the enemy being moved {6}
en_slot     = $d6               ; its sprite: 3 + en_slot {6}
en_reg      = $d7               ; its X register (2) {6}
en_line     = $d9               ; its feet before the move {6}
en_dx       = $da               ; a distance across {6}
; Work bytes of the blow: what it reaches. {7}
st_x0       = $db               ; level x, from (2) {7}
st_x1       = $dd               ; to (2) {7}
st_top      = $df               ; lines: from {7}
st_bottom   = $f6               ; to {7}
flag_mask   = $f7               ; flag_column: SOLID, HAZARD {3}
hurt_dir    = $f8               ; 0 thrown right, 2 left {6}
; The frame of this turn: frame_count at its start, for {8}
; the hazards that flicker at its end (the top interrupt {8}
; may count on). {8}
turn_frame  = $f9 ; {8}
; More of the copy: {-7}
; More of the unpacking: {8}
up_n        = $fa               ; bytes copied now {8}
;|up_on       = $fb               ; 1: data to copy {-7}
up_on       = $fb               ; 1: a stream to unpack {8}
up_pages    = $fc               ; unpack_pages: pages left
; The playfield's background, the setting's $d021, set by {9}
; the top interrupt (the HUD's: black). {9}
play_d021   = $fd ; {9}

; The game's states, together for the tests: at STATES, {12}
; out of the zero page and out of the PRG ($0300: BASIC's {12}
; and the KERNAL's vectors, unused with both out); the {12}
; program sets them before it uses them. {12}
STATES      = $0300 ; {12}
game_state  = STATES            ; ST_PLAY ... ST_DAWN {12}
sound_mode  = STATES + 1        ; MUSIC, SOUND_FX, SILENT {12}
score       = STATES + 2        ; 6 BCD digits, low 1st (3) {12}
score_new   = STATES + 5        ; 1: the HUD to write it {12}
state_timer = STATES + 6        ; frames: of the phase {12}
state_phase = STATES + 7        ; the state's phase {12}
band_on     = STATES + 8        ; 1: a band of text shown {12}
band_top    = STATES + 9        ; its raster lines: from {12}
band_end    = STATES + 10       ; to {12}
band_d018   = STATES + 11       ; the HUD's set, the screen {12}
STATE_BYTES = 12 ; {12}
; The sound effects' (effects.asm), after them: for each {13}
; voice, where its effect has got to in sfx_data (0: {13}
; none), the frames left of its row, its frames a row; the {13}
; voice the last one took; sfx_start's caller's X, Y. {13}
SFX_VARS    = STATES + STATE_BYTES ; {13}
sfx_pos     = SFX_VARS          ; 3 {13}
sfx_tick    = SFX_VARS + 3      ; 3 {13}
sfx_speed   = SFX_VARS + 6      ; 3 {13}
sfx_last    = SFX_VARS + 9      ; 0-2 {13}
sfx_keep    = SFX_VARS + 10     ; X and Y of the caller (2) {13}
SFX_BYTES   = 12 ; {13}
STATE_CODE  = $0400             ; their code (data.asm) {12}
        .cerror SFX_VARS + SFX_BYTES > STATE_CODE, "states" ; {13}
