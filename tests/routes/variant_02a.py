"""Variant 02a (a slow camera, one pixel a frame): the route of step
2 (tests/step_routes.py) with twice its frames."""
from game_model import GO_LEFT as L, GO_RIGHT as R


def route(v):
    return [
        ("still: the back screen made ready", 20, 0, None,
         "scrolling-still.png"),
        ("right: the street scrolls, 1 pixel a frame", 320, R, None,
         "scrolling-right.png"),
        ("let go: the camera stops", 10, 0, None, None),
        ("left: the back screen made again, the other way", 80, L, None,
         None),
        ("right again", 60, R, None, None),
        ("right to the end of the level", 1800, R, None,
         "scrolling-end.png"),
        ("at the end: no more to the right", 20, R, None, None),
        ("left, all the way back", 1840, L, None, "scrolling-start.png"),
        ("at the start: no more to the left", 20, L, None, None),
    ]
