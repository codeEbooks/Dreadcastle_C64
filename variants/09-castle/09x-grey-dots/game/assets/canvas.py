"""A canvas of C64 multicolour pixels, and the drawing tools.

The playfield of Dreadcastle is drawn in the C64's multicolour
character mode: a pixel is two screen pixels wide, so a character
cell is 4 x 8 pixels here and the 40 x 22 cells of the playfield are
160 x 176 pixels. Each pixel holds a C64 colour number (0-15).
"""

WIDTH, HEIGHT = 160, 176          # multicolour pixels
CELL_W, CELL_H = 4, 8
# Not a C64 colour: black as a cell's own colour (bits 11), not
# as the background (bits 00): a sprite behind the characters ($d01b)
# is hidden by it.
INK = 17


class Canvas:
    def __init__(self, colour, width=WIDTH, height=HEIGHT):
        self.width, self.height = width, height
        self.pixels = [[colour] * width for _ in range(height)]
        # cells drawn as hi-res characters: (col, row) -> (bytes, colour)
        self.hires = {}

    def plot(self, x, y, colour):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[y][x] = colour

    def get(self, x, y):
        return self.pixels[y][x]

    def rect(self, x0, y0, x1, y1, colour):
        """Fill the rectangle from (x0, y0) to (x1, y1), inclusive."""
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.plot(x, y, colour)

    def hline(self, x0, x1, y, colour):
        self.rect(x0, y, x1, y, colour)

    def vline(self, x, y0, y1, colour):
        self.rect(x, y0, x, y1, colour)

    def ellipse(self, cx, cy, rx, ry, colour):
        """Fill an ellipse; rx in multicolour pixels, ry in lines."""
        for y in range(cy - ry, cy + ry + 1):
            for x in range(cx - rx, cx + rx + 1):
                dx = (x - cx) / (rx + 0.5)
                dy = (y - cy) / (ry + 0.5)
                if dx * dx + dy * dy <= 1.0:
                    self.plot(x, y, colour)

    def blit(self, x0, y0, rows, palette):
        """Copy a drawing: rows of letters, palette letter -> colour.
        '.' leaves the canvas as it is."""
        for dy, line in enumerate(rows):
            for dx, letter in enumerate(line):
                if letter != ".":
                    self.plot(x0 + dx, y0 + dy, palette[letter])

    def triangle_roof(self, apex_x, apex_y, base_y, slope, colour):
        """A roof: from the apex down to base_y, widening by `slope`
        multicolour pixels every two lines on each side."""
        for y in range(apex_y, base_y + 1):
            half = ((y - apex_y) * slope) // 2
            self.hline(apex_x - half, apex_x + half, y, colour)

    def cell_colours(self, col, row):
        return {self.pixels[row * CELL_H + y][col * CELL_W + x]
                for y in range(CELL_H) for x in range(CELL_W)}
