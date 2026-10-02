# Herd composition (cows vs sheep vs geese) — where the split is decided, what it is worth

Worktree `.claude/worktrees/care-cov` (base 41538be). Subject is **composition**, not timing.
Data: `S/loss6/ledger_days.csv` + `ledger_summary.txt` (the six byte-exact live losses of
sub 56098262, reproduced to the coin — `docs/strategy/2026-09-09-loss6-anatomy.md`) and
`S/carecov/animal_days.csv` (per-animal-per-day census, 3 pinned boards x 2 seats).
Working files `S/herdcomp/`.

## Q1 — where the split is decided

| step | file:line | what it does |
|---|---|---|
| herd **size** | `core/brain.py:923-924` | `animal_share = sig(head[6])`, `animal_count = floor(animal_share * n_dev)` |
| herd **mix** | `core/brain.py:943-946` | `a_mix = clip(out.crew[1:], ±10)`; `wa = softmax(stack(grow[EGG], grow[MILK], grow[WOOL]) * (1 + sig(head[2])*4) + a_mix)`; `animal_want = largest_remainder(wa, animal_count, 3)` |
| pricing / rationing | `core/brain.py:1054` `grow_mult`; `core/budget.py:47-49` one list per animal kind (`L_ANIMAL0..+3`) | the want is priced per kind and can be cut by cash |
| want -> order | `core/plan.py:4815, 5511, 7906-7908` | `w_anim[a]` enters `_wants`; `a_buy` shares the granted budget; one `BUY_ANIMAL` market slot per kind |

**Every input to the mix**, exhaustively:

1. `grow[EGG|MILK|WOOL]` — the encoder's per-product grow head. Its inputs (`brain.features`,
   `:530-551`) are: market inventory `(inv-I0)/T`, `price/base`, `log1p(base)`, `T`, base/above
   targets, **`demand` = `daily_town_demand` (`:183-189`) — units the town removes per whole day
   at TODAY's shop set**, own producing tiles, opponent producing tiles, our shed, first-yield day,
   steady rate. Plus the appended drain block `residual_drain` (`:266-276`) through the `dh`/`ds`
   weights, and the forecast/forward-value blocks.
2. `head[2]` — softmax sharpness, board-global.
3. `out.crew[1:]` — the `animal_mix` gene (`g8`/`gb8` cols 1..3), a fixed per-theta log-share bias,
   **not** board-adaptive.
4. `animal_count` — from `head[6]` and `n_dev`; sets how many of the wants become integers.

So the only board-adaptive channel into the mix is the grow score, and the only sink-shaped
column it carries in the *raw* feature block is **today's** shop demand. The remaining-season
number exists (`residual_drain.share` = fraction of the town's remaining appetite unclaimed,
opponent-inclusive, `:266-276`) but it reaches the mix only through learned `dh`/`ds` weights,
and it is *not* added as a logit the way `animal_mix` is. `PLANT_MIX_DRAIN_ON` (`:958`) does
exactly that add for the five **crops** and ships OFF.

(sections 2-4 follow; checkpoint 1)

## Q2 — what a cow, a sheep and a goose actually returned

Herd by type (GOOSE/COW/SHEEP), six live losses, from `S/loss6/ledger_days.csv`:

| ep | seat | d0 | d3 | d6 | d10 | d15 | d29 |
|---|---|---|---|---|---|---|---|
| 107056463 | ours | 1/3/2 | 1/3/2 | 1/4/3 | 5/6/5 | 6/6/5 | 6/6/2 |
| 107056463 | them | 0/2/2 | 0/4/2 | 2/4/2 | 5/6/5 | 5/6/6 | 5/6/4 |
| 107067869 | ours | 1/3/2 | 1/4/2 | 1/6/2 | 2/10/6 | 2/10/8 | 2/6/4 |
| 107067869 | them | 0/2/2 | 0/4/2 | 0/6/2 | 0/9/7 | 0/9/8 | 0/9/6 |
| 107068399 | ours | 1/3/2 | 1/3/2 | 1/4/3 | 4/5/6 | 6/5/6 | 6/5/3 |
| 107068399 | them | 0/2/2 | 0/4/2 | 2/4/2 | 4/6/6 | 5/6/6 | 5/6/4 |
| 107070717 | ours | 1/3/2 | 1/3/2 | 1/4/3 | 5/5/6 | 6/5/6 | 6/5/0 |
| 107070717 | them | 0/2/2 | 0/4/2 | 0/6/2 | 3/8/5 | 3/8/6 | 3/8/6 |
| 107072760 | ours | 1/3/2 | 1/3/2 | 1/4/2 | 1/10/4 | 1/11/4 | 1/11/2 |
| 107072760 | them | 0/2/2 | 0/4/2 | 0/6/2 | 2/8/6 | 3/8/6 | 3/8/6 |
| 107079367 | ours | 1/3/2 | 1/3/2 | 1/3/5 | 1/4/11 | 1/4/12 | 1/4/10 |
| 107079367 | them | 0/2/2 | 0/4/2 | 0/6/2 | 0/8/8 | 0/8/9 | 0/8/9 |

The clone is the **same open-loop recipe on all six**: 2 COW + 2 SHEEP d0, +1 COW d2, +1 COW d3,
+2-3 COW d6, +1-2 COW d7, sheep only from d8. **Cows first, always, whatever the town does.**

Ours follows the last shop to unlock, on a one-day lag, on all six:

| ep | shop | our next buys |
|---|---|---|
| 107079367 | **YARN_STORE d3** (the only wool sink) | d4 S, d5 S, d6 S, d8 SSS, d10 SSS, d11 S — **11 sheep, 1 cow** |
| 107067869 | PIZZA d3 / YARN d9 | d3 C, d5 CC, d8 CC, d9 C — then d9 S, d10 SS, d11 S, d12 S |
| 107072760 | SMOOTHIE d3, ICE_CREAM d6, PIZZA d9 | d5 C, d8 CC, d9 C, d10 CCC, d11 C — 11 cows, 4 sheep |
| 107070717 | BAKERY d3, BRUNCH d6 (egg) | d8 G, d9 G, d10 GG, d11 G — 6 geese |
| 107068399 | BAKERY d3, PET_CAFE d6, BAKERY d9 | d9 G, d10 GG, d11 G, d12 G |
| 107056463 | BAKERY d3, ICE_CREAM d9 | d8 G, d9 G, d10 GG + d10 C, d11 G |

### The 3.35k/cow, 2.87k/sheep slopes are NOT general

Realised coins per animal-day, our seat (units x the price actually received / animal-days):

| ep | milk sink | wool sink | egg sink | **coins/cow-day** | **coins/sheep-day** | coins/goose-day | cow:sheep |
|---|---|---|---|---|---|---|---|
| 107056463 | 426 | 138 | 192 | 198 | 64 | 60 | 3.09 |
| 107067869 | 336 | 282 | 120 | 62 | 129 | 77 | **0.48** |
| 107068399 | 174 | 318 | 318 | 41 | 129 | 80 | **0.32** |
| 107070717 | 390 | 30 | 336 | 88 | 40 | 91 | 2.23 |
| 107072760 | 660 | 174 | 30 | 262 | 82 | 61 | 3.19 |
| 107079367 | 462 | 354 | 228 | 225 | 133 | 87 | 1.68 |

`sink` = season units the town removes, computed from the board's shop schedule with the engine's
own rule (`kaggriculture.py:728-748`: 6 shop ticks a day, `multiplier = 2` for a one-product shop,
plus the town centre's 1/day). **A cow returns between 41 and 262 coins a day and a sheep between
40 and 133; the cow-versus-sheep advantage flips sign on 2 of the 6 boards.** 3.35k/cow and
2.87k/sheep are the mean of a six-board spread, not a coefficient.

What *is* general is the sink:

    corr(season WOOL sink, coins per sheep-day) = +0.98   (n = 6)
    corr(season MILK sink, coins per cow-day)   = +0.89
    corr(wool sink / joint wool supply, sheep-day) = +0.83
    corr(milk sink / joint milk supply, cow-day)   = +0.91

**A YARN_STORE is worth 12 wool a day — twice any milk shop's 6 — because it is the only
one-product animal shop and `_town_consume` doubles those.** That is why one YARN_STORE on d3
pulled 11 sheep on 107079367, on a board whose season sinks were 462 milk against 354 wool.

Geese are never the loss: 60-91 coins a goose-day against 300 a head, on a first yield at d4 and a
1-day interval. They are the cheap filler and the census shows no board where they are the error.

## Q3 — counterfactual, priced on the engine curve, two purses

The curve is `market_price` (`kaggriculture.py:192-206`) with `MARKET_PARAMS` (`:41-51`):
**MILK glut is linear** (`above_func linear`, target 1.60, `amp = 1.6*160/122 = 2.098` coins a unit)
and **WOOL glut is quadratic** (`above_func sq`, target 3.20, `amp = 3.2*200/105^2 = 0.0581`, so
wool is worth 107 at 40 units over and 5 at 58 over). Both seats sell into **one** shared
`market["inventory"]` (`_process_market:544-628`, `_commit_unit:652-688`).

`S/herdcomp/cf.py` walks each board day by day on that exact curve: the day's town drain and both
seats' recorded per-day sell volumes, six chunks a day, `market_price` per unit. It reproduces the
recorded ledger to 1-13 % (mostly 3-8 %), which is the fidelity these numbers carry. The opponent
is an **open-loop tape**, so holding their sell schedule fixed is exact rather than an assumption.

Counterfactual A — our herd takes the clone's cow share of the same animal-days:

| ep | cow-days -> | our purse | their purse | **two-purse margin** |
|---|---|---|---|---|
| 107056463 | 157 -> 161 | +128 | −399 | **+527** |
| 107067869 | 244 -> 263 | +185 | +1,180 | **−995** |
| 107068399 | 137 -> 160 | −254 | +822 | **−1,076** |
| 107070717 | 137 -> 202 | +966 | −6,398 | **+7,364** |
| 107072760 | already above the clone's share (0.67 vs 0.51) | — | — | — |
| 107079367 | 110 -> 211 | **−6,469** | **−14,012** | **+7,543** |

Mean **+2,227 coins of margin a game**, and it is **denial, not income**: on the −22.2k board the
re-mix *costs our own purse 6.5k* (our +118 milk units push the shared market from 191 into glut)
and costs theirs 14.0k. Their 45.7k of milk was only available because we did not contest it.
Two of six boards are negative; the mean is carried by two.

Counterfactual B — cow share = milk sink / (milk + wool sink) — is **not** better: mean +2,012,
and it overshoots to −5,483 on 107056463, where the milk sink is 426 against a *joint* supply of
375. The right target is therefore the **residual** (sink minus both boards' committed supply),
not the raw sink — which is exactly what `residual_drain.share` is.

## Q4 — the lever: `brain.ANIMAL_MIX_DRAIN_ON` [SWITCH, ships OFF]

`src/kagg3/core/brain.py:816-864` (block) and `:999-1008` (the branch). 10 lines of code.

    if ANIMAL_MIX_DRAIN_ON:
        wa = _softmax(stack(grow[EGG], grow[MILK], grow[WOOL]) * (1 + sig(head[2])*4) + a_mix
                      + ANIMAL_MIX_DRAIN_GAIN * stack(drain[EGG,1], drain[MILK,1], drain[WOOL,1]))
    else:
        wa = <the shipped expression, character for character>

The smallest lever available, and smaller than a cow floor: it changes **no constant of the game**
and adds **no rule**. It swaps the sink the mix is priced against — today's `daily_town_demand`,
which the YARN_STORE doubling structurally biases towards wool — for the season's *unclaimed*
appetite, which the planner already computes and already feeds the crops
(`PLANT_MIX_DRAIN_ON`, `:957`). `animal_count` is untouched, so this is not a timing or size
lever under another name. `ANIMAL_MIX_DRAIN_GAIN = 0.5`; `PLANT_MIX_DRAIN_GAIN = 1.0` lost
decisively on the crops (t = −15.4), so 1.0 is a ceiling here, not a guess.

`tests/test_animal_mix_drain.py`, 5 tests, all pass, plus `test_crew_and_herd_mix`,
`test_mixed_herd`, `test_animal_count_semantics`, `test_drain_feature` (70 passed, 3 skipped):

* OFF, the herd want is bit-for-bit the champion decode over 400 fixture days **with the gain set
  to 7.5** — it is never read;
* OFF, **every field of the Macro** is bit-identical with the gain at −3.25;
* ON, the herd moves towards higher unclaimed `share` and at least one day changes;
* ON, `sum(animal_want)` is unchanged on every day — a mix lever, not a size lever;
* ON at gain 0 is OFF, bit-for-bit.

Planner A/B, `S/herdcomp/planab.py`, 180 hour-0 states = 3 pinned boards x 2 seats x 30 days,
theta `flow135_g350_gpfwdfv_gb028`, decode + `build_day`, per game:

| gain | want GOOSE | want COW | want SHEEP | unit-turns | PASS | PLANT |
|---|---|---|---|---|---|---|
| OFF | 6.3 | 13.2 | 12.7 | 6,516 | 1,123.2 | 171.2 |
| 0.5 | +0.8 | +0.2 | **−1.0** | +0.0 | −0.7 | +0.0 |
| 1.0 | +0.5 | **+0.5** | **−1.0** | +0.0 | −0.7 | +0.0 |
| 2.0 | +2.5 | −0.2 | **−2.3** | +0.0 | +0.3 | +0.0 |

Gain 1.0 is the cow-versus-sheep setting; by 2.0 the whole tilt goes to geese (EGG carries the
largest unclaimed `share` on these boards) and the cow leg reverses. The A/B is open-loop — the
states come from the OFF-arm trajectory, so the standing herd cannot respond and `have_*` is
unchanged by construction. It reads the **decision**, not the season.

## What is not verified

* **No engine read.** The chained legs are the caller's.
* The counterfactual's *yields* are linear in animal-days at our own realised per-animal-day rate;
  only the *prices* come from the engine curve. A cow bought on d10 is not a cow bought on d0.
* The market walk reproduces the recorded per-product income to 1-13 %; it does not model the
  intraday slot interleave, the shed cap, or a sale that hit the $1 floor.
* Every correlation here is n = 6 on one opponent family (all six losses are the same
  5-HIRE/2-COW/2-SHEEP/12-MELON clone, `loss6-anatomy.md` section 4).
* The three pinned boards were used for the planner A/B only; their own realised per-animal
  revenue was not ledgered (`S/carecov/animal_days.csv` carries the census, not the money).
