# SLOTMIRROR — the rival's row is not our row, and the slot rank has no second model

2026-09-16 13:00–13:30Z, branch `slotmirror` off master `4054968`. `2026-09-16-nbintel2.md` §6
items **1 and 2**, the two ranked upgrades to the `SELL_SLOT_PRIORITY` shipped this morning at
+459. **Both REJECTED at the ENG22 kill gate, and again on the clone leg the mirror is actually
about.** No upload, no POOLED180 cut. Mechanics from the public notebook, code from nobody: the
replay is re-derived from our own `sim/market.py`.

## 1. VERDICT

| arm | ENG22 (44 games) | V45LEG clones (60 games) | §115b |
|---|---:|---:|---|
| `SELL_SLOT_MIRROR_ON` | **−23** (t −0.99) | **−60** (t −0.91, 1 flip against) | REJECT |
| `SELL_SLOT_MIRROR_GATE_ON` (SIM 25) | **−22** (t −2.00) | **−40** (t −2.13) | REJECT |
| both | **−45** (t −2.19) | **−90** (t −1.36, 1 flip against) | REJECT |

Bar: +100 and t ≥ 2 on the increment over the shipped pair. Nothing reached it, so POOLED180
(169 boards) was never cut and no package smoked — neither arm can pass §115b with two
out-of-pool legs negative over 264 games. **The sell-slot RIVAL-MODEL family is closed at both
ends**: `slotprio` §5 measured the batch clamp flat, and the exact model is worse than the proxy.

## 2. WHY — the only information in a slot is the rival's REAL row

Nine products, nine slots, one row. Each product has its own market inventory, so **two slots
of one row never interact**: permuting our row is revenue-neutral *except* through the rival's
order on the same item in the same slot round (`sim/market.py`'s coupled walk `M_SELL_PAIR`).
Every coin a slot ordering can earn is a read of the other seat. `SELL_SLOT_PRIORITY` reads
the rival's real board (`DayView.opp_ripe`) and prices our units against it: a crude read of a
real seat, worth +459. `SELL_SLOT_MIRROR` replaces it with an *exact* replay of a rival that
**does not exist** — our own row in default order — trading a weak read of a real board for a
perfect read of an imaginary one. The instrument (§3) prices that fiction at **+4,839 coins a
seat-game**; the engine paid **−23**. The `counterfactuals-overstate` two-purse rule at its
widest yet. And the clone leg is the load-bearing control: on 30 fresh post-09-15 V45 tapes,
where "the rival sells what we sell" is closest to true, the mirror is **−60 with a board flip
against it**. The premise was given its best board and still did not pay.

## 3. THE INSTRUMENT (5 ENG22 boards, 10 seat-games, `S/slotmirror/instrument.py`)

`sell_slot_mirror_scores` / `sell_slot_gate` wrapped in the parent before the eval pool forks,
so every worker records; the gate opened wide, so the PLAN is the MIRROR-alone arm. 530 SELL
rows scored, **2.65 live products a row** (most days have two or three products to order at
all); **314 rows (59.2 %) re-ordered** away from the row the plan would have emitted; modelled
gain **+91.3 coins/row** (+154 on the rows it moves, max +1,324) = **3.59 %** of the row's own
coupled revenue = **+4,839 a seat-game**. The gate's similarity term: median **20 %**, ≥25 % on
47 % of days, ≥50 % on 23 %, **≥90 % on 0 %** — the notebook's own 0.90 clone probe would never
have fired here; money lead median −1,689, under +5,000 on 94 % of days. The one true number is
the 59.2 %: the arm does change the row, on 36 of 44 ENG22 games, for nothing.

## 4. THE GATE FALSIFIES ITS OWN PREMISE

`nbintel2` §6 item 2 reasoned that SLOT-PRIO's 56-coin solo miss was the 25-40 % of the band
that is not a clone, so the losing boards are the non-clone ones. The ablation says no:

| gate | fires on | ENG22 |
|---|---:|---:|
| SIM ≥ 25 (shipped constant) | 47 % of days | **−22** (t −2.00) |
| SIM ≥ 50 | 23 % of days | **−41** (t −2.17) |
| SIM ≥ 0, money-lead veto only | ~94 % of days | **−0** (t +0.52, sd **4**) |

**Monotone in suppression**: the more days the reorder is switched off, the more coins go with
it. SLOT-PRIO's value is not concentrated on clone-similar boards — on ENG22, the *least*
clone-like class we judge, it was +446 in its own leg. The lead veto is a measured no-op (sd 4).

## 5. WHAT SHIPPED (nothing) AND WHAT IS ON DISK

Both switches are module constants **defaulting OFF** (`plan.py:4230`); the whole-plan sha256
over five boards is pinned byte-identical to `git archive 4054968 src`
(`tests/test_slotmirror.py::test_off_plan_is_byte_identical_to_master`, 15 tests green).

* `sell_slot_mirror_revenues` — int[L,9,3], our revenue for a product sold EARLY / COUPLED /
  LATE, each column pinned against `sim/market.sell_walk`'s own walk.
* `sell_slot_mirror_scores` — bounded 2-swap hill climb (10 rounds x 36 pairs, strict
  improvement, live block only), handed back as `8 - slot` so `sell_slot_perm`'s argsort *is*
  the permutation and `_market` is untouched. jit == numpy; within 25 coins of the brute-force
  optimum over the whole live block, never below the identity row.
* `sell_slot_gate` — integer histogram intersection of our row against `opp_ripe` plus the
  money-lead veto; `DayView.opp_money` (new, defaulted) is supplied by `sim/rollout.py` and
  `agent/parse.py` only when the gate is on. `S/slotmirror/`: `run_eng22.sh` (three arms,
  `WITH_V45=1`), `instrument.py`, `results.md`, `csv/` (untracked per `S/.gitignore`; the
  runner banks the same rows in `S/lossflip`).

## 6. WHAT THIS LEAVES

1. One live direction, the one `2026-09-16-slotprio.md` §6 named: **a read of the rival's ACTUAL
   sell row** — not their board, not our own row. `2026-09-16-rivaltell.md` has that tell EXACT
   (P 1.0) with its batch term DEAD; the tell driving the *ranking* was never built.
2. Do not re-open the mirror on a better search: the climb is within 25 coins of its model's
   exact optimum. The model is wrong, and a better optimiser of a fiction is worth less.
3. `nbintel2` §6 item 3 (`FERT_RESERVE_ON`) is untouched and is now the only unbuilt item of
   that ranked table.
