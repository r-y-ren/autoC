"""PURSE repair in the engine-side tape seat (scripts/tape_opponent.py).

HIRE-STICKY re-issues an owed HIRE on the following turns of the same day, but
its room cap reads `_src_hands(step + 1)`, which at the day's LAST hour is
already the next day's empty roster -- so hour 23 is blacked out and an owed
hire never gets its final try.  `TAPE_PURSE_FIX=1` (or `--hire-sticky-purse`)
caps that one hour at the source's roster at THIS hour instead.  It is
deliberately NOT carried across midnight: the engine wipes `hands` and
`hires_today` every night (kaggriculture.py:880-882), so a hire deferred past
midnight is a different hire, and carrying a debt would let the tape out-hire
the seat it is impersonating.

Measured 2026-09-14 (docs/strategy/2026-09-14-tape-purse.md): a no-op on all 18
TOPB3 boards, where hire-sticky already lands 286/286 of the source's season
hires -- which is the evidence that the residual Majkel1337 divergence is not
hire-side cash.
"""
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import tape_opponent as TO  # noqa: E402

R = Path(__file__).resolve().parents[1]
BOARD = "108795516"          # the worst Majkel1337 board, retention 0.27
NEW = R / "S/topb3/tapepurse/tapes" / f"opponent_tape_{BOARD}/main.py"
OLD = R / "S/topb3/tapemap/tapes" / f"opponent_tape_{BOARD}/main.py"
FROZEN = R / "artifacts/panel_opp_town" / f"opponent_tape_{BOARD}/main.py"

CFG = {"turnsPerDay": 24, "maxMarketOrdersPerTurn": 10}


def _load(main_py, sticky, mapfix, pursefix):
    """Exec the emitted file the way kaggle_environments does, flags pinned."""
    os.environ["TAPE_HIRE_STICKY"] = "1" if sticky else "0"
    os.environ["TAPE_MAP_FIX"] = "1" if mapfix else "0"
    os.environ["TAPE_PURSE_FIX"] = "1" if pursefix else "0"
    os.environ.pop("TAPE_MAP_DEBUG", None)
    os.environ.pop("TAPE_PURSE_DEBUG", None)
    ns = {}
    exec(compile(main_py, "<tape>", "exec"), ns)  # noqa: S102
    return ns


def _obs(step, hands, seat=0, money=3000.0, hires_today=0):
    farms = [{"hands": [], "money": money, "hires_today": 0},
             {"hands": [], "money": money, "hires_today": 0}]
    farms[seat] = {"hands": [[0, 0]] * hands, "money": money,
                   "hires_today": hires_today}
    return {"step": step, "player": seat, "farms": farms}


@pytest.mark.skipif(not (NEW.exists() and OLD.exists()), reason="tape packages not cut")
@pytest.mark.parametrize("mapfix", [False, True])
def test_purse_fix_off_is_the_existing_agent(mapfix):
    """Default-off equivalence on one board: the purse-capable package with the
    repair OFF plays the package that predates it, move for move, over a roster
    sequence that keeps a hire owed through the day's LAST hour."""
    new = _load(NEW.read_text(), sticky=True, mapfix=mapfix, pursefix=False)
    old = _load(OLD.read_text(), sticky=True, mapfix=mapfix, pursefix=False)
    diff = 0
    for step in range(0, 24 * 12):
        hour = step % 24
        # lags the source all day (a hire stays owed), and out-hires it at h5.
        hands = 0 if hour == 0 else (9 if hour == 5 else max(1, hour // 3))
        obs = _obs(step, hands, money=4.0 if hour > 12 else 3000.0)
        if new["agent"](obs, CFG) != old["agent"](obs, CFG):
            diff += 1
    assert diff == 0


@pytest.mark.skipif(not (NEW.exists() and FROZEN.exists()), reason="tape packages not cut")
def test_frozen_path_untouched_by_the_new_switch():
    """Both repairs forced on -> still inert while hire-sticky is off, at every
    (step, roster) pair the frozen package can be asked about."""
    os.environ["TAPE_PURSE_FIX"] = "1"
    os.environ["TAPE_MAP_FIX"] = "1"
    assert TO.verify_frozen_match(NEW.read_text(), FROZEN.read_text()) == 0


# A synthetic purse sequence: day 0 hour 0 wipes the roster, the SOURCE lands 2
# hands at hour 1 and holds them all day, the live seat can only afford 1 (the
# engine drops the second for cash, kaggriculture.py:702-705), so exactly one
# hire stays owed from hour 1 to hour 23.  Day 1 repeats it.
_SRC2 = [["H0"], ["H1"]]
SYNTH = ([{"farmer": ["PASS"], "hands": [], "market": []}]
         + [{"farmer": ["PASS"], "hands": _SRC2, "market": []} for _ in range(23)]
         + [{"farmer": ["PASS"], "hands": [], "market": []}]
         + [{"farmer": ["PASS"], "hands": _SRC2, "market": []} for _ in range(23)])


def _synth_agent(pursefix):
    main_py = TO.render_main(SYNTH, episode=1, seat=0, team="T", opp_team="O",
                             final_money=1, town=[], hire_sticky=True)
    return _load(main_py, sticky=True, mapfix=True, pursefix=pursefix)["agent"]


def _run_day(agent, upto, live=1):
    """Hour 0 wipes the roster; hours 1..upto the seat holds `live` hands."""
    out = []
    for step in range(0, upto + 1):
        out.append(agent(_obs(step, 0 if step % 24 == 0 else live,
                              money=4.0, hires_today=1), CFG))
    return out


@pytest.mark.parametrize("pursefix,want", [
    # hour 23: OFF blacks the re-issue out (`_src_hands(step + 1)` is the next
    # day's empty roster); ON caps it at the source's roster at THIS hour.
    (False, []),
    (True, [["HIRE"]]),
])
def test_last_hour_of_the_day_reissues_only_with_the_repair(pursefix, want):
    rows = _run_day(_synth_agent(pursefix), 23)
    assert rows[23]["market"] == want


@pytest.mark.parametrize("pursefix", [False, True])
def test_hours_1_to_22_are_identical(pursefix):
    """The repair touches ONE hour: every earlier hour already re-issues."""
    rows = _run_day(_synth_agent(pursefix), 22)
    assert [r["market"] for r in rows[1:23]] == [[["HIRE"]]] * 22


def test_owed_is_not_carried_across_midnight():
    """The roster is wiped nightly, so the hire owed at 23:00 is NOT re-issued
    at 00:00 the next day -- the tape must never out-hire the seat it plays."""
    agent = _synth_agent(True)
    rows = _run_day(agent, 23)
    assert rows[23]["market"] == [["HIRE"]]
    assert agent(_obs(24, 0, money=4.0), CFG)["market"] == []
    # and the new day's owed is recomputed from the SOURCE's own roster
    assert agent(_obs(25, 1, money=4.0), CFG)["market"] == [["HIRE"]]


def test_repair_never_hires_past_the_source_roster():
    """Caught up at hour 23 -> nothing owed, nothing issued, with the repair on."""
    agent = _synth_agent(True)
    for step in range(0, 24):
        got = agent(_obs(step, 0 if step % 24 == 0 else 2, money=4.0), CFG)
    assert got["market"] == []
