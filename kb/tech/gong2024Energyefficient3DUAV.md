---
id: gong2024Energyefficient3DUAV
name: 最少UAV数的三维节能地面节点接入
field: [三维路径规划, 能耗优化, 组合优化]
published: 2024-01-01
maturity: paper
directions: [创新创业大赛, 数模与时序预测, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 「UAV 数量+节点分配+访问顺序+三维轨迹」联合优化本质是 VRP 变体，单机两点最优能耗+多机路径分配的双层分解可直接套用于数模路径规划/资源配置赛题
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 以「最少无人机完成全覆盖」压低硬件与部署成本，为智慧农业监测申报提供能耗-成本量化论证（MATLAB/CVX 链条清晰）
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 最小车队规模+节能访问顺序类算法题可迁移其双层分解求解思路（几何能耗子问题闭式解 + 上层组合分配）
    reuse_cost: 中
sources:
  - paper_title: "Energy-Efficient 3-D UAV Ground Node Accessing Using the Minimum Number of UAVs"
    doi: 10.1109/TMC.2024.3405494
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# 最少UAV数的三维节能地面节点接入

## 单行摘要

把多 UAV 三维地面节点接入从「给定机群压能耗」推进为「同时决定用几架、谁访问哪些节点、按什么三维轨迹飞」：先解析求解单机连续访问任意两节点时的能耗最优三维控制，再把多机节点路径分配与 UAV 数量选择统一到同一框架，在更一般的 3D 场景中实现最少 UAV 的节能接入。

## 方法快照

- 子问题：单 UAV 两节点间三维飞行的能耗最优控制——能耗不只依赖水平距离，还与三维姿态和轨迹控制相关。
- 上层问题：节点到 UAV 的分配与访问顺序，VRP 型组合结构；凸优化+启发式/群智能路径分配联合求解。
- 数量维度：把 UAV 数量纳入决策变量，从「固定规模优化」推进到「必要规模优化」，权衡增机省能与硬件成本。
- 工具链：MATLAB/CVX 仿真验证最少 UAV 约束下的能耗优势。

## 比赛映射要点

- 数模：最小车队数+节能路径的双层分解（下层闭式/凸解、上层组合分配）是覆盖访问、配送规划类赛题的标准可复用结构，比直接调 TSP 启发式更有建模深度。
- 双创申报：「最少无人机完成全覆盖」直接对应农业监测的硬件成本与续航论证，工程化问题定义评委友好。
- 黑客松：最小车辆数覆盖/节能路径类算法题可迁移其分解思路作差异化解法。

## 溯源说明

- 提炼来源：my_LLM_valut wiki 页 `Gong2024_使用最少UAV的三维节能地面节点接入`；citekey `gong2024Energyefficient3DUAV`。
- bib 回填：标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写。
- 复现性 medium 承自 vault 页自评（MATLAB/CVX 实验链条清晰但开源情况未说明）；如需引用请以论文原文复核。
