# Day-0 melon reachability from B: decoder trace, sigma measurement, gene

Scope: macro decode only — no simulator episode, engine game, training arm or
outcome evidence. Every number is a decode of `flow193_g100_hr.npy` ("B", 6,789
coordinates, zero-padded to `policy.N_PARAMS` = 7,020) on a pinned dawn.
## 1. Decoder trace: what sets the day-0 melon plant target

| Step | Expression | File:line | Genes |
|---|---|---|---|
| Encoder + grow/sell scores | `h = tanh((x@w1+b1) + drain@dh + fcast@fh + mom@mh)`; `scores = (h@w2+b2) + drain@ds + fcast@fs + mom@ms` | `core/policy.py:679-690` | `w1,b1`, `w2,b2`, `dh`, `ds`, `fh`, `fs`, `mh`, `ms` |
| Global hidden + head | `gh = tanh((glob@g1+gb1) + summary@gp + fwdval@fv)`; `head = gh@g2 + gb2` (live slots 1,2,5,6,7) | `core/policy.py:695-706` | `g1,gb1`, `gp`, `fv`, `w3,b3` (via `summary`), `g2,gb2` |
| Free tiles / development / herd split | `land_ok`, `n_free`, `dev_frac = sig(head[5]+aux[2]*n_free/25)`, `animal_share = sig(head[6])` | `core/brain.py:958-991`, `:152` | `g2,gb2`, `g5,gb5`, `g8,gb8` |
| **Crop budget** | `plant_total = n_dev - sum(animal_want)` | `core/brain.py:992` | everything above |
| **Crop logits** | `crop_logits = grow[:5] * (1 + sig(head[7])*4)` | `core/brain.py:1006` | grow path + `g2[:,7],gb2[7]` |
| **Crop mix residual** | `w = softmax(crop_logits + clip(crop_mix, +-CROP_MIX_CLIP))` | `core/brain.py:1013`; `crop_mix = gh @ cm + cb` at `core/policy.py:693` | **`cm`,`cb`** (zero in every shipped theta) |
| Maturity + drain gates | `w *= can_mature`; `absorb = (drain[:5,1] + DRAIN_CLIP*tanh(sat) > -DRAIN_CLIP)` | `core/brain.py:1029-1031`, `:1071-1073`; `DRAIN_CLIP=4.0` at `:236` | `g7,gb7` (`out.sat`) |
| Integer split | `plant_target = _largest_remainder(w, plant_total, 5)` | `core/brain.py:1083`, `:875` | none |
| Seed cap | `plan._wants` clips the want to tiles that will exist | `core/plan.py:2006-2007`, `:4406-4420` | planner, not a gene |
| Sell timing | `hold = qfloor(0.8*base*_unit_ratio(sell))`; `press = qfloor(base*max(tanh(gate),0))` | `core/brain.py:1108-1110` | `w2,b2` (sell col), `w3,b3` (`gate`) |

MEASURED, day-0 dawn of episode 108450468 seat 1 and the engine cold start:
melon's log-share is **-5.6456**; `can_mature` and `absorb` are both **open** for
melon on day 0 (the `-DRAIN_CLIP` pin the `brain.py:1029-1073` commentary
describes starts on day 1). The day-0 blocker is **not** the drain veto, the
maturity mask or the seed cap: it is the softmax share plus `_largest_remainder`.
## 2. The exact boundary, measured on the shipped decoder

B padded to 7,020 makes `cb[I_MELON]` an exact additive bias on melon's crop
logit (`brain.py:1013`). Bisection on that coordinate gives the additive
log-share, in nats, that buys the Nth melon tile:

| board (day 0 dawn) | B target W,C,T,S,M | >=1 | >=4 | >=8 | >=12 |
|---|---|---:|---:|---:|---:|
| ep108450468 seat 1, and engine cold start | 11,11,0,0,0 | **2.0487** | 3.9303 | 4.9557 | 5.7090 |
| warm start nquad 2 / 3,000 | 11,10,0,0,0 | 0.7383 | 3.0300 | 4.0568 | 4.8610 |
| warm start nquad 2 / 20,000 | 3,3,0,3,**12** | 0 | 0 | 0 | 0 |
| warm start nquad 3 / 40,000 | 0,0,0,8,**22** | 0 | 0 | 0 | 0 |

The engine cold-start day-0 dawn carries no seed (`state.initial_state` takes
none), so day 0 is the same observation on every board of
`S/simscreen/boards.json` / `boards_topb2.json`; board identity first enters at
day 1, whose dawns decode `[1,0,0,0,0]` / `[0,0,0,0,0]` on the replay — after a
day-0 22-tile fill there is no free land, so **day 1 is not an alternative entry
point** under B.

B is not melon-blind — melon tiles vs cash (nquad 1) and vs land (3,000 coins):

| money | 3,000 | 8,000 | 12,000 | 20,000 | 30,000 | 50,000 | | nquad | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| melon | 0 | 0 | 0 | 1 | 5 | 8 | | melon | 0 | 1 | 4 | 6 |
## 3. Perturbation table

Melon log-share gradient at B on the ep108450468 day-0 dawn, by block
(`jax.grad` of `log_softmax(crop_logits + clip(crop_mix))[I_MELON]`; features do
not depend on theta, so this is exact). `sd@0.01` is the boundary in units of an
ES draw's *aligned component* — an isotropic sigma-0.01 draw projects onto any
fixed unit direction as N(0, 0.01) — i.e. how many standard deviations out along
the melon direction one candidate must be.

| block set | n | \|\|g\|\| | sd@0.01 | smallest step reaching >=1 melon, all 5 boards | >=4 | >=8 | >=12 |
|---|---:|---:|---:|---|---|---|---|
| FULL theta | 7,020 | 36.26 | 5.7 | sigma 0.02, k=3 | 0.05 k3 | 0.05 k4 | 0.05 k4 |
| flow215 mask `gp,dh,ds,g5,gb5,w3,b3,b1` | 1,224 | 14.29 | 14.3 | sigma 0.05, k=3 | 0.1 k4 | 0.1 k5 | none <=5 sigma at 0.1 |
| H mask `w2,b2` | 130 | 15.85 | 12.9 | sigma 0.05, k=3 | 0.1 k3 | 0.1 k4 | 0.1 k5 |
| `w1` | 2,304 | 28.98 | 7.1 | sigma 0.02, k=4 | 0.05 k3 | 0.05 k4 | 0.05 k5 |
| `dh` | 128 | 11.30 | 18.1 | sigma 0.05, k=3 | 0.1 k5 | none | none |
| `b1` | 64 | 7.16 | 28.6 | sigma 0.05, k=4 | none | none | none |
| `g2,gb2` / `gp` / `g1,gb1` | 594/864/800 | 2.41/2.19/2.24 | 85-94 | none | none | none | none |
| `cm,cb` | 165 | 2.89 | 71.0 | none | none | none | none |
| `cb` alone | 5 | 1.22 | 168.4 | none | none | none | none |

**Within 5 sigma at sigma 0.01 and 0.02 no block reaches even one day-0 melon
tile on the two cold-start boards** (the full theta first reaches one at sigma
0.02 k=3). At sigma 0.05-0.1 the encoder blocks (`w1`, `w2,b2`, `dh`) reach 1-12
tiles. `cm,cb` — the block whose stated job is crop proportions — is the
**worst** lever of all at 71-168 sd.
## 4. Blocker diagnosis

Not `DRAIN_CLIP`, not `can_mature`, not `seed_cap`, not cash priority in the
planner. The blocker is **decode gain versus an integer boundary**:

1. B ranks melon fifth of five on the cold day-0 board, 2.0487 nats below the
   first-tile boundary (`_largest_remainder`, `brain.py:1083`: melon's remainder
   must enter the top two of 22 tiles).
2. The only zero-init block aimed at crop proportions, `cm`/`cb`, has gradient
   norm 2.885 there, so **one sigma-0.01 draw moves melon's log-share ~0.01
   nats: 71 standard deviations short.**
3. The target is integer, so a population that never crosses the boundary gives
   no fitness variation along the melon direction and ES gets **zero gradient
   signal** — the 8,192-candidate zero in
   `2026-09-13-melon-sigma-reachability.md` is this barrier, not an inert policy.

This is the `round(16*z)` defect of the 2026-09-09 gene-slope check
(memory: "gene slope check"): the gene is wired and decodable, and its gain at
the training sigma is ~200x too small to change the decoded integer.
## 5. Switch: `brain.MELON_GENE_ON` (default OFF)

`src/kagg3/core/brain.py:776-802` (constants), `:1009-1013` (branch). ON, the
crop log-share readout is multiplied before the clip:

```python
if MELON_GENE_ON:
    w = _softmax(xp, crop_logits + xp.clip(CROP_MIX_GAIN * out.crop_mix,
                                           -CROP_MIX_CLIP, CROP_MIX_CLIP))
else:
    w = _softmax(xp, crop_logits + xp.clip(out.crop_mix, -CROP_MIX_CLIP, CROP_MIX_CLIP))
```

`CROP_MIX_GAIN = 256.0` from the measurement: 256 * 0.01 = 2.56 nats, above the
2.0487-nat first-tile boundary and below the 3.9303 that would make every draw a
four-tile jump. The OFF branch is the shipped expression character for
character; the ON branch differs only by the multiply and `0.0 * 256.0 == 0.0`,
so B (whose `cm`,`cb` are zero) decodes byte-identically either way. The clip is
unchanged and still last, so a saturated gene is +-10 nats, reached at
|z| ~ 0.039 (~4 sigma at 0.01) — a five-level lever at sigma 0.01, not a
continuous one. Crop-symmetric: a proportions readout for all five crops, not a
melon rule.

NOT IMPLEMENTED, UNVERIFIED — the melon sell-day / lot-timing half. `hold` and
`press` (`brain.py:1108-1110`) decode from `w2,b2` and `w3,b3`, both dense in B;
the 7,020 layout has no zero-init per-crop timing block to give a gain to. Doing
it properly needs a layout append — `("sb", (spec.N_CROPS,))` after `cb`,
decoded round-style as a per-crop hold multiplier `1 + HOLD_BIAS_GAIN * sb` on
`hold[:N_CROPS]` (inert at zero: `x * 1.0 == x`) — which moves
`policy.N_PARAMS` off 7,020 and needs `tests/test_crew_and_herd_mix.py:480`
updated. Out of this box; no slope for it has been measured.
## 6. Slope table for the new gene (day-0 melon tiles vs `cb[I_MELON]`)

Five pinned day-0 dawns: the real ep108450468 dawn, the engine cold start, and
three `initial_state` warm starts (as `Trainer.draw_starts` draws).

| `cb[melon]` | ep108450468 | cold | q2/3k | q1/8k | q2/12k |
|---:|---:|---:|---:|---:|---:|
| OFF, any z in [-0.1, 0.1] | 0 | 0 | 1 | 0 | 5 |
| -0.04 / -0.02 (-1 sigma @ 0.02) | 0 | 0 | 0 | 0 | 0 |
| -0.01 (-1 sigma @ 0.01) | 0 | 0 | 0 | 0 | 1 |
| 0.00 | 0 | 0 | 1 | 0 | 5 |
| **+0.01 (+1 sigma @ 0.01)** | **1** | **1** | **8** | **2** | **16** |
| **+0.02 (+1 sigma @ 0.02)** | **8** | **8** | **18** | **13** | **21** |
| +0.04 / +0.10 | 22 | 22 | 20 | 22 | 21 |

Full targets at z = +0.01: `[10,11,0,0,1] [10,11,0,0,1] [6,5,0,1,8]
[9,11,0,0,2] [2,2,0,1,16]`. Monotone on all five boards, both signs live.
## 7. Tests run

```
JAX_PLATFORMS=cpu .venv/bin/python -m pytest tests/test_melon_gene.py -q
.....                                                            [100%]  PASS 5/5

JAX_PLATFORMS=cpu .venv/bin/python -m pytest tests/test_melon_gene.py \
    tests/test_melon_open.py tests/test_plant_mix_drain.py \
    tests/test_crew_and_herd_mix.py -q
FAILED test_melon_open.py::test_off_plan_is_byte_identical_to_the_pre_switch_planner
FAILED test_crew_and_herd_mix.py::test_a_positive_hire_bias_raises_the_crew_the_planner_chooses
FAILED test_crew_and_herd_mix.py::test_an_early_bucket_raises_the_day_10_crew
FAILED test_crew_and_herd_mix.py::test_the_late_bucket_moves_the_late_crew[21]
FAILED test_crew_and_herd_mix.py::test_the_late_bucket_moves_the_late_crew[27]
FAILED test_crew_and_herd_mix.py::test_no_bucket_hires_on_the_terminal_day
```

Those six are **pre-existing**: `git stash push -- src/kagg3/core/brain.py` then
re-running the same selection reproduces exactly the same six, so the switch
introduces none. `test_plant_mix_drain.py` and the rest of `test_melon_open.py`
pass. New `tests/test_melon_gene.py` covers: default OFF; B's full macro
byte-identical ON at zero gene on all five dawns; OFF a one-sigma gene moves
nothing; ON it adds >=1 melon on >=4 of 5 boards at sigma 0.01 and 0.02; and the
decode is monotone in z.

**OFF-path equivalence, direct.** Every `Macro` field, hashed over 12 thetas
(zeros; B padded to 7,020; the unpadded 6,789 incumbent; 6 random N(0,0.3); B +
noise at sigma 0.01/0.02/0.05) x 80 dawn states (nquad 1-4 x money
3k/8k/20k/60k x days 0/5/13/21/29) x **both backends** (numpy and JAX):

baseline `src @ 529d33d^` (no switch) and current `src` with
`MELON_GENE_ON=False` both digest `3b4e978fecea08f69965d361255be59af747c749
75d30c2268c7320445f9b680`. Identical, so the OFF branch is bit-exact against the
pre-switch decoder on both backends — the guarantee
`tests/test_backend_agreement.py` gives, taken directly.
`tests/test_gene_sweep.py tests/test_gene_diag.py -q` also pass (8/8, exit 0).
## 8. What an ES arm needs to be able to learn early melon

1. **With `MELON_GENE_ON` and the 7,020 layout**: free `cm,cb` (165 coords,
   offsets 6,855-7,019) at **sigma 0.01-0.02**. One sigma on the melon
   coordinate crosses the first-tile boundary, so the population holds both
   0-melon and 8-22-melon day-0 openings and the integer decision receives
   fitness variation. The centre must be a B padded to 7,020 (`policy.pad`); a
   6,789-length checkpoint has no `cm,cb`.
2. **Without the switch** the same arm is dead: `cm,cb` at sigma 0.01 is 71 sd
   from one melon tile, `cb` alone 168 sd. Consistent with
   `2026-09-13-melon-sigma-reachability.md`'s 8,192-candidate zero on the
   flow215 mask, whose own aligned barrier measures 14.3 sd.
3. **Without any decoder change**, the only masks reaching day-0 melon inside 5
   sigma are encoder blocks at a large sigma: `w1` at sigma 0.02 k=4 or 0.05,
   `w2,b2` (H) at 0.05, `dh` at 0.05. Per memory "ES noise floor 2026-09-05"
   §106 that is inside known cliff territory; not recommended on this evidence.
4. **Day 1 is not an entry point**: after a day-0 22-tile fill the day-1 dawn
   decodes `plant_total` 0-1, so an early-melon opening is decided on day 0 or
   funded by land/cash the planner does not have.
5. Reachability is not value. The archive's forced `MELON_OPEN`, `MELON_D1` and
   `m0p1` interventions all lost; a `cm,cb` arm must clear the standing
   seven-family judge like any other.
