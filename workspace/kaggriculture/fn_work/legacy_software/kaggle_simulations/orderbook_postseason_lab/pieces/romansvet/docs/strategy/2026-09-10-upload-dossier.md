# Upload dossier — next Kaggle submission (state at the 20:25Z hand-over line, 2026-09-09/10)

## 1. Purpose

Pick the next Kaggle upload: three packages ranked SAFE / AGGRESSIVE / FALLBACK, plus
flow172_g200 (reads the same as AGGRESSIVE, still in the veto queue) and flow172_g260
(remote-accepted, no LIVE55 read yet).

## 2. Candidates

| tier | package | md5 | theta |
|---|---|---|---|
| SAFE | `dist/submission_flow166_g170_pair.tar.gz` | `2e00efaa3fdaa0d7c92c7b5b96ad6a1d` | g170 + pair defaults |
| AGGRESSIVE | `dist/submission_flow172_g170c_pair.tar.gz` | `bdb718c3f09768a9f7604355a03d36c8` | g170c + pair defaults |
| FALLBACK | `dist/submission_flow172_g60_v2.tar.gz` | `1e7bea9e3299b5fdac335670cd93d4b3` | g60 |
| no pair | `dist/submission_flow172_g170c_v2.tar.gz` | `645d39bc5a40230f60c1212df17c4392` | g170c |
| superseded | `dist/submission_flow166_g170_v2.tar.gz` | `7f9e540bf3439348c638ac5b88f75353` | g170, no pair |

Pair defaults = TAIL_FILL_ON + BANK_BEFORE_LOT_ON.

## 3. How each was judged

All reads are LIVE55 — 55 pinned boards cut from live submission 56098262's own games, played
both seats, paired against the LIVE theta (flow135_g350).

- **SAFE (g170+pair):** LIVE55 34.5 → 52.7 % (+22/−2), excl-2 +4,018, SE 684, t 5.87, 43/53
  positive; +873/game over g170 alone. Drawn legs cleared (top10+today41 85.0→86.4 %,
  +483/game, t 1.72) — **veto clear**.
- **AGGRESSIVE (g170c+pair):** g170c alone: LIVE55 34.5 → 65.5 % (+36/−2), excl-2 +5,930,
  SE 669, t 8.87, 48/53 positive — best live read of the campaign — LOSS20 0 → 35 % (+14
  flips/7 tapes), +5,822, SE 1,342, t 4.34. Pair composed in: 34.5 → 66.4 %, flips +37/−2,
  excl-2 +6,579, SE 648, t 10.15, 49/53 positive, RULE PASS, ~+650/game over g170c alone.
  Pair package equivalence (bdb718c3) **exact** (100461/106312 on 107056463); pair's own drawn legs **clear**; g170c's own
  drawn legs still queued behind g60's; g170c alone (645d39bc) already coin-matched its judge
  row.
- **FALLBACK (g60):** LIVE55 34.5 → 58.2 % (+28/−2), excl-2 +4,834, SE 579, t 8.35, 47/53
  positive; HELD42 +18/−0 (largest net ever), LEG20 +834 PASS. Drawn legs still running.
- **flow172_g200** (remote-accepted, auto-judged): LIVE55 34.5 → 65.5 %, excl-2 +5,850, SE 648,
  t 9.02, 48/53 positive, same flip set as g170c — reads as the same candidate, behind it in
  the veto pipeline. **flow172_g260**: remote-accepted (wins 63→61, margin +375→+734, LEG20
  +11,774) but no LIVE55 read yet.

## 4. What each step actually buys (engine anatomy, 110 board-seats)

g60 over g170 (+1,825, t 8.9) is 91 % own-purse growth — sell rows shift from hour 1 to hour
18 (price/unit 92.38→93.47) — halving g170's downside tail. g170c over g60 (+942, t 3.5) is
**pure denial** (−39 ours / −981 theirs, a 0.7 coins/unit price cut taking ~1k off the
opponent), doubling the tail (worst-5 −36.5k vs g60's −22.6k). Neither step moves d10-14
income: the residual 15 of LOSS20 still lose ~−22.7k there, ~15k the d10-11 melon pot
(opponent 233 units @143.8 vs our 92 @117, zero melon before d10) — d0-9 and d15-29 are
already ours. FORWARD_ADMIT (hire pricing on projected tasks, built to reach that pot) is
**dead**: it already existed in arms-next and the ES chose forward_days = 0 every day; a
rebuild reads HELD42 −2,628 (t −8.0), LEG20 −1,456, LOSS12 −6,403, flips +0/−8. Not a hiring
problem.

## 5. Honest baseline and re-upload cost

The submitted "52 %" includes a 19W-1L ramp against mean rating 1,403. Post-ramp vs
opponents ≥1800, sub 56098262 reads **43 %** (44.0 % on 09-08, 41.9-41.7 % on 09-09, 42.9 %
pooled over 163 games, p 0.77 for a change from flat). Re-upload restarts the rating: ~150
games of re-climb against a ~1,980 ceiling — no candidate should ship for a margin the reads
cannot resolve at that cost.

## 6. Judge rule

LIVE55 (excl-2, SE, paired t) is the primary gate: majority-positive, t-significant margin
gain. The six drawn legs are a **non-regression veto only** — clear unless pooled grouped
t ≤ −2; a drawn win-rate dip alone does not veto when the panel margin is level (ceiling-
artefact rule). LOSS20 is a secondary strength read, not a gate. LIVE-B (11 out-of-sample
post-freeze boards) is directional only (n<15), queued behind the veto pipeline.

## 7. Caveats

- The remote gate **refused** g170c on its own LEG20 leg (−4,210/24 games, a coin flip at
  SE≈18k) despite the largest pinned win jump on record (51→67); shipped only after a hand
  read on LIVE55/LOSS20.
- No local read has ever predicted a Kaggle live-rating gain that held; LIVE55 is the closest
  proxy but is itself untested end-to-end.
- g170c is **denial-only** — no own-purse growth, doubled downside tail.
- The melon-pot residual (~−15k, 15 LOSS20 boards) is untouched by every candidate here, and
  FORWARD_ADMIT — the mechanism that would reach it — is dead.

## 8. Recommendation and order

1. **SAFE — flow166_g170_pair (2e00efaa)**: veto clear, ready now.
2. **AGGRESSIVE — flow172_g170c_pair (bdb718c3)**: best live read of the campaign (66.4 %,
   +6,579, t 10.2); ship once g170c's own drawn
   legs clear (the pair's own legs already are). g200 reads the same and may supersede without
   changing the call.
3. **FALLBACK — flow172_g60_v2 (1e7bea9e)**: lower tail, lower win rate (58.2 %); the choice
   if g170c's veto legs come back negative.

Do not ship either v2 (7f9e540b / 645d39bc) over its pair variant — the pair composes for free
on both thetas with a cleared veto.

## 9. After upload

The user uploads one package and reports the new submission id. Then: start
`S/kagwatch/watch.sh <sub> 0.43` and tally the post-ramp record (opponents ≥1800) at 50, 100,
and 200 games, discounting the first ~20 as the sub-1500 ramp.

## Update 2026-09-11 01:10Z — g60 clears its veto; order revised

flow172_g60's six drawn legs finished level or up (today41 +196 t 0.2, top10 +271 t 0.3, flood6 +2,705 t 1.3, band6 −859/+1,735, jesse4 −1,492 t −0.7 on 128 games; contested wins up on five of six legs). With LIVE55 58.2 % / +4,834 (t 8.4), LOSS20 25 % and the lowest tail of the candidates, `dist/submission_flow172_g60_v2.tar.gz` (md5 1e7bea9e3299b5fdac335670cd93d4b3) is now the **SAFE** file, ahead of g170+pair (52.7 %). Revised order: SAFE g60_v2 (1e7bea9e) → AGGRESSIVE g170c_pair (bdb718c3; g170c's own veto legs running now, pair veto clear) → growth-only alternative g170_pair (2e00efaa). Everything above this line predates the g60 verdict.

## Update 2026-09-11 02:00Z — g60 + pair becomes the SAFE file

flow172_g60 with the switch pair reads LIVE55 34.5 → 64.5 % (+33 flips, 0 drops), excl-2 +5,382 (SE 607, t 8.87), 48/53 positive; on the 11-board out-of-sample leg +5,833 (t 7.6, 11/11). Both components have cleared their drawn vetoes on their own. Package `dist/submission_flow172_g60_pair.tar.gz`, md5 `bcb2f3b020625a6b287299ff4622cd03`, equivalence exact (102004/108602 on 107056463). Revised order: **SAFE g60_pair (bcb2f3b0)** → AGGRESSIVE g170c_pair (bdb718c3; 66.4 %, g170c veto legs running, denial-only step with a doubled tail) → older files g60_v2 (1e7bea9e), g170_pair (2e00efaa). The two leading files differ by about two win points and 1.2k of margin; the safe one has the lower tail.

## Update 2026-09-11 04:20Z — held-out top-tier read (TOPB, §60)

Twenty fresh pinned tapes of the current top ten (in no list): g60_pair 25 → 35 %, +2,890 (t 1.9, 15/20); g170c_pair 25 → 30 %, +3,174 (t 1.9, 12/20). Half the in-sample top-ten margin, same win rates: both files still lose two of three against the top ten, so neither reaches the cutoff on its own (docs/strategy/2026-09-11-rating-equilibrium.md puts them at ~2650-2750). The upload still lifts the rating from ~1950; the top-ten gap is the ES lineage's job.

*Note (05:40Z, §61):* g200 vs g170c on the held-out top tier is noise (t −1.1); but the whole flow172 line hands the top tier +0.8-1.1k where it takes 2.2k off the band, so the held-out band margin overstates the top-tier margin about twofold.

## Update 2026-09-11 06:35Z — g300 + pair leads every leg

flow172's generation-300 record with the switch pair: LIVE55 34.5 → 70.9 % (+42/−2), excl-2 +6,753 (SE 679, t 9.95), 47/53; LOSS20 (theta alone) 0 → 40 %, +6,654; LIVE-B (17 out-of-sample boards) 76.5 %, +8,119 (t 8.4, 17/17); TOPB (20 held-out top-tier) 30 %, +3,730 (t 2.12, 14/20) — the first top-tier read to clear significance. Package `dist/submission_flow172_g300_pair.tar.gz`, md5 `82d0a198a3263e7dbf9768f5b343f877`, equivalence exact. Its drawn veto legs are running (auto-judge, labelled flow172_g260); if they clear, order = AGGRESSIVE g300_pair (82d0a198) → g170c_pair (bdb718c3) → SAFE g60_pair (bcb2f3b0).

## Update 2026-09-11 07:45Z — consolidated table

Sources: `S/glut/verdicts.log` (LIVE-B out-of-sample section onward), §55-§62 of `docs/strategy/2026-09-09-plateau-review-verdicts.md`, `docs/strategy/2026-09-11-flow172-g300-live-anatomy.md`, `docs/strategy/2026-09-11-topb-leg.md`.

| candidate | LIVE55 win / margin / t | LOSS20 win (theta alone) | LIVE-B 22 win / margin | TOPB win / margin / t | drawn veto | tail (worst-5, theta alone) | equivalence |
|---|---|---|---|---|---|---|---|
| **g300_pair** 82d0a198 | 70.9 % / +6,753 / t 9.95 | 40 % | 72.7 % / +7,808 | 30 % / +3,730 / t 2.12 | pending (running as `flow172_g260`, started 22:07Z, not yet resolved) | −21,627 | exact, 75549/58633, 2848 moves, board 106581754 |
| **g170c_pair** bdb718c3 | 66.4 % / +6,579 / t 10.15 | 35 % | 63.6 % / +7,202 | 30 % / +3,174 / t 1.92 | pending (pair's own drawn legs clear standalone; g170c's own veto legs still queued behind the judge lock) | −36,470 | exact, 100461/106312, 2864 moves, board 107056463 |
| **g60_pair** bcb2f3b0 | 64.5 % / +5,382 / t 8.87 | 25 % | 45.5 % / +5,842 | 35 % / +2,890 / t 1.87 | CLEAR (g60 cleared 20:35Z; pair cleared 19:25Z) | −22,585 | exact, 102004/108602, 2852 moves, board 107056463 |

Blank cells: none — every requested cell has a sourced number.

Win rate first favors g300_pair; it leads or ties every judge and, per the anatomy, halves g170c's tail (−21,627 vs −36,470), so it becomes the upload once its drawn veto clears. If uploading before that clears, g60_pair is the only fully-cleared file and ships now with the lowest LIVE55/LIVE-B numbers but the shallowest tail. Either way the rating model (`docs/strategy/2026-09-11-rating-equilibrium.md`) puts these files at a 2650-2750 ceiling, while holding the ~2880 cutoff needs roughly 52-53 % against the 2700-2950 tier and TOPB reads only 30-35 % there — so the top-ten gap stays the ES lineage's job, not this upload's.

User step: upload one package (g300_pair once cleared, else g60_pair now) and send the new submission id. My next step: start `S/kagwatch/watch.sh <sub> 0.43`.

*Note (08:45Z, §63-§64):* the 12 gate boards do not inflate LIVE55 (clean 43-board line for g300+pair: 79.1 %, +6,630, t 9.4). The +0.8-1.1k the lineage hands the top tier is late wool/melon abstention price, not a contested resource; no planner lever targets it.
