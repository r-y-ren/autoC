# §117 — What the 2780-2950 opponents ARE, and what that means for the objective

2026-09-12. Answers the §116 question left open (`docs/strategy/2026-09-12-nexthigh.md`): the
2780-2950 band is where the 2700 → 2967 climb actually happens, and nothing told us whether those
teams are the **mistake-free band clone** of §99 (`2026-09-11-nextband-anatomy.md`) or the
**fertilizer-and-mixed-crop engine** of §114 (`2026-09-12-transfer-mechanism.md`).

Tools: `S/nexthigh/anatomy.py` (`opp` / `cluster` / `band` / `report`), adapted from
`S/nextband/anatomy.py` — same opponent profiler, same pinned-town band decomposition, plus a set
registry that profiles any tape family with a replay on disk and a two-means split on the build
columns. Outputs: `S/nexthigh/{anatomy.md, cluster.md, anatomy_opp.csv, anatomy_cluster.csv,
anatomy_band_B.csv}`.

**What was measured.** 100 opponent tapes profiled from their own recorded games (that team's own
seat): NEXTHIGH 30 (2782-2946), NEXT30 30 (2567-2750), the 20 in-sample top-ten training rungs
(`S/topb2/insample_ids.txt`, TOPTEN) and the 20 held-out TOPB2 (2953-3081). Plus B against all 30
NEXTHIGH pinned-town tapes, both seats, `st.money` scanned per day.

---

## 1. The build table by band — NEXTHIGH is the band clone, not the top-tier engine

Means over each family's tapes (full 69-column table, per half, in `S/nexthigh/anatomy.md §1/§3`):

| column | NEXT30 (n=30)<br>2567-2750 | **NEXTHIGH (n=30)**<br>**2782-2946** | TOPTEN (n=20)<br>2843-3081 | TOPB2 (n=20)<br>2953-3081 |
|---|---:|---:|---:|---:|
| hires d0 | 5.0 | **5.0** | 5.3 | 5.5 |
| hands at d10 | 11.0 | **11.0** | 11.2 | 11.1 |
| melon tiles by d10 | 11.8 | **12.0** | 12.1 | 12.1 |
| carrot tiles by d10 | 0.1 | **0.0** | 1.1 | 0.7 |
| tomato tiles by d10 | 0.0 | **0.0** | 1.5 | 0.3 |
| wheat tiles by d29 | 157.8 | **159.4** | 134.3 | 142.8 |
| carrot tiles by d29 | 30.8 | **30.0** | 40.4 | 32.9 |
| tomato tiles by d29 | 1.3 | **2.3** | 6.5 | 5.8 |
| **FERTILIZE ops** | 68.3 | **79.4** | **127.5** | **128.4** |
| fertilizer units bought | 46.3 | **54.4** | 46.8 | 47.9 |
| fertilizer units sold | 340.3 | **337.3** | 281.1 | 271.4 |
| melon units sold | 72.0 | **72.0** | 78.0 | 76.5 |
| melon units after d14 | 2.8 | **0.0** | 14.1 | 18.0 |
| sell rows (turns with a SELL) | 251.1 | **250.2** | 198.9 | 194.3 |
| PASS rate % | 7.0 | **7.5** | 9.6 | 10.0 |
| units sold, all | 1,549 | **1,582** | 1,637 | 1,589 |

Every §114 signature of the top tier — 128 fertilize ops, 41 carrot / 6 tomato plants, a broad late
liquidation with melon still moving after d14 — is **absent** at 2780-2950. NEXTHIGH sits on the
band-clone side of every one of them: 79.4 fertilize ops (11 above NEXT30, **49 below** the top
tier), 30.0 carrot and 2.3 tomato tiles (vs the clone's 31/1 and the engine's 40/6), **zero** melon
units after d14 (the clone's one-lump d10 dump, exactly), 250 sell rows (vs the engine's ~195), and
the clone's byte-identical opening: **30/30 NEXTHIGH teams hire 5 on d0, hold 11 hands at d10,
plant exactly 12 melon by d10 and sell exactly 72 melon units, all first sold on d10**
(`anatomy.md §1` modal-share table: 100 % on all four columns, both halves).

### The one real gradient inside the band
Unlike NEXT30 (§99: largest |t| = 1.43, *below* the noise maximum), NEXTHIGH does move with rating,
in the direction of the engine but nowhere near it (Pearson r with rating over 30 boards, |t| ≥ 3.4
is the multiplicity-corrected bar):

| column | r | t |
|---|---:|---:|
| wheat **units sold** | +0.605 | **+4.02** |
| **FERTILIZE ops** | +0.565 | **+3.62** |
| wheat **tiles** by d29 | −0.563 | **−3.60** |
| animals bought | +0.509 | +3.13 |
| tiles planted by d29 | −0.488 | −2.96 |
| fertilizer units sold | −0.482 | −2.91 |

So the 2865-2950 half fertilizes more (97.6 ops vs 71.6 in the 2782-2865 half) and pushes the same
wheat through fewer tiles. It is the clone **starting to lean** toward the engine, not the engine:
97.6 ops is still 31 short of TOPTEN's 127.5, and carrot/tomato d10 are **0.0/0.0** in both halves.

## 2. The cluster — one build owns the whole band, and it is not the top tier's

Two-means on 23 z-scored build columns (opening / mix / herd / liquidation, **no money**), 200
restarts, over all 100 tapes (`S/nexthigh/cluster.md`, `anatomy_cluster.csv`):

| cluster | n | rating range | mean rating | families |
|---|---:|---|---:|---|
| **0 — band clone** | 78 | 2567-3000 | 2796 | NEXT30 29, **NEXTHIGH 30**, TOPB2 10, TOPTEN 9 |
| **1 — fertilizer engine** | 22 | 2577-3081 | 2972 | NEXT30 1, **NEXTHIGH 0**, TOPB2 10, TOPTEN 11 |

Centres (raw units): fertilize ops **74.3 vs 170.7**, fertilizer sold **340.6 vs 218.8**, sell rows
**249.6 vs 156.1**, tomato d29 **1.5 vs 10.8**, carrot d10 **0.0 vs 1.8**, tomato d10 **0.0 vs 1.7**,
wheat d29 **158.5 vs 122.5**, melon units **71.8 vs 82.1**, PASS % **7.1 vs 12.2**. The split
explains 23.1 % of the build variance.

**All 30 NEXTHIGH tapes land in cluster 0 — the band clone. Zero land in the engine cluster.** The
engine cluster is a 2953+ phenomenon and even there it is only half the population (TOPB2 10/20,
TOPTEN 11/20); the other half of the top tier is the clone too, and Himanshu Kumar (3000.4) and
feel the agi (2985.9) are clone-cluster teams. The 2967 cutoff is therefore *not* a build boundary.

## 3. Which band decides B's NEXTHIGH games

B vs all 30 pinned-town tapes, both seats averaged (`S/nexthigh/anatomy_band_B.csv`,
`anatomy.md §2`); win % 53.3 reproduces the engine leg's 53.3 % exactly.

| slice | n | d0-9 | d10-14 | d15-29 | margin d29 | win % |
|---|---:|---:|---:|---:|---:|---:|
| ALL | 30 | +2,825 | **−22,257** | **+21,674** | +2,242 | 53.3 |
| upper 2865-2950 | 9 | +3,090 | −22,460 | +20,695 | +1,324 | 55.6 |
| lower 2782-2865 | 21 | +2,712 | −22,170 | +22,093 | +2,635 | 52.4 |
| B's 16 WINS | 16 | +2,969 | −22,414 | **+28,002** | +8,556 | |
| B's 14 LOSSES | 14 | +2,661 | −22,077 | **+14,442** | −4,974 | |
| win − loss | | +308 (t +0.80) | **−337 (t −0.53)** | **+13,560 (t +6.29)** | | |

Correlation with the final margin: d0-9 **+0.087**, d10-14 **−0.118**, d15-29 **+0.984**.

**The d15-29 band decides every one of B's 14 NEXTHIGH losses.** The shape is the §99 shape,
sharper: the d10-14 melon pot is a flat tax paid identically on wins and losses (−22,414 vs
−22,077, t −0.53) while the d15-29 recovery separates them by +13,560 at t +6.29. All 14 losses are
listed in `anatomy.md §2`; the per-board "decisive band" column reads d10-14 on 14 boards purely
because the tax is the largest *absolute* number, but it carries no information (r −0.118) — the
discriminator is the recovery, 14.4k on losses against 28.0k on wins.

### Does B's d29 dump (the §114 mechanism) fire here? Yes — and it earns less
Day-29 money change, from the same per-day ledger:

| set | our d29 | their d29 | **d29 margin** | on B's wins | on B's losses | d25-29 net |
|---|---:|---:|---:|---:|---:|---:|
| NEXTHIGH (2782-2946) | +9,938 | +9,748 | **+190** | +995 | −730 | +3,132 |
| NEXT30 (2567-2750) | +9,596 | +8,787 | **+809** | +1,329 | −404 | +4,594 |

The dump fires — B still books ~9.9k on the last day and the opponent's own last-day liquidation is
the same one-lump carrot/wheat event §114 describes. But against NEXTHIGH the **net** of that
exchange is +190/board against +809 on NEXT30, and it is *negative* (−730) on the boards B loses:
the same weapon, aimed at the same product, against a clone with less slack in it.

---

## 4. The three answers

### (i) Build class of the 2780-2950 band
**The mistake-free band clone of §99, with a measurable lean toward the engine and no trace of its
signature.** 30/30 hire 5 on d0, 11 hands at d10, 12 melon tiles, 72 melon units first sold on d10,
**0.0 melon after d14**; 79.4 fertilize ops (engine 128), 0.0 carrot and 0.0 tomato tiles by d10
(engine 1.1/1.5), 2.3 tomato by d29 (engine 6.5), 250 sell rows (engine 195), PASS 7.5 % (engine
10). The two-cluster split puts **30/30 of them in the clone cluster and 0 in the engine cluster**;
the engine cluster is 21/22 TOPB2+TOPTEN tapes. Inside the band, fertilize ops rise with rating
(r +0.565, t +3.62) — the clone is drifting engine-wards, and at 2865-2950 it is at 97.6 ops, still
31 short.

### (ii) Which band decides B's NEXTHIGH games
**d15-29, decisively and exclusively.** r 0.984 with the final margin; wins +28,002 vs losses
+14,442 (Δ +13,560, t +6.29). d0-9 (+2.8k, r +0.09) and the d10-14 melon pot (−22.3k, r −0.12,
win−loss t −0.53) are flat taxes paid on every board. This is the same reading as NEXT30 (§99) and
as §54's top-tier loss anatomy — one mechanism, three rungs.

### (iii) Implication for the objective
**A band-only arm (W2 / LIVEC42 / BAND40 / NEXT30) trains against the right build for the
2750-2950 climb. NEXTHIGH does not need to enter the objective as a training family** — and if it
did, it would **not** reintroduce the §114 transfer, because the transfer is a *build* difference
and NEXTHIGH does not have the build.

* The objective flow212 keeps (band clone, one d29 carrot/wheat liquidation, no fertilizer engine)
  is a byte-match for what 2782-2946 plays: 30/30 clone-cluster, melon gone by d14, 79 fertilize
  ops, 2.3 tomato tiles. Training on 2350-2750 clones and being judged at 2780-2950 is **not** an
  extrapolation across build classes; it is the same class with the execution noise removed (§99)
  plus ~11 fertilize ops.
* The §114 transfer was a trade between *fertilizer-engine* opponents (128 ops, 41 carrot, 6 tomato,
  broad late liquidation through **milk**) and *band clones* (62-68 ops, 31 carrot, 0-1 tomato, one
  d29 **carrot/wool** lump). Its cost was paid because softening `press` cancelled B's d29 dump into
  the clone's own liquidation. NEXTHIGH liquidates through the **clone's** products (0.0 melon after
  d14, 337 fertilizer units sold, 30 carrot tiles) and B's d29 dump against it is worth **+190/board
  net and −730 on the boards B loses** — i.e. weighting NEXTHIGH would push in the *same* direction
  as LIVEC42/NEXT30 (keep the d29 dump, keep `press`), not against them. There is no second
  liquidation product to fight over, so no fixed-`press` conflict, so no transfer to reintroduce.
* What NEXTHIGH *is* worth is a **judge column**, exactly as §116 staged it: it is the only rung
  whose opponents are the clone-with-no-slack at the rating where the cutoff sits, and its
  d15-29 decomposition (r 0.984) is the cleanest statement anywhere that the remaining margin is a
  d15-29 price/allocation problem — the half of the game the trained blocks (`gp`, `w3`, `b3`, `dh`)
  already control.
* Caveat on the ceiling: this argument covers the climb to ~2950. **Above 2953 the population is
  half engine** (TOPB2 10/20, TOPTEN 11/20), so an objective that never sees the engine is fit for
  the 2700 → 2950 climb and explicitly **not** for the tier above it. If the ladder projection
  needs 2967+, the engine answer is still owed — but it is owed *after* the band-only arm, not
  instead of it.

---

## Caveats
* One recorded game per team (n = 1 per opponent column); the per-team value carries that game's own
  board luck, and the recorded game was against *that team's* opponent, not us, so absolute money is
  not comparable between teams — only build shape is.
* NEXTHIGH's replay reconstruction leaves a residual: `max |recon_err| = 500` on NEXTHIGH, 518 on
  TOPB2, 200 on TOPTEN (NEXT30 was 0). That is ≤ 0.5 % of a game's revenue and does not touch the
  action-derived columns (hires, tiles, animals, ops, sell rows), only the reconstructed per-product
  sell revenue on a handful of boards.
* TOPTEN ratings are the team's *current* leaderboard rating where we still hold it, with the rung
  table's opponent rating as fallback; they label rows only and never enter the split or the
  cluster.
* §2's band decomposition is the pinned-town sim (99.5 % of the engine on pinned towns), not the
  engine leg. Its win rate (53.3 %) reproduces the engine leg (`S/lossflip/nexthigh_B.csv`, 53.3 %)
  exactly; the engine csv remains the number of record.
* The cluster is unsupervised k = 2 on 23 columns; it explains 23.1 % of the build variance, which
  is what a two-way split of a mostly-one-family population looks like. The finding that matters is
  the *assignment* (NEXTHIGH 30/0), which is unanimous and does not depend on k.
