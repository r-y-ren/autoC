# Prospective GPU qualification after a concrete monitor repair

The previous v2 protocol is closed REFUSED after its first arm:82 observed gaps
exceeded200ms, max0.248824s. Preserve its exact execution c79edd84 and all raw
results. No survivor is selected, no remaining arm is resumed, and no old arm
contributes to a new qualification. This is a new measurement after repairing
the observed subprocess-monitor overhead, not a reinterpretation of that result.

Bound the repair to S/unitorder/nvml_monitor.py and gpu_protocol_nvml.py. Keep
gpu_arm.py2a6b649d and gpu_protocol.pyd7ca66f5 byte-exact. The adapter replaces
only Monitor and strengthens the manifest binding for its own new inputs.
One persistent NVML session samples completed observations on50ms deadlines.
The installed nvml.h supplies the ctypes ABI; no installation or driver change.
Use nvmlDeviceGetMemoryInfo_v2 allocated memory, with reserved memory separately
recorded. The installed header defines v1 used as reserved plus allocated;
its453MiB idle reading would not match nvidia-smi's1MiB allocated reading. A
side-by-side query establishes v2 used983040bytes and reserved473759744bytes,
whose sum is exactly v1 used474742784bytes. This corrects API accounting, not
the64MiB idle threshold. Fail closed if the v2 API is missing or fails.
Preserve original UUID/name/driver/total-memory checks, complete process lists,
conservative rounded-up process memory, initial idle sample, final forced idle
sample and process-group cleanup. All observed gaps must still be positive and
<=200ms, including endpoints. Peak process memory must still be<=12000MiB.
A completed two-second monitor-only proof produced41samples/maxgap0.050109s;
this proves idle API operation, not loaded-arm compliance.
After the v2 accounting correction, one second of monitor-only observation
produced21samples/maxgap0.0500923s, all allocated used1MiB, reserved452MiB and
no compute processes. Both proofs remain preserved under their separate paths.

Use the unchanged four arms loop-1,unrolled-1,unrolled-2,loop-2 in fresh processes.
Unchanged workload per arm: actualCLI cold992, two cached992 calls, cold8192,
five warm8192 calls, explicit index arange(8192)%992. Retain all exact outputs,
source/runtime/configuration/state/RNG/B checks. Deterministic XLA flags and
disabled persistent compilation cache are unchanged. No generations, optimizer
updates or checkpoints. This remains ON evaluator qualification only.

Retain the exact frozen comparison: all four arms must pass; same-variant
warm-median ratio<=1.1; unrolled selected only when both paired medians improve
and geometric advantage>=5%, otherwise loop. The chosen pair's maximum cold
costs plus620 times its largest warm8192 time must be<=9000seconds. This is an
evaluator-only estimate on repeated rows, not actual-population throughput.

New remote bundle:
/home/user/stage_hr/S/unitorder/gpu_qualification_nvml_20260913_bundle.
New output canonical path:
/home/user/kagg3/artifacts/unitorder_gpu_nvml_20260913.
Wrapper uses the existing stage_hr/artifacts symlink and adjacent sidecars.
Python /home/user/kagg3/.venv/bin/python; GPU1 UUID
GPU-<uuid>. Refuse existing outputs. Bind the old
manifest's141inputs unchanged, plus the new monitor/adapter/launcher/tests/plan,
monitor-only proof, and original v2 refusal. Keep arm_input_paths unchanged.

Freeze and commit inputs after pure tests and independent Sol static review;
verify remote bundle hashes/canonical output path and idleGPU before launch.
One execution only:900seconds per arm,3660+kill10seconds outer. Stop the whole
protocol on any failure. No arm retry, threshold change or selecting survivors.
Observe the same process to terminal; save and independently audit raw results.

Success advances only to selected-variant OFF confirmation. Its minimal source
contract substitutes exact shipped B plan.py for archived plan.py, together with
the selected units.py overlay. No other source change is intended. Fresh bounded
training then needs its actual992 zero-generation initialization to match that
saved OFF confirmation before generation1; evaluate a resulting candidate on
separate families against B. No new simulator cases, closed Flow215 revival,
family pooling, production edits, promotion or upload. Goal remains top five.
