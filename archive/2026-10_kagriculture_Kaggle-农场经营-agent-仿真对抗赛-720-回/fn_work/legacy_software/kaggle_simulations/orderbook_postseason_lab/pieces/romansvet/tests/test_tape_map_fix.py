"""MAP-REMAP repair in the engine-side tape seat (scripts/tape_opponent.py).

HIRE-STICKY mode addresses hand orders through `_MAP`, a live-hand -> source-hand
assignment that was PERSISTENT for the whole day: a live hand that existed before
the source had a hand for it (the seat landed more of the tape's own recorded
HIREs in a turn than the source did) was pinned to -1 and PASSed for the rest of
the day, while every later source hand went to a NEWER live slot -- so source
order k was executed by live hand k+1 from then on.  Measured on the three DSM
TOPB3 boards 2026-09-14: 1 pin/game, 23 PASS turns, 37 misaddressed acting orders
(docs/strategy/2026-09-14-tape-map.md).

`TAPE_MAP_FIX=1` (or `--hire-sticky-remap`) re-derives the map every turn: a
pinned slot claims the next unassigned source hand, which collapses `_MAP` back
to the identity the frozen tape uses, while keeping the deferred-hire re-issue.
"""
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import tape_opponent as TO  # noqa: E402

R = Path(__file__).resolve().parents[1]
BOARD = "108741964"          # one of the three boards the pin was measured on
NEW = R / "S/topb3/tapemap/tapes" / f"opponent_tape_{BOARD}/main.py"
OLD = R / "S/topb3/hirefix/tapes" / f"opponent_tape_{BOARD}/main.py"


def _load(main_py, sticky, mapfix):
    """Exec the emitted file the way kaggle_environments does, flags pinned."""
    os.environ["TAPE_HIRE_STICKY"] = "1" if sticky else "0"
    os.environ["TAPE_MAP_FIX"] = "1" if mapfix else "0"
    os.environ.pop("TAPE_MAP_DEBUG", None)
    ns = {}
    exec(compile(main_py, "<tape>", "exec"), ns)  # noqa: S102
    return ns


def _obs(step, hands, seat=0):
    farms = [{"hands": []}, {"hands": []}]
    farms[seat] = {"hands": [[0, 0]] * hands}
    return {"step": step, "player": seat, "farms": farms}


@pytest.mark.skipif(not (NEW.exists() and OLD.exists()), reason="tape packages not cut")
def test_map_fix_off_is_the_existing_hire_sticky_agent():
    """Default-off equivalence: the re-cut package with the repair OFF plays the
    package that predates the repair, move for move, over a roster sequence that
    forces pins (live grows one ahead of the source and stays there)."""
    new = _load(NEW.read_text(), sticky=True, mapfix=False)
    old = _load(OLD.read_text(), sticky=True, mapfix=False)
    cfg = {"turnsPerDay": 24, "maxMarketOrdersPerTurn": 10}
    diff = 0
    for step in range(0, 24 * 12):
        hands = 0 if step % 24 == 0 else min(14, 1 + (step % 24) // 2)
        obs = _obs(step, hands)
        if new["agent"](obs, cfg) != old["agent"](obs, cfg):
            diff += 1
    assert diff == 0


@pytest.mark.skipif(not NEW.exists(), reason="tape packages not cut")
def test_frozen_path_untouched_by_the_new_switch():
    """Both flags off -> the byte-frozen tape, at every (step, roster) pair."""
    os.environ["TAPE_MAP_FIX"] = "1"          # must be inert while sticky is off
    bad = TO.verify_frozen_match(
        NEW.read_text(),
        (R / "artifacts/panel_opp_town" / f"opponent_tape_{BOARD}/main.py").read_text())
    assert bad == 0


SYNTH = [
    # step 0 = day 0 hour 0 (roster wiped), then a day where the SOURCE roster
    # goes 0 -> 2 -> 3 -> 4 while the live seat lands 3 hires in the first turn.
    {"farmer": ["PASS"], "hands": [], "market": []},                       # s0  src 0
    {"farmer": ["PASS"], "hands": [["A0"], ["A1"]], "market": []},         # s1  src 2
    {"farmer": ["PASS"], "hands": [["B0"], ["B1"], ["B2"]], "market": []},  # s2  src 3
    {"farmer": ["PASS"], "hands": [["C0"], ["C1"], ["C2"], ["C3"]],
     "market": []},                                                        # s3  src 4
    {"farmer": ["PASS"], "hands": [["D0"], ["D1"], ["D2"], ["D3"]],
     "market": []},                                                        # s4  src 4
]


def _synth_agent(mapfix):
    main_py = TO.render_main(SYNTH, episode=1, seat=0, team="T", opp_team="O",
                             final_money=1, town=[], hire_sticky=True)
    return _load(main_py, sticky=True, mapfix=mapfix)["agent"]


@pytest.mark.parametrize("mapfix,want", [
    # live roster 0,3,3,4,4 against a source roster 0,2,3,4,4.
    # OFF: the surplus live hand 2 is pinned at s1 and stays pinned, so source
    # hand 2 lands on live hand 3 and source hand 3 is never reached.
    (False, [["B0"], ["B1"], ["PASS"]]),
    # ON: at s2 the pinned slot claims source hand 2 -> the map is the identity
    # again and the frozen tape's own addressing is restored.
    (True, [["B0"], ["B1"], ["B2"]]),
])
def test_remap_on_a_synthetic_roster_sequence(mapfix, want):
    agent = _synth_agent(mapfix)
    cfg = {"turnsPerDay": 24, "maxMarketOrdersPerTurn": 10}
    agent(_obs(0, 0), cfg)                    # day boundary: roster wiped
    agent(_obs(1, 3), cfg)                    # 3 hires land, source had 2
    got = agent(_obs(2, 3), cfg)              # source roster is now 3
    assert got["hands"] == want


def test_remap_keeps_the_surplus_hand_at_the_tail():
    """With the repair on, the pin migrates to the NEWEST live hand, so the
    hand that idles is the one the frozen tape would also have idled."""
    agent = _synth_agent(True)
    cfg = {"turnsPerDay": 24, "maxMarketOrdersPerTurn": 10}
    agent(_obs(0, 0), cfg)
    agent(_obs(1, 3), cfg)
    agent(_obs(2, 3), cfg)
    got = agent(_obs(3, 4), cfg)              # source roster 4, live 4
    assert got["hands"] == [["C0"], ["C1"], ["C2"], ["C3"]]


def test_repair_is_inert_when_the_seat_never_out_hires():
    """A live roster that only ever lags the source is unchanged by the repair:
    the map has no -1 to re-derive."""
    cfg = {"turnsPerDay": 24, "maxMarketOrdersPerTurn": 10}
    off, on = _synth_agent(False), _synth_agent(True)
    for step, hands in ((0, 0), (1, 1), (2, 2), (3, 3), (4, 4)):
        a, b = off(_obs(step, hands), cfg), on(_obs(step, hands), cfg)
        assert a == b, step
