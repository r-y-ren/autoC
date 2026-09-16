---
tags: [论文, 安全, 主动窃听, 轨迹优化, 协同干扰]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/guo2024JointOptimizationTrajectory.md
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
  - TensorFlow
  - CVX
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Guo2024 多 UAV 辅助主动窃听的轨迹与干扰功率联合优化

## 单行摘要
论文研究多 UAV 合法监视场景中的主动窃听问题，以两阶段方式联合优化干扰功率与飞行轨迹。

## 题目驱动研究框架
- 研究场景：合法监视方需要借助多架 UAV 监听多个可疑通信链路。
- 研究对象：可疑发射 UAV、其固定接收端、合法窃听 UAV 与协同干扰 UAV。
- 核心问题：如何同时配置协同干扰功率和 UAV 飞行轨迹，以提升窃听成功率并满足飞行安全。
- 标题承诺的方法：joint optimization of trajectory and jamming power for proactive eavesdropping。
- 期望效果：在动态场景下持续压制可疑链路并增强窃听链路。
- 标题与正文的偏差：标题像直接联合优化，但正文实际采用“解析功率求解 + RL 轨迹优化”的两阶段解耦结构。

## Algorithm Design 快照
论文研究多 UAV 辅助合法监视场景，其中协同 UAV 通过发射干扰压制可疑链路，而窃听 UAV 通过飞行机动增强监听信道。作者把这一时序决策问题建模为 MDP，但指出在 RL 中直接学习满足监视约束的干扰功率较困难，因此采用两阶段思路：先在每个状态下用非学习方法求得最优干扰功率，再用强化学习只优化移动动作策略。该解耦既降低了学习难度，也保留了整体最优性分析。

## 图1系统框架草案
- 系统实体：多条可疑 UAV 通信链路、合法窃听 UAV、协同干扰 UAV。
- 任务/数据流：可疑源持续发射信息；合法侧通过干扰降低可疑链路容量，同时移动窃听 UAV 提升监听质量。
- 控制/优化变量：干扰功率分配、窃听 UAV 的轨迹动作、编队安全距离。
- 约束来源：窃听成功约束、飞行安全、动态链路状态。
- 画图提醒：建议把“干扰作用于可疑链路”和“轨迹作用于监听链路”画成两条不同颜色的因果箭头。

## System Model
- 系统由合法监视方与可疑通信方两侧组成，目标不是保密通信而是提升监视能力。
- 协同 UAV 通过 jamming 降低可疑链路容量，窃听 UAV 则通过轨迹机动提升监听链路。
- 动态环境使问题具有明显的时序决策特征，因此自然适合 MDP 建模。
- 相比传统物理层安全模型，这里“安全”站在合法监视者而非合法通信者一侧。

## Algorithm Design 详解
- 第一步是将多 UAV 辅助监视问题建模为序贯决策问题。
- 第二步是在每个状态下求解非学习式最优干扰功率分配。
- 第三步是在固定功率最优响应的前提下，用 RL 只学习飞行轨迹动作。
- 第四步是证明这种解耦不会破坏整体最优性。
- 第五步是通过数值实验展示相对基线的监视性能提升。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成场景或参数仿真
- 平台与软件：`TensorFlow`；`CVX`
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文给出 TensorFlow/CVX 线索并以仿真为主，适合作为主动窃听与协同干扰方向的机制设计参考。

## Introduction 写作素材
- 物理层安全并不只包含防窃听，也包括合法监视场景下如何更有效地监听可疑链路。
- 一旦引入多 UAV 协同，干扰控制和轨迹控制就形成强耦合。
- 这篇论文适合支撑“安全研究也可以从监视视角切入”的引言扩展。

## Related Work 写作素材
- 与被动监听方案相比，本文引入 proactive eavesdropping 和协同干扰。
- 与单 UAV 监视工作相比，本文处理多链路和多 UAV 协同。
- 与端到端 RL 联合学习相比，本文先解析求功率再学习轨迹。

## 相关系统建模页
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[主动窃听]]
- [[安全与服务保障]]
- [[轨迹优化与协同控制]]

## 来源
- [原文](../raw/markdown/guo2024JointOptimizationTrajectory.md)
