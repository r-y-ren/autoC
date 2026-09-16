---
tags: [论文, 数据采集, 多目标优化, 多UAV, 时间能量权衡]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/jia2024EnergyTimeTradeoff.md
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
frameworks: []
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---


# Jia2024 多UAV物联网数据采集的时间能量权衡优化

## 单行摘要
论文把多 UAV 数据采集中的任务完成时间与能量消耗作为并列目标，利用 MSMOACO 求解 Pareto 最优时间-能量折中。

## 题目驱动研究框架
- 研究场景：大范围 IoT 设备的数据采集与多 UAV 协同巡航。
- 研究对象：多架 UAV、IoT 终端、悬停采集点、飞行速度与避碰控制。
- 核心问题：如何同时压低最大任务完成时间与最大能量消耗，而不是只优化其中一个指标。
- 标题承诺的方法：energy and time trade-off optimization。
- 期望效果：得到一组 Pareto 最优解，供系统按任务偏好选取。
- 标题与正文的偏差：正文的重要补充是自适应悬停与几何避碰机制，让多目标结果更接近真实部署。

## Algorithm Design 快照
论文针对多 UAV 物联网数据采集中的时间与能量冲突目标，联合设计每架 UAV 的轨迹、悬停位置、飞行速度和避碰策略，以同时最小化最大完成时间和最大能量消耗。作者把问题写成多目标优化，并使用多策略多目标蚁群算法 MSMOACO 搜索 Pareto 前沿。算法中嵌入适应度引导变异、自适应悬停优化和几何避碰策略，使其既能在复杂网络场景中寻找高质量时间-能量折中解，又能避免多 UAV 之间的潜在碰撞。

## 图1系统框架草案
- 系统实体：多个起终点已知的 UAV、随机分布 IoT 设备、悬停采集点。
- 任务/数据流：UAV 飞往若干 IoT 设备附近悬停完成数据采集，然后返回终点。
- 控制/优化变量：任务分配、访问顺序、悬停位置、飞行速度、避碰轨迹修正。
- 约束来源：机载能量、飞行时间、通信范围、起终点约束、最小安全间距。
- 画图提醒：图里最好同时画出 Pareto 前沿和多机避碰后的轨迹更新结果。

## System Model
- 每架 UAV 从给定起点出发，访问其负责的 IoT 设备集合后回到目标终点。
- 数据采集可通过调整悬停位置来平衡访问精度与飞行代价。
- 目标函数不是总和，而是“最大任务完成时间”和“最大能量消耗”这两个 worst-case 指标。
- 为适应实际多机协同，模型显式加入几何避碰策略来修正轨迹冲突。

## Algorithm Design 详解
- 第一步编码多 UAV 的设备分配、访问序列、悬停位置与速度控制变量。
- 第二步用改进 ACO 生成可行轨迹，并通过自适应悬停优化提升通信效率。
- 第三步通过多策略变异与 Pareto 支配关系维护时间-能量折中解集。
- 第四步在冲突场景中使用几何避碰策略实时调整局部飞行段。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成 IoT 设备分布与场景参数
- 平台与软件：未说明
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文给出了多场景参数和 20 次重复实验，但软件栈与硬件条件未明确。

## Introduction 写作素材
- 真实数据采集任务往往同时关心“最慢 UAV 何时完成”和“最累 UAV 会不会先耗尽电量”。
- 单目标最优常把负担压在少数 UAV 上，因此需要引入 max-time 与 max-energy 的公平折中。
- 这篇论文适合承接“多 UAV 调度需要从单指标最优转向 Pareto 决策”的写作视角。

## Related Work 写作素材
- 与只最小化飞行时间的工作不同，本文把最大能量消耗作为同等重要的目标。
- 与单 UAV 数据采集不同，本文显式考虑多 UAV 避碰与并行调度。
- 与传统 ACO 不同，本文引入多策略变异和自适应悬停机制。

## 相关系统建模页
- [[无人机能耗模型]]
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[轨迹优化]]
- [[无人机辅助群智感知与持续作业]]
- [[轨迹优化与协同控制]]

## 来源
- [原文](../raw/markdown/jia2024EnergyTimeTradeoff.md)
