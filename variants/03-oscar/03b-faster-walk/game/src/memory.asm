; Where everything is. The VIC-II sees bank 1, $4000-$7fff:
; two screens, the characters of the levels and of the HUD,
; the sprites. Each setting has its tables, put in
; ENV_TABLES when a level of that setting starts.
; The maps of the levels and the tables of the settings
; wait at ENV_DATA as they are; a level's are copied where
; they are used when it starts (unpack.asm).

SCREEN_A    = $4000             ; two screens: one shown,
SCREEN_B    = $4400             ; one made ready behind
CHARSET     = $4800             ; characters: the village
SPRITES     = $6800             ; sprite data, 64 bytes each
PROFILE_INDEX = $78c0           ; where the profiles are
HUD_DATA    = $6740             ; the HUD's rows and more
ENV_DATA    = $8000             ; the data of the levels
COLOUR_RAM  = $d800             ; fixed by the C64: only one
HUD         = 880               ; first HUD cell: row 22
HUD_ROW     = 920               ; row 23: the bars
POINTERS    = $3f8              ; sprite pointers in it
LEVEL       = $c000             ; the level being played:
                                ; a copy, made when it
                                ; starts
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
; the VIC-II bank. Oscar's pictures: two blocks each, the
; lines, then the colours.
OSCAR_LINES = (SPRITES - $4000) / 64

; The bottom of the playfield: feet there, Oscar has fallen.
BOTTOM      = 176

; A kind of transition: back at the start, after a fall.
GO_BACK     = 0

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
trans       = $e8               ; frames of the transition
trans_kind  = $e9               ; GO_BACK
respawn_x   = $ea               ; where Oscar starts (2)
level_no    = $ec               ; the level: 0

; The setting of the tables and its two values of $d018
; (screen A, screen B):
env         = $f2
d018_values = $f3               ; (2)

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

; The copy of the data (unpack.asm):
up_src      = $b9               ; the data copied (2)
up_dst      = $bb               ; where the output goes (2)

; Work bytes of the moves and of the transitions:
delta       = $c0               ; speed added this frame (2)
push        = $c2               ; joystick: 1, $ff or 0
height      = $cb               ; Oscar's body: lines
edge        = $cc               ; a level x (2)
row_last    = $ce               ; rows to look in: last
copy_src    = $d0               ; objects, name: from (2)
col_end     = $d4               ; draw_columns: the end
flag_mask   = $f7               ; flag_column: SOLID, HAZARD
; More of the copy:
up_on       = $fb               ; 1: data to copy
up_pages    = $fc               ; unpack_pages: pages left
