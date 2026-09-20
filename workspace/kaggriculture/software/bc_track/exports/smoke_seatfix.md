# Track-C BC 首跑评估（bc_eval）

- 协议：twin-d0-fullseason / opponent=replay-actions / baseline=build_v13_namespace (v14.2 src/)
- 局数：1（held-out，训练零泄漏）
- BC median=2975 vs v14.2 median=n/a
- H2H（同局同对手流）：BC 0 — 0 v14.2（tie 0）；median Δ=n/a
- 塌方带（<45k）：BC 1 / v14.2 0
- 行为：BC move=31.4% pass=67.0% CARE=0 | v14.2 move=n/a pass=n/a CARE=n/a
- X-ray 榜首参照：move 53.8% / pass 3.8% / CARE 348
- BC agent 异常：0

| 局 | BC | v14.2 | 真值 | BC W | v14.2 W |
|---|---:|---:|---:|---|---|
| bc-top:0b20d72e-b4f9-11f1-b047-0242ac130 | 2975 | n/a | 97175 | L | ? |
