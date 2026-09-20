# Track-C BC 首跑评估（bc_eval）

- 协议：twin-d0-fullseason / opponent=replay-actions / baseline=build_v13_namespace (v14.2 src/)
- 局数：8（held-out，训练零泄漏）
- BC median=2975 vs v14.2 median=64238
- H2H（同局同对手流）：BC 0 — 8 v14.2（tie 0）；median Δ=-39432
- 塌方带（<45k）：BC 6 / v14.2 3
- 行为：BC move=31.8% pass=51.4% CARE=100 | v14.2 move=65.4% pass=12.0% CARE=114
- X-ray 榜首参照：move 53.8% / pass 3.8% / CARE 348
- BC agent 异常：0

| 局 | BC | v14.2 | 真值 | BC W | v14.2 W |
|---|---:|---:|---:|---|---|
| bc-top:0b20d72e-b4f9-11f1-b047-0242ac130 | 2975 | 31129 | 97175 | L | L |
| bc-top:6a30a0ce-b4f3-11f1-8e33-0242ac130 | 2967 | 48554 | 90159 | L | L |
| bc-top:951e3540-b4f7-11f1-8510-0242ac130 | 156829 | 187724 | 89692 | W | W |
| bc-top:bca76844-b4f1-11f1-8dac-0242ac130 | 2965 | 79923 | 84190 | L | L |
| bc-top:e80cc5fe-b4f8-11f1-9054-0242ac130 | 2967 | 37550 | 158953 | L | L |
| bc-top:f010fe7c-b4f9-11f1-92c9-0242ac130 | 132769 | 177049 | 111679 | W | W |
| bc-top:f1edb0ee-b4f6-11f1-b843-0242ac130 | 2975 | 37436 | 88750 | L | L |
| local:21926220-b2a6-11f1-97f0-0242ac1302 | 2976 | 80733 | 42284 | L | L |
