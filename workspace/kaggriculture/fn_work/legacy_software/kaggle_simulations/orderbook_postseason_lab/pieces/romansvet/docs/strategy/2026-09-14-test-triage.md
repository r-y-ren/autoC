# Test triage at master b131245 — is the shipped planner still the planner?

**HEAD default-off == shipped package: YES.**

Three independent lines of evidence, all at `master` HEAD `b131245`:

1. **The tarball is the ship commit.** `submission/submission_flow193_g100_hr.tar.gz`
   unpacked and `diff -r`'d against `src/kagg3` at `b1bde4f` (the commit
   `submission/UPLOAD.md` names) reports **zero content differences** — the only
   lines are five `agent/book_*.py` / `agent/opening.py` files and `src/kagg3/{es,sim}`
   that the packager does not vendor. `S/test_triage/diff_pkg_vs_ship_commit.txt`.
   `b1bde4f` is an ancestor of HEAD.
2. **The planner decodes identically.** The whole six-array `build_day` plan,
   digested over `test_route_early.PIN_SEEDS`' 12 seeded boards, is byte-for-byte
   the same at HEAD, at `b1bde4f` (shipped) and at `076c195` (today's session base),
   both under the shipped switch defaults and with `BANK_BEFORE_LOT_ON` forced off.
   `S/test_triage/digests.txt`.
3. **The engine plays the same games.** Six boards (TOPB2 ids 107448662 / 107450553 /
   107454465, both seats, seed-base 777001, theta B = `submission/theta.npy`,
   `OPEN_PUMP_ON=True`) played once from HEAD `src` and once from the `b1bde4f`
   worktree: the two result CSVs are **byte-identical** — same coins, same move
   counts, same unsold, board for board. `S/test_triage/leg_head.csv`,
   `S/test_triage/leg_ship.csv`, `S/test_triage/legs.log`.

So master's default-off planner is still the planner we uploaded, and every
"identity vs HEAD" gate run today measured against the right baseline.

## Why HEAD's source still differs from the package, and why it is inert

`diff -u` of the four differing modules is in `S/test_triage/diff_pkg_vs_head.txt`
(795 lines, 584 of them pure additions). Only four hunks touch a shipped line:

| module | change | why it is inert for theta B |
|---|---|---|
| `core/policy.py` `forward()` | new `momentum=None` arg; `h = tanh(enc_pre + momentum @ p.mh)`, `scores += momentum @ p.ms` | theta B is 6,789 floats = exactly `offset("mh")`, so `unpack` zero-pads `mh/ms`; the added term is an exact `+0.0` |
| `core/brain.py` | passes `market_momentum(xp, obs)` to `forward()` unconditionally | same — the product is zero |
| `core/brain.py` crop-mix block | new `if theta.shape[0] > PO.offset("cm")` branch ahead of the `PLANT_MIX_DRAIN_ON` branch | `offset("cm") = 6,855 > 6,789`, so theta B falls through to the original `elif/else`, the shipped expression |
| `core/plan.py` `HIRE_ROW_ON` | gate widened to `HIRE_ROW_ON and not (MACRO_EXEC_ON and MACRO_SCHEDULE is not None and _macro_site(6))` | `MACRO_EXEC_ON = False`, `MACRO_SCHEDULE = None` at HEAD |
| `core/policy.py` `init()` | `mh/ms/cm/cb/cd` zero-init instead of He | fresh-init only; does not touch decode |

`tests/test_backend_agreement.py::…[incumbent_b_padded]` passes, which is the same
claim measured rather than argued: padding theta B to the new layout changes no
decision in 2,400.

## Per-test bisect

All nine failures are **pre-existing and pre-date today's session**; every one of
them already fails on the exact tree we uploaded to Kaggle.

| test | HEAD b131245 | 076c195 (session base) | b1bde4f (SHIPPED) | b9b732b (ship^) | first failing commit |
|---|---|---|---|---|---|
| `test_bank_before_lot.py::test_off_plan_is_byte_identical_to_the_shipped_planner` | FAIL | FAIL | FAIL | FAIL (1 of 12 digests) | ≤ `b9b732b`; `b1bde4f` widened it to 11 of 12 |
| `test_early_sell.py::test_off_plan_is_byte_identical_to_the_pre_switch_planner` | FAIL | FAIL | FAIL | not measured | ≤ `b1bde4f` |
| `test_early_sell.py::test_on_mode_z_buys_on_the_first_turn_behind_the_hires_with_room` | FAIL | FAIL | FAIL | not measured | ≤ `b1bde4f` |
| `test_early_sell.py::test_on_mode_z_hands_a_wide_day_back_to_mode_a` | FAIL | FAIL | FAIL | not measured | ≤ `b1bde4f` |
| `test_crew_and_herd_mix.py::test_a_positive_hire_bias_raises_the_crew_the_planner_chooses` | FAIL | FAIL | FAIL | not measured | ≤ `b1bde4f` |
| `test_crew_and_herd_mix.py::test_an_early_bucket_raises_the_day_10_crew` | FAIL | FAIL | FAIL | not measured | ≤ `b1bde4f` |
| `test_crew_and_herd_mix.py::test_the_late_bucket_moves_the_late_crew[21]` | FAIL | FAIL | FAIL | not measured | ≤ `b1bde4f` |
| `test_crew_and_herd_mix.py::test_the_late_bucket_moves_the_late_crew[27]` | FAIL | FAIL | FAIL | not measured | ≤ `b1bde4f` |
| `test_crew_and_herd_mix.py::test_no_bucket_hires_on_the_terminal_day` | FAIL | FAIL | FAIL | not measured | ≤ `b1bde4f` |
| `test_backend_agreement.py[legacy]` | FAIL 2/2400 | FAIL 2/2400 | FAIL 2/2400 | not measured | ≤ `b1bde4f` |

Raw runs: `S/test_triage/run.log` (HEAD), `S/test_triage/bisect_b1bde4f_076c195.log`,
`S/test_triage/bisect_076c195_full.log`, `S/test_triage/backend_bisect.log`.

**Pin updated by the behaviour change?** No, in every case. The `test_bank_before_lot`
`PIN` tuple has not been touched since the switch commit `67173cb`/`88452f3`
(`git log -S` on the digest), and `b1bde4f` shipped `HIRE_ROW_ON = True` — a change to
the *default stack the pin is taken against* — without regenerating it. That is the
whole of the (a) failure.

**Failure signatures.**

* (a) `test_off_plan_is_byte_identical_to_the_shipped_planner`: index 0
  `5eb341ee7114330f` (got) vs `b00faee2c2fa62fb` (pin); 11 of 12 digests move.
  At `b9b732b` (HIRE_ROW off) 11 of 12 *match* the pin and only seed 11 differs
  (`b2b2bb6174c67125` vs pinned `26afc79decfc7a22`), so at least two separate
  shipped-default promotions have moved this pin since `bdcf5f9`.
* (b) `test_early_sell` index 0 `9764aaa7e5b33019` vs pinned `d4e7ca576cf7637f`;
  the two Z-mode failures are `assert both == {1, 2}` got `{1}` and
  `assert wides` got `[]` — i.e. **no fixture board hires past the first row any
  more**, which is exactly what `HIRE_ROW_ON` does (it trims the HIRE row to the
  hands whose route is not all PASS).
* (d) all five crew failures read the HIRE row rather than the enumeration:
  `assert 7 > 7`, `assert 11 > 11` (the hire-bias gene no longer separates two
  thetas through the trimmed row) and `assert 0 == 16` on the terminal day.
  Same cause as (b).

**Not a regression, and a small improvement:** `076c195` additionally fails seven
`test_crew_and_herd_mix.py::test_crop_mix_*` tests that **pass at HEAD** — today's
crop-mix work fixed them.

## (c) the 2-of-2400 backend disagreement

```
decision 1532: hire_bias numpy=33 jax=32   (day 16)
decision 1533: hire_bias numpy=33 jax=32   (day 16)
```

* Reproduces **identically** — same two decisions, same field, same values — at
  `076c195` and at `b1bde4f`. It is not new and it is not from today.
* It is on the `[legacy]` parametrisation only, whose theta is
  `artifacts/theta.npy`, **4,848 floats — not the shipped theta B**. The three
  theta-B variants (`incumbent_b`, `incumbent_b_padded`, `incumbent_b_crop_mix`)
  pass with 0 of 2,400.
* `hire_bias` is the only differing field on both decisions; it is a one-coin step
  in a *score bias* fed to the crew enumeration, not an action. Measured: across
  200 seeded boards spanning day/purse/herd/ripe/plant-target, `hire_bias = 32`
  and `hire_bias = 33` produce **the same plan digest on 200 of 200** boards
  (`S/test_triage/hb_probe.txt`). So the artefact does not reach an engine action
  on this evidence.
* Character: an XLA-fusion/ordering artefact at the `floor(continuous * count)`
  cliff the file was written for — `kagg3.precision` closes the TF32 gap to ~2e-6
  and `QUANT_EPS` snaps exact integers, but a product landing this close to a
  floor boundary still splits. Report only; no fix attempted, per brief.

## Pins: none updated

Task 5's condition ("behaviour identical to the shipped package **and** you can name
the commit that legitimately changed it") is only half met. The behaviour half is
proven — HEAD, `b1bde4f` and `076c195` decode the same plan and play the same six
boards to the coin. The attribution half is not: between the pin's origin `bdcf5f9`
and the ship commit there are 34 core commits including at least four shipped-default
promotions (`ff3fe12` OPEN_PUMP_ON, `9041032` OPEN_PUMP_SLOT0_ON, `eff3310`
TAIL_FILL_ON + BANK_BEFORE_LOT_ON, `b1bde4f` HIRE_ROW_ON), and the `b9b732b`
measurement shows the pin had **already** moved on one seed before `HIRE_ROW_ON`.
No single commit can be named, so the pins are left alone and this is the finding.

The (b) Z-mode and (d) crew failures are **not** stale pins at all — they are live
behavioural assertions that `HIRE_ROW_ON` invalidated when it shipped. They need
rewriting against the enumeration rather than the trimmed HIRE row, or new fixture
boards that still go wide. Out of scope here; reported, not touched.
