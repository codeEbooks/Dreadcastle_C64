; Written by game/assets/build_assets.py: do not edit.
; For each setting whose hazards flicker: the page of
; their pictures (flicker.bin); else 0.
env_flicker:
        .byte 0, 0, >flicker_pictures + 0, 0, >flicker_pictures + 256, >flicker_pictures + 512, >flicker_pictures + 768
