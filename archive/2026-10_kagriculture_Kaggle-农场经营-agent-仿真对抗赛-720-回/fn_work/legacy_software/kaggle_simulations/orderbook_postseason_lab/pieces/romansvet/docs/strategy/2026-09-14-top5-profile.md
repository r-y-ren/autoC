# Top-five profile and B's standing against it — 2026-09-14

Snapshot: `S/ladder2/snapshot_20260914T0611Z/` (leaderboard pulled 2026-09-14T06:12:05Z,
credential-free `S/ladder2/fetch.py`; `receipt.json` sha256-verified by
`S/ladder2/summarize_snapshot.py`). New pulls for this study (episode lists for the three
untaped top-five teams + two replays) are under `S/ladder2/top5_20260914/`
(`receipt.json` there, pulled 2026-09-14T07:2xZ). B = sub **56161192** (flow193_g100_hr),
rank **165**, **2767.3**, 415 games, 270-145 (65.1 %).

## 1. Current top ten (2026-09-14T06:12Z) and form

Form = that submission's own ListEpisodes (pulled 07:2xZ for the top five only).

| # | team | submission | score | games | W-L | WR | last 40 | mean opp (40) |
|---|---|---|---:|---:|---|---:|---:|---:|
| 1 | Majkel1337 | 56156662 | 3204.4 | 302 | 258-44 | 85.4 % | 24/40 (60 %) | 3072.9 |
| 2 | SpaTaro | 56114097 | 3021.1 | 543 | 339-204 | 62.4 % | 20/40 (50 %) | 3015.9 |
| 3 | ymg_aq | 56209769 | 3012.5 | 137 | 101-36 | 73.7 % | 24/40 (60 %) | 2971.1 |
| 4 | DSM | 56204618 | 3010.9 | 156 | 135-21 | 86.5 % | 29/40 (72.5 %) | 2952.3 |
| 5 | Mengfei Li | 56173067 | 2996.6 | 326 | 204-122 | 62.6 % | 18/40 (45 %) | 2969.9 |
| 6 | Artem The Farmer 🍅 | 56201964 | 2994.8 | — | — | — | — | — |
| 7 | Orbital Terraformer | 56212726 | 2983.0 | — | — | — | — | — |
| 8 | HowardLeeTW | 56202668 | 2974.2 | — | — | — | — | — |
| 9 | Otter Vibe | 56097405 | 2970.0 | — | — | — | — | — |
| 10 | feel the agi | 56132899 | 2965.3 | — | — | — | — | — |

Cutoffs: **rank 10 = 2965.3, rank 5 = 2996.6, rank 1 = 3204.4** (the §119 reading
"cutoff 2952 ± 15 FLAT, rank 5 3020" still holds; no drift in three days).

### Churn since 2026-09-11

The ten names the task lists as the 09-11 top ten do not reproduce in any snapshot on
disk (our 09-10 TOPB2 cut and the 09-12/09-13 snapshots disagree with it); treat that
list as UNVERIFIED. Measured churn from snapshots we hold:

| list | members still in today's top ten |
|---|---|
| task's 09-11 list | SpaTaro (2), Mengfei Li (5). binghua → 14 (2939.3), THUNDER THUNDER → 41, kaggricodex → 94, Ad Space Available → 724, 自己找差距 → 453, AI是我的豆包 → 719, JustinLee → 1473; Matthew Huang absent from today's board |
| our TOPB2 cut (09-10 top ten) | SpaTaro, Mengfei Li, Otter Vibe (9), feel the agi (10). Himanshu Kumar → 1852, mtmr_s1 → 778, kanno → 758, Yusuke Hayashi → 532, Unknown Mother-Goose → 1245 |
| 09-12T1508 snapshot top ten | 6 of 10 survive; charmq → 609, THIRD FARM CLUB → 57 |

**Caveat that explains most of the collapses:** a leaderboard row carries one submission
per team, and most of those teams have uploaded a *newer* submission that is still
climbing from its placement rating (Himanshu Kumar's row today is sub 56219901 at 1756.5,
not the 3000-rated file we taped). The old files are not weaker — they are off the board.
So "who fell out" is not evidence of strength change.

**Genuinely new at the top:** ymg_aq (3), DSM (4), Orbital Terraformer (7), HowardLeeTW (8).
Majkel1337 has led every snapshot since 09-12 and is **183 points clear of rank 2** —
a single outlier file, not a band.

## 2. Tape coverage and B's paired result vs each top-five file

Judge families searched: TOPB2 (`S/topb2/chosen.json`, 20 tapes of the 09-10 top ten,
2953-3081), NEXTHIGH (`S/nexthigh/boards.csv`, 30 tapes 2782-2946), NEXT30
(`S/nextband/boards.csv`, 2567-2750), LOSS10 (`S/bloss/`, 2175-2381). 104 tapes mapped.

| top-5 team | pinned tape? | episodes | B paired (rows = 2 tapes × 2 seats) | mean margin | B live meeting |
|---|---|---|---|---:|---|
| Majkel1337 | **no** | — | — | — | 1 game, **L**, −18,314 (ep 108740598, 2026-09-14T01:48Z, vs their *other* sub 56216119 rated 2778) |
| SpaTaro | **yes**, TOPB2 | 107465299, 107460204 | **2W-2L** (+5,749/+6,549 on 107465299; −907/−907 on 107460204) | **+2,621** | none |
| ymg_aq | no | — | — | — | none |
| DSM | no | — | — | — | none |
| Mengfei Li | **yes**, TOPB2 | 107466012, 107460216 | **2W-2L** (+146/+146 on 107460216; −5,403/−5,403 on 107466012) | **−2,628** | none |

B has **never met a ≥2900 opponent live** (max opponent rating in its 415 games: 2848.6).
The only live top-ten data point is the Majkel1337 loss, and that was against Majkel's
second, still-placing submission, not the 3204 file.

Context legs for B (per-board csvs in `S/lossflip/`, `S/bloss/`):

| leg | opponents | boards | B rows | B wins | mean margin |
|---|---|---:|---:|---:|---:|
| TOPB2 | 2953-3081 | 20 | 40 | 13 (32.5 %) | −1,654 (sd 13,370, SE 2,114) |
| NEXTHIGH | 2782-2946 | 30 | 60 | 32 (53.3 %) | +2,045 |
| NEXT30 | 2567-2750 | 30 | 60 | 41 (68.3 %) | +3,957 |
| LOSS10 | 2175-2381 | 10 | 20 | 1 (5.0 %) | −3,160 |

TOPB2 broken out by team (4 rows each): feel the agi +20,887 (2W), SpaTaro +2,621 (2W),
mtmr_s1 +2,281 (2W), kanno +1,860 (2W), Himanshu Kumar −705 (2W), **Mengfei Li −2,628 (2W)**,
Otter Vibe −4,731 (1W), Yusuke Hayashi −6,204 (0W), binghua −11,246 (0W),
Unknown Mother-Goose −18,674 (0W).

## 3. Build class of each top-five file

Classifier = the §118 two-means split on 23 z-scored d0-10 build columns
(`S/nexthigh/anatomy.py`, `CLUSTER_COLS`), refit here on the 100 profiled tapes
(`S/nexthigh/anatomy_opp.csv`): cluster 0 "band clone" n=78 (fert applied 74, fert sold 341,
sell rows 250), cluster 1 "fertilizer engine" n=22 (fert applied 171, fert sold 219,
sell rows 156). New rows were profiled from freshly pulled replays and assigned by nearest
centroid; `S/ladder2/top5_20260914/anatomy_new.json` holds the full rows.

| team | evidence | class |
|---|---|---|
| Majkel1337 | `docs/strategy/2026-09-11-majkel-vs-spataro.md` (6 games profiled): six-product wheat/strawberry/melon/milk/wool/fertilizer, 12 melon d0-2 dumped d10, 11 hands d10, 187 fert units sold, tomato 4.5k, 244 sell turns; beats SpaTaro on the **cost** side (buys 151 wheat units vs SpaTaro's 397) | **fertilizer engine**, cost-optimised variant |
| SpaTaro | both TOPB2 tapes → cluster **1** (`S/nexthigh/anatomy_cluster.csv`) | **fertilizer engine** |
| ymg_aq | replay ep 108826138 (seat 0, win 116,345-107,072): fert applied 156, fert sold 250, sell rows 181, 11 hands d10, **43 strawberry tiles by d10 and only 7 melon**, 11 cows / 10 sheep. Nearest centroid = 0, distance 100.3 — **beyond 96 % of the 100 fitted tapes** (fitted median distance 3.3, p90 55.5) | **neither** — engine-level fertilizer with a strawberry-first opening; a third build |
| DSM | replay ep 108818990 (seat 0, loss 99,623-99,942): fert applied 153, fert sold 193, sell rows 302, 11 hands d10, **8 hires on d1**, **102 carrot tiles by d29**, 12 melon d10. Nearest centroid = 0, distance 95.6 — also beyond 96 % of fitted tapes | **neither** — engine-level fertilizer, clone-level selling, carrot-heavy late |
| Mengfei Li | both TOPB2 tapes → cluster **1** | **fertilizer engine** |

The §118 statement "2780-2950 = band clone, fertilizer engine only at 2953+" survives, but
**the top of the board has moved past both classes**: 2 of the 5 (ymg_aq, DSM) sit outside
either cluster, one game each (n=1 per team) — UNVERIFIED as a stable class until more of
their games are profiled.

## 4. What rating and what paired margin B needs

B's fitted strength (P(win)=σ((c−opp)/s), s = 298 pts/logit [182, 686], `S/ladder2/refresh.md`):

| window | WR | mean opp | c (s=298) | c (s=182) | c (s=686) |
|---|---:|---:|---:|---:|---:|
| last 40 | 67.5 % | 2738.8 | **2957** | 2872 | 3240 |
| last 60 | 61.7 % | 2724.5 | 2866 | 2811 | 3051 |
| last 100 | 56.0 % | 2719.9 | **2792** | 2764 | 2885 |
| last 200 | 57.0 % | 2697.4 | 2781 | 2749 | 2891 |

B's displayed rating is still climbing (2663 → 2722 → 2709 → 2767 at g−200/−100/−40/now);
the last-40 c is a 40-game estimate and swings ±100. Take **c ≈ 2790-2870** as the working
range. Gaps, and coins at §115's conversion (**+100 rating ≈ +2,000 pooled band coins**;
t = 2 at ±436 coins ≈ 27 rating):

| target | rating | gap from c≈2792 | pooled band coins | gap from c≈2866 | coins |
|---|---:|---:|---:|---:|---:|
| rank 10 | 2965.3 | +173 | ≈ **+3,500** | +99 | ≈ +2,000 |
| rank 5 | 2996.6 | +205 | ≈ **+4,100** | +131 | ≈ +2,600 |
| rank 1 (Majkel1337) | 3204.4 | +412 | ≈ +8,200 | +338 | ≈ +6,800 |

Measured directly against the top tier instead of via rating: on TOPB2 (2953-3081, the
same band as today's top five) B wins 32.5 % at −1,654 coins/board. A **uniform shift of
+2,471 coins/board** takes B to the 45.5 % TOPB2 rate the 09-11 refit ties to the 2956
cutoff; **+2,517** takes it to 50 %; **+2,716** to 50.5 % (rank-5 scale). These are the
same order as the rating-based numbers and are the number to quote for a candidate:
**about +2,500 coins/board against 2953+ opponents**, versus the ±436 coins that is one
t = 2 step on the 90-board band pool.

## 5. Softest and hardest of the top five

- **Softest: SpaTaro (rank 2, 3021.1).** B is 2W-2L at **+2,621 coins/board** on its two
  pinned tapes — the second-best team margin in the whole TOPB2 leg — and SpaTaro is the
  only top-five file that is *not* improving: 543 games, 62.4 % lifetime, **50 % over its
  last 40** at mean opponent 3015.9, rating flat at 3016.5. It is also the class we have
  the most measurement on (`2026-09-11-spataro-vs-ours.md`, `2026-09-11-majkel-vs-spataro.md`).
- **Hardest: Majkel1337 (rank 1, 3204.4).** 183 points clear of rank 2, 85.4 % lifetime and
  still 60 % over its last 40 against a 3072.9 mean opponent; no pinned tape; the single
  live meeting was a **−18,314 loss** against its weaker second submission. It needs
  ≈ +8,200 pooled coins from B — 3-4× the top-10 requirement.
- Of the two with tapes, **Mengfei Li is the harder** (−2,628/board vs SpaTaro's +2,621)
  and is also the slowest of the five (45 % over its last 40) — its rating is falling
  toward B's reach on its own.
- DSM is the strongest *trend* (86.5 % lifetime, 72.5 % last 40) and ymg_aq the second
  (73.7 %, 60 % last 40); both are new builds outside our clusters and both are **untaped**,
  so B's margin against them is unmeasured. UNVERIFIED.

## 6. Recommendation

1. **Cut tapes for ymg_aq (56209769), DSM (56204618) and Majkel1337 (56156662) and extend
   TOPB2 into a TOPB3 at today's 2965-3204 band.** Three of the current top five are
   invisible to every judge family we own, and two of them are build classes the §118
   anatomy has never seen. The dl/cut recipe is `S/nexthigh/dl.sh` + `cut_one.sh`
   (replays at `https://www.kaggleusercontent.com/episodes/<ep>.json`); their episode lists
   are already on disk in `S/ladder2/top5_20260914/`.
2. **Training/judge target = the SpaTaro-class fertilizer engine at 2950-3050**, judged on
   the refreshed TOPB3 with the +2,500 coins/board bar. It is the only top-five class where
   B already reads positive (+2,621), the class Majkel1337's cost edge is built on top of,
   and the class the 2965 cutoff is made of (SpaTaro, Mengfei Li, Otter Vibe, feel the agi).
3. Keep the band legs (NEXT30/NEXTHIGH) as the incumbent promotion gate — B is +2,045 to
   +3,957 there and that is what the 2767 → ~2860 climb is currently paying for — but stop
   treating TOPB2 as "confirm only": at 32.5 % it is now the binding constraint, and the
   gap it measures (+2,500 coins/board) is the whole remaining distance to rank 10.
