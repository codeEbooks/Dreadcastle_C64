"""A player for the fight with Tom Darkfang, on the model.

The tests need a way to beat Tom that can be played on the C64. Tom's
moves depend only on where Oscar is, so the way is found by a player
that looks at the model (game_model.Game) before every frame and
chooses the joystick, as a person at the C64 looks at the screen:

  - Tom still and not struck since his last move (waiting, growling,
    landed, dazed: tom.asm, strike_tom): walk to where the staff
    reaches his box and Oscar's body does not touch it, facing him
    (from the left: x from Tom's x - 27 to - 10; from the right: + 34
    to + 51), braking on the way, and strike; not when the growl is
    nearly over;
  - a charge coming (the growl nearly over, his next move a charge)
    or going: jump over him, Up held, towards him; once he has gone
    past, follow him to the wall where he will be dazed;
  - a leap coming (his next move a leap) or going: walk away from
    where he will land (towards him, under the leap, at a wall);
  - else keep out of his reach.

Fighter is a joystick for the route of verify_game.py (as Beats):
at(frame) reads the model the test plays next to the C64. play()
plays a whole fight on a model (levels.py: Tom can be beaten).
"""

import game_model

R, L, U, F = game_model.GO_RIGHT, game_model.GO_LEFT, game_model.UP, \
    game_model.FIRE
RIGHT, LEFT = game_model.RIGHT, game_model.LEFT


class Fighter:
    """The joystick of the fight: the model `game` is read at every
    frame."""

    def __init__(self, game):
        self.game = game
        self.over = None        # the way of the jump over a charge
        self.away = None        # the way out of a leap
        self.fired = False      # Fire pushed, the blow going on

    def at(self, frame):
        return self.choose()

    def __str__(self):
        return "the fighter (tests/fight.py), looking at the model"

    __repr__ = __str__

    def choose(self):
        g, k, c = self.game, self.game.k, self.game.c
        tx, ox = g.tom_x >> 8, g.x >> 8
        state, timer = g.tom_state, g.tom_timer
        if state >= k["TS_YELP"]:                   # beaten
            return 0
        left_of = ox + 12 < tx + 24                 # Oscar left of Tom
        vx = game_model.signed(g.vx & 0xFFFF)     # (signed or not)
        toward, away = (R, L) if left_of else (L, R)
        gap = abs((ox + 12) - (tx + 24))
        growl = state == k["TS_GROWL"]
        # A charge coming or going: over him.
        soon = 10 if gap < 45 else 6
        if (growl and g.tom_next == 1 and timer <= soon) or \
                state == k["TS_CHARGE"]:
            if g.ground and growl:
                self.over = toward
                return U | toward
            if not g.ground:
                return U | (self.over or toward)
            coming = (g.tom_face == RIGHT) == left_of
            if not coming:                          # gone past: follow
                if gap > 60:
                    return R if g.tom_face == RIGHT else L
                return 0
            if gap < 70:
                self.over = toward
                return U | toward
            return 0
        # A leap coming or going: away from where he lands.
        if (growl and g.tom_next == 0 and timer <= 12) or \
                state == k["TS_LEAP"]:
            if state == k["TS_LEAP"] and self.away is not None:
                return self.away
            way = away
            if (way == L and ox < c["TOM_MIN_X"] + 40) or \
                    (way == R and ox > g.x_max - 40):
                way = toward
            self.away = way
            return way
        self.away = None
        late = growl and timer <= (16 if g.tom_next == 1 else 12)
        still = state in (k["TS_WAIT"], k["TS_GROWL"], k["TS_LAND"],
                          k["TS_DAZED"])
        if still and not g.tom_safe and not late:
            if left_of:
                low, high, face = tx - 27, tx - 10, RIGHT
            else:
                low, high, face = tx + 34, tx + 51, LEFT
            middle = (low + high) // 2
            if low <= ox <= high and g.ground:
                if g.face != face:
                    return R if face == RIGHT else L
                if g.blow == 0 and not self.fired:
                    self.fired = True
                    return F
                return 0
            self.fired = False
            brake = vx * vx // (2 * k["WALK_FRICTION"] * 256)
            if ox < middle:
                return R if ox + brake < middle else 0
            return L if ox - brake > middle else 0
        self.fired = False
        if gap < 50:                                # out of reach
            if (away == L and ox < c["TOM_MIN_X"] + 8) or \
                    (away == R and ox > g.x_max - 8):
                return 0
            return away
        return 0


def play(game, count, most=6000):
    """The fight on `game`, in the arena at Tom's start: the fighter
    plays until Tom has gone, the victory (or `most` frames).
    count: the frame counter (the top interrupt's). Returns the
    joystick of every frame and the counter after."""
    fighter = Fighter(game)
    joys = []
    for _ in range(most):
        joy = fighter.choose()
        joys.append(joy)
        count += 1
        game.turn(joy, count & 255)
        if game.game_state == game_model.ST_WON:
            break
    return joys, count
