; Oscar's sprites on the screen: his place and his {-2}
; picture. {-2}
; Oscar walks and jumps: the moves of a platform game, in {3}
; fixed point. Positions and speeds count 1/256 pixel: the {3}
; low byte is the fraction. osc_x is the level x of the left {3}
; edge of his sprite; osc_y the line under his feet: the {3}
; line of the surface he stands on. {3-3}
; line of the surface he stands on. Up and Fire together {4}
; turn him into a bat (bat.asm), Down and Fire back into the {4}
; vampire, in a puff of smoke; osc_form says which he is. {4}

;{3}
; The numbers of the moves: to change the feel of the game.
WALK_MAX      = $0180           ; 1.5 pixels a frame
WALK_ACCEL    = $0010           ; speeding up
WALK_SKID     = $0028           ; turning round
WALK_FRICTION = $0018           ; slowing down, let go
JUMP_SPEED    = $0378           ; 3.47 pixels a frame up;
                                ; held: 46.4 pixels up, so
                                ; 2 metatiles, never 3
GRAVITY_HOLD  = $0020           ; going up with Up held
GRAVITY       = $0050           ; going up let go; falling
FALL_MAX      = $0400           ; 4 pixels a frame at most
STEP          = 4               ; up or down while walking
CEILING       = 8               ; feet never higher
SENSOR_X      = 12              ; the column under his feet
X_MAX         = LEVEL_WIDTH * 16 - 24
PUFF_FRAMES   = 12              ; the smoke: 3 pictures x 4 {4}
        .cerror PUFF_FRAMES != 12, "3 pictures, 4 frames" ; {4}

; His body, for the solid blocks: from BODY_LEFT to
; BODY_RIGHT across his sprite, from his feet up
; body_heights lines (the vampire's). {3-3}
; body_heights lines (the vampire's, the bat's). {4}
BODY_LEFT     = 6
BODY_RIGHT    = 17
;{}

; His pictures: 0-5 facing right, 6-11 facing left. {3-3}
; His pictures: 0-5 facing right, 6-11 facing left. Then the {4}
; bat's (bat.asm) and the smoke's, 22-24. {4}
; His first picture: standing, facing right. {-2}
STAND         = 0
WALK_A        = 1 ; {3}
WALK_B        = 2 ; {3}
WALK_C        = 3 ; {3}
JUMP          = 4 ; {3}
FALL          = 5 ; {3}
PUFF          = 22 ; {4}

;{3}
; The kinds of move, for speed_step: Oscar walking. {3-3}
; The kinds of move, for speed_step: Oscar walking, the bat {4}
; flying across. {4}
WALK          = 0
FLY_ACROSS    = 1 ; {4}

; One frame of Oscar: the moves of the vampire. {3-3}
; One frame of Oscar. In the smoke he waits. The keys of a {4}
; change (change_keys: Up and Fire for the vampire, Down {4}
; and Fire for the bat), pushed together now and not in the {4}
; frame before: he changes, the vampire only with a step of {4}
; energy at least, the bat only with room for the vampire {4}
; (no_room). Else the moves of the vampire or of the {4-6}
; bat. {4-6}
; (no_room). Else the moves of the vampire (with the staff, {7}
; Fire pushed alone: a blow, BLOW_FRAMES frames; Fire and {7}
; then Up: the change, the blow cut short) or of the bat. {7}
move_oscar:
        lda stun                ; thrown back by an enemy: {6}
        beq +                   ; no joystick {6}
        dec stun ; {6}
        lda #0 ; {6}
        sta joy ; {6}
+       lda blow                ; the blow goes on {7}
        beq + ; {7}
        dec blow ; {7}
;|        lda osc_puff ; {4-5}
+       lda osc_puff ; {6}
        beq _change ; {4}
        dec osc_puff            ; in the smoke {4}
        jmp oscar_done ; {4}
_change: ; {4}
        ldx osc_form ; {4}
        lda joy ; {4}
        and change_keys,x ; {4}
        cmp change_keys,x ; {4}
        bne _form ; {4}
        lda prev_joy ; {4}
        and change_keys,x ; {4}
        cmp change_keys,x ; {4}
        beq _form               ; held from before {4}
        txa ; {4}
        beq _vampire ; {4}
        jsr no_room             ; the bat: room to change? {4}
        bcs _form               ; no: nothing happens {4}
        bcc _turn ; {4}
_vampire: ; {4}
        lda energy + 1          ; the vampire: enough? {4}
        cmp #ENERGY_STEP ; {4}
        bcc _form               ; no: nothing happens {4}
_turn: ; {4}
        jsr transform ; {4}
        jmp oscar_done ; {4}
_form: ; {4}
        lda osc_form ; {4}
        bne _bat ; {4}
        lda has_staff           ; the staff, Fire pushed {7}
        beq _move               ; now and not before, no {7}
        lda blow                ; blow going on: a blow {7}
        bne _move ; {7}
        lda joy ; {7}
        and #JOY_FIRE ; {7}
        beq _move ; {7}
        lda prev_joy ; {7}
        and #JOY_FIRE ; {7}
        bne _move ; {7}
        lda #BLOW_FRAMES ; {7}
        sta blow ; {7}
        lda #FX_BLOW            ; its sound {13}
        jsr sfx_start ; {13}
_move:
        jmp move_vampire
_bat: ; {4}
        jmp move_bat ; {4}

;{4}
change_keys:
        .byte JOY_UP | JOY_FIRE         ; the vampire
        .byte JOY_DOWN | JOY_FIRE       ; the bat

; Vampire to bat or bat to vampire, where he is, at rest: a
; puff of smoke for PUFF_FRAMES frames, still. The bat
; starts gliding.
transform:
        lda #FX_CHANGE          ; its sound {13}
        jsr sfx_start ; {13}
        lda osc_form
        eor #1
        sta osc_form
        lda #0                  ; no blow {7}
        sta blow ; {7}
        lda #PUFF_FRAMES
        sta osc_puff
        lda #BEAT_FRAMES
        sta osc_flap
        lda #0
        sta osc_vx
        sta osc_vx + 1
        sta osc_vy
        sta osc_vy + 1
        sta osc_gnam
        rts
;{}

; The vampire: walk, then jump, fall or stand.
move_vampire:
        jsr push_across
        ldy #WALK
        jsr speed_step
        jsr move_x
        lda osc_ground
        beq _air

; Standing. Up, pushed now and not in the frame before: the {-6}
; jump. Else a surface within STEP lines: he follows it, up {-6}
; or down; none: he has walked off, and falls. {-6}
; Standing. Up, pushed now and not in the frame before, {7}
; not in a blow: the jump. Else a surface within STEP lines: {7}
; he follows it, up or down; none: he has walked off, and {7}
; falls. {7}
        lda blow ; {7}
        bne _probe ; {7}
        lda joy
        and #JOY_UP
        beq _probe
        lda prev_joy
        and #JOY_UP
        bne _probe              ; held from before
        lda #<($10000 - JUMP_SPEED)
        sta osc_vy
        lda #>($10000 - JUMP_SPEED)
        sta osc_vy + 1
        lda #FX_JUMP            ; its sound {13}
        jsr sfx_start ; {13}
        lda #0
        sta osc_ground
        beq _air
_probe:
        lda old_feet
        sec
        sbc #STEP
        sta probe_top
        lda old_feet
        clc
        adc #STEP
        sta probe_low
        jsr find_surface
        bcc _off
        sta osc_y + 1           ; on the surface
        lda #0
        sta osc_y
        jmp oscar_done
_off:
        lda #0
        sta osc_ground
        sta osc_vy
        sta osc_vy + 1

; In the air: gravity, lighter while he goes up with Up
; held (a higher jump); then y = y + vy.
_air:
        ldx #<GRAVITY
        ldy #>GRAVITY
        lda osc_vy + 1
        bpl +                   ; not going up
        lda joy
        and #JOY_UP
        beq +                   ; Up let go
        ldx #<GRAVITY_HOLD
        ldy #>GRAVITY_HOLD
+       txa
        clc
        adc osc_vy
        sta osc_vy
        tya
        adc osc_vy + 1
        sta osc_vy + 1
        bmi _move_y             ; going up
        lda #<FALL_MAX          ; no faster than FALL_MAX
        cmp osc_vy
        lda #>FALL_MAX
        sbc osc_vy + 1
        bcs _move_y
        lda #<FALL_MAX
        sta osc_vy
        lda #>FALL_MAX
        sta osc_vy + 1
_move_y:
        clc
        lda osc_y
        adc osc_vy
        sta osc_y
        lda osc_y + 1
        adc osc_vy + 1
        sta osc_y + 1
        lda osc_vy + 1
        bpl _falling

; Going up: he passes through every surface (they hold him
; only from above); his feet stop at CEILING, his head under
; a solid block (bump_head).
        lda osc_y + 1
        cmp #CEILING
        bcs _head
        lda #CEILING
        sta osc_y + 1
        lda #0
        sta osc_y
        sta osc_vy
        sta osc_vy + 1
        beq oscar_done
_head:
        jsr bump_head
        jmp oscar_done

; Falling: a surface between his feet before and after the
; move stops him there.
_falling:
        jsr land
        jmp oscar_done

; The end of every frame of Oscar: feet at the bottom of
; the playfield, he has fallen (objects.asm); and the {3-3}
; joystick is kept for the next frame. {3-3}
; the playfield, he has fallen (objects.asm); on a surface {4}
; the energy of the flight comes back, slowly; and the {4}
; joystick is kept for the next frame. {4}
oscar_done:
        lda osc_y + 1
        cmp #BOTTOM
        bcc +
        jsr fallen
+       lda osc_ground ; {4}
        beq + ; {4}
        jsr charge_energy ; {4}
+       lda joy
        sta prev_joy
        rts

; Going down: a surface between his feet before the move
; (old_feet) and after it stops him there, on the ground.
land:
        lda old_feet
        sta probe_top
        lda osc_y + 1
        sta probe_low
        jsr find_surface
        bcc +
        sta osc_y + 1
        lda #0
        sta osc_y
        sta osc_vy
        sta osc_vy + 1
        lda #1
        sta osc_ground
+       rts

; Where the joystick pushes across, in push: 1 right, $ff
; left, 0 neither (right first); he looks that way. {-6}
; left, 0 neither (right first); he looks that way. In a {7}
; blow, standing, the vampire stays still: 0. {7}
push_across:
        lda blow ; {7}
        beq + ; {7}
        lda osc_ground ; {7}
        beq + ; {7}
        lda osc_form ; {7}
        bne + ; {7}
        lda #0 ; {7}
        beq _none ; {7}
;|        lda joy ; {3-6}
+       lda joy ; {7}
        and #JOY_RIGHT
        beq +
        ldx #RIGHT
        lda #1                  ; right
        bne _look
+       lda joy
        and #JOY_LEFT
        beq _none
        ldx #LEFT
        lda #$ff                ; left
_look:
        stx osc_face
_none:
        sta push
        rts

; One frame of the speed across, osc_vx, for a kind of move
; (Y: WALK). Let go (push 0): it slows down to 0. Pushed {3-3}
; the way it goes, or from still: faster, up to the top {3-3}
; speed; against it: it turns. {3-3}
; (Y: WALK or FLY_ACROSS). Let go (push 0): it slows down {4}
; to 0. Pushed the way it goes, or from still: faster, up {4}
; to the top speed; against it: it turns. {4}
speed_step:
        lda push
        bmi _minus
        bne _plus
        lda osc_vx + 1          ; let go
        bmi _slow_minus
        ora osc_vx
        beq _end                ; still
        sec                     ; going right
        lda osc_vx
        sbc move_slow_lo,y
        sta osc_vx
        lda osc_vx + 1
        sbc move_slow_hi,y
        sta osc_vx + 1
        bpl _end
        bmi _stop               ; past 0: stop
_slow_minus:
        clc                     ; going left
        lda osc_vx
        adc move_slow_lo,y
        sta osc_vx
        lda osc_vx + 1
        adc move_slow_hi,y
        sta osc_vx + 1
        bmi _end
_stop:
        lda #0
        sta osc_vx
        sta osc_vx + 1
_end:
        rts
_plus:
        lda osc_vx + 1          ; pushed right
        bmi _turn_plus          ; going left: turning
        lda move_accel_lo,y
        sta delta
        lda move_accel_hi,y
        jmp _add
_turn_plus:
        lda move_turn_lo,y
        sta delta
        lda move_turn_hi,y
_add:
        sta delta + 1           ; vx = vx + delta
        clc
        lda osc_vx
        adc delta
        sta osc_vx
        lda osc_vx + 1
        adc delta + 1
        sta osc_vx + 1
        bmi _end                ; still going left
        lda move_max_lo,y       ; no faster than the top
        cmp osc_vx
        lda move_max_hi,y
        sbc osc_vx + 1
        bcs _end
        lda move_max_lo,y
        sta osc_vx
        lda move_max_hi,y
        sta osc_vx + 1
        rts
_minus:
        lda osc_vx + 1          ; pushed left
        bmi _accel_minus        ; going left already
        ora osc_vx
        beq _accel_minus        ; still
        lda move_turn_lo,y      ; going right: turning
        sta delta
        lda move_turn_hi,y
        jmp _sub
_accel_minus:
        lda move_accel_lo,y
        sta delta
        lda move_accel_hi,y
_sub:
        sta delta + 1           ; vx = vx - delta
        sec
        lda osc_vx
        sbc delta
        sta osc_vx
        lda osc_vx + 1
        sbc delta + 1
        sta osc_vx + 1
        bpl _end                ; still going right
        lda osc_vx              ; no faster than the top:
        cmp move_min_lo,y       ; not under -top
        lda osc_vx + 1
        sbc move_min_hi,y
        bcs _end
        lda move_min_lo,y
        sta osc_vx
        lda move_min_hi,y
        sta osc_vx + 1
        rts

; For each kind of move: speeding up, turning, slowing down
; let go, the top speed and its negative: the walk's, {3-3}
; let go, the top speed and its negative: the walk's, then {4}
; the bat's. {4}
move_accel_lo:  .byte <WALK_ACCEL
                .byte <FLY_ACCEL ; {4}
move_accel_hi:  .byte >WALK_ACCEL
                .byte >FLY_ACCEL ; {4}
move_turn_lo:   .byte <WALK_SKID
                .byte <FLY_TURN ; {4}
move_turn_hi:   .byte >WALK_SKID
                .byte >FLY_TURN ; {4}
move_slow_lo:   .byte <WALK_FRICTION
                .byte <FLY_DRAG ; {4}
move_slow_hi:   .byte >WALK_FRICTION
                .byte >FLY_DRAG ; {4}
move_max_lo:    .byte <WALK_MAX
                .byte <FLY_MAX_X ; {4}
move_max_hi:    .byte >WALK_MAX
                .byte >FLY_MAX_X ; {4}
move_min_lo:    .byte <-WALK_MAX
                .byte <-FLY_MAX_X ; {4}
move_min_hi:    .byte >-WALK_MAX
                .byte >-FLY_MAX_X ; {4}

; x = x + vx: 24 bits, vx with its sign. Not past the ends
; of the level, 0 and X_MAX: there the speed is 0. Not into
; a solid block (push_out). Then the column under his feet
; (sensor), and his feet before the move up or down
; (old_feet).
move_x:
        ldx #0                  ; X: sign of vx, 0 or $ff
        lda osc_vx + 1
        bpl +
        dex
+       clc
        lda osc_x
        adc osc_vx
        sta osc_x
        lda osc_x + 1
        adc osc_vx + 1
        sta osc_x + 1
        txa
        adc osc_x + 2
        sta osc_x + 2
        bpl _max                ; not under 0
        lda #0
        sta osc_x + 1
        sta osc_x + 2
        beq _end_stop
_max:
        lda #<X_MAX             ; past X_MAX?
        cmp osc_x + 1
        lda #>X_MAX
        sbc osc_x + 2
        bcs _sensor
        lda #<X_MAX
        sta osc_x + 1
        lda #>X_MAX
        sta osc_x + 2
_end_stop:
        lda #0
        sta osc_x
        sta osc_vx
        sta osc_vx + 1
_sensor:
        jsr push_out
        clc
        lda osc_x + 1
        adc #SENSOR_X
        sta sensor
        lda osc_x + 2
        adc #0
        sta sensor + 1
        lda osc_y + 1
        sta old_feet
        rts

; His body in a solid block: out of it. The rows of his
; body, from his feet up `height` lines; a solid metatile in
; one of them, in the column of his right edge, pushes him
; left, just out of that column; else one in the column of
; his left edge pushes him right. Pushed, he stops.
push_out:
        lda #SOLID
        sta flag_mask
        ldx osc_form ; {4}
        lda body_heights,x ; {4}
;|        lda body_heights ; {3-3}
        sta height
        lda osc_y + 1           ; the first row: feet -
        sec                     ; height (0 at most)
        sbc height
        bcs +
        lda #0
+       lsr a
        lsr a
        lsr a
        lsr a
        sta probe_row
        ldx osc_y + 1           ; the last: feet - 1
        dex
        txa
        lsr a
        lsr a
        lsr a
        lsr a
        sta row_last
        clc                     ; his right edge
        lda osc_x + 1
        adc #BODY_RIGHT
        sta edge
        lda osc_x + 2
        adc #0
        sta edge + 1
        jsr flag_column
        bcc _left
        lda edge                ; x = its column * 16
        and #%11110000          ; - BODY_RIGHT - 1
        sec
        sbc #BODY_RIGHT + 1
        sta osc_x + 1
        lda edge + 1
        sbc #0
        sta osc_x + 2
        jmp _stop
_left:
        clc                     ; his left edge
        lda osc_x + 1
        adc #BODY_LEFT
        sta edge
        lda osc_x + 2
        adc #0
        sta edge + 1
        jsr flag_column
        bcc _free
        lda edge                ; x = (its column + 1) *
        ora #%00001111          ; 16 - BODY_LEFT
        sec
        sbc #BODY_LEFT - 1
        sta osc_x + 1
        lda edge + 1
        sbc #0
        sta osc_x + 2
_stop:
        lda #0
        sta osc_x
        sta osc_vx
        sta osc_vx + 1
_free:
        rts

;|body_heights:   .byte 20        ; the vampire {3-3}
body_heights:   .byte 20        ; the vampire, the bat {4}
                .byte 12 ; {4}

; The rows of a body A lines high, from his feet up (feet - {4}
; A to feet - 1), in probe_row and row_last; flag_mask: {4}
; SOLID. {4}
body_rows: ; {4}
        sta work ; {4}
        lda osc_y + 1 ; {4}
        sec ; {4}
        sbc work ; {4}
        bcs + ; {4}
        lda #0                  ; above the playfield: row 0 {4}
+       lsr a ; {4}
        lsr a ; {4}
        lsr a ; {4}
        lsr a ; {4}
        sta probe_row ; {4}
        ldx osc_y + 1 ; {4}
        dex ; {4}
        txa ; {4}
        lsr a ; {4}
        lsr a ; {4}
        lsr a ; {4}
        lsr a ; {4}
        sta row_last ; {4}
        lda #SOLID ; {4}
        sta flag_mask ; {4}
        rts ; {4}

; A metatile with flag_mask in those rows, in the column of
; his right edge (carry set, X 0), else of his left edge
; (carry set, X 1); none: carry clear.
edges_flag:
        clc
        lda osc_x + 1
        adc #BODY_RIGHT
        sta edge
        lda osc_x + 2
        adc #0
        sta edge + 1
        jsr flag_column
        ldx #0
        bcs +
        clc
        lda osc_x + 1
        adc #BODY_LEFT
        sta edge
        lda osc_x + 2
        adc #0
        sta edge + 1
        jsr flag_column
        ldx #1
+       rts

; The bat turning back: the vampire's body (his feet up 20 {4}
; lines) in a solid block, in the column of one of his {4}
; edges? Then there is no room: carry set. {4}
no_room: ; {4}
        lda body_heights        ; the vampire's {4}
        jsr body_rows ; {4}
        jmp edges_flag ; {4}

; Going up: his head (feet - height) in a solid metatile, in
; the column of one of his edges: he stops just under it.
bump_head:
        lda osc_y + 1
        sec
        sbc height
        bcc _none               ; above the playfield
        lsr a
        lsr a
        lsr a
        lsr a
        sta probe_row
        sta row_last
        lda #SOLID
        sta flag_mask
        jsr edges_flag
        bcc _none
        lda probe_row           ; feet: (row + 1) * 16 +
        adc #0                  ; height (carry set: + 1)
        asl a
        asl a
        asl a
        asl a
        adc height
        sta osc_y + 1
        lda #0
        sta osc_y
        sta osc_vy
        sta osc_vy + 1
_none:
        rts

; A metatile with flag_mask (SOLID) in the column of level {3-6}
; x `edge`, in rows probe_row to row_last: carry set. {3-6}
; A metatile with flag_mask (SOLID, HAZARD) in the column of {7}
; level x `edge`, in rows probe_row to row_last: carry set. {7}
flag_column:
        lda edge + 1
        sta work
        lda edge
        lsr work
        ror a
        lsr work
        ror a
        lsr work
        ror a
        lsr work
        ror a
        tax
        lda level_lo,x
        sta probe_col
        lda level_hi,x
        sta probe_col + 1
        ldy probe_row
-       lda (probe_col),y
        tax
        lda metaflags,x
        and flag_mask
        bne _yes
        cpy row_last
        iny
        bcc -
        clc                     ; none
        rts
_yes:
        sec
        rts

; The highest surface in column `sensor` of the level from
; line probe_top to line probe_low, in the metatile rows of
; those two lines. Found: carry set, its line in A. None:
; carry clear.
find_surface:
        jsr sensor_column
        lda sensor              ; pixel column in it, 0-15:
        and #%00001111          ; its table of profiles
        tax
        lda profile_lo,x
        sta probe_prof
        lda profile_hi,x
        sta probe_prof + 1
        lda probe_low
        lsr a
        lsr a
        lsr a
        lsr a
        sta probe_last          ; the last metatile row
        lda probe_top
        lsr a
        lsr a
        lsr a
        lsr a
        sta probe_row           ; the first
_row:
        ldy probe_row
        cpy #11                 ; under the level: none
        bcs _none
        lda (probe_col),y       ; the metatile
        tax
        ldy metashape,x         ; its profile
        beq _next               ; 0: no surface in it
        lda (probe_prof),y      ; its line in this column
        cmp #$ff
        beq _next               ; none in this column
        sta work
        lda probe_row           ; the line on the playfield:
        asl a                   ; row * 16 + line
        asl a
        asl a
        asl a
        ora work
        cmp probe_top
        bcc _next               ; above the range
        cmp probe_low
        beq _found
        bcs _next               ; under it
_found:
        sec
        rts
_next:
        lda probe_row
        cmp probe_last
        bcs _none
        inc probe_row
        bne _row
_none:
        clc
        rts

; The metatile column of `sensor` (sensor / 16), in X; where
; it is kept, in probe_col.
sensor_column:
        lda sensor + 1
        sta work
        lda sensor
        lsr work
        ror a
        lsr work
        ror a
        lsr work
        ror a
        lsr work
        ror a
        tax
        lda level_lo,x
        sta probe_col
        lda level_hi,x
        sta probe_col + 1
        rts

; The picture: in the air, up or down; standing still; or a {3-3}
; step of the walk, one every 8 pixels walked. {3-3}
; The picture: in the smoke, one of its three, 4 frames {4}
; each. The vampire: in the air, up or down; standing still; {4}
; or a step of the walk, one every 8 pixels walked. The bat: {4}
; animate_bat (bat.asm). {4}
animate_oscar:
        lda osc_puff ; {4}
        beq _form ; {4}
        lda #PUFF_FRAMES        ; frames of smoke gone by, {4}
        sec                     ; / 4 {4}
        sbc osc_puff ; {4}
        lsr a ; {4}
        lsr a ; {4}
        clc ; {4}
        adc #PUFF ; {4}
        sta osc_pic ; {4}
        rts ; {4}
_form: ; {4}
        lda osc_form ; {4}
        beq + ; {4}
        jmp animate_bat ; {4}
;|        lda osc_ground ; {3-3}
+       lda osc_ground ; {4}
        bne _ground
        ldx #JUMP
        lda osc_vy + 1
        bmi _set
        ldx #FALL
        bne _set
_ground:
        ldx #STAND
        lda osc_vx
        ora osc_vx + 1
        beq _set
        lda osc_vx + 1          ; anim = anim + |vx|
        bmi _back
        clc
        lda osc_anim
        adc osc_vx
        sta osc_anim
        lda osc_anim + 1
        adc osc_vx + 1
        sta osc_anim + 1
        jmp _step
_back:
        sec                     ; going left: anim - vx
        lda osc_anim
        sbc osc_vx
        sta osc_anim
        lda osc_anim + 1
        sbc osc_vx + 1
        sta osc_anim + 1
_step:
        lda osc_anim + 1        ; pixels / 8, 0-3
        lsr a
        lsr a
        lsr a
        and #%00000011
        tax
        lda walk_cycle,x
        tax
_set:
        txa
        ldy osc_face
        beq +
        clc
        adc #6                  ; facing left
+       sta osc_pic
        rts

walk_cycle:
        .byte WALK_A, WALK_B, WALK_C, WALK_B
;{}

; The two sprites: X = level x - camera + 31, with the ninth
; bit in $d010 (the other sprites' kept); Y = feet + 29; the
; picture's two blocks, in the pointers of both screens; on. {-5}
; picture's two blocks, in the pointers of both screens. On, {6}
; or, blinking after a hit (enemies.asm), off. {6}
place_oscar:
        sec
        lda osc_x + 1
        sbc camera
        tax
        lda osc_x + 2
        sbc camera + 1
        tay
        txa
        clc
        adc #31
        sta $d000               ; X of sprite 0
        sta $d002               ; X of sprite 1
        tya
        adc #0                  ; the ninth bit: 0 or 1
        beq +
        lda #%00000011          ; for sprites 0 and 1
+       sta work
        lda $d010
        and #%11111100
        ora work
        sta $d010
        lda osc_y + 1
        clc
        adc #29
        sta $d001               ; Y of sprite 0
        sta $d003               ; Y of sprite 1
        lda osc_pic
        asl a                   ; two blocks a picture
        adc #OSCAR_LINES
        sta SCREEN_A + POINTERS
        sta SCREEN_B + POINTERS
        adc #1                  ; the colours
        sta SCREEN_A + POINTERS + 1
        sta SCREEN_B + POINTERS + 1
        lda protect             ; after a hit he blinks: off {6}
        and #%00000100          ; 4 frames of every 8 {6}
        beq + ; {6}
        lda $d015 ; {6}
        and #%11111100 ; {6}
        sta $d015 ; {6}
        rts ; {6}
;|        lda $d015 ; {-5}
+       lda $d015 ; {6}
        ora #%00000011
        sta $d015
        rts
