# 2026-09-17 — BURNCAUSE: why OUR dusk clip is 22 u and the engine class's is 8

**VERDICT: STOP, nothing built.** The 16.5 u difference is not a smaller haul —
on a clipping night *they* carry 99.2 u to our 106.4 and lose 7.5 u to our 7.3.
It is the **number of clipping nights** (2.7 vs 1.0) = the shed run as a **FLOW**
against our nightly **BATCH**: they deposit **610 u** and sell **432 u after turn
18** every game, we deposit **0** and sell **0** after the turn-18 lot, so the
**328 u/game** our crew harvests at t19-23 ride in its hands into a shed the lot
has just emptied — and one day's harvest (83-91 u on d14-28) is already at the
100-unit cap. The three non-market handles price out at: **(c) 0 by identity**,
**(b) 0** (the ENG22 shed is as empty h19-23 as the band's: 0.9 u), **(a)/(d) =
`CLIP_CAP_ON`, which is already built** (merged OFF `2d2ff67`) and already judged
(§115b `+131 t 2.00`; on the shipped FT2 package `PUMPCLIP2 +441 t 2.77`, nine
coins under the bar). Re-measured here on FT2 it removes **15.8 u / 1,468
spot-coins** of the clip, and the **full ENG22 kill gate** (44 games, label
`bc_clipcap`) reads **+485/board, sd 1,158, t 1.97, flips 0/0, win 40.9 → 40.9;
ours +516 t 2.75, theirs +30 t 0.17** — a clean own-purse gain that misses the
gate's `t ≥ 2` by 0.03 on boards and passes it on rows (row t 2.75). So a burned
unit realises **0.375 of its spot price**, the residual 6.2 u is worth
**~+200/board**, and the built refinement that takes it (`CLIP_CAP_STRICT_ON`)
measured **−0** on ENG22. **No NEW handle with headroom ≥ +450 remains** — but
`CLIP_CAP_ON` is now the closest-to-bar unshipped switch in the tree (§115b +441
t 2.77 against a +450 bar) and this census is the mechanism behind it.

Instrument: 22 ENG22 boards, real engine, both seats, shipped FT2 + theta
`flow193_g100_hr`; shed and hands level every hour, every deposit, SELL and
HARVEST with its turn, and the dusk event (engine `:843`) per night.

## 1. THE CENSUS (per board, mean ± se; "clip" = nights that lose a unit)
| | clip u | clip coins | clip nights | dusk haul | dusk shed | clip haul |
|---|---:|---:|---:|---:|---:|---:|
| us (FT2) | **22.0 ± 4.5** | **1,998 ± 433** | 2.7 | 56.8 | 0.7 | 106.4 |
| them (engine class) | **7.8 ± 2.6** | 369 ± 120 | 1.0 | 40.5 | 7.1 | 99.2 |
| us + `CLIP_CAP_ON` | 6.2 ± 1.5 | 530 ± 109 | 1.9 | 56.3 | 0.7 | 101.6 |

Per **clipping night** the two seats are the same animal (lost 7.3 vs 7.5 u,
crew 12.3 vs 12.3 units): the seat difference is entirely how often the haul
reaches the cap. Our dusk haul sits at **83-91 u on every day d14-28**.

## 2. FLOW vs BATCH — units per game by turn (the cause, in one table)
| turn | 0-9 | 10-16 | 17 | 18 | **19-23** |
|---|---:|---:|---:|---:|---:|
| deposits, us | 5.3 | 39.4 | 25.9 | 28.5 | **0.0** |
| deposits, them | 87.8 | 79.9 | 16.6 | 23.2 | **401.9** |
| SELL commits, us | 836.6 | 29.6 | 465.3 | 83.8 | **0.0** |
| SELL commits, them | 930.7 | 130.2 | 26.7 | 26.2 | **432.1** |
| harvest, us | 286.4 | 605.3 | 80.7 | 74.8 | **327.8** |
| harvest, them | 544.9 | 542.2 | 64.7 | 55.5 | **211.2** |

Our shed by hour: 55 at h0, 17 from h4 to h17, **0.9 from h18 on**; our hands
climb monotonically 0 → 54.8 (**102.3 on clipping nights**) and are never flushed.

## 3. THE FOUR HANDLES, PRICED (two purses, spot on the landing day, ≤ d29)
| handle | ceiling | cost | verdict |
|---|---:|---|---|
| **(a) harvest-excess deferral** | +1,870 c/board at spot (t 4.3; perfect foresight defers 27.5 u / 10.1 harvest ops, residual burn 2.1 u) — **but realised +551 our purse** | tile-day of replant delay; the freed ops refill from the value tail | **already built** = `CLIP_CAP_ON`; §115b REJECT |
| **(b) late lot after the drops** | **0** | — | our deposits are 0.0 u at t19-23 and the shed holds 0.9 u there: a late row has nothing to draw on (= `SHEDDUMP`, ENG22 confirms band) |
| **(c) mid-day shed drop** | **0 by identity** | 2×DIST_SHED per diversion | dusk loss is `max(hands + shed − 100, 0)`; a DROP moves X from hands to shed and leaves the sum invariant. Only a SELL (or a feed/spread) drains it — which is why (c) is worth something *only* with (b), i.e. the route+market pair, closed at `c78d175` and `SHEDDUMP` |
| **(d) smaller haul by design** | = (a) | same | `CLIP_CAP_ON` already suppresses the HARVEST op itself (tile still visited and watered) |

**The clip is a MIX, not a volume.** `CLIP_CAP_ON` cuts harvested units 1,375 →
1,354 and units sold 1,415 → 1,413 while paying +516 our purse: what it buys is
*which* 22 u die (MELON 488→177 c, WOOL 583→48, MILK 116→48). That is
`SHEDCLIP2`'s "the clip was never the quantity to maximise" with the exchange
rate attached — **1 spot-coin of clip removed = 0.375 realised** — because the
rescued unit is sold into the tail of our own 828-unit dawn lot.

## 4. WHY THE ENGINE CLASS NEEDS NONE OF THIS
It never batches: its dusk haul is 40.5 u into 92.9 of room. Reaching that needs
both halves of a closed pair — an evening return leg per block (route-walk family
CLOSED `c78d175`, every walk-priced ceiling overstated by the tail-fill value)
and a market row after it (`SHEDDUMP`, +0.10 u).

## 5. REPRO
`WORKERS=2 bash S/burncause/run_probe.sh` (22 boards, ~3 min) and
`... run_probe.sh clipcap "$FT2,CLIP_CAP_ON=True"`, then
`S/burncause/report.py S/burncause/raw [clipcap]` (census, hourly, per-turn,
per-product), `S/burncause/cfact.py S/burncause/raw` (handle-(a) ceiling) and
`S/burncause/pair_raw.py S/burncause/raw '' clipcap` (paired margin + burn);
kill gate `WORKERS=2 bash S/judge7065/run_eng22.sh bc_clipcap <theta> <worktree>
"$FT2,CLIP_CAP_ON=True"` + `S/nexthigh/pair.py S/lossflip/{ft2,bc_clipcap}_eng22.csv`.
Reports `S/burncause/*.txt`, leg rows `bc_clipcap_eng22.csv`; raws untracked
(5.6 MB). No `src/` change and no test: nothing was built.
