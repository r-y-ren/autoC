# Track-C BC 首跑评估（bc_eval）

- 协议：twin-d0-fullseason / opponent=replay-actions / baseline=build_v13_namespace (v14.2 src/)
- 局数：12（held-out，训练零泄漏）
- BC median=1748 vs v14.2 median=n/a
- H2H（同局同对手流）：BC 0 — 0 v14.2（tie 0）；median Δ=n/a
- 塌方带（<45k）：BC 12 / v14.2 0
- 行为：BC move=31.0% pass=23.0% CARE=24 | v14.2 move=n/a pass=n/a CARE=n/a
- X-ray 榜首参照：move 53.8% / pass 3.8% / CARE 348
- BC agent 异常：0

| 局 | BC | v14.2 | 真值 | BC W | v14.2 W |
|---|---:|---:|---:|---|---|
| bc-top:0b20d72e-b4f9-11f1-b047-0242ac130 | 2065 | n/a | 97175 | L | ? |
| bc-top:6a30a0ce-b4f3-11f1-8e33-0242ac130 | 2114 | n/a | 90159 | L | ? |
| bc-top:951e3540-b4f7-11f1-8510-0242ac130 | 1065 | n/a | 89692 | L | ? |
| bc-top:bca76844-b4f1-11f1-8dac-0242ac130 | 2782 | n/a | 84190 | L | ? |
| bc-top:e80cc5fe-b4f8-11f1-9054-0242ac130 | 901 | n/a | 158953 | L | ? |
| bc-top:f010fe7c-b4f9-11f1-92c9-0242ac130 | 2774 | n/a | 111679 | L | ? |
| bc-top:f1edb0ee-b4f6-11f1-b843-0242ac130 | 1925 | n/a | 88750 | L | ? |
| local:21926220-b2a6-11f1-97f0-0242ac1302 | 1054 | n/a | 42284 | L | ? |
| local:53282276-b471-11f1-84b4-0242ac1302 | 3298 | n/a | 127641 | L | ? |
| local:788f5cba-b3da-11f1-9ac9-0242ac1302 | 1570 | n/a | 58603 | L | ? |
| local:e1d184be-b376-11f1-9467-0242ac1302 | 991 | n/a | 94088 | L | ? |
| local:ecaeae34-a3b8-11f1-bde5-0242ac1302 | 1029 | n/a | 96629 | L | ? |
