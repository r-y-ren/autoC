# REACTCLONE1: our bodies against a REACTING rival (the r5a3 clone), closed loop (2026-09-28, 21:00Z-21:58Z)

Stream dir `S/reactclone1/`. Evidence and harness only: no src, dist, package or clone-cfg change, no upload. Remote CPU only for the grid (3 python workers, `~/stage_reactclone1`, no GPU); local 1 process at `nice 19 ionice -c3` for the python-engine references.

## Verdict
- **The harness is exact.** The fast env with the clone reacting in the rival seat reproduces the python engine to the coin on 4/4 reference games: PFS, V56 forced, clone self-play and GUARD=0 vs GUARD=1. Both purses match, and so does the cash of both seats at h1, dawn d10 and dawn d18. `judge.sh` end-to-end reproduces 4/4 grid rows.
- **The clone is a much weaker rival than the programme.** Against PFS on the original seats it earns **89.8k**. The live programme rival earned **104.1k** on the same seats (ratio 0.875; only 7/40 seats higher), and the recorded tape earns 110.5k against PFS open loop.
  - PFS beats the reacting clone **79/80, +34.7k** margin (t 16.0). Against the tapes on the same boards it wins 10/40 at -7.7k.
  - So closed-loop **flips are saturated for our tree bodies**. Read the contrasts in coins and margin, not wins.
- **Fire effect (V56 forced - PFS), closed loop: -1 flip, dours -2,679 (t -2.58), dtheirs -5,410 (t -6.09), dmargin +2,731 (t +2.00).**
  - The tape on the same 40 boards said **+12 flips, dours +6,411, dtheirs -18,871, dmargin +25,281**.
  - So the tape overstated the rival cut 3.5x and the margin gain 9x (20x on the original seats: +1,232, t 0.66). It also got **the sign of our own purse wrong**.
  - The closed loop reproduces the sign pattern of FIRELIVE1's live truth (13 faithful seats: dours -5,995, dtheirs -3,784).
  - By phase, V56 moves +14.5k of our cash into d10-17 (the melon plate), pays -3.3k in d0-9 and gives back **-13.9k in d18-29** after the hand-back. The rival loses only -4.4k in d10-17 and -5.4k in all.
- **GUARD=0 vs GUARD=1 (clone vs clone), closed loop: +34/-4 = +30 flips of 80 (G0 wins the head-to-head 64-16), dours +4,656 (t +6.08), dtheirs -1,276 (t -1.47), dmargin +5,932 (t +6.12).**
  - The tape on the same 40 boards said +2 flips, dours +3,574, dtheirs **-9,516**.
  - **PRICEFAITH1 was right about the rival cut:** closed loop it shrinks 7x, to an insignificant -1.3k.
  - **But GUARD=0 is not an artefact:** its own-purse gain is real, and larger closed loop (+4.7k, t 6.1). It is all late (our d18-29 cash +5.0k).
  - It is measured against the GUARD=1 clone only, not against PFS or the programme.
- **Clone vs PFS, closed loop:** the clone only ties itself (self-play is a mirror: margin 0 by construction, 12/80 exact ties), while PFS beats the same rival by +34.7k. That is **-45 flips / -34.7k margin** for the clone. The tape said the two are equal (+1 flip, dmargin -7) on the same boards, so **the tape flattered the clone by ~35k**. This is consistent with PRICEFAITH1: every clone band win is on a broken tape.

## 1. Harness (`S/reactclone1/rc.py`, `fastenv/`)
- **Engine.** The bit-exact fast env (`fastenv/kag.py` + `libkag.so`, `kh.py`), copied from PRICEFAITH1 (= BCSIM1 C++ port + the per-farm sales ledger). Decisions and RNG are untouched. `kh.py` differs only in the path of its `kag` import.
- **The rival seat is the clone, reacting.** r5a3 params, decoded exactly as CAPAUDIT1/PRICEFAITH1 decode the clone (`kh._decide`: one batched JAX-CPU forward per unit slot for all N games, then the agent's own overlays from `S/capaudit1/agent/main.py` with that game's ledger swapped in). Cell = CAPAUDIT1 **ctrl**: GUARD=1, CARE=1, caps90, land fix L7t70 (LAND=7, LAND_T=70, LAND_R=800, LAND_END=14), END=1, M3=1, WATER1=1, greedy.
  - **Deviation from the dispatch: no SALE=3.** SALE runs a shadow V56 kernel (a second production runtime) inside the clone every step. The fast env does not carry it, and every fast-env clone number to date (BCBODY6, CAPAUDIT1, PRICEFAITH1) is without it. So the rival is the ctrl cell those tape numbers use, which is also what makes the tape-vs-closed-loop comparison like-for-like.
- **Our seat, `--body tree`.** The production runtime from the vrp18 tree (`S/firebank1/tree/src`, 599f8881), built exactly as `S/judgeall1/ja_leg` builds it (gate2legs1 -> bandleg1 -> ml1leg `_init`: LE.SWITCHES + arm switches, head_940 residual, theta7659, SAFETY_S 1e9, REPAIR_MS 1e7). One fresh `runtime.make_agent` per game, built before the game; the game runs inside `ev._vendored_imports(True)`, as `ev._play` does against a file agent. It is fed the kaggle-shaped observation (structified, `remainingOverageTime` 60) and the kaggle configuration.
- **Our seat, `--body clone`.** A second clone (its own params and cfg), decoded by `kh._decide` in its own batched call. Self-play uses the same r5a3 params.
- **Arms.**
  - (a) **PFS** = vrp18 tree, `KERNEL2_ON=True,KERNEL2_NOOP_H0=False,KERNEL2_INHERIT=True,KERNEL2_FIRE_CASH=99999,KERNEL2_PRELOAD=False,KERNEL2_HANDBACK_DAY=18` (FIRELIVE1's OFF string = the vrp20_pfsoff package).
  - (b) **V56 forced** = the same with `KERNEL2_FIRE_CASH=26|29|2046|2338|2438|938`. **938 is the clone's hour-1 cash against our tree on all 80 seats** (`res/h1scan.csv`; in clone self-play it is 964, the programme's value). So V56 fires at step 1 on every game and hands back on d18.
  - (c) **clone r5a3 ctrl** (self-play). (d) **clone r5a3 GUARD=0** (the rest of the ctrl cell kept).
- **Boards.** `boards_m40.json` = the BCKNOB1 Stage A 40 MELON band seats (the first 40 of the 116; rival R0 2,576-2,732+). Only seed and town are used; the rival tape is not. Each board is played in both seat orders: 80 games per body, 320 in all. Batches of N=20 in lockstep; `grid.sh` / `grid2.sh`, 21:13-21:45Z (320/320 games).
- **Rows** (`res/<body>_h{1,2}.csv`): both purses, both cash at h1, dawn d10 (step 240) and dawn d18 (step 432), plus the per-farm sales ledger (`*_sal.jsonl`).
- **Throughput.** 20 games per 5-6 min per worker on the shared remote CPU (load 8-14 on 8 cores): clone forward ~170 s per batch per clone seat, vrp18 tree ~110-175 s per batch.

## 2. Fidelity: fast env == python engine, money-exact
The reference is `ref.py`: the kaggle engine through `ev._play` with a pinned seed and town. Our tree is built the ja_leg way; the clone is a kaggle FILE agent (`mkwrap.py` -> `wrap_ctrl.py` / `wrap_g0.py`: its own module image of `S/capaudit1/agent/main.py`, cfg set at every call). 1 local process, 42-64 s per game.

| game (board, our seat) | engine | ours | rival | cash h1 (ours / rival) | dawn d10 | dawn d18 |
|---|---|---|---|---|---|---|
| PFS vs clone ctrl (tape_highfrequencyf_114080894, 0) | python / fast | 121,832 / 121,832 | 66,532 / 66,532 | 1,409 / 938 both | 5,967 / 2,024 both | 26,748 / 29,924 both |
| V56 forced vs clone ctrl (tape_readyornothere_114083096, 1) | python / fast | 140,613 / 140,613 | 90,816 / 90,816 | 1,409 / 938 both | 2,132 / 1,259 both | 42,109 / 30,226 both |
| clone ctrl vs clone ctrl (tape_highfrequencyf_114080894, 0) | python / fast | 76,753 / 76,753 | 76,753 / 76,753 | 964 / 964 both | 562 / 562 both | 32,935 / 32,935 both |
| clone G0 vs clone ctrl (tape_tineshagent_114084557, 0) | python / fast | 85,430 / 85,430 | 75,004 / 75,004 | 964 / 964 both | 1,410 / 741 both | 37,017 / 33,581 both |

- **4/4 EXACT**, checkpoints included (`logs/ref3.log` vs `res/*_h1.csv`). The remote smoke equals the local smoke over 30 steps.
- `judge.sh` end-to-end (tree mode, vrp18 PFS, 2 boards x 2 seats, NW=1): 4/4 rows identical to the grid's pfs rows (`res/jsmoke.csv`).
- **Self-play is a mirror.** With identical policies, (board, seat 0) and (board, seat 1) are the same game with the roles swapped. So the self-play margin is exactly 0 over the seat pair, and 12/80 games are exact ties. Asymmetries (market order, the weed RNG) decide the other 68.


## 3. The grid and the contrasts (`res/tables.md` = `an.py` output; per game `res/<body>_h{1,2}.csv`)
Gaps are the change in (ours - rival) cash over the phase: d0-9 = start to dawn d10, d10-17 = dawn d10 to dawn d18, d18-29 = dawn d18 to the end. "orig seat" = the seat we held in the recorded live game.

### Grid (closed loop vs the reacting clone rival r5a3 ctrl; W = ours > rival)

| body | n | W | ties | W seat0 / seat1 | mean margin (t) | ours | rival | margin seat0 / seat1 | gap d0-9 | gap d10-17 | gap d18-29 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PFS unfired (vrp18, FIRE_CASH=99999) | 80 | **79/80** | 0 | 39/40 / 40/40 | +34,689 (+15.96) | 124,795 | 90,106 | +33,713 / +35,664 | +4,371 | -11,972 | +42,291 |
| V56 forced (vrp18 + 938 on the fire list, D18 hand-back) | 80 | **78/80** | 0 | 39/40 / 39/40 | +37,420 (+20.83) | 122,116 | 84,696 | +37,534 / +37,306 | +1,496 | +6,857 | +29,067 |
| clone r5a3 ctrl (self-play) | 80 | **34/80** | 12 | 19/40 / 15/40 | +0 (+0.00) | 93,987 | 93,987 | +909 / -909 | +0 | +0 | +0 |
| clone r5a3 GUARD=0 | 80 | **64/80** | 0 | 32/40 / 32/40 | +5,932 (+7.38) | 98,642 | 92,710 | +6,063 / +5,802 | -95 | +798 | +5,229 |

### Paired contrasts, closed loop (same board + seat; flips = W changes)

| contrast | set | n | flips | dours (t) | dtheirs (t) | dmargin (t) |
|---|---|---|---|---|---|---|
| V56 forced - PFS (fire effect) | all | 80 | +1/-2 = **-1** | -2,679 (-2.58) | -5,410 (-6.09) | +2,731 (+2.00) |
| V56 forced - PFS (fire effect) | seat 0 | 40 | +1/-1 = **+0** | -1,888 (-1.29) | -5,708 (-4.21) | +3,821 (+1.86) |
| V56 forced - PFS (fire effect) | seat 1 | 40 | +0/-1 = **-1** | -3,470 (-2.33) | -5,112 (-4.38) | +1,642 (+0.90) |
| V56 forced - PFS (fire effect) | orig seat | 40 | +0/-1 = **-1** | -3,784 (-2.59) | -5,016 (-4.17) | +1,232 (+0.66) |
| clone - PFS | all | 80 | +0/-45 = **-45** | -30,809 (-17.58) | +3,880 (+3.53) | -34,689 (-15.49) |
| clone - PFS | seat 0 | 40 | +0/-20 = **-20** | -29,548 (-11.90) | +3,256 (+1.99) | -32,804 (-9.99) |
| clone - PFS | seat 1 | 40 | +0/-25 = **-25** | -32,069 (-12.89) | +4,504 (+3.05) | -36,573 (-11.96) |
| clone - PFS | orig seat | 40 | +0/-23 = **-23** | -32,232 (-12.79) | +4,643 (+3.09) | -36,875 (-11.71) |
| clone GUARD=0 - GUARD=1 | all | 80 | +34/-4 = **+30** | +4,656 (+6.08) | -1,276 (-1.47) | +5,932 (+6.12) |
| clone GUARD=0 - GUARD=1 | seat 0 | 40 | +15/-2 = **+13** | +4,082 (+3.89) | -1,072 (-0.83) | +5,154 (+3.70) |
| clone GUARD=0 - GUARD=1 | seat 1 | 40 | +19/-2 = **+17** | +5,230 (+4.67) | -1,481 (-1.26) | +6,711 (+4.95) |
| clone GUARD=0 - GUARD=1 | orig seat | 40 | +18/-1 = **+17** | +5,391 (+5.26) | -1,552 (-1.29) | +6,944 (+5.35) |

### Same contrasts OPEN LOOP on the same boards (recorded rival tape, original seat only)

sources: PFS = S/bandbank2/res/pfs_band2.csv (BCKNOB1 PFS base); V56 = S/bandfamily1/res/v56.csv (open-loop V56 arm, 40/40 of these seats); clone ctrl / G0 = S/capaudit1/res/grid_all.csv (the same cells, open loop)

| contrast | set | n | flips | dours (t) | dtheirs (t) | dmargin (t) |
|---|---|---|---|---|---|---|
| V56 forced - PFS (fire effect) | tape, 40 boards | 40 | +15/-3 = **+12** | +6,411 (+1.81) | -18,871 (-4.80) | +25,281 (+3.58) |
| V56 forced - PFS (fire effect) | closed loop, same seats | 40 | +0/-1 = **-1** | -3,784 (-2.59) | -5,016 (-4.17) | +1,232 (+0.66) |
| clone - PFS | tape, 40 boards | 40 | +7/-6 = **+1** | -7,609 (-2.65) | -7,602 (-1.72) | -7 (-0.00) |
| clone - PFS | closed loop, same seats | 40 | +0/-23 = **-23** | -32,232 (-12.79) | +4,643 (+3.09) | -36,875 (-11.71) |
| clone GUARD=0 - GUARD=1 | tape, 40 boards | 40 | +3/-1 = **+2** | +3,574 (+2.23) | -9,516 (-3.08) | +13,090 (+3.38) |
| clone GUARD=0 - GUARD=1 | closed loop, same seats | 40 | +18/-1 = **+17** | +5,391 (+5.26) | -1,552 (-1.29) | +6,944 (+5.35) |

### Tape grid rows on the 40 boards (open loop, original seat)

| body | n | W | mean margin | ours | rival (tape) |
|---|---|---|---|---|---|
| PFS unfired (vrp18, FIRE_CASH=99999) | 40 | 10/40 | -7,662 | 102,826 | 110,488 |
| V56 forced (vrp18 + 938 on the fire list, D18 hand-back) | 40 | 22/40 | +17,619 | 109,236 | 91,617 |
| clone r5a3 ctrl (self-play) | 40 | 11/40 | -7,669 | 95,216 | 102,886 |
| clone r5a3 GUARD=0 | 40 | 13/40 | +5,421 | 98,790 | 93,369 |

### Rival strength: the reacting clone vs the programme rivals (same boards, original seat; live = the recorded live game)

| set | n | live programme rival | live ours | tape rival vs PFS (open loop) | clone rival vs PFS (closed) | clone rival vs clone (self-play) | clone rival vs V56 |
|---|---|---|---|---|---|---|---|
| orig seat | 40 | 104,125 | 109,150 | 110,488 | 89,811 | 94,454 | 84,794 |

clone-rival / live-rival money ratio (vs PFS, per seat): mean 0.875; seats where the clone rival earns more than the live rival: 7/40


### Per-phase purse contrasts (cash change within the phase, paired mean over 80 games)
| contrast | purse | d0-9 | d10-17 | d18-29 |
|---|---|---|---|---|
| V56 forced - PFS | ours | -3,263 | +14,450 | -13,865 |
| V56 forced - PFS | rival | -389 | -4,380 | -642 |
| GUARD=0 - GUARD=1 | ours | -64 | -297 | +5,018 |
| GUARD=0 - GUARD=1 | rival | +30 | -1,095 | -211 |

## 4. Closed loop vs the open-loop numbers we had
| contrast | closed loop, 80 games (this stream) | tape, same 40 boards (orig seat) | earlier tape / live reads | where the tape was wrong |
|---|---|---|---|---|
| **V56 forced - PFS** (fire) | -1 flip (ceiling), dours **-2,679** (t -2.58), dtheirs -5,410 (t -6.09), dmargin +2,731 (t 2.00) | +12, dours **+6,411**, dtheirs -18,871, dmargin +25,281 | BCEVAL1 27 live seats (tape): +12, dours +13,668, dtheirs -15,559. FIRELIVE1 LIVE (13 faithful): **-3** vs judge +3.30, dours **-5,995**, dtheirs -3,784 | Too optimistic: it overstated the denial 3.5x and the margin 9x, and the sign of our own purse is wrong. The closed loop agrees with live in sign |
| **clone - PFS** | -45 flips, dours -30,809, dtheirs +3,880, dmargin -34,689 (t -15.5); the clone ties itself, PFS beats it 79/80 | +1, dours -7,609, dtheirs -7,602, dmargin -7 | BCBODY6 fast-env 116 (tape): ctrl vs PFS -2; BCKNOB1 CARE=1 116: 0 | Flattered the clone by ~35k margin: on tapes the clone equals PFS, against a reacting rival it is far behind |
| **GUARD=0 - GUARD=1** | **+30 flips** (64-16 head-to-head), dours **+4,656** (t 6.08), dtheirs **-1,276** (t -1.47), dmargin +5,932 (t 6.12) | +2, dours +3,574, dtheirs **-9,516**, dmargin +13,090 | PRICEFAITH1 116: +10, dours +3,918, dtheirs -9,956; JC1-faithful 33: +0, dours +707, dtheirs -8,827 | Put the gain in the rival's purse (a 7x overstatement: the rival cut is breakage, as PRICEFAITH1 said) and under-read our own purse (+3.6k tape, +4.7k closed). The own-purse gain is real |

## 5. Caveat: the rival is weaker than the programme
| set (original seat, 40) | live programme rival (recorded live game) | tape rival vs PFS (open loop) | clone rival vs PFS | clone rival vs clone | clone rival vs V56 |
|---|---|---|---|---|---|
| mean rival money | 104,125 | 110,488 | **89,811** | 94,454 | 84,794 |

- **Size of the gap.** The reacting clone earns 0.875x the live programme rival's money: -14.3k, and -20.7k against the tape. It earns more than the live rival on only 7/40 seats.
  - PFS in turn earns +22k more against it than against the tape (124.8k vs 102.8k), because the clone competes less for the same prices.
  - In margin terms, the clone is ~42k easier than the programme tape for PFS (+34.7k vs -7.7k).
- **What that means for the numbers.**
  - Win counts for our tree bodies are at the ceiling (PFS 79/80, V56 78/80), so flips cannot show a gain. The coin and margin contrasts are the read.
  - A body that beats the clone can still lose to the programme. Use this judge to rank bodies and to catch tape artefacts (sign and size of dours/dtheirs), not to project live flips.
- **Why the clone is weaker (from the numbers, not dissected further).** It has the programme's opening (hour-1 cash 964 in self-play = the programme's value). Its d10-17 is strong: PFS trails it by -12.0k in that phase. But PFS out-earns it by +42.3k in d18-29, which is BCKNOB1's "the MELON gap is the V56 sale layer" again. The dispatch's SALE=3 hand-back (not carried here) targets exactly that late economy. So a SALE rival would probably be stronger in d18-29.

## 6. The judge command (BCBODY7 / SHAPE1)
```
bash S/reactclone1/judge.sh <tree_src_dir | params.npz> <tag>     # launches NW=3 remote CPU workers (~12 min for 80 games), returns
bash S/reactclone1/judge.sh collect <tag>                          # W/80, margin, ours, rival, phase gaps + paired contrasts vs pfs / v56 / clone
```
- **Tree mode.** Our seat = that tree with `SW` (default = PFS unfired, the vrp18 OFF string).
- **Params mode.** Our seat = the clone with those params, cfg = the ctrl cell + `CFG` json overrides (e.g. `CFG='{"BCB_GUARD": "0"}'`).
- **Setup.**
  - The rival is fixed (r5a3 ctrl cell). The boards are `boards_m40.json`, both seats.
  - Env: `NW` (3), `N` (14), `BOARDS`.
  - The remote stage `~/stage_reactclone1` keeps the harness, its dependencies and `params/params_r5a3.npz`. Candidates go to `~/stage_reactclone1/cand/<tag>/`.
- **Budget.** Each worker is one python process. Keep NW + other remote CPU work within the host rule, and use no GPU.
- **Read.**
  - Compare dours, dtheirs and dmargin (t) against `pfs` and the clone baseline.
  - A body whose tape gain lives in dtheirs and disappears here is a tape artefact.

## 7. Files
- `rc.py`: closed-loop harness. `fastenv/`: engine + `kh.py` copy (`libkag.so` is not committed: `g++ -O2 -std=c++17 -shared -fPIC kagapi.cpp -o libkag.so`, as in BCSIM1; the remote stage has it). `ref.py` + `mkwrap.py`: the python-engine reference and the clone file-agent wrapper.
- `grid.sh`, `grid2.sh`: the remote grid (w2 was rebalanced at 21:20Z into chains A/B/C). `judge.sh`: the judge. `an.py`: tables.
- `boards_m40.json` (+ `_h1` / `_h2` halves, `boards_x2.json` smoke).
- `res/`: per-game csv + sales ledger jsonl per body, `h1scan.csv` (the clone's h1 cash), `tables.md`. `logs/`.
- Params, trees and replays are not committed (`params/` is a local copy of `S/bcbody1/agent/params_r5a3.npz`).
