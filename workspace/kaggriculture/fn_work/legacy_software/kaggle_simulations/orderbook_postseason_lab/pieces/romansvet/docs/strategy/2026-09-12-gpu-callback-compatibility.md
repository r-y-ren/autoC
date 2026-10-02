# GPU callback compatibility before any new episode plan

The previous goal turn produced actionable failure evidence: the direct row58
calculation matches its target, but JAX0.10.2 debugcallback dispatch requires a
CPU backend excluded by JAX_PLATFORMS=cuda. Prior root57303 is terminal and
its execution plan has ended. This new first stage is a tiny plumbing probe,
not another episode or a scientific guard waiver.

One GPU1 process, cap60+kill10, freshoutput `artifacts/gpu_callback_probe_20260912`.
Initialize JAX_PLATFORMS=cuda,cpu with CUDA first; preserve CUDA_VISIBLE_DEVICES=1,
JAX/JAXLIB0.10.2, highest precision,x64false,preallocationfalse, and both existing
deterministicXLAflags. Verify sole defaultRTX3090, initialized localCPU and
callback dispatch onCPU. The installed xla_bridge initializes listed platforms
with descending priorities; defaultGPU must nevertheless be observed, not assumed.

The actual archived State NamedTuple passes through a tiny jit/vmap/scan with
three ordered callbacks. No apply_units, planner, evaluator, episode, population
or optimizer may execute. Verify all three complete payloads/steps/dtypes and
unmodified direct-versus-instrumented tiny mathematical outputs; explicitly
synchronize callback completion before checks. Preserve source/helper/runtime
identities, callback evidence and any failure. No automatic retry of this probe.

Only a successful reviewed root receipt permits considering a separately frozen
corrected-episode design. The small probe does not establish episode identity,
trace coverage or simulator fidelity. An episode under cuda,cpu would be a new
execution environment and must recompute direct as well as instrumented results
against the same original row58 target; no reuse of old direct checkpoint as
proof for the new environment. Both previous failures remain preserved.

Two independent reviews and actual runtime proof precede expensive episode work.
No production or submitted payload changes; no training or promotion follows.


## First tiny probe: exact callbacks, incorrect representation predicate

Root40549 ran17:54:38Z–17:54:40Z and exited1. All3callbacks and93saved rawarrays
match fixed expected payload hashes; direct/instrumented/fixedmath exact.
CPUdefaultdevice is observed inside allcallbacks, GPU remainsdefaultcompute.
The only failed predicate requires np.ndarray leaves; installedJAX instead
passes CPU-resident jax.Array after api.device_put. Preserve originalREFUSED
receipt b636de7a417f787b3f04af483ca09a4c547604ee5b4fe47fb291ad9bc6e902fb,
NPZbbb17f496bdfcbac049c51e70aedce70a9906c770b046b4601947c38c1b34a6f,
all7remote/localhashes and rootaudit under S/seedrank/gpu_callback_probe_20260912.
No episode executed. The oldreceipt is not rewritten asPASS.

A separately reviewed v2 corrects only the false representation assumption:
actualnp.ndarray host arrays or actualjax.Array with a nonempty device set all
platformcpu, plus callbackdefaultCPU and all prior byte/shape/order/math guards.
It records qualified types and exact device representations and refuses ducktyped
impostors. Freshoutputgpu_callback_probe_v2_20260912,cap60+kill10, one attempt.
Source/helper/environment proof and rawfailure evidence unchanged. This is a
plumbing verifier correction, not scientific target adjustment. Only actual
v2PASS and rootpayload/hash audit can satisfy the newepisode prerequisite.


## V2 actual GPU probe passed

Root9461 ran17:59:51Z–17:59:53Z exit0,cap60. All3ordered callbacks and93rawarrays
exact; every leaf CPU-resident, callbackdefaultCPU, defaultcompute soleRTX3090.
Direct/callback/fixedmath exact. Rawpayload byte-identicalv1, showing predicate
correction did not alter data. All7remote/localhashes and pre/post source/helper/
environment hashes verified. Receipt60d74c5996fa1ade03bbed20c57be24c451c52a80620c37d2aefc18920023a45;
rootaudit in S/seedrank/gpu_callback_probe_v2_20260912. Fourroot puretests pass.
This proves callbackplumbing only; no game/simulatorstep executed.
