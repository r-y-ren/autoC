# Prospective shipped/OFF ten-generation engine judge

**Parallel-run scope:** The user subsequently authorized using remoteGPU0
alongside the unchanged seed309/GPU1 run. Apply this seven-family protocol
separately to each eligible final centre, including the independently seeded
310 trajectory. Each requires its own audited training evidence, candidate
identity, fresh name/paths, eligibility receipt and prospective manifests.
Never combine centres or family results across trajectories. The shared CPU
judge lock still allows only one campaign at a time.

This is a frozen prospective plan for one descriptive, seven-family real-engine
comparison against candidate B. It is not an executable manifest and does not
authorize a game run. The candidate becomes eligible only after the currently
running fresh shipped/OFF training has completed and its full local saved audit
has passed. No candidate hash is invented or left blank in an executable
manifest: the manifest and launch wrapper must be created only after the real
final centre and persisted source tree are present locally and have concrete
hashes.

The result will be reported as seven separate family effects. It will not pool
families, apply the old Flow215 continuation rule, apply the older pooled
HR-slot rule, or automatically promote, package, upload, resume, or train
anything. Candidate B remains the comparison file. The top-five goal remains
unmet unless later ladder evidence establishes it.

## Eligibility and candidate identity

The prospective candidate is the final centre of the single guarded ten-native-
generation shipped/OFF run. Before any judge input is assembled, require all of
the following:

1. The selected shipped/OFF confirmation has outer verdict `PASS`, its saved
   audit independently reproduces that verdict, and its source/input/runtime
   identities match the frozen qualification result.
2. The training launcher and child have normal exit, the training receipt has
   verdict `PASS`, and an independent saved audit proves the initialization
   boundary, ten completed native generations, `t == adam_t == 10`, unchanged
   source/config/input hashes, and the expected canonical B and 120 ordered
   tapes.
3. Select the centre before any engine result is read. The candidate file is the
   training artifact `work/artifacts/unitorder_off_train/theta.npy`; require
   finite `float32[6789]` contents, array identity with `state.npz["theta"]`,
   and identity with the training receipt's `final_theta_identity`. Do not
   select among `theta`, `best_abs_theta`, `pool[0]`, a checkpoint, or any
   champion after seeing judge outcomes.
4. Pull and preserve the training output's exact `private_stage` beside the
   centre. The source archive's sole `scripts/` member is `scripts/train.py`,
   SHA-256
   `474a28ab8777d7058455be2bcc31e51f840062e5608325755410ccf8999f494e`;
   it does **not** contain `scripts/eval_vs_baselines.py`. The persisted stage
   cannot itself be `$WT` for the existing runners. Preserve it unchanged and
   construct the fresh local adapter described below.
5. Rehash the complete persisted stage against the passing training receipt.
   Its only intended archive-source replacements are the shipped/OFF planner
   `src/kagg3/core/plan.py`, SHA-256
   `19ad28167cb35faa7956ecb0864e293b644023e5aa3d33811842e3f2130a9b26`,
   and the selected loop `src/kagg3/sim/units.py`, SHA-256
   `b5aeeb2ca2563f8af64c87ea0a811f852776c4153abd0d6b111419b7a99f1e07`.
   The source construction contract is
   `S/unitorder/shipped_source_contract_20260913.json`, SHA-256
   `3db9c2bc85bf4c68677ca51a81bdaeec9e8b50bda942184d21c4b1345bfe7a2c`.

The OFF planner has no `SEED_ROOM_PURSE_ON` or `_seed_want` symbol. Its four
shipped switches are literal `True`. The engine command must nevertheless use
the same explicit switch spelling as the completed deterministic controls:

```text
OPEN_PUMP_ON=True,TAIL_FILL_ON=True,BANK_BEFORE_LOT_ON=True,HIRE_ROW_ON=True
```

Do not pass `SEED_ROOM_PURSE_ON=False`: `S/drainpin/on2b.py` asserts that every
named override exists, and absence of this symbol is part of the OFF source
contract. Do not use an unflagged or nondeterministic historical control. Freeze
the deterministic environment, exact imported source paths, switch values,
reference engine, and all input hashes before launch and recheck them after the
judge.

The local wrapper must set `JAX_PLATFORMS=cpu`,
`JAX_DEFAULT_MATMUL_PRECISION=highest`, `XLA_PYTHON_CLIENT_PREALLOCATE=false`
and `PYTHONDONTWRITEBYTECODE=1`. Require `XLA_FLAGS` absent and an initially
empty `KAGG3_*` namespace; each runner supplies only its pinned
`KAGG3_TOWN_SCHEDULE`. Record inherited hash-seed, thread and cache settings
without inventing new values. The GPU-only determinism flags are not a local
engine judge recipe. Pin the resolved interpreter and versions before launch:
the reviewed local environment is CPython3.11.15, NumPy2.4.6 and
kaggle-environments1.32.7. Require multiprocessing's start method `fork`.

Environment precedents are `S/flow215/run_seedroom_pilot.sh` and
`S/flow215/seedroom-engine-pilot.md` (8/8 OFF engine CSV identity on four old
source boards), plus `S/unitorder/launch_row58_tape_season.py` and its passing
`row58_tape_season_20260912/receipt.json` (CPU environment and fidelity only).
The old pilot's explicit seed-room False override must not be reused for this
shipped source, where the symbol is absent. Neither precedent proves strength
or full equivalence of the new candidate.

## Seven separate frozen families

All games use one seed per opponent and both seats. The order of every IDs file
is load-bearing for `--seed-per-opponent`.

| family | boards / rows | ordered IDs and seed base | town registry | candidate CSV | candidate-B baseline |
|---|---:|---|---|---|---|
| TOPB2 | 20 / 40 | `S/topb2/ids.txt`, SHA `95f775f86d871d12714845f8418045823c6ff13ab43db3473ed022bbd1fa6657`; `777001` | shared | `S/lossflip/${NAME}_topb2.csv` | `S/lossflip/flow193_g100_hr_topb2.csv`, SHA `1d5433f87b5cb2451b2d165dd12e86dcb13aa204800664a6e1ccc15976a4a134` |
| LIVEC-H30 | 30 / 60 | rows 43-72 of `S/livec/ids.txt`, full-file SHA `86c5e4900889525fa01f7f637536befcf4cc607717e1b5c53043d2141e6c5921`; `42777127` | shared | `S/lossflip/${NAME}_livech.csv` | combined keyed base `S/lossflip/flow193_g100_hr_livec43_102.csv`, SHA `a8a502011412a69e0d1d48643ebc92b616d30908af369dbe139e0c17cef52967` |
| LIVEC-H30B | 30 / 60 | rows 73-102 of the same IDs file; `72777217` | shared | `S/lossflip/${NAME}_livech2.csv` | same combined keyed base, SHA `a8a502011412a69e0d1d48643ebc92b616d30908af369dbe139e0c17cef52967` |
| LIVE62 | 62 / 124 | `S/live62/ids.txt`, SHA `7b5a522a845cfe24011e92ffc73acd330ee16ec63e89f1a43dacb0f7a3773bf6`; `777001` | shared | `S/lossflip/${NAME}_live62.csv` | `S/lossflip/flow193_g100_hr_live62.csv`, SHA `ac83911f0366292e8a020c345d19e3f5afea753ec0e4b7f777b666886fd0b1b0` |
| LOSS10 | 10 / 20 | `S/bloss/loss_ids.txt`, SHA `e5187c9f1e15cddcde6161afa34a26b16ee9baa2b8c896f91945e06b87767cce`; `300777901` | shared | `S/lossflip/${NAME}_loss10.csv` | `S/bloss/B.csv`, SHA `8500b80e735031e13fa33005e1002216a78807181dbd0c145761ad59ca21a447` |
| NEXT30 | 30 / 60 | `S/nextband/ids.txt`, SHA `7bfede7a94369d3b50d677723d4e8098dca5eb35af4644c2a5c6f000b208c5ae`; `200777601` | NEXT30 | `S/lossflip/nextband_${NAME}.csv` | `S/lossflip/nextband_B.csv`, SHA `6ddbff5f35f3fdf28c023d2dfa9f63354b91fcb5747d3dccbc6d0eab9db5c0f1` |
| NEXTHIGH | 30 / 60 | `S/nexthigh/ids.txt`, SHA `f131f8fe8d22806855ce612e091eb5b4fb0d6e50a40ae6bb1604abd45be4b7f8`; `600778801` | NEXTHIGH | `S/lossflip/nexthigh_${NAME}.csv` | `S/lossflip/nexthigh_B.csv`, SHA `98fc6d7c35a6a73865ce93167f29acc787fc2f230c1802535149745f7a524d43` |

The shared registry is `S/band2100p/town_schedules.json`, SHA-256
`dd3e118fc13fed9bbaadcb7e50b1ac2de54f80aec6a67bd88e0d675df1f2d3f1`.
NEXT30 uses `S/nextband/town_schedules.json`, SHA-256
`a3320b30ca696e15e4d2aea5cf9992659ea1dc9b9ecb66dfc2f81937b90487e0`.
NEXTHIGH uses `S/nexthigh/town_schedules.json`, whose current SHA-256 is the
same `dd3e118fc13fed9bbaadcb7e50b1ac2de54f80aec6a67bd88e0d675df1f2d3f1`.

The 120 unique tape IDs in `S/flow215/config_w00_20260912.json`, SHA-256
`80ec22d89a5c9a6db6d03559f4130c6e40f4f9abbdedaa15ad47315ecd19354f`,
have zero ID overlap separately with TOPB2, H30, H30B, LIVE62, LOSS10,
NEXT30, and NEXTHIGH. This is a source-list census, not permission to assume
the training inputs: eligibility still requires the completed training audit
to prove that its canonical 120-file external map is exactly the frozen
one. Record the seven intersections separately in the judge manifest.

The candidate-independent inventory is now saved in
`S/unitorder/judge_family_inventory_20260913.json`, SHA-256
`647b8b19754c7a653304787fea38f59c6ada62fe34f32d6a38779a62d3da9281`.
Sol and root independently verified all231 input hashes, all424 canonical row
keys, each family's B subset and each empty training-ID intersection. This
inventory has no candidate placeholders and is not an execution manifest.
Rehash it and its inputs when assembling the eventual candidate manifest.

## Immutable local runner contract

The runners are unchanged from the completed Flow215 judge:

| path | SHA-256 |
|---|---|
| `S/drainpin/on2b.py` | `a561785ce061b449a8c961f7b5c71a1652579e63050e836f6c64e665c9640df3` |
| `S/bank/paired.py` | `274465faf0d740a53f9b548e9e18b05c3309e1609450a1b8486cd8c95f09e9c4` |
| `S/topb2/run.sh` | `b62b83ba19bd7799d8130a151ad698f6be51aa9cc9414893f320f6bcb95a6e14` |
| `S/livec/run_holdout.sh` | `ce43fc452ac3701047fbd5f319f46f191451e3c855eaeccc963e34dd6f2cb969` |
| `S/livec/run_holdout2.sh` | `b6c5c107b2c40a0187b8ff12aac537d3e4b3b3c8827a2edd2d886a15a4227484` |
| `S/live62/run.sh` | `44b4c09a5ca935e65fadfb1ae3bad831fec9ff6ce6846ccc643b9aa8d5638345` |
| `S/bloss/run_leg.sh` | `3eb749cb870d5f4532506885fec00ec8df3011b3980a921e3fbe2cad1a906e59` |
| `S/nextband/run.sh` | `01efddf5e2169a8d779e2ad41d6c253f0b5bf532382cfc33bf549145ca8c9285` |
| `S/nexthigh/run.sh` | `817b88b0e42bf7848a4000e134e9f943d2a4ac8f5ee037b602918c1112f24464` |

The adapter's local evaluator closure is exactly these three files. Bind their
resolved paths and bytes before and after the campaign:

| path | SHA-256 | role |
|---|---|---|
| `scripts/eval_vs_baselines.py` | `b8b702811d71abdea055624215b36ed00d67b620f43223839f7a40c73c331735` | engine driver run by `on2b.py` |
| `scripts/plan_stats.py` | `006beb64cbcde0fd16d90cc490336ae5f4aa851c95002c53102e1e06c816847d` | direct sibling import by the evaluator; imports `DayStats` from candidate `src` |
| `scripts/town_inject.py` | `60de62cace303c9e8630e6a9db7aa3d77a7333082bb31caa5cbdb88e9ef1c04e` | worker-local import by `_play`; dynamically binds the installed reference engine |

Static inspection finds no other repository-local import from those three
files. Their `kagg3` imports must resolve through the adapter's candidate
`src`, while standard-library, NumPy, and `kaggle_environments` imports resolve
from the frozen Python environment. The runners' postprocessing closure must
also bind `S/live55/flips.py` SHA-256
`d0fa2ea0d9834c3b7bdd82685f4a3efef4d52251e44e20e399d50621a33ac6d9`,
`S/nextband/pair.py` SHA-256
`ff4a0254eca899bb4ed10673a3a890af5e121e1c384f2b1d2790a7bfec959176`,
and `S/nexthigh/pair.py` SHA-256
`ea86d2602f61099a612bee5de4a61ca4a56e6f3bb74624c419512b0102909f65`,
in addition to `S/bank/paired.py` above.

Also bind every resolved opponent `main.py`, every runner dependency, every
IDs file, all three registries, the six baseline CSV files, the complete
candidate stage manifest, the centre, and the Python environment. Bind
`vendor/engine.lock.json`, SHA-256
`dc0da85cd21c2fa475a97e9743fcf5fb40dc39103f195c611f7a594d7efc1999`,
and require its `source_sha256` plus the installed reference engine source to
equal `bc8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463f23bccee653e`
before and after execution.

These runners hard-code `/mnt/e/_work/kaggriculture3` for `R` and `S`. The
candidate centre and `private_stage` therefore return to this host and the
judge runs locally. This plan authorizes no remote judge or transfer.

## Exact prospective invocation

After eligibility and a no-active-judge/process preflight, create a reviewed
candidate-specific wrapper with a concrete absolute candidate stage, `TH`, a
fresh `NAME`, and a fully concrete immutable manifest. Refuse if any
corresponding CSV, family log, receipt, or result directory already exists.
Create a fresh adapter directory on the same local host using the established
seed-room pattern:

```bash
ADAPTER=$(mktemp -d /tmp/unitorder-off-judge.XXXXXX)
ln -s "$PRIVATE_STAGE/src" "$ADAPTER/src"
ln -s "/mnt/e/_work/kaggriculture3/scripts" "$ADAPTER/scripts"
WT=$ADAPTER
```

Before launch, require `readlink -f "$WT/src"` to equal the concrete persisted
candidate `private_stage/src` and `readlink -f "$WT/scripts"` to equal the
local repository `scripts` directory. Refuse an existing adapter, any other
entry, any copy of candidate source inside the adapter, or a changed symlink target.
Record the adapter path and both resolved targets; recheck the targets and all
bound target bytes after the campaign. The candidate `private_stage` remains
byte-for-byte unchanged. `on2b.py` prepends adapter `src`, and its printed
`plan:` path must resolve to the persisted candidate
`src/kagg3/core/plan.py`; candidate-side `kagg3` modules must likewise resolve
under that candidate `src`. The evaluator deliberately isolates packaged
opponent imports with `_vendored_imports`; their separate module images must
resolve within their own bound packages. The evaluator and its two sibling imports resolve
through the adapter `scripts` symlink to the three exact local files above.

Before games, a separate process using the exact adapter cwd/environment must
import the candidate plan/brain, agent runtime/parse/render/opening, evaluator,
plan_stats, town_inject and engine. Save resolved paths and hashes for all
then-loaded candidate modules, check them against the training source map,
check the OFF switches and engine identity, and record the fork start method.
Each actual family log must contain the correct resolved `plan:` path and all
four True override lines. Together with immutable paths/source and fork this
establishes the candidate import configuration and actual parent plan identity;
it does not claim direct observation of every worker's lazy imports.

Do not call
`S/autojudge/watch.sh --legs`: its width-based routing sends a 6,789-wide theta
to `.claude/worktrees/arms-next`, rather than the candidate's persisted OFF
stage, and its name rules choose family behavior.

The wrapper takes `/root/kagg3_judge.lock` exactly once and places the complete
seven-command body under one `timeout -k 10 7200`. The existing runner calls in
that body are exactly:

```bash
WORKERS=4 bash S/topb2/run.sh "$NAME" "$WT" "$TH" "$SW"
WORKERS=4 bash S/livec/run_holdout.sh "$NAME" "$WT" "$TH" "$SW"
WORKERS=4 bash S/livec/run_holdout2.sh "$NAME" "$WT" "$TH" "$SW"
WORKERS=4 bash S/live62/run.sh "$NAME" "$WT" "$TH" "$SW"
WORKERS=4 bash S/bloss/run_leg.sh "$NAME" "$WT" "$TH" "$SW"
WORKERS=4 bash S/nextband/run.sh "$NAME" "$WT" "$TH" "$SW"
WORKERS=4 bash S/nexthigh/run.sh "$NAME" "$WT" "$TH" "$SW"
```

Here `SW` is the exact four-switch string above. `NAME` must not use an old
Flow215 name and must be frozen before launch. The lock must not be nested;
the raw family runners do not acquire it themselves. The 7,200-second cap is
for this one complete campaign and permits no retry or substitute family.
Preserve start, finish, raw subprocess exit, timeout/refusal reason, process
cleanup, and pre/post hashes even on failure.

Several reused runners can mask an evaluator failure by appending `LEGFAILED`
or a summary and later returning exit zero. A shell exit code is therefore not
evidence of a completed family. Preserve every raw log and summary, but make
the independent post-run coverage audit authoritative.

## Required audit and result scope

For each family independently, the audit must require:

- the exact canonical candidate-B key set for that family, including episode,
  deterministic seed, tape seat, and both candidate seats;
- exactly the board and data-row counts in the table, no duplicates, and
  exactly two rows per board;
- finite, non-void own coins, opponent coins, and margins in every row;
- the expected opponent package, IDs slice, seed base, town schedule and
  candidate source for every game;
- unchanged candidate centre, source, runners, reference engine and complete
  input manifest after the run; and
- candidate/base CSV hashes plus per-family mean own-coin delta, opponent-coin
  delta, margin delta, mirrored-seat board standard error/t-statistic, and
  seat-game flip counts with their denominator labelled correctly.

H30 and H30B both pair against disjoint keyed subsets of the same combined B
CSV; the audit must select exact keys rather than compare row positions. A
family that is incomplete or invalid remains refused/unvalued and is not
silently omitted or combined with another family.

The final report contains seven rows and no aggregate row. It is descriptive
evidence about the preselected final centre versus B. It makes no automatic
promotion decision. A later decision rule, if any, must be reviewed and frozen
without consulting these results; the old Flow215 w01 budget guard and the
older pooled HR-slot rule do not govern this repaired fresh trajectory.

## Remaining implementation gaps

The saved-only helper is now implemented and reviewed:
`S/unitorder/judge_saved_audit.py`, SHA-256
`334e48c11a8896298114137f8c57dcdbbf8db51892cebd02111fb8d5c554cbce`.
Root31550 passed all11 focused tests, including reproducing every metric in the
archived Flow215 seven-family report without rerunning games. The helper fixes
each family's exact board/row counts, rejects invalid coverage/void rows, and
requires prospective binding of its own and paired.py source. The execution
manifest freezes all source/theta/tape/base hashes and canonical keys before
candidate CSVs exist. The saved audit manifest must repeat that contract and
add exactly the execution manifest and seven candidate CSV hashes. These two
manifests have different roles and must not be conflated. This helper does not
verify wrapper custody, source import resolution or runtime execution; those
remain the outer execution/audit's responsibility.

1. The current training execution has not yet produced an audited final centre
   or eligible persisted stage. Their hashes and paths must come from the real
   passing receipts; they must never be placeholders.
2. No candidate-specific local archive receipt, immutable judge manifest,
   fresh adapter or wrapper exists yet.
   Those artifacts require separate review after eligibility. The wrapper must
   prove the adapter resolves candidate imports to persisted `private_stage/src`
   and evaluator imports to the three pinned local scripts.
3. The prospective manifest must enumerate and hash the resolved opponent
   packages and all transitive runner dependencies, then prove they and the
   reference engine are unchanged after execution.
4. Fresh output-name absence, shared-lock availability, local process/memory
   availability, and the 7,200-second cleanup behavior still require a launch
   preflight. No engine run is owed if any guard fails.
5. This plan deliberately defines no promotion threshold. Completion yields
   seven family-specific measurements only; it cannot by itself establish a
   ladder gain, top-five strength, or upload eligibility.

## Reviewed assembly helper

`S/unitorder/assemble_judge.py` assembles only after two passing saved training
audits. Root and Sol reviewed the helper; the final related suite passed27tests.
It pins the existing inventory SHA, verifies final native theta/state/source,
creates a fresh adapter, records runtime eligibility with a180s bounded import
process, then freezes the exact execution manifest. It rechecks the original
proof tuple and every prospective input before success. It runs no games.

For the first eligible trajectory, after full evidence download and both saved
audits pass, use the repository Python with these explicit arguments:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python S/unitorder/assemble_judge.py \
  --candidate unitorder_off_seed309_g10 \
  --evidence-root S/unitorder/off_train_20260913 \
  --training-audit S/unitorder/off_train_20260913/root_saved_audit.json \
  --training-audit S/unitorder/off_train_20260913/sol_saved_audit.json \
  --output S/unitorder/judge_seed309_g10_20260913 \
  --python /mnt/e/_work/kaggriculture3/.venv/bin/python
```

Review the concrete contract, eligibility and manifest before running the
existing `judge_execution.py`. The second fixed candidate label is
`unitorder_off_seed310_g10`, with its own evidence and fresh assembly paths.
Do not create either campaign before its own final training audits pass.
