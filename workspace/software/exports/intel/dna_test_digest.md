# 情报摘要：A DNA Test for Agents（destbreso 谱系学系列）

- 来源 notebook: https://www.kaggle.com/code/destbreso/a-dna-test-for-agents （2026-08-31 经 `kaggle kernels pull` 实抓，30 cells，本地存档 `.tmp-dna/a-dna-test-for-agents.ipynb`）
- 配套数据集: `destbreso/kaggriculture-replay-genomes` （2026-08-31 经 `kaggle datasets download` 实拉，88.8MB；本地 `.tmp-dna/`）
- 引用纪律：以下全部数字来自上述实抓文件，未混入模型记忆。

## 方法（仪器本身）

1. 对局 X 光：逐 turn 比对每局与语料库众数行为 → 发散呈"带状"分布。
2. 按日内小时折叠定位保守窗：**小时 1–4**（小时 0 是决策小时：卖出/买饲料/雇佣，局局不同；引擎夜间重置位置但农场状态跨日携带，日内发散粘滞 ~0.95、隔夜存活 ~0.61）。
3. **日条形码**：对每天小时 1–4 的 plan 通道（farmer/hands、结构性与补给性指令；明确排除卖出与数量）做语义哈希 → 每天 1 个 allele，30 天 = 30 locus 基因组。整条再哈希 = 8 位 genome_id。
4. 判定规则：IDENTICAL / RELATED / WEAK / UNRELATED，随机碰撞概率按等位基因频率表（160 队实测）计算；样本自稳定性 <0.6 时拒绝给出阴性判定（OUT OF RANGE）。

## 验证（forensic 级）

- 同队两流中位匹配 **0.93**（15 对）；跨队 12,720 对中位 **0.00**，**0 对共享 ≥2 带**；α ≤ 2.4e-4（rule of three）。
- 独立性模型会预测平均 4.81 共享带（实测 0），碰撞≈祖先：共享带只有同源一种现实解释。
- 自稳定性（liveness）：纯脚本 ~1.0；tschinkel ~0.72-0.83；**kawashigi 0.37-0.38（板中最深的自适应层，连锚窗都能改写）**。仪器"读不出"本身就是分类信号。

## 棋盘结构发现（对 K-03 直接相关）

- **单文化**：精英样本（数据集 consensus.csv，71 提交/61 队/5 个捕获日 08-15→08-23）中 **38% 聚在同一 day-10 谱系类**，第二大类 14%，28 类中 23 类是单例；公众主干 allele 每天覆盖 20–33% 的队（field_validation.json top_share_by_day，本机复算 d0:0.26 d5:0.33 d10:0.20 d15:0.23 d20:0.30 d25:0.23 d29:0.24）。
- **顶端是共享库存的突变体**：Utkarsh #2（rank 2）= 公众 legacy 布局的直系后代，22/30 带，分叉日 **day 20**；双龙头 kawashigi/tschinkel 距公众路线仅 12–20 带（重度晚季突变）；abdelrazik 是少数零带独立谱系。
- **化石记录**：clade 数天内扫荡全板又灭绝（5 个捕获日的谱系消长）；已发表 notebook 路线（fukami v25）有活着的后代 clade。
- 系列前作：everyone-is-playing-the-same-opening / the-leaderboard-has-a-fossil-record / mutants-at-the-top。

## 对我方的适用性

1. **方向裁决的靶群证据**：600→764 差距是"类差"，而精英层是单文化突变体群 → 针对共享行为的反 conditioning 有大而稳定的靶面（支持 fork A 的前提）。
2. **现成的对手分类器（离线半场）**：数据集直接给 2,479 条 episode 级 barcode（含 opponent、bank）+ 参考谱系 19 条 + allele 频率表；matchups.csv 带 seed 可重放。把 round-5/6 我方 ~50 局对手按谱系归类 → **按谱系分辨的胜率表**，取代现在的 archetype 猜测。注意：提取器代码未随文发布（数据集只有预计算 barcode），需按上文规格本地重实现哈希（规格完整：小时 1–4 plan 通道语义键）。
3. **入场冻结时机**：化石记录节奏（clade 日级扫荡）提示 09-23 freeze 前的最终发布窗口选择有信息可挖。
4. **局限**：仪器读身份不读强弱（作者明示）；对局内我方看不到对手 plan 通道，仅市场外部性可见——不取代此前的市场反推构想，是其离线互补件；其"精英样本"描述的是 ladder 顶部，我方 600 分段构成需用自有回放实测。
