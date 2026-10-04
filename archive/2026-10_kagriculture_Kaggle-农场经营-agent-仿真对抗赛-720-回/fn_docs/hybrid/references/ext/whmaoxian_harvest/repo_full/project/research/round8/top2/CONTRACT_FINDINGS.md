# DSM public-demonstration proxy: same-turn funding repair

## Checkpoint correction: official entry issue

The `7735d6...` source below is **not usable with the official file loader**.
Its final redefinition of `agent` retained an earlier dictionary insertion
position, so Kaggle `get_last_callable` selected `_r8_contract(obs, configuration,
action)` instead. The previous five diagnostic matches explicitly selected
`agent`, so they establish the behavior of that function, not submission loading.
The parent's subsequent 240-match league attempt failed with a missing `action`
argument; those failed matches are invalid policy evidence. The original source
and original diagnostic evidence are preserved.

Engineering-only replacement:
`experiments/round8_top2_dsm_contract_entry.py`, SHA-256
`23768116945ebd7500b2e2298616ff6dd974d27ce2c839643cc7d3e3d4cada57`.
It preserves the entire original source as an unchanged prefix, then adds the
uniquely named final function `round8_dsm_contract_agent`. The official loader now
selects that two-argument entry. Builder:
`build_round8_top2_contract_entry.py`; use `--check` for read-only verification.
Evidence: `contract_entry_build.json` and `contract_entry_loader_check.json`.

After the user resumed work, the replacement passed a complete official
file-path game on the already developed 733556107/seat-0/Fieldcraft fixture:
720 states, all 719 actions equal to the old explicitly selected `agent`, and
exactly reproduced final money 152686 versus 151317. The intervention triggered
once. First and maximum action duration was 0.239551 seconds, including source
compilation and embedded-data decompression. No stderr or policy fallback occurred.
Evidence: `contract_entry_full_validation.json`; validator:
`validate_round8_top2_contract_entry.py`.

This completes the necessary entry and behavioral-equivalence technical checks.
It is not a new independent strategy sample. The intended broader development
evaluation remains separate; no independent confirmation was inspected here.

This is an independent research branch, not the primary round 8 submission.
No independent confirmation results were read or used. The policy was frozen
before its five declared development matches. All results below are local final
money differences, not Kaggle ratings and not games against DSM's private agent.

## Proven cause

The three selected diagnostic losses contain two distinct worlds. Replaying the
saved actions against the official engine exposed a staffing shortfall that the
earlier `absent_worker_requests` statistic missed: Chassis `hand_align` had already
removed actions addressed to workers who were never hired.

In the Fieldcraft diagnostic at step 240, cash was 23. The agent sold six units of
fertilizer, hired eight workers, and bought eleven wheat. At step 241 it had cash
27 and requested two more hires, costing 34 and 55. Both failed. The farmer's
physical action deposited three milk into the shed on that same turn, but their
sale occupied market slot 8, after the two failed hires in slots 0 and 1. The turn
ended with cash 698 and still only eight workers. The original route required ten.

Those two absent workers' route segments watered the five strawberries and
harvested/replanted the melon identified in the loss audit. The original study
route's dawn contracts retain all five strawberries and replace the harvested
melon with wheat on day 11: these were not planned crop retirements.

The seed shortfall is a separate issue: at step 182 cash 84 cannot purchase the
scheduled wheat seed (10) and strawberry seed (100). The subsequent strawberry
plant request fails. This branch does not change seed quantities or purchasing
priorities; no claim is made that this separate shortfall is fully repaired.

Evidence: `seed_contract_audit.json`, produced by
`research/round8/audit_dsm_seed_contract.py` from saved actions. Replayed actions
are diagnostic reconstruction, not new policy-vs-opponent results.

## Frozen change

- Candidate: `experiments/round8_top2_dsm_contract.py`
- SHA-256: `7735d6f4293495a0942a21fb92f6ff6aaec339dc759375e1ecdbe6226c6f2c53`
- Base compact SHA-256: `1cc9732b115dcd1612b3ce848484c88701ac21071ed52f0c00a9571ffbcc0475`
- Reproducible builder: `build_round8_top2_contract.py`; `--check` verifies the
  frozen source without writing it.

When current cash is insufficient for the current action's fixed hire/seed
purchases, existing planned sales of goods already available after physical unit
actions move before the purchases. All existing order quantities and the relative
order of all nonsale orders remain unchanged. No sales are added and the order
count remains at most ten. No unit command, travel route, hire count, seed count,
route selection condition, or demonstration is changed.

The condition uses current visible cash, private inventory, positions, and the
agent's own planned orders. It contains no failing-world IDs, step-241 condition,
hidden seed access, unrevealed shop data, or evaluation outcome fingerprint.
The original compact source is an unchanged prefix and remains separately frozen.

## Five declared development matches

| World | Seat | Opponent | Original money difference | Repaired difference | Improvement |
|---|---:|---|---:|---:|---:|
| 733556107 | 0 | Fieldcraft | -37,463 | +1,369 | +38,832 |
| 733556107 | 0 | Master 2965 | -41,705 | -1,646 | +40,059 |
| 800459488 | 0 | Release v6 | -41,237 | +2,046 | +43,283 |
| 82003 | 1 | Release v7 | +6,597 | +6,597 | 0 |
| 82005 | 0 | Release v7 | +9,309 | +9,309 | 0 |

The first three matches each changed one market turn, successfully hiring both
previously missing workers on their original scheduled turn. Missing-worker
command-turns became zero, and all six previously identified crop deaths were
eliminated. The other two matches had no intervention and reproduced their prior
final rewards exactly. Each retained one unrelated carrot death.

All five games finished with 720 recorded states, no stderr, and zero Chassis
fallbacks. At every callback the audit asserted unchanged physical commands,
unchanged order multiset and unchanged nonsale order sequence. For every changed
turn, the official unit-action executor independently checked real post-action
shed stock; the Chassis projection matched it exactly, including the three milk
that funded the rescued hires. Source loading was preloaded in this screen, so
these five matches are not a new cold-start timing test.

Machine-readable evidence: `contract_build.json` and `contract_screen.json`.
Runner: `research_round8_top2_contract_probe.py`.

## Limits and next validation

This is five matches on four already developed worlds, selected partly because
they were known failures. The large improvement has a concrete causal explanation
but is not independent evidence of general strength. Advancing a sale can alter
market races or prices in other games. The guard is intentionally narrow: it does
not solve every sequential cash shortfall or add a missing hire after its planned
birth time. A larger diverse league should compare this branch separately from
the frozen primary candidate, without using independent confirmation to tune it.

Attribution and license for the compact base are in `compact_NOTICE.txt` and
`compact_LICENSE.txt`. The latter is byte-identical to the upstream Apache-2.0
license. The notice explicitly credits the 24 DSM public demonstration episodes
and preserves the inherited Chassis notice; the proxy is not DSM private source.
