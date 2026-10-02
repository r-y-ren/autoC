# EARLYLOSS — every loss our submissions took in their first 10 rated games
2026-09-17 02:30-03:00Z, research only. `S/earlyloss/{first10.py,replay_check.py,step0_timing.py}`,
`S/earlyloss/loss_profile.csv` (= `scripts/replay_profile.py` on the 4 loss replays; the 120 MB of
raw replays and ListEpisodes payloads are S/.gitignore'd — re-pull with `S/ratingpath/pull.py` and
`curl -L https://www.kaggleusercontent.com/episodes/<ep>.json`).

## 1. The table (8 of our subs, 2,061 rated episodes; only 4 losses land in games 1-10)
| sub | g# | episode | ours | theirs | margin | opp r (then/now) | opponent class | class |
|---|---|---|---|---|---|---|---|---|
| FT2 56284867 | 4 | 109755375 | 93,737 | 102,309 | **-8,572** | 966 / 1281 | melon+sheep clone | C |
| FT2 56284867 | 8 | 109758783 | 124,321 | 127,120 | -2,799 | 1169 / 1304 | melon+cow clone | C |
| control 56277270 | 10 | 109658389 | 80,996 | 81,413 | -417 | 1334 / 1362 | fert build | C |
| kagg2 55651890 | 9 | 95367472 | 107,981 | 113,528 | -5,547 | 1430 / 903 | **mirror of us** | C |
Everything else is 10-0: g940pair, g1000hr, B, pumpoff, lot4t17. First-10 pooled **76W-4L = 95.0 %**.
No episode in any of the 8 histories has a null reward, a non-COMPLETED state, or a non-ACTIVE
per-step status; all four replays reproduce the recorded rewards byte-exact (`replay_check.py`), and
`remainingOverageTime` is still 60 s for both seats at step 719 of all four.

## 2. Class counts — **A: 0/4, B: 0/4, C: 4/4, D: 0/4**
* (A) agent ERROR/TIMEOUT: **none, ever.** A timeout or error nulls the reward (core.py:281-284,
  636-638); 0 of 2,061 episodes. Overage is never touched, so no step ever passed actTimeout.
* (B) beaten by a stronger seat: **none.** All four opponents settle at 903-1,362 (own-score medians
  78.7k-97.5k vs our 96k-113k); none is the 2,900+ engine class. Each loss is the **closest or 2nd
  closest game of that sub's first 10** (|margin| rank 1 or 2 of 10, against a median |margin| of
  22k-35k). Game 9 of kagg2 is a literal mirror — byte-identical opening, 277 hires both sides.
* (C) board/town draw: **all four.** One channel repeats in every single one — **melon realised
  price**: ours 72 / 88 / 131 / 157 coins/unit vs theirs 195 / 199 / 213 / 239. Our median melon sell
  day is 18-22 vs their 10-17 and our pre-day-15 melon revenue is **0** in 3 of the 4 (they take
  6.2k-18.8k there). Second channel, board-specific: ep 109755375's town drew **3x YARN_STORE**
  (wool mean 203, day-29 price still 237); they bought 21 sheep and sold 241 wool at 221/u, we bought
  5 and sold 109 — **-30,067 on wool alone** in a game lost by 8,572 (+ -19,249 on melon). Our
  animal buy is fertilizer-driven, not wool-price-driven (WOOLPRICE), so a yarn town is free money we
  decline. ep 109758783 is the exception in shape: we out-produced them (revenue 150,443 vs 146,595)
  and lost on **spend** — +4,156 BUY_PRODUCT, +1,421 hire, +1,600 animals = -6,647, net -2,799.
* (D) an opponent collapse we still lost: impossible by definition — a collapsed seat scores far
  below its own normal, and all four opponents scored at or above their own median.
Seat asymmetry was checked and is dead: seat 0 608W-429L (58.6 %), seat 1 623W-401L (60.8 %), n≈1,030 each.

## 3. Step-0 timing (`step0_timing.py` on the shipped FT2 tarball ab1acb76, extracted like a Kaggle box)
`build_agent` defers `exec(main.py)` into the first timed act, so the step-0 charge is exec + act:
**exec 15 ms + first act 115 ms = 130 ms**, worst step of a full 720-step self-play game **129 ms**
(p99 94 ms, median ~0 ms, 2.6 s of agent CPU per game) — against **actTimeout 1,000 ms** plus a
**60 s** overage bank, i.e. 7.7x headroom on the hard limit before the bank is touched. The shipped
forward pass is pure numpy (no JAX at run time), so there is no compile cliff to warm up. **No
warm-up or compile cache is needed; do not build one.**

## 4. Verdict
**First-10 losses are class (C): board/town draws lost in the closest game of the window, not agent
defects — fix: nothing in the tarball.** The residual channels are the known ones (melon first-mover
rent; wool/sheep exposure on yarn towns; a spend overrun on one board), all already judged as levers
and closed. What is left is arithmetic, and it is worse than RATINGPATH assumed: our first-10 rate is
95.0 % (P(10-0) = 0.60) but the first-20 rate is **88.1 %** (141W-19L; opponents reach 1,500-2,400 by
g11-20 and those losses are just as close, median |margin| rank 3/20), so **P(20-0) ≈ 0.08** per
upload — a 2,300+ landing cannot be bought by re-rolling the same file at today's strength; it needs
p ≈ 0.97 per game over 20 games. Judge a re-ship on its first 25 games, and spend the engineering on
the g11-20 band (1,500-2,400 seats), not on the opening.
