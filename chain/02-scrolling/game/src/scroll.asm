; Horizontal scrolling with two screens.
;
; camera is the level x at the left edge of the playfield.
; Its low 3 bits are the fine part: the playfield scroll is
; 7 minus them. camera / 8 is the level column in screen
; column 0: when it changes, everything moves by a column.
; The characters for that are ready in the back screen; the
; colour RAM, only one, is moved in place, right after the
; HUD starts, and is done before the beam needs it again.
;
; The back screen is made in three steps, one a frame, not
; in the frame of a swap: stage 0, rows 0-10 copied from
; the front screen one column over; stage 1, rows 11-21
; stage 2, the new column drawn from the level. Stage 3:
; ready. At 2 pixels a frame that is just in time: a swap
; every 4 frames. It is made for last_dir: the way the
; camera goes. Until it is ready the camera waits at the
; edge of its column.

; At the start: no frames counted, no joystick.
; (The camera and the screens: respawn.)
init_scroll:
        lda #0
        sta frame_count
        sta hud_flag
        sta joy
        rts

; At the start: the three steps of the back screen.
first_back:
        jsr prepare_back
        jsr prepare_back
        jmp prepare_back

; The scroll register of the playfield: multicolour, and
; 7 - (camera AND 7), which is (camera AND 7) EOR 7.
set_xscroll:
        lda camera
        and #%00000111
        eor #%00010111          ; bit 4: multicolour
        sta xscroll
        rts

; The joystick moves the camera, two pixels a frame: right
; or left; the back screen is made for that way.
steer_camera:
        lda #0
        sta swap
        lda #2
        sta speed
        lda joy
        and #JOY_RIGHT
        beq +
        lda #RIGHT
        sta last_dir
        jmp camera_right
+       lda joy
        and #JOY_LEFT
        beq +
        lda #LEFT
        sta last_dir
        jmp camera_left
+       rts

; Move the camera by speed pixels, right or left, from 0 to
; CAMERA_MAX. A move into the next column sets swap, if the
; back screen is ready for it; else the camera stops at the
; edge of its column.
camera_right:
        lda camera
        clc
        adc speed
        sta next
        lda camera + 1
        adc #0
        sta next + 1
        lda #<CAMERA_MAX        ; past the end?
        cmp next
        lda #>CAMERA_MAX
        sbc next + 1
        bcs +                   ; CAMERA_MAX >= next: no
        lda #<CAMERA_MAX
        sta next
        lda #>CAMERA_MAX
        sta next + 1
+       lda camera              ; a new column if the fine
        and #%00000111          ; part goes down: 7 -> 0, 1
        sta fine
        lda next
        and #%00000111
        cmp fine
        bcs camera_set          ; same column
        lda prep_dir            ; back screen for right
        bne _hold               ; and ready?
        lda prep_stage
        cmp #3
        bne _hold
        inc swap                ; yes: show it
        jmp camera_set
_hold:
        lda camera              ; no: wait at the last
        ora #%00000111          ; pixel of this column
        sta next
        lda camera + 1
        sta next + 1
        jmp camera_set

camera_left:
        lda camera
        sec
        sbc speed
        sta next
        lda camera + 1
        sbc #0
        sta next + 1
        bcs +                   ; not under 0
        lda #0
        sta next
        sta next + 1
+       lda camera              ; a new column if the fine
        and #%00000111          ; part goes up: 0 -> 7, 6
        sta fine
        lda next
        and #%00000111
        cmp fine
        beq camera_set          ; same column
        bcc camera_set
        lda prep_dir            ; back screen for left
        beq _hold               ; and ready?
        lda prep_stage
        cmp #3
        bne _hold
        inc swap                ; yes: show it
        jmp camera_set
_hold:
        lda camera              ; no: wait at the first
        and #%11111000          ; pixel of this column
        sta next
        lda camera + 1
        sta next + 1

camera_set:
        lda next
        sta camera
        lda next + 1
        sta camera + 1
        jmp set_xscroll

; The back screen goes in front, from the next frame: the
; top interrupt shows it. The colour RAM moves now, in
; place: rows 0-10 before the beam is back at row 0, rows
; 11-21 before it reaches row 11; then the new column.
do_swap:
        lda front
        eor #1
        sta front
        tax
        lda d018_values,x
        sta shown_d018
        lda prep_dir            ; 0 right, 1 left
        asl a
        asl a                   ; two routines a direction
        tax
        jsr colour_half         ; rows 0-10
        ldx prep_dir
        lda edge_columns,x
        tax
        jsr paint_top
top_painted:                    ; the tests check the line
        lda prep_dir
        asl a
        asl a
        tax
        inx
        inx                     ; the second routine
        jsr colour_half         ; rows 11-21
        ldx prep_dir
        lda edge_columns,x
        tax
        jsr paint_bottom
bottom_painted:                 ; and here
        lda #0                  ; a new back screen, from
        sta prep_stage          ; the start
        rts

colour_half:
        lda colour_moves,x
        sta vector
        lda colour_moves + 1,x
        sta vector + 1
        jmp (vector)

; One step of the back screen a frame, for last_dir. At the
; ends of the level there is nothing more to show that way.
prepare_back:
        lda last_dir
        cmp prep_dir
        beq +
        sta prep_dir            ; the other way: start again
        lda #0
        sta prep_stage
+       lda prep_dir
        bne _left_end
        lda camera              ; right: camera in the last
        cmp #<(CAMERA_MAX - 7)  ; column?
        lda camera + 1
        sbc #>(CAMERA_MAX - 7)
        bcs _nothing
        bcc _step
_left_end:
        lda camera + 1          ; left: camera in column 0?
        bne _step
        lda camera
        cmp #8
        bcc _nothing
_step:
        lda prep_stage
        cmp #2
        bcc _copy               ; stages 0 and 1
        bne _nothing            ; stage 3: ready
        jsr new_column          ; stage 2
        inc prep_stage
_nothing:
        rts
_copy:
        lda front               ; routine number:
        asl a                   ; front * 4
        ora prep_dir            ; + direction * 2
        asl a                   ; + stage
        ora prep_stage
        asl a                   ; 2 bytes an address
        tax
        lda screen_moves,x
        sta vector
        lda screen_moves + 1,x
        sta vector + 1
        jsr _call
        inc prep_stage
        rts
_call:
        jmp (vector)

; Stage 2: the column of the level that comes in, into the
; back screen: at column 38 going right, level column
; camera / 8 + 39; at column 0 going left, camera / 8 - 1.
new_column:
        ldx prep_dir
        lda edge_columns,x
        sta col_screen
        ldy front
        lda back_screens,y
        sta target_hi
        lda camera + 1          ; camera / 8, in 16 bits
        sta world + 1
        lda camera
        lsr world + 1
        ror a
        lsr world + 1
        ror a
        lsr world + 1
        ror a
        clc
        adc column_steps,x      ; + 39 or - 1
        sta world
        lda world + 1
        adc column_steps_hi,x
        sta world + 1
        jmp draw_column

back_screens:   .byte >SCREEN_B, >SCREEN_A
edge_columns:   .byte 38, 0     ; right, left
column_steps:   .byte 39, $ff   ; + 39, - 1
column_steps_hi:
                .byte 0, $ff

; The routines that move rows of characters by a column,
; from the front screen to the back one; and those that
; move the colour RAM in place. Going right, the picture
; moves left: cell X takes cell X + 1, X from 0 to 37.
; Going left, cell X takes cell X - 1, X from 38 down to 1.
; Each is unrolled on 11 rows: 9 or 10 cycles a cell.
move_left .macro from, to, first
        ldx #0
-
        .for row := \first, row < \first + 11, row += 1
        lda \from + row * 40 + 1,x
        sta \to + row * 40,x
        .endfor
        inx
        cpx #38
        bne -
        rts
        .endmacro

move_right .macro from, to, first
        ldx #38
-
        .for row := \first, row < \first + 11, row += 1
        lda \from + row * 40 - 1,x
        sta \to + row * 40,x
        .endfor
        dex
        bne -
        rts
        .endmacro

; front A, back B; then front B, back A.
a_right_top     #move_left SCREEN_A, SCREEN_B, 0
a_right_bottom  #move_left SCREEN_A, SCREEN_B, 11
a_left_top      #move_right SCREEN_A, SCREEN_B, 0
a_left_bottom   #move_right SCREEN_A, SCREEN_B, 11
b_right_top     #move_left SCREEN_B, SCREEN_A, 0
b_right_bottom  #move_left SCREEN_B, SCREEN_A, 11
b_left_top      #move_right SCREEN_B, SCREEN_A, 0
b_left_bottom   #move_right SCREEN_B, SCREEN_A, 11
; The colour RAM, in place.
c_right_top     #move_left COLOUR_RAM, COLOUR_RAM, 0
c_right_bottom  #move_left COLOUR_RAM, COLOUR_RAM, 11
c_left_top      #move_right COLOUR_RAM, COLOUR_RAM, 0
c_left_bottom   #move_right COLOUR_RAM, COLOUR_RAM, 11

screen_moves:
        .word a_right_top, a_right_bottom
        .word a_left_top, a_left_bottom
        .word b_right_top, b_right_bottom
        .word b_left_top, b_left_bottom
colour_moves:
        .word c_right_top, c_right_bottom
        .word c_left_top, c_left_bottom
