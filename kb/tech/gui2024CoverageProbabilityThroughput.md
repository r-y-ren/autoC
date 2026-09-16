---
id: gui2024CoverageProbabilityThroughput
name: mmWave与Sub-6GHz融合多UAV灾害网络的覆盖-吞吐联合优化
field: [无人机通信网络, 覆盖优化, 深度强化学习]
published: 2024-01-01
maturity: paper
directions: [创新创业大赛, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 双创-文书与申报
    edge: 灾害应急通信/农业灾情监测申报题材：「先覆盖后吞吐」两阶段设计 + 有效覆盖时间×被覆盖终端比例的新覆盖指标是差异化论证点
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 把信道与功率波束分配写成带频谱-能效约束的 MDP 并用 DDPG 求解，可迁移到资源分配+覆盖部署复合算法题
    reuse_cost: 中
sources:
  - paper_title: "Coverage Probability and Throughput Optimization in Integrated mmWave and Sub-6 GHz Multi-UAV-assisted Disaster Relief Networks"
    doi: 10.1109/TMC.2024.3386550
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# mmWave与Sub-6GHz融合多UAV灾害网络的覆盖-吞吐联合优化

## 单行摘要

面向地面基础设施受损的灾害救援场景，先提出兼顾有效覆盖时间比例与被覆盖终端比例的新型覆盖质量指标并优化多 UAV 部署覆盖，再把 mmWave 与 Sub-6GHz 融合链路的信道与功率波束分配写成带频谱-能效约束的 MDP、用 DDPG 学习策略——覆盖与吞吐作为顺序耦合的两阶段在同一条灾害通信主线上联合优化。

## 方法快照

- 覆盖层：新覆盖质量指标超越静态半径式定义（同时看有效覆盖持续时间与被覆盖终端比例）；利用终端分布不均设计覆盖改进与部署成本降低策略。
- 传输层：信道+功率波束分配建模为约束 MDP，DDPG 求解；Sub-6GHz 保覆盖稳定性、mmWave 供高吞吐的双频融合。
- 跨层耦合：部署/覆盖与传输资源控制顺序串联，而非各自独立优化。
- 环境：Python 3.9.6 + PyTorch 1.13.1 仿真（Apple M2），配置较清楚但开源未说明。

## 比赛映射要点

- 双创申报：灾害应急通信是双创常见题材，可自然延伸到农业灾情监测与应急组网；「新覆盖指标+双频融合」比「无人机基站」式泛泛方案更有技术辨识度。
- 黑客松：约束 MDP+DDPG 的资源分配结构可复用到覆盖部署、频谱/功率分配类算法题；新覆盖指标本身也可作为赛题评价口径的改进主张。

## 溯源说明

- 提炼来源：my_LLM_valut wiki 页 `Gui2024_mmWave与Sub-6GHz融合多UAV灾害网络覆盖吞吐优化`；citekey `gui2024CoverageProbabilityThroughput`。
- bib 回填：标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写。
- 复现性 medium 承自 vault 页自评（软件环境与仿真配置清楚、开源情况未说明）；如需引用请以论文原文复核。
