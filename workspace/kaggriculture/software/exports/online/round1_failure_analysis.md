# Round 1 线上复盘：失败模式分析（公共天梯 1W-2L）

- 提交：Kaggle submission `55858820`（candidate sha256 `7c482921857562e6b7cd58a3ac4bde358981c180cc233ad3913948e5fcafa66a`，git `f76a0bb7542fed3500b35871952408e383ab257b`，提交于 2026-08-29T03:47:25Z）
- 数据来源：`kaggle competitions submissions / episodes / replay` CLI 抓取，台账见 [round1_ledger.json](round1_ledger.json)（4 局：1 局 validation 自对弈 + 3 局公共天梯）
- 本文所有数字均为回放实测计数，无估计值

## 战绩概览

| Episode | 对手 | 我方座位 | 比分（我:对） | 结果 |
|---|---|---|---|---|
| 102188134 | renyxin（自对弈 validation） | seat0 | 18053 : 18046 | W（不计入天梯） |
| 102192249 | Muhammad Yasir Sarwar | seat0 | 40839 : 35705 | **W** |
| 102194478 | Sooriya Senthilkumar | seat0 | 39377 : 74792 | **L** |
| 102196708 | Chirag Bhatnagar | seat1 | 47642 : 62586 | **L** |

关键观察：我方三局公共对局终局资金落在 39.4k–47.6k 的窄带内（引擎产出基本饱和）；两位胜者的终局资金达 62.6k 与 74.8k。差距不是"我方发挥失常"，而是**对手的经济结构上限更高**。

## 我方候选引擎画像（两负局回放实测）

10 头 COW 单一畜牧；无 SHEEP / 无 GOOSE；饲料全部自种自给（未买入任何 WHEAT 商品作饲料）；无高价值作物（STRAWBERRY / MELON / TOMATO 等）副业收入；土地以种植/维持为主，CARE / DIG 操作次数远低于对手。

## 胜者画像（两负局回放实测）

- 负局 1（102194478，对手 Sooriya Senthilkumar，74 792 分）：8 COW + 2 SHEEP + 3 GOOSE，兼种 STRAWBERRY / MELON。全场卖出：WHEAT 393、STRAWBERRY 138、MELON 168、EGG 78、MILK 100、WOOL 59、FERTILIZER 165。买入 549 单位 WHEAT 商品作饲料；操作分布 CARE 198 / FEED 249 / DIG 68。
- 负局 2（102196708，对手 Chirag Bhatnagar，62 586 分）：7 COW + 4 SHEEP，兼种 TOMATO / CARROT / MELON。全场卖出：MILK 176、WHEAT 202、WOOL 65、FERTILIZER 162。买入 199 单位 WHEAT 作饲料；CARE 220。

两位胜者的共同结构：**牛羊（+鹅）多物种组合 + 买入廉价小麦制品做饲料 + 高价值作物副业 + 高频 CARE/DIG 土地周转**，与我方 10 牛单一结构形成四点系统性差异，对应 FM-O1..FM-O4。

## 失败模式清单

### FM-O1 组合集中度：无羊（羊毛）与鹅（蛋）收入线

- 证据：胜者 1 蛋 78 + 羊毛 59 的额外卖出收入线，胜者 2 羊毛 65；我方两局卖出清单中 EGG / WOOL 恒为 0。多物种还把收入分散到多条独立价格曲线上，降低单一 MILK 价格波动的暴露。
- 迭代方向：在现金安全线内引入 2–4 SHEEP（产 WOOL，且羊与牛共用 CARE 收益）与可选 2–3 GOOSE（产 EGG）的小规模试点；先在本地评测验证混合畜群不稀释牛奶引擎的节奏。

### FM-O2 无"买入小麦制品做饲料"的饲料经济学

- 证据：胜者分别买入 549 与 199 单位 WHEAT 商品当饲料——从市场买廉价饲料，把自种土地腾给更高价值用途；我方饲料全靠自种，土地被饲料小麦占用。
- 迭代方向：在饲料单价低于自种机会成本的窗口启用"买入 WHEAT 制品直接 FEED"的通道，并加价格护栏（仅当 WHEAT 售价低于阈值时触发），避免重蹈 FM 风格的逆势扫货。

### FM-O3 无高价值作物副业（草莓/西瓜等）

- 证据：胜者 1 STRAWBERRY 138 + MELON 168、胜者 2 TOMATO/CARROT/MELON 组合的卖出量；我方高价值作物卖出恒为 0，收入几乎全押 MILK / FERTILIZER 两条线。
- 迭代方向：在畜牧现金流转正后，用腾出的地块轮作一季高价值作物（优先 STRAWBERRY / MELON），形成"牛奶基本盘 + 作物脉冲"的双引擎收入。

### FM-O4 CARE / DIG 土地周转利用不足

- 证据：胜者操作计数 CARE 198–220（另有 FEED 249），我方 CARE/DIG 次数远低于该水平；高频 CARE 拉动地力与产出，DIG 支持作物换茬腾地。
- 迭代方向：为 CARE 设定每地块的维持节律（按肥力衰减触发而非按需触发），并在换茬窗口用 DIG 主动腾地，配合 FM-O2/O3 的土地再分配。

## 结论与纪律申明

**本地 92.9%（一次性全矩阵 holdout 128 局 119W-9L，Wilson95 [0.8718, 0.9626]）不能迁移到线上**：公共天梯 3 局 1W-2L，胜者用的是本地对手池之外的多样化经济结构。按 holdout SOP v3（`exports/eval_results.json#/holdout/protocol`：`one_time=true`、`candidate_change_invalidates=true`），任何针对 FM-O1..FM-O4 的新候选都属于候选变更，**必须重新抽取与全部历史种子（含本次 8 个 holdout 种子及 27 个历史排除种子）无交集的全新独立确认种子，重走一次性 holdout 闭环**，不得复用已公布种子的结论外推。

相关产物：台账 `round1_ledger.json`；指标分片 `workspace/software/metrics.json` 的 `unmeasured.online_*` 三键（2026-08-29 线上实测后赋值，键位保持不动以稳定消费方）。
