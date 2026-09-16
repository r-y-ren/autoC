---
tags: [论文, UAV-RIS, GNN, SD3, 轨迹优化, 波束赋形]
created: 2026-04-09
updated: 2026-04-09
sources:
  - ../raw/markdown/wang2025JointOptimizationBeamforming.md
venue_tier: CCF-A
literature_type: method
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - methodology
  - engineering_context
validation_type:
  - simulation
data_origin:
  - synthetic
platforms:
  - PyTorch
  - Windows 11
frameworks:
  - GNN
  - SD3
  - Adam
hardware_stack:
  - Intel Core i7-12700F CPU 2.10GHz
datasets: []
artifact_availability: unknown
reproducibility_level: medium
---

# Wang2025_GNN与SD3驱动的UAV-RIS联合波束与轨迹优化

## 单行摘要
论文面向城市遮挡环境下的 `UAV-mounted RIS` 多用户下行系统，将基站主动波束、RIS 被动波束和 UAV 三维轨迹统一到多目标优化框架中，并用 `GNN + SD3` 分别求解波束与轨迹子问题。

## 题目驱动研究框架
- 研究场景：城市建筑遮挡下的 `MU-MISO` 下行通信。
- 研究对象：基站、挂载 RIS 的 UAV、多用户终端。
- 核心问题：遮挡环境中链路可达性、系统速率、UAV 能耗和飞行时长相互耦合。
- 标题承诺的方法：联合优化 beamforming 和 trajectory。
- 期望效果：提升系统速率，同时降低 UAV 能耗和飞行完成时长。

## Algorithm Design 快照
这篇论文把 `RIS` 和 `UAV` 的组合从“传播增强组件”推进成“可机动的反射平台”。作者因此把问题拆成两层：一层是 `BS active beamforming + RIS passive beamforming`，由 `GNN` 捕捉多用户和多节点之间的关系结构；另一层是 UAV 三维轨迹，由 `SD3` 在连续动作空间中学习。核心价值在于结构化地分而治之，而不是把所有变量一次性交给黑盒强化学习。

## 图1系统框架草案
- 环境层：建筑遮挡导致 BS-UE 直链受阻。
- 空中反射层：RIS 挂载于 UAV 并在空中机动。
- 波束层：基站主动波束和 RIS 被动相位协同。
- 控制层：`GNN` 优化波束，`SD3` 优化 UAV 三维轨迹。
- 目标层：兼顾系统速率、能耗和飞行时长。

## System Model
### 1. 城市 UAV-RIS 通信模型
- 基站向多用户下行传输，RIS 由 UAV 携带并在空中移动。
- 建筑物统计模型决定链路遮挡与空间可达性。

### 2. 多目标优化目标
- 最大化系统速率。
- 最小化 UAV 能量消耗与完成飞行所需时隙数。

### 3. 变量拆分
- 波束变量：主动波束与 RIS 被动相位。
- 轨迹变量：UAV 位置、速度、到达终点约束等。

## Algorithm Design 详解
### 1. GNN 波束优化
- 用图结构编码多用户、基站与 RIS 之间的耦合关系。
- 以无监督方式训练 `GNN` 来联合优化主动与被动波束。

### 2. SD3 轨迹学习
- 将轨迹规划写成 `MDP`。
- 用 `SD3` 的双 actor-critic 与 softmax Q-value 提升训练稳定性，并通过 reward shaping 缓解稀疏奖励问题。

### 3. 研究意义
- 论文说明 `UAV-RIS` 系统适合采用“结构化图学习 + 连续控制 RL”的混合求解，而非纯解析或纯黑盒路线。

## 实验证据卡片
- 验证类型：`simulation`
- 数据来源：合成城市建筑阻挡场景
- 平台与软件：`PyTorch`、`Windows 11`
- 硬件与算力：`Intel Core i7-12700F CPU @ 2.10GHz`
- 方法组件：`GNN`、`SD3`、`Adam`
- 评测指标：系统速率、能效、飞行时长、轨迹质量
- 对比对象：DNN 或其他 UAV-RIS 优化基线
- 开源情况：未说明
- 复现判断：`medium`
- 缺失信息：未披露完整代码与随机种子

## Introduction 写作素材
- 城市环境下，RIS 的真正价值在于与 UAV 机动性耦合，而不只是固定反射板增强。
- 传统解析法难同时处理多用户波束与连续轨迹控制。
- 这篇论文适合支撑“UAV-RIS 需要图结构学习和连续动作强化学习共同参与”的写作判断。

## Related Work 写作素材
- 既有 RIS 优化多聚焦固定 RIS 或单一变量更新。
- 既有 UAV 轨迹学习又往往不显式利用多用户拓扑结构。
- 本文通过 `GNN + SD3` 的两层设计，把结构关系和动作控制分别发挥出来。

## 相关系统建模页
- [[信道与通信速率模型]]
- [[区域覆盖与部署模型]]

## 相关概念与主题页
- [[RIS辅助通信]]
- [[波束预测]]
- [[图神经网络（GNN）]]
- [[轨迹优化]]
- [[空中通信与协同传输]]

## 来源
- [原文](../raw/markdown/wang2025JointOptimizationBeamforming.md)
