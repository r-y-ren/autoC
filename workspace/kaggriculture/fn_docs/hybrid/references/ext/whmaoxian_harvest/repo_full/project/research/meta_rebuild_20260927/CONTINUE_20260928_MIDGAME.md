# Midgame continuation — research only; no approved release

User target remains a substantially stronger V10 with credible 2800 evidence.
No Kaggle submission was made and no release was replaced in this continuation.

## Confirmed execution
- Previous husbandry batch finished: 336 cases, zero invalid (arena completion log).
- New predictor repair renamed only appended `_PG_` symbols to `_K28_PRED_`.
- Builder: `build_predictor_fixed_20260928.py`; preserves old failed candidates/results.
- New `predictor_fixed_jobs.json` batch: 84 completed, zero invalid.
- New herd builder: `build_midgame_herd_20260928.py`.
- Three settings: Yarn-triggered sheep substitution, selective EV, no-milk gate.
- `midgame_herd_jobs.json` batch: 56 completed, zero invalid.
- Herd pilot uses known loss seed 1799657451, seven opponents and both seats.
- This seed is DEVELOPMENT, not a new heldout world.
- Both builders checked frozen R2 SHA256 b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4.

## Evidence and limitations
- R2 first-cow substitution allows only GOOSE; its default shop rule excludes Yarn.
- Replay 114242169: day10 own SHEEP=7 vs rival14; day15 own11 vs rival15.
- Observed R2 cow purchase requests at turns65,88,173,178; current pilot changes only first eligible request in144..191.
- Exact realized-revenue auditor file creation was blocked by platform safety classification.
- REPL result-statistics requests were also blocked; no bypass was attempted.
- Only batch completion/validity is confirmed, NOT victory counts or candidate promotion.
- Next: after permitted result inspection, check `_CS_REPORT` activation/placement and paired margins.
- Then consider earlier (post-first-shop) and repeated cow-batch substitutions, preserving species accounting and cash/worker feasibility.
- Existing final heldout views/worlds were not used. Do not package these candidates as a release.
