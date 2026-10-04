# STAGED upload — `SELL_SLOT_PRIORITY_ON` on top of the shipped `lot4t17`

Not uploaded; tarball in `dist/`, `submission/` untouched. §115b promotion of `2026-09-16-combo2.md`
§3 — the INCREMENT over the live `lot4t17` (sub 56276165), not a fresh pair; standalone the arm was
REJECT by 56 coins (`2026-09-16-slotprio.md`).

| | |
|---|---|
| Tarball | `dist/submission_flow193_g100_hr_lot4t17_slotprio.tar.gz`, 297,632 B, md5 `b3c33bbfe3f22f939d553f7db60b8d25`, sha256 `a899aa8756bd…dbd0b9d` |
| Ship commit / theta | `ship-slotprio`, rebased onto master `6a7ea16` (docs + `S/` only, no `src/`, so the tarball md5 is unchanged and `--ff-only` applies; the digest pin and package base are still the uploaded `lot4t17` `15e8e23`); `flow193_g100_hr.npy`, md5 `7fcf39485bae65ee84171957c5843814` = the live `theta.npy` |
| Changed | `src/kagg3/core/plan.py:4084` `SELL_SLOT_PRIORITY_ON = True` + a dated block citing combo2, and the doc block above it restated (it said the switch is pinned OFF against `git archive HEAD src`); 17 ins / 4 del, the only `src/` file touched. Switches in the tarball: `LOT4_ON` True / `LOT4_TURN` 17, `SELL_SLOT_PRIORITY_ON` + `_SELLS_FIRST_ON` True, `OPEN_PUMP_ON`/`TAIL_FILL_ON`/`BANK_BEFORE_LOT_ON`/`HIRE_ROW_ON` True |
| Replaces | Kaggle sub **56273500** (pump-off), the older active one. NOT `lot4t17` 56276165 |

## Evidence (combo2 §2/§3 — engine, paired CRN, one variable, theta B)

| read | boards | Δ margin | t | flips |
|---|---:|---:|---:|---:|
| **INCREMENT over `lot4t17`, POOLED180 = the §115b statistic** | **169** | **+459** (se 63) | **+7.31** | **8 W / 0 L rows, 4/0 boards** |
| increment: BAND180 / POOLED BAND 90 / LIVEC-H30 / H30B / NEXT30 | 79/90/30/30/30 | +506 / +418 / +587 / +305 / +362 | +4.23 / +7.74 / +4.59 / +4.92 / +5.08 | all ≥ 0, none against |
| COMBO vs B: POOLED180 / ENG22 / V45LEG | 169/22/30 | +1,250 (se 97) / +762 / +1,197 | +12.92 / +4.97 / +6.68 | 24/0, 4/0, 8/0; win 71.6 → 78.7 % |

§115b PASS on the increment (≥ +450, t ≥ 3); nothing flips against us anywhere; two purses ours +244 / theirs −215. §115 vetoes not re-run — combo2 §0 is the whole read.

## Verification

1. Package `plan.py` byte-identical to this worktree's `src/kagg3/core/plan.py`; theta md5 as above.
2. Engine smoke (`eval_vs_baselines.py --me <tarball>`, V45LEG board 109504366, seed base
   1600781801, `--seed-per-opponent`, pinned towns, both seats): **75,405 / 77,759** — coin-exact
   with that board's row in `S/lossflip/c2_combo_v45.csv`.
3. Retention (leg re-run from this worktree → `S/lossflip/topb3r9_l4t17_slotprio.csv`): **9/9
   boards ≥ 0.85** (Majkel1337 0.86, ymg_aq 1.02, DSM 1.00, = B's own); +280/board vs B (t +0.39).
4. `tests/test_slotprio.py` re-pinned: ON is the identity pin against `git archive 15e8e23 src`
   with the knob set after import, OFF pinned to that tree's own `False`, and the
   `test_budget_order`-before-`kagg3` import-order defect fixed as in `ship-lot4` (`4703d9d`)
   with the `kagg3.__file__` assert. ON/OFF digests differ on 4 of the 10 pin entries, so both
   pins bite. **12/12 pass**; `test_lot4.py` 12/12 and `test_shed_dump.py` 9/9 stay green (lot4's
   pin boards use the default macro, which this switch does not reorder). Other
   `*_byte_identical_*` reds = the pre-existing 28 + 14 of `2026-09-16-upload-lot4.md`.

After the upload: `git merge --ff-only ship-slotprio` on master, swap `submission/` for this tarball's payload, add the row above + the new sub id to `submission/UPLOAD.md`.
