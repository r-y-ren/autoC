# Verify F2 — "Admitted essential work can remain unexecuted"

Independent check of finding 2 of `docs/2026-09-10-planner-findings.md` (detail:
`docs/reviews/planner-2026-09-10/REVIEW.md` §3). Read-only on every worktree
`src/`; the instrumented planner was a scratch copy. Engine: 70 s.

**Verdict: CONFIRMED as a source property and reproduced exactly; incidence in
trained play is 0 for the claimed failure mode (survival watering) and 0.67
tiles/game for any mandatory op, all on day 29. The "repair feasible omissions"
lever was already measured and dropped on 2026-09-08. Not a lever.**

## 1. Source — how an admitted tier-2 task is dropped from the route

Reviewed `.claude/worktrees/ship-pair/src/kagg3/core/plan.py`; the shipped tree
`ship-pair-hr` differs in **one line** (`HIRE_ROW_ON` `False`→`True`,
`plan.py:3523`; whole-file diff = 1 hunk), so every line below is byte-identical
in both and the finding transfers unchanged.

| stage | line | code |
|---|---|---|
| survival watering priced | `plan.py:4996-5000` | `survives_water = must_water & (crop_remaining_value(...) > SURVIVAL_WATER_MIN)` |
| mandatory tier / tier-2 / floor | `plan.py:5736-5740`, `5749-5750`, `5759` | `tier = mandatory.astype(i32)`; `tier = tier + (is_plant & survives_water & (t_water == 0))`; `tile_value = maximum(tile_value, minimum(tier, 1))` |
| **admission order** | `plan.py:6436-6438` | `order_v = task_order(xp, d.task, d.tile_value, d.tier)`; `rank_v = _inverse(...)`; `cum_est = cumsum((n_ops + EST_MOVES)[order_v])` |
| admitted count | `plan.py:6472` | `n_admit = minimum(_count_le(cum_est, labour), n_tasks)` |
| **route order** | `plan.py:6473`, `6491` | `route_tier = (d.tile_value > 0)`; `order = task_order(xp, admitted, zeros(N_T), route_tier)` |
| block cut | `plan.py:6939-6950` (`_routes`) | `L(e) = base + cum[e] - cum[s] + max(D(s,e), land_lead)`, "ends at the largest `e` with `L(e) <= turn_budget`" |
| repair | `plan.py:6489`, `6521` | `for _ in range(ADMIT_ROUNDS)` (=3, `plan.py:210`); `n_admit = n_admit - sum(admitted & ~covered)` |

Mechanically, the claim is **literally true**, and by construction:

1. Admission ranks by `(tier, tile_value)`, so a tier-2 survival watering is
   rank 0 and admitted at any `n_admit >= 1`. `plan.py:5741-5748` states the
   intent: "the tile the admit stage's tail must never be allowed to reach".
2. Routing then **re-tiers**: `route_tier` is the two-group rank
   `tile_value > 0` (`plan.py:6473`) and the score argument is all zeros, so
   `task_order` (`plan.py:4109-4131`) breaks every tie by *ascending serpentine
   index*. Inside the priced-or-mandatory group the admission tier carries no
   information — a tier-2 tile at serpentine 99 sweeps last.
3. `_routes` cuts each block at the largest reachable `e` (monotone in `e`), so
   the sweep's tail is dropped whatever its tier: no reservation, no exchange,
   no post-route mandatory check.
4. The repair at `plan.py:6521` only ever **lowers `n_admit`**: it removes the
   tail of the *value* order — never the tier-2 tile (rank 0), never the
   spatially earlier tile that blocks it, reaching the omission only by starving
   the route of everything else.

## 2. Probe reproduction (ship-pair tree)

`probe_f2.py`, the `mandatory_missed` case of `probe.py` (four tiles, purse 0 ⇒
one unit, tile 99 = immature TOMATO `t_yield=0, t_cons=1`; strawberries 4/9/91):

```
survival_tile 99: tier=2  tile_value=240  admitted=True  covered=False
covered_tiles=[9]         turns_to_reach_and_water=10   (budget 22)
admit order head = [99, 9, 91, 4, ...]   route order head = [9, 99, ...]
route_tier: {4:1, 9:1, 91:1, 99:1}       n_admit after 3 rounds = 1
ADMIT_ROUNDS 1/2/3 → tile 99 covered False/False/False;  4/5/6 → True
```

Reproduced to the value. The route order *does* place 99 second — the failure is
the block cut, not a sink to the worthless group (the `plan.py:5759` floor
works). Last-round `admitted` = `{9, 99}`, `covered` = `{9}`: the serpentine-9
harvest is done, the survival watering is not, a 10-turn direct route existed.
Round 4+ waters 99 but drops the 480-coin harvest — repair is not free either.

## 3. Incidence in trained play — the number the review did not measure

Instrumented scratch copy of the `ship-pair-hr` planner (records `tier`, `task`,
final `admitted`, `covered`, `tile_value` after the `ADMIT_ROUNDS` loop, plus
per-day `kind/occ/t_cons` for fate tracing), driven exactly as `S/drainpin/on2b.py`
does: theta `artifacts/kagg2_games/thetas/flow172_g1000.npy`, switches
`OPEN_PUMP_ON=True,TAIL_FILL_ON=True,BANK_BEFORE_LOT_ON=True,HIRE_ROW_ON=True`,
`KAGG3_TOWN_SCHEDULE=S/band2100p/town_schedules.json`, `--games 1
--seed-per-opponent --seed-base 777001`, 3 pinned `S/livec` tapes (107429978 /
107430502 / 107433383) × 2 seats = **6 games, 180 day-plans** (70 s; win
0 / 100 / 100 %, margins −7,535 / +1,479 / +237).

| quantity (6 games, 180 day-plans) | total | per game |
|---|---:|---:|
| tier-2 survival-watering ops queued | 2,240 | 373.3 |
| … admitted | 2,240 | 373.3 |
| **… admitted but NOT emitted** | **0** | **0.00** |
| tier≥1 mandatory ops queued | 5,060 | 843.3 |
| … admitted | 5,058 | 843.0 |
| **… admitted but NOT emitted** | **4** | **0.67** |
| mandatory FEED admitted but not emitted | 0 | 0.00 |
| any tile admitted but not emitted | 6 | 1.00 |

**What happened to the omitted units.** Nothing died. All four mandatory
omissions are on **day 29** (tiles 84/82, still `KIND_PLANT`, `t_cons` 0–1): the
game ends before a second unwatered night can weed the tile. The other two
(day 26) are tier-0 work worth 48 coins. Two day-29 plans also de-admitted one
tier-1 tile via the `plan.py:6521` shrink; zero tier-2 tiles, ever.

**Coins at stake — DESCRIPTIVE, planner-value, not measured profit: 98.7
coins/game** of `tile_value` on admitted-but-unemitted *mandatory* tiles (0 of
it tier-2), **114.7 coins/game** over every tile — 0.13 % of ~87k mean final
coins, and falling on day 29 behind the DROP leg, so most cannot reach cash.

## 4. Archive check — the lever is already closed

- **`2026-09-09-verdicts.txt:897` (2026-09-08T18:40Z) is this exact lever, and
  it was dropped**: *"route repair by insertion/exchange instead of admission
  shrink … NOT a blocker — 96 games/2,880 days: shrink on 21 % of days drops 24
  tiles worth 640 planner-value but routing the un-shrunk set is −2,224/game
  (the shrink EARNS); insertion+exchange oracle recovers +429/game = 0.08 % of
  routed value (bar 1,500); 52 % of undone value is day 29 behind the DROP
  leg. Not built. DROP."* My day-29 result reproduces that on a fresh theta.
- `2026-09-10-planner-wall-audit.md:61` — the whole admit/route turn budget
  (`EST_HOME/EST_LEAD/EST_MOVES/ADMIT_ROUNDS/ADMIT_PICK_SHARED`) is **CLOSED**:
  sim +427 t 8.1, engine 1,904 boards **+188, t 1.0 — level**; and
  `2026-09-09-verdicts.txt:511` reads `ADMIT_ROUNDS` 3/4/5 level, so even the
  probe's "use 4 rounds" answer is a measured null.
- Care/feed coverage: `2026-09-09-plateau-review-verdicts.md` §12 feed supply
  (`FEED_RESERVE_ON` −2,666 us / +812 them, OFF), §14 care-with-feed (+2/−0,
  H_dm −24, LEG20 −258, OFF), §15 care-fill/care-hold (H_dm +54 / LEG20 +46
  inert, −332 with hold, OFF), `2026-09-09-care-coverage.md` (a 20–30 pt
  coverage gap yields **level** production/animal-day). None ever paid.
- `2026-09-10-planner-wall-audit.md:68` lists `SURVIVAL_WATER_MIN` (=0) "never
  measured" — the only untouched knob here, and it changes *which* waterings are
  mandatory, not whether they get routed.

## 5. Verdict, dead ends, and the test a fix would have to pass

**CONFIRMED (source + probe) / REFUTED as a lever.** The admission tier is not an
execution guarantee — a real, reproducible interface defect, stated correctly and
honestly by the review ("Frequency in trained play was not measured"). Measured
now: **0 tier-2 survival waterings admitted-but-unemitted per game; 0.67
mandatory tiles/game, all terminal-day; 0 plants or animals lost in 6 games.**
The implication's repair therefore has an upper bound near zero here, matching
the 2026-09-08 oracle's +429/game against a 1,500 bar.

Could a fix move paired win rate on `S/livec` (72 tapes × 2 seats = 144 games)?
**No** — ~99 planner-value coins/game on day 29 is two to three orders below the
per-board margin lottery, and it is an unpaid change to the route order with
`ROUTE_EARLY_ON` (−158,893 HELD42) as the downside shape.

If built anyway, the exact paired test, in order — same four arguments to each:
`bash S/topb2/run.sh <name> <worktree> artifacts/kagg2_games/thetas/flow172_g1000.npy "OPEN_PUMP_ON=True,TAIL_FILL_ON=True,BANK_BEFORE_LOT_ON=True,HIRE_ROW_ON=True"`
(20 tapes / 40 games, screen) → `S/livec/run.sh` (72 tapes / 144 games, decisive)
→ `S/live62/run.sh` (62 boards / 124 games, LIVE55 flip rule); read out with
`S/bank/paired.py S/lossflip/g940pair_<set>.csv S/lossflip/<name>_<set>.csv`.

**Dead ends.** (a) `ADMIT_ROUNDS` 3→4 "fixes" the probe but costs its 480-coin
harvest and reads level on 1,904 engine boards. (b) A post-route mandatory check
has nothing to catch: 0/2,240 tier-2 ops missed. (c) `value_dropped`
(`plan.py:6915`, `sum(where(task & ~(admitted & covered), tile_value, 0))`) is
already the shipped metric for this, if it is ever revisited.
*Evidence (session scratchpad): `probe_f2.py`, `f2src/` (instrumented planner
copy), `f2log.*` (180 day-plan JSONL), `analyze_f2.py`, `detail_f2.py`.*
