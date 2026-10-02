# Field drift check 2 — is LIVE55 still representative? (sub 56098262)

**Real-time caveat**: this task asked for 09-09 vs 09-10, but at data-pull time
(2026-09-09T17:42Z, `ListEpisodes`, 190 usable games) the clock had not reached
09-10 — the submission's newest games are still 09-09. The honest test available
is LIVE55 (the 55 held-out boards, curated losses+wins spanning 09-09 00:08–15:00)
vs every game **strictly after** the LIVE55 cut, i.e. the most current opponents
the sub is actually meeting right now. Data: `S/drift2/{eps_now.json,rows_now.json,stats.py}`.

## (1) Per-day / per-window

| window | N | W-L | win % | opp rating mean±sd | ≥1800 | ≥2100 |
|---|---|---|---|---|---|---|
| 09-08 (full day) | 108 | 56-52 | 51.9 % | 1931±322 | 84 % | 18 % |
| 09-09 (full day) | 82 | 34-48 | 41.5 % | 1990±52 | 100 % | 1 % |
| LIVE55 (held-out) | 55 | 20-35 | 36.4 % | 1991±52 | 100 % | 0 % |
| 09-09 not-in-LIVE55 | 27 | 14-13 | 51.9 % | 1989±53 | 100 % | 4 % |
| **strictly after LIVE55 cut** (15:00→17:42Z) | 10 | 4-6 | 40.0 % | 1967±55 | 100 % | 0 % |

The field has fully settled into the ~1990-rated band (sd collapsed from 322 on
09-08 to ~53 since); ≥2100 opponents are essentially absent in every 09-09 window.

## (2) Opponent overlap

Of the 27 post-cut 09-09 games (not in LIVE55): **1/27** share a team with LIVE55
(HyperX, same submission id 56051591 both times) — 26 brand-new teams. Of the 10
games strictly after the LIVE55 cut: **0/10** repeat a LIVE55 team or submission
id — all 10 are new teams and new submission ids. The field turns over almost
completely game-to-game; LIVE55's opponent roster is not a fixed pool to regress
against.

## (3) Score distributions

| window | our Q1/med/Q3 | opp Q1/med/Q3 |
|---|---|---|
| LIVE55 | 81,626 / 97,047 / 116,715 | 79,198 / 97,306 / 118,456 |
| post-cut (27) | 88,142 / 91,851 / 107,196 | 82,916 / 91,775 / 107,272 |
| strictly-after (10) | — | — (n too small; medians noisy) |

Money has moved down and tightened: median coins fell ~97k→~92k on both sides,
and the whole game got smaller (Q3 fell 117k→107k) rather than one side pulling
ahead. Margins stay centered near zero on both windows — no shift toward us or
away from us.

## (4) Verdict

**LIVE55 representative — no material drift, within real-time limits of this check.**
Opponent rating (1991±52 vs 1967±55), ≥1800 share (100 % both), and score
distribution shape are unchanged since the LIVE55 cut. Win rate moved
36.4 %→40.0 % (post-cut 27-game block: 51.9 %) but the held-vs-post-cut
two-proportion test is z=1.34 (p≈0.18) — not significant, same noise regime as
the 2026-09-09 drift study. The only real change is opponent-roster turnover
(0/10, 1/27 team overlap), which is expected and doesn't affect representativeness
of the *distribution* LIVE55 draws from. Caveat: "now" here means the last 10
games of 09-09 (real 09-10 data does not exist yet) — re-run this check once
actual 09-10 games land before trusting the win-rate point estimate.
