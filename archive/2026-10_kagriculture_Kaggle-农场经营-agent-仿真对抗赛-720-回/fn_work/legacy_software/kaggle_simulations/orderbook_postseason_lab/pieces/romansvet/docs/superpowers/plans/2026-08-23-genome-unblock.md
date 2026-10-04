# Genome Unblock Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the four winning behaviours (fertilize from own stock, buy land when affordable, fill new land, don't plant what can't mature) reachable by single-gene ES steps, without invalidating any existing theta.

**Architecture:** All changes are in the per-day decode (`brain.decide`) and the budget walk (`plan.build_day`). Every new gene lives in a **new appended parameter block** `g5`/`gb5` (32 → 3, decoded as `out.aux[0..2]`), exactly like the sell head's `g4`/`gb4`: a theta trained before it is a prefix of the new layout, unpacks zero-padded, and decodes to the *old* behaviour. One hard engine rule (no late planting) goes into the decode, not a gene.

> **Why not `head[13..17]`?** Those five outputs are *not* free slots. `N_PARAMS_LEGACY` covers the full `g2 (32×18)` / `gb2 (18)`, so they have been perturbed and Adam-diffused since gen 0. Measured 2026-08-23 on `artifacts/theta.npy`: `gb2[13:18] = [-0.62, -0.33, 0.39, 0.15, 1.31]`, `|g2[:, 13:18]|` column norms 3.2–3.6 (same as the used columns). Gating a new gene on them would bolt random trained noise onto every existing checkpoint.

**Tech Stack:** Python 3.11, numpy + JAX (`xp`-generic code — every new expression must work under both backends, no Python branching on array values), pytest.

**Spec:** This conversation's analysis (2026-08-23 trace of shipped theta vs kagg2 and the forced-gene counterfactual); the memory note `kagg3-vs-kagg2-autopsy.md`.

## Global Constraints

- Run tests with `.venv/bin/python -m pytest` from repo root (`sys.path.insert(0, "src")` is in every test header; copy it).
- All planner/decode code is `xp`-generic: use `xp.where`, never `if` on array values. Both backends must decode an identical `Macro` (`tests/test_gates.py` enforces this).
- Theta layout is append-only: new parameters go in a new block **at the end of `PO.SHAPES`**, never inside an existing one, and never in `head[13..17]` (see Architecture). `plan.ORDER_HEAD0 = 8`; order uses `head[8..12]`.
- A pre-`g5` theta (any current checkpoint, and `PO.init_theta(rng)[:PO.N_PARAMS_LEGACY]`) must decode to the same `Macro` fields it did before, except where a task explicitly says otherwise. The new block is zero for all of them, so every new term must be exactly inert at zero.
- Commit after every task with the message given; never commit `artifacts/`.

---

### Task 1: Separate fertilizer *use* from fertilizer *buy*

Today `plan.py:314` turns any `n_fertilize` above shed stock into a market purchase (`fert_short`). That makes raising the fertilize gene strictly downhill (measured: 50k → 32k coins). After this task the planner fertilizes only from stock unless a new `fert_buy` gene is on.

**Files:**
- Modify: `src/kagg3/core/plan.py:136-153` (Macro), `src/kagg3/core/plan.py:314` (`fert_short`)
- Modify: `src/kagg3/core/policy.py` (`SHAPES`, `Params`, `Outputs`, `forward`, new `offset`)
- Modify: `src/kagg3/core/brain.py:241-245` (decode), `src/kagg3/core/brain.py:290-300` (Macro construction)
- Modify: `tests/test_budget_order.py:45-57`, `tests/test_sell_head.py:45-57`, `tests/test_task_priority.py:45-57` (`_macro` helpers gain `fert_buy`)
- Test: `tests/test_fert_source.py`

**Interfaces:**
- Produces: `PO.N_AUX_OUT = 3`, blocks `g5 (N_HEAD_HID, 3)` / `gb5 (3,)` appended to `SHAPES`, `Outputs.aux: [3]` (= `gh @ g5 + gb5`), `PO.offset(name)`; `Macro.fert_buy: int32 0/1` (new field, appended after `sell_lots`). `brain.decide` sets `fert_buy = (out.aux[0] > 0)`.

- [ ] **Step 1: Write the failing tests**

```python
"""Fertilizer is a by-product of animals (one per animal per night). Using it
on watered plants doubles yield growth; the only reason the shipped policy
never does is that `n_fertilize` above shed stock used to be *bought* at
market price, so every step up the fertilize gene cost more than it earned.
`fert_buy` separates the two decisions."""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, "src")

import numpy as np

from kagg3 import spec
from kagg3.core import brain
from kagg3.core import ops as O
from kagg3.core import plan as P
from kagg3.core import policy as PO


def _view(money, fert_in_shed, n_plants=10):
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    kind[:n_plants] = spec.KIND_PLANT
    occ[:n_plants] = spec.I_STRAWBERRY if hasattr(spec, "I_STRAWBERRY") else 3
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_FERT] = fert_in_shed
    return P.DayView(
        day=np.int32(5), kind=kind, occ=occ,
        t_day=z.copy(), t_water=z.copy(), t_cons=z.copy(), t_yield=z.copy(),
        t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=shed, seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(money), nquad=np.int32(1),
        price=np.full(spec.N_PRODUCTS, 25, np.int32))


def _macro(**kw):
    base = dict(
        sell_qty=np.zeros(spec.N_PRODUCTS, np.int32),
        plant_target=np.zeros(spec.N_CROPS, np.int32),
        animal_kind=np.int32(0), animal_count=np.int32(0), n_hire=np.int32(0),
        buy_land=np.int32(0), n_fertilize=np.int32(0),
        feed_daily=np.int32(0), care_on=np.int32(0),
        order=np.asarray(P.DEFAULT_ORDER, np.int32),
        prio=np.zeros(P.N_PRIO, np.int32),
        sell_min=np.zeros(spec.N_PRODUCTS, np.int32), sell_lots=np.int32(1),
        fert_buy=np.int32(0))
    base.update(kw)
    return P.Macro(**base)


def _fert_bought(view, macro):
    op, arg, qty = P.build_day(np, view, macro)[3:6]
    mask = (op[O.TURN_BUY] == O.MO_BUY_PRODUCT) & (arg[O.TURN_BUY] == spec.I_FERT)
    return int(qty[O.TURN_BUY][mask].sum())


def test_fertilize_above_stock_buys_nothing_when_fert_buy_is_off():
    view = _view(money=5000, fert_in_shed=2)
    assert _fert_bought(view, _macro(n_fertilize=np.int32(8))) == 0


def test_fertilize_above_stock_buys_the_shortfall_when_fert_buy_is_on():
    view = _view(money=5000, fert_in_shed=2)
    m = _macro(n_fertilize=np.int32(8), fert_buy=np.int32(1))
    assert _fert_bought(view, m) == 6


def test_fert_buy_decodes_from_aux_0():
    theta = PO.init_theta(np.random.default_rng(0))
    obs = _obs()
    theta_off = theta.copy()
    theta_on = theta.copy()
    gb5 = PO.offset("gb5")
    theta_off[gb5 + 0] = -10.0
    theta_on[gb5 + 0] = +10.0
    assert int(brain.decide(np, theta_off, obs).fert_buy) == 0
    assert int(brain.decide(np, theta_on, obs).fert_buy) == 1


def test_pre_g5_thetas_have_fert_buy_off():
    # Both the 3,892 and the 4,287 layouts are prefixes; the aux block is zero.
    rng = np.random.default_rng(1)
    full = PO.init_theta(rng)
    n_pre_g5 = PO.offset("g5")
    for theta in (full[:PO.N_PARAMS_LEGACY], full[:n_pre_g5]):
        assert int(brain.decide(np, theta, _obs()).fert_buy) == 0


def test_g5_block_is_the_last_and_zero_padding_is_inert():
    assert [n for n, _ in PO.SHAPES[-2:]] == ["g5", "gb5"]
    theta = PO.init_theta(np.random.default_rng(2))
    theta[PO.offset("g5"):] = 0.0
    np.testing.assert_array_equal(
        np.asarray(PO.forward(np, PO.unpack(np, theta), *brain.features(np, _obs())).aux),
        np.zeros(PO.N_AUX_OUT, np.float32))


def _obs():
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_LOCKED, np.int32)
    kind[spec.TILE_QUAD == 0] = spec.KIND_EMPTY
    shed = np.zeros(spec.N_ITEMS, np.int32); shed[:spec.N_PRODUCTS] = 5
    return brain.PolicyObs(
        day=np.int32(2), money=np.int32(800), opp_money=np.int32(800),
        kind=kind, occ=z - 1, opp_kind=kind.copy(), opp_occ=z - 1,
        t_day=z.copy(), t_yield=z.copy(),
        shed=shed, seeds=np.zeros(spec.N_CROPS, np.int32),
        nquad=np.int32(1), opp_nquad=np.int32(1),
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        price=np.full(spec.N_PRODUCTS, 25, np.int32),
        shops=np.zeros(8, np.int32))
```

Note: check `src/kagg3/spec.py` for the strawberry crop index constant; if there is no `I_STRAWBERRY`, use the index of `"STRAWBERRY"` in `spec.CROPS` (it is 3) — the `hasattr` guard above handles both. The `_obs()` helper is a copy of `tests/test_sell_head.py:115` — keep it a copy; tests don't import each other.

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/python -m pytest tests/test_fert_source.py -v`
Expected: FAIL — `TypeError: Macro.__new__() got an unexpected keyword argument 'fert_buy'` and `AttributeError: module 'kagg3.core.policy' has no attribute 'offset'`.

- [ ] **Step 3: Append the `g5`/`gb5` block and add `PO.offset(name)`**

In `src/kagg3/core/policy.py`:

```python
N_AUX_OUT = 3            # fert_buy, land_afford, free_urgency (brain.decide)

SHAPES = [
    ...,
    ("g4", (N_HEAD_HID, 1)), ("gb4", (1,)),
    # Unblock genes (2026-08-23). Appended for the same reason as g3/g4: every
    # earlier theta is a prefix and unpacks with this block zeroed. NOT placed
    # in head[13..17] -- those outputs were always live parameters and carry
    # trained noise in every checkpoint.
    ("g5", (N_HEAD_HID, N_AUX_OUT)), ("gb5", (N_AUX_OUT,)),
]
```

Add `g5: object` / `gb5: object` to `Params`, `aux: object      # [3]  unblock genes, pre-activation` to `Outputs`, and `aux=gh @ p.g5 + p.gb5` to the `Outputs(...)` in `forward`. Update the module docstring's total (4,287 → 4,386). `N_PARAMS_LEGACY` stays `SHAPES[:8]`.

Directly after `N_PARAMS_LEGACY`:

```python
def offset(name: str) -> int:
    """Start index of parameter block `name` in the flat theta."""
    i = 0
    for n, shape in SHAPES:
        if n == name:
            return i
        i += int(np.prod(shape))
    raise KeyError(name)
```

- [ ] **Step 4: Add `fert_buy` to `Macro` and the walk**

In `src/kagg3/core/plan.py`, append to `class Macro` after `sell_lots`:

```python
    fert_buy: object        # int     0/1  buy the fertilizer shortfall at market
```

Replace `plan.py:314`:

```python
    fert_short = xp.maximum(macro.n_fertilize - view.shed[spec.I_FERT], 0)
```

with:

```python
    # Fertilizer is collected from animals; buying it at market is a separate
    # decision. With the shortfall always bought, every step up the fertilize
    # gene cost more than it earned (measured 2026-08-23: 50k -> 32k coins),
    # which is exactly why ES never raised it.
    fert_short = xp.where(macro.fert_buy > 0,
                          xp.maximum(macro.n_fertilize - view.shed[spec.I_FERT], 0),
                          0).astype(i32)
```

- [ ] **Step 5: Decode it in `brain.decide`**

In `src/kagg3/core/brain.py`, after `care_on = (head[4] > 0).astype(i32)` add:

```python
    aux = out.aux            # g5/gb5 block: zero (hence inert) for pre-g5 thetas
    fert_buy = (aux[0] > 0).astype(i32)
```

and in the `return P.Macro(...)` add `fert_buy=fert_buy,` after `sell_lots=sell_lots,`.

- [ ] **Step 6: Update the three `_macro` helpers**

In `tests/test_budget_order.py`, `tests/test_sell_head.py`, `tests/test_task_priority.py`, add `fert_buy=np.int32(0)` to the `base = dict(...)` of each `_macro` helper (after `sell_lots=np.int32(1)`).

- [ ] **Step 7: Run the full suite**

Run: `.venv/bin/python -m pytest tests -x -q --ignore=tests/test_sim_equivalence.py --ignore=tests/test_trained_equivalence.py`
Expected: all PASS. Then run the two slow gates: `.venv/bin/python -m pytest tests/test_sim_equivalence.py tests/test_trained_equivalence.py -x -q` — Expected: PASS (the hard-coded cases never bought fertilizer and every trained theta has a zero `g5` block; if one now differs, inspect its market row before changing the test).

- [ ] **Step 8: Commit**

```bash
git add src/kagg3/core/plan.py src/kagg3/core/brain.py src/kagg3/core/policy.py tests/test_fert_source.py tests/test_budget_order.py tests/test_sell_head.py tests/test_task_priority.py
git commit -m "Split fertilizer use from fertilizer buy so the fertilize gene can climb"
```

---

### Task 2: Land affordability gene

`buy_land = head[1] > 0` learned a threshold on `nquad`: +1.0 while broke, −0.5 once a second quadrant exists, regardless of 50k in cash. Add a term that grows with cash relative to the next quadrant's price, gated by `aux[1]` so pre-`g5` thetas are unchanged.

The ratio is **clipped to [−1, 4]**: unclipped it reaches ~50 with 50k in hand, so a single `sigma = 0.05` ES step on `gb5[1]` would swing the logit by ~2.5 and the sampled archetypes in the training plan could never decode `buy_land = 0`.

**Files:**
- Modify: `src/kagg3/core/brain.py:241`
- Test: `tests/test_land_affordability.py`

**Interfaces:**
- Produces: `buy_land = (head[1] + aux[1] * clip(money / land_cost − 1, −1, 4) > 0)`.

- [ ] **Step 1: Write the failing tests**

```python
"""The shipped theta's land logit turns negative the moment a second quadrant
exists and stays there with 50k in the bank. aux[1] (the g5/gb5 block) adds a
cash-relative term, clipped to [-1, 4]: zero for every pre-g5 theta, so old
checkpoints decode unchanged."""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, "src")

import numpy as np

from kagg3 import spec
from kagg3.core import brain
from kagg3.core import policy as PO


def _obs(money, nquad):
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_LOCKED, np.int32)
    kind[spec.TILE_QUAD < nquad] = spec.KIND_EMPTY
    shed = np.zeros(spec.N_ITEMS, np.int32)
    return brain.PolicyObs(
        day=np.int32(12), money=np.int32(money), opp_money=np.int32(money),
        kind=kind, occ=z - 1, opp_kind=kind.copy(), opp_occ=z - 1,
        t_day=z.copy(), t_yield=z.copy(),
        shed=shed, seeds=np.zeros(spec.N_CROPS, np.int32),
        nquad=np.int32(nquad), opp_nquad=np.int32(nquad),
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        price=np.full(spec.N_PRODUCTS, 25, np.int32),
        shops=np.zeros(8, np.int32))


def _theta(h1, a1):
    """Zero weights, so head == gb2 and aux == gb5 exactly; set both directly."""
    theta = np.zeros(PO.N_PARAMS, np.float32)
    theta[PO.offset("gb2") + 1] = h1
    theta[PO.offset("gb5") + 1] = a1
    return theta


def test_legacy_threshold_is_unchanged_when_aux_1_is_zero():
    rich, poor = _obs(50_000, 2), _obs(100, 2)
    assert int(brain.decide(np, _theta(-0.5, 0.0), rich).buy_land) == 0
    assert int(brain.decide(np, _theta(+0.5, 0.0), poor).buy_land) == 1


def test_positive_aux_1_buys_when_cash_dwarfs_the_price():
    # nquad 2 -> next quadrant costs 2000; 50k/2000 - 1 = 24, clipped to 4:
    # -0.5 + 0.5 * 4 = 1.5 > 0
    assert int(brain.decide(np, _theta(-0.5, 0.5), _obs(50_000, 2)).buy_land) == 1


def test_positive_aux_1_does_not_buy_when_cash_is_below_the_price():
    # 1000 / 2000 - 1 = -0.5 -> -0.5 + 0.5 * -0.5 = -0.75 < 0
    assert int(brain.decide(np, _theta(-0.5, 0.5), _obs(1_000, 2)).buy_land) == 0


def test_ratio_is_clipped_so_cash_cannot_dominate():
    # 10,000 / 2000 - 1 = 4 and 50,000 / 2000 - 1 = 24 must decode alike
    a = brain.decide(np, _theta(-2.1, 0.5), _obs(10_000, 2)).buy_land
    b = brain.decide(np, _theta(-2.1, 0.5), _obs(50_000, 2)).buy_land
    assert int(a) == int(b) == 0          # -2.1 + 0.5 * 4 = -0.1


def test_both_backends_agree():
    import jax.numpy as jnp
    obs = _obs(50_000, 2)
    th = _theta(-0.5, 0.5)
    a = brain.decide(np, th, obs).buy_land
    b = brain.decide(jnp, jnp.asarray(th), brain.PolicyObs(*[jnp.asarray(x) for x in obs])).buy_land
    assert int(a) == int(b)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/python -m pytest tests/test_land_affordability.py -v`
Expected: `test_positive_aux_1_buys_when_cash_dwarfs_the_price` FAILS (returns 0); the others pass already.

- [ ] **Step 3: Implement**

In `src/kagg3/core/brain.py`, replace:

```python
    buy_land = (head[1] > 0).astype(i32)
```

with:

```python
    # head[1] alone learned a threshold on nquad (measured 2026-08-23: +1.0
    # while broke, -0.5 once a second quadrant exists, with 50k in hand).
    # aux[1] scales a cash-to-price ratio so "rich relative to the next
    # quadrant" can push the decision; zero for pre-g5 thetas. Clipped: the
    # raw ratio reaches ~50, which would make one sigma step on gb5[1] a
    # 2.5-logit swing.
    land_cost = xp.asarray(spec.LAND_PRICES.astype(np.float32))[xp.clip(obs.nquad - 1, 0, 2)]
    afford = xp.clip(obs.money.astype(xp.float32) / land_cost - 1.0, -1.0, 4.0)
    buy_land = (head[1] + aux[1] * afford > 0).astype(i32)
```

- [ ] **Step 4: Run tests**

Run: `.venv/bin/python -m pytest tests/test_land_affordability.py tests/test_gates.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/kagg3/core/brain.py tests/test_land_affordability.py
git commit -m "Let cash relative to the next quadrant's price drive the land gene"
```

---

### Task 3: Free-land urgency gene (fill what you bought)

Forced land purchases lost 14k coins because `dev_frac` (head[5]) is one fraction for every day: 35 tiles sat empty all game. Add `aux[2]` scaling development by the share of free tiles, zero for pre-`g5` thetas.

**Files:**
- Modify: `src/kagg3/core/brain.py:248-249`
- Test: `tests/test_free_land_urgency.py`

**Interfaces:**
- Produces: `dev_frac = sigmoid(head[5] + aux[2] * n_free / 25)`.

- [ ] **Step 1: Write the failing tests**

```python
"""Buying a quadrant only pays if it gets planted. `dev_frac` was one number for
every day, so a freshly unlocked quadrant (25 free tiles) was developed at the
same trickle as a full farm's two free tiles. aux[2] (the g5/gb5 block) makes
the share of free tiles raise it; zero for pre-g5 thetas."""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, "src")

import numpy as np

from kagg3 import spec
from kagg3.core import brain
from kagg3.core import policy as PO


def _obs(n_free_tiles):
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_LOCKED, np.int32)
    kind[spec.TILE_QUAD < 2] = spec.KIND_PLANT          # 50 tiles owned, all planted
    free_ids = np.flatnonzero(spec.TILE_QUAD < 2)[:n_free_tiles]
    kind[free_ids] = spec.KIND_EMPTY
    occ = np.where(kind == spec.KIND_PLANT, 0, -1).astype(np.int32)
    shed = np.zeros(spec.N_ITEMS, np.int32)
    return brain.PolicyObs(
        day=np.int32(12), money=np.int32(10_000), opp_money=np.int32(10_000),
        kind=kind, occ=occ, opp_kind=kind.copy(), opp_occ=occ.copy(),
        t_day=z.copy(), t_yield=z.copy(),
        shed=shed, seeds=np.full(spec.N_CROPS, 50, np.int32),
        nquad=np.int32(2), opp_nquad=np.int32(2),
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        price=np.full(spec.N_PRODUCTS, 25, np.int32),
        shops=np.zeros(8, np.int32))


def _theta(h5, a2):
    theta = np.zeros(PO.N_PARAMS, np.float32)
    theta[PO.offset("gb2") + 5] = h5
    theta[PO.offset("gb5") + 2] = a2
    return theta


def _developed(theta, obs):
    m = brain.decide(np, theta, obs)
    return int(m.plant_target.sum() + m.animal_count)


def test_legacy_dev_frac_is_unchanged_when_aux_2_is_zero():
    # sigmoid(0) = 0.5 of free tiles, whatever their number
    assert _developed(_theta(0.0, 0.0), _obs(2)) == 1
    assert _developed(_theta(0.0, 0.0), _obs(24)) == 12


def test_positive_aux_2_develops_more_of_a_big_free_block():
    # 24 free tiles: 0 + 3 * 24/25 = 2.88 -> sigmoid ~0.95 -> 22 of 24
    assert _developed(_theta(0.0, 3.0), _obs(24)) >= 22


def test_positive_aux_2_barely_changes_a_small_free_block():
    # 2 free tiles: 0 + 3 * 2/25 = 0.24 -> sigmoid 0.56 -> floor(1.12) = 1
    assert _developed(_theta(0.0, 3.0), _obs(2)) == 1
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/python -m pytest tests/test_free_land_urgency.py -v`
Expected: `test_positive_aux_2_develops_more_of_a_big_free_block` FAILS (12 < 22).

- [ ] **Step 3: Implement**

In `src/kagg3/core/brain.py`, replace:

```python
    dev_frac = sig(head[5])
```

with:

```python
    # One fraction for every day left a freshly bought quadrant empty for days
    # (forced-land counterfactual, 2026-08-23: 35 tiles idle all game). aux[2]
    # lets the share of free tiles raise development; zero for pre-g5 thetas.
    dev_frac = sig(head[5] + aux[2] * n_free.astype(xp.float32) / 25.0)
```

- [ ] **Step 4: Run tests**

Run: `.venv/bin/python -m pytest tests/test_free_land_urgency.py tests/test_gates.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/kagg3/core/brain.py tests/test_free_land_urgency.py
git commit -m "Let the share of free tiles raise daily development"
```

---

### Task 4: Never plant a crop that cannot mature

Hard engine rule, not a gene: the shipped agent ends with ~18 wheat units unharvested because it plants on days 26–29. Mask crops that cannot turn into coins out of the planting softmax.

**What the engine actually does** (read `sim/units.py:95-115` and `sim/eod.py:60-80` before touching this): *ongoing* crops (tomato, strawberry) gain yield at end-of-day once `age >= CROP_FIRST_YIELD_DAY`; *one-time* crops (wheat, carrot, melon) gain yield only when **watered** inside `[CROP_WINDOW_START, CROP_MAX_YIELD_DAY]` and become harvestable at `age >= CROP_FIRST_YIELD_DAY`. Either way nothing is harvestable before `day + CROP_FIRST_YIELD_DAY[c]`. The product then has to be sold: `sell_qty` is decoded from the hour-0 shed, and the last playable day is 29 (23 turns, no end-of-day). So a unit harvested on day 29 is never sold, and the binding rule is **harvestable by day 28**: `day + CROP_FIRST_YIELD_DAY[c] <= 28`. (It is *not* "day 28's end-of-day is the last that grows anything" — that describes ongoing crops only.)

**Files:**
- Modify: `src/kagg3/core/brain.py:258-259` (crop softmax)
- Test: `tests/test_no_late_planting.py`

- [ ] **Step 1: Write the failing tests**

```python
"""A crop that cannot be harvested and sold before the season ends is a pure
loss. Nothing is harvestable before day + CROP_FIRST_YIELD_DAY; the sale is
decoded from the hour-0 shed and day 29 is the last playable day, so a unit
harvested on day 29 is never sold. Rule: day + first_yield_day <= 28."""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, "src")

import numpy as np

from kagg3 import spec
from kagg3.core import brain
from kagg3.core import policy as PO


def _obs(day):
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_LOCKED, np.int32)
    kind[spec.TILE_QUAD == 0] = spec.KIND_EMPTY
    return brain.PolicyObs(
        day=np.int32(day), money=np.int32(10_000), opp_money=np.int32(10_000),
        kind=kind, occ=z - 1, opp_kind=kind.copy(), opp_occ=z - 1,
        t_day=z.copy(), t_yield=z.copy(),
        shed=np.zeros(spec.N_ITEMS, np.int32), seeds=np.full(spec.N_CROPS, 50, np.int32),
        nquad=np.int32(1), opp_nquad=np.int32(1),
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        price=np.full(spec.N_PRODUCTS, 25, np.int32),
        shops=np.zeros(8, np.int32))


def _theta_develop_all_crops():
    theta = np.zeros(PO.N_PARAMS, np.float32)
    gb2 = PO.offset("gb2")
    theta[gb2 + 5] = 10.0      # dev_frac -> 1
    theta[gb2 + 6] = -10.0     # animal_share -> 0
    return theta


def test_day_0_plants_every_crop():
    m = brain.decide(np, _theta_develop_all_crops(), _obs(0))
    assert np.all(m.plant_target > 0)


def test_day_20_skips_crops_that_first_yield_after_day_28():
    m = brain.decide(np, _theta_develop_all_crops(), _obs(20))
    late = spec.CROP_FIRST_YIELD_DAY + 20 > 28     # strawberry(10), melon(10)
    assert np.all(m.plant_target[late] == 0)
    assert np.all(m.plant_target[~late] > 0)
    assert int(m.plant_target.sum()) == 25         # the tiles still get used


def test_day_27_plants_nothing():
    m = brain.decide(np, _theta_develop_all_crops(), _obs(27))
    assert int(m.plant_target.sum()) == 0
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/python -m pytest tests/test_no_late_planting.py -v`
Expected: the day-20 and day-27 tests FAIL.

- [ ] **Step 3: Implement**

In `src/kagg3/core/brain.py`, replace:

```python
    w = _softmax(xp, grow[:spec.N_CROPS] * (1.0 + sig(head[7]) * 4.0))
    plant_target = _largest_remainder(xp, w, plant_total, spec.N_CROPS)
```

with:

```python
    w = _softmax(xp, grow[:spec.N_CROPS] * (1.0 + sig(head[7]) * 4.0))
    # Engine fact, not a gene: nothing is harvestable before
    # day + CROP_FIRST_YIELD_DAY, the sale is decoded from the hour-0 shed,
    # and day 29 is the last playable day -- so a crop harvested on day 29 is
    # never sold. It must be harvestable by day 28 or the seed is thrown
    # away. Masked weights are renormalised; if nothing can mature, nothing
    # is planted.
    can_mature = (obs.day + xp.asarray(spec.CROP_FIRST_YIELD_DAY) <= 28).astype(xp.float32)
    w = w * can_mature
    w_sum = xp.sum(w)
    w = xp.where(w_sum > 0, w / xp.maximum(w_sum, 1e-6), w)
    plant_total = xp.where(w_sum > 0, plant_total, 0).astype(i32)
    plant_target = _largest_remainder(xp, w, plant_total, spec.N_CROPS)
```

Check `_largest_remainder` (`brain.py:198`) handles an all-zero weight vector with `total == 0` without division by zero; if it divides by `sum(weights)`, guard it with `xp.maximum(..., 1e-6)`.

- [ ] **Step 4: Run tests**

Run: `.venv/bin/python -m pytest tests/test_no_late_planting.py tests/test_gates.py tests/test_sim_equivalence.py -v`
Expected: PASS. `test_sim_equivalence` may change if a hard-coded case planted late — if so, the *engine* result also changes (same planner on both sides), so it must still pass; if it fails, the failure is a real backend divergence in the new code, fix before continuing.

- [ ] **Step 4b: Confirm the boundary in the real engine**

The `<= 28` boundary is derived above, not measured. Check it once: run the shipped theta with the mask at `<= 28` and at `<= 29` through `scripts/eval_vs_baselines.py` (4 games each, same seeds) and confirm the `<= 28` variant is not worse. If `<= 29` wins, a day-29 harvest *is* being sold (some path this reading missed) and the constant must move; record which in the commit body. Expected gain from this task is small (a day-26 wheat is one 25-coin unit against a 10-coin seed plus labour), so treat a difference under ~500 coins as noise.

- [ ] **Step 5: Commit**

```bash
git add src/kagg3/core/brain.py tests/test_no_late_planting.py
git commit -m "Never plant a crop that cannot mature before the season ends"
```

---

### Task 5: Re-measure the shipped theta

No code; confirms nothing regressed under the new decode and records the baseline the training plan measures against.

**Files:**
- Read only.

- [ ] **Step 1: Evaluate the shipped theta against kagg2**

Run (use the session scratchpad, not a hard-coded path):
```bash
T=$(mktemp -d); tar xzf dist/submission.tar.gz -C "$T" theta.npy
.venv/bin/python scripts/eval_vs_baselines.py --theta "$T/theta.npy" --games 8 --opponents /mnt/e/_work/kaggriculture2/main.py
```
Expected: mean coins within ±5k of the 2026-08-23 baseline (50,046). The shipped theta is a 4,287-prefix of the new layout, so its `g5`/`gb5` block is zero and Tasks 1–3 are exactly inert for it (do **not** rely on `head[13..17]` being zero — they are not); Task 4 may add up to ~2k (no wasted late seeds). A larger move means one of the "inert at zero" claims is false — bisect by task before recording anything.

- [ ] **Step 2: Record the number**

Append one line to `docs/superpowers/plans/2026-08-23-genome-unblock.md` under a `## Baseline` heading: date, theta md5, mean coins, margin. Commit:

```bash
git add docs/superpowers/plans/2026-08-23-genome-unblock.md
git commit -m "Record the post-genome-change baseline for the shipped theta"
```

---

## Out of scope (separate plans)

- Raising `MAX_HANDS` 10 → 15: touches `spec.HIRE_COST`, sim state arrays and the hand scatter; do after the training plan shows the land genes moving.
- Setpoint genome (target tiles / target stock per product): a redesign of `decide`, not an unblock; write its own spec first.
- Per-product hold-then-dump sell timing: same.

## Baseline

- 2026-08-23, theta md5 5371170a82852f382769aa2da848cd0d, mean coins 72,991 (pre-change code on identical seeds: 73,034), mean margin -60,415 vs /mnt/e/_work/kaggriculture2/main.py, win 0%, 8 seeds x 2 seats.
