"""`agent/book_open16.py`: kagg3's own opening, checked against the real engine.

The book is not a tape, so there is nothing to diff against a recording. What
has to hold is the four things the opening is built out of, and one thing it
must never touch:

* every turn of days 0-15 is an action the engine accepts -- a status other
  than ACTIVE anywhere in the sixteen days is the whole switch failing, and
  the engine's own silent-no-op policy means only the status says so;
* the day-0 row is the fixed line: twelve melon and seven wheat, never zero
  wheat;
* day 10 puts the melon out in small lots, the first of them well in front of
  the hour-17 dump every 2800-tier seat makes, out of a shed that already
  holds the crop -- a SELL against an empty shed sells nothing;
* no turn asks to plant more of a crop than the seed slot holds, because the
  engine drops *every* PLANT of a crop when one turn over-asks;
* and with `KAGG3_OPENING` unset the factory hands back the bare planner, so
  the switch is free when it is off.

`PIN` follows `test_melon_open.py`'s pattern, but it digests *this file's*
agent rather than the planner: the book is the only thing this test owns, and
pinning the planner here would fail every time the planner legitimately moves.
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
sys.path.insert(0, str(ROOT / "scripts"))

import numpy as np

from kagg3.agent import book_open16 as B
from kagg3.agent import opening, runtime

SEED = 777001
DAYS = 16
TURNS_PER_DAY = 24

#: The engine's whole unit vocabulary and market vocabulary, read off
#: `kaggriculture.json`'s action description.
UNIT_OPS = {"NORTH", "SOUTH", "EAST", "WEST", "PASS", "PICKUP", "PLANT",
            "WATER", "HARVEST", "FERTILIZE", "BUILD_COOP", "BUILD_PASTURE",
            "FEED", "COLLECT_FERTILIZER", "CARE", "DIG", "PLACE", "DROP"}
MARKET_OPS = {"BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL", "SELL", "HIRE",
              "BUY_LAND"}
MAX_ORDERS = 10
#: `MELON_LOT_TURNS`' own ceiling: the recorded opening walks the squared glut
#: curve in lots of at most this many rather than jumping it in one line.
MAX_MELON_LOT = 24
#: The hour every 2800-tier seat's own melon dump lands on.
OPPONENT_DUMP_HOUR = 17


@pytest.fixture(scope="module")
def game():
    """One full 16-day game of the book against `starter`, as (obs, action)."""
    from kaggle_environments import make
    env = make("kaggriculture",
               configuration={"seed": SEED, "episodeSteps": DAYS * TURNS_PER_DAY + 2})
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


def _rows(frames, day, op, item=None):
    out = []
    for obs, act in frames:
        if int(obs["day"]) != day:
            continue
        for order in act["market"]:
            if order[0] == op and (item is None or order[1] == item):
                out.append((int(obs["hour"]), order))
    return out


# =========================================================================
# the engine accepts every turn
# =========================================================================

def test_every_turn_of_the_opening_is_a_legal_action():
    """Run the book as a real seat, both sides of the board, and let the engine
    judge it: a rejected action shows up as a status, never as an exception."""
    from kaggle_environments import make
    for seat in (0, 1):
        env = make("kaggriculture",
                   configuration={"seed": SEED,
                                  "episodeSteps": DAYS * TURNS_PER_DAY + 2})
        env.run([B.agent, "starter"] if seat == 0 else ["starter", B.agent])
        bad = [(t, s[seat].status) for t, s in enumerate(env.steps)
               if s[seat].status not in ("ACTIVE", "DONE")]
        assert not bad, f"seat {seat} left ACTIVE at {bad[:3]}"


def test_action_shape_matches_the_live_roster(game):
    """One order per hand in `hands` order, at most ten market orders (the
    engine truncates the eleventh silently), and only ops it knows."""
    for obs, act in game:
        me = int(obs.get("player", 0))
        hands = obs["farms"][me]["hands"]
        assert len(act["hands"]) == len(hands)
        for u in [act["farmer"]] + list(act["hands"]):
            assert isinstance(u, list) and u and u[0] in UNIT_OPS, u
        assert len(act["market"]) <= MAX_ORDERS
        for order in act["market"]:
            assert isinstance(order, list) and order[0] in MARKET_OPS, order
            if order[0] in ("BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL", "SELL"):
                assert len(order) == 3 and int(order[2]) > 0, order


def test_no_turn_over_asks_for_seed(game):
    """`interpreter` drops *every* PLANT of a crop when one turn's requests
    outrun the seed slot, so an over-ask costs the whole turn's planting."""
    for obs, act in game:
        want = {}
        for u in [act["farmer"]] + list(act["hands"]):
            if u[0] == "PLANT":
                want[u[1]] = want.get(u[1], 0) + 1
        for crop, n in want.items():
            assert n <= int(obs["private"]["seeds"].get(crop, 0)), \
                f"day {obs['day']} hour {obs['hour']}: {n} x {crop} on " \
                f"{obs['private']['seeds'].get(crop, 0)} seed"


# =========================================================================
# the day-0 line
# =========================================================================

def test_day_zero_buys_seven_wheat_and_twelve_melon(game):
    """The opening row itself.  Later hours of day 0 top the wheat up once the
    NE quadrant is unlocked and its 25 tiles are visible; the fixed line is the
    one the 3000 opening bank is spent on."""
    row = [(o[1], int(o[2])) for h, o in _rows(game, 0, "BUY_SEED") if h == 0]
    assert row == [("MELON", 12), ("WHEAT", B.DAY0_WHEAT)]
    assert B.DAY0_WHEAT == 7


def test_day_zero_never_orders_zero_wheat(game):
    wheat = sum(int(o[2]) for h, o in _rows(game, 0, "BUY_SEED", "WHEAT") if h == 0)
    assert wheat == 7


# =========================================================================
# day 10, the whole edge
# =========================================================================

def test_day_ten_melon_goes_out_in_small_early_lots(game):
    lots = _rows(game, 10, "SELL", "MELON")
    assert lots, "no melon row on the day melon saturates"
    assert all(int(o[2]) <= MAX_MELON_LOT for _, o in lots), lots
    assert lots[0][0] <= 12, f"first melon lot at hour {lots[0][0]}"
    assert len(lots) >= 6, f"only {len(lots)} lots"


def test_no_melon_row_is_offered_against_an_empty_shed(game):
    """`_commit_unit` refuses a SELL the shed cannot cover, so a row raised
    before the crop is dropped is a row that sells nothing."""
    for obs, act in game:
        for order in act["market"]:
            if order[0] == "SELL":
                assert int(obs["private"]["shed"].get(order[1], 0)) > 0, \
                    f"day {obs['day']} hour {obs['hour']} {order}"


def test_sixty_melon_are_settled_before_the_opponent_dumps(game):
    """Cumulative harvest minus what is still held is what actually reached the
    market; the recipe wants sixty of it in front of hour 17."""
    cum_harvest = held = sold_by = 0
    frames = [f for f in game if int(f[0]["day"]) == 10]
    for i, (obs, act) in enumerate(frames):
        held = (int(obs["private"]["shed"].get("MELON", 0))
                + sum(int(inv.get("MELON", 0))
                      for inv in obs["private"]["inventories"]))
        nxt = frames[i + 1][0] if i + 1 < len(frames) else None
        me = int(obs.get("player", 0))
        if nxt is not None:
            before = {(x, y): int(obs["farms"][me]["tiles"][y][x]["yield_units"])
                      for y in range(10) for x in range(10)
                      if isinstance(obs["farms"][me]["tiles"][y][x], dict)
                      and obs["farms"][me]["tiles"][y][x].get("crop") == "MELON"}
            after = {(x, y) for y in range(10) for x in range(10)
                     if isinstance(nxt["farms"][me]["tiles"][y][x], dict)
                     and nxt["farms"][me]["tiles"][y][x].get("crop") == "MELON"}
            if int(obs["hour"]) < OPPONENT_DUMP_HOUR:
                sold_by = cum_harvest - held
            cum_harvest += sum(v for k, v in before.items() if k not in after)
    assert sold_by >= 60, f"only {sold_by} melon settled before hour 17"


# =========================================================================
# off is free
# =========================================================================

def _macro():
    p = ROOT / "artifacts" / "theta.npy"
    if not p.exists():
        pytest.skip("no theta yet")
    import plan_stats
    return plan_stats.make_macro(np.load(p).astype(np.float32))


def test_unset_env_returns_the_bare_planner(monkeypatch):
    """Importing the book changes nothing: off, the factory hands back the
    planner itself, not a wrapper around it."""
    monkeypatch.delenv(opening.ENV_VAR, raising=False)
    macro = _macro()
    agent = runtime.make_agent(macro)
    assert not isinstance(agent, opening.OpeningSplice)

    from kaggle_environments import make
    trainer = make("kaggriculture", configuration={"seed": SEED}).train([None, "starter"])
    obs = trainer.reset()
    assert agent(obs) == runtime.Runtime(macro).act(obs)


def test_env_var_splices_the_book_in_front_of_the_planner(monkeypatch):
    monkeypatch.setenv(opening.ENV_VAR, f"{ROOT / 'src' / 'kagg3' / 'agent' / 'book_open16.py'}:16")
    spliced = runtime.make_agent(_macro())
    assert isinstance(spliced, opening.OpeningSplice) and spliced.k == 16

    from kaggle_environments import make
    trainer = make("kaggriculture", configuration={"seed": SEED}).train([None, "starter"])
    obs = trainer.reset()
    assert spliced(obs) == B.agent(obs)


# =========================================================================
# the book itself, pinned
# =========================================================================

#: Digest of the book's own 384-turn action stream on `SEED` against
#: `starter`, one entry per day.  It pins the file this test owns; move it only
#: with a measured reason, and never to make a red test green.
PIN = ("d664caa7967eebf8",)


def _digest(frames):
    h = hashlib.blake2b(digest_size=8)
    for _, act in frames:
        h.update(json.dumps(act, sort_keys=True, separators=(",", ":")).encode())
    return h.hexdigest()


@pytest.mark.skipif(os.environ.get("KAGG3_BOOK_PIN") == "off",
                    reason="pin deliberately suspended")
def test_book_stream_is_pinned(game):
    assert _digest(game) in PIN
