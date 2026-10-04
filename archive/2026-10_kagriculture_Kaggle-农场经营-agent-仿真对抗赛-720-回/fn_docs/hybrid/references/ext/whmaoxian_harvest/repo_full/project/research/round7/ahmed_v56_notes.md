# Kaggriculture V56 — Smarter Seeds and Fertilizer

This revised V56 keeps the previously validated late seed budget and adds one independently tested fertilizer rule. The earlier seed budget stops purchasing wheat/carrot seeds that exceed all remaining planting opportunities. The new layer avoids spending another fertilizer on a wheat/carrot crop when existing coverage already lasts three days, or when the native scheduled harvest is predicted to be unchanged without it. Sequential worker actions are accounted for; unconfirmed reactive-worker plans retain their fertilizer. Crop production inputs remain available to the rest of the policy.

This is one additional mechanism, not three separate upgrades. Reusing stored fertilizer at purchase time and broadening sequential carrot substitutions were also tested, but failed or did not activate and were excluded. Newly published Fieldcraft was evaluated as an independent opponent; its source was not transplanted.

The source was frozen before confirmation. Tests use the unmodified official engine, reacting opponents, both seats and exact source hashes. Baseline below means the previous seed-budget V56, not V55. These are local results, not a guaranteed live rating.

| Panel | Previous V56 W/L/T | Revised V56 W/L/T | Previous winrate | Revised winrate | Point gain | Mean margin gain |
|---|---:|---:|---:|---:|---:|---:|
| Pilot: 4 worlds | 16/4/12 | 28/4/0 | 0.5000 | 0.8750 | +0.1875 | $+201.00 |
| Confirmation: 8 new worlds | 30/12/22 | 44/12/8 | 0.4688 | 0.6875 | +0.1094 | $+100.25 |
| Final: 4 more worlds, 6 rivals | 35/5/8 | 40/4/4 | 0.7292 | 0.8333 | +0.0625 | $+97.52 |

A paired physical diagnostic kept wheat/carrot harvest quantities unchanged and produced two extra strawberries after retained fertilizer became available to later work. This is a diagnostic of one world, not an assertion that every action or crop total is unchanged. Competitive results include reacting market prices: some improvement comes from reducing the rival's revenue, and not every own-cash result improves. Related opponent lineages and both seats are correlated; research uncertainty is grouped by whole world seeds.

The agent is standard-library-only. Original Apache-2.0 notices are retained, including Thomas Tschinkel, Yusuke Hayashi, destbreso, aurax7, Tetsutani, prvsiyan, Dmitrii Gluzdov and Seyit Kaan Gunes. Ahmed Berat Ozer's additions are the remaining-planting seed budget and harvest-aware fertilizer cap, with integration and independent evaluation.

Run the three code cells on CPU. No dataset attachment, Internet, GPU or training is required. The notebook writes `submission_competitive_v56.tar.gz` in `/kaggle/working`; it does not submit or publish anything.

Source SHA256: `a1ad0fd1d174477ee2cbdd561a812bcb7029647ce34599e79d6b79e9057eff6c`. Isolated normal-GC maximum callback: 28.832 ms on the tested Windows host.
