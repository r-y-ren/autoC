---
id: Symmetry-Informed_MARL_A_Decentralized_and_Cooperative_UAV_Swarm_Control_Approach_for_Communication_Coverage
name: 对称性增强MARL的UAV集群通信覆盖控制（SiGNN）
field: [多智能体强化学习, 图神经网络, 无人机集群控制]
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
    edge: 把旋转/反射/实体排列对称性硬编码进策略与价值网络（SiGNN）以大幅提升样本效率与规模可扩展性，是多智能体连续控制类赛题（覆盖/编队/围捕）可直接复用的结构先验技巧；5-20 架训练设置与 Jetson Nano 推理时延评测可直接参考
    reuse_cost: 中
  - track: 数模-数据分析与决策
    edge: 连续平面 PoI 覆盖最大化的对称 Dec-POMDP 建模（覆盖质量+运动代价+协作效率的奖励设计）为应急通信部署/区域覆盖类数模题提供"学习法对照解析法"的求解路线与实验对照框架
    reuse_cost: 中
sources:
  - paper_title: "Symmetry-Informed MARL: A Decentralized and Cooperative UAV Swarm Control Approach for Communication Coverage"
    doi: 10.1109/TMC.2025.3553285
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 对称性增强MARL的UAV集群通信覆盖控制（SiGNN）

## 单行摘要

论文将多 UAV 通信覆盖建模为对称 Dec-POMDP，设计 SiGNN 把旋转、反射与实体排列对称性硬编码进 MARL 策略/价值网络（而非软约束或数据增强），使模型无需为大量"本质等价"的状态-动作排列重复学习，在最多 20 架 UAV 的连续控制覆盖任务上显著提升样本效率、可扩展性与鲁棒性。

## 方法快照

- 核心观察：覆盖任务天然带空间对称性——某架 UAV 的局部观测整体旋转时，最优动作应同样旋转；利用该结构先验可省去重复学习。
- 问题建模：去中心化部分可观测决策问题（对称 Dec-POMDP），二维连续平面 + 随机分布 PoI，每架 UAV 有固定覆盖半径与观测半径，输出连续二维速度动作。
- SiGNN：在局部图结构中编码几何对称性与邻接关系，直接作为策略/价值网络；相比对称性正则或数据增强，属于"硬编码结构先验"，更适合连续动作与邻居关系变化的大规模场景。
- 奖励设计：兼顾覆盖质量、运动代价（能耗/平滑性）与协作效率。
- 验证：Python/PyTorch，100×100 区域、三高斯混合 PoI 采样、5/10/15/20 架 UAV 训练规模，持续优于多类对称增强或图学习覆盖控制基线；并在 Jetson Nano 上评测机载推理时延（4090+i9-12900KF 训练）。

## 比赛映射要点

- 黑客松/算法赛：等变网络结构先验是 MARL 赛题（多智能体协作控制、游戏 AI）的通用加速技巧——凡是观测旋转等价于动作旋转的任务都适用；样本效率优势在赛期算力受限时尤其值钱。
- 数模：覆盖类赛题常止步于解析部署；本卡提供"局部观测+连续控制"的动态覆盖学习建模与多规模对照实验设计，可作为答卷中学习法路线的差异化方案。

## 关联概念
- 对称性增强多智能体强化学习
- 图神经网络（GNN）

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Shi2025_面向通信覆盖的对称性增强UAV集群MARL控制`（四枚举字段自该页 frontmatter 迁移）。
- citekey-bib 错配留痕：分片 citekey 为长标题式 `Symmetry-Informed_MARL_..._Communication_Coverage`；bib map 中对应条目键为 `shi2025SymmetryinformedMARLDecentralized`，其标题与页内容（页 sources 指向 raw/markdown 同名原文）一致，故据该条目回填 venue/DOI；本卡 id 与文件名保留分片 citekey 原样。
- bib 回填：标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写；复现性 medium 与 PyTorch 仿真形态承自 vault 页自评（artifact_availability: unknown，未给出完整开源代码），如需引用请以论文原文复核。
