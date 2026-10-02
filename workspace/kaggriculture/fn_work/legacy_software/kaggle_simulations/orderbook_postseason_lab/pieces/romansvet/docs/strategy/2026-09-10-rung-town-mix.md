# Is the ES training population's town draw representative of the live ≥2300 boards?

**Verdict: yes — representative, and if anything tilted *toward* the losing towns, not away from them.
No re-weighting is warranted.**

Inputs: 147 pinned rungs + weights from `2026-09-11-launch_flow180.sh` (127 w2, 20 w3; the only `=0`
keys are the four synthetic archetypes — flow172's rung set is identical). Towns from
`S/band2100p/town_schedules.json` (343 rows × 8 unlocks). Judges `S/livec/ids.txt` (63; 24 L / 39 W per
`provenance.txt`), `S/topb2/ids.txt`, `S/live62/ids.txt`. Overlap train ∩ LIVE-C63 = **0**; ∩ LIVE62 = 7.

**Sink index** = FM + YARN − ICE_CREAM − SMOOTHIE (anatomy-B). Product sinks = Σ `SHOP_CONSUME`
(`spec.py:192`, single-product ×2) × remaining days; validated — L/W ratios match anatomy-B's
`towncons` to three digits (TOMATO 0.630 vs 170/270; MILK 1.272 vs 391/307). Kish SE on weighted means.

## 1. Sink index — training sits on the loss side of the live pool

| set | n | sink ± SE | sink (d3/d6/d9 only) | share sink ≤ −1 |
|---|---|---|---|---|
| **TRAIN147 (weighted)** | 147 | **−0.41 ± 0.16** | −0.32 ± 0.11 | **0.497** |
| TRAIN w3 block (20 fresh top-ten) | 20 | −0.70 ± 0.43 | −0.50 ± 0.28 | 0.550 |
| **LIVE-C63 (the live ≥2300 draw)** | 63 | **+0.00 ± 0.26** | −0.14 ± 0.17 | 0.476 |
| LIVE-C63 LOSSES | 24 | −1.12 ± 0.38 | −0.79 ± 0.21 | 0.750 |
| LIVE-C63 WINS | 39 | +0.69 ± 0.31 | +0.26 ± 0.22 | 0.308 |
| TOPB2 | 20 | −0.40 ± 0.43 | −0.05 ± 0.23 | 0.450 |

TRAINw − LIVE-C63 = **−0.41 ± 0.31 (t −1.34)**; − LOSS24 = +0.71 ± 0.41 (t +1.74); − WIN39 =
−1.11 ± 0.35 (t −3.14). Training is level with the live pool, sits **closer to the losing boards than
the winning ones**, and w3 pushes it a further 0.35 that way. The hypothesis — a prior tuned to towns
we win — is falsified in sign.

## 2. Shop-kind frequencies — no significant difference

Mean unlocks/board; t = TRAINw vs that column. BRUNCH/PET_CAFE/PIZZA omitted — all |t| ≤ 0.93 everywhere. LIVE62 sink −0.29 ± 0.27, TRAIN w2 block −0.35 ± 0.17.

| shop | TRAINw | LIVE-C63 | t | LOSS24 | t | WIN39 | t |
|---|---|---|---|---|---|---|---|
| BAKERY | 0.87 | 1.08 | −1.55 | 1.00 | −0.76 | 1.13 | −1.50 |
| FARMERS_MARKET | 0.98 | 1.03 | −0.34 | 0.71 | +1.59 | 1.23 | −1.31 |
| ICE_CREAM_SHOP | 1.10 | 1.06 | +0.23 | 1.46 | −1.28 | 0.82 | **+1.99** |
| SMOOTHIE_SHOP | 1.20 | 0.98 | +1.47 | 1.25 | −0.24 | 0.82 | **+2.26** |
| YARN_STORE | 0.90 | 1.02 | −0.82 | 0.88 | +0.17 | 1.10 | −1.06 |

Contingency χ² (raw counts, df 7): TRAIN147 vs LIVE-C63 **4.76, p 0.69**; vs LOSS24 5.10, p 0.65;
vs WIN39 11.51, p 0.12; vs TOPB2 6.71, p 0.46; vs LIVE62 3.19, p 0.87. KL(TRAINw ‖ LIVE-C63) =
**0.007 nats** — the real signal, LOSS24 vs WIN39, is χ² 13.92 (p 0.053), KL 0.060, **9× larger**.
Unlock days match (worst gap FARMERS_MARKET 14.2 vs 12.7, t 1.46); TRAINw TOMATO sink 31.0 vs pool
33.9 (t −0.97), again loss-side.

## 3. What this closes, and what it does not

The 343-row pool is near-uniform (χ² 13.2 df 7, p 0.067; a mild SMOOTHIE 0.142 / ICE 0.136 excess that
training inherits and the live pool shares). **The losing towns are a per-board draw the theta must
survive, not a hole in the training population** — the sink index explains ~17 % of margin variance
*within* a set whose mean the ES already trains on.

**No `--rung-weight` change is proposed.** For the record: 72 of 147 rungs have sink < 0, so even a 4:1
tilt (w4 on sink < 0) moves the weighted mean only to −1.32 — the LOSS24 mean exactly, but by then the
training population is a 25 %-win caricature of a 62 %-win draw, and rung-weighted abs/gate records
(`train.py:5807`) get nominated off the loss tail. If more low-sink signal is wanted, add **rungs** (n),
not weight (w): the binding SE is LIVE-C63's own 63 boards, not the mix.
