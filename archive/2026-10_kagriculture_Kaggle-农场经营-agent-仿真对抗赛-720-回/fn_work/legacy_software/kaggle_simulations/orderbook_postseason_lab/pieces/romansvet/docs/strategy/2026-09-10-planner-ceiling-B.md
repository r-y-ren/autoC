# Planner ceiling — blind second opinion (B)

2026-09-10. Question (user's): *"what if our planner has erroneous logic that will not help ES
to succeed?"* — is `plan.py` + `brain.decide` the ceiling, so **no** theta reaches the top tier?

Blind: `2026-09-10-forward-horizon-feasibility.md` and consensus §12 were not opened. Angle is
**behavioural reachability**, not code design. All line numbers are the **main worktree**
`/mnt/e/_work/kaggriculture3/src/` (the wall-audit docs cite `arms-next`, whose numbering differs).

## 0. Method and the one empirical read

Static: decode path in `brain.decide`, param layout in `policy.py`, fixed row schedule in `ops.py`.
Behavioural target: the 20 TOPB2 pinned tapes, parsed statically (verb table
`src/kagg3/es/tape_actions.py:60-89`) — median [min..max] over 20 tapes.

Engine, 4 games (~6 min), worktree `.claude/worktrees/ship-pair-hr`, theta
`artifacts/kagg2_games/thetas/flow172_g1000.npy`, switches `OPEN_PUMP_ON,TAIL_FILL_ON,
BANK_BEFORE_LOT_ON,HIRE_ROW_ON`, **seed 4674845 vs tape 107448662, seat 0** (row 1 of
`S/lossflip/g1000pair_hr_topb2.csv`), macro hooked per day à la `scripts/plan_stats.py`.
Probe: `<scratchpad>/probe.py`. **This is one board — it measures the envelope, not profit.**

| arm | perturbation (theta only) | mine | theirs |
|---|---|---|---|
| base | shipped | **81,014** | 75,924 |
| dsmelon | `ds[1,0] = -3.0` (drain-share → grow score) | 50,668 | 109,083 |
| dsmelon_sharp | + `gb2[7] = +6` (mix sharpness → 5x rail) | 50,647 | 109,123 |
| crewmax | `gb8[0]=gb9[:]=gb10[0]=+6` → `hire_bias≡+399/400`, `crew_target→16=MAX_HANDS` | 56,943 | 82,775 |

### What the shipped planner emits vs the tape, same board

| | d0 plant target | d5 board | d10 board | d15 board |
|---|---|---|---|---|
| **us (base)** | W11 C11 **M0** | ANI6 W11 S7, 1 empty | ANI16 W15 S18 C1, **0 empty**, q2, $4,856 | ANI18 W23 S18 **M12**, 4 empty, q3, $9,551 |
| **tape 107448662** | **M12** W7 | ANI6 **M12** W7, 0 empty | ANI13 **M12** S20 W5, 0 empty, q2, $2,666 | ANI17 S33 W24, 0 empty, q3, **$27,548** |

Melon tiles by day — us `0×11, 4, 7, 7, 10, 12, 13…` (first tile **d11**); them `12` on d1-d10, **0 from d11**
(the pot). Our melon reaches the shed d21-26 (18/18/6/18/12/6 units). Their d11→d15 cash swing is
+$24.9k against our +$4.7k, and **we still win the board 81,014-75,924** — the pot is a tax we
repay after d15, exactly as `2026-09-10-topb-loss-anatomy-g1000.md:46-48` and
`2026-09-10-livec63-loss-anatomy.md:21-30` say (d10-14 is −22k on boards we win *and* lose).

## 1. Decision classes, ranked by coins in the ledger

Verdicts: **(a)** reachable, ES has not found it · **(b)** reachable only with a constant/switch
change · **(c)** unreachable by construction.

### C1 — the d0 melon corner (12 tiles, dumped d10) · 14.1k, 69/88 decisive
Path: `brain.py:658-661` `w = softmax(grow[:N_CROPS] * (1 + sig(head[7])*4))` → `:714` `absorb`
→ `:726` `plant_target = _largest_remainder(w, plant_total)`. Genes: `grow` = `scores[:,0]`
(`brain.py:572`), i.e. `(h @ w2 + b2) + drain_feat @ ds` (`policy.py:407`).

**Verdict (a) — reachable, and I reached it with one theta coordinate.** Wall-audit-B W4
(`2026-09-10-planner-wall-audit-B.md:70-73`) says a proportional split over a **clipped** score
cannot corner. That mechanism is wrong: the mix softmax reads the **raw** `grow` (`brain.py:661`);
`GROW_MAX` clips only `grow_mult` at `brain.py:754`, which is the *valuation* `budget.grant` prices
with, one stage later. `ds` (`policy.py:208`, shape `(2, 2)`) is an unbounded linear path from the
drain features onto that raw score, and melon's `share` is *pinned* at `-DRAIN_CLIP = -4`
(`brain.py:205, 256`) while every other crop sits in (−0.2, +1.2) — a ready-made melon-only lever.
Setting `ds[1,0] = -3.0` moved melon from **0 tiles in the whole season** to 2 by d2, 6 by d4,
8 at d10, 23 by d16, with `grow_mult[MELON]` on the 1024 rail from d1. **"0/16,800 decisions"
describes the incumbent theta, not the planner's envelope.**

Caveat, and it matters: **d0 itself stayed melon-0 in all four arms**. On d0 nothing is planted
anywhere, so `share` is not yet saturated and the melon-only lever has no signal. Reaching the
*day-0* corner needs a different coordinate (a `w1`/`w2` combination reading `prod_feat`), which I
did not test — d0 corner reachability is **unproven either way**, and is the one open question here.

Profitability: catastrophic on this board (50,668 vs 81,014), the opponent gaining +33k. That
reproduces `MELON_OPEN −19,557` (`2026-09-09-verdicts.txt:980`) from *inside* the theta, which the
archive had never done. **The melon corner is not a wall; it is a bad trade.** (see §3)

### C2 — sell-lot granularity in d15-29 · the actual top-tier discriminator
Top files **389 sell rows of 3.95 u** to our **152 of 9.39 u** (`2026-09-10-livec-loss-anatomy.md`);
`2026-09-09-verdicts.txt:906` puts TOP at 9.6 rows/selling day in 5.5-unit slices. LIVE-C63 puts
**all** of the win/loss separation in d15-29 and the only surviving product is wool revenue at
constant units, ≈4.3k/board (`2026-09-10-livec63-loss-anatomy.md:69-78`).

Path: `ops.py:126` `SELL_TURNS = (3, 10, 18)`; `sell.py:44` `N_LOTS = len(O.SELL_TURNS)`.
**Verdict (c) for the row count, (b) for slice size.** No theta emits a fourth sell row: the lot
count is `len()` of a module tuple, and the policy's own `lots` head (`policy.py` `g4`) is in the
dead-mask set (`2026-09-10-planner-wall-audit-B.md:5`). A 3-row seat cannot produce 9.6 rows/day
under any theta. This is the **only genuine by-construction wall I found on a live money channel.**
Honest counterweight: the archive already swept the count — `(3,10,21) −165`, 4th row −77, 6 rows
−324, **0 flips** (`2026-09-10-planner-wall-audit.md:§2`). The sweep moved *turns*, not *slice
size*; 4 rows of 9.4 u is not the top's 9.6 rows of 5.5 u, so the family is narrowed, not closed.

### C3 — intraday buy cadence (herd) · ≈6.4k/game net
`2026-09-09-pasture-cadence.md`: all 21 of our `BUY_ANIMAL` orders are at **hour 2**; they buy at
hours 2,4,7,9,11,17,18,21. Path: `ops.py:204` `FULL_MARKET_TURNS = 3` — the day's whole market row
lives in turns 0-2, asserted against `SELL_TURNS` at `ops.py:270`. **Verdict (c)** for extra buy
rows, **(a)** for the herd size itself: my crewmax arm reached `crew_target = 16 = MAX_HANDS`
(`brain.py:806`, `spec.py:243`) so the crew rail is reachable — and it cost 24k on this board
(EMPTY tiles 30 at d10 vs 0 in base: hiring hard starves the seed budget that fills the board).

### C4 — board fill / idle owned tiles · 3.5k
`n_dev = qfloor(dev_frac · n_free)`, `dev_frac = sig(head[5] + aux[2]·n_free/25)` (`brain.py:621-622`).
`sig` ∈ (0,1) so `n_dev < n_free` **strictly**, but sup is `n_free − 1` — the cap is a gene, not a
constant. `2026-09-09-board-fill.md:64-79` attributes 99.4 % of idle tile-days to that cap.
**Verdict (a).** My base run's empty-tile curve is 0-1 through d10 then **20/10/11/8** on d11-14 —
we out-plant them everywhere except the days right after a quadrant unlocks. Note the premise
inversion on file: at d10 we plant 44.5 tiles to their 33.1 (`board-fill.md:10-31`), and on this
board d10 fill was 0 empty for both seats. This is a small, late, quadrant-3-only channel.

### C5 — land · **not a gap at all**
Audit A/B both flag `land_bias` saturated at the veto rail (`brain.py:596-598, 613`; my base run
shows `land_bias = -4000 = -land_price` from d15). But the tapes buy **2 quadrants [2..4], at
median d6 and d11**, and our lineage buys quad2 at d5 and quad3 at d10 — **we buy earlier and
more.** In the base run both seats reach q3 by d15 and we are the richer seat at d10 ($4,856 vs
$2,666). **Verdict (a), and de-prioritise:** the rail is real, its coins are not. Land is a dead end
for closing the top-tier gap, whatever the saturation table says.

### C6 — fertilizer: apply vs sell
We `FERTILIZE` 174-211 times and sell 153-210 units; they fertilize 61 and sell 342-348
(`2026-09-10-livec-loss-anatomy.md:41-51`). Path: the reservation at `plan.py` `want_feed`/
`n_fert_eff`. **Verdict (b)** — the reservation is a constant, and the archive measured the
reservation *pays* (+16.8k over 179 applications), so this is a re-pricing question, not a wall.

## 2. What the class table adds up to

Of six classes carrying real coins, **one** is unreachable by construction (C2 row count, plus C3's
buy row) and it is a fixed row schedule, not "erroneous logic". Everything else the top does is
inside the envelope — I emitted the melon line and the max crew from theta alone, and both **lost**.

## 3. Inexpressibility vs bad trade — the 94 % → 26 %

`2026-09-09-verdicts.txt:915` (band6, n=72 paired, g350): base 94.4 % → `+MELON_OPEN` 26.4 %, and
names the mechanism — hire enumeration admits over **today's** task set (`plan.py:5955-5995`),
`CROP_WINDOW_START[MELON]=6` means 12 of 19 tiles emit no task d1-5, crew collapses to 0-1.

**Decision: bad trade, not inexpressibility** — three independent reads agree.
(i) The named blocker was **built and measured**: `FORWARD_ADMIT_ON` alone −8,676 / +0−10
(`2026-09-09-switch-sweep.md:172`); with the fix in place `MELON_OPEN` got *worse* (15.3 %,
−27,397). Removing the stated cause did not restore the opening.
(ii) The **ES was handed the horizon gene and declined it**: `g11` decodes `forward_days = 0` every
day on the base theta and the ES raised the crew target to 11 by d10 instead
(`2026-09-09-plateau-review-verdicts.md:534-536`).
(iii) My dsmelon arm is the missing experiment — melon from *inside* the theta, no forced opening,
no switch — and it lost 30k while handing the tape +33k. The melon board is **displacement**:
`2026-09-09-verdicts.txt:949` measures that 70 % of the opening's cost is *denial we stop doing*.
Also on file: forced melon harvests 81 units at d10 (more than the band) but sells at 145/u vs
their 243 because our first lot stands at h11 vs their h9 — i.e. the pot's value is a **sell-row
timing** property (C2), not a planting property. The corner without their sell cadence is worthless.

## 4. Verdict

**Is the planner the ceiling? No — with one qualification.** The top tier's *board* is reachable
(C1, C3, C4, C5 all verdict (a); I emitted two of them from theta today). What is not reachable is
their **d15-29 sell cadence** (C2/C3, verdict (c)), and LIVE-C63 puts 100 % of the win/loss
separation in exactly that window. So the planner is not a wall in front of the *opening*; it is a
3-row throttle in front of the *realisation*.

**P(a theta exists in the CURRENT planner reaching LIVE-C ≈ 80 %): 10-15 %.** Reasoning, not a
ledger: today 62-68 %; the calibrated slope needs ≈81 % judge-scale for 2960; every reachable class
I can push is one the ES has already searched at scale (900 generations, and it walked *away* from
melon and toward crew); the one class the ES cannot search is C2, and C2's row-count sweep already
read level. I put most of the remaining mass on C2's **slice size** rather than on any opening.

**Single planner change with the best odds — `LOT_SLICE` (C2).** Not more rows: keep
`SELL_TURNS = (3, 10, 18)`, and split each lot's order into k sub-orders of ≤ `S` units within the
same row, so a 28-unit lot meets the quote curve as 5-6 slices instead of one block. This targets
the only ledger line that survives the LIVE-C63 controls (wool revenue at constant units,
≈4.3k/board, own-purse 70 %) and it is the top's measured signature (5.5 u/row). It is inert at
`S = COIN_CAP` by construction. It does **not** need a gene: sweep `S ∈ {4, 6, 10}` as a constant
first. Second choice, only if C2 reads level: expose `ds`/mix as a *trained* melon dimension rather
than a forced opening — but §3 says price it as a denial trade, so I would not spend the arm.

**Paired acceptance test** (existing runners, usage lines read at
`S/topb2/run.sh:2`, `S/livec/run.sh:2`, `S/live62/run.sh:2`):
```
S/live62/run.sh  slice6  <worktree>  artifacts/kagg2_games/thetas/flow172_g1000.npy \
  "OPEN_PUMP_ON=True,TAIL_FILL_ON=True,BANK_BEFORE_LOT_ON=True,HIRE_ROW_ON=True,LOT_SLICE_ON=True,LOT_SLICE_UNITS=6"
S/topb2/run.sh   slice6  ...same...      # 20 held-out top-ten tapes, both seats
S/livec/run.sh   slice6  ...same...      # 72 target-band boards
```
Accept only on: LIVE62 flip line non-negative **and** TOPB2 paired Δ > 0 with `S/bank/paired.py`
`ALL` t ≥ 2.0 **and** LIVE-C paired Δ > 0. Drawn legs veto only. Base rows for the pairing already
exist as `g940pair_*` / `g1000pair_hr_*` in `S/lossflip/`.

## 5. Dead ends recorded

* **`land_bias` saturation is not the top-tier gap.** The rail is real; the tapes buy 2 quadrants
  at d6/d11 and we buy 3 at d5/d10. Do not spend an arm on the veto arithmetic for *this* question.
* **Wall-audit-B's W4 mechanism is refuted.** The mix softmax reads raw `grow`, not `grow_mult`;
  `GROW_MAX` is not what keeps melon at zero. Any arm justified by "the clip erases the corner"
  should be re-derived.
* **Crew ceiling is not binding.** Forced to `crew_target = 16 = MAX_HANDS` and `hire_bias = +399`,
  we lost 24k and left **30 empty tiles at d10**. `HIRE_BIAS_MAX = 400` needs no widening.
* **Mix sharpness `head[7]` is inert at the margin** — `gb2[7] = +6` changed the season by 21 coins
  on top of dsmelon (50,668 → 50,647). It is already effectively saturated.
* **Instrumentation caveat**: `obs["farms"][p]` carries no roster list I could find, so hands/day
  came out 0 in the probe and I used the on-file numbers (theirs 11 at d10, ours 10) instead.
* **Single board.** Every engine number above is n=1, unpaired. It is an *envelope* read: it proves
  what the planner **can** emit, and gives only a direction on what that emission is worth.
