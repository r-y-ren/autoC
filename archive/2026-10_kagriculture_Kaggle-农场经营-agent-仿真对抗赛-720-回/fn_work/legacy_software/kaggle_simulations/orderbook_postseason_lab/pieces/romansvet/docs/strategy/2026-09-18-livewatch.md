# LIVEWATCH — the live ladder of 56313436 (FT2+ENDROUTE) read game by game, and every loss replayed under the ESR upload candidate

2026-09-18 05:45-06:10Z, research only, branch `livewatch` (worktree off `stack5` 17eaf2b), no `src/`
change, no default flip, no tarball, no merge. Episode lists pulled credential-free
(`EpisodeService/ListEpisodes`, the POST of `S/kaggle/watch_sub.py`); replays from
`kaggleusercontent.com/episodes/<id>.json` (983 MB, scratchpad only, never committed).
New leg `S/livewatch/` (32 boards); rows `S/lossflip/{ship,esr}_livewatch.csv`.

## 1. The two live submissions at 05:46Z

| sub | uploaded | games | W-L | rate | first loss | r@20 | r@40 | now (peak) | max opp met |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|
| **56313436** FT2+ENDROUTE (master `c6da7f0`) | 09-17 ~20:50Z | **100** | **68-32** | 68.0 % | g12 | 2,051 | 2,168 | **2,254.4** (2,281) | 2,360 |
| 56298246 FT2 | 09-17 ~07:15Z | 175 | 124-51 | 70.9 % | g14 | 1,672 | 2,007 | **2,231.9** (2,232) | 2,313 |

Win rate by opponent rating (the `2026-09-17-liveband.md` §4 bands):

| opp band | 56313436 | 56298246 |
|---|---|---|
| <1,900 | 13-1 (92.9 %) | 26-5 (83.9 %) |
| 1,900-2,050 | 6-1 (85.7 %) | 26-8 (76.5 %) |
| 2,050-2,220 | 26-15 (**63.4 %**) | 64-36 (64.0 %) |
| 2,220-2,400 | 23-15 (**60.5 %**) | 8-2 (n=10) |

Reading against `2026-09-17-ratingpath.md`: the new sub's **first 20 games landed it at 2,051** vs FT2's
1,672 — a much better draw (first loss g12 vs g14, but 13 of its first 20 wins came against 1,900+ seats),
and it reached 2,254 in **100 games / 9 h** where FT2 needed 175 games / 22 h for 2,232. It is now the
higher-rated of the two and it is the one being fed 2,220-2,360 opponents (38 of its 100 games; FT2 has
seen 10). Both are in the **flat-step regime** (±4-5/game): the last 30 games read 16-14 for 56313436 at a
mean opponent 2,244 and 24-6 for 56298246 at a mean 2,120 — i.e. the two subs are the same strength
sampled at different heights, and **2,250 is where the FT2 family equilibrates**, exactly the `ratingpath`
bound (equilibrium ≈ 2,180 then, 2,250 now that ENDROUTE is in). Neither is on a path to 3,066 by climbing.

## 2. The new leg `S/livewatch/` — 32 boards, all 32 losses of 56313436

`dl.sh` → `P=5 cut_all.sh` (`cut_one.sh` = byte copy of `S/stack1/cut_one.sh`) → `build_set.py`.
**64/64 cuts byte-exact** (drawn + pinned-town, `verified` on both), opponent seat taped,
town registry `S/liveband/town_schedules.json` 921 → **953 rows**, seed base
`SB0 = 777001 + 1000003*2700 = 2700785101` (unused rung). Runner
`WORKERS=3 bash S/livewatch/run_livewatch.sh <label> <theta> [worktree] ["SWITCHES"]`, 64 rows
(both seats of each pinned town) in **4 min**. INFORMATIONAL — a fresh cut is a monitor, not a gate
(`2026-09-16-judge-baseline-rule.md`).

## 3. The judge reproduces the live ladder again

`ship` = master `c6da7f0` tree, FT2 switch string (ENDROUTE_ON is its default).
**32/32 losses reproduce as losses on the live seat**, and **18/32 to the coin** (mean |replay − live| 633).
Four boards drift by more than 1,000 (110299905 −8,192→−4,773, 110313293 −11,347→−3,976,
110280518 −5,659→−971, 110242547 −3,594→−1,077) — all still losses, so no loss is a seat/seed flip.
On both seats the shipped tree wins **0/64**: these are boards we are simply beaten on.

## 4. ESR on the live losers

ESR = shipped + `ENDROUTE2_ON`, `ENDROUTE2_SPLIT_ON`, `ENDROUTE_ROW2_ON` (pump ON, `CLIP_CAP_ON` OFF),
the `2026-09-18-stack5.md` recommended upload, run from this worktree on the same tapes and seeds.

| statistic (n=32 boards, live seat) | mean | se | t |
|---|---:|---:|---:|
| LIVE margin | −3,720 | 552 | −6.74 |
| SHIP replay | −3,145 | 479 | −6.56 |
| ESR replay | **−2,836** | 486 | −5.83 |
| **ESR − SHIP (paired)** | **+309** | 87 | **+3.55** |

**4 of the 32 losses flip to wins under ESR, 0 anti-flips** (both-seat board wins 0/64 → 8/64):

| ep | opponent | opp rating | live | SHIP | ESR | Δ |
|---|---|---:|---:|---:|---:|---:|
| 110282357 | yuya | 2,308 | −138 | −138 | **+848** | +986 |
| 110280704 | Zhou Songyu | 2,209 | −726 | −622 | **+486** | +1,108 |
| 110243632 | Joyal | 2,236 | −481 | −28 | **+521** | +549 |
| 110238232 | minoneru | 2,247 | −126 | −126 | **+263** | +389 |

ESR is better on 23/32 boards and worse on 9 (worst −1,124, 110228239 Joseph Ayanda). The flips are
exactly the boards the live ladder lost by **under 750 coins**: 5 of the 32 losses were under 750 and ESR
takes 4 of them. It does **not** touch the big losses (−5k..−11.7k move by at most +1,124). Split by
rating the gain is flat — opp ≥2,220 +274 t +1.76 (n=15), opp <2,220 +340 t +3.62 (n=17) — i.e. on the
boards we actually lose, ESR's edge is the route stack's ~+300/board, not a class-specific fix. At the
observed 68 % / 100 games, converting 4 losses in 32 is 68-32 → **72-28**, worth roughly +25-35 rating
points at the current ±4.5 step; it is a real but small move, consistent with stack5's +565 t +9.34 pooled.

## 5. Loss classes — **nothing new**

`classes.py` (fertilizer-density census of `2026-09-17-liveband.md` §2 / `2026-09-16-topleg.md`):

| class | rule | n |
|---|---|---:|
| ENGINE | fert ≥ 140 | 0 |
| **ENGLITE** (band clone) | fert 60-139, d0 melon plate | **32** |
| RACER | fert < 60 | 0 |
| OFFPLATE | no d0 melon | 0 |

All 32 loss opponents: **10 melon tiles on day 0, first melon SELL on d10, 19 plants on d0, 260-288 hires,
fert 61-122 (median 109)**, step-0 row a wheat round trip — the identical fingerprint liveband found on
56298246's 26 losses. Our own seat: 0 melon on d0, fert 139-173 (median 152). So the entire 2,000-2,360
band we lose to is still **one class**, and every mechanism in it is on the closed list
(melon first-mover rent = flat tax, `MELONGIFT`/`MELONRACE`/`EARLYLOSS2`; our back-half volume =
`LOSSMAP2` §3). **No new loss class**, and no engine-class (fert 164-175) seat has beaten either
submission yet — 56313436 has met nothing above 2,360.

## 6. Repro

```
bash S/livewatch/dl.sh                     # 32 replays -> $LWDIR/replays
P=5 bash S/livewatch/cut_all.sh            # 64 byte-exact cuts
.venv/bin/python S/livewatch/build_set.py  # ids.txt, boards.csv, town_schedules.json
WORKERS=3 bash S/livewatch/run_livewatch.sh ship submission/theta.npy $R  "$BASE"
WORKERS=3 bash S/livewatch/run_livewatch.sh esr  submission/theta.npy $WT "$BASE,ENDROUTE_ON=True,ENDROUTE2_ON=True,ENDROUTE2_SPLIT_ON=True,ENDROUTE_ROW2_ON=True"
.venv/bin/python S/livewatch/read_leg.py S/lossflip/ship_livewatch.csv S/lossflip/esr_livewatch.csv
.venv/bin/python S/liveband/opening.py $LWDIR/replays/ep_*.json > S/livewatch/opening.csv
.venv/bin/python S/livewatch/classes.py
```
