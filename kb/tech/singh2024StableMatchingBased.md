---
id: singh2024StableMatchingBased
name: 稳定匹配+图着色的UAV辅助WBAN联邦学习收益最大化
field: [联邦学习, 稳定匹配, 无线资源分配]
published: 2024-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Services Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 稳定匹配生成 UAV-PRB-WBAN 候选配对 + 图着色/最大权独立集处理干扰复用 + 收益分成统一建模，是"匹配理论+资源复用+激励机制"类赛题的完整求解骨架；Shanghai Telecom 真实数据集与 Gurobi 对照现成可复用
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 稳定匹配与图着色均为可独立复用的经典算法组件，叠加 FL 收益模型即可快速搭出"隐私友好数据采集+干扰感知资源分配"的可演示原型；附真实生理数据采集与手机/树莓派原型清单
    reuse_cost: 中
sources:
  - paper_title: "Stable Matching Based Revenue Maximization for Federated Learning in UAV-assisted WBANs"
    doi: 10.1109/TSC.2024.3360692
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 稳定匹配+图着色的UAV辅助WBAN联邦学习收益最大化

## 单行摘要

在 5G 支撑的 UAV 辅助身体域网（WBAN）联邦学习场景中，论文把 FL 数据收集、PRB 分配与收益分成统一为一个资源分配问题：先以稳定匹配框架确定 UAV-PRB-WBAN 三方候选配对，再用图着色/最大权独立集处理同频干扰下的资源复用，联合最大化 UAV 与 WBAN 双方收益。

## 方法快照

- 系统场景：医疗/生理监测 WBAN 经 5G 向 UAV 上传生理数据参与 FL 训练；UAV 回基地后在 MBS 协助下完成训练，MBS 负责 PRB 管理。
- 问题性质：WBAN 的最小/最大 PRB 需求各异且上传互相干扰，收益最大化问题是 NP-hard 优化。
- 求解框架：收益函数同时计入 WBAN 贡献数据的价值、UAV 提供训练与通信资源的收益及上传成本；稳定匹配构造偏好与候选集合，干扰图上冲突资源对借图着色与最大权独立集实现安全复用。
- 核心论点：UAV-assisted FL 的资源分配不是纯通信问题，而与数据价值、模型精度和服务收益直接耦合。
- 验证：数值仿真 + 真实数据（Shanghai Telecom dataset）+ 小型原型（Python 3.9、Gurobi；树莓派 4B、Phantom 4 Pro V2.0、三星/一加手机），是同批文献中最接近真实系统的一篇。

## 比赛映射要点

- 数模：匹配+着色的两层求解可迁移到任何"双方偏好+冲突约束+收益分配"题型（结对交换、资源共享、任务指派）；"数据价值-服务收益"的分成建模为激励类问题提供量化骨架。
- 黑客松/数据赛：FL+激励机制的组合适合隐私主题赛题；稳定匹配与图着色组件可独立复用，公开数据集驱动仿真降低了原型门槛。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Singh2024_基于稳定匹配的UAV辅助WBAN联邦学习收益最大化`（四枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `singh2024StableMatchingBased` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写；复现性 medium 与"仿真+原型+真实数据"验证形态承自 vault 页自评（artifact_availability: unknown，开源情况未说明），如需引用请以论文原文复核。
