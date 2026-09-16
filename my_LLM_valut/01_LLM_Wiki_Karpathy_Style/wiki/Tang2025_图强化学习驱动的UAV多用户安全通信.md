---
tags: [论文, 物理层安全, 图神经网络, UAV安全通信]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/tang2025DeepGraphReinforcement.md
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
platforms: []
frameworks:
  - graph neural network
  - soft actor-critic
  - hierarchical learning
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Tang2025_图强化学习驱动的UAV多用户安全通信

## 单行摘要
论文把 UAV-enabled multi-user secure communications 拆成“内层 GNN 安全波束赋形 + 外层 SAC 部署学习”的双层图强化学习框架，在用户与窃听者成对存在的动态拓扑中显著提升保密速率。

## 题目驱动研究框架
- 研究场景：单 UAV 作为多用户空中基站，在存在对应窃听者的场景中提供保密通信。
- 研究对象：携带多天线的 UAV、合法用户、对应窃听者。
- 核心问题：部署位置与波束赋形跨尺度耦合，传统解析优化难以在复杂拓扑中实时适配。
- 标题承诺的方法：用 deep graph reinforcement learning 联合求解 UAV-enabled secure communications。
- 期望效果：提升系统 secrecy rate，并在复杂用户/窃听者关系下保持可扩展性。

## Algorithm Design 快照
论文把问题拆成两层：内层把安全波束赋形解释为图学习任务，用 GNN 近似复杂的非凸关系；外层用 SAC 学习 UAV 的部署位置，从而把“大尺度部署”和“小尺度传输”分开处理。这个设计的价值在于，它不是简单把 DRL 直接丢给全部变量，而是让图神经网络先吸收用户-窃听者关系，再由 DRL 决定空间部署。

## 图1系统框架草案
- 系统实体：单 UAV 空中基站、`K` 个合法用户、`K` 个对应窃听者。
- 状态关系：UAV 位置决定用户与窃听者的信道质量差异。
- 内层学习：GNN 根据用户-窃听者图关系输出安全波束赋形。
- 外层学习：SAC 根据内层反馈学习最优 UAV 部署。
- 优化目标：最大化整体 secrecy rate。

## System Model
### 1. 多用户安全下行模型
- UAV 在固定高度飞行，并通过多天线向多个合法用户发送保密消息。
- 每个合法用户对应一个窃听者，构成多用户多输入单输出安全通信模型。
- 合法链路与窃听链路都依赖 UAV 空间位置。

### 2. 跨尺度耦合
- 波束赋形属于小尺度传输层变量。
- UAV 部署属于大尺度空间变量。
- 这两类变量共同决定 secrecy rate，因此需要分层学习。

### 3. 图结构解释
- 用户、窃听者与 UAV 之间天然形成图结构依赖。
- 论文借此使用 GNN 近似传统非凸求解过程。

## Algorithm Design 详解
### 1. GNN 内层
- 内层 GNN 负责在固定 UAV 位置下求近似最优安全波束。
- 图结构让不同用户-窃听者关系可共享表达能力。

### 2. SAC 外层
- 外层 SAC 依据内层输出的安全收益反馈学习 UAV 部署位置。
- 这样 DRL 不直接碰全部高维波束变量，降低了学习难度。

### 3. 实验结论
- 在 `200m x 200m` 区域、`8` 对用户-窃听者、`8` 天线配置下，所提框架优于中心部署、几何中心、外接圆心等多种部署基线。
- GNN 使用 `5` 层 GCN，SAC 训练 `500` 轮，结果表明灵活部署对安全收益提升非常显著。
- 这篇论文很好地代表了“GNN + DRL”如何进入 UAV 物理层安全。

## 实验证据卡片
- 验证类型：`simulation`
- 数据来源：多用户-窃听者合成拓扑
- 平台与软件：原文未明确说明
- 硬件与算力：未说明
- 场景设置：`200m x 200m` 区域、`8` 对合法用户/窃听者、`8` 天线、Rician 因子 `10dB`
- 对比基线：区域中心、几何中心、外接圆心、用户多边形质心等部署策略
- 开源情况：未说明
- 复现判断：`medium`
- 缺失信息：未披露实现平台、代码与训练硬件

## Introduction 写作素材
- UAV 的可移动性为物理层安全提供了天然自由度，但也使部署与波束赋形强耦合。
- 单纯解析优化在复杂拓扑下可解释但往往不够灵活。
- 因而图学习与 DRL 结合是一条很自然的安全通信方法线。

## Related Work 写作素材
- 传统 UAV 物理层安全工作多偏解析优化或分块迭代。
- 单层 DRL 难以同时处理部署和波束赋形两类尺度差异明显的变量。
- 这篇论文将 GNN 先验显式用于安全波束赋形，是当前语料中很有代表性的结构化学习路线。

## 相关系统建模页
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[图神经网络（GNN）]]
- [[物理层安全]]
- [[安全与服务保障]]
- [[空中通信与协同传输]]

## 来源
- [原文](../raw/markdown/tang2025DeepGraphReinforcement.md)
