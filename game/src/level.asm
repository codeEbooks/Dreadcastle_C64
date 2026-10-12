; The level on the screen. The level is kept column by
; column: LEVEL_WIDTH columns of 11 metatiles, each metatile
; 2 x 2 characters. A column of characters is half a
; metatile column: its left half (side 0) or right half.
; The program plays a copy of the level, at LEVEL, made {-3}
; from its map when it starts (level_maps: level_no). {-3}
; The program plays a copy of the level, at LEVEL: the {4-4}
; moths eaten change it; it is made from its map when it {4-4}
; starts (level_maps: level_no). {4-4}
; The program plays a copy of the level, at LEVEL: the {5}
; moths eaten, the lantern lit and the gate open change {5}
; it; at a restart the copy is made again from the {5}
; level's map (level_maps: level_no). {5}

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

; Level level_no from its start: its map is copied to {-4}
; LEVEL, MAP_PAGES pages ($c000-$c5ff: the map and zeros {-4}
; after it), by start_map and unpack_page; then restart: {-4}
; Oscar at the start. {-3}
; Oscar at the start, no moth eaten. {4-4}
; Level level_no again from its start: its map is {5}
; copied to LEVEL, MAP_PAGES pages ($c000-$c5ff: the {5-7}
; unpacked to LEVEL, MAP_PAGES pages ($c000-$c5ff: the {8}
; map and zeros after it), by start_map and unpack_page {5}
; (a page a frame in a transition, all at once at the {5}
; start). Then restart: no heirloom taken, the lantern {5}
; dark, the gate shut, the whole night ahead, Oscar at the {5}
; start; the level's objects. {5-9}
; start; the level's objects; not in the arena, sprite 7 {10}
; the heirloom's colour again. {10}
; (Its name in the HUD: show_name, in the lightest step of {5}
; the transition, trans_on.) {5}
LEVEL_BYTES   = LEVEL_WIDTH * 11
        .cerror (LEVEL_BYTES + 255) / 256 != MAP_PAGES, "6"
        .cerror OBJECTS < LEVEL + MAP_PAGES * 256, "objects" ; {5}

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
        lda #0 ; {4}
        sta got ; {5}
        sta got_bits ; {5}
        sta lantern_lit ; {5}
        sta door_open ; {5}
        sta moths_eaten ; {4}
        sta arena ; {10}
        lda #HEIRLOOM_COLOUR ; {10}
        sta $d02e ; {10}
        lda #NIGHT_STEPS ; {5}
        sta night ; {5}
        lda #<NIGHT_STEP ; {5}
        sta night_time ; {5}
        lda #>NIGHT_STEP ; {5}
        sta night_time + 1 ; {5}
        lda #<START_X
        sta respawn_x
        lda #>START_X
        sta respawn_x + 1
;|        rts ; {-4}
        jmp load_objects ; {5}

; The block of objects of level level_no into OBJECTS. {5}
load_objects: ; {5}
        ldx level_no ; {5}
        lda level_objects_lo,x ; {5}
        sta copy_src ; {5}
        lda level_objects_hi,x ; {5}
        sta copy_src + 1 ; {5}
        ldy #OBJECT_BYTES - 1 ; {5}
-       lda (copy_src),y ; {5}
        sta OBJECTS,y ; {5}
        dey ; {5}
        bpl - ; {5}
        rts ; {5}

; Row 24 of the HUD: the number and the name of the level,
; in both screens, and their colours. {-9}
; in both screens, and their colours; in the arena Tom's {10}
; name and his bar (the row after the levels'). {10-11}
; name and his bar (the row after the levels'); the score {12}
; over its zeros. {12}
NAME_ROW      = HUD + 80
show_name:
        ldx level_no
        lda arena ; {10}
        beq + ; {10}
        ldx #LEVEL_COUNT ; {10}
;|        lda level_names_lo,x ; {-9}
+       lda level_names_lo,x ; {10}
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
;|        rts ; {-11}
        jmp write_score ; {12}

; Oscar at respawn_x on the street; the camera on him, {-2}
; screen A in front. {1-1}
; screen A in front, the back screen to make again. {2-2}
; Oscar at respawn_x on the street with the health full, {3-3}
; Oscar at respawn_x on the street, a vampire again with {4}
; the health and the energy full; {4}
; the camera on him, screen A in front, the back screen to {3}
; make again. His sensor and body height as move_x would {3-4}
; make them: what he touches is looked for before he {3-4}
; moves. {3-4}
; the camera on him (in the arena: at the end of the {10}
; level), screen A in front, the back screen to make {10}
; again. {10}
; make them: what he touches is looked for even in a puff {5}
; of smoke, before he moves. {5}
respawn:
        lda #0
        sta osc_x               ; fractions and speeds: 0
        sta osc_y
        sta osc_vx ; {3}
        sta osc_vx + 1 ; {3}
        sta osc_vy ; {3}
        sta osc_vy + 1 ; {3}
        sta osc_anim ; {3}
        sta osc_anim + 1 ; {3}
        sta osc_form            ; a vampire, no smoke {4}
        sta osc_puff ; {4}
        sta osc_gnam ; {4}
        sta osc_flap ; {4}
        sta energy ; {4}
        sta front               ; screen A in front
        sta prep_stage ; {2}
        sta swap ; {2}
;|        sta protect             ; no blinking, no stun {6-6}
        sta protect             ; no blinking, no stun, {7}
        sta stun                ; no blow {7}
;|        sta stun ; {6-6}
        sta blow ; {7}
        lda joy                 ; keys held: not new {3}
        sta prev_joy ; {3}
        lda #ENERGY_FULL ; {4}
        sta energy + 1 ; {4}
        lda #HEALTH_FULL ; {3}
        sta health ; {3}
        lda respawn_x
        sta osc_x + 1
        clc ; {3}
        adc #SENSOR_X ; {3}
        sta sensor ; {3}
        lda respawn_x + 1
        sta osc_x + 2
        adc #0 ; {3}
        sta sensor + 1 ; {3}
        lda body_heights        ; the vampire's {3}
        sta height ; {3}
        lda #START_Y
        sta osc_y + 1
        lda #1 ; {3}
        sta osc_ground ; {3}
        lda #RIGHT ; {2}
        sta osc_face ; {3}
        sta prep_dir ; {2}
        sta last_dir ; {2}
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
+       lda arena               ; the arena: the end {10}
        beq + ; {10}
        lda #<CAMERA_MAX ; {10}
        sta camera ; {10}
        lda #>CAMERA_MAX ; {10}
        sta camera + 1 ; {10}
+       jmp set_xscroll

; Metatile new_tile at column tile_col, row tile_row: into {4}
; the level, and onto the screens. Its four characters in {4}
; the screen in front and their colours in the colour RAM; {4}
; the same characters in the back screen, one column over; {4}
; if that is the column the back screen has just drawn, {4}
; their colours in edge_paint too, for the swap. Only the {4}
; cells of screen columns 0-38. {4}
set_tile: ; {4}
        ldx tile_col            ; the level {4}
        lda level_lo,x ; {4}
        sta probe_col ; {4}
        lda level_hi,x ; {4}
        sta probe_col + 1 ; {4}
        ldy tile_row ; {4}
        lda new_tile ; {4}
        sta (probe_col),y ; {4}
        ldx tile_row            ; its row in a screen {4}
        lda row_lo,x ; {4}
        sta tile_line ; {4}
        lda row_hi,x ; {4}
        sta tile_line + 1 ; {4}
        lda camera + 1          ; its column: tile_col * 2 {4}
        sta work                ; - camera / 8 {4}
        lda camera ; {4}
        lsr work ; {4}
        ror a ; {4}
        lsr work ; {4}
        ror a ; {4}
        lsr work ; {4}
        ror a ; {4}
        sta work ; {4}
        lda tile_col ; {4}
        asl a ; {4}
        sec ; {4}
        sbc work ; {4}
        sta tile_at ; {4}
        lda #3                  ; the four corners {4}
        sta corner ; {4}
_corner: ; {4}
        ldx corner ; {4}
        lda corner_tables_lo,x ; {4}
        sta vector ; {4}
        lda corner_tables_hi,x ; {4}
        sta vector + 1 ; {4}
        ldy new_tile ; {4}
        lda (vector),y          ; the character {4}
        sta fill ; {4}
        lda corner_cols,x       ; in screen columns 0-38? {4}
        clc ; {4}
        adc tile_at ; {4}
        cmp #39 ; {4}
        bcs _back ; {4}
        clc                     ; its cell in the row: {4}
        adc corner_rows,x       ; + 0 or 40 {4}
        sta work ; {4}
        tay                     ; the screen in front {4}
        ldx front ; {4}
        lda front_screens,x ; {4}
        jsr put_cell ; {4}
        ldy fill                ; its colour {4}
        ldx char_colour,y ; {4}
        ldy work ; {4}
        lda #>COLOUR_RAM ; {4}
        jsr put_colour ; {4}
_back: ; {4}
        ldx corner              ; the back screen: one {4}
        lda corner_cols,x       ; column over {4}
        clc ; {4}
        adc tile_at ; {4}
        ldx prep_dir ; {4}
        clc ; {4}
        adc back_shift,x ; {4}
        cmp #39 ; {4}
        bcs _next ; {4}
        sta work ; {4}
        cmp edge_columns,x      ; the column just drawn? {4}
        bne + ; {4}
        lda prep_stage ; {4}
        cmp #3 ; {4}
        bne + ; {4}
        ldx corner              ; its colour in edge_paint {4}
        lda tile_row ; {4}
        asl a ; {4}
        ora corner_rows_2,x ; {4}
        tax ; {4}
        ldy fill ; {4}
        lda char_colour,y ; {4}
        sta edge_paint,x ; {4}
+       ldx corner              ; its cell in the row {4}
        lda work ; {4}
        clc ; {4}
        adc corner_rows,x ; {4}
        tay ; {4}
        ldx front ; {4}
        lda back_screens,x ; {4}
        jsr put_cell ; {4}
_next: ; {4}
        dec corner ; {4}
        bpl _corner ; {4}
        rts ; {4}

; Character `fill` at cell Y of the row tile_line in the {4}
; memory at A * 256; put_colour: X there, A the colour {4}
; RAM's page. {4}
put_cell: ; {4}
        ldx fill ; {4}
put_colour: ; {4}
        clc ; {4}
        adc tile_line + 1 ; {4}
        sta dst + 1 ; {4}
        lda tile_line ; {4}
        sta dst ; {4}
        txa ; {4}
        sta (dst),y ; {4}
        rts ; {4}

corner_tables_lo: ; {4}
        .byte <meta_tl, <meta_tr, <meta_bl, <meta_br ; {4}
corner_tables_hi: ; {4}
        .byte >meta_tl, >meta_tr, >meta_bl, >meta_br ; {4}
corner_cols:    .byte 0, 1, 0, 1 ; {4}
corner_rows:    .byte 0, 0, 40, 40 ; {4}
corner_rows_2:  .byte 0, 0, 1, 1 ; {4}
front_screens:  .byte >SCREEN_A, >SCREEN_B ; {4}
back_shift:     .byte $ff, 1    ; right: -1, left: +1 {4}
row_lo:         .byte <(range(11) * 80) ; {4}
row_hi:         .byte >(range(11) * 80) ; {4}

; At the start, load_level does the level and its setting {-6}
; all at once: its map to LEVEL (start_map), the setting's {-6}
; tables to ENV_TABLES, ENV_PAGES pages (start_tables), its {-6}
; characters for the top interrupt (d018_values, {-6}
; next_env); unpack_pages copies them. {-6}
; The setting of level level_no: its tables to ENV_TABLES, {7}
; ENV_PAGES pages; its characters for the top interrupt {7}
; (d018_values); its set of characters in SET_SLOT, {7}
; SET_PAGES pages, if it is not the village's. The level's {7}
; map, the tables and the set are copied by start_map, {7-7}
; start_tables, start_set and unpack_page (objects.asm: a {7-7}
; map, the tables and the set are unpacked by start_map, {8}
; start_tables, start_set and unpack_page (objects.asm: a {8}
; page a frame in a transition). At the start, load_level {7}
; does the level and its setting all at once. {7}
load_level:
        jsr next_env
        jsr start_map
        ldx #MAP_PAGES
        jsr unpack_pages
        ldy env
        jsr start_tables
        ldx #ENV_PAGES
        jsr unpack_pages
        jsr start_set ; {7}
        ldx #SET_PAGES ; {7}
        jsr unpack_pages ; {7}
        jmp restart

; env := the setting of level level_no; its two $d018. {-7}
; env := the setting of level level_no; its two $d018; {8}
; its $d023 and its moon's bit of $d01b (behind the {8}
; characters, in the mountain). {8-8}
; characters, in the mountain); its $d022 and the {9}
; background of its playfield (blue in the castle). {9}
next_env:
        ldx level_no
        lda level_env,x
        sta env
        tax
        lda env_d018_a,x
        sta d018_values
        lda env_d018_b,x
        sta d018_values + 1
        lda env_d021,x ; {9}
        sta play_d021 ; {9}
        lda env_d022,x ; {9}
        sta $d022 ; {9}
        lda env_d023,x ; {8}
        sta $d023 ; {8}
        lda env_behind,x ; {8}
        sta $d01b ; {8}
        rts

; The stream of the tables of setting Y. {8}
; The tables of setting Y, to copy. {-7}
start_tables:
        lda env_packed_lo,y
        ldx env_packed_hi,y
        ldy #>ENV_TABLES
        jmp unpack_start
        .cerror (<ENV_TABLES) != 0, "on a page"

; The stream of its set of characters; the village's: none {8}
; (up_on := 0: its set stays at CHARSET). {8}
; Its set of characters, to copy; the village's: none {7-7}
; (up_on := 0: its set stays at CHARSET). {7-7}
start_set: ; {7}
        ldy env ; {7}
        lda set_packed_lo,y ; {7}
        ldx set_packed_hi,y ; {7}
        beq + ; {7}
        ldy #>SET_SLOT ; {7}
        jmp unpack_start ; {7}
+       stx up_on ; {7}
        rts ; {7}

        .include "unpack.asm"
