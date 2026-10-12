; DREADCASTLE 08 - the packed levels, PAL C64.
; Levels 4 to 6, the Black Mire, the Grey Crags and the
; Frozen Pass. The maps, the tables and the sets of
; characters of all the levels are kept packed, and
; unpacked a page a frame; the will-o'-the-wisps of the
; mire and the spikes of ice flicker and hurt.
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
        lda #$36                ; BASIC out; I/O, KERNAL in
        sta $01
        jsr move_high           ; the packed data under it
        jsr kernal_out          ; and the KERNAL out
        lda #0                  ; level 1
        sta level_no
        sta has_staff           ; no staff yet
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
        jsr reset_enemies       ; at their start
        jsr place_oscar
        jsr init_irq            ; the interrupts on

; The main loop: one turn a frame, from the HUD down. In a
; transition (trans not 0) only its step; after a fall,
; only the HUD.
frame_loop:
        jsr wait_hud
        jsr read_joystick
joy_ready:                      ; the tests set joy here
        lda frame_count         ; this turn's frame
        sta turn_frame
        lda trans
        bne _between
        jsr flutter_moths
        jsr move_oscar
        lda trans               ; fallen?
        bne _fallen
        jsr animate_oscar
        jsr follow_camera
        jsr place_oscar
        jsr place_staff
        lda swap
        beq +
        jsr do_swap             ; the back screen in front:
        jmp _after              ; the colour RAM first
+       jsr prepare_back        ; else a step of the next
_after:                         ; after the screens
        jsr move_enemies
        jsr hit_enemies
        lda trans               ; no health left?
        bne _fallen
        jsr place_enemies
        jsr touch_things
        jsr tick_night
        jsr show_hud
        jsr place_heirloom
        jsr flicker_hazards     ; after the colour RAM
        jmp frame_done
_fallen:
        jsr show_hud
        jmp frame_done
_between:
        jsr transition
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
        .include "bat.asm"
        .include "enemies.asm"
        .include "staff.asm"
        .include "objects.asm"
        .include "irq.asm"
        .include "level.asm"
        .include "scroll.asm"
        .include "data.asm"
