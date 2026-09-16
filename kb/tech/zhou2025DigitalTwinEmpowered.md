---
id: zhou2025DigitalTwinEmpowered
name: 数字孪生赋能的UAV辅助毫米波多跳V2X路由
field: [数字孪生网络, 毫米波 V2X 路由]
published: 2025-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 街道内中继选择与路口 RL 街道选择的两级路由决策，综合车辆密度/网络负载/链路质量/传输距离多因素——城市交通网络类赛题中"分层决策 + 多因素权衡"的建模模板
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 街道/路口/Core 三层数字孪生加 UAV 路口中继的架构模式可直接复用于城市车流仿真与网络路由类赛题；RL 代理放孪生侧而非机载侧的轻量化设计是差异化点
    reuse_cost: 中
sources:
  - paper_title: Digital Twin Empowered mmWave Multi-Hop V2X Routing Scheme with UAV Assistance
    doi: 10.1109/TMC.2025.3556091
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 数字孪生赋能的UAV辅助毫米波多跳V2X路由

## 单行摘要

面向城市高密度 VANET 的毫米波多跳路由：论文把每条街道与路口映射为数字孪生子体并由核心 DT 统一同步，街道内由 sub-DT 协助中继选择与波束宽度配置，跨街道转发由部署在路口的 UAV 中继承担、经 intersection sub-DT 中的强化学习代理做街道选择，联合提升分组投递率并降低时延。

## 方法快照

- 分层孪生架构：street sub-DT（街道内链路视图）+ intersection sub-DT（路口全局视图）+ Core DT（跨层同步）。
- 街道内转发：按候选节点负载、链路质量与距离做下一跳选择，并调节毫米波波束宽度。
- 路口跨街道转发：UAV 中继利用快速部署与 LoS 优势；RL 代理部署在 intersection sub-DT 而非 UAV 本体，减轻机载资源消耗。
- 街道选择策略结合车辆密度与网络负载，减少拥塞与时延。
- 验证：合成城市 VANET 场景仿真；仿真平台与代码开源情况未披露，论文自报结果。

## 比赛映射要点

- 数模：两级路由决策（局部中继 + 全局街道选择）是交通/网络类赛题的多阶段决策范式，评价指标（投递率/时延/跳数）可直接用作目标函数组。
- 黑客松："物理层-虚拟层-决策层"三层孪生画法与"RL 放边缘侧"的工程取舍都可整体迁移到智慧交通、车路协同类赛题方案。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Zhou2025_数字孪生赋能的UAV辅助毫米波多跳V2X路由`（venue_tier/evidence_tier/paper_role/reproducibility_level 自页 frontmatter 迁移）。
- bib 回填：citekey `zhou2025DigitalTwinEmpowered` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写；验证类信息（simulation、复现性 medium、无开源说明）承自 vault 页自评，如需引用请以论文原文复核。
