# Planner wall audit — where ES pushes and cannot pass

2026-09-10. Read-only audit of `.claude/worktrees/arms-next/src/kagg3/core/{plan,brain,sell}.py`.
Method: `brain.decide`'s Macro logged every day of one real engine game (seed 7 vs `starter`,
`scripts/plan_stats.py` hook) for the seven lineage thetas, plus a gene-slope check —
96 antithetic perturbations at the training sigma 0.02, masked by `policy.live_mask()`,
re-decoded on the 30 captured `PolicyObs`. Seed 20260828 reproduces every finding below.

## 1. Gene saturation

Decode: `brain.decide` (brain.py:860-1157). Bounds: `LAND_BIAS_STEPS=256` (brain.py:640),
`GROW_MAX=4.0`→`grow_mult/dev_weight ≤ 1024` (:646), `DIST_MAX=8` (plan.py:3341),
`HIRE_BIAS_MAX=400` (:673), `CREW_TARGET_MAX=MAX_HANDS=16` (:699), `DEFER_ONE=256`,
`FWD_DAYS_MAX=6` (:721), `press ≤ base`, `hold ≤ COIN_CAP-1`.

Season mean (max) per theta, seed 7:

| gene | f135_g350 | f166_g170 | f172_g60 | f172_g170c | f172_g300 | f172_g940 | f172_g1000 | bound | slope@σ0.02 |
|---|---|---|---|---|---|---|---|---|---|
| land_bias | −3065 | −3061 | −3061 | −3062 | −3064 | −3060 | −3059 | **= −land_price exactly, d1-4/6-9/11-29** | **6.9 %** |
| compact | 6.3 (7) | 6.5 (7) | 6.4 (7) | 6.7 (7) | 6.8 (7) | 6.9 (7) | 6.9 (7) | 8 | **7.2 %** |
| dev_weight | 43 (58) | 46 (80) | 43 (79) | 48 (98) | 46 (110) | 39 (145) | 38 | 1024 (x1 = 256) | 87 % |
| hire_bias | −114 | −135 | −102 | −121 | −134 | **−259** | −254 | ±400 | 98 % |
| crew_target | 8.2 (13) | 7.9 | 8.1 | 6.9 | 5.9 | 6.7 | 6.7 | 16 | 50 % |
| animal_defer | 0 | 0 | 0 | 29.5 (88) | 22.5 | 0 | 0 | 256 | 8.9 % |
| forward_days | 0 | 1.2 (4) | 1.0 | 1.1 | 0.5 | 0.9 (6) | 0.9 | 6 | 20 % |
| grow_mult[WOOL] | 614 (962) | 718 (**1024**) | 652 | 695 (**1024**) | 679 | 611 | 611 | 1024 | 93 % |
| press[WOOL] | 9 | **0 all 30 d** | **0** | **0** | 1 | **0** | 0 | 0..200 | 6.3 % |

### The walls

1. **`land_bias` is pinned at its negative saturation on 27 of 30 days, in every theta of the
   lineage, and has zero ES gradient there.** `land_frac = qfloor(tanh(head[1]+aux[1]·afford)·256)`
   decodes to exactly −256, so `land_bias = −land_price` and the gate
   `land_value + macro.land_bias > 0` (plan.py:5360) demands a quadrant worth **more than its own
   price**. Per-day move rate at σ0.02: d0 0.75, d5 0.15, d10 0.92, **0.00 on every other day**.
   Quadrant 2 is bought d5 and quadrant 3 d10 in *all seven* thetas and both seeds — 900
   generations of ES moved land not one day. Quadrant 4 is never bought and cannot be:
   the gene has no slope after d10.
   Counterfactual (flow172_g940, seed 7, one board, `starter`): `land_bias:=0` → quad 2 on **d0**,
   own coins 121,111 → **159,113**; `land_bias:=+price` → 4 quadrants, 134,485. Single-board and
   unpaired — this is a direction, not a coin count (two-purse rule).
2. **`compact` is at 7 of `DIST_MAX=8` and has slope only on days 8-17** (move rate 0.00 on d0-7
   and d18-29). Monotone up across the lineage 6.33 → 6.93. Near-wall, small stake.
3. **Floors that are inert by design, not walls**: `press` (relu·tanh, 17-30 days at 0 for most
   products), `animal_defer` (0 in 5/7 thetas), `hold[FERT]` (0 everywhere), `forward_days`
   (0 from d11 in all — matching the archive's "the forward horizon belongs to theta").
4. **Not a wall**: `grow_mult[WOOL]` touches 1024 on 2-5 days only and keeps 93 % slope;
   `dev_weight` sits at x0.15 of a 4x ceiling; `crew_target` at 6-13 of 16.
5. **Moving toward a wall**: `hire_bias` is monotone down the lineage (−114 → −259 mean, −337 max
   magnitude = 84 % of `HIRE_BIAS_MAX`). Not yet binding; watch it.

## 2. Hard constants that shape money (not theta-decoded)

Ranked by coins at stake × how unmeasured. Verdicts from `docs/strategy` unless marked.

| constant | file:line | value | money through it | archive verdict |
|---|---|---|---|---|
| `cash_reserve` | plan.py:3573 | `HIRE_BILLS[n_hire+1]`, void from `pay_day` | comes off the purse that prices land → `land_value ≤ 0` | **NEVER measured as a lever.** Named as the land mechanism (2026-09-10-chain-optimisation-review.md:24,43) and called "wrong, the bill is 1 coin" (2026-09-03-dominant-strategy.txt:301). No arm ever run |
| `LIQUIDATE` / tail lot sizing | sell.py:48 | `-COIN_CAP` | d21-29 SELL rows ≈19 units/game short | **NEVER built** (plateau §2:111, intraday review:71) |
| `EST_HOME` / `EST_LEAD` / `EST_MOVES` / `ADMIT_ROUNDS` / `ADMIT_PICK_SHARED` | plan.py:3019/171/149/210/257 | 3 / 5 / 1 / 3 / False | admit-vs-route turn budget | **CLOSED.** Sim +427 t 8.1; engine 1,904 boards **+188, t 1.0 — level, not promoted** |
| `SELL_TURNS`, `N_LOTS`, `EARLY_SELL_MODE` | ops.py:126, sell.py:44, plan.py:2466 | (3,10,18), 3, "A" | the whole sale | **CLOSED**, zero headroom: (3,10,21) −165, 4th row −77, on6 −324 / on4 −348 with 0 flips. Mode A itself +2,184 t 5.1 |
| feed & fert reservations | plan.py:6581-6590 | `want_feed` wheat, `n_fert_eff` fert, void on d29 | 179 fert applications = +16.8k/game | reservation **pays**; `FEED_RESERVE_DAYS=2` −2,666; `FERT_FLOOR` −3,551 t −16.8 |
| `LAND_OWN_DEN` / `LAND_REV_NUM,DEN` | plan.py:190/179 | 2 / 3,4 | land funding | level in knobsweep2; "do not bind on d0" |
| `CREW_TARGET_PUSH` | plan.py:3157 | 400 | hire enumeration | **never in docs/strategy** |
| `MAX_HANDS` | spec.py:243 | 16 | crew cap | not binding (h* 10.6-11.7); forcing crew always loses (RAMP11 −4.3k t −3.0) |
| `OPEN_PUMP_UNITS/KEEP/MIN_MONEY` | plan.py:1184/1189/1194 | 53 / 5 / 1584 | +21.7k splice vs family B | switch measured, **sizing never swept** |
| `DRAIN_CLIP`, `PLANT_FILL_RESERVE_DAYS`, `LAND_PICKUPS`, `DEV_DAYS`, `CHAIN_MAX`, `SURVIVAL_WATER_MIN` | brain.py:224; plan.py:4310/204/195/139/3010 | 4.0 / 3 / 3 / 2 / 6 / 0 | second-order | **never measured** |

## 3. Shortlist — at most five, ranked

1. **Unsaturate the land veto.** `LAND_FLOOR_ON`: clip `land_frac` at `-(LAND_BIAS_STEPS-1)`
   in brain.py:896, so a saturated gene demands `land_value > price·255/256` instead of
   `> price`, and the tanh tail keeps a slope. Byte-identical whenever the gene is unsaturated.
   Arms: OFF (champion) / FLOOR255 / BIAS0 (`land_bias:=0`, the diagnostic bound).
   Judge: paired LIVE55 + TOPB, drawn legs veto only. Not closed by the archive: QUAD3 measured
   land *timing* forced on top of the saturated gene and lost; nothing has measured the gate.
2. **`cash_reserve`.** Arms: shipped `HIRE_BILLS[n_hire+1]` / `HIRE_BILLS[1]` (one-hand floor) /
   0 from day 11. Same judge. Explicitly implicated in the land mechanism and never run.
3. **Day-21-29 liquidation sizing.** Instrument the ≈19 units/game the SELL rows leave behind,
   then one arm: raise `rounds` on the tail-day `allocate` continuation. Same judge.
   Never built; it is the only refusal signature the instrumented engine run found.
4. **`compact`'s ceiling window.** Cheap slope fix: `DIST_MAX` is the bucket count, and the gene
   is at 7/8 with no slope outside d8-17. One arm at `DIST_MAX+2` bands. Low stake — the
   admit/route stage read level in the engine, so treat this as a slope repair, not a lever.
5. **`HIRE_BIAS_MAX = 400`.** No arm yet: log the decode every 100 generations and widen to 800
   only if a theta reaches 95 % of the bound. Widening now changes the champion's decode for
   no measured reason.

**Blunt part.** Six of the twelve genes are healthy (>50 % slope at σ0.02). One is a genuine,
lineage-wide, zero-gradient wall (`land_bias`), one is a near-wall with a narrow live window
(`compact`), and the rest are inert-by-design floors that the decode was built to make inert.
Every hard constant with real coins behind it that the archive *has* measured came back level
or negative. The single largest unmeasured money rule is `cash_reserve`, and it is the same
rule the land wall runs through.
