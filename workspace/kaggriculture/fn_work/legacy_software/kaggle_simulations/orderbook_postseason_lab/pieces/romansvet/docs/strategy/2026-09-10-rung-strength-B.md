# Rung strength vs the live ≥2300 pool — blind review B (2026-09-10)

**Question.** Is the flow185c training population (147 pinned tapes, `~/launch_flow185c.sh`)
the population the live file (g940pair, sub 56140532) loses to?
**Answer: no.** 108 of the 147 rungs are our own *losses* to opponents rated 1628–2212 at the
time (median 1981) — a band the live theta now wins 80–100 % of; the 2300–2700 band, which is
77 % of live games and **100 % of live losses**, holds **one** rung (0.4 % of fitness weight).
The rest of the mass is top-ten tapes (≥2700), a band the live file is never matched against.

## 0. How weights become episodes (verified on the remote)

`scripts/train.py:168` + `artifacts/flow185c/train.log:2`: `pinned-once: 147 pinned rungs x 1
episode + 13 episodes carried`. Under `--pinned-once` **every pinned rung plays exactly one
episode per generation whatever its weight**; `--rung-weight` moves into the fitness
aggregation (`src/kagg3/es/train.py:645` — a weight-w board contributes `w·x` to a weight-sum).
So the *episode* share of any band is `rungs/160` and the *gradient* share is `Σw/458`
(Σw = 127×2 + 20×10.2 = 458). The 13 carried episodes go to self-play/pool (the four archetype
rungs are at w=0). "40 % of the episode budget" for the top-ten rungs (flow183 header) is
really 44.5 % of the gradient and 12.5 % of the episodes.

## 1. Training rungs vs the live pool, by opponent rating

Ratings: 109 own-game rungs from Kaggle ListEpisodes on our 13 submissions (opponent
`updatedScore` at game time; 59 from sub 56098262, 48 from 56028553, 1 each 56006782/56013041);
10 top-ten tapes from the top-ten teams' current submissions; **28 tapes not exactly rated**
(see §4) placed by cut provenance. Live pool = sub 56140532, 94 episodes at 15:00Z
(`S/livec/eps_new3.json`); LIVE-C72 = its full ≥2300 census.

| Opponent band | Rungs | Episode share (of 160) | Gradient share (Σw/458) | Result at cut | Live theta now (paired judge) | Live pool games (W) |
|---|---|---|---|---|---|---|
| <1900 | 49 (all own losses, w2) | 30.6 % | 21.4 % | 0/49 W | LIVE62 <1900: 4/4 | 13 (13 W, 100 %) |
| 1900–2100 | 46 (own losses, w2) | 28.8 % | 20.1 % | 0/46 W | LIVE62 1900–2100: 94/118 = 80 % (raw g940 csv); 7 in-sample rungs 8/14 | 2 (2 W) |
| 2100–2300 | 13 (own losses, w2) | 8.1 % | 5.7 % | 0/13 W | LIVE62 2/2 boards 0/2 | 6 (5 W, 83 %) |
| **2300–2500** | **1** (105592028, 2339, w2) | **0.6 %** | **0.4 %** | 0/1 | LIVE-C 36 boards: **48/72 = 66.7 %** | **36 (24 W, 67 %)** |
| **2500–2700** | **0** | **0** | **0** | — | LIVE-C 36 boards: **43/72 = 59.7 %** | **36 (21 W, 58 %)** |
| 2700–2900 | 4 exact (2886–2894, w10.2) + ~20 by provenance (8 top tapes of 09-08 at w2, 12 top-ten of 09-09 at w10.2; ladder 2820–2950) | ≈15 % | ≈36 % | opponent won | TOPB2/TOPB 25–35 % | 0 |
| ≥2900 | 4 exact (2905–2941, w10.2) + 2 (106802500/2 at 2886/2875 → 2700–2900 strictly) | ≈4 % | ≈13 % | opponent won | TOPB2 25–35 % | 0 |
| unrated: leg family | 8 (105228357…105268279, cut 09-03 as top-tier tapes, w2) | 5.0 % | 3.5 % | — | anti-predictive (family-volatility doc) | — |

Totals: 147 rungs; 108 own losses (median opp 1981, max 2339; our own rating then median 1998);
30 top-tier tapes; 8 family. Live ≥2300 pool: 72 games, 27 L / 45 W (62.5 %); losses by band:
2300–2500 12, 2500–2700 15, elsewhere 0.

## 2. Where the mass sits vs where we lose

* **The training mass is bimodal**: 47 % of the gradient on a 1628–2212 band the live file now
  wins at 80–100 % (its live pool below 2300: 20/21), and 49 % on ≥2700 tapes the live file is
  never paired with (0/94 live games ≥2700; it must first climb through 2300–2700).
* **The target band is absent**: 1 rung of 147, 0.6 % of episodes, 0.4 % of gradient, against
  77 % of live games and 100 % of live losses. Matching the live loss distribution would put
  ~100 % of the loss-derived weight there; matching the game distribution ~77 %. Either way the
  band is under-represented by roughly **two orders of magnitude**, not a re-weighting margin.
* Also in-sample: 7 training rungs sit in LIVE62 (106945656, 106947016, 106948946, 106957848,
  106963001, 106963950, 106964777), so LIVE62 is 55/62 held out, not 62/62.
* Every own-game rung is a *loss at the time* of a weaker theta (flow102/flow135) to a
  1900–2100 opponent. The ES has been fitting "why flow102 lost to 1980-rated clones", which the
  live theta already solved; it has never seen a 2450-rated opponent's play.

## 3. Minimal change for flow187 (episode budget stays 160)

Pinned-once makes rung *count* the budget: adding N pinned rungs needs dropping N (or raising
`--episodes`). Proposal, 63 in / 63 out, 147 pinned rungs, 13 carried, unchanged:

1. **Add LIVE-C ids 1–63** (`artifacts/tape_actions_town/1074*.npz`, already on the remote with
   town rows; `S/livec/ids.txt` lines 1–63) as `--tape-actions` rungs. Weight the 24 losses
   `=3` and the 39 wins `=1` (loss ids: rows 1–4, 9–15, 34, 38, 40, 43, 45, 46, 48, 49, 53–55,
   58, 63 of `S/livec/provenance.txt`) → 72 + 39 = 111.
2. **Drop the 49 rungs rated <1900** (all w2, 21 % of the gradient for a band we win 100 %):
   105400600,106360643,106369632,106371355,106379548,106389341,106398274,106399071,106411964,
   106426223,106448622,106449514,106463532,106474761,106491353,106501074,106522358,106558407,
   106574563,106577326,106598387,106601991,106612177,106616605,106656838,106693472,106697503,
   106755462,106762090,106767822,106769972,106778058,106781931,106363598,106379099,106389749,
   106401414,106438084,106459205,106479420,106512362,106558765,106606614,106629051,106670138,
   106722363,106764139,106773901,106793159.
3. **Drop the 8 leg-family tapes** (105228357, 105232167, 105269242, 105441843, 105442685,
   105443859, 105441481, 105268279 — unrated, 105228357 a documented systematic drag) and the
   **6 lowest 1900–2100 rungs** 106910765, 106945656, 106963001, 106828673, 106851135, 106937336
   (two of them are LIVE62 in-sample, so LIVE62 gets more held-out, not less).
4. **Cut the 20 top-ten rungs from 10.2 to 4.** New Σw = 111 + 80 (40×1900–2100) + 26 + 2 + 20
   (09-08 top tapes) + 80 = 319: target band **35 %** of the gradient, 1900–2300 33 %, ≥2700 31 %.
5. **Gate field**: LIVE-C 1–63 become in-sample, so the `--real-gate-opponent` list must change to
   **TOPB2 (20, on the remote) + LIVE-C 64–72 (9) + LIVE-D 1–12 (12)** = 41 boards / 82 games at
   2 seats, all ≥2300 or top-ten; the 21 new ids need `rsync` of `tape_actions_town/`,
   `panel_opp_town/` and 21 append-only town rows (both sets are "SYNC not run" in their
   provenance). Grow it with `S/livec/extend_new.sh` cuts of sub 56143250's ≥2300 pool.
   Local auto-judge: LIVE-C63 baselines become in-sample; judge on LIVE-C 64–72 + LIVE-D + new
   cuts, and TOPB2/LIVE62 as before.

## 4. Risks and what I could not determine

* **Gate/judge contamination**: after step 1 every LIVE-C63 read (auto-judge, calibration-C's
  61.9 → 83 % target) is training-set; only 21 held-out ≥2300 boards remain until new cuts land.
* **One file's opponents, one four-hour window**: all 63 are sub 56140532's matches
  09:36–13:16Z on 09-10 (matchmaking ±150 around ~2480). Open-loop tapes replay the opponent's
  moves; 39/63 are boards we already win, which is "free" fitness unless weighted down (hence 3/1).
* **Losing 1900–2100**: 40 of 46 rungs stay; LIVE62 remains the guard, and it was 80–89 % — the
  band is not where rating is won. Removing <1900 entirely assumes those wins are robust; the
  live pool says 20/21.
* **Weights do not add exposure**: under pinned-once each board is one deterministic episode;
  raising w only sharpens the gradient on that board. More boards, not weight, is the lever.
* **Not determined**: exact ratings of 28 tapes (ListEpisodes by teamId returns 400; only
  current-submission pulls worked — 12 of the 20 w=10.2 top-ten tapes, 8 top tapes of 09-08,
  8 family tapes); the live theta's per-rung outcome on the 101 own rungs outside LIVE62 (no
  lossflip csv plays them; `log.jsonl` stores only rung-weighted aggregates); whether flow185c's
  gate record (g10, +3 net on 42 boards) reflects the band or the lottery.

Sources: `~/launch_flow185c.sh`, `~/stage_leg20/artifacts/flow185c/train.log`, ListEpisodes
(23 requests, 1/s), `S/livec/provenance.txt`, `S/lossflip/g940pair_livec.csv`,
`S/lossflip/flow172_g940_live62.csv`, `S/topb2/{lb,provenance}`, `S/glut/verdicts.log`.
