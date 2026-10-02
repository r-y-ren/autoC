# SEED SCREEN: the macro-fitted seeds, played paired against B in the CRN sim

**VERDICT: all three lose, and the reason kills the premise. B ALREADY hires 4 hands on day 0,
1 on day 1, 5.5 on day 5 and 8.4 on day 10 — 261 hires a season against ymg_aq's 278 — so the
"they hire 4 on d0, B asks for 0" gap of `2026-09-14-macro-extract.md` §2 is a comparison of THEIR
landed hires against OUR decoded ask, and the ask is not what hires. Lifting the ask to 3/1/3.7/10
(CREW, 99 coordinates, crops byte-identical to B) moves landed hires by −3 a season and costs
−738 coins (t −1.11, 5/12) on the ymg_aq boards and −3,805 (t −6.94, 7/68) on the band. Refitting
the herd split on top (CREWHERD) trades cows for sheep: WOOL +2,635/+1,790, MILK −4,992/−7,281,
net −8,420 (t −5.38) and −8,347 (t −12.21). The FULL macro seed is a catastrophe — −80,122
(t −14.50) and −82,954 (t −36.58), 0/80 wins — and it fails exactly the way the FORWARD_ADMIT
postmortem said it would: it reaches ymg_aq's wheat board (19.2 tiles at d10 vs their 16.5) with
20.2 idle tiles, 143 hires a season instead of 261, and the strawberry and milk lines gone
(−26,939 / −19,800). NO ES arm from any of the three.**

Diagnostic only; per the two-purse rule nothing here is promotion evidence. No engine game.
Tools (new, all under `S/seed_screen/`, originals untouched): `fit_masked.py` (block-masked copy of
`S/macro_extract/fit.py`), `decode.py` (80-dawn harness, `S/wheat_slope/slope.py` recipe),
`decode_real.py` (180 real ymg_aq dawns), `ledger_seeds.py` (copy of `ledger_multi.py`, multi-seed
instead of multi-`z`), `ledger_hires.py` (same + a per-seat HIRE counter in the patched
`_market_turn`), `report_seeds.py` (copy of `S/wheat_slope/report.py`). Switches on every run:
`OPEN_PUMP_ON,TAIL_FILL_ON,BANK_BEFORE_LOT_ON,HIRE_ROW_ON` + `brain.MELON_GENE_ON=True`,
`shop_crn=True`, pinned towns, tape opponent, repo `src` (7,020 layout).

## 1. The three thetas

| theta | what was refitted | blocks | coords moved | md5 |
|---|---|---|---|---|
| **FULL** | the whole 7,020 (as fitted 2026-09-14) | all | 7,020 | `3b6040a6a7a3034c9a8643062b7aae59` |
| **CREW** | crew-ramp readout only, loss = crew | `g10`,`gb10` | **99** | `504b30a2d8d81b4435dc5431effcf12b` |
| **CREWHERD** | + herd-mix readout, loss = crew + animals | `g10`,`gb10`,`g8`,`gb8` | **198** | `4d3a57908f0c167c578b50fb9cd19577` |

`fit_masked.py` asserts every coordinate outside the mask is byte-identical to B, so CREW and
CREWHERD carry **B's crop programme exactly**. 1,500 Adam steps, lr 0.01, same 180 dawns; masked
crew MSE 8.64 → 0.37 (FULL reaches 0.0015 because it may also move the encoder), animal MSE
0.603 → 0.377 (the herd *count* `sig(head[6])*n_dev` is frozen at B, so only the split moves).

### The ask, 80 synthetic dawns (nquad 1-4 x money {3k,8k,20k,60k} x day)
| theta | d0 | d1 | d5 | d10 | crew_target / animal_want G/C/S / plant_target W/C/T/S/M |
|---|---|---|---|---|---|
| B | 0.00 | 0.00 | 2.25 | 8.12 | d10: 0.12/6.19/4.94 — 2.00/1.25/0/10.06/2.88 |
| FULL | 2.31 | 2.75 | 5.94 | 8.00 | d10: 0.00/19.81/11.56 — **19.06/0/0.12/2.00/0.88** |
| CREW | 1.00 | 1.38 | 2.38 | 3.56 | d10: 0.12/6.19/4.94 — 2.00/1.25/0/10.06/2.88 (= B) |
| CREWHERD | 1.00 | 1.38 | 2.38 | 3.56 | d10: **0.38/3.94/6.94** — 2.00/1.25/0/10.06/2.88 (= B) |

### The same ask on the 180 REAL ymg_aq dawns (quantised `brain.decide`, gene ON)

| theta | crew d0 | d1 | d5 | d10 | animal_want/day G/C/S | crew MAE vs ymg_aq |
|---|---:|---:|---:|---:|---|---:|
| ymg_aq REPLAY | 4.00 | 1.00 | 4.00 | 10.67 | 0.03/0.26/0.22 | 0 |
| B | 0.00 | 0.00 | 0.00 | 10.50 | 0.19/0.18/0.23 | 2.19 |
| FULL | 3.00 | 0.50 | 3.00 | 10.17 | 0.00/0.17/0.10 | **0.54** |
| CREW | 3.00 | 1.00 | 3.67 | 10.00 | 0.19/0.18/0.23 | **0.54** |
| CREWHERD | 3.00 | 1.00 | 3.67 | 10.00 | 0.14/0.21/0.26 | **0.54** |

99 coordinates buy the whole crew-ask gain: CREW matches FULL's crew MAE on the real dawns.
## 2. Identity gate — fails as previously documented, and the failure is not ours

| gate | result |
|---|---|
| B here vs `S/topledger3/raw_B.npz` (6,789 worktree) | **not bit-equal**: pooled margin −13,751.4 vs −13,721.6 = **−29.8 coins**, max end-coin delta 381 |
| B here vs `S/melon_decomp/raw_B.npz` (6,789 worktree) | **not bit-equal**: pooled −191.9 vs +101.0 = **−292.9 coins**, max 764 |
| B in `raw_YMG.npz` vs B in `raw_YMGX.npz` (two processes, this tree) | **all 14 arrays BIT-EQUAL** |

Same cross-tree drift `2026-09-14-wheat-slope.md` §2 measured to the coin (−29.8 / −292.9, unchanged
by the working-tree EXEC-SCOPE edits, which are `MACRO_EXEC_ON=False` and inert): the shipped
runners load the 6,789-coordinate worktree, which cannot hold a 7,020 seed at all. **Every Δ below
is paired against a B row from the same run**, so the drift cancels.

## 3. Paired CRN margins (B is the row in the same run, not the stored `raw_B.npz`)

### (a) ymg_aq top five — the 6 retention>=0.95 boards x 2 seats (12 games)

| theta | ours | theirs | margin | Δ vs B | sd | t | wins | d0-9 | d10-19 | d20-29 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| B | 93,127 | 106,879 | −13,751 | — | — | — | — | +3,782 | −20,173 | +2,640 |
| FULL | 52,984 | 146,857 | −93,873 | **−80,122** | 19,137 | **−14.50** | 0/12 | +1,514 | −53,626 | −41,761 |
| CREW | 93,095 | 107,584 | −14,489 | **−738** | 2,294 | −1.11 | 5/12 | +3,832 | −20,992 | +2,671 |
| CREWHERD | 91,824 | 113,995 | −22,172 | **−8,420** | 5,423 | **−5.38** | 0/12 | +2,356 | −24,287 | −241 |

### (b) band clone — all 68 rows of `S/melon_decomp/boards.json` (40 TOPB2 + 28 LIVE-C)

| theta | ours | theirs | margin | Δ vs B | sd | t | wins | d0-9 | d10-19 | d20-29 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| B | 104,092 | 104,284 | −192 | — | — | — | — | +3,300 | −15,478 | +11,986 |
| FULL | 62,873 | 146,020 | −83,146 | **−82,954** | 18,701 | **−36.58** | 0/68 | +1,943 | −44,239 | −40,850 |
| CREW | 101,851 | 105,848 | −3,997 | **−3,805** | 4,522 | **−6.94** | 7/68 | +3,123 | −17,452 | +10,332 |
| CREWHERD | 101,896 | 110,435 | −8,539 | **−8,347** | 5,636 | **−12.21** | 2/68 | +1,753 | −19,483 | +9,191 |

Damage concentrates in **d10-19** for every arm (the `2026-09-08-loss-anatomy` discriminator band);
FULL additionally gives up the whole d20-29 harvest (+11,986 → −40,850).

### Season net by product (ours − theirs, coins/game; Δ vs B in brackets)

| line | ymg B | ymg FULL | ymg CREW | ymg CREWHERD | band B | band FULL | band CREW | band CREWHERD |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| WHEAT | −6,643 | −5,824 (+818) | −7,044 (−401) | −7,964 (−1,321) | −896 | +2,727 (+3,623) | −1,903 (−1,007) | −2,159 (−1,263) |
| WOOL | −5,697 | −8,806 (−3,108) | −6,091 (−394) | −3,063 (**+2,635**) | −2,987 | −7,943 (−4,956) | −3,524 (−536) | −1,198 (**+1,790**) |
| MILK | −3,005 | −22,804 (−19,800) | −2,073 (+932) | −7,996 (−4,992) | +290 | −23,119 (−23,409) | −633 (−923) | −6,991 (−7,281) |
| STRAWBERRY | −3,072 | −30,012 (−26,939) | −3,230 (−158) | −3,426 (−354) | +6,655 | −29,091 (−35,746) | +5,885 (−770) | +5,974 (−681) |

CREWHERD is a clean cow→sheep trade and it is **negative both times**: wool pays +1.8-2.6k, milk
pays −5.0-7.3k. FULL closes the WHEAT line on the band (+3,623) and pays −35,746 strawberry and
−23,409 milk for it — the same conservation `2026-09-14-wheat-slope.md` measured on `cb[WHEAT]`.

## 4. Execution check: the ask is NOT what hires (ymg_aq boards, HIRE counter in the sim seat)

| theta | ask d0/d1/d5/d10 | **landed** d0 | d1 | d5 | d10 | season | cash d5 | cash d10 | wheat d10 | animals d10 G/C/S | idle d10 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|
| ymg_aq replay | — | 4 | 1 | 4 | 11 | 278 | 489 | 1,355 | 16.5 | 0/7.5/3 | — |
| B | 0/0/0/10.5 | **4.00** | **1.00** | **5.50** | 8.42 | **261** | 1,428 | 6,032 | 8.5 | 1.7/6.2/2.8 | 1.1 |
| FULL | 3.0/0.5/3.0/10.2 | 3.00 | 0.00 | 2.50 | 5.25 | **143** | 264 | 3,854 | **19.2** | 0.0/2.5/2.0 | **20.2** |
| CREW | 3.0/1.0/3.7/10.0 | 4.00 | 1.00 | 5.50 | 8.25 | 258 | 1,502 | 6,092 | 8.8 | 1.7/6.0/3.0 | 1.2 |
| CREWHERD | 3.0/1.0/3.7/10.0 | 4.00 | 0.00 | 5.67 | 8.42 | 252 | 1,399 | 4,547 | 8.9 | 1.6/5.2/4.1 | 2.2 |

Three facts, and they close the macro-extract's biggest UNVERIFIED row:

1. **B's crew ramp already executes, and it matches ymg_aq.** 4 hands on d0, 1 on d1, 5.5 on d5,
   261 a season — B's decoded ask of 0 hands before d6 never binds because `HIRE_ROW_ON`'s
   enumeration hires on today's task gain, not on `crew_target`. `crew_target` is a *floor and a deferral*, not
   the hire driver. `2026-09-14-macro-extract.md` §2 compared their landed roster with our decoded
   ask; corrected, the hands gap is **d10 only** (8.4 vs 11).
2. **Raising the ask does essentially nothing to landed hires** (CREW: 258 vs 261) and still loses.
   The ramp gene is not a lever on this margin.
3. **FULL hits the wall from the other side**: it asks for more hands (10.2 at d10) and lands
   *fewer* (5.25, 143 a season) because its wheat-only board emits fewer tasks, and it leaves
   **20.2 idle tiles** at d10 while holding 264 coins at d5. It buys ymg_aq's wheat count and none
   of the work that makes it pay — the FORWARD_ADMIT postmortem (build story, "Forcing the band's
   opening", 94 % → 26 %) repeated with a fitted theta instead of a forced opening.

The band run (no HIRE counter) tells the same story in cash/idle/tiles: FULL holds 159 coins at d5
and leaves 11.6 idle tiles at d10 against B's 2.7.

## 5. Is an ES arm from CREW or CREWHERD worth GPU time? No.

An arm is worth a card when the seed starts ahead or opens a direction the incumbent cannot reach.
Neither holds. CREW starts −738 (t −1.11) on the ymg_aq set and −3,805 (t −6.94) on the band, and
its whole content is 99 coordinates in `g10`/`gb10` — a block ES already perturbs every generation
at sigma 0.02, and B is a strict local optimum in this lattice (2026-09-11 integer search). Seeding
it starts an arm ~4k behind B along a direction the outcome gradient has already declined, and §4
says why the direction is empty: the ask it moves is not the quantity that hires. CREWHERD is worse
and is a known-priced trade (wool +2k, milk −5..7k) that `2026-09-14-wool-mech` already called
negative. Recommend **no arm**; the GPUs stay on the executor question.

**What EXEC-SCOPE (`MACRO_EXEC_ON`) must provide before FULL can execute**, in the order the
numbers demand: (i) a **task source for the non-wheat crops the seed zeroes** — FULL's 20.2 idle
tiles at d10 are tiles the plan cannot fill because the shared softmax gave them no crop; the
executor needs a per-day plan channel (a day-indexed `cb`), not a bigger `dev_frac`; (ii) **hire
enumeration priced against the SCHEDULE, not today's derived tasks** — FULL asks 10.2 hands at d10
and lands 5.25, so the executor must be allowed to hire against tomorrow's planted board (this is
the `FORWARD_ADMIT` gap, still unbuilt); (iii) the **sale/fertiliser legs that have no decoder
channel at all** (§4 of the macro-extract): 348 SELL lots and 138-156 FERTILIZE ops a season carry
the milk and strawberry lines FULL loses by −19.8k and −26.9k. Until (i)-(iii) exist, a macro seed
can only reproduce the top five's *board* and not their *income*, which is what these six numbers
measure.

## 6. Files

`S/seed_screen/`: `seed_CREW.npy` (`504b30a2…`), `seed_CREWHERD.npy` (`4d3a5790…`),
`fit_masked.py`+`.log`/`.json`, `decode.py`, `decode_real.py`, `ledger_seeds.py`,
`ledger_hires.py`, `report_seeds.py`, `raw_{YMG,YMGX,BAND}.npz`, `boards_*.json`, `*.log`.
