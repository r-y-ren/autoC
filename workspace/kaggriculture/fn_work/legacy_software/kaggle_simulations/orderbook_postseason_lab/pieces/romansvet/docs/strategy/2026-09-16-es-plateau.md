# ES PLATEAU — are flowq2_g150 and flow218_g110 real?

*2026-09-16, read-only analysis. Tools in `S/esplateau/`, no `src/` change, no commit.
Every number below is reproducible from the existing judge CSVs in `S/lossflip/`;
nothing was re-simulated.*

## VERDICT IN ONE LINE

**No.** An empirical-Bayes fit over the 22 judged ES checkpoints says the *true* pooled-band
effect of every ES candidate launched from B is **−124 ± 47 coins** — the entire observed spread
of the pooled reads (sd 188) is accounted for by the judge's own standard error (sd 182). The
shrunk estimate of flowq2_g150 is **−98 [−188, −7]** and of flow218_g110 **−97 [−187, −7]**.
The +295/+302 readings are the top two order statistics of ~30 draws from a mean-−124 / se-182
distribution, which is exactly what selection produces. The two candidates' per-board gains do
correlate (r +0.465) — but so does *every* pair of perturbations of B, including rejected
candidates from unrelated families (median pairwise r **+0.387**); after the generic
"move-off-B" factor is regressed out the record-vs-record correlation falls to **+0.224**
(95 % CI +0.018…+0.412) with **51.1 %** sign agreement, i.e. chance.

---

## Q1 — are the two candidates' per-board gains correlated?

`JAX_PLATFORMS=cpu .venv/bin/python S/esplateau/corr.py flowq2_g150_hr flow218_g110_hr`
(per-board = the two seats averaged into one observation, the judge's own statistic,
`S/bank/paired.py:60-90`; legs and CSVs read through `S/judge7065/pooled_band.py:29-45`)

| leg | boards | flowq2 Δ | t | flow218 Δ | t | Pearson r | Spearman ρ | both+ | both− | mixed | sign agree |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| POOLED BAND | 90 | +295 | +1.71 | +302 | +1.32 | **+0.465** | +0.338 | 31 | 22 | 37 | 58.9 % |
| · LIVEC-H30 | 30 | −42 | −0.13 | +428 | +1.08 | +0.662 | +0.648 | 14 | 8 | 8 | 73.3 % |
| · LIVEC-H30B | 30 | +551 | +1.68 | +544 | +1.10 | +0.441 | +0.341 | 9 | 6 | 15 | 50.0 % |
| · NEXT30 | 30 | +377 | +1.66 | −66 | −0.25 | +0.181 | +0.100 | 8 | 8 | 14 | 53.3 % |
| LIVE62 | 62 | +207 | +0.41 | +129 | +0.48 | +0.534 | +0.368 | 27 | 10 | 25 | 59.7 % |
| BAND+LIVE62 | 152 | +259 | +1.12 | +231 | +1.33 | +0.462 | +0.352 | 58 | 32 | 62 | 59.2 % |

Note the two records **do not agree on which leg they win**: flowq2 is −42 on LIVEC-H30 where
flow218 is +428; flow218 is −66 on NEXT30 where flowq2 is +377. Two candidates sharing a
mechanism do not split the band that way.

### The control that settles it

`JAX_PLATFORMS=cpu .venv/bin/python S/esplateau/matrix.py flowq2_g150_hr flow218_g110_hr flowq3_g60_hr flow218_g270_hr flow216_g70_hr flow219_g70_hr momentum_joint_J_seed312 crop_mix_C_seed313`

r between the two records is +0.465. r between **unrelated, rejected** perturbations of B:

| pair | r | ρ | r(|Δ|,|Δ|) | sign agree |
|---|---:|---:|---:|---:|
| flowq2_g150 × flow218_g110 (the two records) | +0.465 | +0.338 | +0.408 | 58.9 % |
| flow216_g70 × flow219_g70 (both rejected, −331 / −335) | +0.501 | +0.438 | +0.309 | 64.4 % |
| flow218_g110 × flow219_g70 (record × rejected) | +0.439 | +0.424 | +0.063 | 65.6 % |
| flowq3_g60 × momentum_joint_J_seed312 (different family) | +0.454 | +0.432 | +0.265 | 67.8 % |
| flowq2_g150 × momentum_joint_J_seed312 | +0.370 | +0.393 | +0.139 | 57.8 % |

**r over all 28 pairs: min +0.022, median +0.387, q3 +0.454, max +0.516.** The record-vs-record
r (+0.465) sits at the ~75th percentile of that null. It is not evidence of a shared mechanism;
it is evidence that *any* perturbation of B moves the same boards the same way.

### The generic "move-off-B" factor

`JAX_PLATFORMS=cpu .venv/bin/python S/esplateau/factor.py` — factor *g* = the per-board mean of
14 control candidates (records excluded), regressed out of each record.

```
generic factor g:  mean -534 coins/board, sd 1143, up on only 27/90 boards
                          raw r(records) = +0.465  rho +0.338
                        resid r(records) = +0.224  rho +0.102   95% CI +0.018 .. +0.412
                        resid sign agreement 51.1 %  (30 both gain, 16 both lose, 44 mixed)
```

Both records load positively on *g* (β +0.75 for flowq2, **+1.13** for flow218, r with g +0.52 /
+0.60). The shared component is the *direction that costs 534 coins a board*; what is left over
is uncorrelated. **→ selection noise, not a shared mechanism.**

---

## Q2 — what do the deltas change in play?

The judge CSVs already carry a per-game behaviour receipt (`moves, move_turns, noops, unsold,
quads`), so this is answered on all 90 boards rather than 6:
`JAX_PLATFORMS=cpu .venv/bin/python S/esplateau/behav.py flowq2_g150_hr flow218_g110_hr`

| candidate | column | mean Δ/board | t | r vs Δmargin | boards changed |
|---|---|---:|---:|---:|---:|
| flowq2_g150 | our coins | +376 | +1.88 | +0.489 | 58 up / 32 dn |
| flowq2_g150 | **their coins** | +81 | +0.42 | **−0.395** | 54 up / 36 dn |
| flowq2_g150 | moves | +7.9 | +1.47 | +0.084 | **180/180 rows** |
| flowq2_g150 | move_turns | −0.4 | −1.12 | +0.163 | 152/180 rows |
| flowq2_g150 | unsold | +0.5 | +1.58 | +0.093 | 143/180 rows |
| flowq2_g150 | **quads** | **0.0** | — | — | **0/180 rows** |
| flow218_g110 | our coins | +278 | +1.17 | +0.630 | 47 up / 43 dn |
| flow218_g110 | **their coins** | −24 | −0.12 | **−0.389** | 45 up / 45 dn |
| flow218_g110 | moves | −5.0 | −0.99 | −0.001 | **180/180 rows** |
| flow218_g110 | move_turns | **−3.0** | **−6.61** | +0.081 | 176/180 rows |
| flow218_g110 | unsold | **+1.1** | **+3.01** | +0.032 | 150/180 rows |
| flow218_g110 | **quads** | **0.0** | — | — | **0/180 rows** |

B's absolutes on the same rows: moves 2,881.6, move_turns 594.4, noops 0.0, unsold 6.7,
**quads 3.0**.

Read:

* **The macro opening is untouched.** `quads` is 3 on every board for B *and* both candidates,
  on all 180 rows. Neither delta ever changes the expansion decision, and `noops` stays 0. The
  ES drift lives entirely below the macro.
* **The drift is diffuse, not one lever.** Every board's move stream changes, but by ~5–8 of
  2,882 moves (0.2–0.3 %) and ~0.5–3 of 594 acting turns (0.1–0.5 %). Consistent with the theta
  picture: `S/esplateau/norms.py` shows each delta is non-zero on 5,997 of 5,997 unfrozen
  coordinates with a largest single coordinate of 0.118 (flow218) / 0.163 (flowq2) against
  |B| = 18.11.
* **The two systematic changes that ARE significant do not pay.** flow218's move_turns −3.0
  (t −6.61) and unsold +1.1 (t +3.01) are the only behaviour changes that clear t 2 — and both
  correlate with Δmargin at |r| ≤ 0.08. Whatever is producing the +302 is not these.
* **Roughly half the "gain" is the opponent's coins moving, not ours.** r(Δtheirs, Δmargin) is
  −0.39 for both candidates, and on several of the top boards our own coins barely move while
  theirs collapse — flowq2 on tape 107593329: Δmine +340, **Δtheirs −3,082**; flow218 on tape
  107469791: Δmine −90, **Δtheirs −4,737**. That is the shared-market price channel re-rolling,
  i.e. the shop/price lottery documented in `shop-lottery-2026-09-06`, not our play improving.

### The day-by-day decode on the one board both candidates win biggest

`JAX_PLATFORMS=cpu .venv/bin/python S/esplateau/trace.py --boards 107630176:1160628595:0 --thetas flow193_g100_hr flowq2_g150_hr flow218_g110_hr`
(same pinned-town + `shop_crn` action-replay board construction as `S/simscreen/screen.py:176-200`;
tape 107630176 is flowq2's #1 gain board, **+5,107**, and flow218's #2, **+5,608**)

| day | metric | B | flowq2_g150 | flow218_g110 |
|---:|---|---:|---:|---:|
| 0 | wheat / carrot / animals | 11 / 8 / 6 | **10 / 9** / 6 | 11 / 8 / 6 |
| 4 | wheat / carrot / straw / shed | 10 / 0 / 7 / 51 | **11 / 1 / 6 / 48** | 10 / 0 / 7 / 51 |
| 6 | quads / wheat / straw | 2 / 18 / 21 | 2 / **19** / 21 | 2 / 18 / 21 |
| 8 | money / shed | 2,126 / 54 | **1,085** / **64** | **2,326** / 54 |
| 10 | quads / straw / melon / animals | 3 / 33 / 2 / 16 | 3 / **32** / 2 / 16 | 3 / **32** / 2 / **17** |
| 15 | wheat / tomato / straw / melon | 8 / 1 / 34 / 14 | 8 / 1 / 34 / 14 | **7** / 1 / **35** / 14 |
| 18 | money | 39,675 | 40,296 | 40,962 |
| 21 | money | 70,178 | 72,564 | 71,882 |
| 24 | money | 91,158 | 94,859 | 94,003 |
| 29 | money / hands / final margin | 132,280 / 9 / **−3,625** | 138,203 / 9 / **+1,874** | 137,914 / 9 / **+1,962** |

* **Quadrant ramp identical** (1 → 2 by d6 → 3 by d10), **hire schedule identical** (0 hands all
  season, 9 on d29), **animal ramp identical** (6 → 17). The opening, the expansion and the
  labour plan are byte-identical macro decisions in all three.
* The only structural differences are **one tile**: B plants 11 wheat / 8 carrot at d0 where
  flowq2 plants 10 / 9; flow218 differs from B only in a single strawberry-for-wheat swap at d15.
* Those one-tile differences compound through the price table: the money gap is *negative*
  for flowq2 at d8 (−1,041), crosses zero by d18 (+621) and reaches +5,923 by d29. Both
  candidates land within 90 coins of each other at the end **by different paths** — flow218 is
  ahead of B at d8, flowq2 is behind — which is the knife-edge board signature, not a shared
  mechanism.

**One mechanism or diffuse drift? Diffuse drift on a knife-edge board set.** The macro is
identical; a single tile's worth of micro difference decides ±5,000 coins.

---

## Q3 — expected value of the running ES portfolio

### The noise floor, measured

`JAX_PLATFORMS=cpu .venv/bin/python S/esplateau/pool_dist.py` (36 judged candidates with full
90-board band coverage) and `S/esplateau/shrink.py` (the 22 ES-from-B checkpoints):

```
mean per-board se of ONE pooled-band read   =  182 coins
observed spread of the 22 ES reads      sd  =  188 coins
=> true-effect spread tau                   =   47 coins   (shrink factor 0.06)
prior mean of an ES checkpoint's true effect = -124 coins
```

| candidate | observed | se | t | EB true effect | 95 % CI |
|---|---:|---:|---:|---:|---|
| flow218_g110_hr | **+302** | 228 | +1.32 | **−97** | −187 … −7 |
| flowq2_g150_hr | **+295** | 173 | +1.71 | **−98** | −188 … −8 |
| flow218_g130_hr | +86 | 224 | +0.38 | −111 | −201 … −21 |
| flowq3_g60_hr | +26 | 233 | +0.11 | −115 | −205 … −25 |
| flow218_g270_hr | −57 | 252 | −0.23 | −120 | −210 … −30 |
| flow218_g40_hr | −426 | 214 | −1.99 | −144 | −233 … −54 |

The best reading in the whole pool is +302. A mean-zero candidate judged on 90 boards has
se 182; the expected maximum of 30 such draws is +2.04 σ = **+371**. The observed maximum is
*below* what pure selection noise produces from the number of candidates already judged. Nothing
in the pool requires a true positive effect to explain it.

The same is true on the "first candidate to beat B at B's own real gate": flow218_g110's
61.3 % / +3,265 vs B's 57.3 % / +3,028 is, when paired board-by-board on those same 62 LIVE62
boards, **+129 coins, t +0.48**.

### The bar and the noise are the same size

Also from `S/esplateau/shrink.py` (per-board sd of a paired Δmargin ≈ 1,724 coins):

| pooled boards | se of the read | +450 is | P(a true-zero candidate reads ≥ +450) | P(≥1 of 30 does) |
|---:|---:|---:|---:|---:|
| **90 (today)** | **182** | 2.48 σ | 0.0066 | **0.181** |
| 120 | 157 | 2.86 σ | 0.0021 | 0.062 |
| 180 | 129 | 3.50 σ | 0.0002 | 0.007 |
| 240 | 111 | 4.04 σ | ~0 | 0.001 |

At 90 boards the §115 t ≥ 2 test is *not* a second check on the +450 test — +450 **is** t 2.48 —
so §115 is one 2.5 σ test, and with ~30 candidates judged it has an 18 % chance of promoting a
theta with no effect at all. Conversely, a candidate whose true effect is the +300 ES has never
actually delivered would clear the bar only **20 %** of the time on 90 boards.

### The lineage is a random walk, not a descent

`JAX_PLATFORMS=cpu .venv/bin/python S/esplateau/norms.py`

| theta | \|d\| from B | max\|d_i\| | cos with d(flowq2_g150) | cos with d(flow218_g110) |
|---|---:|---:|---:|---:|
| flow218_g10 | 0.88 | 0.028 | 0.002 | 0.508 |
| flow218_g110 | 2.45 | 0.118 | 0.000 | 1.000 |
| flow218_g270 | 3.70 | 0.166 | 0.008 | 0.707 |
| flowq2_g150 | 2.70 | 0.163 | 1.000 | 0.000 |
| flowq3_g60 | 3.34 | 0.175 | 0.821 | −0.006 |
| flow216_g70 | 1.89 | 0.084 | −0.008 | 0.005 |
| flow219_g70 | 1.94 | 0.085 | 0.021 | −0.001 |

`|B| = 18.11`, `cos(d1,d2) = 0.0004`, `|d1+d2| = 3.65`, `|(d1+d2)/2| = 1.83`.
Displacement grows ≈ √gens (0.88 at g10 → 2.45 at g110 → 3.70 at g270; √t would predict
2.92 / 4.57) and every lineage is orthogonal to every other. That is diffusion with at most a
marginal drift — the signature of an ES whose gradient estimate is below its own step noise,
which is the same conclusion `docs/strategy/2026-09-14-sim-gate-gap.md` reached from the other
end (the in-sim objective and the gate are *anti*-correlated).

### Is pooled ≥ +450 with t ≥ 2 credible from continued fixed-sigma ES from B?

**No.** Three independent readings agree: (i) the true-effect spread across 22 checkpoints is
τ = 47 coins about a mean of −124, so there is no +450 in the reachable set; (ii) the best of
~30 draws is below the selection-noise expectation; (iii) the lineages diffuse rather than
descend. The only way a +450 appears is as an 18 %-per-30-candidates false promotion — which is
worse than no candidate, because it ships a theta whose EB estimate is −97.

### The options, ranked

| rank | option | one-line justification |
|---|---|---|
| **1** | **(e) stop ES from B, spend the GPUs elsewhere** | τ = 47 coins about −124: the *whole* reachable set of fixed-sigma ES from B is inside the judge's noise, and the macro (`quads`) never moves, so the action interface — not the search — is the binding constraint (`codex-blind-review-2026-09-11`, `forced-opening-ramp-2026-09-09` FORWARD_ADMIT is still unbuilt). |
| **2** | **(d) larger pinned fitness set / more real-gate boards** | The only option that changes anything measurable: 180 pooled boards cuts se 182 → 129 and drops the 30-candidate false-promotion rate 0.181 → 0.007. It buys **honesty, not a winner** — it cannot manufacture an effect that τ says is not there. Do it *if and only if* ES continues; ~2× the judge cost. |
| **3** | **(c) averaging / summing independent record deltas** | Already running, cheap, and worth finishing *as a falsifier*. Prediction from the |d|-vs-read fit (r +0.56, slope +147/unit |d|): B+d1+d2 (|d| 3.65) reads **≈ +126 ± 200** and B+(d1+d2)/2 (|d| 1.83) **≈ −143 ± 200** — i.e. indistinguishable from flow218_g270 (|d| 3.70, −57) and flow218_g50 (|d| 1.76, −200). Additivity would also double the *g*-loading (β 0.75 + 1.13 = 1.88 on a factor worth −534/board). If the sum reads > +450 at t ≥ 2, that is new information; expect it will not. |
| **4** | **(b) restart-from-record with a new seed** | Draws one more sample from the same N(−124, 182) distribution. flow216/flow219/flowq1/flowq4 already are that experiment: −331, −335, and both flowq arms rejected. It adds a candidate to the selection pool, which *raises* the false-promotion rate without raising the truth. |
| **5** | **(a) sigma schedule** | **The premise is wrong**: `--stall-sigma-mult` is floored at 1.0 (`scripts/train.py:2730-2735` raises SystemExit below it; help at `:2422-2429`); it *multiplies* sigma on a stall and cannot shrink it. The shrink experiment has already been run by hand — flowq3 = refine from flowq2_g150 at sigma 0.005 — and read **+26** (from +295). Dead. |

---

## RECOMMENDATION (tonight)

Kill the fixed-sigma-from-B ES portfolio and stop adding candidates to the selection pool. On
this box that is the one local arm, `flowl4` (`--run flowl4 --sigma 0.005 --stall-sigma-mult 1.0`
from `flow193_g100_hr_pad7065.npy`, seed 333) plus its `queue_local3.sh` successor; on the remote
host the same applies to every `flowq*`/`flow219` arm still launched from B at fixed sigma — none
of them can produce a candidate whose true band effect exceeds −50, and each one it does produce
raises the chance of a noise promotion. Let the two sum/average candidates the judge is already
chewing on (`B + d1 + d2`, `B + (d1+d2)/2`) finish, because they are the cheapest falsifier of
this whole report — write down the prediction first (**+126 ± 200** and **−143 ± 200**; anything
above +450 at t ≥ 2 overturns the EB fit) — and judge nothing else from this family. Before any
future ES arm is launched from B, change the *measurement* first: extend the pooled band from 90
to ≥ 180 boards (`S/livec/ids.txt` has unused ids past 102; NEXT30 can be extended from
`nextband_B_ext.csv`), which cuts the read's se from 182 to 129 and the 30-candidate
false-promotion rate from 18 % to 0.7 %; and re-express §115 as a single `t ≥ 3` test, since at
90 boards "+450 **and** t ≥ 2" is one 2.48 σ test wearing two hats. The GPUs freed should go to
the thing the receipts say ES cannot touch: `quads` is 3 on 180/180 rows for B and for both
records, so no amount of fixed-sigma drift in the 6,789-float lattice ever changes the opening —
the FORWARD_ADMIT action-interface work (`forced-opening-ramp-2026-09-09`) and the macro-executor
path (`tape-seeded-path-2026-09-14`) are where a +450 could actually come from.

---

## Files

| file | what |
|---|---|
| `S/esplateau/corr.py` | per-board Δ vectors + Pearson/Spearman/sign split, per leg |
| `S/esplateau/matrix.py` | pairwise r matrix over many candidates (the null control) |
| `S/esplateau/factor.py` | generic move-off-B factor, residual correlation, lineage spread |
| `S/esplateau/behav.py` | behaviour-column deltas from the judge CSVs + top gain/loss boards |
| `S/esplateau/pool_dist.py` | distribution of the pooled statistic over all 36 judged candidates |
| `S/esplateau/shrink.py` | empirical-Bayes true effects, bar-vs-noise table, power table |
| `S/esplateau/norms.py` | theta delta norms / cosines / lineage diffusion |
| `S/esplateau/trace.py` | day-by-day tile/hand/money trace on a pinned board (~10 min JIT) |
