"""The guided variants and the "Where it breaks" versions of the chain.

Read by tools/make_variants.py, which builds each one in
variants/NN-name/ID/ from chain/NN-name/, proves it and writes its
README.md. After tools/variants.py of volume 2 (Cryptmorrow).

A variant is one idea changed in one place of the step. When the
change is in the data (game/assets), the test's model reads the same
data; when it is in the Assembly, the same change is made in the
model (`model`: Python statements run before the model is made, on
`numbers`, the complete game's numbers, or on `game_model`). The test
then compares the changed program with the changed model frame by
frame, on the step's own route or on one of its own (`route`:
tests/routes/variant_ID.py; `shows=False`: what the step must show on
its own route is not asked). `expect` are facts of the test's report
that show the change (Python on `r`, the report; `entry(r, text)`:
the first step of the route whose description starts with text;
`hud(r)`: the HUD's three rows at the end, as text).

A break is a classic mistake made on purpose: the step's own test
must stop it (`fails`: the name of the check that stops it), and
`after` frames later `shot` photographs it.

Edits: (file in the step folder, old text, new text); the old text
must be there exactly once. Everything the reader reads (README) is
in English.
"""

VARIANTS = [
    # --- step 01: the village at night ------------------------------
    dict(id="01a-churchyard-first", step=1, kind="variant",
         title="The churchyard first",
         summary="The program starts in level 2, the Churchyard: the "
                 "level is a number, and everything else is data.",
         edits=[("game/src/main.asm",
                 "        lda #0                  ; level 1",
                 "        lda #1                  ; level 2")],
         model=["game_model.Game.first_level = 1"],
         where="`game/src/main.asm`, at `entry`: the number given to "
               "`load_level` in `level_no` (0 for level 1).",
         see="The Churchyard at night, its graves and its chapel, "
             "with 2 THE CHURCHYARD in the HUD. `load_level` takes the "
             "map, the setting and the name of whatever level "
             "`level_no` says; the churchyard shares the village's "
             "characters, so nothing else is needed.",
         limits="In this step the data of levels 1 to 3 are in memory "
                "(`plain.asm`): 0, 1 or 2. Level 3, the Wild Wood, "
                "needs characters of its own, which this step does not "
                "copy into place yet (step 07 does).",
         depends="The test's model starts at the same level "
                 "(`first_level`).",
         expect=[("level 2 on the screen",
                  "entry(r, 'the village')['level'] == 2"),
                 ("its name in the HUD's last row",
                  "'2 THE CHURCHYARD' in hud(r)[2]")]),
    dict(id="01b-another-name", step=1, kind="variant",
         title="Another name",
         summary="The level's name in the HUD is data: THE SLEEPING "
                 "VILLAGE instead of VILLAGE OF MORTALS.",
         edits=[("game/assets/level1.py",
                 'NAME = "VILLAGE OF MORTALS"',
                 'NAME = "THE SLEEPING VILLAGE"')],
         model=[],
         where="`game/assets/level1.py`, `NAME`; `build_assets.py` "
               "turns it into row 24 of the HUD (`name_row`): the "
               "level's number, the name in cyan, the score.",
         see="Row 24 of the HUD with the new name; `show_name` copies "
             "its 40 characters and 40 colours into both screens and "
             "the colour RAM.",
         limits="At most 30 characters, and only letters the HUD's "
                "font has (`font.py`); the score keeps its place.",
         depends="Nothing else: the name is copied as it is.",
         expect=[("the new name in the HUD's last row",
                  "'THE SLEEPING VILLAGE' in hud(r)[2]")]),
    dict(id="01x-hires-village", step=1, kind="break",
         title="The village in thin stripes",
         summary="The scroll value of the playfield without its "
                 "multicolour bit.",
         edits=[("game/src/scroll.asm",
                 "        eor #%00010111          ; bit 4: multicolour",
                 "        eor #%00000111          ; bit 4: multicolour")],
         fails="$d016 and $d018 from the frame before", after=2,
         shot="hires-village.png",
         symptom="The village loses its colours: grey and white "
                 "houses, roofs and street in fine stripes. The HUD is "
                 "right.",
         cause="Bit 4 of $D016 turns multicolour on. `set_xscroll` "
               "keeps it in `xscroll` with the 3 bits of the fine "
               "scroll; without it the top interrupt sets the "
               "high-resolution mode: every byte of a character "
               "becomes 8 pixels of one colour on the background, "
               "instead of 4 pixels of four colours, and that colour "
               "is the whole value of its colour RAM, whose bit 3 (the "
               "multicolour flag) makes it one of the light colours "
               "8-15. The HUD's interrupt writes its own value "
               "(`%00010000`), so the HUD is still in multicolour."),
    # --- step 02: the scrolling --------------------------------------
    dict(id="02a-slow-camera", step=2, kind="variant",
         title="A slow camera",
         summary="The camera moves one pixel a frame instead of two.",
         edits=[("game/src/scroll.asm",
                 "        lda #2\n        sta speed",
                 "        lda #1\n        sta speed")],
         model=["game_model.Game.camera_speed = 1"],
         route="variant_02a.py",
         where="`game/src/scroll.asm`, `steer_camera`: the speed "
               "given to `camera_right` and `camera_left`.",
         see="The street glides twice as slowly; a new column every 8 "
             "frames, and the back screen, ready in 3, never makes the "
             "camera wait.",
         limits="From 1 to 8 pixels a frame (more would skip a "
                "column). From step 03 the camera follows Oscar and "
                "this speed is his.",
         depends="The test's model moves its camera by the same speed "
                 "(`camera_speed`); its route takes twice the frames.",
         expect=[("one pixel a frame",
                  "entry(r, 'right:')['camera_to'] - "
                  "entry(r, 'right:')['camera_from'] == "
                  "entry(r, 'right:')['frames']"),
                 ("the camera never waits going one way",
                  "entry(r, 'right to the end')['camera_waits'] == "
                  "entry(r, 'right again')['camera_waits']")]),
    dict(id="02b-fast-camera", step=2, kind="variant",
         title="A camera faster than the back screen",
         summary="The camera moves four pixels a frame: faster than "
                 "the back screen can be made ready.",
         edits=[("game/src/scroll.asm",
                 "        lda #2\n        sta speed",
                 "        lda #4\n        sta speed")],
         model=["game_model.Game.camera_speed = 4"],
         where="`game/src/scroll.asm`, `steer_camera`: the speed.",
         see="A new column every 2 frames, but the back screen needs "
             "3 more after a swap (two to move the rows, one for the "
             "new column): at the edge of each column the camera waits "
             "(`_hold`) until it is ready. The street moves in jerks "
             "and, on average, no faster than at two pixels a frame: "
             "8 pixels in 4 frames is all the back screen allows. That "
             "is why `steer_camera` says 2.",
         limits="The cure would be a back screen made in fewer stages, "
                "at the price of a longer frame.",
         depends="The test's model waits the same way (`holds`).",
         expect=[("the camera waits at the edge of its columns",
                  "entry(r, 'right:')['camera_waits'] > 70"),
                 ("no faster than two pixels a frame",
                  "entry(r, 'right:')['camera_to'] - "
                  "entry(r, 'right:')['camera_from'] <= "
                  "2 * entry(r, 'right:')['frames'] + 8")]),
    dict(id="02x-colours-left-behind", step=2, kind="break",
         title="Colours left behind",
         summary="At a swap the colour RAM of rows 11-21 is not moved: "
                 "the characters of the lower half go on, their "
                 "colours stay.",
         edits=[("game/src/scroll.asm",
                 "        jsr colour_half         ; rows 11-21\n",
                 "")],
         fails="colour RAM equals the model", after=60,
         shot="colours-left-behind.png",
         symptom="Scrolling right, the top half of the street is "
                 "right; in the bottom half patches of the wrong colour "
                 "appear on the walls, the windows and the stalls, and "
                 "change at every swap: the characters have moved on, "
                 "their paint has not.",
         cause="Both screens have their own characters, but there is "
               "only one colour RAM: at every swap `do_swap` moves it "
               "by a column, in place, the top half (`colour_half` with "
               "the first routine) and the bottom half (the second). "
               "Without the second, rows 11-21 keep the colours of the "
               "column before, while their characters move one column "
               "at every swap."),
    # --- step 03: Oscar --------------------------------------------
    dict(id="03a-higher-jump", step=3, kind="variant",
         title="A higher jump",
         summary="Oscar leaves the ground at 4 pixels a frame instead "
                 "of 3.47: Up held, he rises 62 lines instead of 47.",
         edits=[("game/src/oscar.asm",
                 "JUMP_SPEED    = $0378           ; 3.47 pixels a frame "
                 "up;",
                 "JUMP_SPEED    = $0400           ; 4 pixels a frame "
                 "up;")],
         model=["numbers['JUMP_SPEED'] = 0x0400"],
         route="variant_03a.py",
         where="`game/src/oscar.asm`, `JUMP_SPEED`: the speed up when "
               "he leaves the ground, in 1/256 of a pixel a frame.",
         see="The jump goes higher and lasts longer; with Up let go "
             "early it is still short, because `GRAVITY` (let go) is "
             "stronger than `GRAVITY_HOLD` (held).",
         limits="The height grows with the square of the speed: "
                "(speed in pixels)^2 / (2 x 0.125). The levels are "
                "drawn for a jump of 2 metatiles, never 3: with this "
                "one he climbs 3, and places meant for the bat or for "
                "a longer way round may come within a jump.",
         depends="The test's model jumps with the same number "
                 "(`numbers['JUMP_SPEED']`).",
         expect=[("62 lines up, Up held",
                  "entry(r, 'Up held')['feet'] == 144 - 62")]),
    dict(id="03b-faster-walk", step=3, kind="variant",
         title="A faster walk",
         summary="Oscar walks at 2.25 pixels a frame at most, instead "
                 "of 1.5.",
         edits=[("game/src/oscar.asm",
                 "WALK_MAX      = $0180           ; 1.5 pixels a frame",
                 "WALK_MAX      = $0240           ; 2.25 pixels a "
                 "frame")],
         model=["numbers['WALK_MAX'] = 0x0240"],
         route="variant_03b.py",
         where="`game/src/oscar.asm`, `WALK_MAX`: the top speed of the "
               "walk; `WALK_ACCEL` takes him there, 1/16 of a pixel "
               "more each frame.",
         see="He reaches the crates in 55 frames instead of 67, and "
             "takes longer to stop (`WALK_FRICTION`).",
         limits="The camera follows him at his speed: above 8 pixels a "
                "frame it would skip columns, and above 2 the back "
                "screen is not ready in time (see step 02): the camera "
                "waits, and he gets ahead of it.",
         depends="The jumps are longer too: their length is the speed "
                 "across times the time in the air.",
         expect=[("at the crates in 55 frames",
                  "entry(r, 'walk right to the crates')['frames'] == 55")
                 ]),
    dict(id="03x-sign-lost", step=3, kind="break",
         title="A step to the left, 256 pixels to the right",
         summary="Moving left, the speed is added to his position "
                 "without its sign in the top byte.",
         edits=[("game/src/oscar.asm",
                 "        lda osc_vx + 1\n        bpl +\n        dex\n",
                 "        lda osc_vx + 1\n        bpl +\n        nop\n")],
         fails="Oscar's variables equal the model", after=30,
         shot="sign-lost.png",
         symptom="Oscar walks left from the start and, at the first "
                 "frame, is 256 pixels further right; the camera runs "
                 "after him.",
         cause="Positions have three bytes (fraction, pixels, 256s of "
               "pixels), speeds two. A speed to the left is negative: "
               "$FFF0 is -16. Added to three bytes, its third byte must "
               "be $FF, the sign carried on (`dex` makes X $FF); with 0 "
               "the carry out of the second byte is not cancelled, and "
               "the third byte goes up by one: 256 pixels."),
    # --- step 04: the bat --------------------------------------------
    dict(id="04a-tireless-bat", step=4, kind="variant",
         title="A tireless bat",
         summary="A beat costs 4 units of energy instead of 8: 48 beats "
                 "in a full bar instead of 24.",
         edits=[("game/src/bat.asm",
                 "FLAP_COST     = 8               ; a beat: 24 beats in "
                 "a bar",
                 "FLAP_COST     = 4               ; a beat: 48 beats in "
                 "a bar")],
         model=["numbers['FLAP_COST'] = 4"],
         route="variant_04a.py",
         where="`game/src/bat.asm`, `FLAP_COST`: what a beat takes "
               "from `energy` (in 256ths: 192 is the full bar).",
         see="The bat climbs and hovers twice as long before it "
             "turns back into the vampire and falls; the bar of the "
             "energy goes down by half a character a beat.",
         limits="The levels are planned for 24 beats: over the canal "
                "or the moat the bat now has energy to spare. A cost "
                "of 0 would never run out.",
         depends="The energy comes back on a surface (`RECHARGE`) and "
                 "with a moth (`MOTH_ENERGY`) as before.",
         expect=[("48 beats before the energy runs out",
                  "entry(r, 'beats until')['events'].get('beat') "
                  "== 48")]),
    dict(id="04b-slow-descent", step=4, kind="variant",
         title="A slow descent",
         summary="Let go, the bat falls at 0.625 pixels a frame at "
                 "most, instead of 1.25.",
         edits=[("game/src/bat.asm",
                 "BAT_FALL_MAX  = $0140           ; 1.25 pixels a "
                 "frame, most",
                 "BAT_FALL_MAX  = $00a0           ; 0.625 pixels a "
                 "frame, most")],
         model=["numbers['BAT_FALL_MAX'] = 0x00a0"],
         route="variant_04b.py",
         where="`game/src/bat.asm`, `BAT_FALL_MAX`: the top speed of "
               "the fall, let go (with Down held the dive has its own, "
               "`BAT_DIVE_MAX`).",
         see="From the top of the sky to the roof over the start the "
             "bat floats down in 71 frames instead of 39; Down still "
             "dives as fast as before.",
         limits="Below `BAT_GRAVITY` ($0020) the speed would be "
                "reached in one frame and the fall would look flat.",
         depends="Nothing else: perching, beats and energy are the "
                 "same.",
         expect=[("down from the top in 71 frames",
                  "entry(r, 'let go')['frames'] == 71")]),
    dict(id="04x-endless-energy", step=4, kind="break",
         title="Endless energy",
         summary="A beat no longer checks that there is energy for "
                 "it.",
         edits=[("game/src/bat.asm",
                 "        bcs +\n        jsr transform           ; not "
                 "enough: a vampire",
                 "        jmp +\n        jsr transform           ; not "
                 "enough: a vampire")],
         fails="Oscar's form, smoke, energy, moths equal the model",
         after=20, shot="endless-energy.png",
         symptom="When the bar is empty the bat beats on, and the bar "
                 "is full again: the bat never has to come down.",
         cause="`sbc #FLAP_COST` leaves the carry clear when the energy "
               "is less than the cost: the subtraction has borrowed. "
               "`bcs` keeps the beat only without a borrow; with `jmp` "
               "the result, 8 less than a small number, wraps round to "
               "near 256, more than the full bar (192)."),
    # --- step 05: heirlooms and the gate ------------------------------
    dict(id="05a-chalice-on-the-street", step=5, kind="variant",
         title="The chalice on the street",
         summary="The first heirloom moved from the awning of the stall "
                 "to the street by the start: the objects are data.",
         edits=[("game/assets/level1.py",
                 'HEIRLOOMS = [(22, 80, "chalice"),       # on the '
                 'awning, h3',
                 'HEIRLOOMS = [(6, 128, "chalice"),       # on the '
                 'street')],
         model=[],
         route="variant_05a.py",
         where="`game/assets/level1.py`, `HEIRLOOMS`: the metatile "
               "column of each, the line of the top of its 16 x 16 box "
               "and its kind.",
         see="The chalice bobs over the street a few steps from the "
             "start; Oscar takes it walking, and the HUD counts 1/3.",
         limits="Its box must be where Oscar can reach it: on a "
                "surface, or within a jump or a flight. Three "
                "heirlooms a level (`HEIRLOOM_COUNT`).",
         depends="`load_objects` copies the level's objects into "
                 "`OBJECTS`: nothing in the code changes.",
         expect=[("taken by walking",
                  "entry(r, 'walk right to the chalice')['heirlooms'] "
                  "== 1")]),
    dict(id="05b-short-night", step=5, kind="variant",
         title="A night of one minute",
         summary="A step of the night lasts 188 frames instead of 375: "
                 "the 16 steps of the bar go by in one minute.",
         edits=[("game/src/objects.asm",
                 "NIGHT_STEP    = 375             ; frames: 7.5 s, 2 "
                 "minutes",
                 "NIGHT_STEP    = 188             ; frames: 3.76 s, 1 "
                 "minute")],
         model=["numbers['NIGHT_STEP'] = 188"],
         route="variant_05b.py",
         where="`game/src/objects.asm`, `NIGHT_STEP`: the frames of "
               "one of the 16 steps of the bar of the night.",
         see="The bar of the night empties twice as fast; at dawn the "
             "level starts again, its heirlooms back in place.",
         limits="`NIGHT_STEP` is a 16-bit count (`night_time`); "
                "`NIGHT_STEPS` stays 16: the bar has 8 characters of 2 "
                "steps (a `.cerror` says so).",
         depends="In step 12 the steps left at the gate become points: "
                 "a shorter night gives fewer.",
         expect=[("dawn after 16 x 188 frames",
                  "entry(r, 'wait at the start')['frames'] == "
                  "3008")]),
    dict(id="05x-taken-again", step=5, kind="break",
         title="The same heirloom three times",
         summary="Taking an heirloom no longer sets its bit in "
                 "`got_bits`.",
         edits=[("game/src/objects.asm",
                 "        lda got_bits\n        ora heirloom_bit,x\n"
                 "        sta got_bits\n",
                 "        lda got_bits\n        sta got_bits\n")],
         fails="the level's variables equal the model", after=30,
         shot="taken-again.png",
         symptom="Oscar touches the chalice: it stays where it is, "
                 "and the HUD counts on past 3/3 (6/3 in the capture) "
                 "while he stands by it; at 3 the gate opened.",
         cause="`touch_heirlooms` skips an heirloom whose bit is set in "
               "`got_bits`. Without the `ora`, the bit is never set: "
               "in every frame that Oscar touches the chalice it is "
               "taken again, `got` goes on counting, and at 3 "
               "`open_gate` runs. The chalice is still drawn: for "
               "`place_heirloom` it has not been taken."),
    # --- step 06: the enemies ----------------------------------------
    dict(id="06a-watchman-at-the-start", step=6, kind="variant",
         title="A watchman at the start",
         summary="The first night watchman walks his round by the "
                 "start, columns 1 to 7, instead of beyond the "
                 "trapdoor: the enemies are data.",
         edits=[("game/assets/level1.py",
                 'ENEMIES = [("patrol", 32, 40, 36, "street", "left"),'
                 '      # A',
                 'ENEMIES = [("patrol", 1, 7, 5, "street", "left"),'
                 '        # A')],
         model=[],
         route="variant_06a.py",
         where="`game/assets/level1.py`, `ENEMIES`: for each enemy its "
               "kind, the first and last metatile column of its "
               "stretch, the column where it starts, what it stands on "
               "and where it faces.",
         see="As soon as the level starts the watchman walks towards "
             "Oscar: a touch, two notches of health, Oscar thrown back "
             "and blinking; the watchman turns at the end of his "
             "stretch and comes back.",
         limits="A patrol's stretch must be on its surface; at most "
                "`MAX_ENEMIES` (8) in a level, and four on the screen "
                "at once (sprites 3-6).",
         depends="`load_objects` copies the level's enemies; "
                 "`reset_enemies` puts each at its start.",
         expect=[("a hit while Oscar waits",
                  "entry(r, 'wait: the watchman')['events'].get('hit') "
                  "== 1"),
                 ("two notches of health",
                  "entry(r, 'wait: the watchman')['health'] == 6")]),
    dict(id="06b-hard-night", step=6, kind="variant",
         title="A hard night",
         summary="A touch takes four notches of health instead of two: "
                 "two touches, and Oscar is back at the lantern.",
         edits=[("game/src/enemies.asm",
                 "HIT_DAMAGE    = 2               ; a character of the "
                 "bar",
                 "HIT_DAMAGE    = 4               ; two characters of "
                 "the bar")],
         model=["numbers['HIT_DAMAGE'] = 4"],
         route="variant_06b.py",
         where="`game/src/enemies.asm`, `HIT_DAMAGE`: what `hurt` "
               "takes from `health` (8: the four characters of the "
               "bar, two notches each).",
         see="In the churchyard the cat jumps at Oscar: half of the "
             "bar goes at once.",
         limits="`HEALTH_FULL` (8) should be a multiple of it, or the "
                "last touch leaves a notch that only the next one "
                "takes.",
         depends="The brambles and the hazards of later steps hurt "
                 "with the same `hurt`.",
         expect=[("four notches at the first touch",
                  "entry(r, 'walk right until')['health'] == 4")]),
    dict(id="06x-pointers-of-one-screen", game="the enemies' pictures "
         "only in the pointers of screen A", step=6, kind="break",
         title="Enemies of one screen",
         summary="The enemies' sprite pointers are written in screen A "
                 "only.",
         after=2, shot="pointers-of-one-screen.png",
         symptom="Scrolling, the enemies vanish whenever screen B is "
                 "in front (in the capture, the watchman by the "
                 "trapdoor is missing), and come back with screen A.",
         cause="The sprite pointers are the last 8 bytes of the screen "
               "the VIC-II shows: with two screens, two sets. "
               "`place_enemy` must write both, as `place_oscar` does; "
               "in screen B the enemies' pointers keep whatever was "
               "there, here a block with nothing visible in it."),
    # --- step 07: the staff --------------------------------------------
    dict(id="07a-slower-blow", step=7, kind="variant",
         title="A slower blow",
         summary="The staff is raised for 7 frames instead of 3 before "
                 "it swings: a blow of 14 frames instead of 10.",
         edits=[("game/assets/staff.py",
                 "BLOW_FRAMES = 10\n"
                 'BLOW = {10: (8, 0, "raise"), 9: (8, 0, "raise"), '
                 '8: (8, 0, "raise"),',
                 "BLOW_FRAMES = 14\n"
                 'BLOW = {14: (8, 0, "raise"), 13: (8, 0, "raise"), '
                 '12: (8, 0, "raise"),\n'
                 '        11: (8, 0, "raise"), 10: (8, 0, "raise"), '
                 '9: (8, 0, "raise"),\n'
                 '        8: (8, 0, "raise"),')],
         model=[],
         route="variant_07a.py",
         where="`game/assets/staff.py`, `BLOW_FRAMES` and `BLOW`: the "
               "frames of a blow and, for each frame left, where the "
               "staff is and which of its pictures; `staff_tables` has "
               "an entry for each.",
         see="Fire, and the staff stays up longer before the swing; "
             "11 frames after Fire the blow is still going on, where a "
             "blow of 10 has ended.",
         limits="The frames that strike are counted from the end "
                "(`STRIKE_FIRST`, `STRIKE_LAST`: 7 to 4 left): the "
                "swing hits 4 frames later after Fire, and an enemy "
                "has 4 more frames to come close. Fire is not heard "
                "again until the blow ends.",
         depends="`BLOW_FRAMES` is a number of the data: the program "
                 "and the test's model read it from there, and the "
                 "staff's table from `staff_tables`.",
         expect=[("still in the blow 12 frames after Fire",
                  "entry(r, 'the blow, 11')['blow'] > 0")]),
    dict(id="07b-moon-on-the-left", step=7, kind="variant",
         title="The moon on the left",
         summary="The moon of the wood high on the left of the sky "
                 "instead of on the right.",
         edits=[("game/assets/moon.py",
                 "X_REGISTER = 296                    # screen pixels "
                 "272-293",
                 "X_REGISTER = 72                     # screen pixels "
                 "48-69")],
         model=[],
         route="variant_07b.py",
         where="`game/assets/moon.py`, `X_REGISTER`: the moon's X in "
               "the sprite registers (the screen's left edge is 24).",
         see="The moon on the left of the wood's sky, still while the "
             "level scrolls; X under 256 needs no ninth bit in $D010.",
         limits="The moon is a sprite behind the characters "
                "($D01B): trees and hills cover it wherever it is.",
         depends="Sprite 6 is the moon's only in the settings with a "
                 "moon; `place_enemies` leaves its bits alone.",
         expect=[("the moon at X 72",
                  "r['screenshots'][-1]['moon'][0] == 72")]),
    dict(id="07x-endless-puff", game="a struck enemy's puff never "
         "ends", step=7, kind="break",
         title="A puff that never ends",
         summary="The frames of a struck enemy's puff are never "
                 "counted down.",
         after=30, shot="endless-puff.png",
         symptom="A struck enemy turns into a puff of smoke, and stays "
                 "a puff: it never goes, and never comes back.",
         cause="`en_gone` counts the puff's frames down to the end, "
               "when the enemy is gone; without the `dec`, the count "
               "stays where it started."),
    # --- step 08: the packed levels ---------------------------------
    dict(id="08a-slower-wisps", step=8, kind="variant",
         title="Slower wisps",
         summary="The hazards that flicker take their next picture "
                 "every 8 frames instead of every 4.",
         edits=[("game/src/bat.asm",
                 "        lda turn_frame\n        and #%00000011\n"
                 "        cmp #2\n        bne _done\n"
                 "        lda turn_frame\n"
                 "        and #%00001100          ; picture * 4\n"
                 "        asl a                   ; * 64 bytes\n"
                 "        asl a\n        asl a\n        asl a\n",
                 "        lda turn_frame\n        and #%00000111\n"
                 "        cmp #2\n        bne _done\n"
                 "        lda turn_frame\n"
                 "        and #%00011000          ; picture * 8\n"
                 "        asl a                   ; * 64 bytes\n"
                 "        asl a\n        asl a\n")],
         model=["game_model.Game.flicker_shift = 3"],
         route="variant_08.py",
         where="`game/src/bat.asm`, `flicker_hazards`: the frames it "
               "acts on (bits 0-2 of the turn's frame, at 2) and the "
               "picture (bits 3-4, times 64 bytes: three shifts).",
         see="The will-o'-the-wisps of the mire drift twice as slowly.",
         limits="The mask and the shifts go together: with bits 3-4 "
                "for the picture, 3 shifts make 64 bytes. It must "
                "never act in the frame of the moths (bits 0-2 at 0).",
         depends="The test's model flickers at the same pace "
                 "(`flicker_shift`).",
         expect=[("the four pictures of the wisps",
                  "r['flicker_pictures'].get('2') == [0, 1, 2, 3]")]),
    dict(id="08b-still-wisps", step=8, kind="variant",
         title="Still wisps",
         summary="The mire left out of the settings that flicker: its "
                 "wisps keep their first picture.",
         edits=[("game/assets/build_assets.py",
                 'FLICKER = {"marsh": "wisps", "pass": "spikes", '
                 '"keep": "spikes",',
                 'FLICKER = {"pass": "spikes", "keep": "spikes",')],
         model=[],
         route="variant_08.py",
         where="`game/assets/build_assets.py`, `FLICKER`: the settings "
               "whose hazards flicker and the pictures they use; "
               "`env_flicker` gets a 0 for the others.",
         see="The wisps hang still over the pools; they hurt as "
             "before: a hazard is a flag of its metatile, not a "
             "picture.",
         limits="One page of pictures for each setting in the table.",
         depends="`flicker_hazards` reads `env_flicker` and does "
                 "nothing where it is 0.",
         expect=[("no picture of the mire's wisps changed",
                  "'2' not in r['flicker_pictures']")]),
    dict(id="08x-repeat-too-near", game="unpack: a repeat from one "
         "byte nearer", step=8, kind="break",
         title="A repeat from one byte nearer",
         summary="In `unpack`, a repeat copies from one byte nearer "
                 "than the stream says.",
         after=60, shot="repeat-too-near.png",
         symptom="From the very start the village is a jumble: pieces "
                 "of roofs and windows scattered over the sky, walls in "
                 "the wrong colours. From this step every level, the "
                 "first too, comes out of `unpack`.",
         cause="A repeat copies earlier output from D + 1 bytes back; "
               "`eor #$ff` and `clc` then `adc` make the low byte of "
               "- (D + 1). With `sec` the sum is one more: D bytes "
               "back, a byte too near, and every repeat copies the "
               "wrong bytes: the map, the setting's tables and its "
               "characters are all wrong."),
    # --- step 09: the castle -------------------------------------------
    dict(id="09a-purple-night", step=9, kind="variant",
         title="A purple night over the castle",
         summary="Dreadcastle Gate under a purple sky instead of a blue "
                 "one.",
         edits=[("game/assets/keep.py",
                 "SKY = BLUE                              # $d021 here"
                 ": the night",
                 "SKY = PURPLE                            # $d021 here"
                 ": the night")],
         model=[],
         route="variant_09.py",
         where="`game/assets/keep.py`, `SKY`: the colour of the "
               "keep's background, $D021 of its setting "
               "(`env_d021`).",
         see="The sky of level 7 purple; the HUD stays black, because "
             "its interrupt sets its own $D021 at line 226.",
         limits="$D021 is the background of every character: it must "
                "be a colour the pictures of the keep do not use as "
                "one of their own.",
         depends="The top interrupt writes `play_d021`, set from "
                 "`env_d021` when the level starts.",
         expect=[("the gate's sky purple",
                  "r['screenshots'][0]['d021'] == 4")]),
    dict(id="09b-brown-stone", step=9, kind="variant",
         title="A hall of brown stone",
         summary="The stone of the Throne Tower brown instead of grey.",
         edits=[("game/assets/hall.py",
                 "STONE = 12                              # $d022 here: "
                 "medium grey",
                 "STONE = 9                               # $d022 here: "
                 "brown")],
         model=[],
         route="variant_09.py",
         where="`game/assets/hall.py`, `STONE`: $D022 of the hall's "
               "setting, the first shared colour of its characters.",
         see="Every stone of level 8 brown: one register, all the "
             "characters that use it.",
         limits="A shared colour is shared: all the hall's pixels of "
                "that colour change together.",
         depends="`level.asm` writes $D022 from `env_d022` when the "
                 "setting changes.",
         expect=[("the captures of the castle as the reference",
                  "all(c['pass'] for c in r['checks'] "
                  "if 'equals the reference' in c['check'])")]),
    dict(id="09x-grey-dots", game="the HUD's background set without "
         "waiting for line 226", step=9, kind="break",
         fails="HUD interrupt on line 226", after=40,
         shot="grey-dots.png",
         title="Grey dots over the HUD",
         summary="The HUD's interrupt no longer waits for line 226 "
                 "before it changes the registers.",
         symptom="A row of grey dots along the last line of the "
                 "playfield, just above the HUD, in every level (in "
                 "the castle, where the sky is blue, as in the "
                 "village).",
         cause="The HUD's interrupt is set for line 225, the line "
               "before the HUD, to have time: it must wait there for "
               "line 226 (`cmp $d012`) before it writes $D021, $D016 "
               "and $D018. Without the wait the registers change while "
               "the beam is still drawing line 225, and the rest of "
               "that line is drawn with the HUD's characters."),
    # --- step 10: Tom Darkfang -------------------------------------
    dict(id="10a-four-blows", step=10, kind="variant",
         title="Four blows for Tom",
         summary="Tom is beaten after four blows of the staff instead "
                 "of eight.",
         edits=[("game/src/tom.asm",
                 "HITS_FULL      = 8               ; the staff's hits: "
                 "his bar",
                 "HITS_FULL      = 4               ; the staff's hits: "
                 "his bar")],
         model=["numbers['HITS_FULL'] = 4", "numbers['HITS_FAST'] = 2"],
         route="variant_10.py",
         where="`game/src/tom.asm`, `HITS_FULL`: the blows Tom takes; "
               "`HITS_FAST` (half of it) is when he gets faster.",
         see="A shorter fight: Tom gets faster after two blows and "
             "runs away after four.",
         limits="His bar in the HUD shows the hits left: with fewer, "
                "a shorter bar.",
         depends="The test's model counts the same hits "
                 "(`HITS_FULL`, `HITS_FAST`).",
         expect=[("beaten after four blows",
                  "entry(r, 'the fight until')['events']"
                  ".get('tom struck') == 4")]),
    dict(id="10b-higher-leaps", step=10, kind="variant",
         title="Higher leaps",
         summary="Tom leaps off the ground at 7 pixels a frame instead "
                 "of 6.",
         edits=[("game/src/tom.asm",
                 "LEAP_VY       = $0600           ; 6 pixels a frame up",
                 "LEAP_VY       = $0700           ; 7 pixels a frame "
                 "up")],
         model=["numbers['LEAP_VY'] = 0x0700"],
         route="variant_10.py",
         where="`game/src/tom.asm`, `LEAP_VY`: the speed up of his "
               "leap; `TOM_GRAVITY` brings him down.",
         see="Tom's leaps go higher and last longer: more time for "
             "Oscar to walk under him, and he lands further on.",
         limits="The arena's ceiling: from the floor, (7 x 7) / (2 x "
                "gravity) lines up must stay under the top of the "
                "playfield.",
         depends="The test's model leaps the same way; its fighter "
                 "(`tests/fight.py`) looks at the model, so it waits "
                 "for the longer leap.",
         expect=[("Tom beaten and gone",
                  "entry(r, 'Tom runs away')['events'].get('tom gone') "
                  "== 1")]),
    dict(id="10x-unmirrored", game="Tom facing left: his bytes not "
         "mirrored (no MIRROR) in page 0", step=10, kind="break",
         title="Tom not turned round",
         summary="Facing left, Tom's pictures are copied without the "
                 "table that turns them round.",
         after=10, shot="unmirrored.png",
         symptom="When Tom faces left his picture falls apart: each "
                 "column of pixels is in its place, but each byte "
                 "still faces right, so the outline is cut into "
                 "slivers.",
         cause="A sprite is turned round by reversing the order of "
               "its bytes in each row and the pixels in each byte. "
               "`MIRROR` reverses the pixels of a byte (in pairs, for "
               "multicolour); without it only the bytes change places."),
    # --- step 11: the music -------------------------------------------
    dict(id="11a-faster-theme", step=11, kind="variant",
         title="A faster theme",
         summary="Every step of the theme lasts 4 frames: 16 frames a "
                 "beat, about 188 beats a minute, instead of 19 (158).",
         edits=[("game/assets/music.py",
                 "TEMPO = [5, 5, 5, 4]                # the theme: "
                 "frames a step",
                 "TEMPO = [4, 4, 4, 4]                # the theme: "
                 "frames a step")],
         model=[],
         route="variant_11.py",
         where="`game/assets/music.py`, `TEMPO`: the frames of each "
               "step of the theme, in turn; `music.py` compiles them "
               "into the song's tempo table.",
         see="The same tune, faster; the player still plays one step "
             "of the song when its count runs out.",
         limits="Frames are the unit: 4 frames a step is 187.5 beats a "
                "minute, 5 is 150; the mix of 5, 5, 5, 4 gives 158.",
         depends="Tom's theme has its own `TEMPO` (in `boss.py`).",
         expect=[("the theme shorter in frames",
                  "r['music']['song_frames'] < 2400")]),
    dict(id="11b-plain-melody", step=11, kind="variant",
         title="A plain melody",
         summary="The lead instrument of the theme without its "
                 "vibrato.",
         edits=[("game/assets/score.py",
                 "                  sweep=0x18, vibrato=18),",
                 "                  sweep=0x18, vibrato=0),")],
         model=[],
         route="variant_11.py",
         where="`game/assets/score.py`, `INSTRUMENTS['lead']`: "
               "`vibrato` is the delay, in frames, before a long note "
               "starts to wobble; 0: never.",
         see="The long notes of the melody stay flat; the rest of the "
             "theme is the same.",
         limits="The vibrato's depth is a table of `player.asm` "
                "(`vibrato_table`), the same for every instrument.",
         depends="The player reads the instrument's bytes as the "
                 "compiled song gives them.",
         expect=[("the theme played",
                  "r['music']['frames_played']['theme'] > 1000")]),
    dict(id="11x-notes-held", game="music: the gate never let go before "
         "a note", step=11, kind="break",
         title="Notes that never let go",
         summary="Before a note the player no longer clears its gate "
                 "bit.",
         symptom="Heard, not seen: the notes of each voice run into "
                 "one another, without attack, a smear of sound.",
         cause="The SID starts a note's envelope when the gate bit "
               "goes from 0 to 1. Left at 1, the next note only "
               "changes the pitch: no new attack."),
    # --- step 12: the title and the ends --------------------------
    dict(id="12a-morning-words", step=12, kind="variant",
         title="Other words at dawn",
         summary="At dawn the band says MORNING HAS COME! instead of "
                 "THE SUN HAS RISEN!",
         edits=[("game/assets/title.py",
                 '"dawn": (2, 5, [(3, WHITE, "THE SUN HAS RISEN!"),',
                 '"dawn": (2, 5, [(3, WHITE, "MORNING HAS COME!"),')],
         model=[],
         route="variant_12a.py",
         where="`game/assets/title.py`, `BANDS`: each band's first "
               "row, its rows and its words (row, colour, text).",
         see="The band of dawn over the village with the new words.",
         limits="The letters of the HUD's font (`font.py`): no J, Q or "
                "X; 40 characters a row.",
         depends="`show_band` copies the band as it is.",
         expect=[("dawn reached",
                  "entry(r, 'dawn')['events'].get('dawn') == 1")]),
    dict(id="12b-night-worth-more", step=12, kind="variant",
         title="A night worth more",
         summary="A step of the night left counts 75 points instead "
                 "of 50.",
         edits=[("game/src/states.asm",
                 "NIGHT_POINTS  = $50             ; a step of the "
                 "night: 50",
                 "NIGHT_POINTS  = $75             ; a step of the "
                 "night: 75")],
         model=["game_model.Game.night_points = 75"],
         route="variant_12b.py",
         where="`game/src/states.asm`, `NIGHT_POINTS`: in BCD, two "
               "decimal digits in a byte ($75 is 75).",
         see="At the victory (and at every gate) each step of the "
             "night left adds 75 to the score.",
         limits="BCD: the decimal flag (`sed`) makes `adc` add decimal "
                "digits; `$7A` would not be a number.",
         depends="The test's model adds the same points "
                 "(`night_points`).",
         expect=[("the score a multiple of 75 more than Tom's 5000",
                  "(entry(r, 'the night into')['score'] - 5000) % 75 "
                  "== 0")]),
    dict(id="12x-band-a-row-down", game="the band's lines a row down: "
         "its words half drawn", step=12, kind="break", stop=False,
         title="The band a row down",
         summary="The band's raster line 8 lines lower than its rows.",
         shot="dreadcastle-clear.png",
         symptom="LEVEL CLEAR! half drawn: the top lines of its "
                 "letters are missing, so that L looks like C and E "
                 "like C.",
         cause="The band is drawn with characters of its own: an "
               "interrupt at `BAND_LINE` switches $D018 to them and "
               "another switches back. 8 lines lower, the top of the "
               "band's row is still drawn with the playfield's set, "
               "where those character codes are empty sky."),
    # --- step 13: the complete game -----------------------------------
    dict(id="13x-effect-held", game="an effect's end: the gate left on",
         step=13, kind="break",
         title="An effect that does not end",
         summary="At the end of a sound effect its gate bit is left "
                 "on.",
         symptom="Heard, not seen: after the first effect its last "
                 "sound hangs on in the voice until another note.",
         cause="A sound fades with its release only when the gate goes "
               "to 0: `and #%11111110` clears it in the copy of the "
               "control register; with `%11111111` nothing changes."),
]
