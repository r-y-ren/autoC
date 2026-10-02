# BRAINSTORM5: the fired MELON-seat body (PFS on V seats by construction, a PFS cell only on whitelisted P48/PQ4 seats) fails the faithful tapes in all three cells; NONE. Round 2: the Q4 wheat field (R1f) cannot be funded from PFS's d10 purse and loses 9-12k; herd from d10 (RD10) keeps the wall but the rival gains more (-4.2k to -6.8k) -> STOP (2026-09-29)

Stream dir `S/brainstorm5/`, checkpoint `S/brainstorm5/checkpoint.txt`. Worktree `/mnt/e/_work/kagg3_wt_brainstorm5`, branch `brainstorm5_0929`.
Participants: BRAINSTORM5 runs the rounds, the orchestrator replies between rounds, codex astra reviews.

## Round 1 (17:09Z-18:40Z)

**Verdict: NONE. No package, no `_pin` row.**
- The fired body is built. Unfired identity is exact: **10/10** V56 games, byte-identical to the PFS rows with the kernel ON.
- The whitelist now covers P48-code seats 47/47 and V seats 0/348.
- No fired cell passes all four legs:
  - **fC (FCSG)** passes p48c (own +3,749, t 3.08; margin +2,126) and g0capsfix (margin +4,787, t 3.75). It fails big (margin -2,061) and the faithful tapes (W 4 -> 3, margin -4,292, t -2.62).
  - **fA (G2)** has margin >= 0 on every clone. It fails the own bar on p48c (+279) and the tapes (W 4 -> 3).
  - **fB (P8d3 + 4:400)** loses margin on every clone and on the tapes. Its tape result reproduces COMBO2's `pC400` row exactly: +825 / +5,375 / -4,550 on 14 seats.
- **Mechanism.** Every fired cell funds its herd or plate out of the d6-10 strawberry tiles. On p48c, PFS has 16.9 strawberry tiles at d6 h12 and 24.0 at d10; fC has 9.4 and 16.4. So our d15-17 strawberry units fall by 16-33 per game (t -9 to -24).
  - The clone rivals sell only 21-28 strawberries in d15-17 and do not charge for the loss. The rival in the faithful tapes does: +1.4k to +5.4k, and every faithful flip is a loss on a 938 (P48-code) seat.

### A. Whitelist (helper report `S/brainstorm5/res/whitelist.md`)
Data: 564 live games from `S/livewatch23/lw23_*.tsv` (09-28 08:14Z to 09-29 16:27Z), all with PFS's real h0. The rival's h1 cash is a pure function of its h0 order list (479 replays read).

| scope (all six PFS-h0 subs) | P48-code | PQ4-code | other MELON | all MELON | V (must be 0) |
|---|---|---|---|---|---|
| vrp19w 36-value list | 33/47 (70 %) | 30/36 (83 %) | 30/104 | 93/187 (50 %) | **6/348 (value 29)** |
| BRAINSTORM5 41-value list | **47/47** | 30/36 | 31/104 | 108/187 (58 %) | **0/348** |
| current three subs (vrp20/vrp21/vrp19w), 41-value list | 35/35 | 19/23 | 14/72 | 68/130 | 0/206 |

- **Removed: 29.** It appears in 6 V games (V rivals rated R0 691-1,022, including vrp21's listed != observed row 115249629) and in 0 MELON games.
- **Added:**
  - 964: P48 h0 with wheat first. 6 games, subs 56648295 / 56629243 / 56662028 / 56660557 / 56666137; also Vadim 56667905 against other opponents.
  - 992: wheat 4. Subs 56651013 / 56655029.
  - 1020: wheat 3. Subs 56667319 / 56640865 / 56670381.
  - 985: wheat arbitrage. Sub 56651424.
  - 1100: no wheat. Sub 56616660.
  - 2097: My second life 56654747, a PQ4 team.
- **Left out: 2464** (PQ4 with wheat first; 6 MELON games, 0 V). It was a deliberate KEEP-OUT in BOLDSLOT1. With it, PQ4 coverage is 36/36.
- DSM 56675988 and UMG 56658433 show 938, which is listed. DECEM's h0 has never been seen against PFS, so its value is unknown.
- **Fire share with the 41-value list: 108/564 = 19 % of the live PFS-h0 games.**
- List: `1|4|8|17|19|23|26|34|73|76|117|160|163|182|190|444|456|553|564|620|638|661|938|964|985|992|1020|1100|1616|2046|2097|2322|2338|2438|2477|2485|2492|2511|2593|2600|2904`

### B. Build and identity
- Commit `79f0d74b` on `brainstorm5_0929`, built as 8d670dad (pure PFS) plus:
  - BRAINSTORM2's switch code: 8 cherry-picks, 29a30244..b7a89977 (REINVEST_DAILY / lane order / FEED_ALL / BANK_LATE_DAYS / ALL_LANES / Q3GUARD / POSTFILL).
  - MELONTRIAL1's `KERNEL2_FIRE_SWITCHES` (f1cbd8c2).
- **One fix: an unfired seat with a latched d1 ENGINE_GATE re-applies the gate after the fire-set base restore.**
  - MELONTRIAL1 did this only on fired seats.
  - Without the fix, cell B's plate items (shared with `ENGINE_GATE_SET`) would reset a ZERO-class seat's engine plate.
- Other defaults: `KERNEL2_FIRE_CASH` = the 41-value list; `KERNEL2_FIRE_SWITCHES` = "".
- A fired seat stays PFS. At step 1 its d0 plan is rebuilt under the set, and the set is written on every turn.
- `tests/test_kernel2_fire_switches.py`: 5 passed.
- **Identity: `b5id_v56_s10_fA` (kernel ON, 41-value list, fire set A) vs VBAND1's `r3v_v56_boards_s10_pfs`: 10/10 EXACT.** Ours, theirs, o240 and t432 are identical in every game, and V56's h1 cash is 2901 (unfired).
- **Fire on the judge boards:** 938 = the P48 h0 of the clone rivals. All seats fired: p48c 80/80, big 40/40, g0capsfix 40/40. No forcing was needed.

### C. Fired-cell grid (paired with PFS on the same games, board-clustered t; harness `S/brainstorm5/t5` = TRANSFER3 copy)
- **Cells:**
  - A = G2: `BANK_LATE_DAYS=8;REINVEST_DAILY=4:200;REINVEST_ALL_LANES=True;FEED_ALL=True;REINVEST_Q3GUARD=8`.
  - B = `MELON_PLATE_TILES=8;MELON_PLATE_DAY=3;NONV_PLATE_LAST=4;REINVEST_DAILY=4:400`.
  - C = FCSG: `REINVEST_DAILY=4:200:CSG;FEED_ALL=True`.
- **Control rows.** On p48c and g0capsfix, TRANSFER3's banked `t3_*_screen_pfs` (screen40 x 2 seats). On g0capsfix only the 40 seat-0 games are paired. For big, a new PFS row on screen40 seat 0.
- The PFS baselines are already lopsided: p48c W 79/80 (margin +32.2k), big 40/40 (+48.2k), g0capsfix 39/40.

| cell | rival | n | W (flips) | d-own (t) | d-rival (t) | **d-margin (t)** | our straw u d15-17 | rival straw u d15-17 | our late animal u d18-29 (E+M+W) | rival late animal u |
|---|---|---|---|---|---|---|---|---|---|---|
| fA | p48c | 80 | 79->80 (+1/-0) | +279 (0.35) | -308 (-0.35) | **+586 (0.42)** | 48.4->30.9 (t -11.2) | 20.8->24.1 | 274.8->286.3 (+11.5) | 303.6->296.3 |
| fB | p48c | 80 | 79->80 (+1/-0) | +5,392 (3.92) | +6,063 (5.19) | **-671 (-0.37)** | 48.4->15.8 (t -19.8) | 20.8->25.7 | 274.8->268.0 (-6.8) | 303.6->299.5 |
| fC | p48c | 80 | 79->78 (+1/-2) | +3,749 (3.08) | +1,623 (1.66) | **+2,126 (1.43)** | 48.4->26.7 (t -16.8) | 20.8->24.8 | 274.8->305.8 (+31.0) | 303.6->285.6 |
| fA | big | 40 | 40=40 | +3,652 (2.45) | +2,247 (1.90) | **+1,405 (0.77)** | 49.9->33.9 | 28.1->26.9 | 296.3->307.1 (+10.8) | 236.7->221.2 |
| fB | big | 40 | 40=40 | +4,271 (3.24) | +5,346 (3.22) | **-1,075 (-0.47)** | 49.9->19.0 | 28.1->27.3 | 296.3->289.9 (-6.5) | 236.7->227.9 |
| fC | big | 40 | 40=40 | +3,616 (2.42) | +5,677 (4.17) | **-2,061 (-0.94)** | 49.9->33.0 | 28.1->27.7 | 296.3->324.4 (+28.1) | 236.7->240.4 |
| fA | g0capsfix | 40 | 39=39 | +2,420 (2.65) | -194 (-0.19) | **+2,613 (1.95)** | 48.2->31.5 | 24.3->24.1 | 272.6->304.2 (+31.5) | 304.4->292.9 |
| fB | g0capsfix | 40 | 39->37 (+0/-2) | +4,535 (3.25) | +5,244 (4.03) | **-710 (-0.39)** | 48.2->20.0 | 24.3->26.0 | 272.6->265.2 (-7.5) | 304.4->320.7 |
| fC | g0capsfix | 40 | 39->40 (+1/-0) | +5,539 (5.05) | +752 (0.67) | **+4,787 (3.75)** | 48.2->26.5 | 24.3->24.4 | 272.6->300.5 (+27.9) | 304.4->299.9 |

**Five books.** Coins, arm minus control, by window d0-9 / d10-17 / d18-29, ours | rival. Full table in `S/brainstorm5/res/t5an_all.md`.
- **fC vs p48c:**
  - EGG +55/+1,275/+1,200 | -0/-199/-681
  - MILK +40/+856/-584 | -52/-121/-669
  - WOOL -5/-568/+2,542 | +169/-353/+670
  - FERT +623/+1,222/-56 | -61/-496/-893
  - STRAW 0/-4,300/+6,151 | 0/+992/+2,537
  - MELON 0/-1,318/+1,183 | 0/+233/-247
- **fC vs big:**
  - EGG +80/+1,356/+1,012 | 0/-113/-261
  - MILK -21/+946/-1,093 | +304/-330/+243
  - WOOL +3/-770/+1,659 | +59/-176/+835
  - FERT +528/+1,234/-203 | -129/-221/-592
  - STRAW 0/-3,173/+5,118 | 0/-20/**+5,032**

  Our strawberry moves late, and the big rival sells its late strawberries at the price we leave it.

**Faithful live27 tapes.** Open loop against the rival tapes on the 18 fired seats (`fired18.txt`). Packages `S/brainstorm5/tmp/p{A,B,C}` = the vrp20 package image + the worktree's plan.py / runtime.py + the cell's `KERNEL2_FIRE_SWITCHES` default. Every run: 18/18 DONE, 0 bad steps, 18/18 fired (the `sw` k2 mode).

| cell | JC1-faithful both n | W live -> pkg (flips) | d-own (t) | d-rival (t) | **d-margin (t)** | faithful flips | all 18 (not counted: tapes break) |
|---|---|---|---|---|---|---|---|
| fA | 13 | 4 -> 3 (+0/-1) | +906 (0.69) | +1,448 (1.78) | **-542 (-0.43)** | thisray 114689938 (938) - | W 4->8, margin +13,702 |
| fB | 14 | 4 -> 3 (+1/-2) | +825 (0.26) | +5,375 (3.13) | **-4,550 (-1.07)** | gradientgrazin 114672177 (938) -, thisray 114689938 (938) -, istinetz 114686994 (1) + | W 4->7, margin +9,739 |
| fC | 14 | 4 -> 3 (+0/-1) | +739 (0.61) | +5,031 (3.08) | **-4,292 (-2.62)** | gradientgrazin 114672177 (938) - | W 4->6, margin +9,224 |

**Strawberry tiles at h12, d6 -> d10 (p48c, 80 g):**

| body | d6 | d7 | d8 | d9 | d10 | dawn cash d10 |
|---|---|---|---|---|---|---|
| PFS | 16.9 | 21.6 | 22.4 | 23.7 | 24.0 | 6,066 |
| fA | 12.2 | 13.3 | 16.8 | 21.9 | 22.8 | 4,658 |
| fB | 4.0 | 8.6 | 12.6 | 15.6 | 17.9 | 5,133 |
| fC | 9.4 | 11.9 | 13.7 | 14.7 | 16.4 | 5,272 |

The fired cells reach PFS's strawberry tile count only by d14-17. The strawberry supply moves from d15-17 into d18-29.

### D. Verdict against the bar
The CANDIDATE bar: own >= +2k with t >= 3 and margin >= 0 vs p48c, AND margin >= 0 vs big, AND tapes W not lower, AND unfired identity exact.

| cell | p48c | big | tapes | result |
|---|---|---|---|---|
| fA | own +279: FAIL | +1,405: PASS | W 4 -> 3: FAIL | NONE |
| fB | margin -671: FAIL | -1,075: FAIL | W 4 -> 3: FAIL | NONE |
| fC | own +3,749 (t 3.08), margin +2,126: PASS | -2,061: FAIL | W 4 -> 3, margin -4,292 (t -2.62): FAIL | NONE |

Identity passes (10/10). There is no package, and the live pair stays vrp20 (PFS anchor) + vrp21_clsearch.

**Hypothesis.** The P48-seat wall is our d15-17 strawberry supply, set by our d6-10 strawberry tiles. A fired cell can add late herd only if it buys the herd after those tiles are seeded, from the d10 cash PFS holds (6.1k at dawn, Q3 at d10.2). The clones are blind to this: they sell 21-28 strawberries d15-17, not the P48 wave. The faithful tapes are the leg that prices it.

**Round-2 cell (exact).** Fired only on the 41-value list: `KERNEL2_FIRE_SWITCHES=REINVEST_DAILY=10:200:CSG;FEED_ALL=True`, FCSG with the reinvest start moved from d4 to d10, on this worktree.
- **Gates, in order:**
  1. The p48c screen: strawberry tiles d6-10 within 1 of PFS; d15-17 strawberry units >= PFS - 2; margin >= 0.
  2. The faithful fired18 tapes: W not lower, margin >= 0.
  3. big 40 g: margin >= 0.
  4. g0capsfix 40 g.
- **Kill:** if the d6-10 strawberry tiles still fall by 2 or more, FEED_ALL is the cause. Rerun without it.

### E. Files
- **Harness:**
  - `S/brainstorm5/t5/`: t5go.sh (combined queue launcher), t5_chain.sh (the OFF string without FIRE_CASH, so the tree default list applies), t5_rc.py, t5an.py, an5.py (unit books + fire share), arms.json, res/ (all rows + the copied PFS control rows).
  - Tape check: `S/brainstorm5/tape.sh`, `pkgrun.py`, `tbl_l27.py` (copies of COMBO2's), `res/pkg_l27_{A,B,C}.csv`, `logs/tbl_l27_*.txt`.
- **Compute:**
  - Remote: 2 chains (nice 19 + ionice idle), launched through `flock -o /home/user/gpu_launch.lock` at load 1.6-3.3. Clone rivals ran on the shared GPU1 forward server; no GPU process of ours. Stage `~/stage_reactclone1/S/brainstorm5` and `cand/t5_*` were removed at the end (checked with a second ssh).
  - Local: 1 tape process.

## Round 2 (18:31Z-20:20Z)

**Verdict: STOP. Both cells are NONE, with no package and no `_pin` row. The fired PFS-internal line ends here, and its compute goes to the executor (PROGAGENT1).**
- **R1f (the Q4 wheat field on fired seats) cannot be funded from PFS's purse.**
  - PFS holds 5.4-6.1k at d10 dawn. It spends that on Q3 (d10 h4) and the d10 herd, and holds 2.0-2.8k at d11 dawn.
  - So Q4 on d10 happens on **0/6** gate-0 seats and never on the 80-game judge. When Q4 is bought on the first day the purse allows (d11-15), the field loses on every judge:

    | judge | margin (t) | W |
    |---|---|---|
    | p48c | **-9,403 (-8.87)** | 79 -> 69 |
    | big | **-10,617 (-7.85)** | 40 = 40 |
    | faithful fired18 tapes | **-11,670 (-6.67)** | 4 -> 0 |

  - We spend +15.8k and earn +7.8k. We do not cannibalise our own Q1-3 wheat. The wheat denial on the rival is real but small: -1.0k.
- **RD10 (herd bought from d10) delivers what it was built to deliver.**
  - The strawberry wall is exact through d9: d10 is -0.1 tiles and d15-17 is -0.2 units.
  - The herd is +2.1 at d14 and +2.0 at d18. Late animal units are +27 (t 3.7).
  - It still loses:

    | judge | margin (t) |
    |---|---|
    | p48c | **-6,753 (-3.68)** |
    | big | **-5,192 (-3.03)** |
    | faithful tapes | **-4,215 (-4.45)**, W 4 -> 3 |

  - On the P48-code tape seats the rival gains more than we do: our own -1,288, the rival's +1,768.
  - The one defect left is escapes: +2.8/game with the d10 feed grant, +4.5 without it. Extra herd without extra hands overloads daily herd service. This is BRAINSTORM4's goose-ledger failure, and no switch fixes it.

### A. Cells, glue, identity
- **R1f.**
  - Switch set: `KERNEL2_FIRE_SWITCHES=Q4_PROG_ON=True;Q4_TARGETS=R1F;Q4_EXTRA_HANDS=1;Q4_HIRE_CAP=0`, built on Q4PROG1's existing switches.
  - Q4 is bought on the first day in `Q4_BUY_DAYS` = (10, 15), with 3 quadrants owned, when the purse covers the land gap. So it can never come before PFS's own Q3.
  - `Q4_HIRE_CAP=0` keeps the default 12-hand cap from cutting PFS's own crew.
  - The only glue is two presets:
    - `R1F`: Q4 wheat census of 12 from d10 and 24 from d11. The relay replants after each harvest.
    - `R1F12`: 12, held.
  - **Not built: 7-unit wheat lots.** The only existing lot switch, SELL_SPREAD, also moves strawberry, which would break the wall.
- **RD10.**
  - Switch set: `REINVEST_DAILY=10:200:CSG;REINVEST_LAST=14;REINVEST_Q3GUARD=10`. REINVEST_LAST defaults to 9, which would make `10:200` a no-op.
  - **D10F** adds `FEED_ALL=True;FEED_ALL_FROM=10`. The glue is `FEED_ALL_FROM` (default 0 = every day), which grants FEED_ALL only from that day on.
- **Code.** Commit `8a986cf3` on `brainstorm5_0929`. It also fixes `test_default_is_off`, which rejected round 1's trailing comment. `test_q4_prog.py` and `test_kernel2_fire_switches.py` pass.
- **Unfired identity holds by construction.** The presets and `FEED_ALL_FROM` are reachable only through a fired set, and every default is unchanged, so round 1's 10/10 exact identity stands. It was not re-run because there is no candidate.
- **Harness.**
  - `t5_rc.py` gained hooks for:
    - wheat, planted and Q4 tiles per day for both farms;
    - wheat PLANT orders;
    - hands per day for both farms;
    - money after each quadrant buy;
    - shed at h23;
    - ordered wheat BUY_PRODUCT / BUY_SEED and HIRE rows per farm per day.
  - Hooked PFS reruns on p48c (80) and big (40) are byte-identical to the banked PFS rows.

### B. Gate 0 (6 games = 3 screen40 boards x 2 seats vs p48c, local, against the hooked PFS)

| cell | Q4 d10 / by d14 | d11 dawn cash | straw tiles d6-10 | straw u d15-17 | herd d14 / d18 | escapes/g | wheat plantings d12-26 | wheat tiles d11-27 | hands d10-27 | d-own (t) | d-rival (t) | **d-margin (t)** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PFS | - | 1,987 | 18.3/26.8/27.3/29.0/29.0 | 59.0 | 17.0 / 17.0 | 3.3 | 64.0 | 16.7 | 9.9 | 132,453 | 102,465 | +29,988 |
| R1f (R1F) | **0/6** / 2/6 (d11 h4, 1,016 left) | 1,987 | identical | 56.0 (-3.0) | 15.7 / 16.5 | 3.7 | 96.5 | 22.7 | 11.6 | -5,346 (-2.59) | -385 (-0.20) | **-4,961 (-3.55)** |
| R1f (R1F12) | 0/6 / 2/6 | 1,987 | identical | 57.0 (-2.0) | 15.7 / - | 8.3 | 94.2 | 22.7 | 11.8 | -8,000 (-3.79) | +512 (0.30) | **-8,511 (-3.56)** |
| RD10 (no feed) | - | 1,314 | identical | 59.2 | 16.7 / 16.7 | **7.3** | - | - | - | -401 (-0.06) | +6,503 (2.10) | **-6,904 (-0.77)** |
| D10F | - | 1,402 | identical | 57.3 (-1.7) | **19.0 / 19.7** | 6.0 | - | - | - | -1,682 (-0.24) | +8,812 (1.86) | **-10,494 (-0.92)** |

Gate-0 reads:
- **R1f fails on funding.** Q4 is never bought on d10. It is bought from d11 once the purse recovers.
- **RD10 without the feed grant fails on herd service:** escapes rise from 20 to 44 over the 6 games, and d0-14 escapes from 0 to 28. That led to D10F.
- **D10F keeps the strawberry wall and adds the herd. Its escapes are still above PFS.**
- **Judge order.** The judge ran R24 as a confirmation read on the budget, and D10F as the cell with the wall preserved.

### C. Grid (paired with PFS on the same games, board-clustered t)
Controls:
- p48c: TRANSFER3's `t3_p48c_screen_pfs` rows, byte-identical to the hooked rerun `b5r2h_p48c_screen_pfs`.
- big: `b5_big_s40_pfs`, equal to `b5r2h_big_s40_pfs`.

Rivals:
- **p48c** is the P48 clone: it buys Q4 by d14 in 0/80 games.
- **big** is a Q4 rival: it buys Q4 by d14 in 40/40 games.
- **The fired18 tape rivals buy no Q4 (0/18).** Decoded from the tapes, every one of them buys only Q2 (d6) and Q3 (d8-9).
- So p48c and the tapes are the no-Q4 read, and big is the Q4 read.

| cell | judge | n | W (flips) | d-own (t) | d-rival (t) | **d-margin (t)** | mechanism |
|---|---|---|---|---|---|---|---|
| R1f | p48c | 80 | 79 -> 69 (+0/-10) | -7,983 (-10.54) | +1,420 (2.06) | **-9,403 (-8.87)** | Q4 by d14 in 59/80 games, mean d12 h10; herd d14 -1.1 (t -3.0) |
| R1f | big (Q4 rival) | 40 | 40 = 40 | -8,615 (-10.02) | +2,003 (2.08) | **-10,617 (-7.85)** | Q4 by d14 in 28/40 games, mean d11 h21; herd d14 -1.8 (t -4.2) |
| R1f | tapes, 18/18 JC1-faithful both | 18 | 4 -> 0 (+0/-4) | -11,607 (-9.40) | +63 (0.08) | **-11,670 (-6.67)** | P48-code 6: -12,029 (t -10.1); other 12: -11,490 (t -4.42) |
| RD10 (no feed) | p48c | 80 | 79 -> 76 (+1/-4) | -4,872 (-3.17) | +5,118 (4.82) | **-9,989 (-4.66)** | escapes 4.5 -> 9.0; our milk d10-17 -1.1k; rival milk d18-29 +2.6k |
| D10F | p48c | 80 | 79 -> 78 (+1/-2) | -3,260 (-2.34) | +3,493 (3.66) | **-6,753 (-3.68)** | herd +2.1 / +2.0; late animal u +27.0 (t 3.67); escapes 4.5 -> 7.3 (t 3.9) |
| D10F | big (Q4 rival) | 40 | 40 = 40 | -2,072 (-1.41) | +3,121 (3.06) | **-5,192 (-3.03)** | herd d14 +1.9; escapes 2.9 -> 6.8 (t 5.1) |
| D10F | tapes, 18/18 JC1-faithful both | 18 | 4 -> 3 (+0/-1) | -2,334 (-1.85) | +1,881 (1.72) | **-4,215 (-4.45)** | P48-code 6: W 3 -> 2, own -1,288, rival +1,768, margin -3,056 (t -1.79); other 12: -4,795 (t -4.16) |

**Common faithful support with round 1.** 13 tape seats are faithful under A, C, D10F and R24:

| cell | margin (t) | P48-code 5 seats |
|---|---|---|
| R24 | -12,422 (-5.69) | -12,333 |
| D10F | -4,994 (-4.29) | -2,601 |
| fC | -3,738 (-2.24) | -5,104 |
| fA | -542 (-0.43) | -373 |

Every fired cell drops W from 4 to 3 or lower.

**The strawberry wall held in every round-2 cell.** p48c tiles at h12, d6-10, are 16.9/21.6/22.4/23.7/24.0 for PFS. D10F matches through d9 and has 23.9 at d10. R24 is identical through d10. d15-17 strawberry units are 48.4 for PFS, 48.3 for D10F and 48.7 for R24. Round 2 removed the round-1 displacement and still lost.

### D. Both purses, by book and window
**R1f wheat book.** R24 vs the hooked PFS, p48c 80 games, arm minus control. Buy orders are counts of ordered rows.

| book | ours | rival |
|---|---|---|
| wheat tiles d11-27 | 18.1 -> 25.1: Q4 wheat 7.1 + Q1-3 18.06 vs 18.14. **No Q1-3 cannibalisation.** On big: Q1-3 19.6 -> 20.1, Q4 7.0 | 28.95 -> 28.86 |
| Q4 use | 17.2 of 25 tiles planted: wheat 7.1 + the planner's own mix 10.1. The census of 24 is never reached (seed and room limits after the day's grant) | - |
| wheat plantings d12-26 | +35.3 (t 16.7) | - |
| wheat sold | +76 u (+9.7 d10-17 / +66.4 d18-29) = +1,914 coins | -3.1 u, **-1,026 coins** (price, d18-29 -936, t -4.0) |
| wheat bought: feed (BUY_PRODUCT) / seed | -7.7 / +35.1 u | -3.3 / -0.9 u |
| hires | hands/day 10.1 -> 12.1; +41 HIRE rows d10-29 | +0.7 rows (hands 10.83 -> 10.88) |
| total spend d10-17 / d18-29 | +5,953 / +9,873 (Q4 land 4,000 inside) | +13 / -78 |
| sale revenue d10-17 / d18-29 | -1,154 / +8,997: d18-29 strawberry +3.8k, melon +1.7k, wheat +1.5k from the Q4 tiles; egg/milk/fert -2.0k over d10-29 with herd d14 -1.1 | +252 / +1,103: milk +1.2k, fert +0.6k |
| **net** | **-7,983** | **+1,420** |

On big the book is the same shape:
- Ours: wheat +100 u (+2.3k coins), seed wheat +38 u, feed wheat bought -13.5 u, hires +33.5 rows, spend +13.3k vs revenue +4.6k.
- Rival: wheat -1.0k coins.

**The field returns about 7.8k of revenue on 15.8k of spend.** Q4DIG1's closure (land plus hands exceed Q4 revenue) holds on the fired PFS body against today's rivals.

**D10F books.** p48c 80 games, coins, d0-9 / d10-17 / d18-29.

| book | ours | rival |
|---|---|---|
| EGG | 0 / +86 / +815 | 0 / +69 / +213 |
| MILK | 0 / -733 / +117 | 0 / +546 / +1,503 |
| WOOL | 0 / -746 / +2,043 | 0 / +160 / +21 |
| FERT | 0 / +608 / +190 | 0 / -57 / -492 |
| STRAW | 0 / -113 / -1,636 | 0 / +324 / +86 |
| MELON | 0 / +5 / +39 | 0 / -36 / +62 |

- Our spend is +2.5k (herd, feed).
- Our d11 dawn cash falls from 2,783 to 1,369.
- Rival milk units are -3.3, but the rival's milk coins rise +2.0k: the price we leave by losing milk to escapes and d10-17 service.

### E. STOP read (astra's, adopted)
- **D10F meets it.** It delivers its intended extra production: herd +2.0, late animal units +27, strawberry wall exact. Yet the common-faithful P48 ledger shows the rival gaining more than us (own -1,280 vs rival +1,321 on the 5 common P48 seats; -1,288 vs +1,768 on all 6), with no win gain (W 3 -> 2).
  - The one open defect, escapes, is the herd-service capacity. It is the same labour bind BRAINSTORM4's repaired goose ledger closed, not a switch bug.
- **R1f fails before it reaches the stop read.** The failure is structural, not an execution defect.
  - The programme buys Q3 on d8: all 6 P48-code tape rivals do, at d8 h4-6, and the other fired families buy it d8-9. PFS buys Q3 at d10 h4.
  - So a PQ4 team built on the programme enters d10 with Q3 already paid and its d10 cash free. Ours is spent on Q3 and the d10 herd.
  - Buying Q4 when affordable (d11-15) is the Q4DIG1 economy: -8 to -12k.
- **Five of five fired cells now lose the faithful tapes:** fA / fB / fC in round 1, R1f / D10F in round 2. The fired line ends. No round-3 fired cell.

**Proposal for the next session (not a fired cell).** Put the compute into PROGAGENT1, the programme executor. Per TOP1WATCH1, its late template must carry the **d10 Q4 on the programme's funding path**:
- Q2 on d6.
- Q3 on d8-9.
- Q4 on d10 from the freed d10 cash.

That is a d0-9 economy change which the fired PFS body cannot make without breaking the d6-10 strawberry wall, as round 1 showed.

**Whitelist note (coordinator).** No values were added from replays. DECEM's current h1 (~1,961-1,967) and Majkel's (~2,005) match no row, and replays read 0-29 coins above live on P48 seats, so both need a live-observation check. A 938/964 hit no longer implies a no-Q4 rival: DSM 56675988 keeps 938 and buys Q4 on d10.

### F. Files and compute
- **Scripts and specs in `S/brainstorm5/t5/`:**
  - Analysis: `g0an.py` (gate-0, dose and both-purse wheat book), `r2an.py` (t5an contrasts for explicit pairs).
  - Runners and queues: `g0local.sh` (local rcr runner), `qadd.sh` (remote queue append under flock), queues `q2*.txt` / `g0l*.txt`, boards `boards_g3.json`, `boards_s40a.json` / `boards_s40b.json`.
  - Arms: `arms.json` (R24 / R12 / D10 / D10F).
  - Harness: `t5_rc.py` (hooks); `t5_rc_r1.py` is the round-1 copy.
- **Results:**
  - `res/b5r2g0_*` (gate-0)
  - `res/b5r2_*` (judge)
  - `res/b5r2h_*` (hooked PFS controls; the s0/s1 and a/b halves merged into `b5r2h_p48c_screen_pfs` / `b5r2h_big_s40_pfs`)
  - Remote logs in `logs/remote2/`
- **Tapes in `S/brainstorm5/`:**
  - Packages: `tmp/p{R24,R12,D10F}`.
  - Tables: `logs/tbl_l27_{D10F,R24}.txt`, `res/pkg_l27_{D10F,R24}.csv`.
  - `tsplit.py`: the P48-code / other split on common faithful support.
- **Compute:**
  - Remote: 1 chain while the shared box sat at 8-11 workers, then 2 chains for the hooked controls at 5-7 workers. All nice 19, ionice idle. Stage and `cand/t5_*` were removed and the removal checked with a second ssh.
  - Local: 1 process at a time for gate 0, the tapes and the big 40 legs. `S/reactclone1/params/params_p48c.npz` was copied from the remote (sha 4fb783d6) for the local p48c runs.
- **Slip:** the first gate-0 run crashed because the new env hook reused `k`, the name of step()'s `**k` argument. It was fixed and rerun, and nothing was lost.

## Round 3 (20:10Z-20:25Z) — Session summary

**Verdict: no BRAINSTORM5 candidate. No package, no `_pin` row, and no round-3 cell (astra's C3, adopted by the coordinator).**
- Both live Kaggle slots hold the PFS anchor: **56686302** (byte-identical, e5d84f03) and **56686308** (with the byte-identical plan fastpath, 6cef390c).
- The compute goes to PROGFIRE1 (the fired h1 executor bridge) and SPLITHEAD1 (ES on a fired-seat-only head with programme-family fitness), both in flight. The volume grid C1 waits for the fresh session.
- Astra's review, verbatim: `docs/strategy/2026-09-29-astra-brainstorm10.md`.

### A. Invariants after rounds 1-2
Astra's ten, each checked against this doc's tables. Own / rival are given wherever a coin figure exists.
1. **Both purses decide.** Report d-own, d-rival and d-margin, including purchases and displaced baseline output. Round 2's two books: R1f own -7,983 / rival +1,420 (§Round 2 D, wheat book); D10F own -3,260 / rival +3,493 (§Round 2 C, p48c).
2. **Timing at fixed production is closed in the tested settings.** Against V56 no timing move is worth more than +7 coins of margin per unit (BRAINSTORM4 summary 1). STRAW_WAIT1 fired 0/61; the $1-floor hold is shed-bound at +10..+36. Astra's "lot splitting -2,069" has no source in the BRAINSTORM4/5 docs and is not checked here.
3. **Denial volume is state-specific.** +1 strawberry on d14-18 = own +3 / margin +204 vs V56 (BRAINSTORM4 summary 2). It is a local counterfactual, not a price for every strawberry.
4. **"Production complete" is scoped** to BRAINSTORM4's traced V56 setting (through d21). IDLE2's feed/care opportunity at existing state is at most ~2.1k (IDLE2, not re-checked here).
5. **Idle is an afternoon tail.** Crew cuts are worth 555-900 coins (IDLE2). Added hands need funded, watered, saleable work: R1f added +2.0 hands/day (10.1 -> 12.1), and its field returned 7.8k of revenue on 15.8k of spend (§Round 2 D).
6. **A tile has a present and a future cost.** A coop/pasture tile displaces ~700-760 own rotation coins and hands the rival 180-470 (BRAINSTORM4 summary 3). TILELEASE1 adds that an occupied tile shrinks the next dawn's ask, n_dev = floor(dev_frac x n_free).
7. **Funding is policy.** PFS's d10 dawn cash (6,066 on p48c, §Round 1 C strawberry table) goes to Q3 at d10 h4 and the d10 herd. d11 dawn is 1,987 (gate 0, 6 g) and 2,783 (p48c 80, D10F book).
   - The programme's Q2 d6 -> Q3 d8-9 -> Q4 d10 is one sequence: the fired18 tape rivals buy Q2 d6, Q3 d8-9 and Q4 0/18; DSM buys Q4 d10 h9-12 in 10/10.
8. **The strawberry wall is necessary, not sufficient.** Round 1 cut d15-17 strawberry units by 16.0-32.6 in all 9 cells (§Round 1 C). Round 2 held it (PFS 48.4, D10F 48.3, R24 48.7) and still lost.
9. **Firing is isolation, not advantage.** The 41-value list fires on P48-code 47/47, PQ4 30/36, **other MELON 31/104** and V 0/348 (§Round 1 A). On the current three subs: 35/35, 19/23, 14/72, 0/206. Unfired identity is 10/10.
   - Revalidate new dispatch code. Never extend cash fingerprints from replays: they read 0-29 coins above live on P48 seats.
10. **PFS's local optimum is scoped.** ESHEADCL2: 0/112 candidates with V56 margin > 0; the best incumbent, c_g06_cen, reads v21 +181 / m40 -702 (t -2.2). This closes head-offset ES as a V lever only.

**Corrections to astra's text:**
- (i) Invariant 9 omits other MELON: 31/104 of those games fire under the 41-value list (§Round 1 A).
- (ii) fB is not a one-win loss like fA and fC. Its faithful flips are +1/-2 (§Round 1 C tapes), on support n 13/14/14 for fA/fB/fC.
- (iii) The D10F escape deficit is +2.8/game on p48c (4.5 -> 7.3) and +3.9 on big (2.9 -> 6.8) (§Round 2 C).
- (iv) Lot splitting -2,069 is unsourced here.

Every other number of astra's that this doc holds matches.

### B. Closed lines (paired vs PFS, board-clustered t)

| line | decisive numbers | failed on |
|---|---|---|
| fA = G2 (fired, r1) | p48c own +279 (t 0.35), margin +586; tapes n13 W 4 -> 3, margin -542 | p48c own bar; tapes W |
| fB = P8d3 + 4:400 (fired, r1) | p48c -671; big -1,075; tapes n14 W 4 -> 3 (+1/-2), -4,550 | p48c, big, tapes |
| fC = FCSG (fired, r1) | p48c own +3,749 (t 3.08), margin +2,126 (pass); big -2,061; tapes n14 W 4 -> 3, -4,292 (t -2.62), rival +5,031 | big, tapes |
| R1f = Q4 wheat field (fired, r2) | Q4 on d10 0/6 (gate 0) and 0/80 (p48c); p48c -9,403 (t -8.87) W 79 -> 69; big -10,617 (t -7.85); tapes 18 -11,670 (t -6.67) W 4 -> 0; spend +15.8k vs revenue +7.8k | funding, then every judge |
| D10F = herd from d10 + FEED_ALL_FROM=10 (fired, r2) | p48c -6,753 (t -3.68), own -3,260 / rival +3,493; big -5,192 (t -3.03); tapes -4,215 (t -4.45) W 4 -> 3; P48-code own -1,288 / rival +1,768 | every judge (RD10 without feed: p48c -9,989, t -4.66) |
| PROGAGENT1 executor (universal) | gate 1 exact 16/16; V56 m40 18/40 -9,896, v21 7/21 -6,940; p48c -2,666 (own +4,537, rival +7,203); late milk 130 -> 96, wool 138 -> 85 | V56 (gate 2), p48c |
| PROGAGENT1 d1 hand-back | V56 0/40: the programme's 7-coin dawn cannot carry PFS's continuation | V56 |
| PROGAGENT1 literal tape | vs PFS H=30 -23,556; vs V56 d-margin -28,267 | PFS and V56 |
| ESHEADCL2 (head-offset ES, V56 in the fitness) | 0/112 with V56 margin > 0; c_g06_cen v21 +181 (W 13 -> 16) / m40 -702 (t -2.2); floor +1,000 never approached | V56 |

The PROGAGENT1 and ESHEADCL2 rows come from their own docs through astra and were not re-checked here.

### C. The coverage gap the fresh session opens with
- **What the fire covers.** The whitelist was built for P48-code (12 % of our band) and PQ4 (6 %). The band mix is V 59 / other MELON 19 / P48-code 12 / PQ4 6 %. In the 564-game whitelist window (§Round 1 A) the families are V 348, other MELON 104, P48-code 47, PQ4 36.
- **Other MELON (19 %) has no cell.** It is our 6-22 pool: MELONLOSS1 reads +3.9k at eod d9 -> -18.7k at eod d14, with the rival selling 50 melons @249 on d10-14. No fired cell was designed or judged for it.
  - It is not simply unfired. 31/104 of its games carry a listed h1 cash (§Round 1 A; 14/72 on the current three subs), so any fired package runs there without its own judge. The other 73/104 stay pure PFS.
  - The only read on non-P48 fired seats is fired18's 12 other seats: R24 -11,490, D10F -4,795 (§Round 2 C).
- **Ceiling arithmetic (astra).** +3k on every P48-code + PQ4 seat is ~+540/game before selector misses.
- **Fingerprints.** DECEM (~1,961-1,967) and Majkel (~2,005) match no row. Check both on live observations before any extension; never extend from replay-only observations. A 938/964 hit no longer implies a no-Q4 rival: DSM 56675988 keeps 938 and buys Q4 on d10.

### D. Fresh-session order (astra's ranking, unchanged, plus research question R)
1. **Finish PROGFIRE1.** First prove the h1 bridge's real timetable: purchases, seeds, crew, Q3 d8 timing, herd survival. Then read its paired programme-family economics. Watch d10-14 cash exhaustion, escapes and lost baseline production. V seats stay exactly PFS.
2. **Finish SPLITHEAD1** on programme-family fitness, with the faithful transfer gates: exact isolation, rival gains charged.
   - **R (a research question, not a build): OTHERMELON.** Data only; it runs alongside 1-2 and reports before step 3 and before any whitelist change. On the 104 other-MELON games:
     - the live-observed h1 fingerprints (DECEM, Majkel);
     - what the 31 fired games get from the in-flight packages;
     - whether any d10-14 melon-wave response exists that keeps V identity.
   - Why here: R uses no judge compute, both in-flight packages already fire on 31/104 of these seats, and C1 inherits the same denominator.
3. **Read TILELEASE1 + PRICEDASK1 together, then decide C1.** If C1 is still distinct, freeze `(dev_frac scale, extra h1 hires from d10)` = (1.15,0), (1.15,2), (1.30,0), (1.30,2).
   - Dose check first: more completed plantings with same-day water, with the wall (d6-10 strawberry tiles within 1, d15-17 >= PFS-2) and herd service (escapes not above PFS) preserved and wages affordable.
   - A higher requested count alone is no dose.
4. **DSM tail as per-day quotas on the bridge, only if the bridge survives.** Q4 d10 h9-12 after the melon receipts; strawberries 4/2/3/2 d10-13; wheat 12/12/8/8/10/8/7/8 d10-17; carrots from d19; crew and watering to match. Copy feasible work, not tile coordinates.
5. **Labour-priced mix (TURN_COST) last.** Judge wheat price effects on both farms' sales and feed buys. No standalone timing or herd additions without new causal evidence.

### E. One gate for any fired package
Astra's candidate gate and the standing ship rule, merged into one.
- Every leg is paired vs the deployed PFS anchor on identical boards and seeds, with board-clustered t.
- All legs must pass. A leg not judged by the deadline leaves the package unqualified.

1. **Dispatch.** OFF is byte-identical to PFS. Unfired V56 identity is exact on all 61 games (v21 21 + m40 40), so the V56 deltas are exact zeros. Fire counts per family are reported.
2. **p48c 80 g.** Own >= +2,000 (t >= 3), and the pooled paired margin over V56 61 (zeros) + p48c 80 at t >= 2. With V exact, this is in effect p48c margin t >= 2, stricter than astra's margin >= 0.
3. **big 40 g.** Margin >= 0.
4. **Faithful fired18 tapes, on the JC1-faithful-both retained support.** Margin >= 0, and W not below PFS on that same support (full baseline 4/18; exclusions listed). The P48-code seats' margin must also be >= 0 on its own.
5. **No negative set, gift-free.** No set in 2-4 has d-margin < 0 or d-rival > 0 at t >= 2.
6. **Units.** d15-17 strawberry units and d18-29 animal units (E+M+W) not below PFS on p48c and big.
7. **Speed.** apply p99 < 0.65 s.

Passing qualifies a package against the judges we have. It does not prove transfer to a reacting real P48 opponent.
