; The VIC-II: memory, mode, colours; the sprites.

init_vic:
        lda #0
        sta $d015               ; no sprites while drawing
        lda $dd02
        ora #%00000011          ; CIA 2 port A: bits 0-1 out
        sta $dd02
        lda $dd00
        and #%11111100
        ora #%00000010          ; bits %10: VIC-II bank 1
        sta $dd00
        lda d018_values         ; screen A, the setting's
        sta $d018               ; characters
        lda #%00010000          ; multicolour, 38 columns
        sta $d016
        lda #%00011011          ; 25 rows, screen on
        sta $d011
        lda #D021_SKY
        sta $d020               ; border like the night sky
        sta $d021               ; (the playfield's: irq_top)
        ldx env                 ; the setting's two shared
        lda env_d022,x          ; colours: of the stone
        sta $d022
        lda env_d023,x          ; and of the wood
        sta $d023
        rts

; Oscar: sprite 0 draws his lines, in black, over sprite 1,
; his colours in multicolour. Position and pictures: in
; place_oscar (oscar.asm), at every frame.
; Sprite 2, in multicolour: the staff (staff.asm).
; Sprites 3-6, in multicolour: the enemies (enemies.asm)
; where there is a moon 3-5, and 6 the moon (place_moon).
; Sprite 7: the heirloom on the screen (objects.asm).
init_sprites:
        lda #0
        sta $d017               ; no expansion
        sta $d01d
        ldx env                 ; sprites in front; the moon
        lda env_behind,x        ; behind the characters in
        sta $d01b               ; the mountain
        lda #%11111110          ; sprites 1-7 in
        sta $d01c               ; multicolour
        lda #SPRITE_SHARED_1
        sta $d025
        lda #SPRITE_SHARED_2
        sta $d026
        lda #OSCAR_LINE_COLOUR
        sta $d027
        lda #OSCAR_COLOUR
        sta $d028
        lda #STAFF_COLOUR       ; sprite 2: the staff
        sta $d029
        lda #HEIRLOOM_COLOUR    ; sprite 7: the heirlooms
        sta $d02e
        lda #%00000011          ; sprites 0 and 1 on
        sta $d015
        rts
