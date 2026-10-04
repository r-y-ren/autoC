# PLANSELECT — ceiling of a rival-conditioned plan selector (offline, no engine run)

2026-09-17 09:04-09:35Z, worktree `planselect` off `70b98ff`, tools/tables `S/planselect/`.
Board = (seed, opponent), seats averaged (`S/nexthigh/pair.py` statistic). Candidates =
banked `S/lossflip` legs covering ≥ 80 % of the boards, leg mean within 2,000 of FT2, FT2
clones de-duped: 51 eng22 / 13 v45 / 6 topleg2 / 3 topleg3; a K-plan selector = FT2 + the
top-(K−1) by leg mean. Observables = the rival's 719-step tape decoded offline (24 steps/day)
cut at end of day 0/2/5 (melon/total plants, hires, animals, land, sells, seed buys, water,
care, harvest, fert pickups, ops) + shops unlocked by that day (`observation.town` carries
only `unlocked_shops`).

## 1 Oracle ceiling (`tables/oracle.csv`)
| leg | K=all | K=8 | K=4 | K=2 | Δours K=4 | Δtheirs K=4 |
|-----|------:|----:|----:|----:|----------:|------------:|
| ENG22 22 | +3,503 | +2,602 | +1,775 | +1,461 | +1,876 | +101 |
| V45 30 | +2,316 | +1,996 | +1,890 | +1,195 | +1,291 | −599 |
| TOPLEG2 30 | +3,164 | +3,164 | +1,681 | +431 | +1,775 | +94 |
| TOPLEG3 30 | +4,850 | +4,850 | +4,850 | +3,793 | +3,884 | −966 |
| POOLED 112 | +3,455 t 6.1 | +3,193 t 5.7 | +2,605 t 4.7 | +1,739 t 3.1 | | |

Oracle board win: ENG22 41→55 %, TOPLEG2 57→77 %. Not sampling noise: the two seats of a
board share seed, town and tape, and the seat-0 argmax scored on seat 1 keeps **93-100 %**
of the oracle (argmax agrees on 77-100 % of boards, `tables/seatsplit.csv`) — which plan
wins is a property of the BOARD.

## 2 Realisable from day-0/2/5 rival observables — nothing (`tables/selector.csv`)

Leave-one-board-out fitted trees, pooled 112 boards, Δ vs FT2:
| selector | K=2 | K=4 | K=8 |
|---|---:|---:|---:|
| depth1 d0 | +184 t 0.94 | +170 t 0.74 | −276 t −0.86 |
| depth1 d2 | **+364 t 1.18** | −138 t −0.37 | −844 t −1.89 |
| depth1 d5 | +344 t 1.13 | +54 t 0.15 | −562 t −1.53 |
| depth2 d5 | +737 t 1.32 | −33 t −0.11 | — |
| town-only d5 | +531 t 0.94 | +363 t 0.60 | −262 t −0.42 |
| town FULL schedule d5 | +202 t 0.37 | −466 t −1.56 | −1,036 t −3.20 |

The no-observation control (always play the best training-mean plan) is itself +182 t 0.50
at K=2 (`tables/fixedbase.csv`); paired against it (`tables/selvalue.csv`) the SELECTION
increment is **+161…+555, t ≤ 0.93** in all seven configurations — a best-of-seven max, so
the honest expectation is lower, and K=8 is negative every day. Half the explanation: the 30
V45 tapes are byte-identical over days 0-5 (open-loop clone), nothing to condition on. The
other way: the K=2 plans (`f223_g30`, `f224_g30`, `bc_clipcap`, `pc2_pumpclip`, `cliptop`)
are all HARD-REJECTED held-out (ESJUDGE3, CLIPTOP, PUMPCLIP) — even the +182 is in-sample.

## 3 The melon cell (`tables/meloncell.csv`)
No uncontested pot exists: the rival plants melon on day 0 on 21/22 ENG22, 30/30 V45, 29/30
TOPLEG2, 30/30 TOPLEG3 boards. On the one ENG22 board where it does not, M3 still loses
−1,993 and M12 −20,106; corr(plate delta, rival d0 melon) = +0.19/+0.15/−0.25 (M3/M6/M12).

## 4 Verdict
(a) Oracle **+1,739** (K=2) to +3,455 (K=all) pooled, a real board property. (b) Realisable
from the rival: **≈ 0** — +161…+555 at t ≤ 0.93 from day 0, 2 or 5, with or without the
town. (c) §115b (≥ +450, t ≥ 3): **not cleared**, t is a third of the bar with 112 boards
already averaged. (d) No architecture: a K-plan switch cannot be built on a signal this box
could not find. **RIVAL-CONDITIONED PLAN SELECTION CLOSED.**

Survives as a different box: the oracle is keyed to the SEED, whose visible half — our OWN
day-0 draw (tiles, quadrant, shop timing) — was never in this feature set, because reading it
needs an engine run. That is board-adaptive, not rival-adaptive, selection.
