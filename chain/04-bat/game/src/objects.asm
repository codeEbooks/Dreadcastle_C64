; The falls: Oscar out of the playfield at the bottom, the
; transition takes him back to the start; the HUD's bars.

HEALTH_FULL   = 8               ; 4 characters of the bar
TRANS_FRAMES  = 50              ; a transition: frames
BLANK_AT      = 14              ; the screen off, then on
SHOW_AT       = 1

; Oscar has fallen out of the playfield: no health left.
; The sprites go off, and the transition takes him back.
fallen:
        lda #0
        sta health
        sta $d015
        lda #GO_BACK

; A transition of kind A begins: TRANS_FRAMES frames.
start_transition:
        sta trans_kind
        lda #TRANS_FRAMES
        sta trans
        rts

; The HUD, in both screens: the bars of the health and of
; the energy.
show_hud:
        lda health
        ldx #4
        ldy #HEALTH_BAR - HUD_ROW
        jsr show_bar
        lda energy + 1          ; whole steps, 0-6
        lsr a
        lsr a
        lsr a
        lsr a
        lsr a
        ldx #3
        ldy #ENERGY_BAR - HUD_ROW
        jsr show_bar
        rts

; A bar of X characters from cell Y of row 23: A steps, two
; a character (BAR_EMPTY + 0, 1 or 2).
show_bar:
        sta work
-       lda work                ; this character's: 0-2
        cmp #3
        bcc +
        lda #2
+       clc
        adc #BAR_EMPTY
        sta SCREEN_A + HUD_ROW,y
        sta SCREEN_B + HUD_ROW,y
        lda work                ; two fewer for the next
        sec
        sbc #2
        bcs +
        lda #0
+       sta work
        iny
        dex
        bne -
        rts

; A frame of a transition: trans counts the frames down,
; and trans_steps gives the step of each frame. The picture
; stays still at first (Oscar gone after a fall). At
; BLANK_AT the screen goes off; Oscar at respawn_x; screen
; A drawn again in four frames, ten columns each, with the
; colour RAM; the HUD. At SHOW_AT the screen comes back on,
; with the sprites and the level's name.
transition:
        dec trans
        ldx trans
        lda trans_steps,x
        tax
        lda trans_low,x
        sta vector
        lda trans_high,x
        sta vector + 1
        jmp (vector)

; The step of each frame, from trans 0 up: 0 none, 1 on,
; 3-6 the drawing, 7 Oscar again, 10 the screen off; 2, 8
; and 9 do nothing yet.
trans_steps:
        .byte 0, 1, 2, 2, 2, 6, 5, 4, 3, 7     ; 0-9
        .byte 2, 2, 2, 2, 10                   ; 10-14
        .byte 0, 0, 0, 0, 0, 0, 0, 0, 0        ; 15-23
        .byte 0, 0, 0, 0, 0, 0, 0, 0, 0        ; 24-32
        .byte 2, 2, 2, 2, 2, 2, 2, 2, 2        ; 33-41
        .byte 9, 2, 2, 2, 2, 2, 2, 8           ; 42-49
        .cerror * - trans_steps != TRANS_FRAMES, "each"
trans_low:
        .byte <trans_none, <trans_on, <trans_none
        .byte <trans_draw_0, <trans_draw_1
        .byte <trans_draw_2, <trans_draw_3
        .byte <trans_second, <trans_none, <trans_none
        .byte <trans_off
trans_high:
        .byte >trans_none, >trans_on, >trans_none
        .byte >trans_draw_0, >trans_draw_1
        .byte >trans_draw_2, >trans_draw_3
        .byte >trans_second, >trans_none, >trans_none
        .byte >trans_off

trans_none:
        rts
; The screen off (bit 7 read: the raster line; written:
; line 256 +) and the sprites.
trans_off:
        lda $d011
        and #%01101111
        sta $d011
        lda #0
        sta $d015
        rts
; Oscar at the start again.
trans_second:
_respawn:
        jsr respawn
        jmp show_hud
trans_draw_0:
        lda #0
        ldx #10
        bne trans_draw
trans_draw_1:
        lda #10
        ldx #20
        bne trans_draw
trans_draw_2:
        lda #20
        ldx #30
        bne trans_draw
trans_draw_3:
        lda #30
        ldx #39
trans_draw:
        sta col_screen
        stx col_end
        jmp draw_columns
trans_on:                       ; the lightest step:
        jsr show_name           ; the level's name
        jsr place_oscar
_on:
        lda $d015               ; Oscar's sprites on
        ora #%00000011
        sta $d015
screen_on:
        lda $d011               ; the screen on
        and #%01111111
        ora #%00010000
        sta $d011
        rts
