# WOOL: why B sells 13 fewer units while holding more sheep

**VERDICT: not a sell-timing defect. We sell 100 % of what we produce with 0.0 unsold at d29; the
−5,659 splits −2,460 volume (of which ~65 % is a *wool-per-sheep-day* production shortfall, 0.930 vs
0.995/1.081) and −3,199 price, and the price half is entirely sale-DAY MIX caused by ymg_aq owning
3 sheep at d1 to our 1 (d0-9 sheep-days 10.5 vs 28.8). Lot sizing is fine (our within-day price walk
is −0.31 c/u vs their −1.80). Sale timing HAS live theta coordinates (`hold[7]`, `press[7]`) but the
measured slope is 12.7 sd per day at sigma 0.02 → NOT REACHABLE.**

Tools: `S/wool_mech/{timeline,decomp,split,slope}.py`. Sources: `S/topledger3/raw_B.npz` (12 games =
6 ymg_aq boards × 2 tape seats, engine-validated to the coin, `2026-09-14-top5-ledger.md` §1) and
`S/melon_decomp/raw_B.npz` (68 band-clone games, TOPB2 40 + LIVE-C 28). All figures coins or units
per game, sim-descriptive. `produced` = `Δsold + Δshed` from the dawn snapshots.
## 1. The gap, decomposed (deliverable 1)

| | vs **ymg_aq** (12 g) | vs **band clone** (68 g) |
|---|---:|---:|
| wool units sold, ours / theirs | 121.67 / 134.67 (**−13.00**) | 116.59 / 147.44 (**−30.85**) |
| wool revenue, ours / theirs | 21,501 / 27,160 (**−5,658**) | 16,309 / 19,273 (**−2,964**) |
| realised price, ours / theirs | 176.7 / 201.7 (**−25.0**) | 139.9 / 131.0 (**+8.9**) |
| volume term (ΔU × p̄) | **−2,460** | **−4,135** |
| price term (Δp × Ū) | **−3,199** | **+1,171** |
| **unsold shed at END** | **0.00 / 0.00** | **0.00 / 0.32** |
| season produced = season sold? | **yes, exactly (121.67 = 121.67)** | **yes (116.59 = 116.59)** |

**(a) later sheep arrival — YES, and it is the whole early story.** Season sheep *bought* is the
same (6.50 vs 6.67; both first buy on d0), but arrival is front-loaded for them: sheep at
d1/d5/d10/d20 = ours 1.0/1.0/2.8/6.5, theirs 3.0/3.2/3.8/5.8. d0-9 sheep-days 10.5 vs 28.8
(clone 11.1 vs 20.2). No sheep is ever sold back by either seat (0.00 units both).

**(b) unsold / late residue — NO at end, small in transit.** End shed 0.00/0.00. Mean shed latency
(days a produced unit waits before sale) ours **0.95** vs theirs **0.42** (clone 0.98 vs 0.61).
Priced against a sell-on-production-day counterfactual at the day-open quote:
our latency costs **−483 coins/game** (ymg) / **−1,294** (clone); theirs costs −250 / −1,079.
**Net latency disadvantage ≈ −233 (ymg) / −215 (clone) coins/game — 4 % and 7 % of the line.**

**(c) lot timing into a glutted price — NOT lot SIZE, only sale DAY.** Splitting the −25.0 c/u price
gap into the day-open benchmark (which day we sold on) vs the within-day walk down the quote curve:
**MIX −26.5 c/u, WALK +1.5 c/u.** Our lots walk the book down *less* than theirs (−0.31 vs
−1.80 c/u). Lot sizing is not the defect — on the clone set the walk term is +3.9 c/u in our favour.

**(d) lower per-unit price — YES, and it is a consequence of (a).** `mkt_inv` never restocks
(`state.prices_of` is a pure table lookup on absolute market inventory, `spec.build_price_table`), so
wool price is a shared, one-way declining pot. Mean day-open wool quote over the 12 ymg_aq games:
d6 **219**, d10 190, d14 138, d17 108, **d19-21 79**, d25 117, d29 142. ymg_aq gets 23.3 units away
in d0-9 at a realised 206 before the pot gluts; our first 5.0 units land on d7 and 107.8 of our 121.7
units arrive in d15-29 into the 79-142 trough.

**The unit gap is mostly production, not arrival.** Two-factor split `U = sheep-days × wool/sheep-day`:

| | sheep-days ours/theirs | wool per sheep-day ours/theirs | sheep-day term | **yield term** |
|---|---:|---:|---:|---:|
| ymg_aq | 130.8 / 135.3 | **0.930 / 0.995** | −4.48 u | **−8.52 u (65 %)** |
| band clone | 125.2 / 136.4 | **0.931 / 1.081** | −12.01 u | **−18.85 u (61 %)** |

Our 0.930 / 0.931 is the same number against both opponent classes — the B-side constant the ledger's
"same sign against both classes" was pointing at.

### Per board (ours / theirs), 6 ymg_aq boards × 2 seats

| episode | sheep d5 | sheep d10 | sheep d20 | units | realised price | wool rev gap | end shed |
|---|---|---|---|---|---|---:|---|
| 108790159 (×2) | 1/3 | 2/3 | 5/3 | 77/72 | 89/142 | −3,373 | 0/0 |
| 108806291 (×2) | 1/3 | 2/3 | 3/3 | 69/75 | 127/160 | −3,231 | 0/0 |
| 108807563 seat0 | 1/4 | 7/8 | 18/16 | 362/352 | 240/239 | **+2,498** | 0/0 |
| 108807563 seat1 | 1/4 | 7/8 | 18/17 | 364/382 | 237/238 | −4,511 | 0/0 |
| 108814574 (×2) | 1/3 | 2/3 | 3/3 | 53/63 | 65/122 | −4,238 | 0/0 |
| 108820106 (×2) | 1/3 | 3/3 | 6/3 | 80/63 | 42/122 | −4,368 | 0/0 |
| 108826138 (×2) | 1/3 | 1/3 | 4/6 | 88/168 | 228/225 | **−17,733** | 0/0 |

End shed is 0 on every board and every seat. The pooled −5,658 is carried by 108826138 (−17.7k, a
pure volume loss: 88 vs 168 units at the *same* price) and by the price gap on the four small boards
(42-127 vs 122-160) where we hold *more* sheep at d20 and still realise half the price.

## 2. Mechanism: where the missing wool/sheep-day is

`spec.py:84` — SHEEP: cost 500, PASTURE, `FIRST_YIELD_DAY 6`, `INTERVAL 3`, `MAX_HELD 6`, product WOOL.
`sim/eod.py:115-147 refresh_animals`: a sheep fires when `(day+1 − t_day − 6) % 3 == 0`, and
`new_yield = min(6, t_yield + 1 + bonus)` where `bonus = t_bank` **only if fed that day**, and
`t_bank += 1` on each day the animal was **cared and fed** (`t_cared == 1 and t_water == 1`).

So the per-fire increment is **1 + care-bank**, the bank is ≤ 3 over a 3-day interval, and the ceiling
is **4 units / 3 days = 1.333 wool per sheep-day** (hard cap `held/interval = 2.000`).
We run **0.930 (70 % of the achievable ceiling)**; ymg_aq 0.995 (75 %), the clone 1.081 (81 %).
Closing to the ceiling on our existing 130.8 sheep-days is **+53 units ≈ +9,319 coins** at our own
realised price — **UNVERIFIED**, ignores our own price impact and the extra hand-turns it costs.
A sheep bought on day d also produces nothing until d+6, which is why our d10-15 herd ramp yields
0.424 wool/sheep-day in d10-14 against their 0.781, and why late sheep meet the d19-21 price trough.

**The lever this points at is the daily CARE + FEED cadence on pasture tiles (hand labour), not the
sell path.** It is a production-side lever and is out of this leg's scope; the herd-growth screen
closed *acquisition*, not *care*.

## 3. Decoder trace: who decides WHEN wool is sold (deliverable 2)

Path: `policy.forward` (policy.py:632) → `brain.decide` (brain.py:904) →
`hold = qfloor(0.8 · BASE · unit_ratio(sell))` (brain.py:1108) and
`press = qfloor(BASE · max(tanh(gate), 0))` (brain.py:1110) → `plan._plan_and_stats`
(plan.py:5902; `avail` = dawn shed only, 6606-6615; `hold` at 6623; `SELL.allocate` at 6639) →
`sell.allocate` (sell.py:100) → `plan._market` emits `MO_SELL` (plan.py:8118-8125) →
`market.process_slot` (market.py:611), `ncap = min(n, shed_have)` (market.py:669).

* **Per item, not aggregate.** `hold`, `press`, `avail`, `lots` are all `[9]`/`[3,9]`.
* **No wool-specific rule exists anywhere** — no per-item threshold, priority, min-lot or price floor.
  The only item-specific sell rules are wheat feed reservation (plan.py:6605-6608), fertilizer
  reservation (6613-6615) and switch-OFF melon/strawberry caps.
* **Lot size has no parameter at all.** `sell.allocate` is a 100-round unit-by-unit greedy; a unit is
  taken iff `best_adj >= hold[p]` (or `hold[p] <= LIQUIDATE`). Quantity is emergent.
* **Sale turns are hardcoded**: `O.SELL_TURNS = (3, 10, 18)` (ops.py:126), `SELL.N_LOTS = 3`
  (sell.py:44), `EARLY_SELL_LOT1_TURN = 1` (ops.py:159). The one head that could have emitted a lot
  count, **`g4`/`gb4` (4254-4286), is DEAD** (policy.py:621, masked at policy.py:730-731).
* **Day gate: only the terminal day.** `plan.py:6624` substitutes `SELL.LIQUIDATE` on day 29.
* `BANK_BEFORE_LOT_ON` (ON) appends banked DROP units in bulk to lot 1 / turn 10 (plan.py:6841-6842);
  `TAIL_FILL_ON` (ON) deliberately excludes HARVEST (plan.py:2593-2596) and moves no sell row.

**Live theta coordinates that reach wool's sale decision** (`N_PARAMS = 7020`), none wool-specific:

| block | indices | reaches |
|---|---|---|
| `w1` 0-2303, `b1` 2304-2367 | encoder | both |
| `w2` col 1 — odd offsets in 2368-2495 (64) | | `hold` |
| `b2[1]` 2497 | | `hold` |
| `w3` 4189-4252, `b3` 4253 | | `press` |
| `dh` 4386-4513, `ds[.,1]` 4515/4517 | drain | both / `hold` |
| `fh` 4980-5491, `fs[.,1]` 5493-5507 (8) | forecast | both / `hold` |
| `mh` 6789-6852, `ms[0,1]` 6854 | momentum | both / `hold` |

`press` is one-sided (`max(tanh·,0)`), so theta can bias wool **earlier within a day** but never
explicitly later; "later" only via raising `hold` until the lots refuse the unit.

**Note / correction:** `2026-09-14-melon-reachability.md` §8 is about a day-0 melon **plant** gene
(`cm,cb`, 6855-7019), **not** a sell-day gene. `cm,cb` has no path into `hold` or `press`.

## 4. Measured slope at training sigma (deliverable 2)

`S/wool_mech/slope.py`, 12 ymg_aq games, antithetic full-block Gaussian draw over the 65-coord HOLD
block (`w2` col 1 + `b2[1]`), seed 20260914, ‖z‖ = 9.40, ‖Δθ‖ = 0.188 at sigma 0.02.
**Identity gate PASSED: the zero-offset arm reproduces `raw_B` to 0 coins** (max |Δ| = 0, margin
−13,722 exactly).

| arm | margin | wool units | wool rev | shed latency (d/u) | **mean wool sale day** |
|---|---:|---:|---:|---:|---:|
| base (B) | −13,722 | 121.67 | 21,501 | 0.952 | **20.790** |
| hold **+**0.02 | −13,934 | 120.50 | 21,047 | 0.949 | 20.707 |
| hold **−**0.02 | −14,462 | 125.50 | 22,006 | 0.964 | 20.865 |

Antithetic slope **0.079 day per sd at sigma 0.02** → **12.7 sd to move the mean wool sale day by one
day**; ≈ **25 sd at sigma 0.01** (linear extrapolation, UNVERIFIED).
Latency slope 0.0075 d/u per sd → **71 sd at sigma 0.02** (≈142 at 0.01) to close the 0.53-day
latency gap to ymg_aq. Both are far outside the ≤5 sd reachability bar.

**→ Wool sale TIMING: NOT REACHABLE at training sigma. Wool LOT SIZE: no coordinate exists at all.**

### Smallest gene append that would make sale day reachable

Worth only ~−233 coins/game on this evidence, so it is **not recommended**; specified for the record.
Append `hb` shape `(9,)` at offsets **7020-7028** (`N_PARAMS` 7020 → 7029; every existing theta stays
a prefix and `policy.pad` zero-fills it). Decode in `brain.decide` immediately after brain.py:1108:
`hold[p] = qfloor(0.8·BASE_p·unit_ratio(sell) + clip(1500·hb[p], −BASE_p, +BASE_p))`.
Gain 1500 is chosen so that **1 sd at sigma 0.01 = 15 coins of hold**, which is one day of the
observed d15-29 wool price drift (79→142 over 10 days, ~10-15 c/day) — i.e. **≈1 sd per day of sale
shift**, ~250× the current slope. Per the gene-slope rule this must be re-measured before launch.
A `press` two-sided fix (relu at brain.py:1110) only buys the within-day lot index — worth nothing.

## 5. Section 3 (paired CRN sell-side screen) — SKIPPED (time box)

The §4 run is the only paired evidence collected. Both HOLD perturbations **lost** margin on the 12
paired ymg_aq games (−13,934 and −14,462 vs −13,722), consistent with B being a local optimum in the
sell block. This is diagnostic only; per the two-purse rule it is not promotion evidence.

## 6. What this closes and what it opens

* **CLOSED — wool sell timing / lot sizing as the −5,659 cause.** Residue 0.00, walk term in our
  favour, latency worth −233 coins/game, and the timing slope is 12.7 sd/day.
* **CLOSED — "sheep bought late produce wool that is never sold."** Every unit is sold; the late
  sheep produce *less* (`FIRST_YIELD_DAY 6`) and sell into the d19-21 price trough.
* **OPEN — wool per sheep-day 0.930 vs a 1.333 ceiling** (`refresh_animals` care-bank). 65 % of the
  unit gap, identical against both opponent classes. A hand-labour/care-cadence question.
* **OPEN — d0-9 sheep arrival** (10.5 vs 28.8 sheep-days at the same season sheep count). This is the
  acquisition side; the herd-growth screen closed *mid-game growth*, not *day-0/day-1 ordering*.
