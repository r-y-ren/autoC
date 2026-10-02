# Planner wall audit B — independent, blind (2026-09-10)

Question: does the hand-written planner carry FIXED (non-theta) logic that binds, so ES
pushes against it and cannot pass? Source read: `.claude/worktrees/arms-next/src/kagg3/`
(6,789-param lineage; `PO.live_mask` leaves **5,997 live** coords, 792 masked dead —
`prio`/`lots` are computed in `policy.forward:649-650` and read by nobody, correctly masked).

Method: decoded `brain.decide` in numpy over **2,400 real decisions** (`tests/data/trajectory_obs.npz`,
40 seeds x 30 days x 2 seats; `opp_t_day/opp_t_yield` reconstructed exactly from the paired row)
for the seven lineage thetas, plus the zero-feature (bias) decode. Scripts in the session scratchpad.

**Verdict: yes — five walls, and all five are inside `brain.decide`'s gene decode, not in `plan.py`.**

## A. Gene saturation (traj mean over 2,400 decisions; bias = value at zero features)

| gene | clip bounds (file:line) | bias | f135_g350 | f166_g170 | f172_g60 | g170c | g300 | g940 | g1000 | flag |
|---|---|---|---|---|---|---|---|---|---|---|
| `land_bias` | `+/- land_price`, `LAND_BIAS_STEPS=256` brain.py:640,896-898 | **-1000 = -land_price, all 7** | -972 | -882 | -888 | -874 | -980 | -902 | -840 | **AT THE VETO RAIL 30-71 % of days** |
| `compact` | `[0, DIST_MAX=8]`, floor caps at 7, brain.py:650,1064 | 5/2/0/1/2/6/6 | 6.66 | 6.68 | 6.86 | 6.97 | **7.00** | **7.00** | **7.00** | **SATURATED, monotone** |
| `dev_weight` | `[0, GROW_MAX*GROW_ONE=1024]` brain.py:646,1067 | 38..91 | 41.6 | 49.4 | 46.6 | 58.7 | 60.7 | 66.8 | 66.3 | pinned <<256 (=x1); rising |
| `hire_bias` | `+/- HIRE_BIAS_MAX=400` brain.py:673,1082 | -136..-185 | -15.7 | -55.5 | -37.8 | -57.1 | -83.6 | **-227.6** | **-227.4** | drifts negative; never within 5 % of the bound |
| `crew_target` | `[0, MAX_HANDS=16]` brain.py:699,1108 | **0, all 7** | 6.50 | 7.40 | 6.90 | 6.47 | 6.48 | 4.16 | 4.74 | falling, not saturated |
| `animal_defer` | `[0, DEFER_ONE=256]` brain.py:714,1112 | **0, all 7** | 0.01 | 0.00 | 0.00 | 0.44 | 1.10 | 0.00 | 0.00 | **DEAD GENE** |
| `forward_days` | `[0, FWD_DAYS_MAX=6]` brain.py:721,1136 | 0/3/1/0/0/3/3 | **0.00** | 1.66 | 1.49 | 2.12 | 1.42 | 1.74 | 2.42 | hits 6; f135 gene is zero |
| `grow_mult` WHEAT | `[0,1024]` brain.py:1054 | | 759 | 778 | 775 | 730 | 743 | 746 | 722 | **on the 1024 rail 52-55 % of days** |
| `grow_mult` FERT | same | | 29.9 | 41.5 | 50.8 | 57.2 | 61.0 | 69.0 | 67.6 | near floor |
| `press` MELON | one-sided `relu(tanh)*base` brain.py:1053 | | 20.0 | 22.7 | 4.2 | 3.9 | 79.2 | 70.7 | 116.0 | live, no bound |
| `hold` STRAWB | `[0, COIN_CAP-1]` brain.py:1051 | | 13.5 | 33.2 | 47.1 | 51.5 | 78.9 | 94.8 | 79.3 | far from cap; rising x7 |
| **`plant_target` MELON** | — | | **0.000** | **0.000** | **0.000** | **0.000** | **0.000** | **0.000** | **0.000** | **never planted, 0/16,800** |
| `animal_want` total | — | | 1.28 | 0.59 | 0.45 | 0.36 | 0.37 | 0.21 | 0.21 | herd walked to zero |

### Rail-occupancy, measured (% of the 2,400 decisions on the clip)

| rail | f135 | f166_g170 | f172_g60 | g170c | g300 | g940 | g1000 |
|---|---|---|---|---|---|---|---|
| `grow_mult == 1024` on some product (`GROW_MAX`) | 53.5 | 55.2 | 54.3 | 52.1 | 52.2 | 53.8 | 52.5 |
| `compact == 7` (`DIST_MAX`) | 65.6 | 68.3 | 86.3 | 96.7 | **100** | **100** | **100** |
| `land_bias <= -land_price` (land vetoed) | 45.0 | 35.6 | 30.1 | 30.0 | **71.4** | 57.6 | 52.3 |
| `forward_days == 6` (`FWD_DAYS_MAX`) | 0.0 | 3.3 | 0.0 | 8.7 | 0.0 | 1.5 | **30.3** |
| `animal_defer == 0` (dead) | 99.9 | 100 | 100 | 95.3 | 88.2 | 100 | 100 |
| melon `plant_target > 0` | **0.0** | **0.0** | **0.0** | **0.0** | **0.0** | **0.0** | **0.0** |
| `dev_weight == 1024`; `crew_target == 16`; `|hire_bias| >= 380` | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

### The five walls

**W1 — `GROW_MAX = 4.0` binds on 52-55 % of all days, in every theta** (brain.py:646, applied at
:1054). `_unit_ratio(grow)` is *also* what `budget.grant` prices a unit at, so any two products
whose scores both clear 4x are **indistinguishable to the purse**. brain.py:940 records this exact
defect once already — *"a want of 0.67 sheep written in the grow score placed 21 COW and 0 SHEEP"* —
and the fix (`a_mix`, g8 cols 1-3) moved only the *want*, deliberately leaving the *valuation*
clipped. Wheat and strawberry sit on this rail on most days; the ES cannot tell the planner that one
is worth more than the other, because the clip erases the difference before `grant` sees it.
This is the most frequently binding fixed number in the decode, and no doc names it.

**W2 — `compact` is saturated at `DIST_MAX`, monotonically, and the three newest thetas are at the
rail on 100 % of days** (65.6 -> 100 across the lineage; brain.py:650, 1064). The planner develops as
tightly around the shed as the rail permits and keeps asking for more.

**W3 — `land_bias` sits at exactly the veto value on 30-71 % of days.** `land_ok = (land_bias >
-land_price) & ...` (brain.py:913); `land_bias = land_price * _qfloor(tanh(z)*256) // 256`, so a
saturated-negative gene decodes to **exactly** `-land_price` and the strict `>` fails. The zero-feature
decode is `-1000` on a 1,000-coin quadrant for all seven thetas. The archive says the same thing from
the other end: *"The planner cannot express 'one extra quad on day 0, all melon' … land purchase has
no switch and its bias is a gene"* (2026-09-09-plateau-review-verdicts.md:560). A gene on a rail is a
zero-gradient half-space, not a preference.

**W4 — melon is never planted: `plant_target[MELON] == 0` in 16,800/16,800 decisions.** The cause is
**not** the `absorb` gate, which I hypothesised and the data refuted: `out.sat` is *positive* for
every theta (mean 0.09-0.56), so melon passes `absorb` on 65-100 % of days. The block is the
proportional mix itself: `w = softmax(grow * (1 + sig(head[7])*4))` then `_largest_remainder`
(brain.py:958-1026). Melon's `grow_mult` averages 187-249 while wheat/strawberry are 722-778 *and
clipped together at 1024* (W1), so melon's share of `plant_total` never rounds up to one whole tile.
The top-tier opening needs **12 melon tiles on day 0**; a proportional split over a clipped score
cannot produce a corner allocation. The loss it gates is -14.1k/game, decisive in 69 of 88 live
losses (2026-09-05-build-story.md:788, 2026-09-10-residual-loss20.md).

**W5 — `animal_defer` (`g10` ramp[3]) is dead:** exactly 0 on 88-100 % of days, 100 % on five of the
seven thetas. Per MEMORY's gene-slope rule this gene has no decodable slope in the shipped regime.

Watch, not yet a wall: `forward_days` hits `FWD_DAYS_MAX = 6` on 30.3 % of `flow172_g1000`'s days
against 0.0 % for `flow135` — the newest theta is walking into that ceiling.

**Not walls:** `hire_bias` never reaches 5 % of +/-400 (max |mean| 227.6); `crew_target` never
reaches `MAX_HANDS`; `dev_weight` never reaches its cap (but never exceeds x1 = 256 either, so
development is *always* cheaper than a harvest to the router - a rail at the bottom); `hold` and
`press` move freely.

## B. Hard-constant inventory, ranked by coins at stake x unmeasured-ness

| # | constant | file:line | value | coins at stake | measured? |
|---|---|---|---|---|---|
| 1 | `cash_reserve = HIRE_BILLS[n_hire+1]` | plan.py:3573-3606, spent at :5138, gates hires at :6107 | fib cumsum; 986 at 14 hands | the whole purse, every day; also defunds `buy_land` (verdicts.txt:452) | **NEVER A/B'd.** Docstring: *"Nothing here is learned … cannot be tuned into uselessness"* |
| 2 | `HIRE_BIAS_MAX = 400` / `CREW_TARGET_PUSH = 400` | brain.py:673 / plan.py:3157 | 400 | sized to beat fib(14)=377 and NOT fib(15)=610 -> a **hard crew ceiling at 14 hands**; loss anatomy = their 12 hands vs our 6 at d10 | ceiling never swept; `CREW_FROM_TASKS` (-4,580) changed pricing, not the cap |
| 3 | `GROW_MAX = 4.0` (clips `grow_mult`, which `budget.grant` prices with) | brain.py:646, 1054 | 4.0 | erases the score gap between every product on the rail, 52-55 % of days; the melon corner (-14.1k) is downstream | **never swept.** The 2026-08-28 COW/SHEEP note fixed the *want*, not the valuation |
| 4 | `land_ok` strict `>` + `LAND_OWN_DEN=2`, `LAND_REV_NUM/DEN=3/4` | brain.py:913; plan.py:190,179 | 2; 3/4 | day-0 quadrant, additive-melon path | `LAND_REV` level; **`LAND_OWN_DEN` never A/B'd**; the `>` never |
| 5 | `SHED_CAPACITY` room = 100 (one pool: wheat+fert+animals) | plan.py:5157, 6635 | 100 | *"shed cap 100 total is the binding constraint (LIVE peaks 96/100)"* verdicts.txt:303 | `SHED_OVERFLOW_ON` inert (0 coins/122 boards) |
| 6 | `EST_LEAD=5`, `EST_MOVES=1`, `EST_HOME=3`, `ADMIT_ROUNDS=3` | plan.py:171,149,3019,210 | 5/1/3/3 | `5*(h+1)` turns off every admit budget | `EST_LEAD` LEVEL, `EST_HOME=7` +188 t 1.0 LEVEL, `EST_MOVES=1`->2 -21,499 |
| 7 | feed-wheat + day's-fertilizer sell abstentions | plan.py:6580, 6588 | — | `FEED_RESERVE_ON DAYS=2` = -2,666 ours / +812 theirs | measured, dead |
| 8 | `SELL_TURNS=(3,10,18)`, `N_LOTS=3` | ops.py:126, sell.py:44 | 3 lots | sell-hour headroom re-measured **zero** | closed (-165/-77/-77 noise) |
| 9 | `DRAIN_CLIP = 4.0` / `absorb` gate | brain.py:224, 1014 | 4.0 | melon `share` pinned at the floor makes the gate a sign test on `sat`; **currently OPEN** (sat > 0), so not the melon blocker | drain *gain* measured (`PLANT_MIX_DRAIN_ON` -11,906); the **clip** never |
| 10 | `CHAIN_MAX=6`, `STREAM_MAX=32`, `MO=10` | plan.py:139,4026,138 | 6/32/10 | silent op drops; animal lifetime value | never swept |
| 11 | `n_adm = min(count_le(cum_est0,turns_h), n_tasks0)` (crew priced on TODAY's tasks) | plan.py:5955/5964 | — | melon tiles emit no task d1-5 -> crew collapses to 0-1 | attacked 3x: FORWARD_ADMIT -8,676, CREW_FROM_TASKS -4,580, JOINT_PLATE -41.9k |
| 12 | no same-day sale path | sim/units.py:171, eod.py:210 | — | ~600/game | SAME_DAY_HARVEST -4,186, SELL_REPRICE -4,964, MIDDAY_DROP -4,311 |

## C. Shortlist — 5 rules worth exposing as a gene or re-measuring

| rule | experiment | judge | why the archive has not closed it |
|---|---|---|---|
| **1. Melon corner allocation (brain.py:958-1026, 646)** | the mix is `softmax(grow*(1+sig(head[7])*4))` -> `_largest_remainder`, and `grow_mult` is clipped at `GROW_MAX`. Two changes, each inert at theta zero: (a) raise `GROW_MAX` 4 -> 16 so `budget.grant` can rank two strong products; (b) append a per-crop `plant_floor` gene (`g12`, 32->5, `floor = _qfloor(N_TILES*relu(tanh(z))/8)`) so a corner opening is *expressible*. Measure the decodable slope at the training sigma before launch (MEMORY gene-slope rule). Warm-start `flow172_g300`. | paired LIVE55 + TOPB; drawn legs veto only | every melon experiment on file forced a *fixed* opening (MELON_OPEN -19,557; MELON_D10B -22.1k; additive-melon) and each was a switch outside the theta. Nobody measured that melon `plant_target` is 0 in 100 % of decisions, or that a proportional split over a clipped score cannot reach a corner. |
| **2. `land_bias` veto arithmetic (brain.py:913)** | change `>` to `>=` (one character; a saturated-negative gene then decodes "buy iff value >= price" instead of "never"), plus a `LAND_BIAS_STEPS` asymmetry so the negative rail is `-land_price+1`. Byte-identical for any theta not on the rail. | paired LIVE55 + TOPB; drawn legs veto only | `LAND_OWN_DEN` and the veto form are absent from both verdict logs. The archive attacked *forcing* a quadrant (`QUAD3` -4.3k), never the rail the gene is stuck on. |
| **3. `cash_reserve` as a gene (plan.py:3573)** | append `g13` (32->1), `reserve = HIRE_BILLS[n+1] * clip(1 + tanh(z), 0, 2)`; inert at z=0 by construction. Sweep the fixed multiplier 0.5/1.0/1.5 first as the cheap read. | paired LIVE55 + TOPB; drawn legs veto only | never A/B'd at all — it is the largest fixed pre-deduction on the purse and its docstring is an argument, not a measurement. |
| **4. crew ceiling `HIRE_BIAS_MAX`/`CREW_TARGET_PUSH` = 400 (brain.py:673, plan.py:3157)** | raise both to 700 (past fib(15)=610), theta unchanged; then a 3-point sweep 400/550/700. | paired LIVE55 + TOPB; drawn legs veto only | the archive measured *how* hands are priced, never the constant that caps the bid at hand 14, while the loss ledger is 12 hands vs our 6 at d10. |
| **5. `compact` ceiling (brain.py:650/1064)** | the gene is on the rail on 100 % of days for the three newest thetas. A/B the decode `DIST_MAX` vs `2*DIST_MAX` with theta unchanged; if level, the rail is right and the 33 params are reclaimable. | paired LIVE55 + TOPB; drawn legs veto only | saturation was never measured; no doc in the archive names `compact`. |

## D. Honest caveats

The archive's own conclusion — residual ceiling = **ES selection resolution** (snr 0.17-0.19 vs
pure-noise 0.23; +/-1-board gate vs 5,997 live coords, 2026-09-09-verdicts.txt:1038) — is not
contradicted here. All five walls are *decode* walls: they cost the search directions, not gradient
scale, so fixing them will not raise snr. But W1 and W4 together gate the single largest ledgered
loss (-14.1k, 69/88 decisive), and unlike `MELON_OPEN` the fix is a clip constant plus a zero-init
gene rather than a hard-coded opening - the cheapest untried shot at that wall.

One hypothesis of this audit was falsified in the writing and is recorded so it is not re-tried:
the `absorb`/`DRAIN_CLIP` gate does **not** block melon. `out.sat` is positive in every lineage
theta (mean 0.09-0.56) and melon passes `absorb` on 65-100 % of days. The block is the proportional
mix, one layer up.

Every dead-lever verdict quoted above is second-hand from docs, not re-run here; the saturation
numbers are mine, from 2,400 decode-only decisions (no engine games), so they describe what the
policy *asks for*, not what the day executes.
