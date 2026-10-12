; Written by game/assets/build_assets.py: do not edit.
; Each level's row 24 of the HUD: 40 characters,
; 40 colours; then Tom's, in the arena.
level_names_lo:
        .byte <(level_names + 0), <(level_names + 80), <(level_names + 160), <(level_names + 240), <(level_names + 320), <(level_names + 400), <(level_names + 480), <(level_names + 560), <(level_names + 640)
level_names_hi:
        .byte >(level_names + 0), >(level_names + 80), >(level_names + 160), >(level_names + 240), >(level_names + 320), >(level_names + 400), >(level_names + 480), >(level_names + 560), >(level_names + 640)
