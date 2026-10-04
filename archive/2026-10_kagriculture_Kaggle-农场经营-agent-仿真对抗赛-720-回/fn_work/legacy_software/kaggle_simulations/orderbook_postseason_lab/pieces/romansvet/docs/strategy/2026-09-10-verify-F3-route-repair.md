# Verify F3 — "Route repair can reduce its own task-value objective"

Independent check of finding 3 of `docs/2026-09-10-planner-findings.md` (detail:
`docs/reviews/planner-2026-09-10/REVIEW.md` §4). Read-only on every worktree
`src/`; the patched planner was an in-memory `exec` of rewritten function source.
Engine: 12 baseline + 12 patched games = **6.1 min**.

**Verdict: the behaviour is CONFIRMED and reproduces byte-identically; "its own
objective" is REFUTED (the loop optimises admission feasibility, not completed
value); the −612.5 coins/game intervention result is REFUTED as an effect
estimate — n=3 distinct games, one counted twice, and on 12 distinct LIVE-C
boards the same patch reads −10 ± 150 coins/game, t −0.07, 0 win flips. "Not a
validated improvement" is right; "worsened by 612.5" is not. Family closed
2026-09-08.** `ship-pair` and the shipped `ship-pair-hr` differ in **one line**
(`HIRE_ROW_ON` `False`→`True`, `plan.py:3523`; whole-file diff = 1 hunk), so
every line cited below is byte-identical in both.

## 1. Source — what the repair loop actually optimises

| stage | line | code |
|---|---|---|
| rounds constant | `plan.py:210` | `ADMIT_ROUNDS = 3` |
| **admission order** (value) | `plan.py:6436-6438` | `order_v = task_order(xp, d.task, d.tile_value, d.tier)`; `cum_est = cumsum((d.n_ops + EST_MOVES)[order_v])` |
| admitted count | `plan.py:6472` | `n_admit = minimum(_count_le(xp, cum_est, labour), n_tasks)` |
| **route order** (spatial) | `plan.py:6473`, `6491` | `route_tier = (d.tile_value > 0)`; `order = task_order(xp, admitted, zeros(N_T, i32), route_tier)` |
| the loop / its only update | `plan.py:6489`, `6521` | `for _ in range(ADMIT_ROUNDS): admitted = d.task & (rank_v < n_admit)` … `n_admit = n_admit - sum(admitted & ~covered)` |
| the residue, stated | `plan.py:6362-6368` | *"`n_admit` falls by the uncovered count each round, so a shortfall deeper than `ADMIT_ROUNDS - 1` tiles still ends on a route that leaves admitted work undone"* |

**The loop has no value objective.** `n_admit` is a *count*; the update at 6521
only ever lowers it (`plan.py:230-233`: *"`ADMIT_ROUNDS` exists precisely to
repair an over-admission … an under-admission has no repair at all — the loop
only ever lowers `n_admit`"*), and `tile_value` enters only through `order_v`,
deciding **which** tile is dropped, never how many. The loop optimises
consistency between the `cum_est` estimate and the exact `_routes` walk —
feasibility, not coins.

**Why a later round can end lower.** Admission is a *prefix* of the value order;
routing is a *serpentine sweep* of that prefix cut into contiguous per-unit
blocks (`plan.py:6939-6950`). Dropping the value-tail tile changes the sweep's
span and every block boundary, so a high-value tile inside a block can fall
outside the next round's cut. "Drop k low-value tiles → covered set" is not
monotone and nothing claims it is: 840→720→360 is a **shape effect of a
feasibility contraction**, not a regression in an optimised quantity. "Reduces
its own objective" is literally false; "reduces a quantity it does not optimise,
and never promised to" is true.

## 2. Reproduction — exact

`probe.py` re-run from a scratch copy against `ship-pair`: `probes.json` is
**identical in all seven keys**, including `route_rounds = {1: 840, 2: 720,
3: 360, 4: 480, 5: 480}` (not even monotone downward) and `route = {queued 1320,
covered [9], 360, brute force 840 in 19 turns}`. Recomputed from `games.json`:
**11/120** day-plans end below an earlier round, totalling **693** planner-value. Context the finding omits: **95/120** day-plans have all
three rounds *identical* (a no-op on 79 % of days); only 15/120 ever fall
round-to-round, by 3–148 planner-value against day totals of 5,000–30,000; and
8 of the 11 rows are one board twice (`107244033` seat 0/1 give bit-identical
traces). 693 planner-value over 4 games ≈ 173/game ≈ 0.2 % of ~87k final coins —
and `tile_value` is not coins.

## 3. The intervention — design audit and re-measurement

**Paired?** Yes. `route_ab.py` takes seed/tape/seat from
`S/lossflip/g940pair_topb.csv` with the same `KAGG3_TOWN_SCHEDULE`
(`S/band2100p/town_schedules.json`), theta (`flow172_g940.npy`) and tree;
`games.py` reproduced all four baselines to the coin (`OPEN_PUMP_ON` is already
the `ship-pair` default). Sound.

**n is not 4.** The `107244033` seat-0/seat-1 rows are bit-identical in the
baseline CSV *and* in the patched arm, so −1,229 is one game entered twice:
3 distinct games (2 boards), mean **−407**, not −612.5. Judge-set property, not
the review's fault — **59 of 72** LIVE-C boards play out identically in both
seats under pinned towns.

**Noise floor.** Paired Δmargin sd for real switch arms on LIVE-C vs
`g940pair_livec.csv`: compactsoft 1,198 · ctpush200 1,431 · fertvol 1,476 ·
chainmax8 1,624/game. At n=3–4 SE is 600–940, so −612.5 sits 0.6–1.0 SE from
zero. **Unmeasured, not "worsened".**

**Re-run (this verification).** Same patch, same source rewrite, in memory;
`ship-pair` + `flow172_g940`, pinned towns, seeds from
`S/lossflip/g940pair_livec.csv`. The baseline was re-run in the same harness and
reproduced that CSV to the coin on all 3 spot-checked boards (confirming
`ship-pair` defaults == the `arms-next`+switches config that produced it).
Boards 1–3 ran both seats — identical in both arms — so boards 4–12 ran seat 0
only and n counts **distinct boards**.

| board | Δ ours | Δ theirs | Δ margin | | board | Δ ours | Δ theirs | Δ margin |
|---|---:|---:|---:|---|---|---:|---:|---:|
| 107427438 | +518 | −236 | **+754** | | 107435352 | +13 | −15 | +28 |
| 107429978 | +20 | +50 | −30 | | 107436314 | −418 | +956 | **−1,374** |
| 107430502 | −46 | −108 | +62 | | 107439261 | −20 | +81 | −101 |
| 107432396 | +522 | −99 | **+621** | | 107446132 | +267 | +68 | +199 |
| 107433383 | −277 | +6 | −283 | | 107441233 · 107442209 · 107445568 | 0 | 0 | 0 |

**n = 12 distinct boards · mean Δmargin −10.3 · sd 520 · SE 150 · t −0.07 ·
wins 4/12 → 4/12 (no flips) · 3/12 games byte-identical.** Two-purse split:
**Δours +48.2/game, Δtheirs +58.6/game** — neither displacement nor denial; the
patch is inert. The 3 both-seat boards alone read −83.7: the sign is a coin flip.

## 4. Archive — this family is already closed

- **`2026-09-09-verdicts.txt:897` (2026-09-08T18:40Z) is this exact question,
  measured 30× larger and dropped:** *"route repair by insertion/exchange
  instead of admission shrink … NOT a blocker — 96 games/2,880 days: shrink on
  21 % of days drops 24 tiles worth 640 planner-value but routing the un-shrunk
  set is **−2,224/game (the shrink EARNS)**; insertion+exchange oracle recovers
  **+429/game** = 0.08 % of routed value (bar 1,500); 52 % of undone value is
  day 29 behind the DROP leg. Not built. DROP."* That oracle keeps the best
  *possible* route for +429; the best-*round* patch is a subset of it.
- `2026-09-09-verdicts.txt:485/511` — CRN sweep: `ADMIT_ROUNDS` 3→6/8 t +6.3/6.6
  in the sim, fine sweep **3/4/5 level**, stage closed;
  `2026-09-10-planner-wall-audit.md:61` — admit/route turn budget **CLOSED**,
  engine 1,904 boards **+188, t 1.0**.
- `2026-09-10-melon-route-capacity.md` (via both chain-optimisation reviews):
  *"the route model is **not** the wall"* — deposit turn is, and
  `MIDDAY_PLACE_V2_ON` fixes it. `2026-09-10-verify-F2-admitted-unexecuted.md`
  — sibling finding, same loop:
  0 tier-2 ops missed/game, 0.67 mandatory tiles/game, all day 29.
  `S/autojudge/verdicts.txt` has no ROUTE line; nothing route-shaped has ever
  been promoted.

## 5. Verdict, per sentence

| sentence | verdict |
|---|---|
| "Route repair can reduce its own task-value objective." | **PARTLY.** Behaviour real and reproduced; "its own objective" is wrong — the loop optimises admission feasibility (a count that only falls), and completed value is a downstream outcome of a re-cut spatial route. |
| "840 → 720 → 360 … 11 of 120 day-plans finish below an earlier round." | **CONFIRMED**, byte-identical. Scope: 95/120 rounds-identical, 693 planner-value coins over 4 games (~0.2 % of final coins), 8 of the 11 rows one duplicated board. |
| "A tested best-round selection intervention worsened mean final score margin by 612.5 coins across four games; it is not a validated improvement." | **PARTLY — conclusion right, number REFUTED.** Design is properly paired, but n=3 distinct games (one duplicated) against a 1,200–1,600 coin/game paired sd. Re-measured on 12 distinct LIVE-C boards: **−10 ± 150, t −0.07, 0 win flips**. The patch is a null, not a loss. |

**Could a route-selection fix move paired win rate on `S/livec`? No.** Upper
bound = the 2026-09-08 oracle's +429/game against a 1,500 bar; inert on 79 % of
day-plans; the direct 12-board read is 0. If built anyway, the exact paired test,
same four arguments to each:
`bash S/topb2/run.sh <name> <worktree> artifacts/kagg2_games/thetas/flow172_g1000.npy "OPEN_PUMP_ON=True,TAIL_FILL_ON=True,BANK_BEFORE_LOT_ON=True,HIRE_ROW_ON=True"`
(40 games, screen) → `S/livec/run.sh` (72 tapes, the decisive read) →
`S/live62/run.sh`; read with
`S/bank/paired.py S/lossflip/g940pair_<set>.csv S/lossflip/<name>_<set>.csv`.
Count **distinct boards**, not games: `--seed-per-opponent` gives both seats one
seed and 59/72 LIVE-C boards then play out identically.

**Dead ends (do not re-measure).** (a) Best-round selection keyed on
`(tier≥2, tier==1, tile_value)` — null on 12 LIVE-C boards, above. (b)
`ADMIT_ROUNDS` 1/4/5/6/8 — sim-positive, engine-level. (c) Insertion/exchange
repair — oracle +429 vs bar 1,500, dropped 2026-09-08. (d) Treating `tile_value`
as coins: the −2,224/game "shrink earns" line shows the two can carry opposite
signs.

*Evidence (session scratchpad): `probe.py` re-run + `out/probes.json`,
`route_ab_livec.py`, `base3/patch3/base9/patch9.json`.*
