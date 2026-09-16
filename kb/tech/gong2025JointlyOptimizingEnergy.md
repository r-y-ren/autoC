---
id: gong2025JointlyOptimizingEnergy
name: 多UAV三维区域覆盖的能量-时间双目标优化
field: [区域覆盖, 多目标优化, 能耗建模]
published: 2025-01-01
maturity: paper
directions: [创新创业大赛, 数模与时序预测]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: low
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 能耗-完成时间双目标 + 区域划分与覆盖路径联合设计的建模结构，是巡检/覆盖类赛题区别于单目标 CPP 的差异化框架，群智能+多任务学习求解器可复用
    reuse_cost: 高
  - track: 双创-文书与申报
    edge: 植保/巡检「续航-时效权衡」论证：考虑扭矩与加速度的精细能耗模型让续航测算有物理依据，支撑申报书的可信量化
    reuse_cost: 高
sources:
  - paper_title: "Jointly Optimizing the Energy and Time for Multi-UAV 3-D Coverage of Terrestrial Regions"
    doi: 10.1109/TMC.2025.3568788
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# 多UAV三维区域覆盖的能量-时间双目标优化

## 单行摘要

把多旋翼多 UAV 三维区域覆盖建模为能量与完成时间双目标联合最小化：指出现有工作通常只优化其一且能耗模型过粗会令权衡失真，引入显式考虑扭矩与加速度的多旋翼闭式能耗模型，并将区域划分与三维覆盖路径联合设计，用多任务学习增强的群智能框架搜索双目标更优解。

## 方法快照

- 能耗模型：显式纳入扭矩与加速度影响的闭式多旋翼能耗建模，提升能量目标的物理可信度（覆盖任务≠普通巡航）。
- 双目标结构：能耗与完成时间相互耦合，「飞得省电」与「尽快完成」存在张力，单目标方案在权衡上失真。
- 联合设计：任务划分（区域→各 UAV）与每机 3D 覆盖轨迹同时决策，而非先分区后局部规划。
- 求解：多任务学习增强的群智能优化框架；证据以仿真与模型验证为主，无开源实现。

## 比赛映射要点

- 数模：能量-时间双目标+分区-路径联合建模，可直接迁移到灾害巡检、农田监测等覆盖类赛题的目标函数设计，双目标帕累托讨论天然适合数模论文结构。
- 双创申报：支撑「作业窗口内最少能耗完成全覆盖」的续航-时效论证；但注意复现成本高（无代码、能耗模型需从零自建），宜作为建模思想引用而非直接复跑。

## 溯源说明

- 提炼来源：my_LLM_valut wiki 页 `Gong2025_多UAV三维区域覆盖的能量时间联合优化`；citekey `gong2025JointlyOptimizingEnergy`。
- bib 回填：标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写。
- 复现性 low 承自 vault 页自评（平台/软件未说明、开源情况未说明、证据以仿真与模型验证为主）；如需引用请以论文原文复核。
