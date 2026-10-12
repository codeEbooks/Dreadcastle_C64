; The falls: Oscar out of the playfield at the bottom, the {3-4}
; transition takes him back to the start; the HUD's bars. {3-4}
; The level as a game: the heirlooms to take, the lantern {5}
; of the checkpoint, the gate that opens with all three; the {5}
; health, the night until dawn, the HUD; and the moments {5}
; between: after a fall, Oscar back at the lantern (or at {5}
; the start); through the gate the next level; at dawn, {5-6}
; level 1 again. {5-6}
; the start); through the gate the next level, with the {7}
; tables of its setting; at dawn, level 1 again. {7-11}
; tables of its setting (after the count of states.asm); a {12}
; new game from the title, level 1; the title, after the {12}
; victory or dawn. {12}
; Where the heirlooms, the lantern and the gate are: the {5}
; level's objects (OBJECTS, memory.asm). {5}

HEALTH_FULL   = 8               ; 4 characters of the bar
NIGHT_STEPS   = 16              ; 8 characters of the bar {5}
NIGHT_STEP    = 375             ; frames: 7.5 s, 2 minutes {5}
TOLL_STEPS    = 2               ; the bell: 15 s {13}
HEIRLOOM_BOX  = 16              ; the box of an heirloom {5}
TOUCH         = 12              ; Oscar's middle to its own {5}
TRANS_FRAMES  = 50              ; a transition: frames
BLANK_AT      = 14              ; the screen off, then on
SHOW_AT       = 1
        .cerror NIGHT_STEPS != 16, "8 characters, 2 steps" ; {5}
;|STEP_LEVELS   = 2               ; the levels of this step {5-6}
;|STEP_LEVELS   = 3               ; the levels of this step {7-7}
;|STEP_LEVELS   = 6               ; the levels of this step {8-8}
;|STEP_LEVELS   = 8               ; the levels of this step {9-9}

; Oscar has fallen out of the playfield: no health left.
; The sprites go off, and the transition takes him back. {-6}
; The sprites go off (the moon stays: env_moon), and the {7}
; transition takes him back. {7}
fallen:
        lda #0
        sta health
;|        sta $d015 ; {-6}
        ldy env ; {7}
        lda env_moon,y ; {7}
        and $d015 ; {7}
        sta $d015 ; {7}
        lda #GO_BACK

; A transition of kind A begins: TRANS_FRAMES frames.
start_transition:
        sta trans_kind
        lda #TRANS_FRAMES
        sta trans
        rts

;{5}
; What Oscar touches: the heirlooms, the lantern, the {5-6}
; gate. {5-6}
; What Oscar touches: the staff, an heirloom, the lantern, {7}
; the gate. {7}
touch_things:
        jsr open_door
        jsr touch_staff ; {7}
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
        lda #$00                ; 500 points {12}
        ldy #$05 ; {12}
        jsr add_score ; {12}
        lda #FX_HEIRLOOM        ; its sound {13}
        jsr sfx_start ; {13}
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
        lda #FX_LANTERN         ; its sound {13}
        jsr sfx_start ; {13}
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
        lda #FX_GATE            ; its sound {13}
        jsr sfx_start ; {13}
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
; feet below its top): the level is done, the next one. {5-9}
; feet below its top): the level is done, the next one. {10-11}
; Through the last level's, the door of the throne room, {10-11}
; Tom's arena. {10-11}
; feet below its top): the level is done; the count, then {12}
; the next one. Through the last level's, the door of the {12}
; throne room, Tom's arena. {12}
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
        ldx level_no ; {10}
        cpx #ARENA_LEVEL ; {10}
        beq + ; {10}
        jmp start_tally         ; the count first {12}
;|        lda #GO_NEXT            ; the next level {5-11}
;|        jmp start_transition ; {5-11}
+       lda #GO_ARENA ; {10}
        jmp start_transition ; {10}
_done:
        rts

; The night: a frame less of the step; at its end a step
; less. No steps left: dawn, level 1 again. {5-11}
; less. No steps left: dawn, the game ends. Not once the {12}
; game has stopped in this turn (the gate, Tom gone). {12}
; The last TOLL_STEPS steps start with a bell. {13}
tick_night:
        lda game_state ; {12}
        bne _done ; {12}
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
;|        rts ; {5-12}
        lda night ; {13}
        cmp #TOLL_STEPS + 1 ; {13}
        bcs _done ; {13}
        lda #FX_TOLL            ; the bell {13}
        jmp sfx_start ; {13}
_dawn:
;|        lda #GO_START           ; dawn: level 1 again {5-11}
;|        jmp start_transition ; {5-11}
        jmp start_dawn          ; dawn: the game ends {12}
_done:
        rts
;{}

; The HUD, in both screens: the bar of the health. {3-3}
; The HUD, in both screens: the bars of the health and of {4-4}
; the energy. {4-4}
; The HUD, in both screens: the bars of the health, of the {5}
; energy and of the night, and the heirlooms taken. {5-9}
; energy and of the night, and the heirlooms taken; in the {10}
; arena Tom's bar too, on row 24. {10-11}
; arena Tom's bar too, on row 24; the score, when it has {12}
; changed. {12}
show_hud:
        lda health
        ldx #4
        ldy #HEALTH_BAR - HUD_ROW
        jsr show_bar
        lda energy + 1          ; whole steps, 0-6 {4}
        lsr a ; {4}
        lsr a ; {4}
        lsr a ; {4}
        lsr a ; {4}
        lsr a ; {4}
        ldx #3 ; {4}
        ldy #ENERGY_BAR - HUD_ROW ; {4}
        jsr show_bar ; {4}
        lda night ; {5}
        ldx #8 ; {5}
        ldy #NIGHT_BAR - HUD_ROW ; {5}
        jsr show_bar ; {5}
        lda got ; {5}
        clc ; {5}
        adc #DIGIT_0 ; {5}
        sta SCREEN_A + HEIRLOOM_DIGIT ; {5}
        sta SCREEN_B + HEIRLOOM_DIGIT ; {5}
        jsr show_score ; {12}
        lda arena ; {10}
        beq + ; {10}
        jmp show_tom ; {10}
;|        rts ; {3-9}
+       rts ; {10}

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

;{5}
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
;{}

; A frame of a transition: trans counts the frames down, {3-4}
; and trans_steps gives the step of each frame. The picture {3-4}
; stays still at first (Oscar gone after a fall). At {3-4}
; BLANK_AT the screen goes off; Oscar at respawn_x; screen {3-4}
; A drawn again in four frames, ten columns each, with the {3-4}
; colour RAM; the HUD. At SHOW_AT the screen comes back on, {3-4}
; with the sprites and the level's name. {3-4}
; A frame of a transition: trans counts the frames down, {5}
; and trans_steps gives the step of each frame. The picture {5}
; stays still at first (Oscar gone after a fall), and {5}
; meanwhile the data are copied, a page a frame: the next {5-7}
; meanwhile the data are unpacked, a page a frame: the next {8}
; level (through the gate), level 1 (at dawn), or the same {5-11}
; level (through the gate), level 1 (a new game), level 7 {12}
; (the title), or the same {12}
; again, from its map (MAP_PAGES frames); if its setting {5}
; is another, the setting's tables (ENV_PAGES frames). At {5}
; BLANK_AT the screen goes off; the setting's characters, {5}
; if another set, SET_PAGES frames; the level's things {5}
; from the start, with its objects; Oscar at respawn_x; {5}
; screen A drawn again in four frames, ten columns each, {5}
; with the colour RAM; the HUD. At SHOW_AT the screen comes {5}
; back on, with the sprites, the level's name. {5-5}
; back on, with the sprites, the enemies at their start, {6}
; the level's name. {6}
; Into the arena (GO_ARENA), instead of a level: Tom's {10}
; pictures, unpacked a page a frame, then mirrored, a {10}
; picture a frame; Oscar at ARENA_X, Tom at his start. {10}
; A new game (GO_START): level 1, the score 0, no staff, the {12}
; HUD's rows again; the title (GO_TITLE): level 7 at its {12}
; end, Oscar at its door, the menu, the name and the moon; {12}
; at the screen off, the band of text gone. {12}
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

; The step of each frame, from trans 0 up: 0 none, 1 on, {3-4}
; 3-6 the drawing, 7 Oscar again, 10 the screen off; 2, 8 {3-4}
; and 9 do nothing yet. {3-4}
; The step of each frame, from trans 0 up: 0 none, 1 on, {5}
; 2 a page, 3-6 the drawing, 7 the level's things and {5-9}
; Oscar, 8 the level, 9 the setting, 10 the screen off. {5-9}
; 2 a page (or a picture of Tom mirrored), 3-6 the drawing, {10}
; 7 the level's things and Oscar, 8 the level (or Tom's {10}
; pictures), 9 the setting, 10 the screen off. {10}
trans_steps:
        .byte 0, 1, 2, 2, 2, 6, 5, 4, 3, 7     ; 0-9
        .byte 2, 2, 2, 2, 10                   ; 10-14
        .byte 0, 0, 0, 0, 0, 0, 0, 0, 0        ; 15-23
        .byte 0, 0, 0, 0, 0, 0, 0, 0, 0        ; 24-32
        .byte 2, 2, 2, 2, 2, 2, 2, 2, 2        ; 33-41
        .byte 9, 2, 2, 2, 2, 2, 2, 8           ; 42-49
        .cerror * - trans_steps != TRANS_FRAMES, "each"
trans_low:
;|        .byte <trans_none, <trans_on, <trans_none ; {3-4}
        .byte <trans_none, <trans_on, <trans_page ; {5}
        .byte <trans_draw_0, <trans_draw_1
        .byte <trans_draw_2, <trans_draw_3
;|        .byte <trans_second, <trans_none, <trans_none ; {3-4}
        .byte <trans_second, <trans_level, <trans_tables ; {5}
        .byte <trans_off
trans_high:
;|        .byte >trans_none, >trans_on, >trans_none ; {3-4}
        .byte >trans_none, >trans_on, >trans_page ; {5}
        .byte >trans_draw_0, >trans_draw_1
        .byte >trans_draw_2, >trans_draw_3
;|        .byte >trans_second, >trans_none, >trans_none ; {3-4}
        .byte >trans_second, >trans_level, >trans_tables ; {5}
        .byte >trans_off

trans_none:
        rts
;{5}
; A page of the data being copied, if any. {5-7}
; A page of the stream being unpacked, if any. {8}
trans_page:
        lda up_on
        beq trans_none
        jmp unpack_page
; The level, from its map: through the gate the next one; {5}
; at dawn level 1; after a fall nothing (the level as it {5-11}
; is). {5-6}
; is). env_copy: another setting. {7-11}
; a new game level 1, the title level 7; after a fall {12}
; nothing (the level as it is). env_copy: another setting. {12}
; Into the arena Tom's pictures. {10}
trans_level:
        lda #0
        sta env_copy ; {7}
        sta up_on
        lda trans_kind
        cmp #GO_BACK
        beq trans_none
        cmp #GO_ARENA           ; Tom's pictures {10}
        bne + ; {10}
        jmp start_tom ; {10}
;|        ldx #0                  ; level 1 {5-9}
+       ldx #0                  ; level 1 {10}
        cmp #GO_START
        beq _level
        ldx #TITLE_LEVEL        ; the title {12}
        cmp #GO_TITLE ; {12}
        beq _level ; {12}
        ldx level_no            ; through the gate
        inx
;|        cpx #STEP_LEVELS        ; past this step's levels: {5-9}
;|        bcc _level              ; level 1 again {5-9}
;|        ldx #0 ; {5-9}
_level:
        stx level_no
        lda level_env,x         ; its setting: another? {7}
        cmp env ; {7}
        beq + ; {7}
        inc env_copy ; {7}
;|        jmp start_map ; {5-6}
+       jmp start_map ; {7}
; The tables of the level's setting, if another (env stays {7}
; the setting shown until the screen goes off). {7}
; The end of the map's data. {5-6}
trans_tables:
        lda #0
        sta up_on
;|        rts ; {5-6}
        lda env_copy ; {7}
        beq trans_none ; {7}
        ldx level_no ; {7}
        ldy level_env,x ; {7}
        jmp start_tables ; {7}
;{}
; The screen off (bit 7 read: the raster line; written: {-6}
; line 256 +) and the sprites. {-6}
; The screen off (bit 7 read: the raster line; written: {7}
; line 256 +) and the sprites; env, its $d018 (shown from {7}
; respawn on), its registers; if another setting, its set {7-11}
; of characters, its first page. {7-11}
; respawn on), its registers (always: dawn may have {12}
; changed its background); no band of text; if another {12}
; setting, its set of characters, its first page. {12}
trans_off:
        lda $d011
        and #%01101111
        sta $d011
        lda #0
        sta $d015
        sta up_on ; {5}
        sta band_on ; {12}
;|        rts ; {3-6}
        jsr next_env ; {7}
        lda env_copy ; {7}
        beq trans_none ; {7}
        jsr start_set           ; the village's: none {7}
        jmp trans_page ; {7}
; Oscar at the start again. {3-4}
; The level's things from the start (not after a fall). {5-9}
; The level's things from the start (not after a fall); {10}
; into the arena, Oscar from now on at ARENA_X; in it, Tom {10}
; at his start. {10-11}
; at his start. A new game: the score, the staff, the HUD {12}
; first; the title: Oscar at the door, the menu (no HUD). {12}
trans_second:
        lda trans_kind ; {5}
        cmp #GO_BACK ; {5}
;|        beq _respawn ; {5-9}
        beq _arena ; {10}
        cmp #GO_ARENA ; {10}
        beq _in ; {10}
        cmp #GO_START ; {7}
        bne + ; {7}
;|        lda #0                  ; level 1: no staff {7-11}
;|        sta has_staff ; {7-11}
        jsr new_game ; {12}
;|        jsr restart             ; the level's things {5-6}
+       jsr restart             ; the level's things {7}
;|        jmp _respawn ; {10-11}
        lda trans_kind ; {12}
        cmp #GO_TITLE ; {12}
        bne _respawn ; {12}
        jmp title_place ; {12}
_in: ; {10}
        lda #1 ; {10}
        sta arena ; {10}
        lda #<ARENA_X ; {10}
        sta respawn_x ; {10}
        lda #>ARENA_X ; {10}
        sta respawn_x + 1 ; {10}
_arena: ; {10}
        lda arena ; {10}
        beq _respawn ; {10}
        jsr reset_tom ; {10}
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
        lda trans_kind          ; the title: its {12}
        cmp #GO_TITLE           ; sprites, its music {12}
        bne + ; {12}
        jsr title_on ; {12}
        jmp screen_on ; {12}
+       cmp #GO_START           ; after the title, {12}
        bne +                   ; the game's sprites {12}
        jsr init_sprites ; {12}
;|        jsr show_name           ; the level's name {-5}
;|        jsr show_name           ; the level's name, the {6-11}
+       jsr show_name           ; the level's name, the {12}
        jsr reset_enemies       ; enemies at their start {6}
        jsr place_oscar
        jsr place_staff ; {7}
        jsr place_enemies ; {6}
        jsr place_heirloom ; {5}
        lda #ST_PLAY            ; playing {12}
        sta game_state ; {12}
        lda arena               ; Tom {10}
;|        beq _on ; {10-10}
        beq + ; {11}
        jsr place_tom ; {10}
        jsr boss_theme          ; his theme {11}
        jmp _on ; {10}
+       lda trans_kind          ; a level from its start: {11}
        cmp #GO_BACK            ; the theme from its start {11}
        beq _on ; {11}
;|        lda #SONG_THEME ; {11-11}
;|        jsr music_start ; {11-11}
        jsr level_theme ; {12}
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
