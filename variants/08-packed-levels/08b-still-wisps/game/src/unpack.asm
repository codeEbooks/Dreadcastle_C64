; The packed data (the author's "Comprimere"): the maps of
; the levels, the tables of the settings and their sets of
; characters are kept packed (pack.py) and unpacked where
; they are used, a page at a time: at the start, and in
; the transitions (objects.asm). A packed stream is a list
; of runs, each led by a byte T:
;   T = $00-$7f: T + 1 bytes follow, to copy as they are
;   T = $80-$ff: (T & $7f) + MIN_MATCH bytes to repeat from
;     the output already made: the next byte is how far
;     back, less 1 (1-256 bytes). The copy goes forward, so
;     it may repeat what it is making.
; Both kinds are a copy of up_run bytes from up_from: the
; stream itself, or the output behind up_dst.

; A stream: packed data at A (low), X (high), unpacked to
; the page Y on; up_on := 1.
unpack_start:
        sta up_src
        stx up_src + 1
        sty up_dst + 1
        lda #0
        sta up_dst
        sta up_run              ; no run going on
        lda #1
        sta up_on
        rts

; X pages of the stream, if up_on (at the start).
unpack_pages:
        lda up_on
        beq _done
        stx up_pages
-       jsr unpack_page
        dec up_pages
        bne -
_done:
        rts

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
; HIGH_DATA_2, HIGH_PAGES_2 pages (SET_SLOT is filled
; again when a level's set is unpacked there).
move_high:
        lda #>HIGH_LOAD
        ldy #>HIGH_DATA
        ldx #HIGH_PAGES
        jsr move_pages
        lda #>SET_SLOT
        ldy #>HIGH_DATA_2
        ldx #HIGH_PAGES_2
        jmp move_pages

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
