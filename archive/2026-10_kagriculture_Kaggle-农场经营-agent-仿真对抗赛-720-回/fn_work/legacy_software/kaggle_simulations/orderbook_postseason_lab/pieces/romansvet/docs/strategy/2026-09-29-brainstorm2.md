# BRAINSTORM2 (2026-09-29): beat the top 5 - session 2

User order 07:00Z: brainstorm with an Opus agent until a solid way into the top 5 (or top 10) is found; 09:19Z: sessions of 3 rounds, then a
summary and a fresh session. Session 1 closed with the open line "PFS's own d0 mix + the programme's d1-9 policy" (docs/strategy/2026-09-29-brainstorm1.md).
Files: S/brainstorm2/ (round1.md, res/, logs/, checkpoint.txt). Worktree /mnt/e/_work/kagg3_wt_brainstorm2, branch brainstorm2_0929 (from 8d670dad).

## Round 1 (09:24:44Z - 11:54:44Z): FEED_ALL + REINVEST_DAILY on PFS's own d0 mix

### Step 1: arithmetic (exact, main-42 live replays, PFS seat vs programme rivals >= 2,450)
* **Engine rule** (kaggriculture.py L805-833): an unfed animal still makes its base unit; only the care bonus is lost (it is added only on a
  FED production day and reset on every production day); fertilizer is available every night fed or not; the first production caps the bonus
  (max_held), so the placement-day and d2 unfed days of a d0 cow are free. Two unfed days in a row = escape.
* **Unfed days in coins**: feeding every unfed d0-9 animal-day is worth **-213..-302 coins/game** (bonus units saved 55-145 vs 358 of wheat);
  d10-17 -48..-331. PFS's d2 (3.6) and d6 (2.2) unfed days are cheap on purpose.
* **Escapes**: d1-16 3 in 42 games, all on d7 (2 cows, 1 goose) = <= ~125 coins/game. (d17-24: ~40 animals in 12 games on product troughs =
  the VRP's care_pays test; FEED_FORWARD_ON is the default-off answer; not this line.)
* **Cash path** (future-min purse from day d h1 to d10 h1): no room for a 500-coin sheep before d8 at reserve 200 (P(>=1) d1-4 0.00, d5 0.07,
  d6 0.12, d7 0.33, d8 0.98, d9 0.98; at reserve 400 0 before d8); a cow fits d6 0.60 / d7 0.86. The d10 lump (Q3 + ~5 animals) is paid by the
  first milk: 22 MILK harvested d8 h7-8, carried in the hands and banked overnight (shed d9 h0), sold 4.9 at d9 h1 + 17.2 at d9 h17 (3,288
  coins; quote flat 196 -> 200); the programme harvests its first milk d8 h1 and sells it d8. => daily reinvestment from dawn cash has little
  to work with before d8; the only way to buy it a day earlier is to bank + sell the first milk on d8.

### Step 2: build (worktree kagg3_wt_brainstorm2, branch brainstorm2_0929: 29a30244, e857d9e2, 245f1609)
* `REINVEST_DAILY="<from_day>:<reserve>[:<order>]"` (port of the BRAINSTORM1 r4 draft): from from_day through d9, whenever dawn money -
  reserve - today's feed bill covers an animal, the affordable part of PFS's own d14 herd (SHEEP 8, COW 7, GOOSE 4) in lane order (default
  S,C,G; "CSG" = cows first) is floored into `animal_want`, passes the spot gate like HERD_PLAN, and its lanes are granted at the value cap.
* `FEED_ALL` (bool): the feed-wheat list (one wheat per passing feed) is granted at the value cap before every other list. Not needed for
  PFS alone (step 1), built at 10:36Z because REINVEST's animal lanes priced the feed wheat out (28 escapes d0-10 in 80 games at 4:400:
  the d0 goose and day-old cows unfed two days running on d7-8).
* OFF = "" / False: bs2_id_gcf 6/6 exact vs jr_g0capsfix_pfs; after FEED_ALL was added, bs2_id2_gcf 6/6 exact again.

### Step 3: state log (3 boards x 2 seats vs g0capsfix, S/brainstorm2/res/state_*.txt)
* 4:400: the designed sequence runs: d5 h1 S2 (the control buys C1) with Q2 still bought at d5 h3 (the h1 wheat sale funds it), d8 S3,
  d9 S1; herd d9 C4.3 S6.7 G1.0 vs C5.0 S2.3 G3.3; Q3 d9 -> d10 on one board; 1 goose escape (d7).
* 2:200 == 4:200 exactly and 2:400 == 4:400 on 20/20 screen games: from_day 2 vs 4 is inert (dawn d2 127 / d3 627 never covers price +
  reserve + feed). The 200 reserve without FEED_ALL starves the feed (fed 6/10 on d6): 8 escapes in 6 games.
* GO (no cash wall, the buys land on d5/d8/d9 as designed); escapes handled by FEED_ALL.

### Step 4: grid (g0capsfix unless named; 20-game screen = m40 boards 1-10 x both seats, paired vs jr_g0capsfix_pfs; 80 g = all 40 boards)
| cell | n | ours | rival | margin | d-ours (t) | d-rival (t) | d-margin (t) | W vs ctl | flips | herd d9 C/S/G | escapes d0-10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| control PFS (first 10 boards) | 20 | 109,563 | 84,533 | +25,030 | - | - | - | 18 | - | 6.1/3.4/1.7 | 0 |
| 4:200 (= 2:200), state log | 6 | 116,175 | 85,954 | +30,221 | -1,599 (-1.03) | +4,544 (+2.62) | -6,144 (-1.89) | 6 vs 6 | 0/0 | 4.3/6.3/2.0 | 8 |
| 4:200 (= 2:200), 20 g | 20 | 112,662 | 88,617 | +24,045 | +3,099 (+3.29) | +4,084 (+2.29) | -985 (-0.41) | 20 vs 18 | +2/-0 | 4.7/6.2/2.9 | 12 |
| 4:400 (= 2:400) | 20 | 114,747 | 86,698 | +28,049 | +5,184 (+7.71) | +2,165 (+1.40) | +3,018 (+1.96) | 20 vs 18 | +2/-0 | 4.8/6.0/1.4 | 4 |
| 4:600 | 20 | 114,268 | 86,660 | +27,608 | +4,705 (+6.00) | +2,127 (+2.18) | +2,578 (+3.31) | 18 vs 18 | 0/0 | 5.5/5.0/2.0 | 6 |
| 4:800 | 20 | 113,988 | 85,613 | +28,375 | +4,425 (+3.40) | +1,081 (+0.83) | +3,345 (+2.63) | 20 vs 18 | +2/-0 | 5.4/4.8/1.8 | 2 |
| 4:400:CSG (cows first) | 20 | 111,884 | 85,197 | +26,687 | +2,321 (+3.33) | +664 (+0.74) | +1,657 (+1.33) | 18 vs 18 | 0/0 | 7.1/3.8/1.8 | 12 |
| 4:200 + FEED_ALL | 20 | 116,120 | 85,343 | +30,777 | +6,557 (+8.65) | +810 (+0.44) | +5,747 (+3.14) | 20 vs 18 | +2/-0 | 4.8/6.0/2.6 | 0 |
| 4:400 + FEED_ALL | 20 | 113,428 | 88,296 | +25,132 | +3,865 (+5.89) | +3,763 (+2.24) | +102 (+0.06) | 18 vs 18 | 0/0 | 4.8/6.0/1.4 | 0 |
| 4:600 + FEED_ALL | 20 | 113,043 | 85,230 | +27,813 | +3,480 (+3.52) | +697 (+0.49) | +2,782 (+1.30) | 18 vs 18 | 0/0 | 5.8/5.0/2.0 | 0 |
| 4:400:CSG + FEED_ALL | 20 | 110,973 | 85,513 | +25,459 | +1,410 (+1.40) | +981 (+0.93) | +429 (+0.25) | 18 vs 18 | 0/0 | 7.1/3.9/2.0 | 0 |
| **4:400, 80 g** | 80 | 118,376 | 92,773 | +25,603 | +3,207 (+4.98) | +2,556 (+3.35) | **+651 (+0.61)** | 78 vs 75 | +3/-0 | 5.0/6.0/1.4 | 28 |
| **4:600, 80 g** | 80 | 116,708 | 92,224 | +24,484 | +1,539 (+2.37) | +2,006 (+3.42) | **-468 (-0.58)** | 74 vs 75 | 0/-1 | 5.3/4.8/2.1 | 14 |
| **4:200 + FEED_ALL, 80 g** | 80 | 120,006 | 94,010 | +25,995 | +4,837 (+7.81) | +3,793 (+3.53) | **+1,044 (+0.76)** | 79 vs 75 | +4/-0 | 4.7/6.3/2.5 | 0 |
| flood 4:400 (20 g, ctl jr2_pfs_fl == ms_ctl_fl 20/20) | 20 | 117,343 | 79,819 | +37,524 | **-2,087 (-1.09)** | +4,726 (+3.59) | -6,812 (-2.50) | 20 vs 20 | 0/0 | | |
| flood 4:200 + FEED_ALL (20 g) | 20 | 116,624 | 80,878 | +35,746 | **-2,805 (-1.35)** | +5,785 (+2.08) | -8,591 (-2.07) | 20 vs 20 | 0/0 | | |
(control 80 g: 115,169 / 90,217 / +24,952, W 75/80.)  Screens on boards 1-10 overstate: 4:400 +3.0k -> +0.65k at 80 g, 4:600 +2.6k -> -0.5k, 4:200F +5.7k -> +1.0k.

Product ledger (80 g, arm - control, d10-29): 4:400 ours STRAW +2.7k, WOOL +2.2k, MILK -1.0k, EGG -0.4k; rival MILK +3.3k, STRAW +1.3k,
WOOL -1.5k. d10-17 is negative for us in every cell (-1.5..-2.8k: the d6-9 seed coins went into animals), d18-29 positive (+3.3..+6.9k).
Worst board (dipamchakrabor_114097777): our milk -76 u, the rival's milk +25 u at +16.3k -> sheep-first crowds out PFS's own d5 cow
(herd d9 C4.8 vs C6.1) and our missing milk is the rival's price.

### Faithful live27 tapes (27 seats, local, vrp20 package + the patched plan.py; the tape rival's SALES do not react, only its prices)
| cell | JC1-faithful n | W live -> pkg | flips | dours (t) | dtheirs (t) | dmargin (t) |
|---|---|---|---|---|---|---|
| 4:400 | 23 | 6 -> 6 | +1/-1 | +1,707 (+1.55) | +2,650 (+1.94) | -943 (-0.63) |
| 4:600 | 23 | 6 -> 7 | +1/-0 | +1,458 (+1.81) | +2,664 (+2.95) | -1,206 (-1.05) |
| 4:400:CSG | 24 | 6 -> 6 | +1/-1 | +458 (+0.51) | +930 (+1.33) | -472 (-0.61) |
| 4:400 + FEED_ALL | 25 | 6 -> 6 | +1/-1 | +93 (+0.07) | +2,751 (+1.84) | -2,659 (-1.45) |
| 4:200 + FEED_ALL | 21 | 6 -> 5 | +0/-1 | +515 (+0.33) | +6,432 (+2.75) | -5,916 (-2.40) |
(all 27 incl. the broken istinetz/ai tapes read W 6 -> 8..11 and are not counted, PRICEFAITH1 rule.)

### Verdict round 1: NONE (NOT YET)
* Step 1: FEED_ALL alone has negative value (-213..-302/game; the engine pays the base unit unfed and caps the pre-yield bonus); the d10 lump
  cannot be bought from dawn cash before d8 (future-min purse); REINVEST_DAILY still runs because it takes the d6-9 seed coins (d10-17 window
  -1.5..-3.1k in every cell) and turns them into sheep.
* The mechanism is real for OWN coins: every reserve >= 400 cell and every FEED_ALL cell adds +1.5..+6.6k own (80 g: 4:400 +3.2k t 5.0,
  4:600 +1.5k t 2.4, 4:200F +4.8k t 7.8; flips +3/-0, 0/-1, +4/-0), and FEED_ALL removes the escapes (28 -> 0 per 80 g).
* It is not a margin: the rival gains back +2.0..+3.8k (80 g, t 3.4-3.5), mostly MILK (+2.2..+4.4k) and strawberry, because the sheep-first
  lanes crowd out PFS's own d5-8 cows (d9 cows 4.7-5.3 vs 6.1) and our missing milk is the rival's price (invariant 3). Cows-first (CSG)
  keeps the milk book (rival milk -1.7k) but loses the wool and the escapes rise (12/20 g) -> +1.7k / +0.4k with FEED_ALL.
* Bars: CANDIDATE needs g0capsfix margin t >= 2 at 80 g: best 4:200F +1,044 (t 0.76). Faithful tapes: W not higher in any cell (6 -> 5..7),
  margin -0.5..-5.9k. Flood own coins: 4:400 -2.1k (t -1.09), 4:200F -2.8k (t -1.35), margins -6.8k / -8.6k (the flood rival takes the late strawberry our sheep coins bought). -> NONE; the 20-game screens on boards 1-10 overstated by 2.5-4.7k.
* Named failure kept: 4:200 without FEED_ALL = escapes (8 in 6 games); 20-g screen own +3.1k, rival +4.1k, margin -1.0k (t -0.41), 12 escapes: FEED_ALL is what makes the low reserve work.

### Round-2 proposal (to the orchestrator)
1. The lever must add our late volume WITHOUT cutting our milk: REINVEST 4:200F with PFS's own cow buys held (sheep only from the coins left
   after the control's day plan, not by outranking it), judged on the same 80 g + flood + tapes.
2. LUMP9 (timing, zero composition change): PFS harvests its first milk d8 h7-8 but carries it until the overnight bank, sells it d9 h17
   (3.3k, quote flat); a d8-only bank-before-lot-3 excursion sells it d8 h17, so the d9 h0 plan holds the d10 lump (Q3 + ~5 animals placed a
   day earlier). State log first (d9 dawn purse, Q3 day), then the grid.

Rule note: two local shell lines used bash process substitution (a `diff <(true) <(true)` no-op at 10:02Z and one `cmp <(cut ...) <(cut ...)`
at 10:29Z); both local, read-only, nothing else under /dev was touched; every later check used files.

## Round 2 (11:27Z - 13:00Z): LUMP9, additive reinvestment, and the cows-kept priority (orchestrator's grid + one named replacement)

### Build (worktree kagg3_wt_brainstorm2: 0c09c4fb, 60c34bd3, 45e8c838; all default off)
* `BANK_LATE_DAYS="8"` = LUMP9: on d8 the BANK_BEFORE_LOT excursion may deposit up to the last lot (turn 18, the ENDROUTE2_SPLIT deadline) and the
  banked units go on that lot. `BANK_LATE_MAX_TURNS` / `BANK_LATE_MIN_VALUE` (17 / 200) turned out INERT: L2 == L on 80/80 rows.
* `REINVEST_ADDITIVE`: no macro floor, no spot-gate floor, no value-cap priority; after the day's grant, the coins it left (the purse is already
  net of hires, the cash reserve and the land gap) minus REINVEST's reserve buy the herd deficit; the stock want is raised so structures follow.
* `REINVEST_ALL_LANES` (named replacement for LA2, 11:52Z): round 1's priority REINVEST, but on a live day EVERY animal lane goes to the value
  cap, so PFS's own cow and goose buys keep their place in front of the seeds (at equal value the greedy takes goose 300 < cow 400 < sheep 500).
* Harness: the chain now runs `rcr.py` -> `rc.py` with `RC_FWD_SOCK` (JUDGEGPU1 server, 2 workers, N 40): OFF identity 6/6 exact on the new path;
  40 games per worker in ~7 min.

### State log (3 boards x 2 seats vs g0capsfix; res/state_r2_LA.txt; d8/d9 income from the per-step money log)
* The fast-env control already banks part of the first milk at d8 h10 (990-1,166 coins on these boards). LUMP9 moves that bank to d8 h17 and
  adds +1.15k on 1 board; d9 dawn cash +0.9..+1.1k with LUMP9 alone, and Q3 lands on d9 on 3/3 boards (control d9/d10/d10). GO.
* With ADDITIVE on top, the d8 leftover buys sheep and the d9 purse falls below Q3 on 2 of 3 boards (Q3 d9 -> d10): coins "left after the
  day's plan" are tomorrow's Q3/lump coins.

### Grid (80 g vs g0capsfix = m40 x both seats; paired vs jr_g0capsfix_pfs and vs round 1's 4:200+FEED_ALL)
| cell | ours | rival | margin | d-ours (t) | d-rival (t) | d-margin (t) | W vs 75 | flips | herd d9 C/S/G | dawn cash d8 / d9 / d10 | Q3 on d9 | escapes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| control PFS | 115,169 | 90,217 | +24,952 | - | - | - | 75 | - | 6.1/3.4/1.7 (20 g) | 2,071 / 1,805 / 5,715 (20 g) | 2/20 | 0 |
| r1 4:200+FEED_ALL (priority, sheep first) | 120,006 | 94,010 | +25,995 | +4,837 (+7.81) | +3,793 (+3.53) | +1,044 (+0.76) | 79 | +4/-0 | 4.7/6.3/2.5 | 2,122 / 1,195 / 5,434 | 7/80 | 0 |
| **L = LUMP9 alone** (== L2) | 115,441 | 90,469 | +24,971 | +272 (+0.59) | +252 (+0.54) | +20 (+0.04) | 72 | +0/-3 | 6.3/3.8/1.6 | 2,104 / 2,657 / 4,282 | 34/80 | 6 |
| **LA = LUMP9 + ADDITIVE 4:200 + FEED_ALL** | 112,826 | 89,875 | +22,951 | -2,343 (-3.61) | -343 (-0.53) | -2,001 (-2.82) | 77 | +3/-1 | 6.7/4.0/1.8 | 2,123 / 2,582 / 3,837 | 28/80 (10 after d10) | 0 |
| **LAC2 = same, cows first** | 112,552 | 90,204 | +22,348 | -2,617 (-3.85) | -14 (-0.02) | -2,604 (-3.59) | 77 | +3/-1 | 6.9/3.9/1.9 | 2,123 / 2,677 / 3,700 | 32/80 (10 after d10) | 0 |
| **LP = LUMP9 + 4:200 + ALL_LANES + FEED_ALL** | 117,264 | 90,040 | +27,224 | **+2,095 (+3.09)** | -177 (-0.25) | **+2,272 (+2.34)** | 73 | +1/-3 | 6.8/3.8/3.6 | 2,123 / 2,523 / 3,760 | 43/80 | 0 |
| LP vs r1 4:200+FEED_ALL | | | | -2,742 (-3.12) | -3,970 (-4.30) | +1,229 (+0.99) | 73 vs 79 | +0/-6 | | | | |
| LP flood (80 g, ctl jr2_pfs_fl) | 124,924 | 78,910 | +46,014 | **+794 (+0.86)** | +1,860 (+1.43) | -1,066 (-0.57) | 80 vs 80 | 0/0 | 6.7/3.6/3.9 | | 47/80 | 0 |
| LP big (40 g = boards 1-20, ctl bm_pfs) | 119,123 | 75,415 | +43,708 | +3,927 (+3.25) | +2,194 (+2.31) | +1,733 (+1.35) | 40 vs 40 | 0/0 | 6.5/4.3/3.0 | | 16/40 | 0 |

LP's three lost games (+1/-3) are kuengo_114130181 s0 and two yannikschiffne seats (own -7.8k / -14.0k / -11.8k); on kuengo LUMP9 alone loses it
too, and there LP slips Q3 to d11.

### Per-book purse split (arm - control, coins/game; ours d0-9 / d10-29 | rival d0-9 / d10-29), 80 g vs g0capsfix
| book | r1 4:200+FEED_ALL | LP | LA | L |
|---|---|---|---|---|
| MILK | -30 / -1,849 \| +200 / **+4,407** | -69 / -716 \| +115 / **-839** | -53 / -380 \| -28 / -43 | -72 / +516 \| +96 / -317 |
| STRAWBERRY | 0 / +3,249 \| 0 / +2,448 | 0 / +2,160 \| 0 / +767 | 0 / -726 \| 0 / +282 | 0 / -212 \| 0 / +182 |
| WOOL | +1 / +2,941 \| +84 / -2,068 | +9 / -296 \| +7 / +955 | -1 / -1,265 \| +110 / -664 | 0 / -325 \| -19 / +310 |
| FERTILIZER | +495 / +511 \| +16 / -757 | +468 / +782 \| -52 / -884 | -10 / +49 \| -22 / -47 | 0 / +56 \| -25 / +28 |
| EGG | +137 / +1,024 \| 0 / +19 | +137 / +2,732 \| 0 / -271 | +51 / -123 \| 0 / +248 | 0 / -3 \| 0 / -2 |
| MELON | 0 / +576 \| 0 / -646 | 0 / -154 \| 0 / -209 | 0 / +158 \| 0 / -74 | 0 / +46 \| 0 / -116 |
| WHEAT | -135 / -158 \| -2 / +405 | -144 / -305 \| -3 / +375 | -56 / +474 \| +2 / +212 | -24 / -221 \| +2 / +617 |
| CARROT / TOMATO | -22 / -797 \| 0 / -363 | -22 / -1,190 \| 0 / -163 | 0 / -312 \| 0 / -42 | 0 / +235 \| 0 / -168 |
* d0-9 moves in no cell by more than +0.5k (fertilizer +0.47-0.50k, egg +0.14k): with PFS's purse the d1-9 books are out of reach (step 1).
* The rival's take-back in round 1 was MILK-LED (+4.4k of +7.2k gross; strawberry +2.4k; wool -2.1k and fertilizer -0.8k back to us). Keeping
  PFS's cows in front (LP) turns the rival's milk to -0.8k and its net to -0.2k on g0capsfix. On flood the rival still takes +1.9k (strawberry
  +2.3k, wheat +1.1k; milk -1.3k); on big +2.2k (strawberry +2.6k).

### Faithful live27 tapes (27 seats, vrp20 package + patched plan.py; the tape rival's sales do not react)
| cell | faithful n | W live -> pkg | flips | dours (t) | dtheirs (t) | dmargin (t) |
|---|---|---|---|---|---|---|
| LA (v1) | 24 | 6 -> 8 | +2/-0 | +744 (+1.21) | +285 (+0.44) | +458 (+0.47) |
| LA2 (== LA by the L2 identity) | 24 | 6 -> 8 | +2/-0 | +619 (+0.95) | +255 (+0.40) | +364 (+0.36) |
| LP | 22 | 6 -> 5 | +0/-1 | +602 (+0.62) | +2,033 (+2.37) | -1,432 (-1.49) |
| L (LUMP9 alone) | 27 | 6 -> 6 | +0/-0 | -126 (-0.58) | -334 (-2.07) | +209 (+0.76) |
| LAC2 | 24 | 6 -> 7 | +2/-1 | +100 (+0.12) | +469 (+0.76) | -369 (-0.34) |

### Verdict round 2
* LUMP9 is worth ~0 (+0.27k own, +20 margin at 80 g). The fast-env control already banks part of the first milk on d8, and a one-day-earlier
  lump only moves timing, not the herd.
* ADDITIVE reinvestment is NEGATIVE: LA -2.3k own (t -3.6), cows first LAC2 -2.6k (t -3.9), margin -2.0k / -2.6k. The coins left after today's plan are tomorrow's Q3/lump coins; round 1's own-coin gain
  came from displacing d6-9 SEED coins.
* **LP (priority reinvest with PFS's cows kept)** meets the orchestrator's bar: g0capsfix own +2,095 (t 3.09) with margin +2,272 (t 2.34) >= 0,
  flood own +794 >= 0, big own +3.9k (t 3.25) / margin +1.7k. It does not meet my round-1 CANDIDATE bar on the tapes: faithful W 6 -> 5,
  dtheirs +2.0k. Flips on g0capsfix are +1/-3 despite the mean margin. The gain is eggs and fertilizer (geese first at equal value: d9 G3.6 vs
  1.7) plus strawberry, with no milk gift. -> **PROMISING, not CANDIDATE**: margin is positive on 2 of 3 reacting rivals, W is not up anywhere.

### Answer to the orchestrator's hypothesis
The take-back is **milk-led, not milk-only**. Round 1's rival gained +4.4k in milk and +2.4k in strawberry, and gave back 2.1k of wool and
0.8k of fertilizer (net +3.8k). Keeping PFS's cows (LP) cuts the rival's milk to -0.8k and its net to -0.2k on g0capsfix. A strawberry/wheat
take-back stays: +0.8k on g0capsfix, +3.3k on flood, +2.6k on big. d1-9 books move by <= +0.5k in every cell.

### Round-3 proposal
1. Replicate LP on a fresh board set (m76 / band) and on the live27 closed loop vs g0capsfix.
2. Take LUMP9 out (it is ~0), and run the reserve {200, 400} x {ALL_LANES} grid.
3. Look at LP's three lost games (Q3 slips to d11 on kuengo) and add a Q3 guard (no reinvest buy that pushes the d9 purse below the Q3 price).
   If it holds, package it for the user's slot decision.

## Round 3 (12:28Z - 14:10Z): LP + Q3 guard, same-hour fills (POSTFILL), on FRESH boards (m76 1-40 x 2 seats)

### Build (worktree kagg3_wt_brainstorm2: e23167ae, b7a89977; default off)
* `REINVEST_Q3GUARD=<day>`: from that day, while nquad < 3, the REINVEST budget keeps back the next quadrant's price.
* `POSTFILL="A"|"AL"` (the same-hour probe; PORTGAP1 / ASTRA_BS1 cell C). The fact behind it: PFS's h1 (TURN_BUY) row already SELLS lot 1
  FIRST and buys after it, and the engine commits the queue in order with money checked per unit. So lot-1 proceeds can pay for that row's
  buys, but the grant counted them only for BUY_LAND's gap (3/4 of the projection).
  * "A": on d2-9 without a land buy, a second animal-only walk spends what the grant left plus `rev1` on the herd deficit.
  * "AL": the land gap also counts the full projection.
  * `POSTFILL_KEEP_FROM=2` keeps the next quadrant's price.
  * As astra noted, this reacts to the h1 row's own fills only, not to afternoon receipts.
* OFF identity on m76 through this harness: bs2r3_id76 6/6 exact vs m76_ctl (DAGGER1 r0m76).

### State log (m76 boards 1-3 x 2)
* G (LP + Q3 guard at d8): Q3 on d9 on 3/3 boards (control d10), no slip, d9 cash 3.0-3.6k. GO.
* PFA without the land keep: the d3-4 lot-1 fills bought sheep and geese, and Q2 slipped d5 -> d8 and Q3 d10 -> d11 on 2/3 boards (NO-GO).
  With POSTFILL_KEEP_FROM=2 (PFA2) it is equal to G on 1 board and nearly equal on 2. In PFS's layout the lot-1 fills of d2-9 are fertilizer /
  eggs / wheat, a few hundred coins, and the land keep absorbs them.
* Orchestrator's change at 12:43Z (from astra's note, accepted as accurate): PFAL was replaced by G2NL = G2 without LUMP9.

### Grid (80 g vs g0capsfix on m76 boards 1-40 x 2, paired vs m76_ctl; LP's round-2 rows were on m40)
| cell | ours | rival | margin | d-ours (t) | d-rival (t) | d-margin (t) | W vs 77 | flips | Q3 d9 / d10 | herd d9 C/S/G | dawn d9 / d10 | escapes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| control PFS (m76_ctl) | 109,848 | 85,025 | +24,823 | - | - | - | 77 | - | | | | |
| **G2 = LP + Q3 guard (res 200)** | 112,954 | 83,736 | +29,218 | +3,106 (+4.23) | -1,289 (-2.18) | +4,395 (+4.36) | 80 | +3/-0 | 40 / 40 | 6.7/3.6/3.3 | 2,599 / 4,224 | 0 |
| G4 = LP + Q3 guard (res 400) | 112,436 | 83,733 | +28,704 | +2,588 (+3.24) | -1,292 (-1.79) | +3,880 (+3.25) | 80 | +3/-0 | 18 / 62 | 6.4/4.2/2.0 | 1,989 / 5,017 | 4 |
| G4 vs G2 | | | | -518 (-0.83) | -3 | -515 (-0.53) | 80 vs 80 | 0/0 | | | | |
| PFA = G2 + POSTFILL A (guarded) | 113,322 | 83,898 | +29,424 | +3,474 (+4.94) | -1,127 (-1.91) | +4,601 (+4.78) | 80 | +3/-0 | 38 / 42 | 6.9/3.6/3.1 | 2,621 / 4,108 | 0 |
| **G2NL = G2 without LUMP9** | 113,557 | 83,960 | +29,597 | +3,709 (+4.37) | -1,065 (-2.05) | +4,774 (+4.37) | 80 | +3/-0 | 4 / 76 | 6.5/3.0/3.1 | 1,567 / 5,892 | 0 |
| PFA vs G2 | | | | +368 (+1.81) | +162 | +206 (+0.58) | 80 vs 80 | 0/0 | | | | |
| G2NL vs G2 | | | | +603 (+1.59) | +224 | +379 (+0.63) | 80 vs 80 | 0/0 | | | | |

G2's extra reads (best cell by W then margin when they were queued at 12:43Z; PFA and G2NL came in later within +0.2..+0.4k of it):
| read | n | ours | rival | margin | d-ours (t) | d-rival (t) | d-margin (t) | W | Q3 d9 / d10 |
|---|---|---|---|---|---|---|---|---|---|
| flood (m40, ctl jr2_pfs_fl) | 80 | 127,038 | 76,766 | +50,271 | **+2,908 (+2.98)** | -284 (-0.27) | +3,192 (+1.84) | 80 vs 80 | 33 / 47 |
| flood, vs LP (round 2) | 80 | | | | +2,114 (+2.77) | -2,144 (-1.49) | +4,258 (+2.04) | | |
| big (m40 boards 1-20, ctl bm_pfs) | 40 | 118,132 | 74,160 | +43,972 | +2,937 (+2.58) | +939 (+1.22) | +1,998 (+1.61) | 40 vs 40 | 6 / 34 |
| live27 CLOSED loop vs g0capsfix (ctl ms_ctl_l27) | 27 | 113,829 | 84,336 | +29,492 | +1,594 (+1.16) | +43 (+0.04) | +1,551 (+0.94) | **27 vs 27** | 15 / 12 |
| G2NL flood (m40, ctl jr2_pfs_fl) | 80 | 125,640 | 78,016 | +47,625 | +1,510 (+1.51) | +965 (+1.21) | +545 (+0.36) | 80 vs 80 | |
| G2NL live27 CLOSED loop | 27 | 113,962 | 84,133 | +29,828 | +1,727 (+1.48) | -160 (-0.15) | +1,887 (+1.18) | 27 vs 27 | |
(G2NL = G2 without LUMP9: equal on m76 (+379, t 0.63) and on live27 CL (+336), but -1.4k own / -2.6k margin on flood. LUMP9 stays in the
package; the round-2 read "LUMP9 ~0" held on g0capsfix only.)

### Book split, d10-29 (arm - control, coins/game; ours | rival)
| book | G2 m76 | G2NL m76 | G2 flood | G2 big | G2 live27 CL |
|---|---|---|---|---|---|
| EGG | +2,212 \| -1,497 | +2,178 \| -1,473 | +1,989 \| -600 | +737 \| -622 | +2,469 \| -177 |
| STRAWBERRY | +1,858 \| +1,547 | +1,808 \| +1,595 | +1,108 \| +1,861 | +1,833 \| +1,505 | +843 \| +2,020 |
| FERTILIZER | +599 \| -813 | +580 \| -848 | +618 \| -648 | +988 \| -812 | +428 \| -620 |
| MILK | -401 \| -446 | -578 \| -437 | +1,748 \| -1,586 | +499 \| -402 | -911 \| -302 |
| WOOL | -13 \| +416 | +418 \| +122 | -630 \| -611 | +2,241 \| -536 | -602 \| -342 |
| MELON | +292 \| -941 | +374 \| -905 | -796 \| +203 | -87 \| -165 | +3 \| -440 |
| WHEAT / CARROT / TOMATO | -1,427 \| +344 | -1,294 \| +465 | -1,074 \| +1,222 | -2,625 \| +1,610 | -226 \| -1,383 |
(d0-9 moves by <= +0.5k in every cell: fertilizer +0.4-0.5k, eggs +0.1k.)

### CANDIDATE bar (unchanged: m76 own >= +2k t >= 3 with margin >= 0; flood own >= 0; live27 closed-loop W >= control)
* G2 meets all three: m76 own +3,106 (t 4.23) margin +4,395 (t 4.36); flood own +2,908 (t 2.98); live27 CL W 27 = 27 (+1,551 margin).
* -> **CANDIDATE**: dist/ship_vrp21_bs2lp.tar.gz, **md5 b76283db**, 1,169,701 B, 31 files. It is the vrp20_pfsoff package plus this plan.py
  (defaults BANK_LATE_DAYS="8", REINVEST_DAILY="4:200", REINVEST_ALL_LANES=True, FEED_ALL=True, REINVEST_Q3GUARD=8; KERNEL2_FIRE_CASH "99999").
  The tar round-trip is exact. Config commit 64a0101f on branch ship_vrp21_bs2lp. Package smoke = the package as a FILE agent on the 27 live27 seats: 27/27 DONE, 0 bad steps, 720 steps, fire_cash 99999, k2_mode pfs,
  10 turns > 1 s, max step 1,551 ms (r1's REINVEST package 19 / 2,876 ms). Its faithful tape read (22 seats; the tape rival's sales do not react):
  W 6 -> 6 (+1/-1), dours +1,434 (t 1.75), dtheirs +2,775 (t 4.31), dmargin -1,341 (t -1.67).
* tests/_pin.py row `vrp21_bs2lp` (candidate, md5 b76283db, ref 64a0101f) is in the working tree, NOT committed by me: the same file carries
  CLSEARCH1's uncommitted `vrp21_clsearch` row (REINVEST_DAILY "4:200:CSG" + FEED_ALL, m76 own +4,118 margin +2,815), which I must not commit.
* Slot line (the user's decision): an upload retires vrp19w 56649892 (FIFO; the final pair would be vrp20_pfsoff + this). Two copies of PFS =
  +10..+14 rating points. A bold body earns the slot only if its own mean rating >= PFS's; here every closed-loop read is >= PFS's
  (margin +1.6..+4.8k), but the live27 tape reads of LP-family cells stayed flat (W 6 -> 5..8).

### Verdict round 3
**CANDIDATE: G2 = LP + Q3 guard (reserve 200)**, dist/ship_vrp21_bs2lp.tar.gz md5 b76283db.
* m76 (fresh boards): margin +4.4k (t 4.4), W 80 vs 77 (+3/-0).
* flood: own +2.9k.
* big: margin +2.0k.
* live27 closed loop: W 27 = 27, margin +1.6k.
* Faithful tapes: W 6 = 6, margin -1.3k (the tape rival does not react).

Other cells:
* Same-hour lot-1 fills (POSTFILL) add ~0 in PFS's layout (+0.2k, 83 % of games identical): PFS already sells lot 1 first in its buy row; its
  d2-9 lot-1 fills are small; the programme's same-hour money is wool / milk that PFS does not have on d6 / d8.
* Reserve 400 < 200 (-0.5k).
* Without the Q3 guard (round 2's LP on m40): W 73 vs 75. With it: 80 vs 77 on m76, and flood +4.3k margin vs LP.

### Round 3 addendum (13:25Z): the live pair changed during the round; G2 vs the uploaded vrp21_clsearch
* SHIPSYNC6 (58f81ba3): the user uploaded vrp21_clsearch (sub 56676381, md5 d93d6f5c, ~13:10Z) = REINVEST_DAILY "4:200:CSG" + FEED_ALL (the
  priority reinvestment built here, cows-first order, no ALL_LANES / Q3 guard / LUMP9). vrp19w 56649892 is retired.
  * The live pair is vrp20_pfsoff 56652418 + vrp21_clsearch 56676381.
  * The same commit carried this round's pin row `vrp21_bs2lp` and BUILD-STORY paragraph into HEAD.
* Paired on the same games (CLSEARCH1's r3_fc_m76q0-3 and r2fl_fc* rows), G2 vs vrp21_clsearch:

  | read | n | own | rival | margin | W |
  |---|---|---|---|---|---|
  | m76 | 80 | -1,929 (t -2.81) | -2,744 | **+814 (t 0.85)** | 80 = 80 |
  | flood | 80 | +2,058 (t 1.72) | -2,333 | **+4,391 (t 2.35)** | 80 = 80 |

  - On these m76 games vrp21_clsearch is itself own +5,036 / margin +3,581 vs PFS.
  - The Q3 guard + ALL_LANES body concedes less to the rival: flood rival -2.3k, and flood own +2.1k.
* **Slot line now:** an upload of ship_vrp21_bs2lp FIFO-retires vrp20_pfsoff, the PFS anchor. The pair would then be two reinvestment bodies
  (vrp21_clsearch + vrp21_bs2lp). G2's mean margin is >= vrp21_clsearch's on both paired reads (m76 +0.8k ns, flood +4.4k t 2.35). Keeping
  vrp20 keeps PFS's rating as the floor of the pair. The decision is the user's.

## Session summary (written by the orchestrator, 2026-09-29 13:32Z, three participants: the Opus agent, the orchestrator, codex astra)

**Rule applied:** 3 rounds per session, then this summary and a fresh session (BRAINSTORM3). Astra's turns: docs/strategy/2026-09-29-astra-brainstorm{2,3}.md.

**Established (closed loop vs g0capsfix unless stated; 80-game paired reads; 20-game screens overstated every cell by 2.5-4.7k):**
1. Feeding every unfed d0-9 animal-day is worth -213..-302/game on PFS (base unit + fertilizer still come unfed; only the care bonus is lost). FEED_ALL alone -3.4k. Feed-first inside reinvestment is what prevents escapes (28 -> 0 / 80 g).
2. Sheep-first daily reinvestment raises own +4.8k (t 7.8) but the rival wins +3.8k back, milk-LED (+4.4k milk, +2.4k strawberry); flood margin -8.6k. Keeping PFS's own cows ahead of the sheep turns the rival's late milk from +4.4k to -0.8k.
3. PFS's d1-9 purse cannot buy animals earlier from dawn cash (no room for a sheep before d8; LUMP9 alone +20 margin; additive reinvestment from leftovers -2.0..-2.6k because today's leftover is tomorrow's Q3 coins). The gain comes from moving d5-9 SEED coins into animals while keeping the cows and guarding Q3.
4. G2 = LUMP9 + REINVEST 4:200 all animal lanes before seeds + FEED_ALL + Q3 guard (reserve 200): fresh m76 80 g own +3,106 (t 4.2) rival -1,289 margin +4,395 (t 4.4) W 77->80; flood own +2,908 (t 3.0) margin +3,192; big margin +1,998; live27 closed loop W 27=27 margin +1,551; faithful tapes W 6=6 margin -1,341. Books d10-29 ours|rival: eggs +2.2k|-1.5k, fert +0.6k|-0.8k, strawberry +1.9k|+1.5k, milk -0.4k|-0.4k. CANDIDATE package dist/ship_vrp21_bs2lp.tar.gz md5 b76283db (NOT uploaded).
5. Same-hour fills (POSTFILL) add +206 margin (t 0.6, 83 % identical games): PFS's h1 row already sells lot 1 before buying; the programme's edge is the executor ROUTE (P48GRAPH1: funding goods sold 5-9 h earlier), not the accounting. Reserve 400 loses 515 margin and adds 4 escapes. LUMP9 stays only for flood (+2.6k there).
6. Sibling cell FCSG (CLSEARCH1: 4:200 cows-first + FEED_ALL) was UPLOADED 13:10Z as vrp21_clsearch (sub 56676381); G2 vs it paired: m76 margin +814 (t 0.85), flood +4,391 (t 2.35), 0 net win changes.

**Closed:** blanket feeding; additive reinvestment; LUMP9 standalone; POSTFILL; reserve 400; the plate + reinvest combination (COMBO2: super-additive vs the clone but flood -6.9k on late strawberry/milk, V56 margin -9.1k for P8d3).

**Open:** transfer. The judge rival is ~25 % under-built (JUDGECAL1/TARGETS1: it sells 30-43 % of real late eggs and 41-45 % of real late strawberries, exactly G2's gain books), the faithful tapes are flat, and NEITHER reinvest body has been judged against the V band (57 % of our games) - VCHECK1 is running that now. Slot state: pair = vrp20 (PFS anchor) + vrp21_clsearch; uploading bs2lp retires the anchor -> HOLD (astra's trigger table in astra-brainstorm3.md: decision read frozen at 09-30 18:00Z on >= 40 vrp21 games with >= 20 V and >= 12 MELON, split by family, vs contemporaneous vrp20; fallback PFS + PFS needs two uploads).

**BRAINSTORM3 seed (astra's choice, agreed):** TRANSFER3 = the frozen three-body comparison {PFS, CLSEARCH, G2} against a FAITHFUL programme rival once P48GRAPH2 clears its gates (d9 h12 herd 18 +- 2, productive 68.9 +- 4, first melon sale 246 +- 3, volumes +- 10 %, same-board final +- 5k), 80/arm then 152/arm untouched, board-clustered t; pass = own >= +2k t >= 3, margin >= +2k t >= 2, W >= control, G2 vs CLSEARCH margin >= 0, V gates. While waiting: the 12-prefix funding audit of HERD_RECEIPTS_18 (astra-brainstorm2.md) - can PFS's actual receipts fund 18 placed animals by d9 h12 in 10/12 prefixes with no Q2 delay and Q3 by d9 h3? P(pass) 35 % for the transfer, subjective.
