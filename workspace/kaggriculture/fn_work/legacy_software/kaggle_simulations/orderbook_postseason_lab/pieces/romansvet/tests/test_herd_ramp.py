"""HERD_RAMP: the day-0..9 purse moved toward the herd instead of away from it.

`2026-09-17-earlyramp.md` spent the early purse on non-melon seed tiles and the
herd starved -- animals 17 -> 13.8, collected fertilizer 379 -> 230, their milk
and fertilizer revenue +6,432, ENG22 -10,278.  That reading names the herd as
what the early purse buys.  `brain.HERD_RAMP_ON` is the untested opposite sign
on the same axis: the same `n_dev` free tiles, `HERD_RAMP_SHIFT` of them pushed
from `plant_total` into `animal_count` while `obs.day < HERD_RAMP_DAYS`.

The first test is the pin: OFF the whole decode is the SHIPPED tree's, byte for
byte (`tests/_pin.py`, `_pin.SHIPPED`).
"""
from __future__ import annotations

import hashlib
import os
import sys

import _pin

_pin.bootstrap()                       # kagg3 FIRST, out of the right tree

import numpy as np
import pytest

from kagg3 import spec
from kagg3.core import brain
from kagg3.core import plan as P
from kagg3.core import policy as PO
from kagg3.es import archetypes as A

BASE = np.array([spec.DEFAULT_MARKET_PARAMS[n]["base"] for n in spec.PRODUCTS],
                np.float32)
SWITCH = "HERD_RAMP_ON"


class _On:
    def __init__(self, **kw):
        self.kw = kw

    def __enter__(self):
        self.old = {k: getattr(brain, k) for k in self.kw}
        for k, v in self.kw.items():
            setattr(brain, k, v)

    def __exit__(self, *a):
        for k, v in self.old.items():
            setattr(brain, k, v)


def _obs(day=0, money=3000, nquad=4, kind=None, occ=None):
    z = np.zeros(100, np.int32)
    return brain.PolicyObs(
        day=np.int32(day), money=np.int32(money), opp_money=np.int32(3000),
        kind=np.full(100, spec.KIND_EMPTY, np.int32) if kind is None else kind,
        occ=z - 1 if occ is None else occ,
        opp_kind=np.full(100, spec.KIND_EMPTY, np.int32), opp_occ=z - 1,
        t_day=z.copy(), t_yield=z.copy(),
        shed=np.zeros(spec.N_ITEMS, np.int32), seeds=np.zeros(spec.N_CROPS, np.int32),
        nquad=np.int32(nquad), opp_nquad=np.int32(nquad),
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32), price=BASE.copy(),
        shops=np.zeros(spec.N_SHOPS, np.int32))


#: A spread of boards, so the pin is a claim about the decode and not about one
#: lucky day: inside the window, on its edge, and well past it.
OBS = [_obs(), _obs(day=3, money=900, nquad=1), _obs(day=9, money=2_000),
       _obs(day=10, money=6_000), _obs(day=12, money=40_000),
       _obs(day=27, money=120_000, nquad=2)]


#: B / the shipped centre, padded to whatever layout the tree under test has.
#: A pin taken on a zero theta would assert nothing about the herd split, which
#: is exactly the block this switch edits.
#: `artifacts/` is untracked, so a worktree checkout has none -- fall back to
#: the master checkout, then to a zero archetype.  Both ends of the pin resolve
#: it the same way (the subprocess runs with `cwd` = this repo root).
_TH = next((p for p in (
    os.path.join(_pin.repo_root(__file__),
                 "artifacts/kagg2_games/thetas/flow193_g100_hr.npy"),
    "/mnt/e/_work/kaggriculture3/artifacts/kagg2_games/thetas/flow193_g100_hr.npy",
) if os.path.exists(p)), "")


def _theta():
    t = np.load(_TH).astype(np.float32) if _TH \
        else np.asarray(A.archetype_theta(), np.float32)
    n = PO.N_PARAMS
    return np.concatenate([t[:n], np.zeros(max(0, n - t.size), np.float32)])


def _digest_macro(m):
    h = hashlib.sha256()
    for a in m:
        h.update(np.ascontiguousarray(np.asarray(a, np.int32)).tobytes())
    return h.hexdigest()[:16]


# ---- the plan side, for `MELON_VETO_FLOOD` ------------------------------
# Built HERE and not imported from `test_route_early` / `test_budget_order`:
# those fixtures do their own `sys.path.insert(0, "src")` on the way in, which
# in a `--digests` subprocess would load THIS tree's planner into the pin and
# compare the tree with itself (`tests/_pin.py` §1).

def _pview(day=14, melon_over=0, n_ripe=6, money=20_000):
    """A board with `n_ripe` ripe tomatoes and empty land for the mix, and a
    dawn melon book standing `melon_over` units over `spec.MARKET_I0`."""
    z = np.zeros(spec.N_TILES, np.int32)
    kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_yield = z.copy()
    kind[:n_ripe] = spec.KIND_PLANT
    occ[:n_ripe] = spec.I_TOMATO
    t_yield[:n_ripe] = 4
    inv = np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32)
    inv[spec.I_MELON] = spec.MARKET_I0 + melon_over
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(),
        t_cons=z.copy(), t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(),
        t_favail=z.copy(), shed=np.zeros(spec.N_ITEMS, np.int32),
        seeds=np.zeros(spec.N_CROPS, np.int32), money=np.int32(money),
        nquad=np.int32(4), price=BASE.astype(np.int32), mkt_inv=inv)


#: wheat, carrot, tomato, strawberry, melon -- a mix with melon in it, so the
#: veto has a subject and the OFF pin has something to hold still.
PMIX = np.array([3, 2, 1, 4, 5], np.int32)


def _pmacro(mix=None):
    base = {
        "plant_target": (PMIX if mix is None else np.asarray(mix, np.int32)).copy(),
        "animal_want": np.zeros(spec.N_ANIMALS, np.int32),
        "land_bias": np.int32(0),
        "hold": np.full(spec.N_PRODUCTS, 10_000, np.int32),
        "press": np.zeros(spec.N_PRODUCTS, np.int32),
        "grow_mult": np.full(spec.N_PRODUCTS, brain.GROW_ONE, np.int32),
        "compact": np.int32(0), "dev_weight": np.int32(brain.GROW_ONE),
        "hire_bias": np.int32(0), "crew_target": np.int32(6),
        "animal_defer": np.int32(0), "forward_days": np.int32(0),
    }
    if "fert_defer" in P.Macro._fields:
        base["fert_defer"] = np.int32(0)
    return P.Macro(**base)


#: Plan boards the OFF pin is taken on: below the hinge, on it, and past it,
#: with the melon book quiet, at the threshold and dead.  OFF every one of them
#: must digest to the shipped tree's plan.
PBOARDS = [(9, 60), (10, 0), (10, 60), (14, 59), (14, 60), (20, 200), (29, 127)]


def _own_digests():
    th = _theta()
    return {f"b{i}": _digest_macro(brain.decide(np, th, o)) for i, o in enumerate(OBS)}


def _own_plan_digests():
    return {f"p{i}": _pin.digest(P.build_day(np, _pview(day, over), _pmacro()))
            for i, (day, over) in enumerate(PBOARDS)}


# =========================================================================
# OFF: the shipped program, byte for byte
# =========================================================================

def test_off_is_the_default():
    assert brain.HERD_RAMP_ON is False


def test_off_decode_is_byte_identical_to_the_shipped_tree():
    #: `b*` only: the `p*` rows are the plan side, owned by the
    #: `MELON_VETO_FLOOD` pin at the foot of this file.
    ref = _pin.tree_digests(__file__)
    assert _own_digests() == {k: v for k, v in ref.items() if k[0] == "b"}


# =========================================================================
# ON: the shift is real, bounded, and only inside the window
# =========================================================================

def _want(day, money=3000, nquad=4, **kw):
    o = _obs(day=day, money=money, nquad=nquad)
    with _On(**kw):
        m = brain.decide(np, _theta(), o)
    return np.asarray(m.animal_want), int(np.asarray(m.plant_target).sum())


def test_on_raises_the_early_animal_want_and_pays_from_the_plant_total():
    off_a, off_p = _want(0)
    on_a, on_p = _want(0, HERD_RAMP_ON=True)
    assert on_a.sum() == off_a.sum() + brain.HERD_RAMP_SHIFT
    assert on_p <= off_p                    # n_dev is unchanged; crops pay
    assert on_a.sum() + on_p <= off_a.sum() + off_p


@pytest.mark.parametrize("day", [0, 3, 9])
def test_the_shift_fires_on_every_day_inside_the_window(day):
    off_a, _ = _want(day)
    on_a, _ = _want(day, HERD_RAMP_ON=True)
    assert on_a.sum() == off_a.sum() + brain.HERD_RAMP_SHIFT


@pytest.mark.parametrize("day", [10, 12, 20, 29])
def test_nothing_moves_outside_the_window(day):
    assert _digest_macro(brain.decide(np, _theta(), _obs(day=day, money=40_000))) == \
        (lambda: (_On(HERD_RAMP_ON=True).__enter__(),
                  _digest_macro(brain.decide(np, _theta(), _obs(day=day, money=40_000))),
                  setattr(brain, "HERD_RAMP_ON", False))[1])()


def test_a_zero_shift_is_the_off_program():
    with _On(HERD_RAMP_ON=True, HERD_RAMP_SHIFT=0):
        assert _own_digests() == {f"b{i}": _digest_macro(brain.decide(np, _theta(), o))
                                  for i, o in enumerate(OBS)}


def test_a_zero_window_is_the_off_program():
    with _On(HERD_RAMP_ON=True, HERD_RAMP_DAYS=0):
        assert _own_digests() == {f"b{i}": _digest_macro(brain.decide(np, _theta(), o))
                                  for i, o in enumerate(OBS)}


def test_the_bump_can_never_exceed_the_free_development():
    """`n_dev` caps it: on a one-quadrant board with nothing free the want
    cannot be pushed past the tiles that exist."""
    kind = np.full(100, spec.KIND_PLANT, np.int32)
    kind[:1] = spec.KIND_EMPTY
    o = brain.PolicyObs(*[getattr(_obs(day=0, nquad=1), f) for f in
                          brain.PolicyObs._fields])
    o = o._replace(kind=kind, occ=np.zeros(100, np.int32))
    with _On(HERD_RAMP_ON=True, HERD_RAMP_SHIFT=40):
        m = brain.decide(np, _theta(), o)
    assert int(np.asarray(m.animal_want).sum()) <= 1
    assert int(np.asarray(m.plant_target).sum()) >= 0


# =========================================================================
# HERD_TILT: the day slope is ONE-SIDED -- nothing before the d12 hinge
# =========================================================================

def test_tilt_off_is_the_default():
    assert brain.HERD_TILT == 0.0


@pytest.mark.parametrize("day", [0, 5, 9, 11, 12])
@pytest.mark.parametrize("tilt", [-1.0, -2.0, +1.0])
def test_the_tilt_is_inert_up_to_the_hinge(day, tilt):
    """`max(0, day - 12)` is zero on every day at or before the hinge, so the
    whole decode there is the shipped one byte for byte -- which is what
    `herdtilt`'s two-sided form got wrong (a negative tilt RAISED the herd
    share on d10-11, `earlyramp` inside the measurement window)."""
    o = _obs(day=day, money=40_000)
    off = _digest_macro(brain.decide(np, _theta(), o))
    with _On(HERD_TILT=tilt):
        assert _digest_macro(brain.decide(np, _theta(), o)) == off


def test_a_negative_tilt_moves_late_turns_off_the_herd():
    off_a, off_p = _want(22, money=40_000)
    on_a, on_p = _want(22, money=40_000, HERD_TILT=-2.0)
    assert on_a.sum() < off_a.sum()         # the herd ask falls
    assert on_p >= off_p                    # and the crop ask is what pays


# =========================================================================
# TURN_COST: the turn-price on the crop mix is hinged at day 10
# =========================================================================

def test_turn_cost_off_is_the_default_and_inert_before_the_hinge():
    """Default 0.0, and below `TURN_COST_DAY` the decode is the shipped one
    byte for byte whatever the value -- d0-9 is `earlyramp`'s window, not
    this gene's."""
    assert brain.TURN_COST == 0.0
    assert len(brain.TURN_COST_TURNS) == spec.N_CROPS
    for day in (0, 5, 9):
        o = _obs(day=day, money=40_000)
        off = _digest_macro(brain.decide(np, _theta(), o))
        for v in (0.15, 0.6, -0.3):
            with _On(TURN_COST=v):
                assert _digest_macro(brain.decide(np, _theta(), o)) == off, (day, v)


def test_a_positive_turn_cost_moves_late_plantings_to_the_cheap_crops():
    """Past the hinge a positive value must shift the plant target toward the
    crops OPSCENSUS measured as cheap to tend (wheat 4.64 / carrot 3.63) and
    away from the expensive tail (strawberry 11.35 / melon 8.73), without
    changing how many tiles are asked for at all."""
    o = _obs(day=14, money=40_000)
    off = np.asarray(brain.decide(np, _theta(), o).plant_target)
    with _On(TURN_COST=0.6):
        on = np.asarray(brain.decide(np, _theta(), o).plant_target)
    cheap = [spec.I_WHEAT, spec.I_CARROT]
    dear = [spec.I_STRAWBERRY, spec.I_MELON, spec.I_TOMATO]
    assert on.sum() == off.sum()                       # the ask is unchanged
    assert on[cheap].sum() > off[cheap].sum()
    assert on[dear].sum() < off[dear].sum()


# =========================================================================
# MELON_VETO_FLOOD: the planting decision is refused while the book is dead
# =========================================================================

def test_melon_veto_off_is_the_default_and_the_plan_is_byte_identical():
    """OFF `_melon_veto` is never called -- the call site is a Python `if` on a
    module global -- so the whole six-array plan digests to the SHIPPED tree's
    on all seven boards, including the flooded ones the switch is cut for.  A
    theta trained before the switch decodes byte for byte."""
    assert P.MELON_VETO_FLOOD_ON is False
    assert (P.MELON_VETO_FLOOD_DAY, P.MELON_VETO_FLOOD_K) == (10, 60)
    ref = _pin.tree_digests(__file__)
    assert _own_plan_digests() == {k: v for k, v in ref.items() if k[0] == "p"}


def test_on_drops_the_melon_ask_only_on_a_flooded_late_book(monkeypatch):
    """ON the melon share of the ask goes to zero -- and nowhere else -- when
    the day is at or past the hinge AND the dawn book stands
    `MELON_VETO_FLOOD_K` over `spec.MARKET_I0`.  Either condition missing and
    the mix is the one the brain chose, to the tile."""
    monkeypatch.setattr(P, "MELON_VETO_FLOOD_ON", True)
    macro = _pmacro()
    assert PMIX.size == spec.N_CROPS and PMIX[spec.I_MELON] > 0

    def out(day, over):
        return np.asarray(
            P._melon_veto(np, _pview(day, over), macro).plant_target)

    fired = out(P.MELON_VETO_FLOOD_DAY, P.MELON_VETO_FLOOD_K)
    assert list(fired) == [0 if c == spec.I_MELON else int(PMIX[c])
                           for c in range(spec.N_CROPS)]
    # A DEVELOPMENT change, not a mix change: the total falls by melon's share
    # and nothing is redistributed (that is the TURNCOST gift this avoids).
    assert int(fired.sum()) == int(PMIX.sum()) - int(PMIX[spec.I_MELON])
    for day, over in ((P.MELON_VETO_FLOOD_DAY - 1, P.MELON_VETO_FLOOD_K),
                      (P.MELON_VETO_FLOOD_DAY, P.MELON_VETO_FLOOD_K - 1),
                      (29, -11)):
        assert list(out(day, over)) == list(PMIX), (day, over)
    # And the veto reaches the plan the day actually runs, not just the Macro:
    # the flooded board's whole six-array plan moves, the quiet one's does not.
    on_hit = _pin.digest(P.build_day(np, _pview(14, 200), macro))
    on_miss = _pin.digest(P.build_day(np, _pview(14, 0), macro))
    monkeypatch.setattr(P, "MELON_VETO_FLOOD_ON", False)
    assert on_hit != _pin.digest(P.build_day(np, _pview(14, 200), macro))
    assert on_miss == _pin.digest(P.build_day(np, _pview(14, 0), macro))


def test_jit_equals_numpy_on_both_arms():
    """The switch is a trace-time `if`, so XLA must schedule the same program
    the numpy backend does -- on BOTH arms."""
    import jax
    import jax.numpy as jnp
    th = _theta()
    for kw in ({}, {"HERD_RAMP_ON": True}):
        with _On(**kw):
            for o in OBS:
                jo = o._replace(**{f: jnp.asarray(getattr(o, f))
                                   for f in o._fields if getattr(o, f) is not None})
                got = jax.jit(lambda t, v: brain.decide(jnp, t, v))(jnp.asarray(th), jo)
                assert _digest_macro([np.asarray(a) for a in got]) == \
                    _digest_macro(brain.decide(np, th, o)), kw


if __name__ == "__main__":                      # the SHIPPED-tree subprocess
    for _n, _d in {**_own_digests(), **_own_plan_digests()}.items():
        print(_n, _d)
