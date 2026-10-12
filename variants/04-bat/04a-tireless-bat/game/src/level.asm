; The level on the screen. The level is kept column by
; column: LEVEL_WIDTH columns of 11 metatiles, each metatile
; 2 x 2 characters. A column of characters is half a
; metatile column: its left half (side 0) or right half.
; The program plays a copy of the level, at LEVEL: the
; moths eaten change it; it is made from its map when it
; starts (level_maps: level_no).

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
; Oscar at the start, no moth eaten.
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
        lda #0
        sta moths_eaten
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

; Oscar at respawn_x on the street, a vampire again with
; the health and the energy full
; the camera on him, screen A in front, the back screen to
; make again. His sensor and body height as move_x would
; make them: what he touches is looked for before he
; moves.
respawn:
        lda #0
        sta osc_x               ; fractions and speeds: 0
        sta osc_y
        sta osc_vx
        sta osc_vx + 1
        sta osc_vy
        sta osc_vy + 1
        sta osc_anim
        sta osc_anim + 1
        sta osc_form            ; a vampire, no smoke
        sta osc_puff
        sta osc_gnam
        sta osc_flap
        sta energy
        sta front               ; screen A in front
        sta prep_stage
        sta swap
        lda joy                 ; keys held: not new
        sta prev_joy
        lda #ENERGY_FULL
        sta energy + 1
        lda #HEALTH_FULL
        sta health
        lda respawn_x
        sta osc_x + 1
        clc
        adc #SENSOR_X
        sta sensor
        lda respawn_x + 1
        sta osc_x + 2
        adc #0
        sta sensor + 1
        lda body_heights        ; the vampire's
        sta height
        lda #START_Y
        sta osc_y + 1
        lda #1
        sta osc_ground
        lda #RIGHT
        sta osc_face
        sta prep_dir
        sta last_dir
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

; Metatile new_tile at column tile_col, row tile_row: into
; the level, and onto the screens. Its four characters in
; the screen in front and their colours in the colour RAM
; the same characters in the back screen, one column over
; if that is the column the back screen has just drawn,
; their colours in edge_paint too, for the swap. Only the
; cells of screen columns 0-38.
set_tile:
        ldx tile_col            ; the level
        lda level_lo,x
        sta probe_col
        lda level_hi,x
        sta probe_col + 1
        ldy tile_row
        lda new_tile
        sta (probe_col),y
        ldx tile_row            ; its row in a screen
        lda row_lo,x
        sta tile_line
        lda row_hi,x
        sta tile_line + 1
        lda camera + 1          ; its column: tile_col * 2
        sta work                ; - camera / 8
        lda camera
        lsr work
        ror a
        lsr work
        ror a
        lsr work
        ror a
        sta work
        lda tile_col
        asl a
        sec
        sbc work
        sta tile_at
        lda #3                  ; the four corners
        sta corner
_corner:
        ldx corner
        lda corner_tables_lo,x
        sta vector
        lda corner_tables_hi,x
        sta vector + 1
        ldy new_tile
        lda (vector),y          ; the character
        sta fill
        lda corner_cols,x       ; in screen columns 0-38?
        clc
        adc tile_at
        cmp #39
        bcs _back
        clc                     ; its cell in the row:
        adc corner_rows,x       ; + 0 or 40
        sta work
        tay                     ; the screen in front
        ldx front
        lda front_screens,x
        jsr put_cell
        ldy fill                ; its colour
        ldx char_colour,y
        ldy work
        lda #>COLOUR_RAM
        jsr put_colour
_back:
        ldx corner              ; the back screen: one
        lda corner_cols,x       ; column over
        clc
        adc tile_at
        ldx prep_dir
        clc
        adc back_shift,x
        cmp #39
        bcs _next
        sta work
        cmp edge_columns,x      ; the column just drawn?
        bne +
        lda prep_stage
        cmp #3
        bne +
        ldx corner              ; its colour in edge_paint
        lda tile_row
        asl a
        ora corner_rows_2,x
        tax
        ldy fill
        lda char_colour,y
        sta edge_paint,x
+       ldx corner              ; its cell in the row
        lda work
        clc
        adc corner_rows,x
        tay
        ldx front
        lda back_screens,x
        jsr put_cell
_next:
        dec corner
        bpl _corner
        rts

; Character `fill` at cell Y of the row tile_line in the
; memory at A * 256; put_colour: X there, A the colour
; RAM's page.
put_cell:
        ldx fill
put_colour:
        clc
        adc tile_line + 1
        sta dst + 1
        lda tile_line
        sta dst
        txa
        sta (dst),y
        rts

corner_tables_lo:
        .byte <meta_tl, <meta_tr, <meta_bl, <meta_br
corner_tables_hi:
        .byte >meta_tl, >meta_tr, >meta_bl, >meta_br
corner_cols:    .byte 0, 1, 0, 1
corner_rows:    .byte 0, 0, 40, 40
corner_rows_2:  .byte 0, 0, 1, 1
front_screens:  .byte >SCREEN_A, >SCREEN_B
back_shift:     .byte $ff, 1    ; right: -1, left: +1
row_lo:         .byte <(range(11) * 80)
row_hi:         .byte >(range(11) * 80)

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
