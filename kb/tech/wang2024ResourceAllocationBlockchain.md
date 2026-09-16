---
id: wang2024ResourceAllocationBlockchain
name: 区块链UAV-MEC的Stackelberg微分博弈资源定价
field: [移动边缘计算, 区块链, 微分博弈]
published: 2024-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Services Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 用户服务需求与验证节点信誉都被建成随时间演化的微分方程状态，再做两阶段 Stackelberg 微分博弈求开环均衡——「动态状态演化 + 领导者定价 / 跟随者分配」为定价与资源分配类数模题提供完整建模求解模板
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 信誉机制筛选验证节点 + 单位资源价格动态均衡的组合，可直接作为「算力 / 资源交易平台」赛题中供给侧激励与定价算法的差异化组件，区块链记账层提供可信交易叙事
    reuse_cost: 高
  - track: 双创-文书与申报
    edge: 农业植保无人机算力服务场景下「可信资源交易 + 信誉激励」的技术支撑点（TSC 2024 机制设计，DPoS 全量记账保障透明）
    reuse_cost: 低
sources:
  - paper_title: "Resource Allocation in Blockchain Integration of UAV-enabled MEC Networks：A Stackelberg Differential Game Approach"
    doi: 10.1109/TSC.2024.3418330
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# 区块链UAV-MEC的Stackelberg微分博弈资源定价

## 单行摘要

在区块链集成的 UAV 辅助 MEC 网络中，UAV 主节点（DPoS 机制）作为领导者发布单位资源价格，由信誉机制选出的边缘验证节点作为跟随者决定计算资源供给；由于用户需求与验证节点信誉都随时间动态演化，论文将两者写成微分方程约束，构建两阶段 Stackelberg 微分博弈并求开环均衡，在链上全量记账保障可信交易的同时提升 QoS 与资源利用效率。

## 方法快照

- 系统实体：UAV 主节点（兼移动 MEC 服务提供者）、多个信誉验证节点、地面用户、区块链账本。
- 状态建模：用户服务需求与验证节点信誉均为随时间变化的动态状态（微分方程约束），静态定价无法反映真实供需。
- 博弈结构：第一阶段 UAV 定价，第二阶段验证节点按收益决定资源分配；求开环解观察价格、分配、需求与信誉的收敛行为。
- 区块链角色：不是附加记录层，而是改变资源价格、信誉激励与验证节点参与积极性的机制层（DPoS、100% 交易上链）。
- 验证：MATLAB R2018b 数值仿真、合成场景，给出完整参数表与状态演化实验；代码与区块链实现细节未披露，无开源。

## 比赛映射要点

- 数模决策类：动态状态 + 博弈均衡的建模链路可整体迁移到「定价与资源分配」题型；微分方程约束刻画供需 / 信誉演化的写法可直接复用。
- 黑客松算法类：资源竞价、拍卖或共享算力平台赛题中，信誉加权供给 + 领导者定价可作为超越静态拍卖基线的机制设计组件。
- 双创申报：无人机共享算力 / 农业算力服务平台叙事的可信交易机制背书。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Wang2024_区块链集成UAV_MEC的资源定价与分配`（4 枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `wang2024ResourceAllocationBlockchain` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）；标题中「: 」按本跑批 YAML 约定改写为全角冒号。
- `published` 仅年份已知（2024），按 2024-01-01 填写；复现性 medium 与 simulation/synthetic 验证形态承自 vault 页自评（artifact_availability: unknown），如需引用请以论文原文复核。
