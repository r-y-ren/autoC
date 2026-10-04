# STAGED upload candidate — `OPEN_PUMP_ON=False` (pump-off B)

Not uploaded. Built 2026-09-16 for the user's upload decision; the tarball is in `dist/`
and nothing under `submission/` was touched.

| | |
|---|---|
| Tarball | `dist/submission_flow193_g100_hr_pumpoff.tar.gz`, 290,015 bytes, md5 `890b489d863f5e15d63508021f7a1dd4`, sha256 `b3698a8978425d5b292783134e50151b1ed69a8b73becb73d2f6d7c93aaeb398` |
| Ship commit | `d0e469d` (branch `ship-pumpoff`, parent `ef2eff6`): all 17 `kagg3/*.py` in the tarball are byte-identical to `src/kagg3` at that commit (`git show d0e469d:src/kagg3/<f> | cmp -` , 17/17) |
| Theta | `artifacts/kagg2_games/thetas/flow193_g100_hr.npy` — the **unpadded** 6,789 float32 file, md5(file) `7fcf39485bae65ee84171957c5843814`, md5(bytes) `41b87adc`; byte-identical to `theta.npy` inside the live submission tarball |
| Switches | `TAIL_FILL_ON`, `BANK_BEFORE_LOT_ON`, `HIRE_ROW_ON` True as shipped; **`OPEN_PUMP_ON` now False** (the only change). `OPEN_PUMP_SLOT0_ON` stays True but dormant, `OPEN_PUMP_TELL_KEEP0_ON` stays False, and every line of pump code is kept |
| Built by | `.venv/bin/python scripts/package_submission.py --theta artifacts/kagg2_games/thetas/flow193_g100_hr.npy --out dist/submission_flow193_g100_hr_pumpoff.tar.gz` |
| Smoke | **124/124 coin-exact** against the judge's `OPEN_PUMP_ON=False` rows on the 62 LIVE boards (`S/lossflip/B_pumpoff_live62.csv`), and 0/124 against shipped B — see below |
| Replaces | Kaggle sub **56143250** (flow172_g1000_pair_hr, md5 `8274d577`), the older of the two active submissions. **Not** B 56161192 |

## Why it ships

`docs/strategy/2026-09-16-v45leg.md` (commit `ef2eff6`). The 2026-09-04 denial the switch is
built on no longer exists: **134 of B's last 146 opponents open step 0 with a same-turn wheat
round trip** (the V42-V44 `[BUY 5, BUY 10, SELL 60]` clips to the 15 units just bought, so it
is net-zero too). The pot is restored before their step-1 buy, the denial collapses to **six
coins**, both their 500-coin sheep land and their 12 day-0 melons are planted in every arm —
and their SELL leg is quoted off the pot **our** 53 units drained, so the trip hands them
exactly our own excess over the solo ladder: **+26** against a 15-unit opening, **+106**
against V45's 70-unit one.

### Evidence (v45leg §5.1 — engine, paired, CRN, the switch is the only difference)

| family | boards | B (shipped) | `OPEN_PUMP_ON=False` | paired Δ/board | t |
|---|---:|---:|---:|---:|---:|
| SYNTH-V45 (V45 opening, 18 CRN twins) | 18 | +1,703 | +2,858 | **+1,155** | **+4.54** |
| LIVE62 (live hold-out) | 62 | +9,191 | +11,159 | **+1,968** | **+4.04** |
| BAND180 | 79 | +3,494 | +4,395 | **+901** | **+3.14** |
| V45LEG (live tapes cut 09-15/16) | 30 | +1,103 | +1,517 | +414 | +1.16 |
| NEXTHIGH (clone, cut 09-11) | 30 | +2,045 | +1,938 | −107 | −0.47 |
| TOPB2 (2,953+ mixed) | 20 | −1,654 | −1,882 | −228 | −0.40 |
| ENG22 (cluster-1 engine) | 22 | −3,228 | −3,808 | −580 | −0.65 |

§115b pooled read (`pooled_band180.py B_pumpoff`): **POOLED180 +410, se 170, t +2.41** on 169
boards / 338 games — **below** the §115b bar of ≥ +450 **and** t ≥ 3, so this is a **staged
candidate, not a §115b promotion**. Both §115 vetoes pass with room (TOPB2 −228 against a
−1,400 floor, LIVE62 +1,968 against −700) and nothing anywhere is significantly negative.
Detail: old POOLED BAND (90) −20 (t −0.11), BAND180 +901 (t +3.14), the 68-board sim band −76
(t −0.22) — i.e. **switching this 2026-09-04 default off costs the old tapes nothing**, while
it is worth ~+1.1k per V45 opponent, and V45 was 2 of 26 of B's games on 09-16 and zero
before. The upside grows with adoption; the downside on the old band is measured at zero.

Sim-only, for completeness: `OPEN_PUMP_UNITS=70` is −779 live / −5,344 synthetic and `80` is
−4,030 — **the pump must never be resized up**. The corrected tell (`KEEP=0`) is worth +2
coins (t +0.01) and no tell switch was written.

## Verification

1. **Tarball vs source.** 17/17 `kagg3/*.py` byte-identical to `src/kagg3` at `d0e469d`.
2. **Tarball vs a control built from `master` HEAD (`ef2eff6`) with the same theta.** The only
   differing file is `kagg3/core/plan.py`, and the only differing lines are
   `OPEN_PUMP_ON = True` → `OPEN_PUMP_ON = False` plus the dated doc paragraph above it.
   `theta.npy`, `main.py`, `engine.lock.json` and the other 16 modules are byte-identical.
3. **Tarball vs the LIVE upload (`submission/submission_flow193_g100_hr.tar.gz`, md5
   `adf27cb0`).** Six files differ — `plan.py`, `brain.py`, `policy.py`, `sell.py`,
   `agent/runtime.py`, `main.py` — because the live upload was built at `b1bde4f` (09-11) and
   `master` has taken **23 commits touching `src/kagg3` since**, all of them default-off
   switches (LOT4, SHED_DEFICIT, ROUTE_FREEFIRST, PRESTOCK_V2, LOT_SPLIT, REBUY,
   ANIMAL_SAME_DAY, CREW_PUSH_COST, SPREAD_ROWS, MACRO_EXEC, MELON_GENE, CROP_DAY …) plus the
   momentum plumbing (`runtime.pass_prev_mkt_inv`). **That drift is measured to be
   behaviourally inert:** on the 62 LIVE boards the live tarball scores mean margin **+9,191**
   (`S/pkgcheck/flow193_g100_hr_pkg_live62.csv`, 09-11, itself 124/124 coin-exact with the
   judge's B rows) and this tarball scores **+11,159** — a delta of **+1,968/board, exactly
   the judge's single-switch paired LIVE62 figure**, with board wins 106 → 112 of 124. The
   pump is the whole difference between the two uploads.
   The gene flags are inert for this theta by construction: `cm`/`cb`/`cd` are zero in a 6,789
   theta and both ON branches add `exp(0)=1` / `+0.0` (`S/judge7065/judge_candidate.sh`
   header, `decode_receipt.py`, `2026-09-14-judge7065.md` §3), so the judge's
   `brain.MELON_GENE_ON=True,brain.CROP_DAY_ON=True` and the package's shipped `False` decode
   byte-identically — which the 124/124 smoke confirms end to end.
4. **Engine smoke, the UPLOAD.md recipe** (`S/pkgcheck/smoke_flow193_g100hr.sh`, same 62
   boards in `S/live62/ids.txt` order, seed base 777001, `--seed-per-opponent`, town schedule
   `S/band2100p/town_schedules.json`, the packaged tarball in our seat):
   **124/124 coin-exact** against `S/lossflip/B_pumpoff_live62.csv` (the judge's
   `OPEN_PUMP_ON=False` arm), **0/124** against `S/lossflip/flow193_g100_hr_live62.csv`
   (shipped B). Mean coins 108,257 (judge 108,257); mean margin +11,159 (judge +11,159).
5. **Day-0 trace, real engine, V45 board 109529850** (`S/v45leg` seed 1,813,374,004, our seat
   0, packaged agent in our seat): our step-0 market row is
   `[HIRE, HIRE, HIRE, HIRE]` — **no `BUY_PRODUCT WHEAT 53`** — and step 1 carries no
   sell-back; the wheat pot walks `10000 → 9999 → 9994` (their 70-unit round trip restores it,
   we never draw). Final coins **132,904 / 126,511**, coin-exact with that board's row in
   `S/lossflip/B_pumpoff_v45.csv` (shipped B on the same board: 139,753 / 125,839 — one of the
   two live V45 boards, n=2, which v45leg reports as −1,862 t −0.33 against the powered
   SYNTH-V45 +1,155 t +4.54).

## Tests

`tests/test_open_pump_racer.py::test_slot0_ships_on_by_default` is **re-pinned** to the new
shipped default (`OPEN_PUMP_SLOT0_ON is True`, `OPEN_PUMP_ON is False`,
`OPEN_PUMP_TELL_KEEP0_ON is False`). It is the only test changed and the only assertion
touched; nothing was weakened.

**The sweep.** The seven files asked for (`test_open_pump`, `test_open_pump_racer`,
`test_crewpush`, `test_lot4`, `test_spread6`, `test_plant_fill_late`, `test_carrot_hold`) plus
every other test file that mentions `OPEN_PUMP`, plus `test_submission_runs` — 31 files, 399
tests, **14 failed**. The same 14 names, one for one, fail on `master` with `src/` unmodified
(176 tests over the 9 files that carry them): **zero new failures, zero fixed**, and nothing
re-pinned but the one default assertion above.

Pre-existing red, not this switch's doing (`2026-09-16-v45leg.md` §7,
`2026-09-14-test-triage.md` §4) — twelve are `*_off_plan_is_byte_identical_*` digest pins that
have drifted from the planner they were taken against:

```
test_animal_defer.py::test_off_plan_is_byte_identical_to_the_shipped_planner
test_animal_defer.py::test_on_at_full_keep_is_the_off_plan
test_animal_defer.py::test_on_before_day_zero_is_the_off_plan
test_budget_order.py::test_grow_multiplier_tilts_the_seed_mix
test_early_sell.py::test_off_plan_is_byte_identical_to_the_pre_switch_planner
test_early_sell.py::test_on_mode_z_buys_on_the_first_turn_behind_the_hires_with_room
test_early_sell.py::test_on_mode_z_hands_a_wide_day_back_to_mode_a
test_endgame_tomato.py::test_off_plan_is_byte_identical_to_the_pre_switch_planner
test_feed_mandatory.py::test_off_plan_is_byte_identical_to_the_pre_switch_planner
test_fert_volume.py::test_off_plan_is_byte_identical_to_the_pre_switch_planner
test_harvest_first.py::test_off_plan_is_byte_identical_to_the_shipped_planner
test_open_pump.py::test_off_plan_is_byte_identical_to_the_pre_switch_planner
test_open_pump_racer.py::test_off_plan_is_byte_identical_to_the_pre_switch_planner
test_open_pump_racer.py::test_slot0_traces_under_jit_and_keeps_both_legs
```

The three `OPEN_PUMP` ones monkeypatch the switch themselves, so they read exactly the same
with the default flipped — the pump-off build inherits a gate that was already red and does
not add to it. **Fixing them is a separate job and was deliberately not done here.**

## What the user does

1. Upload `dist/submission_flow193_g100_hr_pumpoff.tar.gz` to Kaggle (md5
   `890b489d863f5e15d63508021f7a1dd4`). Kaggle keeps **2** active submissions: this one
   replaces the older **56143250**, **not** B **56161192** — B stays live as the control, and
   the two then race each other in the band.
2. After the upload lands, per the master-branch rule (user, 2026-09-11):
   `git checkout master && git merge --ff-only ship-pumpoff` (ship commit `d0e469d`), replace
   `submission/` with this tarball's payload, and update `submission/UPLOAD.md` with the row
   above plus the new submission id.
3. Re-read in 24-48 h: `bash S/v45leg/cut_all.sh` on a fresh cut and
   `WORKERS=8 bash S/judge7065/run_v45.sh` — v45leg §6 says the same arm becomes a
   promotion-grade read as V45 adoption rises, or it does not.
