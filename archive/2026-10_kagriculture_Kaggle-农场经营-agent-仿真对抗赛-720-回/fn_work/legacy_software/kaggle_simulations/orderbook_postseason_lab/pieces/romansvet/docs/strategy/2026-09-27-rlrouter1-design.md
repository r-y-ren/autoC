# RLROUTER1 (2026-09-27): learned destroy step inside the VRP ruin-recreate loop — design + headroom bound → NOT WORTH IT

Branch selfplay1 (HEAD 23e52ff1), read-only on src. Tools `S/rlrouter1/` (`bound.py` per-dawn replay, `summ.py`), outputs
`S/rlrouter1/out/` (`b_<iters>_<restarts>.pkl`, `summ.txt`). Inputs read: ROUTERAUDIT1, RRDEPTH1, RRSPEED1, RRDEEP2, ROUTERJIT1,
SHIPJIT1 and `route_vrp._rr_chain` (destroy = random seed stop + its 3..k nearest tiles; recreate = late-first insertion in one
`rv_insert_seq` kernel call; accept if the route total falls, or with 2 % probability; incumbent checkpointed by `sol_key`).

## 1. Headroom measurement (the one new run)
600 recorded pre-VRP dawns (`rec_base_0.pkl`, 20 dev boards x 30 days, open loop), master route_vrp (== stage_rrdeep2 src_live),
vrp8_jit config (EMPTY_ROUTE_UNHIRE_ON, k 10, resolve ON, JIT), SAFETY_S 1e9 / REPAIR_MS 1e7, one pinned core per cell.
| cell | CPU/dawn mean | Δbill saved/g vs shipped (t over 20 boards) | d0-9 / d10-19 / d20-29 | Δhands dropped/g | dawns better / worse / same |
|---|---|---|---|---|---|
| shipped 150 x 1 | 0.054 s | 3,385.8 saved, 40.75 hands dropped (base) | | | |
| 10x iterations 1500 x 1 | 0.403 s | **+12.9 (0.13)** | +6 / +109 / −103 | +5.25 | 153 / 44 / 403 |
| random restarts 150 x 10 | 0.397 s | **+22.0 (0.22)** | +6 / +45 / −29 | +3.90 | 131 / 48 / 421 |
| per-dawn best of the three (hindsight portfolio, 21x CPU) | 0.85 s | +503.5 | +9 / +223 / +272 | | |
Reading. Ten times more descent on the RR objective (route time at a fixed crew) moves the hire bill by +13 to +22 coins/game,
t 0.1-0.2: the search on its own objective is saturated at 150/10 (RRDEEP2 found the same in closed loop). The only large number,
+503/game, is hindsight selection across chaotic outcomes of the greedy drop loop (mode2_ii: drop hand u if the re-solved crew has no
miss). A small route change at the full crew flips whether the next hand drops, so the three arms disagree on 260 of 600 dawns in
both directions. A destroy policy trained on Δsol_key per iteration learns the route-time descent that 10x iterations already
bounds (+13 to +22). It does not see which chain will drop the next hand.

## 2. Coins/game (question 1)
| source | Δbill/g | → Δmargin/g | note |
|---|---|---|---|
| ROUTERAUDIT1 oracle vs shipped-30 (5 boards) | +722 | — | mostly the 30→150 step, already shipped in vrp8_jit (RRDEEP2) |
| RRDEPTH1 30→150 (shipped) | +357 offline | dev +126, held +323, FRESH +355 | first step: 0.35-1.0 margin per bill coin |
| RRDEEP2 150→300 / 300 k14 / 150 x 2 (closed loop) | +147 / +164 / +84 real | ≈ +12 / +49 / +100; flips −1 / −2 / 0 | plateau: the rival takes about 100 back on the deeper cells |
| **learned destroy at the live clock (bound = 10x iterations)** | **≤ +13 to +22** | **≤ +2 to +20** | far below the +150 build bar |
| hindsight portfolio (not reachable by a destroy policy) | +503 | ≈ +40 at the plateau rate; ≤ +175 even at the first-step rate | needs 21x CPU and a seer |
Hand-turns: 10x adds +5.25 dropped hands/game (about 126 hand-turns), but they are cheap low-fib hands and the bill barely moves. Moves were not
re-measured (ROUTERAUDIT1: routes already within 4.4 % of each hand's own TSP bound).

## 3. Design as it would be built (question 2; kept for the record)
* Input per stop j (n ≤ ~120): tile (x, y), time window (early, late, width), ops count, current hand's fib wage, route slack before
  and after j (waits), detour (removal gain), insertion regret (2nd−1st best), same-hand/neighbour counts, day, hour, n hands, iteration/iters.
  About 16 floats per stop.
* Output: seed stop (softmax over stops) plus destroy size 3..k (6-way head), nearest-by-score set. Zero logits = the shipped random destroy.
* Model: 2-layer per-stop MLP 16→32→1 (≈600 weights) plus a mean-pooled context vector, run as one matrix-vector product per iteration
  in the compiled kernel (a new `rv_score` in route_vrp_c.c, weights as a baked const array). About 120 x 600 = 72 k FLOP per iteration,
  < 0.05 ms, so 150 iterations add < 10 ms. No torch/JAX at inference. A fixed-seed argmax/sample keeps sims deterministic.
* Training signal: DAgger on recorded dawns. The label is the destroy set that gives the best Δsol_key (hands x fib first, then route
  time) among M=16 sampled destroys per iteration, taken from 1500-iteration rollouts, opponent-free. PPO fine-tune on 150-iteration
  episodes with reward = final sol_key vs the shipped chain on the same dawn (common random numbers).
* Data: 600 recorded dawns now. LIVE250 boards 200-299 can be recorded as 3,000 more (never gate boards), about 0.05 s CPU per dawn replay.
  Train on the remote GPUs (free); rollouts on remote CPU.
* Judge: offline bar ≥ +150 bill/g over 150 x 1 on the 600 dev dawns, then the ship legs: dev100 / held100 / FRESH300 paired (1e9 both arms),
  faithful-59, tapes dev50 at the live clock, CPU p99 < 0.65 s.

## 4. Risk (question 3)
* Clock: the scorer adds < 10 ms per dawn. The vrp8_jit CPU p99 is 0.22-0.28 s, so the clock is not the risk.
* Determinism: weights are baked in and the chain seed is fixed; byte-exact sims hold if the kernel runs in float64 and argmax ties are broken by index.
* Failure modes: (a) the objective is misaligned. The destroy step optimises route time, but the money is in whether the drop loop sheds the next hand, and
  §1 shows that outcome is chaotic (44-48 dawns worse under strictly more search). A learned policy can be worse than random destroy
  on exactly those dawns. (b) Gift: deeper drops on d20-29 hand the rival about +100/game (RRDEEP2 a/c, VRPREPAIR2 board 24).
  (c) Diversity loss: random destroy is what escapes local optima. A peaked policy collapses the chain; the 2 % random accept is not enough.

## Verdict — NOT WORTH IT
Headroom a learned destroy step can reach = the 10x-iteration bound, **+13 to +22 bill/game (t 0.13-0.22), ≤ +20 margin/game,
expected 0 flips**, far below the +150 bar. The rest (+503 hindsight) is drop-loop chaos, not destroy quality. RRDEEP2 already showed that
84-164 real bill/game converts to net 0 to −2 flips at this plateau. The router axis stays CLOSED. Not built: an unmeasured
non-learned variant, best-of-R whole-apply() seeds chosen by sol_key (R=2-3 at the shipped 150 iterations, about 0.16 s mean CPU). Its
expected value is capped by the same RRDEEP2 conversion (≤ +1 flip), so it is not recommended either.
