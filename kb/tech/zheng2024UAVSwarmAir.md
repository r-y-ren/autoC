---
id: zheng2024UAVSwarmAir
name: 迁移增强MARL的UAV蜂群空战机动决策
field: [多智能体强化学习, 迁移学习, 无人机蜂群]
published: 2024-01-01
maturity: paper
directions: [黑客松与数据竞赛, 数模与时序预测, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: Science China Information Sciences
  runnable: false
competition_fit:
  - track: 黑客松-数据与算法
    edge: 先在稳定的一对一空战场景预训练、再把表征迁移到蜂群对抗环境 + 奖励分配机制的分阶段 MARL 框架，可整体迁移到多机协同避障/对抗博弈/群体决策类仿真赛题；reward assignment 对懒惰智能体的 credit assignment 修正是多智能体团队题的通用组件
    reuse_cost: 中
  - track: 数模-数据分析与决策
    edge: 竞争-协作双重耦合场景的多智能体建模思路（actor 吃局部可执行态势、critic 吃全局态势的分层设计），为博弈/对抗类数模题提供 MARL 求解骨架；无迁移、无奖励分配的消融基线设计可直接借鉴
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 蜂群协同作业训练方法论背书——先单机后集群的分阶段训练与按贡献重分摊团队收益的机制，可转写为植保/巡检多机协同作业系统的训练与激励策略
    reuse_cost: 低
sources:
  - paper_title: "UAV Swarm Air Combat Maneuver Decision-Making Method Based on Multi-Agent Reinforcement Learning and Transferring"
    doi: 10.1007/s11432-023-4088-2
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 迁移增强MARL的UAV蜂群空战机动决策

## 单行摘要

针对短距 UAV 蜂群空战中协同与对抗双重耦合导致的训练不稳定与懒惰智能体问题，设计可处理不同态势信息的 actor 网络与局部-全局分层结构，并通过单机空战向蜂群空战的迁移训练和奖励分配机制，提升蜂群机动决策质量与训练效率。

## 方法快照

- 场景特征：蜂群智能体同时与敌方（对抗）和友方（协作）交互，状态变化快、动作与回报高度耦合，从头训练复杂蜂群策略易协作退化。
- 表征设计：actor 侧重局部可执行信息，critic 利用更完整的全局态势评估——局部-全局分层适配高动态对抗。
- 迁移训练：先在更稳定的一对一空战场景预训练基础网络，再把相关表征迁移到多机对抗环境，分阶段降低训练难度。
- 奖励分配：通过 reward assignment 重新分摊团队收益，缓解多智能体协作中的 credit assignment 问题、避免局部智能体躺平。
- 验证：合成蜂群空战环境仿真，消融基线为无迁移训练、无奖励分配（页内自评复现 medium）；训练平台与代码未披露。

## 比赛映射要点

- 黑客松/仿真赛：军事场景本身不构成迁移边界，可迁移的是算法组件——分阶段迁移训练框架适用于多机协同避障、对抗博弈、群体决策类题目；奖励重分配适用于一切团队型多智能体问题。
- 数模赛：竞争-协作耦合建模与局部/全局信息分层，可直接迁移到对抗-合作并存的多主体决策题。
- 双创申报：多机协同作业的分阶段训练与贡献分配激励设计叙事。

## 关联概念（vault 概念页折叠于此，不独立成卡）

- **空战机动决策**：空中对抗场景下智能体根据敌我态势实时选择机动动作、协同策略与攻击/规避行为；在本篇中被写成兼具竞争与协作的多智能体问题。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Zheng2024_迁移增强MARL的UAV蜂群空战机动决策`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `zheng2024UAVSwarmAir` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写。
- 复现性承自 vault 页自评（medium，仿真验证、平台与代码未披露）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
- 概念页 `空战机动决策.md`（vault，tags 含"概念"）已按跑批规程折叠进本卡"关联概念"节。
