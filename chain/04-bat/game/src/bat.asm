; The bat. Oscar flies by beating his wings: every push of
; Up is a beat, that throws him up; let go, he falls,
; slowly, faster with Down held (a dive). Left and right
; steer him with a little sweep, as he walks (speed_step).
; Falling onto a surface he perches there, until a beat.
; Every beat uses up some energy; on a surface it comes
; back, slowly, and a moth eaten gives a third of it. When
; there is not enough for a beat, he turns back into the
; vampire at once and falls. The moths are in the level, a
; metatile each; their wings change every 8 frames
; (flutter_moths).

; The numbers of the flight: to change the feel of the game.
FLAP_SPEED    = $01c0           ; a beat: 1.75 pixels up
BAT_GRAVITY   = $0020           ; falling, let go
BAT_FALL_MAX  = $0140           ; 1.25 pixels a frame, most
BAT_DIVE      = $0040           ; falling with Down held
BAT_DIVE_MAX  = $0300           ; 3 pixels a frame at most
FLY_MAX_X     = $0180           ; 1.5 pixels a frame across
FLY_ACCEL     = $0014           ; speeding up
FLY_TURN      = $0020           ; turning round
FLY_DRAG      = $000c           ; slowing down, let go
BAT_TOP       = 14              ; feet never higher
BAT_MIDDLE    = 10              ; his middle: over the feet
BEAT_FRAMES   = 16              ; a beat of the wings, drawn

; The energy, in units of 256: ENERGY_FULL is the whole bar,
; six steps of ENERGY_STEP; the vampire needs a step to fly.
ENERGY_FULL   = 192
ENERGY_STEP   = 32
FLAP_COST     = 8               ; a beat: 24 beats in a bar
RECHARGE      = $0040           ; a frame on a surface: 0.25
MOTH_ENERGY   = 64              ; a moth: a third
GNAM_FRAMES   = 16              ; the moth in his mouth
        .cerror ENERGY_FULL != 6 * ENERGY_STEP, "6 steps"
        .cerror ENERGY_STEP != 32, "a step: energy / 32"

; His pictures: 12-16 facing right, 17-21 facing left.
BAT_PICTURES  = 12
FLY_A         = 0               ; wings up
FLY_B         = 1               ; level
FLY_C         = 2               ; down
PERCH         = 3               ; wings folded
GNAM          = 4               ; a moth in his mouth

; One frame of the bat. Up, pushed now and not in the frame
; before: a beat, if there is energy for it (else he is a
; vampire again). Perched, without a beat, he stays (left
; and right turn him round). Flying: the speed across, x;
; gravity, y; his feet never above BAT_TOP. Going down, a
; surface stops him: he perches. Then the moths.
move_bat:
        lda joy
        and #JOY_UP
        beq _perched
        lda prev_joy
        and #JOY_UP
        bne _perched            ; held from before
        lda energy + 1          ; the beat's energy
        sec
        sbc #FLAP_COST
        bcs +
        jsr transform           ; not enough: a vampire
        jmp oscar_done
+       sta energy + 1
        lda #<($10000 - FLAP_SPEED)
        sta osc_vy              ; thrown up
        lda #>($10000 - FLAP_SPEED)
        sta osc_vy + 1
        lda #0
        sta osc_ground          ; off the surface
        sta osc_flap            ; the wings beat
_perched:
        lda osc_ground
        beq _fly
        jsr push_across         ; perched: he only turns
        jmp _moths
_fly:
        jsr push_across
        ldy #FLY_ACROSS
        jsr speed_step
        jsr move_x
        lda joy                 ; gravity: Down held, a dive
        and #JOY_DOWN
        lsr a                   ; X: 0 or 1
        tax
        clc
        lda osc_vy
        adc bat_gravity_lo,x
        sta osc_vy
        lda osc_vy + 1
        adc bat_gravity_hi,x
        sta osc_vy + 1
        bmi _move_y             ; going up
        lda bat_fall_lo,x       ; no faster than its limit
        cmp osc_vy
        lda bat_fall_hi,x
        sbc osc_vy + 1
        bcs _move_y
        lda bat_fall_lo,x
        sta osc_vy
        lda bat_fall_hi,x
        sta osc_vy + 1
_move_y:
        clc                     ; y = y + vy
        lda osc_y
        adc osc_vy
        sta osc_y
        lda osc_y + 1
        adc osc_vy + 1
        sta osc_y + 1
        cmp #BAT_TOP            ; never above BAT_TOP
        bcs +
        lda #BAT_TOP
        sta osc_y + 1
        lda #0
        sta osc_y
        sta osc_vy
        sta osc_vy + 1
        beq _moths
+       lda osc_vy + 1
        bmi _up                 ; going up
        ora osc_vy
        beq _moths              ; level: nowhere to land
        jsr land                ; down: perched?
        lda osc_ground
        beq _moths
        lda #0                  ; perched: he stops
        sta osc_vx
        sta osc_vx + 1
_moths:
        jsr eat_moth
        jmp oscar_done
_up:
        jsr bump_head           ; his head under a block?
        jmp _moths

; Falling, let go and with Down held (a dive): gravity and
; the limit of the speed.
bat_gravity_lo: .byte <BAT_GRAVITY, <BAT_DIVE
bat_gravity_hi: .byte >BAT_GRAVITY, >BAT_DIVE
bat_fall_lo:    .byte <BAT_FALL_MAX, <BAT_DIVE_MAX
bat_fall_hi:    .byte >BAT_FALL_MAX, >BAT_DIVE_MAX

; On a surface: RECHARGE a frame, up to ENERGY_FULL.
charge_energy:
        lda energy + 1
        cmp #ENERGY_FULL
        bcs _done               ; full
        clc
        lda energy
        adc #<RECHARGE
        sta energy
        lda energy + 1
        adc #>RECHARGE
        cmp #ENERGY_FULL
        bcc +
        lda #0                  ; no more than full
        sta energy
        lda #ENERGY_FULL
+       sta energy + 1
_done:
        rts

; The bat's middle: the column under his feet, BAT_MIDDLE
; lines above them. A moth in that metatile: he eats it.
; It becomes empty sky, in the level and on the screens
; (set_tile). The energy goes up by MOTH_ENERGY, to
; ENERGY_FULL at most.
eat_moth:
        jsr sensor_column       ; X: the metatile column
        stx tile_col
        lda osc_y + 1
        sec
        sbc #BAT_MIDDLE
        lsr a
        lsr a
        lsr a
        lsr a
        sta tile_row
        tay
        lda (probe_col),y       ; the metatile
        cmp #MOTH_TILE
        beq +
        rts
+       inc moths_eaten
        lda #GNAM_FRAMES
        sta osc_gnam
        lda energy + 1          ; the energy, up
        clc
        adc #MOTH_ENERGY
        bcs _full
        cmp #ENERGY_FULL
        bcc _keep
_full:
        lda #0
        sta energy
        lda #ENERGY_FULL
_keep:
        sta energy + 1
        lda #EMPTY_SKY          ; gone
        sta new_tile
        jmp set_tile

; The picture of the bat: a moth in his mouth; perched; in
; the BEAT_FRAMES after a beat, the wings down, level, up,
; level, 4 frames each; else gliding, the wings level.
animate_bat:
        lda osc_flap            ; frames since the beat,
        cmp #BEAT_FRAMES        ; up to BEAT_FRAMES
        bcs +
        inc osc_flap
+       ldx #GNAM
        lda osc_gnam
        beq +
        dec osc_gnam
        jmp _set
+       ldx #PERCH
        lda osc_ground
        bne _set
        ldx #FLY_B              ; gliding
        lda osc_flap
        cmp #BEAT_FRAMES
        bcs _set
        lsr a                   ; in the beat: 4 frames
        lsr a                   ; a picture
        tax
        lda beat_cycle,x
        tax
_set:
        txa
        clc
        adc #BAT_PICTURES
        ldy osc_face
        beq +
        adc #5                  ; facing left
+       sta osc_pic
        rts

beat_cycle:
        .byte FLY_C, FLY_B, FLY_A, FLY_B
        .cerror BEAT_FRAMES != 16, "4 pictures, 4 frames"

; Every 8 frames the moths' wings change: one of their two
; pictures (frame_count AND 8) into their two characters.
flutter_moths:
        lda frame_count
        and #%00000111
        bne +
        lda frame_count
        and #%00001000          ; 0 or 8: picture 0 or 1
        asl a                   ; 16 bytes each
        tay
        ldx #0
-       lda moth_frames,y
        sta CHARSET + MOTH_CHAR * 8,x
        iny
        inx
        cpx #16
        bne -
+       rts
