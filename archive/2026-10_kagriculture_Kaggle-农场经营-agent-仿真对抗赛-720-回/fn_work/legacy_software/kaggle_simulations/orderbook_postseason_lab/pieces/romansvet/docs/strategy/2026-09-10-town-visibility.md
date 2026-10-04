# Can the trained theta see the town's shop draw?

Tree: `.claude/worktrees/arms-next`. Theta: `artifacts/kagg2_games/thetas/flow172_g1000.npy`
(6,789 params = `policy.N_PARAMS`, so every appended block is live). Fixture:
`tests/data/trajectory_obs.npz`, 2,400 recorded observations, `opp_t_day`/`opp_t_yield`
filled with zeros (the fixture predates them).

## 1. What reaches the network

`PolicyObs.shops` is `int[8]` — the **per-kind** unlocked-shop count in `spec.SHOP_NAMES`
order (`brain.py:107`), built by `agent/parse.py:140 parse_town`. The raw draw is already
in the observation. Three paths carry it into `decide`:

1. **`prod_feat` column 6**, the main one: `daily_town_demand` (`brain.py:183-189`) is
   `shops @ _SHOP_DAILY + _CENTER_DAILY`, units the town removes per day, entered as
   `demand / 20.0` (`brain.py:546`). **Linear, unclipped, product-identified** — the
   per-product sink index §4-5 regresses on. Its sd across the fixture is 6.8-11.9
   units/day per product: real variance, not a near-constant.
2. **`drain_feat`** — `expected_drain` (`brain.py:192-210`) x `residual_drain`
   (`brain.py:227-276`), two columns `gap`/`share` clipped at `DRAIN_CLIP = 4.0`.
3. **`glob_feat[18]`** = `sum(shops) / 8.0` (`brain.py:590`) — count only, no identity.

In `policy.forward` the demand column enters `w1` and the drain columns add through
`dh`/`ds` (`policy.py:635,637`); the product summary then reaches the global head through
`gp` (`policy.py:646`), so `head[2,5,6,7]`, `crew`/`animal_mix` and `sat` are product-identified too.

**Timing is not visible.** Only the cumulative multiset survives — which kind arrived at
the day-3/6/9 unlock, in what order, is unrecoverable. Undrawn shops are priced at the
mean row `_MEAN_SHOP_DAILY` (`brain.py:56`) over the calendar constant `_SHOPS_ON_DAY`
(`brain.py:65`) — a function of `day`, not of the draw.

## 2. Do the read weights and the decisions move?

Read-weight norms are ordinary, not vestigial: `w1` row 6 (demand) 2.012 vs 1.69-2.20 for
the other product rows; `w1` row 30 (shop count) 1.833; `g1` row 18 1.398 vs 1.09-1.57;
`dh` columns 2.06 / 1.879; `ds` = [[.506,.217],[.124,.830]]; `gp` rms 0.112.

Sensitivity, 300-600 fixture decisions, ±1 shop instance, deltas vs. the unperturbed decode:

| perturbation | wool `grow_mult` | wool `hold` | wool `press` | crop mix changed | herd mix changed |
|---|---|---|---|---|---|
| +1 YARN_STORE | **+105 (+26.7 %)** | **+30.7 (+64 %)** | **-26.2 (-70 %)** | 58.8 % | 5.4 % |
| +1 PET_CAFE | carrot -40.5 (-9.6 %) | carrot -1.9 | carrot -10.4 (-57 %) | 49.7 % | 1.0 % |
| +1 PIZZA_SHOP | milk +33.7, tomato +15.2 | milk +7.8 | tomato -4.8 | 63.7 % | 7.3 % |

The response is product-specific and correctly signed for wool: one more yarn store makes
the theta value a sheep 27 % more, hold wool for 64 % more per unit and drop its sell
pressure 70 %. The drain block is not a saturating bottleneck: `gap` saturates only on
strawberry (69.5 %) and wool (7.5 %), `share` on melon/fertilizer by construction and
~10-18 % elsewhere; `grow_mult` hits `GROW_MAX` on 10.2 % of products.

## 3. Verdict — question (4)

**The theta can see the draw and does respond.** No observation work is warranted; the
mid-tier losses of §4-5 are the ES's to fix, not a blindness.

Two honest caveats, neither an observation gap:

* `animal_want` barely moves (mean |Δ| 0.007 animals) because `animal_count =
  floor(sig(head[6]) * n_dev)` is zero on 90.7 % of decisions — the herd *size* is a
  scalar decided before the mix, and the yarn response reaches the herd through
  `grow_mult` into `budget.grant`, not through `animal_want` (`brain.py:941-947`).
  Our step-function sheep count across yarn counts is that path working.
* PET_CAFE's sign is inverted: more carrot sink makes the theta plant *less* carrot
  (`plant_target` carrot -0.47, `grow_mult` -9.6 %). That is a learned response with a
  questionable sign — a fitness/curriculum question, not a feature question.

## 4. If an extension were wanted anyway (not recommended)

The only genuinely absent facts are unlock **order** and the identity of undrawn shops.
Smallest zero-init block: append `("sh", (8, N_HEAD_HID))` after `fv` — the raw
`shops/2.0` vector onto the global head's pre-activation, `gpre + shops_feat @ p.sh`,
parenthesised outside `fv`'s add so every 6,789 theta stays a bit-exact prefix.
N_PARAMS 6,789 -> 7,045 (+256). Per the gene rule, measure the decodable slope at sigma
0.02 first: perturb `sh` alone over ~200 antithetic pairs on the fixture and require a
non-zero mean |Δ| in `animal_want` and `plant_target`. A zero-init matmul off a nonzero
input is not stationary, so a slope should exist — but §2 says the head already has this
signal through `gp`, so expect a null.
