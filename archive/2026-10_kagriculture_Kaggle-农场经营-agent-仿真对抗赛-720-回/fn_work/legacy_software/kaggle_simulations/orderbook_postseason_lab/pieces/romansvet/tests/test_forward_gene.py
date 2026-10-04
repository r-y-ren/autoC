"""The forward-admit horizon gene (`policy.SHAPES`' `g11`/`gb11`, 2026-09-09).

`plan` 1.5 prices every candidate crew against the task set `_derive` emits
**today**, and a field of one-time crops outside their bonus window emits
nothing at all: `spec.CROP_WINDOW_START[I_MELON]` is 6, so the twelve melon
tiles of the recorded top-tier opening are silent through day 5 and the argmax
reads an empty board.  `plan.FORWARD_ADMIT_ON` was the first answer and it
loses as a fixed switch (band6, 72 paired boards, flow135_g350: win 94.4 ->
65.3 %, -9,224 a game) -- a theta's `hire_bias` and crew ramp are already
priced for today-only admission, so a window forced on top of them
double-counts.  What ships instead is a *horizon the theta states*:
`macro.forward_days`, decoded from one global-head logit, zero for every theta
written before the block.

Three groups, the same three every appended block here has to pass:

* the layout -- an append at the tail, nothing before it moved, and a padded
  champion plans byte for byte what the short one planned;
* the decode -- exactly 0 days at zero, monotone, clipped to `[0,
  FWD_DAYS_MAX]`, and a horizon that reaches the melon window buys hands;
* backend agreement -- numpy against JAX with the gene trained off zero, and
  numpy against a *trace*, where the two take structurally different paths
  (`plan._static_horizon`) and must still agree byte for byte.
"""
from __future__ import annotations

import os
import sys

import _pin

# `kagg3` FIRST, out of the tree this process is meant to measure: the
# shared fixtures below do their own `sys.path.insert(0, "src")` and import
# `kagg3` on the way in, so a module that imported one of them first loaded
# THIS tree into a `--digests` subprocess and pinned the tree against itself
# (`tests/_pin.py`).
_pin.bootstrap()

import numpy as np
import pytest
from test_budget_order import _macro
from test_crew_and_herd_mix import _obs
from test_forward_admit import TABLE, _melon_open, _ripe

from kagg3 import spec
from kagg3.core import brain
from kagg3.core import ops as O
from kagg3.core import plan as P
from kagg3.core import policy as PO

#: The layout `g11` appends to -- `gp`'s, i.e. the length of every theta
#: written before 2026-09-09 (`flow135_g350_gp` included). The gene is carried
#: on the fitness-terms tree, so it appends after the global product residual
#: rather than after the crew ramp.
PRE_FWD_N = 6372

CHAMPION = ("/mnt/e/_work/kaggriculture3/artifacts/kagg2_games/thetas/"
            "flow135_g350_gp.npy")

#: Six boards with a day, a purse and a field each: three under the forced
#: melon opening (the case the gene exists for, before / at / past its window)
#: and three with real work on them, so "byte-identical" is a claim about the
#: decode and not about one lucky day.
BOARDS = [(_melon_open(day=1), 1, 3_000),
          (_melon_open(day=3, money=9_000), 3, 9_000),
          (_melon_open(day=6, money=20_000), 6, 20_000),
          (_ripe(), 13, 3_000),
          (_ripe(day=4, money=500), 4, 500),
          (_ripe(day=27, money=120_000), 27, 120_000)]


@pytest.fixture(autouse=True)
def _restore():
    """Every test leaves the module override where it found it."""
    on, days = P.FORWARD_ADMIT_ON, P.FORWARD_ADMIT_DAYS
    yield
    P.FORWARD_ADMIT_ON, P.FORWARD_ADMIT_DAYS = on, days


def _theta(logit=0.0, base=None):
    """A theta whose only forward-admit signal is `gb11`.

    `g11` stays zero, so `fwd = gh @ g11 + gb11` is `logit` whatever the board
    puts in the hidden layer -- which is what makes the horizon assertions
    below statements about the *decode* rather than about one observation.
    """
    th = np.zeros(PO.N_PARAMS, np.float32) if base is None else np.array(base, np.float32)
    th[PO.offset("gb11")] = logit
    return th


def _logit_for(days):
    """The logit whose decode is exactly `days` -- the rounding cell's centre."""
    return float(days) / brain.FWD_DAYS_GAIN


def _horizon(theta, day=1):
    return int(brain.decide(np, np.asarray(theta, np.float32), _obs(day=day)).forward_days)


def _plan(view, macro):
    return [np.asarray(x) for x in P.build_day(np, view, macro, TABLE)]


def _hires(view, macro):
    op, _, qty = P.build_day(np, view, macro, TABLE)[3:6]
    return int(np.asarray(qty)[np.asarray(op) == O.MO_HIRE].sum())


# ------------------------------------------------------------------ layout

def test_the_gene_is_a_clean_append():
    """`g11` starts exactly where the previous layout ended, so `flow135_g350`
    and every theta before it is still a prefix rather than a re-layout."""
    assert PO.N_FWD_OUT == 1
    assert PO.offset("g11") == PRE_FWD_N
    # The block's own end, not `N_PARAMS`: `fv` (the forward-value input) has
    # since been appended past it, and pinning the tail here would fail every
    # later append by construction -- which is the append this layout exists to
    # allow.
    assert PRE_FWD_N + PO.N_HEAD_HID * PO.N_FWD_OUT + PO.N_FWD_OUT == 6405
    assert PO.offset("gb11") + PO.N_FWD_OUT == 6405
    names = [n for n, _ in PO.SHAPES]
    assert names[names.index("gp") + 1:names.index("gp") + 3] == ["g11", "gb11"]
    # Every new coordinate is live: the block feeds an output `brain.decide`
    # reads, so the ES must be able to find it without a flag.
    assert PO.live_mask()[PO.offset("g11"):6405].all()
    # And `--train-only` can name it, which is the whole point of the block
    # being one the trainer can address on its own.
    from kagg3.es.train import train_mask
    m = train_mask("g11,gb11")
    assert m[PO.offset("g11"):6405].all() and not m[:PO.offset("g11")].any()
    assert not m[6405:].any()
    assert train_mask("all-biases")[PO.offset("gb11")] == 1.0


def test_pad_zero_extends_and_keeps_the_prefix():
    rng = np.random.default_rng(1)
    old = rng.normal(0.0, 0.3, PRE_FWD_N).astype(np.float32)
    new = PO.pad(old)
    assert new.shape == (PO.N_PARAMS,)
    assert np.array_equal(new[:PRE_FWD_N], old)
    assert not new[PO.offset("g11"):].any()


# ------------------------------------------------------------------ decode

def test_a_zero_gene_decodes_a_zero_horizon():
    """The inertness assertion: the decode is `round(GAIN * z)` and `round(0)`
    is none of a day, whatever the gain."""
    assert brain.FWD_DAYS_MAX == 6
    # The rounding tie itself, since zero lands exactly on it: `_qfloor(0.5)`
    # must break *down*, or an untrained gene would ship a one-day horizon.
    assert int(brain._qfloor(np, np.float32(brain.FWD_DAYS_GAIN * 0.0 + 0.5))) == 0
    for day in (0, 1, 5, 12, 29):
        m = brain.decide(np, np.zeros(PO.N_PARAMS, np.float32), _obs(day=day))
        assert int(m.forward_days) == 0, day
        assert np.asarray(m.forward_days).dtype == np.int32


@pytest.mark.parametrize("target", [0, 1, 2, 3, 4, 5, 6])
def test_the_logit_that_asks_for_n_days_decodes_n_days(target):
    """`round(FWD_DAYS_GAIN * z)` inverted: the centre of each rounding cell
    is `z == target / FWD_DAYS_GAIN`."""
    if target == 0:
        z = 0.0                                  # the untrained gene itself
    elif target == brain.FWD_DAYS_MAX:
        z = 8.0                                  # far past the clip: 128 -> 6
    else:
        z = _logit_for(target)
    assert _horizon(_theta(z)) == target


def test_the_horizon_is_monotone_and_clipped_to_its_range():
    """Nothing a logit can say puts the scan outside `[0, FWD_DAYS_MAX]`, and
    the sweep never goes backwards -- the ES walks a logit, not a horizon."""
    seen = [_horizon(_theta(float(z))) for z in np.arange(-40.0, 40.1, 0.5)]
    assert min(seen) == 0 and max(seen) == brain.FWD_DAYS_MAX
    assert seen == sorted(seen), "the decode must be monotone in the logit"
    for z in (-100.0, -30.0, 30.0, 100.0):   # saturated, and short of exp's overflow
        assert 0 <= _horizon(_theta(z)) <= brain.FWD_DAYS_MAX


# --------------------------------------------------------- a slope ES feels
#
# A gene the search cannot select on is a dead gene, and "inert at zero" and
# "inert one sigma away from zero" are one line of code apart. The block first
# shipped as `round(6 * sigmoid(z - 4))`, which is both: measured here with the
# live arm's own init and its own noise, **not one** of 512 members decoded a
# single day, at sigma 0.02, 0.03 or 0.05. `FWD_DAYS_GAIN` is the fix and these
# two tests are its bar -- the second one fails if a later edit walks the slope
# back into a flat zone.

INIT = ("/mnt/e/_work/kaggriculture3/artifacts/kagg2_games/thetas/"
        "flow135_g350_gpfwdfv.npy")
TRAJ = "/mnt/e/_work/kaggriculture3/tests/data/trajectory_obs.npz"

#: Population and step of the live ES arm (flow151): 512 antithetic members at
#: an isotropic sigma of 0.02 over all `N_PARAMS` coordinates.
ES_POP, ES_SIGMA = 512, 0.02

#: The band the gain is sized for, as a fraction of members that decode at
#: least one day on a *typical* board: enough of the population differs from
#: the centre for selection to have something to rank, and not so much that the
#: horizon is noise. `>= FWD_DAYS_MAX - 2` is the other side of it -- no member
#: may be thrown to the far end of the range by the step alone.
BAND, FAR_END = (0.15, 0.35), 0.05


def _boards(n, seed=0):
    """`n` real observations off the recorded trajectory, and the per-board
    half of `brain.decide`'s inputs -- which do not depend on theta, so the
    population below pays for them once."""
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
                    reason="needs the padded init theta and the trajectory fixture")
def test_the_arms_init_decodes_no_horizon_on_any_real_board():
    """Zero-init, the way the arm actually meets it: `flow135_g350_gpfwdfv` is
    trained everywhere *except* `g11`/`gb11`, so `z` is the zero block's
    output over a fully trained hidden layer -- and that is still exactly 0.0,
    hence exactly no horizon, on 200 recorded boards."""
    theta = PO.pad(np.load(INIT).astype(np.float32))
    assert theta.shape == (PO.N_PARAMS,), theta.shape
    assert not theta[PO.offset("g11"):PO.offset("gb11") + PO.N_FWD_OUT].any()
    P.FORWARD_ADMIT_ON = False
    obs, _ = _boards(200)
    for o in obs:
        m = brain.decide(np, theta, o)
        assert int(m.forward_days) == 0
        assert np.asarray(m.forward_days).dtype == np.int32


@pytest.mark.skipif(not os.path.isfile(INIT) or not os.path.isfile(TRAJ),
                    reason="needs the padded init theta and the trajectory fixture")
def test_one_es_step_moves_the_horizon_for_a_minority_of_the_population():
    """The measurement the gain is set by, run as an assertion.

    512 isotropic draws at sigma 0.02 off the arm's own init, decoded on eight
    recorded boards. Under `round(6 * sigmoid(z - 4))` this read 0.00 % and the
    gene was invisible to selection; the bar is a *minority*, not a majority --
    the centre must still be the plan most members make.
    """
    theta = PO.pad(np.load(INIT).astype(np.float32))
    _obs_, inputs = _boards(8, seed=3)
    rng = np.random.default_rng(1234)
    pop = (theta[None] + ES_SIGMA * rng.normal(0.0, 1.0, (ES_POP, PO.N_PARAMS))
           ).astype(np.float32)

    days = np.empty((ES_POP, len(inputs)), np.int32)
    for m, member in enumerate(pop):
        params = PO.unpack(np, member)
        for b, args in enumerate(inputs):
            z = PO.forward(np, params, *args).fwd
            days[m, b] = int(np.clip(brain._qfloor(np, brain.FWD_DAYS_GAIN * z + 0.5),
                                     0, brain.FWD_DAYS_MAX))

    per_board = (days >= 1).mean(axis=0)
    lo, hi = BAND
    assert lo <= float(np.median(per_board)) <= hi, per_board
    assert per_board.min() > 0.05, per_board          # no board where it is dead
    far = (days >= brain.FWD_DAYS_MAX - 2).mean()
    assert far <= FAR_END, far
    # ... and the centre itself is unmoved: the population's *mode* is 0.
    assert (days == 0).mean() > 0.5, (days == 0).mean()


# ----------------------------------------------------------------- the gene

def test_a_horizon_that_reaches_the_melon_window_buys_hands(monkeypatch):
    """The gene in the planner, not in the decode: the twelve-melon opening
    emits nothing before age 6, so the crew the day is willing to pay for is a
    function of how far ahead the scan is allowed to look.

    Day 1 needs five days of horizon to see the window (1 + 5 == 6) and day 3
    needs three -- what the scan reads is `age + forward_days`, nothing else.
    """
    # Measure admission before HIRE_ROW_ON removes hands with no work today.
    monkeypatch.setattr(P, "HIRE_ROW_ON", False)
    P.FORWARD_ADMIT_ON = False                    # the gene rules
    for day, days in ((1, 5), (3, 3)):
        view = _melon_open(day=day)
        assert _horizon(_theta(_logit_for(days)), day=day) == days
        off = _hires(view, _macro(forward_days=np.int32(0)))
        on = _hires(view, _macro(forward_days=np.int32(days)))
        assert off == 0, f"day {day}: today's board has no task to hire for"
        assert on > off, f"day {day}: horizon {days} must reach the window"
    # ... and one short of it still reads the empty board it always did.
    assert _hires(_melon_open(day=1), _macro(forward_days=np.int32(4))) == 0


def test_the_module_override_beats_the_gene_and_only_then(monkeypatch):
    """`FORWARD_ADMIT_ON` is a manual A/B lever: ON it pins the horizon at
    `FORWARD_ADMIT_DAYS` whatever the theta says, OFF the theta rules."""
    monkeypatch.setattr(P, "HIRE_ROW_ON", False)
    view = _melon_open(day=1)
    gene5 = _macro(forward_days=np.int32(5))
    gene0 = _macro(forward_days=np.int32(0))

    P.FORWARD_ADMIT_ON = False
    assert _hires(view, gene5) > 0 and _hires(view, gene0) == 0

    P.FORWARD_ADMIT_ON, P.FORWARD_ADMIT_DAYS = True, 5
    assert _hires(view, gene0) == _hires(view, gene5) > 0   # the gene is ignored
    P.FORWARD_ADMIT_DAYS = 0
    assert _hires(view, gene5) == 0                          # ... in both directions


# ---------------------------------------------------------------- identity

@pytest.mark.skipif(not os.path.isfile(CHAMPION), reason="needs flow135_g350")
def test_the_padded_champion_plans_byte_for_byte():
    """`flow135_g350_gp` zero-padded to 6,405 makes the identical plan on six
    boards -- the claim `artifacts/.../flow135_g350_gpfwd.npy` rests on."""
    old = np.load(CHAMPION).astype(np.float32)
    assert old.shape == (PRE_FWD_N,), old.shape
    new = PO.pad(old)
    assert not new[PO.offset("g11"):].any()
    P.FORWARD_ADMIT_ON = False
    for view, day, money in BOARDS:
        obs = _obs(day=day, money=money)
        a, b = brain.decide(np, old, obs), brain.decide(np, new, obs)
        for f, x, y in zip(a._fields, a, b):
            assert np.array_equal(np.asarray(x), np.asarray(y)), f"day {day}: {f}"
        assert int(b.forward_days) == 0
        for i, (x, y) in enumerate(zip(_plan(view, a), _plan(view, b))):
            assert np.array_equal(x, y), f"day {day}: plan[{i}]"


def test_a_zero_horizon_derives_exactly_the_unwidened_prefix():
    """Why the trace may build the projected pass unconditionally: `age + 0 >=
    window` is `age >= window` in integers, so `forward=0` returns `d0` field
    for field rather than something close to it."""
    view, macro = _melon_open(day=1), _macro()
    args = (np, view, macro, TABLE, np.int32(0), np.False_, np.int32(0))
    plain = P._derive(*args)
    zero = P._derive(*args, rev1=plain.rev1, forward=np.int32(0))
    for f, x, y in zip(plain._fields, plain, zero):
        assert np.array_equal(np.asarray(x), np.asarray(y)), f


# ------------------------------------------------------- backend agreement

def test_numpy_matches_jax_on_the_new_output():
    """The trainer runs one backend and the submission the other, and the
    horizon is a `floor` away from a different crew."""
    import jax.numpy as jnp

    rng = np.random.default_rng(21)
    theta = PO.pad(rng.normal(0.0, 0.3, PRE_FWD_N).astype(np.float32))
    # `g11` and `gb11` only -- `fv` is appended past them and is not this
    # test's subject.
    theta[PO.offset("g11"):6405] = rng.normal(0.0, 0.5, PO.N_HEAD_HID + 1)
    theta = theta.astype(np.float32)
    p_np = PO.unpack(np, theta)
    p_jx = PO.unpack(jnp, jnp.asarray(theta))

    worst = 0.0
    for seed in range(6):
        r = np.random.default_rng(300 + seed)
        prod = r.normal(0.0, 1.0, (spec.N_PRODUCTS, PO.N_PROD_FEAT)).astype(np.float32)
        glob = r.normal(0.0, 1.0, PO.N_GLOBAL_FEAT).astype(np.float32)
        drain = r.normal(0.0, 1.0, (spec.N_PRODUCTS, PO.N_DRAIN_FEAT)).astype(np.float32)
        a = PO.forward(np, p_np, prod, glob, drain).fwd
        b = PO.forward(jnp, p_jx, jnp.asarray(prod), jnp.asarray(glob),
                       jnp.asarray(drain)).fwd
        worst = max(worst, abs(float(a) - float(b)))
    assert worst < 1e-4, worst

    # ... and the decoded integer, which is what the planner actually reads.
    for day in (0, 3, 9, 20):
        obs = _obs(day=day)
        jobs = obs._replace(**{f: None if getattr(obs, f) is None else jnp.asarray(getattr(obs, f)) for f in obs._fields})
        assert int(brain.decide(np, theta, obs).forward_days) == \
            int(brain.decide(jnp, jnp.asarray(theta), jobs).forward_days)


def test_numpy_and_a_trace_agree_at_a_zero_horizon():
    """`plan._static_horizon` makes the two backends take structurally
    different paths at a zero horizon -- numpy knows the value and skips the
    projected `_derive`, a trace cannot and builds it -- and the plans they
    produce must still be equal byte for byte."""
    import jax
    import jax.numpy as jnp

    P.FORWARD_ADMIT_ON = False
    jf = jax.jit(lambda v, m: P.build_day(jnp, v, m, jnp.asarray(TABLE)))
    for view, day, _money in BOARDS[:3]:
        macro = _macro(forward_days=np.int32(0))
        jview = view._replace(**{f: jnp.asarray(getattr(view, f)) for f in view._fields})
        jmacro = macro._replace(**{f: jnp.asarray(getattr(macro, f))
                                   for f in macro._fields})
        for i, (x, y) in enumerate(zip(P.build_day(np, view, macro, TABLE),
                                       jf(jview, jmacro))):
            assert np.array_equal(np.asarray(x), np.asarray(y)), f"day {day}: [{i}]"
