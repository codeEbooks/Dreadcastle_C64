; Written by game/assets/build_assets.py: do not edit.
; The texts of the title and of the bands
; (title.py): a row, a column, a colour, a length,
; the characters (the HUD's codes); $ff: no more.
menu_texts:
        .byte 22, 12, 4, 5, 22, 29, 27, 19, 13
        .byte 23, 12, 4, 8, 27, 24, 29, 23, 14, 0, 16, 45
        .byte 24, 12, 4, 6, 27, 19, 21, 15, 23, 28
        .byte 23, 26, 3, 10, 25, 26, 15, 27, 27, 0, 16, 19, 26, 15
        .byte $ff
texts_clear:
        .byte 3, 14, 7, 12, 21, 15, 30, 15, 21, 0, 13, 21, 15, 11, 26, 47
        .byte $ff
texts_won:
        .byte 4, 9, 7, 22, 28, 24, 22, 0, 14, 11, 26, 20, 16, 11, 23, 17, 0, 18, 11, 27, 0, 16, 21, 15, 14, 47
        .byte 5, 10, 1, 20, 14, 26, 15, 11, 14, 13, 11, 27, 28, 21, 15, 0, 19, 27, 0, 27, 11, 16, 15, 49
        .byte 6, 6, 1, 28, 11, 23, 14, 0, 17, 26, 11, 23, 14, 25, 11, 0, 31, 19, 21, 21, 0, 23, 15, 30, 15, 26, 0, 20, 23, 24, 31, 47
        .byte 8, 15, 3, 10, 25, 26, 15, 27, 27, 0, 16, 19, 26, 15
        .byte $ff
texts_dawn:
        .byte 3, 11, 1, 17, 22, 24, 26, 23, 19, 23, 17, 0, 18, 11, 27, 0, 13, 24, 22, 15, 47
        .byte 5, 15, 3, 10, 25, 26, 15, 27, 27, 0, 16, 19, 26, 15
        .byte $ff
; Each band: its first row, how many rows, its texts.
band_first:
        .byte 2, 3, 2
band_rows:
        .byte 3, 7, 5
band_texts_lo:
        .byte <texts_clear, <texts_won, <texts_dawn
band_texts_hi:
        .byte >texts_clear, >texts_won, >texts_dawn
; Dawn: the playfield's background, step by step.
dawn_colours:
        .byte 6, 4, 10, 8
