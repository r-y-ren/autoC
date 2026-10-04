# The sim screen learns the top-tier leg: `boards_topb2.json` (2026-09-11)

`S/simscreen/screen.py` could only rank thetas on the LIVE-C hold-out family, and it
priced the one loss shape that matters most badly: `flow201_g10_hr`, which the engine
TOPB2 leg scores **−1,815 paired vs B**, read only **−174** on the LIVE-C boards. The
screen was blind to top-tier losses because it never played top-tier opponents. This
adds the missing board file.

## What was built

* **`S/simscreen/boards_topb2.json`** — the second frozen board list: the 20 TOPB2 tapes
  (`S/topb2/ids.txt`) in both seats on the engine's own first `--seed-per-opponent` draw
  (`seed_base 777001`, `SEED_STRIDE 1000003`) = 40 boards. Cross-checked against
  `S/lossflip/flow193_g100_hr_topb2.csv`: the (tape, seed, seat) set is **identical, 40/40** —
  the screen plays byte-for-byte the games `S/topb2/run.sh` hands the engine.
  All 20 ids have pinned-town tapes in `artifacts/tape_actions_town/` (0 missing), so nothing
  was taken from the open-loop `artifacts/tape_actions/` and no town was fabricated.
* **`screen.py --board-file`** (new; `--boards` stays the board *count*, default unchanged).
  Default is `boards.json`, so every earlier invocation is unaffected. Switch-string handling
  is untouched: the shipped `hr` composition
  `OPEN_PUMP_ON=True,TAIL_FILL_ON=True,BANK_BEFORE_LOT_ON=True,HIRE_ROW_ON=True`
  is still applied before the `sim` imports.
* Run artefacts: `S/simscreen/topb2_40.csv`, `topb2_40.log` (280 episodes, **252 s** wall,
  4 CPU threads, ~190 s of it XLA compile).

## Validation — screen vs engine, TOPB2, paired vs B (`flow193_g100_hr`)

Engine columns recomputed from the `S/lossflip/*_topb2.csv` pairs; they reproduce the
`AUTOJUDGE-vsB` lines in `S/glut/verdicts.log` to the coin.

| theta | screen Δ vs B | screen t (n=40) | screen t (20 boards) | engine Δ vs B | engine t (n=40) | sign |
|---|---|---|---|---|---|---|
| flow201_g10_hr   | **−1,837** | −3.70 | −2.60 | **−1,815** | −3.63 | ✓ |
| flow201_g20_hr   | **−1,681** | −3.21 | −2.31 | **−1,663** | −3.20 | ✓ |
| flow194_g100_hr  | −866 | −1.40 | −1.02 | −797 | −1.30 | ✓ |
| flow200_g100p_hr | −335 | −0.75 | −0.53 | −290 | −0.65 | ✓ |
| flow187_g160     | −253 | −0.59 | −0.42 | −292 | −0.68 | ✓ |
| flow200_g30_hr   | −58 | −0.12 | −0.09 | −61 | −0.13 | ✓ |

* **Sign agreement 6/6.** Largest Δ error **45 coins** on a −1,815 read; mean |Δ error| 33 coins.
* **Win % is exact on all 7 thetas**: B 32.5, g10 25.0, g20 25.0, g30 27.5, g100p 25.0,
  f187 25.0, f194 27.5 — screen and engine agree digit for digit.
* **Spearman(theta-level Δ) = 0.943.** The single inversion is `flow187_g160` vs
  `flow200_g100p_hr`, which the engine itself separates by **2 coins** (−292 vs −290): a tie,
  not a ranking failure.
* Per-board fidelity (280 board cells): mean error **+166** coins, MAE 920, **sign agreement
  97.9 %** (274/280). The +166 is a constant level bias that cancels under pairing — the
  per-board *paired-Δ* error is mean −19, MAE 681.
* `shopdiff 0.0 %` on all 280 cells: every theta saw byte-identical shop sequences. The
  ±25k YARN_STORE lottery that breaks engine pairing is absent, as on the LIVE-C file.

## Resolution

Paired SE is **431–617 coins** at the 40 CSV rows. That number is optimistic: on this leg the
action-replay seat makes the two seats the *same game* on 10–15 of the 20 tapes (the engine
csv shows the same degeneracy, 10/20 for B, 15/20 for `flow201_g10_hr`), so the honest unit
is the 20 tapes and the SE is **606–849 coins/board**. Read the `t (20 boards)` column when
deciding, and treat |t| ≳ 2.5 there as the refusal threshold rather than the |t| > 3 the
60-tape LIVE-C file supports.

## Can the screen now refuse on top-tier grounds?

**Yes.** `flow201_g10_hr` — the loss the LIVE-C file priced at −174 — reads −1,837 with
t −3.70 (t −2.60 on 20 boards) in 4 CPU-minutes and no engine leg; `flow201_g20_hr` reads
−1,681/−3.21. Both are the arms the engine judge actually refused. The screen remains a
REFUSE-and-ORDER instrument, never a promotion one: it can now say "this theta pays for its
hold-out gain on the top tier" before an engine leg is spent, which is exactly the stop-rule
clause (`TOPB2 not down`) that promotion turns on.

Unchanged limits: it prices only the 20 TOPB2 tapes (not the wider top-ten population), it
cannot price the glut/CARE_FILL family (`2026-09-09-care-coverage.md:175`), and an open-loop
tape or a drawn town is outside it.
