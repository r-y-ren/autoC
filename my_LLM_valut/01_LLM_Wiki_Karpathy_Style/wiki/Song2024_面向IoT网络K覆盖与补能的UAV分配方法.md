---
tags: [论文, K覆盖, 补能调度, MPC, MCTS, IoT]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/song2024MethodsAssignUAVs.md
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
  - mixed
platforms:
  - Python
  - Gurobi
frameworks:
  - MILP
  - MPC
  - MCTS
  - Gaussian mixture model
datasets: []
hardware_stack:
  - Intel Core i5 2.4 GHz CPU
  - 8 GB RAM
  - DJI Mavic 3
  - HEISHA C300 charging pad
artifact_availability: unknown
reproducibility_level: medium
---

# Song2024 面向IoT网络K覆盖与补能的UAV分配方法

## 单行摘要
论文在太阳能充电平台支持的 IoT 网络中联合优化 UAV 对监测点与充电平台的多时隙分配，以最大化 K-coverage lifetime。

## 题目驱动研究框架
- 研究场景：具有太阳能充电平台的 IoT 监测网络。
- 研究对象：多架 UAV、监测点、太阳能充电平台、中央控制器。
- 核心问题：在多时隙能量耦合和未来光照未知的条件下，如何维持长期 K 覆盖。
- 标题承诺的方法：assign UAVs for K-coverage and recharging.
- 期望效果：使 UAV 在监测与回充之间切换时获得尽可能长的持续覆盖寿命。
- 标题与正文的偏差：正文重点不只是 assignment，而是“多时隙能量状态 + 预测式决策 + K 覆盖寿命最大化”的系统控制框架。

## Algorithm Design 快照
论文研究多架 UAV 在监测点和太阳能充电平台之间的分配问题，目标是在整个规划周期内尽可能延长 K-coverage lifetime。难点在于 UAV 电量和充电平台储能在时间上耦合，且未来光照到达是未知的。作者先构建一个需要非因果信息的 MILP 作为最优基准，再用 GMM 预测未来充电能量，把 MPC-MILP 变成可在线执行的方案，同时设计基于 Monte Carlo Tree Search 的启发式方法降低计算开销。这样，K 覆盖、补能与能量溢出管理被统一到了同一张时隙决策图中。

## 图1系统框架草案
- 系统实体：监测点集合、太阳能充电平台集合、多架 UAV、控制器。
- 任务/数据流：控制器收集平台能量状态并下发 UAV 下一时隙的监测/充电分配。
- 控制/优化变量：每架 UAV 当前去哪个监测点或充电平台、何时回充、平台能量存储状态。
- 约束来源：K-coverage 约束、UAV 电池容量、平台储能上限、太阳能随机到达。
- 画图提醒：图中要突出“监测点-充电平台-时间轴”三维关系，而不是仅画静态部署图。

## System Model
- 系统按离散时隙运行，每个时隙都要决定 UAV 去监测点还是去充电平台。
- 充电平台能量受太阳能随机到达影响，并存在电量溢出损失。
- UAV 的剩余能量既受飞行距离影响，也受悬停监测与充电影响。
- 目标函数是最大化连续满足 K-coverage 的时隙数，而不是最小化单次代价。

## Algorithm Design 详解
- MILP 基准：在已知未来能量到达的理想条件下求解全局最优分配。
- MPC-MILP：控制器通过 GMM 预测未来一段时间的平台能量到达，再滚动求解 MILP。
- MCTS：把每一时隙的替换/回充决策组织为树搜索，依靠 rollout 评估 coverage lifetime。
- 对比意义：MILP 是上界，MPC 是可部署近似，MCTS 是更轻量的在线启发式。
- 关键结果：MPC 与 MCTS 的 coverage lifetime 分别约为 MILP 的 `81.04%` 与 `67.07%`。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成监测拓扑与测量驱动的太阳能到达模型
- 平台与软件：`Python`、`Gurobi`
- 硬件与算力：`Intel Core i5 2.4 GHz CPU`、`8 GB RAM`
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文公开了求解平台、复杂度分析和多组参数扫描，但未公开完整代码。

## Introduction 写作素材
- 持续监测系统的难点不只是 UAV 电量有限，而是“谁监测、谁补能、什么时候换班”在时间上强耦合。
- 一旦引入太阳能充电平台，平台自身储能状态就成为新的系统瓶颈。
- 这篇论文适合支撑“长期覆盖问题应从静态部署走向时隙化能量控制”的引言判断。

## Related Work 写作素材
- 与传统 coverage/deployment 研究相比，本文把补能平台能量演化显式纳入系统状态。
- 与只做充电调度的工作相比，本文同时要求每个时隙满足 K-coverage。
- 与纯最优控制模型相比，本文提供了 MPC 与 MCTS 两条更接近可执行系统的落地路线。

## 相关系统建模页
- [[无人机能耗模型]]
- [[区域覆盖与部署模型]]

## 相关概念与主题页
- [[K覆盖]]
- [[无线充电网络（WCN）]]
- [[覆盖与部署优化主线]]
- [[无人机辅助群智感知与持续作业]]
- [[UAC研究路线图]]

## 来源
- [原文](../raw/markdown/song2024MethodsAssignUAVs.md)
