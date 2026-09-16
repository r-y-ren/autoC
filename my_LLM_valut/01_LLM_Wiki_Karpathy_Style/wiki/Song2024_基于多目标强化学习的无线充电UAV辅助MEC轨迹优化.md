---
tags: [论文, 轨迹优化, 无线充电, MEC, 多目标强化学习]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/song2024EnergyefficientTrajectoryOptimization.md
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
  - Python-based simulator
frameworks:
  - PyTorch 1.7
  - MOMDP
  - MORL-TER
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Song2024 基于多目标强化学习的无线充电UAV辅助MEC轨迹优化

## 单行摘要
论文在 HAP 激光补能的 UAV-assisted MEC 系统中，把“能效最大化”和“任务采集数量最大化”写成 MOMDP，并用 MORL-TER 学习可适配不同偏好的轨迹策略。

## 题目驱动研究框架
- 研究场景：HAP 为 UAV 提供激光补能、UAV 为地面智能设备采集任务并执行计算的 MEC 场景。
- 研究对象：HAP、单架 UAV、地面智能设备 GSD、任务队列与补能链路。
- 核心问题：不同任务偏好下，如何在能效和采集任务总数之间做动态可调的轨迹决策。
- 标题承诺的方法：energy-efficient trajectory optimization with wireless charging based on MORL。
- 期望效果：相比单目标 RL，更稳地覆盖整个偏好空间，并在动态偏好下保持适应性。
- 标题与正文的偏差：正文的核心不是简单“多目标 RL”，而是通过 TER 改善 sample efficiency，并用一套参数化策略统一表示多偏好解。

## Algorithm Design 快照
论文研究带无线充电的 UAV-assisted MEC 轨迹优化问题。UAV 一边接收 HAP 激光供能，一边飞行采集地面设备的计算任务并在机载侧处理。系统同时追求更高能效和更多任务采集量，这两个目标天然冲突。为此，作者先建立带向量奖励的 MOMDP，再在 EMOQL 基础上设计 trace-based experience replay，形成 MORL-TER。这样，训练后的策略网络可以在给定偏好权重时快速输出对应轨迹，无需为每种偏好单独重训。

## 图1系统框架草案
- 系统实体：HAP、UAV、多个 GSD、任务队列、激光补能链路。
- 任务/数据流：GSD 产生任务；UAV 飞行靠近并收集任务；HAP 通过激光给 UAV 持续供能。
- 控制/优化变量：UAV 轨迹、每时隙动作、任务采集策略、偏好权重。
- 约束来源：机载存储上限、机载计算能力、飞行能耗、激光补能、任务随机到达。
- 画图提醒：图里要明确显示“任务流”和“能量流”两条并行链路，以及权重变化触发的轨迹差异。

## System Model
- 系统由一个高空平台 HAP、一架 UAV 和多个 GSD 构成。
- GSD 任务到达服从随机过程，UAV 维护机载计算队列并按有限算力执行任务。
- HAP 通过激光束为 UAV 提供能量，形成持续飞行与持续计算的补能基础。
- 目标是同时最大化 UAV 能效与总采集任务数，因此是典型双目标优化问题。

## Algorithm Design 详解
- 问题建模：把状态、偏好和向量奖励统一写入 MOMDP。
- 策略学习：在 EMOQL 框架上引入 TER，缓解经验回放偏差并提高训练效率。
- 决策输出：训练完成后，系统可按给定偏好权重直接得到对应轨迹策略。
- 结果解释：在偏好偏向能效时，UAV 更倾向稀疏区域与更少任务；偏向任务数时则更积极进入高密集区域。
- 这篇论文适合作为[[无线供能移动边缘计算]]与[[多目标强化学习（MORL）]]交叉代表作。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成 UAV-assisted MEC 场景
- 平台与软件：`Python-based simulator`、`PyTorch 1.7`
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文给出了 6 组测试实例、完整参数表和网络结构设置，但未公开实现代码。

## Introduction 写作素材
- 对 UAV-assisted MEC 而言，任务采集量更大不必然等于系统更优，因为机载处理和飞行能耗会同步上升。
- 当用户偏好随时间变化时，为每个偏好单独训练一套策略的代价过高，多目标学习更自然。
- 这篇论文适合支撑“供能过程已经不再是背景条件，而是轨迹设计的一等公民变量”的写作判断。

## Related Work 写作素材
- 与单目标 DRL 轨迹工作相比，本文显式保留能效和任务量的冲突关系，而不是线性标量化后强行合并。
- 与传统无线供能研究相比，本文把 HAP 激光补能与 UAV 机载计算队列写入同一控制模型。
- 与多目标进化算法相比，本文强调动态偏好适配和在线策略表达能力。

## 相关系统建模页
- [[无人机能耗模型]]
- [[任务队列与时延保障模型]]

## 相关概念与主题页
- [[无线供能移动边缘计算]]
- [[多目标强化学习（MORL）]]
- [[高空平台（HAP）]]
- [[轨迹优化与协同控制]]
- [[任务卸载与资源分配研究主线]]

## 来源
- [原文](../raw/markdown/song2024EnergyefficientTrajectoryOptimization.md)
