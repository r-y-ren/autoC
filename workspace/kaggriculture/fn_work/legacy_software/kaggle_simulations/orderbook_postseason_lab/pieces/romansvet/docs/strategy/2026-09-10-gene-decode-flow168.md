# What the drain-mix gene has actually learned by flow168 gen-54

*2026-09-10. Measurement only, read-only code, worktree `.claude/worktrees/drain-gene`
(HEAD `4a7a885`, `N_PARAMS` 7,053). Thetas: `~/stage_draingene/artifacts/flow168/`
`best_sim.npy` md5 `34dbd4c9` (mean theta, gen-54) and `champion.npy` md5 `8d0d6e83`,
against the padded init `artifacts/kagg2_games/thetas/flow166_g170_gd.npy` md5
`8dbc9964`. States: 300 recorded hour-0 observations from
`tests/data/trajectory_obs.npz` (the fixture the gene's slope test uses,
`rng(0).choice(2400, 300)`). Scripts under the session scratchpad `genedec/`.*

## 1. The gene has moved exactly as far as every other block

`theta - init`, rms per block. Every trainable block moved **0.006-0.013**; the
gene moved **0.0110**. The arm's sigma is 0.015, so this is 0.72-0.74 sigma of
movement everywhere — the isotropic random walk of an ES mean over 54
generations, not a gradient.

| block | n | rms(init) | rms(move) | move/init |
|---|---|---|---|---|
| w1/b1/w2/b2 (encoder) | 2,498 | 0.207 | 0.0115 | 0.06 |
| g1/gb1/g2/gb2 (head) | 1,394 | 0.216 | 0.0110 | 0.05 |
| g3/gb3, g4/gb4 | 330 | 0.249 | **0.0000** | 0.00 (ES-masked) |
| g5..gb10 (genes) | 690 | 0.16 | 0.0110 | 0.07 |
| fh/fs (forecast) | 528 | 0.037 | 0.0113 | 0.30 |
| gp (global product) | 864 | 0.043 | 0.0113 | 0.26 |
| g11/gb11, fv | 417 | 0.043 | 0.0113 | 0.26 |
| **gd (32x8)** | 256 | 0.000 | **0.01104** | — |
| **gbd (8)** | 8 | 0.000 | **0.01187** | — |
| pre-gene pooled | 6,789 | 0.191 | 0.01074 | 0.056 |

`champion.npy` replicates it one step further out: gene rms 0.02259 against a
pre-gene move of 0.02030. Both thetas are a sphere, not a direction.

## 2. The decoded logit, per product

`mix_drain[p] = clip(5.0 * mixd[p] * share[p], +-3)`, 300 states, `best_sim`.
`share` is `residual_drain`'s column 1 (positive = the town's remaining season
appetite is unclaimed). **Nothing clips**: max |term| 1.9 against a clip of 3.

| product | share mean | `mixd` mean (the gene) | term mean | term sd | term range | % clipped | % \|term\|>0.1 |
|---|---|---|---|---|---|---|---|
| WHEAT | +2.09 | **-0.017** | -0.249 | 0.277 | -1.05 .. +0.05 | 0.0 | 56 |
| CARROT | +1.77 | **+0.036** | +0.448 | 0.528 | -0.06 .. +1.88 | 0.0 | 59 |
| TOMATO | +1.85 | **+0.043** | +0.392 | 0.228 | +0.16 .. +1.08 | 0.0 | 100 |
| STRAWBERRY | +1.86 | **-0.018** | -0.115 | 0.141 | -0.45 .. +0.51 | 0.0 | 73 |
| MELON | -3.78 | **-0.018** | +0.393 | 0.475 | -0.45 .. +1.15 | 0.0 | 92 |
| EGG | +1.34 | **+0.041** | +0.271 | 0.347 | -1.23 .. +1.12 | 0.0 | 100 |
| MILK | +0.22 | **-0.002** | -0.019 | 0.042 | -0.32 .. +0.06 | 0.0 | 5 |
| WOOL | +0.01 | **+0.032** | +0.054 | 0.202 | -0.59 .. +0.47 | 0.0 | 78 |

Sign of `mixd` is the whole story: **+ = follow the sink** (tilt toward a
product whose appetite is unclaimed, away from one that is glutted), **- =
contrarian**. The pattern reads as the top-ten census direction — sink-following
on CARROT, TOMATO, EGG and WOOL, suppressive on WHEAT and STRAWBERRY. Section 4
is why that reading is not evidence.

## 3. What it changes on those states

Fractions of the 300 states whose `Macro.plant_target` / `Macro.animal_want`
differ. Two comparisons, because `best_sim` moved all 7,053 coordinates:

| comparison | plant vector | plant argmax | herd vector | herd argmax |
|---|---|---|---|---|
| `best_sim` vs init (whole theta) | 37.0 % | 2.5 % | 1.7 % | 3.5 % |
| **gene only** (`best_sim` vs `best_sim` with gd/gbd zeroed) | **14.0 %** | 2.1 % | **0.3 %** | 0.9 % |

Gene-only direction, units per state: WHEAT **+0.080** (10.7 % of states up,
2.0 % down), STRAWBERRY **-0.093** (0.7 % up, 10.0 % down), TOMATO +0.017,
CARROT -0.003, MELON 0.000 (never plantable on these boards: `absorb` masks a
negative share). Herd: EGG +0.003, MILK -0.003, WOOL 0.000 — 0.3 % of states.
The herd half is dead for the structural reason the launch doc already
recorded: these boards buy ~1 animal a day against ~7 plantings, so a
three-way softmax rounded to one unit almost never flips.

## 4. The control: a random block of the same size does the same thing

The gene's rms is the drift rms, so the honest test is a random `gd`/`gbd` drawn
isotropically at **that same rms** (0.01106) on top of the same `best_sim`
prefix. 400 draws for the decoded logit, 4 draws for the full `decide`.

* **Per-product logit.** The trained gene's mean term is inside the random-draw
  spread on every one of the eight products: |z| = 0.68 (wheat), 1.38 (carrot),
  1.21 (tomato), 0.35 (strawberry), 0.67 (melon), 1.21 (egg), 0.61 (milk),
  0.82 (wool). Nothing reaches 2.
* **Mix change.** Trained gene moves the plant vector on **14.0 %** of states;
  four random blocks moved 11.3 %, 19.3 %, 21.3 %, 13.0 %. Herd: 0.3 % trained,
  0.0-0.3 % random.
* **Direction.** The trained gene's wheat/strawberry tilt (+0.080 / -0.093) is a
  coin flip across the random draws: +0.113/-0.087, -0.153/+0.050,
  +0.213/-0.187, -0.103/+0.037.

The sign pattern in section 2 is therefore four of eight signs landing where a
census would want them, out of a draw that produces per-product means of exactly
that magnitude with random signs. It is not a learned tilt.

## 5. Verdict

**No.** The block is live — it decodes, it is linear, it clips nothing, it moves
14 % of plant decisions, and the launch doc's slope measurement was right. What
it has not done in 54 generations is *learn*: gd/gbd moved 0.0110 rms against a
pre-gene move of 0.0107, and every per-product decoded logit and every
mix-change fraction sits inside the band a random block of the same rms
produces. The gene is drifting, not being selected — consistent with a gen-10
candidate the margin gate refused (+14/-4 wins on 206 live gate games) and with
nothing above the init since. Selection pressure on 264 coordinates out of 7,053
under a joint `--train-only all` search is too weak to separate this block from
noise; the cheap variant the launch doc names (`--train-only gd,gbd`, champion
held byte for byte) is the arm that would answer whether the tilt pays.
