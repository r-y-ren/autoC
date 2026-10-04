# OPP_SUPPLY_ON on PINNED boards, paired vs candidate B — REFUSED (2026-09-11T15:33Z)

T1 of `docs/strategy/2026-09-11-b-toptier-ledger.md` (consensus §54): re-test
`OPP_SUPPLY_ON` (`src/kagg3/core/plan.py:1507`, `OPP_SUPPLY_SCALE`:1511,
`OPP_SUPPLY_PATH`:1517) on pinned-town boards, because the read that closed it in
September was taken on drawn boards. **Verdict: REFUSED, and the mechanism it was
predicted to move does not move.**

## 1. Prior reads (archive, per the archive rule)

| read | boards | result |
|---|---|---|
| `2026-09-04-verdicts.txt:275` / `2026-09-09-verdicts.txt:275` (stream A, 2026-09-05) | band6@777001, **drawn** | scale 1.0 −2,972 t −3.8; scale 0.5 −3,616 t −4.8, dose-responsive |
| `2026-09-09-switch-sweep.md:34,119` | **pinned** HELD42 / LEG20 / LOSS12 | +617 t +2.54 (+6 flips/−0), LEG20 +47, LOSS12 −733 — "worth one confirmation leg" |
| `2026-09-09-verdicts.txt:1337` (COMP167) | 55 live boards | flow167_g150+pair +OPP_SUPPLY 52.7 % +3,360 vs 50.9 % +3,391 — +1 flip, margin level → "DEAD on live boards" |
| `2026-09-10-verdicts.txt:16` / consensus §2 | review | counted among the reactive-market losers |

The drawn −3k is indeed voided by `tape-fidelity-2026-09-11`. The HELD42 +617 is the
claim under test here; it does not survive.

## 2. Screen (S/oppsupply/run.sh, S/oppsupply/pair.py)

Theta = candidate B (`flow193_g100_hr`), shipped `hr` switch string plus
`OPP_SUPPLY_ON=True,OPP_SUPPLY_PATH=artifacts/opp_supply/S_pop.npy,OPP_SUPPLY_SCALE=s`
(the `S/fertcow/run.sh` append pattern). Curve loads: `S_pop.npy` is (720, 9) float32,
mean 0.32 u/turn. Paired cell-by-cell against B's own baselines
`S/simscreen/{topb2_40.csv,full120.csv}`; `shopdiff 0/160` everywhere, so every pair is
the same board with the same shop stream.

| arm | n | Δ margin | t (cells) | honest unit | Δ (honest) | t | W/L | win % | dours | dtheirs |
|---|---|---|---|---|---|---|---|---|---|---|
| scale 0.5 / TOPB2 | 40 | −430 | −2.64 | 20 tapes | −430 | −1.94 | 6/13 | 32.5 → 32.5 | −326 | **+103** |
| scale 1.0 / TOPB2 | 40 | −752 | −3.10 | 20 tapes | −752 | −2.26 | 4/16 | 32.5 → 32.5 | −543 | **+209** |
| scale 2.0 / TOPB2 | 40 | −3,166 | −4.19 | 20 tapes | −3,166 | −2.95 | 4/16 | 32.5 → 25.0 | −2,352 | **+814** |
| scale 0.5 / LIVE-C | 120 | −251 | −2.05 | 60 tapes | −251 | −1.46 | 32/26 | 71.7 → 68.3 | −381 | −130 |
| scale 1.0 / LIVE-C | 120 | −444 | −2.34 | 60 tapes | −444 | −1.66 | 28/32 | 71.7 → 71.7 | −587 | −143 |
| scale 2.0 / LIVE-C | 120 | −3,986 | −9.73 | 60 tapes | −3,986 | −6.87 | 9/51 | 71.7 → 58.3 | −1,927 | **+2,059** |

Decision rule from the brief: **REFUSED** — TOPB2 Δ ≤ 0 at every scale (and the 20-board
t at scale 2.0 is −2.95 ≤ −2.5). Monotone in the dose on both files, in the losing
direction, which is the same shape the drawn band6 legs reported; the pinned boards do
not reverse it, they only shrink it at small scale.

Two-purse split: at the doses that matter our purse falls and **theirs rises**
(TOPB2 +103 / +209 / +814). That is the handed-back signature of
`counterfactuals-overstate`, not denial.

## 3. Mechanism (S/topledger, 40 TOPB2 boards, B vs scale 0.5)

The ledger predicted their d15-29 realised c/u on our loss boards falling 80 → 65.

| seat / boards | B c/u | +OPP_SUPPLY c/u | Δ | B rev | arm rev | Δ | units |
|---|---|---|---|---|---|---|---|
| theirs / all 40 | 75.5 | 75.6 | +0.1 | 88,363 | 88,465 | +102 | 1,170.7 → 1,170.7 |
| theirs / 27 loss | 80.2 | 80.2 | **−0.0** | 94,770 | 94,751 | −19 | 1,181.4 → 1,181.4 |
| theirs / 13 win | 65.4 | 65.7 | +0.3 | 75,055 | 75,408 | +353 | 1,148.5 → 1,148.5 |
| ours / 27 loss | 96.5 | 96.4 | −0.1 | 102,538 | 101,808 | −730 | 1,062.2 → 1,056.0 |

**The predicted signature does not appear.** Their late c/u on the loss boards is
unchanged to a tenth of a coin and their late revenue moves 19 coins in 94,770; on the
boards we win it *rises*. All of the movement is on our own row: 6 units and 730 coins
off our late book. The forecast is priced into OUR lot sizing only, and the opponent
seat is an action tape whose SELL rows are fixed, so the single available channel is the
shared price — and pulling our own lots back hands that price to them. M2 stays real as
a description of the gap, but this switch is not an instrument for it.

## 4. Ledger animal-column fix (Task B)

`S/topledger/ledger.py:101` counted `st.occ == spec.N_CROPS + a`; `sim/units.py:227`
writes `new_o = pa = arg - spec.I_GOOSE`, the **bare** animal index (0-2), so the test
never matched and every animal column in the 2026-09-11 ledgers read 0. Fixed to
`st.occ == a` (the `animal` mask already restricts to KIND_COOP/KIND_PASTURE, so a bare
index cannot collide with a crop's). `ledger.py` only; `git diff --stat src/` stays empty.

Herd, 40 TOPB2 boards, ours | theirs (B, re-run):

| kind | d10 | d15 | d20 | d29 |
|---|---|---|---|---|
| GOOSE | 3.00 \| 2.45 | 3.38 \| 3.05 | 3.33 \| 3.05 | 3.08 \| 3.05 |
| COW | 6.50 \| 7.08 | 6.55 \| 7.42 | 6.47 \| 7.22 | 6.10 \| 6.62 |
| SHEEP | 5.90 \| 5.38 | 6.78 \| 6.08 | 6.78 \| 6.22 | 3.58 \| 4.62 |

We run ~0.6-0.9 more geese and ~0.6-0.9 more sheep than the top tier all game, and
**0.6-0.9 fewer cows** from d10 on; both herds shed sheep into d29 and theirs keeps more
cows to the end. The one animal line where the top tier is ahead the whole way is the
cow, which is the seat of the open fertilizer/milk item (−7.3k/game, LOSS10 note) — the
herd half of that question is now readable and the cow count is the thing to test, not
the sheep. The arm at scale 0.5 changes the herd by ≤0.35 animals anywhere (cows
6.47 → 6.28 at d20), confirming it is a pure sell-schedule lever.

## 5. Files

`S/oppsupply/{run.sh,pair.py}`, logs `S/oppsupply/os_s{05,10,20}_{topb2,livec}.log`,
boards `S/simscreen/os_*.csv`, ledgers `S/topledger/topb2_{B,os05}.npz`,
herd readout `S/topledger/herd.py`.
