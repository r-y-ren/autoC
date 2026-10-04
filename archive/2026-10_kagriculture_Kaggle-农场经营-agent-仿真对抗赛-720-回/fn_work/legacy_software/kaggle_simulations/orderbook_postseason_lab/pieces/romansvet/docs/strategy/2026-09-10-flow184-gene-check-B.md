# flow184 gene check — independent second read (B)

Blind of the first check. 2,400 decisions of `tests/data/trajectory_obs.npz`,
`PLANT_FLOOR_ON = True`, slope-repair worktree.

## 1. Decode

`flow184_mean_now.npy` and `flow184_g10r.npy` are **byte-identical** — one trajectory point,
not two: no per-generation slope is readable (`flow184_g10_hr` = zero block).
Mean logit, WHEAT/CARROT/TOMATO/STRAWBERRY/MELON:

    +0.0013   -0.1698   -0.2195   -0.1789   -0.1709

**Nonzero floor: 0.00 % on every crop**, all 12,000 decodes; max logit +0.043, under the
+0.0625 first step.

## 2. Null

Block norm **0.1974** (0.01536/coord); the noise walk
(`grad=(adv[:h]−adv[h:])@eps/(pop·σ)`, sgd `lr·m`) gives 0.018/coord at pop 96, 17 gens.
**Distance travelled is exactly noise; all signal is direction.** With that rms as the null
scale (conservative), mean-logit sd 0.047: melon **z = −3.64** (MC p = 1e−4); four crops at
≤ −0.15 jointly **0 of 200,000 draws**; their `g12` columns at cos −0.58…−0.73 to mean `gh`
(null sd 0.177).

Population expression (σ 0.02, 192 members), gen 0 → gen ≤17:

    WHEAT 18.1 -> 19.6 %   CARROT 21.0 -> 0.13   TOMATO 17.6 -> 0.05
    STRAWBERRY 20.6 -> 0.67   MELON 18.7 -> 0.54

Wheat — the crop the incumbent already plants — is the untouched control. Drift cannot
collapse four crops 30x and leave the fifth exact.

## 3. Verdict

**(b) alive and selected against**, p < 1e−5, converged. Members decoding a floor lost; the
mean slid until the cloud stopped reaching the step. Melon sits 3.21 member-sd below it —
the gene is going *dark*, past which (b) and (c) stop being separable.

Gen 100 separates them only on the wheat control (b: wheat ~19 %, the four <1 %; c: wheat
drifts too, or all five move symmetrically) and on day conditioning — day ≤1 expression
diverging from later days, the sole evidence of the "melon on day 0 only" theta this gene
exists to find.

## 4. flow184b

Unsound. `gb12[melon]=+0.30` (2/16) puts the *whole* population on a floor (spread 0.073):
it hard-codes the corner rather than searching for it, voiding H2's "NOT A FORCED OPENING",
and moves the start, not the gradient — the descent covering 0.17 in ≤17 generations covers
0.30 in ~30–50 more.

`w = floor + (1−Σfloor)·w` is a **swap**, the displacement signature the archive closed:
`MELON_OPEN` 54.2→15.1 % (−17,554); pinned judge 1.9 % at 12 tiles, 3.8 % at 8;
additive-melon §1 — pot reachable, still −15…20k over d12-29. Top-ten rungs at 40 % cannot
flip that: topb-anatomy §1 has the d10–14 melon hole as one we win back (107244957 −645 on
−22,133/+22,592). Expect it switched off again, more slowly. Cheaper: gate the floor to
day ≤1.
