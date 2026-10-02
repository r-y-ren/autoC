"""`plan.RIVAL_TELL_ON`: the slot-priority batch, measured instead of guessed.

`docs/strategy/2026-09-16-rivaltell.md` sect.7. `SELL_SLOT_PRIORITY` ranks a
SELL row's slots by the coins a rival batch would take away and sizes that
batch from `opp_ripe` -- the yield standing on the rival's board. This switch
replaces it, per item, with what the rival has actually been selling, read off
the public pot by `agent/tell.py`'s engine identity.

OFF, and with the measurement held at its sentinel, the plan is the one the
shipped tree emits -- both pinned below by whole-plan sha256, the OFF arm
against a pristine `git archive HEAD src` tree in a subprocess
(`tests/test_slotprio.py`'s pin).
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import tempfile

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, sys.argv[sys.argv.index("--digests") + 1]
                if "--digests" in sys.argv else "src")

import numpy as np
from test_budget_order import _macro

from kagg3 import spec
from kagg3.core import plan as P

BASE_PRICE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)


def _view(day=10, money=20_000, n_wh=8, age=4, shed_wh=0, shed_to=0,
          t_water=0, yld=6, nquad=1, shops=0, mkt_inv=spec.MARKET_I0,
          opp_ripe=None, opp_rate=None):
    z = np.zeros(spec.N_TILES, np.int32)
    kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_day, t_wat, t_yield = z.copy(), z.copy(), z.copy()
    kind[:n_wh] = spec.KIND_PLANT
    occ[:n_wh] = spec.I_WHEAT
    t_day[:n_wh] = day - age
    t_yield[:n_wh] = yld
    t_wat[:n_wh] = t_water
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_WHEAT] = shed_wh
    shed[spec.I_TOMATO] = shed_to
    kw = {} if opp_ripe is None else {"opp_ripe": np.asarray(opp_ripe, np.int32)}
    if opp_rate is not None:
        kw["opp_rate"] = np.asarray(opp_rate, np.int32)
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=t_day, t_water=t_wat,
        t_cons=z.copy(), t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(),
        t_favail=z.copy(), shed=shed,
        seeds=np.zeros(spec.N_CROPS, np.int32), money=np.int32(money),
        nquad=np.int32(nquad), price=BASE_PRICE,
        mkt_inv=np.full(spec.N_PRODUCTS, int(mkt_inv), np.int32),
        shops=np.full(spec.N_SHOPS, int(shops), np.int32), **kw)


def _sell_macro():
    return _macro(hold=np.zeros(spec.N_PRODUCTS, np.int32))


def _plan(view, macro=None):
    return tuple(np.asarray(a) for a in P.build_day(np, view, macro or _macro()))


def _digest(plan):
    h = hashlib.sha256()
    for a in plan:
        h.update(np.ascontiguousarray(np.asarray(a, np.int32)).tobytes())
    return h.hexdigest()[:16]


PIN_BOARDS = (
    ("hot", dict(day=10, n_wh=8, shed_wh=50, shed_to=45)),
    ("cool", dict(day=10, n_wh=8, shed_wh=0, shed_to=0)),
    ("wet", dict(day=10, n_wh=8, shed_wh=50, shed_to=45, t_water=1)),
    ("bare", dict(day=12, n_wh=0, shed_wh=60, shed_to=38)),
    ("town", dict(day=10, n_wh=8, shed_wh=50, shed_to=45, shops=2)),
)


def _own_digests():
    out = {}
    for n, kw in PIN_BOARDS:
        out[n] = _digest(_plan(_view(**kw)))
        out[n + "_sell"] = _digest(_plan(_view(**kw), _sell_macro()))
    return out


def _head_digests():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(f"git archive HEAD src | tar -x -C {td}", shell=True,
                       cwd=root, check=True)
        out = subprocess.run(
            [sys.executable, os.path.abspath(__file__), "--digests",
             os.path.join(td, "src")],
            cwd=root, capture_output=True, text=True, check=True)
    return dict(line.split(None, 1) for line in out.stdout.strip().splitlines())


# =========================================================================
# OFF: the shipped program, byte for byte
# =========================================================================

def test_off_is_the_default():
    assert P.RIVAL_TELL_ON is False
    assert P.RIVAL_TELL_FORCE_PROXY is False
    assert (P.RIVAL_TELL_WINDOW, P.RIVAL_TELL_MIN_TURNS) == (6, 2)
    assert P.RIVAL_TELL_SKIP == (spec.I_WHEAT, spec.I_FERT)
    assert np.all(np.asarray(_view().opp_rate) == -1)


def test_off_plan_is_byte_identical_to_head():
    """The whole plan tuple, hashed, against a pristine HEAD tree."""
    assert _own_digests() == _head_digests()


def test_the_sentinel_is_the_slotprio_plan(monkeypatch):
    """Judge leg 1 at plan level: an armed seat whose measurement has not
    fired plans exactly `SELL_SLOT_PRIORITY_ON`'s plan, board for board."""
    ripe = np.zeros(spec.N_PRODUCTS, np.int32)
    ripe[spec.I_TOMATO] = 30
    monkeypatch.setattr(P, "SELL_SLOT_PRIORITY_ON", True)
    slotprio = {n: _digest(_plan(_view(opp_ripe=ripe, **kw), _sell_macro()))
                for n, kw in PIN_BOARDS}
    monkeypatch.setattr(P, "RIVAL_TELL_ON", True)
    sentinel = np.full(spec.N_PRODUCTS, -1, np.int32)
    armed = {n: _digest(_plan(_view(opp_ripe=ripe, opp_rate=sentinel, **kw),
                              _sell_macro()))
             for n, kw in PIN_BOARDS}
    assert armed == slotprio


def test_the_measured_rate_replaces_the_proxy_per_item():
    """`batch[p] = clip(rate if gated else ripe, MIN, MAX)`, item by item."""
    pt = P.default_price_table()
    inv = np.full((1, spec.N_PRODUCTS), int(spec.MARKET_I0), np.int32)
    lots = np.zeros((1, spec.N_PRODUCTS), np.int32)
    lots[0, spec.I_STRAWBERRY] = 5
    ripe = np.zeros(spec.N_PRODUCTS, np.int32)
    ripe[spec.I_STRAWBERRY] = 30                      # proxy would clamp to 24
    i0 = int(spec.MARKET_I0) - spec.PRICE_TABLE_LO
    row = pt[spec.I_STRAWBERRY]
    for rate, want_batch in ((-1, 24), (0, 8), (3, 8), (12, 12), (40, 24)):
        r = np.full(spec.N_PRODUCTS, -1, np.int32)
        r[spec.I_STRAWBERRY] = rate
        got = int(P.sell_slot_scores(np, pt, inv, lots, ripe, r)[0,
                                                                spec.I_STRAWBERRY])
        want = int(sum(row[i0 + j] - row[i0 + want_batch + j] for j in range(5)))
        assert got == want, (rate, got, want)
    # no rate vector at all is the shipped expression
    assert int(P.sell_slot_scores(np, pt, inv, lots, ripe)[0, spec.I_STRAWBERRY]) \
        == int(P.sell_slot_scores(np, pt, inv, lots, ripe,
                                  np.full(spec.N_PRODUCTS, -1, np.int32))
               [0, spec.I_STRAWBERRY])


def test_a_fired_item_reorders_the_row_against_the_proxy():
    """The whole point: the proxy puts the rival's standing STRAWBERRY first,
    the measurement puts the MILK it has actually been selling there."""
    pt = P.default_price_table()
    inv = np.full((1, spec.N_PRODUCTS), int(spec.MARKET_I0), np.int32)
    lots = np.zeros((1, spec.N_PRODUCTS), np.int32)
    lots[0, spec.I_MILK] = lots[0, spec.I_STRAWBERRY] = 5
    ripe = np.zeros(spec.N_PRODUCTS, np.int32)
    ripe[spec.I_STRAWBERRY] = 30
    proxy = P.sell_slot_perm(np, lots[0],
                             P.sell_slot_scores(np, pt, inv, lots, ripe)[0])
    assert list(np.asarray(proxy))[:2] == [spec.I_STRAWBERRY, spec.I_MILK]
    rate = np.full(spec.N_PRODUCTS, -1, np.int32)
    rate[spec.I_MILK], rate[spec.I_STRAWBERRY] = 24, 0
    told = P.sell_slot_perm(np, lots[0],
                            P.sell_slot_scores(np, pt, inv, lots, ripe, rate)[0])
    assert list(np.asarray(told))[:2] == [spec.I_MILK, spec.I_STRAWBERRY]


# =========================================================================
# the estimator, on a synthetic observation stream
# =========================================================================

from kagg3.agent import tell            # noqa: E402


def _stream(riv_sell, riv_buy=None, our_sell=None, our_buy=None, shops=None,
            inv0=None, step0=0):
    """Play `T` turns of a made-up engine and hand the seat what it would see.

    `inv[t+1] = inv[t] + our_sell + riv_sell - our_buy - riv_buy - town(t)`,
    which is the engine identity this estimator inverts.
    """
    riv_sell = np.asarray(riv_sell, np.int32)
    T = riv_sell.shape[0]
    z = np.zeros((T, spec.N_PRODUCTS), np.int32)
    riv_buy = z if riv_buy is None else np.asarray(riv_buy, np.int32)
    our_sell = z if our_sell is None else np.asarray(our_sell, np.int32)
    our_buy = z if our_buy is None else np.asarray(our_buy, np.int32)
    shops = (np.zeros(spec.N_SHOPS, np.int32) if shops is None
             else np.asarray(shops, np.int32))
    inv = (np.full(spec.N_PRODUCTS, int(spec.MARKET_I0), np.int32)
           if inv0 is None else np.asarray(inv0, np.int32)).copy()
    out = []
    for t in range(T):
        rows = [["SELL", spec.PRODUCTS[p], int(our_sell[t, p])]
                for p in range(spec.N_PRODUCTS) if our_sell[t, p]]
        rows += [["BUY_PRODUCT", spec.PRODUCTS[p], int(our_buy[t, p])]
                 for p in range(spec.N_PRODUCTS) if our_buy[t, p]]
        out.append((step0 + t, inv.copy(), shops, rows))
        inv = (inv + our_sell[t] + riv_sell[t] - our_buy[t] - riv_buy[t]
               - tell.town_tick(step0 + t, shops)).astype(np.int32)
    out.append((step0 + T, inv.copy(), shops, []))   # the dawn that closes it
    return out


def _play(rt, stream):
    for step, inv, shops, rows in stream:
        rt.observe(step, inv, shops)
        rt.record_orders(rows)
    return rt


def test_the_identity_recovers_a_rival_that_trades_beside_us():
    """Seven turns, both seats trading, shops and the town centre both eating:
    the rate is the rival's own units per turn and nothing else."""
    T = 7
    riv = np.zeros((T, spec.N_PRODUCTS), np.int32)
    riv[:, spec.I_MILK] = 12                      # every turn: 12/turn
    riv[2, spec.I_WOOL] = 30                      # one turn only
    riv[3, spec.I_WOOL] = 30                      # two turns -> gate fires
    riv[:, spec.I_WHEAT] = 20                     # excluded item
    ours = np.zeros((T, spec.N_PRODUCTS), np.int32)
    ours[:, spec.I_MELON] = 7
    ourb = np.zeros((T, spec.N_PRODUCTS), np.int32)
    ourb[1, spec.I_FERT] = 5
    shops = np.ones(spec.N_SHOPS, np.int32)       # every shop unlocked, x1
    rt = _play(tell.RivalTell(), _stream(riv, our_sell=ours, our_buy=ourb,
                                         shops=shops, step0=19))
    b = rt.batch()
    assert int(b[spec.I_MILK]) == 12              # 6 turns x 12 / 6
    assert int(b[spec.I_WOOL]) == 10              # 60 units over the window
    assert int(b[spec.I_WHEAT]) == -1 and int(b[spec.I_FERT]) == -1
    for p in (spec.I_CARROT, spec.I_TOMATO, spec.I_STRAWBERRY, spec.I_MELON,
              spec.I_EGG):
        assert int(b[p]) == -1, p


def test_one_turn_of_history_does_not_fire_and_a_short_window_keeps_the_proxy():
    T = 8
    riv = np.zeros((T, spec.N_PRODUCTS), np.int32)
    riv[5, spec.I_EGG] = 40                       # one turn in the window
    rt = _play(tell.RivalTell(), _stream(riv))
    assert int(rt.batch()[spec.I_EGG]) == -1      # 1 of 6 < MIN_TURNS
    # and before a full window has been seen, nothing fires at all
    riv2 = np.zeros((3, spec.N_PRODUCTS), np.int32)
    riv2[:, spec.I_EGG] = 9
    short = _play(tell.RivalTell(), _stream(riv2))
    assert np.all(short.batch() == -1)


def test_a_gap_in_the_stream_drops_the_history():
    """The identity is only exact on consecutive steps, so a seat that misses
    a turn starts again rather than pricing a delta across the hole."""
    T = 7
    riv = np.zeros((T, spec.N_PRODUCTS), np.int32)
    riv[:, spec.I_MILK] = 12
    stream = _stream(riv)
    rt = _play(tell.RivalTell(), stream)
    assert int(rt.batch()[spec.I_MILK]) == 12
    gapped = [s for i, s in enumerate(stream) if i != 3]
    assert np.all(_play(tell.RivalTell(), gapped).batch() == -1)


def test_force_proxy_holds_the_sentinel(monkeypatch):
    T = 7
    riv = np.zeros((T, spec.N_PRODUCTS), np.int32)
    riv[:, spec.I_MILK] = 12
    rt = _play(tell.RivalTell(), _stream(riv))
    assert int(rt.batch()[spec.I_MILK]) == 12
    monkeypatch.setattr(P, "RIVAL_TELL_FORCE_PROXY", True)
    assert np.all(rt.batch() == -1)


if __name__ == "__main__":                      # the HEAD-tree subprocess
    for _n, _d in _own_digests().items():
        print(_n, _d)
