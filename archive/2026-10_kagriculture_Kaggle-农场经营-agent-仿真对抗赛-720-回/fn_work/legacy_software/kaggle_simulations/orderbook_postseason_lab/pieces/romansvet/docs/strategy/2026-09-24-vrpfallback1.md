# VRPFALLBACK1 (2026-09-24, 15:06-16:20Z): recover the VRP days VERIFY throws back

Branch `vrpfallback1` (off master 3dcf0d62), worktree `/mnt/e/_work/kagg3_wt_vrpfallback1`. Switch (plan.py, default OFF):
`ROUTE_VRP_NEEDS_FIX_ON` (+ `ROUTE_VRP_NEEDS_TRIM`=True sub-switch). Code `src/kagg3/agent/route_vrp.py` (`build`: harvested
wheat as `give`; `_short_items` / `_trim_sells` after the write-back). VERIFY unchanged. Tests `tests/test_route_vrp.py`
(+2, data `tests/data/route_vrp_needs_d28.pkl`). Tools `S/vrpfallback1/` (ledger.py, timing.py, parity.py, dbgday.py,
llane.sh, rlane.sh, eng.sh, tape.sh; outputs `out/`).

## 0. Baseline finding
`S/ship_vrp2/v2dev100.tsv` is **not** the shipped config: it is `RESIDUAL_RIVAL_PURSE_ON=True` (SALEPIN1's `sim.sh` dev leg
adds it; the shipped tarball res940_vrp2 has it False). My RRP=True rerun of dev boards 0-19 = v2dev100 20/20 byte-exact;
my shipped-default rerun (no extra switches, KAGG3_SIM_SALES=1, 1 V56 worker) = v2dev100 on only 19/100 boards
(85-15 vs 86-14). `devvrp100_salepin.tsv` / routeopt2 `dev_base.tsv` are the older VRP30 arm (0-3/100 identical). The
fresh shipped base = ROUTEOPT2 `Lvb_0.tsv` 96/100 byte-exact (4 boards ±230 own: the 0.7 s safety break under load).
RR_ITERS is 30 in all of them. Every gate below uses MY fresh base (same box, same time as the arm).

## 1. Ledger of the fallback days (dev boards 0-19, 600 dawns recorded on the shipped trajectory)
| cause | days (20 games) | days/game | hire saving foregone/game |
|---|---|---|---|
| wheat PICKUP short: the planner FEEDs from wheat its own same-day HARVEST stops carry and picks its shed wheat at h1 BEFORE its own h1 SELL row sells the rest; the VRP counts every FEED as a shed pickup (`_needs` has no harvest give) and places the pickups at h2-h4, after the row -> 1-2 units short | 52 | 2.60 | 321 |
| same + an animal pickup short the planner also has | 2 | 0.10 | 23 |
| PICKUP off an access tile + (tile, op) moved (spawn / frozen-hand mismatch) | 7 | 0.35 | 20 |
| (tile, op) moved only | 1 | 0.05 | 2 |
| **total** | **62** | **3.10** | **366** |
The brief's second hypothesis (pickup before the h1 BUY row lands) did not occur on its own: `avail` already = buy hour + 1.
The real timing issue is the h1 SELL row (units act before market rows): the shed holds the planner's pickups only
until h1. Worked example (dev board 17 d28, test data): shed wheat 30, planner picks 3x2 at h1, the h1 row sells 24, hand 5
feeds at h21 from wheat it harvested at h9/h12; VRP picks 1+2 at h1, 2 at h2, 2 at h3 -> short 1 -> fallback.

## 2. Fix (`ROUTE_VRP_NEEDS_FIX_ON`)
(a) a planner HARVEST op on a ripe wheat tile gives its dawn `yield_units` of WHEAT to the route (like COLLECT_FERTILIZER's
fertilizer), so a route that harvests then FEEDs no longer picks that wheat up; (c) after the write-back, replay the
new table in engine order; where a product's PICKUP shortfall exceeds the planner's, sell that many fewer in the latest
SELL row of it before the short pickup (1.5 units/game), or, with no sale to trim, add them to its BUY_PRODUCT row
(0.25 units/game; `BUY_TOPUP`). (b) not needed (see ledger). OFF parity: 600/600 recorded dawns byte-identical output vs
master 3dcf0d62 src (safety break off); sim dev boards 0-2 byte-exact vs ROUTEOPT2 Lvb_0.

Offline (same 600 dawns, per game):
| variant | fallback days | hires dropped | hire bill saved | Δ bill |
|---|---|---|---|---|
| base (FIX_FROZEN+VERIFY, shipped) | 3.10 | 25.25 | 2,288 | - |
| (a) harvest give only (`NEEDS_TRIM=False`) | 2.00 | 26.20 | 2,350 | +62 |
| (a)+(c) no buy top-up | 0.65 | 27.90 | 2,536 | +248 |
| **(a)+(c) NEEDS_FIX** | **0.40** | **28.20** | **2,597** | **+308** |
| NEEDS_FIX on ROUTEOPT2's recording (rec_dev20b; its base 3.20 / 2,386) | 0.15 | 30.65 | 2,755 | +369 |
Left: 0.40/game spawn/off-access days (foregone 7/game).

Timing (600 dawns, apply() per dawn, base and fix interleaved in one process): remote i3-10300 (load 2.5, EGGDOSE gone,
my 2 FRESH lanes on other cores) base median 0.049 / p99 0.247 / max 0.356 s, **fix 0.051 / 0.230 / 0.256 s**;
`_trim_sells` <= 1 ms. Worst dawn fix 0.256 + planner ~0.14 = 0.40 s <= 0.5 s. (Local loaded box: base max 0.530, fix 0.452.)

## 3. Gates (arm `ROUTE_VRP_NEEDS_FIX_ON=True` vs fresh shipped base; same box, same time)
| variant | leg | W-L base -> arm | flips | Δours (t) | Δtheirs (t) | Δmargin (t) |
|---|---|---|---|---|---|---|
| **NEEDS_FIX** | V56 dev100 (local) | 86-14 -> 87-13 | +2/-1 = **+1** | +273 (4.40) | -31 (-0.68) | +304 (4.10) |
| **NEEDS_FIX** | FRESH300 (remote) | 243-57 -> 250-50 | +10/-3 = **+7** | +226 (5.57) | +10 (0.43) | +216 (**4.19**) |
| **NEEDS_FIX** | V56 held-out100 (local, boards 150-249) | 86-14 -> 89-11 | +4/-1 = **+3** | +279 (4.85) | -14 (-0.24) | +292 (3.76) |
| **NEEDS_FIX** | band tapes dev50 (100 seat-games, local; base = ROUTEOPT2 vb csv) | 86-14 -> 86-14 | +0/-0 = 0 | +283 (5.91) | +84 (1.91) | +199 (3.08) |
| **NEEDS_FIX** | ENGINE faithful-59 (remote; base eng_vrp2 = ROUTEOPT2 vb59 byte-exact) | 15-44 -> 14-45 | +0/-1 = **-1** | +411 (3.25) | +116 (1.30) | +296 (2.71) |
| give only | V56 dev100 | 86-14 -> 86-14 | +1/-1 = 0 | +122 (2.11) | -23 (-0.51) | +146 (1.97) |
| give only | band tapes dev50 | 86-14 -> 86-14 | 0 | +130 (2.67) | +87 (2.08) | +43 (0.71) |
| give only | faithful-59 | 15-44 -> 14-45 | +0/-1 = -1 | +167 (1.51) | +4 (0.05) | +163 (1.37) |
FRESH base = ROUTEOPT2 fr_vb 300/300 identical W-L (own -2). The faithful flip is one knife-edge board, the same in both
variants: ep 111903332 +519 -> -25 (ours +579, theirs +1,123; give-only -86 with the identical theirs 127,398), i.e. the
harvest-give part moves a route and the replayed rival's price lands +1.1k; 5 of the 15 base wins are within +1,000.
Tapes Δtheirs +84 is the same with give only (+87), so it is not the trimmed sale.

## 4. Verdict
Real own-purse gain on every leg (+226..+411, t 3.3-5.9, = the offline +308 bill), wins dev +1 / held-out +3 / FRESH300 +7
(margin t 4.19) / tapes 0, **but faithful-59 -1** (one board at +519 margin, theirs +1.1k price) -> fails the letter of
the bar (faithful >= 0). Candidate switch string if the caller accepts the knife-edge faithful flip:
`ROUTE_VRP_NEEDS_FIX_ON=True` (NEEDS_TRIM default True). Give-only is dominated (dev 0, faithful -1, half the own gain).
Tarball not built. Left: the 0.35/game spawn/off-access fallback days; the faithful board 111903332 divergence (engine
day-level diff not run).

## 5. Remote state
`user@remote-host`: `~/stage_vrpfallback1` (copy of stage_routeopt2 + this branch's src; FRESH csvs
`S/vrpfallback1/out/{base,fix}_F0.tsv`, mirrored locally) and `~/stage_vrpfallback1e` (copy of stage_routeopt2e + src;
`S/routeopt1/eng_vf_{fix,give}.csv`, rec_base_0.pkl + timing_r.py). No process of this job running at hand-back.

## 6. Ship (SHIP_VRP3, 2026-09-24T17:20Z) — packaged res940_vrp3, awaiting user upload
**Tie-breaker** (second ENGINE-class read): DSMGAP2 seat swap, ENGINE-held 40 boards (vrp2 held set + class; list
`S/ship_vrp3/eng40.txt`), our agent in DSM's seat vs its recorded opponent tape, remote. Pairer `S/ship_vrp3/pair.py`.
The remote box went from load 0.4 to ~24 mid-run (foreign ESV57/RLV57/POOLCHECK1), so the 0.7 s safety break made the
default-code reads load-dependent (base rerun vs recorded vrp2: 13/40 identical, own -368 t -4.1). The decisive read
is therefore the load-free one: both arms with SAFETY_S = BUDGET = 1000 s (`src_nb`, stage only; RR_ITERS 30 as shipped),
whose base reproduces the recorded vrp2 on 36/40 boards (8-32, Δmargin +41).

| read | n | W-L base -> NEEDS_FIX | flips | Δours (t) | Δtheirs (t) | Δmargin (t) |
|---|---|---|---|---|---|---|
| **load-free, both arms same time** (`arm_OURS_nb{base,fix}.tsv`) | 40 | **8-32 -> 8-32** | +0/-0 | +379 (2.94) | +72 (0.85) | **+307 (1.81)** |
| default code, fix vs recorded vrp2 (`arm_OURS.tsv`) | 40 | 8-32 -> 8-32 | +0/-0 | +45 (0.31) | +78 (0.93) | -33 (-0.21) |
| default code, fix vs base rerun (base under load 24) | 40 | 7-33 -> 8-32 | +1/-0 | +413 (2.67) | +133 (1.85) | +280 (1.62) |
| same, all 131 swap boards | 131 | 86-45 -> 88-43 | +2/-0 | +392 (5.18) | +70 (2.38) | +322 (4.09) |
Bar (wins >= 8, Δmargin >= 0): **PASS** on the load-free read (8, +307); the only negative row pairs a partly loaded arm
with an unloaded recorded base.

- `d6c64188`: `ROUTE_VRP_NEEDS_FIX_ON = True` (NEEDS_TRIM True); 4 switch strings gained `,ROUTE_VRP_NEEDS_FIX_ON=True`;
  switch-off arms kept (d28 test OFF arm, SALEPIN1 frozen-d17, ROUTEOPT2 opt fixture, ROUTEFILL1 digest pin NEEDS_FIX off).
  `pytest tests/test_route_vrp.py tests/test_route_vrp_opt.py tests/test_route_fill.py tests/_pin.py` pass.
- Archive `/mnt/e/_work/kaggriculture3/dist/submission_res940_vrp3.tar.gz`: md5 `c3eac8dccfc8495f8fa46989f1ed9d4c`,
  506,262 bytes, 30 files (same file set as vrp2); diffs vs vrp2: route_vrp.py (VRPFALLBACK1 + ROUTEOPT2 OFF code),
  plan.py (NEEDS_FIX True; ROUTEOPT2 / EGGDOSE1 switches all OFF).
- Tarball smoke (`S/ship_vrp/drive.py`, real engine, packaged main.py; local box load ~24; tape with town_live302):

| board | ours/theirs tarball | gate csv | worst turn s | mean dawn s |
|---|---|---|---|---|
| FRESH 0 vs V56 (seat 1) | 119,691 / 114,588 | out/fix_F0 same | 0.697 | 0.332 |
| FRESH 1 vs V56 (seat 1) | 80,251 / 76,170 | out/fix_F0 same | 0.570 | 0.328 |
| FRESH 2 vs V56 (seat 1) | 70,750 / 65,390 | out/fix_F0 same | 0.557 | 0.334 |
| tape 111257750 seat 0 | 85,852 / 75,305 | vrpfallback1_tape_fix_band3 same | 0.570 | 0.394 |
| tape 111257750 seat 1 | 85,793 / 75,394 | vrpfallback1_tape_fix_band3 same | 0.639 | 0.383 |
  5/5 byte-exact, 0 non-ACTIVE/DONE statuses, worst turn 0.70 s < 1.0 (loaded box; vrp2 smoke on a quieter box 0.45).
- Pin `tests/_pin.py` SHIPPED 0769ad8a -> d6c64188.
