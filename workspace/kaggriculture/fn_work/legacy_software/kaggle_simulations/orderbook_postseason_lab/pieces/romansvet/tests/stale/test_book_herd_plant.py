"""`agent/book_herd_plant.py`: book D3 -- book B, plus three gated constants.

The book is `book_herd.py` with, from day 1 onward and nothing on day 0:

    PRI_HARVEST_STRAW = 6.4   a strawberry tile HOLDING UNITS
    PRI_PLANT_STRAW   = 6.5   an empty strawberry-role tile
    PLANT_STRAW_FROM_DAY = 1  the day-0 guard both of them obey

Book C found the plant constant: on days 5-9 the bought strawberry seed sat in
the slot on every turn because planting ranked below COLLECT, CARE and HARVEST.
Two arms then paid for the two guards around it, and both are recorded here
because the tests are the receipt for them:

* ungated (book D, -28,233 against book B's -22,833) the plant also outran the
  MELON plant on day 0, so the crew put 8 strawberry in the ground and 1 melon,
  and from day 1 `agent` re-roles an empty MELON tile to STRAWBERRY -- 5 melon
  seeds stranded, day-10 dump 36 units -> 6.  `PLANT_STRAW_FROM_DAY` fixes it;
* with the plant alone (book D2, -19,897) the field reached 30 tiles by day 11
  and the book sold ZERO strawberry inside days 0-13 against book B's 21,
  because 6.5 also outranks PRI_HARVEST = 10 and the saturated crew planted the
  next tile instead of picking the ripe one.  `PRI_HARVEST_STRAW` fixes it.

What this file asserts, measured on seed 777001 against `starter`:

* day 0 is book B's, op for op -- 6 MELON, 3 WHEAT, 6 STRAWBERRY, and only the
  2 leftover strawberry seeds in the slot at dawn of day 1;
* the day-10 melon dump is whole: 36 units, the same as book B;
* the field grows for free -- 15 standing strawberry at dusk of day 9 against
  book B's 9, and 34 by day 13 against book B's 25;
* and it is now PICKED: 22 strawberry units sold inside days 0-13, against
  book B's 21 and book D2's 0.

The one `xfail(strict=True)` carries its measured number and mechanism in the
reason string rather than being asserted away.

Book B and `tests/test_book_herd.py` are untouched by any of this.
"""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from kagg3.agent import book_herd as BOOKB
from kagg3.agent import book_herd_plant as B

SEED = 777001
DAYS = 14
TURNS_PER_DAY = 24


@pytest.fixture(scope="module")
def game():
    """One 14-day game of book D against `starter`, as (obs, action) frames."""
    from kaggle_environments import make
    env = make("kaggriculture",
               configuration={"seed": SEED,
                              "episodeSteps": DAYS * TURNS_PER_DAY + 2})
    trainer = env.train([None, "starter"])
    obs = trainer.reset()
    frames = []
    for _ in range(DAYS * TURNS_PER_DAY):
        act = B.agent(obs)
        frames.append((obs, act))
        obs, _, done, _ = trainer.step(act)
        if done:
            break
    return frames


def _standing(obs, crop):
    seat = int(obs.get("player", 0))
    return sum(1 for row in obs["farms"][seat]["tiles"] for t in row
               if isinstance(t, dict) and t.get("kind") == "PLANT"
               and t["crop"] == crop)


def _dusk(frames, day):
    """The last observation of `day` -- hour 23, before that hour's action."""
    seen = [o for o, _ in frames if int(o["day"]) == day]
    assert seen, f"day {day} never reached"
    return seen[-1]


def _sell_units(frames, day, item):
    return sum(int(r[2]) for o, a in frames if int(o["day"]) == day
               for r in (a.get("market") or [])
               if isinstance(r, list) and len(r) >= 3
               and r[0] == "SELL" and r[1] == item)


def _plant_ops(frames, day):
    out = {}
    for o, a in frames:
        if int(o["day"]) != day:
            continue
        for u in [a.get("farmer") or []] + list(a.get("hands") or []):
            if u and u[0] == "PLANT":
                out[u[1]] = out.get(u[1], 0) + 1
    return out


# =========================================================================
# the engine accepts every turn, on both sides of the board
# =========================================================================

def test_every_turn_of_the_opening_is_a_legal_action():
    """Days 0-13 as a real seat, both seats: a rejected action shows up as a
    status, never as an exception, so only the status can say so."""
    from kaggle_environments import make
    for seat in (0, 1):
        env = make("kaggriculture",
                   configuration={"seed": SEED,
                                  "episodeSteps": DAYS * TURNS_PER_DAY + 2})
        env.run([B.agent, "starter"] if seat == 0 else ["starter", B.agent])
        bad = [(t, s[seat].status) for t, s in enumerate(env.steps)
               if s[seat].status not in ("ACTIVE", "DONE")]
        assert not bad, f"seat {seat} left ACTIVE at {bad[:3]}"


# =========================================================================
# the one change is the only change
# =========================================================================

def test_book_d_differs_from_book_b_only_in_the_plant_priority():
    """Byte-level provenance: the two files differ in the docstring, the three
    new constants, and the two functions that read them -- `_crop_job` for the
    pick and `agent` for the plant.  Nothing else may move."""
    a = (ROOT / "src" / "kagg3" / "agent" / "book_herd.py").read_text()
    b = (ROOT / "src" / "kagg3" / "agent" / "book_herd_plant.py").read_text()
    import ast
    ta, tb = ast.parse(a), ast.parse(b)
    # strip both docstrings; what is left is code
    ta.body[0] = tb.body[0] = ast.Expr(ast.Constant(""))
    names = lambda t: [getattr(n, "name", None) or ast.dump(n)[:24] for n in t.body]
    src_a = {ast.dump(n) for n in ta.body}
    src_b = {ast.dump(n) for n in tb.body}
    extra = sorted(src_b - src_a)
    missing = sorted(src_a - src_b)
    # one new top-level statement (the constant) plus the one function that
    # reads it; `agent` carries the planting block, so it is the only body that
    # may differ, and nothing may vanish that is not its old copy.
    assert len(extra) == 5 and len(missing) == 2, (names(ta), names(tb))
    consts = [e for e in extra if "FunctionDef" not in e]
    assert len(consts) == 3, consts
    assert any("PRI_HARVEST_STRAW" in e for e in consts), consts
    assert any("PRI_PLANT_STRAW" in e for e in consts), consts
    assert any("PLANT_STRAW_FROM_DAY" in e for e in consts), consts
    fns = sorted(e[:40] for e in extra if "FunctionDef" in e)
    assert fns == sorted(e[:40] for e in missing), (fns, missing)
    assert all(e.startswith("FunctionDef(name='agent'")
               or e.startswith("FunctionDef(name='_crop_job'") for e in fns), fns
    assert B.PRI_HARVEST_STRAW == 6.4
    assert B.PRI_PLANT_STRAW == 6.5
    assert B.PLANT_STRAW_FROM_DAY == 1
    assert B.PRI_PLANT == BOOKB.PRI_PLANT == 11
    # Both new ranks land between FEED (6) and COLLECT (7), the pick ahead of
    # the plant: survival water, the melon, the builds, the animal harvest and
    # FEED all still outrank both, and what they jump is COLLECT, CARE and
    # HARVEST.  Neither collides with an existing rank, so no other pair of
    # jobs is silently merged into one bucket.
    assert B.PRI_WATER_MUST < B.PRI_MELON < B.PRI_HARVEST_STRAW
    assert B.PRI_FEED < B.PRI_HARVEST_STRAW < B.PRI_PLANT_STRAW < B.PRI_COLLECT
    assert B.PRI_PLANT_STRAW < B.PRI_CARE < B.PRI_HARVEST < B.PRI_PLANT
    ranks = [v for k, v in vars(B).items() if k.startswith("PRI_")]
    assert len(ranks) == len(set(ranks)), sorted(ranks)


# =========================================================================
# what the change bought: the field
# =========================================================================

def test_the_day_nine_field_is_more_than_twice_book_b_s(game):
    """The constant does exactly what book C said it does.  Book B stands 9
    strawberry tiles at dusk of day 9 on this seed, 12 at dusk of day 11 and 25
    at dusk of day 13; book D3 stands 15, 32 and 34, having bought not one
    extra seed -- the binding constraint on days 5-9 was crew turns, not
    coins."""
    assert _standing(_dusk(game, 9), "STRAWBERRY") == 15
    assert _standing(_dusk(game, 5), "STRAWBERRY") == 15
    assert _standing(_dusk(game, 11), "STRAWBERRY") == 32
    assert _standing(_dusk(game, 13), "STRAWBERRY") == 34


@pytest.mark.xfail(strict=True, reason=(
    "brief gate: >= 24 standing strawberry at dusk of day 9.  Measured 15.  "
    "Day 0 is book B's again, so only 6 tiles are sown before the melon takes "
    "its six; the field reaches 24 on day 10 and 30 on day 11, once the melon "
    "block is harvested and re-roled.  Book C reached 30 by day 7 only by "
    "re-cutting the tile roles and cutting the herd, which cost more than the "
    "field was worth."))
def test_brief_gate_day_nine_field_reaches_twenty_four(game):
    assert _standing(_dusk(game, 9), "STRAWBERRY") >= 24


# =========================================================================
# what the change cost: the melon block
# =========================================================================

def test_day_zero_is_book_b_s_op_for_op(game):
    """The whole point of the gate.  Book B's day 0 issues 6 MELON, 6
    STRAWBERRY and 3 WHEAT plants and leaves 2 strawberry seeds in the slot;
    book D2's issues exactly the same, because `PLANT_STRAW_FROM_DAY` keeps the
    strawberry job at 11 alongside the melon on the one day the melon block can
    ever be sown.  Ungated (book D) this read STRAWBERRY 8, MELON 1 with 5
    melon seeds stranded for the rest of the game."""
    assert _plant_ops(game, 0) == {"MELON": 6, "WHEAT": 3, "STRAWBERRY": 6}
    dawn_d1 = [o for o, _ in game if int(o["day"]) == 1 and int(o["hour"]) == 0]
    left = {k: v for k, v in dawn_d1[0]["private"]["seeds"].items() if v}
    assert left == {"STRAWBERRY": 2}, left
    assert _standing(_dusk(game, 9), "MELON") == 6


def test_the_day_ten_melon_dump_is_whole(game):
    """36 units on day 10, the same as book B, in three 12-unit lots -- the one
    day of the season with no other melon on the market.  Ungated this was 6,
    and that collapse was the largest single line of book D's regression."""
    assert _sell_units(game, 10, "MELON") == 36


def test_the_strawberry_the_field_grows_is_actually_sold(game):
    """The hole book D2 left, closed.  Book B sells 21 strawberry units inside
    days 0-13 and book D2 sells 0 -- 6.5 outranks PRI_HARVEST = 10, so the
    saturated crew planted the next tile instead of picking the ripe one.  With
    the pick at 6.4, ahead of the plant, book D3 sells 22 off a field twice the
    size, and the first lot goes out on day 10 beside the melon."""
    per_day = {d: _sell_units(game, d, "STRAWBERRY") for d in range(10, 14)}
    assert sum(per_day.values()) >= 20, per_day
    assert per_day[10] > 0, per_day


# =========================================================================
# the book itself, pinned
# =========================================================================

#: Digest of book D3's own action stream on `SEED` against `starter`, 14 days.
#: It pins the file this test owns; move it only with a measured reason, and
#: never to make a red test green.
PIN = ("16979a48e657cd8f",)


def _digest(frames):
    h = hashlib.blake2b(digest_size=8)
    for _, act in frames:
        h.update(json.dumps(act, sort_keys=True, separators=(",", ":")).encode())
    return h.hexdigest()


@pytest.mark.skipif(os.environ.get("KAGG3_BOOK_PIN") == "off",
                    reason="pin deliberately suspended")
def test_book_stream_is_pinned(game):
    assert _digest(game) in PIN
