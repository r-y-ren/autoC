# Measuring ES action-threshold reach before another training run

The cheapest remaining measurement is a **complete-plan crossing census** at
the existing Flow215 radius. It is a diagnostic of what the current
perturbations express, not an optimizer, policy change, candidate selector, or
reason to start another ten-generation run.

The archived trainer draws 2,048 float32 perturbations and evaluates
`theta + sigma*eps` followed by `theta - sigma*eps`
(`es/train.py:497-505,5125-5128`). Flow215 uses `sigma=0.01` and masks this to
1,191 live coordinates. The saved generation-zero OFF result already contains
the exact seed-309 `eps` array, so the census needs no new random draw. For a
fixed observation, `brain.decide` maps each member to integer `Macro` fields
(`core/brain.py:860`), and `plan.build_day` maps that macro to the six complete
action arrays (`core/plan.py:1-13,5771-5778`). Equality of those six arrays is
the executable threshold that matters.

Use the twelve H30 B dawns already frozen for the planner timing measurement:
the first three fixed captures, seat 0, days 0, 5, 15 and 25. They were chosen
before this question and are not selected by candidate judge outcomes. Select
the first 128 antithetic pairs by epsilon index before decoding. For each of
the 12 observations, build the center plan and the 256 `+/-` member plans, then
record separately by board and day:

- the fraction of members whose six-array plan differs from the center;
- the fraction of pairs where neither, one, or both signs cross a plan cell;
- the fraction where the two signs produce different plans from each other;
- macro-changed/plan-unchanged incidence, which directly measures filtering
  between integer decode and scheduling;
- changed-cell counts for `unit_op`, `unit_a`, `unit_q`, `mkt_op`, `mkt_a`,
  and `mkt_q`, plus distinct complete-plan hashes.

Keep the 12 rows visible. A single pooled percentage would hide whether all
crossings come from one season phase. The result can distinguish “the sampled
sigma rarely changes an executable plan” from “plans change readily, so lack
of search progress needs another explanation.” It cannot measure gradient
quality, candidate value, engine transfer, or whether a changed action is
helpful. No pass threshold should be invented after reading it.

This is narrower than earlier integer work and does not reopen it. The tie
census already showed widespread macro-cell changes; block-SNR found no old
block surviving multiplicity; per-block sigma entered the measured do-nothing
shell; dithering failed its held-out gradient gate; ISEARCH found no profitable
radius-1/2 move around B; and pinning the coarse integers did not reveal a
stable gradient (`2026-09-10-consensus.md:640-676`). Those results close the
corresponding training remedies. The proposed census only checks whether the
actual `sigma=0.01`, 1,191-coordinate population reaches the **final plan** on
these already-fixed states. A high crossing rate would add no permission to
retry those arms. A low rate would describe this population's local geometry,
not show that changing sigma or decode will pay.

## Cost and implementation boundary

The existing NumPy benchmark measured one `build_day` at 90.5 ms median on the
local Ryzen host. The proposed sample is 3,072 member-plans plus 12 centers, or
about 279 seconds of planner time before parsing and hashing. That makes a
plain CPU implementation the simplest first measurement. A full population on
the same 12 dawns would be 49,152 plans, roughly 74 minutes at that rate; all 90
dawns from the three replays would be about 9.3 hours and is unnecessary for
the first census.

An RTX 3070 implementation is possible but not yet demonstrated faster. JIT a
single-observation function containing `vmap(brain.decide)` and
`vmap(plan.build_day)`, process observations sequentially, and start with a
fixed 16-member chunk. Each complete raw plan is only 7,776 bytes
(`MAX_UNITS=17`; three `[17,24]` and three `[24,10]` int32 arrays), so a
16-member output is about 122 KiB. Planner intermediates and XLA compilation,
rather than retained outputs, are the memory risk. The local 8 GiB device was
already using about 1.4 GiB when assessed; the helper must bind its UUID,
record cold compile separately from warm execution, monitor peak memory, and
refuse rather than enlarge the chunk after seeing results. The prior
4,096-member macro-only decode does not establish that the much larger planner
trace fits. Given the five-minute CPU estimate, GPU compilation work is not a
prerequisite.

Any implementation must extract or copy the audited source into `/tmp` before
import, use `.venv/bin/python` with `PYTHONDONTWRITEBYTECODE=1`, pin the source,
B, epsilon, replay and observation hashes before computing, and verify NumPy
and JAX center plans byte-for-byte if the GPU path is used. It must never
import the live audited private stage, run the simulator or engine, inspect
judge outcomes, or alter the perturbations. The existing day-0 melon probe and
the final-theta 30-dawn comparison remain supporting evidence: macro thresholds
are crossed by many members, while a small learned center displacement changed
only one of 30 complete plans. Neither substitutes for this fixed-sigma
member-level plan census, and neither justifies another training run.
