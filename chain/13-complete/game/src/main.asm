; DREADCASTLE 13 - the complete game, PAL C64.
; The title: the name over the castle's door, the menu
; (MUSIC, SOUND FX, SILENT: Up and Down), Fire: the game.
; Eight levels: the Village of Mortals, the Churchyard,
; the Wild Wood, the Black Mire, the Grey Crags, the
; Frozen Pass, Dreadcastle Gate and the Throne Tower: 128
; metatile columns each, from the start to the gate. Oscar
; walks and jumps with joystick 2 (Up to jump, held
; longer, higher); Up and Fire together turn him into a
; bat, Down and Fire back; the bat beats its wings (Up),
; falls when let go, dives with Down and eats the moths of
; the sky. Three heirlooms to take in each level; the
; lantern of the checkpoint; the gate opens with all
; three; through it LEVEL CLEAR, the night left into the
; score, and the next level; in level 8 the door of the
; throne room leads to Tom Darkfang: he leaps and charges
; struck eight times, he runs away through the window: the
; victory, the night left into the score; Fire, the title.
; A fall into a pit or into water: back at the lantern, or
; at the start. The enemies (sprites 3-6): the watchman
; walks to and fro, the crow flies on a wave, the cat
; jumps at Oscar; a touch takes two notches of health and
; throws him back; he blinks, safe, for a moment; with no
; health left, back at the lantern. In the wood the staff
; of the Count lies on the path: taken, Fire strikes with
; it, and a struck enemy vanishes in a puff until Oscar
; starts again; the brambles hurt as a touch; his head
; stops under the blocks. In the mire the
; will-o'-the-wisps flicker and hurt as a touch; in the
; mountain the spikes of ice glint and hurt, in the castle
; the spikes of iron and the fire. The night: two minutes
; a level; at dawn the sky lightens, Oscar vanishes in a
; puff of smoke: the game is over; Fire, the title. The
; score: an enemy struck 100, an heirloom 500, a moth 10,
; Tom 5000, a step of the night left 50. The theme plays
; in a loop; in the arena Tom's, tense and fast, until he
; is beaten; a jingle at the gate, at the victory, at
; dawn; with SOUND FX the sound effects.
; Assemble this file: it includes the others.
; With -D RECORD_SONG=N the program plays song N from the
; start (1 Tom's theme, 2-4 the jingles); with
; -D RECORD_SFX=1 the sound effects one after the other
; (tools/record_music.py records them).
        .cpu "6502"
        .weak
RECORD_SONG   = 0               ; 0: the game as it is
RECORD_SFX    = 0
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
        .if RECORD_SONG + RECORD_SFX != 0
        jsr music_stop          ; to record: silence
        .fi                     ; till the interrupts are on
        jsr init_irq            ; the interrupts on
        .if RECORD_SONG != 0
        lda #RECORD_SONG        ; that song, from its start
        jsr music_start
        .fi
        .if RECORD_SFX != 0     ; every effect, one
        lda #SOUND_FX           ; each FX_REEL_FRAMES frames
        sta sound_mode
        ldx #0                  ; X: the effect
_reel:
        lda frame_count
        clc
        adc #FX_REEL_FRAMES
        sta work
        txa
        jsr sfx_start           ; (it keeps X)
_wait:
        lda frame_count
        cmp work
        bne _wait
        inx
        cpx #FX_COUNT
        bne _reel
_rest:
        jmp _rest               ; then nothing more
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
        .include "effects.asm"
        .include "level.asm"
        .include "scroll.asm"
        .include "data.asm"
