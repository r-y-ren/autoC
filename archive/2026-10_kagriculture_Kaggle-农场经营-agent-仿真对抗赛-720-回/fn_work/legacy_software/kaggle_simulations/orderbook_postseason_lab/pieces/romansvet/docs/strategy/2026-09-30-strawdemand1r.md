Stream: STRAWDEMAND1R (remote-only)
Date: 2026-09-30 (committed by DOCSYNC1; verbatim S/strawdemand1r/2026-09-30-strawdemand1r.md, rows S/strawdemand1r/res/*.csv)
Verdict: NONE - demand-sized strawberry / wool cell (STRAW_DEMAND_ON) on PFS: glut removal is a two-purse wash

# STRAWDEMAND1R (2026-09-30): demand-sized strawberry / wool cell on PFS, closed-loop

Remote-only stream (/mnt/e down). Everything is on user@remote-host:/home/user/stage_r/strawdemand1r.

## Build
- tree = copy of ~/stage_reactclone1/S/pq4tail1/cand/t0 (PROG_* OFF = PFS). Patches patch.py..patch5.py: plan.py `STRAW_DEMAND_ON` (default OFF) + `_straw_demand` (last mix rewrite, after ESWORK, before PROGRAM_ENGINE); runtime.py `_straw_latch` (rival d2h0 melon tiles 1..10 = latch A; strawberry-consuming shop instances unlocked by d6 = k; log of the board draw, per-day asks, market inventory d15/18/23 per game in <cell>.sd.jsonl).
- Knobs: D0/D1 window, S0..S3 ask scale by k (cumulative, round-half-up), SEATS latched|all, SHEEP_CUT (latched only), FLAT (one scale), CAP0..3 (cap on STANDING strawberry tiles by k).
- OFF identity: 2/2 V56 m40 boards byte-identical to S/vband1 v56_ctl rows (97037/93046, 125669/122307). Logged identity arm L0 (ON, scale 1) = ctl on m40 40/40, v21 21/21, p16 32/32. Latch fires 0/40 m40, 0/21 v21, 32/32 p16, 64/64 executor: every latched cell is V56-identical by construction (Ls/Lw rows = ctl exactly).

## Judges
- V56: S/pq4tail1/vr.py, m40 (ctl W 38/40 +7,862) and v21 (13/21 +3,099).
- p16: rcr.py --rival p48c, S/p48graph1/res/boards_p48_16.json, both seats (n 32). Own OFF control (res/p48c/pfs.csv not on the remote): W 32/32 +26.5k, d18-29 straw 162 u @142: the clone does NOT glut, no flips possible. No-harm check only.
- ex9 (added): S/progagent1/fr.py, rival = PROGAGENT1 executor (PROG_AGENT_ON=9: a real P48 seat's tape d0-8, then PFS; t0 tree read-only), seats auto, 16 boards; ex9a/b/c = the same with the other three P48 tapes (p48_115161550_0, p48_115162799_1, p48_115165607_0). It reproduces the P48LOSS1R glut: ctl W 6/16 -5,542, our d15-29 straw 201 u @106, d23 market straw +54 over I0 (= the L class, +54).
- p48s (P48RIVAL1R faithful scripted rival): res/p48s/pfs.csv never appeared (v1 fidelity 7/34), not read.

## Finding 1: PFS strawberry ask is d3-7, not d8-14
Mean daily strawberry ask on m40: d3 4.2, d4 4.0, d5 10.6, d6 6.7, d7 1.6, then d8-14 0.2-2.3 (about 6 tiles in total). The named d8-14 cells cut 1.1-1.3 tiles and move nothing.

## Named grid (d8-14, scale 0.5/0.75/1.0/1.0 by k at d6; 3+ cannot occur at d6, max 2), paired vs OFF
| cell | V56 m40 (n40) | V56 v21 (n21) | p16 vs p48c (n32) |
|---|---|---|---|
| Ls latched, sheep 0 | = ctl (38/40) | = ctl (13/21) | -671 t -1.10, own -167 |
| Lw latched, sheep -2 | = ctl | = ctl | +213 t 0.23, own -7 |
| As all seats, sheep 0 | +213 t 1.25 (38/40) | -333 t -1.41 (13/21) | -671 t -1.10 |
| Aw all seats, sheep -2 | +213 t 1.25 | -333 t -1.41 | +213 t 0.23 |
ex9 Lw: -660 t -0.91, W 6->5.

## Extension (latched only, V-identical by construction)
Ask scale does not bind: the cumulative ask double counts re-asked tiles (X3f50 cuts 26 ask-tiles, standing strawberry d14 26.9 -> 26.0).
| cell | ex9 n16 dMarg (t) own / riv | W | d23 straw over I0 | p16 n32 dMarg (t) own |
|---|---|---|---|---|
| X3k d3-14 k-scaled | +701 (0.91) +627 / -74 | 6->6 | 54.2->54.1 | +925 (0.95) +1,194 |
| X5k d5-14 k-scaled | +1,453 (2.22) +1,389 / -65; pooled 4 tapes n64 +485 (1.09), W 45->44 | 6->5 | 54.2->54.1 | +28 (0.05) +256 |
| X3f75 / X3f50 flat | -125 (-0.15) / +372 (0.60) | 6 / 5 | 53.2 / 48.8 | +359 / +1,278 (0.73) |
| X5f75 / X5f50 flat | - | - | - | +1,137 (1.12) / +1,254 (1.06) |
CAP mode (standing strawberry tiles capped, d3-19): the cuts bind and the glut goes away, but the rival takes the price relief.
| cell | ex9 n16 dMarg (t) | own / riv | W | our d15-29 straw u @price | d23 straw over I0 | p16 n32 dMarg (t), own |
|---|---|---|---|---|---|---|
| C16 | -5,790 (-1.51) | +1,408 / +7,199 | 6->4 | 201@106 -> 118@136 | 54.2->23.4 | -7,272 (-4.17), -6,128 |
| C20 | -1,312 (-0.57) | +3,295 / +4,607 | 6->5 | 144@127 | 37.8 | -3,043 (-2.49), -3,720 |
| C24 | -166 (-0.09) | +2,059 / +2,226 | 6->5 | 166@118 | 46.8 | -1,817 (-2.09), -2,740 |
| K12 (12/18/24 by k) | +373 (0.18) | +4,302 / +3,929 | 6->5 | 133@138 | 36.7 | -1,997 (-1.25), -4,416 |
| K16 (16/20/24) | +798 (0.39) | +4,156 / +3,357 | 6->5 | 148@127 | 42.0 | -2,217 (-2.10), -2,896 |
By shop class on ex9 the cuts pay only where no strawberry shop is open by d6 (K12 k0 n5 +5,719; k2 boards: C16 -19.7k, rival +18.5k). So the k0-only caps were pooled over all four executor tapes:
| cell | pooled executor n64 dMarg (t) | own / riv | W | flips L>W / W>L | d23 straw over I0 | p16 n32 |
|---|---|---|---|---|---|---|
| Q12 (cap 12 when k=0) | -158 (-0.23) | +776 / +934 | 45->43 | 1 / 3 | 44.1->42.2 | +221 (0.17) |
| Q8 (cap 8 when k=0) | -118 (-0.11) | +1,084 / +1,203 | 45->44 | 2 / 3 | 44.1->37.4 | +1,826 (1.12), own +873 |

## Verdict: NONE
- Wool: sheep -2 on latched seats is noise (ex9 -660, p16 +213).
- Strawberry: cutting the ask does not reach the tiles. Capping the standing tiles does remove the glut (d23 +54 -> +23..+47 over I0, price 106 -> 118-138) and raises OUR purse by +1.4k to +4.3k per game. The rival, which also sells strawberry into the same book, gains as much or more: margin -5.8k to +0.8k, and W is flat or -1 to -2 in every cell. Our late oversupply is also denial. The P48LOSS1R accounting (+7.4k/game at win-class prices) held the rival's price fixed; closed loop it does not stay fixed.
- No cell meets the programme bar (margin >= +2k, t >= 2, flips >= +2). The one n16 t 2.22 read (X5k) falls to +485 t 1.09 pooled over four tapes (n64), W -1.
- Production sizing on strawberry is closed as a margin lever against the P48 class unless the rival's strawberry supply is in the rule too.

## Files
tree/ (patched copy), patch.py..patch5.py, chain.sh, launch.sh, after.sh, an.py (paired reader), byk.py (by shop class), pool.py (pooled executor), res/<cell>_<leg>_w*.csv (+_st/_sal/.sd.jsonl), logs/.
