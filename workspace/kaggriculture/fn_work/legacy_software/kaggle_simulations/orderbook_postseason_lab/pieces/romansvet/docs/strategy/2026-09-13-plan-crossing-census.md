# Fixed-population complete-plan crossing census

The prospective no-game census completed once, exit 0, in 288.888 seconds.
It used the first 128 antithetic epsilon rows from the exact captured seed-309
generation-zero OFF population, with B as centre, sigma 0.01, and the frozen
1,191-coordinate mask. It built all six NumPy plan arrays for the twelve
states previously fixed by the planner timing benchmark. No game state was
advanced, no training update or coefficient search was performed, and no
outcome-based pass threshold was applied.

| replay seed | day | changed plans / 256 | macro changed, plan same | pair neither / one / both | plus vs minus differ | distinct member plans |
|---:|---:|---:|---:|---:|---:|---:|
| 1196709180 | 0 | 179 | 77 | 1 / 75 / 52 | 124 | 6 |
| 1196709180 | 5 | 111 | 145 | 58 / 29 / 41 | 70 | 5 |
| 1196709180 | 15 | 126 | 130 | 2 / 126 / 0 | 126 | 2 |
| 1196709180 | 25 | 82 | 174 | 58 / 58 / 12 | 70 | 7 |
| 2097576449 | 0 | 179 | 77 | 1 / 75 / 52 | 124 | 6 |
| 2097576449 | 5 | 111 | 145 | 58 / 29 / 41 | 70 | 5 |
| 2097576449 | 15 | 167 | 89 | 5 / 79 / 44 | 123 | 18 |
| 2097576449 | 25 | 102 | 154 | 32 / 90 / 6 | 96 | 3 |
| 2079139712 | 0 | 179 | 77 | 1 / 75 / 52 | 124 | 6 |
| 2079139712 | 5 | 153 | 103 | 37 / 29 / 62 | 91 | 9 |
| 2079139712 | 15 | 110 | 146 | 57 / 32 / 39 | 71 | 16 |
| 2079139712 | 25 | 90 | 166 | 45 / 76 / 7 | 83 | 23 |

Every row expresses more than one complete plan, and 82–179 of its 256
members differ from B. Every member changes at least one decoded macro field,
while 77–174 members per row are filtered back to B's complete plan. Thus the
narrow claim that this fixed population is almost wholly unable to cross an
stored-plan boundary is unsupported on these states. This does not show
that any expressed plan helps, explain seed 309's judge result, or justify a
sigma, decoder, mask, policy, or training change.

The twelve rows contain ten unique observations: the three day-0 states are
identical. Their identical results are reproducibility checks and are not
independent evidence. All rows remain separate; the ranges above summarize
their display and are not pooled estimates. Every row changes `mq` and `ua` in
some members. Other arrays are state dependent: `uq` changes in six rows,
`uop` in nine, and `mop`/`ma` in five. The machine-readable result preserves
per-array member and cell counts plus every distinct complete-plan hash.
The full census compares stored arrays. It does not establish that every
changed cell would alter a rendered or successfully executed action: unused
slots, future hands and later game states can affect that interpretation.

Independent Sol review reconstructed epsilon pair0 on all twelve cases (24
members), reproduced every centre, checked reconstructed hashes against each
saved histogram, and verified all saved arithmetic. Every changed spot member
also changed at least one rendered turn with both maximum hands and recorded
B hand counts. This spot check found no difference due solely to ignored
padding or arguments. The result stores histograms rather than member-indexed
hashes, so this establishes membership, not a saved per-index identity check.
Recorded B hand counts are not candidate-generated future states. The audit
is `sol_first_pair_audit.json` in the run directory, SHA-256
`0568e9747a5724a84b018000deda558715d29eb0fa078c469dc0a294b8cdc379`.

All twelve B centre plans exactly match the frozen timing benchmark. Fresh-view
and reverse-order centre builds also match, and the helper confirms input
immutability and zero epsilon outside the named mask. The copied 38-file source
tree matches the pinned eligibility map and tree hash. The source selection,
observation hashes, epsilon capture, RNG identity, mask, B, configuration, and
copy command are frozen in
`S/unitorder/plan_crossing_census_20260913/manifest.json`.

Artifacts:

- helper `S/unitorder/plan_crossing_census.py`, SHA-256
  `7057302422f137e5ab21d5d340972943cdc1695f4da6120319d2f8d77309176b`;
- manifest SHA-256
  `ec33ba2ae488ec7ff986ec9154f81ad549b93d0d5d4624cfd1d9daf53c886f1c`;
- result `S/unitorder/plan_crossing_census_20260913/result.json`, SHA-256
  `6c500cfa5831bd210ee3921b6195a097a0cf3d33c38c3014e605fd29f3c7034d`.
