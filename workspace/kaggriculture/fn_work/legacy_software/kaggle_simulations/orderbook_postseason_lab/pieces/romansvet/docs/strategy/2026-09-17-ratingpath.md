# RATINGPATH — how a submission's rating travels; when a 2,700-band read is possible
2026-09-17 02:15-02:35Z, research only. `S/ratingpath/{pull,analyze,project}.py`; credential-free
ListEpisodes, 8 subs / 1,744 episodes (raw payloads S/.gitignore'd — re-pull with `pull.py <sub>`).

## 1. Per-episode mechanics (all subs start at mu=600; displayed score = mu)
* **Step size depends on GAMES PLAYED, not on rating or results.** Near-equal pairings (|gap|<80):
  `dW(n)=1270*n^-1.28` (n=260, r=-0.93) to n~60, then a **hard floor** — B (56161192) holds dW/dL
  +4.5/-4.4 flat from game 100 to 658 (5 d); the 4 fresh subs are +3.6..+5.1 at g61-120.
* **Pairing tracks our own rating from game 1**: settled opp p10/p90 within +-60 of own rating, mean gap
  -20. Win prob vs gap, shared logistic `p = 1/(1+exp((opp-mine-a)/193))`, i.e. 193 pts per logit.
* Ladder rate: 10-18 g/h for the first ~50 games, then 7, then **3-5 g/h** steady state.

## 2. The first-loss clock decides the whole day
| sub | first 20 | first loss | dW g11-20 | r@20 | r@40 | now |
|---|---|---|---|---|---|---|
| 56284867 FT2 | 18-2 | **g4** | +23.8 | 1408 | 1595 | 1733 (g70, 91.4 %) |
| 56277270 control | 16-4 | g10 | +52.4 | 1562 | 1604 | 1899 (g122, 78.7 %) |
| 56161192 B | 18-2 | g18 | +94.8 | 2113 | 2284 | 2516 (g658, peak 2773) |
| 56282369 rank10 | 20-0 | g36 | +89.0 | 2404 | 2871 | 3025 (g111) |
| 56278178 rank9 | 20-0 | g35 | +79.1 | 2323 | 2773 | 3012 (g118) |
| 56156662 rank1 | 20-0 | g56 | +89.7 | 2344 | 2805 | 3177 (g505) |
Landing rating is monotone in the first-loss game (also 56273500 g12 -> 1853, 56276165 g12 -> 1784): an
early loss subtracts ~60 AND collapses every later step. **Games 1-10 are worth ~100 pts each** and their
opponents are weak (500-1,300, stale August subs) — a defect there is the costliest thing we can ship.

## 3. Top climbers, first 150 games
56282369 crossed 2,700 at **game 28 / 1.6 h** after submit, 56278178 at g33 / 2.2 h, 56156662 hit 2,805 by
g40; each was paired >=2,500 by game 21-25 (89/93 such episodes). FT2 has met **zero** >=2,500 (max 1,794).
Is a 90 %-win sub fed strength faster? No — strength arrives only as fast as the rating moves, and it moves
only while the step is large: 91 % is not enough, 100 % is. Slow reference, our B: 2,400 g81/5.2 h, 2,500
g125/14.9 h, **2,700 g305/51.7 h**, peak 2,773 g402, decay to 2,516 on 33-43 % wins.

## 4. FT2 projection (`project.py`: net/game = 4.5*tanh(a/386), 3-4.5 g/h, pairing at own rating)
From 1,733 at game 70, p=0.91 => +3.7/game: **2,000** 60-90 games = 15-30 h (09-17 17Z..09-18 08Z);
**2,400** 150-190 games = 35-62 h (09-18 13Z..09-19 16Z); **2,700** 230-260 games = 55-85 h (09-19
09Z..09-20 15Z). Assumption: p=0.91 holds as opponents strengthen — it will not (B held 73 % at 2,550, 33 %
at 2,700). Bound: FT2's p at gap 0 implies equilibrium ~2,180; at B's ~2,650, 2,400 lands ~09-19 and 2,700
never arrives on this submission.

## 5. Answers
(a) **>=2,500 opponents regularly: 09-19 09Z earliest, more likely 09-20/09-21, never if equilibrium
<2,500.** A fresh upload going 20-0 is there in 22-25 games = **1.5-2 h**; re-shipping is ~30x faster than
climbing, so waiting on FT2 for a band read is not a plan.
(b) **No.** The control's 1,899 is no ceiling: it is 52 games older and lost first at g10 vs FT2's g4, and
both sit in the floor regime where rating lags strength (logistic offsets FT2 +455, control +253, rank1
+145 — every live sub is under-rated while climbing). FERT_TIMING's +2,845/game is untested live: neither
sub has met an opponent above 1,957.
(c) **Replace the control; no A/B.** A settled low-step sub can never be paired into the band, so the
second slot buys no information — it is worth more as a second independent first-20 draw of the candidate
(~900 pts of landing variance at equal strength). Judge a re-ship on its **first 25 games** (W-L + the
opponent ratings crossed), readable ~3 h after upload, not on the settled rating two days later, and treat
any loss in games 1-10 as the event to diagnose.
