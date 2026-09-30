# whzy_exp066 原始拉取物 provenance（ext/whzy_exp066/）

- 来源 URL：https://github.com/whzy3185/kagriculture （EXP 工作台，2026-09-30 首推）
- 抓取方式：`git clone --depth 1 https://github.com/whzy3185/kagriculture /tmp/whzy66`
- 抓取日期：2026-10-01
- commit sha：`da999d2fdfb7b7992dd089985c2a4c030de4c96f`（HEAD，2026-09-30 18:01:35 +0800，"strategy: add EXP067 pizza wheat route"）
- 许可：Apache-2.0（血统件 LICENSE.txt/NOTICE.txt 取自 `agents/candidates/exp012/` 随包——上游候选目录 exp012/exp014 等 LICENSE/NOTICE/PROVENANCE 齐；exp066 目录本身仅 main.py，attribution/SPDX 头内嵌于 main.py；谱系=Metav4/Pipe16 系 dmitriigluzdov/nathanjacob 等公开重用声明）
- 自报版本：EXP-066-liquidity-wool-flush（"LiquidityWool"，低风险实验候选，未提交 Kaggle）

## 文件清单与 SHA-256（见 SHA256SUMS.txt）

| 文件 | SHA-256 | 说明 |
|---|---|---|
| main.py | 8d2c5d42d492f4c5a38c9736af5704a80e0f2f415d4d2ec54c01e9d8ea84b640 | 候选件 `agents/candidates/exp066_liquidity_wool_flush/main.py`（1,208,219 B）；与上游 `submissions/EXP-066-liquidity-wool-flush.manifest.json` 自报 sha 一致 |
| EXP-066-liquidity-wool-flush.manifest.json | 8e65ae8fcabf108f43d03a1140df1e3e6cdd1a5ccaf74023002638258d5f4947 | 上游打包清单（自报 sha/bytes/成员表） |
| EXP045_EXP054_KAGGLE_FAILURE_OPTIMIZATION_20260930.md | 86813f61daaf3f18a6ada4dfd55f00aad6cd35d5fd7a47cbdb93ffcad7854819 | 在册报告：官方 wool-race 两败局修复 +1,032/+300（未翻胜）、12 强开源 134-0-10、40 局平 EXP054 |
| exp066_vs_exp054_fresh20.json | a4a574bbe676ebad048332fa0c39060999a7c9f41127a547d467865726cfea44 | 自报回归：20 新种子双席 40 局 vs EXP054 全平 |
| exp066_vs_current_open_source_6seeds.json | ec66ec88b92325e25277c6d3989f29e914c6262a64eb8c8f806d279386e3cd80 | 自报回归：6 种子对 12 强开源 134-0-10 |
| LICENSE.txt | cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30 | Apache-2.0（血统件 exp012/ 随包；与 haodou_v94 归档 LICENSE 同文） |
| NOTICE.txt | 636f47d447e2366f7f281b4e326fb796a0c8b4a2f9898a502c5e87aab26e8359 | 上游署名（Gold-stack hybrid derivative：Pipe16/Metav4 生产栈 nathanjacob/thomastschinkel/ahmedberatozer/dmitriigluzdov 等） |

## 机制自述（报告/README 自报口径，未迁移验证）

- EXP066 触发条件（EXP063→EXP066 消融链）：羊毛镜像局中我方现金 < 42,000 时提前 flush 羊毛换流动性（cash-gate 精确隔离 seed 1403 回归）。
- 自报战绩：修 2 条官方 wool-race 败录钱差 +1,032/+300（未翻胜）；对 12 强开源包 134-0-10（与 EXP054 一致）；20 新种子 40 局与 EXP054 全平。
- 自报≠可迁移（六连败教训）：以上均自报口径，判决只认本池实测（orderbook_whzy66_lab/evidence/exp066_arena.json）。

## 本地实测（本次紧急池测）

- 判决证据：`fn_work/legacy_software/kaggle_simulations/orderbook_whzy66_lab/evidence/exp066_arena.json`（bwrap 沙箱内跑：根只读+断网；零修改直跑本归档 main.py）。
- 只测不发：不在线提交（硬禁令），不修改件本体。
