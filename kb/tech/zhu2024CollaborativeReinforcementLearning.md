---
id: zhu2024CollaborativeReinforcementLearning
name: ZD-RL：协同强化学习的三维UAV跟踪与定位
field: [多机协同强化学习, UAV 轨迹优化, 无线定位]
published: 2024-01-01
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
  - track: 数模-预测与评估
    edge: 一架主动 UAV 发射 + 四架被动 UAV 接收的协同定位结构，附受控 UAV 相对位置如何影响最小可达定位误差的几何分析——目标跟踪/多源定位类赛题的观测模型与误差评估模板
    reuse_cost: 中
  - track: 数模-数据分析与决策
    edge: 发射功率与多机轨迹统一建模的序贯决策，Z function decomposition 直接学习未来回报分布（论文自报较 VD-RL 定位误差最多降 39.4%）是差异化求解器
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 多智能体协同 RL 跟踪框架可直接复用于仿真环境下的无人机追踪/围捕类赛题，功率-轨迹耦合建模是与常规路径规划的差异点
    reuse_cost: 中
sources:
  - paper_title: Collaborative Reinforcement Learning Based Unmanned Aerial Vehicle (UAV) Trajectory Design for 3D UAV Tracking
    doi: 10.1109/TMC.2024.3382913
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# ZD-RL：协同强化学习的三维UAV跟踪与定位

## 单行摘要

用 1 架主动 UAV 发射定位信号、4 架被动 UAV 接收反射信号、地面 BS 汇聚多路测距估计目标坐标，把主动 UAV 发射功率与全部 UAV 轨迹统一建模为定位误差最小化问题，并提出基于 Z function decomposition 的协同强化学习 ZD-RL：直接学习未来回报分布而非单一期望值，改善协同训练稳定性与三维定位精度。

## 方法快照

- 协同定位结构：主动-被动多机几何布局提供三维定位所需的多重测距约束，BS 融合估计目标位置。
- 功率-轨迹耦合：被动 UAV 与目标距离影响测距精度，主动 UAV 功率影响 SNR，两者必须联合优化。
- 误差分析：论文除学习算法外还分析了受控 UAV 相对目标位置对最小可达定位误差的影响，兼具几何建模与方法属性。
- ZD-RL：以回报分布学习替代传统 value decomposition，服务定位误差最小化而非通信吞吐。
- 论文自报（仿真）：较 VD-RL 与独立 DRL 定位误差最多分别降 39.4% 与 64.6%；代表性场景最小定位误差约 1.61m；训练平台与代码未披露。

## 比赛映射要点

- 数模-预测与评估：多源测距 + 几何误差分析是"跟踪/定位/估计"类题目的观测与评估环节模板。
- 数模-数据分析与决策：功率与轨迹联合的序贯决策建模，可讲清"控制变量如何影响评估指标"。
- 黑客松：多智能体 RL + 仿真追踪场景（如无人机围捕）现成框架。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Zhu2024_协同强化学习的三维UAV跟踪与定位`（venue_tier/evidence_tier/paper_role/reproducibility_level 自页 frontmatter 迁移）；正文性能数字均为论文自报仿真值，非本库实测。
- bib 回填：citekey `zhu2024CollaborativeReinforcementLearning` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写；验证类信息（simulation/synthetic、复现性 medium、无开源说明）承自 vault 页自评，如需引用请以论文原文复核。
