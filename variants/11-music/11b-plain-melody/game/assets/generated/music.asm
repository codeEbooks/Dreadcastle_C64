; Written by game/assets/music.py from score.py and
; boss.py: do not edit.

MUSIC_TEMPO_STEPS = 4
MUSIC_GATE_TICK = 2
MUSIC_HIGHEST = 93
MUSIC_SONGS = 5
SONG_THEME = 0
SONG_THEME_FRAMES = 2432
SONG_BOSS = 1
SONG_BOSS_FRAMES = 1224
SONG_CLEAR = 2
SONG_CLEAR_FRAMES = 95
SONG_WON = 3
SONG_WON_FRAMES = 264
SONG_DAWN = 4
SONG_DAWN_FRAMES = 168
SONG_END = $fd

freq_lo:
        .byte $16, $27, $39, $4b, $5f, $74, $8a, $a1
        .byte $ba, $d4, $f0, $0e, $2d, $4e, $71, $96
        .byte $be, $e7, $14, $42, $74, $a9, $e0, $1b
        .byte $5a, $9c, $e2, $2d, $7b, $cf, $27, $85
        .byte $e8, $51, $c1, $37, $b4, $38, $c4, $59
        .byte $f7, $9d, $4e, $0a, $d0, $a2, $81, $6d
        .byte $67, $70, $89, $b2, $ed, $3b, $9c, $13
        .byte $a0, $45, $02, $da, $ce, $e0, $11, $64
        .byte $da, $76, $39, $26, $40, $89, $04, $b4
        .byte $9c, $c0, $23, $c8, $b4, $eb, $72, $4c
        .byte $80, $12, $08, $68, $39, $80, $45, $90
        .byte $68, $d6, $e3, $99, $00, $24
freq_hi:
        .byte $01, $01, $01, $01, $01, $01, $01, $01
        .byte $01, $01, $01, $02, $02, $02, $02, $02
        .byte $02, $02, $03, $03, $03, $03, $03, $04
        .byte $04, $04, $04, $05, $05, $05, $06, $06
        .byte $06, $07, $07, $08, $08, $09, $09, $0a
        .byte $0a, $0b, $0c, $0d, $0d, $0e, $0f, $10
        .byte $11, $12, $13, $14, $15, $17, $18, $1a
        .byte $1b, $1d, $1f, $20, $22, $24, $27, $29
        .byte $2b, $2e, $31, $34, $37, $3a, $3e, $41
        .byte $45, $49, $4e, $52, $57, $5c, $62, $68
        .byte $6e, $75, $7c, $83, $8b, $93, $9c, $a5
        .byte $af, $b9, $c4, $d0, $dd, $ea
tempo_table:
        .byte $05, $05, $05, $04, $04, $04, $04, $05
        .byte $05, $05, $05, $04, $06, $05, $06, $05
        .byte $06, $06, $06, $06
song_lists:
        .byte $00, $03, $06, $09, $0c
ins_ad:
        .byte $0a, $06, $05, $05, $05, $05, $05, $06
        .byte $08, $29, $0a
ins_sr:
        .byte $a8, $c4, $00, $00, $00, $00, $00, $00
        .byte $a6, $98, $4a
ins_wave:
        .byte $00, $00, $04, $08, $0c, $10, $14, $1a
        .byte $00, $02, $00
ins_pw_lo:
        .byte $00, $00, $00, $00, $00, $00, $00, $00
        .byte $00, $00, $00
ins_pw_hi:
        .byte $08, $06, $04, $04, $04, $04, $08, $08
        .byte $06, $08, $08
ins_sweep:
        .byte $18, $00, $10, $10, $10, $10, $00, $00
        .byte $30, $00, $10
ins_vibrato:
        .byte $00, $00, $00, $00, $00, $00, $00, $00
        .byte $00, $0c, $12
wave_ctrl:
        .byte $40, $ff, $20, $ff, $40, $40, $40, $ff
        .byte $40, $40, $40, $ff, $40, $40, $40, $ff
        .byte $40, $40, $40, $ff, $40, $10, $10, $10
        .byte $10, $ff, $80, $40, $80, $80, $ff
wave_pitch:
        .byte $00, $00, $00, $02, $00, $03, $07, $04
        .byte $00, $04, $07, $08, $00, $03, $06, $0c
        .byte $00, $04, $0a, $10, $b0, $a4, $9e, $9a
        .byte $96, $18, $d4, $a8, $cc, $c8, $1d
pattern_lo:
        .byte <pat_0
        .byte <pat_1
        .byte <pat_2
        .byte <pat_3
        .byte <pat_4
        .byte <pat_5
        .byte <pat_6
        .byte <pat_7
        .byte <pat_8
        .byte <pat_9
        .byte <pat_10
        .byte <pat_11
        .byte <pat_12
        .byte <pat_13
        .byte <pat_14
        .byte <pat_15
        .byte <pat_16
        .byte <pat_17
        .byte <pat_18
        .byte <pat_19
        .byte <pat_20
        .byte <pat_21
        .byte <pat_22
        .byte <pat_23
        .byte <pat_24
        .byte <pat_25
        .byte <pat_26
        .byte <pat_27
        .byte <pat_28
        .byte <pat_29
pattern_hi:
        .byte >pat_0
        .byte >pat_1
        .byte >pat_2
        .byte >pat_3
        .byte >pat_4
        .byte >pat_5
        .byte >pat_6
        .byte >pat_7
        .byte >pat_8
        .byte >pat_9
        .byte >pat_10
        .byte >pat_11
        .byte >pat_12
        .byte >pat_13
        .byte >pat_14
        .byte >pat_15
        .byte >pat_16
        .byte >pat_17
        .byte >pat_18
        .byte >pat_19
        .byte >pat_20
        .byte >pat_21
        .byte >pat_22
        .byte >pat_23
        .byte >pat_24
        .byte >pat_25
        .byte >pat_26
        .byte >pat_27
        .byte >pat_28
        .byte >pat_29
order_lo:
        .byte <order_0
        .byte <order_1
        .byte <order_2
        .byte <order_3
        .byte <order_4
        .byte <order_5
        .byte <order_6
        .byte <order_7
        .byte <order_8
        .byte <order_9
        .byte <order_10
        .byte <order_11
        .byte <order_12
        .byte <order_13
        .byte <order_14
order_hi:
        .byte >order_0
        .byte >order_1
        .byte >order_2
        .byte >order_3
        .byte >order_4
        .byte >order_5
        .byte >order_6
        .byte >order_7
        .byte >order_8
        .byte >order_9
        .byte >order_10
        .byte >order_11
        .byte >order_12
        .byte >order_13
        .byte >order_14
; pattern 0: lead_intro
pat_0:
        .byte $bf, $60, $ff
; pattern 1: lead_a
pat_1:
        .byte $c0, $83, $3b, $40, $81, $43, $42, $83
        .byte $40, $81, $3f, $40, $42, $43, $87, $47
        .byte $83, $48, $81, $47, $45, $83, $40, $3c
        .byte $81, $3b, $3c, $83, $40, $87, $39, $83
        .byte $43, $81, $40, $43, $85, $48, $81, $47
        .byte $45, $43, $83, $42, $3f, $3b, $81, $40
        .byte $42, $43, $45, $83, $47, $43, $42, $3f
        .byte $87, $3b, $ff
; pattern 2: lead_b
pat_2:
        .byte $c0, $83, $4a, $81, $47, $43, $83, $4a
        .byte $4c, $4e, $81, $4c, $4a, $87, $45, $81
        .byte $43, $45, $83, $47, $4c, $47, $48, $81
        .byte $47, $45, $83, $43, $40, $81, $45, $47
        .byte $83, $48, $4c, $48, $4a, $81, $48, $47
        .byte $83, $45, $42, $4b, $47, $42, $3f, $8b
        .byte $47, $83, $60, $ff
; pattern 3: lead_a2
pat_3:
        .byte $c0, $83, $3b, $40, $81, $43, $42, $83
        .byte $40, $81, $3f, $40, $42, $43, $87, $47
        .byte $83, $48, $81, $47, $45, $83, $40, $3c
        .byte $81, $3b, $3c, $83, $40, $87, $39, $83
        .byte $43, $81, $40, $43, $85, $48, $81, $47
        .byte $45, $43, $83, $42, $3f, $3b, $81, $40
        .byte $42, $43, $47, $83, $4c, $4b, $8b, $4c
        .byte $83, $60, $ff
; pattern 4: lead_bridge
pat_4:
        .byte $c0, $83, $3c, $40, $43, $48, $47, $45
        .byte $87, $40, $83, $42, $45, $48, $4b, $87
        .byte $4e, $83, $4b, $47, $ff
; pattern 5: bass
pat_5:
        .byte $c1, $81, $1c, $28, $1c, $28, $1c, $28
        .byte $1c, $28, $ff
; pattern 6: arps_minor
pat_6:
        .byte $c2, $81, $34, $34, $34, $34, $34, $34
        .byte $34, $34, $ff
; pattern 7: minor
pat_7:
        .byte $c6, $80, $34, $c2, $82, $34, $c7, $80
        .byte $34, $c2, $82, $34, $c6, $80, $34, $c2
        .byte $82, $34, $c7, $80, $34, $c2, $82, $34
        .byte $ff
; pattern 8: major
pat_8:
        .byte $c6, $80, $34, $c3, $82, $34, $c7, $80
        .byte $34, $c3, $82, $34, $c6, $80, $34, $c3
        .byte $82, $34, $c7, $80, $34, $c3, $82, $34
        .byte $ff
; pattern 9: dim
pat_9:
        .byte $c6, $80, $34, $c4, $82, $34, $c7, $80
        .byte $34, $c4, $82, $34, $c6, $80, $34, $c4
        .byte $82, $34, $c7, $80, $34, $c4, $82, $34
        .byte $ff
; pattern 10: dom7
pat_10:
        .byte $c6, $80, $34, $c5, $82, $34, $c7, $80
        .byte $34, $c5, $82, $34, $c6, $80, $34, $c5
        .byte $82, $34, $c7, $80, $34, $c5, $82, $34
        .byte $ff
order_0:
        .byte $00, $00, $01, $00, $02, $00, $03, $00
        .byte $04, $00, $fe, $01
order_1:
        .byte $05, $00, $05, $00, $05, $fc, $05, $07
        .byte $05, $00, $05, $00, $05, $05, $05, $05
        .byte $05, $fc, $05, $07, $05, $00, $05, $07
        .byte $05, $03, $05, $fe, $05, $00, $05, $fc
        .byte $05, $05, $05, $fe, $05, $07, $05, $07
        .byte $05, $00, $05, $00, $05, $05, $05, $05
        .byte $05, $fc, $05, $07, $05, $00, $05, $00
        .byte $05, $fc, $05, $05, $05, $02, $05, $07
        .byte $fe, $04
order_2:
        .byte $06, $00, $06, $00, $08, $fc, $0a, $07
        .byte $07, $00, $07, $00, $07, $05, $07, $05
        .byte $08, $fc, $0a, $07, $07, $00, $0a, $07
        .byte $08, $03, $08, $fe, $07, $00, $08, $fc
        .byte $07, $05, $08, $fe, $0a, $07, $0a, $07
        .byte $07, $00, $07, $00, $07, $05, $07, $05
        .byte $08, $fc, $0a, $07, $07, $00, $07, $00
        .byte $08, $fc, $07, $05, $09, $02, $0a, $07
        .byte $fe, $04
