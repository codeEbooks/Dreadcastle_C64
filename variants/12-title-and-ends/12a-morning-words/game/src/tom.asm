; Tom Darkfang: the fight in the throne room, the
; arena at the end of level 8. Through the door of the
; throne room (touch_gate) Oscar comes into the arena in a
; transition (GO_ARENA): Tom's pictures are unpacked under
; the KERNAL; Oscar starts again at ARENA_X,
; the camera at the end of the level, still; from then on
; he starts again there (after a fall or with no health
; left), until dawn or the victory.
;
; Tom is four multicolour sprites, 3, 4, 5 and 7 (the moon
; stays 6): a picture of 48 x 42 pixels, a page of four
; blocks (tom.py), copied into the page of TOM_SPRITES not
; shown when it changes (facing left, mirrored as it is
; copied), and shown from then on. His x is
; the level x of his left edge, his y the line under his
; feet. His moves, leaps and charges:
;   TS_WAIT   at the start, still, looking at Oscar;
;   TS_GROWL  the warning: he growls, his arms up;
;   TS_LEAP   a leap at where Oscar is;
;   TS_LAND   still, after it;
;   TS_CHARGE a run at Oscar, to the wall;
;   TS_DAZED  against the wall, stars round his head.
; A leap and a charge in turn. Still (waiting, growling,
; landed, dazed) the staff strikes him: he flashes, a hit
; less; one hit until his next leap or charge. With half
; his hits gone he is faster. His touch takes health as an
; enemy's does. With no hits left he is beaten and runs
; away through the window: TS_YELP, then TS_RUN back to his
; throne, TS_HOP onto its dais, TS_PAUSE, TS_UP away
; through the high window over it, TS_GONE; then the
; victory (states.asm). Tom's theme stops when he is
; beaten; beaten, 5000 points.

TS_WAIT      = 0
TS_GROWL     = 1
TS_LEAP      = 2
TS_LAND      = 3
TS_CHARGE    = 4
TS_DAZED     = 5
TS_YELP      = 6
TS_RUN       = 7
TS_HOP       = 8
TS_PAUSE     = 9
TS_UP        = 10
TS_GONE      = 11
; His pictures (tom.py, NAMES).
T_STAND       = 0
T_GROWL       = 1
T_RUN_A       = 2
T_RUN_B       = 3
T_DAZED       = 4
        .cerror TOM_PICTURES != 5, "five pictures"

; The numbers of the fight: to change its feel.
HITS_FULL      = 8               ; the staff's hits: his bar
HITS_FAST      = HITS_FULL / 2    ; this many left: faster
WAIT_FRAMES   = 50              ; at the start
GROWL_FRAMES  = 40              ; the warning
GROWL_FAST    = 24
LAND_FRAMES   = 20
DAZED_FRAMES  = 60
DAZED_FAST    = 40
LEAP_VY       = $0600           ; 6 pixels a frame up
TOM_GRAVITY   = $0060           ; 0.375 more down a frame
LEAP_REACH    = 160             ; across: at most this far
CHARGE_ACCEL  = $0020           ; speeding up
CHARGE_MAX    = $0300           ; 3 pixels a frame
CHARGE_FAST   = $0400           ; 4 when he is faster
FLASH_FRAMES  = 16              ; struck: he flashes
YELP_FRAMES   = 50              ; beaten
FLEE_SPEED    = $0280           ; back to his throne
HOP_VY        = $0580           ; onto its dais
PAUSE_FRAMES  = 16
UP_SPEED      = 4               ; away: pixels a frame up
GONE_FRAMES   = 75              ; then the victory
TOM_FLOOR     = START_Y         ; the floor's line
; A leap lasts 31 frames: across, a 32nd of the way a
; frame (vx = dx * 8).
TOM_BLOCKS    = (TOM_SPRITES - $4000) / 64
        .cerror (TOM_SPRITES & $ff) != 0, "on a page"
        .cerror TOM_SPRITES + 512 > $8000, "in the bank"
        .cerror (TOM_PICS & $ff) != 0, "pages"
HIGH_TOP      = HIGH_DATA_2 + HIGH_PAGES_2 * 256
        .cerror HIGH_TOP > TOM_PICS, "under the KERNAL"
        .cerror TOM_PAGES != TOM_PICTURES + 1, "one empty"
TOM_END       = TOM_PICS + TOM_PAGES * 256
        .cerror TOM_END > HIGH_DATA_3, "mirror_to after"
        .cerror (MIRROR & $ff) != 0, "the table: a page"

; Into the arena, the transition's first step: the stream
; of Tom's pictures, unpacked a page a frame (TOM_PAGES:
; the last empty) at TOM_PICS; the theme stops (Tom's
; starts when the arena is shown, trans_on).
start_tom:
        lda #<tom_packed
        ldx #>tom_packed
        ldy #>TOM_PICS
        jsr unpack_start
        jmp music_stop

; The table that mirrors a byte of a multicolour sprite:
; its four pixels the other way round (made once, at the
; start: init_tom). Bits 76 54 32 10 become 10 32 54 76.
mirror_table:
        ldx #0
-       txa                     ; 10 to 76
        asl a
        asl a
        asl a
        asl a
        asl a
        asl a
        sta work
        txa                     ; 32 to 54
        asl a
        asl a
        and #%00110000
        ora work
        sta work
        txa                     ; 54 to 32
        lsr a
        lsr a
        and #%00001100
        ora work
        sta work
        txa                     ; 76 to 10
        lsr a
        lsr a
        lsr a
        lsr a
        lsr a
        lsr a
        ora work
        sta MIRROR,x
        inx
        bne -
        rts

; At the start of the program: Tom's bytes all 0; the
; table that mirrors.
init_tom:
        lda #0
        ldx #15
-       sta TOM,x
        dex
        bpl -
        ldx #TOM_2_BYTES - 1
-       sta TOM_2,x
        dex
        bpl -
        jmp mirror_table

; Tom at the start of the fight: in front of his throne,
; facing Oscar, all his hits; nothing shown yet (the page
; to copy into: the second).
reset_tom:
        lda #0
        sta tom_front
        sta tom_x
        sta tom_y
        sta tom_vx
        sta tom_vx + 1
        sta tom_vy
        sta tom_vy + 1
        sta tom_flash
        sta tom_safe
        sta tom_next            ; a leap first
        lda #<TOM_START_X
        sta tom_x + 1
        lda #>TOM_START_X
        sta tom_x + 2
        lda #TOM_FLOOR
        sta tom_y + 1
        lda #TS_WAIT
        sta tom_state
        lda #WAIT_FRAMES
        sta tom_timer
        lda #LEFT
        sta tom_face
        lda #T_STAND
        sta tom_pic
        lda #HITS_FULL
        sta tom_hits
        lda #$ff                ; a page to copy
        sta tom_shown
        rts

; A frame of the fight: Tom moves; the blow strikes him;
; while Oscar blinks nothing counts, else Tom's touch.
fight_tom:
        lda tom_flash
        beq +
        dec tom_flash
+       ldx tom_state
        lda tom_moves_lo,x
        sta vector
        lda tom_moves_hi,x
        sta vector + 1
        jsr _move
        jsr strike_tom
        lda protect
        beq touch_tom
        dec protect
        rts
_move:
        jmp (vector)

tom_moves_lo:
        .byte <tom_wait, <tom_growl, <tom_leap, <tom_land
        .byte <tom_charge, <tom_dazed, <tom_yelp, <tom_run
        .byte <tom_hop, <tom_pause, <tom_up, <tom_gone
tom_moves_hi:
        .byte >tom_wait, >tom_growl, >tom_leap, >tom_land
        .byte >tom_charge, >tom_dazed, >tom_yelp, >tom_run
        .byte >tom_hop, >tom_pause, >tom_up, >tom_gone
        .cerror * - tom_moves_hi != TS_GONE + 1, "each"

; His touch (fighting, not beaten): his box over Oscar's
; body, as an enemy's. Across: his box from TOM_BOX_LEFT
; to 47 - TOM_BOX_LEFT, Oscar's from BODY_LEFT to
; BODY_RIGHT: they meet when Oscar's x - Tom's x +
; (BODY_RIGHT - TOM_BOX_LEFT) is from 0 to TOUCH_SPAN.
; Up and down: Tom's feet less than TOM_BOX_UP under
; Oscar's, not more than his height - 1 over them.
BODY_WIDTH    = BODY_RIGHT - BODY_LEFT
TOUCH_SPAN    = 47 - 2 * TOM_BOX_LEFT + BODY_WIDTH
MIDDLES       = BODY_RIGHT - TOM_BOX_LEFT + 24 - 12 ; at one
touch_tom:
        lda tom_state
        cmp #TS_YELP
        bcs _no
        sec
        lda osc_x + 1
        sbc tom_x + 1
        sta edge
        lda osc_x + 2
        sbc tom_x + 2
        sta edge + 1
        clc
        lda edge
        adc #BODY_RIGHT - TOM_BOX_LEFT
        sta edge
        lda edge + 1
        adc #0
        bne _no                 ; under 0, or 256 or more
        lda edge
        cmp #TOUCH_SPAN + 1
        bcs _no
        lda tom_y + 1           ; his feet - Oscar's
        sec
        sbc osc_y + 1
        bcc _over
        cmp #TOM_BOX_UP         ; under: less than BOX_UP
        bcs _no
        bcc _hit
_over:
        eor #$ff                ; over: d = Oscar's - his
        adc #1
        sta work
        lda height
        sec
        sbc #1
        cmp work                ; d up to height - 1
        bcc _no
_hit:
        ldy #0                  ; thrown away from him:
        lda edge                ; Tom's middle right of
        cmp #MIDDLES            ; Oscar's: to the left
        bcs +
        ldy #2
+       sty hurt_dir
        jmp hurt
_no:
        rts

; The blow (blow_box) meets his box, while he is still
; (waiting, growling, landed, dazed) and not struck since
; his last move: a hit. He flashes; with no hits left he
; is beaten.
strike_tom:
        lda tom_safe
        bne _no
        ldx tom_state
        lda tom_still,x
        beq _no
        jsr blow_box
        bcs _no
        clc                     ; his box's left edge: not
        lda tom_x + 1           ; right of the blow's end
        adc #TOM_BOX_LEFT
        sta en_reg
        lda tom_x + 2
        adc #0
        sta en_reg + 1
        lda st_x1
        cmp en_reg
        lda st_x1 + 1
        sbc en_reg + 1
        bcc _no
        clc                     ; its right edge: not left
        lda tom_x + 1           ; of the blow's start
        adc #47 - TOM_BOX_LEFT
        sta en_reg
        lda tom_x + 2
        adc #0
        sta en_reg + 1
        lda en_reg
        cmp st_x0
        lda en_reg + 1
        sbc st_x0 + 1
        bcc _no
        lda tom_y + 1           ; its top: not under the
        sec                     ; blow
        sbc #TOM_BOX_UP
        cmp st_bottom
        beq +
        bcs _no
+       lda tom_y + 1           ; its bottom: not over it
        sec
        sbc #1
        cmp st_top
        bcc _no
        lda #1                  ; struck
        sta tom_safe
        lda #FLASH_FRAMES
        sta tom_flash
        dec tom_hits
        bne _no
        lda #$00                ; beaten: 5000
        ldy #$50
        jsr add_score
        jsr music_stop          ; his theme stops
        lda #TS_YELP
        ldx #YELP_FRAMES
        ldy #T_GROWL
        jmp tom_to
_no:
        rts

tom_still:      .byte 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0
        .cerror * - tom_still != TS_GONE + 1, "each"

; State A, for X frames, picture Y.
tom_to:
        sta tom_state
        stx tom_timer
        sty tom_pic
        rts

; Facing Oscar: left if his middle is left of Tom's.
face_oscar:
        sec
        lda osc_x + 1
        sbc tom_x + 1
        sta work
        lda osc_x + 2
        sbc tom_x + 2
        bmi _left               ; Oscar's x - Tom's < 0
        bne _right              ; 256 or more
        lda work
        cmp #24 - 12            ; middles: + 12, + 24
        bcs _right
_left:
        lda #LEFT
        bne +
_right:
        lda #RIGHT
+       sta tom_face
        rts

; At the start: still, looking at Oscar; then the growl.
tom_wait:
        jsr face_oscar
        dec tom_timer
        bne +
        jmp growl
+       rts

; The growl: looking at Oscar; then a leap and a charge
; in turn (tom_next: 0 a leap); he can be struck again
; after it.
tom_growl:
        jsr face_oscar
        dec tom_timer
        bne _done
        lda #0
        sta tom_safe
        lda tom_next
        eor #1
        sta tom_next
        bne leap                ; it was 0: a leap
        jmp charge
_done:
        rts

; The growl, for GROWL_FRAMES (faster: GROWL_FAST).
growl:
        lda tom_hits
        cmp #HITS_FAST + 1
        ldx #GROWL_FRAMES
        bcs +
        ldx #GROWL_FAST
+       lda #TS_GROWL
        ldy #T_GROWL
        jmp tom_to

; The leap at Oscar: up at LEAP_VY; across a 32nd a frame
; of the way to where Tom's middle is under Oscar's (his
; x there: Oscar's - 12), in the arena, at most
; LEAP_REACH away. It lasts 31 frames.
leap:
        sec                     ; where: Oscar's x - 12
        lda osc_x + 1
        sbc #24 - 12
        sta edge
        lda osc_x + 2
        sbc #0
        sta edge + 1
        lda edge                ; not left of TOM_MIN_X
        cmp #<TOM_MIN_X
        lda edge + 1
        sbc #>TOM_MIN_X
        bcs +
        lda #<TOM_MIN_X
        sta edge
        lda #>TOM_MIN_X
        sta edge + 1
+       lda #<TOM_MAX_X         ; nor right of TOM_MAX_X
        cmp edge
        lda #>TOM_MAX_X
        sbc edge + 1
        bcs +
        lda #<TOM_MAX_X
        sta edge
        lda #>TOM_MAX_X
        sta edge + 1
+       sec                     ; the way: there - x
        lda edge
        sbc tom_x + 1
        sta edge
        lda edge + 1
        sbc tom_x + 2
        sta edge + 1
        bmi _back
        bne _far                ; 256 or more
        lda edge
        cmp #LEAP_REACH + 1
        bcc _speed
_far:
        lda #LEAP_REACH
        ldx #0
        beq _most
_back:
        cmp #$ff                ; -256 or less
        bne _far_back
        lda edge
        cmp #<-LEAP_REACH
        bcs _speed
_far_back:
        lda #<-LEAP_REACH
        ldx #$ff
_most:
        sta edge
        stx edge + 1
_speed:
        lda edge                ; vx: the way * 8
        ldx #3
-       asl a
        rol edge + 1
        dex
        bne -
        sta tom_vx
        lda edge + 1
        sta tom_vx + 1
        lda #<-LEAP_VY
        sta tom_vy
        lda #>-LEAP_VY
        sta tom_vy + 1
        lda #TS_LEAP
        ldx #0
        ldy #T_RUN_B
        jmp tom_to

; In the leap: across and down; on the floor, still.
tom_leap:
        jsr tom_across
        lda #TOM_FLOOR
        jsr tom_fall
        bcc +
        lda #TS_LAND
        ldx #LAND_FRAMES
        ldy #T_STAND
        jmp tom_to
+       rts

; Landed: then the growl.
tom_land:
        dec tom_timer
        bne +
        jmp growl
+       rts

; x + vx (24 bits, signed), in the arena: at its edge he
; stops there.
tom_across:
        ldy #0
        lda tom_vx + 1
        bpl +
        dey
+       clc
        lda tom_x
        adc tom_vx
        sta tom_x
        lda tom_x + 1
        adc tom_vx + 1
        sta tom_x + 1
        tya
        adc tom_x + 2
        sta tom_x + 2
        lda tom_x + 1           ; left of TOM_MIN_X?
        cmp #<TOM_MIN_X
        lda tom_x + 2
        sbc #>TOM_MIN_X
        bcc _min
        lda #<TOM_MAX_X         ; right of TOM_MAX_X?
        cmp tom_x + 1
        lda #>TOM_MAX_X
        sbc tom_x + 2
        bcs _done
        lda #<TOM_MAX_X
        ldx #>TOM_MAX_X
        bne _stop
_min:
        lda #<TOM_MIN_X
        ldx #>TOM_MIN_X
_stop:
        sta tom_x + 1
        stx tom_x + 2
        lda #0
        sta tom_x
        sta tom_vx
        sta tom_vx + 1
_done:
        rts

; Tom up and down: vy + TOM_GRAVITY, y + vy. Falling onto
; line A or past it: there, still (carry set).
tom_fall:
        sta en_line
        clc
        lda tom_vy
        adc #<TOM_GRAVITY
        sta tom_vy
        lda tom_vy + 1
        adc #>TOM_GRAVITY
        sta tom_vy + 1
        clc
        lda tom_y
        adc tom_vy
        sta tom_y
        lda tom_y + 1
        adc tom_vy + 1
        sta tom_y + 1
        lda tom_vy + 1          ; going up
        bmi _up
        lda tom_y + 1
        cmp en_line
        bcc _up                 ; over the line yet
        lda en_line
        sta tom_y + 1
        lda #0
        sta tom_y
        sta tom_vx
        sta tom_vx + 1
        sta tom_vy
        sta tom_vy + 1
        sec
        rts
_up:
        clc
        rts

; The charge: the way he faces (at Oscar, from the growl),
; faster each frame, to CHARGE_MAX (faster: CHARGE_FAST);
; a stride every 4 frames; at the wall, dazed. tom_vx:
; the speed.
charge:
        lda #0
        sta tom_vx
        sta tom_vx + 1
        lda #TS_CHARGE
        ldx #0                  ; frames: the strides
        ldy #T_RUN_A
        jmp tom_to

tom_charge:
        jsr stride
        clc
        lda tom_vx
        adc #<CHARGE_ACCEL
        sta tom_vx
        lda tom_vx + 1
        adc #>CHARGE_ACCEL
        sta tom_vx + 1
        ldx #>CHARGE_MAX        ; at most
        lda tom_hits
        cmp #HITS_FAST + 1
        bcs +
        ldx #>CHARGE_FAST
+       cpx tom_vx + 1          ; there or past it (the
        beq _most               ; most's low byte 0): the
        bcs _run                ; most
_most:
        stx tom_vx + 1
        lda #0
        sta tom_vx
_run:
        jsr tom_run_on
        bcc _on
        ldx #DAZED_FRAMES       ; at the wall
        lda tom_hits
        cmp #HITS_FAST + 1
        bcs +
        ldx #DAZED_FAST
+       lda #TS_DAZED
        ldy #T_DAZED
        jmp tom_to
_on:
        rts
        .cerror (CHARGE_MAX & $ff) != 0, "whole pixels"
        .cerror (CHARGE_FAST & $ff) != 0, "whole pixels"

; The two strides in turn, every 4 frames.
stride:
        inc tom_timer
        lda tom_timer
        lsr a
        lsr a
        and #1
        clc
        adc #T_RUN_A
        sta tom_pic
        rts

; Running at tom_vx the way he faces, to the wall: there
; (carry set), still.
tom_run_on:
        lda tom_face
        bne _left
        clc
        lda tom_x
        adc tom_vx
        sta tom_x
        lda tom_x + 1
        adc tom_vx + 1
        sta tom_x + 1
        lda tom_x + 2
        adc #0
        sta tom_x + 2
        lda tom_x + 1           ; TOM_MAX_X or past it?
        cmp #<TOM_MAX_X
        lda tom_x + 2
        sbc #>TOM_MAX_X
        bcc _on
        lda #<TOM_MAX_X
        ldx #>TOM_MAX_X
        bne _wall
_left:
        sec
        lda tom_x
        sbc tom_vx
        sta tom_x
        lda tom_x + 1
        sbc tom_vx + 1
        sta tom_x + 1
        lda tom_x + 2
        sbc #0
        sta tom_x + 2
        lda #<TOM_MIN_X         ; TOM_MIN_X or past it?
        cmp tom_x + 1
        lda #>TOM_MIN_X
        sbc tom_x + 2
        bcc _on
        lda #<TOM_MIN_X
        ldx #>TOM_MIN_X
_wall:
        sta tom_x + 1
        stx tom_x + 2
        lda #0
        sta tom_x
        sta tom_vx
        sta tom_vx + 1
        sec
        rts
_on:
        clc
        rts

; Dazed: then the growl.
tom_dazed:
        dec tom_timer
        bne +
        jmp growl
+       rts

; Beaten: he yelps; then he runs back to his throne.
tom_yelp:
        dec tom_timer
        bne _done
        lda #<FLEE_SPEED
        sta tom_vx
        lda #>FLEE_SPEED
        sta tom_vx + 1
        lda tom_x + 1           ; the throne: right of him?
        cmp #<THRONE_X
        lda tom_x + 2
        sbc #>THRONE_X
        lda #RIGHT
        bcc +
        lda #LEFT
+       sta tom_face
        lda #TS_RUN
        ldx #0
        ldy #T_RUN_A
        jmp tom_to
_done:
        rts

; Back to the throne, at FLEE_SPEED; there, a hop onto
; its dais.
tom_run:
        jsr stride
        lda tom_face
        bne _left
        clc
        lda tom_x
        adc tom_vx
        sta tom_x
        lda tom_x + 1
        adc tom_vx + 1
        sta tom_x + 1
        lda tom_x + 2
        adc #0
        sta tom_x + 2
        lda tom_x + 1           ; THRONE_X or past it?
        cmp #<THRONE_X
        lda tom_x + 2
        sbc #>THRONE_X
        bcs _there
        rts
_left:
        sec
        lda tom_x
        sbc tom_vx
        sta tom_x
        lda tom_x + 1
        sbc tom_vx + 1
        sta tom_x + 1
        lda tom_x + 2
        sbc #0
        sta tom_x + 2
        lda #<THRONE_X          ; THRONE_X or past it?
        cmp tom_x + 1
        lda #>THRONE_X
        sbc tom_x + 2
        bcs _there
        rts
_there:
        lda #<THRONE_X
        sta tom_x + 1
        lda #>THRONE_X
        sta tom_x + 2
        lda #0
        sta tom_x
        sta tom_vx
        sta tom_vx + 1
        lda #<-HOP_VY
        sta tom_vy
        lda #>-HOP_VY
        sta tom_vy + 1
        lda #TS_HOP
        ldx #0
        ldy #T_RUN_B
        jmp tom_to

; The hop: onto the dais, then a moment there.
tom_hop:
        lda #DAIS_TOP
        jsr tom_fall
        bcc +
        lda #TS_PAUSE
        ldx #PAUSE_FRAMES
        ldy #T_STAND
        jmp tom_to
+       rts

tom_pause:
        dec tom_timer
        bne +
        lda #TS_UP
        ldx #0
        ldy #T_GROWL            ; his arms up: away
        jmp tom_to
+       rts

; Away, up through the high window, UP_SPEED a frame:
; past the top, gone.
tom_up:
        lda tom_y + 1
        sec
        sbc #UP_SPEED
        sta tom_y + 1
        bcs +
        lda #TS_GONE
        ldx #GONE_FRAMES
        ldy #T_STAND
        jmp tom_to
+       rts

; Gone: a moment, then the victory.
tom_gone:
        dec tom_timer
        bne +
        jmp start_won
+       rts

; Sprites 3, 4, 5 and 7: Tom, the four blocks of the page
; shown (tom_page); X register = x - camera + 31, + 24 on
; the right; Y register = feet - 42 + 50, + 21 below. His
; colour; struck, white two frames of every four. Gone:
; off. Then the moon (place_oscar has set $d010).
place_tom:
        lda tom_state
        cmp #TS_GONE
        bne +
        lda $d015
        and #%01000111
        sta $d015
        jmp place_moon
+       jsr tom_page
        sec
        lda tom_x + 1
        sbc camera
        sta tom_reg
        lda tom_x + 2
        sbc camera + 1
        sta tom_reg + 1
        clc
        lda tom_reg
        adc #31
        sta tom_reg
        sta $d006               ; 3: top left
        sta $d00a               ; 5: bottom left
        lda tom_reg + 1
        adc #0
        sta tom_reg + 1
        lda $d010               ; the ninth bits
        and #%01000111
        ldx tom_reg + 1
        beq +
        ora #%00101000          ; of 3 and 5
+       sta $d010
        clc
        lda tom_reg
        adc #24
        sta $d008               ; 4: top right
        sta $d00e               ; 7: bottom right
        lda tom_reg + 1
        adc #0
        beq +
        lda $d010
        ora #%10010000          ; of 4 and 7
        sta $d010
+       lda tom_y + 1
        clc
        adc #50 - 42
        sta $d007
        sta $d009
        adc #21
        sta $d00b
        sta $d00f
        lda tom_front           ; the four blocks shown
        asl a
        asl a
        adc #TOM_BLOCKS
        ldx #3
-       ldy tom_slots,x
        sta SCREEN_A + POINTERS,y
        sta SCREEN_B + POINTERS,y
        clc
        adc #1
        dex
        bpl -
        ldx #TOM_COLOUR
        lda tom_flash
        and #%00000010
        beq +
        ldx #TOM_FLASH_COLOUR
+       stx $d02a
        stx $d02b
        stx $d02c
        stx $d02e
        lda $d015
        ora #%10111000
        sta $d015
        jmp place_moon          ; its ninth bit too

; His sprites, the blocks of the page in reverse: bottom
; right, bottom left, top right, top left.
tom_slots:    .byte 7, 5, 4, 3

; Tom's picture (tom_pic, facing tom_face): when it is not
; the one shown (tom_shown: the mirrored ones numbered
; after the others), it is copied into the page not shown,
; which is shown from now on. Facing left it is
; mirrored as it is copied: byte Y of the picture, through
; MIRROR, to byte mirror_to[Y] of the page.
tom_page:
        lda tom_face            ; RIGHT 0, LEFT 1: then
        beq +                   ; the numbers after the
        lda #TOM_PICTURES       ; others
+       clc
        adc tom_pic
        cmp tom_shown
        beq _done
        sta tom_shown
        lda tom_pic             ; the picture, facing right
        clc
        adc #>TOM_PICS
        sta copy_src + 1
        lda #0
        sta copy_src
        tay
        lda tom_front           ; the page not shown
        eor #1
        sta tom_front
        ldx tom_face
        bne _left
        clc                     ; facing right: as it is
        adc #>TOM_SPRITES
        sta dst + 1
        sty dst
-       lda (copy_src),y
        sta (dst),y
        iny
        bne -
_done:
        rts
_left:
        tax                     ; facing left: page 0 or 1
        bne _left_1
-       lda (copy_src),y        ; mirrored into page 0
        tax
        lda MIRROR,x
        ldx mirror_to,y
        sta TOM_SPRITES,x
        iny
        bne -
        rts
_left_1:
-       lda (copy_src),y        ; mirrored into page 1
        tax
        lda MIRROR,x
        ldx mirror_to,y
        sta TOM_SPRITES + 256,x
        iny
        bne -
        rts

; The arena shown (trans_on): Tom's theme from its start,
; unless it is playing already (after a fall there it goes
; on); if the menu said MUSIC.
boss_theme:
        lda sound_mode
        bne +
        lda mus_song
        cmp #SONG_BOSS
        beq +
        lda #SONG_BOSS
        jmp music_start
+       rts

; In the arena, row 23 of the HUD's bars and Tom's on row
; 24 (show_hud): his hits left.
show_tom:
        lda tom_hits
        ldx #4
        ldy #TOM_BAR - HUD_ROW  ; (row 24: 40 on)
        jmp show_bar
