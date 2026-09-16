---
tags: [论文, 边缘分析, 共调度, 真实轨迹, 机载推理]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/khochare2024ImprovedAlgorithmsCoScheduling.md
venue_tier: CCF-A
literature_type: system
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - methodology
  - system_model
validation_type:
  - simulation
  - trace_driven
  - field_test
data_origin:
  - mixed
platforms:
  - Python
frameworks:
  - IBM CPLEX MILP solver v12
datasets:
  - OpenStreetMap Bangalore road network subset
hardware_stack:
  - Intel Xeon Gold 6208U CPU
  - 128 GB RAM
  - X-wing quad-copter
  - Pixhawk2 flight controller
  - NVIDIA Jetson TX2
artifact_availability: unknown
reproducibility_level: medium
---


# Khochare2024 无人机编队任务中边缘分析与航线共调度

## 单行摘要
论文提出 Mission Scheduling Problem，把无人机编队的航线规划与机载视觉分析任务统一共调度，并用真实飞行能耗轨迹校验调度可执行性。

## 题目驱动研究框架
- 研究场景：城市巡检、交通监测和建造测绘等多无人机边缘分析任务。
- 研究对象：无人机编队、航线、观测活动、机载 DNN 推理、能量与截止期。
- 核心问题：访问路径和机载分析任务不能分开优化，否则既可能错过时限，也可能浪费能源。
- 标题承诺的方法：co-scheduling of edge analytics and routes。
- 期望效果：在满足截止期和能量预算的前提下最大化采集与计算效用。
- 标题与正文的偏差：正文真正的价值是把“真实飞行/悬停/计算能耗轨迹”拉回调度验证中。

## Algorithm Design 快照
论文围绕无人机编队执行视觉巡检任务时“飞到哪里”和“何时在机上完成分析”这两个耦合决策，提出 Mission Scheduling Problem。问题同时考虑航线、悬停观测、DNN 推理、活动截止期、计算资源和能源预算。作者首先证明 MSP 是 NP-hard，并用 MILP 得到最优基线；随后设计五个启发式调度器，在不同负载下实现效用与运行时权衡。更重要的是，论文基于 X-wing 四旋翼的真实飞行、悬停和机载推理能耗轨迹，对生成的任务时间线进行回放验证，从而评估真实电量条件下的行程完成率。

## 图1系统框架草案
- 系统实体：多架无人机、活动航点、机载相机、机载 DNN 推理模块、调度器。
- 任务/数据流：无人机飞往活动点采集视频，再在机载模块上完成部分边缘分析。
- 控制/优化变量：活动分配、路线顺序、起飞/降落时间、机载计算安排。
- 约束来源：能量预算、活动开始时间、处理截止期、机载算力、无人机数量。
- 画图提醒：图里最好把“路线层”和“分析层”画成同一时间线上的并行约束。

## System Model
- 每个活动既需要被访问采集，也可能需要在机上完成 DNN 推理。
- 任务效用由数据采集、按时分析和机上处理价值共同组成。
- UAV 的飞行、悬停和计算都消耗能量，因此调度必须同时考虑三类成本。
- 真实路网、活动时间窗和机载 DNN 延迟共同决定任务可行性。

## Algorithm Design 详解
- 第一步把航线与机载分析耦合成 MSP，并用 MILP 建立最优解基线。
- 第二步设计 CS、RSS、HUFD、EOFO 和 IPS 五类启发式调度器。
- 第三步在不同工作负载、活动类型和负载因子下比较效用与运行时。
- 第四步使用真实飞行/悬停/推理能耗轨迹回放调度时间线，检查计划是否能真实完成。

## 实验证据卡片
- 验证类型：数值仿真；真实数据驱动仿真；真实飞行/现场测试
- 数据来源：真实飞行能耗轨迹 + `OpenStreetMap Bangalore road network subset`
- 平台与软件：`Python`；`IBM CPLEX MILP solver v12`
- 硬件与算力：`Intel Xeon Gold 6208U CPU`；`128 GB RAM`；`X-wing quad-copter`；`Pixhawk2 flight controller`；`NVIDIA Jetson TX2`
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：这篇论文虽然不是完整在线原型，但在真实能耗轨迹和机载计算方面的实验链条很扎实。

## Introduction 写作素材
- 许多无人机任务规划工作默认“先飞完，再离线分析”，但实际边缘系统需要把飞行和推理同时考虑。
- 路线与机载分析如果分开调度，会直接损害活动截止期和电量可行性。
- 这篇论文适合支撑“空中任务执行正在从路径规划走向飞行-计算协同调度”的论断。

## Related Work 写作素材
- 与经典车辆路径问题不同，本文把机载边缘分析和任务截止期引入同一模型。
- 与只做最优 MILP 的工作不同，本文还提供多种实用启发式调度器。
- 与纯理想能耗模型不同，本文用真实飞行与推理能耗轨迹进行可行性回放。

## 相关系统建模页
- [[无人机能耗模型]]
- [[任务队列与时延保障模型]]

## 相关概念与主题页
- [[边缘分析共调度]]
- [[无人机辅助群智感知与持续作业]]
- [[实验与复现证据总览]]

## 来源
- [原文](../raw/markdown/khochare2024ImprovedAlgorithmsCoScheduling.md)
