# Four-arm GPU qualification: fixed execution plan

The exact tape gate completed in root17719 with helper/root/independent saved
PASS (execution4570f980). Previous goal turn is progress. Implement the reviewed
[GPU design](2026-09-12-unit-order-gpu-design.md) without new correctness games,
policy ranking or training. Topfive remains unachieved.

Use a fresh bundle rooted at
/home/user/stage_hr/S/unitorder/gpu_qualification_20260913_bundle.
The bundle holds exact relative source/input copies. No production source or
old output is changed. Remote Python is /home/user/kagg3/.venv/bin/python.
GPU1 is UUID GPU-<uuid>, RTX3090,24576MiB,
driver580.126.20. Read-only inspection at about21:12Z showed both GPUs idle
with1MiB used; readiness must be rechecked immediately before the run.

The helper gpu_arm.py uses the actual frozen CLI initialization via
_probe_archetypes, with no generations/updates/checkpoints. Its131 source/input
paths include the reviewed overlay, archive, pinned probe/T helpers, config,
B theta, fixed capture/liveness/window identities and120 ordered tapes.
The root manifest additionally binds gpu_protocol.py, launch_gpu_protocol.sh,
this plan, reviewed design and completed tape execution/receipt. Its exact
input map, selected UUID, execution root and output root are immutable.
Private extraction excludes bytecode. Only units.py changes, with the chosen
loop/unrolled alias; imported module paths and hashes are recorded and audited.

One protocol runs loop-1,unrolled-1,unrolled-2,loop-2, each in a fresh process.
For each arm, capture synchronized cold992 plus two cached992 outputs, then
cold8192 and five warm8192 outputs. Expand only the explicit seven batched
leaves with arange(8192)%992, keep price tables shared and flow absent.
Materialize inputs before timing. Require all12 columns exact within each
shape, across processes/variants and under the index mapping. Hash and compare
full trainer state, typed key, RNG and slot credit before/after calls.
Every completed raw output is saved before subsequent assertions.

Use CUDA only, highest precision, x64false, preallocationfalse, disabled
persistent compilation cache and deterministic XLA flags:
--xla_gpu_autotune_level=0 --xla_gpu_exclude_nondeterministic_ops=true.
The ON workload is performance qualification only. Fresh training/judging
must use the declared shipped OFF contract after the separate confirmation.

The outer process samples nvidia-smi XML every100ms, requires measured gaps
<=200ms, no competing compute PID and peak process memory<=12000MiB. Its first
sample must show an idle GPU with<=64MiB used; a forced post-child sample must
show no compute process and the child process group must be gone. A short
read-only NVML sampling preflight may check the monitor before launch; it does
not execute JAX, compile an evaluator or run an arm.

launch_gpu_protocol.sh fixes the fresh output root
/home/user/stage_hr/artifacts/unitorder_gpu_20260913 with adjacent .started,
.log,.exit,.finished sidecars. Each arm uses timeout-k10/900; the external
protocol cap is3660+kill10. Refuse an existing output and stop the whole protocol
on any failure, timeout, missing evidence, source/runtime mismatch, changed
outputs/state, memory excess or monitor failure. No retries or selecting a
surviving arm. Persist refusal and final input-hash status even when no arm
receipt survives a kill; the shell sidecars preserve the external timeout exit.

Apply the exact replicated median/noise and geometric advantage rule in the
design. Use maximum warm time for the evaluator-only620-call projection and
9000second ceiling. This repeated chunk is not a real population benchmark.
Training needs its own fixed run/budget and exact OFF initialization match;
no failed historical population result is waived.

Before launch: pure helper snapshot/mutation and outer decision/failure tests,
independent Sol static review, commit exact source/plan/manifest, transfer and
verify every bundle hash, and recheck actual GPU availability. Observe the same
remote process/session to terminal status. Then retrieve all raw artifacts and
independently audit saved evidence. No pooling, promotion or upload is authorized
by this performance result.
