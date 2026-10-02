# Shipped/OFF confirmation and guarded fresh training

This is a prospective source and launch contract. It becomes actionable only
after the reviewed GPU qualification selects one unit-order implementation.
It authorizes neither that qualification nor training by itself.

## One exact OFF source tree

Start from `S/flow215/remote_source_20260912T1202.tar`, SHA-256
`520619b2ab7c7395ffcd214e27b0d3b41c2b0f1a10e6394129fb7d2b20264169`.
Apply exactly two replacements:

1. Replace `src/kagg3/core/plan.py`
   (`8044a3c6c8fb4fb9ccb0392aa1d5ed3f0ec8703b9768987aabf38a734b026a90`) with
   `kagg3/core/plan.py`
   (`19ad28167cb35faa7956ecb0864e293b644023e5aa3d33811842e3f2130a9b26`)
   read byte-for-byte from `submission/submission_flow193_g100_hr.tar.gz`
   (`ebad35c6d8eb4da4affb5ca5c075e350680219f4383e640e5392f4a3d312e050`). This is the
   shipped OFF planner: `SEED_ROOM_PURSE_ON` and `_seed_want` are absent, while
   `OPEN_PUMP_ON`, `TAIL_FILL_ON`, `BANK_BEFORE_LOT_ON`, and `HIRE_ROW_ON` are
   literal `True`. Do not add, set, or monkeypatch an ON flag.
2. Replace `src/kagg3/sim/units.py` with the implementation selected by the
   completed GPU qualification. For loop, this is reviewed
   `S/unitorder/units.py`
   (`b5aeeb2ca2563f8af64c87ea0a811f852776c4153abd0d6b111419b7a99f1e07`)
   unchanged. For unrolled, make only the
   already reviewed alias substitution from `apply_units_loop` to
   `apply_units_unrolled`, then freeze its resulting hash before either
   process.

`S/unitorder/shipped_source_contract_20260913.json` binds the packaged planner,
the 16 other byte-identical shared `kagg3` modules, the unchanged submitted
entrypoint and B theta, and the external plan exports. A staging helper must
rehash every archive member and prove that the two paths above are the only
source differences. Confirmation and training use separate private
extractions of this same source manifest.

## Selected-variant OFF confirmation

Use one fresh process and the actual archived Trainer CLI initialization. Keep
the 120 ordered w00 tapes, B, seed 309, pop 4096, 124 episodes, sigma 0.01,
1,191/6,789 mask, SGD, chunk 8,192, deterministic XLA settings and all other
Flow215 settings fixed. Give this confirmation a fresh run name and `gens=1`.
Before either process, derive and freeze one executable config baseline by the
reviewed `gpu_arm.expected_driver_config` rule: start from
`config_w00_20260912.json`, substitute the pinned canonical absolute B path for
`init_theta`, and substitute the ordered 120 canonical absolute tape paths for
`tape_actions`. Both private source trees must refer to those same external B
and tape files; extraction-local spellings are forbidden.

Intercept the first `_probe_archetypes` call exactly as the reviewed GPU arm
does. Capture its seven positional `_eval` inputs, `flow=None`, `tape_ctl`, and
the synchronized `int32[992,12]` output. Preserve raw inputs and output before
later checks. Apply the selected arm's existing within-process gates: two
cached 992 calls, the explicit modulo expansion to 8,192, one cold and five
warm 8,192 calls, exact repeats/index mapping, unchanged Trainer state, source
and runtime hashes, memory bound and timing projection. Stop before the first
generation; perform no perturbation, ranking, gradient, optimizer update or
checkpoint write.

The cold callback occurs inside `Trainer.__init__`; the archived CLI installs B
only after that constructor returns. Therefore the callback checks the random
initial state and evaluator call but must not require B. Require B at the
stopped first-generation boundary, after `install_init_theta` has replaced
`theta`, `best_abs_theta`, and `pool[0]`.

This is the selected implementation's required OFF confirmation. It does not
measure relative OFF speed or reopen implementation selection. A mismatch or
timeout is a refusal, with no alternate implementation or automatic retry.

## Training boundary guard

Only a passing OFF confirmation can name the expected initialization receipt
and raw 992 artifact for training. Start one new process from a second exact
extraction of the same selected OFF source manifest. Use the same physical GPU,
runtime and deterministic environment. Invoke the same archived CLI with the
same argument spelling and paths, changing only the fresh run name and
`gens=10`.

Before `runpy` enters the CLI, wrap `Trainer._probe_archetypes`. Around its
first `_eval` call:

- require the exact seven-input schema and hashes from the OFF confirmation;
- synchronize and require the complete `int32[992,12]` output byte-exact to
  the saved OFF output;
- require no mutation of theta, optimizer state, JAX key, host RNG, counters,
  pool/record arrays or slot-carry credit; and
- atomically preserve the training process's own raw inputs, output, source
  hashes and refusal-capable receipt before returning to the CLI.

The wrapper must then restore `_probe_archetypes`. Wrap the first
`Trainer.generation` entry as a final boundary: require exactly one successful
initialization probe, the saved cross-process identity, B installed exactly,
generation/Adam counters still zero, identity with the confirmation's stopped
post-B Trainer state, no checkpoint artifacts, and unchanged source/config
hashes. Restore the real method and call it only after all checks pass. Any
exception exits before generation 1, so no optimizer work can precede the
identity decision.

Compare the confirmation and training `config.json` objects in full after
normalizing only `run` and `gens`. Confirmation uses its fresh name and one;
training uses its fresh name and ten. Init theta and all 120 tape paths must use
the same spelling in both commands, so no path normalization or other config
exception is permitted. Each config must equal the frozen executable baseline
after only those two fields are normalized. The original JSON remains the
recipe source; the explicit B/tape substitutions above are part of the single
frozen executable baseline rather than extra comparison exceptions.

Run the fresh ten-generation process under a proposed outer
`timeout -k 10 10800`. Use a new output directory, immutable manifest, durable
start/finish/exit sidecars, pre/post input hashes and the normal idle-GPU and
process cleanup guards. Preserve a refusal or timeout without continuing or
resuming it. This is a fresh ten-generation trajectory from B; it is not
Flow215 w01 and does not inherit a failed population, checkpoint, optimizer or
rotation state.

Passing the boundary proves that fresh training began from the exact selected
shipped/OFF evaluator initialization. It does not establish engine fidelity,
policy improvement, a promotion result, or that the projected evaluator cost
will equal complete generation wall time.
