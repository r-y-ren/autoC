---
tags: [论文, QoE, UAV辅助MEC, Lyapunov优化, 在线优化]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/he2024OnlineJointOptimization.md
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
  - CVX
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# He2024 UAV 辅助 MEC 服务质量体验最大化的在线联合优化

## 单行摘要
论文通过 Lyapunov 在线优化将未来依赖的联合卸载、资源分配与轨迹规划转化为逐时隙决策，以最大化 UAV-MEC 中的 QoE。

## 题目驱动研究框架
- 研究场景：单 UAV 作为空中边缘服务器，为多个地面用户提供计算服务。
- 研究对象：UD、UAV、任务卸载决策、资源分配与飞行轨迹。
- 核心问题：在 UAV 能量受限且用户需求时变时，如何最大化长期 QoE。
- 标题承诺的方法：an online joint optimization approach for QoE maximization。
- 期望效果：在不依赖未来信息的前提下获得更优的长期用户体验。
- 标题与正文的偏差：正文真正的亮点是 Lyapunov 框架下“两阶段 game theory + convex optimization”的逐时隙求解结构。

## Algorithm Design 快照
论文把 UAV-enabled MEC 中的联合任务卸载、资源分配和轨迹规划问题表述为 QoE 最大化问题。由于原问题未来依赖且 NP-hard，作者先利用 Lyapunov 优化把长期问题转化为逐时隙实时优化，再通过两阶段方法求解：第一阶段用博弈思想处理参与方决策，第二阶段用凸优化细化资源与轨迹子问题。这样既保留了在线性，又显式引入了用户体验指标。

## 图1系统框架草案
- 系统实体：单 UAV、多个用户设备、无线接入与边缘计算资源。
- 任务/数据流：用户任务在本地或经无线链路卸载到 UAV，由 UAV 处理并回传结果。
- 控制/优化变量：卸载决策、CPU 资源、带宽/功率资源、UAV 轨迹。
- 约束来源：UAV 能量预算、用户体验需求、任务时变性和未来不可见。
- 画图提醒：图里要把“长期 QoE 目标 -> Lyapunov 逐时隙 PROP -> 两阶段求解”画成方法主线。

## System Model
- 系统是典型的单 UAV 辅助 MEC 场景，但优化目标从时延/能耗推进到 QoE。
- 论文显式考虑 UAV 能量约束，因此轨迹和计算分配不能脱离续航独立设计。
- 因为用户需求随时间变化，问题必须按在线控制方式处理。
- QoE 作为目标函数意味着系统需要对用户感知而非平均效率负责。

## Algorithm Design 详解
- 第一步把联合卸载、资源分配和轨迹规划表述为未来依赖的 JTRTOP。
- 第二步使用 Lyapunov 优化把长期问题转化为逐时隙 PROP。
- 第三步通过 game theory 与 convex optimization 的两阶段方法求解实时子问题。
- 第四步与基线方案对比，展示 QoE 与系统性能优势。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成场景或参数仿真
- 平台与软件：`CVX`
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文适合充当“QoE + 在线优化 + 轨迹/资源联合设计”的参考模板。

## Introduction 写作素材
- UAV-MEC 系统如果只优化平均时延，未必能真正提升用户体验。
- 在未来需求不可见的动态环境里，QoE 目标更能揭示在线决策的实际价值。
- 这篇论文适合支撑“从性能指标走向体验指标”的方法论转向。

## Related Work 写作素材
- 与只关注时延或能耗的工作相比，本文显式以 QoE 为长期优化目标。
- 与离线最优方法不同，本文强调未来不可见场景下的在线求解。
- 与纯 DRL 方法相比，本文保留了 Lyapunov + 凸优化的结构化求解骨架。

## 相关系统建模页
- [[计算卸载模型]]
- [[任务队列与时延保障模型]]
- [[无人机能耗模型]]

## 相关概念与主题页
- [[服务质量体验（QoE）]]
- [[Lyapunov优化]]
- [[任务卸载与资源分配研究主线]]
- [[安全与服务保障]]

## 来源
- [原文](../raw/markdown/he2024OnlineJointOptimization.md)
