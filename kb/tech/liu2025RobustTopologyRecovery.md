---
id: liu2025RobustTopologyRecovery
name: RTRA/CRTRA：UAV蜂群鲁棒拓扑恢复
field: [UAV 蜂群, 拓扑恢复, 代数连通度]
published: 2025-01-01
maturity: paper
directions: [创新创业大赛, 黑客松与数据竞赛, 数模与时序预测]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 黑客松-数据与算法
    edge: 割点/冗余节点识别 + 级联移动分担位移 + 代数连通度导向选点的图连通性修复组合，直接可落网络修复/图鲁棒性类算法题，优于只修补当前割点的贪心重定位基线
    reuse_cost: 中
  - track: 数模-数据分析与决策
    edge: 把恢复当前连通与降低未来再断裂频率统一进节点选择的建模思路，适配网络韧性/设施抗毁评估类题目，代数连通度可作为韧性的量化指标
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 农业植保无人机蜂群自愈组网（单机失效不中断作业）的系统可靠性技术支撑（TMC 2025，长期连通性维护）
    reuse_cost: 低
sources:
  - paper_title: "On the Robust Topology Recovery of UAV Swarm for Detection and Localization of Electronic Signals"
    doi: 10.1109/TMC.2025.3586447
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# RTRA/CRTRA：UAV蜂群鲁棒拓扑恢复

## 单行摘要

面向电子信号探测定位任务中 UAV 蜂群因干扰、故障或电量耗尽导致的拓扑分裂问题，提出两类鲁棒拓扑恢复算法：RTRA 优先重定位对修复最有效且位移最短的冗余节点并纳入未来鲁棒性增益权重；CRTRA 在其上引入级联移动让多机接力分担位移成本，避免单个被调度节点过度耗电；两者都把代数连通度引入节点选择，使恢复动作同时修补当前割点并提升后续阶段的拓扑鲁棒性。

## 方法快照

- 问题结构：蜂群拓扑连通性决定探测数据能否汇聚用于定位；节点失效导致拓扑分裂，任务直接中止。
- 节点角色：割点（失效即分裂）、冗余节点（可重定位的修复候选）、普通节点。
- RTRA：最短位移修复当前拓扑，同时把潜在鲁棒性增益纳入权重。
- CRTRA：级联移动多节点接力分摊位移，防止单机因恢复动作过快耗尽电量。
- 鲁棒性判断：未来潜在断裂风险写入当前恢复选择，从修一次转向长期连通性维护。
- 验证：Python 自建模拟器（400m×400m×400m 空域，100 次仿真平均，对比不同失效模式）；无标准化开源包。

## 比赛映射要点

- 黑客松算法题：割点识别+冗余节点调度+级联移动是一套完整可复刻的图连通性修复流水线，图论类赛题的差异化组件。
- 数模决策题：网络韧性量化（代数连通度）+ 长期维护决策建模，适配抗毁评估、应急网络规划类题。
- 双创申报：集群作业可靠性叙事（自愈网络、任务不中断）支撑。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Liu2025_电子信号探测定位中的UAV蜂群鲁棒拓扑恢复`（venue_tier/evidence_tier/paper_role/reproducibility_level 承自该页 frontmatter）。
- bib 回填：citekey `liu2025RobustTopologyRecovery` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2025），按年-01-01 填写；验证类信息（simulation/synthetic/复现性 medium）承自 vault 页自评，如需引用请以论文原文复核。
