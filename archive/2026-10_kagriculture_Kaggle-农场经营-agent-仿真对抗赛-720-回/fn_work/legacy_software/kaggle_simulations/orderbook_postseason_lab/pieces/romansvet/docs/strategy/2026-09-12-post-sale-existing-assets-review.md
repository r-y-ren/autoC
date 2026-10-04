# Existing-asset post-sale hiring: review gap remains open

Two bounded independent Sol reviews agree that the existing B12 census does
not value all omitted work. Closed dawn crew/hire/feed knobs do not directly
test a hand funded after a realized sale and assigned to an already-owned
asset. This supports refining the descriptive census, not a performance pilot.
No new census, simulator evaluation or policy edit ran during this review.

Both reviews require current observed cash, the cached baseline plan, exact
hire-turn spawn after existing units act, an empty market row, preserved base
orders and next-day cash reserve, unreserved feed wheat, conflict-free routing,
and end-of-day shed capacity. Future baseline work may annotate acceleration
retrospectively; it cannot enter a runtime trigger. End-of-day automatic banking
removes the need to require a return-and-DROP route.

The first review proposes the shipped planner's admitted/covered and value
predicates, routes through WATER/HARVEST/COLLECT and FEED/CARE, and a modeled
value test. The blind second review instead emphasizes survival-critical work,
production capacity and exact next-dawn asset/yield/shed differences on the
already-fixed public B12 convenience corpus. It explicitly requires accounting
for the increased Fibonacci bill on every later planned hire. If k later hires
remain, inserting one hire increases the total day's bill by the final marginal
hire price, not necessarily only the immediate price.

These are not yet one agreed implementation contract. The first review's
suggested 20% board incidence, 1.5x modeled value/cost, and 300 modeled coins/game
are proposals, not adopted thresholds or measured outcomes. A modeled value
screen must not be confused with actual terminal coin gains. A zero-next-dawn
production test must also distinguish delayed CARE credit from no effect.
Resolve corpus/day scope, eligibility and value accounting before building.
Any future evaluation families remain separate; no pooling is allowed.

The existing public B12 sample includes ten historically loss-selected replays.
It can establish observed feasibility but not representative ladder incidence.
Preserve the original census and its limitations in
`2026-09-12-post-sale-hire-census.md`. The paired seed-room population audit is
the active experiment; this review supplies no reason to alter it.

## Reconciled fixture scope (15:57Z)

The reviewers reconciled directly and agree on the following first step.
Use the existing frozen public B12 corpus on days 1–9 only. Trigger at the
first realized positive sale after hour zero, then the earliest strictly later
empty market row. Preserve baseline actions, purchases, reserve and all later
hire costs. Compute spawn after existing units execute the hire turn; reserve
remaining baseline feed inventory. Select a deterministic conflict-free route
on existing assets, excluding any target with a later baseline state-changing
operation. Future replay work is an audit label only. The previously proposed
20%/1.5x/300 thresholds are withdrawn; positive feasibility never launches a
pilot automatically.

A minimal own-seat suffix execution fixture is required before claiming exact
feasibility. It must reproduce baseline transitions and then track the added
hand, tile mutations, wheat, carried products, hire costs and EOD banking/
overflow without overwriting simulated physical state with recorded outcomes.
Recorded baseline market settlements may be fixed only where the intervention
cannot affect them. No opponent policy needs to be modeled for an extra HIRE.

Root assigned bounded staging under S/hireasset, with no full census or pilot.
The initial development limit is twelve minutes and every CPU smoke is capped
at 180 seconds. No production, reference engine or replay modification.

Completeness caveat: one-time crop harvest can change the weed RNG sequence by
emptying a tile. Survival-rescue WATER/FEED can also change EOD topology by
preventing death/escape. These cases require actual RNG reconstruction for an
exact next-dawn comparison; otherwise report them UNVALUED. A zero result in
an easier topology-preserving subset cannot close the broader channel.
Zero fully funded routes or zero physical/pending-care benefit can close only
the complete scope actually verified. Baseline failure is a fixture failure,
not evidence against hiring. A ready fixture still needs independent review.

## Seeded suffix fixture validated (16:16Z)

`S/hireasset/suffix_fixture.py` now replays the original seed and both recorded
players through the locked reference engine. Baseline prefix and suffix must
match every physical observation before alternative claims. The PASS example
changes only the hire bill; the productive fixed example adds an eight-coin
hand on episode107766829 seat0 day5 and a seven-action route to WATER[1,2].
At EOD that wheat tile changes only yield1→2 and consecutive_unwatered1→0;
all other physical state in both seat views matches after exact declared
normalization. The later baseline BUY_LAND still settles in this fixed case.

Independent review accepted the plumbing and requested fixed-case, target-touch,
exact-field and provenance checks. They are in v5. Root's five focused tests
and full seeded replay passed (sessions8956/37845 exit0), reproducing v5's
receipt byte-for-byte, SHA f0983ea1b86229918f10e6d7248c96c199de2ae0424fd14b75e681b111955ae8.
The initial reviewer claim that later FEED itself must also reserve current
shed wheat was corrected against the engine: FEED consumes private worker
inventory; subtracting both prior PICKUP and FEED would double count.

The full census is still unrun. All purchase/reserve funding, broader operation
coverage and general route selection remain required. This fixed productive
example comes from the already-known priority WATER channel; it is a fixture,
not newly discovered aggregate hiring value. No terminal gain or pilot follows.
