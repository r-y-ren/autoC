---
tags: [论文, 蜂窝连接无人机通信, 干扰管理, 在线优化, 轨迹规划]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/zhan2024InterferenceawareOnlineOptimization.md
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
platforms:
  - MATLAB R2022a
  - CVX
frameworks:
  - SCA
  - exact penalty method
datasets: []
hardware_stack:
  - Intel Core i5-6700
  - 16 GB RAM
artifact_availability: unknown
reproducibility_level: medium
---

# Zhan2024 能量约束蜂窝连接多UAV的干扰感知在线优化

## 单行摘要
论文在蜂窝连接多 UAV 网络中联合优化传输调度、功率控制与三维轨迹，以在未知未来信道条件下最大化最小上行吞吐并满足能量约束。

## 题目驱动研究框架
- 研究场景：蜂窝连接的多 UAV 上行通信网络。
- 研究对象：多架 UAV、多个地面基站 BS、建筑遮挡、方向性天线与能量受限飞行。
- 核心问题：在 UAV 对非关联 BS 造成强干扰的情况下，如何在线设计功率、调度和 3D 路径。
- 标题承诺的方法：interference-aware online optimization。
- 期望效果：在缺乏未来 CSI 的条件下提高所有 UAV 的最小吞吐量并保持能量可行。
- 标题与正文的偏差：正文其实提出了两套在线方案，一套使用 CDI 进行前瞻优化，一套完全不依赖 CDI 并加入能量触发惩罚项。

## Algorithm Design 快照
论文研究蜂窝连接多 UAV 上行通信中的在线联合设计问题，目标是在建筑遮挡和方向性天线共同作用下，协调多 UAV 的传输调度、功率控制和三维轨迹，使所有 UAV 的最小吞吐量最大化。难点在于 UAV 与多个 BS 之间存在强 LoS 干扰，且飞行过程中未来信道条件通常未知。为此，作者首先设计结合瞬时 CSI 与统计 CDI 的在线优化方法；随后又提出仅依赖当前 CSI 的低复杂度方案，并通过能量触发惩罚项保证 UAV 留有足够能量飞抵终点。两个方案都通过精确罚函数、交替优化和逐次凸近似求解。

## 图1系统框架草案
- 系统实体：两架蜂窝连接 UAV、多个 BS、城市建筑、方向性天线。
- 任务/数据流：UAV 在飞行过程中把数据上行到不同 BS，调度与功率控制随时隙变化。
- 控制/优化变量：BS 关联调度、发射功率、三维位置与飞行时间。
- 约束来源：能量预算、终点到达要求、建筑遮挡、天线方向图、共信道干扰。
- 画图提醒：图中应同时表现 2D/3D 轨迹和“靠近 BS 不一定最优”的建筑阻挡影响。

## System Model
- 网络中多架 UAV 通过蜂窝上行与多个 BS 通信，所有 UAV 共享频谱并造成互扰。
- 空地信道受建筑遮挡、天线方向图和小尺度衰落共同影响，因此几何距离不是唯一决定因素。
- UAV 具有固定时间终点约束与总能量预算，必须在吞吐与飞行耗能之间权衡。
- 目标函数采用 max-min 吞吐量，强调公平而不是总吞吐最大。

## Algorithm Design 详解
- 在线设计 with CDI：利用当前瞬时 CSI 与未来时隙的统计 CDI 做滚动优化。
- 在线设计 without CDI：只基于当前时隙 CSI，加入能量触发罚项，降低复杂度并保证剩余航程可行。
- 求解上把问题拆为功率与辅助变量、3D 轨迹、调度三类子问题，再分别用 SCA、线性规划和精确罚函数处理。
- 论文特别有价值的一点是证明了“轨迹本身就是干扰管理工具”，而不仅是覆盖或接入优化工具。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成城市子区域；建筑分布来自 `ITU statistical model` 的一个 realization
- 平台与软件：`MATLAB R2022a`、`CVX`
- 硬件与算力：`Intel Core i5-6700`、`16 GB RAM`
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文明确报告了在线求解运行时间，说明方案具有一定工程可行性，但仍属仿真层验证。

## Introduction 写作素材
- UAV 引入蜂窝网络后，LoS 优势和强上行干扰是同时出现的两面性。
- 在线设计不应默认能获得未来 CSI，因此仅依赖当前信息的低复杂度方案很有研究价值。
- 这篇论文可用于支撑“多 UAV 通信优化正在从覆盖最优转向干扰感知与公平吞吐”的写法。

## Related Work 写作素材
- 与离线轨迹设计相比，本文强调飞行过程中的滚动在线决策。
- 与只做二维轨迹或只做功率控制的工作相比，本文联合处理三维路径、调度和功率。
- 与忽略互扰的多 UAV 网络工作相比，本文把共信道干扰作为核心建模对象。

## 相关系统建模页
- [[信道与通信速率模型]]
- [[无人机能耗模型]]

## 相关概念与主题页
- [[蜂窝连接无人机通信]]
- [[空中通信与协同传输]]
- [[轨迹优化与协同控制]]
- [[UAC研究路线图]]

## 来源
- [原文](../raw/markdown/zhan2024InterferenceawareOnlineOptimization.md)
