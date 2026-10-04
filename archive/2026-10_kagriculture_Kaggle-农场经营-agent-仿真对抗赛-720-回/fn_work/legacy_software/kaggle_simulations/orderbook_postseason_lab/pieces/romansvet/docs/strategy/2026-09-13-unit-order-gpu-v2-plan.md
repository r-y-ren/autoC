# GPU setup correction before the first performance arm

The initial launch of committed e1ee159 stopped at21:35:47Z with exit1 before
Monitor construction, JAX, any child arm or initial protocol receipt. The shell
sidecars are preserved in S/unitorder/gpu_setup_failure_20260913. Remote output
directory is empty. There are zero prior timing, output, memory or implementation
results; this setup refusal cannot count as a performance arm or select a winner.

Cause: the wrapper's /home/user/stage_hr/artifacts is a symlink to
/home/user/kagg3/artifacts. `out.resolve()` correctly found the canonical path,
but the frozen manifest incorrectly contained the logical path. Preserve the
original bundle, manifest2aeb385c and output/sidecars without edits or restart.

The reviewed correction makes two changes only: freeze the correct canonical
output root and put the path assertions after durable initial REFUSED receipt
publication, inside the failure-handling try. A pure symlink regression requires
zero monitor/child access and a final REFUSED receipt on wrong binding; a second
case proves a correct canonical binding reaches the monitor guard. No GPU code,
loop implementation, workload, threshold or selection rule changes.

Fresh v2 execution bundle:
/home/user/stage_hr/S/unitorder/gpu_qualification_20260913_v2_bundle.
Wrapper logical output and sidecar root:
/home/user/stage_hr/artifacts/unitorder_gpu_20260913_v2.
Manifest canonical output_root:
/home/user/kagg3/artifacts/unitorder_gpu_20260913_v2.
Manifest name: S/unitorder/gpu_manifest_20260913_v2.json.

All four performance arms remain unexecuted. Run the exact previously reviewed
loop-1,unrolled-1,unrolled-2,loop-2 protocol from the original GPU design/plan,
with900seconds per arm,3660+kill10 outer cap and all source/runtime/output/state,
memory, monitor and timing guards unchanged. This is a reviewed setup-only retry,
not a retry of an executed performance arm or a waiver of a failing measurement.
Any actual arm failure still terminates the entire qualification without retry.

Before this fresh launch, regenerate and commit all exact input hashes, verify
local pure tests and independent review, transfer into the fresh v2 bundle,
check every input and both logical-to-canonical output paths on the actual host,
and verify GPU idle immediately before the first arm. No NVML sampling run need
be repeated: original read-only preflight passed18 samples/max gap0.130seconds;
actual protocol still collects its own complete memory/process evidence.

Initial transfer auto-review rejection was resolved by read-only proof that this
is the training host named in the user-requested handoff and the private archive,
B, config, captures and all120 tapes already exist there with matching hashes.
The same transfer was then approved. No permission bypass occurred.

A qualified simulator enables the next OFF confirmation and fresh training;
it does not demonstrate a competitive gain. Topfive remains unachieved.
