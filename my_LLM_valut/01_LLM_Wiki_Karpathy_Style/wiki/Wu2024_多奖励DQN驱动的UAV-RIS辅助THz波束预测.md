---
tags: [论文, THz通信, UAV-RIS, 波束预测, DQN]
created: 2026-04-09
updated: 2026-04-09
sources:
  - ../raw/markdown/wu2024BeamformingPredictionBased.md
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
  - public_dataset
platforms: []
frameworks:
  - MRDDQN
  - Adam
  - OFDM THz model
hardware_stack: []
datasets:
  - DeepMIMO O1-drone
artifact_availability: unknown
reproducibility_level: medium
---

# Wu2024_多奖励DQN驱动的UAV-RIS辅助THz波束预测

## 单行摘要
论文在 `UAV-RIS-assisted THz` 系统中把反射波束选择写成预测问题，通过 `MRDDQN` 结合 `DeepMIMO O1-drone` 数据生成的信道样本学习最优反射码字，以降低波束训练开销并提升速率与功率预算表现。

## 题目驱动研究框架
- 研究场景：`THz OFDM` 通信中的 `UAV-RIS` 反射增强系统。
- 研究对象：地面基站、挂载飞行 RIS 的 UAV、多用户接收端。
- 核心问题：THz 宽带系统中码本搜索和波束训练成本高，难以快速找到优反射波束。
- 标题承诺的方法：基于多奖励 DQN 做 beamforming prediction。
- 期望效果：利用采样信道直接预测高质量 RIS 反射码字。

## Algorithm Design 快照
这篇论文将反射波束问题重新表述为“离散码本动作选择”，并给出 `double-reward DDQN` 设计。它不是直接优化连续相位，而是用少量激活 RIS 单元的采样信道构造环境状态，再让模型根据 achievable rate 与 RIS 功率预算两类奖励学习最优码字，因此更适合低开销在线预测。

## 图1系统框架草案
- 信道层：基站通过 THz-OFDM 向用户传输，部分链路由 UAV 挂载 RIS 反射。
- 数据层：基于 `DeepMIMO O1-drone` 生成宽带信道样本。
- 状态层：由采样到的 RIS 通道签名构造状态。
- 学习层：`MRDDQN` 预测最佳 RIS 反射码字。
- 目标层：在满足 RIS 功率预算下最大化接收速率。

## System Model
### 1. THz UAV-RIS 宽带模型
- 系统采用 `OFDM` 架构，多子载波下存在明显的宽带波束效应。
- UAV 挂载 RIS 位于固定高度，辅助被遮挡用户建立反射链路。

### 2. 码本式 RIS 控制
- RIS 相位从预定义码本中选择，而不是连续求解。
- 波束选择目标受最大可达速率和 RIS 激活功率约束共同影响。

### 3. 数据驱动状态表示
- 通过少量激活 RIS 单元采样出多径签名。
- 将 sampled channel 向量输入神经网络做动作决策。

## Algorithm Design 详解
### 1. MRDDQN 设计
- 用双奖励同时刻画 achievable rate 与 RIS 功率预算表现。
- 通过 replay buffer 与 double-Q learning 稳定训练。

### 2. 数据集与训练流程
- 用 `DeepMIMO O1-drone` 生成 30000 个样本。
- 80% 训练、20% 测试，并用 `Adam` 优化网络参数。

### 3. 研究意义
- 论文表明在 `THz + RIS` 场景下，波束问题可从“逐次搜索”转向“数据驱动预测”，这是很值得跟进的工程化方向。

## 实验证据卡片
- 验证类型：`simulation`
- 数据来源：`DeepMIMO O1-drone`
- 平台与软件：未明确说明
- 方法组件：`MRDDQN`、`Adam`、`OFDM THz model`
- 评测指标：可达速率、RIS 功率预算、波束预测质量
- 对比对象：穷举训练与传统波束训练流程
- 开源情况：未说明
- 复现判断：`medium`
- 缺失信息：未披露具体硬件和完整代码实现

## Introduction 写作素材
- THz 场景下，波束训练和波束分裂问题会显著放大控制开销。
- UAV-RIS 引入机动性后，波束配置不能再只依赖慢速穷举。
- 这篇论文很适合支撑“RIS 控制正从解析优化转向数据驱动预测”的论述。

## Related Work 写作素材
- 既有 RIS 工作多关注连续相位优化。
- 既有 THz 工作关注宽带信道建模，但较少直接把采样信道映射到码字预测。
- 本文的代表性在于把 `DeepMIMO + DDQN` 结合到 UAV-RIS 波束控制中。

## 相关系统建模页
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[波束预测]]
- [[RIS辅助通信]]
- [[THz辅助空天地一体网络]]
- [[空中通信与协同传输]]
- [[信道与通信速率模型]]

## 来源
- [原文](../raw/markdown/wu2024BeamformingPredictionBased.md)
