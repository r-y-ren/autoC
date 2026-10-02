# Field drift check — live sub 56098262, 2026-09-09

Question: today's 30W/42L (41.7 %) after "~52 % in the first ~150 games" — stronger field (a),
rating inflation (b), board/coin draws (c), or noise (d)?

Data: `ListEpisodes {"submissionId":56098262}` → 181 episodes, 180 usable (1 malformed).
Raw + scripts: `S/drift/{eps_fresh.json,rows.json,an*.py}`. Ratings = per-episode `initialScore`
(opponent's rating entering the match); coins = `reward`.

## Per-day

| day | N | W | L | win % | opp rating mean | sd | ≥2000 | our coins | their coins | our rating end |
|---|---|---|---|---|---|---|---|---|---|---|
| 09-08 (all) | 108 | 56 | 52 | 51.9 % | 1931 | 322 | 64 % | 101,410 | 97,217 | 2007 |
| 09-09 | 72 | 30 | 42 | 41.7 % | 1993 | 51 | 42 % | 100,337 | 100,338 | 1954 |

The 09-08 row is **ramp-contaminated**: games 1-20 were 19W-1L against a mean rating of 1403
(85 % below 1800) while the new submission climbed from ~600 to ~2050. That block alone is the
whole "52 %".

Chronological blocks of 20 (rating / win %):

| block | day | win % | opp rating | ≥2000 | our coins | their coins |
|---|---|---|---|---|---|---|
| g1-20 | 09-08 | 95 % | 1403 | 10 % | 109,007 | 87,360 |
| g21-40 | 09-08 | 45 % | 2116 | 95 % | 99,629 | 97,159 |
| g41-60 | 09-08 | 30 % | 2071 | 85 % | 93,889 | 98,932 |
| g61-80 | 09-08 | 45 % | 2001 | 55 % | 99,357 | 98,108 |
| g81-100 | 09-08 | 55 % | 2029 | 75 % | 107,744 | 103,400 |
| g101-120 | 09-08/09 | 35 % | 2005 | 55 % | 100,876 | 101,228 |
| g121-140 | 09-09 | 60 % | 2009 | 55 % | 91,376 | 90,625 |
| g141-160 | 09-09 | 40 % | 1983 | 35 % | 106,273 | 105,171 |
| g161-180 | 09-09 | 25 % | 1986 | 30 % | 100,675 | 104,206 |

**Ramp-free baseline**: 09-08 restricted to opp ≥ 1800 = 91 games, **40W-51L = 44.0 %**
(opp 2050 ± 73, 76 % ≥ 2000, our coins 99,449 / theirs 98,957).
Same cut on our own rating (≥1900) gives 43.3 %. Today is 41.7 % against a *weaker* field
(1993 ± 51, 42 % ≥ 2000). The true regression is 44.0 → 41.7 %, not 52 → 42 %.

## The four hypotheses

**(a) stronger field — NO.** Today's mean opponent rating is 57 points *lower* than the
settled part of 09-08 and the ≥2000 share fell 76 % → 42 %. Per-band records are flat:
2000+ 38 % (26-43) → 33 % (10-20); 1950-2000 60 % (9-6) → 58 % (18-13). The only band that
moved is <1950, 71 % (5-2) → 18 % (2-9), on 18 games total — those are freshly-uploaded agents
whose ratings have not settled, so the label is unreliable, not the field.

**(b) rating inflation — NO.** 8 teams appear on both days; their mean rating *fell*
−45 points (median −47) from 09-08 to 09-09.

**(c) board/coin draws — NO.** Our final coins are flat: 99,449 (09-08 settled) → 100,337
(+0.9 %), sd 21.7k → 22.9k. Opponent coins rose 98,957 → 100,338 (+1.4 %). Mean margin
+492 → −1. Median margin was already **negative on both days** (−1,768 → −1,268): we have been
losing the median game since the ramp ended; the 09-08 mean was carried by a few blowouts.
Narrow (<5k) losses: 16/42 today vs 18/51 on 09-08 settled — same shape.

**(d) noise — YES, mostly.**
- P(≤30 of 72 | p = 0.52) = **0.051** — borderline against the contaminated baseline.
- P(≤30 of 72 | p = 0.466, first-150 opp≥1800) = **0.236**.
- P(≤30 of 72 | p = 0.44, the honest baseline) = **0.391**.
- Two-proportion 09-08(opp≥1800) vs 09-09: z = 0.29, **p = 0.77**.
- 09-08 all vs 09-09: z = 1.34, p = 0.18. First-150 vs today: z = 1.44, p = 0.15.
- Elo-expected wins (400-scale, per-game initialScore): 09-08 settled actual 40 vs expected 44.0
  (−0.84 sd); today actual 30 vs expected 36.3 (−1.51 sd). Neither is significant on its own.
- Only sub-signal worth a second look: today's **last 24 games are 6W-18L, −2.38 sd vs Elo**
  (first 48 were 19W-29L, −0.1 sd). Two-prop first48 vs last24 z = 1.23, p = 0.22 — still noise
  at n = 24, but re-check tomorrow; a real late-day drift would repeat.

## Repeat-opponent structure of today's 42 losses

The field turns over almost completely: only 8 of 72 games today were against a team we met on
09-08, and 67/72 were against submission ids unseen yesterday.

- vs a team we **beat** earlier in the submission's life: **3**
- vs a team that only beat us earlier: **1**
- vs a team **never seen before**: **38**
- (today's 30 wins: 2 prior-beat, 2 prior-loss, 26 new)

So "we lost to teams we used to beat" is not the story — there is essentially no overlap to
regress against. New-team games today: 26W-38L (41 %); repeat-team games 4W-4L.
Opponent submissions dated ≥09-08: 62 % of today's games vs 51 % on 09-08 settled, and we score
the same against fresh (42 %) and older (41 %) uploads today.

## Verdict and what it means for the fresh-loss leg

**(d) noise, on a baseline that was never 52 %.** The submission's real settled win rate against
the ~2000 band is 43-44 %, established over 163 post-ramp games (70W-93L = 42.9 % pooled). Today
is a 1.5-sd wobble on that, not a regime change; the "52 %" figure is an artifact of counting the
19W-1L ramp against 1400-rated opponents.

Implications for the fresh-loss leg built from today's games:
1. Do **not** treat it as a harder-than-usual sample. Its opponent mix is 57 rating points
   *softer* than the 09-08 settled field and its band-by-band records match. It is a
   representative ~2000-band sample.
2. Do **not** expect a lever validated on it to recover "the missing 10 points" — 8 of those
   points never existed. The honest gap to close is 44 % → 50 %, ~4 wins per 72 games.
3. The leg is loss-*conditioned*, so it inherits the usual selection bias
   (see `counterfactuals-overstate`): 16/42 of its losses are inside 5k coins, i.e. inside the
   shop-draw noise band (±25k zero-mean per game). Paired legs with `--seed-per-opponent` remain
   the only judge; a replay-level improvement on these 42 boards is not evidence.
4. Because 38/42 losing opponents were never seen before, the leg is a *breadth* sample of the
   band, not a rematch set — good for generality, useless for detecting "we regressed against
   opponent X".
