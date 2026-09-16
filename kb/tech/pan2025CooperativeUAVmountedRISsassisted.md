---
id: pan2025CooperativeUAVmountedRISsassisted
name: INSGA-II-CDC：协同UAV-RIS能效通信三目标优化
field: [UAV-RIS 通信, 多目标优化, 能效设计]
published: 2025-01-01
maturity: paper
directions: [黑客松与数据竞赛, 数模与时序预测]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 黑客松-数据与算法
    edge: 对连续/离散/复数三类决策变量分别定制进化算子的 NSGA-II 增强版（INSGA-II-CDC），混合变量多目标优化赛题可直接改造复用，超越标准 NSGA-II 基线
    reuse_cost: 中
  - track: 数模-数据分析与决策
    edge: 最小用户速率（公平）-总速率（容量）-总能耗的三目标 Pareto 权衡建模，决策变量横跨波束、三维部署与离散相位，是数模多目标优化题的标准问题结构
    reuse_cost: 中
sources:
  - paper_title: Cooperative UAV-mounted RISs-assisted Energy-Efficient Communications
    doi: 10.1109/TMC.2025.3579597
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# INSGA-II-CDC：协同UAV-RIS能效通信三目标优化

## 单行摘要

面向直达链路受限的多用户蜂窝场景，把 BS 波束、多 UAV 挂载 RIS 的三维部署与离散相位写成统一的三目标优化框架 EEComm-MOF，提出 INSGA-II-CDC 多目标进化算法对连续、离散、复数变量分别定制处理机制，在公平速率、总速率与总能耗之间求 Pareto 折中，并给出 Raspberry Pi 侧实现性分析。

## 方法快照

- 系统建模：BS-地面用户直达链路不可用，通信依赖多个 UAV-RIS 反射链路；RIS 元件用离散相位量化，贴近 UAV 硬件负载约束。
- 三目标：最小可用速率（用户公平）、总可用速率（容量）、总能耗（含 UAV 飞行能耗与通信能耗）——部署位置直接影响能效。
- INSGA-II-CDC：在 NSGA-II 基础上分别为连续变量、离散变量、复数变量设计解处理机制，增强混合变量搜索能力。
- 验证：大规模仿真（MATLAB + Python，合成场景）考察收敛性、稳定性与多目标最优性；Raspberry Pi 4B 实现性分析验证运行时间可接受；未开源统一工程代码。

## 比赛映射要点

- 黑客松/算法赛：混合变量（连续 + 离散 + 复数）多目标优化是常见题型难点，本文「按变量类型定制进化算子」的思路可直接迁移，比直接套标准 NSGA-II 有差异化与精度优势。
- 数模多目标题：公平-容量-能耗的三角冲突 + Pareto 前沿呈现是数模论文的标准分析结构，目标函数设定与权衡讨论框架可整体借鉴。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Pan2025_协同UAV挂载RIS能效通信优化`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `pan2025CooperativeUAVmountedRISsassisted` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写。
- 复现性承自 vault 页自评（medium，仿真 + 原型级实现性分析、未开源）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
