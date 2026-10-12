; The game's states: the title, playing, the count
; at the end of a level, the victory, dawn; the score. The
; title: the castle under the moon; the count at the end
; of a level: the night left into the score; the victory:
; in the arena; dawn: the sun rises; the score: classic.
;
; game_state says which: ST_PLAY is the main loop's game;
; the others have their turn here (state_turn). The game
; leaves one for another through a transition
; (objects.asm): GO_START from the title to level 1,
; GO_NEXT after the count, GO_TITLE after the victory or
; dawn; or at once: the gate (start_tally), Tom gone
; (start_won), the night over (start_dawn).
;
; The words over the playfield are a band of rows (BANDS,
; title.py): its first and last rows blank, the words in
; the rows between, in the HUD's characters. The rows are
; written into both screens, and the top interrupt brings
; two more interrupts (irq.asm): the HUD's characters from
; a line of the first row, the playfield's from a line of
; the last. The band stays until the screen goes off.
;
; The score: six BCD digits (score: the low two first), on
; row 24 of the HUD; add_score adds, show_score writes it
; when it has changed.
;
; This file is assembled for STATE_CODE, $0400 (data.asm:
; in the PRG in the screens, after the third block for under
; the KERNAL; moved there by move_high at the start); its
; texts (texts.asm, from title.py) wait under the KERNAL,
; in the third block.

TALLY_WAIT    = 40              ; LEVEL CLEAR, then count
TALLY_TICK    = 3               ; frames a step of the night
TALLY_END     = 60              ; counted: then the next

WON_WAIT      = 50              ; the victory, then count
BAND_LINE     = 61              ; row 0's third line
NIGHT_POINTS  = $50             ; a step of the night: 50
SCORE_DIGITS  = 6

; The states at the start: the title, MUSIC, the score 0,
; no band.
init_states:
        ldx #STATE_BYTES - 1
        lda #0
-       sta STATES,x
        dex
        bpl -
        lda #ST_TITLE
        sta game_state
        rts

; A turn of the state game_state (not ST_PLAY).
state_turn:
        ldx game_state
        lda state_low - 1,x
        sta vector
        lda state_high - 1,x
        sta vector + 1
        jmp (vector)
state_low:
        .byte <title_turn, <tally_turn
        .byte <won_turn, <dawn_turn
state_high:
        .byte >title_turn, >tally_turn
        .byte >won_turn, >dawn_turn
        .cerror ST_TITLE != 1 || ST_DAWN != 4, "the order"

; The keys pushed in this frame and not in the one before:
; in A; prev_joy := joy.
new_keys:
        lda prev_joy
        eor #$ff
        and joy
        ldx joy
        stx prev_joy
        rts

; ---------------------------------------------------------
; The title.

; Oscar standing in front of the castle's door at the end of
; level 7 (respawn at TITLE_X: the camera as far right as it
; goes); the menu.
title_place:
        lda #<TITLE_X
        sta respawn_x
        lda #>TITLE_X
        sta respawn_x + 1
        jsr respawn
        jmp show_menu

; Sprites 0 and 1, Oscar; 2-5 the name in big letters
; (logo.py: hi-res, stretched twice across and down, its
; colour); 6 the moon, in the sky between the towers; 7 off.
title_sprites:
        jsr place_oscar
        ldx #LOGO_SPRITES - 1
-       txa
        clc
        adc #LOGO_BLOCK
        sta SCREEN_A + POINTERS + 2,x
        sta SCREEN_B + POINTERS + 2,x
        lda #LOGO_COLOUR
        sta $d029,x
        dex
        bpl -
        lda #LOGO_X             ; across, LOGO_STEP apart
        sta $d004
        lda #LOGO_X + LOGO_STEP
        sta $d006
        lda #LOGO_X + LOGO_STEP * 2
        sta $d008
        lda #LOGO_X + LOGO_STEP * 3
        sta $d00a
        lda #LOGO_Y
        sta $d005
        sta $d007
        sta $d009
        sta $d00b
        .cerror LOGO_X + LOGO_STEP * 3 > 255, "no ninth bit"
        .cerror LOGO_SPRITES != 4, "sprites 2-5"
        lda #MOON_BLOCK         ; the moon
        sta SCREEN_A + POINTERS + 6
        sta SCREEN_B + POINTERS + 6
        lda #TITLE_MOON_X
        sta $d00c
        lda #TITLE_MOON_Y
        sta $d00d
        lda #MOON_COLOUR
        sta $d02d
        .cerror TITLE_MOON_X > 255, "no ninth bit"
        lda $d010               ; no ninth bit but Oscar's
        and #%00000011
        sta $d010
        lda #%00111100          ; the name: big, hi-res
        sta $d017
        sta $d01d
        lda $d01c
        and #%11000011
        sta $d01c
        lda $d015               ; 2-6 on (Oscar's: as
        and #%00000011          ; place_oscar left them)
        ora #%01111100
        sta $d015
        rts

; The title shown (trans_on): its sprites, its music; the
; state.
title_on:
        jsr title_sprites
        lda #ST_TITLE
        sta game_state
        jmp title_music

; The menu in the HUD's three rows, both screens: the
; choices, the chosen in white with the pointer before it,
; PRESS FIRE.
show_menu:
        lda #MENU_ROW
        ldx #MENU_CHOICES
        jsr clear_rows
        lda #<menu_texts
        sta copy_src
        lda #>menu_texts
        sta copy_src + 1
        jsr put_texts
        lda sound_mode          ; the chosen one's row
        clc
        adc #MENU_ROW
        jsr row_cells
        ldy #POINTER_COL
        lda #POINTER_CODE
        sta (top_tab),y
        sta (bottom_tab),y
        lda #POINTER_COLOUR
        sta (col_ptr),y
        ldy #MENU_COL + 7       ; its colour: 8 cells
        lda #CHOSEN_COLOUR
-       sta (col_ptr),y
        dey
        cpy #MENU_COL - 1
        bne -
        rts

; On the title, MUSIC: the theme (from its start, if it is
; not playing); else silence.
title_music:
        lda sound_mode
        bne _quiet
        lda mus_on
        beq +
        lda mus_song
        cmp #SONG_THEME
        beq _done
+       lda #SONG_THEME
        jmp music_start
_quiet:
        jmp music_stop
_done:
        rts

; The title's turn: Fire (pushed now) a new game; Up and
; Down the choice above or below; PRESS FIRE blinks, 32
; frames in each colour.
title_turn:
        jsr new_keys
        tax
        and #JOY_FIRE
        beq +
        lda #GO_START
        jmp start_transition
+       txa
        and #JOY_UP
        beq +
        lda sound_mode
        beq _blink
        dec sound_mode
        jmp _chosen
+       txa
        and #JOY_DOWN
        beq _blink
        lda sound_mode
        cmp #MENU_CHOICES - 1
        beq _blink
        inc sound_mode
_chosen:
        jsr show_menu
        jsr title_music
_blink:
        ldx #PRESS_ON
        lda turn_frame
        and #%00100000
        beq +
        ldx #PRESS_OFF
+       txa
        ldx #PRESS_LENGTH - 1
-       sta COLOUR_RAM + PRESS_CELL,x
        dex
        bpl -
        rts

; A level from its start (trans_on): the theme from its
; start, if the menu said MUSIC.
level_theme:
        lda sound_mode
        bne +
        lda #SONG_THEME
        jmp music_start
+       rts

; A new game (GO_START, trans_second): the score 0, no
; staff, the HUD's rows 22 and 23 again (the title had the
; menu there).
new_game:
        lda #0
        sta score
        sta score + 1
        sta score + 2
        sta has_staff
        jmp draw_hud

; ---------------------------------------------------------
; The count at the end of a level.

; Through the gate of levels 1-7 (touch_gate): the game
; stops; LEVEL CLEAR.
start_tally:
        lda #ST_TALLY
        sta game_state
        lda #0
        sta state_phase
        lda #TALLY_WAIT
        sta state_timer
        ldx #BAND_CLEAR
        jmp show_band

; After TALLY_WAIT frames, every TALLY_TICK a step of the
; night left into the score; none left, TALLY_END frames
; more, then the next level.
tally_turn:
        dec state_timer
        bne _done
        lda state_phase
        bne _next
        jsr count_night
        lda #TALLY_TICK
        bcc +
        inc state_phase         ; counted
        lda #TALLY_END
+       sta state_timer
_done:
        rts
_next:
        lda #GO_NEXT
        jmp start_transition

; A step of the night left into the score (NIGHT_POINTS),
; the HUD again; none left: carry set.
count_night:
        lda night
        sec
        beq +
        dec night
        lda #NIGHT_POINTS
        ldy #0
        jsr add_score
        jsr show_hud
        clc
+       rts

; ---------------------------------------------------------
; The victory ("Nell'arena").

; Tom gone (tom_gone): the game stops in the arena; the
; words of the end over it.
start_won:
        lda #ST_WON
        sta game_state
        lda #0
        sta state_phase
        lda #WON_WAIT
        sta state_timer
        ldx #BAND_WON
        jmp show_band

; The night left into the score, as at a gate; then Fire
; (pushed now): the title.
won_turn:
        jsr new_keys
        ldx state_phase
        bne fire_title
        dec state_timer
        bne +
        jsr count_night
        lda #TALLY_TICK
        sta state_timer
        bcc +
        inc state_phase         ; counted: Fire now
+       rts

; A: the keys pushed now; Fire among them, the title.
fire_title:
        and #JOY_FIRE
        beq +
        lda #GO_TITLE
        jmp start_transition
+       rts

; ---------------------------------------------------------
; Dawn: the sun rises.

; The night over (tick_night): the game stops.
start_dawn:
        lda #ST_DAWN
        sta game_state
        lda #0
        sta state_phase
        lda #DAWN_FRAMES
        sta state_timer
        rts

; Phases 0 to DAWN_STEPS - 1: every DAWN_FRAMES frames the
; playfield's background a colour of dawn_colours, blue to
; orange; with the last, phase DAWN_STEPS, Oscar in a puff
; of smoke for PUFF_FRAMES frames, then gone with the
; staff; then THE SUN HAS RISEN, and Fire: the title.
dawn_turn:
        jsr new_keys
        ldx state_phase
        cpx #DAWN_STEPS
        bcc _sky
        beq _puff
        jmp fire_title
_sky:
        dec state_timer
        bne _done
        lda dawn_colours,x
        sta play_d021
        inc state_phase
        lda #DAWN_FRAMES
        sta state_timer
        cpx #DAWN_STEPS - 1     ; the last: the smoke
        bne _done
        lda #PUFF_FRAMES
        sta osc_puff
_done:
        rts
_puff:
        dec osc_puff
        beq _gone
        jsr animate_oscar
        jsr place_oscar
        jmp place_staff
_gone:
        lda $d015               ; Oscar and the staff off
        and #%11111000
        sta $d015
        inc state_phase
        ldx #BAND_DAWN
        jmp show_band

; ---------------------------------------------------------
; The score.

; A (tens and units) and Y (thousands and hundreds), BCD,
; added to the score; X kept. In decimal mode (sed), with
; the interrupts held: the music's sums in the top
; interrupt would go wrong in it (the 6510 does not leave
; it for an interrupt). plp brings back the flags of
; before: binary mode, the interrupts as they were.
add_score:
        php
        sei
        sed
        clc
        adc score
        sta score
        tya
        adc score + 1
        sta score + 1
        lda #0
        adc score + 2
        sta score + 2
        plp
        lda #1
        sta score_new
        rts

; The score on row 24 of the HUD, both screens, if it has
; changed (show_hud); write_score: in any case (show_name,
; after the row's zeros).
show_score:
        lda score_new
        bne write_score
        rts
write_score:
        lda #0
        sta score_new
        ldx #2                  ; the high byte first
        ldy #0
-       lda score,x
        lsr a
        lsr a
        lsr a
        lsr a
        clc
        adc #DIGIT_0
        sta SCREEN_A + SCORE_CELL,y
        sta SCREEN_B + SCORE_CELL,y
        lda score,x
        and #%00001111
        clc
        adc #DIGIT_0
        sta SCREEN_A + SCORE_CELL + 1,y
        sta SCREEN_B + SCORE_CELL + 1,y
        iny
        iny
        dex
        bpl -
        rts

; ---------------------------------------------------------
; Words on the screen.

; Band X (BAND_CLEAR, BAND_WON, BAND_DAWN): its rows blank
; in both screens, its texts; the lines of the interrupts,
; a line of its first row and of its last; the HUD's
; characters with the screen shown; on.
show_band:
        lda band_texts_lo,x
        sta copy_src
        lda band_texts_hi,x
        sta copy_src + 1
        lda band_first,x        ; first row * 8 + BAND_LINE
        asl a
        asl a
        asl a
        adc #BAND_LINE
        sta band_top
        lda band_rows,x         ; + (rows - 1) * 8
        asl a
        asl a
        asl a
        adc band_top
        sec
        sbc #8
        sta band_end
        ldy band_rows,x         ; its rows blank
        lda band_first,x
        pha
        tya
        tax
        pla
        jsr clear_rows
        jsr put_texts
        lda shown_d018          ; the screen shown, the
        and #%11110000          ; HUD's characters
        ora #D018_HUD & %00001110
        sta band_d018
        lda #1
        sta band_on
        rts
        .cerror D018_HUD & %11110000 != 0, "screen A"

; dst := the offset of row A's first cell, A * 40; the
; pointers of text_pointers.
row_cells:
        sta dst
        asl a
        asl a
        adc dst                 ; * 5 (carry clear: A < 52)
        asl a                   ; * 10
        sta dst
        lda #0
        asl dst                 ; * 20
        rol a
        asl dst                 ; * 40
        rol a
        sta dst + 1
; The cell at offset dst in screen A (top_tab), in screen B
; (bottom_tab), in the colour RAM (col_ptr): draw_column's
; pointers, free outside it.
text_pointers:
        lda dst
        sta top_tab
        sta bottom_tab
        sta col_ptr
        lda dst + 1
        clc
        adc #>SCREEN_A
        sta top_tab + 1
        clc
        adc #>(SCREEN_B - SCREEN_A)
        sta bottom_tab + 1
        lda dst + 1
        clc
        adc #>COLOUR_RAM
        sta col_ptr + 1
        rts
        .cerror (SCREEN_A | SCREEN_B) & $ff != 0, "pages"

; X rows from row A, in both screens: blank (code 0, blank
; in every set and in the HUD's), the colour RAM black.
clear_rows:
        jsr row_cells
-       ldy #39
        lda #0
_cell:
        sta (top_tab),y
        sta (bottom_tab),y
        sta (col_ptr),y
        dey
        bpl _cell
        lda top_tab             ; a row down
        clc
        adc #40
        sta top_tab
        sta bottom_tab
        sta col_ptr
        bcc +
        inc top_tab + 1
        inc bottom_tab + 1
        inc col_ptr + 1
+       dex
        bne -
        rts

; The texts at copy_src into both screens, their colours
; into the colour RAM: records of a row, a column, a
; colour, a length and the characters (the HUD's codes);
; $ff after the last (texts.asm, from title.py).
put_texts:
        ldy #0
        lda (copy_src),y
        cmp #$ff
        bne +
        rts
+       jsr row_cells           ; the row, + the column
        ldy #1
        lda (copy_src),y
        clc
        adc dst
        sta dst
        bcc +
        inc dst + 1
+       jsr text_pointers
        ldy #2
        lda (copy_src),y
        sta fill                ; the colour
        iny
        lda (copy_src),y
        tax                     ; the length
        lda copy_src            ; the characters
        clc
        adc #4
        sta copy_src
        bcc +
        inc copy_src + 1
+       ldy #0
-       lda (copy_src),y
        sta (top_tab),y
        sta (bottom_tab),y
        lda fill
        sta (col_ptr),y
        iny
        dex
        bne -
        tya                     ; the next record
        clc
        adc copy_src
        sta copy_src
        bcc put_texts
        inc copy_src + 1
        jmp put_texts
