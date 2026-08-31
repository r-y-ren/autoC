# 对手目录（external opponents）

本目录存放用于本地 H2H 评估的外部/历史 agent 快照。**仅作陪练对手，任何字节不得进入我方提交路径**（行为引用，非代码借用；AGENTS.md 合规底线 + Kaggle 竞赛规则）。

## v48_main.py
- 来源: kaitofukami "40/40 Early Floor | 39/46 Top-10 | v48 Fast Routes" notebook（2026-08-31 经 `kaggle kernels pull` 实抓，自解包 cell 执行重建）
- SHA-256: dadee25a9840313218384208c53b2c4752f82c3209cc654632e0b96c65e2664a（与 notebook §7 公布值逐字节一致，107,008 bytes）
- 作者自报面板: 旧 first-20 40/40、Top-10 holdout 39/46、Top-30 97/140（冻结动作流重放，非天梯分）
- 许可注意: notebook 未附显式开源许可 → 只作对手重放，不挖其实现；若未来需引用其思路，须以行为观察+自写代码路线实现并注明出处。

## v72_main.py
- 来源: 本仓库 git fdd5b87 提交的 workspace/software/kaggle_simulations/agent/main.py（提交信息即 "K-05 round-5 提交：v7.2 55884001 验证 COMPLETE score 718.6"）
- SHA-256: f0bcd6570d442422...（119,972 bytes）
- 用途: 在线 718.6 分的历史冠军基线，作为 H2H 参照锚点
