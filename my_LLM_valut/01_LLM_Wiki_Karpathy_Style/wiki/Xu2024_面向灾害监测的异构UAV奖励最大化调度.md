---
tags: [论文, 灾害监测, 异构UAV, 奖励最大化, 近似算法]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/xu2024RewardMaximizationDisaster.md
venue_tier: CCF-A
literature_type: method
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - methodology
  - related_work
validation_type:
  - simulation
data_origin:
  - synthetic
platforms: []
frameworks:
  - approximation algorithm
  - orienteering
  - heterogeneous UAV scheduling
datasets: []
hardware_stack:
  - DJI Phantom 4 RTK
  - DJI Mavic 2 Enterprise Advanced
  - DJI M300 RTK
  - Parrot ANAFI Ai
  - senseFly eBee X
artifact_availability: unknown
reproducibility_level: medium
---

# Xu2024 面向灾害监测的异构UAV奖励最大化调度

## 单行摘要
论文在灾害区域 PoI 监测中研究异构 UAV 调度问题，通过常数近似算法在能量约束下最大化总监测奖励。

## 题目驱动研究框架
- 研究场景：灾害区域的多 PoI 快速监测与救援决策支持。
- 研究对象：多架异构 UAV、PoI、救援站、能量受限飞行回路。
- 核心问题：不同 UAV 的航时和监测能力不一致时，如何给每架 UAV 分配收益最大的飞行巡回。
- 标题承诺的方法：reward maximization for disaster zone monitoring with heterogeneous UAVs.
- 期望效果：在能量约束下提升总监测奖励，并优于现有启发式或 DRL 对手。
- 标题与正文的偏差：正文亮点不只是 reward，而是“监测能力与续航不成比例”的异构性被写入近似算法设计。

## Algorithm Design 快照
论文研究多架异构 UAV 在灾害区域监测 PoI 的调度问题。每架 UAV 的续航、单位距离能耗和感知能力都不同，因此高奖励 UAV 不一定有最长航时。作者把问题建模为带能量约束的异构巡回选择问题，并设计了首个常数近似算法，通过为每架 UAV 构造近似最优巡回来提升总监测奖励。实验基于多种商用 UAV 参数，验证了异构机群相比同质化建模更贴近真实应急部署。

## 图1系统框架草案
- 系统实体：救援站、多架异构 UAV、带权重 PoI。
- 任务/数据流：UAV 从救援站出发监测若干 PoI，并将图像/视频回传用于决策。
- 控制/优化变量：每架 UAV 的 PoI 子集、飞行巡回、UAV 类型分配。
- 约束来源：电池容量、单位距离能耗、监测奖励差异、返回救援站约束。
- 画图提醒：图中要突出“同一 PoI 对不同 UAV 奖励不同”“高能力 UAV 可能更重更耗能”的异构性。

## System Model
- 每个 PoI 对不同 UAV 对应不同监测奖励，奖励由设备能力和任务重要性共同决定。
- 每架 UAV 有独立能量上限和单位飞行能耗，因此可服务路径长度不同。
- 所有飞行巡回都从同一救援站出发并返回。
- 优化目标是最大化所有 UAV 总奖励，而不是简单覆盖最多 PoI。

## Algorithm Design 详解
- 问题本质：可视作异构约束下的多巡回 orienteering 变体。
- 核心难点：高奖励 UAV 可能更耗能，监测能力与续航不成正比。
- 近似算法：为每架 UAV 构造近似巡回，并证明其常数近似比；论文指出该界是紧的。
- 实验设置：使用 `DJI Phantom 4 RTK`、`DJI M300 RTK`、`senseFly eBee X` 等商用 UAV 的真实参数。
- 关键结果：与对比算法相比，总监测奖励最高提升约 `25%`。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成灾害拓扑；商用 UAV 真实参数
- 平台与软件：未说明
- 硬件与算力：评测使用多种商用 UAV 参数，但未进行实飞
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：这篇论文没有真实飞行测试，但硬件参数使用真实机型，适合做异构机群调度的系统假设参考。

## Introduction 写作素材
- 灾害监测中的关键不只是“派几架 UAV”，而是“哪种能力的 UAV 去看哪类目标更划算”。
- 异构机群会让奖励最大化问题显著不同于传统同质 UAV 覆盖问题。
- 这篇论文适合支撑“应急监测正在从 homogeneous coverage 转向 heterogeneous utility optimization”的引言判断。

## Related Work 写作素材
- 与同质 UAV 监测研究相比，本文把感知能力差异和续航差异同时纳入调度。
- 与纯覆盖最大化相比，本文用 reward 替代 binary coverage，更接近真实救援优先级。
- 与 DRL 型路径方法相比，本文提供了具理论保证的近似算法路线。

## 相关系统建模页
- [[区域覆盖与部署模型]]
- [[无人机能耗模型]]

## 相关概念与主题页
- [[异构无人机调度]]
- [[覆盖与部署优化主线]]
- [[无人机辅助群智感知与持续作业]]
- [[UAC研究路线图]]

## 来源
- [原文](../raw/markdown/xu2024RewardMaximizationDisaster.md)
