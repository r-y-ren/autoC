# Land-veto switch review — c97cd6e (`land-veto`, base `arms-next` 45f8217)

## 1. OFF byte-identity — clean

The decode and `land_ok` lines are character-identical to base. All three
switches are plain Python `if`s on module bools: OFF adds no ops, no
dtype/rounding move; every `.astype(i32)` is inside an ON branch.

Tests: **69 passed** — land_veto_switch 30, land_value 15, prospective_land 10,
budget_order 9, land_affordability 5.

`test_backend_agreement.py` **FAILS**: 2/2400, `hire_bias numpy=33 jax=32`
(decisions 1532/1533). **Pre-existing** — base 45f8217 in a scratch checkout
fails identically. Not this diff, but `arms-next` carries a backend divergence.

## 2. Semantics

ZERO sets `land_bias` to int32 0, so the gate is exactly `land_value > 0` with
the unchanged `nquad<4 & ~terminal & money>=land_gap & money>=land_cost//2`.

But `land_ok = (land_bias > -land_price) & (nquad<4) & (view.money>=land_cost)`
then holds on *every affordable* board, while `buy_land` still needs
`land_value>0` and the post-bill/post-reserve purse. Measured (d6, nquad=1):
money 1,000 → `land_ok=1`, `buy_land=0`. One-sided for placement
(`_wants` clips) but not free: `n_free` feeds `dev_frac`/`n_dev`, and the
exploratory `_derive` at `hire_bill=0` (plan.py:6011) sizes the hire ladder on a
50-tile board. The reverse gap survives (brain reads gross `view.money`).

**Saturation premise is half true.** On `artifacts/theta.npy`: quadrant 4 is at
−4,000 at every purse, but quadrant 2 decodes −836 at 3,000 coins, **+93** at
10,000, saturating only above ~80k. ZERO also overrides a *live* gene early.

## 3. Override plumbing

`brain` does `from . import plan as P` and reads `P.NAME` inside `decide` — so
under numpy, **at call time**. The judge's `setattr` reaches
`plan_stats.make_macro → brain.decide(np, …)`, built at
`eval_vs_baselines.py:312` from the working tree before `_vendored_imports`.
Hazards: under `jax.jit` (es/train.py:1092) the branch bakes **at trace time**,
so a later `setattr` is ignored; a `--me <pkg>.tar.gz` seat plans in its own
module image and scores as OFF.

## 4. Day-0 risk — confirmed, collides with OPEN_PUMP

Probe: under ZERO the shipped theta buys quadrant 2 on days 0–3 at every purse
from 3,000 down to **1,500**; OFF, on none. Day 0 from 3,000 (TURN_HIRE 0,
TURN_BUY 1, SELL_TURNS (3,10,18); BUY_LAND rides slot 9 of turn 3):

1. Pump gate reads `view.money>=1584` at plan time (3,000); land is charged two
   turns later, so ZERO cannot suppress the pump — the land buy breaks instead.
2. turn 0/1: pump takes 53 wheat on a 25→32 quote, ≈1,400–1,700 out; hires behind.
3. turn 1: greedy spends `purse = money − land_gap` (the 1,000 *is* reserved).
4. turn 1 B_WHEAT: sell-back of 48 recovers most; net ≈110 plus slippage.
5. turn 3 slot 9: BUY_LAND charges 1,000.

The pump is sized *after* `_derive` fixed the purse, so its net cost is absent
from `money`: the gate reserved ~110–400 coins too few, and a **failed BUY_LAND
is not a no-op** (plan.py:176) — every prospective op no-ops, stranding turn-1
seed/animal coins. Only floor is `money >= land_cost//2` = 500.

## 5. Verdict — fix first

Code is correct, OFF is safe, but the arm is not *interpretable*: raw ZERO
confounds "remove the quadrant-4 wall" with "buy quadrant 2 on day 0 against a
live gene, in front of a measured +21.5k pump". Add a day floor
(`LAND_VETO_MIN_DAY`, arm from day ≥ 2), or split the read by first-purchase
day; then judge FLOOR(0.5) and ZERO paired, on the theta seat, not `--me`.
