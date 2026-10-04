# Training Archetypes & Absolute Eval Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make self-play punish the "2 quadrants, idle hands, no fertilizer" equilibrium by adding generated strategy archetypes to the opponent pool, measure absolute strength inside the training loop, ship the right artifact, and detect trapped genes automatically.

**Architecture:** An archetype is a theta built from ~12 strategy knobs by writing only bias blocks (plus one encoder unit that tilts crop choice by product value), so the decode is constant-ish and readable. The trainer keeps `archetypes` as a separate, never-evicted list alongside the self-play `pool`; `candidates = pool + archetypes + [theta]`. `absolute_eval(theta)` plays fixed seeds against the archetypes and returns mean own coins; the trainer tracks the best theta by that number. A bias-shift sweep per head output flags genes where every nudge is downhill.

**Tech Stack:** Python 3.11, JAX (GPU or `JAX_PLATFORMS=cpu` in tests), numpy, pytest.

**Spec:** This conversation's analysis (2026-08-23) and memory notes `kagg3-vs-kagg2-autopsy.md`, `kagg3-selfplay-blind-spot.md`. **Prerequisite:** `docs/superpowers/plans/2026-08-23-genome-unblock.md` Tasks 1–3 (uses `PO.offset`, the appended `g5`/`gb5` block decoded as `out.aux[0..2]`, and `Macro.fert_buy`). Nothing here touches `head[13..17]` — those are live, noise-carrying parameters in every checkpoint, not spare slots.

## Global Constraints

- Tests: `.venv/bin/python -m pytest`, header `os.environ.setdefault("JAX_PLATFORMS", "cpu"); sys.path.insert(0, "src")`.
- No third-party agents in the pool (memory `no-third-party-agents`): archetypes are thetas for **our own** planner, nothing else.
- Checkpoint format is append-only: new `state.npz` keys must be optional on load (`load_resume` falls back when absent).
- Common random numbers: anything drawn per generation is drawn once and shared by the whole population.
- `Trainer.__init__` compiles the evaluator (~40 s on GPU); tests that construct a `Trainer` use tiny configs (`pop=4, episodes=4, chunk=8`) and run on CPU.

---

### Task 1: Archetype theta builder

**Files:**
- Create: `src/kagg3/es/archetypes.py`
- Test: `tests/test_archetypes.py`

**Interfaces:**
- Produces:
  ```python
  KNOBS = ("hire", "land", "fert_use", "feed", "care", "dev", "animal_share",
           "crop_sharp", "value_tilt", "sell", "gate", "lots", "fert_buy",
           "land_afford", "free_urgency")
  def archetype_theta(**knobs) -> np.ndarray          # float32 [PO.N_PARAMS]
  def sample_archetype(rng: np.random.Generator) -> dict
  def named(name: str) -> dict                        # "expander" | "rusher" | "rancher" | "wheat_farmer"
  ```
  Knob semantics (all floats are pre-activation logits unless noted): `hire` → `head[0]`; `land` → `head[1]`; `fert_use` → `head[2]`; `feed` → `head[3]`; `care` → `head[4]`; `dev` → `head[5]`; `animal_share` → `head[6]`; `crop_sharp` → `head[7]`; `value_tilt` → grow score slope on `log1p(base)` (positive prefers melon/strawberry/wool, negative prefers wheat); `sell` → `b2[1]`; `gate` → `b3[0]`; `lots` → `gb4[0]`; `fert_buy` → `gb5[0]`; `land_afford` → `gb5[1]`; `free_urgency` → `gb5[2]`.

  Decode arithmetic to remember when asserting: every count is `floor(sigmoid(z) * n + 1e-4)`, and `sigmoid(10) = 0.99995`, so a "saturated" knob decodes to `n - 1` whenever `n * 4.5e-5 > 1e-4`, i.e. for any `n >= 3`. `n_hire` is the exception only because it multiplies by `MAX_HANDS + 1` and clips.

- [ ] **Step 1: Write the failing tests**

```python
"""Strategy archetypes are thetas for our own planner whose decode is set by
hand: bias blocks carry the global decisions, one encoder unit tilts crop
choice by product value. They exist so self-play has opponents that expand,
fertilize and dump -- behaviours a single lineage never shows itself."""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, "src")

import numpy as np

from kagg3 import spec
from kagg3.core import brain
from kagg3.core import policy as PO
from kagg3.es import archetypes as A


def _obs(money=20_000, nquad=2, day=12):
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_LOCKED, np.int32)
    kind[spec.TILE_QUAD < nquad] = spec.KIND_EMPTY
    kind[:10] = spec.KIND_PLANT
    occ = np.where(kind == spec.KIND_PLANT, 3, -1).astype(np.int32)
    shed = np.zeros(spec.N_ITEMS, np.int32); shed[:spec.N_PRODUCTS] = 20
    return brain.PolicyObs(
        day=np.int32(day), money=np.int32(money), opp_money=np.int32(money),
        kind=kind, occ=occ, opp_kind=kind.copy(), opp_occ=occ.copy(),
        t_day=z.copy(), t_yield=z.copy(),
        shed=shed, seeds=np.full(spec.N_CROPS, 50, np.int32),
        nquad=np.int32(nquad), opp_nquad=np.int32(nquad),
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        price=np.asarray(brain._BASE, np.int32),
        shops=np.zeros(8, np.int32))


def test_theta_has_the_full_layout():
    th = A.archetype_theta()
    assert th.shape == (PO.N_PARAMS,) and th.dtype == np.float32


def test_expander_buys_land_fertilizes_and_develops():
    m = brain.decide(np, A.archetype_theta(**A.named("expander")), _obs())
    assert int(m.buy_land) == 1
    assert int(m.n_fertilize) == 9             # floor(sigmoid(10) * 10 plants) -- all but one
    assert int(m.fert_buy) == 0                # from own stock only
    assert int(m.plant_target.sum() + m.animal_count) >= 35   # 40 free tiles, dev ~0.9+
    assert int(m.n_hire) == spec.MAX_HANDS     # floor(sigmoid(10) * 11) = 10


def test_value_tilt_prefers_high_value_crops():
    hi = brain.decide(np, A.archetype_theta(value_tilt=+3.0, dev=10.0, animal_share=-10.0), _obs())
    lo = brain.decide(np, A.archetype_theta(value_tilt=-3.0, dev=10.0, animal_share=-10.0), _obs())
    wheat = list(spec.CROPS).index("WHEAT")
    melon = list(spec.CROPS).index("MELON")
    assert hi.plant_target[melon] > hi.plant_target[wheat]
    assert lo.plant_target[wheat] > lo.plant_target[melon]


def test_sell_knob_sets_the_shed_fraction_sold():
    dump = brain.decide(np, A.archetype_theta(sell=10.0), _obs())
    hold = brain.decide(np, A.archetype_theta(sell=-10.0), _obs())
    # floor(sigmoid(10) * 20) = 19 of the 20 units per product
    assert int(dump.sell_qty[:spec.N_PRODUCTS].sum()) == 19 * spec.N_PRODUCTS
    assert int(hold.sell_qty.sum()) == 0


def test_sampled_archetypes_are_diverse_and_valid():
    # At _obs() the affordability ratio is clip(20000/2000 - 1, -1, 4) = 4, so
    # buy_land = land + 4 * land_afford > 0. With land ~ U(-6, 6) and
    # land_afford ~ U(0, 1) each draw lands on the "no" side with p ~ 0.33;
    # over 40 draws the chance of never seeing it is ~1e-7.
    rng = np.random.default_rng(0)
    lands, ferts = set(), set()
    for _ in range(40):
        k = A.sample_archetype(rng)
        assert set(k) == set(A.KNOBS)
        m = brain.decide(np, A.archetype_theta(**k), _obs())
        lands.add(int(m.buy_land))
        ferts.add(int(m.n_fertilize) > 0)
    assert lands == {0, 1}
    assert ferts == {False, True}


def test_every_named_archetype_decodes():
    for name in ("expander", "rusher", "rancher", "wheat_farmer"):
        brain.decide(np, A.archetype_theta(**A.named(name)), _obs())
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/python -m pytest tests/test_archetypes.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'kagg3.es.archetypes'`.

- [ ] **Step 3: Implement `src/kagg3/es/archetypes.py`**

```python
"""Strategy archetypes: hand-set thetas for our own planner.

A single self-play lineage never shows itself the behaviours that beat it
(measured 2026-08-23: the shipped policy never buys a third quadrant, never
fertilizes, and sells melons into the opponent's glut). These thetas put such
opponents in the ladder without any third-party agent: every knob is a bias
on a head output, so the decode is a constant strategy readable from the dict.

The one non-bias knob, `value_tilt`, routes the per-product feature
`log1p(base) / 6` (brain.features, column 2) through encoder unit 0 into the
grow score, so crop choice can lean toward high-value or cheap products.
"""
from __future__ import annotations

import numpy as np

from ..core import policy as PO

KNOBS = ("hire", "land", "fert_use", "feed", "care", "dev", "animal_share",
         "crop_sharp", "value_tilt", "sell", "gate", "lots", "fert_buy",
         "land_afford", "free_urgency")

_HEAD_INDEX = {"hire": 0, "land": 1, "fert_use": 2, "feed": 3, "care": 4,
               "dev": 5, "animal_share": 6, "crop_sharp": 7}
_AUX_INDEX = {"fert_buy": 0, "land_afford": 1, "free_urgency": 2}   # gb5

_VALUE_FEAT = 2          # brain.features prod column: log1p(base) / 6


def archetype_theta(**knobs) -> np.ndarray:
    unknown = set(knobs) - set(KNOBS)
    if unknown:
        raise KeyError(f"unknown archetype knobs: {sorted(unknown)}")
    theta = np.zeros(PO.N_PARAMS, np.float32)
    gb2 = PO.offset("gb2")
    for name, idx in _HEAD_INDEX.items():
        theta[gb2 + idx] = knobs.get(name, 0.0)
    gb5 = PO.offset("gb5")
    for name, idx in _AUX_INDEX.items():
        theta[gb5 + idx] = knobs.get(name, 0.0)
    # crop value tilt: x[:, 2] -> h[0] -> grow score
    w1 = PO.offset("w1")
    w2 = PO.offset("w2")
    theta[w1 + _VALUE_FEAT * PO.N_ENC_HID + 0] = 1.0          # w1[2, 0]
    theta[w2 + 0 * PO.N_ENC_OUT + 0] = 10.0 * knobs.get("value_tilt", 0.0)  # w2[0, 0]
    b2 = PO.offset("b2")
    theta[b2 + 1] = knobs.get("sell", 0.0)                    # sell logit, all products
    theta[PO.offset("b3")] = knobs.get("gate", 0.0)
    theta[PO.offset("gb4")] = knobs.get("lots", 0.0)
    return theta


_NAMED = {
    # buys land whenever it can, fills it, fertilizes from stock, 10 hands
    "expander": dict(hire=10.0, land=10.0, fert_use=10.0, feed=10.0, care=10.0,
                     dev=3.0, animal_share=-1.5, crop_sharp=0.0, value_tilt=1.0,
                     sell=0.0, gate=0.0, lots=0.5, fert_buy=-10.0,
                     land_afford=1.0, free_urgency=3.0),
    # melon/strawberry heavy, dumps everything in one lot
    "rusher": dict(hire=10.0, land=2.0, fert_use=10.0, feed=10.0, care=0.0,
                   dev=10.0, animal_share=-10.0, crop_sharp=3.0, value_tilt=3.0,
                   sell=10.0, gate=0.0, lots=-1.0, fert_buy=-10.0,
                   land_afford=0.5, free_urgency=3.0),
    # animals first, sells wool/milk/fertilizer
    "rancher": dict(hire=10.0, land=1.0, fert_use=-10.0, feed=10.0, care=10.0,
                    dev=3.0, animal_share=2.0, crop_sharp=0.0, value_tilt=0.0,
                    sell=2.0, gate=0.0, lots=1.0, fert_buy=-10.0,
                    land_afford=0.5, free_urgency=2.0),
    # cheap stable crop in bulk
    "wheat_farmer": dict(hire=10.0, land=10.0, fert_use=10.0, feed=10.0, care=0.0,
                         dev=10.0, animal_share=-10.0, crop_sharp=3.0, value_tilt=-3.0,
                         sell=10.0, gate=0.0, lots=1.0, fert_buy=-10.0,
                         land_afford=1.0, free_urgency=3.0),
}


def named(name: str) -> dict:
    return dict(_NAMED[name])


def sample_archetype(rng: np.random.Generator) -> dict:
    """A random strategy: every knob uniform over a range wide enough that
    each binary decision lands on both sides across a handful of draws."""
    # `land` and `land_afford` are sized together: the affordability ratio is
    # clipped to [-1, 4] in brain.decide, so land + 4 * land_afford must be
    # able to go negative often enough that the sampled ladder contains
    # non-expanders too.
    u = lambda lo, hi: float(rng.uniform(lo, hi))
    return dict(
        hire=u(-1.0, 6.0), land=u(-6.0, 6.0), fert_use=u(-4.0, 6.0),
        feed=u(-1.0, 6.0), care=u(-3.0, 6.0), dev=u(-1.0, 6.0),
        animal_share=u(-6.0, 3.0), crop_sharp=u(-2.0, 4.0),
        value_tilt=u(-3.0, 3.0), sell=u(-3.0, 6.0), gate=u(0.0, 1.0),
        lots=u(-1.0, 2.0), fert_buy=u(-6.0, 1.0), land_afford=u(0.0, 1.0),
        free_urgency=u(0.0, 4.0))
```

Verify the `w1`/`w2` flat indexing against `PO.SHAPES`: `w1` is `(N_ENC_IN, N_ENC_HID)` row-major so element `[2, 0]` is at `offset + 2 * N_ENC_HID`; `w2` is `(N_ENC_HID, N_ENC_OUT)` so `[0, 0]` is at `offset + 0`. If `test_value_tilt_prefers_high_value_crops` fails, print `PO.forward(...).scores[:, 0]` for both tilts and confirm the slope sign before touching the constants.

- [ ] **Step 4: Run tests**

Run: `.venv/bin/python -m pytest tests/test_archetypes.py -v`
Expected: PASS. The floored-count assertions (`n_fertilize == 9`, `19 * N_PRODUCTS`, `n_hire == 10`) are exact consequences of `_qfloor`; if one is off by one, the decode changed — do not "fix" the test without reading `brain.decide`.

- [ ] **Step 5: Commit**

```bash
git add src/kagg3/es/archetypes.py tests/test_archetypes.py
git commit -m "Add hand-set strategy archetypes as thetas for the planner"
```

---

### Task 2: Archetypes in the opponent ladder

**Files:**
- Modify: `src/kagg3/es/train.py:60-77` (Config), `:196-212` (init), `:308-310` (candidates), `:384-398` (`_snapshot` unchanged — archetypes are not in `pool`)
- Modify: `scripts/train.py:47-99` (`load_resume`, `save_state`)
- Test: `tests/test_archetype_ladder.py`

**Interfaces:**
- Consumes: `archetypes.named`, `archetypes.sample_archetype`, `archetypes.archetype_theta`.
- Produces: `Config.n_archetypes: int = 4` (named four first, then sampled); `Trainer.archetypes: list[jnp.ndarray]`; `Trainer.candidates() -> list[jnp.ndarray]` (`pool + archetypes + [theta]`); `state.npz` key `archetypes` (float32 `[k, N_PARAMS]`).

- [ ] **Step 1: Write the failing tests**

```python
"""Archetypes sit beside the self-play pool: faced every generation like a
rung, never evicted, never snapshotted over."""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, "src")

import numpy as np

from kagg3.es.train import Config, Trainer
from kagg3.es import archetypes as A


def _tiny(**kw):
    return Config(pop=4, episodes=4, chunk=8, **kw)


def test_default_archetypes_are_the_four_named_ones():
    tr = Trainer(_tiny(n_archetypes=4), seed=0)
    assert len(tr.archetypes) == 4
    for th, name in zip(tr.archetypes, ("expander", "rusher", "rancher", "wheat_farmer")):
        assert np.array_equal(np.asarray(th), A.archetype_theta(**A.named(name)))


def test_extra_archetypes_are_sampled_deterministically_from_the_seed():
    a = Trainer(_tiny(n_archetypes=6), seed=3).archetypes
    b = Trainer(_tiny(n_archetypes=6), seed=3).archetypes
    assert len(a) == 6
    assert all(np.array_equal(np.asarray(x), np.asarray(y)) for x, y in zip(a, b))


def test_candidates_are_pool_then_archetypes_then_theta():
    tr = Trainer(_tiny(n_archetypes=2), seed=0)
    c = tr.candidates()
    assert len(c) == len(tr.pool) + 2 + 1
    assert np.array_equal(np.asarray(c[-1]), np.asarray(tr.theta))


def test_zero_archetypes_is_the_old_ladder():
    tr = Trainer(_tiny(n_archetypes=0), seed=0)
    assert tr.archetypes == []
    assert len(tr.candidates()) == len(tr.pool) + 1
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/python -m pytest tests/test_archetype_ladder.py -v`
Expected: FAIL — `TypeError: Config.__new__() got an unexpected keyword argument 'n_archetypes'`.

- [ ] **Step 3: Implement in `src/kagg3/es/train.py`**

Add to `Config` after `warm_money_max`:

```python
    n_archetypes: int = 4       # hand-set strategy opponents kept beside the pool
```

Add the import near the other `..` imports:

```python
from . import archetypes as AR
```

In `Trainer.__init__`, after `self.pool = [self.theta]`:

```python
        # Strategy archetypes: never evicted, never snapshotted, faced every
        # generation like a rung. A single lineage never shows itself the
        # behaviours that beat it; these do. The first four are the named
        # ones, the rest are sampled from the same seed as everything else.
        names = ("expander", "rusher", "rancher", "wheat_farmer")
        self.archetypes = []
        for i in range(cfg.n_archetypes):
            knobs = AR.named(names[i]) if i < len(names) else AR.sample_archetype(rng)
            self.archetypes.append(jnp.asarray(AR.archetype_theta(**knobs)))
```

Add the method after `draw_starts`:

```python
    def candidates(self):
        """Every opponent faced this generation, in round-robin order."""
        return self.pool + self.archetypes + [self.theta]
```

In `generation`, replace `candidates = self.pool + [self.theta]` with `candidates = self.candidates()`.

- [ ] **Step 4: Persist them in `scripts/train.py`**

In `save_state`, add `archetypes=np.asarray(jnp.stack(tr.archetypes)) if tr.archetypes else np.zeros((0, tr.n), np.float32),` to the `np.savez(...)` call.

In `load_resume`, inside the `if os.path.isfile(npz):` branch after the pool is restored, add:

```python
        if "archetypes" in d and d["archetypes"].shape[0] > 0:
            tr.archetypes = [jnp.asarray(a) for a in d["archetypes"]]
```

(Older checkpoints keep the archetypes `__init__` built — that is the intended fallback.)

Note: for `n_archetypes > 4` the sampler consumes draws from `rng` before `self.rng = rng`, so every later draw (episode seeds, warm starts) shifts relative to a run without archetypes. Intended; mention it in the commit body so nobody hunts for a lost bit-for-bit resume.

- [ ] **Step 5: Run tests**

Run: `.venv/bin/python -m pytest tests/test_archetype_ladder.py tests/test_warm_start.py tests/test_shard_chunking.py -v`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/kagg3/es/train.py scripts/train.py tests/test_archetype_ladder.py
git commit -m "Face strategy archetypes every generation beside the self-play pool"
```

---

### Task 3: Absolute strength inside the loop

**Files:**
- Modify: `src/kagg3/es/train.py` (Config, `__init__`, new method, `generation`)
- Test: `tests/test_absolute_eval.py`

**Interfaces:**
- Produces: `Config.abs_every: int = 50`, `Config.abs_pairs: int = 32`; `Trainer.absolute_eval(theta) -> tuple[float, float]` (mean own coins, win rate) against `archetypes` on fixed seeds, both seats, cold start; `Trainer.best_abs: float`, `Trainer.best_abs_theta`, `Trainer.abs_history: list[(gen, coins, win)]`; `generation()` now returns `(mean_win, best_win, abs_coins_or_None)`.

- [ ] **Step 1: Write the failing tests**

```python
"""`mean_win` and `champ` are ladder-relative and sit near 0.5 by construction.
This is the number that says whether the policy is getting *better*: coins
against a fixed set of opponents on fixed seeds."""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, "src")

import numpy as np

from kagg3.es.train import Config, Trainer


def _tiny(**kw):
    return Config(pop=4, episodes=4, chunk=8, abs_pairs=2, **kw)


def test_absolute_eval_is_deterministic_for_a_theta():
    tr = Trainer(_tiny(n_archetypes=2), seed=0)
    a = tr.absolute_eval(tr.theta)
    b = tr.absolute_eval(tr.theta)
    assert a == b
    assert isinstance(a[0], float) and 0.0 <= a[1] <= 1.0


def test_absolute_eval_needs_archetypes():
    tr = Trainer(_tiny(n_archetypes=0), seed=0)
    coins, win = tr.absolute_eval(tr.theta)
    assert coins == 0.0 and win == 0.0


def test_generation_measures_on_schedule_and_tracks_the_best():
    tr = Trainer(_tiny(n_archetypes=2, abs_every=2), seed=0)
    r1 = tr.generation()
    assert r1[2] is None
    r2 = tr.generation()
    assert isinstance(r2[2], float)
    assert tr.abs_history and tr.abs_history[-1][0] == tr.t
    assert tr.best_abs == r2[2]
    assert np.asarray(tr.best_abs_theta).shape == np.asarray(tr.theta).shape
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/python -m pytest tests/test_absolute_eval.py -v`
Expected: FAIL — `unexpected keyword argument 'abs_pairs'`.

- [ ] **Step 3: Implement**

`Config` additions:

```python
    abs_every: int = 50         # generations between absolute-strength measurements
    abs_pairs: int = 32         # fixed seed pairs the measurement plays (x2 seats)
```

In `Trainer.__init__`, after the archetypes block:

```python
        # Fixed seeds for the absolute measurement: the same games every time,
        # so two checkpoints' numbers are comparable.
        abs_seeds = np.random.default_rng(20260823).integers(0, 2 ** 31 - 1, cfg.abs_pairs)
        self.abs_words = jnp.asarray(host_words(abs_seeds))
        self.best_abs = -1.0
        self.best_abs_theta = self.theta
        self.abs_history = []
```

New method after `_versus_pool`:

```python
    def absolute_eval(self, theta):
        """(mean own coins, win rate) vs the archetypes on fixed seeds, both seats.

        Cold start, default market: the number means the same thing in every
        run. Without archetypes there is nothing fixed to measure against.
        """
        if not self.archetypes:
            return 0.0, 0.0
        arch = self.archetypes
        n_pairs = int(self.abs_words.shape[0])
        total = 2 * n_pairs * len(arch)
        k = np.arange(total)
        a_idx = k % len(arch)
        seat = ((k // len(arch)) % 2).astype(np.int32)
        widx = k // (2 * len(arch))
        nq, mo = cold_starts(total)
        money = np.asarray(self.evaluate(
            self.tables,
            jnp.broadcast_to(theta, (total, theta.shape[0])),
            jnp.stack([arch[i] for i in a_idx]),
            self.abs_words[jnp.asarray(widx)],
            jnp.asarray(seat), jnp.asarray(nq), jnp.asarray(mo)))
        win = float(np.asarray(win_scores(money[:, 0], money[:, 1])).mean())
        return float(money[:, 0].mean()), win
```

Check how `self.evaluate` is called in `_versus_pool` (`train.py:359-376`) — it may go through a chunked/sharded wrapper rather than the raw jit; use the same call path (copy the exact call, including any `_chunked` helper) so shapes and sharding match.

In `generation`, before the final `return`:

```python
        abs_coins = None
        if self.t % cfg.abs_every == 0:
            abs_coins, abs_win = self.absolute_eval(self.theta)
            self.abs_history.append((self.t, abs_coins, abs_win))
            if abs_coins > self.best_abs:
                self.best_abs, self.best_abs_theta = abs_coins, self.theta
        return float(win.mean()), float(win.max()), abs_coins
```

Confirm where `self.t` is incremented inside `generation` so the `% abs_every` check fires on the generation count the caller sees (the test expects the second call to measure with `abs_every=2`).

Update every caller of `generation()` that unpacks two values: `scripts/train.py:160` (`mean, best = tr.generation()` → `mean, best, abs_coins = tr.generation()`). `tests/test_fitness_shaping.py:111` discards the return and needs no change; confirm with `grep -rn "generation()" tests scripts`.

- [ ] **Step 4: Run tests**

Run: `.venv/bin/python -m pytest tests/test_absolute_eval.py tests/test_archetype_ladder.py tests/test_fitness_shaping.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/kagg3/es/train.py tests/test_absolute_eval.py scripts/train.py
git commit -m "Measure absolute strength against the archetypes inside the loop"
```

---

### Task 4: Log, checkpoint and promote the right artifact

`--promote` writes the pool champion (`scripts/train.py:175`), which is measured ~7k coins worse than the ES mean. Ship the ES mean; also save the best-by-absolute theta.

**Files:**
- Modify: `scripts/train.py:150-180`, `save_state`, `load_resume`
- Test: manual 3-generation smoke run (script has no unit tests).

- [ ] **Step 1: Log and save**

In the loop body, extend `rec` with `"abs": abs_coins, "best_abs": round(tr.best_abs, 1)` and the print line with `abs {abs_coins if abs_coins is not None else '-'}`.

In the checkpoint block, add `save_atomic(os.path.join(out, "best_abs.npy"), np.asarray(tr.best_abs_theta))`, and change the promote line to:

```python
            if args.promote:
                # Ship the ES mean. The pool champion is selected by ladder
                # noise and measured ~7k coins worse (memory: submission-packaging).
                save_atomic(os.path.join("artifacts", "theta.npy"), np.asarray(tr.theta))
```

In `save_state`, add `best_abs=np.float64(tr.best_abs), best_abs_theta=np.asarray(tr.best_abs_theta),`. In `load_resume`'s npz branch, restore both when present:

```python
        if "best_abs_theta" in d:
            tr.best_abs = float(d["best_abs"]); tr.best_abs_theta = jnp.asarray(d["best_abs_theta"])
```

Add CLI flags mirrored into `Config`: `--n-archetypes` (default 4), `--abs-every` (default 50).

- [ ] **Step 2: Smoke run**

Run: `JAX_PLATFORMS=cpu .venv/bin/python scripts/train.py --gens 3 --pop 4 --episodes 4 --chunk 8 --abs-every 1 --run smoke_arch --ckpt-every 1`
Expected: three lines printed with `abs <number>`, files `artifacts/smoke_arch/{theta,champion,pool,best_abs}.npy` and `state.npz` present, `log.jsonl` rows contain `"abs"`. Then: `JAX_PLATFORMS=cpu .venv/bin/python scripts/train.py --gens 1 --pop 4 --episodes 4 --chunk 8 --resume artifacts/smoke_arch --run smoke_arch2` — Expected: resumes at gen 3 without error. Delete both smoke dirs afterwards (`rm -r artifacts/smoke_arch artifacts/smoke_arch2`).

- [ ] **Step 3: Commit**

```bash
git add scripts/train.py
git commit -m "Log absolute strength, checkpoint the best-by-absolute theta, promote the ES mean"
```

---

### Task 5: Trapped-gene sweep

A gene is *trapped* when every nudge of its bias is worse than leaving it — the counterfactual I ran by hand (fertilize, land). Automate it: shift one bias by ±δ, measure `absolute_eval`, report. Gene index `g` spans both bias blocks: `0..17` → `gb2[g]`, `18..20` → `gb5[g - 18]` (`fert_buy`, `land_afford`, `free_urgency`).

**Files:**
- Create: `src/kagg3/es/sweep.py`, `scripts/gene_sweep.py`
- Test: `tests/test_gene_sweep.py`

**Interfaces:**
- Produces:
  ```python
  DELTAS = (-3.0, -1.0, -0.3, 0.3, 1.0, 3.0)
  N_GENES = PO.N_HEAD_OUT + PO.N_AUX_OUT                      # 21
  def gene_offset(g: int) -> int                              # flat theta index of the bias
  def shifted(theta: np.ndarray, g: int, delta: float) -> np.ndarray
  def classify(base: float, scores: dict[float, float], tol: float) -> str   # "trapped" | "uphill+" | "uphill-" | "flat"
  def sweep(tr, theta, genes, deltas=DELTAS, tol=500.0) -> list[dict]
  ```

- [ ] **Step 1: Write the failing tests**

```python
"""A gene every nudge of which is worse is coupled to something the planner
hides; find those automatically instead of by hand-forcing heads."""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, "src")

import numpy as np

from kagg3.core import policy as PO
from kagg3.es import sweep as S


def test_shifted_moves_exactly_one_bias():
    th = np.zeros(PO.N_PARAMS, np.float32)
    out = S.shifted(th, 2, 1.5)
    assert out[PO.offset("gb2") + 2] == 1.5
    assert np.count_nonzero(out) == 1
    assert np.count_nonzero(th) == 0            # input untouched


def test_genes_past_the_head_land_in_gb5():
    th = np.zeros(PO.N_PARAMS, np.float32)
    out = S.shifted(th, PO.N_HEAD_OUT + 1, -2.0)     # land_afford
    assert out[PO.offset("gb5") + 1] == -2.0
    assert np.count_nonzero(out) == 1
    assert S.N_GENES == PO.N_HEAD_OUT + PO.N_AUX_OUT


def test_classify():
    base = 50_000.0
    assert S.classify(base, {-1.0: 45_000, 1.0: 44_000}, tol=500) == "trapped"
    assert S.classify(base, {-1.0: 45_000, 1.0: 56_000}, tol=500) == "uphill+"
    assert S.classify(base, {-1.0: 57_000, 1.0: 44_000}, tol=500) == "uphill-"
    assert S.classify(base, {-1.0: 50_200, 1.0: 49_900}, tol=500) == "flat"


def test_sweep_reports_one_row_per_head_index():
    from kagg3.es.train import Config, Trainer
    tr = Trainer(Config(pop=4, episodes=4, chunk=8, abs_pairs=2, n_archetypes=2), seed=0)
    rows = S.sweep(tr, np.asarray(tr.theta), [1, 2], deltas=(-1.0, 1.0))
    assert [r["gene"] for r in rows] == [1, 2]
    assert set(rows[0]) >= {"gene", "base", "scores", "verdict"}
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/python -m pytest tests/test_gene_sweep.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'kagg3.es.sweep'`.

- [ ] **Step 3: Implement `src/kagg3/es/sweep.py`**

```python
"""Trapped-gene detection by head-bias shifts.

Shifting a bias by delta moves that output by delta in every state, so it
is the cleanest single-gene counterfactual that stays a plain theta. A gene
whose every shift scores below the base is "trapped": its payoff is coupled
to another decision the planner makes for it (fertilize -> market buy was
the 2026-08-23 case).

Genes 0..17 are the head biases `gb2`; 18..20 are the unblock block `gb5`.
"""
from __future__ import annotations

import numpy as np

from ..core import policy as PO

DELTAS = (-3.0, -1.0, -0.3, 0.3, 1.0, 3.0)
N_GENES = PO.N_HEAD_OUT + PO.N_AUX_OUT


def gene_offset(g):
    if g < PO.N_HEAD_OUT:
        return PO.offset("gb2") + g
    if g < N_GENES:
        return PO.offset("gb5") + (g - PO.N_HEAD_OUT)
    raise IndexError(g)


def shifted(theta, g, delta):
    out = np.array(theta, np.float32, copy=True)
    out[gene_offset(g)] += delta
    return out


def classify(base, scores, tol):
    up_pos = any(s > base + tol for d, s in scores.items() if d > 0)
    up_neg = any(s > base + tol for d, s in scores.items() if d < 0)
    all_down = all(s < base - tol for s in scores.values())
    if all_down:
        return "trapped"
    if up_pos and not up_neg:
        return "uphill+"
    if up_neg and not up_pos:
        return "uphill-"
    return "flat"


def sweep(tr, theta, genes, deltas=DELTAS, tol=500.0):
    base, _ = tr.absolute_eval(np.asarray(theta))
    rows = []
    for g in genes:
        scores = {float(d): tr.absolute_eval(shifted(theta, g, d))[0] for d in deltas}
        rows.append({"gene": int(g), "base": base, "scores": scores,
                     "verdict": classify(base, scores, tol)})
    return rows
```

`tr.absolute_eval` takes a JAX or numpy array; `Trainer.absolute_eval` calls `jnp.broadcast_to(theta, ...)`, which accepts numpy. If it does not, wrap with `jnp.asarray` inside `sweep`.

- [ ] **Step 4: Implement `scripts/gene_sweep.py`**

```python
"""Which head genes are trapped? Usage:

    python scripts/gene_sweep.py artifacts/run/theta.npy [--genes 0-20] [--abs-pairs 32]

Genes 0..17 are head biases (gb2), 18..20 the unblock block (gb5).
"""
import argparse, sys
sys.path.insert(0, "src")
import numpy as np

from kagg3.es.train import Config, Trainer
from kagg3.es import sweep as S

GENE_NAMES = {0: "hire", 1: "land", 2: "fertilize", 3: "feed", 4: "care", 5: "dev",
              6: "animal_share", 7: "crop_sharp", 8: "ord_wheat", 9: "ord_fert",
              10: "ord_seeds", 11: "ord_animal", 12: "ord_land",
              # head[13..17] feed nothing in decide but are live, trained
              # parameters; sweeping them is a null-effect sanity row.
              13: "head13(unused)", 14: "head14(unused)", 15: "head15(unused)",
              16: "head16(unused)", 17: "head17(unused)",
              18: "fert_buy", 19: "land_afford", 20: "free_urgency"}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("theta")
    ap.add_argument("--genes", default="0-20")
    ap.add_argument("--abs-pairs", type=int, default=32)
    ap.add_argument("--n-archetypes", type=int, default=4)
    ap.add_argument("--chunk", type=int, default=1024)
    args = ap.parse_args()
    lo, hi = (int(x) for x in args.genes.split("-"))
    theta = np.load(args.theta).astype(np.float32)
    tr = Trainer(Config(pop=2, episodes=2, chunk=args.chunk, abs_pairs=args.abs_pairs,
                        n_archetypes=args.n_archetypes), seed=0)
    rows = S.sweep(tr, theta, range(lo, hi + 1))
    print(f"base {rows[0]['base']:,.0f} coins vs {len(tr.archetypes)} archetypes x {args.abs_pairs} pairs x 2 seats")
    print(f"{'gene':>4} {'name':16} {'verdict':9} " + " ".join(f"{d:>7}" for d in S.DELTAS))
    for r in rows:
        print(f"{r['gene']:>4} {GENE_NAMES[r['gene']]:16} {r['verdict']:9} "
              + " ".join(f"{r['scores'][d] - r['base']:>+7.0f}" for d in S.DELTAS))
```

- [ ] **Step 5: Run tests and the script on the shipped theta**

Run: `.venv/bin/python -m pytest tests/test_gene_sweep.py -v` — Expected: PASS.

Run (GPU host, or CPU with `--abs-pairs 4`): `.venv/bin/python scripts/gene_sweep.py <shipped theta.npy> --genes 0-20`
Expected: a table; with the genome plan applied, genes 2 (fertilize) and 1 (land) should read `uphill+` rather than `trapped`, and genes 13–17 should read `flat` with every delta at exactly `+0` (they feed nothing in `decide`; a non-zero entry there means a decode path reads them and the genome plan's "no `head[13..17]`" rule was broken). Record the table in the commit message body.

- [ ] **Step 6: Commit**

```bash
git add src/kagg3/es/sweep.py scripts/gene_sweep.py tests/test_gene_sweep.py
git commit -m "Detect trapped genes by sweeping head biases against the absolute eval"
```

---

### Task 6: Retrain and measure

**Files:** none (run + record).

- [ ] **Step 1: Launch on the GPU host**

`python scripts/train.py --pop 128 --episodes 256 --chunk 2048 --n-archetypes 6 --abs-every 50 --warm-frac 0.0 --run arch1` (warm starts off: empty-land warm starts teach the wrong lesson; the archetypes supply multi-quadrant pressure instead).

- [ ] **Step 2: Gate at gen 1,000**

Compare `log.jsonl` `abs` at gen 50 vs gen 1,000. Expected: rising. Run `scripts/gene_sweep.py artifacts/arch1/theta.npy` — genes 1, 2, 19, 20 (land, fertilize, land_afford, free_urgency) should be `flat` or `uphill±`, none `trapped`. If `abs` is flat for 500 gens, stop and run the sweep before spending more GPU time.

- [ ] **Step 3: Real-engine check at gen 2,000**

`.venv/bin/python scripts/eval_vs_baselines.py --theta artifacts/arch1/best_abs.npy --games 12 --opponents /mnt/e/_work/kaggriculture2/main.py` and the same for `theta.npy`. Record both against the 50k baseline from the genome plan in memory (`kagg3-status.md`). Ship whichever is higher via `scripts/package_submission.py` — and verify the packaged theta's md5 matches the file you chose.
