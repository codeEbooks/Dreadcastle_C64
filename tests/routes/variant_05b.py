"""Variant 05b (a night of one minute): Oscar waits at the start
until dawn; level 1 from its start again."""


def route(v):
    return [
        ("wait at the start until dawn", v.Until(
            lambda m: any(e == "dawn" for _, e in m.events), 4000,
            "dawn"), 0, "street", None, dict(event="dawn")),
        ("the transition: level 1 again", 50, 0, "street", None),
        ("level 1 from its start, the night full", 30, 0, "street",
         None),
    ]
