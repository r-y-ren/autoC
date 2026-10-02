# Labour compounding — mechanics, measurement, history, candidates (2026-09-11)

Research only; nothing built, nothing run in the engine. Trees read: working tree
`src/kagg3/` (planner line numbers marked WT) and the shipped tree
`.claude/worktrees/ship-pair-hr/src/kagg3/` (marked HR; this is what sub 56143250 and the
candidate B package carry). Replays: SpaTaro x2 (`S/flow198/eps/ep_107738945.json`,
`ep_107738965.json`), Majkel1337 x3 (`S/spataro/ep_107751894.json`, `ep_107722216.json`,
`ep_107683794.json`), ours x4 (`S/ep_107744147.json`, `ep_107743508.json`, `ep_107723697.json`,
`ep_107738911.json`). Scripts: `S/spataro/tools/ledger.py` (reused, read-only) plus
`scratchpad/labour/hours.py` (per-day hand-hour census, written here; per-game json/txt beside it).
Reconstruction error (profiler `_simulate_market`, coins per seat per game): ours 0-350,
SpaTaro 128/500, Majkel 30-260 — all below one day's revenue, so the day-level rows hold.

**One-paragraph answer.** In this engine labour does not compound: hands are dismissed every
night (`sim/eod.py:237` `nhands = 0`, `hires_today = 0`), carry no skill or upkeep, and cost a
per-day Fibonacci bill so small (6 hands = 20 coins, 10 = 143, 12 = 376) that it never binds.
What compounds is *capital* — standing tiles, fed animals, and the day-10 melon pot — and
labour is the near-free complement that works it. SpaTaro's six day-0 hands are 41-47 % PASS
for six days; Majkel1337, who beats SpaTaro 6-0, fields four. Our own hands are already the
busiest of the three files on days 0-5 (10.3 productive turns per hand-day vs 5.1). The
measured slack on our side is idle *cash*, 0.6-5.7k overnight on days 2-9 (both top files run
at 0-200), not idle hands. Every hand-count lever in the archive lost, and the two that were
level (`HIRE_ROW_ON`, `SHEEP_FLOOR=8`) were level. The candidates below are therefore about
converting the overnight purse into capital inside today's legal task list, with one cheap
labour-side residual; none is a hand-count target.

## 1. Mechanics (engine facts, from the bit-exact JAX port; the Kaggle package itself is not installed — `vendor/engine.lock.json` pins `kaggle_environments 1.32.7`, `kaggriculture.py` sha256 bc8a5487…; the port is the harness-verified transcription)

| fact | value | source |
|---|---|---|
| hire cost | the (n+1)-th hire **of the day** costs `fib(n)` with fib(0)=fib(1)=1: 1,1,2,3,5,8,13,21,34,55,89,144,… ; 4 hands = 7, 6 = 20, 8 = 54, 10 = 143, 12 = 376, 14 = 986, 16 = 2,583 | `spec.py:234-258` (`HIRE_COST`), `sim/market.py:106-134` (`_hire` reads `hires_today`) |
| why the replays show 7 then 13 | SpaTaro's `[HIRE]x4` at h0 = 1+1+2+3 = 7; `[HIRE]x2` at h1 continues the day's count: fib(4)+fib(5) = 5+8 = 13. Splitting rows costs nothing extra | same |
| wage / upkeep | none; the bill is the only cost | `spec.py:234` "the engine caps nothing" |
| tenure | hands vanish at end of day; every morning starts at 0 hands and `hires_today = 0`; units respawn on the shed tile | `sim/eod.py:236-239` |
| cap | none in the engine; 10 market orders per turn (`MAX_MARKET_ORDERS = 10`, `spec.py:216`), planner cap `MAX_HANDS = 16` | `spec.py:243` |
| what a unit does | exactly one op per turn: move 1 tile (N/S/E/W), PLANT, WATER, HARVEST, FERTILIZE, FEED, CARE, COLLECT_FERTILIZER, DIG, BUILD_COOP/PASTURE, PLACE, PICKUP/DROP at a shed-adjacent tile, or PASS. Farmer is one more unit | `sim/units.py:31-180` |
| selling | SELL/BUY/HIRE are *market* orders on the farmer's row, not unit actions — zero labour | replay `action['market']` vs `action['hands']`; `sim/rollout.py:267` |
| watering | +1 yield per in-window day watered, **+2 if the tile is fertilized** (`t_fert >= day`), capped at `CROP_MAX_YIELD`; a tile unwatered two days running dies (`cons >= 2`) | `sim/units.py:157-159`, `sim/eod.py:85-95` |
| task emission (plants) | window = `[ (max_yield_day+1)//2 , max_yield_day ]` in age-days: WHEAT ages 2-4 (harvest ≥2), CARROT 2-3, **MELON 6-12 (harvest ≥10, saturates at 10)**, STRAWBERRY/TOMATO are ongoing crops (no water bonus, yield on an interval) → a melon tile emits no bonus-water or harvest task for its first 6 days | `spec.py:42-76`, `CROP_WINDOW_START` |
| task emission (animals) | FEED (1 wheat) + CARE daily, COLLECT_FERTILIZER when available; production fires every `interval` days from `first_yield` (COW 400c, milk from d+5 every 2; SHEEP 500c, wool from d+5 every 3; GOOSE 300c, eggs from d+4 daily); unfed two days → escapes | `spec.py:80-95`, `sim/eod.py:112-140`, `sim/units.py:168-172` |
| idle-hand cost | the fib bill only; a PASSing hand burns nothing else | — |

So a "hand-day" is worth at most ~21 productive turns (24 minus spawn walk and pickups), and
its price is 1-8 coins for the first eight hands of a day. Labour cannot be the scarce input
below ~12 hands; tasks and cash are.

## 2. Labour → coins, measured (per-game windows; hh = hand-hours, "used" = non-PASS non-move hand ops)

| file | window | hand-days | hh used / avail | PASS % | move % | coins earned | coins / productive hh |
|---|---|---|---|---|---|---|---|
| SpaTaro (2) | d0-5 | 36 / 36 | 195/816, 176/816 | 41-47 | 31-35 | 3.4k, 3.4k | 17.6, 19.5 |
| Majkel (3) | d0-5 | 32 | 292-307/732 | 2-3 | 56-57 | 2.6-2.7k | 8.7-9.1 |
| ours (4) | d0-5 | 23-25 | 241-246/529-575 | 16-25 | 33-36 | 5.7-5.8k | 23.4-24.0 |
| SpaTaro | d6-10 | 44-45 | 414-427/~1,000 | 11-14 | 43-47 | 21.1k, 22.5k (of which d10 melon 10.6-11.4k) | 50.9, 52.6 |
| Majkel | d6-10 | 46-47 | 510-526/1,052-1,074 | <1 | 50 | 18.8-19.4k (melon ~7.5k) | 36.3-36.9 |
| ours | d6-10 | 32-36 | 356-377/736-828 | 10-19 | 40-41 | 10.0-11.2k | 27.6-31.4 |
| SpaTaro | d11-20 | 109-111 | 1,203-1,281/~2,500 | 6-8 | 42-44 | 73.6k, 74.7k | 57.4, 62.1 |
| Majkel | d11-20 | 110 | 1,317-1,421/2,500 | <1 | 42-47 | 54.5-68.5k | 38.4-51.8 |
| ours | d11-20 | 109-117 | 1,231-1,369/2,489-2,657 | 8-9 | 40-42 | 40.7-64.3k | 33.1-48.4 |
| SpaTaro | d21-29 | 88-89 | 940-968/~2,000 | 10 | 42 | 38.5k, 39.5k | 39.8, 42.0 |
| ours | d21-29 | 88-97 | 923-1,048/2,005-2,205 | 10-12 | 41-45 | 46.1-72.4k | 45.3-69.1 |

Per-day detail (ours d1 = 1 hand, 9 used ops: FEED 2 CARE 2 COLLECT 2 WATER 2 PICKUP 1;
SpaTaro d1 = 6 hands, 20-21 used ops, 75-76 PASS) is in `scratchpad/labour/*.txt`.

**Implied marginal value of one extra hand-day.**
* d0-5: SpaTaro fields 11-13 more hand-days than we do and earns *less* in the window (3.4k vs
  5.7k); its extra hands PASS 41-47 % of turns. Direct marginal value ≈ **0 coins**; cost ≈ 3-8
  coins each. Their return is deferred and runs through capital (melon in the ground, herd
  fed from hour 0), not through hand-turns. Ours are the busiest hands of the three files.
* d6-10: +12 hand-days over ours; non-melon coins level (SpaTaro 10.5-11.1k vs ours
  10.0-11.2k; Majkel ~11.5k). Marginal hand-day ≈ **0-80 coins** direct. The 10.6-11.4k melon dump
  is capital planted on d0, not labour of d6-10.
* d11-20: identical hand-days (109-117 all three) and identical productive hand-hours
  (1.2-1.4k), yet SpaTaro earns 57-62 coins per productive hand-hour against our 33-48 and
  Majkel's 38-52. The gap (+10-30k) is **what the hour works**: 56-62 standing tiles vs our
  46.5 at d10, 16-22 fed animals vs our ~10-15, fertilized wheat at 4.4 units/tile vs our
  2.5-2.9 (SpaTaro waters 977-1,096 tile-days, Majkel 1,226-1,312, ours 771-880; we FERTILIZE
  *more*, 126-179 vs 109-131, so fertilizer self-use is not the gap — tile count is).
* d21-29: we out-earn both (45-69 per productive hh) — the late mix edge the SpaTaro ledger
  already records.

**Cash idle overnight** (end-of-day purse): SpaTaro d0-9 0-167; Majkel 7-2,127 (few hundred
d4-5, 1-2k d8); ours 130-196 (d0-1), 614-691 (d2-3), 1,393-1,484 (d4), 826-880 (d5), 684-712
(d6), 1,433-2,466 (d8), 2,085-5,728 (d9-10). Quad 2 (1,000) is bought d5 and quad 3 (2,000)
d10, so d3-4 and d8-9 are partly saving for land — but `land_gap` is deducted only on the day
`buy_land` fires (HR `plan.py:5365-5387`), and 5.7k on d9 is 3.7k above the quad-3 price. The
purse is idle because the greedy ran out of eligible wants (`budget.grant` has no retention
candidate — F5 verify §1), i.e. `plant_target`/`animal_want` were exhausted, which are theta
outputs.

## 3. Our planner's labour logic (HR line numbers; WT is −27 lines around the hire block)

* **Enumeration** (`plan.py:5971-6152` HR; WT `:5845-6000`): pass A `d0 = _derive(bill 0,
  reserve 0)` (HR `:6000`); projected pass `d_sc = _derive(..., forward=fwd_days)` (HR
  `:6020-6027`, `fwd_days = macro.forward_days` = gene g11, or `FORWARD_ADMIT_DAYS=3` when
  `FORWARD_ADMIT_ON`, HR `:3563/:3570`, default False); per candidate h: `turns_h =
  (h+1)*(per_unit − n_kinds0 − EST_LEAD)` (`EST_LEAD = 5` WT `:171`, `EST_MOVES = 1` `:149`),
  `n_adm = min(count_le(cum_est0, turns_h), n_tasks0)` (HR `:6108`), `gain = cum_take(cum_val0,
  n_adm) − HIRE_BILLS[h] + hire_bias*h + CREW_TARGET_PUSH*min(h, crew_target)` (HR `:6124`,
  `CREW_TARGET_PUSH = 400` `:3183`), `afford = HIRE_BILLS[h] + cash_reserve(h, day) <= money`
  (`:6132`), `h_star = argmax` (`:6135`, ties → fewer hands). Pass B re-derives with the
  winner's bill and **no horizon** (`:6142`).
* **Cash reserve** = `HIRE_BILLS[n_hire + 1]` (HR `plan.py:3531-3562`, `cash_reserve`) — tomorrow's
  crew bill plus one marginal hand: 8-34 coins at 4-8 hands. It is not what idles the purse.
* **Admission** (HR `:6369-6472`): `labour = n_units*(turn_budget − max(pickup_kinds, land_lead)
  − EST_LEAD)`, `n_admit = min(count_le(cum_est, labour), n_tasks)`; `EST_HOME = 3` (`:3045`),
  `ADMIT_ROUNDS = 3` (WT `:210`), `ADMIT_PICK_SHARED = False` (WT `:257`, sim +3.1 pts / engine
  level 2026-09-07). Route `_routes` (HR `:6516`, def `:6939`).
* **`HIRE_ROW_ON = True`** (HR `:3523`; WT `:3496` False): clamps the market HIRE row to the smallest
  prefix of hands whose route is not all-PASS — idle hand-days 17.06 → 0.00; engine −378 ±506
  (n=768) alone, shipped on h2h evidence (+453 t 3.6 LIVE62, +990 t 5.0 LIVE-C22, +664 t 3.9
  LIVE-D).
* **Why hands stall at 4-5 on d1-7.** `n_adm <= n_tasks0`: the crew is capped by the task count,
  never by cash. d0 board = 14 wheat/strawberry tiles + 4 cows + 1 sheep + 1 goose. d1: wheat
  is age 1, window opens at 2 → tasks = 6 animals × (FEED, CARE, some COLLECT) ≈ 9 → 1 hand
  (exactly what the replay shows). d2: 11 in-window waters + herd → 3-4 hands. d3-7: 19-23
  waters + 6-7 animals × 3 + 4-13 plantings ≈ 45-60 ops ≈ 5 hands at ~11 turns each. The
  crew tracks the plate; the plate (`plant_target = dev_frac*n_free` split by the mix head,
  `brain.py:621-726`) is what stalls, and it is a theta output.
* **Exact hook for a projected-task admission**: HR `plan.py:6020-6031` already is it (`d_sc`
  feeds `n_tasks0/order0/cum_est0/cum_val0`); the route side would hook at `:6490-6516`
  (`admitted = d.task & (rank_v < n_admit)` → `_routes`) and needs *ops legal today*, because
  the engine refuses a projected HARVEST/WATER (`sim/units.py:163/157`, `in_window` false).
* **FORWARD_ADMIT status**: built three times, dead three times. (i) `FORWARD_ADMIT_ON` (3792b8e,
  2026-09-08): band6 94.4 → 65.3 %, −9,224 t −6.7, d-ours −13,157; +MELON_OPEN 15.3 %;
  DAYS=6 13.9 %. (ii) Switch sweep 2026-09-09: HELD42 −8,676 t −12.1 (+0/−10), LEG20 −6,361,
  LOSS12 −8,178. (iii) Narrow rebuild (quiet tiles only, value /(1+k), hire argmax only;
  `2026-09-10-forward-admit.md`, ba21fd4 unmerged): HELD42 −2,628 t −8.0, LEG20 −1,456,
  LOSS12 −6,403, flips +0/−8. The horizon then became gene g11 (d23bc95; `forward_days =
  clip(round(6·σ(z−4)),0,6)`, `brain.py:1140`, `FWD_DAYS_MAX = 6` `:721`); the trained theta
  decodes mean 0.9-2.1 days (F4 verify §3), and forcing it to 0 costs −13.0/−13.7k own cash on
  two boards — an interior optimum the ES already holds.

## 4. What was tried and why it failed

| lever (date, doc) | paired result | failure mode |
|---|---|---|
| hire_bias saturated (2026-08-28, `brain.py:391-412`) | 13+ hands from d5: hire 12,425 coins, finish 7,159 vs 75,042 | cash starvation (fib bill + reserve) |
| Crew ramp 12-by-d9 (2026-09-05, verdicts:176) | band6 44.8 → 28.6 %, −8,879 t −9.5; ours −887 / theirs +7,992 | denial handed back |
| RAMP11 clone hand curve (2026-09-06 c5e7f40, verdicts:384-385) | band6 55.0 → 52.5; top10 69.4 → 55.6 %, −4.3k t −3.0 | task-emission gap: PASS 15 → 37 %, revenue 112.8k → 67.3k; bills price land off the purse |
| CREW_FROM_TASKS (2026-09-07, how-we-built §2a) | per-hand 5: 51.6 → 39.8 % t −28; per-hand 4: 16.3 % | extra hands PASS (task cap) |
| JOINT_PLATE (2026-09-07 3839aed) | band6 54.2 → 1.0 %, −41.9k t −27; half scale 13.0 % | sizing written above `_derive`: 7 hands d6 at 58 % PASS, quadrant unstaffed |
| MELON_OPEN (2026-09-05/09) | 54.2 → 15.1 %, −17,554 t −12.8; pinned judge 1.9 % | displacement of the animal/wheat line; hands 0-1 on d1-5 (melon emits no task for 6 days) |
| Forced top opening (MELON_OPEN + ramp + PLANT_FILL, 2026-09-08, verdicts:915) | 94.4 → 26.4 / 23.6 / 22.2 % | task-emission gap (d1 hires 0 vs their 4 with 222 coins in hand) |
| FORWARD_ADMIT ×3 (2026-09-08/09/10, §3 above) | −9,224 t −6.7; −8,676 t −12; −2,628 t −8 | extra hands PASS until the window opens; bigger bill; melon variant hands denial back (+6,806 theirs) |
| QUAD3 early land (2026-09-06) | d8 47.9 % t −4.0; d6 44.3 %; d10 inert | cash starvation of the plate |
| ANIMAL_DEFER_ON (2026-09-09 sweep) | −36,544 t −27.7, 18/18 dropped | half-priced early animals displace seeds |
| SHEEP_FLOOR=8 (2026-09-10 consensus §7) | LIVE-C72 63.2 → 61.1 %, −381 t −1.1 (binds d0-11 only) | level; early herd ramp buys nothing |
| HIRE_ROW_ON (2026-09-09/10) | −378 ±506 alone (n=768); shipped on h2h +453/+990/+664 | idle hands were nearly free |
| PRESTOCK_ON / MARKET_PACK_ON | not runnable with `EARLY_SELL_ON` (assert plan:2478) | — |
| N_SELL_ROWS 6 (2026-09-10 consensus §12, 17:35Z) | LIVE-C72 68.1 → 63.9 %, −447 t −5.9; 4 rows identical to the coin | shared-pot price; LOT_SLICE inert by construction (`sell_walk` cumsum) |

Common thread: every lever that added hands added PASSes (the crew is capped by tasks), and
every lever that added early capital displaced the day-0 basket the ES chose. Nothing in the
archive has tested *spending the overnight purse on top-up plantings inside today's task list*.

## 5. Candidate mechanisms

Judge for every candidate: `S/livec/run_holdout.sh <name> <wt> <theta> "<switches>"` (ids
43-72) + `S/livec/run_holdout2.sh` (73-102) + `S/topb2/run.sh` (veto), theta
`flow193_g100` (candidate B) or `flow172_g1000`, switch string = shipped
`OPEN_PUMP_ON=True,TAIL_FILL_ON=True,BANK_BEFORE_LOT_ON=True,HIRE_ROW_ON=True` + the new flag;
identity leg (flag OFF) must be byte-exact; pass = ≥ +3 win points on hold-out 43-102 with
paired d-margin > 0 and no TOPB2 drop > 2 points; kill = d-theirs > 0 (denial handed back) or
d-ours < 0 with win rate down (displacement).

**(1) IDLE_PURSE_TOPUP_ON (planner code; days 0-9).** After `budget.grant` (HR `plan.py:5409`),
if `purse_left > cash_reserve + LAND_HOLD` and free tiles remain, grant extra wheat (10c) /
strawberry (100c) plantings — the cheapest positive-value seeds already in `values` — until the
purse is spent or `n_free` is; hands are then enumerated on the *enlarged* task list, so the
crew follows. Not a repeat: JOINT_PLATE/CREW_FROM_TASKS wrote sizes above `_derive`; this
spends a measured leftover *after* the greedy, on ops legal today (PLANT), so no hand can
PASS on it. Arithmetic: idle 0.6-1.5k on d2-6 ≈ 15-60 wheat tiles or 6-15 strawberry over the
window; SpaTaro's d11-20 return is 57-62 coins per productive hand-hour on 56-62 standing
tiles vs our 46.5 → +6-10 standing tiles ≈ +3-6k by d20 if the shared pot does not eat it.
Risk: displacement of the d5/d10 land purchases (`land_gap` only fires on the buy day — set
`LAND_HOLD` = next quad price when `land_value > 0`), and wheat glut (shared-pot, wheat
curve). Theta-reachable? Partly — `dev_frac` (head[5]) and the mix head set `plant_target`,
so the ES *could* plant more; that it has not is the reason to test the rule as a switch
first and, if it reads positive, hand it to the ES as a floor gene. Cost ~1 engineer-day.

**(2) HORIZON_CHARGED_ON (planner code, one expression).** Discount `cum_val0`'s projected
rungs by their distance `f` before `plan.py:6124` compares them to `bills[h]`, leaving `d0`'s
rungs undiscounted (F4 verify §5 residual; byte-identical at `fwd_days == 0`). Not a repeat:
FORWARD_ADMIT lengthened the horizon by hand; forcing 0 lost −13k; this keeps the trained
g11 and only stops it buying hands whose work lands days out. Arithmetic: 8.5 of 11 idle
hand-days/game come from the gene — but HIRE_ROW_ON already deletes their bill, so the direct
value is ≤ +0.4k; the real question is whether the *route* is better sized when the enumeration
stops over-counting. Expected +0-1k, P(real) ~20 %, cost 0.5 day. Cheap, low ceiling.

**(3) COW_DAILY_ON (planner code; d3-9).** `animal_want` floor of +1 COW/day while
`ub_coins > ANIMAL_COST` (HR `:5308`) and a pasture slot is free, hooked at `_wants`
(`:4762`) — SpaTaro's one-cow-a-day ramp. Not a repeat of ANIMAL_DEFER (which half-priced
candidates and displaced seeds) nor of SHEEP_FLOOR (wool market); it is one 400-coin item a
day out of an idle 600-1,500 purse. Arithmetic per cow bought d3-9: milk every 2 days from
d+5 (~11 units × ~100 falling) + ~0.5 fert/day (~45) − feed ~35/day ≈ +0.6-0.9k net over the
season, ×5-6 cows ≈ +3-5k gross, **minus** our own milk-curve depression (milk `sqrt` 0.60,
already 4-5 cows) — realistic +1-2k. Labour: 3 hand-turns per animal-day = one hand at 5-13
coins. Risk: Majkel beats SpaTaro with *fewer* cows (milk M−S negative 5/6). P(real) 15 %,
cost 0.5 day.

**(4) FORWARD_ADMIT + purse-to-zero (the brief's (a)).** As a hire-side rule it is dead
three times (§3) because pass C never sees the projection and the engine refuses projected
ops; only Phase 2 of `2026-09-10-forward-horizon-feasibility.md` (a pull-forward route tier
of ops legal today) could make it live, at 3-4 engineer-days and a 10-15 % estimate. Do not
re-run the hire-side variant. Theta-reachable: the horizon (g11), hire_bias (g8/g9),
crew_target (g10) and the plant/animal volume (head[5], head[2]) all are — the ES holds them at
an interior optimum (hire_bias −358, forward_days 0.9-2.1, crew_target 11 by d10).

**(5) Hour-0 herd on bought wheat (the brief's (b)).** Already ours in substance: we buy 4
cows + 1 sheep + 1 goose at d0h1 and COLLECT_FERTILIZER from d1 (replay d1 ops). The
difference is (3) above plus SpaTaro's 375-535 bought wheat units (14-22k), which Majkel
shows is a *loss* line (spend gap = the whole M−S margin). Not a candidate beyond (3).

**(6) 24-hour sell spread (the brief's (c)).** A market effect, not labour: SELL is a
farmer-row market order (zero hand-turns); the price comes from restock between rows
(`SHOP_SELL_INTERVAL = 4`, `sell_walk` cumsum per row). Tested: N_SELL_ROWS 6 → −447 t −5.9 on
LIVE-C72, 4 identical; LOT_SLICE inert by construction. Dead in the layouts tried; a 12-24 row
layout is a by-construction wall of `SELL_TURNS = (3,10,18)` (`ops.py:126`) and would be a
market-controller build, out of scope here.

## 6. Recommendation

Rank by expected coins × P(real) ÷ cost: **(1) IDLE_PURSE_TOPUP_ON** (+3-6k × 0.25 ÷ 1 day ≈
1.1k/day) > **(3) COW_DAILY_ON** (+1-2k × 0.15 ÷ 0.5 ≈ 0.45k/day) > **(2) HORIZON_CHARGED_ON**
(+0.5k × 0.2 ÷ 0.5 ≈ 0.2k/day) > (6) sell spread (dead as tested) > (4) FORWARD_ADMIT (dead
×3; only the 3-4 day route rewrite remains, 10-15 %). Labour itself is not the lever: our
hands are already the busiest on days 0-5 and cost 7-12 coins a day; the top files' extra
hands PASS. **Single first test: IDLE_PURSE_TOPUP_ON on days 0-9**, identity leg exact, then
hold-out 43-72 + 73-102 + TOPB2 on candidate B's theta; read d-ours vs d-theirs before the
win rate. If it reads positive, the follow-up is a zero-init plant-floor gene so the ES can
size it (flow184's slope rule applies). If it reads as displacement (d-ours down), the
overnight purse is the ES's chosen reserve against the shared pot and the labour/capital
family closes with the melon, wool and mix families.

Files: `scratchpad/labour/hours.py` (census), `sp_*.json/us_*.json/mj_*.json` per-game rows.
