"""The packer: maps, settings' tables, sets of characters.

The data of
the levels are kept packed and unpacked where they are used, a page at
a time, in the transitions (game/src/unpack.asm). The format is a
plain LZ77, chosen to be short to unpack on the 6510:

  - a run of bytes as they are: a byte T from $00 to $7f, then T + 1
    bytes (1-128);
  - a run repeated from the output: a byte T from $80 to $ff, then a
    byte D; (T & $7f) + MIN_MATCH bytes (3-130) copied, one by one,
    from D + 1 bytes back (1-256). The copy goes forward, so a run may
    overlap what it makes: D = 0 and a length of 50 is one byte fifty
    times.

pack() finds, for every place of the data, the longest run that can
be repeated from the 256 bytes before it, then chooses the cheapest
way through the data from its end back to its start (each choice: a
run as it is, of 1 to 128 bytes, costing 1 + its length; or a repeat
of 3 up to the longest, costing 2). unpack() is the same thing as the
6510's, in Python: the tests use it, and pack() checks itself with it.

Standard library only.
"""

MIN_MATCH = 3                   # the shortest repeat: 2 bytes for 3
MAX_MATCH = 0x7F + MIN_MATCH    # the longest: 130
MAX_LITERAL = 0x80              # bytes as they are, in one run
WINDOW = 256                    # how far back a repeat can come from


def longest_repeats(data):
    """For each place: (length, distance) of the longest repeat, the
    nearest one when two are as long."""
    found = []
    for at in range(len(data)):
        limit = min(MAX_MATCH, len(data) - at)
        best = (0, 0)
        for distance in range(1, min(WINDOW, at) + 1):
            length = 0
            while length < limit and \
                    data[at - distance + length] == data[at + length]:
                length += 1
            if length > best[0]:
                best = (length, distance)
                if length == limit:
                    break
        found.append(best)
    return found


def pack(data):
    """The packed stream of `data` (bytes)."""
    data = bytes(data)
    size = len(data)
    repeats = longest_repeats(data)
    cost = [0] * (size + 1)         # bytes to pack data[at:]
    choice = [None] * size
    for at in range(size - 1, -1, -1):
        best = None
        for length in range(1, min(MAX_LITERAL, size - at) + 1):
            value = 1 + length + cost[at + length]
            if best is None or value < best:
                best, choice[at] = value, ("as is", length)
        for length in range(MIN_MATCH, repeats[at][0] + 1):
            value = 2 + cost[at + length]
            if value < best:
                best, choice[at] = value, ("repeat", length)
        cost[at] = best
    out = bytearray()
    at = 0
    while at < size:
        kind, length = choice[at]
        if kind == "as is":
            out.append(length - 1)
            out += data[at:at + length]
        else:
            out.append(0x80 | (length - MIN_MATCH))
            out.append(repeats[at][1] - 1)
        at += length
    packed = bytes(out)
    if unpack(packed, size) != data:
        raise ValueError("the packer does not unpack what it packed")
    return packed


def unpack(packed, size):
    """`size` bytes out of the packed stream, as unpack.asm makes them;
    the stream must end there."""
    out = bytearray()
    at = 0
    while len(out) < size:
        head = packed[at]
        if head < 0x80:
            out += packed[at + 1:at + head + 2]
            at += head + 2
        else:
            distance = packed[at + 1] + 1
            if distance > len(out):
                raise ValueError("a repeat from before the start")
            for _ in range((head & 0x7F) + MIN_MATCH):
                out.append(out[-distance])
            at += 2
    if len(out) != size or at != len(packed):
        raise ValueError("the stream does not end with the data")
    return bytes(out)


def runs(packed):
    """How many runs the stream has (for the measures)."""
    count = at = 0
    while at < len(packed):
        count += 1
        at += packed[at] + 2 if packed[at] < 0x80 else 2
    return count
