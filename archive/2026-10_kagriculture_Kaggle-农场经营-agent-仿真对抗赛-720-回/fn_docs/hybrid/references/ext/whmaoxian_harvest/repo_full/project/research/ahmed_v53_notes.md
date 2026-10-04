# Kaggriculture V53 — Opening Signature and Current-Meta Sale Streams

V53 keeps the exact V52 farm, route, and market policy. It adds executed premium-product sale histories from the public [Pipe16 idle-workers](https://www.kaggle.com/code/nathanjacob/kaggriculture-pipe16-idle-workers) and [More Wheat, Smarter Sales](https://www.kaggle.com/code/dmitriigluzdov/kaggriculture-more-wheat-smarter-sales) agents to V52's existing opponent-sale forecaster. A public wheat-inventory change at the second step distinguishes the V52-like 30-unit market opening from the newer opening: V52-like matches keep the original forecast library. No rival name or private data is used.

Paired local evaluation against the exact V52 source, four reacting public agents plus a V52 mirror, both seats. W/L/T are wins/losses/ties; margin and own cash are mean candidate-minus-V52 dollars per game. The ranking holdout and unmodified-engine seeds were frozen before play.

| Set | V52 W/L/T | V53 W/L/T | Points | Margin | Own cash |
|---|---:|---:|---:|---:|---:|
| 8-world pilot | 29/37/14 | 33/33/14 | +0.050 | +185.2 | +110.5 |
| 20-world cash-gate study | 92/68/40 | 104/56/40 | +0.060 | +164.5 | +30.0 |
| 20-world ranking-gate study | 90/70/40 | 96/64/40 | +0.030 | +171.4 | +68.7 |
| 60-world pooled confirmation | 273/209/118 | 302/180/118 | +0.048 | +160.6 | +53.4 |
| 8-world unmodified engine | 38/26/16 | 38/26/16 | +0.000 | +89.0 | +28.6 |

Two earlier single-set gates failed: the cash-gate study missed its +$75 own-cash threshold, and the ranking-gate study missed its +0.04 points threshold and had a Dmitrii subgroup loss. The unchanged source was then tested once more on fresh worlds under a preregistered 60-world pooled criterion; the failed single-set gates remain reported. The pooled world-cluster 90% margin interval is [+93.1, +233.7]. In four V52-like mirror fixtures, all 719 actions matched V52 exactly. Normal-GC isolated runtime was at most 20.22 ms on the measured Windows host. Local results do not guarantee a live ladder rating.

Run all three code cells below on Kaggle CPU. The complete tested agent is embedded, requires only Python's standard library, and needs no notebook inputs, downloads, training or GPU. The final cell builds `submission_competitive_v53.tar.gz` containing only `main.py`. It does not submit to the competition.

Credits: Ahmed Berat Ozer (V52, stream recording, opening classifier and V53 integration); Nathan Jacob and Dmitrii Gluzdov (public agent sale streams); Thomas Tschinkel, yhay81, destbreso, prvsiyan, aurax7, tetsutani and other upstream authors retained in `main.py`. Apache-2.0 notices are retained in the source.

Agent SHA256: `20fe549dd4573b9fd1dfb32a1782c205fa74f0edfdfd6cbe935079533e0a9d0e`.
