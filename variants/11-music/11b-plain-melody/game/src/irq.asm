; Two raster interrupts a frame. On line 20, in the upper
; border, the top one sets the playfield: its scroll, the
; screen to show and the level's characters, its
; background (blue in the castle). On line 226 the HUD one
; sets the background black, scroll 0 and the HUD's
; characters for the three HUD rows, and tells the main
; loop to start. It comes on line 225 and waits for 226,
; to set $d021 in its left border: written while the
; picture is drawn, a colour register leaves a grey dot on
; the C64C's VIC-II.
; After the top one's work, a frame of music.

; The CIA's interrupts off; the KERNAL out (its ROM and its
; interrupts are not used), the vectors in RAM.
kernal_out:
        lda #%01111111          ; CIA interrupts off
        sta $dc0d               ; CIA 1: IRQ
        sta $dd0d               ; CIA 2: NMI
        lda $dc0d               ; clear what is pending
        lda $dd0d
        lda #0
        sta $dc02               ; CIA 1 port A: all inputs
        lda #$35                ; I/O in; BASIC, KERNAL out
        sta $01
        lda #<irq_top           ; the vectors, now in RAM
        sta $fffe
        lda #>irq_top
        sta $ffff
        lda #<nmi
        sta $fffa
        lda #>nmi
        sta $fffb
        rts

; The raster interrupts on.
init_irq:
        lda #TOP_LINE           ; first interrupt: line 20
        sta $d012
        lda $d011
        and #%01111111          ; line bit 8: 0
        sta $d011
        lda #%00000001          ; raster interrupt on
        sta $d01a
        sta $d019               ; clear one pending
        cli
        rts

; RESTORE: nothing happens.
nmi:
        rti

irq_top:
        pha
        lda play_d021           ; the playfield's background
        sta $d021
        lda xscroll             ; the playfield's scroll
        sta $d016
        lda shown_d018          ; the screen to show
        sta $d018
        inc frame_count
        lda #HUD_LINE - 1       ; next: the HUD (just
        sta $d012               ; before its line)
        lda #<irq_hud
        sta $fffe
        lda #>irq_hud
        sta $ffff
        lda #%00000001          ; done with this one
        sta $d019
        txa                     ; then a frame of music:
        pha                     ; it uses X and Y too
        tya
        pha
        jsr music_play
music_done:                     ; the tests look here
        pla
        tay
        pla
        tax
        pla
        rti

irq_hud:
        pha
        lda #HUD_LINE           ; wait for line 226
-       cmp $d012
        bne -
        lda #D021_SKY           ; the HUD's background, in
        sta $d021               ; the border: no grey dot
        lda #%00010000          ; multicolour, scroll 0
hud_write:                      ; the tests check the line
        sta $d016
        sta hud_flag            ; not 0: the loop can go
        lda #D018_HUD           ; the HUD's characters (the
        sta $d018               ; rest of line 226: blank)
        lda #TOP_LINE           ; next: the top
        sta $d012
        lda #<irq_top
        sta $fffe
        lda #>irq_top
        sta $ffff
        lda #%00000001
        sta $d019
        pla
        rti

; Wait for the HUD interrupt, then clear its flag.
wait_hud:
        lda hud_flag
        beq wait_hud
        lda #0
        sta hud_flag
        rts
