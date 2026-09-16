---
id: tang2025DeepGraphReinforcement
name: 图强化学习双层求解UAV多用户安全通信
field: [物理层安全, 图神经网络, 分层强化学习]
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
    edge: 内层 GNN 近似非凸波束赋形 + 外层 SAC 学部署的双层结构化学习模板——让图网络先吸收实体关系、DRL 只管大尺度决策，可迁移到图结构决策/跨尺度变量耦合类优化赛题，规避单层 DRL 直接啃高维变量的训练不稳
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 低空经济安全通信专网（无人机空中基站防窃听）方案支撑点，UAV 可移动性作为物理层安全自由度的叙事 + 8 对用户-窃听者 8 天线的具体实验配置可直接复述
    reuse_cost: 低
sources:
  - paper_title: "Deep Graph Reinforcement Learning for UAV-enabled Multi-User Secure Communications"
    doi: 10.1109/TMC.2025.3558790
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 图强化学习双层求解UAV多用户安全通信

## 单行摘要

面向单 UAV 空中基站服务多用户且每用户对应一个窃听者的保密通信场景：UAV 部署位置（大尺度空间变量）与安全波束赋形（小尺度传输变量）跨尺度耦合，传统解析优化难以在复杂拓扑下实时适配。论文拆成两层学习——内层把安全波束赋形解释为图学习任务，用 5 层 GCN 依据用户-窃听者图关系输出近似最优波束；外层用 soft actor-critic 依据内层安全收益反馈学习 UAV 部署位置——在 200m x 200m 区域、8 对用户-窃听者、8 天线配置下，secrecy rate 显著优于区域中心、几何中心、外接圆心等部署基线。

## 方法快照

- 问题抽象：多用户 MISO 保密通信，合法链路与窃听链路都依赖 UAV 空间位置，目标是最大化整体 secrecy rate。
- 跨尺度解耦：大尺度部署（SAC 外层）与小尺度传输（GNN 内层）分开学习，DRL 不直接接触高维波束变量。
- 图结构先验：用户、窃听者与 UAV 天然构成图依赖，GNN 让不同用户-窃听者关系共享表达能力。
- 实验设置：5 层 GCN、SAC 训练 500 轮、Rician 因子 10dB；灵活部署对安全收益提升显著。
- 验证：数值仿真（合成拓扑），平台/代码/训练硬件均未披露，复现性 medium。

## 比赛映射要点

- 黑客松：双层「近似器 + 决策器」架构是通用的——凡问题里同时存在「连续高维配置变量」与「离散/大尺度布局变量」，都可让 GNN/小模型管内层、RL/搜索管外层；图关系建模可迁移到带对抗关系的网络设计题。
- 双创申报：低空专网、无人机应急通信安全保障等项目的物理层安全技术点（移动性即安全自由度的论证角度新颖）。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Tang2025_图强化学习驱动的UAV多用户安全通信`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `tang2025DeepGraphReinforcement` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写。
- 复现性承自 vault 页自评（medium，仿真级、实现资产未披露）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
