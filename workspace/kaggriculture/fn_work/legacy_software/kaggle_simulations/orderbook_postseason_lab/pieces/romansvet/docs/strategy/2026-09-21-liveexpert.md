# LIVEEXPERT — exact-board greedy residual search

## Verdict

**KEEP the arm alive: 4/16 training losses flipped, clearing the kill rule of
3/16.**  On the 16 earliest losses in LIVE250 games 0--149, the greedy d10--19
expert gained **+1,893.9 mean margin** while reducing the taped opponent by
**1,442.1 coins/board** (sum Δtheirs **−23,073**).  This is an oracle ceiling
on pinned towns and fixed opponent actions, not a deployable policy result.

| boards | loss→win flips | mean margin gain | mean Δtheirs | commits | kill rule |
|---:|---:|---:|---:|---:|---|
| 16 | **4** | **+1,893.9** | **−1,442.1** | 49 | PASS (≥3 flips) |

The incumbent real-engine pass reproduced all 16 recorded purse pairs exactly.
The search evaluated 1,440 candidate continuations (16 boards × 10 dawns ×
9 rows: committed incumbent plus eight overrides) with eight CPU workers in
2,783 seconds, including baseline/final passes and replay-ledger extraction.

## Protocol

The boards are the first 16 rows with `live margin < 0` when
`S/band3/live250_selection.json` is restricted to chronological game indices
0--149: indices 14, 20, 36, 37, 40, 43, 46, 49, 52, 54, 57, 59, 65, 68, 70,
74.  Each uses its exact `info.seed`, original seat, pinned town, and taped
opponent.

At each dawn d10--19, candidate zero is the previously committed program with
`head_940` argmax continuation.  Eight alternatives replace one v1 categorical
action at that dawn.  A candidate is eligible only if its final opponent purse
is no greater than the board's original incumbent opponent purse.  Eligible
candidates rank by `(win, clip(margin, -20000, 20000))`; only a strict
improvement over candidate zero is committed.

No production or planner source is changed.  `live_expert_head.py` wraps the
normal numpy `head_940` path and replaces an action in a worker-local
`[day, slot]` table.  An empty table is the incumbent.  The real Kaggle engine
is used because the faster JAX tape simulator missed one LIVE250 board by two
coins per purse and therefore did not satisfy the exact-oracle contract.

## Slot map

`head_940` is the 18-slot v1 layout.  It has no independent `seed_buy` or
`ask_fill` slot (those belong to the unshipped 20-slot wide layout), so wheat
slot 0 is the shipped head's direct wheat/seed-demand lever and plant slots
0--4 are its fill levers.

| candidate | v1 slot | categorical value | decoded effect |
|---|---:|---:|---|
| hire | 8 | 4 | `d_hire = +2` |
| wheat ask | 0 | 8 | `d_plant[WHEAT] = +4` |
| strawberry fill | 3 | 8 | `d_plant[STRAWBERRY] = +4` |
| melon fill | 4 | 8 | `d_plant[MELON] = +4` |
| tomato fill | 2 | 8 | `d_plant[TOMATO] = +4` |
| carrot fill | 1 | 8 | `d_plant[CARROT] = +4` |
| strawberry sell row | 12 | 0 | `hold[STRAWBERRY] × 0` |
| melon sell row | 13 | 0 | `hold[MELON] × 0` |

## Board results

| game idx | episode | incumbent margin | final margin | gain | Δtheirs | flip |
|---:|---:|---:|---:|---:|---:|:---:|
| 14 | 110962225 | −926 | −631 | +295 | −246 |  |
| 20 | 110968944 | −1,166 | +1,431 | +2,597 | −433 | **yes** |
| 36 | 110983233 | −1,836 | +556 | +2,392 | −2,766 | **yes** |
| 37 | 110984336 | −2,550 | −1,349 | +1,201 | −295 |  |
| 40 | 110987627 | −1,578 | −534 | +1,044 | −569 |  |
| 43 | 110990897 | −1,949 | −816 | +1,133 | −51 |  |
| 46 | 110994188 | −8,648 | −7,921 | +727 | −19 |  |
| 49 | 110996375 | −1,481 | −1,025 | +456 | −381 |  |
| 52 | 110999752 | −3,119 | +1,712 | +4,831 | −1,892 | **yes** |
| 54 | 111000857 | −3,817 | −53 | +3,764 | −3,805 |  |
| 57 | 111003042 | −2,574 | +949 | +3,523 | −7,510 | **yes** |
| 59 | 111004672 | −1,697 | −581 | +1,116 | −1,410 |  |
| 65 | 111009509 | −4,747 | −4,200 | +547 | −537 |  |
| 68 | 111010654 | −1,081 | −564 | +517 | −1,175 |  |
| 70 | 111011836 | −10,226 | −6,036 | +4,190 | −1,614 |  |
| 74 | 111015168 | −2,056 | −87 | +1,969 | −370 |  |

## Mechanism

The expert chose plant volume, not direct sell timing: **48/49 commits were
`d_plant +4`**, one was `d_hire +2`, and neither sell-row candidate was ever
accepted.  Tomato led (12 commits), then melon 11, strawberry 9, wheat 8, and
carrot 8.  Commits concentrated early: 20/49 were on d10--12.

| accepted slot | commits | accepted days |
|---|---:|---|
| tomato +4 | 12 | d12--15, d17--19 |
| melon +4 | 11 | d10--16, d19 |
| strawberry +4 | 9 | d10--14, d16 |
| wheat +4 | 8 | d11--13, d19 |
| carrot +4 | 8 | d10--12, d15--16, d18 |
| hire +2 | 1 | d14 |
| sell holds ×0 | 0 | — |

The four flips used 13 overrides; 9 were on d10--12.  None used the direct
hire or sell controls.  Two flips raised ours while lowering theirs; two were
denial flips where both purses fell but the opponent fell farther.

| episode | committed mechanism | Δours | Δtheirs | final margin |
|---:|---|---:|---:|---:|
| 110968944 | d10 strawberry; d12/d18/d19 tomato; d15 melon | +2,164 | −433 | +1,431 |
| 110983233 | d10/d18 carrot; d11 wheat; d12 tomato | −374 | −2,766 | +556 |
| 110999752 | d10 carrot; d11/d12 strawberry | +2,939 | −1,892 | +1,712 |
| 111003042 | d10 strawberry | −3,987 | −7,510 | +949 |

Across all boards the final programs executed +23 hire actions, +45 plant
actions and +33 harvest actions relative to incumbent.  The fixed tape's
operation counts are unchanged; only its purse changes through the shared
market.  Per-board, per-day incumbent/final/delta rows for hires, plantings,
harvests and both purses are in `S/actionrl/live_expert_ledger.tsv`; committed
programs and final purses are in `S/actionrl/live_expert_results.jsonl`.

## Commands

```bash
cd /mnt/e/_work/kaggriculture3

JAX_PLATFORMS=cpu OMP_NUM_THREADS=8 \
  .venv/bin/python -m pytest -q tests/test_live_expert.py

JAX_PLATFORMS=cpu WORKERS=8 OMP_NUM_THREADS=8 \
  .venv/bin/python -u S/actionrl/live_expert.py \
  --backend engine --workers 8 --candidates 8 --day0 10 --day1 19
```

If wall time is constrained, `--candidates 4` retains hire, wheat,
strawberry, and melon in that priority order.  Do not substitute the JAX debug
backend for the result above: the real-engine baseline equality is part of the
oracle contract.

## Next decision

Arm 1 survives its falsifier, but its labels are strongly board-specific and
half of the flips include a lower own purse.  Distillation should therefore
train the categorical actions with incumbent-action rehearsal and be judged on
complete held-out greedy rollouts with the same Δtheirs constraint.  Oracle
success alone is not evidence to ship.
