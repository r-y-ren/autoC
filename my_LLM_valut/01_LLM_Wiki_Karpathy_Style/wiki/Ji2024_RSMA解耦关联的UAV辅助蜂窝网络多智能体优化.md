---
tags: [论文, 解耦关联, RSMA, UAV辅助蜂窝, 多智能体强化学习]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/ji2024DecoupledAssociationRate.md
venue_tier: CCF-A
literature_type: method
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - methodology
  - system_model
validation_type:
  - simulation
data_origin:
  - synthetic
platforms:
  - Python 3.6
frameworks:
  - PyTorch
datasets: []
hardware_stack:
  - NVIDIA GTX 2080 GPU
artifact_availability: unknown
reproducibility_level: medium
---


# Ji2024 RSMA解耦关联的UAV辅助蜂窝网络多智能体优化

## 单行摘要
论文把全双工多UAV蜂窝网络中的上下行解耦关联、RSMA 波束赋形与多智能体强化学习统一起来，以提升系统总速率。

## 题目驱动研究框架
- 研究场景：多 UAV 辅助蜂窝网络中的全双工上下行联合接入。
- 研究对象：MBS、多架 UAV 基站、用户、上下行关联与波束赋形。
- 核心问题：上下行需求不对称、组播/单播并存以及全双工干扰共存时，如何做高效接入与干扰管理。
- 标题承诺的方法：decoupled association + RSMA + MADRL。
- 期望效果：在回传容量与功率受限下提升 UL/DL 总和速率。
- 标题与正文的偏差：正文的真正难点不只是“关联”，而是把 RSMA、组播和波束赋形共同放进一个鲁棒 POMDP。

## Algorithm Design 快照
论文面向多 UAV 辅助蜂窝网络中的全双工上下行联合接入问题，允许用户在上行和下行分别关联不同的 UAV 或宏基站，从而利用解耦关联改善链路质量。同时，作者在下行组播与上行用户对上引入 RSMA，通过公共流和私有流的拆分缓解复杂干扰。在此基础上，论文把上下行关联、波束赋形和公共速率分配建模为带有回传约束与功率约束的鲁棒 POMDP，并利用多智能体 DRL 学习分布式控制策略，最终通过改进的 clip-and-count PPO 获得更高总速率和更快收敛。

## 图1系统框架草案
- 系统实体：宏基站、多架 UAV 基站、全双工用户、组播用户组。
- 任务/数据流：上行由用户向 UAV/MBS 发送数据，下行由多个基站协同向组播组发送公共流和私有流。
- 控制/优化变量：UL/DL 解耦关联、强弱用户配对、公共/私有流速率分配、UAV 波束赋形。
- 约束来源：UAV 发射功率、用户功率、MBS-UAV 回传容量、自干扰消除能力、组播组服务关系。
- 画图提醒：图中要明确画出“上行与下行关联对象可以不同”以及“公共流 + 私有流”的 RSMA 结构。

## System Model
- 系统由一个 MBS 和多架 UAV 组成，所有 UAV 通过容量受限回传与 MBS 相连。
- 用户在上行和下行可分别关联不同节点，形成上下行解耦接入。
- 下行采用面向多组组播的 RSMA，上行采用强弱用户配对后的速率分裂接入。
- 全双工传输引入 BS 侧和用户侧自干扰，链路速率同时受跨链路干扰和回传约束影响。

## Algorithm Design 详解
- 第一步把 UL/DL 关联、组播选择、波束赋形与公共速率分配写成非凸联合优化问题。
- 第二步由于单个 UAV 无法完整观测全局奖励，将问题重写为鲁棒 POMDP。
- 第三步使用 MADRL 做集中训练、分布执行，让每架 UAV 基于局部观测学习策略。
- 第四步设计 clip-and-count PPO，通过内在奖励和改进裁剪机制提升探索效率与训练稳定性。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成蜂窝网络场景
- 平台与软件：`Python 3.6`；`PyTorch`
- 硬件与算力：`NVIDIA GTX 2080 GPU`
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：平台和训练网络结构描述较明确，但没有给出公开代码或统一数据集。

## Introduction 写作素材
- 多 UAV 蜂窝网络中的接入问题不应再默认“上下行绑定”，因为 UL 与 DL 的最优服务节点往往不同。
- 当组播、全双工和多 UAV 并存时，传统线性预编码和耦合关联会明显损失频谱效率。
- 这篇论文适合支撑“接入机制本身也是 UAV 通信系统设计变量”的引言推进。

## Related Work 写作素材
- 与耦合关联工作相比，本文突出上下行解耦关联的系统收益。
- 与只做 NOMA/SDMA 的多 UAV 通信论文相比，本文使用 RSMA 处理复杂干扰。
- 与单智能体 DRL 不同，本文强调分布式多智能体学习与部分可观测决策。

## 相关系统建模页
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[解耦关联]]
- [[速率分裂多址（RSMA）]]
- [[多智能体强化学习]]
- [[空中通信与协同传输]]

## 来源
- [原文](../raw/markdown/ji2024DecoupledAssociationRate.md)
