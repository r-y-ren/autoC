# MELONHYBRID3 (2026-09-27 23:18Z - 2026-09-28 ~00:55Z, box clock): the idle-h0, h1-cash-gated two-kernel bot

**Verdict: SHIP-CANDIDATE on the BAND leg only: +11 flips (+6 on JC1-faithful seats), GATE2 band branch A PASS on all and faithful
seats, B PASS on all seats only. Costs: ZERO -4 (gate false positive), V -3 (idle hour, small gift dtheirs t 2.3). Not a package: the
GATE2 legs beyond the band (dev100, held100, FRESH300, tapes50, faithful59) and the gift rule are the follow-up agent's.**  Gated bot on BAND142 (73 seats measured by the gated harness, 38/38 overlap byte-identical to the
cell rows, 41 seats from those cells, 28 V seats not reached in the time box = base row): **W 91 -> 102, flips +23/-12 = +11, dours +1.3k
(t 1.0), dtheirs -6.0k (t -4.8), soft dth +70.2 (z 3.28); JC1-faithful n112: +13/-7 = +6, dtheirs -2.2k (t -3.75), soft dth +61.5
(z 2.62), band A PASS / B fail.**  By family: MELON 14 -> 32 (+18), V 70 -> 67 (-3, idle-hour cost; dtheirs +495 t 2.3 = small gift),
ZERO 5 -> 1 (-4, the gate's false positive), OTHER 2 -> 2.

## Design
- Step 0 (d0 h0): our seat emits the engine no-op `{"farmer":["PASS"],"hands":[],"market":[]}` on every seat (no hands exist at h0).
- Step 1 (d0 h1): latch `rival money in the obs <= 2,550`. With OUR h0 idle it fires on MELON 49/51, V 0/81, ZERO 7/7, OTHER 0/3
  (same as MELONHYBRID2's PFS-h0 measurement; rival h1 money differs by a few coins only).
- Fired -> V56 kernel (`S/v56leg/main.py`, Apache-2.0 public notebook) for the whole game; unfired -> PFS for the whole game.
- **Harness finding 1 (V56 needs its h0 row).** Plain cell A (V56 first called at step 1, its h0 row never played) is broken: the h0 row
  is the feed-wheat pump (BUY_PRODUCT WHEAT 20 / SELL WHEAT 15 / BUY_SEED WHEAT 1). Without it the d0 herd is unfed (our sheep at d10
  1 vs 5-8 under V56-from-h0) and the game collapses (n29: W 2, dours -50k t -11.6, dtheirs +23k t 3.4 vs PFS). Fix `v56h1m`: at step 1
  the kernel is called on the h1 obs relabelled step 0/hour 0 (its h0 row), then on the real step-1 obs; our step-1 market = h0 rows +
  h1 rows (3 + 7 = 10 = engine cap `maxMarketOrdersPerTurn`, 51/51 seats exactly 10, none truncated), farmer/hands from the h1 call.
  Smoke 2/2 ~ V56-from-h0 (80,861/81,236 vs 80,868/81,230; 128,661/26,573 vs 130,755/18,766). d1-dawn melon tiles 12 on 49/51 (10 on 2):
  the melon seed orders fill.
- **Harness finding 2 (PFS plans its d0 at h1).** `pfsh1`: on day 0 PFS is shown the obs with hour-1/step-1, so its d0 plan is built at
  our h1 as its dawn and played one hour late (plan row h-1 at hour h; d0 row 23 lost; `ROUTE_VRP` step-0 init fires at real step 1).
  Checked on a V seat: step 1 = BUY_PRODUCT WHEAT 53 + 4 HIRE, step 2 = SELL WHEAT 48 + seeds + animals (PFS's h0/h1 rows).
- Harness: `S/melonhybrid3/hybrid.py` (= S/melonhybrid2 runner + modes v56h1, v56h1m, pfsh1, pfsh1n, gated; S/bandleg1 harness:
  BAND142 tapes, orig seat, pinned seed+town, SAFETY_S 1e9, REPAIR_MS 1e7, actTimeout 600, master src = vrp12_pfs). No src edit.
  Controls: `off` = pfv1 2/2 and `v56all` = bandfamily1 v56 2/2 byte-identical (highfrequencyf, kuengo).

## Cells (vs PFS = S/bandleg1/res/pfv1.csv; vs V56 = S/bandfamily1/res/v56.csv, V56 from h0)

| cell | seats | n | W | PFS W | V56 W | flips vs PFS | dours vs PFS (t) | dtheirs vs PFS (t) | flips vs V56 | dours vs V56 (t) | dtheirs vs V56 (t) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A `v56h1` (plain, KILLED) | MELON | 29 | 2 | 5 | 16 | +1/-4 = -3 | -50,228 (-11.6) | +23,103 (3.4) | +1/-15 | -56,098 (-9.5) | +42,329 (7.8) |
| A' `v56h1m` | MELON | 51 | **32** | 14 | 31 | **+21/-3 = +18** | +5,574 (1.9) | **-16,613 (-5.7)** | +1/-0 | -2,070 (-0.8) | +2,738 (1.0) |
| B `pfsh1` | V (first 20 of pfv1) | 20 | 17 | 17 | 5 | +1/-1 = 0 | +1,659 (1.1) | +414 (0.8) | +13/-1 | +11,672 (8.2) | -2,360 (-0.9) |
| B `pfsh1` | ZERO | 7 | 3 | 5 | 1 | +1/-3 = -2 | -6,251 (-3.4) | +2,434 (1.8) | +2/-0 | +15,408 (4.7) | +8,817 (3.6) |
| B `pfsh1` | OTHER | 3 | 2 | 2 | 0 | 0 | -481 (-0.6) | +349 (0.3) | +2/-0 | +7,662 (1.5) | +1,830 (0.5) |
| C `v56h1m` | ZERO | 7 | **1** | 5 | 1 | +1/-5 = -4 | -21,671 (-5.6) | -6,372 (-1.9) | 0 | -12 | +12 |

JC1 faithful rows (`S/judgeclean1/pair_faith.py`, units basis from kept replays for MELON, cash proxy elsewhere):

| cell | ALL | FAITHFUL |
|---|---|---|
| A `v56h1` vs PFS | n29 W 5->2, -3, dours t -11.6, dtheirs t +3.4, soft dth -33.0 | n22 W 2->0, -2, dtheirs +37.3k t +12.8 |
| A' `v56h1m` vs PFS | n51 W 14->32, **+21/-3 = +18**, dours +5.6k (1.85), dtheirs -16.6k (-5.74), soft t +4.69, soft dth +96.9 (z 4.50), band A+B PASS | n29 W 6->17, **+12/-1 = +11**, dours -0.6k (-0.32), dtheirs -10.0k (-6.91), soft t +3.73, soft dth +91.8 (z 3.43), band A+B PASS |
| A' `v56h1m` vs V56-from-h0 | n51 W 31->32, +1/-0, dours -2.1k (-0.79), dtheirs +2.7k (+0.99) | n25 W 12->12, 0, dours +0.4k, dtheirs -54 |
| B `pfsh1` V+OTHER vs PFS | n23 W 19->19, +1/-1, dours +1.4k (1.00), dtheirs +405 (0.90), soft t -0.93 | n21 W 17->17, +1/-1, dours -5, **dtheirs +668 (t +2.26)**, soft t -1.63 |
| C `v56h1m` ZERO vs PFS | n7 W 5->1, +1/-5, dours -21.7k (-5.60), soft dth -22.1 | n3 W 2->0, -2 |

- A' is the V56 kernel's MELON record reproduced (32 vs 31, 0 flips lost vs V56) from an idle h0: the gate costs V56 nothing.
- A' breakage share (vs PFS): 66 % of the sum of dtheirs sits on unfaithful seats; on faithful seats the rival still loses 10.0k (t -6.9)
  and we gain +11 flips -> real denial, not breakage (compare MELONHYBRID2 hybrid (c): faithful 0/18, dtheirs +30k).
- B: the idle hour costs PFS nothing measurable on V (0 flips, dours +1.7k t 1.1); faithful dtheirs +668 (t 2.26) is a small rival gain
  (the rival's h0 wheat pump fills against an empty book) = the one gift sign in the stream; soft t -1.63 (a BAND sub-family, not a GATE2 leg;
  flagged for the gift rule on the follow-up legs). pfsh1b not triggered (V lost 1 of 20 < 3); pfsh1n (unshifted) not run.
- C: the gate's false positive: ZERO seats (7/7 fire) go to V56 = 1/7 (PFS 5/7): -4 flips, dours -21.7k. This is the whole cost.

## Projection and the measured gated bot on BAND142
Projection (res/projection.md, res/faith_proj_band.txt; fired -> A'/C row, unfired -> B row where measured else pfv1):
`n142 W 91 -> 105, flips +23/-9 = +14, dours +945 (0.80), dtheirs -5,912 (-4.88), soft t +2.77, soft dth +71.0 (SE 21.6, z 3.29), band A+B PASS;
FAITHFUL n113 W 77 -> 86, +13/-4 = +9, dtheirs -2,473 (-4.38), soft t +2.28, soft dth +61.8 (z 2.70), band A+B PASS` -> >= +6 faithful: gated cell run.

Measured gated bot (`HY_MODE=gated`, res/gated_all.csv; assembled res/gated_band.csv, res/gated_band.md, res/faith_gated_band.txt):

| rows | n | W PFS -> gated | flips | dours (t) | dtheirs (t) | soft t | soft dth (z) | GATE2 band |
|---|---|---|---|---|---|---|---|---|
| gated harness only | 73 | 47 -> 52 | +12/-7 = +5 | +1,718 (0.93) | -5,839 (-3.37) | +1.42 | +68.6 (2.11) | A PASS, B fail |
| gated harness only, faithful | 59 | 40 -> 43 | +7/-4 = +3 | -192 (-0.29) | -2,011 (-2.31) | +1.31 | +78.6 (2.31) | A PASS, B fail |
| BAND142 assembled | 142 | 91 -> **102** | **+23/-12 = +11** | +1,252 (1.04) | -5,972 (-4.79) | +2.49 | +70.2 (3.28) | A PASS, B PASS |
| BAND142 assembled, faithful | 112 | 76 -> 82 | **+13/-7 = +6** | -632 (-1.07) | -2,226 (-3.75) | +1.72 | +61.5 (2.62) | A PASS, B fail |

| family | n | fired | PFS W | gated W | flips | dours (t) | dtheirs (t) | rows |
|---|---|---|---|---|---|---|---|---|
| MELON | 51 | 49 | 14 | **32** | +21/-3 = +18 | +5,644 (1.9) | -16,560 (-5.8) | 23 gated + 27 A' + 1 base (unfired, not reached) |
| V | 81 | 0 | 70 | 67 | +1/-4 = -3 | +532 (1.3) | +495 (2.3) | 47 gated + 7 B + 27 base (not reached) |
| ZERO | 7 | 7 | 5 | 1 | +1/-5 = -4 | -21,671 (-5.6) | -6,372 (-1.9) | 3 gated + 4 C |
| OTHER | 3 | 0 | 2 | 2 | 0 | -481 (-0.6) | +349 (0.3) | 3 B |

- The measured gate fired exactly as specified (MELON 49/51, V 0/81 in the reached rows, ZERO 7/7, OTHER 0/3).
- The V cost grew from 0 (first 20 V seats) to -3 flips on 54 V seats (all near-ties: pfsh1 dours +532/seat, dtheirs +495 t 2.3): the
  idle hour is not free on V; 27 V seats are unmeasured (base row = 0 cost assumed; at the measured rate ~ -1.5 more flips).
- The -5 / -7 losses split: ZERO 5 (gate false positive), V 4 (idle hour), MELON 3 (V56 kernel's own losses vs PFS wins).

## Mechanism
- MELON rivals spend their d0 purse at h0 (herd, hires, some melon seed: rival h1 money <= 2,550 on 49/51); V rivals open with the V56
  wheat pump (~2,857 left); ZERO rivals also buy herd + hires at h0 (fires 7/7).
- PFS's h0 spend (1,602 coins) was what broke the MELONHYBRID2 handover. Idling h0 leaves 3,000 coins, so the V56 kernel's open-loop d0
  (5 hires, 2 cows, 2 sheep at h1, 12 melon seeds d0 h6-h17) fills exactly as from h0 once its h0 feed-wheat row is merged into step 1.
- PFS planning its d0 at h1 is ~free on V seats: its d0 plan executes one hour late and loses only d0 row 23.
- ZERO seats are the cost: V56 is 1/7 there (it is the same 1/7 from h0), PFS 5/7. A sharper gate (e.g. a second latch on
  rival h1 hires/animals, visible fields) would keep them on PFS: ZERO rivals hire 3.9 at h0 vs MELON 2.2 (MELONHYBRID2 Q1) - untested.

## Packaging notes (not built)
- V56 is Apache-2.0 (Kaggle public notebook, attribution block preserved in the file); `S/v56leg/main.py` is 1.06 MB and would ship as a
  second kernel module next to our package. exec/import cost 0.18 s (measured, box loaded) -> load at module import, not at step 1.
- runtime.py would need: (1) step 0: return the no-op on every seat (before `Runtime.act`, so no PFS state is touched); (2) step 1: latch
  `obs.farms[1-player].money <= 2,550` once per game (per player key); (3) V56 branch: call the kernel on a deepcopy of the h1 obs with
  step=0/hour=0, then on the real obs, concatenate markets (cap 10), return; thereafter forward every step unchanged (the kernel keeps its
  own per-seat state; it resets on step==0 or step going backwards, so the relabelled call is its game start); (4) PFS branch: on day 0
  (hour >= 1) pass PFS a copy of the obs with hour-1 and step-1 (step 0 init of ROUTE_VRP/PROGRAM_ENGINE then runs at real step 1); from
  d1 h0 pass-through; (5) both kernels behind the existing never-raise wrapper (V56 already falls back to PASS on exceptions).
- Turn budget (1 s): V56 3.0 ms mean/step, max 426 ms (median game max 70 ms); PFS 11.4 ms mean, max 512 ms (median game max 388 ms);
  the step-1 double V56 call is ~2x a normal V56 step. Both are inside the 1 s actTimeout; the per-game overage bank is untouched.
- Follow-up agent (GATE2 legs beyond the band, docs/PIPELINE.md §3): dev100, held100, FRESH300, tapes50, faithful59 with the gated
  harness (HY_MODE=gated), plus the gift rule over the reacting legs (watch the pfsh1 V faithful dtheirs t +2.26) and a live-ZERO check.

## Files
S/melonhybrid3/{run.sh, hybrid.py, sum.py, proj.py, gatedband.py, addunits.py, diff0.py, checkpoint.txt},
res/{ctl_*, v56h1_melon*, v56h1m_melon*, v56h1m_zero*, pfsh1_*, gated_all*, gated_band.csv, projection.md, proj_band.csv, sum_*.md, faith_*.txt}.
Replays: S/melonhybrid3/gz/<arm>/ (not committed if large).
