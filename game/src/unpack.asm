; The data of the levels wait as they are (plain.asm, {-7}
; data.asm): the maps, the tables of the settings, their {-7}
; sets of characters. unpack_start and unpack_page copy {-7}
; them where they are used, a page at a time: at the {-7}
; start. {-4}
; start, and in the transitions (objects.asm). {5-7}
; (From step 8 they are packed, and these routines unpack {-7}
; them.) {-7}
; The packed data (the author's "Comprimere"): the maps of {8}
; the levels, the tables of the settings and their sets of {8}
; characters are kept packed (pack.py) and unpacked where {8}
; they are used, a page at a time: at the start, and in {8}
; the transitions (objects.asm). A packed stream is a list {8}
; of runs, each led by a byte T: {8}
;   T = $00-$7f: T + 1 bytes follow, to copy as they are; {8}
;   T = $80-$ff: (T & $7f) + MIN_MATCH bytes to repeat from {8}
;     the output already made: the next byte is how far {8}
;     back, less 1 (1-256 bytes). The copy goes forward, so {8}
;     it may repeat what it is making. {8}
; Both kinds are a copy of up_run bytes from up_from: the {8}
; stream itself, or the output behind up_dst. {8}

; Data at A (low), X (high), to copy to the page Y on; {-7}
; up_on := 1. {-7}
; A stream: packed data at A (low), X (high), unpacked to {8}
; the page Y on; up_on := 1. {8}
unpack_start:
        sta up_src
        stx up_src + 1
        sty up_dst + 1
        lda #0
        sta up_dst
        sta up_run              ; no run going on {8}
        lda #1
        sta up_on
        rts

; X pages of the data, if up_on (at the start). {-7}
; X pages of the stream, if up_on (at the start). {8}
unpack_pages:
        lda up_on
        beq _done
        stx up_pages
-       jsr unpack_page
        dec up_pages
        bne -
_done:
        rts

; The next 256 bytes: from up_src to up_dst, both on to {-7}
; the next page. {-7}
;|unpack_page: ; {-7}
;|        ldy #0 ; {-7}
;|-       lda (up_src),y ; {-7}
;|        sta (up_dst),y ; {-7}
;|        iny ; {-7}
;|        bne - ; {-7}
;|        inc up_src + 1 ; {-7}
;|        inc up_dst + 1 ; {-7}
;|        rts ; {-7}

;{8}
; The next 256 bytes of the stream: up_dst, on a page, goes
; to the next. A run cut at the page's end goes on at the
; next call (up_run, up_from).
unpack_page:
_next:
        lda up_run              ; a run going on?
        bne _copy
        ldy #0                  ; no: the next one's byte
        lda (up_src),y
        bmi _repeat
        tax                     ; T + 1 bytes as they are
        inx
        stx up_run
        inc up_src              ; from the stream, after T
        bne +
        inc up_src + 1
+       lda up_src
        sta up_from
        clc                     ; and the stream goes on
        adc up_run              ; after them
        sta up_src
        lda up_src + 1
        sta up_from + 1
        adc #0
        sta up_src + 1
        bne _copy               ; (never 0: not in page 0)
_repeat:
        and #$7f                ; (T & $7f) + MIN_MATCH
        clc
        adc #MIN_MATCH
        sta up_run
        iny
        lda (up_src),y          ; from D + 1 bytes back:
        eor #$ff                ; - (D + 1) is $ff00 + ~D
        clc
        adc up_dst
        sta up_from
        lda up_dst + 1
        adc #$ff
        sta up_from + 1
        lda up_src              ; the stream: 2 bytes on
        clc
        adc #2
        sta up_src
        bcc _copy
        inc up_src + 1
_copy:
        lda up_dst              ; 255 - low: the room on the
        eor #$ff                ; page, less 1
        cmp up_run
        bcs _whole              ; the run fits in the page
        adc #1                  ; (carry clear) the room
        bne _count
_whole:
        lda up_run
_count:
        sta up_n                ; bytes to copy now: 1-130
        ldy #0
-       lda (up_from),y
        sta (up_dst),y
        iny
        cpy up_n
        bne -
        lda up_run              ; what is left of the run
        sec
        sbc up_n
        sta up_run
        tya                     ; from: n on
        clc
        adc up_from
        sta up_from
        bcc +
        inc up_from + 1
+       tya                     ; to: n on; at the end of
        clc                     ; the page the next, done
        adc up_dst
        sta up_dst
        bne _next
        inc up_dst + 1
        rts

; At the start: the packed data that wait under the KERNAL
; come in the PRG at HIGH_LOAD, where the level is copied
; later; they go to HIGH_DATA, HIGH_PAGES pages. (A write
; under a ROM reaches the RAM; the program reads them with
; the KERNAL out.) More come at SET_SLOT; they go to
; HIGH_DATA_2, HIGH_PAGES_2 pages (SET_SLOT is filled {-11}
; again when a level's set is unpacked there). {-9}
; again when a level's set is unpacked there); more at {10-11}
; SCREEN_A, to HIGH_DATA_3, the screens left empty. {10-11}
; HIGH_DATA_2, HIGH_PAGES_2 pages (SET_SLOT is not {12}
; emptied: the title's set fills it at once); more at {12}
; SCREEN_A, to HIGH_DATA_3; after them the code of the {12}
; states, to STATE_CODE; the screens left empty. {12}
move_high:
        lda #>HIGH_LOAD
        ldy #>HIGH_DATA
        ldx #HIGH_PAGES
        jsr move_pages
        lda #>SET_SLOT
        ldy #>HIGH_DATA_2
        ldx #HIGH_PAGES_2
;|        jmp move_pages ; {8-9}
        jsr move_pages ; {10}
        lda #>SCREEN_A          ; the third {10}
        ldy #>HIGH_DATA_3 ; {10}
        ldx #HIGH_PAGES_3 ; {10}
        jsr move_pages ; {10}
        lda #>STATE_LOAD        ; the states' code, low {12}
        ldy #>STATE_CODE ; {12}
        ldx #STATE_PAGES ; {12}
        jsr move_pages ; {12}
        lda #>SCREEN_A          ; the two screens empty {10}
        ldx #8 ; {10}
; X pages from page A on: zeros. {10}
zero_pages: ; {10}
        sta up_dst + 1 ; {10}
        lda #0 ; {10}
        sta up_dst ; {10}
        tay ; {10}
-       sta (up_dst),y ; {10}
        iny ; {10}
        bne - ; {10}
        inc up_dst + 1 ; {10}
        dex ; {10}
        bne - ; {10}
        rts ; {10}

; X pages from page A to page Y.
move_pages:
        sta up_src + 1
        sty up_dst + 1
        ldy #0
        sty up_src
        sty up_dst
-       lda (up_src),y
        sta (up_dst),y
        iny
        bne -
        inc up_src + 1
        inc up_dst + 1
        dex
        bne -
        rts
;{}
