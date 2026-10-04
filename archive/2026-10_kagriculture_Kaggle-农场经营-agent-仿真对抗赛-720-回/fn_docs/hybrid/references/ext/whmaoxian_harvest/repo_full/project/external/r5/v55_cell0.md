# Kaggriculture V55 — One-Turn Market Race Edge

V55 keeps V54's production, purchases, route tables, field actions, and visible wheat-price guard intact. It changes one market parameter: a planned premium-product sale may be reserved 41 turns ahead instead of 40. That extra turn matters when close Frontier-family agents compete for the same demand, while leaving most worlds unchanged.

The candidate was frozen before two independent confirmations. Every game below used the unmodified official engine, both seats, 719 callbacks, terminal `DONE`, exact action replay on the checked fixtures, and no telemetry errors.

| Panel | V54 W/L/T | V55 W/L/T | V54 points | V55 points | Paired margin gain |
|---|---:|---:|---:|---:|---:|
| Five-lineage selection, 3 worlds | 21/5/4 | 25/5/0 | 0.7667 | 0.8333 | $+64.93 |
| Six-lineage confirmation, 4 new worlds | 38/2/8 | 42/4/2 | 0.8750 | 0.8958 | $+63.88 |
| Frontier/Auto stress, 8 new worlds | 16/2/14 | 24/6/2 | 0.7188 | 0.7812 | $+56.00 |

Across the three panels, V54 scored 75/9/26 and V55 scored 91/15/4 over 110 games per arm. Match points rose from 0.8000 to 0.8455 and paired mean margin rose by about $61.9. The final untouched stress panel improved points by +0.0625, margin by $+56.00, and own cash by $+19.81. Its worst paired change was $-14 and its best was $+385.

The broader search rejected more aggressive 42/43-turn horizons because each regressed in 10 paired games despite larger mean-dollar gains. It also rejected opening, post-consumption sale, animal service, crop salvage, final courier, and apparent no-op patches. V55 contains none of those layers.

The public lineage credits and Apache-2.0 notices for Tetsutani, haideptry, Dmitrii Gluzdov, prvsiyan, and upstream contributors remain inside `main.py`. Ahmed Berat Ozer performed the current-meta audit, sequential-engine correction, official-engine selection, independent confirmations, packaging, and validation for V55.

Run the three code cells on Kaggle CPU. The last cell writes `submission_competitive_v55.tar.gz` to `/kaggle/working`; it does not submit or publish anything. No input dataset, internet, GPU, training, or non-standard package is required. Local evidence supports a stronger attempt than V54, but a ladder rating cannot be guaranteed because the live opponent mix and rating path vary.

Agent SHA256: `f09034624844da494669c4ab0e0d9a797da1a19db95eb138b875d309bd1aa01b`. Isolated normal-GC maximum callback on the tested Windows host: 45.350 ms.
