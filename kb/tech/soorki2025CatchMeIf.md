---
id: soorki2025CatchMeIf
name: 元强化学习驱动的LoRa无人机搜救轨迹控制
field: [UAV 轨迹优化, 元强化学习, LoRa 搜救]
published: 2025-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 部分可观测环境（POMDP）下的序贯搜救决策建模 + 跨环境元学习快速适配，可直接迁移到不确定环境下的搜索/侦察路径类决策题，附「贪心搜索易陷局部最优」的现成对比论证
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: RSSI 时序观测驱动的 meta-RL 飞行策略骨架（多环境元训练 + 新环境快速微调），可用于环境分布会变的数据驱动决策赛题
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 山区搜救/应急感知的 LoRa 无人机飞行网关方案支撑点（campus/plain/canyon 三类真实环境实测背书，弱网远距低功耗叙事完整）
    reuse_cost: 低
sources:
  - paper_title: "Catch Me If You Can: Deep Meta-RL for Search-and-Rescue Using LoRa UAV Networks"
    doi: 10.1109/TMC.2024.3468382
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 元强化学习驱动的LoRa无人机搜救轨迹控制

## 单行摘要

面向偏远山区等遮挡复杂环境的搜救任务，把携带 LoRa 节点的失踪者（发射端）、作为飞行网关的 UAV 与地面救援站建模为 POMDP：UAV 每时隙依据 RSSI 与历史观测选择飞行动作，目标是同时压缩搜索时间与能耗；核心创新在用 deep meta-RL 把多个旧环境（校园/平原/峡谷）的经验编码进元策略，使 UAV 进入传播特性未知的新环境时能快速微调适配，而非像单环境 DRL 那样迁移即失效。

## 方法快照

- 问题抽象：非视距遮挡 + 有限电池 + RSSI 波动 + 未知环境几何下的搜索轨迹控制，属高不确定性序贯决策。
- 基线策略：先在单一环境训练 deep RL 飞行网关控制策略。
- 元学习层：把过去多环境的训练经验作为先验，deep meta-RL 元策略在新环境中少量交互即可适配。
- 对比对象：deep RL、Actor-Critic 与传统贪心式 LoRa 搜索。
- 关键结果：峡谷场景中 SAR time slots 从 141 降到 50，能耗分别比 deep RL 与 Actor-Critic 低 57% 与 23%。
- 验证：数值仿真 + 原型系统 + 三类真实环境实测（campus/plain/slotted canyon），是少见的 LoRa 搜救实证锚点；未披露代码，复现性 medium。

## 比赛映射要点

- 数模：环境不确定下的搜索路径/侦察调度题可套「POMDP 建模 + 元学习跨场景迁移」框架，跨环境适应能力可作为模型评价维度（对比单场景训练的策略）。
- 黑客松：信号强度序列驱动的目标搜索类题（信标定位、灾情探测）可复用「RSSI 历史编码 + RL 动作输出」的最小闭环；meta-RL 思想用于处理训练/测试分布漂移。
- 双创申报：应急搜救、山区巡检、弱网感知等场景的无人机方案章节可直接引用其真实环境实测结论与能耗收益。

## 关联概念
- LoRa辅助搜救

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Soorki2025_面向LoRa搜索救援的深度元强化学习UAV轨迹控制`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `soorki2025CatchMeIf` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写。
- 复现性承自 vault 页自评（medium，仿真+原型+实测但未披露代码与硬件型号）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
