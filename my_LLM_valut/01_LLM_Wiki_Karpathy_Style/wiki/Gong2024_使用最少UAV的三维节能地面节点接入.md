---
tags: [论文, 三维覆盖, 无人机部署, 能耗优化, 多无人机协同]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/gong2024Energyefficient3DUAV.md
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
  - MATLAB
frameworks:
  - CVX
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Gong2024 使用最少 UAV 的三维节能地面节点接入

## 单行摘要
论文在三维地面节点接入场景中同时优化能耗与 UAV 数量，通过最少 UAV 的路径规划实现节能访问。

## 题目驱动研究框架
- 研究场景：多 UAV 在三维空间中访问一组地面节点并完成通信/采集任务。
- 研究对象：多个地面节点、可协同工作的多架 UAV、三维飞行轨迹与节点访问顺序。
- 核心问题：如何既减少总体能耗，又避免使用超过必要数量的 UAV。
- 标题承诺的方法：energy-efficient 3-D UAV ground node accessing using the minimum number of UAVs。
- 期望效果：在更一般化的 3D 场景中，用最少 UAV 实现节能接入。
- 标题与正文的偏差：标题强调 minimum number of UAVs，但正文还把单 UAV 相邻节点访问能耗建模和多 UAV 路径分配结合起来。

## Algorithm Design 快照
论文研究多 UAV 在三维空间访问地面节点的节能问题，目标不是在给定 UAV 数量下压缩能耗，而是同时决定“需要多少架 UAV”以及“每架 UAV 如何访问节点”。作者先求解单架 UAV 连续访问任意两个地面节点时的能耗最优控制，再把多 UAV 场景下的地面节点路径规划与 UAV 数量选择统一起来，最终形成基于最少 UAV 的节能访问框架。

## 图1系统框架草案
- 系统实体：若干地面节点、多架 UAV、三维飞行空间。
- 任务/数据流：每个地面节点需被某架 UAV 访问，UAV 按规划路径依次完成节点接入。
- 控制/优化变量：UAV 数量、节点分配、访问顺序、三维飞行轨迹。
- 约束来源：UAV 运动学、推进能耗、三维空间高度变化、节点全覆盖要求。
- 画图提醒：应把“单 UAV 两点间最优能耗”与“多 UAV 节点路径分配”分上下两层。

## System Model
- 论文把三维地面节点接入问题抽象为多 UAV 访问路径与数量联合优化。
- 单 UAV 能耗不仅与水平距离有关，还与三维飞行姿态和轨迹控制有关。
- 多 UAV 层面则需要决定节点如何分配到不同 UAV，以及是否增加 UAV 以降低总体能耗。
- 因此该模型天然连接部署优化、三维覆盖和能耗模型三个层面。

## Algorithm Design 详解
- 第一步是单 UAV 两节点访问子问题建模，求解能耗最优的三维访问控制。
- 第二步是把多节点访问抽象为多 UAV 路径规划与分配问题。
- 第三步是把 UAV 数量也纳入优化对象，从“固定规模优化”推进到“必要规模优化”。
- 第四步是结合凸优化与启发式/群智能路径分配算法求解整体问题。
- 第五步是用 MATLAB/CVX 仿真展示最少 UAV 约束下的能耗优势。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成场景或参数仿真
- 平台与软件：`MATLAB`；`CVX`
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文提供了较清晰的 MATLAB/CVX 实验链条，适合作为三维覆盖与部署方向的系统建模参考。

## Introduction 写作素材
- 很多多 UAV 覆盖工作默认 UAV 数量足够，但现实中硬件数量和部署成本往往受限。
- 当三维能耗模型进入问题后，部署数量和路径控制就不能再分开看。
- 这篇论文适合支撑“最少 UAV + 节能接入”这一更工程化的问题定义。

## Related Work 写作素材
- 与固定 UAV 数量的节能路径规划工作相比，本文把 UAV 数量作为决策变量。
- 与二维覆盖/巡航模型相比，本文强调 3D 场景下的能耗建模。
- 与只优化访问顺序的工作相比，本文同时关注相邻节点间的飞行控制代价。

## 相关系统建模页
- [[区域覆盖与部署模型]]
- [[无人机能耗模型]]

## 相关概念与主题页
- [[三维区域覆盖]]
- [[无人机部署优化]]
- [[覆盖与部署优化主线]]

## 来源
- [原文](../raw/markdown/gong2024Energyefficient3DUAV.md)
