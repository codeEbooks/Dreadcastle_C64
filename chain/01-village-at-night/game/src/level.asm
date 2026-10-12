; The level on the screen. The level is kept column by
; column: LEVEL_WIDTH columns of 11 metatiles, each metatile
; 2 x 2 characters. A column of characters is half a
; metatile column: its left half (side 0) or right half.
; The program plays a copy of the level, at LEVEL, made
; from its map when it starts (level_maps: level_no).

; Columns col_screen to col_end - 1 of screen A, with their
; colours: level columns camera / 8 + those.
draw_columns:
        lda #>SCREEN_A
        sta target_hi
_column:
        lda camera + 1          ; camera / 8
        sta world + 1
        lda camera
        lsr world + 1
        ror a
        lsr world + 1
        ror a
        lsr world + 1
        ror a
        clc
        adc col_screen
        sta world
        bcc +
        inc world + 1
+       jsr draw_column
        ldx col_screen
        jsr paint_top           ; its colours, rows 0-10
        jsr paint_bottom        ; and rows 11-21
        inc col_screen
        lda col_screen
        cmp col_end
        bne _column
        rts

; Draw column `world` of the level into column col_screen
; of the screen at target_hi * 256, rows 0-21; its 22
; colours go to edge_paint, for the colour RAM.
draw_column:
        lda world + 1
        lsr a                   ; world / 2, in 9 bits:
        lda world
        ror a                   ; A: metatile col., C: side
        tax
        lda level_lo,x          ; where the column is kept
        sta col_ptr
        lda level_hi,x
        sta col_ptr + 1
        lda #0
        rol a                   ; the side: 0 or 1
        asl a
        asl a                   ; 4 bytes for each side
        tax
        ldy #0
-       lda side_tables,x       ; top_tab and bottom_tab
        sta top_tab,y
        inx
        iny
        cpy #4
        bne -
        lda col_screen          ; the first cell: row 0
        sta dst
        lda target_hi
        sta dst + 1
        lda #0
        sta mrow
        tax                     ; X: row of the cell, 0-21
_metatile:
        ldy mrow
        lda (col_ptr),y         ; the metatile
        tay
        lda (bottom_tab),y      ; its lower character
        sta below
        lda (top_tab),y         ; its upper character
        ldy #0
        sta (dst),y
        tay
        lda char_colour,y
        sta edge_paint,x
        inx
        lda below
        ldy #40                 ; one row down
        sta (dst),y
        tay
        lda char_colour,y
        sta edge_paint,x
        inx
        lda dst                 ; two rows down: 80 bytes
        clc
        adc #80
        sta dst
        bcc +
        inc dst + 1
+       inc mrow
        lda mrow
        cmp #11
        bne _metatile
        rts

; The four character tables of each side: upper, lower.
side_tables:
        .word meta_tl, meta_bl  ; side 0: the left half
        .word meta_tr, meta_br  ; side 1: the right half

; The colours of edge_paint into column X of the colour
; RAM: rows 0-10, then rows 11-21. X is kept.
paint_cells .macro first
        .for row := \first, row < \first + 11, row += 1
        lda edge_paint + row
        sta COLOUR_RAM + row * 40,x
        .endfor
        rts
        .endmacro

paint_top       #paint_cells 0
paint_bottom    #paint_cells 11

; HUD rows 22 and 23, in both screens, and their colours
; (row 24, the level's name: show_name).
draw_hud:
        ldx #79
-       lda hud_chars,x
        sta SCREEN_A + HUD,x
        sta SCREEN_B + HUD,x
        lda hud_colours,x
        sta COLOUR_RAM + HUD,x
        dex
        bpl -
        rts

; Level level_no from its start: its map is copied to
; LEVEL, MAP_PAGES pages ($c000-$c5ff: the map and zeros
; after it), by start_map and unpack_page; then restart:
; Oscar at the start.
LEVEL_BYTES   = LEVEL_WIDTH * 11
        .cerror (LEVEL_BYTES + 255) / 256 != MAP_PAGES, "6"

start_map:
        ldx level_no
        lda level_maps_lo,x
        pha
        lda level_maps_hi,x
        tax
        pla
        ldy #>LEVEL
        jmp unpack_start

restart:
        lda #<START_X
        sta respawn_x
        lda #>START_X
        sta respawn_x + 1
        rts

; Row 24 of the HUD: the number and the name of the level,
; in both screens, and their colours.
NAME_ROW      = HUD + 80
show_name:
        ldx level_no
        lda level_names_lo,x
        sta copy_src
        lda level_names_hi,x
        sta copy_src + 1
        ldy #39
-       lda (copy_src),y        ; 40 characters
        sta SCREEN_A + NAME_ROW,y
        sta SCREEN_B + NAME_ROW,y
        dey
        bpl -
        ldy #79                 ; then 40 colours
-       lda (copy_src),y
        sta COLOUR_RAM + NAME_ROW - 40,y
        dey
        cpy #39
        bne -
        rts

; Oscar at respawn_x on the street; the camera on him,
; screen A in front.
respawn:
        lda #0
        sta osc_x               ; fractions and speeds: 0
        sta osc_y
        sta front               ; screen A in front
        lda respawn_x
        sta osc_x + 1
        lda respawn_x + 1
        sta osc_x + 2
        lda #START_Y
        sta osc_y + 1
        lda #STAND
        sta osc_pic
        lda d018_values         ; screen A, the setting's
        sta shown_d018          ; characters
        sec                     ; camera: x - SCREEN_START
        lda respawn_x           ; + 7, from 0 to CAMERA_MAX
        sbc #SCREEN_START - 7
        sta camera
        lda respawn_x + 1
        sbc #0
        sta camera + 1
        bcs +
        lda #0                  ; under 0
        sta camera
        sta camera + 1
+       lda #<CAMERA_MAX
        cmp camera
        lda #>CAMERA_MAX
        sbc camera + 1
        bcs +
        lda #<CAMERA_MAX        ; past the end
        sta camera
        lda #>CAMERA_MAX
        sta camera + 1
+       jmp set_xscroll

; At the start, load_level does the level and its setting
; all at once: its map to LEVEL (start_map), the setting's
; tables to ENV_TABLES, ENV_PAGES pages (start_tables), its
; characters for the top interrupt (d018_values,
; next_env); unpack_pages copies them.
load_level:
        jsr next_env
        jsr start_map
        ldx #MAP_PAGES
        jsr unpack_pages
        ldy env
        jsr start_tables
        ldx #ENV_PAGES
        jsr unpack_pages
        jmp restart

; env := the setting of level level_no; its two $d018.
next_env:
        ldx level_no
        lda level_env,x
        sta env
        tax
        lda env_d018_a,x
        sta d018_values
        lda env_d018_b,x
        sta d018_values + 1
        rts

; The tables of setting Y, to copy.
start_tables:
        lda env_packed_lo,y
        ldx env_packed_hi,y
        ldy #>ENV_TABLES
        jmp unpack_start
        .cerror (<ENV_TABLES) != 0, "on a page"

        .include "unpack.asm"
