---
id: hao2025ReliabilityawareOptimizationTask
name: 可靠性感知UAV辅助边缘计算任务卸载优化
field: [UAV 辅助边缘计算, 可靠性建模, 深度强化学习]
published: 2025-01-01
maturity: paper
directions: [黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Computers
  runnable: false
competition_fit:
  - track: 黑客松-数据与算法
    edge: 把"任务可能失败"写进优化目标（长期平均任务成功率替代平均时延），dependence-aware 潜空间+TD3 处理离散-连续混合动作，对带失败重试/可用性约束的调度类赛题是稀缺的目标函数设计参照
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 面向基础设施薄弱环境的 UAV 边缘计算可靠性设计（Kubernetes 测试床验证），正中乡村网络条件差的智慧农业落地痛点，申报书可信度支撑强（TC 2025）
    reuse_cost: 低
sources:
  - paper_title: "Reliability-Aware Optimization of Task Offloading for UAV-assisted Edge Computing"
    doi: 10.1109/TC.2025.3604463
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 可靠性感知UAV辅助边缘计算任务卸载优化

## 单行摘要

针对基础设施薄弱环境中 UAV 与无线链路均不可靠的现实，把任务成功率作为核心目标，联合优化轨迹、卸载决策与传输功率以最大化长期平均任务成功率；用 task-driven 决策替代 time-driven 策略避免额外等待，并以 Kubernetes 测试床补强仿真验证，是可靠性感知卸载分支里少有的"仿真+测试床"双证据工作。

## 方法快照

- 目标重构：从平均时延/能耗转向端到端任务成功率（失败可来自链路传输或计算执行环节）。
- 决策机制：task-driven 事件驱动决策，避免 time-driven 策略引入额外等待时间。
- 求解：可靠性感知协同卸载问题转 MDP；dependence-aware 潜空间表示处理离散-连续混合动作空间，结合 TD3 联合学习卸载、功率与轨迹控制。
- 验证：数值仿真 + Kubernetes 测试床（混合数据来源）；未说明开源。

## 比赛映射要点

- 黑客松算法题：目标函数设计（成功率优先于时延）与混合动作 DRL 组件可迁移到带失败概率的调度/路由赛题，与常见"只优化时延"的队伍形成差异化。
- 双创申报："弱基础设施可用"正是农村场景卖点，测试床证据让方案从纸面设计升级为工程验证叙事。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Hao2025_可靠性感知的UAV辅助边缘计算任务卸载优化`（venue_tier/evidence_tier/paper_role/reproducibility_level 承自该页 frontmatter）。
- bib 回填：citekey `hao2025ReliabilityawareOptimizationTask` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2025），按年-01-01 填写；验证类信息（simulation+emulation/mixed/复现性 medium）承自 vault 页自评，如需引用请以论文原文复核。
