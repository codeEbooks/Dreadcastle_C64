; Written by game/assets/build_assets.py: do not edit.
; For steps 01-07 of the book's chain: the data of the
; first levels as they are, not packed (from step 08
; packed.asm packs them all); each map with zeros
; after it, to MAP_PAGES pages.
level_map_1:
        .binary "level1.bin"
        .fill 128
level_map_2:
        .binary "level2.bin"
        .fill 128
level_map_3:
        .binary "level3.bin"
        .fill 128
level_map_4 = 0               ; not yet
level_map_5 = 0               ; not yet
level_map_6 = 0               ; not yet
level_map_7 = 0               ; not yet
level_map_8 = 0               ; not yet
env_packed_village:
        .binary "env_village.bin"
env_packed_forest:
        .binary "env_forest.bin"
set_packed_forest:
        .binary "charset_forest.bin"
; Where each setting's tables and set are (0: not yet).
env_packed_lo:
        .byte <env_packed_village, <env_packed_forest, 0, 0, 0, 0, 0
env_packed_hi:
        .byte >env_packed_village, >env_packed_forest, 0, 0, 0, 0, 0
set_packed_lo:
        .byte 0, <set_packed_forest, 0, 0, 0, 0, 0
set_packed_hi:
        .byte 0, >set_packed_forest, 0, 0, 0, 0, 0
