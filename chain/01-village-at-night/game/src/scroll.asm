; The camera and the scroll register.
;
; camera is the level x at the left edge of the playfield.
; Its low 3 bits are the fine part: the playfield scroll is
; 7 minus them. camera / 8 is the level column in screen

; At the start: no frames counted.
; (The camera and the screens: respawn.)
init_scroll:
        lda #0
        sta frame_count
        sta hud_flag
        rts

; The scroll register of the playfield: multicolour, and
; 7 - (camera AND 7), which is (camera AND 7) EOR 7.
set_xscroll:
        lda camera
        and #%00000111
        eor #%00010111          ; bit 4: multicolour
        sta xscroll
        rts
