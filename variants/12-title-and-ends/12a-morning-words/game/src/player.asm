; The music player: three voices of the SID, one frame of
; music at every top interrupt.
;
; The SID's registers can only be written: the player keeps
; a copy of all 25 (sid_shadow), works on the copy, and at
; the next frame copies it into the SID, always at the same
; moment of the frame. The tests read the copy.
;
; Time goes by steps (a semiquaver), each of 5, 5, 5 and 4
; frames in turn (tempo_table). A voice reads its pattern
; when its note is over: a note, or a rest, and before them
; a duration or an instrument. At the end of a pattern, the
; voice's order list gives the next pattern and how many
; semitones to move it; at the end of the list, $fe and the
; entry to start again from. In every frame each voice reads
; a row of its instrument's wavetable: a waveform, and a
; pitch above its note or a fixed note (arpeggios, drums);
; long notes waver (vibrato); the pulse width sweeps up and
; down between PW_LOW and PW_HIGH.
;
; Two songs: the theme (song 0) and Tom's (song 1, its
; patterns and order lists under the KERNAL: the player
; only meets them with the KERNAL out).
; Each song has its three order lists (order_lo, order_hi:
; song 0's, then song 1's, and on; song_lists: where a
; song's start) and its tempo (tempo_table: four steps
; each). music_start plays a song from its start;
; music_stop lets the notes go and stops (the copy into the
; SID goes on).

SID           = $d400
PW_LOW        = $0200           ; the pulse width sweeps
PW_HIGH       = $0e00           ; between these two
REST          = $60             ; a pattern byte: a rest
        .cerror MUSIC_TEMPO_STEPS != 4, "tempo: 4 steps"
        .cerror MUSIC_SONGS != 5, "five songs"

; Silence, and every voice at the start of its order list:
; the theme.
music_init:
        ldx #24
        lda #0
-       sta sid_shadow,x        ; all the registers 0
        dex
        bpl -
        lda #%00001111          ; volume 15, no filter
        sta sid_shadow + 24
        lda #0
        sta mus_frame
        sta mus_frame + 1
        sta mus_song            ; SONG_THEME
        jmp start_song

; Song A from its start, the interrupts held: the notes
; playing let go (their gates off in the copy), then the
; new ones start in the next frame.
music_start:
        php
        sei
        sta mus_song
        jsr gates_off
        jsr start_song
        plp
        rts

; The notes let go, and no more: the player stops (until
; music_start).
music_stop:
        php
        sei
        lda #0
        sta mus_on
        jsr gates_off
        plp
        rts

gates_off:
        ldx #2
-       ldy voice_regs,x        ; the control register of
        lda sid_shadow + 4,y    ; each voice: the gate off
        and #%11111110
        sta sid_shadow + 4,y
        dex
        bpl -
        rts

; Every voice at the start of its order list of mus_song;
; playing.
start_song:
        lda #1                  ; the first frame starts
        sta mus_tick            ; a step
        sta mus_on
        lda #0
        sta mus_tempo
        ldx #2                  ; voices 2, 1, 0
_voice:
        lda #0
        sta v_order,x
        sta v_ins,x
        sta v_note,x
        sta v_gate,x
        sta v_wave,x
        sta v_ctrl,x
        sta v_pw_lo,x
        sta v_pw_hi,x
        sta v_sweep,x
        sta v_vib,x
        lda #1                  ; a step to wait: the notes
        sta v_dur,x             ; start in the first frame
        sta v_left,x
        jsr load_order
        dex
        bpl _voice
        rts

; One frame, from the top interrupt; stopped, only the
; copy.
music_play:
        ldx #24                 ; the copy into the SID,
-       lda sid_shadow,x        ; from the top: each voice's
        sta SID,x               ; ADSR before its control
        dex
        bpl -
        lda mus_on
        bne +
        rts
+       inc mus_frame
        bne +
        inc mus_frame + 1
+       dec mus_tick
        bne _frame
        lda mus_song            ; a new step: the song's
        asl a                   ; tempo, four steps a song
        asl a
        ora mus_tempo
        tax
        lda tempo_table,x
        sta mus_tick
        inc mus_tempo
        lda mus_tempo
        and #MUSIC_TEMPO_STEPS - 1
        sta mus_tempo
        ldx #2
-       dec v_left,x            ; a note over: read on
        bne +
        jsr read_events
+       dex
        bpl -
_frame:
        ldx #2
-       jsr voice_frame
        dex
        bpl -
        rts

; Voice X: the pattern and the transposition of entry
; v_order of its order list (the song's); $fe: start again
; from the entry that follows it.
load_order:
        txa                     ; the song's lists
        ldy mus_song
        clc
        adc song_lists,y
        tay
        lda order_lo,y
        sta mus_ptr
        lda order_hi,y
        sta mus_ptr + 1
        lda v_order,x
        asl a                   ; two bytes an entry
        tay
        lda (mus_ptr),y
        cmp #$fe
        bne +
        iny                     ; the end: back to the entry
        lda (mus_ptr),y
        sta v_order,x
        asl a
        tay
        lda (mus_ptr),y
+       sta mus_work            ; the pattern
        iny
        lda (mus_ptr),y
        sta v_trans,x           ; its transposition
        ldy mus_work
        lda pattern_lo,y
        sta v_ptr_lo,x
        lda pattern_hi,y
        sta v_ptr_hi,x
        rts

; Voice X: read its pattern up to a note or a rest.
read_events:
        lda v_ptr_lo,x
        sta mus_ptr
        lda v_ptr_hi,x
        sta mus_ptr + 1
        ldy #0
_next:
        lda (mus_ptr),y
        iny
        cmp #$ff
        bne _event
        inc v_order,x           ; end of the pattern: the
        jsr load_order          ; next entry of the list
        lda v_ptr_lo,x
        sta mus_ptr
        lda v_ptr_hi,x
        sta mus_ptr + 1
        ldy #0
        beq _next
_event:
        cmp #$c0
        bcc +
        and #%00011111          ; an instrument
        sta v_ins,x
        jmp _next
+       cmp #$80
        bcc +
        and #%00111111          ; a duration
        clc
        adc #1
        sta v_dur,x
        jmp _next
+       sta mus_work            ; a note or a rest
        tya                     ; the pattern goes on here
        clc
        adc mus_ptr
        sta v_ptr_lo,x
        lda mus_ptr + 1
        adc #0
        sta v_ptr_hi,x
        lda v_dur,x
        sta v_left,x
        lda mus_work
        cmp #REST
        bne _note
        lda #0                  ; a rest: the gate off
        sta v_gate,x
        rts
_note:
        clc
        adc v_trans,x
        sta v_note,x
        lda #1                  ; a note: the gate on, and
        sta v_gate,x            ; the instrument restarts
        ldy v_ins,x
        lda ins_wave,y
        sta v_wave,x
        lda ins_pw_lo,y
        sta v_pw_lo,x
        lda ins_pw_hi,y
        sta v_pw_hi,x
        lda ins_sweep,y
        sta v_sweep,x
        lda ins_vibrato,y
        sta v_vib,x
        rts

; Voice X, one frame: gate, wavetable, frequency, vibrato,
; pulse width; then its seven registers in the copy.
voice_frame:
        lda v_left,x            ; in the last frames of the
        cmp #1                  ; note the gate is off, so
        bne +                   ; that the next one starts
        lda mus_tick
        cmp #MUSIC_GATE_TICK + 1
        bcs +
        lda #0
        sta v_gate,x
+       ldy v_wave,x            ; the wavetable row
        lda wave_ctrl,y
        cmp #$ff
        bne +
        lda wave_pitch,y        ; $ff: jump
        tay
        lda wave_ctrl,y
+       sta v_ctrl,x
        lda wave_pitch,y
        bmi _fixed
        clc                     ; semitones above the note
        adc v_note,x
        jmp _pitch
_fixed:
        and #%01111111          ; a fixed note
_pitch:
        sta mus_note
        iny
        tya
        sta v_wave,x            ; next frame: the next row
        ldy mus_note
        lda freq_lo,y
        sta mus_freq
        lda freq_hi,y
        sta mus_freq + 1
        ldy v_ins,x             ; vibrato, after a delay
        lda ins_vibrato,y
        beq _pulse
        lda v_vib,x
        beq _wobble
        dec v_vib,x
        jmp _pulse
_wobble:
        lda mus_freq + 1        ; a step: frequency / 256
        sta mus_work
        lda mus_frame
        and #%00000111
        tay
        lda vibrato_table,y     ; -2 to 2 steps
        beq _pulse
        bmi _down
        tay
-       clc
        lda mus_freq
        adc mus_work
        sta mus_freq
        bcc +
        inc mus_freq + 1
+       dey
        bne -
        beq _pulse
_down:
        eor #$ff                ; how many: -A
        clc
        adc #1
        tay
-       sec
        lda mus_freq
        sbc mus_work
        sta mus_freq
        bcs +
        dec mus_freq + 1
+       dey
        bne -
_pulse:
        lda v_sweep,x           ; the pulse width sweeps
        beq _copy
        bmi _narrower
        clc                     ; wider
        adc v_pw_lo,x
        sta v_pw_lo,x
        lda v_pw_hi,x
        adc #0
        sta v_pw_hi,x
        cmp #>PW_HIGH
        bcc _copy
        lda #<PW_HIGH           ; at the top: turn back
        sta v_pw_lo,x
        lda #>PW_HIGH
        sta v_pw_hi,x
        jmp _turn
_narrower:
        clc                     ; narrower: sweep < 0
        adc v_pw_lo,x
        sta v_pw_lo,x
        lda v_pw_hi,x
        adc #$ff
        sta v_pw_hi,x
        cmp #>PW_LOW
        bcs _copy
        lda #<PW_LOW            ; at the bottom: turn back
        sta v_pw_lo,x
        lda #>PW_LOW
        sta v_pw_hi,x
_turn:
        lda v_sweep,x
        eor #$ff
        clc
        adc #1
        sta v_sweep,x
_copy:
        ldy v_ins,x             ; ADSR of the instrument
        lda ins_ad,y
        pha
        lda ins_sr,y
        pha
        ldy voice_regs,x        ; the voice's 7 registers
        lda mus_freq
        sta sid_shadow,y
        lda mus_freq + 1
        sta sid_shadow + 1,y
        lda v_pw_lo,x
        sta sid_shadow + 2,y
        lda v_pw_hi,x
        sta sid_shadow + 3,y
        lda v_ctrl,x
        ora v_gate,x            ; gate: bit 0
        sta sid_shadow + 4,y
        pla
        sta sid_shadow + 6,y    ; sustain and release
        pla
        sta sid_shadow + 5,y    ; attack and decay
        rts

voice_regs:
        .byte 0, 7, 14
vibrato_table:
        .byte 0, 1, 2, 1, 0, $ff, $fe, $ff
