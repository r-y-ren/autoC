# Candidate B on its own ladder boards: a real-engine paired re-play (2026-09-11 10:35-11:00Z)

## The question

Live submission **B** (sub 56161192, theta `artifacts/kagg2_games/thetas/flow193_g100_hr.npy`, package
`dist/submission_flow193_g100_hr.tar.gz`) was promoted over the previous live file **hr**
(sub 56143250, `dist/submission_flow172_pair_hr` = theta `flow172_g1000` + the pair/hr switches) because it
won our paired judge legs.  On the ladder B sits at 34W-16L, rating 2269 after 50 games, while hr passed
~2400 at 70 games and reads 2550 now.  **Is the judge miscalibrated -- would hr (or candidate A,
`flow187_g160_hr`, `dist/submission_flow187_g160_hr.tar.gz`) have done better on the boards B actually
played?**

## Method

1. `S/bladder/eps_raw.json` = the credential-free `ListEpisodes` record for sub 56161192, fetched
   2026-09-11 10:36Z.  It holds **50** completed non-validation games (34W-16L) -- one more than the 49 in
   the brief; game 50 (107792945, a loss) landed at 10:29Z.  All 50 are measured, wins and losses, no
   selection of any kind.  `S/bladder/ids.txt` = `<episode id> <our seat> <opponent seat>`.
2. For every episode the replay was downloaded (`S/bladder/dl.sh`, 40 new + 10 already on disk from the
   LOSS10 cut) and a **pinned-town action tape of the OPPONENT's seat** was cut with `S/bladder/cut_one.sh`
   (= `S/top50/cut_one.sh`): `scripts/tape_opponent.py --seat <opp> --with-town` +
   `scripts/make_tape_actions.py --with-town`.  All 80 tape lines report `verified`; the taped player is the
   opponent on all 50 boards (never OurTeam).  Logs: `S/bladder/cut/<ep>.out`.
3. Towns appended under the TOWN APPEND protocol (`S/bladder/town_append.sh`): `S/band2100p/town_schedules.json`
   463 -> 503, backup `.bak_20260911T104135Z`, all 463 prior rows asserted unchanged; then merged as a
   superset into `artifacts/town_schedules.json` 463 -> 503 (backup `.bak_20260911T104135Z`).  Logged as
   TOWN APPEND #8 / TOWN SYNC in `S/livec/provenance.txt`.  The remote host was not touched.
4. Three thetas were played in **our** seat against those 50 tapes in the shipped composition -- worktree
   `.claude/worktrees/ship-pair-hr`, switches `OPEN_PUMP_ON=True`, i.e. byte-for-byte the leg
   `S/bloss/run.sh` uses for the LOSS10 board set: **B** `flow193_g100_hr`, **hr** `flow172_g1000`,
   **A** `flow187_g160_hr` (all 6789 params, same worktree/switch class).  Seed base 400778201,
   `--seed-per-opponent`, `--games 1`, WORKERS=5, so every theta meets each board on the **same** seed:
   `S/bladder/run.sh` -> `S/bladder/{B,hr,A}.csv` (100 rows each = 50 boards x both seats).
   The LOSS10 rows were **not** reused: `seed_lists` keys the seed to the opponent's index in the list, so a
   50-board list draws different seeds than the 10-board list.  Analysis: `S/bladder/analyze.py`.

The per-board table below uses the row whose eval seat equals our seat in the live game; the "both seats"
line in the totals uses all 100 games per theta.

## Fidelity

**B reproduces the Kaggle W/L on 50 / 50 boards**, and reproduces the live score line **to the coin on
25 / 50**.  Median (B engine margin - Kaggle margin) is exactly 0; the mean is +392 coins and the largest
single deviation is 8,210.  The residue is the known shop lottery: the pinned town removes all board
randomness, but the end-of-day shop draw still follows our seed base, not the live one, so half the boards
drift a few hundred coins without ever crossing the win line.  For this measurement that is the ideal
outcome: the seat, the board and the opponent's actions are the live game's, and the W/L column is exact.

## Per-board table (sorted by opponent rating, descending)

| # | episode | opponent (rating) | band | Kaggle | B | hr | A | K margin | B margin | hr margin | A margin |
|--:|---|---|---|:--:|:--:|:--:|:--:|--:|--:|--:|--:|
| 1 | 107790945 | Mark Astrid (2392) | 2300-2499 | L | L | L | L | -6,172 | -6,172 | -6,323 | -4,884 |
| 2 | 107766829 | daulettoibazar (2381) | 2300-2499 | L | L | L | L | -1,468 | -1,468 | -2,251 | -1,612 |
| 3 | 107775976 | pig7selene (2348) | 2300-2499 | W | W | W | W | +27,242 | +27,242 | +26,972 | +32,215 |
| 4 | 107777972 | cha7ura (2334) | 2300-2499 | L | L | L | L | -3,451 | -2,781 | -3,676 | -3,836 |
| 5 | 107791734 | Artyom Lyan (2324) | 2300-2499 | L | L | L | L | -8,307 | -7,044 | -5,135 | -2,988 |
| 6 | 107788854 | zigiella (2320) | 2300-2499 | W | W | W | W | +2,919 | +2,919 | +1,439 | +3,538 |
| 7 | 107785953 | Aleksandr Ulianin (2312) | 2300-2499 | W | W | W | W | +7,803 | +7,803 | +6,218 | +7,886 |
| 8 | 107789956 | zigiella (2310) | 2300-2499 | W | W | W | W | +16,716 | +16,716 | +13,185 | +16,729 |
| 9 | 107776966 | Jacob Alstrup (2309) | 2300-2499 | W | W | W | W | +13,307 | +14,179 | +9,542 | +11,887 |
| 10 | 107779009 | Maksim Borisov (2300) | 2300-2499 | L | L | L | W | -917 | -56 | -1,671 | +222 |
| 11 | 107786955 | Malyshev Danil (2298) | 2100-2299 | L | L | L | W | -2,214 | -1,120 | -2,537 | +241 |
| 12 | 107792945 | s_a_ai_enginner (2288) | 2100-2299 | L | L | L | L | -99 | -99 | -349 | -562 |
| 13 | 107780983 | My second life (2284) | 2100-2299 | L | L | L | L | -4,655 | -4,597 | -2,522 | -1,798 |
| 14 | 107779976 | TOSS (2279) | 2100-2299 | L | L | L | L | -5,365 | -5,518 | -7,600 | -4,951 |
| 15 | 107782960 | Silhouette (2274) | 2100-2299 | W | W | W | W | +7,633 | +7,617 | +3,586 | +6,385 |
| 16 | 107777279 | Sōsuke Aizen (2272) | 2100-2299 | W | W | W | W | +2,798 | +2,850 | +1,931 | +944 |
| 17 | 107781955 | Kucing Garong (2269) | 2100-2299 | L | L | L | L | -3,203 | -6,295 | -1,208 | -6,516 |
| 18 | 107770990 | honjousetuna (2256) | 2100-2299 | W | W | W | W | +662 | +1,995 | +2,928 | +930 |
| 19 | 107784954 | kunihiro (2253) | 2100-2299 | W | W | W | W | +9,398 | +11,051 | +16,244 | +16,604 |
| 20 | 107767971 | David Goldrajch (2249) | 2100-2299 | W | W | W | W | +29,382 | +29,382 | +24,336 | +31,115 |
| 21 | 107765935 | Seho.Connect (2237) | 2100-2299 | W | W | W | W | +6,530 | +6,530 | +6,924 | +6,749 |
| 22 | 107791945 | Molood (2228) | 2100-2299 | L | L | L | W | -296 | -296 | -2,226 | +243 |
| 23 | 107783960 | Chirag Desai (2228) | 2100-2299 | W | W | W | W | +16,789 | +16,789 | +19,792 | +21,325 |
| 24 | 107772993 | ujimaa (2222) | 2100-2299 | W | W | L | L | +90 | +90 | -243 | -1,863 |
| 25 | 107769126 | dont share my work for (2220) | 2100-2299 | L | L | L | L | -3,530 | -3,530 | -4,526 | -3,549 |
| 26 | 107773986 | Xiangsong Tian (2217) | 2100-2299 | W | W | W | W | +10,188 | +10,188 | +7,665 | +9,748 |
| 27 | 107787963 | Karthik Nambiar (2206) | 2100-2299 | L | L | L | W | -174 | -174 | -1,863 | +474 |
| 28 | 107775056 | Savan Javia (2203) | 2100-2299 | W | W | W | W | +7,528 | +7,595 | +7,233 | +6,964 |
| 29 | 107764944 | Sinh Nguyễn Đức (2203) | 2100-2299 | L | L | L | L | -677 | -677 | -612 | -183 |
| 30 | 107772694 | way to you (2195) | 2100-2299 | W | W | L | L | +1,808 | +1,808 | -2,532 | -1,879 |
| 31 | 107769991 | JiangWenfeng1 (2188) | 2100-2299 | L | L | L | L | -4,661 | -4,661 | -6,645 | -3,430 |
| 32 | 107771992 | Variiiiiii (2175) | 2100-2299 | L | L | L | L | -8,544 | -9,000 | -12,296 | -8,899 |
| 33 | 107763934 | yarneo (2159) | 2100-2299 | W | W | W | W | +14,131 | +14,131 | +12,584 | +13,570 |
| 34 | 107766953 | Howon Kang (1995) | <2100 | W | W | W | W | +15,691 | +23,901 | +18,177 | +20,990 |
| 35 | 107762934 | infamemconculcemus (1942) | <2100 | W | W | W | W | +31,350 | +31,350 | +29,010 | +30,639 |
| 36 | 107761940 | peppersaltman (1877) | <2100 | W | W | W | W | +14,542 | +14,264 | +13,557 | +11,466 |
| 37 | 107762763 | Kometa (1785) | <2100 | W | W | L | W | +742 | +742 | -353 | +5,013 |
| 38 | 107759976 | kiyomiya-k (1730) | <2100 | W | W | W | W | +10,112 | +10,105 | +11,922 | +11,960 |
| 39 | 107760962 | Sridip Basu (1700) | <2100 | W | W | W | W | +4,715 | +4,763 | +5,658 | +5,045 |
| 40 | 107759008 | Ak (1614) | <2100 | W | W | W | W | +14,517 | +14,517 | +12,844 | +12,804 |
| 41 | 107758033 | chacha260 (1419) | <2100 | W | W | W | W | +19,118 | +19,139 | +18,125 | +19,244 |
| 42 | 107757048 | huayang sun (1401) | <2100 | W | W | W | W | +34,854 | +34,854 | +30,618 | +31,556 |
| 43 | 107756078 | Ryuuga89 (1300) | <2100 | W | W | W | W | +53,488 | +53,488 | +48,314 | +50,338 |
| 44 | 107755101 | Fire Bird (1012) | <2100 | W | W | W | W | +10,833 | +12,005 | +12,460 | +12,272 |
| 45 | 107754127 | Bruce Cole (994) | <2100 | W | W | W | W | +24,786 | +29,576 | +25,365 | +27,015 |
| 46 | 107752189 | lmq (821) | <2100 | W | W | W | W | +35,981 | +36,173 | +35,849 | +39,513 |
| 47 | 107753152 | Clement Ling (786) | <2100 | W | W | W | W | +32,590 | +32,514 | +24,992 | +28,485 |
| 48 | 107751214 | Abdalrahman Eissa (732) | <2100 | W | W | W | W | +48,885 | +50,206 | +51,122 | +49,773 |
| 49 | 107750239 | Vespidae (708) | <2100 | W | W | W | W | +61,444 | +61,444 | +57,041 | +60,943 |
| 50 | 107749280 | Dmitri Bugakov (580) | <2100 | W | W | W | W | +76,326 | +76,305 | +72,752 | +75,024 |

## By opponent rating band

The 2500+ band is **empty** -- the strongest opponent B has drawn is Mark Astrid at 2392, and 17 of the 50
games are placement games against sub-2100 opponents, so a `<2100` row is added rather than dropping them.

| band | n | Kaggle | B | hr | A | mean margin B | hr | A |
|---|--:|:--:|:--:|:--:|:--:|--:|--:|--:|
| <2100 | 17 | 17-0 | 17-0 | 16-1 | 17-0 | +29,726 | +27,497 | +28,946 |
| 2100-2299 | 23 | 12-11 | 12-11 | 10-13 | 13-10 | +3,220 | +2,525 | +3,551 |
| 2300-2499 | 10 | 5-5 | 5-5 | 5-5 | 6-4 | +5,134 | +3,830 | +5,916 |
| 2500+ | 0 | - | - | - | - | - | - | - |
| **2100+ (all rated games)** | **33** | **17-16** | **17-16** | **15-18** | **19-14** | **+3,800** | **+2,920** | **+4,267** |

## Totals and sign tests

| theta | record over the 50 boards | mean margin | flips vs B (board rows) | sign test | flips vs B (both seats, 100 games) | sign test |
|---|:--:|--:|:--:|--:|:--:|--:|
| B `flow193_g100_hr` | **34W-16L** (= its Kaggle 34-16) | +12,615 | - | - | 68W / 100 | - |
| hr `flow172_g1000`+pair+hr | **31W-19L** | +11,276 | +0 / -3 | p = 0.250 | 62W, +0 / -6 | **p = 0.031** |
| A `flow187_g160_hr` | **36W-14L** | +12,658 | +4 / -2 | p = 0.688 | 72W, +8 / -4 | p = 0.388 |

Paired margin (same board, same seed, our seat): **hr - B = -1,339 coins/game (SE 363, t = -3.68)**;
**A - B = +43 coins/game (SE 313, t = +0.14)**.

The six boards that move (per-board rows):

```
FLIP hr: ep 107762763 Kometa (1785)          B W (+742)   -> hr L (-353)
FLIP hr: ep 107772694 way to you (2195)      B W (+1808)  -> hr L (-2532)
FLIP hr: ep 107772993 ujimaa (2222)          B W (+90)    -> hr L (-243)
FLIP A:  ep 107772694 way to you (2195)      B W (+1808)  -> A  L (-1879)
FLIP A:  ep 107772993 ujimaa (2222)          B W (+90)    -> A  L (-1863)
FLIP A:  ep 107787963 Karthik Nambiar (2206) B L (-174)   -> A  W (+474)
FLIP A:  ep 107791945 Molood (2228)          B L (-296)   -> A  W (+243)
FLIP A:  ep 107786955 Malyshev Danil (2298)  B L (-1120)  -> A  W (+241)
FLIP A:  ep 107779009 Maksim Borisov (2300)  B L (-56)    -> A  W (+222)
```

## Verdict

**The judge is not falsified by B's ladder record.**  Re-played on B's own 50 boards, in B's own seat,
against the opponents' own action tapes, **hr wins fewer games than B, not more**: 31-19 against B's 34-16,
zero boards gained and three lost per-board (six lost and none gained across both seats, sign test
p = 0.031), and it gives up 1,339 coins/game paired (t = -3.68).  There is no board in the set where hr
rescues a game B lost.  A is level with B and possibly a shade better -- 36-14, +4/-2 flips (p = 0.69) and
+43 coins/game (t = +0.14) -- which is exactly the "A and B are hard to separate" reading the promotion legs
gave; four of A's six moved boards are B losses by 56-1,120 coins that A converts by 222-474 coins, i.e.
coin-flip boards, not a class B cannot handle.  So B's 2269 is not evidence that our judge picked the wrong
file.  The rating gap is an Elo-history artefact: 17 of B's 50 games are placement wins against sub-2100
opponents that pay almost no rating, B has played 50 games to hr's 70+, and on the 33 games that were
against 2100+ opponents B is 17-16 -- a file sitting near the middle of the 2100-2300 crowd it keeps being
matched into, which is what LOSS10 already said about the 2200 counter class.  **Caveats, stated plainly:**
(1) the whole measurement is against **open-loop replays** -- every opponent here repeats its live actions
and cannot react to hr's or A's different play, so the hr/A columns are optimistic in exactly the way the
tape-fidelity note warns; (2) 50 boards with 3-9 moving games is thin -- only the hr both-seat sign test
(p = 0.031) and the hr paired margin (t = -3.68) clear noise, the A comparison does not; (3) the band split
leaves 10 games in 2300-2499 and none above 2500, so nothing here says which file is better against the
top-10 class we are actually chasing.

## Files

`S/bladder/` -- `ids.txt` (50 boards), `meta.json` + `eps_raw.json` (Kaggle record), `dl.sh` + `eps/`
(replays), `cut_one.sh` / `cut_all.sh` + `cut/` (tape cuts), `town_append.sh`, `run.sh` (the three legs),
`B.csv` `hr.csv` `A.csv` (100 rows each), `analyze.py`, `rows.json`, `analysis.txt`, `flips.txt`,
`table.md`, `run.out`.
