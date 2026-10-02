# Exact row58 trace:17collision groups, no duplicateHARVEST

Root26261 completed exit0 at18:13:19Z,480seconds after start, within900cap.
Under corrected cuda,cpu runtime, direct and instrumented12-int32 outputs both
exactly equal the original frozen target and both prior direct values. All719
pre-action states are captured in order. This validates this trace's identity;
it does not retroactively supply the internal CUDA-only trajectory.

Root independently verified all8remote/local file hashes, fullsource/input/tape
identity, all31serializedarray hashes,27State field shapes/dtypes,719step/day
sequence, action dimensions and the recomputed complete collision census.
Receipt d6afef93bc1fc57b1125d723440416b72a61e52dce1d295094c46ba254244a0e;
NPZ a806cd60e8869089ffd660d966f1fd173568850041ad9d36e6c7bb53176cad5d.
Evidence/rootaudit under S/seedrank/row58_trace_gpu_cpu_20260912. BothGPUidle,
timeout/python absent. Earlier timeout, CUDAcallback failure and tinyprobe type
refusal remain preserved; no source/evaluator or acceptance guard was changed.

The17groups are all onseat0. In unit-index order their operation pairs are:
FEED/CARE2; CARE/COLLECT_FERT5; CARE/CARE3; WATER/WATER1;
HARVEST/FEED1; FEED/HARVEST1; HARVEST/CARE1; WATER/HARVEST2;
WATER/FERTILIZE1. These are active requested operations on a shared prestate,
not proof of noncommuting effects or fullturn divergence.

No group has twoHARVEST requests. The prospectively selected firstduplicate
HARVEST fixture has no eligiblecase and remains unexecuted, with no whole-channel
closure. Mixed operation groups remain unvalued. Two independent reviews are
considering a new explicitly frozen CPU comparison of all17groups from this
same fixedtrace, retaining singleton and ordered-engine controls and excluding
fullturn/terminalcausality claims. No eventcomparison, repair, population,
optimizer/training/promotion orupload has run.
