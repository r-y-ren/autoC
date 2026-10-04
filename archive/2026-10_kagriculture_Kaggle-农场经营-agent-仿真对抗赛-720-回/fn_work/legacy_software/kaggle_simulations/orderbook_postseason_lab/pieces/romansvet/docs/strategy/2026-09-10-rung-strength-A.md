# Rung strength vs the live ≥2300 pool (review A, 2026-09-10)

**Question.** Is the flow185c training population (147 pinned tapes, `~/launch_flow185c.sh`)
the population the live file loses to (LIVE-C72, opponents 2331-2615)?

**Answer: no.** The objective puts **0.4 %** of its weight on 2300-2700 opponents (one rung,
3정훈 2313). 46.5 % sits below 2300 (median w2 opponent 1998) and ~49-52 % on the ≥2700 top
tier. The band that decides top-10 is absent from training; it exists only as the gate.

## How weights become episodes

`--pinned-once` (train.log: `147 pinned rungs x 1 episode + 13 episodes carried`): each
pinned rung is played once per generation whatever its weight; the weight enters the fitness
mean as `2 × rung-weight` per episode (`pinned_weights`, `src/kagg3/es/train.py`), carried
episodes at 1.0. Objective share = `2w / 929` (929 = 127×4 + 20×20.4 + 13).

## 1. Rung mass vs where we lose

Ratings = opponent `initialScore` at that game (Kaggle ListEpisodes; 127/147 rated,
41 API calls, then HTTP 429). LIVE-C ratings from `S/livec/provenance.txt`
(`updatedScore`, ±15 pts vs initial); paired read = `S/lossflip/g940pair_livec.csv`.

| band | rungs | eps/gen | objective share | our result when taped | LIVE-C72 boards | live W % | g940pair W % (mean margin) |
|---|---|---|---|---|---|---|---|
| <1900 | 49 | 49 | 21.1 % | 0-49 (loss tapes) | 0 | — | — |
| 1900-2100 | 49 | 49 | 21.1 % | 0-49 | 0 | — | — |
| 2100-2300 | 10 | 10 | 4.3 % | 0-10 | 0 | — | — |
| **2300-2500** | **1** | 1 | **0.4 %** | 0-1 | **36** | **66.7 %** | 66.7 % (+4,115) |
| **2500-2700** | **0** | 0 | **0 %** | — | **36** | **58.3 %** | 59.7 % (+2,116) |
| 2700-2900 | 9 rated + 4 doc¹ | 13 | 10.9 % | n/a (third-party tapes) | 0 | — | — |
| ≥2900 | 9 rated | 9 | 18.0 % | n/a | 0 | — | — |
| top-ten, API-unrated² | 9 (w10.2) | 9 | 19.8 % | n/a | — | — | — |
| leg family, unrated³ | 7 (w2) | 7 | 3.0 % | — | — | — | — |
| carried (pool/self-play) | — | 13 | 1.4 % | — | — | — | — |

¹ 106800430/106802486/106803087/106803884 = the "current top 10, 2821-2938" cut (verdicts).
² 107010600 107000107 107010590 107005822 107008406 107008216 107014982 107014375 107015773
(Matthew Huang, mtmr_s1, 自己找差距, DECEM, keiz, Tarang222): the 2850-2954 top-ten cut of 09-09.
³ 105228357 105232167 105268279 105269242 105441481 105441843 105443859 (Dmitry Larko, Jesse
Bullard, …): the 09-05 "top-tier" cut; the one rated sibling (105442685) is 2721.

Sources of the w2 rungs: 59 losses of sub 56098262 (flow135_g350, rated ~1900-2100 then),
48 losses of sub 56028553 (flow102_g280, ~1580 rated, so its opponents are 1620-1900),
2 older, 18 top-tier third-party tapes. Percentiles of the 116 rated w2 opponents:
p10 1704 / p25 1756 / **p50 1998** / p75 2061 / p90 2186.

Judges: LIVE62 = 60/62 opponents in 1900-2100 (file wins 88.7 %); TOPB2 = 20 boards ≥2953
(25-30 %); LIVE-C72 = the full ≥2300 pool of sub 56140532, 27 L / 45 W, mean opponent 2497.

## 2. Verdict on the mass

* Sub-2300: 46.5 % of the objective, all loss tapes against opponents the current file
  already beats ~89 % of the time — half the signal defends a band that is won.
* Top tier: ~50 % (the 20 top-ten rungs alone 43.9 %); weakest band (TOPB2 25 %), but the
  calibration (13:26Z/15:04Z) says 2960 is reached through LIVE-C ≈ 80-83 %, not TOPB2.
* Target 2300-2700: **0.4 %**, versus 100 % of the pool where the win rate must move
  62 → 80 %. Under-representation factor is effectively infinite; a proportional objective
  would put ≥30 % there. Losses are spread over both halves (2300-2500: 12 L, 2500-2700: 15 L),
  so both halves need rungs, the upper half slightly more.
* Independently verified: none of the 72 LIVE-C ids is a flow185c rung (0/72 overlap with
  the launcher's `--tape-actions`); the "46 band ids in-sample" finding of 15:22Z concerns
  a different, sub-2300 field.

## 3. Minimal change for flow187 (budget stays `--episodes 160`)

Keep 147 pinned + 13 carried. Swap 42 rungs; touch two weight classes.

**Add (w4)** LIVE-C ids 1-42 (`artifacts/tape_actions_town/<id>.npz`, town rows already on the
remote, 14 L / 28 W, mean opp 2457):
`107429978 107430502 107433383 107436314 107427438 107432396 107435352 107439261 107441233 107442209 107445568 107446132 107449091 107451072 107454026 107429785 107437298 107442736 107444178 107447134 107450083 107454541 107431404 107434362 107438287 107440248 107443200 107445151 107445446 107447522 107448103 107452062 107453041 107455021 107456009 107456982 107457950 107458946 107459924 107460905 107461880 107462861`

**Drop** the 42 lowest-rated `<1900` rungs (opponents 1622-1816; keeps the seven ≥1817
incl. 106363598 Follow Me Gradient 1873):
`106612177 106389341 106769972 106781931 106438084 106793159 106762090 106501074 106399071 106693472 106764139 106522358 106629051 106722363 106778058 106616605 105400600 106474761 106656838 106360643 106448622 106755462 106411964 106558407 106398274 106670138 106379548 106449514 106401414 106479420 106491353 106606614 106463532 106558765 106389749 106371355 106379099 106512362 106577326 106598387 106459205 106426223`
(105400600 is a leg-family tape; if the family must stay whole, drop 106773901 instead.)

**Weights**: `--rung-weight tape_act_<livec>=4` for the 42; leave the 20 top-ten at 10.2 and
the rest at 2. Resulting objective (total 1,097): **2300-2700 = 30.6 %**, top-ten 37.2 %,
1900-2100 17.9 %, 2100-2300 3.6 %, <1900 2.6 %, other top-tier w2 6.6 %, carried 1.2 %.
(w2 gives 18.1 %, w6 39 % but 42 boards would out-vote the other 105.) Init flow172_g1000, sigma 0.02.

**Gate field replacing the moved boards**: LIVE-C ids 43-72 (30 boards, 13 L / 17 W, mean opp
2536; 43-63 are on the remote, **64-72 must be pushed append-only with their town rows**,
`S/livec/extend_new.sh` pattern) + TOPB2 (20) = 50 opponents / 100 games,
`--real-gate-metric win --real-gate-min-flips 4` (B's +5/60 scaled to 50 boards).
The staged `launch_flow186.sh` gate (LIVE-C 1-63 + TOPB2, min-flips 7) becomes in-sample for
flow187 and must not be reused. Local promotion judge stays LIVE-C 43-72 + TOPB2 + LIVE62.

## 4. Risks and what was not determined

* **Gate contamination**: 42 of the 63 flow185b/186 gate boards move in-sample; the
  replacement gate has 50 boards (SE ~10 % on win rate at 2 seats) — a lottery per the
  archive (±5-10 pt reads); rely on the local 30+20 judge, not on the remote accept.
* **One file's opponents**: LIVE-C is one submission's six-hour matchmaking window (some
  opponents repeat: Factual Explorer, parv goyal2, Reinforcement Larping); a theta that
  overfits 42 pinned boards is exactly what min-flips gates false-accepted before. Watch
  1-42 vs 43-72 divergence as the overfit alarm.
* **Losing 1900-2100**: that band keeps 17.9 % (49 rungs) and LIVE62 stays held out; the
  dropped <1900 boards are the ones with the least transfer. Keep LIVE62 ≥ 85 % as a veto.
* **Top-ten dilution** 43.9 → 37.2 %: TOPB2 may sag; accept if LIVE-C rises (calibration
  says LIVE-C carries the rating).
* Not determined: exact ratings of 20 rungs (429 rate limit; band assignment from cut
  documents); the taped seat of third-party tapes (assumed the higher-rated agent); whether
  wins in LIVE-C (28 of the 42) add gradient or merely anchor — a loss-only variant
  (14 boards) is too small to pin, so wins go in.

Data (durable): `S/rungstrength/` — `rung_table.json` (id, weight, opponent, rating, result),
`analyse.py`, the raw `eps_<sub>.json` lists.
