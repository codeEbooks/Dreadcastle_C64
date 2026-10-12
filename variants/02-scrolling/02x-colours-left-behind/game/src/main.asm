; DREADCASTLE 02 - the scrolling, PAL C64.
; Joystick 2 moves the camera over the village, both ways,
; two pixels a frame, with the HUD still: the scroll
; register, two screens, the colour RAM moved in place.
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
        lda #0                  ; level 1
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

; The main loop: one turn a frame, from the HUD down: the
; joystick moves the camera.
frame_loop:
        jsr wait_hud
        jsr read_joystick
joy_ready:                      ; the tests set joy here
        jsr steer_camera
        lda swap
        beq +
        jsr do_swap             ; the back screen in front:
        jmp _after              ; the colour RAM first
+       jsr prepare_back        ; else a step of the next
_after:                         ; after the screens
frame_done:                     ; the tests compare here
        jmp frame_loop

; Joystick 2: CIA 1, port A, bits 0-4 low when pushed.
; In joy they are turned round: bit set = pushed.
read_joystick:
        lda $dc00
        eor #$ff
        and #%00011111          ; fire right left down up
        sta joy
        rts

        .include "vic.asm"
        .include "oscar.asm"
        .include "irq.asm"
        .include "level.asm"
        .include "scroll.asm"
        .include "data.asm"
