# Momentum feature isolated-stage integration

The isolated stage appends `mh (1,64)` and `ms (1,2)` after the existing
6,789-coordinate layout. A padded incumbent is therefore 6,855 coordinates;
the old prefix is unchanged and both new blocks are zero. Fresh initialization
also zeros these blocks. `live_mask` leaves them trainable, and the existing
named-block training mask can select `mh,ms` because it reads `policy.SHAPES`.

`PolicyObs.prev_mkt_inv` is an optional final field. `brain.market_momentum`
computes `(previous - current) / T` as float32 `[9,1]`; absent history produces
zero. The simulator freezes the previous dawn vector before both decisions.
Runtime tracks consecutive observed planner dawns separately for each physical
seat, rotates history once per dawn, and supplies zero on its first planner
call. The package and evaluator opt into the fourth macro argument; legacy
three-argument callers retain their existing interface.

`policy.forward` accepts optional `momentum` last. Legacy direct callers skip
the new arithmetic. `brain.decide` always supplies it, with zero for legacy or
day-0 observations. With `mh/ms` zero, both additions are exact zeros and the
verified outputs match the legacy call byte for byte on the NumPy fixture.

Completed checks cover structural layout, history cadence, a nonzero signal,
and zero-weight compatibility on 120 recorded dawn states. All 12 macro fields
and six complete plan arrays match B exactly on NumPy, JAX CPU, and local CUDA.
All six saved output archives have SHA256
`d15043f051b7fdd7e46b0ce08af538f377cfa4e6515615b05890fa37d216a4b9`.
The CUDA check finished at 10:47:19Z with exit 0. Packaging also preserved all
1,440 recorded actions and one 720-frame engine game per archive, apart from
the elapsed-overage-time observation field. These are compatibility checks,
not evidence of stronger play.

This experiment is OFF only. Opening splice bypasses planner calls differently
from simulator tape overrides, so opening-ON history equivalence is unproven.

This is interface and prefix-compatibility plumbing. The saved predictor result
motivates testing the feature but does not establish a policy or score gain.
