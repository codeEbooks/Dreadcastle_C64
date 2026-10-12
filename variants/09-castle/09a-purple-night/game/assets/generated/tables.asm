; Written by game/assets/build_assets.py: do not edit.
; The setting of each level: its set of characters and
; its tables (0: the village, 1: the forest, 2: the
; mire, 3: the crags, 4: the pass, 5: the keep, 6: the
; hall).
level_env:
        .byte 0, 0, 1, 2, 3, 4, 5, 6
; For each setting: the enemies it shows at most (in
; the wood three: sprite 6 is the moon); its moon's
; bit in $d015 (moon.py), or 0.
env_slots:
        .byte 4, 3, 3, 3, 3, 3, 3
env_moon:
        .byte %00000000, %01000000, %01000000, %01000000, %01000000, %01000000, %01000000
; Its moon behind the characters: its bit of $d01b; its
; second shared colour, $d023.
env_behind:
        .byte %00000000, %00000000, %00000000, %01000000, %00000000, %01000000, %01000000
env_d023:
        .byte 9, 9, 9, 12, 14, 12, 8
; Its background, $d021 of the playfield (the top
; interrupt's), and its first shared colour.
env_d021:
        .byte 0, 0, 0, 0, 0, 4, 6
env_d022:
        .byte 11, 11, 11, 11, 11, 11, 12
