# GPU qualification v2: refused on monitor cadence

The four-arm protocol stopped after loop-1. Root SSH session98842 is terminal,
exit1; do not poll it as live, resume its remaining arms, or select its survivor.
Started2026-09-12T21:43:20.279939Z, finished21:51:13.440954Z, elapsed473.161031s.
The helper completed exit0/PASS, but the unchanged outer audit rejects82 of3790
monitor gaps exceeding200ms. Maximum gap0.2488242139806971s;3791 samples.
Independent saved-only Sol audit reproduced the exact assertion. No arm rerun.

All checks preceding that assertion pass:131 arm inputs against141 bound files,
archive/overlay/imported-source identity, actual normalized CLI configuration,
runtime,32-field cold and steady trainer-state invariance including key/RNG/slot,
B centre after initialization, zero generations/updates/checkpoints, all9 arrays
and their digests, within-shape equality, and8192-to992 indexed equality.
Downstream saved evidence independently confirms only helperPID1070516,
peak4962MiB, first/last idle1MiB, terminal sample0.148535s after child completion,
and the process group gone. Both GPUs were independently observed idle afterward.

Diagnostic timings only: cold992200.952172135s; CLI init203.613551453s;
cached9924.106138503/4.107870767s; cold8192195.515908481s; warm8192
10.829531393/10.847367376/10.861445961/10.864072227/10.861556559s.
These are one unqualified arm, not a replicated performance gate, implementation
selection, population measurement, or authorization for fresh training.

Downloaded unchanged evidence is under S/unitorder/gpu_qualification_20260913_v2:

| File | SHA256 |
| --- | --- |
| execution.json | c79edd84a2f9d01e068943ff23a7c0a43c68721300bbcbc0cd5cfd7824a007a4 |
| loop-1/receipt.json | 5721927e160c08225c6c5e5b7b3b6827cb388a83f0efd04c5709134ab618b4bb |
| loop-1/outputs.npz | a1379161d4586a342f3d88460a6201ade6a590b8598802c362eaef58392ef956 |
| loop-1.gpu.jsonl | 4f3c3faea1a03566c75ee6e7b425ded61c16e9c918da62d287a8b01a5dbe3a30 |
| loop-1.log | 03e81ae73dd406d432d0de9e2e82532d7a45cb8d9314e4f024684a2be28b3807 |

Wrapper .started/.finished/.exit/.log sidecars are preserved alongside them.
Frozen gpu_arm.py2a6b649d, gpu_protocol.pyd7ca66f5, launcheraba9ea6c and
manifest e696b0ee remain unchanged. The protocol rechecked all source inputs
after refusal. Original setup-only refusal remains separately preserved.

The observed blocker is subprocess-based memory sampling during GPU load.
A persistent direct NVML monitor is a targeted repair; a new prospective
protocol must be frozen/reviewed before renewed measurements. Keep the200ms,
12000MiB, exact-output, repeatability, selection and cost gates unchanged.
The original refused arm cannot contribute to that new protocol.

Goal remains top five: complete GPU qualification, exact shipped/OFF source
confirmation, then fresh bounded training and separate-family evaluation against
B. No new correctness games, old Flow215 restoration, pooling, production edits,
promotion or upload. Topfive remains unachieved.
