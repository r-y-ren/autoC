# VRPDEADLINE1 — one deadline for route_vrp.apply, checkpointed solutions (2026-09-24)

Branch `vrpdeadline1` (from 22c798a8). Code `src/kagg3/agent/route_vrp.py`; tests `tests/test_route_vrp_deadline.py`
(+ load-independent fixtures in the two existing VRP test files); tools `S/vrpdeadline1/` (split.py, summ.py, parity.py,
pcmp.py, ckdiag.py, dev.py, lane.sh, load8.sh, devcmp.py; outputs `out/`). Recording: 600 dawns
`kagg3_wt_vrpfallback1/S/vrpfallback1/out/rec_base_0.pkl` (20 V56 dev boards x 30 days).

## 1. Claim-by-claim verdict (master 22c798a8 line numbers)
| claim | verdict | lines / evidence |
|---|---|---|
| best_insert() checks the global 0.7 s deadline | TRUE | `_DEADLINE` set in apply :1024 (`time.time() + SAFETY_S`), checked only at :361 |
| improve() and ruin-and-recreate use local deadlines + HARD_CAP = 3.0 | TRUE (literally) but INERT | :408/:412 `t_end + HARD_CAP`, :490; t_end = now + 0.7 (or +budget/4, /2) so the local caps sit at >= 3.2 s. Both loops call best_insert, so the global 0.7 s check fires first: 0/580 dawns ever reached a local cap (improve max 0.42 s, RR max 0.36 s under load). RR is bounded by RR_ITERS = 30 anyway |
| inner 2-opt loop has no deadline check | TRUE | :424-432; max interval between two deadline checks 0.33 s (cold numpy.random in day-0 RR, load 30) / p99 0.06 s |
| final encoding/verification is outside the enforcement | TRUE | _write :820-836, _trim_sells :837, verify :1029 run after the last check; measured 3-4 ms median, 34 ms max (load 20), 28 ms max (load 30) |
| so 0.7 s is not a strict total bound | TRUE | worst case = 0.7 + longest unchecked segment (0.33) + post-solve (0.03) ≈ 1.06 s; observed max 0.705 s on 580 dawns under 8-process load |
| a later insertion can time out and discard everything incl. earlier crew reductions | TRUE | the exception from best_insert inside mode2_ii :588 (next hand) propagates to apply :1033, which returns the planner table: every hand already dropped is lost |

The statement is true in substance. The practical exposure is the last claim (a timeout costs the whole day), not the overrun:
the overrun past 0.7 s was <= 0.01 s in every measured case except the cold first call.

## 2. Time split (580 dawns d0-28, NEEDS_FIX on = vrp3 config; seconds; box shared with other agents)
| phase | before, load ~20: med / p99 / max | before, +8 busy procs (load 30-32) | after, load ~17 | after, +8 busy procs (load 20-30) |
|---|---|---|---|---|
| construct (insertion) | 0.000 / 0.060 / 0.090 | 0.000 / 0.070 / 0.095 | 0.000 / 0.061 / 0.079 | 0.000 / 0.079 / 0.112 |
| improve (relocate + 2-opt) | 0.044 / 0.253 / 0.327 | 0.059 / 0.326 / 0.420 | 0.046 / 0.252 / 0.300 | 0.062 / 0.316 / 0.351 |
| ruin-recreate | 0.054 / 0.207 / 0.268 | 0.067 / 0.273 / 0.360 | 0.053 / 0.196 / 0.239 | 0.071 / 0.294 / 0.324 |
| mode2 crew-drop insertion | 0.002 / 0.006 / 0.009 | 0.002 / 0.011 / 0.029 | 0.002 / 0.006 / 0.033 | 0.002 / 0.013 / 0.045 |
| write-back (encode) | 0.000 / 0.001 / 0.001 | 0.000 / 0.005 / 0.009 | 0.000 / 0.001 / 0.006 | 0.000 / 0.005 / 0.017 |
| NEEDS_FIX trim | 0.000 / 0.001 / 0.001 | 0.000 / 0.004 / 0.005 | 0.000 / 0.001 / 0.002 | 0.000 / 0.004 / 0.008 |
| VERIFY | 0.002 / 0.005 / 0.032 | 0.002 / 0.011 / 0.027 | 0.002 / 0.037 / 0.047 | 0.002 / 0.026 / 0.088 |
| after last deadline check | 0.004 / 0.008 / 0.034 | 0.004 / 0.018 / 0.028 | 0.003 / 0.039 / 0.049 | 0.004 / 0.027 / 0.088 |
| longest unchecked interval | - | 0.003 / 0.060 / **0.328** | 0.001 / 0.047 / 0.054 | 0.004 / 0.080 / 0.118 |
| **total apply** | 0.111 / 0.511 / 0.675 | 0.151 / 0.667 / **0.705** | 0.113 / 0.498 / 0.607 | 0.152 / 0.612 / **0.613** |
| deadline fired / fell back to the planner table | 0 / 0 | **3 / 3** | 1 / 0 (restored) | **15 / 0** (all 15 restored) |
Local deadlines (HARD_CAP) overrun: 0 in every run. Checkpoint bookkeeping cost: median total +0.002 s.
(The "after" columns: search deadline 0.6 s. Final setting 0.65 s under +8 procs: total max 0.690 s, 6 fires, 6 restored; §5.)

## 3. Design (all in route_vrp.py)
- ONE deadline: `apply` reads `t0 = _CLOCK()` (`time.perf_counter`, swappable for tests) and sets
  `_DEADLINE = t0 + SAFETY_S - RESERVE_S` (SAFETY_S 0.75 total, RESERVE_S 0.10 for write-back + trim + VERIFY + restore:
  measured post-search max 0.05-0.09 s under load). `_check()` sits in best_insert, at the top of `_solve`, in every
  2-opt outer step, in every RR iteration and in every fix_spawns round. HARD_CAP and the local `t_end` bounds are gone
  (t_end only feeds the research knob RR_ITERS=None). RR_ITERS = 30 stays deterministic.
- Checkpoints: `Solver._ckpt` records every complete feasible solution of the current context (crew, dropped hires,
  the spawns it was evaluated under): after insertion/init, after each improve pass, after each RR improvement of the
  best, and in mode2_ii right after the dropped hand's stops are re-inserted (then after its improve/RR). Consecutive
  duplicates are skipped. The fill modes and the ROUTEOPT2 optional-stop path do not checkpoint (both OFF in the ship).
- On `_Timeout`: the checkpoints are tried latest first (up to 64, each only if still inside SAFETY_S). `_restore`
  re-evaluates the routes on the checkpoint's spawns, settles spawns to the engine's rule (<= 3 rounds, routes kept, no
  search), writes the table, removes the dropped HIRE rows, runs the NEEDS_FIX trim, and keeps it only if VERIFY accepts.
  Otherwise (no checkpoint yet, none valid, or past SAFETY_S) the planner's table, as before. fstate (fill ledger) is not
  committed on a restore.
- numpy.random is warmed at import (its first call cost 0.06 s idle / 0.33 s loaded inside day 0's RR).
- Offline restore rate (ckdiag.py, SAFETY_S 0.25 forcing 180 timeouts on the 600 dawns): 175/180 restored (97 %);
  with only the 4 latest checkpoints tried it was 150/176 (spawn-inconsistent same-crew checkpoints reject in 0.5 ms).

## 4. Parity (no deadline fired => byte-identical to master)
- 600 recorded dawns, SAFETY_S = 1e9, NEEDS_FIX off and on: plan arrays and stats identical 600/600 in both configs
  (`parity.py` + `pcmp.py`, final code).
- 3 sim boards (V56 dev 0-2, exact sim, NEEDS_FIX on, SAFETY_S = 1e9): purses and per-board VRP stats identical.
- V56 dev100 (real clock): on every board where neither side's deadline fired, the purses are identical (0 exceptions
  in 3 separate arm runs; table below).
- Tests: `tests/test_route_vrp_deadline.py` — (a) no-deadline output equal across budgets; (b) fake clock expiring
  after the first improve pass returns a restored checkpoint (not the planner table), VERIFY-clean, hires <= the
  insertion solution's; (b') expiring after a successful crew drop keeps that drop (master lost the day); (c) expiring
  before the first checkpoint returns the planner table byte for byte; (d) past SAFETY_S nothing is restored.
  The existing VRP tests got `SAFETY_S = 1e9` fixtures: `test_fix_recovers` failed on master itself at load 22
  (the 0.7 s break fired).

## 5. V56 dev100 (exact sim, NEEDS_FIX on, 1 lane each, head_940)
| run (arm vs master base) | box | W base -> arm | boards w/ a fire: base / arm | fired days: base / arm (restored) | identical / differ w/o fire | dours | dmargin (t) |
|---|---|---|---|---|---|---|---|
| **final** (search 0.65 s, total 0.75 s), base+arm run concurrently | load 13-55, stalls | 86 -> 87 | 18 / 28 | 21 / 33 (13) | 69 / **0** | +13 | **+20 (1.07)** |
| search 0.6 s, 4 tries (devf) vs devm | load ~20 | 87 -> 87 | 8 / 19 | 10 / 20 (7) | 82 / **0** | -11 | -15 (-1.81) |
| search 0.6 s, 64 tries (devf2) vs devm | load 13-20 | 87 -> 87 | 8 / 9 | 10 / 10 (2) | 87 / **0** | -4 | -9 (-0.89) |
| search 0.6 s (devf3, diag, ran beside the load test) vs devm | load 30-60 | 87 -> 87 | 8 / 37 | 10 / 44 (36) | 72 / **0** | -20 | -21 (-1.02) |
Purse effect: noise (|t| <= 1.8, sign flips with the load); wins flat or +1. Fire counts track the box load, not the
code (the same master base fired on 8 boards at load ~20 and 18 boards at load 20-55). Diag (dev.py VRPDL_DIAG): in the
final pair 15 (master) / 21 (arm) dawns took > 0.8 s, max 172 s / 30 s — the lane process was descheduled mid-step; those
fires come back past SAFETY_S, so they correctly keep the planner table (restored 13 of 33). Offline (no stalls)
the restore rate is 97 %.

Final setting under +8 busy processes (580 dawns, load 22-26): total med 0.139 / p99 0.659 / **max 0.690 s**, 6
fires all restored, 0 planner fallbacks; master under the same test: max 0.705 s, 3 fires, 3 planner fallbacks.

## 6. Left
- VERIFY-fail days (3-4/game) still return the planner table; the checkpoints could serve them too (changes the
  no-deadline output, needs its own gate).
- Under heavy box load the process itself stalls 0.8-2 s inside single steps (dev lane diag: 7 days with total 0.9-2.0 s,
  the search had used < 0.06 s on two of them): no in-process deadline bounds that; it is load, not the solver.
