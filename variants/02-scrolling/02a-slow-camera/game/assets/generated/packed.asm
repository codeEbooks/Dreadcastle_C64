; Written by game/assets/build_assets.py: do not edit.
; The packed data (pack.py): each level's map, then each
; setting's tables and set of characters.
level_map_1:
        .binary "level1.lz"
level_map_2:
        .binary "level2.lz"
level_map_3:
        .binary "level3.lz"
level_map_5:
        .binary "level5.lz"
level_map_6:
        .binary "level6.lz"
level_map_7:
        .binary "level7.lz"
level_map_8:
        .binary "level8.lz"
env_packed_village:
        .binary "env_village.lz"
env_packed_forest:
        .binary "env_forest.lz"
set_packed_forest:
        .binary "charset_forest.lz"
env_packed_marsh:
        .binary "env_marsh.lz"
set_packed_marsh:
        .binary "charset_marsh.lz"
env_packed_crags:
        .binary "env_crags.lz"
set_packed_crags:
        .binary "charset_crags.lz"
env_packed_pass:
        .binary "env_pass.lz"
set_packed_pass:
        .binary "charset_pass.lz"
env_packed_keep:
        .binary "env_keep.lz"
; Where each setting's tables and set are.
env_packed_lo:
        .byte <env_packed_village, <env_packed_forest, <env_packed_marsh, <env_packed_crags, <env_packed_pass, <env_packed_keep, <env_packed_hall
env_packed_hi:
        .byte >env_packed_village, >env_packed_forest, >env_packed_marsh, >env_packed_crags, >env_packed_pass, >env_packed_keep, >env_packed_hall
set_packed_lo:
        .byte 0, <set_packed_forest, <set_packed_marsh, <set_packed_crags, <set_packed_pass, <set_packed_keep, <set_packed_hall
set_packed_hi:
        .byte 0, >set_packed_forest, >set_packed_marsh, >set_packed_crags, >set_packed_pass, >set_packed_keep, >set_packed_hall
