; Oscar's sprites on the screen: his place and his
; picture.

; His first picture: standing, facing right.
STAND         = 0

; The two sprites: X = level x - camera + 31, with the ninth
; bit in $d010 (the other sprites' kept); Y = feet + 29; the
; picture's two blocks, in the pointers of both screens; on.
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
        lda $d015
        ora #%00000011
        sta $d015
        rts
