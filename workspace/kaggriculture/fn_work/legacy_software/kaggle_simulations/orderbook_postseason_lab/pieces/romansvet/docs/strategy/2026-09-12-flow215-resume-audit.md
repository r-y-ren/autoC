# flow215 changed-tape resume audit (2026-09-12)

## Verdict

A direct `--resume` with a changed `--tape-actions` list does **not rotate** the
pinned objective. `scripts/train.py:load_resume` replaces the freshly built
ladder with `state.npz`'s `archetypes`/`archetype_names`; then
`Trainer.reprobe_archetypes` only appends command-line tape names absent from
that restored ladder. Removed tapes survive. Repeated swaps monotonically grow
the ladder, episode count and absolute-probe shape.

Use `S/flow215/rotate_checkpoint.py` between windows. It writes a new resume
directory (never mutates the source), preserving theta, optimizer moments,
device PRNG key, host RNG state, generation/step, pool, sigma restart counters
and elapsed time. It removes the restored ladder, its names, slot-allocation
credit and signature, so `Trainer.__init__`'s new command-line ladder remains.
It explicitly retires the old objective's `best_abs`, `best_hold`, champion,
record theta, stall clock and replicate-rejection count. It copies no real-gate
sidecars or candidate files. `rotation.json` binds the output to the source
checkpoint SHA-256 and exact per-family ID lists.

Example (staging only):

```bash
JAX_PLATFORMS=cpu python S/flow215/rotate_checkpoint.py \
  artifacts/flow215_window00 artifacts/flow215_resume01 \
  S/flow215/window01_band_ids.txt
```

The next launcher must pass exactly those lists as `--tape-actions` and point
`--resume` at `artifacts/flow215_resume01`. Use a distinct `--run` output. The
tool deliberately does not construct a launcher or tapes.

The staged first segment is `S/flow215/launch_flow215_w00.sh`. It starts fresh
from B as run `flow215_w00`, uses exactly ROTBAND window 0's 120 tapes for ten
generations, and keeps NEXT30 held out. Its 124 episodes are 120 pinned tapes
plus four carried episodes. At 64 absolute pairs the unsplit probe is 15,872
rows, below the 21,760-row established ceiling. `S/flow215/window_ids.py`
requires all 120 IDs in the private registry and checksum manifest, verifies
every destination tape byte-for-byte, and checks the window against the full
exclusion set before the launcher creates its run directory.

Window 0 has no real-engine gate because ten generations are shorter than the
inherited 100-generation gate cadence. The auto-judge watcher therefore gets
no gate `RECORD` line. Evaluate the centre theta from the generation-10
`state.npz` checkpoint, keeping each evaluation family as a separate read;
neither `best_abs.npy` nor a combined family total is promotion evidence.

## State audit

- `_fit_layout` pads every parameter-indexed array, including theta, `m`, `v`,
  pool, champion, best theta and archetype thetas. A policy-layout extension is
  safe; a newer/longer checkpoint is refused. This is independent of tape
  rotation.
- `ladder_sig` covers names, weights, handicap, selection metric, tape score,
  flow ensemble and absolute-seed selector. Its reset path preserves theta,
  momentum and RNGs, but direct resume compares against the *restored old
  ladder*, so a replacement list can be invisible. Removing ladder arrays is
  necessary; resetting the signature alone is insufficient.
- Both JAX `key` and NumPy `rng_state` are restored. The transformer preserves
  them byte-for-byte, maintaining the perturbation and episode-draw streams.
- Objective-dependent cached state is `best_abs`, `best_hold`,
  `best_abs_theta`, `champion_score`/`champion`, `last_improve` and
  `replicate_rejects`. These are reset. `last_day_metrics`, absolute history and
  generation reports are memory/log state and are not checkpoint-restored.
- `slot_credit` is rung-indexed and is dropped. Starting allocation credit
  afresh costs at most one generation of carry fairness and avoids assigning an
  old rung's credit to a new tape.
- The optimizer pool is policy theta state, not rung state, and is preserved.
  `m` and `v` are preserved as requested; this continues SGD momentum (and is
  also correct if a checkpoint uses Adam). `adam_t` is preserved when present.
- Gate state lives in sidecar files and may refer to an in-flight nomination.
  The new directory contains only sanitized `state.npz` and `rotation.json`, so
  no pending verdict or old gate record is imported.

## Evidence

Commands run from `/mnt/e/_work/kaggriculture3`:

```text
JAX_PLATFORMS=cpu .venv/bin/python -m pytest -q S/flow215/test_rotate_checkpoint.py
... [100%]

python -m py_compile S/flow215/rotate_checkpoint.py S/flow215/test_rotate_checkpoint.py
exit 0
```

The tests include the real 5.5 MB `S/snr/flow211/state_g00020.npz` and call the
actual arms-next `scripts/train.py:load_resume` function. They prove exact
equality of theta, both moments, typed JAX key data, host RNG state and
counters; that the loader leaves the prebuilt three-rung replacement ladder at
exactly three rungs; absence of old ladder, names, signature and slot credit;
objective-record invalidation; and refusal of an ID shared by two evidence
families. The archived checkpoint's arrays are numeric or Unicode, and both the
transformer and loader read them with `allow_pickle=False`. Its 6,789-element
theta/m/v arrays match the current policy layout, so the resumed optimizer and
the current 1,191-gene training mask have compatible parameter dimensions.
The manifest keeps families separate; no pooled promotion statistic is computed
or recorded.

`best_hold=-inf` is the trainer's `NO_BEST` sentinel and round-trips through
NPZ as a scalar float64. `last_improve` is measured in `Trainer.t` units (stall
logic subtracts it from `self.t`), so setting it to carried `t`, rather than the
usually equal outer checkpoint `gen`, is deliberate. With `ladder_sig` absent,
`load_resume` records `ckpt_rungs=0`; its fallback reset would also retire a
nonempty new ladder. The transformer resets the records directly as well, so
correctness does not depend on that fallback or on selection metric defaults.

## Remaining hazards before any launch

The controller cannot prove that supplied IDs are absent from judge families,
that each `.npz` tape exists and verifies, or that launcher weights/episode and
absolute-probe bounds match the new window. A flow215 precheck must establish
those facts separately for every window. A crash while the old trainer still
writes its source directory is harmless to the new directory only if rotation
is run after a clean checkpoint; stop by verified PID first. This audit did not
launch training, contact the remote host, download tapes, or alter production
training code.
