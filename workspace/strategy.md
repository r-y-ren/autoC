---
generated_at: 2026-08-29
direction: 黑客松与数据竞赛
profile_ref: config/profile.yaml
kb_snapshot: d19f500
---

> **决策变更记录**：Kaggriculture 战役 II（审计修订版）四波全部收口并通过 K-04 全量自动验收（128/181 测试、一次性 holdout 128 局 119W-9L、Wilson95 [0.8718,0.9626]），候选 `7c482921…` 已于 2026-08-29 03:47 UTC 线上提交（submission 55858820）。**线上首轮实测 1W-2L（公共天梯），skill 549.9，全榜 4550/6806**【workspace/metrics.json `unmeasured.online_*`；workspace/software/exports/online/round1_ledger.json，2026-08-29 CLI 实抓】。两负局回放解构产生 FM-O1..O4（组合集中/无外购饲料/无高价值作物/CARE-DIG 不足）；进一步对榜首对局（episode 102201446，Kaggle 网页回放 2026-08-29 手工下载实抓）的解构显示**顶部选手是市场自适应的作物轮作引擎而非畜牧引擎**。同日实测确认官方批量回放数据集通道可用（`kaggle/kaggriculture-episodes-index` + 每日快照）。本攻略据此重开战役 III：批量回放画像 → 线上风格对手池 → 市场自适应候选重构 → 一次性 holdout v2 → 提交 SOP v4。
>
> K-01 前置：本轮增量同步提交 `d19f500`（tech 0 新增、LA Hacks 待核维持、MLH 噪声弃置），未出现改变 Kaggriculture 主攻判断的新证据。

## 一、赛事情报摘要

- **kaggle-kaggriculture（重开主攻）**：30 日 720 回合农场经营仿真对抗；持续 Elo 天梯只按胜负平计分，终交后约两周收敛并跑 Bradley-Terry 锦标赛定榜；**终交 2026-09-30 23:59 UTC**，Entry/Team-Merger 截止 09-23；奖金 $50,000（前 10 名各 $5,000）；每日最多 5 次提交、**仅最近 2 次被跟踪**；团队上限 5 人【kaggle-kaggriculture，2026-08-28 官方直抓】。全榜规模 6806 队（2026-08-29 leaderboard CSV CLI 实测）。
- **线上首轮证据（本项目实测）**：公共天梯 3 局 1W-2L；两位胜者分别为全榜 3629 名（707.2）与 3978 名（640.4），即**打赢我们的是中下游分段选手**；胜者结构为"牛羊（+鹅）多物种 + 买入小麦制品做饲料 + 高价值作物副业 + 高频 CARE/DIG"，我方 10 牛单一引擎终局资金锁死 39.4k–47.6k 窄带【workspace/software/exports/online/round1_failure_analysis.md，回放实测】。
- **榜首结构情报（单局实测，待跨局验证）**：episode 102201446（榜一 Crop Dusta 74 662 : 榜二 Milan Leonard 60 779，2026-08-29 网页回放实抓，文件暂存本机）：榜一收入 ~125k 来自作物（麦 2553u + 胡萝卜 269u@92 + 草莓 + 西瓜），动物仅 ~11k；9 羊 3 牛 2 鹅小规模混合畜群；外购饲料 2305u@均价 30（我方 112u）；雇佣 295 次（持续 10–12/天，我方峰 5）；3 象限（我方 2）；day 0 花到剩 52 币；终局 2 天囤积倾销贡献 +36% 资金。**本局牛奶价格崩盘（区间 1..141），榜一的应对是不扩牛群、产能全转活着的曲线**——顶部 bot 的核心能力是市场自适应重构，而非固定引擎。
- **数据通道（2026-08-29 实测可用）**：① Kaggle 网页 episode 页可直接下载任意对局完整回放；② 官方数据集 `kaggle/kaggriculture-episodes-index`（索引）+ `kaggle/kaggriculture-episodes-YYYY-MM-DD` 每日快照（300–800MB/天）及社区镜像（7.6GB，更新至 08-28），CLI 直下。回放属竞赛数据（Apache 2.0），离线画像合规【kaggle-kaggriculture ai_policy】。
- **证据边界**：该赛 patterns confidence=低（未放榜）；榜首画像来自**单局**回放，牛奶恰好崩盘，"低牛"可能是局内应激而非固定形态——稳健结论仅为"顶部 bot 市场自适应、结构随局变化"，具体参数须由 m1 批量语料跨局验证【kaggle-kaggriculture】。
- **备选**：`kaggle-rsna-knee-abnormality-detection`（10 月窗口接力）与 `tianchi-qoder-thursday`（低改造 agent 支线）不变【kaggle-rsna-knee-abnormality-detection；tianchi-qoder-thursday】。

## 二、赛道对比矩阵（六维）

| 赛事 | 时间窗 | 技术契合 | 通吃度 | 画像匹配 | 竞争密度 | 合规风险 |
|---|---|---|---|---|---|---|
| **kaggle-kaggriculture（战役 III）** | **强证据**：终交 09-30，剩 ~4.5 周；每日 5 提交/最近 2 次跟踪给了线上采样空间【kaggle-kaggriculture】 | **强**：官方引擎/评估治理/101+ 测试资产在库；新增回放画像与对手池是纯增量工程；榜首结构情报已实测在手 | **中强**：画像管线+评估治理可复投任意仿真赛与模型评测赛道 | **强**：Python/数据分析画像直接匹配，且已有同赛两轮资产 | **强证据**：6806 队全榜实测；本队当前 4550 名 549.9 分——爬升目标分段明确（先 500–900 近段再向上）【metrics `unmeasured.online_skill_rating`】 | **低**：apply；外部数据/模型明文允许，回放数据 Apache 2.0【kaggle-kaggriculture】 |
| kaggle-rsna-knee-abnormality-detection | **强证据**：10 月窗口接力【kaggle-rsna-knee-abnormality-detection】 | **中**：监督学习匹配，医学域无实测 | **中**：实验治理可复用，模型栈重建 | **中强**：ML 履历匹配 | **有限证据**：旗舰赛竞争强，无本队实测 | **低**：apply【kaggle-rsna-knee-abnormality-detection】 |
| tianchi-qoder-thursday | **强证据**：长窗口至 2027-07【tianchi-qoder-thursday】 | **中强**：agent 工程栈匹配 | **中**：评估资产迁移 | **强** | **低证据**：无可比规模数据 | **低**：AI 工具鼓励【tianchi-qoder-thursday】 |

## 三、大显身手信号（近 90 天 KB-2 新卡 × 该赛命中）

- `arxiv-2608.26753`（ABE-Ralph）继续命中：本轮把**回放语料本身**纳入证据身份链——语料来源（数据集 URL+抓取日期）、画像档案哈希、异常局剔除规则全部可审计，防止"画像污染策略结论"。
- `arxiv-2608.27456`（UrbanGround）命中：线上风格对手进入同一 runnable 沙盒与完整门禁，画像→失败模式→修复的失败驱动闭环直接复用。
- `arxiv-2608.15291`（ReasonCast）命中升级：选择性干预从"卖出 timing 门控"扩展为"按价格曲线重构生产结构"（轮作/畜群/饲料来源的自适应层）。
- `arxiv-2608.25992` + `arxiv-2608.24087`：LLM 质量-成本路由保持可选 A/B，无 key 时如实 null，不阻塞主线。
- **证据降权**：无 winner-derived patterns；榜首画像为单局实测，跨局稳健性由本战役 m1 交付物验证，呈报时不得引用为已确认规律【kaggle-kaggriculture】。

## 四、一鱼多吃路线

1. **主线**：Kaggriculture 战役 III（本蓝图）。新增资产：回放画像管线、线上风格对手池、市场自适应引擎、分层分段画像方法。
2. **近期开枝**：收官后转 `kaggle-rsna-knee-abnormality-detection`，复用实验身份/holdout/原子指标工具；模型管线改造量**中高**。
3. **低成本复投**：画像管线+评估治理脚手架用于 `tianchi-qoder-thursday` 类 agent 题，改造量**低**。
4. **方法论输出**：回放→对手池→去同族偏移的评估方法可写入后续数模/评测类报告，改造量**低**。

## 五、合规与风险

**模式判定：apply。** 依据（KB 抓取 2026-08-28 原文摘引）：

> "The use of external data and models is acceptable unless specifically prohibited by the Host."
> "a small subscription charge to use additional elements of a large language model such as Gemini Advanced are acceptable if meeting the Reasonableness Standard"
> "Individual Participants and Teams may use automated machine learning tool(s) ('AMLT') ... provided that ... they have an appropriate license"

竞赛数据 Apache 2.0（商用亦允许）、获奖许可 CC-BY 4.0；官方回放数据集与网页 episode 下载均为平台公开通道，离线画像合规【kaggle-kaggriculture】。提交 bot 保持 stdlib-only、离线自主：**画像只用于离线设计，不进入 bot 运行时依赖**。

风险与缓解：

1. **分段分布偏差**：天梯按分段匹配，我们当前 549 分先遇 500–900 段对手；只学榜首结构可能跳过近段。缓解：m1 语料**分层抽样**（榜首 top-20 + top-100 + 500–900 近段），对手池覆盖两类结构。
2. **单局画像过拟合**：榜首"低牛"可能是牛奶崩盘局的应激。缓解：画像结论须跨局复核（同选手 ≥3 局一致才进对手池参数），单局结论标 exploratory。
3. **数据量与新鲜度**：每日快照 300–800MB；镜像 7.6GB。缓解：原始回放只落 gitignored 数据目录，仅小体积画像档案入库；按需下载指定日分片/episode，不做全量镜像。
4. **holdout 一次性纪律**：候选变更必须全新独立种子（与 27 历史 + 8 已公布 + 3 线上实测 seed 无交集），禁止复用旧 holdout 结论外推新候选。
5. **同族偏移复发**：新对手池仍是我方实现。缓解：线上每轮提交后回拉本方 episode 复盘（SOP v4 循环），画像档案滚动更新；本地胜率不得外推天梯。
6. **提交预算**：每日 5 次、最近 2 次跟踪；09-23 团队截止前保持阵容稳定。缓解：SOP v4 规定提交节奏（每候选 ≤2 次/日，验证局 Error 即停）。
7. **止损线**：若新候选线上 ≥6 局公共局胜率仍 <50%，停止本方向继续调参，转备选赛道（评估治理资产保留）。

## 六、推荐结论

**推荐第一名：重开 Kaggriculture 战役 III——"批量回放画像 + 线上风格对手池 + 市场自适应候选重构 + 一次性 holdout v2"。**

理由：① 线上 1W-2L 与榜首解构共同指向同一根因——静态单一引擎 vs 市场自适应结构，且修复方向已有实测参数在手（作物轮作配比、外购饲料价位 26–32、雇佣强度 10–12/天、3 象限、终局囤倾）；② 官方回放数据集使"对手分布偏移"从不可控变为可工程化消除（画像→对手池→分层验证），这是战役 II 风险清单第 3 条的正面解法；③ 前 two 轮的全部评估治理资产（AB/BA、fail-closed、身份冻结、原子发布）直接复用，重开边际成本低；④ 窗口充裕（~4.5 周 × 每日 5 提交 × 最近 2 次规则天然支持采样-迭代循环）。

**备选：kaggle-rsna-knee-abnormality-detection。** 触发条件见止损线（新候选线上持续负于近段对手）；届时评估治理与画像管线资产随迁。
