# Initialization liveness repeatability — 2026-09-12

The unchanged ON initialization is not repeatable under the original runtime
settings. Root session51198 finished exit0 at16:28:58Z; this means the diagnostic
completed, not that reproducibility passed. GPU1 is idle afterward.

Raw outputs are int32 arrays of shape992×12. Root verified remote/local file
SHA256, each raw-array digest, and identical argument fingerprints across all
three calls. Against the first call, the cached call changes173 elements in32
rows (sum absolute21809 coins; maximum609), and the retraced call changes183
elements in34 rows (sum absolute22230; maximum609). This establishes repeated
execution instability in this process before any cache clear. It does not
identify whether the mechanism is a reduction, colliding scatter, or another
backend operation. No population rollout, optimizer update or checkpoint exists.

Artifacts: `S/seedrank/seedrank_liveness_repro_20260912/` with receipt, raw NPZ
and independent `root_audit.json`; adjacent log/exit/finished preserved. NPZ SHA
8cb41dbddb7daf670d2ab9083f39cec56765bf29c352c02b1b621d5f6762de38;
receipt SHA2ec47204d0b47a214a129d4384c71a319e09a6516b5475e5ad98931c77fb5218.
The original population reference failure remains invalid and unmodified.

## Prospective bounded runtime control, frozen before launch

After independent review, run the unchanged helper once on GPU1 with
`XLA_FLAGS=--xla_gpu_autotune_level=0 --xla_gpu_exclude_nondeterministic_ops=true`.
Use the same136 checked inputs, source/archive/B/window, highest precision,
CUDA backend and no preallocation; cap900 seconds with forced kill after10.
Output must be a new `artifacts/seedrank_liveness_deterministic_20260912` directory.

[OpenXLA determinism documentation](https://openxla.org/xla/determinism)
describes disabling live autotuning and excluding nondeterministic GPU
operations; unsupported deterministic operations may fail compilation. Both
flag names are present in the installed same-version jaxlib0.10.2 binary.
This is a runtime control, not a source fix or a claimed causal diagnosis.

Verify within-run raw equality and unchanged arguments, then compare argument,
source, helper, B and tape fingerprints against the preserved unflagged run.
Compilation failure, timeout or any mismatch supplies diagnostic evidence only;
no population run follows. Three exact calls establish repeatability only for
this initialization program in one process. They do not establish the larger
population shape, fresh-process/device identity or historical exact reference.
No automatic next run, training, score waiver, promotion or upload follows.

## Launch observation

Independent Sol reviewer next_lever accepts the flags and controls. The flags
are partly redundant but consistent. Root session13744 started once16:37:17Z,
GPU1 timeout1050470/probe1050471, cap900 pluskill10. Manifest136 exact; both GPUs
idle immediately before launch. Driver580.126.20, JAX/JAXLIB0.10.2. Persistent
cache environment variables are unset. Actual initialization is in progress.
See `S/seedrank/deterministic_launch_receipt.json` and remote adjacent
`.environment/.started/.log/.exit/.finished`; preserve them after terminal exit.

Reviewer source caveat: tape unit actions may contain duplicate scatter-set
indices, whereas the batched unit step assumes disjoint planner writes. Every
changed liveness row is in a tape group, none in the four ordinary archetypes.
This is a mechanism lead, not an observed causal attribution. Stable parallel
scatter results need not match the reference engine's sequential unit order.

## Terminal deterministic result

Root13744 finished exit0 at16:45:24Z. All three raw992×12 int32 arrays are
bitwise identical. Root verifies remote/local NPZ/receipt hashes, each raw
digest, all within-run argument hashes, and old/new argument, source, helper,
configuration, B and ordered tape fingerprints. Both GPUs are idle afterward.
This establishes same-process repeatability for this small program under these
flags. It does not establish sequential-engine fidelity or the population
shape; the original strict population reference remains failed.

The flagged original differs from the unflagged original in1161 elements/221
rows (maximum609coins), so a stable lowering is not a reproduction of the old
result. Changing two runtime controls together does not identify which backend
operation caused the difference. No population comparison or training follows.

Preserved local `S/seedrank/seedrank_liveness_deterministic_20260912/`:
NPZ SHA5bc13fc48ee6c985eb80e9bf062cadc8061c3988cc7e2c66ed5d56f42d865959;
receipt SHAab965f1a814655f7c5d1dfc8ab36723fcdbe5fa83e5dc09b0a8242b42f1594e0;
root_audit.json and adjacent terminal logs/environment/times. Original unflagged
root_group_audit independently confirms zero changed ordinary groups,27 cached
and29 retraced tape groups.

## Separate structural fidelity counterexample

Independent source reviews agree that archived tile operations compute every
unit predicate from the pre-turn state, whereas the locked engine processes
farmer then hands in order. Root42447 executed the reviewed one-turn fixture
under CPU cap60+kill10 and exited0. HARVEST/PASS control matches: inventories
[3,0], tile yield0. Duplicate HARVEST gives engine[3,0] versus simulator[3,3],
tile yield0 in both. This is a constructed mature ongoing TOMATO case.

Fixture source imports are bound to the exact archive modules; archive/engine
hashes are checked before execution and publication. Receipt SHA
4bccea7567d826bec6c4c51384fd4a41af906354ea90b4df3644e1828526921e at
`S/seedrank/tile_collision_fixture_20260912_root/receipt.json`; root log adjacent.
The first agent invocation failed on an absent display-only KIND_NAMES map,
without receipt; preserve tile_collision_fixture_first_failure.json. Corrected
explicit map and source-binding guard passed the root retry.

This does not refute earlier sampled planner-disjointness fixtures, establish
actual tape collisions or explain cached nondeterminism: identical HARVEST
writes can be stably wrong. Two independent bounded reviews are designing a
trace of actual frozen tape states before any source repair or new training.
