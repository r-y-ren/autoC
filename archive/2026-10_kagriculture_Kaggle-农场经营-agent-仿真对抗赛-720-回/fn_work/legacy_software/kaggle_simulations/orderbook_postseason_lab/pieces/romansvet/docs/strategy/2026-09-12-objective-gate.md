# The §107 objective read at four independent pinned-board draws — the flow211 gate

*2026-09-12. `S/objaudit/obj_rungs.py` (extended), `S/objaudit/run_gate.sh`,
`S/objaudit/obj_rungs_seeds.md`, `S/objaudit/obj_rungs_gate.json`.*

## Question

§107 measured, from **one** draw, that the flow209 g20 step is a *transfer*:
TOPTEN +461 (t 2.0) and LOSS10 +565 (t 2.1) bought with LIVEC42 −382 (t −1.6)
and W2 band −249 (t −1.3), with the objective-weighted win flat
(0.5904 → 0.5859). flow211's re-weighting (top-ten 32.7 → 10 %, NEXT30 38 %)
was staged on that reading, and §107 set the launch gate:

> over 4 independent batch seeds, both band families (LIVEC42, W2) negative and
> TOPTEN positive, pooled |t| ≥ 2 on each of those three.

## Method — and why the seed had to be a *board* seed

The trainer draws one seed word per episode slot from its own
`np.random.default_rng(--seed 309)` (train.py:3771/3818; `obj_rungs.py`
line ~34). But under `--pinned-once --pinned-fixed-seed`,
`Trainer.pinned_seeds` (train.py:4701-4728) **overwrites** the drawn word of
every pinned slot with `pinned_seed_word(name)` =
`blake2b(name, key=PINNED_SEED_SALT)` — a function of the tape id alone. With
196 of 198 slots pinned, `--shop-crn` on and `market_jitter = 0`, re-seeding
that draw changes only the two carried residual pairs and the self-play slots:
**one family out of seven, and none of the three the gate names.** A
`--batch-seed` gate would have been four copies of the same measurement.

The replicate exposed instead is `--word-offset K`: every pinned word is
re-derived as `blake2b(f"{name}#{K}", key=PINNED_SEED_SALT)`, i.e. every pinned
rung plays a *different fixed board*, which is exactly the question the gate
means to ask ("was that family's verdict about the theta or about those
boards?") and exactly what train.py's own `PINNED_SEED_SALT` docstring
describes as the way to ask it. Offset 0 is the stock board set, byte-for-byte,
so §107's numbers are reproduced as seed 0. `--batch-seed` is exposed too, and
`--offsets 0,1,2,3` additionally sets batch-seed = 309 + K so the
residual/self-play slots are independent replicates as well.

Within an offset, B and the g20 centre play the **byte-identical** batch
(paired/CRN, one `_play` call, pop = 2). Across offsets the board sets are
disjoint draws, so offsets are independent replicates.

Ladder: flow211's expanded 196-rung ladder
(`S/famgrad/launch_flow211_expanded.sh`, §105's ladder), which is flow209's 166
rungs on their same pinned words **plus the 30 NEXT30 tapes** — so NEXT30 comes
out as the seventh family in the same run. A per-family Δmargin is an
unweighted mean over that family's episodes, so it does not depend on which
launcher's weights are in force; only the weighted-win line does, and both
weightings are printed.

Pooling: each offset contributes one family mean; the pooled mean is the mean of
the four, `SE(between)` is their sample SE (df 3) and `SE(within)` is
`sqrt(Σ se_i²)/4` (the paired within-offset noise). `SE(between)` already
subsumes the within-offset noise, so the gate is read on the **more
conservative** of the two t's.

## What the word offset can and cannot re-roll (the binding caveat)

Every rung on this ladder is a `--with-town` tape. train.py's own
`pinned_fixed_seed` docstring (train.py:261-272) says what that means:

> A `--with-town` tape pins the *shops* (`sim.eod.unlock_shop`), which is the
> big lottery and the reason the rung is called pinned at all. It does not pin
> the rest of the day generator: `sim.eod.spawn_weeds` still walks two words per
> empty tile out of `eod.host_stream(seed, day)` …

So the seed word controls **the weed history and nothing else** on these rungs.
Changing it (the `--word-offset`) gives an independent *weed* draw on the *same*
196 games; it cannot give a different shop draw, a different town, a different
opponent or a different tape. There is therefore **no knob anywhere in this
estimator that makes the 196 boards independent** — they are a fixed, chosen
set, and the honest sampling unit is the rung, not the seed.

That changes how the gate must be read:

* **t(board)** — average each rung's Δ over the four weed draws (this is the
  variance reduction the replicates actually buy), then take the SE *across the
  rungs in the family* (n = 42 LIVEC42, 85 W2, 20 TOPTEN, 30 NEXT30, 10 LOSS10,
  9 TOP50). This is the statistic that answers "is this family's transfer real
  for these boards"; it is the one the gate is read on below.
* **t(between offsets)** — the spread of the four family means. Because the
  boards are identical, this measures the *weed* noise alone. It is reported as
  a stability check; a large t there is not evidence about the families, and a
  small one is not evidence against them.
* Neither statistic can speak to board-set selection: the LIVEC42 / W2 / TOPTEN
  / NEXT30 sets are the ladder's own, and a family Δ measured on them
  generalises only as far as §101's held-out reads say it does.

## Results

### Per weed draw (word offset): Δmargin = g20 − B, coins/episode, within-draw t across the family's rungs

| family | rungs | off 0 | off 1 | off 2 | off 3 | signs |
|---|---|---|---|---|---|---|
| LIVEC42 | 42 | -353 (-1.48) | -158 (-0.73) | -510 (-2.49) | -357 (-1.62) | 4/4 − |
| W2 band | 85 | -247 (-1.33) | -115 (-0.68) | -229 (-1.49) | -275 (-1.52) | 4/4 − |
| LOSS10 | 10 | +549 (+2.13) | +615 (+2.59) | +584 (+2.07) | +639 (+2.63) | 4/4 + |
| TOPTEN | 20 | +450 (+1.92) | +961 (+2.61) | +457 (+1.58) | +156 (+0.76) | 4/4 + |
| TOP50 | 9 | -598 (-0.61) | -400 (-0.41) | -845 (-1.03) | -653 (-0.69) | 4/4 − |
| NEXT30 | 30 | +258 (+1.19) | +70 (+0.32) | +234 (+1.08) | +170 (+0.79) | 4/4 + |
| self-play | 4 | +1437 (+0.74) | -10 (-0.00) | +1228 (+1.42) | -1091 (-0.42) | mixed |

### Pooled — board level (per-rung Δ averaged over the 4 weed draws, SE across the family's rungs)

| family | rungs | mean Δ | SE | **t(board)** | rungs neg | Bwin | Gwin | weed SD/rung | t(between draws) |
|---|---|---|---|---|---|---|---|---|---|
| LIVEC42 | 42 | -344 | 203 | **-1.70** | 64 % | 0.875 | 0.815 | 400 | -4.78 |
| W2 band | 85 | -216 | 151 | **-1.43** | 61 % | 0.788 | 0.794 | 455 | -6.19 |
| LOSS10 | 10 | +597 | 248 | **+2.41** | 20 % | 0.000 | 0.075 | 144 | +30.76 |
| TOPTEN | 20 | +506 | 169 | **+2.99** | 25 % | 0.362 | 0.413 | 510 | +3.03 |
| TOP50 | 9 | -624 | 899 | **-0.69** | 67 % | 0.361 | 0.361 | 528 | -6.81 |
| NEXT30 | 30 | +183 | 203 | **+0.90** | 50 % | 0.642 | 0.667 | 284 | +4.35 |
| self-play | 4 | +391 | 1067 | **+0.37** | 25 % | 0.500 | 0.438 | 3429 | +0.66 |

### Aggregates (board level)

| group | rungs | mean Δ | SE | t |
|---|---|---|---|---|
| BAND sold (LIVEC42 + W2) | 127 | -259 | 121 | -2.14 |
| BAND + TOP50 | 136 | -283 | 126 | -2.24 |
| BOUGHT (TOPTEN + LOSS10) | 30 | +536 | 138 | +3.90 |
| BOUGHT + NEXT30 | 60 | +360 | 124 | +2.91 |
| all 196 pinned rungs | 196 | -86 | 98 | -0.88 |

### Win scalars (Δ = g20 − B, over the 4 draws)

| scalar | off 0 | off 1 | off 2 | off 3 | mean | SE | t |
|---|---|---|---|---|---|---|---|
| mean_win (unweighted, train.py's log line) | +0.0000 | -0.0050 | +0.0200 | -0.0100 | +0.0012 | 0.0066 | +0.19 |
| flow211-weighted win (this ladder's ep_weight) | +0.0155 | -0.0127 | +0.0183 | +0.0065 | +0.0069 | 0.0070 | +0.98 |
| flow209-weighted win (§107's objective) | -0.0029 | +0.0100 | +0.0165 | +0.0036 | +0.0068 | 0.0042 | +1.63 |

### GATE (both band families negative and TOPTEN positive, pooled |t| ≥ 2 on each)

| family | required | mean Δ | t(board) | t(4 draws as independent episodes) | sign 4/4? | verdict |
|---|---|---|---|---|---|---|
| TOPTEN | positive, \|t\| ≥ 2 | +506 | **+2.99** | +3.60 | yes | PASS |
| LIVEC42 | negative, \|t\| ≥ 2 | -344 | **-1.70** | -3.13 | yes | FAIL |
| W2 band | negative, \|t\| ≥ 2 | -216 | **-1.43** | -2.50 | yes | FAIL |

**GATE FAIL on the board-level statistic.**

Offset 0 reproduces §107's single draw inside ~30 coins on every family
(LIVEC42 −353 vs −382, W2 −247 vs −249, TOPTEN +450 vs +461, LOSS10 +549 vs
+565); the residue is the ladder (196 vs 166 rungs shifts the residual pairs and
the per-rung seat stagger), not the pinned boards.

## Verdict

**GATE FAIL as written.** The *direction* is not in doubt — every one of the
three families has the predicted sign on all four draws, and the two band
families are negative on 61-64 % of their individual rungs — but the
|t| ≥ 2 requirement is met by TOPTEN alone (+506, t +2.99). LIVEC42 (−344,
t −1.70) and W2 (−216, t −1.43) fall short.

**The gate cannot be rescued by more seeds.** Because the pinned word moves only
the weeds, the four draws are four measurements of *one* board set; their spread
(t between draws −4.8 / −6.2 / +3.0) is weed noise, and pooling the four as if
they were independent episodes (t −3.13 / −2.50 / +3.60, which would read PASS)
double-counts the same 196 games. The uncertainty that matters is board-to-board
(SD/rung ≈ 1,300-1,400 coins vs a weed SD/rung of 400-510), so reaching |t| ≥ 2
needs **more tapes**: 59 LIVEC42-style boards (have 42) and 166 W2 boards (have
85). Four more seeds buy nothing.

**What does clear the bar.** Taken together as "the band", LIVEC42 + W2 is
**−259 SE 121, t −2.14** over 127 boards (−283, t −2.24 with TOP50), and the
bought side TOPTEN + LOSS10 is **+536 SE 138, t +3.90** over 30. So the
*transfer* itself — band margin sold, top-tier margin bought — is established at
|t| > 2 on both sides; what is not established at |t| > 2 is the claim about
each band family **separately**, which is what the gate asked for.

**NEXT30 did not pay for it.** The seventh family is **+183 SE 203, t +0.90**
(positive on all four draws, 50 % of its rungs negative): the g20 step sold the
LIVE-C/W2 band, not the 2550-2750 band. This qualifies §107's consequence (3):
cutting top-ten 32.7 → 10 % does remove the transfer's *destination*, but
raising NEXT30 to 38 % enlarges a family that sits on the **bought** side of
this step, not its source. flow211 remains a sampling/support A/B (§105: the
two objectives' directions correlate ρ 0.93 disattenuated), and its rationale
should be stated as "less weight on a destination that pays nothing held-out
(§101)" rather than "more weight on the source of the transfer".

**The objective is still blind to the trade.** Over the four draws the
flow209-weighted win moves +0.0068 (SE 0.0042, t +1.63), the flow211-weighted
win +0.0069 (t +0.98) and the unweighted `mean_win` +0.0012 (t +0.19), while
all 196 rungs together are −86 coins/episode. Rank-normalised win is indifferent
to a trade that costs ~260 coins on 127 band boards to gain ~540 on 30 top-tier
ones; the held-out engine judge (LIVE-C hold-outs, LIVE62, NEXT30 provenance) is
not. That is §107's finding, and it survives four draws.

## Caveats

1. The four replicates are **weed** draws, not board draws (see above). No knob
   in this estimator can make the 196 boards independent.
2. Family membership is the ladder's own labelling (`rungmap.csv` +
   `S/nextband/ids.txt`); LOSS10 (10 rungs) and TOP50 (9) are small, and TOP50's
   board-level SE (899) makes its −624 uninformative.
3. Self-play is 4 episodes with a weed SD of 3,429 per rung; its +391 is noise
   and should not be read as §107's −543 reversing.
4. Everything here is *in-sample* by construction — these are the rungs the arm
   trains on. It says what the objective rewards, not what the judge will see;
   §101/§106/§107's held-out engine reads remain the promotion evidence.
5. The ladder is flow211's expanded 196-rung one, run at pop 2 with the centre
   theta only (no perturbation), `--chunk 64` on the local 3070.
