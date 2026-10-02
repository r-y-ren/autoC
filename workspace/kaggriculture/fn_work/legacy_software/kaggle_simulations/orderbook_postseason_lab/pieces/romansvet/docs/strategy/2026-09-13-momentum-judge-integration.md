# Shared judge integration

Development continues on `feature/market-momentum`. The existing `assemble_judge.py`, `judge_runtime_preflight.py`, `judge_execution.py`, and `judge_saved_audit.py` now handle both legacy and momentum candidates. The duplicate momentum judge implementations were removed; Git preserves their history. No separate benchmark was introduced.

The seven existing families retain their frozen 424 keys, baselines, opponent files, shell runners, CPU settings, lock, and separate reporting. No pooled promotion statistic is introduced. Changes to the family inventory's historical auditor and evaluator are explicit version transitions: their recorded hashes are checked, the census/data inputs remain exact, and each new campaign binds its actual executable sources.

`assemble_judge.py --candidate momentum_mhms_seed311` (or `momentum_mhms_seed312`) requires the explicit training evidence root and two distinct matching saved final-centre audits. It derives `train/work/artifacts/momentum_mhms_seed{seed}/theta.npy`; there is no arbitrary checkpoint or best-candidate input. The existing seed309/310 labels remain available.

Momentum preflight binds the training receipt, execution, audits, final state, generation-10 snapshot, exact float32 6,855-coordinate centre, unchanged 6,789-coordinate B prefix, and persisted 43-file source. Both source and evaluator scripts come from that stage, so daily market history reaches the candidate. Legacy campaigns recover the three matching evaluator scripts from Git revision `e8a49f2f0c0285b5f8d19914b6af5d638d7cfe99` into their output artifacts and verify their original hashes; they retain their own audited training source. Neither runtime depends on mutable canonical evaluator scripts.

Assembly runs the bounded import preflight and emits the established execution contract, manifest and eligibility receipt. It does not run games or select a model. The family runners require the exact workspace `.venv/bin/python` path. Frozen training manifests and running remote source snapshots remain unchanged.

On `feature/crop-mix-head` (2026-09-14), the same helpers accept exactly
`crop_mix_C_seed313` and `crop_mix_C_seed314`. Each requires the frozen campaign
manifest `c1d0ddcb324d01f2dc6be176344a58ae01fb7f2e910de7df7f7776806d4ee8da`
and stage manifest `aadd696c7c9e15f9429fb75736eb6ed812334feff13c03c92a998df74c6a9d85`.
The final float32 centre has7,020 coordinates; only the165 cm/cb coordinates
6855:7020 may differ from zero-padded B. Both the B prefix and66 momentum
coordinates remain exact. Native final state/generation10 equality, the173
campaign inputs, the exact43-file private stage and two byte-equal saved
audits remain required. The seven families,424 keys and B baselines are unchanged.

Validation used the four existing helper test modules:92 passed initially and
one legacy fixture rejected three pre-existing Python3.10 bytecode files in the
historical momentum stage. All43 declared source hashes were unchanged. Those
three caches were preserved outside the stage; the failing legacy test then
passed. The crop source-manifest binding also passed its focused final-byte
check. Cache custody is recorded in the crop campaign launch record. No game or
promotion evidence is implied by these helper tests.
