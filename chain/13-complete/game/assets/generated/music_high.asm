; Written by game/assets/music.py from boss.py and
; jingles.py: do not edit. Under the KERNAL: song 1,
; Tom's theme; songs 2-4, the jingles.

; pattern 11: boss_lead_intro
pat_11:
        .byte $9f, $60, $ff
; pattern 12: boss_lead_a
pat_12:
        .byte $c8, $81, $40, $80, $60, $40, $81, $43
        .byte $40, $47, $45, $43, $42, $40, $80, $60
        .byte $40, $81, $43, $47, $83, $4c, $4b, $81
        .byte $4c, $80, $60, $4c, $81, $4a, $48, $47
        .byte $48, $47, $43, $42, $80, $60, $42, $81
        .byte $45, $48, $83, $4b, $47, $81, $40, $80
        .byte $60, $40, $81, $43, $40, $47, $45, $43
        .byte $42, $43, $45, $47, $4c, $83, $4f, $4e
        .byte $81, $4d, $4c, $48, $45, $41, $45, $48
        .byte $4c, $83, $4b, $81, $47, $42, $83, $3f
        .byte $3b, $ff
; pattern 13: boss_lead_b
pat_13:
        .byte $c8, $81, $45, $80, $60, $45, $81, $48
        .byte $45, $4c, $4a, $48, $47, $45, $48, $4c
        .byte $51, $83, $4f, $4c, $81, $4f, $80, $60
        .byte $4f, $81, $4e, $4c, $47, $4c, $4b, $47
        .byte $87, $4c, $83, $60, $81, $47, $48, $48
        .byte $80, $60, $48, $81, $4c, $4f, $4e, $4c
        .byte $4a, $48, $51, $80, $60, $51, $81, $4e
        .byte $48, $83, $4b, $4e, $81, $47, $4b, $4e
        .byte $51, $83, $53, $51, $4e, $4b, $47, $60
        .byte $ff
; pattern 14: boss_bass
pat_14:
        .byte $c1, $80, $1c, $1c, $28, $1c, $1c, $1c
        .byte $28, $1c, $1c, $1c, $28, $1c, $1c, $28
        .byte $1c, $28, $ff
; pattern 15: boss_minor
pat_15:
        .byte $c6, $80, $34, $c2, $82, $34, $c7, $80
        .byte $34, $c2, $82, $34, $c6, $80, $34, $c2
        .byte $82, $34, $c7, $80, $34, $c2, $34, $c7
        .byte $34, $34, $ff
; pattern 16: boss_major
pat_16:
        .byte $c6, $80, $34, $c3, $82, $34, $c7, $80
        .byte $34, $c3, $82, $34, $c6, $80, $34, $c3
        .byte $82, $34, $c7, $80, $34, $c3, $34, $c7
        .byte $34, $34, $ff
; pattern 17: boss_dom7
pat_17:
        .byte $c6, $80, $34, $c5, $82, $34, $c7, $80
        .byte $34, $c5, $82, $34, $c6, $80, $34, $c5
        .byte $82, $34, $c7, $80, $34, $c5, $34, $c7
        .byte $34, $34, $ff
; pattern 18: boss_dim
pat_18:
        .byte $c6, $80, $34, $c4, $82, $34, $c7, $80
        .byte $34, $c4, $82, $34, $c6, $80, $34, $c4
        .byte $82, $34, $c7, $80, $34, $c4, $34, $c7
        .byte $34, $34, $ff
order_3:
        .byte $0b, $00, $0c, $00, $0d, $00, $fe, $01
order_4:
        .byte $0e, $00, $0e, $ff, $0e, $00, $0e, $00
        .byte $0e, $fc, $0e, $07, $0e, $00, $0e, $00
        .byte $0e, $01, $0e, $07, $0e, $05, $0e, $05
        .byte $0e, $00, $0e, $00, $0e, $fc, $0e, $02
        .byte $0e, $07, $0e, $07, $fe, $02
order_5:
        .byte $0f, $00, $12, $ff, $0f, $00, $0f, $00
        .byte $10, $fc, $11, $07, $0f, $00, $0f, $00
        .byte $10, $01, $11, $07, $0f, $05, $0f, $05
        .byte $0f, $00, $0f, $00, $10, $fc, $12, $02
        .byte $11, $07, $11, $07, $fe, $02
; pattern 19: clear_lead
pat_19:
        .byte $c9, $81, $40, $43, $47, $83, $4c, $81
        .byte $4b, $87, $50, $ff
; pattern 20: clear_bass
pat_20:
        .byte $c1, $81, $1c, $28, $1c, $83, $28, $81
        .byte $17, $87, $1c, $ff
; pattern 21: clear_chords
pat_21:
        .byte $c6, $80, $34, $c2, $88, $34, $c7, $80
        .byte $34, $c5, $2f, $c6, $34, $c3, $86, $34
        .byte $ff
order_6:
        .byte $13, $00, $fd
order_7:
        .byte $14, $00, $fd
order_8:
        .byte $15, $00, $fd
; pattern 22: won_lead
pat_22:
        .byte $c9, $83, $3b, $40, $81, $44, $42, $83
        .byte $40, $81, $3f, $40, $42, $44, $87, $47
        .byte $8b, $4c, $83, $60, $ff
; pattern 23: won_bass
pat_23:
        .byte $c1, $83, $1c, $28, $1c, $28, $17, $23
        .byte $17, $23, $8b, $1c, $83, $60, $ff
; pattern 24: won_major
pat_24:
        .byte $c6, $80, $34, $c3, $86, $34, $c7, $80
        .byte $34, $c3, $86, $34, $ff
; pattern 25: won_dom7
pat_25:
        .byte $c6, $80, $34, $c5, $86, $34, $c7, $80
        .byte $34, $c5, $86, $34, $ff
; pattern 26: won_end
pat_26:
        .byte $c6, $80, $34, $c3, $8a, $34, $83, $60
        .byte $ff
order_9:
        .byte $16, $00, $fd
order_10:
        .byte $17, $00, $fd
order_11:
        .byte $18, $00, $19, $07, $1a, $00, $fd
; pattern 27: dawn_lead
pat_27:
        .byte $c0, $83, $47, $43, $40, $3f, $ca, $40
        .byte $87, $3b, $ff
; pattern 28: dawn_bass
pat_28:
        .byte $c1, $83, $28, $26, $24, $23, $21, $87
        .byte $1c, $ff
; pattern 29: dawn_chords
pat_29:
        .byte $c2, $87, $34, $c3, $83, $30, $c5, $2f
        .byte $c2, $2d, $c2, $87, $28, $ff
order_12:
        .byte $1b, $00, $fd
order_13:
        .byte $1c, $00, $fd
order_14:
        .byte $1d, $00, $fd
