---
tags: [论文, 三维轨迹优化, 智慧城市, 多任务, 补能]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/zema20243DTrajectoryOptimization.md
venue_tier: CCF-A
literature_type: system
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - methodology
  - engineering_context
validation_type:
  - simulation
data_origin:
  - synthetic
platforms:
  - NS3 3.30
  - Java
  - CPLEX 12.10
  - CPLEX 12.7
frameworks:
  - MILP
  - online reactive planning
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Zema2024 智慧城市多任务UAV的三维轨迹优化

## 单行摘要
论文围绕智慧城市中的多任务 UAV 规划，引入 TRA 与 EDD 设施，把离线 MILP 与在线反应式规划结合起来，处理补能、数据下载与三维飞行协同问题。

## 题目驱动研究框架
- 研究场景：智慧城市中多架 UAV 在执行任务同时需要 opportunistic recharge 和数据同步的场景。
- 研究对象：UAV、Training and Recharge Areas (TRA)、Energy and Data Dispensers (EDD)、多任务区域。
- 核心问题：如何在三维城市环境中同时满足任务执行、补能停靠、数据下载与时限要求。
- 标题承诺的方法：3D trajectory optimization for multimission UAVs。
- 期望效果：让离线全局规划与在线轻量规划之间形成可对照、可替换的工程路线。
- 标题与正文的偏差：正文真正价值在于 TRA/EDD 这一基础设施设定，以及 offline vs online 的清晰工程比较。

## Algorithm Design 快照
论文研究智慧城市中的多任务 UAV 三维轨迹规划问题。为扩展 UAV 的持续作业能力，作者提出 TRA 和 EDD 设施：UAV 可以在特定区域停靠补能并通过高速链路下载数据。难点在于多个 UAV 共享 EDD 带宽、城市三维路径和时限约束彼此耦合，且离线全局最优与在线快速反应之间存在明显计算代价差异。为此，作者分别给出离线 MILP 模型与在线仿真驱动规划方案，并用 NS3 提供通信参数与在线性能评估。

## 图1系统框架草案
- 系统实体：UAV、TRA、EDD、任务区域、城市建筑环境。
- 任务/数据流：UAV 执行任务 -> 进入 TRA -> 接入 EDD 完成补能与数据下载 -> 返回任务区域。
- 控制/优化变量：UAV 访问顺序、EDD 连接选择、三维位置与离场时刻。
- 约束来源：飞行时间、带宽共享、充电与下载时间、区域进出限制。
- 画图提醒：图中应明确 TRA 是区域设施、EDD 是区域内具体补能/数据节点。

## System Model
- 城市场景中存在一个或多个 TRA，TRA 内部署若干 EDD 作为补能与高速通信节点。
- UAV 在执行任务过程中可 opportunistically 进入 TRA，完成数据下载和电量恢复。
- 离线模型将问题写成 MILP，在线模型则在 NS3 中按事件驱动近似决策。
- 多 UAV 同时连接同一 EDD 时会共享带宽，因此连接分配直接影响停留时间。

## Algorithm Design 详解
- 离线模型：分别给出 M1 与 M2 两类目标，在完整先验下用 CPLEX 求解。
- 在线模型：在 NS3 里以 mobility model + application 形式实现 UAV 与 EDD 的交互。
- Preliminary simulation：先通过 NS3 测定不同并发连接数下的带宽和 10 MB 下载时间，再回填给离线模型。
- 对比结论：离线模型在小规模实例上可提供 benchmark，但计算开销会指数增长；在线方案更适合实际运行。
- 这篇论文非常适合作为[[训练与补能区域（TRA）]]与工程仿真平台分支的入口页。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成智慧城市 TRA/EDD 场景
- 平台与软件：`NS3 3.30`、`Java`、`CPLEX 12.10`、`CPLEX 12.7`
- 硬件与算力：论文披露 `Java VM memory = 7500 MB`
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文把网络预仿真、离线求解和在线 NS3 对比串联起来，平台层信息比较完整。

## Introduction 写作素材
- 智慧城市中的 UAV 不只是“执行任务”，还需要像移动终端一样 opportunistically 接入补能与高带宽基础设施。
- 若没有 TRA/EDD 这类中继设施，多任务 UAV 的持续作业能力会很快触到能量与数据回传天花板。
- 这篇论文适合支撑“空中持续作业需要基础设施级补能与数据同步节点”的判断。

## Related Work 写作素材
- 与只讨论电池补能的持续作业研究相比，本文同时引入补能和数据下载。
- 与纯离线 MILP 规划相比，本文进一步给出可在 NS3 中运行的在线近似策略。
- 与传统单次任务路径规划相比，本文强调的是多任务与基础设施机会接入。

## 相关系统建模页
- [[区域覆盖与部署模型]]
- [[无人机能耗模型]]

## 相关概念与主题页
- [[训练与补能区域（TRA）]]
- [[覆盖与部署优化主线]]
- [[轨迹优化与协同控制]]
- [[无人机辅助群智感知与持续作业]]
- [[UAC研究路线图]]

## 来源
- [原文](../raw/markdown/zema20243DTrajectoryOptimization.md)
