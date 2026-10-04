# hr's own ladder boards: hr vs candidate B vs candidate A (real-engine paired replay)

*2026-09-11 12:10Z. Scripts, ids, csvs and logs: `S/hladder/` (a clone of `S/bladder/`, parameterised on the hr
submission id 56143250). Companion: `docs/strategy/2026-09-11-b-ladder-paired.md` (candidate B's own 50 boards,
TOWN APPEND #8) — the two board sets are disjoint and must not be pooled.*

## Question

Our leaderboard entry is the **hr file** — Kaggle sub 56143250, package
`dist/submission_flow172_g1000_pair_hr.tar.gz` = theta `flow172_g1000` + the pair/hr switches; 133W-56L,
rating 2571 at the time of this measurement, paired against 2400-2650 opponents.

Candidate **B** (sub 56161192, theta `artifacts/kagg2_games/thetas/flow193_g100_hr.npy`) beat hr on our judge
and on B's own 50 ladder boards, but B has only ever met the ~2200-2400 band the fresh submission is seeded
into: it has never played a 2500+ opponent. The open question for promotion was therefore whether B's edge
survives against the tier hr *actually* faces. Same question for candidate **A**
(`artifacts/kagg2_games/thetas/flow187_g160_hr.npy`).

**Would B and A do better or worse than hr against the 2500-2650 tier?**

## Method

1. `S/hladder/pick.py 56143250 60` reads the credential-free `ListEpisodes` record for the hr submission
   (`S/hladder/eps_raw.json`, 189 completed games, 133W-56L) and takes the **most recent 60 completed ladder
   games in ladder order — wins AND losses, no loss selection** (`S/hladder/meta.json`, `ids.txt`). Games
   created 2026-09-11 01:12Z .. 11:25Z; Kaggle record on these 60 = **33W-27L**, mean margin +3,590; opponent
   ratings 2426-2657 (11 in 2400-2499, 40 in 2500-2599, 9 at 2600+).
2. For each game, `S/hladder/cut_one.sh` cuts a byte-exact action tape of **hr's OPPONENT** (drawn + pinned
   town) from the 32 MB replay. 35 boards were cut here; 25 were already on disk from the flow197 rotation cut
   (2026-09-11 07:29Z) and each of those 25 was re-verified to have been cut at the **same opponent seat** this
   ids.txt records. All 60 tape lines read "verified"; the taped player is never OurTeam.
3. TOWN APPEND #9 (`S/livec/provenance.txt`): `S/band2100p/town_schedules.json` 503 -> 538 and the superset
   merge into `artifacts/town_schedules.json` 503 -> 538, both with `.bak_20260911T114003Z` backups and the
   assertion that every prior row is unchanged. The remote host was not touched.
4. `S/hladder/run.sh` plays **hr, B and A in our seat** against those 60 pinned-town opponent tapes in the
   shipped composition — worktree `ship-pair-hr`, `OPEN_PUMP_ON=True`, `KAGG3_TOWN_SCHEDULE=S/band2100p/...`,
   `--seed-per-opponent`, seed base 400778201 — exactly the switch/theta wiring `S/bladder/run.sh` used
   (`hr` = theta `flow172_g1000`, `B` = `flow193_g100_hr`, `A` = `flow187_g160_hr`). The runner plays every
   board in **both seats**; the live-fidelity row is the seat our agent actually held on Kaggle, and the
   both-seat count is reported separately.
5. `S/hladder/analyze.py` joins the legs to the Kaggle record -> `S/hladder/{rows.json,table.md,analysis.txt}`.

## Fidelity

**hr reproduces its own Kaggle W/L on 56 of 60 boards (93.3 %); coin-exact on 31/60.** The four misses:

| episode | opponent | rating | Kaggle | hr replay |
|---|---|---|---|---|
| 107674654 | kwon yong deuk | 2449 | L -65 | W +587 |
| 107764793 | King-damon | 2501 | L -1,631 | W +7,702 |
| 107770325 | AbhiniveshSharma5354 | 2557 | W +6,514 | L -12,011 |
| 107790346 | Toru59er | 2548 | L -350 | W +443 |

Three of the four are coin-flip margins (65, 350, 1,631 coins) — the end-of-day shop draw is the one piece of
board randomness a pinned-town tape does not remove, and it is worth +/-25k zero-mean. This is the same
fidelity level B's own board set showed (50/50 there, 25/50 coin-exact), i.e. the replay harness is sound and
the residual noise is the shop lottery, not a seating or tape defect.

## Totals (60 boards, our Kaggle seat)

| file | theta | record | mean margin |
|---|---|---|---|
| Kaggle (live, hr) | flow172_g1000 + pair/hr | 33W-27L | +3,590 |
| **hr** (replay) | flow172_g1000 | 35W-25L | +3,552 |
| **B** | flow193_g100_hr | **43W-17L** | **+5,131** |
| **A** | flow187_g160_hr | 40W-20L | +4,390 |

### Paired flips and sign tests

| comparison | board flips (our seat) | sign test | mean margin delta | t |
|---|---|---|---|---|
| **B vs hr** | **+10 / -2** | **p = 0.039** | **+1,579 coins** (SE 447) | **+3.53** |
| B vs hr, both seats (120 games) | +20 / -3 | p = 0.0005 | — | — |
| **A vs hr** | +7 / -2 | p = 0.180 | +838 coins (SE 456) | +1.84 |
| A vs hr, both seats (120 games) | +14 / -4 | p = 0.031 | — | — |
| B vs A | +5 / -2 | p = 0.45 | +741 coins (SE 288) | +2.57 |

B's ten gains are at ratings 2476, 2544, 2557, 2560, 2563, 2578, 2590, 2601, 2626, 2639 — spread across the
band, not concentrated at its bottom. B's two losses (107763467 @2584, 107775658 @2526) are the *same two*
boards A loses, so both candidates share one small regression pocket.

## Per band

| band | n | Kaggle | hr | B | A | hr margin | B margin | A margin |
|---|---|---|---|---|---|---|---|---|
| 2400-2499 | 11 | 6/11 | 7/11 | 8/11 | 9/11 | +2,261 | +3,441 | +3,463 |
| 2500-2599 | 40 | 23/40 | 24/40 | **28/40** | 25/40 | +4,069 | **+5,805** | +4,780 |
| 2600+ | 9 | 4/9 | 4/9 | **7/9** | 6/9 | +2,834 | **+4,204** | +3,791 |

B is ahead of hr in every band, and its largest relative gain is at **2600+** (4/9 -> 7/9) — the opposite of
the "B only looks good because it has been farming the 2200 band" hypothesis this measurement was built to
test. A improves on hr mainly in the 2400-2499 band and is roughly level with hr at 2500-2599.

## Verdict

**B is the stronger leaderboard file against the tier hr actually faces, and A is second.** On hr's own most
recent 60 ladder boards — the real 2426-2657 field, wins and losses in ladder order — B turns hr's 35W-25L
into 43W-17L: +10/-2 paired board flips (sign test p = 0.039), +20/-3 across both seats (p = 0.0005), and
+1,579 coins per board at t = +3.53. The edge is not a low-band artefact: it is largest at 2600+ (4/9 -> 7/9)
and clearly present at 2500-2599 (24/40 -> 28/40). A is directionally the same but weaker and not significant
on the seat we actually played (+7/-2, p = 0.18); B beats A head-to-head by +741 coins/board (t = +2.57) on
these boards. Nothing here contradicts the counter-class finding in the 2200 band — that concerned B's *own*
loss cluster against tomato-poor public-band clones, a class that does not appear in this 2500+ field. The
reading is: B's judge and ladder gains do carry into the tier that decides our rating, so B (already live as
sub 56161192) should stay, and the hr file is the one to retire when a slot is needed.

**Caveat — open-loop replays flatter the counterfactual columns.** The opponent tapes are byte-exact action
replays: they repeat the moves the opponent made *against hr*, and cannot react to anything B or A does
differently. hr's own column is the only one that is a true replay of a game that happened; B's and A's columns
are counterfactuals in which the opponent keeps playing hr's game. Every prior measurement of this kind has
found open-loop tapes overstate us (62 % paired vs 3-10 % live against the 2100 band), so the *size* of B's
+1,579 coins should be treated as an upper bound. What the design does buy is the paired sign test: hr, B and A
all face the identical frozen opponent on the identical pinned board with the identical seed, so the *ordering*
(B > A > hr) is the load-bearing result, not the absolute margins. The residual coin-flip risk is the shop
draw, which the 56/60 fidelity count prices at roughly 4 boards in 60.

## Per-board table

*Ladder order, oldest first. "seat" = the seat our agent held on Kaggle; margins are ours minus theirs.*

| # | episode | opponent | rating | band | seat | Kaggle | margin | hr | hr margin | B | B margin | A | A margin |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 107656052 | goh | 2567 | 2500-2599 | 0 | W | +8,071 | W | +8,233 | W | +7,068 | W | +6,499 |
| 2 | 107656809 | Sohshi Nakamura | 2601 | 2600+ | 0 | L | -2,167 | L | -2,167 | W | +156 | L | -2,080 |
| 3 | 107659697 | Sebastian Mateus | 2544 | 2500-2599 | 0 | L | -1,874 | L | -2,225 | W | +382 | L | -2,575 |
| 4 | 107660512 | ykhnkf | 2538 | 2500-2599 | 0 | L | -847 | L | -847 | L | -123 | L | -233 |
| 5 | 107661261 | Rotation Theory | 2557 | 2500-2599 | 0 | W | +10,014 | W | +10,255 | W | +8,563 | W | +9,515 |
| 6 | 107666058 | Ahmed Ansari | 2535 | 2500-2599 | 0 | W | +23,481 | W | +24,579 | W | +21,677 | W | +24,833 |
| 7 | 107670917 | Arul Prasad S P | 2578 | 2500-2599 | 0 | L | -742 | L | -644 | W | +495 | W | +608 |
| 8 | 107674654 | kwon yong deuk | 2449 | 2400-2499 | 1 | L | -65 | W | +587 | W | +493 | W | +1,520 |
| 9 | 107679724 | Shunsuke Hayashi | 2571 | 2500-2599 | 1 | W | +16,944 | W | +16,944 | W | +18,163 | W | +19,231 |
| 10 | 107683908 | kaguramena | 2445 | 2400-2499 | 0 | L | -9,279 | L | -9,135 | L | -10,244 | L | -10,705 |
| 11 | 107689582 | src | 2550 | 2500-2599 | 0 | W | +14,141 | W | +14,141 | W | +19,495 | W | +19,539 |
| 12 | 107691037 | Iwa Iwa | 2562 | 2500-2599 | 0 | L | -2,700 | L | -2,700 | L | -1,297 | W | +474 |
| 13 | 107696609 | 213tubo | 2533 | 2500-2599 | 0 | L | -7,611 | L | -7,611 | L | -10,771 | L | -12,515 |
| 14 | 107697593 | KodamaSec | 2526 | 2500-2599 | 1 | L | -4,220 | L | -4,220 | L | -4,790 | L | -7,191 |
| 15 | 107702473 | hatry | 2530 | 2500-2599 | 1 | W | +5,606 | W | +5,606 | W | +6,051 | W | +5,907 |
| 16 | 107702677 | Bardia Bahadori | 2476 | 2400-2499 | 1 | L | -165 | L | -165 | W | +710 | W | +5,869 |
| 17 | 107704608 | gamesu7107 | 2568 | 2500-2599 | 1 | L | -12,396 | L | -12,396 | L | -8,648 | L | -10,447 |
| 18 | 107705195 | Yuta Yamazaki | 2528 | 2500-2599 | 1 | W | +23,120 | W | +23,621 | W | +27,591 | W | +27,673 |
| 19 | 107705439 | Shun | 2478 | 2400-2499 | 0 | W | +2,479 | W | +2,479 | W | +5,659 | W | +5,770 |
| 20 | 107706936 | xiao xiongwei | 2551 | 2500-2599 | 0 | W | +26,213 | W | +26,213 | W | +29,586 | W | +26,830 |
| 21 | 107707090 | JustinLee | 2498 | 2400-2499 | 1 | W | +4,231 | W | +6,275 | W | +6,392 | W | +4,559 |
| 22 | 107712450 | 在高速上逆行是危险的 | 2426 | 2400-2499 | 0 | W | +460 | W | +1,772 | W | +4,105 | W | +3,530 |
| 23 | 107712501 | Lucas Boesen | 2588 | 2500-2599 | 0 | W | +8,475 | W | +8,475 | W | +12,920 | W | +15,266 |
| 24 | 107717823 | Van-Phuc Huynh | 2657 | 2600+ | 0 | W | +7,938 | W | +7,938 | W | +9,336 | W | +7,850 |
| 25 | 107718261 | akmr | 2528 | 2500-2599 | 1 | W | +13,304 | W | +11,749 | W | +20,193 | W | +16,858 |
| 26 | 107724129 | Forrest | 2534 | 2500-2599 | 0 | W | +3,196 | W | +3,196 | W | +3,307 | W | +3,855 |
| 27 | 107729297 | edteoh | 2590 | 2500-2599 | 0 | L | -962 | L | -962 | W | +1,444 | L | -3,124 |
| 28 | 107732164 | easonyanyan | 2560 | 2500-2599 | 0 | L | -242 | L | -242 | W | +917 | L | -667 |
| 29 | 107737990 | Yaojinming | 2563 | 2500-2599 | 0 | L | -595 | L | -595 | W | +1,170 | L | -133 |
| 30 | 107738911 | Joyal | 2626 | 2600+ | 1 | L | -1,525 | L | -1,546 | W | +87 | W | +632 |
| 31 | 107743508 | Satoshi Nguyen | 2596 | 2500-2599 | 0 | W | +8,548 | W | +8,548 | W | +8,654 | W | +5,084 |
| 32 | 107744147 | Fuat Çakıcı | 2447 | 2400-2499 | 1 | W | +16,342 | W | +17,510 | W | +21,207 | W | +20,388 |
| 33 | 107746922 | Quantum Farm | 2542 | 2500-2599 | 0 | L | -14,517 | L | -14,517 | L | -11,940 | L | -18,744 |
| 34 | 107752872 | Pai | 2472 | 2400-2499 | 1 | W | +7,883 | W | +8,171 | W | +6,609 | W | +5,128 |
| 35 | 107752878 | john inan | 2639 | 2600+ | 1 | L | -611 | L | -102 | W | +3,281 | W | +2,700 |
| 36 | 107757219 | Subin An | 2651 | 2600+ | 0 | L | -1,432 | L | -4,440 | L | -2,414 | L | -4,729 |
| 37 | 107757813 | Berat Egemen Gök | 2456 | 2400-2499 | 1 | L | -3,591 | L | -3,591 | L | -215 | W | +170 |
| 38 | 107760897 | Sohshi Nakamura | 2554 | 2500-2599 | 0 | W | +2,516 | W | +3,701 | W | +4,595 | W | +3,714 |
| 39 | 107763467 | 薄荷喵呜 | 2584 | 2500-2599 | 0 | W | +1,784 | W | +1,835 | L | -772 | L | -4,714 |
| 40 | 107763540 | Naru041104 | 2554 | 2500-2599 | 0 | L | -5,996 | L | -5,996 | L | -5,937 | L | -6,072 |
| 41 | 107764793 | King-damon | 2501 | 2500-2599 | 1 | L | -1,631 | W | +7,702 | W | +10,449 | W | +10,754 |
| 42 | 107768737 | GIVE ME A JOB | 2498 | 2400-2499 | 1 | W | +2,715 | W | +2,684 | W | +3,253 | W | +1,866 |
| 43 | 107770325 | AbhiniveshSharma5354 | 2557 | 2500-2599 | 0 | W | +6,514 | L | -12,011 | W | +8,431 | W | +6,135 |
| 44 | 107775658 | Ankit Hemant Lade | 2526 | 2500-2599 | 1 | W | +863 | W | +1,007 | L | -190 | L | -258 |
| 45 | 107777478 | Zhengxu Yu | 2562 | 2500-2599 | 1 | L | -3,212 | L | -2,677 | L | -2,932 | L | -2,808 |
| 46 | 107777651 | Lin | 2548 | 2500-2599 | 0 | W | +3,987 | W | +3,987 | W | +4,516 | W | +4,825 |
| 47 | 107781407 | Ken_Ken_Pa | 2579 | 2500-2599 | 1 | L | -16,093 | L | -16,041 | L | -12,807 | L | -10,391 |
| 48 | 107782511 | Aastik Rajan15 | 2574 | 2500-2599 | 1 | W | +20,647 | W | +20,767 | W | +14,941 | W | +16,635 |
| 49 | 107782986 | Jamie Nojek | 2543 | 2500-2599 | 1 | W | +6,363 | W | +6,363 | W | +8,396 | W | +7,407 |
| 50 | 107786171 | Michael Chen | 2531 | 2500-2599 | 0 | W | +12,021 | W | +12,021 | W | +15,748 | W | +13,987 |
| 51 | 107787487 | Артём Свинобоев | 2551 | 2500-2599 | 1 | W | +13,164 | W | +13,164 | W | +16,633 | W | +14,691 |
| 52 | 107787968 | Prashant Bhattarai093 | 2481 | 2400-2499 | 1 | L | -1,717 | L | -1,717 | L | -116 | L | -4 |
| 53 | 107790346 | Toru59er | 2548 | 2500-2599 | 1 | L | -350 | W | +443 | W | +1,152 | W | +583 |
| 54 | 107792763 | esis_ai | 2595 | 2500-2599 | 0 | L | -1,727 | L | -1,079 | L | -2,136 | L | -3,449 |
| 55 | 107795903 | 成吉思汗 | 2558 | 2500-2599 | 1 | W | +6,085 | W | +6,085 | W | +12,753 | W | +5,335 |
| 56 | 107799234 | simmons1025 | 2617 | 2600+ | 0 | W | +19,701 | W | +19,701 | W | +19,190 | W | +18,729 |
| 57 | 107800818 | RuiFSPinto | 2612 | 2600+ | 0 | W | +7,420 | W | +6,526 | W | +6,528 | W | +9,460 |
| 58 | 107801590 | Aaron amacadu | 2530 | 2500-2599 | 1 | W | +8,893 | W | +8,893 | W | +9,248 | W | +8,302 |
| 59 | 107806853 | Oleksandr Kovalchuk | 2611 | 2600+ | 0 | W | +2,410 | W | +2,410 | W | +5,869 | W | +2,133 |
| 60 | 107807058 | mech_39 | 2612 | 2600+ | 1 | L | -3,836 | L | -2,813 | L | -4,201 | L | -576 |
