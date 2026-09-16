---
tags: [论文, 可靠性, 任务卸载, UAV辅助边缘计算, TD3]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/hao2025ReliabilityawareOptimizationTask.md
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
  - emulation
data_origin:
  - mixed
platforms:
  - Kubernetes
frameworks: []
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Hao2025 可靠性感知的 UAV 辅助边缘计算任务卸载优化

## 单行摘要
论文把任务成功率作为核心目标，在不可靠 UAV 与无线链路条件下联合优化轨迹、卸载与功率，并用 Kubernetes 测试床补强验证。

## 题目驱动研究框架
- 研究场景：基础设施薄弱环境中的 UAV 辅助边缘计算网络。
- 研究对象：UE、多个 UAV、边缘云与事件驱动任务流。
- 核心问题：UAV 与无线链路不可靠时，如何提高任务成功率而不引入额外决策等待。
- 标题承诺的方法：reliability-aware optimization of task offloading。
- 期望效果：在动态环境下提升长期平均任务成功率。
- 标题与正文的偏差：正文真正的亮点是以 task-driven 机制替代 time-driven 策略，并用测试床验证其实用性。

## Algorithm Design 快照
论文关注“任务可能失败”这一现实问题，把 UAV 不可靠性和无线信道不可靠性共同纳入卸载优化框架。作者将问题建模为轨迹、卸载决策和传输功率联合优化，以长期平均任务成功率最大化为目标。为了处理离散-连续混合动作空间，论文设计 dependence-aware 潜空间表示，并与 TD3 结合形成 DRL 方案。与纯仿真论文不同，它还借助 Kubernetes 测试床验证策略的实际可部署性。

## 图1系统框架草案
- 系统实体：UE、多架 UAV、边缘云、任务执行队列。
- 任务/数据流：任务可本地执行、卸载到 UAV、或进一步由云协助处理。
- 控制/优化变量：卸载决策、UAV 轨迹、传输功率。
- 约束来源：UAV/链路不可靠、任务到达事件驱动、队列等待与资源有限。
- 画图提醒：图里要突出“成功率”是从任务生成到结果返回的端到端指标。

## System Model
- 系统由多 UAV 与边缘云共同支撑，决策由边缘云基于分布式信息进行协调。
- 每个 UAV 管理任务执行队列，任务失败可能来自链路传输或计算执行环节。
- 论文强调 task-driven 决策，避免 time-driven 策略引入额外等待时间。
- 目标函数不再是纯时延或纯能耗，而是长期平均任务成功率。

## Algorithm Design 详解
- 第一步把可靠性感知 cooperative offloading 问题转化为 MDP。
- 第二步构建 dependence-aware 潜空间表示，处理离散-连续混合动作。
- 第三步结合 TD3 设计 DRL 方案，联合学习卸载、功率与轨迹控制。
- 第四步通过仿真与 Kubernetes 测试床同时评估方案的性能与可用性。

## 实验证据卡片
- 验证类型：数值仿真；仿真测试床/仿真化原型
- 数据来源：合成场景与自建测试环境
- 平台与软件：`Kubernetes`
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：测试床验证让这篇论文在“可靠性感知卸载”分支里比纯仿真论文更有工程说服力。

## Introduction 写作素材
- 在 UAV 辅助边缘计算中，任务是否成功完成比平均时延更接近真实服务质量。
- 如果忽视 UAV 与链路的不可靠性，很多看似最优的卸载策略在真实系统里会失效。
- 这篇论文适合支撑“从时延最优走向任务成功率最优”的引言推进。

## Related Work 写作素材
- 与 time-driven 策略不同，本文强调 task-driven 决策以减少额外等待。
- 与只优化时延或能耗的卸载论文不同，本文以任务成功率为核心目标。
- 与纯仿真 DRL 方法相比，本文额外提供了 Kubernetes 测试床证据。

## 相关系统建模页
- [[计算卸载模型]]
- [[任务队列与时延保障模型]]
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[可靠性感知卸载]]
- [[任务卸载]]
- [[安全与服务保障]]
- [[任务卸载与资源分配研究主线]]

## 来源
- [原文](../raw/markdown/hao2025ReliabilityawareOptimizationTask.md)
