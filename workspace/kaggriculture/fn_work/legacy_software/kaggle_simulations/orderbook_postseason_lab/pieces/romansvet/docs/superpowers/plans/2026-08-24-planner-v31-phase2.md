# Planner V3.1 — Phase 2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Dispatch each task to a fresh **Opus** subagent (`model: "opus"`); the implementer sees only its own task plus the header, so every task repeats what it needs.

**Goal:** Land Phase 2 of `docs/PLANNER_V3_1.md` §8 — the Layer-1 optimizers (§1.2 sell, §1.3 buy, §1.4 feed, §1.5 hire, §1.6 labour), the §2 genome re-type with parameter masking, the init-posture assertion — and start the fresh lineage with the §7 measurement protocol.

**Architecture:** Every learned output is re-typed from *decision* to *value estimate in coins* (`hold`, `press`, `grow_mult`), and the planner makes every decision by deterministic integer arithmetic over those values plus the engine's tables. Three new array-agnostic modules carry the optimizers — `core/sell.py` (lot allocation), `core/budget.py` (marginal-unit purchases), `core/loop.py` (a bounded loop the simulator can trace) — and `core/valuation.py` grows the values they need. Ten genes stop existing as decisions; their parameter columns are masked out of the ES perturbation and update. Checkpoints do not survive: Phase 2 is a fresh lineage, compared lineage-vs-lineage.

**Tech Stack:** Python 3, numpy, JAX (CPU for tests; GPU for training), pytest, ruff.

**Spec:** `docs/PLANNER_V3_1.md` §§1.1–1.6, §2, §7, §8 (Phase 2 bullet). Audit record: `docs/PLANNER_V3_1_REVIEW.md`. Read both before starting a task.

**Prerequisites:** the Phase-0 and Phase-1 plans are fully landed — `git log --oneline | grep -c "Record the Phase-"` prints `2`. This plan quotes post-Phase-1 code by content: `core/projector.py` (`projected_inv`, `sell_quotes`, `buy_quotes`, `marginal_quote`, `K`), `core/valuation.py` (`fires_between`, `fires_on`, `next_fire_after`, `crop_fires_on`, `animal_value`, `fert_marginal_value`), `plan._rank_by`, `plan._cum_take`, `DayView.mkt_inv/.shops/.t_bank`, `build_day(xp, view, macro, price_table=None)`, `_routes(...) -> (route_op, route_a, route_q, blk, covered, n_pick)`, `task_order(xp, task, score, tier=None)`, and `build_day` locals named in each task's Interfaces block.

**Out of scope:** Phase 3 (§3 walk-and-cap executor guard, §4 DROP, M1–M3, per-parameter sigma). §5's open items.

## Global Constraints

Every task's requirements implicitly include this section.

- Planner code is array-agnostic (`xp` = numpy or `jax.numpy`), shape-static, int32; pairwise ranking, never sorting, inside `build_day`; bounded loops go through `core/loop.py` (Task 2), never a data-dependent Python loop.
- `core/` never imports `jax` — not even lazily inside a function: the packager's gate (`scripts/package_submission.py::forbidden_imports`) parses every shipped file's AST for import statements.
- Every learned quantity that becomes an integer passes through `brain._qfloor` (`QUANT_EPS`); raw linear outputs are never treated as calibrated coins (§2). Coin values are int32 and clipped to `< 2**20` before any ratio arithmetic.
- Tie-breaking: pairwise/lexicographic, ties to the lower index (serpentine position), the earlier lot, the lower product, the lower candidate list — in that order of precedence where several apply.
- Market orders only on turns 0, 1, 2, 10, 18 (§6.1). Both seats keep an identical slot layout (`sim/market.py::assert_no_cross`).
- Checkpoint compatibility is **not** a constraint in Phase 2 (§2: "Checkpoint semantics do not survive the re-typing"). `artifacts/theta.npy` is the *old* lineage; do not measure it under the new planner. The theta *layout* (`policy.SHAPES`, `N_PARAMS = 4386`) is unchanged; dead parameters are masked, not removed.
- Every deleted decision is deleted from `plan.Macro` and from `brain.decide` in the task that replaces it; nothing decodes to a value nobody reads.
- The §2 decode table is the contract: grow multiplier `min(softplus(z)/softplus(0), 4)`; reservation `0.8 × base_p × softplus(z)/softplus(0)`; pressure `base_p × relu(tanh(z))`; `dev_frac`, free-tile aux, `animal_share`, `buy_land` + afford aux, plant-mix sharpness unchanged. 32 decoded scalars.
- Every optimizer lands with a compile-time and throughput measurement (§7): `python scripts/bench_sim.py` before and after, numbers in the commit message; a slowdown above 15% is reported and stops the task (§1.5 is explicitly benchmark-gated).
- Interpreter: every `python` in this plan means the repo's `.venv/bin/python` (or a shell with that venv activated) — the system `python` has neither JAX nor `kaggle_environments`.
- Tests: file header `os.environ.setdefault("JAX_PLATFORMS", "cpu")`, `sys.path.insert(0, "src")`; the shared fixtures are `tests/test_budget_order.py`'s `_view`/`_macro` (Task 1 re-shapes `_macro`); filler tiles that must stay occupied hold an ongoing crop; run `python -m pytest tests/<file>.py -q`, full suite `python -m pytest -q`.
- Lint: `ruff check src tests` clean before every commit. Commit per task on branch `fitness-shaping`, one-line sentence-case imperative message. Never commit `artifacts/`.

## Engine and code facts the tasks lean on

- `policy.forward` returns `Outputs(scores[9, 2], head[18], prio[9], gate[9], lots[], aux[3])`; `scores[:, 0]` is the grow score, `scores[:, 1]` the sell score. Live heads after Phase 2: `head[1]` (land logit), `head[5]` (dev_frac), `head[6]` (animal_share), `head[7]` (sharpness), `aux[1]` (land afford), `aux[2]` (free-tile urgency). Dead: `head[0]` (was n_hire), `head[2:5]` (n_fertilize, feed_daily, care_on), `head[8:18]` (order + never used), `prio` (`g3/gb3`), `lots` (`g4/gb4`), `aux[0]` (`g5[:, 0]`, `gb5[0]`; was fert_buy).
- ES update (`es/train.py::Trainer.generation`): antithetic `eps ~ N(0, 1)[pop/2, n]`, `grad = (adv[:half] - adv[half:]) @ eps / (pop * sigma)`, elementwise Adam, then decoupled decay `theta = (1 - wd) * step`. Masking a coordinate = zero its `eps` column and leave `theta` untouched there.
- The engine walks each SELL one unit at a time; a sale at the floor pays but does not add supply; town ticks between lots lower inventory (§1.1). Own units sold in an earlier lot raise the inventory every later lot faces, so a lot's revenue shifts by `price[start + n] - price[start]` when its start moves one unit up (telescoping) — the externality Task 2's greedy charges.
- Buy quotes: the j-th unit costs `price[inv - 1 - j]` (Phase 1, `projector.buy_quotes`); seeds, animals and land are fixed-price.
- `_routes` cuts the ordered task list into contiguous per-unit blocks and charges exact Manhattan moves between consecutive tiles (Phase 1 §0.12 accounting).

## File map

| File | Responsibility after Phase 2 |
|---|---|
| `src/kagg3/core/brain.py` | decode `hold`, `press`, `grow_mult` (+ `GROW_ONE`, `_softplus`, `_unit_ratio`); stop decoding the ten deleted decisions |
| `src/kagg3/core/plan.py` | `Macro` = `plant_target, animal_kind, animal_count, buy_land, hold, press, grow_mult`; `_derive` prefix + hire enumeration + admit/route + sale; `_market` takes `lots[3, 9]` |
| `src/kagg3/core/loop.py` | **new** — `repeat(xp, n, body, carry)` with an installable traced implementation |
| `src/kagg3/core/sell.py` | **new** — `allocate`, `best_lot`, `adjusted_marginals` (§1.2) |
| `src/kagg3/core/budget.py` | **new** — `grant` (§1.3 threshold greedy) |
| `src/kagg3/core/valuation.py` | + `new_plant_units`, `remaining_plant_units`, `crop_remaining_value` |
| `src/kagg3/core/projector.py` | + `daily_town_units`, `inv_at_day` (sales-window inventory) |
| `src/kagg3/core/policy.py` | + `DEAD_HEAD`, `live_mask()` |
| `src/kagg3/es/train.py` | masked perturbation and update; `Trainer.mask` |
| `src/kagg3/es/archetypes.py` | knobs re-typed to the live outputs |
| `src/kagg3/sim/rollout.py` | installs the traced loop |
| `scripts/train.py` | `--trunk-from` |
| tests | `test_genome_retype.py`, `test_sell_allocator.py`, `test_sell_side.py`, `test_feed_value.py`, `test_budget_greedy.py`, `test_admit_route.py`, `test_hire_enumeration.py`, `test_es_masking.py`; rewrites of `test_budget_order.py`, `test_hire_bill.py`, `test_task_priority.py`, `test_archetypes.py`; deletions of `test_fert_source.py`, `test_sell_head.py`, `test_learned_order.py` |

Task order: 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9. Each optimizer task deletes the gene it replaces, so the planner is consistent at every commit.

---

### Task 1: The re-typed genome — `hold`, `press`, `grow_mult`; drop the four dead decisions (§2)

**Files:**
- Modify: `src/kagg3/core/brain.py` (`decide`, new helpers), `src/kagg3/core/plan.py` (`Macro`), `src/kagg3/es/archetypes.py`
- Modify fixtures: `tests/test_budget_order.py::_macro`, `tests/test_sell_head.py::_macro`, `tests/test_task_priority.py::_macro`, `tests/test_day29_endgame.py::_greedy_macro`
- Delete: `tests/test_fert_source.py` (its layout test moves here); delete `test_old_genes_are_ignored` from `tests/test_fertilizer_value.py` and `test_feed_daily_gene_no_longer_forces_a_feed`, `test_care_on_gene_no_longer_gates_it` from `tests/test_feed_care_cadence.py` (the kwargs they pass no longer exist)
- Rewrite: `tests/test_archetypes.py` (three tests)
- Test: `tests/test_genome_retype.py`

**Interfaces:**
- Produces: `brain.GROW_ONE = 256` (fixed-point unit of the grow multiplier), `brain.GROW_MAX = 4.0`, `brain._softplus(xp, z)`, `brain._unit_ratio(xp, z)` (= `softplus(z)/softplus(0)`); `Macro.hold` (int[9], coins), `Macro.press` (int[9], coins per lot of delay), `Macro.grow_mult` (int[9], `GROW_ONE` = ×1). `Macro` loses `n_fertilize`, `feed_daily`, `care_on`, `fert_buy`. `archetypes.KNOBS` gains `hold`, `press` (biases on `b2[1]` and `b3`), loses `fert_use`, `feed`, `care`, `fert_buy`, `sell`, `gate`.
- Transitional (deleted by later tasks): `Macro.sell_qty`, `sell_min`, `sell_lots` (Task 3), `order` (Task 5), `prio` (Task 6), `n_hire` (Task 7) keep decoding as today.

**Background (§2).** The encoder's sell score is re-typed to a **reservation value** — the coins one unit is worth if kept until tomorrow — at `0.8 · base` when `z = 0`, so the initial policy sells; the per-product gate head becomes **opponent timing pressure**, 0 at `z = 0`; the grow score becomes a **value multiplier** in `[0, 4]`, 1 at `z = 0`, applied to seed and animal candidate values. All three are quantized (`_qfloor`); the multiplier is fixed-point so every downstream value stays int32. The init-posture assertion (§8): at `z = 0` the first unit's lot-3 quote on a fresh market clears `0.8 · base` for every product — "the initial policy sells" is a test.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_genome_retype.py`:

```python
"""PLANNER_V3_1 section 2: learned outputs are values in coins, not decisions.
`hold` is a reservation value (0.8 x base at z = 0, so the initial policy
sells -- asserted against the projector, not assumed), `press` an opponent
timing pressure (0 at z = 0), `grow_mult` a value multiplier (x1 at z = 0,
capped at x4, fixed-point). The four decisions the planner stopped reading in
Phase 1 no longer exist in the Macro.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, "src")

import numpy as np
from test_sell_head import _obs as _obs_sell   # small fresh-market observation (day 2)

from kagg3 import spec
from kagg3.core import brain
from kagg3.core import ops as O
from kagg3.core import plan as P
from kagg3.core import policy as PO
from kagg3.core import projector as PJ

TABLE = spec.build_price_table()


def _theta_with(sell=0.0, gate=0.0, grow=0.0):
    th = np.zeros(PO.N_PARAMS, np.float32)
    th[PO.offset("b2") + 1] = sell            # sell-score bias, every product
    th[PO.offset("b2") + 0] = grow            # grow-score bias
    th[PO.offset("b3")] = gate                # gate bias
    return th


def test_zero_theta_decodes_to_the_spec_init_posture():
    m = brain.decide(np, np.zeros(PO.N_PARAMS, np.float32), _obs_sell())
    expect_hold = np.floor(0.8 * brain._BASE + brain.QUANT_EPS).astype(np.int32)
    assert m.hold.tolist() == expect_hold.tolist()
    assert m.press.tolist() == [0] * spec.N_PRODUCTS
    assert m.grow_mult.tolist() == [brain.GROW_ONE] * spec.N_PRODUCTS


def test_the_initial_policy_sells():
    # day-1 projected marginals clear 0.8 x base: the first unit of every
    # product, sold in the last lot of a fresh market, fetches at least `hold`
    m = brain.decide(np, np.zeros(PO.N_PARAMS, np.float32), _obs_sell())
    inv = PJ.projected_inv(np, np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
                           np.zeros(spec.N_SHOPS, np.int32), O.SELL_TURNS[-1])
    first_unit = PJ.sell_quotes(np, TABLE, inv)[:, 0]
    assert np.all(first_unit >= m.hold)


def test_transforms_are_monotone_and_bounded():
    lo = brain.decide(np, _theta_with(sell=-6.0, gate=-6.0, grow=-6.0), _obs_sell())
    mid = brain.decide(np, _theta_with(), _obs_sell())
    hi = brain.decide(np, _theta_with(sell=6.0, gate=6.0, grow=6.0), _obs_sell())
    assert np.all(lo.hold < mid.hold) and np.all(mid.hold < hi.hold) and np.all(lo.hold >= 0)
    assert np.all(lo.press == 0) and np.all(mid.press == 0) and np.all(hi.press > 0)
    assert np.all(hi.press <= brain._BASE)
    assert np.all(lo.grow_mult < mid.grow_mult) and np.all(hi.grow_mult == int(brain.GROW_MAX * brain.GROW_ONE))


def test_dead_decisions_are_gone_from_the_macro():
    for name in ("n_fertilize", "feed_daily", "care_on", "fert_buy"):
        assert name not in P.Macro._fields


def test_g5_block_is_the_last_and_zero_padding_is_inert():
    assert [n for n, _ in PO.SHAPES[-2:]] == ["g5", "gb5"]
    short = np.ones(PO.N_PARAMS_LEGACY, np.float32)
    padded = np.concatenate([short, np.zeros(PO.N_PARAMS - PO.N_PARAMS_LEGACY, np.float32)])
    a = brain.decide(np, short, _obs_sell())
    b = brain.decide(np, padded, _obs_sell())
    for x, y in zip(a, b):
        np.testing.assert_array_equal(np.asarray(x), np.asarray(y))


def test_decode_agrees_across_backends():
    import jax
    import jax.numpy as jnp
    th = _theta_with(sell=1.5, gate=0.7, grow=-0.4)
    obs = _obs_sell()
    a = brain.decide(np, th, obs)
    b = brain.decide(jnp, jnp.asarray(th), jax.tree_util.tree_map(jnp.asarray, obs))
    for x, y in zip(a, b):
        assert np.array_equal(np.asarray(x), np.asarray(y))
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_genome_retype.py -q`
Expected: FAIL — `AttributeError: 'Macro' object has no attribute 'hold'`.

- [ ] **Step 3: Decode the three values in `brain.py`**

Add after `QUANT_EPS = 1e-4`:

```python
#: Fixed-point unit of the grow value multiplier: GROW_ONE == x1.0. Values it
#: scales are int32 coins, so the multiplier is an integer too.
GROW_ONE = 256
GROW_MAX = 4.0
_SOFTPLUS0 = float(np.log(2.0))


def _softplus(xp, z):
    return xp.maximum(z, 0.0) + xp.log1p(xp.exp(-xp.abs(z)))


def _unit_ratio(xp, z):
    """softplus(z) / softplus(0): exactly 1 at z = 0, positive everywhere."""
    return _softplus(xp, z) / _SOFTPLUS0
```

In `decide`, delete the lines that decode `n_fertilize`, `feed_daily`, `care_on` and `fert_buy` (the `n_plant_tiles`, `n_fertilize`, `feed_daily`, `care_on`, `fert_buy` assignments), and add, after `sell_qty = ...`:

```python
    # The re-typed value outputs (PLANNER_V3_1 section 2). Each is quantized
    # where it becomes an integer, and none is a decision: the planner makes
    # those from these values and the engine's tables.
    base = xp.asarray(_BASE)
    hold = _qfloor(xp, 0.8 * base * _unit_ratio(xp, sell)).astype(i32)            # coins per unit kept
    press = _qfloor(xp, base * xp.maximum(xp.tanh(out.gate), 0.0)).astype(i32)    # coins per lot of delay
    grow_mult = _qfloor(xp, xp.minimum(_unit_ratio(xp, grow), GROW_MAX) * GROW_ONE).astype(i32)
```

and return `hold=hold, press=press, grow_mult=grow_mult` from the `P.Macro(...)` call, dropping `n_fertilize=`, `feed_daily=`, `care_on=`, `fert_buy=`.

In `plan.py::Macro` delete the four fields and append:

```python
    hold: object            # int[9]  reservation value: coins one unit is worth kept until tomorrow
    press: object           # int[9]  opponent timing pressure: coins a unit loses per lot of delay
    grow_mult: object       # int[9]  value multiplier on new plantings/animals, GROW_ONE = x1
```

- [ ] **Step 4: Re-type the archetype knobs**

In `src/kagg3/es/archetypes.py` set:

```python
KNOBS = ("hire", "land", "dev", "animal_share", "crop_sharp", "value_tilt",
         "hold", "press", "lots", "land_afford", "free_urgency")

_HEAD_INDEX = {"hire": 0, "land": 1, "dev": 5, "animal_share": 6, "crop_sharp": 7}
_AUX_INDEX = {"land_afford": 1, "free_urgency": 2}   # gb5
```

replace the two lines that write `sell` and `gate` with

```python
    theta[b2 + 1] = knobs.get("hold", 0.0)                    # reservation-value logit, all products
    theta[PO.offset("b3")] = knobs.get("press", 0.0)          # timing-pressure logit
```

remove every `fert_use=`, `feed=`, `care=`, `fert_buy=` entry from `_NAMED` and rename `sell=` → `hold=` (negate the value: a dumping archetype has a *low* reservation, so `sell=10.0` becomes `hold=-6.0` and `sell=0.0` becomes `hold=0.0`, `sell=2.0` becomes `hold=-1.0`), `gate=` → `press=`; in `sample_archetype` drop the same knobs, use `hold=u(-6.0, 3.0)` and `press=u(-1.0, 1.0)`. Update the module docstring's first paragraph to say the knobs bias the *value* outputs.

- [ ] **Step 5: Update fixtures and the archetype tests**

In every `_macro` (`tests/test_budget_order.py`, `tests/test_sell_head.py`, `tests/test_task_priority.py`) delete the `n_fertilize=`, `feed_daily=`, `care_on=`, `fert_buy=` entries and add:

```python
        hold=np.full(spec.N_PRODUCTS, 10_000, np.int32),    # hold everything unless a test lowers it
        press=np.zeros(spec.N_PRODUCTS, np.int32),
        grow_mult=np.full(spec.N_PRODUCTS, 256, np.int32),
```

In `tests/test_day29_endgame.py::_greedy_macro` drop `n_fertilize=`, `fert_buy=`, `feed_daily=`, `care_on=`. Delete `tests/test_fert_source.py`. Delete the three tests named in **Files** from `test_fertilizer_value.py` and `test_feed_care_cadence.py`.

In `tests/test_archetypes.py` replace `test_expander_buys_land_fertilizes_and_develops`, `test_sell_knob_sets_the_shed_fraction_sold` and the `ferts` assertions in `test_sampled_archetypes_are_diverse_and_valid` with:

```python
def test_expander_buys_land_and_develops():
    m = brain.decide(np, A.archetype_theta(**A.named("expander")), _obs())
    assert int(m.buy_land) == 1
    assert int(m.plant_target.sum() + m.animal_count) >= 35   # 40 free tiles, dev ~0.9+


def test_hold_knob_scales_the_reservation_value():
    dump = brain.decide(np, A.archetype_theta(hold=-10.0), _obs())
    keep = brain.decide(np, A.archetype_theta(hold=10.0), _obs())
    base = brain.decide(np, A.archetype_theta(), _obs())
    assert np.all(dump.hold < base.hold) and np.all(base.hold < keep.hold)
    assert np.all(dump.hold >= 0)


def test_press_knob_is_zero_or_positive():
    assert np.all(brain.decide(np, A.archetype_theta(press=-3.0), _obs()).press == 0)
    assert np.all(brain.decide(np, A.archetype_theta(press=3.0), _obs()).press > 0)
```

and in `test_sampled_archetypes_are_diverse_and_valid` replace the `ferts` set with `presses = set()` collecting `bool(np.any(m.press > 0))` and assert `presses == {False, True}`.

- [ ] **Step 6: Run the tests and the full suite**

Run: `python -m pytest tests/test_genome_retype.py tests/test_archetypes.py -q` — Expected: PASS.
Run: `python -m pytest -q` — Expected: all pass (the planner reads none of the four deleted fields since Phase 1).
Run: `ruff check src tests`.

- [ ] **Step 7: Commit**

```bash
git add -A src/kagg3/core/brain.py src/kagg3/core/plan.py src/kagg3/es/archetypes.py tests/
git commit -m "Re-type the genome: reservation value, timing pressure and grow multiplier in coins"
```

---

### Task 2: The sell allocator and the traced loop (§1.2, pure)

**Files:**
- Create: `src/kagg3/core/loop.py`, `src/kagg3/core/sell.py`
- Modify: `src/kagg3/sim/rollout.py` (install the traced loop at import)
- Test: `tests/test_sell_allocator.py`

**Interfaces:**
- Produces: `loop.repeat(xp, n_iter, body, carry) -> carry` (numpy: Python loop; `jax.numpy` with the simulator imported: `lax.fori_loop`); `loop.install(fn)`.
- `sell.N_LOTS = 3`; `sell.LIQUIDATE = -(1 << 20)`; `sell.lot_inventories(xp, mkt_inv, shops) -> int[3, 9]`; `sell.adjusted_marginals(xp, price_table, inv_lots, lots, press) -> int[3, 9]`; `sell.allocate(xp, price_table, mkt_inv, shops, avail, hold, press) -> int[3, 9]` (units per lot per product); `sell.best_lot(xp, price_table, mkt_inv, shops, lots, press) -> int[9]`.
- Consumers: Task 3 (`allocate`, `best_lot`), Task 5 (`loop.repeat`).

**Background (§1.2).** Opponent-free, selling later within the day is uniformly weakly better and exactly indifferent for fertilizer, so the allocator answers *whether* through `hold` and *when* through `press`: marginal-price greedy over the three lot curves, lot-2/3 inventories advanced by town ticks and by own earlier lots, ties to the earlier lot then the lower product. Plain "next quote" greedy misses that a unit sold in lot 1 lowers every later lot's quotes; the exact effect on a later lot holding `n` units whose start moves up one is `price[start + n] − price[start]` (telescoping), so the greedy charges that externality to the earlier lot. Labelled [HEURISTIC]; a bounded exhaustive split check is the verification test. Floor sales do not advance supply in the engine; counting them as advancing is conservative for the later quotes.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_sell_allocator.py`:

```python
"""The sell allocator (PLANNER_V3_1 section 1.2): a unit is sold iff the best
adjusted lot marginal clears the reservation value; it goes to the lot whose
adjusted marginal -- next quote, minus timing pressure per lot of delay, minus
the externality on later lots -- is highest, ties to the earlier lot.
"""
from __future__ import annotations

import itertools
import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, "src")

import numpy as np

from kagg3 import spec
from kagg3.core import loop
from kagg3.core import ops as O
from kagg3.core import projector as PJ
from kagg3.core import sell as S

TABLE = spec.build_price_table()
I0 = np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32)
NO_SHOPS = np.zeros(spec.N_SHOPS, np.int32)


def _shops(**counts):
    s = np.zeros(spec.N_SHOPS, np.int32)
    for name, n in counts.items():
        s[spec.SHOP_NAMES.index(name)] = n
    return s


def _only(product, n):
    a = np.zeros(spec.N_PRODUCTS, np.int32)
    a[product] = n
    return a


def _revenue(product, split, shops):
    """Projected coins of selling `split` = (n1, n2, n3) units of `product`,
    own earlier lots advancing the later inventories."""
    inv = np.stack([PJ.projected_inv(np, I0, shops, t) for t in O.SELL_TURNS])[:, product]
    total, sold_before = 0, 0
    for k, n in enumerate(split):
        start = int(inv[k]) + sold_before
        total += sum(int(TABLE[product, start + j - spec.PRICE_TABLE_LO]) for j in range(n))
        sold_before += n
    return total


def test_zero_pressure_zero_shops_is_indifferent_and_takes_the_earliest_lot():
    lots = S.allocate(np, TABLE, I0, NO_SHOPS, _only(spec.I_WOOL, 20),
                      np.zeros(spec.N_PRODUCTS, np.int32), np.zeros(spec.N_PRODUCTS, np.int32))
    assert lots[:, spec.I_WOOL].tolist() == [20, 0, 0]
    assert int(lots.sum()) == 20


def test_reservation_value_gates_the_quantity():
    hold = np.full(spec.N_PRODUCTS, 10_000, np.int32)
    lots = S.allocate(np, TABLE, I0, NO_SHOPS, _only(spec.I_WOOL, 20), hold, np.zeros(spec.N_PRODUCTS, np.int32))
    assert int(lots.sum()) == 0
    hold[spec.I_WOOL] = 190          # wool starts at 200 and falls; some units clear it, not all
    lots = S.allocate(np, TABLE, I0, NO_SHOPS, _only(spec.I_WOOL, 20), hold, np.zeros(spec.N_PRODUCTS, np.int32))
    n = int(lots[:, spec.I_WOOL].sum())
    assert 0 < n < 20
    quotes = PJ.sell_quotes(np, TABLE, PJ.projected_inv(np, I0, NO_SHOPS, O.SELL_TURNS[0]))[spec.I_WOOL]
    assert n == int((quotes[:20] >= 190).sum())


def test_town_consumption_moves_the_sale_later():
    # a yarn store drains wool between lots, so later lots quote higher and win
    shops = _shops(YARN_STORE=1)
    lots = S.allocate(np, TABLE, I0, shops, _only(spec.I_WOOL, 20),
                      np.zeros(spec.N_PRODUCTS, np.int32), np.zeros(spec.N_PRODUCTS, np.int32))
    assert int(lots[2, spec.I_WOOL]) > int(lots[0, spec.I_WOOL])
    assert int(lots[:, spec.I_WOOL].sum()) == 20


def test_pressure_pulls_the_sale_earlier():
    shops = _shops(YARN_STORE=1)
    press = _only(spec.I_WOOL, 1000)
    lots = S.allocate(np, TABLE, I0, shops, _only(spec.I_WOOL, 20), np.zeros(spec.N_PRODUCTS, np.int32), press)
    assert lots[:, spec.I_WOOL].tolist() == [20, 0, 0]


def test_greedy_is_close_to_the_exhaustive_split():
    # bounded exhaustive check (the spec's verification-mode fallback)
    shops = _shops(YARN_STORE=2, BAKERY=1)
    for product, n in ((spec.I_WOOL, 12), (spec.I_MILK, 10), (spec.I_WHEAT, 15), (spec.I_FERT, 8)):
        lots = S.allocate(np, TABLE, I0, shops, _only(product, n),
                          np.zeros(spec.N_PRODUCTS, np.int32), np.zeros(spec.N_PRODUCTS, np.int32))
        got = _revenue(product, tuple(int(x) for x in lots[:, product]), shops)
        best = max(_revenue(product, s, shops) for s in itertools.product(range(n + 1), repeat=3)
                   if sum(s) == n)
        assert got >= 0.97 * best, (product, lots[:, product].tolist(), got, best)


def test_best_lot_reports_where_a_forced_unit_goes():
    shops = _shops(YARN_STORE=1)
    lots = np.zeros((S.N_LOTS, spec.N_PRODUCTS), np.int32)
    assert int(S.best_lot(np, TABLE, I0, shops, lots, np.zeros(spec.N_PRODUCTS, np.int32))[spec.I_WOOL]) == 2
    assert int(S.best_lot(np, TABLE, I0, shops, lots, _only(spec.I_WOOL, 1000))[spec.I_WOOL]) == 0


def test_allocator_agrees_across_backends_with_and_without_the_traced_loop():
    import jax.numpy as jnp
    shops = _shops(YARN_STORE=1, PET_CAFE=1)
    avail = np.arange(spec.N_PRODUCTS, dtype=np.int32) * 3
    hold = np.full(spec.N_PRODUCTS, 30, np.int32)
    press = np.arange(spec.N_PRODUCTS, dtype=np.int32) * 5
    a = S.allocate(np, TABLE, I0, shops, avail, hold, press)
    b = S.allocate(jnp, jnp.asarray(TABLE), jnp.asarray(I0), jnp.asarray(shops),
                   jnp.asarray(avail), jnp.asarray(hold), jnp.asarray(press))
    assert a.tolist() == np.asarray(b).tolist()
    from kagg3.sim import rollout  # noqa: F401  -- installs lax.fori_loop
    assert loop._impl is not None
    c = S.allocate(jnp, jnp.asarray(TABLE), jnp.asarray(I0), jnp.asarray(shops),
                   jnp.asarray(avail), jnp.asarray(hold), jnp.asarray(press))
    assert a.tolist() == np.asarray(c).tolist()
    d = S.allocate(np, TABLE, I0, shops, avail, hold, press)      # numpy still runs the Python loop
    assert a.tolist() == d.tolist()
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_sell_allocator.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'kagg3.core.loop'`.

- [ ] **Step 3: Write `loop.py`**

Create `src/kagg3/core/loop.py`:

```python
"""A bounded, fixed-count loop the planner can run on either backend.

numpy runs a Python loop. The simulator installs `jax.lax.fori_loop` through
`install` when it is imported (see sim/rollout.py), so a body that runs a
hundred times compiles once instead of being unrolled a hundred times inside
the day scan. `core` itself never imports jax: the submission's
forbidden-import gate parses every shipped file for import statements, and
the numpy path must stay numpy even when the simulator is loaded in the same
process (the equivalence tests do exactly that).
"""

from __future__ import annotations

import numpy as np

_impl = None


def install(fn):
    """`fn(n_iter, body, carry) -> carry`, a traced loop for non-numpy backends."""
    global _impl
    _impl = fn


def repeat(xp, n_iter, body, carry):
    """`carry = body(carry)` repeated `n_iter` times."""
    if _impl is None or xp is np:
        for _ in range(n_iter):
            carry = body(carry)
        return carry
    return _impl(n_iter, body, carry)
```

In `src/kagg3/sim/rollout.py`, after the imports, add:

```python
from ..core import loop as _loop

_loop.install(lambda n, body, carry: jax.lax.fori_loop(0, n, lambda i, c: body(c), carry))
```

- [ ] **Step 4: Write `sell.py`**

Create `src/kagg3/core/sell.py`:

```python
"""The sell side [HEURISTIC, PLANNER_V3_1 section 1.2].

Two learned values per product: `hold`, what one unit is worth kept until
tomorrow, and `press`, the coins a unit is expected to lose per lot of delay
to opponent sales. Everything else is table arithmetic: the three lots' quote
curves from the projector (town ticks between lots, own earlier lots advancing
the later inventories), and a unit-by-unit greedy that gives each unit to the
lot whose *adjusted* marginal is highest and sells it only if that marginal
clears `hold`.

The adjustment has two parts. Timing pressure: `press * lot_index`. The
externality: a unit sold in lot l moves every later lot's start up by one,
which changes a later lot holding n units by `price[start + n] - price[start]`
(telescoping) -- charged to lot l so the greedy does not undercut its own
later sales. Verified opponent-free fact: selling later is weakly better on
every town-consumed product and exactly indifferent for fertilizer; with no
town and no pressure every lot quotes alike and ties fall to the earliest.

Array-agnostic; the loop goes through core.loop so the simulator traces it.
"""

from __future__ import annotations

from .. import spec
from . import loop
from . import ops as O
from . import projector as PJ

N_LOTS = len(O.SELL_TURNS)
#: Reservation that sells every unit whatever its adjusted marginal (day 29:
#: the terminal value of anything unsold is exactly zero [LAW, 0.4]).
LIQUIDATE = -(1 << 20)


def lot_inventories(xp, mkt_inv, shops):
    """int[3, 9]: opponent-free market inventory when each lot resolves,
    before any own sale that day."""
    return xp.stack([PJ.projected_inv(xp, mkt_inv, shops, t) for t in O.SELL_TURNS])


def _price_at(xp, price_table, pos):
    """price_table[p, pos[l, p]] for a [3, 9] position array."""
    i32 = xp.int32
    idx = xp.clip(pos - spec.PRICE_TABLE_LO, 0, spec.PRICE_TABLE_N - 1)
    pid = xp.arange(spec.N_PRODUCTS, dtype=i32)[None, :]
    return price_table[pid, idx]


def adjusted_marginals(xp, price_table, inv_lots, lots, press):
    """int[3, 9]: what the next unit in each lot is worth, net of timing
    pressure and of the externality on the later lots, given `lots` units
    already allocated."""
    i32 = xp.int32
    before = xp.cumsum(lots, axis=0) - lots                 # own units in earlier lots
    start = inv_lots + before                               # each lot's first-unit inventory
    nxt = _price_at(xp, price_table, start + lots)          # quote of the next unit
    drop = _price_at(xp, price_table, start + lots) - _price_at(xp, price_table, start)   # <= 0 per lot
    # externality on later lots: sum of their drops, exclusive of this lot
    later = xp.flip(xp.cumsum(xp.flip(drop, 0), 0), 0) - drop
    lot_ix = xp.arange(N_LOTS, dtype=i32)[:, None]
    return nxt - press[None, :] * lot_ix + later


def allocate(xp, price_table, mkt_inv, shops, avail, hold, press):
    """int[3, 9]: units of each product to sell in each lot.

    K-1 rounds cover a full shed; each round gives at most one unit per
    product to its best adjusted lot, iff that lot's adjusted marginal clears
    the reservation value. Ties: argmax takes the earliest lot.
    """
    i32 = xp.int32
    inv_lots = lot_inventories(xp, mkt_inv, shops)
    lot_ix = xp.arange(N_LOTS, dtype=i32)[:, None]
    avail = avail.astype(i32)
    hold = hold.astype(i32)
    press = press.astype(i32)

    def body(lots):
        adj = adjusted_marginals(xp, price_table, inv_lots, lots, press)
        best = xp.argmax(adj, axis=0)
        best_adj = xp.max(adj, axis=0)
        take = (xp.sum(lots, axis=0) < avail) & (best_adj >= hold)
        return lots + ((lot_ix == best[None, :]) & take[None, :]).astype(i32)

    return loop.repeat(xp, PJ.K - 1, body, xp.zeros((N_LOTS, spec.N_PRODUCTS), i32))


def best_lot(xp, price_table, mkt_inv, shops, lots, press):
    """int[9]: the lot whose adjusted marginal is highest after `lots` --
    where a unit sold regardless of `hold` (a forced overflow sale) goes."""
    adj = adjusted_marginals(xp, price_table, lot_inventories(xp, mkt_inv, shops), lots,
                             press.astype(xp.int32))
    return xp.argmax(adj, axis=0)
```

- [ ] **Step 5: Run the tests**

Run: `python -m pytest tests/test_sell_allocator.py -q` — Expected: PASS (7 tests). If `test_greedy_is_close_to_the_exhaustive_split` fails on one product, print the split and the best split; a gap above 3% means the externality term is wrong, not that the bound is too tight.
Run: `ruff check src tests`.

- [ ] **Step 6: Commit**

```bash
git add src/kagg3/core/loop.py src/kagg3/core/sell.py src/kagg3/sim/rollout.py tests/test_sell_allocator.py
git commit -m "Add the reservation-value lot allocator and a loop the simulator can trace"
```

---

### Task 3: Wire the sell side into the planner; delete `sell_qty`, `sell_min`, `sell_lots` (§1.2)

**Files:**
- Modify: `src/kagg3/core/plan.py` (`Macro`, the sale block of `build_day`, `_market`), `src/kagg3/core/brain.py` (`decide`), `src/kagg3/es/archetypes.py` (`lots` knob)
- Modify tests: `tests/test_budget_order.py::_macro`, `tests/test_task_priority.py::_macro` (drop the three fields), `tests/test_day29_endgame.py`, `tests/test_fert_reserved.py`, `tests/test_overflow_forced_sale.py`
- Delete: `tests/test_sell_head.py` (Task 1's `test_genome_retype.py` imports `_obs` from it — move that helper into `test_genome_retype.py` first)
- Test: `tests/test_sell_side.py`

**Interfaces:**
- Consumes: `sell.allocate`, `sell.best_lot`, `avail` (net of reservations), `terminal`, `forced` (Phase 0's overflow sale), `price_table`, `view.mkt_inv`, `view.shops`.
- Produces: `build_day` locals `hold` (terminal → `sell.LIQUIDATE`), `lots` (int[3, 9]); `_market(xp, wheat_buy, fert_buy, seed_buy, a_buy, a_kind, buy_land, lots, n_hire)` — no `macro`, no `terminal`, no `s_qty`. `Macro` loses `sell_qty`, `sell_min`, `sell_lots`.

**Background.** The sale becomes: reservations (0.7, Phase 0) → `allocate` with `hold` (`sell.LIQUIDATE`, a large negative, on the terminal day: the terminal value of anything unsold is exactly zero, and the gate must not be the adjusted marginal, which can be ≤ 0 under pressure) → 0.9's forced overflow units appended to `best_lot` → rows. Day-29 liquidation is therefore `hold = LIQUIDATE` through the same allocator, which places lots by pressure and town ticks; on a town with no shops every lot quotes alike and the earliest wins the tie — the Phase-0 test that pinned "everything in the last lot" is updated to the allocator's answer.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_sell_side.py`:

```python
"""The planner's sale is the reservation-value allocator (PLANNER_V3_1 1.2)
folded with the Phase-0 laws: feed wheat and fertilizer reservations, the
forced overflow sale, and day-29 liquidation at zero reservation.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, "src")

import numpy as np
from test_budget_order import _macro

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

TABLE = spec.build_price_table()


def _view(shed, day=3, shops=None, geese_hungry=0):
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_cons = z.copy()
    kind[:geese_hungry] = spec.KIND_COOP
    occ[:geese_hungry] = 0
    t_cons[:geese_hungry] = 1
    sh = np.zeros(spec.N_ITEMS, np.int32)
    for i, n in shed.items():
        sh[i] = n
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(),
        t_cons=t_cons, t_yield=z.copy(), t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=sh, seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(0), nquad=np.int32(1),
        price=np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32),
        shops=np.zeros(spec.N_SHOPS, np.int32) if shops is None else shops)


def _sells(view, macro):
    """{turn: {product: qty}}."""
    op, arg, qty = P.build_day(np, view, macro, TABLE)[3:6]
    out = {}
    for t in O.SELL_TURNS:
        for s in range(spec.MAX_MARKET_ORDERS):
            if int(op[t, s]) == O.MO_SELL:
                out.setdefault(t, {})[int(arg[t, s])] = int(qty[t, s])
    return out


def _total(sells, product):
    return sum(d.get(product, 0) for d in sells.values())


def test_zero_reservation_sells_the_shed():
    sells = _sells(_view({spec.I_WOOL: 12, spec.I_EGG: 7}), _macro(hold=np.zeros(9, np.int32)))
    assert _total(sells, spec.I_WOOL) == 12 and _total(sells, spec.I_EGG) == 7


def test_default_reservation_holds_everything():
    assert _sells(_view({spec.I_WOOL: 12}), _macro()) == {}


def test_reservation_gates_per_product():
    hold = np.full(9, 10_000, np.int32)
    hold[spec.I_EGG] = 0
    sells = _sells(_view({spec.I_WOOL: 12, spec.I_EGG: 7}), _macro(hold=hold))
    assert _total(sells, spec.I_EGG) == 7 and _total(sells, spec.I_WOOL) == 0


def test_pressure_moves_a_yarn_town_sale_to_the_first_lot():
    shops = np.zeros(spec.N_SHOPS, np.int32)
    shops[spec.SHOP_NAMES.index("YARN_STORE")] = 1
    view = _view({spec.I_WOOL: 12}, shops=shops)
    late = _sells(view, _macro(hold=np.zeros(9, np.int32)))
    assert late.get(O.SELL_TURNS[-1], {}).get(spec.I_WOOL, 0) > late.get(O.SELL_TURNS[0], {}).get(spec.I_WOOL, 0)
    press = np.zeros(9, np.int32)
    press[spec.I_WOOL] = 1000
    early = _sells(view, _macro(hold=np.zeros(9, np.int32), press=press))
    assert early[O.SELL_TURNS[0]][spec.I_WOOL] == 12


def test_feed_wheat_stays_reserved():
    view = _view({spec.I_WHEAT: 10}, geese_hungry=4)
    sells = _sells(view, _macro(hold=np.zeros(9, np.int32)))
    assert _total(sells, spec.I_WHEAT) == 6


def test_day_29_liquidates_at_zero_reservation():
    sells = _sells(_view({spec.I_WOOL: 12, spec.I_MELON: 3}, day=29), _macro())   # default hold 10,000 is void
    assert _total(sells, spec.I_WOOL) == 12 and _total(sells, spec.I_MELON) == 3


def test_day_29_liquidates_under_pressure_too():
    # a pressure gene above every quote makes every adjusted marginal negative;
    # the law still sells the whole shed [0.4]
    press = np.full(9, 5000, np.int32)
    sells = _sells(_view({spec.I_WOOL: 12, spec.I_FERT: 4}, day=29), _macro(press=press))
    assert _total(sells, spec.I_WOOL) == 12 and _total(sells, spec.I_FERT) == 4
    assert set(sells) == {O.SELL_TURNS[0]}         # everything in the first lot


def test_forced_overflow_units_join_the_best_lot():
    # 95 in the shed, 20 harvested tonight, everything held: 15 must go anyway
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    kind[:20] = spec.KIND_PLANT
    occ = z - 1
    occ[:20] = spec.I_TOMATO
    t_yield = z.copy()
    t_yield[:20] = 1
    sh = np.zeros(spec.N_ITEMS, np.int32)
    sh[spec.I_TOMATO], sh[spec.I_WHEAT] = 90, 5
    inv = np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32)
    inv[spec.I_TOMATO] = spec.MARKET_I0 + 40_000
    view = P.DayView(
        day=np.int32(13), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(), t_cons=z.copy(),
        t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=sh, seeds=np.zeros(spec.N_CROPS, np.int32), money=np.int32(1000), nquad=np.int32(1),
        price=np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32),
        mkt_inv=inv, shops=np.zeros(spec.N_SHOPS, np.int32))
    sells = _sells(view, _macro(n_hire=np.int32(spec.MAX_HANDS)))
    assert _total(sells, spec.I_TOMATO) == 15 and _total(sells, spec.I_WHEAT) == 0


def test_macro_has_no_sell_decisions():
    for name in ("sell_qty", "sell_min", "sell_lots"):
        assert name not in P.Macro._fields
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_sell_side.py -q`
Expected: FAIL — the default macro (old `sell_qty = 0`) sells nothing in `test_zero_reservation_sells_the_shed`; `test_macro_has_no_sell_decisions` fails on `sell_qty`.

- [ ] **Step 3: Replace the sale block**

In `build_day`, keep the reservation lines (`wheat_reserved`, `avail`, the wheat `_set1`, `fert_reserved`, the fertilizer `_set1`) and replace everything from `s_qty = xp.minimum(macro.sell_qty, avail)` through the `_market(...)` call with:

```python
    # ---- the sale [HEURISTIC, 1.2] ----------------------------------------
    # Whether to sell is the reservation value; when is the timing pressure
    # against the projected lot curves. The terminal value of anything unsold
    # on day 29 is exactly zero, so the reservation is void there [LAW, 0.4]
    # -- `LIQUIDATE`, not 0: an adjusted marginal (net of pressure and the
    # externality) can be negative, and day 29 must sell regardless.
    hold = xp.where(terminal, SELL.LIQUIDATE, macro.hold).astype(i32)
    lots = SELL.allocate(xp, price_table, view.mkt_inv, view.shops, avail, hold, macro.press)
    s_qty = xp.sum(lots, axis=0).astype(i32)
```

then keep Phase 0's forced-sale block unchanged up to (but excluding) its final line `s_qty = (s_qty + forced).astype(i32)`, and replace that line and the market call with:

```python
    # Forced overflow units bypass the reservation and take the lot whose
    # adjusted marginal is highest after the value-gated allocation [0.9].
    forced_lot = SELL.best_lot(xp, price_table, view.mkt_inv, view.shops, lots, macro.press)
    lot_ix = xp.arange(SELL.N_LOTS, dtype=i32)[:, None]
    lots = (lots + (lot_ix == forced_lot[None, :]).astype(i32) * forced[None, :]).astype(i32)

    mkt = _market(xp, wheat_buy, fert_bought, seed_buy, a_buy, a_kind, buy_land, lots, n_hire)
    return (unit_op, unit_a, unit_q) + mkt
```

Add `from . import sell as SELL` to the imports. Rewrite `_market`'s signature and SELL section:

```python
def _market(xp, wheat_buy, fert_buy, seed_buy, a_buy, a_kind, buy_land, lots, n_hire):
    """Fixed market schedule (see the module docstring). `lots` is int[3, 9]:
    units of each product in each SELL lot, already gated and reserved."""
```

(the hire and BUY blocks are unchanged), ending with:

```python
    pad = xp.zeros(MO - spec.N_PRODUCTS, i32)
    arg_row = xp.concatenate([xp.arange(spec.N_PRODUCTS, dtype=i32), pad])
    for k, turn in enumerate(O.SELL_TURNS):
        lot = lots[k].astype(i32)
        op = _row(xp, op, turn,
                  xp.concatenate([xp.where(lot > 0, O.MO_SELL, O.MO_NONE).astype(i32), pad]))
        arg = _row(xp, arg, turn, arg_row)
        qty = _row(xp, qty, turn, xp.concatenate([lot, pad]))
    return op, arg, qty
```

Delete `sell_qty`, `sell_min`, `sell_lots` from `Macro`; in `brain.decide` delete the `sell_qty = ...` line, the `unit = lambda ...`, `sell_min = ...`, `n_turns = ...`, `sell_lots = ...` lines and the three fields from the `P.Macro(...)` call. In `archetypes.py` remove the `lots` knob from `KNOBS`, `_NAMED`, `sample_archetype`, and the line writing `gb4`.

- [ ] **Step 4: Update the tests that used the deleted fields**

- `tests/test_genome_retype.py`: copy `test_sell_head.py`'s `_obs()` helper into it (rename the import away); then delete `tests/test_sell_head.py`.
- `tests/test_budget_order.py::_macro`, `tests/test_task_priority.py::_macro`: remove `sell_qty=`, `sell_min=`, `sell_lots=`.
- `tests/test_day29_endgame.py`: in `_greedy_macro` drop `sell_min=` and `sell_lots=`; replace `test_day_29_liquidates_the_whole_shed_in_the_last_lot` with a total-per-product check (`{WHEAT: 10, EGG: 7, MELON: 3, FERT: 4}` summed over all SELL turns), and in `test_day_28_is_not_terminal` keep the "no SELL anywhere" assertion (the default `hold` of 10,000 holds everything).
- `tests/test_fert_reserved.py`: replace `_sell_all_fert()` with `hold=np.zeros(spec.N_PRODUCTS, np.int32)` in every `_macro(...)` call and delete the helper.
- `tests/test_overflow_forced_sale.py`: in `test_forced_sale_bypasses_the_price_gate` replace `sell_min=np.full(...)` with nothing (the default `hold` already gates everything) and rename it `test_forced_sale_bypasses_the_reservation`.

- [ ] **Step 5: Run the tests and the full suite**

Run: `python -m pytest tests/test_sell_side.py tests/test_day29_endgame.py tests/test_fert_reserved.py tests/test_overflow_forced_sale.py tests/test_genome_retype.py -q` — Expected: PASS.
Run: `python -m pytest -q` — Expected: all pass, including the sim-equivalence gates (the rows still land only on turns 2/10/18).
Run: `python scripts/bench_sim.py` here and on the Task-2 commit (`git worktree add /tmp/claude-0/kagg3-t2 HEAD~1`); record both in the commit message; the `fori_loop` body is small, so the delta should be within noise.
Run: `ruff check src tests`.

- [ ] **Step 6: Commit**

```bash
git add -A src/kagg3/core/plan.py src/kagg3/core/brain.py src/kagg3/es/archetypes.py tests/
git commit -m "Sell by reservation value and timing pressure; delete the sell quantity, gate and lot genes"
```

---

### Task 4: Feeding as a value decision (§1.4)

**Files:**
- Modify: `src/kagg3/core/plan.py` — `build_day` survival section (feed), the clamp section's `feed_value`/`feed_rank`/`want_feed` lines; the `inv_buy`/`buy_q`/`wheat_cum`/`fert_cum` lines move up
- Test: `tests/test_feed_value.py`

**Interfaces:**
- Consumes: `valuation.animal_value`, `valuation.next_fire_after`, `projector.buy_quotes`, `_rank_by`, `feed_want` (hungry or bank-fire, Phase 1), `an_first/an_int/an_prod`, `a_idx`, `view.t_bank`.
- Produces: `build_day` locals, all defined **before** the budget walk: `inv_buy`, `buy_q` (int[9, K]), `wheat_cum`, `fert_cum`, `feed_value` (int[100], capped at cost, bank included), `feed_rank0` (rank among `feed_want`), `feed_price` (int[100]), `feed_pass` (bool[100]), `feed_rank` (rank among `feed_pass`), `feed_need = sum(feed_pass)`. The clamp section keeps `want_feed = feed_pass & (feed_rank < wheat_avail)`.

**Background (§1.4).** Feed a hungry animal iff its remaining conservatively-projected sellable production — capped at replacement cost, **including a pending CARE bank** cashable at a monetizable fire (payout needs fed-on-fire-day and the bank is wiped at every fire, so a feed test that ignores it destroys a bonus 0.11 paid labour to build) — exceeds the feed's engine-curve wheat price: the hour-0 quote for wheat already in the shed, the curve price for wheat that must be bought. An animal that fails is not fed and, with 0.8, not replaced: the exact exit rule that prices the buy→starve→re-buy loop. Feeds that pass are survival feeds and join the mandatory tier (0.5) through `want_feed & must_feed`, unchanged.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_feed_value.py`:

```python
"""A hungry animal is fed iff what it can still sell -- capped at what a
replacement costs, plus any pending CARE bank a fed fire day would cash --
beats the wheat's engine-curve price (PLANNER_V3_1 section 1.4). One that
fails is not fed and, with 0.8, not replaced.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, "src")

import numpy as np
from test_budget_order import _macro

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P
from kagg3.core import projector as PJ

TABLE = spec.build_price_table()
BASE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)


def _farm(day, geese, *, wheat=10, egg=50, fert=100, t_bank=0, money=3000):
    """`geese` hungry geese placed on day 0 at the head of the sweep."""
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    kind[:geese] = spec.KIND_COOP
    occ = z - 1
    occ[:geese] = 0
    t_cons = z.copy()
    t_cons[:geese] = 1
    bank = z.copy()
    bank[:geese] = t_bank
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_WHEAT] = wheat
    price = BASE.copy()
    price[spec.I_EGG], price[spec.I_FERT] = egg, fert
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(),
        t_cons=t_cons, t_yield=z.copy(), t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=shed, seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(money), nquad=np.int32(1), price=price, t_bank=bank)


def _counts(view, **macro):
    plan = P.build_day(np, view, _macro(**macro), TABLE)
    unit_op, op, arg, qty = plan[0], plan[3], plan[4], plan[5]
    row = O.TURN_BUY
    wheat = sum(int(qty[row, s]) for s in range(spec.MAX_MARKET_ORDERS)
                if int(op[row, s]) == O.MO_BUY_PRODUCT and int(arg[row, s]) == spec.I_WHEAT)
    animals = int(qty[row][op[row] == O.MO_BUY_ANIMAL].sum())
    return int((unit_op == O.OP_FEED).sum()), wheat, animals


def test_a_paying_animal_is_fed():
    # day 27 goose: one egg (50) and one fertilizer (100) left, wheat costs 25
    assert _counts(_farm(27, 1))[0] == 1


def test_a_worthless_animal_is_left_to_escape_and_not_replaced():
    # 10 + 10 = 20 coins left in it, wheat costs 25: no feed, no wheat, no goose
    assert _counts(_farm(27, 1, egg=10, fert=10, wheat=0), animal_count=np.int32(0)) == (0, 0, 0)


def test_a_pending_bank_counts_toward_the_value():
    # 8 + 8 = 16 < 25 alone; a bank of 2 eggs (16) cashed on day 28 lifts it to 32
    assert _counts(_farm(27, 1, egg=8, fert=8))[0] == 0
    assert _counts(_farm(27, 1, egg=8, fert=8, t_bank=2))[0] == 1


def test_each_bought_feed_is_priced_on_the_curve():
    # 30 geese worth 27 coins each, no wheat in the shed: the curve starts at
    # 26 and rises, so only the feeds whose quote stays below 27 pass
    view = _farm(27, 30, egg=17, fert=10, wheat=0)
    inv1 = PJ.projected_inv(np, view.mkt_inv, view.shops, O.TURN_BUY)
    quotes = PJ.buy_quotes(np, TABLE, inv1)[spec.I_WHEAT]
    expect = int((quotes[:30] < 27).sum())
    assert 0 < expect < 30
    fed, wheat, _ = _counts(view, n_hire=np.int32(spec.MAX_HANDS))
    assert fed == expect and wheat == expect


def test_shed_wheat_is_priced_at_the_hour_zero_quote():
    # the same 30 geese with 30 wheat in the shed: every feed costs 25 < 27
    fed, wheat, _ = _counts(_farm(27, 30, egg=17, fert=10, wheat=30), n_hire=np.int32(spec.MAX_HANDS))
    assert fed == 30 and wheat == 0


def test_feed_value_agrees_across_backends():
    import jax
    import jax.numpy as jnp
    view, macro = _farm(27, 30, egg=17, fert=10, wheat=0), _macro(n_hire=np.int32(3))
    a = P.build_day(np, view, macro, TABLE)
    b = P.build_day(jnp, jax.tree_util.tree_map(jnp.asarray, view),
                    jax.tree_util.tree_map(jnp.asarray, macro), jnp.asarray(TABLE))
    for x, y in zip(a, b):
        assert np.array_equal(np.asarray(x), np.asarray(y))
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_feed_value.py -q`
Expected: FAIL — the worthless goose is fed (`1 == 0`), the bank case feeds both ways.

- [ ] **Step 3: Move the buy quotes up and add the value test**

In `build_day`, cut the four lines `inv_buy = ...`, `buy_q = ...`, `wheat_cum = ...`, `fert_cum = ...` (and their comment) out of the budget walk and paste them directly **after** `survival_pays = day < O.LAST_SHED_DAY` — they depend only on the view.

Directly after the line `feed_want = has_animal & (view.t_water == 0) & (must_feed | bank_feed)` add:

```python
    # Feeding as a value decision [EXACT-OPT, 1.4]: feed iff what the animal
    # can still sell -- capped at a replacement's cost, plus a pending CARE
    # bank cashable at a monetizable fire -- beats this feed's wheat price:
    # the hour-0 quote for shed wheat, the curve price for bought wheat. One
    # that fails is left to escape and (0.8) not replaced.
    bank_h = VAL.next_fire_after(xp, view.t_day, an_first, an_int, day - 1)     # first fire with eod >= today
    bank_val = xp.where(bank_h <= O.LAST_SHED_DAY, view.t_bank, 0) * view.price[an_prod]
    feed_value = xp.minimum(
        VAL.animal_value(xp, view.price, view.t_day, view.t_yield, view.t_favail, a_idx, day) + bank_val,
        xp.asarray(spec.ANIMAL_COST)[a_idx]).astype(i32)
    feed_rank0 = _rank_by(xp, feed_want, feed_value)
    shed_wheat = view.shed[spec.I_WHEAT]
    feed_price = xp.where(feed_rank0 < shed_wheat, view.price[spec.I_WHEAT],
                          buy_q[spec.I_WHEAT][xp.clip(feed_rank0 - shed_wheat, 0, PJ.K - 1)])
    feed_pass = feed_want & (feed_value > feed_price)
    feed_rank = _rank_by(xp, feed_pass, feed_value)
```

Change `feed_need = xp.sum(feed_want.astype(i32))` to `feed_need = xp.sum(feed_pass.astype(i32))`.

In the clamp section delete the Phase-1 `feed_value = xp.minimum(...)` and `feed_rank = _rank_by(xp, feed_want, feed_value)` lines and set:

```python
    want_feed = feed_pass & (feed_rank < wheat_avail)
```

- [ ] **Step 4: Run the tests and the full suite**

Run: `python -m pytest tests/test_feed_value.py -q` — Expected: PASS (6 tests).
Run: `python -m pytest -q` — Expected: all pass. `test_feed_rationing.py` and `test_feed_care_cadence.py` use prices where every goose clears 25 coins.
Run: `ruff check src tests`.

- [ ] **Step 5: Commit**

```bash
git add src/kagg3/core/plan.py tests/test_feed_value.py
git commit -m "Feed an animal only when its remaining value beats the wheat's curve price"
```

---

### Task 5: The marginal-unit budget; delete `order` (§1.3)

**Files:**
- Create: `src/kagg3/core/budget.py`
- Modify: `src/kagg3/core/valuation.py` (+`new_plant_units`, +`remaining_plant_units`), `src/kagg3/core/projector.py` (+`daily_town_units`, +`inv_at_day`), `src/kagg3/core/plan.py` (`GROW_ONE`, `_cum_at`, `_pipeline_units`, the budget walk, `Macro.order`, the `B_*` comment), `src/kagg3/core/brain.py` (`GROW_ONE` alias, drop the `order` decode), `src/kagg3/core/policy.py` (nothing)
- Delete: `tests/test_learned_order.py`
- Rewrite: `tests/test_budget_order.py` (keep `_view`, `_macro`, `_buy_qty`, `PURSE`), `tests/test_hire_bill.py` (drop `order=`)
- Modify fixtures: `tests/test_task_priority.py::_macro` (drop `order=`)
- Test: `tests/test_budget_greedy.py`, `tests/test_seed_horizon.py`

**Interfaces:**
- Produces: `budget.N_LISTS = 8` with `L_WHEAT, L_FERT, L_SEED0, L_ANIMAL = 0, 1, 2, 7`; `budget.grant(xp, values, costs, wants, purse) -> int[8]` (`values`, `costs` int[8, K]; `wants` int[8]); `valuation.new_plant_units(xp, crop, day) -> int` (units a crop planted today yields by the horizon, unfertilized, watered every in-window day); `valuation.remaining_plant_units(xp, crop, t_day, day) -> int` (the same for a tile planted on `t_day`, counting only fires after `day`; equals `new_plant_units` when `t_day == day`); `projector.daily_town_units(xp, shops) -> int[9]` (units the town removes per day: six shop ticks plus the centre); `projector.inv_at_day(xp, mkt_inv, shops, days_ahead) -> int[9]` (hour-0 inventory advanced `days_ahead` days of town drain, opponent-free, `days_ahead` a scalar or int[9]); `plan._pipeline_units(xp, view, is_plant, has_animal, day) -> int[9]` (own supply already committed by the horizon: planted tiles, placed animals' fires, one fertilizer per animal-day, the shed); `build_day` locals `inv_h` (int[9], the sales-window inventory each candidate list is priced from); `plan.GROW_ONE = 256` (`brain.GROW_ONE` becomes an alias); `plan._cum_at(xp, cum, k)` (vectorised `_cum_take`); `plan.STREAM_MAX = 32`, `plan._stream_rev(xp, price_table, inv0, u, k) -> int[K]` (coins the k-th block of `u` units fetches, `k*u` units down the curve from `inv0`; `u <= STREAM_MAX`); `build_day` locals `purse`, `u_new` (int[5]), `ub_coins` (scalar: `ub_units * price[a_prod] + ub_fert * price[I_FERT] - ub_feeds * price[I_WHEAT]`), `n_buy` (int[8]). `Macro` loses `order`.
- `feed_rank` (Task 4) and `fert_rank` (Phase 1, moved up in this task) must be defined before the walk.

**Background (§1.3).** Whole-category grants are structurally suboptimal — feed value differs per animal, the tenth seed is worth less than the first, land is indivisible. Budget over **marginal purchase candidates**: one wheat per passing feed (value: 1.4's table), one fertilizer per application (0.11's table), the k-th seed of each crop (projected clipped units × projected price × grow multiplier, declining in k because the k-th planting's units sell further down the curve), the k-th animal (0.2's stream × grow multiplier), land (the learned logit, gated by 0.3). Grant greedily by value per coin down the purse, engine-curve priced. Within each list the ratio is non-increasing (values fall, costs rise), so "best ratio first" is a threshold: the smallest `tau` whose total cost fits, found by bisection through `loop.repeat`, then up to three lumpy top-ups. Land is compared two ways ahead of the greedy — grant if affordable, else skip — because its value is a logit, not coins; the gene owns its timing. Zero-value candidates are never bought. Labelled a documented greedy approximation: purchases still compete for labour, tiles and shed room outside the model.

**Sales-window pricing (gap review 2026-08-24, folded in).** A seed's units do not sell today: they sell on the crop's first harvest day into a market the town has been draining meanwhile and the farm's own pipeline has been filling. Pricing them off today's hour-0 inventory ranks crops by the base-price table, which the forum sweep measured as almost exactly backwards once the town's per-product demand is counted (`docs/FORUM_RESEARCH.md` §3.1: strawberry $100k into the hole vs $4k dumped; melon has no shop sink and the centre eats 30 a season). The correction is table arithmetic, not learning: each candidate list is priced from `inv_h[p] = inv_at_day(mkt_inv, shops, first_p) + pipeline[p]`, where `first_p` is the product's first fire (`CROP_FIRST_YIELD_DAY[c]`, `a_first` for the animal's product, 0 for fertilizer, which the town never eats) and `pipeline[p]` is the supply the farm has already committed by the horizon. Measured on the default table (direct table reads, 2026-08-24, one of each shop, blank board, day 0): the ratio of a first seed's value to its cost moves wheat 9.7 → 13.2, strawberry 4.7 → 10.1, tomato 4.6 → 5.8, melon 18.8 → 20.1 — the town's drain rewards the products it eats, and **melon still ranks first opponent-free on a fresh board**; what un-ranks it is its own pipeline: with 72 melon units already growing the next seed reads 15.6, with 150 it reads 3.5 (6 units at inventory `I0 + 140` fetch 282 coins) — i.e. the projection says a *few* melons pay and a field of them does not, which is the marginal behaviour §1.3 wants. The opponent's supply (kagg2's 76-unit day-10 dump in the autopsy) stays invisible to the projection by construction and remains `press`/`grow_mult`'s job [LEARNED]; the pipeline count is conservative (it includes supply landing after the candidate's own harvest and assumes daily watering), so a gluttable product is under-, never over-valued. Labelled [HEURISTIC]; the multi-day drift the spec defers to genes is untouched — this is the town's *deterministic* part of it only.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_budget_greedy.py`:

```python
"""The marginal-unit budget (PLANNER_V3_1 section 1.3): candidates from eight
monotone lists granted by value per coin down the purse, lumpy leftovers
topped up, wants and zero values respected.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, "src")

import numpy as np

from kagg3 import spec
from kagg3.core import budget as B
from kagg3.core import ops as O
from kagg3.core import projector as PJ
from kagg3.core import valuation as V

K = PJ.K


def test_single_list_buys_the_affordable_prefix():
    values = np.zeros((B.N_LISTS, K), np.int32)
    costs = np.ones((B.N_LISTS, K), np.int32)
    wants = np.zeros(B.N_LISTS, np.int32)
    values[0, :4], costs[0, :4], wants[0] = [100, 90, 80, 70], [10, 11, 12, 13], 4
    assert B.grant(np, values, costs, wants, np.int32(33)).tolist() == [3, 0, 0, 0, 0, 0, 0, 0]
    assert B.grant(np, values, costs, wants, np.int32(1000)).tolist() == [4, 0, 0, 0, 0, 0, 0, 0]
    assert B.grant(np, values, costs, wants, np.int32(0)).tolist() == [0] * 8


def test_two_lists_interleave_by_value_per_coin():
    values = np.zeros((B.N_LISTS, K), np.int32)
    costs = np.ones((B.N_LISTS, K), np.int32)
    wants = np.zeros(B.N_LISTS, np.int32)
    values[0, :3], costs[0, :3], wants[0] = [50, 40, 30], [10, 10, 10], 3      # ratios 5, 4, 3
    values[7, :3], costs[7, :3], wants[7] = [90, 45, 20], [20, 20, 20], 3      # ratios 4.5, 2.25, 1
    # purse 50: 5 (10) -> 4.5 (20) -> 4 (10) -> 3 (10) = 50
    assert B.grant(np, values, costs, wants, np.int32(50)).tolist() == [3, 0, 0, 0, 0, 0, 0, 1]


def test_a_lumpy_item_that_does_not_fit_is_skipped_for_cheaper_ones():
    values = np.zeros((B.N_LISTS, K), np.int32)
    costs = np.ones((B.N_LISTS, K), np.int32)
    wants = np.zeros(B.N_LISTS, np.int32)
    values[7, :1], costs[7, :1], wants[7] = [1000], [300], 1                  # ratio 3.3, unaffordable
    values[2, :5], costs[2, :5], wants[2] = [20, 20, 20, 20, 20], [10] * 5, 5  # ratio 2
    assert B.grant(np, values, costs, wants, np.int32(45)).tolist() == [0, 0, 4, 0, 0, 0, 0, 0]


def test_stream_rev_prices_every_candidate_not_just_a_sheds_worth():
    from kagg3.core import plan as P
    inv0 = np.int32(spec.MARKET_I0)
    k = np.arange(K, dtype=np.int32)
    rev = P._stream_rev(np, spec.build_price_table()[spec.I_MELON], inv0, np.int32(6), k)
    assert rev.shape == (K,)
    assert int(rev[0]) == 6 * 250
    assert np.all(rev[1:] <= rev[:-1]) and int(rev[K - 1]) > 0     # declining, never clipped to zero
    assert int(rev[30]) == sum(int(spec.build_price_table()[spec.I_MELON, inv0 + 180 + m - spec.PRICE_TABLE_LO])
                               for m in range(6))


def test_zero_value_candidates_are_never_bought():
    values = np.zeros((B.N_LISTS, K), np.int32)
    costs = np.ones((B.N_LISTS, K), np.int32)
    wants = np.zeros(B.N_LISTS, np.int32)
    values[2, :3], costs[2, :3], wants[2] = [0, 0, 0], [10, 10, 10], 3
    assert B.grant(np, values, costs, wants, np.int32(1000)).tolist() == [0] * 8


def test_total_cost_never_exceeds_the_purse():
    rng = np.random.default_rng(0)
    for _ in range(50):
        values = np.zeros((B.N_LISTS, K), np.int32)
        costs = np.ones((B.N_LISTS, K), np.int32)
        wants = rng.integers(0, 20, B.N_LISTS).astype(np.int32)
        for i in range(B.N_LISTS):
            values[i] = np.sort(rng.integers(0, 500, K))[::-1]
            costs[i] = np.sort(rng.integers(1, 60, K))
        purse = np.int32(rng.integers(0, 2000))
        n = B.grant(np, values, costs, wants, purse)
        assert np.all(n <= wants) and np.all(n >= 0)
        spent = sum(int(costs[i, :n[i]].sum()) for i in range(B.N_LISTS))
        assert spent <= int(purse)


def test_new_plant_units_at_the_spec_numbers():
    I = np.int32
    assert int(V.new_plant_units(np, I(spec.I_WHEAT), I(0))) == 4        # born 1, watered ages 2, 3, 4
    assert int(V.new_plant_units(np, I(spec.I_MELON), I(0))) == 6        # saturates
    assert int(V.new_plant_units(np, I(spec.I_TOMATO), I(0))) == 4       # four fires
    assert int(V.new_plant_units(np, I(spec.I_WHEAT), I(25))) == 3       # deadline harvest at age 3
    assert int(V.new_plant_units(np, I(spec.I_WHEAT), I(27))) == 0       # cannot mature
    assert int(V.new_plant_units(np, I(spec.I_TOMATO), I(19))) == 2      # fires 27, 28


def test_grant_agrees_across_backends():
    import jax.numpy as jnp
    rng = np.random.default_rng(1)
    values = np.sort(rng.integers(0, 500, (B.N_LISTS, K)), axis=1)[:, ::-1].astype(np.int32)
    costs = np.sort(rng.integers(1, 60, (B.N_LISTS, K)), axis=1).astype(np.int32)
    wants = rng.integers(0, 30, B.N_LISTS).astype(np.int32)
    a = B.grant(np, values, costs, wants, np.int32(700))
    b = B.grant(jnp, jnp.asarray(values), jnp.asarray(costs), jnp.asarray(wants), jnp.int32(700))
    assert a.tolist() == np.asarray(b).tolist()
```

Create `tests/test_seed_horizon.py` (the numbers below are direct reads of `spec.build_price_table()` on the default market, taken 2026-08-24; if the table changes, re-derive them from the table, never from the planner):

```python
"""Sales-window pricing of purchase candidates (PLANNER_V3_1 section 1.3,
gap review 2026-08-24): a seed's units are priced at the inventory the town
will have drained to by the crop's first harvest day, plus the supply the
farm has already committed. Opponent-free by construction.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, "src")

import numpy as np

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P
from kagg3.core import projector as PJ
from kagg3.core import valuation as V
from test_budget_order import _macro, _view

I0 = spec.MARKET_I0
ONES = np.ones(spec.N_SHOPS, np.int32)


def test_daily_town_units_is_six_shop_ticks_plus_the_centre():
    assert PJ.daily_town_units(np, np.zeros(spec.N_SHOPS, np.int32)).tolist() == [1] * 8 + [0]
    assert PJ.daily_town_units(np, ONES).tolist() == [31, 19, 13, 25, 1, 13, 19, 13, 0]


def test_inv_at_day_drains_per_product_and_takes_a_vector_of_days():
    inv = np.full(spec.N_PRODUCTS, I0, np.int32)
    assert int(PJ.inv_at_day(np, inv, ONES, np.int32(10))[spec.I_STRAWBERRY]) == I0 - 250
    days = np.arange(spec.N_PRODUCTS, dtype=np.int32)
    out = PJ.inv_at_day(np, inv, ONES, days)
    assert out.tolist() == (I0 - days * np.array([31, 19, 13, 25, 1, 13, 19, 13, 0])).tolist()
    assert int(PJ.inv_at_day(np, inv, ONES, np.int32(20))[spec.I_FERT]) == I0     # no town demand


def test_remaining_plant_units_counts_only_future_fires():
    I = np.int32
    assert int(V.remaining_plant_units(np, I(spec.I_STRAWBERRY), I(0), I(0))) == 4    # fires 10, 12, 14, 16
    assert int(V.remaining_plant_units(np, I(spec.I_STRAWBERRY), I(0), I(11))) == 3   # 12, 14, 16 remain
    assert int(V.remaining_plant_units(np, I(spec.I_STRAWBERRY), I(0), I(20))) == 0
    assert int(V.remaining_plant_units(np, I(spec.I_WHEAT), I(0), I(3))) == 4         # unharvested until age 4
    for c in range(spec.N_CROPS):
        for d in (0, 9, 17, 25):
            assert int(V.remaining_plant_units(np, I(c), I(d), I(d))) == int(V.new_plant_units(np, I(c), I(d)))


def _seed_buys(view, macro):
    op, arg, qty = P.build_day(np, view, macro)[3:6]
    return {int(arg[O.TURN_BUY, s]): int(qty[O.TURN_BUY, s]) for s in range(spec.MAX_MARKET_ORDERS)
            if int(op[O.TURN_BUY, s]) == O.MO_BUY_SEED}


def test_the_towns_drain_prices_the_first_harvest_day():
    # one of each shop, blank board, day 0: strawberry's four units sell at
    # I0 - 250 (1,010 coins, ratio 10.1) and melon's six at I0 - 10 (1,611,
    # ratio 20.1) -- opponent-free, melon still ranks first on a fresh board
    view = _view(1000)._replace(shops=ONES)
    macro = _macro(plant_target=np.array([0, 0, 0, 30, 30], np.int32))
    seeds = _seed_buys(view, macro)
    assert seeds.get(spec.I_MELON, 0) == 12 and seeds.get(spec.I_STRAWBERRY, 0) == 0


def test_own_pipeline_un_ranks_a_gluttable_crop():
    # the same board with 25 melon tiles already growing (150 units by day
    # 10): the next melon seed's six units sell at I0 + 140 for 282 coins
    # (ratio 3.5) and ten strawberries take the purse instead
    view = _view(1000)._replace(shops=ONES)
    kind, occ = view.kind.copy(), view.occ.copy()
    kind[:25], occ[:25] = spec.KIND_PLANT, spec.I_MELON
    view = view._replace(kind=kind, occ=occ)
    macro = _macro(plant_target=np.array([0, 0, 0, 30, 30], np.int32))
    seeds = _seed_buys(view, macro)
    assert seeds.get(spec.I_STRAWBERRY, 0) == 10 and seeds.get(spec.I_MELON, 0) == 0


def test_pipeline_units_counts_tiles_animals_fert_and_the_shed():
    view = _view(0)
    kind, occ, t_day = view.kind.copy(), view.occ.copy(), view.t_day.copy()
    kind[:3], occ[:3] = spec.KIND_PLANT, spec.I_STRAWBERRY                 # 3 x 4 units
    kind[3], occ[3] = spec.KIND_COOP, 0                                      # a goose placed day 0
    shed = view.shed.copy()
    shed[spec.I_WOOL] = 7
    view = view._replace(kind=kind, occ=occ, t_day=t_day, shed=shed)
    is_plant = view.kind == spec.KIND_PLANT
    has_animal = (view.kind == spec.KIND_COOP) | (view.kind == spec.KIND_PASTURE)
    pipe = P._pipeline_units(np, view, is_plant, has_animal, np.int32(0))
    goose_eggs = int(V.fires_between(np, np.int32(0), np.int32(spec.ANIMAL_FIRST_YIELD_DAY[0]),
                                     np.int32(spec.ANIMAL_INTERVAL[0]), np.int32(1), np.int32(O.LAST_SHED_DAY)))
    assert int(pipe[spec.I_STRAWBERRY]) == 12
    assert int(pipe[spec.I_EGG]) == goose_eggs
    assert int(pipe[spec.I_FERT]) == O.LAST_SHED_DAY
    assert int(pipe[spec.I_WOOL]) == 7
```

`test_pipeline_units_counts_tiles_animals_fert_and_the_shed` assumes the fixture's `has_animal` predicate matches `build_day`'s (`plan.py`, the `has_animal` local): read it there and mirror it — if the animal on a coop tile is encoded differently (`occ` is the animal *kind*, `0` = goose, per `a_have = view.shed[spec.I_GOOSE + a_kind]`), adjust the fixture, not the planner.

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_budget_greedy.py tests/test_seed_horizon.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'kagg3.core.budget'`; `AttributeError: module 'kagg3.core.projector' has no attribute 'daily_town_units'`.

- [ ] **Step 3: Write `budget.py` and `new_plant_units`**

Create `src/kagg3/core/budget.py`:

```python
"""The buy side [HEURISTIC, PLANNER_V3_1 section 1.3]: marginal purchase
candidates granted greedily by value per coin down the purse.

Eight lists, each up to a shed's worth long, each already ordered so that
value per coin is non-increasing along it -- values fall (the k-th seed's
units sell further down the curve), costs rise (the k-th wheat is quoted
higher). "Best ratio first" across such lists is a threshold: every item
whose ratio is at least tau, for the smallest tau whose total cost fits the
purse. Bisection finds tau; top-ups then spend what the threshold left,
one item per round until nothing fits. Land is not a list: its value is a learned logit, so the
planner compares it two ways ahead of this greedy.

Documented approximation: purchases still compete for labour, tiles and shed
room outside this model.
"""

from __future__ import annotations

from . import loop
from . import projector as PJ

N_LISTS = 8                       # wheat (feeds), fertilizer, five seed crops, animals
L_WHEAT, L_FERT, L_SEED0, L_ANIMAL = 0, 1, 2, 7
RATIO_SHIFT = 10                  # value * 1024 // cost, int32-safe for values < 2**20
VALUE_CAP = (1 << 20) - 1
_NONE = -1


def _cum_at(xp, cum, k):
    """cum[:, k-1] per row (0 where k == 0)."""
    idx = xp.clip(k - 1, 0, cum.shape[1] - 1)
    return xp.where(k > 0, xp.take_along_axis(cum, idx[:, None], axis=1)[:, 0], 0)


def grant(xp, values, costs, wants, purse):
    """int[N_LISTS]: how many of each list to buy.

    values, costs: int[N_LISTS, K]; wants: int[N_LISTS]; purse: int scalar.
    """
    i32 = xp.int32
    values = xp.clip(values.astype(i32), 0, VALUE_CAP)
    costs = xp.maximum(costs.astype(i32), 1)
    wants = wants.astype(i32)
    j = xp.arange(PJ.K, dtype=i32)[None, :]
    live = (j < wants[:, None]) & (values > 0)
    ratio = xp.where(live, (values << RATIO_SHIFT) // costs, _NONE)
    cum = xp.cumsum(costs, axis=1)

    def counts(tau):
        return xp.sum((ratio >= tau).astype(i32), axis=1)

    def total(n):
        return xp.sum(_cum_at(xp, cum, n))

    # smallest tau with total(counts(tau)) <= purse; 31 halvings cover 2**31
    def bisect(carry):
        lo, hi = carry
        mid = (lo + hi) // 2
        fits = total(counts(mid)) <= purse
        return (xp.where(fits, lo, mid + 1), xp.where(fits, mid, hi))
    lo, hi = loop.repeat(xp, 31, bisect, (xp.asarray(0, i32), xp.asarray((1 << 30), i32)))
    n = counts(hi)
    left = purse - total(n)

    # Lumpy top-ups: the threshold is all-or-nothing per ratio level, so equal
    # ratios at the boundary can leave coins unspent. Keep granting the
    # best-ratio next item that still fits until nothing does -- at most one
    # item per round, K rounds cover every list.
    lid = xp.arange(N_LISTS, dtype=i32)

    def topup(carry):
        n, left = carry
        nxt = xp.clip(n, 0, PJ.K - 1)
        c_next = xp.take_along_axis(costs, nxt[:, None], axis=1)[:, 0]
        r_next = xp.take_along_axis(ratio, nxt[:, None], axis=1)[:, 0]
        ok = (n < wants) & (r_next >= 0) & (c_next <= left)
        # argmax takes the first maximum, so ties already fall to the lower
        # list; packing the list into the key would overflow int32 (ratio
        # reaches 2**30).
        key = xp.where(ok, r_next, _NONE)
        best = xp.argmax(key)
        can = key[best] >= 0
        n = n + (lid == best).astype(i32) * can.astype(i32)
        left = left - xp.where(can, c_next[best], 0)
        return n, left
    n, left = loop.repeat(xp, PJ.K, topup, (n, left))
    return n.astype(i32)
```

Append to `src/kagg3/core/valuation.py`:

```python


def new_plant_units(xp, crop, day):
    """int: units a crop planted today yields by LAST_SHED_DAY, unfertilized
    and watered on every in-window day; 0 if it cannot mature in time."""
    ongoing = xp.asarray(spec.CROP_ONGOING)[crop]
    first = xp.asarray(spec.CROP_FIRST_YIELD_DAY)[crop]
    interval = xp.maximum(xp.asarray(spec.CROP_INTERVAL)[crop], 1)
    mxy = xp.asarray(spec.CROP_MAX_YIELD)[crop]
    mxd = xp.asarray(spec.CROP_MAX_YIELD_DAY)[crop]
    ws = xp.asarray(spec.CROP_WINDOW_START)[crop]
    can = day + first <= O.LAST_SHED_DAY
    harvest_age = xp.clip(O.LAST_SHED_DAY - day, first, mxd)
    one = xp.minimum(mxy, 1 + xp.maximum(harvest_age - ws + 1, 0))
    last_h = day + first + (mxy - 1) * interval
    ong = fires_between(xp, day, first, interval, day + 1, xp.minimum(O.LAST_SHED_DAY, last_h))
    return xp.where(can, xp.where(ongoing == 1, ong, one), 0)


def remaining_plant_units(xp, crop, t_day, day):
    """int: units a tile planted on `t_day` still delivers to the shed after
    `day` -- a one-time crop keeps everything until its (clamped) harvest, an
    ongoing crop only its fires after today. `new_plant_units(c, d)` is the
    `t_day == day` case."""
    ongoing = xp.asarray(spec.CROP_ONGOING)[crop]
    first = xp.asarray(spec.CROP_FIRST_YIELD_DAY)[crop]
    interval = xp.maximum(xp.asarray(spec.CROP_INTERVAL)[crop], 1)
    mxy = xp.asarray(spec.CROP_MAX_YIELD)[crop]
    mxd = xp.asarray(spec.CROP_MAX_YIELD_DAY)[crop]
    ws = xp.asarray(spec.CROP_WINDOW_START)[crop]
    can = t_day + first <= O.LAST_SHED_DAY
    harvest_age = xp.clip(O.LAST_SHED_DAY - t_day, first, mxd)
    one = xp.minimum(mxy, 1 + xp.maximum(harvest_age - ws + 1, 0))
    last_h = t_day + first + (mxy - 1) * interval
    ong = fires_between(xp, t_day, first, interval, day + 1, xp.minimum(O.LAST_SHED_DAY, last_h))
    return xp.where(can, xp.where(ongoing == 1, ong, one), 0)
```

Append to `src/kagg3/core/projector.py`:

```python


#: Shop ticks per day: one every SHOP_SELL_INTERVAL turns.
SHOP_TICKS_PER_DAY = spec.TURNS_PER_DAY // spec.SHOP_SELL_INTERVAL


def daily_town_units(xp, shops):
    """int[9]: units the town removes per whole day -- six shop ticks plus
    the centre's one of everything but fertilizer."""
    return SHOP_TICKS_PER_DAY * town_tick_units(xp, shops) + xp.asarray(spec.TOWN_CENTER_CONSUME)


def inv_at_day(xp, mkt_inv, shops, days_ahead):
    """int[9]: the hour-0 inventory advanced `days_ahead` days of town drain
    (scalar or int[9]), opponent-free and before any own order. The engine
    has no inventory floor, so none is applied; the price table's low end is
    the only clamp, taken by the caller's table read."""
    return (mkt_inv.astype(xp.int32)
            - xp.asarray(days_ahead).astype(xp.int32) * daily_town_units(xp, shops))
```

- [ ] **Step 4: Replace the budget walk**

In `plan.py`: add `GROW_ONE = 256` next to `CHAIN_MAX` (and in `brain.py` replace `GROW_ONE = 256` with `GROW_ONE = P.GROW_ONE`); add `from . import budget as BUD`; add next to `_cum_take`:

```python
def _cum_at(xp, cum, k):
    """Vectorised `_cum_take`: cum[k-1] for each entry of `k` (0 where k == 0)."""
    return xp.where(k > 0, cum[xp.clip(k - 1, 0, cum.shape[0] - 1)], 0)


#: Longest per-candidate unit stream `_stream_rev` prices (a goose's whole
#: season of eggs or fertilizer is under 32).
STREAM_MAX = 32


def _stream_rev(xp, price_table, inv0, u, k):
    """int[len(k)]: coins the k-th block of `u` units of one product fetches
    when sold `k*u` units down the curve from inventory `inv0` -- straight
    table reads, so a hundred candidates of six units each price correctly
    (a K-long cumsum would clip every unit past the shed's worth to zero)."""
    m = xp.arange(STREAM_MAX, dtype=xp.int32)[None, :]
    idx = xp.clip(inv0 + k[:, None] * u + m - spec.PRICE_TABLE_LO, 0, spec.PRICE_TABLE_N - 1)
    return xp.sum(xp.where(m < u, price_table[idx], 0), axis=1).astype(xp.int32)
```

`price_table[idx]` above is the product's own row (`price_table[c]`); callers pass the row.

Add next to `_stream_rev`:

```python
def _pipeline_units(xp, view, is_plant, has_animal, day):
    """int[9]: own supply already committed by LAST_SHED_DAY -- every planted
    tile's remaining units (as if watered daily), every placed animal's
    remaining fires, one fertilizer per animal-day, and the shed. An upper
    bound on what the farm itself will push into each product's market before
    the season ends: conservative for valuing one more seed of it."""
    i32 = xp.int32
    crop = xp.clip(view.occ, 0, spec.N_CROPS - 1)
    kind = xp.clip(view.occ, 0, spec.N_ANIMALS - 1)
    t_units = xp.where(is_plant, VAL.remaining_plant_units(xp, crop, view.t_day, day), 0)
    a_units = xp.where(has_animal, VAL.fires_between(
        xp, view.t_day, xp.asarray(spec.ANIMAL_FIRST_YIELD_DAY)[kind],
        xp.maximum(xp.asarray(spec.ANIMAL_INTERVAL)[kind], 1), day + 1, O.LAST_SHED_DAY), 0)
    prod = xp.where(is_plant, crop, xp.asarray(spec.ANIMAL_PRODUCT)[kind])
    live = (is_plant | has_animal)[:, None]
    onehot = (prod[:, None] == xp.arange(spec.N_PRODUCTS, dtype=i32)[None, :]) & live
    pipe = xp.sum(onehot.astype(i32) * (t_units + a_units)[:, None], axis=0)
    fert = xp.sum(has_animal.astype(i32)) * xp.maximum(O.LAST_SHED_DAY - day, 0)
    pipe = pipe + xp.where(xp.arange(spec.N_PRODUCTS, dtype=i32) == spec.I_FERT, fert, 0)
    return (pipe + view.shed[:spec.N_PRODUCTS].astype(i32)).astype(i32)
```

(`is_plant` and `has_animal` are `build_day`'s own locals; `occ` holds the crop index on a plant tile and the animal kind on a stocked coop/pasture, as `a_have = view.shed[spec.I_GOOSE + a_kind]` already assumes.)

Move Phase 1's `fert_rank = _rank_by(xp, fert_cand, fert_val)` line from the clamp section to directly after `n_fert_want = ...` (before the walk). In the acquisition block (Phase 1 Task 4) add, after `ub_feeds = ...`:

```python
    ub_coins = (ub_units * view.price[a_prod] + ub_fert * view.price[spec.I_FERT]
                - ub_feeds * view.price[spec.I_WHEAT])
    acquire_ok = ub_coins > 0
```

(replacing the existing `acquire_ok = (...) > 0` expression).

Replace everything from `wheat_buy = xp.zeros((), i32)` through the end of the `for pos in range(N_BUDGET_CATS):` loop with:

```python
    # ---- marginal-unit budget [HEURISTIC, 1.3] ---------------------------
    # Purchases are marginal candidates -- one wheat per passing feed, one
    # fertilizer per application, the k-th seed of each crop, the k-th animal
    # -- each with a value in coins and an engine-curve cost, granted by
    # value per coin down the purse (core/budget.py). Land is lumpy and its
    # value is the learned logit, not coins: when the gene asks for it, it is
    # compared two ways -- grant if affordable, else skip -- ahead of the
    # greedy, so the gene owns its timing.
    purse = money
    # 1.3 says "gated by 0.3"; the derived last-useful-purchase-day gate is
    # not implemented in any phase (it belongs with M1, Phase 3) -- until then
    # the gene alone owns land's timing, as today.
    buy_land = ((macro.buy_land > 0) & (view.nquad < 4) & (purse >= land_cost)).astype(i32)
    purse = (purse - buy_land * land_cost).astype(i32)

    j = xp.arange(PJ.K, dtype=i32)
    grow_mult = macro.grow_mult.astype(i32)
    # feeds and applications in value order; the shed covers the first ranks free
    sorted_feed = xp.sum(((feed_rank[:, None] == j[None, :]) & feed_pass[:, None]).astype(i32)
                         * feed_value[:, None], axis=0)
    v_wheat = sorted_feed[xp.clip(j + view.shed[spec.I_WHEAT], 0, PJ.K - 1)]
    sorted_fert = xp.sum(((fert_rank[:, None] == j[None, :]) & fert_cand[:, None]).astype(i32)
                         * fert_val[:, None], axis=0)
    v_fert = sorted_fert[xp.clip(j + view.shed[spec.I_FERT], 0, PJ.K - 1)]
    # the k-th planting's units sell k*u further down the curve, priced by
    # direct table reads (not a K-long cumsum: K = 101 would value every
    # melon past the 16th and every wheat past the 25th at zero) -- and the
    # curve is the SALES-WINDOW one [HEURISTIC, gap review 2026-08-24]: the
    # hour-0 inventory drained by the town to the product's first fire, plus
    # everything the farm has already committed to that market. Opponent
    # supply is absent by construction; `press`/`grow_mult` carry it.
    first_p = xp.concatenate([xp.asarray(spec.CROP_FIRST_YIELD_DAY, dtype=i32),
                              xp.zeros(spec.N_PRODUCTS - spec.N_CROPS, i32)])
    first_p = xp.where(xp.arange(spec.N_PRODUCTS, dtype=i32) == a_prod, a_first, first_p)
    inv_h = (PJ.inv_at_day(xp, view.mkt_inv, view.shops, first_p)
             + _pipeline_units(xp, view, is_plant, has_animal, day))
    u_new = VAL.new_plant_units(xp, xp.arange(spec.N_CROPS, dtype=i32), day)
    v_seed, c_seed = [], []
    for c in range(spec.N_CROPS):
        rev = _stream_rev(xp, price_table[c], inv_h[c], u_new[c], j)
        v_seed.append(grow_mult[c] * rev // GROW_ONE)
        c_seed.append(xp.full((PJ.K,), int(spec.CROP_SEED_COST[c]), i32))
    w_seed = xp.maximum(macro.plant_target - view.seeds, 0)
    # the k-th animal's product and fertilizer streams sell further down theirs
    rev_a = (_stream_rev(xp, price_table[a_prod], inv_h[a_prod], xp.minimum(ub_units, STREAM_MAX), j)
             + _stream_rev(xp, price_table[spec.I_FERT], inv_h[spec.I_FERT], xp.minimum(ub_fert, STREAM_MAX), j)
             - ub_feeds * view.price[spec.I_WHEAT])
    v_anim = xp.maximum(grow_mult[a_prod] * rev_a // GROW_ONE, 0)
    c_anim = xp.full((PJ.K,), 1, i32) * a_cost
    w_anim = xp.where(acquire_ok, xp.maximum(a_want - a_have, 0), 0)

    values = xp.stack([v_wheat, v_fert] + v_seed + [v_anim])
    costs = xp.stack([buy_q[spec.I_WHEAT], buy_q[spec.I_FERT]] + c_seed + [c_anim])
    wants = xp.stack([wheat_short, fert_short] + [w_seed[c] for c in range(spec.N_CROPS)] + [w_anim])
    n_buy = BUD.grant(xp, values, costs, wants, purse)
    wheat_buy = n_buy[BUD.L_WHEAT]
    fert_bought = n_buy[BUD.L_FERT]
    seed_buy = n_buy[BUD.L_SEED0:BUD.L_SEED0 + spec.N_CROPS]
    a_buy = n_buy[BUD.L_ANIMAL]
```

Delete `Macro.order`, `DEFAULT_ORDER`'s "fallback priority" comment (keep the constant — `_market` uses it as the BUY-row slot layout; retitle the comment "BUY-row slot layout, fixed"), `N_BUDGET_CATS`, `ORDER_HEAD0`, `wheat_cum`/`fert_cum` (no longer read), and the long comment block above the old loop. In `brain.decide` delete the `pr = head[...]`/`ci`/`outranks`/`rank`/`order` lines and `order=` from the `P.Macro(...)` call.

- [ ] **Step 5: Rewrite the tests that pinned the category walk**

Delete `tests/test_learned_order.py`. In `tests/test_hire_bill.py` delete `LAND_FIRST` and every `order=` kwarg (the land-first rule now comes from `buy_land`); its two tests keep asserting `_buy_bill(...) + _hire_bill(n) <= PURSE`. In `tests/test_task_priority.py::_macro` and `tests/test_budget_order.py::_macro` drop `order=`.

Replace the tests in `tests/test_budget_order.py` (keep `_view`, `_macro`, `_buy_qty`, `PURSE` and the module docstring's first paragraph rewritten to describe the marginal-unit budget) with:

```python
def test_a_requested_quadrant_is_granted_ahead_of_the_greedy():
    view = _view(PURSE)
    macro = _macro(buy_land=np.int32(1), animal_count=np.int32(1))
    assert _buy_qty(view, macro, O.MO_BUY_LAND) == 1
    assert _buy_qty(view, macro, O.MO_BUY_ANIMAL) == 0


def test_without_the_request_the_purse_goes_to_the_greedy():
    view = _view(PURSE)
    macro = _macro(buy_land=np.int32(0), animal_count=np.int32(1))
    assert _buy_qty(view, macro, O.MO_BUY_LAND) == 0
    assert _buy_qty(view, macro, O.MO_BUY_ANIMAL) == 1


def test_value_per_coin_decides_between_seeds_and_an_animal():
    # 300 coins: thirty wheat seeds (4 units x 25 = 100 coins per 10-coin seed)
    # beat one goose (~975 coins of stream per 300)
    view = _view(300)
    macro = _macro(animal_count=np.int32(1), plant_target=np.array([30, 0, 0, 0, 0], np.int32))
    assert _buy_qty(view, macro, O.MO_BUY_SEED) == 30
    assert _buy_qty(view, macro, O.MO_BUY_ANIMAL) == 0
    # floor the wheat market and the goose wins
    inv = view.mkt_inv.copy()
    inv[spec.I_WHEAT] = spec.MARKET_I0 + 40_000
    assert _buy_qty(view._replace(mkt_inv=inv), macro, O.MO_BUY_ANIMAL) == 1


def test_grow_multiplier_tilts_the_seed_mix():
    view = _view(60)
    macro = _macro(plant_target=np.array([30, 30, 0, 0, 0], np.int32))
    op, arg, qty = P.build_day(np, view, macro)[3:6]
    seeds = {int(arg[O.TURN_BUY, s]): int(qty[O.TURN_BUY, s]) for s in range(spec.MAX_MARKET_ORDERS)
             if int(op[O.TURN_BUY, s]) == O.MO_BUY_SEED}
    assert seeds.get(spec.I_WHEAT, 0) == 6 and seeds.get(spec.I_CARROT, 0) == 0
    grow = np.full(spec.N_PRODUCTS, 256, np.int32)
    grow[spec.I_CARROT] = 1024
    op, arg, qty = P.build_day(np, view, macro._replace(grow_mult=grow))[3:6]
    seeds = {int(arg[O.TURN_BUY, s]): int(qty[O.TURN_BUY, s]) for s in range(spec.MAX_MARKET_ORDERS)
             if int(op[O.TURN_BUY, s]) == O.MO_BUY_SEED}
    assert seeds.get(spec.I_CARROT, 0) == 3 and seeds.get(spec.I_WHEAT, 0) == 0


def test_the_buy_row_layout_is_fixed_whatever_is_bought():
    view = _view(3000)
    macro = _macro(buy_land=np.int32(1), animal_count=np.int32(2),
                   plant_target=np.array([3, 2, 0, 0, 0], np.int32))
    op = P.build_day(np, view, macro)[3][O.TURN_BUY]
    live = [int(o) for o in op if int(o) != O.MO_NONE]
    assert live == [O.MO_BUY_SEED, O.MO_BUY_SEED, O.MO_BUY_ANIMAL, O.MO_BUY_LAND]


def test_macro_has_no_order():
    assert "order" not in P.Macro._fields
```

Arithmetic for `test_grow_multiplier_tilts_the_seed_mix` (fixture: no shops, fresh market, so only the centre's one unit a day drains, and the four wheat units sell at `I0 - 2 .. I0 + 1`, the three carrot units at `I0 - 2 .. I0`): a wheat seed (10 coins) is worth 101 (ratio 10.1); a carrot seed (20 coins) 105 (ratio 5.25); with 60 coins the greedy buys six wheat. At ×4 the carrot is worth 420 (ratio 21) and three carrots take the whole purse. (`test_value_per_coin_decides_between_seeds_and_an_animal`'s comment "4 units x 25 = 100" is the same 101 — table reads, not `base × units`.)

- [ ] **Step 6: Run the tests and the full suite**

Run: `python -m pytest tests/test_budget_greedy.py tests/test_seed_horizon.py tests/test_budget_order.py tests/test_hire_bill.py -q` — Expected: PASS.
Run: `python -m pytest -q` — Expected: all pass. `test_day29_endgame.py`'s day-28 fixture no longer buys wheat seeds (a day-28 planting is worth 0 and is never bought) — its assertions do not depend on that.
Run: `python scripts/bench_sim.py` here and on the Task-4 commit; record both; the bisection and the top-ups are small steps in traced loops.
Run: `ruff check src tests`.

- [ ] **Step 7: Commit**

```bash
git add -A src/kagg3/core/budget.py src/kagg3/core/valuation.py src/kagg3/core/projector.py src/kagg3/core/plan.py src/kagg3/core/brain.py tests/
git commit -m "Budget over marginal purchase candidates priced at their sales window; delete the order gene"
```

---

### Task 6: Admit by value, then route by serpentine stripe; delete `prio` (§1.6)

**Files:**
- Modify: `src/kagg3/core/valuation.py` (+`crop_remaining_value`), `src/kagg3/core/plan.py` (task values, admission, `_routes` signature, `Macro.prio`, the `PRIO_*`/`N_PRIO`/`PRIO_SCALE`/`PRIO_MAX`/`SHED_DIST`/`SERP_QUAD` constants), `src/kagg3/core/brain.py` (drop the `prio` decode)
- Rewrite: `tests/test_task_priority.py` (keep the four `task_order` tests; delete the three sweep tests and `_macro`'s `prio=`; delete `test_old_theta_unpacks_with_zero_priority` and `test_priority_head_reaches_the_macro`)
- Modify fixtures: `tests/test_budget_order.py::_macro` (drop `prio=`), `tests/test_mandatory_tier.py` (its `_weed_prio()` fixture — replace the three build_day tests' `_macro(prio=_weed_prio())` with `_macro()`; the weeds now score 0 and the tier still decides)
- Test: `tests/test_admit_route.py`

**Interfaces:**
- Consumes: `feed_value`, `fert_val`, `u_new`, `ub_coins`, `grow_mult`, `harvest_age`, `must_water`, `want_*` masks, `plant_here`/`plant_crop`, `m_place`, `n_ops`, `tier`, `_routes`.
- Produces: `valuation.crop_remaining_value(xp, price, t_day, t_yield, crop, day, harvest_age) -> int`; `build_day` locals `tile_value` (int[100]), `order_v` (admission order), `rank_v`, `n_admit`, `admitted` (bool[100]), `order` (serpentine order of the admitted tiles); `plan._inverse(xp, perm)`; `plan.ADMIT_ROUNDS = 3`; `_routes(xp, chain_op, chain_a, chain_q, n_ops, order, n_tasks, pick_masks, n_units, budget)` (takes the visiting order; no longer sorts). `Macro` loses `prio`; `plan.EST_MOVES = 2`.

**Background (§1.6).** `_routes` charges the true Manhattan move between consecutive tiles but never *minimises* it, so a global value sort thrashes the board. Two stages: **admit** tasks by `(tier, value)` against the day's total turn budget, each tile costed at its ops plus a conservative two moves; **route** the admitted set spatially — serpentine order is the stripe clustering, the existing block splitter cuts contiguous stripes per unit, and within a stripe consecutive *admitted* tiles are visited in sweep order (adjacent only when the stripe is fully admitted — this is the spec's nearest-insertion replaced by the sweep, a documented simplification). Shape-static, integer, no TSP. The admit threshold is the marginal admitted value at the boundary — computed, not learned; `prio` is deleted. The two-move estimate is not a bound, so the admit→route pair runs up to `ADMIT_ROUNDS = 3` times: each round subtracts the tiles the exact route left uncovered from the admitted count — from the value tail, so a mandatory tile (0.5, a LAW) is never the one dropped while any optional tile remains — and routes again. What a third route still cannot reach is the §7 "task value dropped at the labour boundary" metric (Task 9 Step 1b).

- [ ] **Step 1: Write the failing tests**

Create `tests/test_admit_route.py`:

```python
"""Labour is admitted by (tier, value) and routed by serpentine stripe
(PLANNER_V3_1 section 1.6): the most valuable work is done, and done in a
spatial sweep rather than in value order.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, "src")

import numpy as np
from test_budget_order import _macro

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P
from kagg3.core import valuation as V

TABLE = spec.build_price_table()
BASE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)


def _farm(tiles, day=13):
    """`tiles`: position -> dict(kind=, occ=, t_yield=, t_cons=, t_day=)."""
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    occ, t_yield, t_cons, t_day = z - 1, z.copy(), z.copy(), z.copy()
    for pos, t in tiles.items():
        kind[pos] = t["kind"]
        occ[pos] = t.get("occ", -1)
        t_yield[pos] = t.get("t_yield", 0)
        t_cons[pos] = t.get("t_cons", 0)
        t_day[pos] = t.get("t_day", 0)
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=t_day, t_water=z.copy(), t_cons=t_cons,
        t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=np.zeros(spec.N_ITEMS, np.int32), seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(0), nquad=np.int32(4), price=BASE.copy())


def _ripe(crop, units):
    return dict(kind=spec.KIND_PLANT, occ=crop, t_yield=units)


def test_admission_is_by_value_not_by_position():
    # twenty weeds at the head of the sweep (worth nothing), one ripe melon at
    # its tail (six units at 250): the old sweep dug weeds and never got there
    tiles = {p: dict(kind=spec.KIND_WEED) for p in range(20)}
    tiles[99] = _ripe(spec.I_MELON, 6)
    unit_op = P.build_day(np, _farm(tiles), _macro(), TABLE)[0]
    assert int((unit_op == O.OP_HARVEST).sum()) == 1


def test_admitted_tiles_are_routed_in_serpentine_order():
    # values descend 55 > 53 > 46 > 45 > 44, but the route is the sweep
    # 44 (4,4: the spawn) -> 45 -> 46 -> 53 (6,5) -> 55 (4,5)
    tiles = {55: _ripe(spec.I_TOMATO, 4), 53: _ripe(spec.I_TOMATO, 3), 46: _ripe(spec.I_TOMATO, 2),
             45: _ripe(spec.I_STRAWBERRY, 1), 44: _ripe(spec.I_WHEAT, 1)}
    unit_op = P.build_day(np, _farm(tiles), _macro(), TABLE)[0]
    harvest_turns = [int(t) for t in np.flatnonzero(unit_op[0] == O.OP_HARVEST)]
    assert harvest_turns == [2, 4, 6, 8, 11]


def test_mandatory_work_is_admitted_before_any_value():
    # sixty ripe melons and one thirsty tomato at the tail; one unit admits the
    # tomato (mandatory) and as many melons as fit
    tiles = {p: _ripe(spec.I_MELON, 6) for p in range(60)}
    tiles[99] = dict(kind=spec.KIND_PLANT, occ=spec.I_TOMATO, t_cons=1)
    unit_op = P.build_day(np, _farm(tiles), _macro(), TABLE)[0]
    assert int((unit_op == O.OP_WATER).sum()) == 1
    assert int((unit_op == O.OP_HARVEST).sum()) > 0


def test_a_mandatory_tile_survives_when_the_estimate_undershoots():
    # three ripe melons on the far row (90..92) and a thirsty tomato at 99: the
    # two-move estimate admits all four (12 <= 19), the exact route needs
    # 11 + 2 + 2 + 8 = 23 > 22 turns. Re-admission drops from the value tail
    # -- a melon, never the survival watering [0.5].
    tiles = {p: _ripe(spec.I_MELON, 6) for p in (90, 91, 92)}
    tiles[99] = dict(kind=spec.KIND_PLANT, occ=spec.I_TOMATO, t_cons=1)
    unit_op = P.build_day(np, _farm(tiles), _macro(), TABLE)[0]
    assert int((unit_op[0] == O.OP_WATER).sum()) == 1
    assert int((unit_op[0] == O.OP_HARVEST).sum()) == 2


def test_crop_remaining_value_at_the_spec_numbers():
    I = np.int32
    ha = lambda c, t: I(int(np.clip(O.LAST_SHED_DAY - t, spec.CROP_FIRST_YIELD_DAY[c], spec.CROP_MAX_YIELD_DAY[c])))
    # wheat planted day 0, seen day 2 holding 1: three in-window waterings
    # left (today, tomorrow, the harvest day) -> 4 units
    assert int(V.crop_remaining_value(np, BASE, I(0), I(1), I(spec.I_WHEAT), I(2), ha(0, 0))) == 4 * 25
    # tomato planted day 0, seen day 9 holding 1: fires 10, 11 left -> 3 units
    assert int(V.crop_remaining_value(np, BASE, I(0), I(1), I(spec.I_TOMATO), I(9), ha(2, 0))) == 3 * 60
    # a crop that cannot be harvested by day 28 is worth nothing
    assert int(V.crop_remaining_value(np, BASE, I(27), I(1), I(spec.I_WHEAT), I(28), ha(0, 27))) == 0


def test_prio_is_gone():
    assert "prio" not in P.Macro._fields


def test_admit_route_agrees_across_backends():
    import jax
    import jax.numpy as jnp
    tiles = {p: _ripe(spec.I_MELON, 6) for p in range(0, 60, 3)}
    tiles.update({p: dict(kind=spec.KIND_WEED) for p in range(1, 60, 3)})
    tiles[99] = dict(kind=spec.KIND_PLANT, occ=spec.I_TOMATO, t_cons=1)
    view, macro = _farm(tiles), _macro(n_hire=np.int32(2))
    a = P.build_day(np, view, macro, TABLE)
    b = P.build_day(jnp, jax.tree_util.tree_map(jnp.asarray, view),
                    jax.tree_util.tree_map(jnp.asarray, macro), jnp.asarray(TABLE))
    for x, y in zip(a, b):
        assert np.array_equal(np.asarray(x), np.asarray(y))
```

Route arithmetic for the serpentine test: position 44 is tile (4, 4), the farmer's spawn — HARVEST on turn 2 with no move; 45 = (5, 4): one move, HARVEST turn 4; 46 = (6, 4): turn 6; 53 is on row 5 (odd, x runs 9→0) so 53 = (6, 5): one move south, turn 8; 55 = (4, 5): two moves west, turn 11.

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_admit_route.py -q`
Expected: FAIL — the melon at position 99 is never reached (`0 == 1`); the harvest turns come out in value order; the mandatory-tile test loses its watering.

- [ ] **Step 3: Add `crop_remaining_value`**

Append to `src/kagg3/core/valuation.py`:

```python


def crop_remaining_value(xp, price, t_day, t_yield, crop, day, harvest_age):
    """Coins a standing crop will still sell if kept alive and watered: a
    one-time crop's clipped units at its harvest day (0 past the horizon), an
    ongoing crop's held units plus the fires left before its last."""
    ongoing = xp.asarray(spec.CROP_ONGOING)[crop]
    first = xp.asarray(spec.CROP_FIRST_YIELD_DAY)[crop]
    interval = xp.maximum(xp.asarray(spec.CROP_INTERVAL)[crop], 1)
    mxy = xp.asarray(spec.CROP_MAX_YIELD)[crop]
    ws = xp.asarray(spec.CROP_WINDOW_START)[crop]
    d_h = t_day + harvest_age
    w_lo = xp.maximum(day, t_day + ws)
    n_water = xp.maximum(d_h - w_lo + 1, 0)
    one = xp.where(d_h <= O.LAST_SHED_DAY, xp.minimum(mxy, t_yield + n_water), 0)
    last_h = t_day + first + (mxy - 1) * interval
    ong = t_yield + fires_between(xp, t_day, first, interval, day + 1, xp.minimum(O.LAST_SHED_DAY, last_h))
    return xp.where(ongoing == 1, ong, one) * price[crop]
```

- [ ] **Step 4: Value the tiles, admit, and route by serpentine**

In `plan.py` add `EST_MOVES = 2` and `ADMIT_ROUNDS = 3` next to `CHAIN_MAX`, delete the `PRIO_*`, `N_PRIO`, `PRIO_SCALE`, `PRIO_MAX`, `SHED_DIST`, `SERP_QUAD` definitions and the comment block above them, delete `Macro.prio`, and add next to `_rank`:

```python
def _inverse(xp, perm):
    """rank[perm[k]] = k."""
    n = perm.shape[0]
    ranks = xp.arange(n, dtype=xp.int32)
    if hasattr(perm, "at"):
        return xp.zeros(n, xp.int32).at[perm].set(ranks)
    out = np.zeros(n, np.int32)
    out[np.asarray(perm)] = ranks
    return out
```

In `build_day` replace the whole `# ---- labour priority ---` block (from `want_harvest = ...` through `tier = mandatory.astype(i32)`) and the `_routes(...)` call with:

```python
    # ---- task values [1.6 admit stage] -------------------------------------
    # Every op's worth in coins under the day's value model: harvests at
    # today's price (plus the unit an in-window watering adds first),
    # survival waterings at the crop's remaining value, bonus waterings at one
    # unit, feeds at 1.4's value, care at the unit net of its wheat,
    # fertilizer at 0.11's marginal table, collections at the fertilizer
    # price, plantings and placements at their stream value under the grow
    # multiplier. A weed dig is worth what gets planted on it, which is the
    # planting's own value.
    want_harvest = harvest_one | harvest_ong | want_harv_animal
    p_crop = view.price[crop]
    bonus_today = (want_water & (c_ongoing == 0)).astype(i32)
    v_harvest = (xp.where(harvest_one | harvest_ong, (view.t_yield + bonus_today) * p_crop, 0)
                 + xp.where(want_harv_animal, view.t_yield * view.price[an_prod], 0))
    crop_val = VAL.crop_remaining_value(xp, view.price, view.t_day, view.t_yield, crop, day, harvest_age)
    v_water = xp.where(want_water & ~(harvest_one | harvest_ong),
                       xp.where(must_water, crop_val, p_crop), 0)
    v_feed = xp.where(want_feed, feed_value, 0)
    v_care = xp.where(want_care, view.price[an_prod] - view.price[spec.I_WHEAT], 0)
    v_fert = xp.where(want_fert, fert_val, 0)
    v_collect = xp.where(want_collect, view.price[spec.I_FERT], 0)
    v_plant = xp.where(plant_here,
                       grow_mult[plant_crop] * u_new[plant_crop] * view.price[plant_crop] // GROW_ONE, 0)
    v_place = xp.where(m_place, xp.maximum(grow_mult[a_prod] * ub_coins // GROW_ONE, 0), 0)
    tile_value = xp.clip(v_harvest + v_water + v_feed + v_care + v_fert + v_collect + v_plant + v_place,
                         0, (1 << 20) - 1).astype(i32)

    # Mandatory tier [LAW, 0.5]: whatever the value says, work that is lost
    # for good if skipped today goes first -- deadline harvests, survival
    # waterings, survival feeds that passed 1.4's test.
    mandatory = (harvest_one
                 | ((day >= O.LAST_SHED_DAY) & want_harvest)
                 | (is_plant & must_water & (view.t_water == 0))
                 | (want_feed & must_feed))
    tier = mandatory.astype(i32)

    # ---- admit, then route [HEURISTIC, 1.6] --------------------------------
    # Admit tiles by (tier, value) against the day's whole turn budget, each
    # costed at its ops plus EST_MOVES; then route the admitted set as a
    # serpentine sweep -- `_routes` cuts it into contiguous stripes per unit.
    # The estimate is not a bound: when the exact route leaves admitted tiles
    # uncovered, the shortfall is re-admitted from the *value* tail (the
    # mandatory tier sits at the head of `order_v`, so a deadline harvest or
    # survival watering is never the tile that goes [LAW, 0.5]) and the route
    # is rebuilt -- ADMIT_ROUNDS times, shape-static.
    task = n_ops > 0
    n_tasks = xp.sum(task.astype(i32))
    order_v = task_order(xp, task, tile_value, tier)
    rank_v = _inverse(xp, order_v)
    cum_est = xp.cumsum((n_ops + EST_MOVES)[order_v])
    labour = n_units * budget - O.MAX_PICKUPS
    n_admit = xp.minimum(_count_le(xp, cum_est, labour), n_tasks).astype(i32)
    pick_masks = xp.stack([want_feed, want_fert, m_place])
    for _ in range(ADMIT_ROUNDS):
        admitted = task & (rank_v < n_admit)
        order = task_order(xp, admitted, xp.zeros(N_T, i32))
        route_op, route_a, route_q, blk, covered, n_pick = _routes(
            xp, chain_op, chain_a, chain_q, n_ops, order, n_admit, pick_masks, n_units, budget)
        n_admit = (n_admit - xp.sum((admitted & ~covered).astype(i32))).astype(i32)
```

with `ADMIT_ROUNDS = 3` defined next to `EST_MOVES`. After the loop `n_admit` is the count the last route actually covered (the last iteration's subtraction is 0 whenever the route fit). Three rounds cover the measured cases; whatever a third route still cannot reach is dropped from the serpentine tail — that residue is the "task value dropped at the labour boundary" metric of §7 (Task 9 Step 1b logs it), never a mandatory tile unless *only* mandatory tiles remain.

(`budget` and `n_units` are defined just above in the route block; keep that block, it now precedes this one — move the `# ---- route ---` two lines up if needed.)

In `_routes` change the signature to `(xp, chain_op, chain_a, chain_q, n_ops, order, n_tasks, pick_masks, n_units, budget)`, delete the three lines `task = n_ops > 0`, `order = task_order(xp, task, score, tier)`, `n_tasks = xp.sum(task.astype(i32))`, and update its docstring: "Tiles are visited in `order`, the first `n_tasks` of which carry work; whatever the turn budget cannot reach is left undone."

In `brain.decide` delete the `prio = xp.clip(...)` line and `prio=` from the `P.Macro(...)` call.

- [ ] **Step 5: Update the tests that used `prio`**

`tests/test_task_priority.py`: keep `test_task_order_ties_fall_to_serpentine_position`, `test_task_order_ranks_by_score_then_position`, `test_task_order_agrees_across_backends`; delete `_thirsty_plants_then_weeds`/`_ripe_plants_then_weeds`, the three sweep tests, `_obs`, `test_old_theta_unpacks_with_zero_priority`, `test_priority_head_reaches_the_macro`, and `prio=` from its `_macro` (or delete `_macro`/`_view` if now unused); rewrite the module docstring: "`task_order` is the pairwise ranker the admit stage uses (PLANNER_V3_1 1.6): descending tier, then descending value, exact ties by serpentine position." `tests/test_budget_order.py::_macro`: drop `prio=`. `tests/test_mandatory_tier.py`: delete `_weed_prio()` and pass `_macro()` in its three build_day tests.

- [ ] **Step 6: Run the tests and the full suite**

Run: `python -m pytest tests/test_admit_route.py tests/test_task_priority.py tests/test_mandatory_tier.py -q` — Expected: PASS.
Run: `python -m pytest -q` — Expected: all pass. Watch `test_gates.py::test_no_tile_write_collisions` (blocks are still contiguous cuts of one order) and `test_overflow_forced_sale.py` (`covered` and `blk` unchanged in shape; its 11-hand fixtures admit everything).
Run: `python scripts/bench_sim.py` here and on the Task-5 commit; record both — the route now runs `ADMIT_ROUNDS` times inside the day scan, so this is the task most likely to trip the 15% rule; if it does, report and stop (the user may lower `ADMIT_ROUNDS` to 2).
Run: `ruff check src tests`.

- [ ] **Step 7: Commit**

```bash
git add -A src/kagg3/core/valuation.py src/kagg3/core/plan.py src/kagg3/core/brain.py tests/
git commit -m "Admit labour by value and route it as a serpentine sweep; delete the priority gene"
```

---

### Task 7: Hiring as an enumerated argmax; delete `n_hire` (§1.5, benchmark-gated)

**Files:**
- Modify: `src/kagg3/core/plan.py` — split `build_day` into `_derive` (the cheap prefix) and the enumeration/route/sale that follows; `Macro.n_hire`; `src/kagg3/core/brain.py` (drop the `n_hire` decode); `src/kagg3/es/archetypes.py` (drop the `hire` knob)
- Modify fixtures: every test that passes `n_hire=` to `_macro` — `tests/test_overflow_forced_sale.py` (`_many_hands`), `tests/test_feed_rationing.py`, `tests/test_unit_pickups.py`, `tests/test_feed_value.py`, `tests/test_sell_side.py`, `tests/test_admit_route.py`, `tests/test_day29_endgame.py`, `tests/test_hire_bill.py`, `tests/test_budget_order.py::_macro`
- Test: `tests/test_hire_enumeration.py`

**Interfaces:**
- Consumes: everything `build_day` computes before routing (Tasks 4–6), `task_order`, `_count_le`, `_cum_take`, `EST_MOVES`, `spec.HIRE_COST`.
- Produces: `plan.Prefix` (NamedTuple: `task, n_ops, chain_op, chain_a, chain_q, tile_value, tier, want_feed, want_fert, m_place, wheat_buy, fert_bought, seed_buy, a_buy, buy_land, a_kind, n_fert_eff`), `plan._derive(xp, view, macro, price_table, hire_bill, terminal) -> Prefix`, `plan.HIRE_BILLS` (int32[MAX_HANDS + 2], `HIRE_BILLS[h]` = cost of `h` hires), `build_day` locals `h_star`, `n_hire`. `Macro` loses `n_hire`.

**Background (§1.5).** For each `h ∈ 0..10` run the cheap prefix — budget, tasks, `task_order`, cumulative block values — pick the `h` maximising in-model day value minus the fib hire bill, and route once with the winner. The label is exact-argmax-under-the-model, not exact: spawn effects, per-unit pickups and purchase interactions sit outside the projection. Two passes keep the purse honest: pass A derives tasks with a zero bill and scores every `h` from the admission prefix (the cumulative admitted value under `(h+1)` units' turns); pass B re-derives with the winner's bill so purchases never exceed what the day can pay. Ties go to fewer hands. **Gate:** the day scan pays compile and runtime for two prefixes; measure before adopting. A throughput loss above 15% versus the Task-6 commit is reported and stops this task — the spec makes the gate, not the number, the requirement.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_hire_enumeration.py`:

```python
"""Hands are hired by enumerated argmax (PLANNER_V3_1 section 1.5): the count
whose admitted task value minus its fib bill is highest, ties to fewer hands,
and the bill is reserved from the purse before anything is bought.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, "src")

import numpy as np
from test_budget_order import _macro

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

TABLE = spec.build_price_table()
BASE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)


def _farm(ripe, crop, units, money=3000, day=13):
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_yield = z.copy()
    kind[:ripe] = spec.KIND_PLANT
    occ[:ripe] = crop
    t_yield[:ripe] = units
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(), t_cons=z.copy(),
        t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=np.zeros(spec.N_ITEMS, np.int32), seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(money), nquad=np.int32(4), price=BASE.copy())


def _hires(view, **macro):
    op = P.build_day(np, view, _macro(**macro), TABLE)[3]
    return int((op[O.TURN_HIRE] == O.MO_HIRE).sum())


def test_no_work_hires_nobody():
    assert _hires(_farm(0, spec.I_WHEAT, 0)) == 0


def test_a_big_harvest_hires_every_hand():
    # a hundred melons at 1,500 each: every hand pays its fib cost many times over
    assert _hires(_farm(100, spec.I_MELON, 6)) == spec.MAX_HANDS


def test_hands_are_hired_only_while_they_add_admitted_value():
    # twelve ripe wheat tiles at 25: the farmer admits six (3 est. turns each
    # of 19), a second hand covers the rest; a third would add nothing
    assert _hires(_farm(12, spec.I_WHEAT, 1)) == 1


def test_the_purse_caps_the_bill():
    # 1 + 1 + 2 = 4 for three hands; with 3 coins only two can be paid
    assert _hires(_farm(100, spec.I_MELON, 6, money=3)) == 2


def test_the_terminal_day_hires_nobody():
    assert _hires(_farm(100, spec.I_MELON, 6, day=29)) == 0


def test_macro_has_no_n_hire():
    assert "n_hire" not in P.Macro._fields


def test_enumeration_agrees_across_backends():
    import jax
    import jax.numpy as jnp
    view, macro = _farm(30, spec.I_TOMATO, 1), _macro()
    a = P.build_day(np, view, macro, TABLE)
    b = P.build_day(jnp, jax.tree_util.tree_map(jnp.asarray, view),
                    jax.tree_util.tree_map(jnp.asarray, macro), jnp.asarray(TABLE))
    for x, y in zip(a, b):
        assert np.array_equal(np.asarray(x), np.asarray(y))
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_hire_enumeration.py -q`
Expected: FAIL — `_macro()` still carries `n_hire = 0`, so the melon farm hires nobody (`0 == 10`).

- [ ] **Step 3: Split `build_day` into the prefix and the rest**

In `plan.py`, define after `Macro`:

```python
class Prefix(NamedTuple):
    """Everything a day's plan needs that does not depend on how many hands
    are hired -- computed once per candidate hire bill (1.5)."""
    task: object            # bool[100]
    n_ops: object           # int[100]
    chain_op: object        # int[100, CHAIN_MAX]
    chain_a: object
    chain_q: object
    tile_value: object      # int[100]
    tier: object            # int[100]
    want_feed: object       # bool[100]
    want_fert: object
    m_place: object
    wheat_buy: object       # scalars / int[5]: the purchases
    fert_bought: object
    seed_buy: object
    a_buy: object
    buy_land: object
    a_kind: object
    n_fert_eff: object


#: HIRE_BILLS[h] = fib cost of hiring h hands in one day.
HIRE_BILLS = np.concatenate([[0], np.cumsum(spec.HIRE_COST)]).astype(np.int32)
```

Create `_derive(xp, view, macro, price_table, hire_bill, terminal)` whose body is the current `build_day` from `kind, occ = view.kind, view.occ` through `tier = mandatory.astype(i32)`, with these edits: the hire-bill lines become `money = xp.where(terminal, 0, xp.maximum(view.money - hire_bill, 0)).astype(i32)` (delete `hire_cost`/`hire_bill` computation), the `budget`/`n_units` lines are removed (they move to `build_day`), and it ends with `return Prefix(task=n_ops > 0, n_ops=n_ops, chain_op=chain_op, chain_a=chain_a, chain_q=chain_q, tile_value=tile_value, tier=tier, want_feed=want_feed, want_fert=want_fert, m_place=m_place, wheat_buy=wheat_buy, fert_bought=fert_bought, seed_buy=seed_buy, a_buy=a_buy, buy_land=buy_land, a_kind=a_kind, n_fert_eff=n_fert_eff)`.

Rewrite `build_day` as:

```python
def build_day(xp, view: DayView, macro: Macro, price_table=None):
    """Whole-day plan. See the module docstring for the returned shapes."""
    i32 = xp.int32
    if price_table is None:
        price_table = xp.asarray(default_price_table())
    day = view.day
    terminal = day > O.LAST_SHED_DAY
    budget = xp.asarray(TPD - O.ROUTE_BASE, i32)

    # ---- hiring: enumerated argmax under the day's value model [1.5] -----
    # Pass A derives the day with no hire bill and scores every hand count by
    # the admitted value its turns buy minus its fib bill; pass B re-derives
    # with the winner's bill so the purse is honest. Ties go to fewer hands.
    bills = xp.asarray(HIRE_BILLS)
    d0 = _derive(xp, view, macro, price_table, xp.asarray(0, i32), terminal)
    n_tasks0 = xp.sum(d0.task.astype(i32))
    order0 = task_order(xp, d0.task, d0.tile_value, d0.tier)
    cum_est0 = xp.cumsum((d0.n_ops + EST_MOVES)[order0])
    cum_val0 = xp.cumsum(d0.tile_value[order0])
    scores = []
    for h in range(spec.MAX_HANDS + 1):
        labour = (h + 1) * (TPD - O.ROUTE_BASE) - O.MAX_PICKUPS
        n_adm = xp.minimum(_count_le(xp, cum_est0, labour), n_tasks0)
        gain = _cum_take(xp, cum_val0, n_adm) - bills[h]
        scores.append(xp.where(bills[h] <= view.money, gain, -(1 << 30)))
    h_star = xp.argmax(xp.stack(scores)).astype(i32)
    n_hire = xp.where(terminal, 0, h_star).astype(i32)
    n_units = xp.asarray(1, i32) + n_hire
    d = _derive(xp, view, macro, price_table, bills[n_hire], terminal)

    # ---- admit, then route [HEURISTIC, 1.6; Task 6's re-admission loop] ----
    n_tasks = xp.sum(d.task.astype(i32))
    order_v = task_order(xp, d.task, d.tile_value, d.tier)
    rank_v = _inverse(xp, order_v)
    cum_est = xp.cumsum((d.n_ops + EST_MOVES)[order_v])
    labour = n_units * budget - O.MAX_PICKUPS
    n_admit = xp.minimum(_count_le(xp, cum_est, labour), n_tasks).astype(i32)
    pick_masks = xp.stack([d.want_feed, d.want_fert, d.m_place])
    for _ in range(ADMIT_ROUNDS):
        admitted = d.task & (rank_v < n_admit)
        order = task_order(xp, admitted, xp.zeros(N_T, i32))
        route_op, route_a, route_q, blk, covered, n_pick = _routes(
            xp, d.chain_op, d.chain_a, d.chain_q, d.n_ops, order, n_admit, pick_masks, n_units, budget)
        n_admit = (n_admit - xp.sum((admitted & ~covered).astype(i32))).astype(i32)

    t = xp.arange(TPD, dtype=i32)[None, :]
    r = t - (O.ROUTE_BASE + n_pick[:, None])
    on_route = (r >= 0) & (r < budget - n_pick[:, None])
    rc = xp.clip(r, 0, TPD - 1) + xp.zeros((MU, 1), i32)
    unit_op = xp.where(on_route, xp.take_along_axis(route_op, rc, axis=1), O.OP_PASS).astype(i32)
    unit_a = xp.where(on_route, xp.take_along_axis(route_a, rc, axis=1), 0).astype(i32)
    unit_q = xp.where(on_route, xp.take_along_axis(route_q, rc, axis=1), 0).astype(i32)

    # ---- morning PICKUPs (0.12) -------------------------------------------
    pk_active = (blk > 0).astype(i32)                                     # [3, MU]
    pk_turn = xp.cumsum(pk_active, axis=0) - pk_active + O.ROUTE_BASE     # [3, MU]
    pk_item = xp.stack([xp.asarray(spec.I_WHEAT, i32),
                        xp.asarray(spec.I_FERT, i32),
                        xp.asarray(spec.I_GOOSE, i32) + d.a_kind])
    for i in range(3):
        hit = (pk_active[i][:, None] > 0) & (t == pk_turn[i][:, None])
        unit_op = xp.where(hit, O.OP_PICKUP, unit_op)
        unit_a = xp.where(hit, pk_item[i], unit_a)
        unit_q = xp.where(hit, blk[i][:, None], unit_q)

    # Terminal day: no unit op can still monetize [LAW, 0.4].
    unit_op = xp.where(terminal, O.OP_PASS, unit_op).astype(i32)
    unit_a = xp.where(terminal, 0, unit_a).astype(i32)
    unit_q = xp.where(terminal, 0, unit_q).astype(i32)

    # ---- the sale (0.7 reservations, 1.2 allocator, 0.9 forced overflow) --
    wheat_reserved = xp.where(terminal, 0, xp.sum(d.want_feed.astype(i32))).astype(i32)
    avail = view.shed[:spec.N_PRODUCTS].astype(i32)
    avail = _set1(xp, avail, spec.I_WHEAT,
                  xp.maximum(avail[spec.I_WHEAT] - wheat_reserved, 0))
    fert_reserved = xp.where(terminal, 0, d.n_fert_eff).astype(i32)
    avail = _set1(xp, avail, spec.I_FERT,
                  xp.maximum(avail[spec.I_FERT] - fert_reserved, 0))
    hold = xp.where(terminal, SELL.LIQUIDATE, macro.hold).astype(i32)
    lots = SELL.allocate(xp, price_table, view.mkt_inv, view.shops, avail, hold, macro.press)
    s_qty = xp.sum(lots, axis=0).astype(i32)

    has_harv = xp.sum((d.chain_op == O.OP_HARVEST).astype(i32), axis=1) > 0
    has_coll = xp.sum((d.chain_op == O.OP_COLLECT_FERT).astype(i32), axis=1) > 0
    inflow = (xp.sum(xp.where(covered & has_harv, view.t_yield, 0).astype(i32))
              + xp.sum((covered & has_coll).astype(i32)))
    buys_in = (d.wheat_buy + d.fert_bought + d.a_buy).astype(i32)
    picks_out = xp.sum(blk).astype(i32)
    proj_eod = xp.sum(view.shed.astype(i32)) - xp.sum(s_qty) - picks_out + buys_in + inflow
    deficit = xp.maximum(proj_eod - spec.SHED_CAPACITY, 0).astype(i32)
    spare = xp.maximum(avail - s_qty, 0).astype(i32)
    inv_lot1 = PJ.projected_inv(xp, view.mkt_inv, view.shops, O.SELL_TURNS[0])
    marg = PJ.marginal_quote(xp, PJ.sell_quotes(xp, price_table, inv_lot1), s_qty)
    pid = xp.arange(spec.N_PRODUCTS, dtype=i32)
    forced = xp.zeros(spec.N_PRODUCTS, i32)
    left = deficit
    for _ in range(spec.N_PRODUCTS):
        key = xp.where(spare > 0, marg * spec.N_PRODUCTS + pid, _BIG)
        pick = xp.argmin(key)
        amt = xp.where(spare[pick] > 0, xp.minimum(left, spare[pick]), 0).astype(i32)
        hit = (pid == pick).astype(i32)
        forced = forced + hit * amt
        spare = spare - hit * spare[pick]
        left = left - amt
    forced_lot = SELL.best_lot(xp, price_table, view.mkt_inv, view.shops, lots, macro.press)
    lot_ix = xp.arange(SELL.N_LOTS, dtype=i32)[:, None]
    lots = (lots + (lot_ix == forced_lot[None, :]).astype(i32) * forced[None, :]).astype(i32)

    mkt = _market(xp, d.wheat_buy, d.fert_bought, d.seed_buy, d.a_buy, d.a_kind, d.buy_land,
                  lots, n_hire)
    return (unit_op, unit_a, unit_q) + mkt
```

The tail above is the existing Phase-0/1/2 code with `d.` prefixes and its comments condensed to section headers — keep the fuller comments from the current file. Delete `Macro.n_hire`; in `brain.decide` delete the `n_hire = xp.clip(...)` line and `n_hire=` from `P.Macro(...)`; in `archetypes.py` remove `hire` from `KNOBS`, `_HEAD_INDEX`, `_NAMED` and `sample_archetype`.

- [ ] **Step 4: Update every fixture that passed `n_hire`**

Remove the `n_hire=` entry from `tests/test_budget_order.py::_macro`, and every `n_hire=np.int32(...)` kwarg in the files listed under **Files** (in `test_overflow_forced_sale.py` make `_many_hands(**kw)` return `_macro(**kw)` and keep its name — the enumeration now hires because each reached tomato is worth 60 and a hand costs 1–55; in `test_day29_endgame.py` replace the `assert int((op[O.TURN_HIRE] == O.MO_HIRE).sum()) == 3` line with `assert int(qty[O.TURN_BUY][op[O.TURN_BUY] == O.MO_BUY_LAND].sum()) == 1` — on day 27 the greedy still grants the requested quadrant; in `test_hire_bill.py` replace `_hire_bill(n)` on a macro-given count with the count read from the emitted hire row: `n = int((op[O.TURN_HIRE] == O.MO_HIRE).sum())` and keep the assertion `_buy_bill(view, macro) + int(spec.HIRE_COST[:n].sum()) <= PURSE`, giving the fixture enough ripe work that at least one hand is hired: add twenty ripe tomatoes with `t_yield = 1` on positions 0..19).

- [ ] **Step 5: Run the tests and the full suite**

Run: `python -m pytest tests/test_hire_enumeration.py tests/test_hire_bill.py -q` — Expected: PASS.
Run: `python -m pytest -q` — Expected: all pass. Coverage-dependent fixtures (`test_overflow_forced_sale.py`, `test_feed_value.py`'s 30-goose cases, `test_unit_pickups.py`) now depend on the enumeration hiring enough; each tile in them is worth far more than its hand's fib cost, so they do. If one is short, the fix is the fixture's values, not the enumeration.
Run: `ruff check src tests`.

- [ ] **Step 6: The benchmark gate**

Run `python scripts/bench_sim.py` on this commit and on the Task-6 commit (`git worktree add /tmp/claude-0/kagg3-t6 HEAD~1`). Record both numbers and the compile time in the commit message. **If throughput fell by more than 15%, do not commit: report the two numbers and stop** — the spec gates §1.5 on this measurement and the user decides whether to keep the enumeration, thin it (e.g. score `h ∈ {0, 2, 5, 10}` and interpolate), or defer it.

- [ ] **Step 7: Commit**

```bash
git add -A src/kagg3/core/plan.py src/kagg3/core/brain.py src/kagg3/es/archetypes.py tests/
git commit -m "Hire by enumerated argmax over admitted value minus the fib bill; delete the hire gene"
```

---

### Task 8: Mask the dead parameters out of ES; trunk warm start for the fresh lineage (§2)

**Files:**
- Modify: `src/kagg3/core/policy.py` (+`DEAD_HEAD`, `DEAD_AUX`, `live_mask`), `src/kagg3/es/train.py` (`Trainer.__init__`, `generation`), `scripts/train.py` (`--trunk-from`)
- Test: `tests/test_es_masking.py`

**Interfaces:**
- Produces: `policy.DEAD_HEAD = (0, 2, 3, 4, 8, ..., 17)`, `policy.DEAD_AUX = (0,)`, `policy.live_mask() -> float32[N_PARAMS]` (1 = live), `policy.N_DEAD = 825`; `Trainer.mask` (device array); `scripts/train.py::warm_trunk(tr, path)` and the `--trunk-from PATH` flag.

**Background (§2, "Inert parameters").** Verified from the update rule — elementwise Adam, decoupled per-coordinate decay, no clipping, no norm coupling — a dead parameter's perturbation changes no candidate's fitness and cannot alter live coordinates' updates; it only random-walks at ~0.23·lr on noise. Masking the columns that feed deleted outputs out of both the perturbation and the update is hygiene protecting future reactivation, claimed as hygiene, not as a speed-up. Counts: `g2[:, dead]` 14 × 32 = 448 and `gb2[dead]` 14; `g3/gb3` 297; `g4/gb4` 33; `g5[:, 0]/gb5[0]` 33 — 825 of 4,386, of which the never-used `head[13:18]` block alone is 165. The fresh lineage may warm-start the encoder trunk (`w1, b1, g1, gb1`); the heads must not inherit trained biases from the old decode.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_es_masking.py`:

```python
"""Dead parameter columns (PLANNER_V3_1 section 2) are masked out of the ES
perturbation and update: they neither move nor move anything. The fresh
lineage may copy an older theta's encoder trunk and nothing else.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, "src")

import jax.numpy as jnp
import numpy as np

from kagg3.core import policy as PO
from kagg3.es.train import Config, Trainer


def _block(mask, name):
    off = PO.offset(name)
    shape = dict(PO.SHAPES)[name]
    return mask[off:off + int(np.prod(shape))].reshape(shape)


def test_mask_counts_match_the_spec():
    m = PO.live_mask()
    assert m.shape == (PO.N_PARAMS,) and m.dtype == np.float32
    dead = int((m == 0).sum())
    assert dead == PO.N_DEAD == 825
    assert int((_block(m, "g3") == 0).sum()) + int((_block(m, "gb3") == 0).sum()) == 297
    assert int((_block(m, "g4") == 0).sum()) + int((_block(m, "gb4") == 0).sum()) == 33
    assert int((_block(m, "g5") == 0).sum()) + int((_block(m, "gb5") == 0).sum()) == 33
    g2 = _block(m, "g2")
    assert int((g2[:, 13:18] == 0).sum()) + int((_block(m, "gb2")[13:18] == 0).sum()) == 165


def test_live_heads_and_the_encoder_are_unmasked():
    m = PO.live_mask()
    g2 = _block(m, "g2")
    for h in (1, 5, 6, 7):
        assert np.all(g2[:, h] == 1)
    for name in ("w1", "b1", "w2", "b2", "w3", "b3", "g1", "gb1"):
        assert np.all(_block(m, name) == 1)
    g5 = _block(m, "g5")
    assert np.all(g5[:, 1:] == 1) and np.all(g5[:, 0] == 0)


def test_a_generation_leaves_dead_coordinates_untouched():
    # one tiny real generation on CPU (compiles the episode once)
    tr = Trainer(Config(pop=4, episodes=2, chunk=8, n_archetypes=0, warm_frac=0.0), seed=0)
    before = np.asarray(tr.theta).copy()
    tr.generation()
    after = np.asarray(tr.theta)
    dead = PO.live_mask() == 0
    assert np.array_equal(before[dead], after[dead])
    assert not np.array_equal(before[~dead], after[~dead])


def test_trunk_warm_start_copies_only_the_encoder_trunk():
    sys.path.insert(0, "scripts")
    import train as T
    tr = Trainer(Config(pop=4, episodes=2, chunk=8, n_archetypes=0), seed=1)
    fresh = np.asarray(tr.theta).copy()
    old = np.full(PO.N_PARAMS, 7.0, np.float32)
    path = os.path.join(os.environ.get("TMPDIR", "/tmp"), "old_theta_test.npy")
    np.save(path, old)
    T.warm_trunk(tr, path)
    got = np.asarray(tr.theta)
    for name in ("w1", "b1", "g1", "gb1"):
        assert np.all(_block(got, name) == 7.0)
    for name in ("w2", "b2", "g2", "gb2", "g3", "gb3", "w3", "b3", "g4", "gb4", "g5", "gb5"):
        assert np.array_equal(_block(got, name), _block(fresh, name))
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_es_masking.py -q`
Expected: FAIL — `AttributeError: module 'kagg3.core.policy' has no attribute 'live_mask'`.

- [ ] **Step 3: The mask**

Append to `src/kagg3/core/policy.py`:

```python

#: Head outputs nothing decodes any more (PLANNER_V3_1 section 2): 0 was
#: n_hire, 2..4 n_fertilize / feed_daily / care_on, 8..12 the budget order,
#: 13..17 were never read. Live: 1 land, 5 dev_frac, 6 animal_share, 7
#: plant-mix sharpness.
DEAD_HEAD = (0, 2, 3, 4) + tuple(range(8, N_HEAD_OUT))
#: aux[0] was fert_buy; aux[1] (land afford) and aux[2] (free-tile urgency) live.
DEAD_AUX = (0,)


def live_mask() -> np.ndarray:
    """float32[N_PARAMS]: 1 where a parameter can change a decoded output, 0
    where it only feeds a deleted one. ES perturbs and updates the live
    coordinates only -- hygiene that keeps dead blocks at their init for a
    future reactivation, not a speed-up (their noise never reached the live
    coordinates: elementwise Adam, decoupled decay, no norm coupling)."""
    mask = np.ones(N_PARAMS, np.float32)
    shapes = dict(SHAPES)

    def zero(name, cols=None):
        off = offset(name)
        block = mask[off:off + int(np.prod(shapes[name]))].reshape(shapes[name])
        if cols is None:
            block[...] = 0.0
        else:
            block[..., list(cols)] = 0.0

    zero("g2", DEAD_HEAD)
    zero("gb2", DEAD_HEAD)
    zero("g3")
    zero("gb3")
    zero("g4")
    zero("gb4")
    zero("g5", DEAD_AUX)
    zero("gb5", DEAD_AUX)
    return mask


N_DEAD = int((live_mask() == 0).sum())
```

In `src/kagg3/es/train.py::Trainer.__init__` add after `self.n = ...`:

```python
        # Dead parameter columns are neither perturbed nor updated (section 2).
        self.mask = jnp.asarray(PO.live_mask())
```

In `generation` change `eps = perturbations(k, half, self.n)` to `eps = perturbations(k, half, self.n) * self.mask` and the final update to:

```python
        step = self.theta + cfg.lr * mhat / (jnp.sqrt(vhat) + cfg.eps_adam)
        self.theta = jnp.where(self.mask > 0, (1.0 - cfg.weight_decay) * step, self.theta)
```

- [ ] **Step 4: The trunk warm start**

In `scripts/train.py` add after `load_resume`:

```python
def warm_trunk(tr, path):
    """Copy an older theta's encoder trunk (w1, b1, g1, gb1) into a fresh
    lineage; every head stays at its fresh init -- the re-typed outputs
    (section 2) must not inherit biases trained under the old decode."""
    old = np.load(path).astype(np.float32)
    new = np.asarray(tr.theta).copy()
    for name in ("w1", "b1", "g1", "gb1"):
        off = PO.offset(name)
        n = int(np.prod(dict(PO.SHAPES)[name]))
        if off + n > old.shape[0]:
            raise SystemExit(f"--trunk-from {path}: theta too short for block {name}")
        new[off:off + n] = old[off:off + n]
    tr.theta = jnp.asarray(new)
```

add the flag:

```python
    ap.add_argument("--trunk-from", metavar="THETA_NPY",
                    help="fresh lineage: copy this theta's encoder trunk (w1, b1, g1, gb1), "
                         "leave every head at its fresh init")
```

and after the `--resume` handling:

```python
    if args.trunk_from:
        warm_trunk(tr, args.trunk_from)
        print(f"trunk warm-started from {args.trunk_from}", flush=True)
```

- [ ] **Step 5: Run the tests and the full suite**

Run: `python -m pytest tests/test_es_masking.py -q` — Expected: PASS (the generation test compiles one episode on CPU; allow a few minutes).
Run: `python -m pytest -q` — Expected: all pass (`test_gene_sweep.py` shifts a live gene, `land_afford`; `test_fitness_shaping.py` and `test_absolute_eval.py` run generations that now mask).
Run: `ruff check src tests scripts`.

- [ ] **Step 6: Commit**

```bash
git add src/kagg3/core/policy.py src/kagg3/es/train.py scripts/train.py tests/test_es_masking.py
git commit -m "Mask dead parameter columns out of ES and add a trunk warm start for the fresh lineage"
```

---

### Task 9: The fresh lineage and its measurement (§7)

**Files:**
- Modify: `scripts/eval_vs_baselines.py` (`--csv` per-game rows), new `scripts/paired_ci.py`
- Produces: `artifacts/opponents/phase1/main.py` (the incumbent as an engine opponent), `artifacts/zero_theta.npy` (the `z = 0` planner), `artifacts/zero_heldout.csv`, three training runs `artifacts/p2s{0,1,2}/`, a "Phase-2 result" section appended to this plan, and — if the decision rule passes — a promoted `artifacts/theta.npy`.

**Interfaces:**
- Consumes: `scripts/train.py` (`--trunk-from`, `--promote`), `scripts/package_submission.py`, `scripts/eval_vs_baselines.py` (seeds fixed by `default_rng(20260821)`; `env.run([me, opponent])` accepts a Python file path as the opponent).

**Protocol (§7).** Lineage-vs-lineage, never checkpoint-for-checkpoint: the incumbent is the Phase-1 tree's packaged submission with the old `theta.npy`; the challenger is the Phase-2 planner with a theta trained from scratch (trunk warm-started from the incumbent's theta) under an equal rollout budget. Decision on **held-out** seeds disjoint from the discovery seeds, paired by seed and seat, over three training seeds; equal wall-clock budgets; the opponent panel is the incumbent, `starter`, `random`, **kagg2** (`../kaggriculture2/main.py` — the previous-generation agent that defines the −60k gap, an *evaluation* opponent only, never in the training pool: `no-third-party-agents` is about the pool), and the archetype ladder inside training.

**Why kagg2 and a `z = 0` run are gates (gap review 2026-08-24).** Every prior gate measured vs `starter` (already 100% wins, ~85–103k vs 3.5k — it is the absolute anchor, not the win condition) and vs self-play. The forum's payoff-matrix finding (`docs/FORUM_RESEARCH.md` §11) says the ladder pays per opponent, and the only strong opponent we can run in the engine is kagg2. And after Phase 2 the untrained planner is itself a rule-based agent (at `z = 0` it sells, feeds by value, hires by value, fertilizes what pays, prices the churn); the forum's verdict is that rule-based reaches 150k+ and no top entry uses RL. So the cheapest, most diagnostic measurement of the whole phase is the `z = 0` planner vs kagg2, *before* any training: if it already closes most of the −60k margin, the win is in the planner and training is polish; if it does not, the learned values are the gap, and the optimiser defects `kagg3-es-converged` measured (sigma, no absolute anchor, Adam norm diffusion — untouched by this plan except the Phase-3 SNES trial) decide whether Phase 2 can win at all. Either answer is recorded; neither is assumed.

**Headline prediction (§7), stated before the runs.** With the churn priced (0.8 + 1.4 + 1.3), land value flips sign for the trained challenger — it buys quadrants 2–4 at some point in the season and the kagg2 matchup moves: the paired margin vs kagg2 (mean own − kagg2 coins over matched seeds and seats), −59,907 for the shipped `best_abs.npy` at n = 16 on the discovery seeds, is the number this phase exists to move. Falsify early: if no challenger seed buys a second quadrant in the held-out games, the prediction failed regardless of the coin totals. Second pre-registered reading: the `z = 0` planner's paired margin vs kagg2 is recorded before training, and the trained challenger must beat it — a lineage that trains *below* its own `z = 0` posture says the fitness signal, not the planner, is broken.

- [ ] **Step 1: Per-game output and a paired-CI script**

In `scripts/eval_vs_baselines.py` add `ap.add_argument("--csv", help="write one row per game: seed,opponent,seat,mine,theirs")` and, after the results are collected, if `args.csv`: write `csv.writer` rows `(int(seed), opponent, seat, mine, theirs)` for each job/result pair. (`_play` already returns `mine, theirs`; `jobs` carries `seed, opponent, seat`.)

Create `scripts/paired_ci.py`:

```python
"""Paired confidence interval of challenger-minus-incumbent coins over
matched (seed, seat) games. Usage:

    python scripts/paired_ci.py CHALLENGER.csv INCUMBENT.csv --opponent starter
"""
from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict


def load(path, opponent, metric):
    """(seed, seat) -> own coins (`coins`) or own − opponent coins (`margin`).
    `opponent` matches the CSV's opponent column exactly (a name or a path)."""
    rows = defaultdict(dict)
    with open(path) as fh:
        for seed, opp, seat, mine, theirs, *_extra in csv.reader(fh):
            if opp == opponent:
                m, t = float(mine), float(theirs)
                rows[(int(seed), int(seat))] = m if metric == "coins" else m - t
    return rows


def win_rate(path, opponent):
    n = w = 0
    with open(path) as fh:
        for seed, opp, seat, mine, theirs, *_extra in csv.reader(fh):
            if opp == opponent:
                n += 1
                w += float(mine) > float(theirs)
    return w, n


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("challenger")
    ap.add_argument("incumbent")
    ap.add_argument("--opponent", default="starter")
    ap.add_argument("--metric", choices=("coins", "margin"), default="coins",
                    help="own coins, or own minus opponent coins (use margin vs kagg2)")
    args = ap.parse_args()
    a, b = load(args.challenger, args.opponent, args.metric), load(args.incumbent, args.opponent, args.metric)
    keys = sorted(set(a) & set(b))
    diffs = [a[k] - b[k] for k in keys]
    n = len(diffs)
    mean = sum(diffs) / n
    sd = math.sqrt(sum((d - mean) ** 2 for d in diffs) / (n - 1)) if n > 1 else float("nan")
    half = 1.96 * sd / math.sqrt(n) if n > 1 else float("nan")
    print(f"n={n} paired games vs {args.opponent} ({args.metric}): challenger - incumbent = "
          f"{mean:+.0f} coins, 95% CI [{mean - half:+.0f}, {mean + half:+.0f}]")
    for label, path in (("challenger", args.challenger), ("incumbent", args.incumbent)):
        w, g = win_rate(path, args.opponent)
        print(f"  {label}: {w}/{g} wins vs {args.opponent}")
```

(`--csv` rows carry the Step-1b extras after `theirs`; `load` and `win_rate` ignore them.)

Run: `python -m pytest tests/test_submission_runs.py -q` — Expected: PASS (nothing in the shipped tree changed). Commit: `git add scripts/eval_vs_baselines.py scripts/paired_ci.py && git commit -m "Emit per-game rows from the baseline eval and add a paired-CI script"`.

- [ ] **Step 1b: The §7 operational metrics**

§7 requires six per-run operational metrics; none falls out of coin totals. Two sources:

*Engine replays* (`scripts/eval_vs_baselines.py`, from `env.steps`, per game and seat, appended to the `--csv` row): **walking turns** (count of `MOVE` actions issued by the seat), **forced no-ops** (turns whose issued action list was non-empty but the next observation shows no state change — compare `farms[seat]` before/after; the engine's per-step `info`/`status` reports rejected orders if present, use that first), **unsold terminal inventory** (sum of the seat's `private.shed` at the last step), **final quadrants** (`len(farms[seat]["unlocked_quadrants"])` — this is also the headline-prediction count). Extend the CSV header to `seed,opponent,seat,mine,theirs,moves,noops,unsold,quads`; `paired_ci.py` reads by column name and ignores the extras.

*Planner-side* (`src/kagg3/core/plan.py`, numpy only): add `plan.DayStats(NamedTuple)` = `overflow_destroyed` (`max(proj_eod - SHED_CAPACITY - sum(forced), 0)`: certain inflow the forced sale could not absorb, §0.9), `purchase_shortfall` (coins of wanted candidates the greedy did not grant: `sum(values * (j < wants)) - sum(values * (j < n_buy[:, None]))`), `value_dropped` (`sum(tile_value[task & ~admitted])` after the re-admission loop), and a module function `build_day_stats(view, macro, price_table=None) -> DayStats` that runs the same `_derive` + admit/route + sale code and returns the stats instead of the plan. To keep `build_day`'s return tuple (the sim consumes it) unchanged, factor the body into `_plan_and_stats(...) -> (plan_tuple, DayStats)` and have both public functions call it. Add `scripts/plan_stats.py`: replay one engine game (`--seed`, `--theta`, `--opponent`) through `runtime`, call `build_day_stats` each morning, and print the three sums per game; `eval_vs_baselines.py --stats` calls it for every game and appends the three columns. Test: `tests/test_day_stats.py` — the forced-overflow fixture from `test_sell_side.py` reports `overflow_destroyed == 0` and the same fixture with 30 harvested tonight reports 5; the mandatory-tile fixture from `test_admit_route.py` reports `value_dropped == 1500`.

Commit: `git add src/kagg3/core/plan.py scripts/eval_vs_baselines.py scripts/plan_stats.py tests/test_day_stats.py && git commit -m "Log the section-7 operational metrics from engine replays and the planner"`.

- [ ] **Step 2: Freeze the incumbent as an engine opponent**

```bash
P1=$(git log --format=%h --grep="Record the Phase-1" -n 1)
git worktree add /tmp/claude-0/kagg3-phase1 "$P1"
cd /tmp/claude-0/kagg3-phase1
python scripts/package_submission.py --theta /mnt/e/_work/kaggriculture3/artifacts/theta.npy --out /tmp/claude-0/phase1_submission.tar.gz
cd /mnt/e/_work/kaggriculture3
mkdir -p artifacts/opponents/phase1 && tar -xzf /tmp/claude-0/phase1_submission.tar.gz -C artifacts/opponents/phase1
ls artifacts/opponents/phase1/main.py
git worktree remove /tmp/claude-0/kagg3-phase1
ls ../kaggriculture2/main.py      # kagg2 runs from its own tree; nothing to package
```

- [ ] **Step 2b: The `z = 0` planner and the kagg2 baselines, before any training**

The untrained planner is a policy: `theta = 0` decodes to the §2 defaults (reservation `0.8 × base`, no pressure, grow multiplier ×1, `dev_frac`/`animal_share`/land logit at their zero-input values). Save it and measure it on the held-out seeds against the whole panel, and measure the incumbent on the same seeds against kagg2 (the incumbent's `starter`/`random` rows come from Step 4):

```bash
python - <<'EOF'
import sys; sys.path.insert(0, "src")
import numpy as np
from kagg3.core import policy
np.save("artifacts/zero_theta.npy", np.zeros(policy.N_PARAMS, np.float32))
EOF
python scripts/eval_vs_baselines.py --theta artifacts/zero_theta.npy --games 32 --seed-base 20260825 \
    --opponents starter random ../kaggriculture2/main.py artifacts/opponents/phase1/main.py \
    --csv artifacts/zero_heldout.csv
```

(`--seed-base` is added in Step 4; land it first — the two steps are order-free otherwise.) Record, in the result section, the `z = 0` planner's mean coins and win rate vs each opponent and its paired margin vs kagg2, next to the incumbent's. Pre-registered reading: the shipped incumbent's margin vs kagg2 is about −60k; if the `z = 0` planner's margin is inside −20k the planner carries the gap and Step 3's training is expected to finish it; if it is still beyond −40k, the learned values carry the gap, and the result section must say so before the training budget is spent — do not let the training runs be the first place this is learned. A `z = 0` planner that *loses* to `starter` is a Phase-2 defect (the init-posture assertion of Task 1 covers only the sell side); stop and bisect Tasks 3–7 on the frozen zero theta before training.

- [ ] **Step 3: Match the rollout budget and train three seeds**

Read the incumbent's budget: `python - <<'EOF'` printing `gens × pop × episodes` from the run that produced `artifacts/theta.npy` (its `artifacts/<run>/config.json` and the last `gen` in `log.jsonl`; the memory notes say the shipped theta came from a gen-7,500 run). Set `GENS` so that `GENS × 128 × 64` equals that product (`--chunk 8192` = pop × episodes: the zero-padding ceiling from the throughput notes; the script's default 256 pads every device call). §7 also asks for equal *wall-clock*: record the incumbent run's total seconds from its `log.jsonl` and each challenger's; if a challenger's rollout-matched run takes more than 1.25× the incumbent's wall-clock, report both numbers in the result section — the rollout budget is the primary control, the wall-clock ratio is disclosed, not silently equalised. Then, one after another (or in parallel if the GPUs have room — check `nvidia-smi`):

```bash
for S in 0 1 2; do
  nohup python scripts/train.py --run p2s$S --seed $S --gens $GENS --pop 128 --episodes 64 \
      --chunk 8192 --trunk-from artifacts/theta.npy --abs-every 50 > artifacts/p2s$S.log 2>&1 &
done
```

This is a multi-hour job; use `tail -f artifacts/p2s0.log` and stop here if the session cannot wait — the remaining steps are the evaluation and can run in a later session.

- [ ] **Step 4: Held-out evaluation, paired**

The discovery seeds are the script's `default_rng(20260821)` draws; held-out seeds must differ. Add `ap.add_argument("--seed-base", type=int, default=20260821)` to `scripts/eval_vs_baselines.py` (use it in the `default_rng(...)` call) and run, for each seed `S`:

```bash
python scripts/eval_vs_baselines.py --theta artifacts/p2s$S/theta.npy --games 32 --seed-base 20260825 \
    --opponents starter random ../kaggriculture2/main.py artifacts/opponents/phase1/main.py \
    --csv artifacts/p2s$S/heldout.csv
```

and once for the incumbent from the Phase-1 worktree (re-add it) with the same `--seed-base 20260825 --games 32 --opponents starter random ../kaggriculture2/main.py --csv artifacts/incumbent_heldout.csv`. Then:

```bash
K2=../kaggriculture2/main.py
for S in 0 1 2; do
  python scripts/paired_ci.py artifacts/p2s$S/heldout.csv artifacts/incumbent_heldout.csv --opponent starter
  python scripts/paired_ci.py artifacts/p2s$S/heldout.csv artifacts/incumbent_heldout.csv --opponent $K2 --metric margin
  python scripts/paired_ci.py artifacts/p2s$S/heldout.csv artifacts/zero_heldout.csv      --opponent $K2 --metric margin
done
```

Record every line, plus each challenger's win rate and mean margin against `artifacts/opponents/phase1/main.py` and against kagg2 (per-opponent win rates, never a pooled mean — `docs/FORUM_RESEARCH.md` §11), plus — for the headline prediction — the number of held-out games in which the challenger's final `quads` column (Step 1b) exceeded 1, plus the per-seed means of the six §7 metrics (`moves`, `noops`, `unsold`, `overflow_destroyed`, `purchase_shortfall`, `value_dropped`) for challenger and incumbent side by side. The opponent panel here is the incumbent, `starter` and `random` (the archetype ladder is inside training); the spec's frozen historical pool is not available as engine agents and is stated as absent in the result section.

- [ ] **Step 5: Decide and record**

Decision rule, fixed now: rank the challenger seeds by paired margin vs kagg2 (the win condition), and promote the best iff (a) its 95% paired CI vs `starter` excludes 0 on the positive side (no absolute regression), **and** (b) it wins more than 50% of held-out games against the incumbent, **and** (c) its paired margin vs kagg2 does not regress — the 95% CI of challenger − incumbent margin vs kagg2 does not lie wholly below 0 — **and** (d) its paired margin vs kagg2 is not below the `z = 0` planner's (a trained theta worse than its own zero posture is not promoted; it is a finding about the fitness signal). A challenger that passes (a)–(d) but does not *improve* the kagg2 margin beyond its CI is promoted and reported as "no regression, headline not yet moved" — promotion and the headline are separate verdicts. Then `cp artifacts/p2s$S/theta.npy artifacts/theta.npy` and `python scripts/package_submission.py`, and update the memory note on submission packaging. Otherwise, do not promote: the incumbent stays shipped and the result section says which condition failed. Either way, append `## Phase-2 result` to this plan with the training budgets (rollouts and wall-clock), the paired CIs (vs `starter` coins, vs kagg2 margin — against the incumbent and against the `z = 0` planner), the head-to-head win rates per opponent, the `z = 0` planner's own row, the quadrant counts against the headline prediction, the §7 metric table, and the decision with the condition that decided it.

```bash
git add docs/superpowers/plans/2026-08-24-planner-v31-phase2.md scripts/eval_vs_baselines.py
git commit -m "Record the Phase-2 lineage measurement"
```

---

## Self-review notes (written with the plan)

- **Spec coverage, Phase 2 (§8):** §1.2 → Tasks 2–3; §1.3 → Task 5; §1.4 → Task 4; §1.5 → Task 7 (benchmark-gated, with the stop rule); §1.6 → Task 6; §2 decode table → Task 1 (transforms, 32 outputs) with each deletion landing in the task that replaces it (Tasks 1, 3, 5, 6, 7); §2 parameter masking → Task 8; fresh lineage with optional trunk warm start → Tasks 8–9; init-posture assertion → Task 1 (`test_the_initial_policy_sells`); §7 measurement (paired CIs, held-out seeds, three training seeds, equal budgets, opponent panel, headline prediction) → Task 9. §1.1 was Phase 0/1.
- **Deviations from the spec's letter, deliberate and labelled in code:** §1.3 "land at its position" → land is compared two ways *ahead* of the greedy when its logit asks (its value is a logit, not coins, so it has no ratio position); §1.3 "gated by 0.3" → the derived last-purchase-day gate is not implemented in any phase (belongs with M1); §1.5 "run the prefix for each h" → one prefix at zero bill scores every h, one re-derivation with the winner's bill (pass A ignores that the bill shrinks the purse; the benchmark gate is why); §1.6 "nearest-insertion within a block" → admitted tiles are visited in serpentine order with up to three re-admission rounds, no insertion step; §7 "frozen historical pool" → absent from the engine panel; §7 "equal wall-clock" → rollouts are equalised, wall-clock is disclosed.
- **Design decisions the spec left open:** the sell greedy charges the telescoping externality of earlier lots on later ones; the admit stage costs each tile at its ops plus two moves; valuation prices are the sales-window curve — hour-0 inventory drained by the town to the product's first fire plus the farm's own committed pipeline (`inv_h`; `_stream_rev` walks that curve per candidate, so a hundred candidates are priced without clipping) — while feed and fertilizer values (Tasks 4 and Phase 1) stay at hour-0 quotes, since they pay within days; day-29 liquidation passes `sell.LIQUIDATE`, not 0, because an adjusted marginal can be negative.
- **Review 2026-08-24 (folded in):** K-truncated seed/animal valuation → `_stream_rev`; int32 overflow in the top-up key → argmax tie-break; day-29 LAW under pressure → `LIQUIDATE`; mandatory tier lost at the route tail → re-admission rounds; §7 metrics → Step 1b; `--chunk 8192`.
- **Gap review 2026-08-24 (folded in), two gaps found by reading the four phase plans against the measured evidence:** (1) seed/animal candidates were priced off today's hour-0 inventory, which ranks crops by the base-price table — the forum sweep measured that table as almost backwards once the town's drain is counted — → Task 5 prices each list at its sales window (`projector.inv_at_day` + `plan._pipeline_units`, `tests/test_seed_horizon.py`), with the measured caveat that opponent-free melon still ranks first on a fresh board and only its own pipeline un-ranks it; (2) no gate measured the win condition — every criterion was vs `starter` (already 100%) or self-play — → Task 9 adds kagg2 to the held-out panel as an evaluation-only opponent, a pre-training `z = 0` planner baseline (Step 2b), paired *margin* CIs and per-opponent win rates (`paired_ci.py --metric margin`), and conditions (c)–(d) in the decision rule.
- **Type consistency:** `Macro` ends as `plant_target, animal_kind, animal_count, buy_land, hold, press, grow_mult`; `_routes` takes `(order, n_tasks)` from Task 6 on; `_market` takes `lots` from Task 3 on and loses `terminal`; `GROW_ONE` lives in `plan.py` from Task 5 on (`brain.GROW_ONE` aliases it); `feed_rank`/`fert_rank` are defined before the walk from Tasks 4/5 on; `Prefix`/`_derive` exist from Task 7 on; `loop.repeat(xp, n, body, carry)` is what `sell.allocate` and `budget.grant` call; `ADMIT_ROUNDS`/`rank_v` exist from Task 6 on and Task 7's `build_day` carries the same loop; `DayStats`/`build_day_stats` arrive in Task 9 Step 1b and must not change `build_day`'s return tuple.

---

## Phase-2 result (2026-08-25, pre-training measurement; training awaits the user's command)

All nine tasks landed on `fitness-shaping` (5df6afa → cf24c4c, 24 commits including two post-review fix waves; full suite 294 passed). Steps 1–2b of Task 9 are complete; Step 3 (training) awaits the user's explicit command (`p2s0` was launched, stopped after 35 minutes when the final review changed the route key, and not relaunched — `artifacts/p2s0/` holds the aborted run); Steps 4–5 are **pending** on it.

**Host.** One RTX 3070 (8 GB) and 12 CPUs, not the 2×3090 host the incumbent was trained on. Bench (`scripts/bench_sim.py`, B=1024, mean of 3): Task-2 commit 1,529 eps/s → Phase-2 head 1,139 eps/s (compile 60 → 73 s); every task inside the 15% gate (Task 3 −5.2%, Task 4 +14%, Task 5 −14.4%, Task 6 −2.8%, Task 7 −11.8%, Task 9a +1.6%, fix waves −7.8% — of which the budget's second threshold pass is −5.2% alone; unit-by-unit forced-overflow placement was measured at −5.2% for +3.4% revenue and reverted to bulk placement, one documented line to flip).

**Training budget (Step 3).** Incumbent = `work1` gen 7,500 at pop 128 × episodes 256 = 245,760,000 rollouts. Challenger command, per seed S: `scripts/train.py --run p2sS --seed S --gens 30000 --pop 128 --episodes 64 --chunk 8192 --trunk-from artifacts/theta.npy --abs-every 50` (the legacy 3,892-parameter theta; `warm_trunk` copies `w1, b1, g1, gb1`). Measured 4.1 s/gen on this host → ≈34 h per seed; the three seeds must run sequentially here (one 8 GB GPU) or on the 2×3090 host. The incumbent's wall-clock is on the remote host's log; the challenger's is disclosed in `artifacts/p2sS/log.jsonl`.

**Held-out panel (Step 2b), seed-base 20260825, 32 seeds × 2 seats, measured at cf24c4c.** The `z = 0` planner (`artifacts/zero_theta.npy`, `artifacts/zero_heldout.csv`) and the Phase-1 incumbent (`artifacts/opponents/phase1/main.py`, packaged from 5f8bcb0 with the shipped `theta.npy`, evaluated with `--me`; `artifacts/incumbent_heldout.csv`):

| agent | vs starter | vs random | vs kagg2 (`../kaggriculture2/main.py`) | vs phase1 incumbent |
|---|---|---|---|---|
| `z = 0` Phase-2 planner | 100% · 29,893 coins · margin +26,299 | 100% · 30,358 · +30,341 | **0%** · 22,299 · **−130,757** | 60.9% · 27,972 · +1,885 |
| Phase-1 incumbent | 100% · 45,724 · +42,193 | 100% · 43,090 · +43,080 | **0%** · 20,857 · **−146,809** | — |

Paired (n = 64 matched seed×seat games): `z = 0` − incumbent vs `starter` = **−15,831 coins**, 95% CI [−17,729, −13,932]; `z = 0` − incumbent **margin vs kagg2 = +16,053**, 95% CI [+9,984, +22,122].

**Pre-registered readings.** (1) The `z = 0` planner's margin vs kagg2 (−130,757) is far beyond −40k: *the learned values carry the gap* — the planner alone does not close it, and whether training can is decided by the optimiser defects `kagg3-es-converged` measured, which this plan does not touch. Recorded before any training budget was spent, as required. (2) The `z = 0` planner does not lose to `starter` (100%), so no bisect of Tasks 3–7 is needed. (3) Untrained, the Phase-2 planner beats the trained incumbent head-to-head 60.9% of the time and has a 16k better kagg2 margin, but earns 16k fewer coins against a passive opponent — it sells everything (`unsold = 0`) and never buys land (`quads = 1` in all 256 games; the headline prediction concerns the *trained* challenger and is still open).

**§7 operational metrics, held-out means per game (z = 0 planner / incumbent).** MOVE ops 1,092–1,163 / 809–1,026 (walking turns for z = 0: 460–488); forced no-ops 0 / 0.0–0.2; unsold terminal product inventory 0 / 0; final quadrants 1 / 1 (0 of 256 games above 1, both agents). Planner-side (z = 0 only — a packaged file agent has no in-process planner, so the incumbent's three planner metrics are unobtainable): overflow_destroyed 0; purchase_shortfall 13,297–13,943 coins/game; value_dropped 6,648–6,762 coins/game (every task tile whose work is not done, including the route's residue).

**Decision (Step 5).** Pending the three trained challengers' held-out rows: the rule (a)–(d) is unchanged. The incumbent stays shipped until then.
