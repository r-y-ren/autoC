# SWITCHSWEEP1R: every default-OFF plan.py switch, ON alone, on the real-tape programme panel (2026-09-30, 07:47Z to 10:50Z)

This stream runs the grid P48SWEEP1R skipped: every switch in `src/kagg3/core/plan.py` that is OFF in the shipped configuration, flipped ON alone. The shipped configuration is master b1ffcd36, which is the anchor tree 8d670dad plus `TERMINAL_DEPOSIT_VALUE_ON` and `PLAN_FASTPATH_ON` (plan.py md5 69bf445c), run with `LE.SWITCHES`.

Files:
- Remote: user@remote-host:/home/user/stage_r/switchsweep1r.
- Local mirror: `S/switchsweep1r`. It holds `srun.py`/`lrun.py`, `qworker.sh`, `ctl.py`, `tbl.py`, `t2.py`, `robust.py`, `res/` + `rres/` (rows) and `screen_tbl.md` / `stage2_tbl.md` / `robust.txt`.

## Grid
master plan.py defines 130 `*_ON` names at module level. Three more names (`CARROT_SINK_ON`, `HIRE_CLAMP_ON`, `PLANT_MIX_DRAIN_ON`) appear only in comments.
- **39 already ON.** They default True, and every value `LE.SWITCHES` sets is already True, except `CLIP_CAP_ON=False`, which is the default.
- **91 default False.** Of these, 8 were dropped before the run:

- `RESIDUAL_ON`: already ON in the shipped config (live_expert.apply_switches sets P.RESIDUAL_ON=True: the head_940 residual)
- `MACRO_EXEC_ON`: harness flag: every site is `if MACRO_EXEC_ON and MACRO_SCHEDULE is not None`, the schedule JSON comes from an env var (S/macro_exec extract) -> no-op alone
- `MELON_OPEN_ON`: invalid alone: plan.py import-time contract `not (BANK_BEFORE_LOT_ON and MELON_OPEN_ON)`, BANK_BEFORE_LOT_ON is shipped ON
- `MIDDAY_PLACE_ON`: invalid alone: contract requires MELON_OPEN_ON or MIDDAY_PLACE_V2_ON (both OFF/invalid)
- `MIDDAY_PLACE_V2_ON`: invalid alone: contract requires MIDDAY_PLACE_ON and forbids BANK_BEFORE_LOT_ON (shipped ON)
- `SAME_DAY_FERT_ON`: invalid alone: contract forbids BANK_BEFORE_LOT_ON (shipped ON)
- `MARKET_PACK_ON`: invalid alone: contract `not (EARLY_SELL_ON and MARKET_PACK_ON)`, EARLY_SELL_ON shipped ON
- `PRESTOCK_ON`: invalid alone: contract `not (EARLY_SELL_ON and PRESTOCK_ON)`, EARLY_SELL_ON shipped ON

That leaves **83 cells**. Two of them turned out not to be runnable as flipped:
- **`SPREAD_ROWS_ON`** is also contract-invalid alone. It raises a runtime `AssertionError` on every step: "spread row 17 collides with a row the day already uses [0, 2, 3, 10, 17, 18]". Our seat passes all game, and the read is -152k over 6 games. It was stopped after 6/12 games.
- **`OPP_SUPPLY_ON`** needs its curve file. On the first run it raised `FileNotFoundError` for `artifacts/opp_supply/S_pop.npy` in the stage. It was re-run with `OPP_SUPPLY_PATH=<abs>/artifacts/opp_supply/S_pop.npy` (md5 e071e7a6), and that re-run is the row in the table.

## Method
**Runner.** `srun.py` is GENETAPE1 `grun.py`, the P48SWEEP1R `run.py` plus the `GT1_REACT` v2 gate-reactive P48 wool tape. That runner is verified exact 51/51 on TUNE. The P48 wool sales are recomputed from its gate at 25 on the sim price, with the evolving stock delta taken against the tape's own rival wool stock. Additions to the runner:
- resume;
- a per-step exception count (`nerr`, which catches a switch that silently passes all game);
- our sales ledger at steps 360/432/end, and the rival's at the end;
- a game-directory search.

`lrun.py` is the same file with local paths. Remote and local are the same master `git archive`.

**Identity.** OFF equals live on every check:
- Remote non-reactive: 3/3.
- Remote reactive: 3/3.
- Local reactive: 3/3.
- 2 PQ4-only and 3 OTH-only games, non-reactive: 5/5 (ndiff 0, money to the coin).
- `ctl.py` is a pure replay of both recorded seats with no agent. It reproduces live money on 162/162 unique games, so it serves as the OFF arm's control (money and ledger).

**Stage 1 screen.** The first 24 P48TAPE103 games, reactive. They ran as pass 1 (games 1-12, every cell) and then pass 2 (games 13-24).
- Pass 2 was ordered by the pass-1 margin, and the stage-2 jobs were queued ahead of the low-priority pass-2 cells.
- **55 cells kept the 12-game read** (pass 2 was ordered by the pass-1 margin, but the cells that finished pass 1 after 09:00Z sat at the queue tail; n 16-22 = killed at the 10:40Z stop; none of these has t > 1 at n 12, but REPLANT_SAME_TURN +1,080, FILL_WORK +1,060 and PLANT_FILL_LATE +872 are positive): `REPLANT_SAME_TURN_ON`, `FILL_WORK_ON`, `PLANT_FILL_LATE_ON`, `ROUTE_VRP_OPT_ON`, `WHEAT_CYCLE_ON`, `SELL_SLOT_MIRROR_GATE_ON`, `MELONVETO_POST_ON`, `RESIDUAL_RIVAL_PURSE_ON`, `LATE_STRAW_CAP_ON`, `ANIMAL_BUY_FWD_ON`, `CLIP_CAP_STRICT_ON`, `LOT_SPLIT_ON`, `MELON_DENY_ON`, `OPEN_PUMP_TELL_KEEP0_ON`, `OPP_MIX_ON`, `ROUTE_CUT_ON`, `ROUTE_NN_ON`, `SHED_OVERFLOW_ON`, `CLIP_FERT_SKIP_ON`, `MELON_LOT_EARLY_ON`, `PRESTOCK_V2_FARMER0_ON`, `REBUY_ON`, `ROUTE_NN3_ON`, `SHED_DUMP_ROW_ON`, `STRAW_SWAP1_ON`, `SELL_SLOT_RIVALRANK_ON`, `ANIMAL_SAME_DAY_ON`, `SHED_DEFICIT_ON`, `FERT_DUMP_ON`, `DRIP_SELL_ON`, `SELL_SLOT_MIRROR_ON`, `FEED_FORWARD_ON`, `WHEAT_CYCLE_CARROT_ON`, `ASK_FILL_ON`, `EVENING_SEED_ON`, `PLANT_ASK_ON`, `RELAY_FILL_ON`, `SELL_SPREAD_ON`, `V15_DODGE_ON`, `WHEAT_CYCLE_H3_ON`, `CREW_RELAY_ON`, `FERT_FLOOR_ON`, `CLIP_CAP_ON`, `CARROT_EARLY_HOLD_ON`, `ENDGAME_TOMATO_ON`, `MIDDAY_DROP_ON`, `Q4_VRP_ON`, `Q4_PROG_ON`, `OPEN_DENY_ON`, `PROGRAM_ENGINE_ON`, `ANIMAL_DEFER_ON`, `SHEEP_FIRST_ON`, `FERT_RESERVE_ON`, `ROUTE_EARLY_ON`, `SPREAD_ROWS_ON`.

**Stage 2.** Every cell with margin > 0 and t > 1 on its 24-game screen was read on three sets:
- the full P48TAPE103, reactive;
- PQ4TAPE23 (the 23 exact games of PQ4TAPE24, non-reactive, as in pair.py);
- OTH56 (non-reactive).

18 of the 23 PQ4 games and 2 of the 56 OTH games are also in P48TAPE103. **POOLED** is the 162 unique games, using the reactive P48 row where one exists.

**Compute.** 2 remote workers (nice 19, ionice idle; launched at 1-min load 11.87 and 11.99) and 1 local worker (nice 19). Both sides ran dynamic queues (`qworker.sh`).

## Stage 1 screen: every cell (24 or 12 P48TAPE games, reactive; control = live = OFF)
Columns:
- **fired:** games with any action differing from live.
- **err:** games with exceptions.
- **react games (edits):** games where the reactive wool gate changed the tape (P48's gate is judged reactively).
- **wool hard:** the P48SWEEP1R audit count.
- **straw15-17 / anim18-29:** the arm's own mean units. Control on games 1-12 is 50.0 / 277.9.

**16 cells are byte-identical to OFF** on every game read (0 fired): `ANIMAL_BUY_FWD_ON`, `CLIP_CAP_STRICT_ON`, `LOT_SPLIT_ON`, `MELON_DENY_ON`, `OPEN_PUMP_TELL_KEEP0_ON`, `OPP_MIX_ON`, `ROUTE_CUT_ON`, `ROUTE_NN_ON`, `SHED_OVERFLOW_ON`, `CLIP_FERT_SKIP_ON`, `MELON_LOT_EARLY_ON`, `PRESTOCK_V2_FARMER0_ON`, `REBUY_ON`, `ROUTE_NN3_ON`, `SHED_DUMP_ROW_ON`, `STRAW_SWAP1_ON`.

| cell | n | fired | err | own | rival | margin | t | flips | react games (edits) | wool hard | straw15-17 | anim18-29 | p99 s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| WHEAT_VOLUME_ON | 24 | 24 | 0 | +2339 | -2468 | +4807 | 1.57 | +2 -1 | 12 (86) | 29 | 47.2 | 287.4 | 0.449 |
| HARVEST_FIRST_ON | 24 | 24 | 0 | +951 | -1178 | +2129 | 1.72 | +1 -1 | 5 (18) | 7 | 49.0 | 274.0 | 0.527 |
| HIRE_BIAS_ZERO_ON | 24 | 20 | 0 | +1275 | -844 | +2119 | 1.65 | +0 -0 | 6 (17) | 15 | 48.6 | 271.5 | 0.444 |
| ROUTE_EFF_ON | 24 | 24 | 0 | +807 | -981 | +1788 | 1.99 | +0 -1 | 6 (21) | 10 | 48.6 | 270.9 | 0.553 |
| WOOL_FIRST_ON | 24 | 24 | 0 | +2729 | +1178 | +1551 | 0.70 | +2 -1 | 21 (172) | 236 | 42.9 | 275.7 | 0.238 |
| EVE_STOCK_ON | 24 | 24 | 0 | +586 | -850 | +1436 | 1.59 | +0 -0 | 9 (26) | 13 | 48.7 | 269.5 | 0.643 |
| ROUTE_ORDER_ON | 24 | 24 | 0 | +531 | -655 | +1186 | 1.33 | +1 -0 | 4 (9) | 9 | 48.7 | 269.0 | 0.557 |
| REPLANT_SAME_TURN_ON | 12 | 12 | 0 | +292 | -789 | +1080 | 0.46 | +0 -1 | 4 (15) | 12 | 47.4 | 281.8 | 0.283 |
| H1_WORK_ON | 24 | 22 | 0 | +475 | -587 | +1062 | 1.24 | +0 -0 | 3 (4) | 3 | 49.8 | 273.2 | 0.460 |
| ROUTE_FREEFIRST_ON | 24 | 22 | 0 | +475 | -587 | +1062 | 1.24 | +0 -0 | 3 (4) | 3 | 49.8 | 273.2 | 0.472 |
| FILL_WORK_ON | 12 | 12 | 0 | -304 | -1364 | +1060 | 0.51 | +0 -1 | 2 (5) | 4 | 49.1 | 276.6 | 0.258 |
| PF_NOBUY_ON | 24 | 24 | 0 | +515 | -439 | +955 | 0.78 | +1 -1 | 8 (31) | 21 | 49.2 | 276.0 | 0.478 |
| H23_WATER_ON | 24 | 14 | 0 | +230 | -713 | +943 | 0.95 | +0 -1 | 3 (4) | 5 | 49.4 | 273.8 | 0.451 |
| MIRROR_OPEN_ON | 24 | 24 | 0 | +7349 | +6420 | +929 | 0.18 | +3 -2 | 18 (190) | 123 | 31.2 | 282.0 | 0.507 |
| PLANT_FILL_LATE_ON | 12 | 12 | 0 | -645 | -1517 | +872 | 0.41 | +0 -1 | 1 (2) | 5 | 49.1 | 281.2 | 0.274 |
| IDLE_TAIL_HOPS_ON | 24 | 24 | 0 | +473 | -375 | +848 | 1.09 | +0 -0 | 4 (14) | 6 | 49.7 | 269.2 | 0.590 |
| OPP_SUPPLY_ON | 24 | 24 | 0 | +80 | -732 | +812 | 0.62 | +0 -1 | 11 (52) | 45 | 50.0 | 274.0 | 0.269 |
| ADMIT_SLACK_ON | 24 | 16 | 0 | +150 | -658 | +808 | 0.81 | +0 -1 | 3 (4) | 8 | 49.4 | 273.3 | 0.476 |
| TILE_ALLOC_ON | 24 | 12 | 0 | +238 | -502 | +740 | 0.96 | +0 -0 | 0 (0) | 0 | 49.0 | 273.8 | 0.560 |
| FERT_VOLUME_ON | 24 | 24 | 0 | -302 | -1035 | +733 | 0.67 | +0 -1 | 5 (20) | 17 | 50.0 | 267.9 | 0.483 |
| FORWARD_ADMIT_ON | 24 | 21 | 0 | +929 | +223 | +706 | 0.72 | +0 -1 | 7 (20) | 12 | 48.5 | 265.8 | 0.508 |
| ROUTE_VRP_FIX_ON | 24 | 14 | 0 | +524 | -26 | +550 | 2.96 | +0 -0 | 1 (5) | 3 | 49.4 | 269.7 | 0.512 |
| CREW_PUSH_COST_ON | 24 | 8 | 0 | +784 | +263 | +521 | 1.41 | +0 -0 | 2 (2) | 5 | 49.3 | 269.1 | 0.238 |
| CROP_SCARCE_ON | 24 | 21 | 0 | +582 | +195 | +387 | 0.48 | +0 -1 | 6 (23) | 10 | 48.3 | 268.1 | 0.469 |
| CARE_HOLD_ON | 24 | 15 | 0 | -113 | -430 | +317 | 1.41 | +1 -0 | 4 (9) | 6 | 49.2 | 280.7 | 0.242 |
| PRESTOCK_V2_ON | 24 | 24 | 0 | +457 | +147 | +310 | 0.57 | +0 -0 | 7 (22) | 10 | 48.8 | 259.9 | 0.226 |
| PLANT_FILL_ON | 24 | 24 | 0 | -105 | -264 | +160 | 0.09 | +0 -1 | 7 (29) | 29 | 46.9 | 267.0 | 0.536 |
| MELON_VETO_FLOOD_ON | 24 | 2 | 0 | +133 | -26 | +159 | 1.34 | +0 -0 | 0 (0) | 0 | 49.3 | 270.1 | 0.448 |
| ROUTE_VRP_OPT_ON | 12 | 12 | 0 | +64 | -58 | +122 | 0.70 | +0 -0 | 0 (0) | 0 | 50.0 | 278.6 | 0.230 |
| WHEAT_CYCLE_ON | 12 | 12 | 0 | -414 | -497 | +83 | 0.12 | +0 -0 | 1 (4) | 4 | 49.8 | 276.2 | 0.241 |
| NOOP_FIX_ON | 24 | 16 | 0 | +44 | -39 | +83 | 1.37 | +0 -0 | 1 (5) | 4 | 49.3 | 270.2 | 0.469 |
| SELL_SLOT_MIRROR_GATE_ON | 12 | 12 | 0 | +67 | +2 | +65 | 0.18 | +0 -0 | 0 (0) | 1 | 50.0 | 275.4 | 0.227 |
| MELONVETO_POST_ON | 18 | 1 | 0 | +20 | -44 | +64 | 1.00 | +0 -0 | 0 (0) | 0 | 51.7 | 265.3 | 0.222 |
| RESIDUAL_RIVAL_PURSE_ON | 12 | 10 | 0 | +52 | +8 | +44 | 0.13 | +0 -0 | 0 (0) | 1 | 50.0 | 275.4 | 0.221 |
| LATE_STRAW_CAP_ON | 12 | 3 | 0 | +41 | +16 | +25 | 0.18 | +0 -0 | 0 (0) | 0 | 50.0 | 277.4 | 0.207 |
| RIVAL_TELL_ON | 24 | 15 | 0 | +4 | -4 | +8 | 1.23 | +0 -0 | 0 (0) | 0 | 49.3 | 270.2 | 0.466 |
| ANIMAL_BUY_FWD_ON | 12 | 0 | 0 | +0 | +0 | +0 | 0.00 | +0 -0 | 0 (0) | 0 | 50.0 | 277.9 | 0.224 |
| CLIP_CAP_STRICT_ON | 12 | 0 | 0 | +0 | +0 | +0 | 0.00 | +0 -0 | 0 (0) | 0 | 50.0 | 277.9 | 0.182 |
| LOT_SPLIT_ON | 12 | 0 | 0 | +0 | +0 | +0 | 0.00 | +0 -0 | 0 (0) | 0 | 50.0 | 277.9 | 0.227 |
| MELON_DENY_ON | 12 | 0 | 0 | +0 | +0 | +0 | 0.00 | +0 -0 | 0 (0) | 0 | 50.0 | 277.9 | 0.187 |
| OPEN_PUMP_TELL_KEEP0_ON | 12 | 0 | 0 | +0 | +0 | +0 | 0.00 | +0 -0 | 0 (0) | 0 | 50.0 | 277.9 | 0.173 |
| OPP_MIX_ON | 12 | 0 | 0 | +0 | +0 | +0 | 0.00 | +0 -0 | 0 (0) | 0 | 50.0 | 277.9 | 0.171 |
| ROUTE_CUT_ON | 12 | 0 | 0 | +0 | +0 | +0 | 0.00 | +0 -0 | 0 (0) | 0 | 50.0 | 277.9 | 0.220 |
| ROUTE_NN_ON | 12 | 0 | 0 | +0 | +0 | +0 | 0.00 | +0 -0 | 0 (0) | 0 | 50.0 | 277.9 | 0.258 |
| SHED_OVERFLOW_ON | 12 | 0 | 0 | +0 | +0 | +0 | 0.00 | +0 -0 | 0 (0) | 0 | 50.0 | 277.9 | 0.192 |
| CLIP_FERT_SKIP_ON | 12 | 0 | 0 | +0 | +0 | +0 | 0.00 | +0 -0 | 0 (0) | 0 | 50.0 | 277.9 | 0.470 |
| MELON_LOT_EARLY_ON | 12 | 0 | 0 | +0 | +0 | +0 | 0.00 | +0 -0 | 0 (0) | 0 | 50.0 | 277.9 | 0.512 |
| PRESTOCK_V2_FARMER0_ON | 12 | 0 | 0 | +0 | +0 | +0 | 0.00 | +0 -0 | 0 (0) | 0 | 50.0 | 277.9 | 0.452 |
| REBUY_ON | 12 | 0 | 0 | +0 | +0 | +0 | 0.00 | +0 -0 | 0 (0) | 0 | 50.0 | 277.9 | 0.460 |
| ROUTE_NN3_ON | 12 | 0 | 0 | +0 | +0 | +0 | 0.00 | +0 -0 | 0 (0) | 0 | 50.0 | 277.9 | 0.452 |
| SHED_DUMP_ROW_ON | 12 | 0 | 0 | +0 | +0 | +0 | 0.00 | +0 -0 | 0 (0) | 0 | 50.0 | 277.9 | 0.490 |
| STRAW_SWAP1_ON | 12 | 0 | 0 | +0 | +0 | +0 | 0.00 | +0 -0 | 0 (0) | 0 | 50.0 | 277.9 | 0.395 |
| SELL_SLOT_RIVALRANK_ON | 12 | 12 | 0 | -4 | +1 | -6 | -0.92 | +0 -0 | 0 (0) | 0 | 50.0 | 277.9 | 0.217 |
| ANIMAL_SAME_DAY_ON | 16 | 16 | 0 | +26 | +43 | -17 | -0.06 | +0 -0 | 1 (2) | 3 | 51.5 | 263.3 | 0.522 |
| EXPIRY_SLOT_ON | 24 | 15 | 0 | -51 | -32 | -19 | -0.15 | +0 -0 | 0 (0) | 0 | 49.3 | 269.9 | 0.560 |
| SHED_DEFICIT_ON | 12 | 3 | 0 | +43 | +63 | -20 | -0.44 | +0 -0 | 0 (0) | 2 | 50.0 | 277.6 | 0.449 |
| FERT_DUMP_ON | 12 | 11 | 0 | +74 | +102 | -29 | -0.09 | +0 -0 | 1 (3) | 6 | 50.0 | 276.8 | 0.245 |
| DRIP_SELL_ON | 12 | 12 | 0 | -502 | -415 | -88 | -0.34 | +0 -0 | 1 (10) | 5 | 50.0 | 277.4 | 0.460 |
| SELL_SLOT_MIRROR_ON | 12 | 12 | 0 | -53 | +53 | -106 | -1.01 | +0 -0 | 0 (0) | 0 | 50.0 | 277.5 | 0.487 |
| FEED_FORWARD_ON | 22 | 5 | 0 | -173 | -58 | -115 | -1.37 | +0 -0 | 0 (0) | 1 | 49.9 | 274.4 | 0.483 |
| WHEAT_CYCLE_CARROT_ON | 12 | 11 | 0 | -73 | +75 | -148 | -0.52 | +0 -0 | 1 (2) | 5 | 50.0 | 279.3 | 0.518 |
| ASK_FILL_ON | 12 | 12 | 0 | -439 | -128 | -311 | -0.18 | +0 -1 | 4 (7) | 10 | 47.8 | 267.0 | 0.264 |
| EVENING_SEED_ON | 12 | 12 | 0 | -385 | -68 | -317 | -1.37 | +0 -1 | 0 (0) | 3 | 50.0 | 276.8 | 0.399 |
| PLANT_ASK_ON | 12 | 11 | 0 | -750 | -381 | -368 | -0.20 | +0 -1 | 3 (4) | 8 | 48.3 | 279.0 | 0.594 |
| RELAY_FILL_ON | 12 | 12 | 0 | -479 | +275 | -754 | -2.41 | +0 -0 | 1 (2) | 4 | 50.0 | 275.0 | 0.235 |
| SELL_SPREAD_ON | 12 | 12 | 0 | +89 | +852 | -764 | -1.71 | +0 -1 | 0 (0) | 0 | 50.0 | 270.2 | 0.190 |
| V15_DODGE_ON | 12 | 12 | 0 | -937 | -120 | -817 | -1.78 | +0 -0 | 3 (12) | 1 | 50.0 | 280.7 | 0.260 |
| WHEAT_CYCLE_H3_ON | 12 | 12 | 0 | -2178 | -982 | -1196 | -1.00 | +0 -1 | 2 (3) | 8 | 49.3 | 291.7 | 0.306 |
| CREW_RELAY_ON | 12 | 12 | 0 | -1023 | +964 | -1986 | -3.45 | +0 -1 | 2 (2) | 6 | 50.0 | 276.8 | 0.453 |
| FERT_FLOOR_ON | 12 | 12 | 0 | -1847 | +587 | -2434 | -1.40 | +0 -0 | 1 (7) | 6 | 50.0 | 269.2 | 0.229 |
| CLIP_CAP_ON | 12 | 12 | 0 | -2340 | +1568 | -3908 | -2.44 | +0 -1 | 2 (2) | 6 | 50.0 | 262.8 | 0.181 |
| CARROT_EARLY_HOLD_ON | 12 | 12 | 0 | -1568 | +2541 | -4109 | -1.71 | +0 -2 | 6 (27) | 18 | 47.2 | 256.9 | 0.225 |
| ENDGAME_TOMATO_ON | 12 | 5 | 0 | -4949 | +316 | -5266 | -1.59 | +0 -2 | 0 (0) | 0 | 50.7 | 257.1 | 0.471 |
| MIDDAY_DROP_ON | 12 | 12 | 0 | -5232 | +308 | -5540 | -7.18 | +0 -2 | 0 (0) | 0 | 50.0 | 265.0 | 0.484 |
| Q4_VRP_ON | 12 | 12 | 0 | -7933 | -1339 | -6594 | -2.05 | +0 -2 | 2 (5) | 6 | 51.3 | 267.6 | 0.528 |
| Q4_PROG_ON | 12 | 11 | 0 | -6741 | +1460 | -8201 | -2.74 | +0 -2 | 3 (8) | 9 | 49.3 | 261.8 | 0.255 |
| OPEN_DENY_ON | 12 | 12 | 0 | +339 | +9401 | -9062 | -1.78 | +1 -3 | 8 (95) | 51 | 36.1 | 283.5 | 0.480 |
| PROGRAM_ENGINE_ON | 12 | 12 | 0 | -5104 | +5590 | -10695 | -1.87 | +2 -4 | 8 (54) | 50 | 26.8 | 294.1 | 0.756 |
| ANIMAL_DEFER_ON | 12 | 12 | 0 | -7248 | +20317 | -27564 | -10.85 | +0 -4 | 7 (49) | 49 | 34.2 | 232.9 | 0.478 |
| SHEEP_FIRST_ON | 12 | 12 | 0 | -11063 | +16808 | -27872 | -4.72 | +0 -3 | 8 (75) | 64 | 36.6 | 212.9 | 0.461 |
| FERT_RESERVE_ON | 12 | 12 | 0 | -10215 | +19291 | -29506 | -12.22 | +0 -4 | 6 (37) | 42 | 42.2 | 201.3 | 0.410 |
| ROUTE_EARLY_ON | 12 | 12 | 0 | -100671 | +44922 | -145592 | -17.26 | +0 -4 | 8 (95) | 110 | 8.6 | 0.6 | 0.162 |
| SPREAD_ROWS_ON | 6 | 6 | 6 | -107104 | +45636 | -152741 | -12.15 | +0 -3 | 5 (43) | 72 | 0.0 | 0.0 | -1.000 |

## Stage 2 (control = ctl.py replay = OFF = live)
Units columns are the arm minus control, in units per game, with the paired t.

| cell / set | n | fired | err | own | rival | margin | t | flips | react-edit games | wool hard (audit) | straw d15-17 d units | animal d18-29 d units | p99 s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HIRE_BIAS_ZERO_ON P48 | 103 | 89 | 0 | +708 | -77 | +785 | 2.21 | +1 -3 | 28 | 73 | -0.24 (t -1.07) | +0.87 (t 0.42) | 0.562 |
| HIRE_BIAS_ZERO_ON PQ4 | 23 | 21 | 0 | +83 | +682 | -598 | -1.01 | +0 -3 | 0 | 27 | -0.26 (t -0.48) | -0.39 (t -0.11) | 0.256 |
| HIRE_BIAS_ZERO_ON OTH | 56 | 52 | 0 | +345 | +137 | +208 | 0.74 | +1 -0 | 0 | 30 | -0.12 (t -0.40) | +1.86 (t 1.38) | 0.324 |
| HIRE_BIAS_ZERO_ON POOLED | 162 | 144 | 0 | +542 | -20 | +562 | 2.23 | +2 -3 | 28 | 113 | -0.12 (t -0.65) | +1.03 (t 0.73) | 0.562 |
| ROUTE_EFF_ON P48 | 103 | 103 | 0 | +378 | -283 | +661 | 2.24 | +2 -4 | 35 | 80 | -0.34 (t -1.08) | +0.32 (t 0.14) | 0.606 |
| ROUTE_EFF_ON PQ4 | 23 | 23 | 0 | +410 | -276 | +686 | 1.52 | +1 -2 | 0 | 26 | -0.17 (t -0.34) | +1.22 (t 0.26) | 0.287 |
| ROUTE_EFF_ON OTH | 56 | 56 | 0 | -296 | +140 | -437 | -0.79 | +2 -0 | 0 | 47 | -0.12 (t -0.32) | -1.14 (t -0.50) | 0.315 |
| ROUTE_EFF_ON POOLED | 162 | 162 | 0 | +144 | -170 | +314 | 1.15 | +4 -4 | 35 | 138 | -0.27 (t -1.12) | -0.49 (t -0.29) | 0.606 |
| HARVEST_FIRST_ON P48 | 103 | 103 | 0 | +509 | -200 | +709 | 2.16 | +3 -3 | 21 | 33 | -0.52 (t -2.27) | +0.18 (t 0.12) | 0.527 |
| HARVEST_FIRST_ON PQ4 | 23 | 23 | 0 | +325 | +336 | -10 | -0.02 | +0 -2 | 0 | 11 | -0.91 (t -1.83) | -2.00 (t -0.64) | 0.257 |
| HARVEST_FIRST_ON OTH | 56 | 56 | 0 | -194 | -164 | -30 | -0.14 | +1 -0 | 0 | 24 | -0.20 (t -1.40) | -0.11 (t -0.07) | 0.248 |
| HARVEST_FIRST_ON POOLED | 162 | 162 | 0 | +251 | -183 | +434 | 1.91 | +4 -3 | 21 | 64 | -0.45 (t -2.85) | +0.13 (t 0.11) | 0.527 |
| EVE_STOCK_ON P48 | 103 | 103 | 0 | +1291 | -1504 | +2796 | 1.99 | +5 -1 | 35 | 83 | -0.50 (t -1.69) | -0.44 (t -0.20) | 0.643 |
| EVE_STOCK_ON PQ4 | 23 | 23 | 0 | +7710 | -11730 | +19440 | 1.85 | +2 -0 | 0 | 32 | -0.65 (t -0.78) | -5.09 (t -0.91) | 0.268 |
| EVE_STOCK_ON OTH | 56 | 56 | 0 | +2150 | -1445 | +3596 | 1.59 | +3 -0 | 0 | 48 | -0.18 (t -0.48) | +2.29 (t 0.86) | 0.434 |
| EVE_STOCK_ON POOLED | 162 | 162 | 0 | +2422 | -2560 | +4982 | 2.77 | +10 -1 | 35 | 144 | -0.44 (t -1.90) | -0.49 (t -0.28) | 0.643 |
| ROUTE_ORDER_ON P48 | 103 | 103 | 0 | +252 | -26 | +278 | 1.08 | +3 -2 | 28 | 68 | -0.16 (t -0.76) | -0.05 (t -0.02) | 0.674 |
| ROUTE_ORDER_ON PQ4 | 23 | 23 | 0 | -169 | -654 | +484 | 0.91 | +0 -0 | 0 | 24 | -0.57 (t -1.37) | +0.26 (t 0.07) | 0.269 |
| ROUTE_ORDER_ON OTH | 56 | 56 | 0 | -292 | -6 | -286 | -0.64 | +1 -0 | 0 | 26 | -0.29 (t -1.02) | +3.16 (t 1.46) | 0.563 |
| ROUTE_ORDER_ON POOLED | 162 | 162 | 0 | +28 | -132 | +160 | 0.68 | +4 -2 | 28 | 102 | -0.25 (t -1.49) | +0.88 (t 0.58) | 0.674 |
| ROUTE_FREEFIRST_ON P48 | 103 | 91 | 0 | +216 | -113 | +329 | 1.46 | +1 -3 | 17 | 22 | -0.11 (t -0.50) | +2.03 (t 1.61) | 0.534 |
| ROUTE_FREEFIRST_ON PQ4 | 23 | 16 | 0 | -121 | +189 | -310 | -1.29 | +0 -1 | 0 | 7 | +0.00 (t 0.00) | +1.30 (t 0.52) | 0.263 |
| ROUTE_FREEFIRST_ON OTH | 56 | 48 | 0 | -106 | +78 | -184 | -0.84 | +0 -0 | 0 | 12 | -0.11 (t -1.18) | -1.59 (t -0.80) | 0.466 |
| ROUTE_FREEFIRST_ON POOLED | 162 | 140 | 0 | +103 | -24 | +128 | 0.78 | +1 -3 | 17 | 39 | -0.13 (t -0.93) | +0.88 (t 0.81) | 0.534 |
| IDLE_TAIL_HOPS_ON P48 | 103 | 103 | 0 | +64 | -72 | +136 | 0.58 | +3 -5 | 27 | 63 | -0.05 (t -0.20) | -1.42 (t -0.85) | 0.598 |
| IDLE_TAIL_HOPS_ON PQ4 | 23 | 23 | 0 | +344 | -26 | +370 | 0.76 | +1 -2 | 0 | 17 | -0.83 (t -1.44) | -1.65 (t -0.51) | 0.223 |
| IDLE_TAIL_HOPS_ON OTH | 56 | 56 | 0 | +247 | -202 | +449 | 1.82 | +1 -0 | 0 | 28 | -0.50 (t -3.06) | +3.09 (t 2.00) | 0.469 |
| IDLE_TAIL_HOPS_ON POOLED | 162 | 162 | 0 | +137 | -143 | +280 | 1.58 | +4 -5 | 27 | 102 | -0.22 (t -1.28) | +0.16 (t 0.13) | 0.598 |

## Tape-collapse check (games where the taped rival loses more than 20k against control)
HIRE_BIAS_ZERO_ON P48: collapse games 0 [] | without them n 103 own +708 margin +785 t 2.21 flips +1 -3
HIRE_BIAS_ZERO_ON PQ4: collapse games 0 [] | without them n 23 own +83 margin -598 t -1.01 flips +0 -3
HIRE_BIAS_ZERO_ON OTH: collapse games 0 [] | without them n 56 own +345 margin +208 t 0.74 flips +1 -0
HIRE_BIAS_ZERO_ON POOLED: collapse games 0 [] | without them n 162 own +542 margin +562 t 2.23 flips +2 -3
ROUTE_EFF_ON P48: collapse games 0 [] | without them n 103 own +378 margin +661 t 2.24 flips +2 -4
ROUTE_EFF_ON PQ4: collapse games 0 [] | without them n 23 own +410 margin +686 t 1.52 flips +1 -2
ROUTE_EFF_ON OTH: collapse games 0 [] | without them n 56 own -296 margin -437 t -0.79 flips +2 -0
ROUTE_EFF_ON POOLED: collapse games 0 [] | without them n 162 own +144 margin +314 t 1.15 flips +4 -4
HARVEST_FIRST_ON P48: collapse games 0 [] | without them n 103 own +509 margin +709 t 2.16 flips +3 -3
HARVEST_FIRST_ON PQ4: collapse games 0 [] | without them n 23 own +325 margin -10 t -0.02 flips +0 -2
HARVEST_FIRST_ON OTH: collapse games 0 [] | without them n 56 own -194 margin -30 t -0.14 flips +1 -0
HARVEST_FIRST_ON POOLED: collapse games 0 [] | without them n 162 own +251 margin +434 t 1.91 flips +4 -3
EVE_STOCK_ON P48: collapse games 2 ['114962331', '115271256'] | without them n 101 own +726 margin +972 t 3.14 flips +4 -1
EVE_STOCK_ON PQ4: collapse games 3 ['115271256', '115554227', '115560503'] | without them n 20 own +631 margin +553 t 1.06 flips +0 -0
EVE_STOCK_ON OTH: collapse games 1 ['115293787'] | without them n 55 own +1121 margin +1437 t 2.13 flips +2 -0
EVE_STOCK_ON POOLED: collapse games 5 ['114962331', '115271256', '115293787', '115554227', '115560503'] | without them n 157 own +864 margin +1144 t 3.71 flips +6 -1
ROUTE_ORDER_ON P48: collapse games 0 [] | without them n 103 own +252 margin +278 t 1.08 flips +3 -2
ROUTE_ORDER_ON PQ4: collapse games 0 [] | without them n 23 own -169 margin +484 t 0.91 flips +0 -0
ROUTE_ORDER_ON OTH: collapse games 0 [] | without them n 56 own -292 margin -286 t -0.64 flips +1 -0
ROUTE_ORDER_ON POOLED: collapse games 0 [] | without them n 162 own +28 margin +160 t 0.68 flips +4 -2
ROUTE_FREEFIRST_ON P48: collapse games 0 [] | without them n 103 own +216 margin +329 t 1.46 flips +1 -3
ROUTE_FREEFIRST_ON PQ4: collapse games 0 [] | without them n 23 own -121 margin -310 t -1.29 flips +0 -1
ROUTE_FREEFIRST_ON OTH: collapse games 0 [] | without them n 56 own -106 margin -184 t -0.84 flips +0 -0
ROUTE_FREEFIRST_ON POOLED: collapse games 0 [] | without them n 162 own +103 margin +128 t 0.78 flips +1 -3
IDLE_TAIL_HOPS_ON P48: collapse games 0 [] | without them n 103 own +64 margin +136 t 0.58 flips +3 -5
IDLE_TAIL_HOPS_ON PQ4: collapse games 0 [] | without them n 23 own +344 margin +370 t 0.76 flips +1 -2
IDLE_TAIL_HOPS_ON OTH: collapse games 0 [] | without them n 56 own +247 margin +449 t 1.82 flips +1 -0
IDLE_TAIL_HOPS_ON POOLED: collapse games 0 [] | without them n 162 own +137 margin +280 t 1.58 flips +4 -5

**EVE_STOCK_ON's five collapse games.** In these games the fixed rival tape breaks. The rival loses 70k to 107k, and its end revenue falls to about 45-54k against a normal 110-170k. Our seat gains 26k to 75k in the same games. This is the classic tape-denial artefact: EVE_STOCK buys tomorrow's feed wheat and fertilizer at turn 20, and a scripted rival whose recorded buys then fail does not re-plan.

**Without those games, EVE_STOCK still reads:**
- P48 +972, t 3.14, flips +4 -1.
- PQ4 +553, t 1.06, flips 0/0.
- OTH +1,437, t 2.13, flips +2 -0.
- Pooled +1,144, t 3.71, flips +6 -1, own +864.

No other stage-2 cell has a collapse game.

**EVE_STOCK ledger** (pooled, collapse games excluded, n 157):
- Strawberry d15-17: -0.45 u/game (t -1.95) against control 44.1.
- Animal d18-29: -0.22 u/game (t -0.13) against control 260.0.
- End-of-game sold units per game: wheat +18.8, fertilizer +2.4, strawberry +1.5, milk +1.4, egg -1.4.
- Spend +585, revenue +1,449.

## Verdict
**CANDIDATE, conditional: `EVE_STOCK_ON=True` (the only cell that clears the money and flip bars).**

| bar | EVE_STOCK_ON read | pass |
|---|---|---|
| pooled paired margin t >= 2 | +4,982, t 2.77 (n 162); without the 5 tape-collapse games +1,144, t 3.71 | yes |
| own >= 0 on every set | P48 +1,291 / PQ4 +7,710 / OTH +2,150 (without collapses +726 / +631 / +1,121) | yes |
| no set with a negative margin | +2,796 / +19,440 / +3,596 (without collapses +972 / +553 / +1,437) | yes |
| net flips >= +3 | +10 -1 (without collapses +6 -1) | yes |
| wool gate | P48 judged reactively (35 games with gate edits); PQ4/OTH non-reactive (audit hard 32 / 48) | yes on P48 |
| d15-17 strawberry, d18-29 animal units not below control | straw -0.44 u/game (t -1.90), animal -0.49 (t -0.28); without collapses -0.45 (t -1.95) / -0.22 (t -0.13) | **no, marginally** |

- **By the letter of the units clause this is NONE.** It is flagged for the V56 confirmation as the one near-candidate.
- **Most of the raw margin is tape denial.** Five collapse games carry +3.8k of the +5.0k pooled mean.
- **The robust read is still positive and significant on P48 and OTH.**
- **Runtime:** apply p99 0.64 s against the 0.65 s bar (runner timing under load).
- **Code note:** the plan.py comment block records the product half of this switch as measured -33 on ENG22. The P48/OTH programme panel is a different class.

**NONE, with numbers (stage 2, pooled over 162 games):**
- `HIRE_BIAS_ZERO_ON`: +562, t 2.23, flips +2 -3 (PQ4 -598).
- `HARVEST_FIRST_ON`: +434, t 1.91, flips +4 -3. Strawberry d15-17 is -0.45 (t -2.85).
- `IDLE_TAIL_HOPS_ON`: +280, t 1.58, flips +4 -5.
- `ROUTE_EFF_ON`: +314, t 1.15, flips +4 -4 (OTH -437).
- `ROUTE_FREEFIRST_ON`: +128, t 0.78, flips +1 -3.
- `ROUTE_ORDER_ON`: +160, t 0.68, flips +4 -2.

The routing/labour family (these six plus `H1_WORK_ON`, which is identical to FREEFIRST) all read about +1-2k on the 24-game screen and regress to +130..+560 at n 162.

**Screen qualifiers not read in stage 2** (their 24th game landed at 10:34-10:44Z):
- `WHEAT_VOLUME_ON` +4,807, t 1.57 (own +2,339, flips +2 -1). This is the most interesting unread cell.
- `ROUTE_VRP_FIX_ON` +550, t 2.96 (0/0 flips).
- `CREW_PUSH_COST_ON` +521, t 1.41.
- `CARE_HOLD_ON` +317, t 1.41.
- `MELON_VETO_FLOOD_ON` +159, t 1.34.
- `NOOP_FIX_ON` +83, t 1.37.
- `RIVAL_TELL_ON` +8, t 1.23.

**Every other cell** is at or below 0 margin or t <= 1 on the screen, or is byte-identical. The table above has the numbers.

The top cells, with the tree path and switch strings, are in `S/switchsweep1r/TOP.txt` for STACK1.

## Slips
- 08:00Z slip 1: first local launch used relative EPS/OUT paths (runner chdirs to S/vband1): created empty S/vband1/res/loc_offr_id3.jsonl, removed; worker killed (own PIDs 1465080/1465340/1465344) after 1 min, 0 rows
- 08:59Z slip 2: used bash process substitution <(head ...) for a 2-game ctl.py test (reads /dev/fd); replaced by files
- 09:13Z slip 3: again bash process substitution <(...) in a comm call (local, read-only listing); no further use
- 09:34Z slip 4: a leftover '> /dev/null 2>&1' on a no-op head command (local); no data written
- 10:18Z-10:40Z ordering miss: `WHEAT_VOLUME_ON` / `WOOL_FIRST_ON` finished pass 1 after the pass-2 reorder and sat at the queue tail. Their 24-game reads were run late (10:42Z), with no stage 2 for `WHEAT_VOLUME_ON`.
- The queue workers' STOP check is string >, so 3 low-priority jobs started at 10:40Z. They were killed at 10:41Z (own PIDs), and partial rows (n 16-22) are shown as such.
