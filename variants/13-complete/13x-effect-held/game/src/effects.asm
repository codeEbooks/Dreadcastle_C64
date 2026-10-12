; The sound effects: classic and short, fifteen of them
; (sfx.py). They play only
; with SOUND FX, and not while a jingle plays: the menu's
; choices are kept apart, as in volume 2 (the jingles are
; the exception: they play with MUSIC and with SOUND FX).
;
; The game calls sfx_start with the effect's number (FX_*)
; where the thing happens. The effect takes a voice, the
; one after the voice the last one took (0, 1, 2, then 0
; again): three can sound together, and a fourth stops the
; oldest. Its data (sfx_data, under the KERNAL) are a
; header and rows: the header its frames a row, attack and
; decay, sustain and release, its pulse width; a row a
; waveform with the gate on and a note (the music's
; frequency table). At every top interrupt, after the
; music, sfx_play writes the next row of each voice into
; the copy of the SID's registers (sid_shadow), which the
; music player copies into the SID in the next frame; after
; the last row, the gate off: the sound fades with its
; release.

; Effect A, from the main loop: with SOUND FX, no music
; playing. Its voice: the gate off in the copy (the effect
; starts again from its attack in the next frame), its
; envelope and pulse width; its first row in the next top
; interrupt. The interrupts held: the player reads these.
; X and Y kept (the game calls it in its loops).
sfx_start:
        stx sfx_keep
        sty sfx_keep + 1
        ldx sound_mode          ; SOUND FX only
        cpx #SOUND_FX
        bne _done
        php
        sei
        ldx mus_on              ; a jingle playing: none
        bne _held
        tax                     ; X: the effect
        ldy sfx_last            ; Y: the voice after the
        iny                     ; last one's
        cpy #3
        bcc +
        ldy #0
+       sty sfx_last
        lda sfx_first,x         ; X: its data
        tax
        lda sfx_data,x          ; its frames a row
        sta sfx_speed,y
        lda #1                  ; its first row: next frame
        sta sfx_tick,y
        txa
        clc
        adc #FX_HEADER
        sta sfx_pos,y
        lda voice_regs,y        ; Y: the voice's registers
        tay
        lda sfx_data + 1,x      ; attack and decay
        sta sid_shadow + 5,y
        lda sfx_data + 2,x      ; sustain and release
        sta sid_shadow + 6,y
        lda sfx_data + 3,x      ; the pulse width
        sta sid_shadow + 3,y
        lda #0
        sta sid_shadow + 2,y
        sta sid_shadow + 4,y    ; the gate off
_held:
        plp
_done:
        ldx sfx_keep
        ldy sfx_keep + 1
        rts

; A frame of the effects (the top interrupt, after the
; music): in each voice with an effect, its frames a row
; over, the next row into the copy; none left, the gate
; off and the voice free. Not while music plays.
sfx_play:
        lda mus_on
        bne _done
        ldx #2
_voice:
        lda sfx_pos,x           ; 0: no effect
        beq _next
        dec sfx_tick,x
        bne _next
        lda sfx_speed,x
        sta sfx_tick,x
        ldy sfx_pos,x
        lda sfx_data,y          ; the waveform, gate on
        beq _end                ; 0: the end
        sta mus_work
        lda sfx_data + 1,y      ; the note
        tay
        lda freq_lo,y           ; its frequency
        sta mus_freq
        lda freq_hi,y
        sta mus_freq + 1
        ldy voice_regs,x
        lda mus_freq
        sta sid_shadow,y
        lda mus_freq + 1
        sta sid_shadow + 1,y
        lda mus_work
        sta sid_shadow + 4,y
        lda sfx_pos,x           ; the next row
        clc
        adc #2
        sta sfx_pos,x
_next:
        dex
        bpl _voice
_done:
        rts
_end:
        sta sfx_pos,x           ; (0) the voice free
        ldy voice_regs,x
        lda sid_shadow + 4,y    ; the gate off
        and #%11111111
        sta sid_shadow + 4,y
        jmp _next
