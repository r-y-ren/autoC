"""HIRE-STICKY tape mode: the opt-in repair for a refused HIRE.

A tape is an open-loop action replay.  `_do_hire` drops a HIRE the purse cannot
pay for in silence (`kaggriculture.py:702`), the roster is append-only inside a
day and wiped every night (`:880`), and an out-of-range hand order is a silent
per-unit no-op, not an illegal action (`:282`, `:907`).  So against a hire-heavy
file our leg replays a crew that is short of hands, does less work, earns less,
and can afford even fewer hires the next day.

`scripts/tape_opponent.py --hire-sticky` bakes in the reflex the recording had:
re-issue the owed HIRE on the following turns of the same day, never past the
roster the source reached, and address hand orders by SOURCE hand index.

What is asserted here:

* **off is off** -- a file cut with the flag plays the frozen tape's game at
  every step and every roster size, and `TAPE_HIRE_STICKY=0` wins over a baked
  `True`;
* the **owed hire is re-issued**, appended after the tape's own market orders,
  and stops the moment the roster matches the source's;
* it **never overshoots** the source roster, and is **dropped at the day
  boundary**;
* hand orders are **addressed by source index**, and a live hand with no source
  hand to impersonate PASSes instead of taking someone else's order.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import pytest

import tape_opponent as T

TPD = 4  # short days keep the fixtures readable; the engine's default is 24


def _frame(hands, market=(), farmer=("PASS",)):
    return {"farmer": list(farmer), "hands": [list(h) for h in hands],
            "market": [list(o) for o in market]}


def _tape():
    """Two 4-hour days.  Day 0: the source hires 2 at hour 0 and works them.
    Day 1: it hires 1 at hour 0 and 1 more at hour 1."""
    return [
        _frame([], market=[["HIRE"], ["HIRE"]]),                     # 0  d0h0
        _frame([["NORTH"], ["SOUTH"]]),                              # 1  d0h1
        _frame([["EAST"], ["WEST"]], market=[["SELL", "WHEAT", 3]]), # 2  d0h2
        _frame([["WATER"], ["HARVEST"]]),                            # 3  d0h3
        _frame([], market=[["HIRE"]]),                               # 4  d1h0
        _frame([["NORTH"]], market=[["HIRE"]]),                      # 5  d1h1
        _frame([["EAST"], ["PLANT", "WHEAT"]]),                      # 6  d1h2
        _frame([["WATER"], ["WATER"]]),                              # 7  d1h3
    ]


def _build(hire_sticky):
    return T.render_main(_tape(), episode=1, seat=0, team="tapee", opp_team="x",
                         final_money=1234, town=[[3, "BAKERY"]],
                         hire_sticky=hire_sticky)


def _load(main_py, on):
    return T.load_agent(main_py, hire_sticky=on)


def _obs(step, hands):
    return {"step": step, "player": 0,
            "farms": [{"hands": [[0, 0]] * hands}, {"hands": []}]}


CFG = {"turnsPerDay": TPD, "maxMarketOrdersPerTurn": 10}


@pytest.fixture
def on():
    ns = _load(_build(True), True)
    ns["_reset"]()
    return ns


def test_flag_off_is_the_frozen_tape():
    """The baked-on file, run with the flag off, is the frozen agent -- at every
    step and every roster size, which is the whole surface it has."""
    assert T.verify_frozen_match(_build(True), _build(False)) == 0
    assert T.verify_frozen_match(_build(False), _build(False)) == 0


def test_env_beats_the_baked_default():
    ns = _load(_build(True), False)
    # frozen: a 3-hand roster at step 1 gets the tape's 2 orders plus a PASS
    assert ns["agent"](_obs(1, 3), CFG)["hands"] == [["NORTH"], ["SOUTH"], ["PASS"]]
    ns = _load(_build(False), True)
    ns["_reset"]()
    assert ns["_hire_sticky_on"]() is True


def test_source_roster_is_recovered_from_the_tape(on):
    assert on["_SRC_HANDS"] == [0, 2, 2, 2, 0, 1, 2, 2]


def test_owed_hire_is_reissued_after_the_tape_orders(on):
    """One of the two day-0 hires is refused: the next turn re-issues exactly
    one HIRE, appended behind the tape's own market orders."""
    a0 = on["agent"](_obs(0, 0), CFG)
    assert a0["market"] == [["HIRE"], ["HIRE"]]          # the tape's own, untouched
    a1 = on["agent"](_obs(1, 1), CFG)                    # only one landed
    assert a1["market"] == [["HIRE"]]                    # one owed, re-issued
    assert on["_STATE"]["map"] == [0] and on["_STATE"]["owed"] == [1]
    a2 = on["agent"](_obs(2, 2), CFG)                    # it landed
    assert a2["market"] == [["SELL", "WHEAT", 3]]        # nothing owed -> nothing added
    assert on["_STATE"]["map"] == [0, 1] and on["_STATE"]["owed"] == []


def test_reissue_is_appended_not_prepended(on):
    """Order matters: the re-issue goes behind this turn's SELLs, which are the
    cash that pays for it, and the engine walks the queue index by index."""
    on["agent"](_obs(0, 0), CFG)
    on["agent"](_obs(1, 1), CFG)
    assert on["agent"](_obs(2, 1), CFG)["market"] == [["SELL", "WHEAT", 3], ["HIRE"]]


def test_never_overshoots_the_source_roster(on):
    """Nothing is owed when the roster already matches, and the cap is the
    source's roster at the END of this step, not some larger number."""
    on["agent"](_obs(0, 0), CFG)
    assert on["agent"](_obs(1, 2), CFG)["market"] == []
    assert on["_STATE"]["owed"] == []
    # day 1 hour 1: source goes 1 -> 2 hands, we already have 2 -> no room
    on["_reset"]()
    on["agent"](_obs(4, 0), CFG)
    on["agent"](_obs(5, 2), CFG)
    assert on["_STATE"]["owed"] == []


def test_owed_hire_dies_at_the_day_boundary(on):
    """`_end_of_day` empties `hands`, so a hire deferred past midnight is a
    different hire and must not be carried."""
    on["agent"](_obs(0, 0), CFG)
    on["agent"](_obs(1, 0), CFG)                  # both refused
    assert on["_STATE"]["owed"] == [0, 1]
    a4 = on["agent"](_obs(4, 0), CFG)             # day 1 hour 0
    assert on["_STATE"]["owed"] == [] and on["_STATE"]["map"] == []
    assert a4["market"] == [["HIRE"]]             # only the tape's own


def test_hands_are_addressed_by_source_index(on):
    """The live hand impersonates the source hand it was hired to replace, and
    the frame's own orders are read at that index."""
    on["agent"](_obs(0, 0), CFG)
    on["agent"](_obs(1, 1), CFG)                  # live 0 -> source 0, source 1 owed
    a = on["agent"](_obs(2, 2), CFG)              # the owed hire landed
    assert a["hands"] == [["EAST"], ["WEST"]]     # source 0, source 1 -- in order
    assert on["_STATE"]["map"] == [0, 1]


def test_unresolvable_hand_passes_and_the_turn_survives(on):
    """A live hand the source never had has no order to replay: it PASSes, and
    the farmer and market halves of the turn are untouched."""
    on["agent"](_obs(0, 0), CFG)
    a = on["agent"](_obs(1, 3), CFG)              # 3 hands, the source had 2
    assert a["hands"] == [["NORTH"], ["SOUTH"], ["PASS"]]
    assert on["_STATE"]["map"] == [0, 1, -1]
    a = on["agent"](_obs(2, 3), CFG)
    assert a["hands"] == [["EAST"], ["WEST"], ["PASS"]]
    assert a["farmer"] == ["PASS"] and a["market"] == [["SELL", "WHEAT", 3]]


def test_new_episode_resets_the_state(on):
    on["agent"](_obs(0, 0), CFG)
    on["agent"](_obs(1, 0), CFG)
    assert on["_STATE"]["owed"] == [0, 1]
    on["agent"](_obs(0, 0), CFG)                  # a step that does not follow -> new game
    assert on["_STATE"]["owed"] == [] and on["_STATE"]["map"] == []


def test_past_the_end_of_the_tape_passes(on):
    a = on["agent"](_obs(len(_tape()) + 3, 2), CFG)
    assert a == {"farmer": ["PASS"], "hands": [["PASS"], ["PASS"]], "market": []}
