# NumPy complete-day planner timing on twelve H30 B dawn states

Date: 2026-09-12. This is the lowest-cost prerequisite for the proposed
runtime choice among 2–4 complete day plans. It measures cost only. No engine
game, JAX rollout, GPU work, candidate policy, or outcome scoring was run.

## Frozen inputs and method

Before timing, the probe fixed twelve B dawn observations: controlled seat 0
in the first three H30 boards (`1196709180`, `2097576449`, `2079139712`) at
days 0, 5, 15 and 25. The observations come from
`S/postlot/pilot/replay_off_h30_cash/`. It uses `submission/theta.npy` (MD5
`7fcf39485bae65ee84171957c5843814`), actual `arms-next` source at `45f8217`,
and the shipped switches `OPEN_PUMP_ON`, `TAIL_FILL_ON`,
`BANK_BEFORE_LOT_ON`, and `HIRE_ROW_ON`.

`S/planselect/benchmark.py` reconstructs the packaged macro path: own
`parse_view`, public opponent view with empty private fields, `PolicyObs`, and
`brain.decide(np, theta, obs)`. The timed region contains only 1, 2, or 4
consecutive `plan.build_day(np, view, macro)` calls. Parsing, macro decode,
candidate generation, deduplication and scoring are outside it. Repeating the
same macro is valid only for this cost measurement; it says nothing about
candidate quality.

Each configuration has 120 interleaved samples (10 rounds over 12 fixed
observations), after two warmup calls per observation. The fixed rotation of
1/2/4 shares timing drift among configurations. Clock:
`time.perf_counter_ns`.

## Result

| complete `build_day` calls | median | p95 | max | samples |
|---:|---:|---:|---:|---:|
| 1 | 90.469 ms | 95.414 ms | 119.729 ms | 120 |
| 2 | 180.998 ms | 191.952 ms | 213.552 ms | 120 |
| 4 | 363.865 ms | 391.613 ms | 522.309 ms | 120 |

The total scales almost exactly linearly at the median: the cost per plan is
90.5, 90.5 and 91.0 ms for 1/2/4 calls. Four complete NumPy plans therefore add
about 273 ms at the median over today's one-plan path on this machine. The
timed region consumed 72.44 wall seconds. The 522 ms four-call maximum shows
the expected host-noise tail and is retained rather than trimmed.

All twelve observations passed three independent checks:

* four direct builds of the same input had identical six-array SHA-256;
* the direct one-call plan equalled the plan cached by a fresh normal
  `Runtime.act` at hour 0;
* the following hour-1 `Runtime.act` reused the same tuple object and its
  arrays remained identical.

This corrects the loose “microsecond-scale” design description for the complete
planner: on this machine a full `build_day` is about 90 ms. Later cached turns
remain cheap; the probe did not time them.

## Runtime context and limit of the reading

The measured host was WSL2/Linux on an AMD Ryzen 7 2700X, Python 3.11.15,
NumPy 2.4.6, with 12 logical CPUs in its affinity mask. `JAX_PLATFORMS=cpu` was
set, although this path imports no JAX. The planner call itself is ordinary
NumPy and was not pinned to a single core.

The installed local environment configuration says `actTimeout: 1` second and
defaults `remainingOverageTime` to 60 seconds. The frozen observations also
carry 60. `arms-next/GOAL.md` records the target runtime resources as 1.6 vCPU,
6.5 GiB RAM, 8 GiB disk and a submission no larger than 100 MiB. These are
quoted constraints, not a derived legal-time guarantee. This host is not the
competition runtime, four-plan p95 excludes decode and selection, and CPU
performance may differ. The result supports feasibility measurement: 2–4
plans are not obviously disqualified by local latency, but a real prototype
would still need end-to-end timing under the packaged agent path.

The machine-readable result preserves source-tree, theta, replay, local-config
and GOAL hashes in `docs/strategy/2026-09-12-numpy-plan-timing.json`.
Reproduce without starting the engine:

```bash
JAX_PLATFORMS=cpu timeout 180 .venv/bin/python \
  S/planselect/benchmark.py --rounds 10 --warmup 2 \
  --output docs/strategy/2026-09-12-numpy-plan-timing.json
```

No selector-improvement claim follows from this benchmark.
