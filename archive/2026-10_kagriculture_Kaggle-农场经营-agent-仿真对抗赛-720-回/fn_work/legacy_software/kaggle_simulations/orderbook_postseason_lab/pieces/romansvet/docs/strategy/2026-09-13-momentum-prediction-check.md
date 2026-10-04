# Daily market-stock history prediction check

Adding previous-dawn stock movement improved mean squared prediction error in
all nine products in this fixed check. The evidence is more consistent across
episodes for melon, egg, milk, fertilizer and strawberry. Carrot and tomato
have negative median episode improvements and worse mean absolute error despite
positive average squared-error changes. These are prediction results, not gains
in planting decisions, game score or Kaggle rank.

The single run used the audited 120 Flow215 training episodes, with 120 distinct
board seeds. Both seats were held together in each leave-one-episode-out fold.
There were 6,720 eligible seat rows (days 1–28), with each episode/product metric
averaging its two dependent seat perspectives. Episode/source IDs are metadata,
not features. No judge replay was used. One submission appears per episode, but
team or strategy independence is not established.

The baseline contains all 234 existing neural feature columns: current product,
global, residual-demand, production-forecast and forward-value inputs. The
augmented model adds nine `(inventory[d-1] - inventory[d]) / T` values. Both
predict `(inventory[d] - inventory[d+1]) / T`. Per-fold scaling and centering use
training rows only. Ridge regularization was fixed at 0.01 in the mean-squared
objective, with an unpenalized intercept and float64 arithmetic. No coefficient,
feature, horizon or regularization search followed the results.

| Product | Mean squared error reduction | Mean absolute error reduction | Episodes with lower squared error |
| --- | ---: | ---: | ---: |
| WHEAT | +1.75% | +0.55% | 60/120 |
| CARROT | +0.49% | -3.87% | 42/120 |
| TOMATO | +7.45% | -0.45% | 43/120 |
| STRAWBERRY | +4.34% | +3.02% | 77/120 |
| MELON | +13.04% | +8.54% | 85/120 |
| EGG | +4.88% | +1.45% | 90/120 |
| MILK | +5.13% | +3.37% | 92/120 |
| WOOL | +0.81% | +0.04% | 78/120 |
| FERTILIZER | +7.52% | +5.01% | 93/120 |

Percentages compare mean per-episode errors; products are never averaged into
one score. Counts and medians describe this sample, without significance or
policy-benefit claims. Current demand is already in the baseline; the target
still includes town consumption and both players. It is not opponent selling.
A positive result supports a bounded policy-feature experiment. A null result
would only apply to this model and one-day horizon.

The fit completed once in 13.103 seconds (14.146-second wrapper), under its
600-second cap. Root checked all label/lag rows and episode/product error
arithmetic. Sol independently reconstructed only the first held-out fold, and
both 56×9 prediction matrices matched exactly; all folds received coverage,
scaling-hash and metric audits. Inputs and helper remained unchanged.

- `receipt.json` SHA-256: `32f325dfbb37ef199bd3795de4878c17e6cd1a12dafd2ee9589b108c835a854e`.
- `predictions.npz` SHA-256: `863a36085c83deb3e455fceb1e74285082064b38603035f41c48fab8b7bd572c`.
- `metrics.json` SHA-256: `33cbffabc6e5f84dca2ee99fbce4405413b76baad8a41bfbbd15924295e75a07`.
- `root_saved_audit.json` SHA-256: `47f8e10b4ef0ca35fbed32bd0f5c3b77649810c0792f926c3d8d235441efd96e`.
- `sol_saved_audit.json` SHA-256: `b8b8d9e72beefc60203d00ca806f65e29fb5e451a3ddf740a8915cb12cbfdd8b`.

Protocol: `S/unitorder/momentum_predict_manifest.json`, SHA-256
`cdc235eeb30d15204cbbd8606b5bf5cb4581180ed9bcf22569041937da2bd8bf`.
Helper: `S/unitorder/momentum_predict.py`, SHA-256
`a0708d4247f7af57e3534e510a0ea1bdfb4fbc0e66821f639d99de76d3dda83b`.

The resulting implementation stage appends 66 zero-initialized parameters to
original B and carries one prior dawn inventory. It remains isolated from the
submitted agent and the completed seed309/310 checkpoints. Compatibility checks
and actual training-initializer verification precede any momentum training run.
