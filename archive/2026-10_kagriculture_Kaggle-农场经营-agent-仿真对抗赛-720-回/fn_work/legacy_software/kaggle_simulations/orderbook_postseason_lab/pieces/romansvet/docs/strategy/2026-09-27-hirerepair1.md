# HIREREPAIR1 (2026-09-27 20:04Z-21:50Z): the runtime.py:295 hire-repair gate is unreachable in every shipped package

**Verdict: NO MOVE.** The gate overvalues exactly as BUILDREVIEW1-B says: unfertilised wheat by 50 %, carrot by 33 %, and late ongoing plantings through the horizon. But it lives in `ProgramEngineState.repair_hire`. That object is built only when `PROGRAM_ENGINE_ON` is set, and the flag is `False` in master 942b46cb, in the vrp12_pfs and vrp10_esw tarballs, and in every judge harness switch set. Under the shipped PFS config the three traced BAND seats constructed 0 `ProgramEngineState`s and made 0 `repair_hire` calls. The corrected valuation (`HIRE_REPAIR_TRUEYIELD_ON`, default False) is byte-identical to `res/pfv1.csv` with the switch OFF (3/3 seats) and with it ON (3/3 seats + MELON 51/51 and 101/142 BAND seats). It is not a ship candidate, because nothing ships through this code. The fix is kept on branch `hirerepair1` (this commit), not merged, for any future ENGINE-port body.

## 1. What the gate values (`src/kagg3/agent/runtime.py:258-296`, `ProgramEngineState.repair_hire`)
- **When it runs.** From hour 4 onwards the gate releases one more `HIRE` if all of these hold:
  - the day's programme intent still wants hands (`hired < hands_target`);
  - the next crew row is idle for the rest of the day, and no purchase is planned for the rest of the day;
  - the owed plantings exceed the idle rows;
  - an empty tile is reachable;
  - some owed crop `c` satisfies `day + FIRST_YIELD_DAY[c] <= pay_day` (29 under `HORIZON_DROP_ON`), `cash - reserve >= HIRE_COST[hired] + seed[c]`, and
    **`price[c] * CROP_MAX_YIELD[c] > HIRE_COST[hired] + seed[c]`** (line 295).
- **Engine truth** (`kaggriculture.py`):
  - `_new_plant` seeds a one-time crop with 1 unit.
  - `WATER` adds +1 per in-window day, or +2 while fertilised (`py:440-443`), capped at `max_yield`.
  - An ongoing crop fires `max_yield` times at +1, or +2 when watered and fertilised (`py:799-800`).
  - The unfertilised, watered-every-day, horizon-clipped count is `core.valuation.new_plant_units(crop, day)`. The planner already uses it elsewhere. The fix is to use it here.

`S/hirerepair1/res/valuation_table.tsv` (pay_day 29):

| crop | seed | gate units | true unfert (early) | fert max | over-valuation | gate horizon last day | true units planted d15/17/18/19/20/22/25/26/27 | flip price band, hire #7 (13+seed) | hire #11 (89+seed) |
|---|---|---|---|---|---|---|---|---|---|
| WHEAT | 10 | 6 | 4 | 6 | +50 % | d27 | 4/4/4/4/4/4/4/3/2 | p ∈ (3.8, 5.8] | p ∈ (16.5, 24.8] |
| CARROT | 20 | 4 | 3 | 4 | +33 % | d27 | 3/3/3/3/3/3/3/3/2 | p ∈ (8.2, 11.0] | p ∈ (27.2, 36.3] |
| TOMATO | 50 | 4 | 4 | 8 | 0 early; 4 vs 3/2/1 on d19-21 | d21 | 4/4/4/3/2/0/0/0/0 | – | – |
| STRAWBERRY | 100 | 4 | 4 | 8 | 0 early; 4 vs 3/2/1/1 on d15-19 | d19 | 3/2/1/1/0/0/0/0/0 | – | – |
| MELON | 80 | 6 | 6 | 6 | 0 | d19 | 6/6/6/6/0/… | – | – |

- **Where it could flip a decision.** Hire costs are Fibonacci: 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144. With the programme's crews (7-11 hands), cost + seed is usually far below price × units under either valuation. A flip needs one of two things:
  - a wheat or carrot price inside the band above, with no other owed crop passing; or
  - a late planting where the horizon clip bites: wheat or carrot on d26-27, tomato on d19-21, strawberry on d15-19.
- **Fertiliser.** The fix uses the unfertilised count, which is a lower bound. A fertilised wheat tile does reach 6. So the old value is right only for tiles the plan fertilises.

## 2. Trace: 3 BAND seats, the first 3 MELON seats of BAND142 (`trace.py`, `res/trace_table.tsv`, `res/trace_calls.tsv`)
Every `repair_hire` call is evaluated twice, with the switch OFF and ON (the method is pure), and both outcomes are logged. The game follows the run's own setting.

| config | ProgramEngineState built | repair_hire calls | HIREs issued, old / new valuation | flips | result vs pfv1 |
|---|---|---|---|---|---|
| shipped PFS, switch OFF | 0 | 0 | 0 / 0 | 0 | 3/3 identical (ours, theirs, mech cols) |
| shipped PFS, switch ON | 0 | 0 | 0 / 0 | 0 | 3/3 identical |
| PFS + `PROGRAM_ENGINE_ON` (ENGINE port, the only body where the gate is live) | 1 per game | 719 per game | 82 / 81 | **1** (readyornothere d27 h5, hired 10, wheat 36 / carrot 33: old 6×36 = 216 > 99, true 2×36 = 72) | – |

Even where the gate is live, it flips 1 of 82 hire releases, a d27 horizon case. The price-band case never occurred.

Side read, not a lead: PFS + `PROGRAM_ENGINE_ON` on these 3 MELON seats is +1 flip with Δtheirs −32k, but one rival collapsed (86k → 12k). That is n = 3. BANDFAMILY1's ENGINE port was 10/91 on BAND142.

## 3. Paired judge (`pair.py`, GATE2 A/B per `S/gate2/rescore.py`)
ON (`PLACEFEED_ON,PF_PUMPSAFE_ON,HIRE_REPAIR_TRUEYIELD_ON`) vs PFS base `S/bandleg1/res/pfv1.csv`, 1 worker, about 45 s per game.

| leg | seats | identical rows (all 7 cols) | flips MELON / V / ZERO / OTHER | Δours | Δtheirs (t) | GATE2 (A) BAND soft family Δθ (z) | GATE2 (B) soft-win t | GATE2 |
|---|---|---|---|---|---|---|---|---|
| BAND142 MELON | 51/51 | 51 | 0/0 · – · – · – | 0 | 0 (0.00) | +0.0 (SE 0, z 0) | 0.00 | FAIL (no effect) |
| BAND142 V/ZERO/OTHER | 50/91 (V 44, ZERO 4, OTHER 2; stopped at the time box, 21:44Z) | 50 | – · 0/0 · 0/0 · 0/0 | 0 | 0 (0.00) | – | – | – |
| **pooled** | 101/142 | **101** | **+0/−0** | **0** | **0 (0.00)** | **+0.0 (z 0)** | **0.00** | **FAIL = no move** |

- MELON is not a gift: it is byte-identical. The full-142 read was stopped after 101 seats. The other 41 seats are identical by construction: 0 `ProgramEngineState` objects exist.
- BAND-HOLD 104 and NEW30 were not run. They require a GATE2 pass on 142, and the arm cannot move any seat under the shipped config.

## 4. Second flagged item: the weed-spawn RNG couples the shop draw to both farms' empty tiles (no games)
- **Engine fact.** `_end_of_day` seeds `random.Random((seed*1_000_003) ^ day)`. `_spawn_weeds` draws one `rng.random()` for every empty unlocked tile, farm 0 first and then farm 1. Every third day `rng.choice(sorted(SHOPS))` follows on the same stream (`py:836-839, 865-891`). The day's shop and farm 1's weed tiles therefore depend on E0 + E1, the total count of empty tiles at the end of the day.
- **Not exploitable.** `resolve_episode_seed` scrubs the seed from the configuration: "agents must not be able to read it" (kaggle_environments/utils.py:205-214). Without the 31-bit seed, choosing E_own steers the draw only to a different unknown shop, which is a lottery ticket, not a lever. Recovering the seed from observed weeds and shops gives too few bits: about 3 per shop draw plus rare weeds at p 0.005, against 2^31 Mersenne seedings under a 1 s actTimeout. It is also against the stated intent of hidden state.
- **What it does mean: judge noise.** Any arm that changes our end-of-day empty-tile count re-rolls the town shop sequence (±25k/game, L1) and the rival's weed tiles. Paired Δtheirs on small legs therefore carries a non-causal lottery term. The cure is more seats (BANDBANK2), not a rule.

## Commands
```
# worktree src (branch hirerepair1); all runs 1 worker, from S/bandleg1
bash S/hirerepair1/run.sh trace   # 9 games: OFF / ON / ENGINE-port traces on 3 MELON seats -> res/trace_{off,on,eng}.csv, res/trace_calls.tsv
bash S/hirerepair1/run.sh melon   # 51 MELON seats of BAND142, ON -> res/hrty_melon.csv
.venv/bin/python S/hirerepair1/pair.py S/hirerepair1/res/hrty_melon.csv   # vs S/bandleg1/res/pfv1.csv
```

## Files
- `S/hirerepair1/`: run.sh, trace.py, pair.py.
- `S/hirerepair1/res/`: valuation_table.tsv, trace_table.tsv, trace_calls.tsv, trace_*.csv, hrty_melon.csv/.log, pair_melon.txt.
- Code, on branch `hirerepair1`:
  - `plan.HIRE_REPAIR_TRUEYIELD_ON` (default False);
  - runtime.py:295 now prices a job at `P.VAL.new_plant_units(np, c, day)` when the switch is on;
  - the spec.py:58-66 comment is corrected (comment only).
- **Residual, not changed.** `agent/overflow.py:_job_cost` also prices a PLANT at `CROP_MAX_YIELD`. There it is a relative displacement cost inside the shipped overflow guard, not an absolute gate. It was not flagged by the review, so it was left alone.
