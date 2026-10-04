# Frozen day-5 selector fails its continuation threshold

The full thirty-tape H30-development label run and frozen leave-one-tape-out
calibration completed successfully. The learned gate loses 130.25 margin coins
per board versus B (SE 110.77, t=-1.18). It fails the predeclared positive-mean,
t>=2 resource threshold. **Stop this fixed compact+1 day-5 selector without
feature, alpha, threshold or transform retuning. No held-out engine pilot or
production change follows.** This does not close every possible complete-plan
selection method.

| Strategy | Own coins delta | Opponent coins delta | Margin delta | Board SE | Board t |
|---|---:|---:|---:|---:|---:|
| B | 0 | 0 | 0 | 0 | undefined |
| Always compact+1 | -86.33 | +105.67 | -192.00 | 167.85 | -1.14 |
| Frozen ridge gate | -172.48 | -42.23 | -130.25 | 110.77 | -1.18 |
| Per-seat hindsight maximum | +175.62 | -12.02 | +187.63 | 69.95 | descriptive only |

Each board value averages both recorded tape seats; all thirty boards are from
the single development family. Hindsight uses the observed terminal target to
choose and is not an implementable policy or evidence of predictable gain.
The first four tapes were seen before the recipe was frozen, so this analysis
is exploratory development calibration, not pristine out-of-fold inference.
No H30B, NEXT or other evaluation family entered fitting or combined statistics.

The gate chooses the alternative on 28/60 rows, changing the complete plan on
20; eight chosen alternatives deduplicate with B. Across all candidates, 42/60
plans differ and eighteen deduplicate. Every fold keeps both held-out seats
together, trains on 58 rows, scales from those rows alone, drops zero-variance
columns and uses ridge with intercept, alpha 10 and prediction >0. All folds
retain 34 active features. The frozen recipe is in
[the pre-run plan](2026-09-12-planselect-all30-label-plan.md).

## Validation and execution

- Runner `2178a6d` completed under root session 1881, exit 0, from
  14:54:54Z to 15:01:46Z within its 600-second cap. No resume was needed.
  Sixty B branches, forty-two distinct alternatives and one duplicate B
  produce 103 simulated jobs. All future days use ordinary unchanged B.
  Day 29 has exactly 23 turns and no end-of-day step.
- Injected B equals ordinary B, and duplicate B is state-identical on the
  first state. All sixty terminal B own/opponent/margin values match keyed
  `S/isearch/lc.csv` rows exactly. Root independently reproduced that audit,
  verified both checkpoint hashes, and confirmed that all eight original
  pilot target rows are unchanged. This is simulator validation; alternatives
  have not received a new real-engine validation.
- Calibrator `5cfeb92` completed under root session 55291, exit 0 and a
  120-second cap. All eleven focused tests passed in both agent and root runs:
  held-out features cannot alter training scaling or coefficients; held-out
  targets cannot alter predictions for that fold; audit fields cannot enter
  features; altered baseline files and invalid target accounting are refused.
  Root independently recomputed gate decisions, thirty paired-board values
  and all fold memberships. The seventeen runner tests passed before launch.

## Preserved artifacts

Under `S/planselect/`:

- `day5_labels_all30.json`, SHA-256
  `1b03683c34aba50cca5fbbc50ae44c8d0efda5f8e5a9a958649a9af8c028cfed`;
  its UTC progress log and `day5_labels_all30_root_audit.json`.
- `day5_calibration_all30.json`, SHA-256
  `20c188adeaf77d07a37d0ca38ab47d03191ae856e55ca3b0ee8ebc96d39300ed`;
  per-row predictions/decisions, separate strategy outcomes, fold audits,
  feature/recipe/source hashes, and empty successful stderr log.
- Ignored dawn checkpoint SHA-256
  `22007df444c84366d823eaefa1bc02de4ea0b219c722898b3dcc15f0b08506cd`;
  day6 checkpoint
  `47120681b57363b1d41439eaa85bf9ce1f57f868ed28d4dccc47eb01884dfd4e`.

Runner SHA-256 is
`45d405c28a300d214948ada30331c53dbeca349780e5a45930f6733998262ffe`;
calibrator SHA-256 is
`f2a90d405be6d9fee646cfd815ea8cc6c6fa78e2cd75d24fefa08b4a2ed5539c`.
Neither completed job should be rerun. Production and submitted B retain MD5
`7fcf39485bae65ee84171957c5843814`. No upload or top-five result is established.
