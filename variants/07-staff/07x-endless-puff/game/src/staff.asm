; The Count's staff: it lies in level 3, on the
; path; Oscar takes it walking over it (touch_staff), and
; from then on holds it (has_staff) and Fire strikes with
; it (move_oscar starts a blow, hit_enemies: strike). It is
; sprite 2, multicolour, behind Oscar's two sprites, its
; pictures at STAFF_SPRITES (staff.py).

STAFF_TOUCH   = 12              ; Oscar's middle to its own

; His middle (sensor) within STAFF_TOUCH pixels of the
; middle of the staff (its sprite's x + 12), his feet on
; its line or lower and his head above it: he takes it.
touch_staff:
        lda has_staff
        bne _no
        lda staff_line
        beq _no                 ; none in this level
        sec                     ; sensor - x - 12
        lda sensor
        sbc staff_x_lo
        sta edge
        lda sensor + 1
        sbc staff_x_hi
        sta edge + 1
        lda edge
        sec
        sbc #12
        sta edge
        lda edge + 1
        sbc #0
        sta edge + 1
        bpl +                   ; |difference|
        lda edge
        eor #$ff
        clc
        adc #1
        sta edge
        lda edge + 1
        eor #$ff
        adc #0
+       bne _no                 ; 256 or more
        lda edge
        cmp #STAFF_TOUCH
        bcs _no
        lda osc_y + 1           ; his feet on its line or
        cmp staff_line          ; lower
        bcc _no
        sec                     ; his head above it
        sbc height
        bcc _take               ; above the playfield
        cmp staff_line
        bcs _no
_take:
        lda #1
        sta has_staff
_no:
        rts

; Sprite 2. Held: only the vampire's, out of the smoke,
; blinking with him; X = his X + dx, Y = his Y + dy, from
; his picture (held_dx, held_dy, held_block) or, in a blow,
; from its frames left (blow_dx...: 10 a facing). Lying in
; the level, not yet his: there, if X is 0-343. Else off.
place_staff:
        lda $d010
        and #%11111011
        sta $d010
        lda has_staff
        bne +
        jmp _lying
+       lda osc_form
        ora osc_puff
        beq +
        jmp _off
+       lda blow
        beq _held
        tax                     ; the blow: X = frames - 1
        dex                     ; + 10 facing left
        lda osc_face
        beq +
        txa
        clc
        adc #BLOW_FRAMES
        tax
+       lda blow_dx,x
        sta work
        lda blow_dy,x
        sta en_dx
        lda blow_block,x
        jmp _place
_held:
        ldx osc_pic
        lda held_dx,x
        sta work
        lda held_dy,x
        sta en_dx
        lda held_block,x
_place:
        sta SCREEN_A + POINTERS + 2
        sta SCREEN_B + POINTERS + 2
        sec                     ; his X register:
        lda osc_x + 1           ; x - camera + 31
        sbc camera
        sta edge
        lda osc_x + 2
        sbc camera + 1
        sta edge + 1
        clc
        lda edge
        adc #31
        sta edge
        lda edge + 1
        adc #0
        sta edge + 1
        ldy #0                  ; + dx, signed
        lda work
        bpl +
        dey
+       clc
        adc edge
        sta $d004               ; X of sprite 2
        tya
        adc edge + 1
        and #1                  ; the ninth bit
        beq +
        lda $d010
        ora #%00000100
        sta $d010
+       lda osc_y + 1           ; Y = feet + 29 + dy
        clc
        adc #29
        clc
        adc en_dx
        sta $d005
        lda protect             ; blinking with him
        and #%00000100
        bne _off
_on:
        lda $d015
        ora #%00000100
        sta $d015
        rts
_off:
        lda $d015
        and #%11111011
        sta $d015
        rts
_lying:
        lda staff_line
        beq _off                ; none in this level
        sec                     ; X = x - camera + 31
        lda staff_x_lo
        sbc camera
        sta edge
        lda staff_x_hi
        sbc camera + 1
        sta edge + 1
        clc
        lda edge
        adc #31
        sta edge
        lda edge + 1
        adc #0
        bmi _off                ; left of the screen
        beq +                   ; 0-255
        cmp #1
        bne _off
        lda edge                ; 256-343
        cmp #344 - 256
        bcs _off
        lda $d010
        ora #%00000100
        sta $d010
+       lda edge
        sta $d004
        lda staff_line          ; Y = its line + 29
        clc
        adc #29
        sta $d005
        lda #STAFF_BLOCKS + STAFF_LYING
        sta SCREEN_A + POINTERS + 2
        sta SCREEN_B + POINTERS + 2
        jmp _on
