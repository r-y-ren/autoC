---
id: xu2024RewardMaximizationDisaster
name: 灾害监测异构UAV奖励最大化调度（常数近似算法）
field: [异构无人机调度, 定向问题, 近似算法]
published: 2024-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE/ACM Transactions on Networking
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 能量约束下异构多巡回 orienteering 建模 + 首个常数近似比算法（且界为紧），直接对应数模赛「多机分配巡回收益最大化」题型，理论保证是对比启发式/DRL 路线方法的硬差异化
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 带能量约束的巡回选择近似算法可作路线收益类赛题主解法，实验用 DJI Phantom 4 RTK、M300 RTK、senseFly eBee X 等商用机型真实参数，假设贴近实机
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 应急监测与农业巡查的异构机队调度方案支撑——同一 PoI 对不同机型奖励不同、高能力机型更耗能的异构效用建模，比同质机队假设更贴近真实装备组合
    reuse_cost: 低
sources:
  - paper_title: "Reward Maximization for Disaster Zone Monitoring With Heterogeneous UAVs"
    doi: 10.1109/TNET.2023.3300174
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# 灾害监测异构UAV奖励最大化调度（常数近似算法）

## 单行摘要

灾害区域多 PoI 监测场景下研究异构 UAV 调度：各机续航、单位距离能耗与感知能力互不成比例（高奖励机型可能更重更耗能），把问题建成带能量约束的异构巡回选择问题（多巡回 orienteering 变体），设计首个具常数近似比的算法——为每架 UAV 构造近似最优巡回使总监测奖励最大，论文报告相比对比算法总奖励最高提升约 25%。

## 方法快照

- 模型要点：每个 PoI 对不同 UAV 有不同监测奖励（由设备能力与任务重要性共同决定）；每机有独立能量上限与单位距离能耗；所有巡回从同一救援站出发并返回。
- 问题本质：异构约束下的多巡回 orienteering——优化总奖励而非二元覆盖数，更贴近救援优先级。
- 算法：为每架 UAV 构造近似巡回并证明常数近似比，界为紧；与启发式/DRL 路径方法相比提供有理论保证的路线。
- 验证：数值仿真（合成灾害拓扑 + 商用 UAV 真实参数），未做实飞；开源情况未说明。

## 比赛映射要点

- 数模：异构机队 + 能量约束 + 收益最大化的组合是典型赛题骨架（选点、排序、分配三合一）；「有近似比保证」在论文与答辩中都是可量化的方法学优势。
- 黑客松：orienteering 变体可直接落到应急响应、巡检路线收益类赛题；商用机型参数表可复用作能耗假设。
- 双创申报：应急/农业异构机队调度模块（哪些机型看哪类目标更划算），回应「机队怎么编」的运营问题。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Xu2024_面向灾害监测的异构UAV奖励最大化调度`（vault 页 4 枚举字段 venue_tier=CCF-A、evidence_tier=core、paper_role=anchor、reproducibility_level=medium 已迁移至本卡）。
- bib 回填：citekey `xu2024RewardMaximizationDisaster` → 标题/venue/DOI 来自 vault 自带 Zotero bib（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按年-01-01 填写；验证类信息（simulation/synthetic + 商用机型参数/复现性 medium、开源未说明故 runnable=false）承自 vault 页自评，如需引用请以论文原文复核；25% 提升数字转引自 vault 页对论文实验的记录。
