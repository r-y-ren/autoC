# Post-sale hire: measured priority subset is small

A newly hired hand can act from the next turn and can work on existing assets.
This avoids the new-land displacement found in the seed-only hook. The hand
lasts only that day; the engine automatically deposits carried goods before
clearing hands at the day boundary. A return-and-DROP trip is not mandatory
for next-day inventory, although shed overflow and later sale still matter.

The fixed public-B12 convenience corpus was audited with
`S/postlot/post_sale_hire_census.py`. It contains ten historically loss-selected
replays, so this is descriptive mechanism evidence, not a representative ladder
sample. The helper excludes hour-zero sales and uses the first positive-net-cash
SELL after hour zero. This differs from the older census's first-SELL test;
their denominators must not be compared directly.

## Results and scope

On days 1–9, all 84 qualifying sale-days have raw cash for one additional hire
and an empty next market row. Within the explicitly defined priority subset,
12 single-tile routes exist on seven episode-days in seven episodes. All are
day-5 WHEAT watering opportunities, adding up to 12 immediate tile-yield units
at the observed states. On days 1–26, 127 of 277 qualifying sale-days have raw
hire feasibility; the subset contains 21 routes on eleven episode-days:
18 WATER and three HARVEST operations. The longer interval includes the early
one; these results must not be added.

The priority subset includes survival-due or one-time-crop bonus-window WATER,
ripe ongoing crops, saturated one-time crops, held animal product, and available
fertilizer collection. It excludes some legal work, including early harvest,
watering a fertilized ongoing crop solely for its production bonus, and
feed/care valuation. Its small count is not an upper bound on all labor value.

Raw omitted legal operations are therefore retained separately. On days 1–9,
individually route-feasible counts are WATER 564, HARVEST 678, FEED 40 and CARE
64. On days 1–26 they are WATER 1,324, HARVEST 981, FEED 173 and CARE 215.
These are individual possibilities across days, not simultaneously executable
allocations. A legal earlier harvest may only advance stock; watering may add
nothing; feeding/care needs production timing, wheat supply and capacity
accounting. No terminal value or performance gain follows from these counts.

No late-hire pilot is justified by the small immediate watering channel alone.
The broader existing-asset labor question remains unvalued. In particular, the
agent's preliminary feed-only scratch estimate is not a preserved, validated
result and is not used to close that question.

## Verification and limits

Root corrected the standalone import and reproduced the saved counts. The
replay alignment uses observation `base+h` before action row `base+h+1`, including
the final hour via the next-day observation. Coordinates are `(x,y)` and tiles
are indexed `[y][x]`. Two focused tests cover last-hour reservations on an
off-diagonal tile and a harvest route that only fits with automatic deposit.

Raw hire affordability does not preserve future purchase liabilities or B's
cash reserve. Future base actions are used only for this offline diagnostic;
they do not supply a runtime trigger. A new hand's exact spawn can also change
as existing units execute the hiring turn, so the reported route fit is an
observed-state estimate. Individual chains are not a conflict-free itinerary.
Immediate water increments are not final extra harvest or sale proceeds.

```bash
JAX_PLATFORMS=cpu .venv/bin/python -m pytest -q S/postlot/test_post_sale_hire_census.py
JAX_PLATFORMS=cpu timeout 180 .venv/bin/python S/postlot/post_sale_hire_census.py
```

The preserved root output is `S/postlot/post_sale_hire_census_root.json`, with
all thirteen metadata/replay SHA-256 identities and detailed rows. The earlier
agent output is retained separately as `S/postlot/post_sale_hire_census.json`.
No engine evaluation, policy edit, training run, or submission resulted.
