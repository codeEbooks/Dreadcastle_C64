"""Variant 06a (a watchman at the start): Oscar waits; the watchman
walks into him."""


def route(v):
    return [
        ("wait: the watchman comes", v.Until(
            lambda m: any(e == "hit" for _, e in m.events), 400,
            "a hit"), 0, None, None, dict(event="hit")),
        ("thrown back, blinking", 20, 0, None, "watchman-at-start.png"),
        ("wait on", 200, 0, None, None),
    ]
