; DREADCASTLE 01 - the village at night, PAL C64.
; The Village of Mortals at night, drawn from its map of
; metatiles in multicolour characters, and Oscar at its
; start; under it the HUD, in characters of its own: two
; raster interrupts a frame.
; Assemble this file: it includes the others.
        .cpu "6502"
        .include "memory.asm"
        .include "../assets/generated/assets.inc"

        * = $0801
        .word basic_end         ; BASIC line: 10 SYS 2061
        .word 10
        .byte $9e
        .text "2061"
        .byte 0
basic_end:
        .word 0

entry:
        sei                     ; no interrupts here
        cld
        ldx #$ff                ; fresh stack
        txs
        jsr kernal_out          ; the KERNAL out
        lda #1                  ; level 2
        sta level_no
        jsr load_level          ; its map, its setting
        jsr init_vic
        jsr init_scroll
        jsr respawn             ; Oscar at the start
        lda #0                  ; screen A, colour RAM
        sta col_screen
        lda #39
        sta col_end
        jsr draw_columns
        jsr draw_hud            ; the HUD's rows
        jsr show_name           ; the level's name
        jsr init_sprites
        jsr place_oscar
        jsr init_irq            ; the interrupts on

; The main loop: one turn a frame, from the HUD down.
; Nothing moves yet: the turn is empty.
frame_loop:
        jsr wait_hud
frame_done:                     ; the tests compare here
        jmp frame_loop

        .include "vic.asm"
        .include "oscar.asm"
        .include "irq.asm"
        .include "level.asm"
        .include "scroll.asm"
        .include "data.asm"
