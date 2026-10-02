# GAPMATRIX — FT2's gaps vs the engine class, what closed them, what is left (2026-09-17 15:35Z, master e5b6eca)

Sizes are per board, paired, from the docs cited. "Closed" = judged on the engine and rejected on the pair.

| # | Gap (ours vs theirs) | Size | Tried and closed | Remaining fix | Generalize / swap |
|---|---|---|---|---|---|
| 1 | Melon first-mover rent: they sell d10-16 @ 222, we d20+ @ 54-163 | −15k on their sale, a FLAT TAX (same on won boards) | MELON_OPEN, MELONRACE, MIRROROPEN, MELONREACT, plan selection | none on our side of the pot: plating ourselves gifts +15.4k price | accept; judge every lever on the PAIR (MELONGIFT rule) |
| 2 | Day-10 cash 2.7-4k vs 9.6-11k | the melon rent re-invested | EARLYRAMP (seed-ward −10,278), HERDRAMP (herd-ward −1,633) | only via faster turnover, not re-splitting the purse | the d0-9 split is a local optimum in BOTH directions |
| 3 | Worked crew-turns −380/game (d0-9 hires 43 vs 64, h0-1 wait, d20-29) | ceiling ≈ +3,850 | FWDHIRE, H1WAIT, EARLYRAMP floor, ROUTEEFF, IDLEOPS | a schedule commitment that overrides the hire row (SCHEDSEARCH, in flight) | SWAP hire pricing "today's tasks" for a searched per-day floor |
| 4 | Back-half mix on losing boards (carrot 83 vs 166 u) | +10,592 W−L swing, +5,445 carrot | BACKHALF: town shop draw, labour identical | none: seed-drawn shop schedule; carrot-vs-rival-money term +1.2k t ~1 | our reaction to the quote is at ceiling |
| 5 | Every quantity lever credits their purse (shared pot) | gift 0.23-1.0 of our cut | ~60 reallocation families | produce MORE units, never re-allocate | two-purse rule on every leg |
| 6 | Optimizer overfits (sim peak, engine level) | noise ±25k/board vs gains of hundreds | ES on every mask/σ/fitness; knob sweeps | direct schedule search with seedmem + ENG22 gate; more boards per eval | swap fitness to margin + board-flip bonus once a basin exists |
| 7 | Planner has no intent memory (one-day greedy, 1/3/7-day crew vectors) | see #3 | hand-written intents all lost | SCHED_OVERRIDE table (in flight) → state-conditional table | generalize: table keyed on day+state instead of fixed |
| 8 | Fertilizer landing 29 % best-day vs 91 % | was −2,845 | — | DONE: FERT_TIMING_ON (largest pass); DAYS 3 = 2 | closed |
| 9 | Sell timing (hour / order / day) | −308 / 0 / −26 realisable | SELLRACE, SELLDAY, SPREAD6 | none | closed |
| 10 | Ladder: landing in first 40 games, 61 % live in band, P(20-0) 0.08 | plateau 2,100-2,300 | upload lottery (killed) | replace the control at every §115b pass; strength in g11-20 | rating is f(first loss), not f(mean) |
| 11 | Population drift (V-series clone ~1/day) | — | — | daily cron: NBINTEL + V45LEG re-cut | monitor, not gate |

Reading: rows 1, 2, 4, 5 are the pot's structure and not fixable from our seat; 8, 9 are done; 10, 11 are process. The only open
engineering rows are 3, 6, 7, and they are one fix: a searched multi-day schedule the greedy must honour, gated held-out.

## 2. Strategy map — FT2 vs the engine class (top 10), per game unless noted (added 15:45Z)

| axis | FT2 (ours) | engine class (theirs) | source |
|---|---|---|---|
| planning | reactive: theta → 41-int macro each dawn → one-day greedy over turns | open-loop fixed tape, reproducible to the coin | TOPLEG, LIVEBAND |
| melon | plant d4-6, first sale d15-22 @ 54-163 | 6-13 tiles d0 (10 live), first sale d10 @ 222, 26.5 u then 13.3 u | MELONENG, HERDRAMP |
| d0-9 spend | seed 3,297 c · wheat 80.6 u · animals 2,617 c · hires 43 | seed 3,987 · wheat 105.8 · animals 3,283 · hires 64 (same 3,000 start) | HERDRAMP |
| d0-9 revenue | 14,712 | 14,628 (equal) | HERDRAMP |
| dawn cash d10/11/12 | 5,958 / 2,669 / 4,004 | 2,337 / 9,632 / 11,274 (melon rent) | HERDRAMP |
| hands d0-9 | 4.2/day (hire row clamped to today's tasks) | 6.6/day | TOPLEG, TURNCENSUS |
| worked turns | −380/game: h0-1 wait −164, d0-9 hires, d20-29 −180 | — | TURNCENSUS |
| wheat bought (season) | 157 u | 242 u (wheat is a wash on the pair) | LOSSMAP2, BACKHALF |
| fertilizer | FERT_TIMING_ON best-day; collect-fert 386 | 171 apps, 91 % best-day; collect 347 | FERTENGINE, HERDRAMP |
| herd | 6.9 d0-9 → 17.5 d10-19, season 13.7 | 7.6 → 16.1, season 13.1 | HERDRAMP |
| land | d5 and d10, no variance | d5-11, Q4 never | BACKHALF, TOPLEG |
| sell timing | lots at hours 2 / 11 / 19 (+17) | 23.7 % of units in hours 0-1 | SELLRACE |
| back half d16-30 | carrot / wool / milk / strawberry volume, set by the town's carrot bid | same carrot supply (88.6 vs 90.8) | BACKHALF |
| head-to-head | 25 % of engine-class boards, level on coins; live 61 % in the 2,050-2,220 band | — | JUDGEKIT, LIVEBAND |
