# Flow215 training limitation: own-coin dominance on disputed directions

This ranks two general explanations for Flow215's failed transfer using source
and already-preserved data. No game, fit, policy change, or weight sweep was
run. The quantitative audit is reproducible with
`S/unitorder/flow215_objective_alignment.py` and reads the archived OFF
generation-0 population in `S/seedrank/seedrank_pair_20260912/off/result.npz`.

## 1. Highest priority: the update objective favors own coins on disputed directions

Flow215 does not optimize the tournament score directly. Its native advantage
is a separately rank-normalized blend of 60% weighted mean log own coins and
40% weighted mean sigmoid of margin divided by 3,000
(`src/kagg3/es/train.py:584-668`). The frozen config confirms
`abs_weight=0.6` and zero auxiliary shaping
(`S/flow215/config_w00_20260912.json:21-32`). It also sets
`select_metric="coins"`, which makes the optional in-simulator record selector
return `rep.coins` (`src/kagg3/es/train.py:5693-5740,5754-5770`). That selector
is not the choice or promotion rule for the current seed-309/310 runs: those
runs explicitly take the final native theta. The update blend remains relevant
to every generation that produces that final theta.

The actual generation-0 opponent mix was not a generic self-play batch. The
preserved receipt records one episode against each of 120 fixed tape opponents,
two against `rusher`, and two against `expander`; `rancher`, `patient_grower`,
the pool, and the centre each received zero. `tape_score="margin"`, so the
relative component in this audit really reads simulated opponent money rather
than replacing tape margins with own coins.

The episode counts are not the aggregation weights. Under `pinned_once`, each
of the 120 fixed tape episodes has weight 2, while the four residual
`rusher`/`expander` episodes have weight 1. Both component means therefore use
the same denominator, `120*2 + 4 = 244` (`src/kagg3/es/train.py:4686-4701`).

The two objective components disagree materially on that exact 4,096-member,
124-episode population:

| population diagnostic | result |
|---|---:|
| own-vs-relative candidate rank correlation | 0.270 |
| antithetic pairs preferring opposite signs | 855 / 2,048 (41.7%) |
| among conflicts, blended objective follows own / relative | **622 / 233** |
| gradient cosine: own vs relative | 0.208 |
| gradient cosine: blend vs own / relative | **0.926 / 0.561** |
| top-410 overlap: own vs relative | 69 / 410 |
| top-410 overlap: blend vs own / relative | 227 / 169 |

As a descriptive robustness criterion, stop calling the blend own-dominated if
it follows the relative sign at least as often on disputed pairs, or if its
gradient is at least as close to the relative gradient. This criterion was
written after the population results were inspected, so it is not a
predeclared test. Both conditions are false: the configured blend resolves
72.7% of disagreements in the own-coin direction and is substantially closer
to the own-coin gradient.

The later independent-family judge has the matching failure shape. Flow215 g10
increased own coins on TOPB2, H30B, LIVE62, NEXT30, and NEXTHIGH, but increased
the opponent purse more and lost margin on every family; H30 itself was own
-55, opponent +814, margin -869 (`2026-09-12-flow215-g10-judge.md:9-21`). The
population audit does not prove the objective caused those held-out changes,
but it shows the conflict was active in the exact training population rather
than merely possible in the formula.

Among the two explanations reviewed here, this is the stronger descriptive
risk because it acts in every update. The preference is partly expected from
the configured 0.6 own-coin weight; these diagnostics do not establish that
changing it would improve performance. It is not a proposal to sweep `abs_weight`: objective reweighting
has prior closed evidence, and one archived population cannot identify a
better coefficient. No objective branch or rerun follows from this result. If
a corrected-simulator no-update population is later produced for an
independently approved reason, freeze the same criterion before reading it and
apply this algebra to check whether the same conflict persists. Persistence
would support further diagnosis, not automatically reject the objective or
authorize a replacement: the separate engine results must establish whether
the trained policy improves. Do not produce another population solely for
this audit.

The current raw population predates the scalar unit-order repair. It is exact
evidence about the objective that trained Flow215, not evidence about the
numerical gradient of the already-qualified repaired simulator used by the
active guarded runs.

## 2. Lower priority: the large `gp` block may dilute behavioral exploration

`gp` owns 864 of 1,191 live coordinates (72.5%), but the raw gradient does not
make coordinate count alone the best explanation. It carries 45.4% of the
blended gradient's squared norm. The direct product-score blocks `b1`, `dh`,
and `ds` carry 45.6% with only 196 coordinates; the remaining five blocks carry
9.0%. The earlier fixed-dawn macro test also found that 56% of candidates cross
some wheat/carrot target boundary, so the population is not broadly inert.

`gp` dilution remains plausible because global-head changes can miss discrete
planner boundaries, while the direct score blocks are much more efficient per
coordinate. It ranks second because no blockwise complete-plan census yet
shows `gp` to be behaviorally inert, and the existing gradient already assigns
it less energy than its coordinate share. A future no-game falsifier, if needed,
would replay the same epsilon with one named block at a time over a fixed dawn
state bank and compare complete-plan hashes at the single frozen sigma. It
would stop if `gp` changes complete plans at a coordinate-normalized rate
comparable to the direct blocks. No sigma sweep or training run is justified by
the current evidence.

## Evidence boundary

The audit pins the capture helper, source archive, archived trainer and policy
members, validates all saved array digests, population and episode shapes,
receipt-attested no-update status, exact 1,191-coordinate support, and the
configured weighted advantage and gradient reconstruction. The no-update
evidence comes from the hash-pinned capture helper's before/after assertions;
the receipt does not preserve duplicate raw trainer-state snapshots for a
second independent comparison. Its output is
`S/unitorder/flow215_objective_alignment.json`. It describes one fixed
generation's simulator objective. It does not pool evaluation families,
estimate engine wins, select a new weight, or reopen the melon family.
