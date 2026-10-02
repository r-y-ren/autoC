# ROUTERAUDIT1 (2026-09-26): how much the VRP crew router leaves on the table + RL-router design (design only)

Branch `routeraudit1` off master 6f4283f3. Read-only on src. Tools `S/routeraudit1/` (`audit.py` arms on recorded dawns,
`summ.py`, `summ2.py`), outputs `S/routeraudit1/out/` (`summ.txt`, `summ2.txt`, `rr150_20.txt`, per-arm pkl).
Data: 600 recorded pre-VRP dawns (20 V56 dev boards x 30 days, `kagg3_wt_vrpfallback1/.../rec_base_0.pkl`), shipped
switches (vrp5: NEEDS_FIX, VERIFY, REPAIR_ON with REPAIR_LAST_DAY 20). Offline, open loop: a dawn's plan is solved,
not played; bill = the fib wage of the dropped hands (`drop_cost`). Box load 8-26 during the runs.

## Part A. What the router leaves (per game)

### A1. Route quality and task side (600 dawns, shipped router, SAFETY_S 1e9; live 0.75 s is identical, see A2)
| quantity | planner table | VRP (shipped) | bound / note |
|---|---|---|---|
| hires | 264.5 | 236.3 (28.2 dropped, bill 2,596) | oracle below: about 16 more hands can go |
| moves | 2,885 | 2,085 | exact per-hand TSP on the hand's own tiles (Held-Karp, <= 10 tiles, no time windows) 1,998 (+4.4 % slack); whole-crew MST 1,462 |
| moves/day d0-9 / d10-19 / d20-29 | 51.6 / 115.0 / 122.0 | 37.5 / 82.8 / 89.3 | per-hand TSP 37.1 / 80.4 / 82.2 |
| work ops (incl. pickups) | 3,249 | 3,166 | -83 = merged pickups, 0 planner (tile, op) missing |
| idle h0-2 / h3-20 / h21-23 | 260 / 74 / 276 | 52 / 364 / 451 | idle comes from the drops: it is the part of a hand's day the crew no longer needs |
| hires with < 3 ops | 1.4 | 1.5 | not a leak |
| fallback days (planner table kept) | - | 2.05 (miss 1.65, VERIFY fail 0.40) | about 100-150 coins/day of bill forgone at d10+ |
| ops later than the planner's hour | - | 824 (harvests 131), 4,100 hour-shifts; 1,627 earlier | units with a same-day drop/place are frozen; late harvests reach the shed at dusk as before |
Sequencing is almost solved: each hand's route is within 4.4 % of its own TSP bound. The slack is the ASSIGNMENT and the CREW SIZE (MST 1,462 vs
2,085), and it shows up as hires, not moves.

### A2. Time: 0.75 s vs unlimited, shipped search
apply() wall: median 0.126 s, p90 0.32, p99 0.57, max 0.66 s. At 0.75 s it timed out on 1/600 dawns and the checkpoint was restored.
**Live 0.75 s minus 1e9: 0 bill, -2.4 moves per game (1 dawn differs).** Running the shipped search longer gains nothing: it stops at
RR_ITERS 30, not at the clock. The headroom is in HOW DEEP the search goes.

### A3. Oracle (150 dawns = boards 0-4 x 30; shipped arm on these boards saves 2,101/game)
| arm | bill saved/game (d0-9 / d10-19 / d20-29) | Δ vs shipped | hands dropped | moves | fallback days | wall median / p99 |
|---|---|---|---|---|---|---|
| shipped (0.75 s or 1e9) | 2,101 (24 / 861 / 1,216) | - | 27.4 | 2,074 | 1.2 | 0.13 / 0.50 s |
| + drop loop only (re-solve the smaller crew from scratch after mode2_ii fails) | 2,158 | +57 | 28.0 | 2,069 | 1.2 | 0.13 / 0.42 |
| full insertion scan + repair every day, EJECT_K 12 + drop loop | 2,072 | -29 | 27.6 | 2,083 | 1.6 | 0.35 / 1.28 |
| **RR 300 iters x 3 seeds, destroy <= 10 + drop loop** | **2,919** | **+818** | 44.2 | 1,892 | 1.0 | 1.78 / 4.33 |
| oracle (all of the above, repair every day) | 2,823 | +722 | 43.4 | 1,922 | 1.6 | 4.5 / 13.3 |
| portfolio max(oracle, shipped) per dawn | 3,067 | +966 (d10-19 +388, d20-29 +560) | +18.2 | | | |
| **RR 150 x 1 seed, destroy <= 10 + drop loop, LIVE 0.75 s** | 2,635 | +534 | 38.0 | 1,951 | 0.6 | 0.34 / 0.66 (4.4 timeouts/game, all restored) |
The headroom is LNS depth (ruin-recreate) together with re-solving the smaller crew. Wider insertion scans and more repair add nothing.
**At the live clock on all 20 boards (`rr150_20.txt`): RR150 + drop loop saves 2,953/game vs shipped 2,596 = +357** (d0-19 +106,
d20-29 +251), 35.4 vs 28.2 hands dropped, fallback days 1.40 vs 2.05, 3.95 checkpoint restores/game, max 0.670 s.

### A4. Coins/game headroom: plain verdict
* Router-only ceiling (bill, offline): about **+800-970/game** (5-board oracle; the 5 boards run lower than the 20, where the reachable part
  scales from +534 to +357, so a 20-board ceiling of about +550-650 is likely). About 70 % of it is on d20-29.
* Reachable without learning at 0.75 s: **+357 bill/game** (RR150 + drop loop).
* Bill does not equal margin. Past conversions: ROUTEOPT1 offline 2,898 -> Δours +2,813 -> tapes Δmargin +2,069 (25 % mirrored to the
  rival); VRPREPAIR1 offline +412 -> dev Δours +286 -> Δmargin +124. The late (d20+) drops are exactly where VRPREPAIR2 found the
  board-24 price gift (fewer hands -> fewer occupied tiles/late units -> the rival sells higher).
  Expected margin: **+100-250/game reachable, +250-600 at the full ceiling**.
* **The router beyond a knob change is below the 500 coins/game bar.** A learned router can only chase the ~+300 bill/game between
  RR150 and the oracle, which is about +100-200 margin. The router is not where the next big gain is.
* Objective blind spots: `sol_key` = (-Σ fib wage of the dropped hands, route time). A saved hire is valued at the wage only; the purse
  it frees is not valued. The day-after cost of a late drop (occupied tiles, late sale volume, price gift) is also not valued, and
  that cost is where VRPREPAIR2/3 lost. Tasks are all-or-nothing: 0 planner tasks are ever left undone, and optional tail work is worth 65-72/game (ROUTEOPT2).

## Part B. RL router with the VRP as warm-up (design only; the user reviews before anything is built)
**Why ROUTENN1-3 collapsed to KEEP.** (1) They acted per TURN (dispatch, 2,700 KEEP decisions/game). Almost every deviation broke couplings the
planner had set up (market rows, h1 pickups, spawns, same-day lots), so the only purse-positive policy was "no deviation" (rn3_c:
changes 17 -> 1.3/game). (2) The money in routing is the CREW SIZE, a dawn-level combinatorial decision. rn2/rn3 froze the hire
head and rn1's hire head gifted. (3) Reward = game purse (ON-OFF) is noisy and delayed per decision.
What changes it: learn at the DAWN inside the solver. The reward is the solver's own exact objective (opponent-free, no rollouts),
and the VRP solution is kept as the incumbent, so any learned output is accepted only if it beats the incumbent.

| option | what is learned | state / action | warm start | reward | never worse than VRP by | per-dawn cost (1 s actTimeout) | data | risk |
|---|---|---|---|---|---|---|---|---|
| (i) BC VRP routes + PPO residual | per-unit route/dispatch | turn-level unit state / next stop | BC on VRP routes | purse ON-OFF | elite: ship only if held dawns >= VRP | ms/turn | game rollouts (remote GPU) | = ROUTENN3 again: executor fidelity, KEEP collapse, noisy reward; the crew size is still not learned |
| (ii) RL over solver knobs per dawn | INSERT_K, RR iters/destroy size, repair on/off, hire cap | dawn features / small discrete | shipped knobs | Δsol_key offline (+ gate) | knob set includes shipped; argmax keeps shipped if no gain | 0 (picks knobs) | recorded dawns | low ceiling: RR depth dominates and a fixed knob (A3) already takes most of it; per-dawn choice adds little |
| **(iii) learned LNS destroy/repair operator inside the budget** | which stops to ruin (seed stop + size) and in what order to re-insert | per stop: tile, window, ops, route slot, insertion regret, hand load / pointer over stops | uniform random destroy (= shipped RR, zero logits) + BC on the oracle's improving iterations | Δsol_key per iteration (hands x fib, then route time), exact | runs AFTER the shipped search on the remaining clock; incumbent + checkpoints kept; accept only a better sol_key | ~1 ms/iteration numpy; 100-300 iterations fit in 0.5 s | 3,000+ recorded dawns, offline, CPU solver + GPU trainer | ceiling = RR150 -> oracle gap (~+300 bill/game); gift risk on d20+ drops |
| (iv) offline imitation of the oracle | crew size + assignment as supervised labels | dawn / hands to drop + stop->hand | none (supervised) | cross-entropy vs oracle | decode, then repair; fall back to VRP if infeasible | ms | oracle labels (4.5 s/dawn x 3,000 = CPU hours) | infeasible decodes; labels from a heuristic oracle; same ceiling as (iii) |

**Recommendation: (iii), but only after the knob step. The knob step is the real gain; the learned part is below the bar.**
1. RRDEPTH1 (non-learned, 1 day): RR_ITERS 150, destroy size <= 10, re-solve drop loop after mode2_ii, under the existing deadline and checkpoints
   (offline +357 bill/game at 0.75 s). Gate it as any VRP switch (dev100 / held-out100 / FRESH300 paired, SAFETY_S 1e9 both arms, faithful-59,
   band tapes, live-clock timing). Run a REPAIR_LAST_DAY-style late-day cut grid in the same dispatch: that is where the gift sits.
2. (iii) only if RRDEPTH1 passes and the user still wants the RL router. It warm-starts from exactly the RRDEPTH1 search (zero logits = shipped
   random destroy), so the learned policy starts equal to the VRP and can only replace destroy choices when Δsol_key improves.

**2-day build plan for (iii)** (branch `lnsrl1`, switch `ROUTE_VRP_LNS_ON` default OFF):
* Day 1. `S/lnsrl1/record.py`: 3,000 pre-VRP dawns (LIVE250 boards 200-299, never gate boards). `S/lnsrl1/env.py`: RR iteration as an
  env step on `route_vrp.Solver` (state = stop features + incumbent; action = seed stop via pointer + size 3-10; reward = Δsol_key,
  hands first). `S/lnsrl1/train.py`: JAX pointer net (~20k params), BC to the oracle's improving destroys, then PPO on 150-iteration
  episodes. Solver rollouts on remote CPU workers, trainer on remote GPU0 (GPU LAW).
* Day 2. numpy inference in `route_vrp.py` (runs after the shipped search, fixed iteration count so sim results are deterministic, deadline and
  checkpoints unchanged). Offline table on the 600 dev dawns vs RRDEPTH1 and the oracle (bar: >= +150 bill/game over RRDEPTH1). Then the gates:
  dev100 / held-out100 / FRESH300 paired vs the shipped router, SAFETY_S 1e9 both arms; faithful-59; band tapes (Δtheirs); live-clock
  timing (local loaded + remote unloaded, p99 apply < 0.65 s, 0 non-restored timeouts).

**Where the learned component should sit instead.** The router already does the planner's task set with about 16 hands/game of crew
slack left (A3), and sequencing is within 4 % of TSP. The next gain is in WHAT the planner asks: plantings/animals per day (YIELD1:
their volume = COUNTS, tomato 709 vs 315 plantings), costed by the VRP's exact marginal-hire price of each extra task. That is
different from FILLWORK1/ROUTEFILL1's fixed spare heuristic. History warns that V56 takes volume gains back through price (ROUTEFILL1, RELAYFILL1), so that
stream must gate on margin, not purse.
