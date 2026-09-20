# Track-C BC 首跑评估（bc_eval）

- 协议：twin-d0-fullseason / opponent=replay-actions / baseline=build_v13_namespace (v14.2 src/)
- 局数：8（held-out，训练零泄漏）
- BC median=604 vs v14.2 median=55935
- H2H（同局同对手流）：BC 0 — 8 v14.2（tie 0）；median Δ=-55335
- 塌方带（<45k）：BC 8 / v14.2 3
- 行为：BC move=18.5% pass=39.8% CARE=54 | v14.2 move=62.0% pass=13.6% CARE=136
- X-ray 榜首参照：move 53.8% / pass 3.8% / CARE 348
- BC agent 异常：0

| 局 | BC | v14.2 | 真值 | BC W | v14.2 W |
|---|---:|---:|---:|---|---|
| bc-top:0b20d72e-b4f9-11f1-b047-0242ac130 | 533 | 31129 | 97175 | L | L |
| bc-top:6a30a0ce-b4f3-11f1-8e33-0242ac130 | 592 | 48554 | 90159 | L | L |
| bc-top:951e3540-b4f7-11f1-8510-0242ac130 | 607 | 65412 | 89692 | L | L |
| bc-top:bca76844-b4f1-11f1-8dac-0242ac130 | 602 | 79923 | 84190 | L | L |
| bc-top:e80cc5fe-b4f8-11f1-9054-0242ac130 | 614 | 37550 | 158953 | L | L |
| bc-top:f010fe7c-b4f9-11f1-92c9-0242ac130 | 608 | 63316 | 111679 | L | L |
| bc-top:f1edb0ee-b4f6-11f1-b843-0242ac130 | 608 | 37436 | 88750 | L | L |
| local:21926220-b2a6-11f1-97f0-0242ac1302 | 538 | 80733 | 42284 | L | L |
