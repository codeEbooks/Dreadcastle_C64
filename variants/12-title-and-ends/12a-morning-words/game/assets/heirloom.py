"""The heirlooms of the family: drawn for the game.

An heirloom is sprite 7, one block: a multicolour sprite of 12 x 21
pixels two screen pixels wide, drawn in its top 16 lines (the box of
a metatile, 16 x 16 screen pixels, in its middle 8 pixels: the sprite
stands 4 screen pixels left of the box). Its colours:

  Y  its own colour ($d02e): yellow, the gold
  R  shared colour 1 ($d025): red, as for Oscar
  G  shared colour 2 ($d026): light grey, as for Oscar
  .  nothing: the sky behind

The plan gives six kinds, two to a level in turn (the odd levels:
chalice, portrait, medallion; the even ones: candelabrum, hourglass,
book). Level 1 has the first three; level 2 the other
three.
"""

OWN_COLOUR = 7                          # yellow
KINDS = {
    "chalice": [
        "..YYYYYYYY..",
        "..YGGYYYYY..",
        "..YGYYYYYY..",
        "...YYRRYY...",
        "...YYRRYY...",
        "....YYYY....",
        ".....YY.....",
        ".....YY.....",
        ".....YY.....",
        ".....YY.....",
        "....YYYY....",
        "...YYYYYY...",
        "...RRRRRR...",
        "............",
        "............",
        "............"],
    "portrait": [
        ".....YY.....",
        "....Y..Y....",
        "..YYYYYYYY..",
        "..YGGGGGGY..",
        "..YGGRRGGY..",
        "..YGRRRRGY..",
        "..YGGRRGGY..",
        "..YGRRRRGY..",
        "..YRRRRRRY..",
        "..YRRRRRRY..",
        "..YYYYYYYY..",
        "............",
        "............",
        "............",
        "............",
        "............"],
    "medallion": [
        ".....GG.....",
        "....G..G....",
        "....G..G....",
        ".....GG.....",
        "....YYYY....",
        "...YYYYYY...",
        "..YYGRRYYY..",
        "..YGRRRRYY..",
        "..YYRRRRYY..",
        "..YYYRRYYY..",
        "...YYYYYY...",
        "....YYYY....",
        "............",
        "............",
        "............",
        "............"],
    "candelabrum": [
        "............",
        "............",
        "............",
        "..R..R..R...",
        "..Y..Y..Y...",
        "..G..G..G...",
        "..Y..Y..Y...",
        "..Y..Y..Y...",
        "..YY.Y.YY...",
        "...YYYYY....",
        ".....Y......",
        ".....Y......",
        ".....Y......",
        "....YYY.....",
        "...YYYYY....",
        "..YYYYYYY..."],
    "hourglass": [
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "..YYYYYYYY..",
        "...G....G...",
        "...GRRRRG...",
        "....GRRG....",
        ".....RR.....",
        ".....GG.....",
        "....G..G....",
        "...G.RR.G...",
        "...GRRRRG...",
        "..YYYYYYYY.."],
    "book": [
        "............",
        "............",
        "............",
        "............",
        "..RRRRRRRR..",
        ".RYYYYYYYYR.",
        ".RYRRRRRRYR.",
        ".RYRRYYRRYR.",
        ".RYRRYYRRYR.",
        ".RYRRRRRRYR.",
        ".RYYYYYYYYR.",
        ".RGGGGGGGGR.",
        "..RRRRRRRR..",
        "............",
        "............",
        "............"],
}
BITS = {".": 0b00, "R": 0b01, "Y": 0b10, "G": 0b11}


def block(kind):
    """The 64 bytes of one heirloom's sprite."""
    rows = KINDS[kind]
    if len(rows) != 16 or any(len(row) != 12 for row in rows):
        raise ValueError(f"{kind}: 16 rows of 12 pixels")
    data = bytearray()
    for row in rows + ["." * 12] * 5:
        value = 0
        for letter in row:
            value = (value << 2) | BITS[letter]
        data += value.to_bytes(3, "big")
    return bytes(data + b"\0")
