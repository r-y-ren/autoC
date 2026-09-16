---
tags: [论文, 移动群智感知（MCS）, RIS辅助通信, Transformer, 深度强化学习]
created: 2026-04-10
updated: 2026-04-10
sources:
  - ../raw/markdown/wu2025ReconfigurableIntelligentSurface.md
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
  - trace_driven
data_origin:
  - synthetic
  - public_dataset
platforms:
  - Python 3.7
frameworks:
  - PyTorch 1.7.0
  - TRAIL
  - Transformer
  - PER-DDQN
datasets:
  - KAIST
hardware_stack:
  - Intel Core i9-13900K processor
artifact_availability: unknown
reproducibility_level: medium
---

# Wu2025_TRAIL面向UAV群智感知的RIS辅助Transformer强化学习

## 单行摘要
论文针对 RIS 辅助 UAV-MCS 场景，提出 `TRAIL`，用 Transformer 提取 UAV 轨迹历史依赖，再与 `PER-DDQN` 结合联合优化 UAV 轨迹和 RIS 相位，以提升吞吐并降低能耗。

## 题目驱动研究框架
- 研究场景：城市或遮挡环境下的 UAV-assisted mobile crowd sensing。
- 研究对象：多个 UAV、一个 RIS、大量 PoI。
- 核心问题：NLoS 场景中，单纯优化 UAV 水平轨迹难以同时保证通信质量和能耗。
- 标题承诺的方法：Transformer enhanced DRL with RIS assistance。
- 期望效果：通过时间依赖建模和相位控制，提升吞吐并压低 UAV 能耗。

## Algorithm Design 快照
作者把问题写成 MDP，但没有停留在普通 DDQN 上，而是先用 Transformer 从轨迹状态序列里提取长期依赖特征，再把这些特征输入 `PER-DDQN` 进行决策。这样，RIS 相位和 UAV 三维轨迹不只是瞬时最优，而会显式利用历史状态序列，有助于在复杂 NLoS 环境中做更稳定的联合控制。

## 图1系统框架草案
- 实体：多 UAV、固定 RIS、地面 PoI。
- 决策：UAV 三维轨迹、RIS 离散相位。
- 指标：吞吐、能耗。
- 画图提醒：RIS 放在建筑外立面、PoI 分布在地面，这样更容易突出 NLoS 场景。

## System Model
- 场景是多 UAV 下行通信增强的 MCS 系统，RIS 部署在建筑表面用于改善 NLoS 条件。
- UAV 在三维空间内运动，PoI 在地面分布并可能呈现移动性变化。
- 信道采用 Rician 模型，并显式考虑 RIS 离散相位量化。
- 目标是联合优化吞吐与 UAV 能耗，而 არა只追求单一速率最大化。

## Algorithm Design 详解
- 第一步：建立 RIS-assisted UAV-MCS 的 MDP，状态包含 UAV 历史轨迹与环境状态。
- 第二步：用 Transformer 对状态序列做编码，捕捉长时依赖。
- 第三步：利用 `PER-DDQN` 学习 UAV 轨迹和 RIS 相位的联合动作策略。
- 第四步：在不同环境密度、不同 RIS 元件数量和 PoI 移动性下验证算法表现。

## 实验证据卡片
- 验证类型：`simulation` + `trace_driven`
- 数据来源：合成环境 + `KAIST` 移动轨迹数据
- 平台与软件：`Python 3.7`
- 方法组件：`PyTorch 1.7.0`、`TRAIL`、`Transformer`、`PER-DDQN`
- 硬件与算力：`Intel Core i9-13900K`
- 开源情况：未说明
- 复现判断：`medium`
- 缺失信息：未公开统一训练代码与完整环境配置

## Introduction 写作素材
- RIS 把传播环境控制带进 UAV-MCS，但传统 DRL 往往忽略轨迹历史依赖。
- 群智感知场景下，吞吐与能耗的折中会被 NLoS 条件和 PoI 密度共同重塑。
- 因此这篇论文适合支持“Transformer 正在进入 UAV 轨迹决策”的判断。

## Related Work 写作素材
- 与只做 UAV-RIS 通信优化的工作相比，本文明确放在 MCS 场景。
- 与普通 DDQN 不同，本文用 Transformer 显式编码历史轨迹依赖。

## 相关系统建模页
- [[信道与通信速率模型]]
- [[无人机能耗模型]]

## 相关概念与主题页
- [[移动群智感知（MCS）]]
- [[UAV-RIS协同通信]]
- [[无人机辅助群智感知与持续作业]]

## 来源
- [原文](../raw/markdown/wu2025ReconfigurableIntelligentSurface.md)
