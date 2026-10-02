# Row58 trace: one explicit compilation-budget follow-up

This is a new prospective execution plan following the preserved incomplete
300-second attempt, not a continuation of that terminal process. No acceptance
criterion, case, source, evaluator, captured input or numerical setting changes.
The purpose remains to determine whether a known structural simulator defect
occurs in an actual affected liveness episode before considering trainer repair.

Prior root39301 started17:23:52Z and exited124 at17:28:52Z. Remote filesystem
mtime places its exact direct checkpoint at17:27:42.805070097Z:230.805seconds
for setup/direct compilation/evaluation, leaving69.195seconds for independent
instrumented compilation. This supports a larger computational allowance;
it supplies no evidence that the instrumented output or collision gate will pass.
Old artifacts and directcheckpoint e38841aedd975f6198036ada089632130afcd961298248baf6165804e0d7c979 remain immutable.

Proposed once: GPU1, timeout900+kill10, fresh output
`artifacts/row58_trace_budget900_20260912`. Unchanged helper
065269ebeadfa14afef10b881060bc5603e4f01577578fb6d3d1d8ef99de9705;
unchanged141-input manifest762902182cc786d6e47a1b992624dc63e694bec1295c1d0b2850192a8f46fa1a.
Same exact archived source,120tape union,capturedrow58,policy switches,
JAX/JAXLIB0.10.2,RTX3090,highest/x64false and deterministic flags.
Fresh full remote hash check, idle GPU check, and independent review convergence
are prerequisites. Launcher differs only in fresh output and timeout900.

Both direct and instrumented12-int32 outputs must equal the original frozen
target and trace must cover719steps in exact order. Preserve failures, no target
padding or alternative case. This follow-up gets no further automatic retry.
If no complete trace arrives, stop and retain incomplete status. If either output
fails identity, retain unverified trace with no causal interpretation.

Only a valid trace can enable the separately reviewed conditional event fixture
in the original trace plan. All collision groups remain descriptive; first
supported duplicateHARVEST only for bounded sequential-engine/singleton controls,
othergroupsUNVALUED. No full repaired season, population, optimizer, training,
promotion or upload follows automatically. Original population reference failed
and remains invalid regardless of the outcome here.

Review status: two independent read-only Sol reviews agree; final launcher
review converged. Root confirms the only launcher changes are output path and
300-to-900 timeout; bash syntax passes. Full141 remote hashes matched17:33:59Z
and no compute process was present. Plan and launcher committed before launch.


Launched once17:35:22Z, root57303, timeout1059692/python1059693, GPU1.
Actual helper phase is direct archived evaluator. Observe the same process;
no second launch or change to helper while live. Adjacent log/times/exit and
output directory must be preserved after terminal completion.


## Terminal: instrumentation requires a CPU backend

Root57303 exited1 at17:43:12Z,470seconds after start, within900cap. Direct
12-int32 output is exact and directcheckpoint is byte-identical to the prior
attempt, SHAe38841aedd975f6198036ada089632130afcd961298248baf6165804e0d7c979.
Instrumented evaluation failed before recording any callback because
`jax.debug.callback` needs a local CPU device but the frozen environment sets
`JAX_PLATFORMS=cuda`. The installed JAX0.10.2 `_src/debugging.py` implementation
calls `local_devices(backend="cpu")` before placing callback arguments. The
actual error and later atexit token errors are preserved in the log/receipt.

This is an instrumentation failure, not a computed instrumented-target mismatch
or evidence for/against collisions. Receipt has valid_trace:false,
row_identity_verified:false, instrumented:null,trace_steps:0 and an empty trace
NPZ. Root rechecked all8remote/local file hashes, emptyNPZ, exact direct and
error text. PIDs1059692/1059693 absent; GPUs both1MiB.
ReceiptSHA6815b48d2eac6fd0bb56a60df5c4a56d1f90a5598e1239464f96c8373c326299;
NPZSHA8739c76e681f900923b900c9df0ef75cf421d39cabb54650c4b9ad19b6a76d85.
Evidence under `S/seedrank/row58_trace_budget900_20260912/` including root audit.

The prior CPU-only callback smoke did not test GPU callback dispatch under
CUDA-only platform initialization. Preserve that coverage limitation. This
execution plan ends here without another retry, case substitution or event
postprocess. Any future instrumentation design must first prove callback/runtime
compatibility at minimal cost and retain these failures; no production change,
source repair, population comparison, training or promotion follows.
