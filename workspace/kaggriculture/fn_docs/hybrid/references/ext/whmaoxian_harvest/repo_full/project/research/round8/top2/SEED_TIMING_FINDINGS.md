# Bounded residual seed-liquidity study

The frozen `237681...` policy source was not modified. This investigation uses
the three existing diagnostic action recordings, covering two developed worlds.
No independent confirmation was read, no complete new match or large league was
started, and no new agent candidate was created.

## What failed

All three recordings have the same day-7 cash problem. In the Fieldcraft case:

| Step | Cash before | Existing market orders | Cash after |
|---:|---:|---|---:|
| 175 | 277 | Sell 2 fertilizer | 450 |
| 179 | 350 | Sell 3 fertilizer | 605 |
| 180 | 605 | Sell 1 fertilizer; buy 1 sheep; buy 3 wheat | 94 |
| 181 | 94 | Buy 1 wheat seed | 84 |
| 182 | 84 | Buy 1 wheat seed; buy 1 strawberry seed | 74 |
| 183 | 74 | Buy 1 wheat seed | 64 |
| 186 | 64 | None; physical PLANT STRAWBERRY at (6,0) | 64 |

The strawberry seed costs 100. Changing the two seed orders' relative order at
182 cannot help: neither ordering provides 100 cash. Through the planting deadline
at 186 there is no further planned sale, no fertilizer/cash crop in the shed, and
no physical delivery that could fund it. Current-turn seed purchase would also be
too late at 186 because the official engine processes unit actions before market
orders. The other two cases differ by at most one coin in this local timeline.

Trace: `seed_timing_audit.json`; builder/auditor:
`research/round8/audit_dsm_seed_timing.py`.

## Small counterfactuals on saved actions

`research/round8/diagnose_dsm_seed_prepay.py` replays only through step 215. Rival
actions are fixed recordings, so these are local causal diagnostics, not matches
against responding agents or evidence of final profit.

1. **Advance only already-planned fertilizer sales to the earliest physical
   delivery during days 6 and 7**, keeping their same daily total. Each case
   gains only one coin by step 216; the strawberry still cannot be planted. This
   tested timing change is too small to cover the liquidity deficit.
2. **Move the existing strawberry seed purchase from 182 to 175**, suppressing
   its later duplicate and keeping every physical command unchanged. All three
   cases plant the strawberry at the original place and time. However, the cash
   diversion makes the wheat-product purchase at 180 fill only 2 of 3 units, and
   one later wheat-seed purchase fails. At step 193, worker 3's previously
   successful PICKUP WHEAT 1 fails. By step 216 there are no extra failed FEED
   operations, but cash is 56 lower and wheat seeds are 0 instead of 1.

The strawberry remains alive at step 216. It has not yet reached its 10-day first
yield age, so this is a successful establishment, not demonstrated additional
revenue. Later harvesting, resource replenishment, route selection and final bank
balance remain untested.

All details and individual unit-operation outcomes are saved in
`seed_prepay_counterfactual.json`. The initial diagnostic observer was attached
before `env.step`, where the framework's state copy prevented it observing unit
execution. It was corrected to attach within the official interpreter and now
asserts more than 100 observed operations per replay. The earlier informal
statement that no successful operation was lost is superseded by the actual
step-193 failed pickup above. Cash and seed-stock results were unaffected.

## Decision

Do **not** add a simple early-seed purchase to the frozen candidate. It resolves
one deadline by borrowing resources from the next part of the route. Unlike the
same-turn milk/hire repair, it does not preserve the already-funded physical
resource contract.

There is a plausible general next experiment: reserve seeds before their planting
deadline, track planned purchases against actual seed inventory, and repay any
resulting seed shortage before the next planting. Admission needs a conservative
cash and material check that preserves upcoming hires, animals and successful
feeding through the next dawn. It must also account for the strict router's seed
minimums; 0 rather than 1 wheat seed at a route boundary can reject a route switch.
These checks should use visible state and the selected own route, never a fixed
world ID or the diagnostic step numbers.

That is a separate policy change requiring bounded full-game comparisons. The
current evidence supports further research, but does not justify promoting a new
candidate or assuming a net gain. Existing-sale timing alone did not solve these
three cases.
