# Post-lot feasibility, corrected B census (2026-09-12)

Candidate B is identified by `submissionId=56161192` in `S/ladder2/ep_56161192.json`, then mapped to the matching seat in each cached `S/ep_<id>.json`. Replay row `t` stores the action with its resulting observation (`scripts/eval_vs_baselines.py:_replay_metrics`), so its delta is observation `t-1 -> t`.

Across the first 12 matched B replays on days 1–6:

| B-only necessary condition | result |
|---|---:|
| day-seats with a first SELL | 60 |
| positive net cash change on that SELL row | 46 / 60 |
| median net row cash change | +425 |
| later unused market row | 60 / 60 |
| positive net cash + free/weed tile + at least two later PASS slots | 20 / 60 |
| positive net cash + empty animal building + at least three PASS slots | 0 / 60 |

Cash change is net row cash, not gross sale proceeds. In episode 107940668, B is metadata seat 0; steps 49→50 move cash 112→614 while step 50 submits BUY wheat 3 and SELL fertilizer 6, and step 51 stays at 614. B's first sale can share its morning BUY row.

Actual tile schema was checked: usable undeveloped cells are JSON null or `kind: WEED`; locked cells are `LOCKED`; an empty COOP/PASTURE has no `animal` member. `S/postlot/census.py` uses those forms. The 20/60 intersection warrants examining a default-off plant bundle. The small zero animal count does not close that family.

`S/postlot/route_feasibility.py` is a conservative OFF-policy collector. Replay farms expose coordinates directly: episode 107940668 step 50 has farmer `[3,4]` and hands `[5,4]`, `[4,5]`, `[5,5]`. For each unit it finds the trailing all-PASS suffix, reads position and tiles immediately before that suffix, and uses BFS over non-LOCKED owned cells. This prevents combining a post-sale position with a suffix reached after intervening movement.

On the same 12 B replays it finds 19/60 sale days where positive net row cash, a reachable free/weed tile and one unit's untouched suffix fit movement plus PLANT (and DIG for weed). Seeds are global, so seed-only needs no pickup. It finds 0/60 fertilizer routes after including shed travel, PICKUP fertilizer, optional DIG, PLANT and FERTILIZE. These prove observed action-preserving capacity only, not conservative runtime funding or value. The small zero does not close fertilizer or animal mechanisms generally.

Recommendation: a default-off seed-only pilot is justified; fertilizer-plus-seed is not justified by this sample. Runtime funding must use a public-state conservative bound and current global seed count; replay future proceeds cannot enter the rule. The isolated simulator must schedule the added BUY turn as a full-market turn in `sim/rollout.py`. Tests must cover a foreign SELL row meeting the BUY row because fixed categories do not prevent that cross and `process_slot`'s floor-price handling is approximate.

Reproduction uses one CPU and no JAX:

```bash
python S/postlot/census.py 'S/ep_*.json' --episodes-index S/ladder2/ep_56161192.json --submission-id 56161192 --limit 12 --summary-only
python S/postlot/route_feasibility.py S/ep_107940668.json --episodes-index S/ladder2/ep_56161192.json --limit 1
```

`S/postlot/test_route_feasibility.py` verifies the real coordinate schema, a
synthetic movement followed by a true idle suffix, and a LOCKED-tile detour.

These are necessary-condition observations only. No family is pooled and no causal gain is claimed.

The twelve sampled episode IDs, in sorted cache order, are 107764944,
107766829, 107769126, 107769991, 107771992, 107777972, 107779009,
107779976, 107780983, 107781955, 107786955, and 107787963. Their embedded
episode IDs and unique B seat mappings were independently checked. Episode
107940668 is the separate timing/schema spot check, not one of these twelve.

The route counts remain an upper bound. They do not establish a seed purchase
shortfall, net crop value, a purchase row resolving before the new PLANT, or
absence of conflict with another unit's remaining tasks. A tile empty at the
idle suffix start may still be targeted by another unit later. Those checks
belong in the pilot before calling any extra planting productive or legal.
