; The enemies. Each level has up to MAX_ENEMIES, in its
; block of objects: the type (the look of its setting and
; its behaviour, type_kind), the ends of its stretch, where
; it starts. Three ways of moving:
;   PATROL, the night watchman, the werewolf scout: to and
;     fro along his stretch of street, at PATROL_SPEED;
;   FLYER, the crow, the owl: to and fro across its stretch
;     at FLYER_SPEED, up and down on a wave, through all;
;   JUMPER, the black cat, the giant toad: it sits and looks
;     at Oscar; every CAT_WAIT frames, if he is within
;     CAT_REACH pixels, it jumps at him, and falls onto the
;     surface under it.
; Their x is the level x of the left edge of the sprite, y
; the line under their feet, as for Oscar. Touching Oscar
; takes HIT_DAMAGE of his health and throws him back; then
; he blinks for PROTECT_FRAMES, and no touch counts. Four

PATROL        = 0
FLYER         = 1
JUMPER        = 2
PATROL_SPEED  = $00c0           ; 0.75 pixels a frame
FLYER_SPEED   = $0100           ; 1 pixel a frame
CAT_JUMP      = $0300           ; 3 pixels a frame up
CAT_VX        = $0100           ; and 1 across
CAT_GRAVITY   = $0020           ; falling
CAT_WAIT      = 60              ; frames between two jumps
CAT_REACH     = 96              ; pixels: Oscar near enough
HIT_DAMAGE    = 2               ; a character of the bar
PROTECT_FRAMES = 75             ; 1.5 seconds of blinking
KNOCK_FRAMES  = 16              ; thrown back: no joystick
        .cerror BODY_LEFT + BODY_RIGHT != 23, "symmetric"
        .cerror ENEMY_KINDS != 3, "three kinds"

; The enemies of the level, all of them, every frame.
move_enemies:
        ldx enemy_count
        bne +
        rts
+       dex
_one:
        stx en_i
_move:
        ldy en_kind,x           ; its type: its behaviour
        lda type_kind,y
        cmp #JUMPER
        bne +
        jsr move_jumper
        jmp _next
+       jsr move_across
_next:
        ldx en_i
        dex
        bpl _one
        rts

; The patrol and the flyer (X): across at the speed of its
; kind; at an end of its stretch, there, turned round. A
; counter: the patrol's steps; the flyer's place on the
; wave (64 frames), and its wings.
move_across:
        ldy en_kind,x           ; behaviour 0 or 1: its
        lda type_kind,y         ; speed
        tay
        lda en_dir,x
        bne _left
        clc                     ; right: x + speed
        lda en_x_frac,x
        adc speed_lo,y
        sta en_x_frac,x
        lda en_x_lo,x
        adc speed_hi,y
        sta en_x_lo,x
        lda en_x_hi,x
        adc #0
        sta en_x_hi,x
        lda en_x_lo,x           ; at the end, or past it?
        cmp en_max_lo,x
        lda en_x_hi,x
        sbc en_max_hi,x
        bcc _count
        lda en_max_lo,x         ; there, and to the left
        sta en_x_lo,x
        lda en_max_hi,x
        sta en_x_hi,x
        lda #LEFT
        bne _turn
_left:
        sec                     ; left: x - speed
        lda en_x_frac,x
        sbc speed_lo,y
        sta en_x_frac,x
        lda en_x_lo,x
        sbc speed_hi,y
        sta en_x_lo,x
        lda en_x_hi,x
        sbc #0
        sta en_x_hi,x
        lda en_min_lo,x         ; at the end, or past it?
        cmp en_x_lo,x
        lda en_min_hi,x
        sbc en_x_hi,x
        bcc _count
        lda en_min_lo,x         ; there, and to the right
        sta en_x_lo,x
        lda en_min_hi,x
        sta en_x_hi,x
        lda #RIGHT
_turn:
        sta en_dir,x
        lda #0
        sta en_x_frac,x
_count:
        lda en_timer,x
        clc
        adc #1
        cpy #FLYER
        beq _wave
        sta en_timer,x          ; the patrol: 0-255
        jmp _picture
_wave:
        and #63                 ; the flyer: 0-63
        sta en_timer,x
        tay
        lda en_start_y,x        ; its line, on the wave
        clc
        adc wave,y
        sta en_y,x
_picture:
        lda en_timer,x          ; a picture every 8 frames
        lsr a
        lsr a
        lsr a
        and #1
        sta en_pic,x
        rts

speed_lo:   .byte <PATROL_SPEED, <FLYER_SPEED
speed_hi:   .byte >PATROL_SPEED, >FLYER_SPEED

; The cat (X). Sitting, it looks at Oscar; it waits; then,
; if he is near, it jumps at him. In the air: across, but
; not out of its stretch; falling, onto the first surface
; under its middle. Below the playfield: back at its start.
move_jumper:
        lda en_air,x
        bne _air
        lda osc_x + 1           ; Oscar left of it: left
        cmp en_x_lo,x
        lda osc_x + 2
        sbc en_x_hi,x
        lda #RIGHT
        bcs +
        lda #LEFT
+       sta en_dir,x
        lda en_timer,x
        beq _try
        dec en_timer,x          ; waiting
        rts
_try:
        lda #CAT_WAIT
        sta en_timer,x
        sec                     ; |Oscar's x - its x|
        lda osc_x + 1
        sbc en_x_lo,x
        sta en_dx
        lda osc_x + 2
        sbc en_x_hi,x
        bcs +
        sec                     ; negative: its x - his
        lda en_x_lo,x
        sbc osc_x + 1
        sta en_dx
        lda en_x_hi,x
        sbc osc_x + 2
+       bne _far                ; 256 or more
        lda en_dx
        cmp #CAT_REACH
        bcs _far
        lda #<-CAT_JUMP         ; the jump
        sta en_vy_lo,x
        lda #>-CAT_JUMP
        sta en_vy_hi,x
        ldy en_dir,x
        lda cat_vx_lo,y
        sta en_vx_lo,x
        lda cat_vx_hi,y
        sta en_vx_hi,x
        lda #1
        sta en_air,x
        sta en_pic,x
_far:
        rts
_air:
        ldy #0                  ; x + vx: 24 bits, signed
        lda en_vx_hi,x
        bpl +
        dey
+       clc
        lda en_x_frac,x
        adc en_vx_lo,x
        sta en_x_frac,x
        lda en_x_lo,x
        adc en_vx_hi,x
        sta en_x_lo,x
        tya
        adc en_x_hi,x
        sta en_x_hi,x
        lda en_vx_hi,x
        bmi _min
        lda en_x_lo,x           ; going right: past the end?
        cmp en_max_lo,x
        lda en_x_hi,x
        sbc en_max_hi,x
        bcc _fall
        lda en_max_lo,x
        sta en_x_lo,x
        lda en_max_hi,x
        jmp _stop
_min:
        lda en_min_lo,x         ; going left: past the end?
        cmp en_x_lo,x
        lda en_min_hi,x
        sbc en_x_hi,x
        bcc _fall
        lda en_min_lo,x
        sta en_x_lo,x
        lda en_min_hi,x
_stop:
        sta en_x_hi,x           ; there, and no more across
        lda #0
        sta en_x_frac,x
        sta en_vx_lo,x
        sta en_vx_hi,x
_fall:
        lda en_y,x              ; its feet before the move
        sta en_line
        clc                     ; gravity, to FALL_MAX
        lda en_vy_lo,x
        adc #<CAT_GRAVITY
        sta en_vy_lo,x
        lda en_vy_hi,x
        adc #>CAT_GRAVITY
        sta en_vy_hi,x
        bmi _move               ; going up
        lda #<FALL_MAX
        cmp en_vy_lo,x
        lda #>FALL_MAX
        sbc en_vy_hi,x
        bcs _move
        lda #<FALL_MAX
        sta en_vy_lo,x
        lda #>FALL_MAX
        sta en_vy_hi,x
_move:
        clc                     ; y + vy
        lda en_y_frac,x
        adc en_vy_lo,x
        sta en_y_frac,x
        lda en_y,x
        adc en_vy_hi,x
        sta en_y,x
        lda en_vy_hi,x
        bmi +
        jsr cat_lands           ; falling
+       lda en_y,x
        cmp #BOTTOM
        bcc +
        jmp reset_enemy         ; fallen out
+       rts

cat_vx_lo:  .byte <CAT_VX, <-CAT_VX
cat_vx_hi:  .byte >CAT_VX, >-CAT_VX

; The cat (en_i) falling: a surface in its middle column
; between its feet before (en_line) and now. There it sits,
; and waits. find_surface looks under `sensor`, Oscar's:
; kept on the stack.
cat_lands:
        lda sensor
        pha
        lda sensor + 1
        pha
        clc
        lda en_x_lo,x           ; its middle column
        adc #12
        sta sensor
        lda en_x_hi,x
        adc #0
        sta sensor + 1
        lda en_line
        sta probe_top
        lda en_y,x
        sta probe_low
        jsr find_surface        ; (X and Y change)
        ldx en_i
        bcc +
        sta en_y,x              ; on it
        lda #0
        sta en_y_frac,x
        sta en_vx_lo,x
        sta en_vx_hi,x
        sta en_vy_lo,x
        sta en_vy_hi,x
        sta en_air,x
        sta en_pic,x
        lda #CAT_WAIT
        sta en_timer,x
+       pla
        sta sensor + 1
        pla
        sta sensor
        rts

; Every enemy of the level at its start (respawn).
reset_enemies:
        ldx enemy_count
        beq _done
        dex
-       jsr reset_enemy
        dex
        bpl -
_done:
        rts

; Enemy X at its start, still, facing its way.
reset_enemy:
        lda en_start_lo,x
        sta en_x_lo,x
        lda en_start_hi,x
        sta en_x_hi,x
        lda en_start_y,x
        sta en_y,x
        lda en_start_dir,x
        sta en_dir,x
        lda #0
        sta en_x_frac,x
        sta en_y_frac,x
        sta en_vx_lo,x
        sta en_vx_hi,x
        sta en_vy_lo,x
        sta en_vy_hi,x
        sta en_timer,x
        sta en_air,x
        sta en_pic,x
        rts

; While he blinks, nothing counts. An enemy's box over his
; body: he is hit.
; box over his body: he is hit. Across, the boxes touch
; when |its x - his x| is up to his right edge less its
; left (both boxes the same from both sides); up and down,
; when its feet are less than its box's top over his feet,
; and not more than his height less the bottom of its box
; under them.
hit_enemies:
        lda protect
        beq _enemies
        dec protect
        rts
_enemies:
        ldx enemy_count
        bne +
        rts
+       dex
_one:
        ldy en_kind,x
        sec                     ; |its x - his x|
        lda en_x_lo,x
        sbc osc_x + 1
        sta en_dx
        lda en_x_hi,x
        sbc osc_x + 2
        bcs +
        sec                     ; negative: his - its
        lda osc_x + 1
        sbc en_x_lo,x
        sta en_dx
        lda osc_x + 2
        sbc en_x_hi,x
+       bne _next               ; 256 or more
        lda type_reach,y
        cmp en_dx
        bcc _next
        lda en_y,x              ; its feet - his
        sec
        sbc osc_y + 1
        bcc _over
        cmp type_up,y           ; under his: less than UP
        bcs _next
        bcc _hit
_over:
        eor #$ff                ; over his: d = his - its
        adc #1
        sta en_dx
        lda height
        sec
        sbc type_down,y
        cmp en_dx               ; d up to height - DOWN
        bcs _hit
_next:
        dex
        bpl _one
        rts
_hit:
        jmp hit

; Hit by enemy X: HIT_DAMAGE of the health,
; PROTECT_FRAMES of blinking. Out of the smoke, a jump back
; away from it, and KNOCK_FRAMES without the joystick. No
; health left: back at the lantern (or the start), as after
; a fall.
hit:
        ldy #0
        lda osc_x + 1           ; the enemy right of him?
        cmp en_x_lo,x
        lda osc_x + 2
        sbc en_x_hi,x
        bcs +
        ldy #2                  ; yes: to the left
+       sty hurt_dir
hurt:
        lda health
        sec
        sbc #HIT_DAMAGE
        bcs +
        lda #0
+       sta health
        lda #PROTECT_FRAMES
        sta protect
        lda osc_puff
        bne _health
        lda osc_form
        clc
        adc hurt_dir
        tay
        lda knock_x_lo,y
        sta osc_vx
        lda knock_x_hi,y
        sta osc_vx + 1
        ldy osc_form
        lda knock_y_lo,y
        sta osc_vy
        lda knock_y_hi,y
        sta osc_vy + 1
        lda #0
        sta osc_ground
        lda #KNOCK_FRAMES
        sta stun
_health:
        lda health
        bne +
        jmp fallen
+       rts

; The jump back: the vampire's, the bat's; to the right,
; then to the left; and up.
knock_x_lo: .byte <$0200, <$0180, <-$0200, <-$0180
knock_x_hi: .byte >$0200, >$0180, >-$0200, >-$0180
knock_y_lo: .byte <-$0200, <-$0100
knock_y_hi: .byte >-$0200, >-$0100

; Sprites 3-6: the enemies on the screen, in their order,
; four at most (the setting's env_slots). X register = x -
; camera + 31, from 0 to 343; Y register = feet + 29; the
; picture of its type, facing and step, in the pointers of
; both screens; the colour of its type.
place_enemies:
        lda $d010               ; sprites 3-6 off
        and #%10000111
        sta $d010
        lda $d015
        and #%10000111
        sta $d015
        lda #0
        sta en_slot
        tax
_one:
        cpx enemy_count
        bcs _done
        ldy env                 ; the setting's slots
        lda en_slot
        cmp env_slots,y
        bcs _done
        sec
        lda en_x_lo,x
        sbc camera
        sta en_reg
        lda en_x_hi,x
        sbc camera + 1
        sta en_reg + 1
        clc
        lda en_reg
        adc #31
        sta en_reg
        lda en_reg + 1
        adc #0
        bmi _next               ; left of the screen
        beq _show               ; 0-255
        cmp #1
        bne _next
        lda en_reg              ; 256-343
        cmp #344 - 256
        bcs _next
        lda #1
_show:
        sta en_reg + 1
        jsr place_enemy
        inc en_slot
_next:
        inx
        bne _one
_done:
        rts

; Enemy X into sprite 3 + en_slot.
place_enemy:
        lda en_slot
        asl a
        tay
        lda en_reg              ; X, Y
        sta $d006,y
        lda en_y,x
        clc
        adc #29
        sta $d007,y
        ldy en_slot
        lda en_reg + 1          ; the ninth bit
        beq +
        lda $d010
        ora slot_bits,y
        sta $d010
+       lda $d015               ; on
        ora slot_bits,y
        sta $d015
_picture:
        stx en_i                ; its picture: the four
        lda en_dir,x            ; blocks of its type (on a
        asl a                   ; multiple of 4), 2 a facing
        ora en_pic,x
        sta work
        lda en_kind,x
        tax
        lda type_block,x
        ora work
        ldx en_i
_block:
        sta SCREEN_A + POINTERS + 3,y
        sta SCREEN_B + POINTERS + 3,y
        stx en_i                ; the colour of its type
        lda en_kind,x
        tax
        lda type_colour,x
        sta $d02a,y
        ldx en_i
        rts

slot_bits:
        .byte %00001000, %00010000, %00100000, %01000000

; The flyer's wave: 64 lines up and down, a sine of 12.
wave:
        .char round(12 * sin(range(64) * 2.0 * pi / 64))
