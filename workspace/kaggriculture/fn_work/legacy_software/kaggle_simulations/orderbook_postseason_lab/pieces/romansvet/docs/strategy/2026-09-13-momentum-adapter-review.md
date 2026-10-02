# Market-momentum adapter: reach and conditional next experiment

2026-09-13. This is a source and saved-evidence review. It does not change the
frozen momentum stage, run a game, fit another predictor, or authorize a new
training run. The seed-311 and seed-312 experiments remain separate fixed
lineages.

## What the 66-coordinate adapter can change

The current adapter has a credible path to multi-day crop decisions. At each
dawn, `brain.market_momentum` forms one normalized scalar per product,

```
(previous_dawn_inventory - current_dawn_inventory) / T
```

where `T` is the existing product-specific market scale
(`S/unitorder/momentum_stage_20260913/src/kagg3/core/brain.py:128-134`). Runtime
rotates this history once per new observed dawn and rebuilds one complete daily
plan (`agent/runtime.py:42-59`); the simulator carries the same previous-dawn
state between days (`sim/rollout.py:491-519`). This is daily feedback, not an
intraday reaction or recurrence within the cached plan.

The two trained blocks enter live decoder paths:

- `mh (1,64)` adds the scalar to the product encoder before `tanh`; `ms (1,2)`
  adds it directly to grow and sell scores (`core/policy.py:650-659`). The
  scores set animal mix and the crop planting distribution, including maturity
  and residual-demand masks (`core/brain.py:955-1039`). They also feed the sell
  gate and hold quantities.
- The product scores and sell pressure are flattened, not pooled, and pass
  through the already-trained `gp` block into the global hidden state
  (`core/policy.py:663-677`). Thus momentum can also move land bias,
  development fraction, animal share, hiring, crew ramp, and forward-admit
  horizon. It need not alter the frozen 6,789-coordinate prefix to reach those
  decisions.

The saved one-row liveness check confirms the immediate arithmetic rather than
the whole causal chain. A normalized MILK input of `1.0` produced the exact
declared `ms` score delta `[0.5, 0]` and a first-hidden-coordinate `mh` delta of
`0.2478703856`; NumPy and JAX agreed within `7.75e-7`
(`S/unitorder/momentum_signal_20260913/receipt.json`). The 120-dawn compatibility
and package checks establish zero-weight identity, not that a learned adapter
changes a useful complete plan
(`2026-09-13-momentum-stage-integration.md`).

The training setup can therefore discover a daily market-conditioned policy in
principle. It perturbs and updates only these 66 coordinates, with population
4,096, sigma 0.01, ten generations, and the exact 120 tapes plus four carried
archetypes; the old prefix remains fixed
(`S/unitorder/momentum_train.py:80-98`,
`2026-09-13-momentum-training-plan.md`). This is enough reach for a bounded
experiment. It is not evidence that the shared-stock signal identifies the
opponent, forecasts price causally, or improves judge results.

## The material representation risk

Both new matrices are shared across products. Equal normalized movement gives
every product the same direct two-score shift through `ms`. The `mh` shift also
uses one common hidden direction; its effect can vary with the existing product
state through the `tanh` derivative and frozen downstream weights, but it cannot
learn an independent input direction for each product.

That restriction matters because the saved fixed prediction result is strongly
heterogeneous. Previous-dawn inventory reduced mean squared error by 13.04% for
MELON, 7.52% for FERTILIZER, 5.13% for MILK, and 4.34% for STRAWBERRY, but only
0.49% for CARROT and 0.81% for WOOL. CARROT and TOMATO also had worse mean
absolute error and negative median episode improvement. These are separate
product results over 120 leave-one-episode-out folds; they must not be averaged
into a policy claim (`2026-09-13-momentum-prediction-check.md`, saved metrics SHA
`33cbffabc6e5f84dca2ee99fbce4405413b76baad8a41bfbbd15924295e75a07`).
The target is aggregate town-plus-both-seat market movement, so even the strong
products do not identify opponent selling or a profitable response.

Prior experiments make a hard-coded response especially unsafe.
`OPP_SUPPLY_ON` reduced our late book without moving the tape opponent's units
and lost at every tested dose (`2026-09-11-oppsupply-screen.md`). The interday
half of `OPP_FRONTRUN` also lost, while its surviving intraday half failed the
multi-family promotion rule (`2026-09-11-oppfrontrun-engine.md`). Those tests do
not close a learned lag feature, but they show why a common “stock fell, sell or
plant less” sign is not a sound fallback. The old Flow215 population also showed
the configured blended gradient following own coins on 622 of 855 disputed
antithetic pairs, with held-out opponent-purse transfer afterward
(`2026-09-13-flow215-objective-alignment.md`). A new adapter still uses that
objective, so its own-versus-relative alignment has to be observed rather than
assumed.

## One experiment if both fixed lineages fail

Keep the two current lineages at their prescribed ten generations. One proposed
follow-up is a **product-indexed direct-score adapter generation-zero audit**:

1. Starting from the same 6,789-coordinate B, append one zero-initialized
   `ms_product (9,2)` block. Decode it as elementwise
   `momentum[p] * ms_product[p,:]`. Keep every old coordinate fixed and trainable
   support exactly the new 18 coordinates. This permits a different grow/sell
   sign for each product while retaining the already-qualified history,
   normalization, daily cadence, and direct score-to-plan path.
2. Run two independently seeded, no-update generation-zero populations of
   4,096 on the same frozen 120+4 training field. Preserve candidate epsilons,
   both pre-rank objective components, shaped advantages, product-block
   gradients, and complete-plan change counts. Do not open judge families or
   apply an optimizer step.
3. Before reading the result, freeze a permutation/sign-flip null for the
   cross-draw gradient cosine. Also report whether the blended antithetic
   preference follows own coins or relative margin on every disputed pair,
   using the existing objective-alignment algebra. Advance to any training only
   if the 18-coordinate direction is reproducible, changes relevant plans, and
   is not driven by the same own-purse/opponent-purse conflict. A negative result
   would argue against this specific follow-up; it would not rule out other
   market-history representations. These are proposed diagnostic criteria,
   not a new mandatory gate for every future experiment.

This tests one precise explanation for two failed shared-adapter lineages:
cross-product cancellation. It is smaller than another ten-generation arm and
does not reuse evaluation families, pool them, or repeat the saved ridge fit.
Opponent public-forecast revision remains a distinct future signal, but its
existing review requires an incremental-information check before policy work
(`2026-09-13-other-momentum-review.md`); failure of market momentum alone would
not supply that missing evidence.
