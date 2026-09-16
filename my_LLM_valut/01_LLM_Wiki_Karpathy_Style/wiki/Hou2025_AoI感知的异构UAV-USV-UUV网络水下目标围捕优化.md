---
tags: [论文, AoI, 异构网络, MARL, 轨迹设计]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/hou2025AgeInformationawareMultiobjective.md
venue_tier: CCF-A
literature_type: method
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - methodology
  - idea_seed
validation_type:
  - simulation
data_origin:
  - synthetic
platforms: []
frameworks: []
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Hou2025 AoI 感知的异构 UAV-USV-UUV 网络水下目标围捕优化

## 单行摘要
论文构建 UAV-USV-UUV 异构 3U 网络，将 AoI 融入水下目标围捕任务，在能耗与任务时长双目标下优化多车辆轨迹。

## 题目驱动研究框架
- 研究场景：复杂海洋环境中的水下目标搜索、跟踪与围捕。
- 研究对象：UAV、USV、UUV 群体、目标、障碍与涡流环境。
- 核心问题：在跨域异构车辆协同中，如何兼顾目标信息新鲜度、能耗和任务时长。
- 标题承诺的方法：AoI-aware multi-objective optimization for heterogeneous UAV-USV-UUV networks。
- 期望效果：提升目标检测时效并提高围捕任务成功率。
- 标题与正文的偏差：正文不仅关注 AoI，还强调复杂流体环境、连接约束和多车辆动力学。

## Algorithm Design 快照
论文提出异构 3U 网络，将 UAV 的广域搜索能力、USV 的中继能力和 UUV 群体的水下围捕能力结合起来。为了提升目标检测的时效性，作者把 AoI 引入 UAV 搜索策略，并在能耗、任务时长、连接约束与安全约束下构建多目标优化问题。求解上，论文设计 AE-MVTD3，通过 AoI 与能量联合奖励引导多车辆协作控制。

## 图1系统框架草案
- 系统实体：UAV、USV、多个 UUV、海洋障碍、涡流场、目标。
- 任务/数据流：UAV 搜索目标并把信息经 USV 中继给 UUV 群。
- 控制/优化变量：三类车辆的轨迹、协同围捕动作、通信连通策略。
- 约束来源：动力学、障碍、涡流、通信连接、安全距离、任务时长。
- 画图提醒：图里要突出“UAV 搜索 - USV 中继 - UUV 围捕”的跨域协作链。

## System Model
- UAV 负责快速搜索与跟踪，USV 承担空海通信中继，UUV 群完成围捕执行。
- AoI 用于衡量目标状态信息的新鲜度，因此搜索效率不仅是时间长短，还取决于信息更新频率。
- 系统目标是多目标的，同时关注总能耗和任务时长，并受复杂环境约束。
- 这类异构网络说明 UAV 研究正在走向跨域多平台联合任务系统。

## Algorithm Design 详解
- 第一步构建包含动力学、障碍、涡流和连接约束的 3U 网络模型。
- 第二步将 AoI 融入 UAV 搜索奖励，并与能量/时长目标联合建模。
- 第三步设计 AE-MVTD3 进行多车辆控制策略学习。
- 第四步在多种复杂场景下比较任务成功率、AoI 与能耗表现。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成环境与参数设定
- 平台与软件：未说明
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：虽然场景跨到海空水多域，但这篇论文对 AoI 感知协同控制非常有启发。

## Introduction 写作素材
- 跨域异构任务系统正在把 UAV 从单域平台推进成多平台协作链的一环。
- AoI 提醒我们，信息多快到达并不是唯一问题，信息有多新同样关键。
- 这篇论文适合支撑“UAV 协同研究已扩展到更复杂的跨域系统任务”这一判断。

## Related Work 写作素材
- 与传统 UUV 单域围捕不同，本文引入 UAV 与 USV 形成异构 3U 网络。
- 与只做路径规划的工作不同，本文同时把 AoI、能耗和任务时长纳入目标。
- 与单车或同质多车 RL 不同，本文处理跨域异构车辆协作。

## 相关系统建模页
- [[任务队列与时延保障模型]]
- [[无人机能耗模型]]

## 相关概念与主题页
- [[信息年龄（AoI）]]
- [[多无人机协同]]
- [[轨迹优化与协同控制]]

## 来源
- [原文](../raw/markdown/hou2025AgeInformationawareMultiobjective.md)
