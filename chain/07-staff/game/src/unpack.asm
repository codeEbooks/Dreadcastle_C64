; The data of the levels wait as they are (plain.asm,
; data.asm): the maps, the tables of the settings, their
; sets of characters. unpack_start and unpack_page copy
; them where they are used, a page at a time: at the
; start, and in the transitions (objects.asm).
; (From step 8 they are packed, and these routines unpack
; them.)

; Data at A (low), X (high), to copy to the page Y on
; up_on := 1.
unpack_start:
        sta up_src
        stx up_src + 1
        sty up_dst + 1
        lda #0
        sta up_dst
        lda #1
        sta up_on
        rts

; X pages of the data, if up_on (at the start).
unpack_pages:
        lda up_on
        beq _done
        stx up_pages
-       jsr unpack_page
        dec up_pages
        bne -
_done:
        rts

; The next 256 bytes: from up_src to up_dst, both on to
; the next page.
unpack_page:
        ldy #0
-       lda (up_src),y
        sta (up_dst),y
        iny
        bne -
        inc up_src + 1
        inc up_dst + 1
        rts
