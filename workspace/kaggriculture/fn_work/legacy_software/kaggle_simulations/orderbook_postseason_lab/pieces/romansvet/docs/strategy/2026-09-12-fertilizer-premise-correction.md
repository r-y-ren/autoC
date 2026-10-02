# Correction: the clone does not buy cheap fertilizer early for resale

The cheap-early-fertilizer premise in consensus §34 and the September 11
fertilizer-engine report is false on the report's own thirteen replays.
Observed fertilizer quotes on days 0–9 range from **77 to 100**; none reaches
30. Early BUY_PRODUCT FERTILIZER requests see pre-row quotes of **81–89**.
Quotes first reach 30 or below on days **21–25**, depending on the replay.

Root reproduced this with `S/postlot/audit_fertilizer_premise.py`. The audit
reads all 720 observations in each original replay, checks that both seats
see the same public market, and validates every fertilizer quote against the
existing market-price function. The installed reference engine matches
`vendor/engine.lock.json`, SHA-256
`bc8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463f23bccee653e`.
Fertilizer starts at 100 at inventory 10,000 and has no town-center or shop
drain in that engine. Its quote falls as net sales accumulate.

The fixed public-B12 cache is reported separately: the same early range 77–100,
zero early quotes at or below 30, first cheap quotes on days 21–27. Ten replays
overlap the original thirteen, so these are not independent replications and
their counts must not be added. That overlap also limits the earlier public
vacancy census: its selector ignored outcomes, but its source cache contains
previously loss-selected replays. It is a fixed convenience corpus, not an
unbiased sample of the live ladder.

The original table's roughly 1,915-coin "purchases re-sold" term is purchased
unit count multiplied by an average sale quote in a gross revenue
decomposition. It does not subtract purchase cost or track bought units to
their later use/sale, so it establishes neither arbitrage profit nor even
which purchased units were resold. The retained production/application/sales
counts do not repair that missing inference. The report's claim of buying at
8–30 on days 0–9 and selling later at 43–56 must not guide a policy experiment.

No fertilizer storage-buy pilot is justified by this premise. This correction
does not establish a universal impossibility result for every market policy;
it removes the particular evidence offered for early speculative fertilizer
buying. No policy, evaluation semantics, or reference engine was changed.

Reproduce with:

```bash
JAX_PLATFORMS=cpu timeout 180 .venv/bin/python \
  S/postlot/audit_fertilizer_premise.py
```

The preserved output `S/postlot/pilot/fertilizer_premise.json` contains each
input replay's SHA-256, per-episode quote ranges, first cheap day and every
fertilizer BUY request's pre-row quote. These are quotes and submitted
requests, not claims of executed purchase cost or counterfactual profit.
