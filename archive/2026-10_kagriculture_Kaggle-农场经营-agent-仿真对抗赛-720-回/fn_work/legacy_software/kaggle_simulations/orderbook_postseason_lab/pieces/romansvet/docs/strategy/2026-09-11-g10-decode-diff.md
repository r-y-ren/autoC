# g0 -> g10: what flow209 and flow210 actually moved, and whether it reached the decoder

2026-09-11, records `g00010_record.npy` fetched 22:35Z (flow209) / 22:26Z (flow210).
Tool: `S/snr/g10_diff.py` (new, reproducible); tables in `S/snr/g10_diff.md`;
raw payloads `S/snr/g10_diff_209.json` / `S/snr/g10_diff_210.json`.

Both arms run the §73 recipe: `--optimizer sgd`, lr 1.8e-4, sigma 0.01, pop
4,096, weight decay 4e-7, `--train-only gp,dh,ds,g5,gb5,w3,b3,b1` = **1,191
trained genes of 6,789** (`es.train.train_mask(spec) AND policy.live_mask()`,
the same code `S/snr/step_cosine.py` uses). flow209 is seeded from candidate B
(`flow193_g100_hr.npy`, md5 7fcf3948, the LIVE submission 56161192), flow210
from hr (`flow172_g1000.npy`, md5 f091deb2).

## 1. Mask integrity and where the step went

The **5,598 untrained genes are byte-identical to the seed in both arms** -- not
merely close: the raw bytes of the held coordinates compare equal. With
`--optimizer sgd` and the mask gating the perturbation as well as the update
(including the weight decay), that is what the recipe promised, and it means the
whole of the g0->g10 difference is inside the 1,191.

Every one of the 1,191 moved (momentum SGD gives each coordinate a nonzero step;
"moved" is not the interesting statistic, the magnitude is):

| | flow209 (B) | flow210 (hr) |
|---|---:|---:|
| `\|\|delta\|\|` over trained genes | 0.007098 | 0.012180 |
| as a fraction of `\|\|theta_trained\|\|` (5.58 / 5.35) | 0.127 % | 0.227 % |
| as a fraction of ONE sigma-0.01 draw (norm 0.3451) | 2.1 % | 3.5 % |
| max `\|delta\|` / sigma | 0.233 | 0.501 |
| rms `\|delta\|` / sigma | 0.021 | 0.035 |

Ten generations have walked each arm about **one fiftieth (flow209) to one
thirtieth (flow210) of a single population perturbation**. Block shares of
`||delta||^2`:

| block | what it is | flow209 share | flow210 share |
|---|---|---:|---:|
| `gp` (864) | global head's product residual | **34.9 %** | 21.6 % |
| `dh` (128) | residual town drain into the encoder hidden | **30.8 %** | **32.3 %** |
| `w3` (64) | sell head's per-product price gate | 5.4 % | **33.0 %** |
| `ds` (4) | drain straight onto grow/sell | 13.7 % | 1.5 % |
| `b1` (64) | encoder bias | 8.8 % | 2.8 % |
| `g5` (64) | unblock genes (land_afford, free_urgency) | 5.5 % | 6.7 % |
| `gb5` (2) | those genes' biases | 0.5 % | 1.2 % |
| `b3` (1) | sell head's global lot-count bias | 0.4 % | 0.9 % |

Read per coordinate rather than per block, the picture inverts: `gp` carries a
third of flow209's norm only because it has 864 coordinates (rms 1.4e-4 = 0.014
sigma, the *smallest* per-gene step in the layout), while the four `ds` genes
move 1.3e-3 each and the single `b3` scalar moves 4.7e-4 on a seed value of
0.048 -- **1 % of its own magnitude**. In flow210 `b3` is the standout: the seed
value is 0.0109 and the step is 0.00116, a **10.6 % relative move in ten
generations**, by far the largest in either arm. The two arms have *not* chosen
the same direction of attack: flow209's norm is in `gp`+`dh` (what the global
head knows about which product is glutted, and the town's residual drain),
flow210's is in `w3`+`dh` (the sell-side price gate and the same drain).

## 2. Decode: the step does reach the integers, barely

`S/snr/g10_diff.py` replays the first 8 boards of `S/simscreen/boards.json` (the
LIVE-C hold-out list -- 4 pinned-town tapes x both seats) day by day under the
**seed's** trajectory, and decodes both thetas on the identical `PolicyObs` of
every board-day: 240 decisions, 42 integer knobs each. Common observations, so a
difference is the decoder's response to the gene step and not a board that has
already diverged.

**It is not a null decode.** Every one of the 240 decisions differs in at least
one knob in both arms. But almost all of that is in the fixed-point priority
scalars, where a one-unit change is only a decision if it crosses a comparison
inside `plan`. Restricted to the *coarse* integers the planner acts on directly
(`plant_target`, `animal_want`, `crew_target`, `compact`, `animal_defer`,
`forward_days`):

* **flow209: 14 knob-changes over 240 decisions (~6 board-days).**
  `plant_target` +-1 tile on d11 and d24 (three slots), `animal_want` swaps one
  unit between animals 1 and 2 on d9, and `crew_target` 11 -> 12 hands on d22.
  `compact`, `animal_defer` and `forward_days` are identical everywhere.
* **flow210: 20 knob-changes over 240 decisions, ALL of them `plant_target`**
  (+-1 tile on d5, d13, d16, d20, d27). `animal_want`, `crew_target`, `compact`,
  `animal_defer` and `forward_days` are identical on all 240 decisions.

The ratio fields move much more freely, as expected from their scale:
`press[4]` differs on 100 % of flow210's decisions and `grow_mult[4]` on 96.7 %
of flow209's, but by one or two fixed-point units at a time.

This is the §76 lattice reading holding *at the edge*, not being refuted. B is
still in the interior of its rounding cell almost everywhere; ten generations
found six board-days out of 240 where it is not. The corroboration is
independent: the auto-judge's flow210_g10 legs (verdicts.log 22:38Z) read LEVEL
against its own seed with **0 flips** on 284 games -- exactly what 20 one-tile
`plant_target` changes on 8 % of board-days should produce.

## 3. In-sample, and which rungs it is on

Both arms draw **166 pinned-town action-tape rungs** per generation
(`artifacts/tape_actions_town/*.npz`, `pinned_once: true`,
`pinned_fixed_seed: true`, `shop_crn: true`), one episode each, plus 6 `_pool`
and 6 `_theta` self-play episodes -- 178 of a configured 179. The four
archetypes (`expander`, `rusher`, `rancher`, `patient_grower`) are weighted 0
and drew **zero** episodes despite `arch_frac 0.9`. **The log carries no
per-rung win field**, so the gain cannot be attributed rung by rung from it;
what can be said is that by episode allocation 93 % of the fitness signal is
pinned tapes and none of it is drawn-town, so there is no drawn-rung channel for
a gain to hide in.

| | flow209 | flow210 |
|---|---|---|
| `mean_win` g1 -> g10 | 0.6660 -> 0.6675 (+0.0015), peak 0.6744 at g5 | 0.6059 -> 0.6198 (+0.0139), peak at g10 |
| `best_win` g1 -> g10 | 0.7360 -> 0.7303 (**down**) | 0.6854 -> 0.6966 |
| `d10_cash` | -11,558.9 -> -11,599.4 | -11,545.1 -> -11,572.1 |
| `tile_fill` | 45.91 -> 45.84 | 43.50 -> 43.80 |

flow209's in-sample curve is a flat random walk of amplitude ~0.013 with no
trend; its `best_win` ends lower than it started. flow210's rises +0.0139 over
ten generations, close to monotone, and its `best_win` ends higher -- but it
starts 6 points below flow209 and the whole rise is smaller than flow209's
gen-to-gen jitter, so it is equally consistent with hr having more slack to
recover than with a real gradient. The only independent read in the window is
`real_gate` at gen 0 (124 games, `real_gate_every: 100`, so the next is gen
100): flow209 0.5726 win / +3,027.8 margin, flow210 0.5565 / +1,948.2. Both are
the seeds' own baselines.

## 4. Judgement, and what to expect at the g30 SNR read

**Both arms are moving decodable knobs, but only at the margin, and in
different blocks.** The mask is clean (5,598 genes byte-identical), the step is
2-3.5 % of one sigma draw, and it reaches the coarse integers on roughly six to
eight board-days in 240 -- `plant_target` in both arms, plus one `animal_want`
swap and one `crew_target` 11->12 in flow209. flow209's norm sits in `gp`+`dh`
(the global head's product identity and the town drain), flow210's in `w3`+`dh`
(the sell price gate and the same drain); `b3`, a single near-zero sell-head
scalar, is the one coordinate making a double-digit relative move (flow210,
10.6 %). `dh` being the one block both arms load is the only cross-arm agreement
in the layout and is worth watching: it is the residual-drain path into the
shared encoder, the newest input the champion has never had trained alone.

At g30, `step_cosine.py` will have three records and print its first two block
deltas. The prediction that follows from this read: the **decode is not yet the
binding constraint** -- theta is moving out of its rounding cells at a rate of
~0.6 coarse knob-changes per board-day per 10 generations, so by g30 a candidate
should differ on ~15-20 % of board-days and an engine leg should start showing
flips instead of the 0 flips flow210_g10 produced. What that read tests is
whether the direction is the *same* direction: the consecutive-block cosine has
to beat the optimizer-momentum null (beta1 0.9 makes consecutive 10-gen deltas
overlap by construction; `step_cosine` simulates the run's own schedule for it,
about +0.5 at d=1,191), not the analytic 0.029. Given §72 (the gradient at B is
real but dimension-limited, disjoint cosine 0.039 = P/(P+d)) and §77 (noise
divided by 20 still left kappa 0.01-0.03), the base rate says the two blocks
will come back orthogonal-after-momentum and the g30 verdict will be NOISE. The
useful asymmetry to watch for is flow210 beating flow209 there: hr has the
larger step, the monotone in-sample curve and the 10 % `b3` move, so if either
arm carries a real direction it is the hr seed -- which would also say the
§73 recipe is finding slack hr has and B does not, i.e. a gradient that exists
away from B's local optimum rather than at it.
