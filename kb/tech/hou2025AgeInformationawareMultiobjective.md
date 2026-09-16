---
id: hou2025AgeInformationawareMultiobjective
name: AoI感知异构UAV-USV-UUV水下目标围捕多目标优化
field: [异构无人系统, 信息年龄 AoI, 多智能体强化学习]
published: 2025-01-01
maturity: paper
directions: [黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 黑客松-数据与算法
    edge: 把 AoI（信息新鲜度）写进多智能体奖励的协同控制设计（AE-MVTD3），对追捕/围捕/协同覆盖类算法赛题提供了"信息时效作为一等目标"的差异化建模视角
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 空-海-水跨域异构协同架构（UAV 搜索-USV 中继-UUV 执行）可支撑智慧渔业/海洋牧场监测类申报的多平台协同叙事
    reuse_cost: 高
sources:
  - paper_title: "Age of Information-Aware Multi-Objective Optimization for Heterogeneous UAV-USV-UUV Networks in Underwater Target Hunting"
    doi: 10.1109/TMC.2025.3581836
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# AoI感知异构UAV-USV-UUV水下目标围捕多目标优化

## 单行摘要

构建 UAV-USV-UUV 异构 3U 网络（UAV 广域搜索、USV 空-海通信中继、UUV 群水下围捕），将 AoI 融入 UAV 搜索策略以衡量目标状态信息的新鲜度，在能耗与任务时长双目标以及动力学、障碍、涡流、通信连接与安全约束下构建多目标优化问题，并设计 AoI 与能量联合奖励引导的多车辆 TD3（AE-MVTD3）学习跨域协同控制策略。

## 方法快照

- 跨域分工：UAV 快速搜索跟踪 → USV 中继 → UUV 群围捕执行，UAV 从单域平台变为多平台协作链一环。
- AoI 引入：搜索效率不只看耗时，还看目标信息更新频率；AoI 进入 UAV 搜索奖励与联合建模。
- 多目标：总能耗与任务时长双目标，受连接与安全约束。
- 求解：AE-MVTD3（AoI+能量联合奖励的多车辆协同 DRL）；多场景比较任务成功率、AoI 与能耗。
- 验证：数值仿真（合成环境）；未说明平台与开源。

## 比赛映射要点

- 黑客松算法题：追捕/围捕/多机协同类赛题可借鉴其奖励设计——把信息新鲜度（AoI）与能耗同时写进 reward，区别于只优化到达时间的常见做法。
- 双创申报：跨域异构协同链可作为海洋渔业/水域监测类项目架构参考；跨域仿真环境搭建门槛高，标注 reuse_cost 高。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Hou2025_AoI感知的异构UAV-USV-UUV网络水下目标围捕优化`（venue_tier/evidence_tier/paper_role/reproducibility_level 承自该页 frontmatter）。
- bib 回填：citekey `hou2025AgeInformationawareMultiobjective` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2025），按年-01-01 填写；验证类信息（simulation/synthetic/复现性 medium）承自 vault 页自评，如需引用请以论文原文复核。
