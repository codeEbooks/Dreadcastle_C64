; Written by game/assets/sfx.py: do not edit.

FX_JUMP = 0
FX_FLAP = 1
FX_BLOW = 2
FX_MOTH = 3
FX_STRUCK = 4
FX_HURT = 5
FX_CHANGE = 6
FX_HEIRLOOM = 7
FX_LANTERN = 8
FX_GATE = 9
FX_TOLL = 10
FX_GROWL = 11
FX_TOM_HIT = 12
FX_TOM_LAND = 13
FX_CLICK = 14
FX_COUNT = 15
FX_HEADER = 4
FX_REEL_FRAMES = 30

sfx_first:
        .byte $00, $11, $1c, $2b, $34, $43, $56, $69
        .byte $7c, $85, $94, $9b, $ac, $b9, $c4
; 0: jump
sfx_data:
        .byte $01, $08, $84, $08, $41, $30, $41, $32, $41
        .byte $35, $41, $39, $41, $3c, $41, $41, $00
; 1: flap
        .byte $01, $06, $63, $06, $41, $2b, $41, $30, $41
        .byte $37, $00
; 2: blow
        .byte $01, $05, $83, $08, $81, $54, $81, $51, $81
        .byte $4d, $81, $4a, $81, $45, $00
; 3: moth
        .byte $02, $04, $63, $08, $11, $4c, $11, $51, $00
; 4: struck
        .byte $01, $05, $84, $04, $81, $3c, $41, $2b, $41
        .byte $29, $41, $28, $41, $26, $00
; 5: hurt
        .byte $01, $06, $94, $08, $21, $40, $21, $3c, $21
        .byte $39, $21, $35, $21, $32, $21, $2f, $21, $2b
        .byte $00
; 6: change
        .byte $02, $05, $84, $08, $81, $30, $81, $34, $81
        .byte $37, $81, $3c, $81, $37, $81, $34, $81, $30
        .byte $00
; 7: heirloom
        .byte $02, $04, $a6, $04, $41, $40, $41, $44, $41
        .byte $47, $41, $4c, $41, $50, $41, $53, $41, $58
        .byte $00
; 8: lantern
        .byte $06, $04, $6a, $08, $11, $47, $11, $4c, $00
; 9: gate
        .byte $03, $08, $a6, $08, $81, $18, $81, $1a, $81
        .byte $18, $81, $1a, $81, $18, $00
; 10: toll
        .byte $0f, $09, $0b, $08, $11, $2b, $00
; 11: growl
        .byte $02, $18, $a6, $08, $21, $1c, $21, $1d, $21
        .byte $1c, $21, $1b, $21, $1c, $21, $1d, $00
; 12: tom_hit
        .byte $01, $05, $85, $04, $81, $45, $41, $30, $41
        .byte $2f, $41, $2e, $00
; 13: tom_land
        .byte $01, $05, $84, $08, $81, $24, $81, $21, $81
        .byte $1d, $00
; 14: click
        .byte $01, $00, $00, $08, $41, $48, $00
