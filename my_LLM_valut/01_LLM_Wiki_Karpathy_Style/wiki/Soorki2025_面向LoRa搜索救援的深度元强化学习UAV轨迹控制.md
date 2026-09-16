---
tags: [论文, LoRa, 搜索救援, 深度元强化学习, UAV轨迹]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/soorki2025CatchMeIf.md
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
  - prototype
  - field_test
data_origin:
  - mixed
platforms: []
frameworks:
  - deep reinforcement learning
  - deep meta-RL
  - Actor-Critic
  - POMDP
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Soorki2025 面向LoRa搜索救援的深度元强化学习UAV轨迹控制

## 单行摘要
论文在 UAV-assisted LoRa 搜索救援系统中将飞行网关控制建模为 POMDP，并用 deep meta-RL 让 UAV 快速适应未知山地搜索环境。

## 题目驱动研究框架
- 研究场景：偏远山区和遮挡复杂环境中的搜索救援。
- 研究对象：携带 LoRa 发射节点的失踪者、作为飞行网关的 UAV、地面救援站。
- 核心问题：在未知环境中，如何根据 RSSI 等观测快速调整 UAV 轨迹并找到目标。
- 标题承诺的方法：deep meta-RL for search-and-rescue using LoRa UAV networks.
- 期望效果：相较于深度 RL 和 Actor-Critic，在新环境中更快收敛、更省能、更不易陷入局部最优。
- 标题与正文的偏差：正文重点并不只在“能找人”，而在“如何利用跨环境经验实现新环境快速适应”。

## Algorithm Design 快照
论文研究 UAV 作为飞行 LoRa 网关时的搜索救援轨迹控制问题。由于山地、峡谷与校园等环境的无线传播特性不同，单一环境下训练好的策略很难直接迁移。作者先在给定环境中训练深度 RL 策略，再把多个旧环境经验作为先验，通过 deep meta-RL 让 UAV 在新环境中快速适配。这样既能利用 LoRa 的远距离低功耗优势，又能缓解传统贪心搜索在非视距环境下容易卡住局部最优的问题。

## 图1系统框架草案
- 系统实体：LoRa 发射节点、UAV 飞行网关、救援站、未知搜索环境。
- 任务/数据流：失踪者节点发射 LoRa 信号；UAV 根据信号强度与历史观测调整下一步飞行方向；成功定位后把信息回传救援站。
- 控制/优化变量：UAV 每时隙的飞行方向/动作、观测历史长度、元训练适配策略。
- 约束来源：非视距遮挡、有限电池、RSSI 波动、未知环境几何。
- 画图提醒：图中要画出 campus/plain/canyon 三类环境的迁移关系，而不只是单个场景。

## System Model
- 系统被建模为部分可观测马尔可夫决策过程，观测主要来自 LoRa 链路强度与历史状态。
- UAV 在每个 SAR 时隙选择飞行动作，目标是最小化搜索时间与能耗。
- 新环境不提供先验地图，因此控制策略必须具备跨环境适应能力。
- 性能指标包括 SAR time slots、能量消耗和成功定位能力。

## Algorithm Design 详解
- Deep RL 基线：先在单一环境中学习基本飞行网关控制策略。
- Deep meta-RL：将过去多个环境的经验编码进元策略，再在新环境中快速微调。
- 对比对象：deep RL、Actor-Critic 与传统贪心类 LoRa 搜索策略。
- 实验意义：这篇论文把[[LoRa辅助搜救]]和[[深度元强化学习]]接入到 UAV 轨迹控制网络中，说明搜索救援是轨迹优化中的一类高不确定性问题。
- 关键结果：在峡谷场景中，meta-RL 把 SAR time slots 从 `141` 降到 `50`，能耗分别比 deep RL 和 Actor-Critic 低 `57%` 与 `23%`。

## 实验证据卡片
- 验证类型：数值仿真；原型系统；真实环境测试
- 数据来源：混合来源；三类真实搜索环境实测
- 平台与软件：未说明
- 硬件与算力：未明确披露具体 UAV 与 LoRa 模块型号
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文给出 campus、plain、slotted canyon 三类真实测试环境，是当前语料里少见的 LoRa 搜救实证锚点。

## Introduction 写作素材
- 搜索救援中的 UAV 轨迹并不是普通路径最短问题，而是“在不完整无线感知下持续试探”的决策问题。
- 山地和峡谷环境下，贪心式 LoRa 搜索容易陷入局部最优，因此需要能迁移的学习策略。
- 这篇论文可支撑“跨环境快速适应能力正在成为 UAV 智能救援控制的新要求”的引言判断。

## Related Work 写作素材
- 与基于 RSSI 的贪心搜索相比，本文强调跨环境学习与局部最优规避。
- 与只在已知环境中训练的 DRL 方案相比，本文引入 meta-RL 处理新环境适应。
- 与纯仿真 SAR 研究相比，本文具备三类真实场景测试证据。

## 相关系统建模页
- [[信道与通信速率模型]]
- [[无人机能耗模型]]

## 相关概念与主题页
- [[LoRa辅助搜救]]
- [[深度元强化学习]]
- [[轨迹优化与协同控制]]
- [[无人机辅助群智感知与持续作业]]
- [[UAC研究路线图]]

## 来源
- [原文](../raw/markdown/soorki2025CatchMeIf.md)
