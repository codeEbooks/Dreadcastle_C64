; The level as a game: the heirlooms to take, the lantern
; of the checkpoint, the gate that opens with all three; the
; health, the night until dawn, the HUD; and the moments
; between: after a fall, Oscar back at the lantern (or at
; the start); through the gate the next level; at dawn,
; level 1 again.
; Where the heirlooms, the lantern and the gate are: the
; level's objects (OBJECTS, memory.asm).

HEALTH_FULL   = 8               ; 4 characters of the bar
NIGHT_STEPS   = 16              ; 8 characters of the bar
NIGHT_STEP    = 188             ; frames: 3.76 s, 1 minute
HEIRLOOM_BOX  = 16              ; the box of an heirloom
TOUCH         = 12              ; Oscar's middle to its own
TRANS_FRAMES  = 50              ; a transition: frames
BLANK_AT      = 14              ; the screen off, then on
SHOW_AT       = 1
        .cerror NIGHT_STEPS != 16, "8 characters, 2 steps"
STEP_LEVELS   = 2               ; the levels of this step

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

; What Oscar touches: the heirlooms, the lantern, the
; gate.
touch_things:
        jsr open_door
        jsr touch_heirlooms
        jsr touch_lantern
        jmp touch_gate

; His middle (sensor) within TOUCH pixels of the middle of
; an heirloom's box, and his body (feet up `height` lines)
; across the box's lines: he takes it. The HUD counts it;
; the third opens the gate.
touch_heirlooms:
        ldx #HEIRLOOM_COUNT - 1
_one:
        lda got_bits
        and heirloom_bit,x
        bne _next               ; taken already
        sec                     ; sensor - the middle of
        lda sensor              ; the box: x + 4 + 8
        sbc heirloom_x_lo,x
        sta edge
        lda sensor + 1
        sbc heirloom_x_hi,x
        sta edge + 1
        lda edge
        sec
        sbc #12
        sta edge
        lda edge + 1
        sbc #0
        sta edge + 1
        bpl +                   ; |difference| < TOUCH?
        lda edge
        eor #$ff
        clc
        adc #1
        sta edge
        lda edge + 1
        eor #$ff
        adc #0
+       bne _next               ; 256 or more
        lda edge
        cmp #TOUCH
        bcs _next
        lda heirloom_top,x      ; feet below the top of
        cmp osc_y + 1           ; the box?
        bcs _next
        adc #HEIRLOOM_BOX       ; head above its bottom:
        sta work                ; feet - height < top + 16
        lda osc_y + 1
        sec
        sbc height
        bcc _take               ; above the level
        cmp work
        bcs _next
_take:
        lda got_bits
        ora heirloom_bit,x
        sta got_bits
        inc got
        lda got
        cmp #HEIRLOOM_COUNT
        bne _next
        txa
        pha
        jsr open_gate
        pla
        tax
_next:
        dex
        bpl _one
        rts

heirloom_bit:   .byte 1, 2, 4

; The lantern: touched (Oscar's middle in its column, his
; feet on its head's top or lower), it lights up, and from
; now on Oscar comes back here.
touch_lantern:
        lda lantern_lit
        bne _done
        lda sensor + 1          ; its column?
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
        cmp lantern_col
        bne _done
        lda osc_y + 1
        cmp lantern_line        ; its row * 16
        bcc _done
        lda #1
        sta lantern_lit
        lda lantern_x
        sta respawn_x
        lda lantern_x + 1
        sta respawn_x + 1
        lda lantern_col
        sta tile_col
        lda lantern_row
        sta tile_row
        lda lantern_tile
        sta new_tile
        jmp set_tile
_done:
        rts

; The gate opens: touch_gate lets him through at once; its
; doors become their open tiles one a frame, from the next
; (open_door), the last first. (All six in one frame take
; too long in a frame with a swap.)
open_gate:
        lda #DOOR_COUNT + 1
        sta door_open
        rts

; A door of the opening gate: door_open counts the doors
; left, plus 1, down to 1 (the gate open).
open_door:
        ldx door_open
        cpx #2
        bcc _done
        dex
        stx door_open
        dex
        lda door_col,x
        sta tile_col
        lda door_row,x
        sta tile_row
        lda door_tile,x
        sta new_tile
        jmp set_tile
_done:
        rts

; Through the open gate (Oscar's middle in its doorway, his
; feet below its top): the level is done, the next one.
touch_gate:
        lda door_open
        beq _done
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
        cmp door_first
        bcc _done               ; left of the doorway
        cmp door_last
        beq +
        bcs _done               ; right of it
+       lda osc_y + 1
        cmp door_line           ; its top * 16 + 1
        bcc _done
        lda #GO_NEXT            ; the next level
        jmp start_transition
_done:
        rts

; The night: a frame less of the step; at its end a step
; less. No steps left: dawn, level 1 again.
tick_night:
        lda night_time
        bne +
        dec night_time + 1
+       dec night_time
        lda night_time
        ora night_time + 1
        bne _done
        lda #<NIGHT_STEP
        sta night_time
        lda #>NIGHT_STEP
        sta night_time + 1
        dec night
        beq _dawn
        rts
_dawn:
        lda #GO_START           ; dawn: level 1 again
        jmp start_transition
_done:
        rts

; The HUD, in both screens: the bars of the health, of the
; energy and of the night, and the heirlooms taken.
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
        lda night
        ldx #8
        ldy #NIGHT_BAR - HUD_ROW
        jsr show_bar
        lda got
        clc
        adc #DIGIT_0
        sta SCREEN_A + HEIRLOOM_DIGIT
        sta SCREEN_B + HEIRLOOM_DIGIT
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

; Sprite 7: the heirloom on the screen, if there is one
; (they are 21 columns apart: never two). X register = its
; x - camera + 31, from 0 to 343; Y register = its top + 50,
; one line lower every other 16 frames of the night.
place_heirloom:
        ldx #HEIRLOOM_COUNT - 1
_one:
        lda got_bits
        and heirloom_bit,x
        bne _next
        sec
        lda heirloom_x_lo,x
        sbc camera
        sta edge
        lda heirloom_x_hi,x
        sbc camera + 1
        sta edge + 1
        clc
        lda edge
        adc #31
        sta edge
        lda edge + 1
        adc #0
        sta edge + 1
        bmi _next               ; left of the screen
        beq _show               ; 0-255
        cmp #1
        bne _next
        lda edge                ; 256-343
        cmp #344 - 256
        bcc _show
_next:
        dex
        bpl _one
        lda $d015               ; none: sprite 7 off
        and #%01111111
        sta $d015
        rts
_show:
        lda edge
        sta $d00e
        lda $d010
        and #%01111111
        ldy edge + 1
        beq +
        ora #%10000000
+       sta $d010
        lda night_time          ; 0 or 16 (a frame of the
        and #%00010000          ; night: one each turn)
        cmp #16                 ; carry: one line lower
        lda heirloom_top,x
        adc #50
        sta $d00f
        lda heirloom_block,x
        sta SCREEN_A + POINTERS + 7
        sta SCREEN_B + POINTERS + 7
        lda $d015
        ora #%10000000
        sta $d015
        rts

; A frame of a transition: trans counts the frames down,
; and trans_steps gives the step of each frame. The picture
; stays still at first (Oscar gone after a fall), and
; meanwhile the data are copied, a page a frame: the next
; level (through the gate), level 1 (at dawn), or the same
; again, from its map (MAP_PAGES frames); if its setting
; is another, the setting's tables (ENV_PAGES frames). At
; BLANK_AT the screen goes off; the setting's characters,
; if another set, SET_PAGES frames; the level's things
; from the start, with its objects; Oscar at respawn_x
; screen A drawn again in four frames, ten columns each,
; with the colour RAM; the HUD. At SHOW_AT the screen comes
; back on, with the sprites, the level's name.
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
; 2 a page, 3-6 the drawing, 7 the level's things and
; Oscar, 8 the level, 9 the setting, 10 the screen off.
trans_steps:
        .byte 0, 1, 2, 2, 2, 6, 5, 4, 3, 7     ; 0-9
        .byte 2, 2, 2, 2, 10                   ; 10-14
        .byte 0, 0, 0, 0, 0, 0, 0, 0, 0        ; 15-23
        .byte 0, 0, 0, 0, 0, 0, 0, 0, 0        ; 24-32
        .byte 2, 2, 2, 2, 2, 2, 2, 2, 2        ; 33-41
        .byte 9, 2, 2, 2, 2, 2, 2, 8           ; 42-49
        .cerror * - trans_steps != TRANS_FRAMES, "each"
trans_low:
        .byte <trans_none, <trans_on, <trans_page
        .byte <trans_draw_0, <trans_draw_1
        .byte <trans_draw_2, <trans_draw_3
        .byte <trans_second, <trans_level, <trans_tables
        .byte <trans_off
trans_high:
        .byte >trans_none, >trans_on, >trans_page
        .byte >trans_draw_0, >trans_draw_1
        .byte >trans_draw_2, >trans_draw_3
        .byte >trans_second, >trans_level, >trans_tables
        .byte >trans_off

trans_none:
        rts
; A page of the data being copied, if any.
trans_page:
        lda up_on
        beq trans_none
        jmp unpack_page
; The level, from its map: through the gate the next one
; at dawn level 1; after a fall nothing (the level as it
; is).
trans_level:
        lda #0
        sta up_on
        lda trans_kind
        cmp #GO_BACK
        beq trans_none
        ldx #0                  ; level 1
        cmp #GO_START
        beq _level
        ldx level_no            ; through the gate
        inx
        cpx #STEP_LEVELS        ; past this step's levels:
        bcc _level              ; level 1 again
        ldx #0
_level:
        stx level_no
        jmp start_map
; The end of the map's data.
trans_tables:
        lda #0
        sta up_on
        rts
; The screen off (bit 7 read: the raster line; written:
; line 256 +) and the sprites.
trans_off:
        lda $d011
        and #%01101111
        sta $d011
        lda #0
        sta $d015
        sta up_on
        rts
; The level's things from the start (not after a fall).
trans_second:
        lda trans_kind
        cmp #GO_BACK
        beq _respawn
        jsr restart             ; the level's things
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
        jsr place_heirloom
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
