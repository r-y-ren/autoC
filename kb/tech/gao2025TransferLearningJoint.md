---
id: gao2025TransferLearningJoint
name: PTMF-MAAC：大规模UAV-MEC的策略迁移联合轨迹卸载
field: [迁移学习, 多智能体强化学习, 移动边缘计算]
published: 2025-01-01
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
    edge: 智慧农业「无人机机群+边缘算力」巡检/植保申报的算法支撑：大规模机群低时延服务与训练成本论证，vault 页自评代码已公开
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 平均场近似压缩多智能体联合状态空间 + 策略迁移止步防负迁移，两招是大规模多体决策算法题的通用降维/加速套路
    reuse_cost: 中
sources:
  - paper_title: "Transfer Learning for Joint Trajectory Control and Task Offloading in Large-Scale Partially Observable UAV-assisted MEC"
    doi: 10.1109/TMC.2025.3579748
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# PTMF-MAAC：大规模UAV-MEC的策略迁移联合轨迹卸载

## 单行摘要

针对大规模部分可观测 UAV 辅助 MEC 中联合轨迹控制与任务卸载训练成本随规模爆炸的问题，提出 PTMF-MAAC：以策略迁移（含终止时机判断、防负迁移）缩短冷启动，以平均场近似把其他 UAV 的影响压缩为均值表示，在局部观测下做 actor-critic 联合学习，使策略随机群规模扩张仍可训练、可扩展。

## 方法快照

- 问题建模：部分可观测多智能体环境，每架 UAV 联合决定服务终端的轨迹与卸载决策；UAV 数量增长导致联合状态/动作空间指数级膨胀、样本需求剧增。
- 策略迁移：为每架 UAV 判断哪些历史策略可复用、何时终止迁移以避免负迁移，加速冷启动。
- 平均场近似：以均值表示替代对其余 UAV 交互影响的显式枚举，显著压缩联合空间规模。
- 联合动作：轨迹控制与任务卸载纳入同一策略输出空间，在部分可观测 MAAC 框架下学习。

## 比赛映射要点

- 双创申报：智慧农业「无人机机群+边缘算力」场景中，支撑「从可解小规模到可扩展大规模」的技术叙事——机群扩容时学习框架不失控是评委可感知的差异化点；vault 页自评代码已公开。
- 黑客松：多智能体调度、集群仿真类算法题中，平均场近似+迁移止步是直接可移植的降维与加速组件（对比朴素 MARL 基线在规模下的训练爆炸）。

## 溯源说明

- 提炼来源：my_LLM_valut wiki 页 `Gao2025_面向大规模部分可观测UAV辅助MEC的迁移学习联合轨迹卸载`；citekey `gao2025TransferLearningJoint`。
- bib 回填：标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写。
- 复现性 medium 承自 vault 页自评（数值仿真为主、vault 标注资产已公开但页内无具体链接，本卡 runnable 如实标 false）；如需引用请以论文原文复核。
