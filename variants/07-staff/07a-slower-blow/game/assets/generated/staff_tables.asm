; Written by game/assets/build_assets.py: do not edit.
; The staff in his hand, for each of Oscar's 12
; pictures: X, Y from his sprite's, its block.
held_dx:
        .byte 22, 22, 22, 22, 20, 20, 234, 234, 234, 234, 236, 236
held_dy:
        .byte 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0
held_block:
        .byte STAFF_BLOCKS + 0, STAFF_BLOCKS + 0, STAFF_BLOCKS + 0, STAFF_BLOCKS + 0, STAFF_BLOCKS + 1, STAFF_BLOCKS + 1, STAFF_BLOCKS + 5, STAFF_BLOCKS + 5, STAFF_BLOCKS + 5, STAFF_BLOCKS + 5, STAFF_BLOCKS + 6, STAFF_BLOCKS + 6
; The blow, by its frames left (1-10), facing right,
; then left.
blow_dx:
        .byte 16, 16, 16, 16, 16, 16, 16, 8, 8, 8, 8, 8, 8, 8, 240, 240, 240, 240, 240, 240, 240, 248, 248, 248, 248, 248, 248, 248
blow_dy:
        .byte 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
blow_block:
        .byte STAFF_BLOCKS + 4, STAFF_BLOCKS + 4, STAFF_BLOCKS + 4, STAFF_BLOCKS + 3, STAFF_BLOCKS + 3, STAFF_BLOCKS + 3, STAFF_BLOCKS + 3, STAFF_BLOCKS + 2, STAFF_BLOCKS + 2, STAFF_BLOCKS + 2, STAFF_BLOCKS + 2, STAFF_BLOCKS + 2, STAFF_BLOCKS + 2, STAFF_BLOCKS + 2, STAFF_BLOCKS + 9, STAFF_BLOCKS + 9, STAFF_BLOCKS + 9, STAFF_BLOCKS + 8, STAFF_BLOCKS + 8, STAFF_BLOCKS + 8, STAFF_BLOCKS + 8, STAFF_BLOCKS + 7, STAFF_BLOCKS + 7, STAFF_BLOCKS + 7, STAFF_BLOCKS + 7, STAFF_BLOCKS + 7, STAFF_BLOCKS + 7, STAFF_BLOCKS + 7
