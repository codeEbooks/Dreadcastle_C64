; DREADCASTLE 01 - the village at night, PAL C64. {1-1}
; The Village of Mortals at night, drawn from its map of {1-1}
; metatiles in multicolour characters, and Oscar at its {1-1}
; start; under it the HUD, in characters of its own: two {1-1}
; raster interrupts a frame. {1-1}
; DREADCASTLE 02 - the scrolling, PAL C64. {2-2}
; Joystick 2 moves the camera over the village, both ways, {2-2}
; two pixels a frame, with the HUD still: the scroll {2-2}
; register, two screens, the colour RAM moved in place. {2-2}
; DREADCASTLE 03 - Oscar, PAL C64. {3-3}
; Oscar walks and jumps with joystick 2 (Up to jump, held {3-3}
; longer, higher) on the streets, the roofs, the {3-3}
; balconies and the carts; the crates stop him; the {3-3}
; camera follows him. A fall into a pit: back at the {3-3}
; start. {3-3}
; DREADCASTLE 04 - the bat, PAL C64. {4-4}
; Up and Fire together turn Oscar into a bat, Down and {4-4}
; Fire back; the bat beats its wings (Up), falls when let {4-4}
; go and dives with Down; its flight uses up the energy, {4-4}
; and the moths of the sky give some back. {4-4}
; DREADCASTLE 05 - heirlooms and the gate, PAL C64. {5-5}
; The Village of Mortals and the Churchyard: three {5-5}
; heirlooms to take in each, the lantern of the {5-5}
; checkpoint, the gate that opens with all three and leads {5-5}
; to the next level; two minutes of night a level, then {5-5}
; level 1 again. {5-5}
; DREADCASTLE 06 - the enemies, PAL C64. {6-6}
; The night watchman walks to and fro, the crow flies on a {6-6}
; wave, the cat jumps at Oscar; a touch takes two notches {6-6}
; of health and throws him back; he blinks, safe, for a {6-6}
; moment; with no health left, back at the lantern. {6-6}
; DREADCASTLE 07 - the staff, PAL C64. {7-7}
; Level 3, the Wild Wood, with its own characters, its {7-7}
; moon and its brambles that hurt; the staff of the Count {7-7}
; lies on the path: taken, Fire strikes with it, and a {7-7}
; struck enemy vanishes in a puff. {7-7}
; DREADCASTLE 08 - the packed levels, PAL C64. {8-8}
; Levels 4 to 6, the Black Mire, the Grey Crags and the {8-8}
; Frozen Pass. The maps, the tables and the sets of {8-8}
; characters of all the levels are kept packed, and {8-8}
; unpacked a page a frame; the will-o'-the-wisps of the {8-8}
; mire and the spikes of ice flicker and hurt. {8-8}
; DREADCASTLE 09 - the castle, PAL C64. {9-9}
; Levels 7 and 8, Dreadcastle Gate and the Throne Tower: {9-9}
; stone and lit windows on a blue sky, the spikes of iron {9-9}
; and the fire. {9-9}
; DREADCASTLE 10 - Tom Darkfang, PAL C64. {10-10}
; The door of the throne room leads to Tom's arena: he {10-10}
; leaps and charges; struck eight times with the staff, {10-10}
; he runs away through the window. {10-10}
; DREADCASTLE 11 - the music, PAL C64. {11-11}
; The theme in a loop in the levels; in the arena Tom's, {11-11}
; tense and fast, until he is beaten: three voices of the {11-11}
; SID, a frame of music at every top interrupt. {11-11}
; DREADCASTLE 12 - the title and the ends, PAL C64. {12-12}
; The title over the castle's door, with its menu (MUSIC, {12-12}
; SOUND FX, SILENT); the count of the night left at the {12-12}
; gate; the victory in the arena; dawn, when the night is {12-12}
; over: the game is over. The score. {12-12}
; DREADCASTLE 13 - the complete game, PAL C64. {13}
; The title: the name over the castle's door, the menu {13}
; (MUSIC, SOUND FX, SILENT: Up and Down), Fire: the game. {13}
; Eight levels: the Village of Mortals, the Churchyard, {13}
; the Wild Wood, the Black Mire, the Grey Crags, the {13}
; Frozen Pass, Dreadcastle Gate and the Throne Tower: 128 {13}
; metatile columns each, from the start to the gate. Oscar {13}
; walks and jumps with joystick 2 (Up to jump, held {13}
; longer, higher); Up and Fire together turn him into a {13}
; bat, Down and Fire back; the bat beats its wings (Up), {13}
; falls when let go, dives with Down and eats the moths of {13}
; the sky. Three heirlooms to take in each level; the {13}
; lantern of the checkpoint; the gate opens with all {13}
; three; through it LEVEL CLEAR, the night left into the {13}
; score, and the next level; in level 8 the door of the {13}
; throne room leads to Tom Darkfang: he leaps and charges; {13}
; struck eight times, he runs away through the window: the {13}
; victory, the night left into the score; Fire, the title. {13}
; A fall into a pit or into water: back at the lantern, or {13}
; at the start. The enemies (sprites 3-6): the watchman {13}
; walks to and fro, the crow flies on a wave, the cat {13}
; jumps at Oscar; a touch takes two notches of health and {13}
; throws him back; he blinks, safe, for a moment; with no {13}
; health left, back at the lantern. In the wood the staff {13}
; of the Count lies on the path: taken, Fire strikes with {13}
; it, and a struck enemy vanishes in a puff until Oscar {13}
; starts again; the brambles hurt as a touch; his head {13}
; stops under the blocks. In the mire the {13}
; will-o'-the-wisps flicker and hurt as a touch; in the {13}
; mountain the spikes of ice glint and hurt, in the castle {13}
; the spikes of iron and the fire. The night: two minutes {13}
; a level; at dawn the sky lightens, Oscar vanishes in a {13}
; puff of smoke: the game is over; Fire, the title. The {13}
; score: an enemy struck 100, an heirloom 500, a moth 10, {13}
; Tom 5000, a step of the night left 50. The theme plays {13}
; in a loop; in the arena Tom's, tense and fast, until he {13}
; is beaten; a jingle at the gate, at the victory, at {13}
; dawn; with SOUND FX the sound effects. {13}
; Assemble this file: it includes the others.
; With -D RECORD_SONG=1 the program plays Tom's theme from {11-12}
; the start, to record it. {11-12}
; With -D RECORD_SONG=N the program plays song N from the {13}
; start (1 Tom's theme, 2-4 the jingles); with {13}
; -D RECORD_SFX=1 the sound effects one after the other {13}
; (tools/record_music.py records them). {13}
        .cpu "6502"
        .weak ; {11}
RECORD_SONG   = 0               ; 0: the game as it is {11}
RECORD_SFX    = 0 ; {13}
        .endweak ; {11}
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
        lda #$36                ; BASIC out; I/O, KERNAL in {8}
        sta $01 ; {8}
        jsr move_high           ; the packed data under it {8}
;|        jsr kernal_out          ; the KERNAL out {-7}
        jsr kernal_out          ; and the KERNAL out {8}
        jsr init_states         ; the title, MUSIC {12}
        jsr init_tom            ; none of Tom yet {10}
        lda #TITLE_LEVEL        ; the title: level 7 at its {12}
        sta level_no            ; end {12}
;|        lda #0                  ; level 1 {-11}
;|        sta level_no ; {-11}
        lda #0                  ; no staff yet {12}
        sta has_staff ; {12}
;|        sta has_staff           ; no staff yet {7-11}
        jsr load_level          ; its map, its setting
        jsr init_vic
        jsr init_scroll
        jsr title_place         ; Oscar, camera, menu {12}
;|        jsr respawn             ; Oscar at the start {-11}
        lda #0                  ; screen A, colour RAM
        sta col_screen
        lda #39
        sta col_end
        jsr draw_columns
;|        jsr draw_hud            ; the HUD's rows {-11}
;|        jsr show_name           ; the level's name {-11}
        jsr init_sprites
;|        jsr reset_enemies       ; at their start {6-11}
;|        jsr place_oscar ; {-11}
        jsr title_sprites       ; the name, the moon {12}
        jsr music_init          ; silence; the song's start {11}
;|        .if RECORD_SONG != 0 ; {11-12}
        .if RECORD_SONG + RECORD_SFX != 0 ; {13}
        jsr music_stop          ; to record: silence {11}
        .fi                     ; till the interrupts are on {11}
        jsr init_irq            ; the interrupts on
        .if RECORD_SONG != 0 ; {11}
        lda #RECORD_SONG        ; that song, from its start {11}
        jsr music_start ; {11}
        .fi ; {11}
        .if RECORD_SFX != 0     ; every effect, one {13}
        lda #SOUND_FX           ; each FX_REEL_FRAMES frames {13}
        sta sound_mode ; {13}
        ldx #0                  ; X: the effect {13}
_reel: ; {13}
        lda frame_count ; {13}
        clc ; {13}
        adc #FX_REEL_FRAMES ; {13}
        sta work ; {13}
        txa ; {13}
        jsr sfx_start           ; (it keeps X) {13}
_wait: ; {13}
        lda frame_count ; {13}
        cmp work ; {13}
        bne _wait ; {13}
        inx ; {13}
        cpx #FX_COUNT ; {13}
        bne _reel ; {13}
_rest: ; {13}
        jmp _rest               ; then nothing more {13}
        .fi ; {13}

; The main loop: one turn a frame, from the HUD down. {1-1}
; Nothing moves yet: the turn is empty. {1-1}
; The main loop: one turn a frame, from the HUD down: the {2-2}
; joystick moves the camera. {2-2}
; The main loop: one turn a frame, from the HUD down. In a {3}
; transition (trans not 0) only its step; after a fall, {3}
; only the HUD. {3-9}
; only the HUD; in the arena Tom instead of the enemies {10}
; and the level's things. {10-11}
; and the level's things; out of the game (the title, the {12}
; count, the victory, dawn) the state's turn. {12}
frame_loop:
        jsr wait_hud
        jsr read_joystick ; {2}
joy_ready:                      ; the tests set joy here {2}
        lda frame_count         ; this turn's frame {8}
        sta turn_frame ; {8}
        lda trans ; {3}
        bne _between ; {3}
        lda game_state          ; not playing {12}
        bne _state ; {12}
        jsr flutter_moths ; {4}
;|        jsr steer_camera ; {2-2}
        jsr move_oscar ; {3}
        lda trans               ; fallen? {3}
        bne _fallen ; {3}
        jsr animate_oscar ; {3}
        jsr follow_camera ; {3}
        jsr place_oscar ; {3}
        jsr place_staff ; {7}
        lda swap ; {2}
        beq + ; {2}
        jsr do_swap             ; the back screen in front: {2}
        jmp _after              ; the colour RAM first {2}
+       jsr prepare_back        ; else a step of the next {2}
_after:                         ; after the screens {2}
        lda arena ; {10}
        bne _tom ; {10}
        jsr move_enemies ; {6}
        jsr hit_enemies ; {6}
        lda trans               ; no health left? {6}
        bne _fallen ; {6}
        jsr place_enemies ; {6}
        jsr touch_things ; {5}
        jsr tick_night ; {5}
        jsr show_hud ; {3}
        jsr place_heirloom ; {5}
        jsr flicker_hazards     ; after the colour RAM {8}
        jmp frame_done ; {3}
_tom: ; {10}
        jsr fight_tom           ; he moves, struck, touches {10}
        lda trans               ; no health left, or gone? {10}
        bne _fallen ; {10}
        jsr place_tom ; {10}
        jsr tick_night ; {10}
        jsr show_hud ; {10}
        jsr flicker_hazards ; {10}
        jmp frame_done ; {10}
_fallen: ; {3}
        jsr show_hud ; {3}
        jmp frame_done ; {3}
_state: ; {12}
        jsr state_turn ; {12}
        jmp frame_done ; {12}
_between: ; {3}
        jsr transition ; {3}
frame_done:                     ; the tests compare here
        jmp frame_loop

; Joystick 2: CIA 1, port A, bits 0-4 low when pushed. {2}
; In joy they are turned round: bit set = pushed. {2}
read_joystick: ; {2}
        lda $dc00 ; {2}
        eor #$ff ; {2}
        and #%00011111          ; fire right left down up {2}
        sta joy ; {2}
        rts ; {2}

        .include "vic.asm"
        .include "oscar.asm"
        .include "bat.asm" ; {4}
        .include "enemies.asm" ; {6}
        .include "tom.asm" ; {10}
        .include "staff.asm" ; {7}
        .include "objects.asm" ; {3}
        .include "irq.asm"
        .include "player.asm" ; {11}
        .include "effects.asm" ; {13}
        .include "level.asm"
        .include "scroll.asm"
        .include "data.asm"
