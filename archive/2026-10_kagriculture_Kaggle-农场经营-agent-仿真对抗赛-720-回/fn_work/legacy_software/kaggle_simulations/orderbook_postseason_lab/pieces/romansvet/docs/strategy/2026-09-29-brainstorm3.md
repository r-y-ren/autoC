# BRAINSTORM3 (2026-09-29, fresh session; three participants: the Opus agent, the orchestrator, codex astra)

Seed (docs/strategy/2026-09-29-brainstorm2.md "Session summary", astra-brainstorm3.md s3): TRANSFER3 = the frozen three-body comparison
{PFS, CLSEARCH, G2} against a FAITHFUL programme rival once P48GRAPH2 clears its gates; while waiting, astra's cheapest kill test for the
HERD_RECEIPTS_18 timetable (astra-brainstorm2.md s2). Stream dir `S/brainstorm3/`, checkpoint `S/brainstorm3/checkpoint.txt`.

## Round 1 (13:35Z-14:25Z)

**Verdict.** HERD_RECEIPTS_18 fails the funding audit **0/12** (bar 10/12): NO BUILD. The first purchase, the d2 h1 cow, fails in 12/12. The
cash is there (about 630 after lot 1 against 400), but PFS's NW quadrant has **0 free tiles from d2 h2** until harvests open 1-3 tiles on d3
afternoon. In 3/12 the cow also displaces a later PFS spend (Q2 d5 h3 short 143 / 181; PFS's own d9 h3 Q3 short 176). Even with every
purchase allowed to slip, 2/12 reach 18 placed animals by d9 h12 (mean 14.6 vs PFS 11.4), and an advanced Q3 by d9 h3 fits in 4/12 (plus 1 seat whose own Q3 is d9 h3).
TRANSFER3 is ready to run the moment `p48` is registered. Identity is 6/6 exact for all three package trees. The dry runs work against
g0capsfix, p48c, V56 (exact on the VBAND1 control row) and a tree rival.

### A. HERD_RECEIPTS_18 funding audit (no games)
- **Prefixes.** 12 vrp20 (PFS, sub 56652418) live seats, 6 MELON + 6 V: the first 6 of each family by episode in CREWLOSS2's
  ledger_rerun.json. Replays are in `S/livewatch23/gz` (CREWLOSS2's gz dir holds 2 files only).
- **Replay (`S/brainstorm3/fund.py`).** The PORTGAP1 exact engine replay (`S/econcensus/census.py measure()` unchanged, d10 cut, 0 cash
  mismatches in 12/12) plus wrappers. Every commit (SELL / BUY_*), land and hire is logged in queue order with money before/after. Per hour:
  empty tiles and empty coop/pasture in unlocked quadrants, placed herd, shed/carried animals, PASS turns, feed ops, wheat price
  (`S/brainstorm3/res/steps_<ep>.json`).
- **Walk (`S/brainstorm3/audit.py`).** Astra's timetable as cumulative bought targets C/S/G, deduplicated against PFS's own purchases up to
  each hour:
  - d2 h1: 5/1/1
  - d4 h1: 5/1/2
  - d5 h3 (after Q2): 6/1/2
  - d7 h1: 6/1/5
  - d8 h17: Q3 first, then 7/2/6
  - d9 h1: 7/4/7
- **Audit rules** (conservative: baseline receipts only, no credit for extra production):
  - Extras transact at the END of their hour, after that hour's actual sales and after PFS's own same-hour buys, which are protected
    commitments.
  - Extra spend E(t) = animals + 1 feed wheat per extra animal per day (FEED_ALL, the vrp21 base) + 2,000 for the advanced Q3.
  - Every later PFS spend on d0-9 (seeds, feed wheat, Q2, hires, its own animals) must still clear: money_after - E >= 0.
  - Q3 must be bought by d9 h3.
  - Placement route: for every hour from the purchase to d9 h12, room (free tiles + empty structures, +25 once the advanced Q3 is owned)
    >= the extras bought. No PFS tile is displaced.

| fam | ep | PFS Q2 / Q3 | PFS herd d9 h12 C/S/G | k1 d2 h1 cow: cash m0 / same-hour sold / own buys / avail after | first failing purchase (strict) | reason, coins short | relaxed: placed d9 h12 (extras hour:kind) | Q3 alone by d9 h3 (cash gap at best hour) |
|---|---|---|---|---|---|---|---|---|
| V | 114918927 | d5h3 / d10h3 | 7/4/2 | 99 / 592 / 60 / 631 | k1 cow d2 h1 | no placement room d2h2 (room-need -1) | 15 (d3h16:C d7h1:G) | NO (484) |
| MELON | 114922257 | d5h3 / d10h3 | 5/3/4 | 104 / 591 / 60 / 635 | k1 cow d2 h1 | displaces a later PFS spend d5h3 LAND Q2 short 143 | 14 (d4h1:G d7h1:G) | NO (1005) |
| V | 114923741 | d5h3 / d10h3 | 5/6/1 | 89 / 592 / 60 / 621 | k1 cow d2 h1 | no placement room d2h2 (room-need -1) | 20 (d3h16:C d9h1:G d9h1:G d9h1:G d9h1:G d9h1:C d9h1:G d9h1:G) | d9h1 (-3109) |
| V | 114925209 | d5h3 / d9h3 | 7/2/2 | 89 / 592 / 60 / 621 | k1 cow d2 h1 | displaces a later PFS spend d9h3 LAND Q3 short 176 | 12 (d5h0:G) | base (-651) |
| V | 114925938 | d5h3 / d10h3 | 8/3/1 | 128 / 592 / 90 / 630 | k1 cow d2 h1 | no placement room d2h2 (room-need -1) | 14 (d3h14:C d7h1:G) | NO (721) |
| MELON | 114926674 | d5h3 / d10h3 | 5/2/2 | 98 / 591 / 60 / 629 | k1 cow d2 h1 | no placement room d2h2 (room-need -1) | 10 (d3h14:C) | d8h17 (-522) |
| V | 114927542 | d5h3 / d10h3 | 7/3/2 | 68 / 592 / 30 / 630 | k1 cow d2 h1 | no placement room d2h2 (room-need -1) | 13 (d3h16:C) | d8h17 (-840) |
| V | 114928132 | d5h3 / d10h3 | 5/5/2 | 102 / 592 / 60 / 634 | k1 cow d2 h1 | no placement room d2h2 (room-need -1) | 19 (d3h16:C d9h1:G d9h1:G d9h1:G d9h1:G d9h1:C d9h1:G) | d8h17 (-2639) |
| MELON | 114929695 | d5h3 / d10h3 | 4/2/3 | 107 / 590 / 59 / 638 | k1 cow d2 h1 | displaces a later PFS spend d5h3 LAND Q2 short 181 | 17 (d5h0:G d9h1:C d9h1:C d9h1:G d9h1:G d9h1:C d9h1:G d9h1:S) | d8h17 (-3402) |
| MELON | 114934555 | d5h3 / d10h3 | 7/3/2 | 98 / 591 / 60 / 629 | k1 cow d2 h1 | no placement room d2h2 (room-need -1) | 13 (d3h14:C) | NO (806) |
| MELON | 114937683 | d5h3 / d10h3 | 6/5/1 | 107 / 590 / 60 / 637 | k1 cow d2 h1 | no placement room d2h2 (room-need -1) | 15 (d3h14:C d7h1:G d9h1:G) | NO (617) |
| MELON | 114939034 | d5h3 / d10h3 | 7/2/2 | 99 / 591 / 60 / 630 | k1 cow d2 h1 | no placement room d2h2 (room-need -1) | 13 (d3h16:C d7h1:G) | NO (497) |

- **Count.** Strict: **0/12** fund 18 placed by d9 h12 with no Q2 delay and Q3 by d9 h3. The first failing purchase is **k1 (d2 h1 cow)**
  in 12/12:
  - 9/12 fail on no placement route: room minus need = -1 from d2 h2.
  - 3/12 fail on a displaced later PFS spend: Q2 short 143 and 181, PFS's own d9 h3 Q3 short 176.
  - Every one of the 12 also has room -1.
  - Feed at 0.5 wheat/day gives the same 0/12 (shortfalls 98 / 136 / 67).
- **Relaxed read.** Every item may slip to the first later hour where it is affordable, keeps later PFS spends clear and has room. Result:
  2/12 reach 18 (both with Q3 on d9 h1). An advanced Q3 by d9 h3 fits in 4/12. The cow lands on d3 h14-16 in 9/12, once harvests free a tile.
  The d7 geese and the d9 sheep mostly never fit.
- **Q3 alone** (no extra animals) by d9 h3: fundable in 6/12, one of them PFS's own d9 h3. The other 6 are short **484-1,005** at the best
  hour, with PFS's own d8-9 animal buys kept.
- **Why P48 does it and PFS cannot, d0 unchanged** (PORTGAP1 led.jsonl, h12 means, 56 P48 / 88 PFS seats):
  - P48 fills Q1 too (25 used tiles on d2).
  - On d3-5 P48 swaps harvested crop tiles into animals: plants 20 -> 17 -> 17 -> 16.3, animals 5 -> 6 -> 7 -> 8.3. Q2 comes only on d6 h3.
  - PFS replants: plants 19 -> 18 -> 15.9, animals flat at 6 until Q2 on d5 h3.
  - So the d2-5 herd gap is a **tile-use choice on d3-5** (crop replant vs pasture), not a receipts problem. The timetable's "d0 unchanged,
    crops are commitments" premise makes the d2-5 purchases unplaceable by construction.
- Files: `S/brainstorm3/res/audit.md` (both feed rates, per-checkpoint cash / same-hour sold / own buys / cost vs available / run slack /
  room), `audit.json`, `greedy.json`, `S/brainstorm3/logs/q3alone.txt`, `q1room.txt`.

### B. TRANSFER3 preparation (`S/brainstorm3/transfer3/`)
- **Arm trees.** `mktrees.sh` recreates them (not committed): `pkg/<arm>` is the extracted dist package; `tree/<arm>/src` is the git archive
  of its commit.
  - pfs = `dist/vrp20_pfsoff.tar.gz` e5d84f03 @ 8d670dad.
  - cls = `dist/vrp21_clsearch.tar.gz` d93d6f5c @ b1835440.
  - g2 = `dist/ship_vrp21_bs2lp.tar.gz` b76283db @ 64a0101f.
  - All 27 package kagg3 files are byte-identical in the run tree, for all three arms. The run tree adds the 16 harness-only files
    (`agent/opening.py`, `es/`, `sim/`); `make_agent` needs `opening.py`, which the package lacks.
  - Package theta.npy / residual_head.npz == theta7659 / head_940, the harness's weights.
  - The package switches are plan.py defaults: cls REINVEST_DAILY "4:200:CSG" + FEED_ALL; g2 BANK_LATE_DAYS "8" + REINVEST_DAILY "4:200"
    + ALL_LANES + Q3GUARD 8 + FEED_ALL. Our seat adds only the PFS OFF string.
- **Identity (6 games per arm vs g0capsfix, m76 boards 1-3 x 2 seats; `idcheck.py`).** Exact on all 8 money fields for **6/6 pfs** vs
  `S/clsearch1/ctl/m76_ctl.csv`, **6/6 cls** vs `S/clsearch1/res/r3_fc_m76q0.csv` and **6/6 g2** vs `S/brainstorm2/res/bs2r3_G2_80.csv`.
- **Board manifests (`mkboards.py`, `manifest.json`).** 116 fresh boards: 69 from TOPAUDIT1 top-10 replays, then 47 from our livewatch23
  games. Order is md5(ep). Disjoint by ep AND by seed from 33 board files (330 seeds): m40, m76 (all 76), live27, the 56 real P48 boards
  (incl. the 16), v21, and every BRAINSTORM2 / CLSEARCH1 / REACTCLONE1 subset.
  - `boards_screen40.json`: 40 boards x 2 seats = 80 per arm.
  - `boards_confirm76.json`: 76 x 2 = 152 per arm, untouched until the screen is read.
  - `boards_id6.json`: m76 boards 1-3.
  - `boards_dry1.json`: screen board 1.
  - V56 arm (coordinator 14:0xZ): `S/vband1/boards_v21.json`, seat 0. VCHECK1's cls/g2 rows and VBAND1's PFS control rows are reusable as
    they stand (same trees).
  - Rival arms and bars: `grid.json`.
- **Runner (`t3run.sh`).** `bash S/brainstorm3/transfer3/t3run.sh --rival <cfg> [--arms pfs,cls,g2] [--set screen|confirm|id|dry|v21|<file>] [--seats] [--nw <=2]`
  - Clone cfgs from `S/judgerival1/rivals.json` (g0capsfix, flood, big, p48c, pq4c; it syncs rcr.py + rivals.json as judge.sh does) run
    through `S/judgerival1/rcr.py` on the shared GPU1 fwd server.
  - Tree rivals from `transfer3/rivals_tree.json` run through `S/rivalp48/rp.py`. P48GRAPH2 registers `p48` once, with
    `--rival p48 --rtree <src> --rsw '<switches>'`.
  - `v56` runs through `S/vband1/vr.py` with the V56 bank agent.
  - Remote chains: one process each, nice 19 + ionice idle. Each launches only at 1-min load < 12, through
    `flock -o /home/user/gpu_launch.lock -c '...; sleep 90'`.
  - `t3run.sh collect <pfx>` pulls the results and runs the analysis.
  - The state + sales hooks are in `t3_rc.py`, which wraps the Runtime and the fastenv Env read-only.
- **Analysis (`t3an.py`).** Per tag: n, W, own / rival / margin, our d15-17 strawberry units, the rival's realised strawberry price d18-29,
  Q2/Q3 hour for both farms, herd placed at d9 h12 (ours | rival), our shed/carried animals at d9, escapes (all game and d0-14, both farms).
  Paired contrasts (every arm vs pfs, and g2 vs cls) report d-own / d-rival / d-margin with **board-clustered t** (seat deltas averaged per
  board), W flips +/-, the count of identical games, and both purses' books (EGG MILK WOOL FERT STRAW MELON coins, d0-9 / d10-17 / d18-29).
- **Dry runs** (all rows in `transfer3/res/`):
  - g0capsfix, 2 games per arm: PFS +63,081 margin, 62 strawberries d15-17; cls 46, g2 36; rival strawberry price about 185 in all three.
  - p48c, 2 games per arm: all three run; g2 -15.3k vs pfs on the one board, which is noise, not a read.
  - V56 (`v_114925209`, PFS): **115,266 / 119,643 = the VBAND1 control row exactly**.
  - Tree rival (`pfsself` = PFS as its own rival, dry only): 1 game, 154,691 / 155,186.
  - One side read from the identity boards (6 games, 3 boards): our d15-17 strawberries pfs 40.7 / g2 29.3 / cls 22.0 per game. This is
    the ordering VCHECK1 found against V56.
- **Launch commands** once `p48` clears its gates:
  - `t3run.sh --rival p48 --rtree <P48GRAPH2 src> --rsw '<sw>' --set screen` (3 x 80 games, 2 chains).
  - `t3run.sh collect t3_p48_screen`.
  - The confirmation set only after the screen read. p48c (`--rival p48c --set screen`) is the additional family-clone arm.

### My round-1 hypothesis
What transfers is **timing denial**: PFS's ~50 d15-17 strawberries ahead of V56's fixed wave, and the first melon sale. The herd-reinvest
gain does not transfer. It is measured against a rival that leaves the eggs/strawberries uncontested, and it is paid for with the d5-9
seed coins that fund that denial. Against a faithful P48, which builds its own 18-animal herd, I expect G2/CLSEARCH to be at most flat vs
PFS on margin.

### My round-2 cell
`REINVEST_SEED_KEEP = "STRAWBERRY"` on G2. On a live REINVEST day d5-9, the control's STRAWBERRY seed rows keep their place ahead of every
REINVEST lane, so reinvestment may spend only the other seeds' coins and the leftovers. Default "" = byte-identical OFF.
- Grid: {G2, G2+KEEP, CLS+KEEP} x V56 v21 seat 0 (21 games each) + V56 m40 (40 games each) first. Only if the V gate passes: p48c and
  g0capsfix on the TRANSFER3 screen boards, 80 games each.
- Bar:
  - V56 v21 W >= 12/21 and margin >= -1k vs the PFS control; m40 margin >= -1k.
  - Our d15-17 strawberries >= PFS's minus 5 units.
  - Then vs p48c: own >= +1.5k (board t >= 2) and margin >= 0; 0 escapes d0-14.
- The cell tests whether any herd gain survives once it no longer takes the V-denial coins. If G2+KEEP is flat vs PFS on p48c, the
  reinvest family is closed for the slot.

### Rule slips (logged, not repeated)
1. One repo-wide `grep -rn` (it walked `.claude/worktrees`). I killed my two literal PIDs after 131 s.
2. One command named the null device as a sed target and in a redirect; sed refused, so nothing was written.
3. A `sed -i` with an empty line number emptied my own `t3run.sh`; I rewrote it from the same text.

Remote: my staged trees (`cand/t3_*`, `cand/t3r_pfsself`), `S/brainstorm3` and `S/rivalp48` under `~/stage_reactclone1` were removed at the end; `t3run.sh` re-stages everything on each call.

## Round 2 (14:17Z-16:10Z): the KEEP repair, and the tile-use cell (ledger first)

Inputs: astra-brainstorm4.md s1-3 (KEEP semantics, EARLY_COW_TILE, the strawberry determinant) and the orchestrator's round-2 grid.

### A. REINVEST_SEED_KEEP (worktree `/mnt/e/_work/kagg3_wt_brainstorm3`, branch `brainstorm3_0929`)
- **Base.** b1835440 (uploaded vrp21 = CLS). G2's switch commits from the BRAINSTORM2 lineage are ported on top: BANK_LATE_DAYS
  (+ the MAX_TURNS / MIN_VALUE gates), REINVEST_ADDITIVE, REINVEST_ALL_LANES, REINVEST_Q3GUARD and POSTFILL (0c09c4fb, 60c34bd3, 45e8c838,
  e23167ae, b7a89977; one conflict resolved: CLSEARCH1's HERD_PLAN floor kept, `and not REINVEST_ADDITIVE` added). All default OFF.
  - Identity, g0capsfix, m76 boards 1-3 x 2: worktree OFF = **6/6 exact vs CLSEARCH1's r3_fc rows**; worktree + G2 switches = **6/6 exact vs
    BRAINSTORM2's bs2r3_G2 rows**; worktree as pure PFS (`REINVEST_DAILY=,FEED_ALL=False`) = **6/6 exact vs m76_ctl**.
- **Switch.** `REINVEST_SEED_KEEP="STRAWBERRY"` (comma list; "" = shipped graph), astra's semantics. On a live REINVEST day
  (from_day..REINVEST_LAST = d4-9):
  - the unmodified grant (the same `BUD.grant` on the values as they stood before the REINVEST / FEED_ALL lifts, same costs, wants,
    purse and shed room) is computed first;
  - its granted strawberry seed units are lifted to the value cap before the real grant. At the cap the grant ranks by value/cost, so a
    100-coin strawberry seed outranks every capped animal (300-500) and yields only to the capped feed wheat. The control's strawberry
    quantity and its coins are therefore reserved before any reinvest animal;
  - feed stays first, and land is already out of the purse. No seed want is raised.
- **Cells.** CLS+KEEP = worktree + KEEP; G2+KEEP = worktree + the G2 switch string + KEEP. The state log adds seed rows, strawberry tiles
  at h12 d0-20, herd at d2-4 h23, per-day sales and escapes.

- **V56 screen** (S/vband1/vr.py unchanged, the public V56 bank agent reacting, seat 0, one game per board; paired by board vs VBAND1's
  PFS rows; the VCHECK1 rows for CLS/G2 are reproduced exactly by `S/brainstorm3/van.py`). Tables: `S/brainstorm3/res/v56_v21.md`,
  `v56_m40.md`.

| set | body | n | W (vs PFS: flips) | margin | d-own (t) | d-rival (t) | **d-margin (t)** | our straw d15-17 | V56 straw px d18-29 | herd d9 C/S/G | esc d0-14 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| v21 | PFS | 21 | 13 | +3,099 | - | - | - | 50.9 | 89.2 | - | - |
| v21 | CLS (VCHECK1) | 21 | 4 (+0/-9) | -2,703 | +1,837 (1.43) | +7,639 (8.67) | **-5,802 (-5.13)** | 21.3 | 134.9 | - | - |
| v21 | G2 (VCHECK1) | 21 | 12 (+1/-2) | +32 | +932 (1.12) | +3,999 (3.62) | **-3,067 (-3.73)** | 30.6 | 108.7 | - | - |
| v21 | **CLS+KEEP** | 21 | **15 (+2/-0)** | +1,141 | +257 (0.31) | +2,215 (1.87) | **-1,958 (-2.63)** | 50.2 | 89.8 | 7.0/2.6/2.8 | 0 |
| v21 | **G2+KEEP** | 21 | **17 (+4/-0)** | +3,520 | +478 (0.43) | +56 (0.08) | **+422 (0.55)** | 48.4 | 90.6 | 6.4/3.9/1.8 | 0 |
| m40 | PFS | 40 | 38 | +7,862 | - | - | - | 48.5 | 71.1 | - | - |
| m40 | CLS (VCHECK1) | 40 | 21 (+0/-17) | +373 | +1,048 (1.12) | +8,537 (8.33) | **-7,489 (-8.24)** | 20.8 | 105.5 | - | - |
| m40 | G2 (VCHECK1) | 40 | 33 (+1/-6) | +6,121 | +889 (1.60) | +2,629 (4.46) | **-1,741 (-3.06)** | 27.8 | 84.8 | - | - |
| m40 | **G2+KEEP** | 40 | **38 (+2/-2)** | +7,293 | +721 (1.32) | +1,290 (2.25) | **-569 (-0.93)** | 47.9 | 71.5 | 6.2/4.0/2.2 | 0 |

- **KEEP restores the strawberry wall exactly.** Our d15-17 strawberries go back to PFS's level (CLS 21 -> 50, G2 31 -> 48 on v21; 28 -> 48
  on m40), and V56's late price follows (135 -> 90, 109 -> 91; 85 -> 72 on m40).
  - Books d10-29 vs PFS: strawberry is now -95 | +98 (CLS+KEEP) and -79 | +324 (G2+KEEP). CLS had been +2,489 | +9,879.
  - Only the purchase priority changed, not the harvest or lot schedule; the strawberry tiles at h12 d8/d12 are 22.6/30.0.
- **CLS+KEEP fails the V56 screen** (v21 margin -1,958, bar -1k), though W passes (15). The residual is **wool**: rival +2,656, ours -633.
  CLS's cows-first order leaves 2.6 sheep at d9, so V56's wool sells dearer. CLS+KEEP m40 was not run: it failed v21.
- **G2+KEEP passes the V56 screen on both sets**: v21 W 17 (+4/-0), margin +422; m40 W 38 (+2/-2), margin -569; strawberries >= PFS-3;
  0 escapes. Against G2 itself: v21 margin +3,489 (t 3.34), m40 +1,172 (t 1.46).
  - The id boards vs g0capsfix (6 games) showed the same: d15-17 strawberries clsk 43.3 / g2k 41.3 vs CLS 22.0 / G2 29.3 / PFS 40.7.
- **G2+KEEP on the TRANSFER3 screen boards** (40 fresh boards x 2 seats, `S/judgerival1/rcr.py` via `t3run.sh`, paired vs PFS on the same
  boards, board-clustered t; the PFS rows are also TRANSFER3's controls). Tables: `S/brainstorm3/transfer3/logs/collect_p48c.txt`,
  `collect_g0.txt`.

| rival | body | n | W (flips) | own | rival | margin | **d-own (t)** | d-rival (t) | **d-margin (t)** | straw d15-17 | rival straw px d18-29 | Q2/Q3 day | herd d9 C/S/G (shed) | esc d0-14 o/r |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| p48c | PFS | 80 | 79 | 126,397 | 94,189 | +32,209 | - | - | - | 48.4 | 166.2 | 5.17/10.17 | 5.8/3.1/1.4 (0) | 0/16 |
| p48c | G2+KEEP | 80 | 80 (+1/-0) | 126,810 | 94,770 | +32,040 | **+413 (0.61)** | +581 (1.04) | **-169 (-0.21)** | 49.1 | 164.5 | 5.17/9.93 | 6.0/3.4/2.1 (0.3) | 2/23 |
| g0capsfix | PFS | 80 | 78 | 121,815 | 93,895 | +27,920 | - | - | - | 48.3 | 167.3 | 5.17/10.17 | 6.1/3.2/1.6 (0.1) | 4/20 |
| g0capsfix | G2+KEEP | 80 | 77 (+0/-1) | 122,381 | 93,337 | +29,044 | **+566 (1.05)** | -558 (-0.82) | **+1,124 (1.18)** | 48.2 | 167.8 | 5.17/9.85 | 6.4/3.5/2.1 (0.4) | 0/22 |

  - Books d0-9 / d10-17 / d18-29 vs PFS, ours | rival:
    - p48c: EGG +17/+376/+356 \| 0/+3/-31; MILK -19/-121/+623 \| +8/+187/+458; WOOL 0/-244/+341 \| +44/-173/-125;
      FERT +34/+152/-116 \| -24/+31/-38; STRAW 0/+86/-981 \| 0/+769/+115.
    - g0capsfix: EGG +51/+263/+202 \| 0/+96/+99; MILK -40/-138/+265 \| +132/0/-142; WOOL 0/-310/+312 \| -71/-22/+322;
      FERT +42/+127/-65 \| -47/+116/-140; STRAW 0/-57/-48 \| 0/-337/-44.
- **Verdict A: the reinvest line closes.** G2+KEEP fails the screen bar (own >= +1.5k with t >= 2, margin >= 0, W >= control) on both
  clone rivals:
  - p48c: own +413 (t 0.61), margin -169. g0capsfix: own +566 (t 1.05), margin +1,124 (t 1.18), W -1.
  - The d5-9 seed coins were the purse, as astra computed. With the strawberry seeds kept, reinvestment adds only +0.3 C / +0.3 S /
    +0.6 G at d9 and brings Q3 forward about 0.3 day (d9.9 vs d10.2).
  - Before KEEP, G2 read own +3,106 / margin +4,395 on m76 vs g0capsfix. That gain was the strawberry concession: V56 takes it back,
    and the under-built clone does not.
  - KEEP is V-safe (v21 W 13 -> 17, margin +422; m40 W 38 -> 38, margin -569), so G2+KEEP is a no-harm body, not a gain. Nothing is
    packaged.

### B. EARLY_COW_TILE (astra s2): the ledger passes 10/12; no build from existing switches keeps the invariant
- **Ledger (`S/brainstorm3/tile.py`, no games).** The same 12 exact PFS prefixes as round 1. Replay observations are traced per NW tile
  through d29.
  - Candidate: an hour in d3-4 where a NW tile is empty (harvested) and PFS's next planting on it is WHEAT or CARROT.
  - Dedup: PFS's first later COW purchase is not made; the cow's baseline tile Y is then free.
  - Cash: E = 400 from the end of the step (after its sales and PFS's own buys) + 1 feed wheat/day, until the dedup. Every PFS spend
    before the dedup must clear.
  - Unit: >= 2 PASS unit-turns in t..t+3.
  - Displaced crop: every PFS planting on the tile before the dedup cow's placement needs ONE specific tile that is empty for its whole
    growth window, or it waits for Y.
- **Result: feasible 10/12 (bar 10/12).** The earliest feasible advance is **d3 h15-18** (a NW WHEAT tile after its first harvest,
  9/10) against PFS's own cow bought d5 h1 and placed d5 h6-13 (8/10) or d6 h1: an advance of **36-46 h**. Cash slack is 137-303, and
  the displaced wheat cycle waits 0-4 h (one 36 h).
  - Fails: 114926674 (no idle unit at the candidate hours; the only later cow is d8) and 114929695 (no PFS cow purchase before d10 h9).
  - Table: `S/brainstorm3/res/tile.md`.
- **Build attempt.** No new executor code; CLSEARCH1/HERD1's default-off stock floor `HERD_PLAN` on the worktree as pure PFS (identity 6/6
  above). 6 identity games vs g0capsfix, m76 boards 1-3 x 2:
  - `P|C:3:5` (5 cows from d3, served before competing seeds): the dedup works (the cow is bought at step 73 = d3 h1 and placed in the NW
    quadrant; PFS's d5 h1 cow is not bought). But it is funded from the d3-4 **strawberry seeds**: strawberry tiles at h12 d3/d4 are
    **0/0 vs PFS 1/3-4**, and the cells lose **own -4,655, margin -4,781/game**. This breaks astra's invariant ("never displace
    strawberry/melon planting").
  - `C:3:5` / `C:4:5` without the priority token: **6/6 games identical to PFS**. The planner never buys the cow on d3-4 from the dawn
    purse.
  - Why: the ledger's feasible advance is the **d3 h15 same-hour receipts on a just-harvested tile**, and PFS's day plan is made at h0
    from the dawn purse with the tile still planted.
  - A faithful EARLY_COW_TILE therefore needs an executor-level change (an intra-day pasture + buy on a harvested WHEAT/CARROT tile,
    funded after that hour's sales). I did not build it this round.
  - Value bound for that build: one cow about 1.6 days early is astra's +0..+0.9k gross planning range. B stops here; the 40-game read
    was not run.

### Answers
- **Orchestrator's round-2 hypothesis:** I agree in part.
  - The wall is the d15-17 units sold. Those units are fixed by the **d5-7 strawberry seed purchases**: strawberries first yield 10 days
    after planting, then every 2 days.
  - KEEP changed only the purchase priority, with no harvest or lot change. It restored 21 -> 50 units and V56's price 135 -> 90.
  - As predicted, KEEP passes V56 and loses the gain on p48c, so the reinvest line closes.
  - But first-melon-sale timing is not a lever for our body. On the 40 screen boards PFS sells **no melon before d14** (first sale
    d14, 94 units per game). p48c sells 14 by d11 and 40 by d13. The 246-vs-256 gap is the rival port's fidelity gate (P48GRAPH2), not
    PFS's.

### Round-3 proposal (mine): STRAW_WALL, more d15-17 strawberries than PFS, judged against V56 first
- **Premise.** The measured price response is linear:
  - V56 v21: 50.9 / 30.6 / 21.3 units -> 89 / 109 / 135 coins, about -1.5 coins per unit we sell in d15-17.
  - m40: -1.2 per unit.
  - The strawberry market is linear above I0 (1.92 coins/unit), and V56 sells a fixed ~208-unit wave on d18-29. So each extra d15-17
    unit costs V56 about 250-320 coins. It costs us about 75 on our own ~50 units and earns about 90, so our own is flat.
  - At about 2.5 units per d5-7 tile, **+4 tiles = +10 units = about +3k margin vs V56 and about +2k vs a 155-unit P48 wave** (planning
    arithmetic from the measured slope, not a result).
- **Why it is not already closed.** The mix and strawberry levers were judged against the clone, which leaves late strawberries
  uncontested (41-45 % of real volume). That judge cannot see denial; V56 can.
- **Switch.** `STRAW_WALL="<n>:5:7"` on pure PFS (the worktree as PFS, identity 6/6 above).
  - On d5-7 the strawberry plant target rises by n tiles, taken from free Q2 slots first and never from a melon or animal tile.
  - The seeds get KEEP's value-cap lift, feed stays first, and Q2 is not delayed.
- **Grid.** n in {2, 4, 6} x V56 v21 (21 games) + m40 (40 games) first; the cells that pass then go to the TRANSFER3 screen vs p48c,
  pq4c and g0capsfix (80 games each, PFS rows above reused for p48c / g0capsfix).
- **Bar.**
  - V56 v21 margin >= +1k (t >= 2) with W >= 13, and m40 margin >= 0 with W >= 37.
  - Our d15-17 strawberries >= PFS + 2n.
  - p48c / pq4c / g0capsfix margin >= 0, own >= -500 everywhere, 0 extra escapes.
- **Second cell,** if round 3 has room: the executor-level EARLY_COW_TILE. A pasture and buy on the d3 h15 harvested NW wheat tile,
  funded after that hour's sales. Value bound: +0..+0.9k gross.

### Rule slips
None this round.
- Remote: ≤ 2 chains of one process each (nice 19 + ionice idle, launched through `flock -o` at load 2-5).
- One queue-name reuse (`q_t3_p48c_screen.txt`, pfs then g2k). It was harmless: the pfs chain had already popped its spec, and the queue
  pop is under flock. Tags include the arm now, so the queue name is the only shared part.

Files:
- Scripts: `S/brainstorm3/tile.py`, `van.py`.
- Tables: `S/brainstorm3/res/{tile.md, v56_v21.md, v56_m40.md}`.
- TRANSFER3 rows: `S/brainstorm3/transfer3/res/{r2id*, r2v_*, r2m_*, t3_p48c_screen_*, t3_g0capsfix_screen_*}`.
- Arms: `transfer3/arms.json` (package arms + worktree arms wcls / wg2 / wpfs / clsk / g2k / ect*).
- Worktree commit `5e9a3b4a` on `brainstorm3_0929`.

## Round 3 (15:13Z-17:15Z): EARLY_COW_TILE as an executor buy, STRAW_WALL ledger-first

Inputs: astra-brainstorm5.md s1-2 (STRAW_WALL re-priced on our own late book; EARLY_COW_TILE semantics) and VCHECK2 (the V wall also includes our late animal-product units).

### A. EARLY_COW_TILE as a same-row executor buy (worktree `brainstorm3_0929`, on pure PFS)
- **Build.** `EARLY_COW_TILE` (default 0 = shipped graph). Semantics:
  - On d3-4, after the day's grant has run unchanged, one cow is bought LAST in the day's first market row (TURN_BUY). Lot 1 sells
    earlier in the same row, so it is funded by realised receipts: the POSTFILL mechanism.
  - Budget = the purse left after the grant (net of hires, crew reserve, feed wheat, seeds) + lot 1's projected fill - 2 days of feed.
    Never on a land-buy day.
  - Only while the farm owns at most 4 cows (placed + shed + today's grant), so at most one cow is advanced per game.
  - The stock want is raised so the planner builds the pasture. No dawn stock floor, no seed priority.
  - The cell runs on pure PFS: the worktree with `REINVEST_DAILY=,FEED_ALL=False`, 6/6 exact vs m76_ctl. It is not a separate
    worktree from 8d670dad: the behaviour is identical and the switch is additive.
  - OFF identity: `EARLY_COW_TILE=0` with the r3 code is **6/6 exact vs m76_ctl** (8 money fields).
  - Deviation from astra's tile semantics: the pasture tile is the planner's, and the buy rides the h1 row, not the harvest hour. On
    the id games the cow stands in the NW quadrant on d3-4 (NW cows 5 at d4 h23).
- **Screen, ECT=1** (preregistered: the first 10 TRANSFER3 screen boards, seat 0, OFF vs ON, V56 via vr.py and p48c via rcr.py; the OFF
  p48c rows are the round-2 PFS screen rows). Table: `S/brainstorm3/res/ecow_screen.md`.

| rival | n | W off->on | d-own (t) | d-rival (t) | **d-margin (t)** | cows bought d1-9 off/on | herd d9 C/S/G off -> on | straw tiles d5 h12 off/on | straw d15-17 off/on | late EGG/WOOL/FERT units off -> on | esc d0-14 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| V56 | 10 | 10->9 (+0/-1) | -452 (-0.33) | +161 (0.14) | **-613 (-0.44)** | 13/23 | 5.3/5.1/1.3 -> 6.3/4.8/1.2 | 11.4/5.4 | 51.2/36.2 | 73/186/174 -> 68/175/180 | 0/0 |
| p48c | 10 | 9->10 (+1/-0) | +3,345 (1.47) | +546 (0.36) | **+2,799 (1.10)** | 10/18 | 5.0/4.3/1.1 -> 5.7/4.2/1.3 | 10.2/5.9 | 49.2/40.0 | 60/177/155 -> 68/175/156 | 0/0 |

  - Pooled 20: own +1,446 (t 1.06), margin +1,093 (t 0.75).
  - **Fails:** pooled t < 2; V56 margin < 0; cow purchases not unchanged (+1 cow/game); late animal units below PFS on V56 (eggs -5,
    wool -11).
  - First strawberry/melon sale days are unchanged (d15 / d21 V56, d15 / d15 p48c).
  - Books d10-29 on-off (ours | rival): V56 STRAW -255 | +2,388, MILK +365 | -2,792; p48c WOOL +1,591 | -392, MILK +1,084 | +232.
- **Mechanism.** The advanced cow is **additive**: PFS still buys its own d5-9 cows (cow buys 13 -> 23 over 10 games; d9 cows +1).
  - PFS's later cow purchases are value-driven, not stock-target-driven, so "count it toward PFS's target" does not happen by itself.
  - The extra 400 comes out of the d4-5 purse, which is exactly where the first strawberry batch is bought: strawberry tiles at d5 h12
    fall 11.4 -> 5.4 and d15-17 units 51 -> 36. V56 then sells its wave dearer (+2.4k).
  - Against p48c the extra milk/wool pays (+2.8k margin, t 1.10). Against V56 the lost wall costs more than the cow earns.
- **Screen, ECT=2** (= 1 + an explicit dedup: on d5 a farm owning more than 4 cows at dawn buys one cow fewer). Same 20 games, table
  `S/brainstorm3/res/ecow2_screen.md`:
  - V56: W 10->9, own -1,426 (t -1.23), rival +778, **margin -2,204 (t -1.95)**. Cows bought d1-9 13 -> 19 (+0.6/game), strawberry
    tiles d5 11.4 -> 5.3, d15-17 51.2 -> 39.3, V56 strawberry book +2,450, 1 extra escape.
  - p48c: W 9->10, own +3,087 (t 1.54), **margin +2,306 (t 0.79)**.
  - Pooled own +830 (t 0.67), margin +51 (t 0.03). **Fails.** The dedup removes part of the extra cow, but the d4 grant has already
    spent 400 fewer coins, and those were the first strawberry batch.
- **Verdict A: fails its screen in both forms.** The ledger's 137-303 "cash slack" is slack only against PFS's recorded spends.
  - The live planner re-plans every dawn and spends its whole purse by value per coin. So on d3-5 any coin moved to an animal is a coin
    taken from the d5 strawberry batch: the d15-17 wall.
  - No 80-game read was run.

### B. STRAW_WALL resource ledger: 0/12 at n=2 and at n=4 (bar 10/12), NO BUILD
- **Ledger (`S/brainstorm3/straw.py`, no games).** The same 12 exact PFS prefixes. For n TOTAL extra strawberry plantings on d5-7:
  - tile: a tile EMPTY in the baseline from its planting hour (after Q2) through +17 days, so occupancy is reserved through ages
    10/12/14/16 and the last harvest; distinct tiles;
  - cash: 100 per seed, and every later PFS spend through d9 must still clear;
  - labour: the engine turns a plant unwatered on its planting day, or on any two consecutive days, into WEED. So each extra tile needs
    1 PLANT + a WATER that day + a WATER every other day to age 16 + 4 HARVEST = 14 unit-turns. These must come out of the baseline's
    PASS unit-turns of each day, so no PFS action (hence no protected sale) moves.
- **Result: 0/12 for both n=2 and n=4.** The binding check is the tile. No tile in any prefix stays empty for 17 days from a d5-7 planting.
  - The longest empty run of any tile starting d5 h3-d7 h23 is **140-259 h** (need about 408). The 2nd longest is 43-186 h. Only 1-6
    tiles per prefix are empty for 96 h or more (`strawrun.py`).
  - PFS fills every Q2 tile it opens within about 6-11 days (Q3 comes on d10).
  - Cash (slack 309-761 after the extra seeds) and labour (PASS surplus >= 5 unit-turns every day d5-23) are **not** binding.
- **Reading.** A capped wall cannot be added on free tiles. Every extra strawberry displaces a later PFS planting on the same tile (the
  d8-12 melon/strawberry/wheat that PFS puts there). That is a substitution cell, which DRAWREACT2 measured at -4.9k / -8.6k own.
  Astra's sensitivity (own -889 / -1,815 at n=2 / 4) plus the missing tiles leaves no admissible dose. B stops at the ledger.

### Answers
- **Orchestrator's round-3 hypothesis:** false for PFS. The advanced cow did not add units without price pressure. Its coins were
  the d4-5 strawberry seeds:
  - strawberry tiles d5 11.4 -> 5.4, d15-17 units 51 -> 36, V56 strawberry book +2.4k;
  - V56 margin -0.6k / -2.2k (ECT 1 / 2);
  - the cow pays only against the clone, which leaves the late animal books uncontested (p48c +2.3 to +2.8k, t <= 1.1).
  - At PFS's purse, advancing an animal adds late units *and* removes the early strawberry units that hold V56's price. B fails
    earlier: no tile stays free for an extra strawberry (0/12).
- **Session established (BRAINSTORM3, three rounds):**
  1. V56's margin against us is set by our d15-17 strawberry units (51 -> 21 moves V56's late price 89 -> 135, about 9.9k) and our late
     animal-product units (VCHECK2). Both come from the first strawberry batch, which the d4-5 purse buys, and from the d9 herd.
  2. For the live planner, PFS's d3-9 purse and tiles are zero-slack:
     - reinvestment was paid from seed coins (KEEP restores the wall and erases the gain: p48c own +413, g0capsfix +566);
     - a d3-4 cow costs half the first strawberry batch (V56 -0.6/-2.2k);
     - no tile stays free 17 days for an extra strawberry (0/12);
     - HERD_RECEIPTS_18 is unplaceable (0/12).
  3. Clone rivals reward the animal books that V56 punishes. Every clone gain this session was a strawberry concession. Any body must
     clear V56 (v21 + m40) before any clone read.
  4. Nothing beat PFS. G2+KEEP is a no-harm body (V56 +422 / -569), not a gain.
- **STRAW_PULL ledger (my first candidate for BRAINSTORM4, run now; `S/brainstorm3/pull.py`, `res/pull.md`): 2/12, closed.** It would
  pull PFS's own d8-9 strawberry plantings onto their already-empty tiles on d6-7.
  - PFS already front-loads its strawberries: plantings d3 3 / d4 4-5 / d5 8-13 / d6 0-10. Only 0-3 fall on d8-9 (one prefix has 9).
  - Only 0-2 per prefix are pullable (tile empty since d6-7). Cash (slack 442-738) and labour (PASS surplus >= 5) are not binding.
- **What the per-day books show instead** (`S/brainstorm3/logs/strawdays.txt`). Against V56 (first 10 screen boards) the strawberry price
  **collapses to 20-47 coins on d21-24** (both farms sell 18-27 units a day) and **recovers to 52-107 on d25-28**, once both farms sell
  3-19 a day. PFS sells **about 64 units on d21-24 at 22-47**. Against p48c (80 games) the price never falls below 135.
- **BRAINSTORM4 first cell: `STRAW_FLOOR`, sale timing at fixed production (astra's seed).**
  - Switch: on d19-25, do not sell strawberries while the quoted price is below a floor f. Hold them in the shed, within its room, and
    sell from d26 at the recovered price. Default off. Production, plantings and every other product are untouched. Against p48c it never
    binds (price >= 135), so it is V-conditioned by construction.
  - Ledger first on the V56 per-day rows: units sold below f and shed room d19-25; bar: >= 20 held units/game fit in 10/10 games.
  - Then V56 v21 + m40 with f in {40, 60}. Bar: own >= +500 (t >= 2), margin >= +500, W >= control, late EGG/WOOL/FERT units >= PFS.
  - Then p48c / pq4c / g0capsfix at 80 games each, where it must be exactly neutral: identical games where the floor never binds.
  - Upper bound, arithmetic only: about 40 held units x (70 - 25) = about +1.8k own before our own repricing of d26-29.

### Rule slips
None this round.
- Remote: ≤ 2 chains of one process each (nice 19 + ionice idle, flock-gated at load 0.9-2.1). Remote staging was cleaned at the end.

Files:
- Worktree `brainstorm3_0929`: `EARLY_COW_TILE` (0 / 1 / 2) in `src/kagg3/core/plan.py`.
- Scripts: `S/brainstorm3/{straw.py, strawrun.py, r3an.py, pull.py}`; per-day strawberry books in `S/brainstorm3/logs/strawdays.txt`.
- Tables: `S/brainstorm3/res/{straw.md, ecow_screen.md, ecow2_screen.md, pull.md}`.
- Rows: `S/brainstorm3/transfer3/res/{r3id_*, r3v_*, r3c_*}`.

## Session summary (written by the orchestrator, 2026-09-29 15:42Z; three participants: the Opus agent, the orchestrator, codex astra — docs/strategy/2026-09-29-astra-brainstorm{4,5,6}.md)

**Rule applied:** 3 rounds, then this summary and a fresh session (BRAINSTORM4).

**Established (all closed loop, paired, with the faithful V56 rival on the 21 live V boards + m40 and the family-pure P48 clone p48c; V56 control W 13/21 +3.1k, 38/40 +7.9k):**
1. THE DETERMINANT of margin against our rival mix (57 % V, 26 % P48-code, 10 % other MELON, 7 % other) is our d15-17 strawberry supply sold before the rival's late wave (V56 208 units, P48 155, PQ4 168, Majkel 189): our 51 -> 21 units moved V56's late price 89 -> 135 = +9.9k to the rival (VCHECK1). PLUS our late animal-product volume: the head-offset candidate kept the wall (46 units) yet lost -6.2k because its offsets halved d9 geese and our late eggs / wool / fertilizer fell 122 -> 56 / 117 -> 89 / 142 -> 92 units (VCHECK2).
2. PFS's money AND tiles from d3 to d9 have NO SLACK in the live planner: the 18-animal timetable fails 0/12 (no free tile from d2; P48 grazes animals on harvested tiles where PFS replants), extra strawberry tiles fail 0/12 (no tile free for the ~408 h a d5-7 strawberry needs), the early cow is extra not advanced and its 400 coins are the first strawberry batch (units 51 -> 36-39). Every reinvest / herd / advance cell this session paid for its gain with first-batch strawberry coins or tiles.
3. KEEP (reserve PFS's own strawberry grant before any reinvest animal) restores the wall exactly (21 -> 50 units, V56 135 -> 90) and makes reinvestment V-safe (G2+KEEP v21 W 13 -> 17, margin +422 / m40 -569) but leaves no gain (p48c own +413, g0capsfix +566): the d5-9 seed coins were the whole reinvestment purse. REINVEST LINE CLOSED.
4. The clone rivals cannot see that cost: they under-sell eggs (30-43 % of real) and strawberries (41-45 %), so ES / search / reinvest against them reliably finds bodies that trade our late volume for uncontested strawberry coins (vrp21_clsearch, bs2lp, esheadcl all V-LOSS or V-flat). Every new body faces V56 BEFORE any clone read (gate addendum in memory).
5. Nothing beat PFS across the mix. The uploaded vrp21_clsearch is live-confirmed V-losing (37 games 21-16, V 18-14 in the sub-2,400 band where PFS is 44-12 / V 21-0). Slot: two PFS copies recommended (astra: operational cutoff 09-30 18:00Z for both uploads).

**Closed this session:** HERD_RECEIPTS_18 (0/12), REINVEST_SEED_KEEP as a gain, EARLY_COW_TILE (both implementations), STRAW_WALL (0/12), STRAW_PULL (2/12).
**Open:** programme transfer (P48GRAPH4 building the port's d1-4 cash engine: d0 wheat sales, fertilizer 5-7/day, seeds after the h8 cow); rival fidelity (CLONEMKT1's market-head loss x4: income +4.2k over p48c, melon 53.8 / 71); bounded sale timing at fixed production.

**BRAINSTORM4 seed (astra's amendment of the agent's STRAW_FLOOR, agreed):** STRAW_WAIT1=(f,8): at PFS's existing h17 sale on d21-25 defer at most 8 strawberries in total, only when the marginal price is below f, projected shed occupancy (100-unit shared shed) permits, and current-shop demand over the next 24 h exceeds twice a conservative public-state estimate of the rival's strawberry sales + 2; sell deferred stock at the next h17 regardless; overflow protection overrides; no double deferral. Ledger first (replay turn-level sales, deposits, demand ticks and shed occupancy with both farms' production fixed; reprice both books per unit; kill unless mean +500 own / +500 margin on 10 traces), then OFF identity 6/6, V56 v21 + m40 (own ≥ +500 t ≥ 2, margin ≥ +500 t ≥ 2, W ≥ 13 / 38, animal units ≥ PFS), one arm to the three 80-game clone checks (inactive games identical). P(pass) 10 %; the unconditional d26 dump ≤ 5 % (sensitivity: f=40 own +4.6k / V56 +4.6k / margin ~0; f=60 +7.1k / +8.5k / -1.3k). The invariant to break: at fixed production, withholding supply gives the rival at least as much as us — break it with paired receipts. Priors against: FLOORHOLD1 (-4..-7 band wins), SELLSPREAD1 (-1.2..-4.9k).
