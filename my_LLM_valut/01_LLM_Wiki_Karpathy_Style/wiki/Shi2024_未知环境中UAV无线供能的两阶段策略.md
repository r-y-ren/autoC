---
tags: [论文, 无线供能, WPT, 轨迹优化, 聚类]
created: 2026-04-10
updated: 2026-04-10
sources:
  - ../raw/markdown/shi2024TwoStageStrategyUAVenabled.md
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
  - C++17
frameworks:
  - UMC
  - DGC
datasets: []
hardware_stack:
  - Intel Core i5 2.30 GHz CPU
  - 8 GB RAM
artifact_availability: unknown
reproducibility_level: medium
---

# Shi2024_未知环境中UAV无线供能的两阶段策略

## 单行摘要
论文研究未知传感节点位置下的 UAV-enabled WPT，提出“搜索 + 供能”两阶段策略：先用 `UMC` 搜索节点位置，再用 `DGC` 动态聚类与路径设计提升总收能与 UAV 能量利用效率。

## 题目驱动研究框架
- 研究场景：多个传感节点位置未知，UAV 既要先找到它们，又要完成后续无线补能。
- 研究对象：UAV、可充电传感节点及其聚类形成的供能簇。
- 核心问题：在未知目标位置条件下，搜索效率、收能总量、飞行能耗和能量利用率如何同时兼顾。
- 标题承诺的方法：a two-stage strategy。
- 期望效果：让能量受限 UAV 在不掌握先验位置信息的情况下，仍能完成高效搜索与补能。

## Algorithm Design 快照
作者没有直接把问题写成单一优化，而是按照任务流程把它拆成两个阶段。第一阶段 `UMC` 让 UAV 在未知环境中完成传感节点搜索；第二阶段 `DGC` 根据已发现节点的空间分布动态成簇，并设计补能路线与停留方案。这样，未知环境探索和补能优化被明确分层，避免了把全部不确定性同时压给一个求解器。

## 图1系统框架草案
- 实体：搜索 UAV、充电节点 CN、终端节点 EN。
- 阶段 1：环境探索与节点定位。
- 阶段 2：节点聚类、补能停留与路径规划。
- 目标：搜索效率、收能量、飞行能耗、能量利用率。

## System Model
- 系统区分搜索 UAV 与用于补能的节点簇结构，允许节点在发现后动态组织成供能集合。
- 研究重点集中在水平平面轨迹与停留，不考虑复杂三维机动。
- 补能不仅看 CN 收能，还关注簇内 EN 的后续能量分配。
- 因为目标位置未知，搜索阶段本身就是系统性能的一部分，而非外部先验输入。

## Algorithm Design 详解
- 第一步：用 `UMC` 控制 UAV 在未知区域中搜索尽可能多的节点。
- 第二步：节点被发现后，利用 `DGC` 依据空间结构形成动态簇。
- 第三步：根据聚类结果优化补能路线和停留顺序，提升总收能。
- 第四步：综合评估 UAV 自身飞行能耗与系统能量利用效率。

## 实验证据卡片
- 验证类型：`simulation`
- 数据来源：合成场景参数
- 平台与软件：`C++17`
- 方法组件：`UMC`、`DGC`
- 硬件与算力：`Intel Core i5 2.30 GHz`、`8 GB RAM`
- 开源情况：未说明
- 复现判断：`medium`
- 缺失信息：未给出完整代码与更大规模真实部署结果

## Introduction 写作素材
- 许多 WPT 论文默认节点位置已知，但真实部署中“先找到谁需要充电”本身就是代价高昂的问题。
- 当搜索和补能顺序被统一考虑后，UAV 续航约束会直接重塑补能策略。
- 这篇论文适合支持“UAV 无线供能研究正在从静态补能走向探索型补能”的判断。

## Related Work 写作素材
- 与位置已知的 WPT 论文相比，本文把目标搜索写成问题主体的一部分。
- 与单阶段路径优化相比，本文通过两阶段分解处理未知环境与供能簇组织。

## 相关系统建模页
- [[无人机能耗模型]]

## 相关概念与主题页
- [[无线供能传输（WPT）]]
- [[轨迹优化与协同控制]]
- [[无人机辅助群智感知与持续作业]]

## 来源
- [原文](../raw/markdown/shi2024TwoStageStrategyUAVenabled.md)
