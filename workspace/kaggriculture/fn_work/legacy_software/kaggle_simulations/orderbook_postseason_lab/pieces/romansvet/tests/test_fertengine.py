"""`plan.FERT_TIMING_ON` / the `g12` gene `macro.fert_defer`: spend the
fertilizer unit on the day it buys the most.

A FERTILIZE sets `fertilized_until_day = day + 2` (`kaggriculture.py:481`), so
it covers three end-of-days and what it buys depends on WHEN it lands: a
one-time crop scores +2 instead of +1 on each in-window watering inside the
coverage (`:440`), an ongoing crop on each fire inside it (`:799`).
`fert_marginal_value` prices that exactly; what the shipped site never asks is
whether the SAME unit on the SAME tile buys more TOMORROW.  It does not,
because `fert_cand` is a bar test and both the good day and the mediocre one
clear a 20-70 coin quote.

Measured on the 22 ENG22 boards, both seats, real engine
(`docs/strategy/2026-09-16-fertengine.md`, `S/fertengine/`): 132.2 of our 185.1
applications a game land off the best day (71 %) against 14.5 of the
fertilizer-ENGINE class's 170.7 (8.5 %).

THE SWITCH SHIPS OFF and the gene ships at zero unless the legs in that
document say otherwise.
"""
from __future__ import annotations

import contextlib
import hashlib
import os
import subprocess
import sys
import tempfile

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, sys.argv[sys.argv.index("--digests") + 1]
                if "--digests" in sys.argv else "src")

import numpy as np
import pytest

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P
from kagg3.core import policy as PO
from kagg3.core import brain

# `kagg3` FIRST -- see the note in `tests/test_fertdenial.py`.
from test_budget_order import _macro

if "--digests" in sys.argv:                 # the pristine-tree subprocess
    import kagg3
    _want = os.path.abspath(sys.argv[sys.argv.index("--digests") + 1])
    assert os.path.abspath(kagg3.__file__).startswith(_want + os.sep), \
        f"the pin loaded {kagg3.__file__}, not the tree under {_want}"

BASE_PRICE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)

#: A fertilizer market 400 units long, so the quote is
#: `100 - 0.2 * 400 = 20` and even a one-unit wheat application clears the bar.
#: The gate is about WHICH DAY, not about the bar, so every board here has to
#: admit the application OFF or it measures nothing.
CHEAP = spec.MARKET_I0 + 400


def _view(day=22, crop=spec.I_STRAWBERRY, n=6, age=10, money=20_000,
          shed_fert=20, n_wh=0, wh_age=0, mkt_inv=CHEAP, nquad=2):
    z = np.zeros(spec.N_TILES, np.int32)
    kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_day, t_yield, t_fert = z.copy(), z.copy(), z - 1
    kind[:n] = spec.KIND_PLANT
    occ[:n] = crop
    t_day[:n] = day - age
    kind[n:n + n_wh] = spec.KIND_PLANT
    occ[n:n + n_wh] = spec.I_WHEAT
    t_day[n:n + n_wh] = day - wh_age
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_FERT] = shed_fert
    inv = np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32)
    inv[spec.I_FERT] = int(mkt_inv)
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=t_day, t_water=z.copy(),
        t_cons=z.copy(), t_yield=t_yield, t_fert=t_fert, t_cared=z.copy(),
        t_favail=z.copy(), shed=shed,
        seeds=np.zeros(spec.N_CROPS, np.int32), money=np.int32(money),
        nquad=np.int32(nquad),
        price=np.array([25, 35, 60, 120, 250, 50, 160, 200,
                        max(1, 100 - (int(mkt_inv) - spec.MARKET_I0) // 5)], np.int32),
        mkt_inv=inv, shops=np.zeros(spec.N_SHOPS, np.int32))


def _sell_macro(**kw):
    """A zero reservation price, so the lot greedy actually sells -- what the
    gate refuses is observable in the market rows alone.  `fert_defer` is
    dropped on the pristine PRE-`g12` tree the digest pin runs against."""
    if "fert_defer" in kw and "fert_defer" not in P.Macro._fields:
        kw = {k: v for k, v in kw.items() if k != "fert_defer"}
    return _macro(hold=np.zeros(spec.N_PRODUCTS, np.int32), **kw)


def _plan(view, macro=None):
    return tuple(np.asarray(a) for a in P.build_day(np, view, macro or _sell_macro()))


def _digest(plan):
    h = hashlib.sha256()
    for a in plan:
        h.update(np.ascontiguousarray(np.asarray(a, np.int32)).tobytes())
    return h.hexdigest()[:16]


def _sold(plan, product):
    op, arg, qty = plan[3], plan[4], plan[5]
    return int(np.asarray(qty)[(np.asarray(op) == O.MO_SELL)
                               & (np.asarray(arg) == product)].sum())


def _applied(plan, shed_fert=20):
    """Applications the day admitted: the shed holds `shed_fert` and the
    reservation is `n_fert_eff`, so what is NOT sold is what is spent."""
    return shed_fert - _sold(plan, spec.I_FERT)


#: STRAWBERRY fires every 2 days from age 10, so a tile at age 10 on day 22
#: (fires 22/24/26/28) has ONE fire in today's `day+1..day+3` window and TWO in
#: tomorrow's -- the deferral case.  Age 11 is its control: two today, one
#: tomorrow.  WHEAT's window is ages 2..4, so age 0 buys one unit today and
#: three at age 2, and age 2 is that pair's control.  TOMATO fires every day,
#: so its window is three fires whatever the day -- nothing to defer.
PIN_BOARDS = (
    ("straw-early", dict(day=22, crop=spec.I_STRAWBERRY, age=10)),
    ("straw-eve", dict(day=23, crop=spec.I_STRAWBERRY, age=11)),
    ("tomato", dict(day=22, crop=spec.I_TOMATO, age=9)),
    ("wheat-young", dict(day=22, crop=spec.I_STRAWBERRY, age=11, n=2,
                         n_wh=4, wh_age=0)),
    ("wheat-ripe", dict(day=22, crop=spec.I_STRAWBERRY, age=11, n=2,
                        n_wh=4, wh_age=2)),
    ("terminal", dict(day=29, crop=spec.I_STRAWBERRY, age=10)),
)

#: The commit this branch sits on, whose planner has no `FERT_TIMING_ON` and no
#: `g12` at all.  A SHA and not `HEAD~1`, so the pin keeps its meaning after the
#: branch is merged and master moves on.
PRE_SWITCH = "d214bc7"


@contextlib.contextmanager
def _knob(on=True, days=None):
    if not hasattr(P, "FERT_TIMING_ON"):
        # `--digests` mode inside the pristine pre-switch tree: nothing to set.
        yield
        return
    was = (P.FERT_TIMING_ON, P.FERT_TIMING_DAYS)
    P.FERT_TIMING_ON = on
    if days is not None:
        P.FERT_TIMING_DAYS = days
    try:
        yield
    finally:
        (P.FERT_TIMING_ON, P.FERT_TIMING_DAYS) = was


def _digests():
    """The OFF plan of every pin board (the knob is set explicitly: ON ships)."""
    with _knob(on=False):
        return {n: _digest(_plan(_view(**kw))) for n, kw in PIN_BOARDS}


def _tree_digests(ref=PRE_SWITCH):
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(f"git archive {ref} src | tar -x -C {td}", shell=True,
                       cwd=root, check=True)
        out = subprocess.run(
            [sys.executable, os.path.abspath(__file__), "--digests",
             os.path.join(td, "src")],
            cwd=root, capture_output=True, text=True, check=True)
    return dict(line.split(None, 1) for line in out.stdout.strip().splitlines())


# =========================================================================
# OFF is master, byte for byte
# =========================================================================

def test_on_is_shipped():
    """Shipped ON since Kaggle sub 56284867 (2026-09-16, DAYS=2); every "off"
    read below sets the knob explicitly."""
    assert P.FERT_TIMING_ON is True and P.FERT_TIMING_DAYS == 2


def test_off_plan_is_byte_identical_to_master():
    """The whole-plan digest of six boards against a pristine master tree --
    which has no `fert_defer` field, so the pin also proves the appended Macro
    entry changed nothing the planner reads at zero."""
    assert _digests() == _tree_digests()


def test_a_zero_look_ahead_is_the_off_plan_on_every_board():
    """`FERT_TIMING_DAYS = 0` names no later day, so ON has to re-evaluate to
    OFF -- the property that makes the constant a size and not a mechanism."""
    off = _digests()
    with _knob(days=0):
        assert {n: _digest(_plan(_view(**kw))) for n, kw in PIN_BOARDS} == off


def test_the_gene_at_zero_is_the_off_plan_on_every_board():
    """The other half of the same statement: the gene path, driven by a macro
    whose `fert_defer` is the zero every pre-`g12` theta decodes."""
    off = _digests()
    with _knob(on=False):
        got = {n: _digest(_plan(_view(**kw), _sell_macro(fert_defer=np.int32(0))))
               for n, kw in PIN_BOARDS}
    assert got == off


def test_gene_cap_matches_the_plan_loop_bound():
    """`plan` cannot import `brain`, so the clip and the static loop bound are
    two constants that must agree or the gene's top value is unreachable."""
    assert int(brain.FERT_DEFER_MAX) == int(P.FERT_TIMING_MAX)


# =========================================================================
# WHAT THE GATE DOES
# =========================================================================

def test_an_application_a_day_early_is_deferred_and_the_fire_eve_one_is_kept():
    """STRAWBERRY at age 10 on day 22: one fire in `23..25`, two in `24..26`.
    At age 11 the two-fire window IS today's.  One day of look-ahead is enough
    for both."""
    early, eve = _view(day=22, age=10), _view(day=23, age=11)
    with _knob(on=False):
        assert _applied(_plan(early)) == 6 and _applied(_plan(eve)) == 6
    with _knob(days=1):
        assert _applied(_plan(early)) == 0
        assert _applied(_plan(eve)) == 6


def test_a_one_time_crop_waits_for_its_yield_window():
    """WHEAT's window is ages 2..4 and the coverage is three days, so an
    application at age 0 buys one unit and at age 2 buys three.  Two days of
    look-ahead reach the peak from age 0; one day is enough to refuse age 0,
    because tomorrow alone already beats today."""
    young = _view(day=22, age=11, n=2, n_wh=4, wh_age=0)
    ripe = _view(day=22, age=11, n=2, n_wh=4, wh_age=2)
    with _knob(on=False):
        assert _applied(_plan(young)) == 6 and _applied(_plan(ripe)) == 6
    for d in (1, 2):
        with _knob(days=d):
            assert _applied(_plan(young)) == 2, d      # the 2 strawberry only
            assert _applied(_plan(ripe)) == 6, d


def test_a_daily_crop_is_never_deferred():
    """TOMATO fires every day, so `day+1..day+3` holds three fires whatever the
    day -- today is never beaten and the gate is a no-op on it."""
    v = _view(day=22, crop=spec.I_TOMATO, age=9)
    with _knob(on=False):
        off = _applied(_plan(v))
    assert off == 6
    for d in (1, 2, 3):
        with _knob(days=d):
            assert _applied(_plan(v)) == off, d


def test_the_deferred_unit_is_sold_and_no_other_product_moves():
    """The refused applications need no plumbing of their own: `n_fert_want`
    falls, `fert_reserved` falls, `avail[I_FERT]` rises and the lot greedy puts
    them on the day's rows."""
    v = _view(day=22, age=10)
    with _knob(on=False):
        off = _plan(v)
    with _knob(days=1):
        on = _plan(v)
    assert _sold(on, spec.I_FERT) == _sold(off, spec.I_FERT) + 6
    for p in range(spec.N_PRODUCTS):
        if p != spec.I_FERT:
            assert _sold(on, p) == _sold(off, p), p


def test_the_gene_drives_the_gate_with_the_switch_off():
    """`FERT_TIMING_ON` is the A/B override; the shipped path is the gene, so a
    macro with `fert_defer = 1` must produce the switch's plan on its own."""
    v = _view(day=22, age=10)
    with _knob(days=1):
        want = _digest(_plan(v))
    with _knob(on=False):
        assert _digest(_plan(v, _sell_macro(fert_defer=np.int32(1)))) == want


def test_the_look_ahead_is_monotone_in_days():
    """A longer horizon can only refuse more: the gate is a running maximum
    over the projected days."""
    v = _view(day=22, age=11, n=2, n_wh=4, wh_age=0)
    got = []
    for d in range(0, P.FERT_TIMING_MAX + 1):
        with _knob(days=d):
            got.append(_applied(_plan(v)))
    assert got == sorted(got, reverse=True), got
    assert got[0] == 6 and got[-1] < got[0], got


# =========================================================================
# THE GENE -- inert at zero, and a slope the ES can feel
# =========================================================================

INIT = ("/mnt/e/_work/kaggriculture3/artifacts/kagg2_games/thetas/"
        "flow193_g100_hr.npy")
TRAJ = "/mnt/e/_work/kaggriculture3/tests/data/trajectory_obs.npz"
ES_POP, ES_SIGMA = 512, 0.02
#: The `g11` band, restated: a minority of the population must decode at least
#: one day, and the centre must still be the plan most members make.
BAND = (0.15, 0.35)


def _boards(n, seed=0):
    d = np.load(TRAJ)
    obs = [brain.PolicyObs(**{f: d[f][i] for f in brain.PolicyObs._fields
                              if f in d.files})
           for i in np.random.default_rng(seed).choice(len(d["day"]), n, replace=False)]
    inputs = []
    for o in obs:
        prod, glob, drain = brain.features(np, o)
        boards = brain.board_forecasts(np, o)
        inputs.append((prod, glob, drain, brain.production_forecast(np, o, boards),
                       brain.forward_value(np, o, boards)))
    return obs, inputs


@pytest.mark.skipif(not os.path.isfile(INIT) or not os.path.isfile(TRAJ),
                    reason="needs the shipped theta and the trajectory fixture")
def test_the_shipped_theta_decodes_no_look_ahead_on_any_real_board():
    theta = PO.pad(np.load(INIT).astype(np.float32))
    assert theta.shape == (PO.N_PARAMS,), theta.shape
    assert not theta[PO.offset("g12"):PO.offset("gb12") + PO.N_FT_OUT].any()
    obs, _ = _boards(200)
    for o in obs:
        m = brain.decide(np, theta, o)
        assert int(m.fert_defer) == 0
        assert np.asarray(m.fert_defer).dtype == np.int32


@pytest.mark.skipif(not os.path.isfile(INIT) or not os.path.isfile(TRAJ),
                    reason="needs the shipped theta and the trajectory fixture")
def test_one_es_step_moves_the_look_ahead_for_a_minority_of_the_population():
    """`round(16 * z)` first steps at `|z| >= 1/32`, so the antithetic pair at
    sigma 0.02 straddles the step and selection has something to rank."""
    theta = PO.pad(np.load(INIT).astype(np.float32))
    _obs, inputs = _boards(8, seed=3)
    rng = np.random.default_rng(1234)
    pop = (theta[None] + ES_SIGMA * rng.normal(0.0, 1.0, (ES_POP, PO.N_PARAMS))
           ).astype(np.float32)
    days = np.empty((ES_POP, len(inputs)), np.int32)
    for m, member in enumerate(pop):
        params = PO.unpack(np, member)
        for b, args in enumerate(inputs):
            z = PO.forward(np, params, *args).ft
            days[m, b] = int(np.clip(brain._qfloor(np, brain.FERT_DEFER_GAIN * z + 0.5),
                                     0, brain.FERT_DEFER_MAX))
    per_board = (days >= 1).mean(axis=0)
    lo, hi = BAND
    assert lo <= float(np.median(per_board)) <= hi, per_board
    assert per_board.min() > 0.05, per_board
    assert (days == 0).mean() > 0.5, (days == 0).mean()


def test_a_short_theta_still_unpacks_and_decodes_the_zero_gene():
    """Every theta on disk predates `g12`; `unpack` pads and the decode is the
    shipped plan."""
    short = np.zeros(PO.offset("g12"), np.float32)
    p = PO.unpack(np, short)
    assert p.g12.shape == (PO.N_HEAD_HID, PO.N_FT_OUT)
    assert not np.asarray(p.g12).any() and not np.asarray(p.gb12).any()


# =========================================================================
# jit == numpy
# =========================================================================

def test_the_whole_switch_traces_under_jit_and_agrees_with_numpy():
    import jax
    import jax.numpy as jnp
    for kw in (dict(day=22, age=10), dict(day=22, age=11, n=2, n_wh=4, wh_age=0)):
        v = _view(**kw)
        with _knob(days=2):
            want = _plan(v)
            jv = P.DayView(**{k: jnp.asarray(x) for k, x in v._asdict().items()})
            m = _sell_macro()
            jm = type(m)(**{k: (jnp.asarray(x) if isinstance(x, np.ndarray) else x)
                            for k, x in m._asdict().items()})
            got = jax.jit(lambda w: P.build_day(jnp, w, jm))(jv)
        for a, b in zip(want, got):
            assert (np.asarray(a) == np.asarray(b)).all(), kw


def test_the_traced_gene_path_is_one_program_for_every_horizon():
    """Under `jit` `macro.fert_defer` is a tracer, so the horizon must be a
    `where` and not a Python branch -- one traced program serving 0, 1 and 2."""
    import jax
    import jax.numpy as jnp
    v = _view(day=22, age=10)
    jv = P.DayView(**{k: jnp.asarray(x) for k, x in v._asdict().items()})
    f = jax.jit(lambda w, m: P.build_day(jnp, w, m))
    for d in (0, 1, 2):
        m = _sell_macro(fert_defer=np.int32(d))
        jm = type(m)(**{k: (jnp.asarray(x) if isinstance(x, np.ndarray) else x)
                        for k, x in m._asdict().items()})
        for a, b in zip(_plan(v, m), f(jv, jm)):
            assert (np.asarray(a) == np.asarray(b)).all(), d


if __name__ == "__main__":                # the pristine-tree subprocess
    for _n, _d in _digests().items():
        print(_n, _d)
