# WHEATCYCLE1: DSM's fertilize-at-2 / harvest-at-3 grain cycle, ported and gated (2026-09-23)

Branch `wheatcycle1` (from master 0d97fa1a). Flags in `src/kagg3/core/plan.py` (all default OFF, OFF 3-board byte parity in
`tests/test_wheat_cycle.py`): `WHEAT_CYCLE_ON` (fert wheat at age >= 2), `WHEAT_CYCLE_CARROT_ON` (same for carrot),
`WHEAT_CYCLE_H3_ON` (harvest fertilized wheat at age 3) with sub-knob `WHEAT_CYCLE_RP_ON` (default True: replant the freed tile on the same stop).
Harness `S/wheatcycle1/`: `v56.sh`/`v56.py` (reacting V56, actTimeout 600, two-seat ledger), `measure.py`, `table.py`, `pair.py`,
`tpair.py`, `tape.sh`, `eng.py` + `faithful59.txt`; results `led_*` (per-game ledgers), `table_*.tsv`, `eng_*.csv`, `logs/`.

## 1. Engine rule (sim == engine; `src/kagg3/sim/units.py`, `src/kagg3/spec.py`)
- PLANT sets a one-shot crop's yield to 1 (`units.py:152`). WATER inside the window `[(maxday+1)//2, maxday]` adds +1, or +2 while
  `fertilized_until_day >= day` (`units.py:113-115`). FERTILIZE sets `fertilized_until = max(old, day + 2)`, i.e. it covers
  today, +1, +2 (`units.py:159-160`). HARVEST needs `age >= first_yield_day` and yield > 0 (`units.py:116`). Only the waterings
  matter; fertilizer has no effect on growth by itself (`eod.py:97` only touches ongoing crops).
- WHEAT (`spec.py:43`: first 2, maxday 4, max 6) has window ages 2-4. Unfertilized: 1+1+1+1 = **4 u at age 4** (3 at age 3).
  Fertilized at age 1 (covers ages 1-3) or at age 2 (covers 2-4): **6 u at age 4** either way, **5 u at age 3** either way (1+2+2).
  Fert at age 2 applied AFTER the age-2 water gives only 4 at age 3.
- CARROT (`spec.py:44`: first 2, maxday 3, max 4), window ages 2-3: 3 u unfertilized, 4 u fertilized (age 1 or 2), harvest age 3.
- So DSM's "fert at age 2" buys **no yield** over our age-1 application: it only moves the FERTILIZE onto the age-2 water stop (no
  separate age-1 trip). The yield trade of "harvest at 3" is 5 u in 3 days (1.67 u/tile-day) vs 6 u in 4 days (1.5), and it
  pays only if the freed tile is replanted at once.
- Our planner: harvest age = `clip(pay_day - t_day, first, CROP_SATURATE_AGE)` (`plan.py:9795`), sat age wheat 4 / carrot 3
  (`spec.py:73`), so we already harvest carrot at 3; fert candidates `fert_cand` (`plan.py:10075`) value age 1 and age 2 equally
  (`valuation.py:127`, +2 wheat u), so age 1 wins by being first.

## 2. Measurement (reacting V56 dev 0-99, per game d10-29; `S/wheatcycle1/table_dev.tsv`; ours | theirs unchanged within 1 %)
| arm | n | wheat plant | wheat harv (age3) | wheat u harvested | wheat sold / rev | carrot harv / u | fert wheat a1/a2 | fert carrot | fert sold | dead | hires | PASS | replant |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| OFF | 100 | 69 | 78 (5) | 427 | 212 / 8,137 | 30 / 116 | 59 / 6 | 29 | 162 | 0 | 210 | 451 | 68 |
| W (fert@2 wheat) | 100 | 69 | 78 (4) | 421 | 216 / 8,278 | 30 / 115 | 0 / 60 | 30 | 166 | 0 | 209 | 432 | 68 |
| C (fert@2 carrot) | 100 | 69 | 78 (5) | 426 | 215 / 8,264 | 30 / 113 | 58 / 6 | 27 | 164 | 0 | 209 | 441 | 68 |
| WC | 100 | 69 | 77 (4) | 420 | 215 / 8,253 | 29 / 112 | 0 / 60 | 27 | 167 | 0 | 208 | 430 | 68 |
| W+H3 (+replant) | 32 | 94 | 103 (83) | 495 | 272 / 10,114 | 28 / 108 | 0 / 84 | 27 | 164 | 0 | 210 | 430 | 96 |
| W+H3 no replant (diag) | 24 | 79 | 88 (67) | 417 | 217 / 8,330 | 27 / 104 | 0 / 69 | 27 | 173 | 0 | 204 | 420 | 80 |
DSM for scale (DSMLOGIC1): 135 wheat harvests, 175 replants per game. Theirs (V56) 122 wheat harvests, unchanged in every arm.
- fert@2 (W/WC) does what it should: all 59 age-1 applications move to age 2, wheat units -1 %, **PASS -19..-21 hand-turns/game**,
  hires -1..-3; that crew time is the whole effect (+54..+139 coins).
- H3 is mechanically faithful (83 age-3 harvests, replants 68 -> 96, wheat revenue +1.2k/game paired) but the relay takes the
  tiles and seed of the day's other crops: paired W+H3 vs OFF (n 32) tomato -1,265, melon -1,213, strawberry -700, carrot -289,
  fert -362 against wheat +1,212 -> **ours -1,738**. Without the replant the freed tile sits empty (+40 empty tile-days d20-28)
  and wheat units FALL (5 u instead of 6 per harvest): ours -814.

## 3. Gates (paired ON vs fresh OFF from this tree, JAX_PLATFORMS=cpu, WORKERS 3-4, actTimeout 600)
| leg | arm | W-L OFF -> ON | flips = net | d_ours (t) | d_theirs (t) |
|---|---|---|---|---|---|
| V56 dev 0-99 | W | 69-31 -> 73-27 | +6/-2 = **+4** | -5 (-0.07) | -85 (-1.14) |
| V56 dev 0-99 | C | 69-31 -> 73-27 | +5/-1 = **+4** | +139 (3.16) | -65 (-0.75) |
| V56 dev 0-99 | WC | 69-31 -> 73-27 | +5/-1 = **+4** | +54 (0.69) | -146 (-2.03) |
| V56 dev (n 32-33, stopped) | W+H3 | 24-8 -> 18-14 | +0/-6 = **-6** | -1,738 (-4.24) | +525 (1.39) |
| V56 dev (n 33, stopped) | C+H3 | 25-8 -> 19-14 | +0/-6 = **-6** | -1,604 (-4.11) | +853 (2.01) |
| V56 dev (n 32, stopped) | WC+H3 | 24-8 -> 17-15 | +0/-7 = **-7** | -1,710 (-4.10) | +612 (1.47) |
| V56 dev (n 24, diag) | W/C/WC+H3 no replant | 16-8 -> 15-9 | +1/-2 = -1 each | -814 / -741 / -736 (t -2.5..-2.7) | +280 / +174 / +136 |
| V56 held-out 150-249 | WC | 72-28 -> 71-29 | +2/-3 = **-1** | +201 (2.86) | -115 (-1.46) |
| V56 held-out (n 48, stopped) | C | 32-16 -> 32-16 | +1/-1 = 0 | +148 (2.04) | -60 (-1.07) |
| band tapes dev50 (100 seat-games) | WC | 76-24 -> 78-22 | +4/-2 = **+2** | +203 (2.58) | -54 (-1.02) |
| ENGINE faithful-59 | WC | 9-50 -> 8-51 | +0/-1 = **-1** | +153 (1.18) | -127 (-0.72) |
| ENGINE faithful-59 | C | 9-50 -> 8-51 | +0/-1 = **-1** | -260 (-3.29) | -7 (-0.13) |
| v15stack dev 0-49 | WC | 35-15 -> 35-15 | 0 | +100 (1.03) | -59 (-0.93) |
H3 cells were stopped at n 32-33 once t < -4 (and the replant-less variant at n 24); `led_dev_*norp` / `led_dev_w3ng`
(first H3 without the dawn-yield guard, n 8: -1,340) are kept as diagnostics. Tape leg: the first OFF run (box load 50) broke
19 games (`tape_off_corrupt.csv`, ours < 20k); the rerun `tape_off.csv` is byte-identical to `relayfill1_tape_off` and is the one used.

## 4. Verdict: NO SHIP; H3 (harvest@3 + relay) CLOSED on our planner, fert@2 parked
- Harvest-at-3 loses in every cell (-1.6..-1.7k, net -6/-7, gift +0.5..0.9k): our day plan has no spare tiles/seed/turns for a
  3-day wheat relay, so the relay displaces tomato/melon/strawberry. DSM's 135 harvests come with its whole crew programme
  (filler jobs, JIT seed, 16-hand d10); the rule does not port alone.
- fert@2 is gift-free and saves ~20 PASS hand-turns/game, but it is a +50..+200 coin effect: WC dev +4 -> held-out -1 (ours +201
  t 2.86), tapes +2 (ours +203 t 2.58), ENGINE -1, v15stack 0; C fails ENGINE (ours -260 t -3.3). Fails the bar on held-out
  net (-1) and faithful-59 net (-1); every leg is gift-free (d_theirs <= 0).
- If revisited: WC as a small-gain candidate needs held-out ours t >= 3 on more boards; do not spend more on H3 without a planner that
  budgets the relay's tiles/seed ahead of the day's ask.
