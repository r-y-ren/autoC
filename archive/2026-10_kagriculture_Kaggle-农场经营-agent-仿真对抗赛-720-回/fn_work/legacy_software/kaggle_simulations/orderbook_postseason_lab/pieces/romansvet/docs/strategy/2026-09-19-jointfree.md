# JOINTFREE — the two free switches cancel each other's gift, and still miss the bar

2026-09-19, master `4b081a9`. Three free coordinates were banked one at a time and all three left OFF: [[herdtilt2]]'s `brain.HERD_TILT = −1.0` (HIBAND +64 t 2.19 but **Δtheirs +65** on POOLED278, 74 % of Δours leaking), [[melonveto]]'s `MELON_VETO_FLOOD_ON` at `K = 60` (HIBAND **+0**, Δtheirs −90, wins 41→42), and [[turncost]]'s `brain.TURN_COST` — rejected **by gift**, so excluded here. The two gift-free ones were never flown together. Same switch string, same base `ship7692`, same seeds, CRN: `SW_EXTRA=,brain.HERD_TILT=-1.0,MELON_VETO_FLOOD_ON=True`. No theta column, no layout move (7,692).

## 1. The joint cell — `S/winjudge/joint_ht_mv{,_hi}/`

| leg | bds | Δmargin | se | t | Δours (t) | **Δtheirs (t)** | bett/wors | win% | flips | worst |
|---|---:|---:|---:|---:|---:|---:|---|---|---|---:|
| **HIBAND** | 56 | **+81** | 82 | +0.99 | −21 (−0.25) | **−102 (−1.89)** | 18/11 | 73.2→**75.0** | **+1/−0** | −19,542 → **−17,500** |
| BAND250 | 250 | +146 | 91 | +1.60 | +83 (1.11) | −62 (−1.49) | 133/117 | 83.6→84.4 | +3/−1 | |
| ENGINE28 | 28 | +122 | 77 | +1.58 | +129 (1.46) | +7 (0.13) | 10/3 | 35.7→35.7 | +0/−0 | |
| **POOLED278** | 278 | **+143** | 82 | **+1.74** | +88 (1.30) | **−55 (−1.45)** | 143/120 | 78.8→**79.5** | **+3/−1** (signp 0.625) | −21,442 → −21,031 |

## 2. Additivity — the margins add, the GIFT does not

HIBAND, the only leg where both singles are banked: joint **+81** vs sum **+64 + 0 = +64**, interaction **+17** — a fifth of one se. The two switches touch disjoint decisions (the d12+ crop/herd split; the post-d10 melon plant target) and the coins behave accordingly. POOLED278 has no banked `melonveto_k60` row ([[melonveto]] never earned one — its HIBAND precondition was t 0.00), so the comparison there is joint **+143** vs `HERD_TILT` alone **+23**.

**The interaction that matters is on Δtheirs, and it is a cancellation, not a sum.** `HERD_TILT` alone pays the rival **+65** on POOLED278; the joint cell pays **−55**, with **Δours identical (+88 both)** — so every coin of the +120 improvement is THEIR purse falling, not ours rising. MELONVETO's withheld melon takes back exactly the shared-curve leak [[melongift]] prices, and the pair is **gift-free on every leg** (ENGINE28 +7 is noise) where neither half was gift-free and useful at once.

## 3. Bar and the near-flip census

Gift-free **PASS** (Δtheirs ≤ 0 on POOLED278 and HIBAND). HIBAND ≥ 0 **PASS** (+81). Net win-flips > 0 **PASS** (+3/−1 = **+2** of 278; +1/−0 of 56). POOLED278 t ≥ 3 **FAIL** — **t 1.74**, se 82 on a +143 mean. Boards within **750 coins of a flip** under the joint cell: **7 of 57** POOLED278 losses (base 6) and **0 of 14** HIBAND losses (base 1) — the losses are not close, so no cheaper gate buys the remaining flips.

**VERDICT: NO SHIP** on the stated bar — but this is the strongest free-coordinate cell on the record, and the first that is gift-free, win-positive and margin-positive on **both** bands at once. `HERD_TILT` and `MELON_VETO_FLOOD_ON` stay OFF at their defaults, byte-identical and layout-free: a **pair** of ES coordinates worth +143/board and the obvious seed for a WINRATE gate. Resolving t 1.74 to t 3 needs ~2.8× the boards, not another switch. **LESSON: gift is a property of the PAIR, not of the switch** — a leaky gene can be paid for with a gene that leaks the other way.

Repro: `[LEGS=hiband] WORKERS=8 SW_EXTRA=,brain.HERD_TILT=-1.0,MELON_VETO_FLOOD_ON=True bash S/winjudge/judge.sh joint_ht_mv S/winjudge/ship7692/theta7659.npy`; additivity/near-flip reader reuses `S/winjudge/report.py`'s own BASE-row ENGINE28 keep set.
