"""Variants 10a and 10b (Tom): on to the Throne Tower with the staff,
into the arena; the fight until Tom is gone."""
from game_model import GO_ARENA, GO_NEXT


def route(v):
    return [
        ("on to level 8, the staff in hand (the test writes it)", 1, 0,
         None, None, dict(poke={"level_no": 6, "trans": 50,
                                "trans_kind": GO_NEXT, "has_staff": 1})),
        ("the transition into level 8", 49, 0, None, None),
        ("into the arena (the test writes it)", 1, 0, None, None,
         dict(poke={"trans": 50, "trans_kind": GO_ARENA})),
        ("the transition into the arena", 49, 0, None, None),
        ("Tom waits, then growls", v.Until(
            lambda m: any(e == "tom growls" for _, e in m.events), 400,
            "Tom growls"), v.FIGHT, None, None),
        ("the fight until Tom is beaten", v.Until(
            lambda m: any(e == "tom beaten" for _, e in m.events), 6000,
            "Tom beaten"), v.FIGHT, None, None),
        ("Tom runs away", v.Until(
            lambda m: any(e == "tom gone" for _, e in m.events), 600,
            "Tom gone"), v.FIGHT, None, "tom-gone.png"),
    ]
