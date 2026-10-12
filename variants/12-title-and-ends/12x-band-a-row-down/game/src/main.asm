; DREADCASTLE 12 - the title and the ends, PAL C64.
; The title over the castle's door, with its menu (MUSIC,
; SOUND FX, SILENT); the count of the night left at the
; gate; the victory in the arena; dawn, when the night is
; over: the game is over. The score.
; Assemble this file: it includes the others.
; With -D RECORD_SONG=1 the program plays Tom's theme from
; the start, to record it.
        .cpu "6502"
        .weak
RECORD_SONG   = 0               ; 0: the game as it is
        .endweak
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
        jsr init_states         ; the title, MUSIC
        jsr init_tom            ; none of Tom yet
        lda #TITLE_LEVEL        ; the title: level 7 at its
        sta level_no            ; end
        lda #0                  ; no staff yet
        sta has_staff
        jsr load_level          ; its map, its setting
        jsr init_vic
        jsr init_scroll
        jsr title_place         ; Oscar, camera, menu
        lda #0                  ; screen A, colour RAM
        sta col_screen
        lda #39
        sta col_end
        jsr draw_columns
        jsr init_sprites
        jsr title_sprites       ; the name, the moon
        jsr music_init          ; silence; the song's start
        .if RECORD_SONG != 0
        jsr music_stop          ; to record: silence
        .fi                     ; till the interrupts are on
        jsr init_irq            ; the interrupts on
        .if RECORD_SONG != 0
        lda #RECORD_SONG        ; that song, from its start
        jsr music_start
        .fi

; The main loop: one turn a frame, from the HUD down. In a
; transition (trans not 0) only its step; after a fall,
; only the HUD; in the arena Tom instead of the enemies
; and the level's things; out of the game (the title, the
; count, the victory, dawn) the state's turn.
frame_loop:
        jsr wait_hud
        jsr read_joystick
joy_ready:                      ; the tests set joy here
        lda frame_count         ; this turn's frame
        sta turn_frame
        lda trans
        bne _between
        lda game_state          ; not playing
        bne _state
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
        lda arena
        bne _tom
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
_tom:
        jsr fight_tom           ; he moves, struck, touches
        lda trans               ; no health left, or gone?
        bne _fallen
        jsr place_tom
        jsr tick_night
        jsr show_hud
        jsr flicker_hazards
        jmp frame_done
_fallen:
        jsr show_hud
        jmp frame_done
_state:
        jsr state_turn
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
        .include "tom.asm"
        .include "staff.asm"
        .include "objects.asm"
        .include "irq.asm"
        .include "player.asm"
        .include "level.asm"
        .include "scroll.asm"
        .include "data.asm"
