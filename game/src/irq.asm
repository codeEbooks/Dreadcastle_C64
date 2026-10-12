; Two raster interrupts a frame. On line 20, in the upper
; border, the top one sets the playfield: its scroll, the
; screen to show and the level's characters. On line 226 {-8}
; the HUD one sets scroll 0 and the HUD's characters for {-8}
; the three HUD rows, and tells the main loop to start. {-8}
; screen to show and the level's characters, its {9}
; background (blue in the castle). On line 226 the HUD one {9}
; sets the background black, scroll 0 and the HUD's {9}
; characters for the three HUD rows, and tells the main {9}
; loop to start. It comes on line 225 and waits for 226, {9}
; to set $d021 in its left border: written while the {9}
; picture is drawn, a colour register leaves a grey dot on {9}
; the C64C's VIC-II. {9}
; After the top one's work, a frame of music. {11-12}
; After the top one's work, a frame of music and of the {13}
; sound effects. {13}
; With a band of text over the playfield (band_on, {12}
; states.asm) two more between them: on a line of the {12}
; band's first row the HUD's characters, on a line of its {12}
; last row the playfield's again. Both rows are blank, in {12}
; both sets: the change can come anywhere in their lines. {12}

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
        lda play_d021           ; the playfield's background {9}
        sta $d021 ; {9}
        lda xscroll             ; the playfield's scroll
        sta $d016
        lda shown_d018          ; the screen to show
        sta $d018
        inc frame_count
        lda band_on             ; a band of text: {12}
        beq _hud                ; its interrupt next {12}
        lda band_top ; {12}
        sta $d012 ; {12}
        lda #<irq_band ; {12}
        sta $fffe ; {12}
        lda #>irq_band ; {12}
        sta $ffff ; {12}
        jmp _done ; {12}
_hud: ; {12}
;|        lda #HUD_LINE           ; next: the HUD {-8}
;|        sta $d012 ; {-8}
        lda #HUD_LINE - 1       ; next: the HUD (just {9}
        sta $d012               ; before its line) {9}
        lda #<irq_hud
        sta $fffe
        lda #>irq_hud
        sta $ffff
_done: ; {12}
        lda #%00000001          ; done with this one
        sta $d019
        txa                     ; then a frame of music: {11}
        pha                     ; it uses X and Y too {11}
        tya ; {11}
        pha ; {11}
        jsr music_play ; {11}
        jsr sfx_play            ; and of the effects {13}
music_done:                     ; the tests look here {11}
        pla ; {11}
        tay ; {11}
        pla ; {11}
        tax ; {11}
        pla
        rti

; The band's first row: the HUD's characters, with the {12}
; screen shown (band_d018). {12}
irq_band: ; {12}
        pha ; {12}
        lda band_d018 ; {12}
        sta $d018 ; {12}
        lda band_end            ; next: its last row {12}
        sta $d012 ; {12}
        lda #<irq_band_off ; {12}
        sta $fffe ; {12}
        lda #>irq_band_off ; {12}
        sta $ffff ; {12}
        lda #%00000001 ; {12}
        sta $d019 ; {12}
        pla ; {12}
        rti ; {12}

; Its last row: the playfield's characters again; next, {12}
; the HUD. {12}
irq_band_off: ; {12}
        pha ; {12}
        lda shown_d018 ; {12}
        sta $d018 ; {12}
        lda #HUD_LINE - 1 ; {12}
        sta $d012 ; {12}
        lda #<irq_hud ; {12}
        sta $fffe ; {12}
        lda #>irq_hud ; {12}
        sta $ffff ; {12}
        lda #%00000001 ; {12}
        sta $d019 ; {12}
        pla ; {12}
        rti ; {12}

irq_hud:
        pha
        lda #HUD_LINE           ; wait for line 226 {9}
-       cmp $d012 ; {9}
        bne - ; {9}
        lda #D021_SKY           ; the HUD's background, in {9}
        sta $d021               ; the border: no grey dot {9}
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
