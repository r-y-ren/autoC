---
tags: [论文, 目标跟踪, USV, MEC, 计算卸载]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/wang2024UAVassistedTargetTracking.md
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
frameworks:
  - Lyapunov optimization
  - Elman neural network
  - BAS-Elman
  - JOISR
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Wang2024 USV辅助MEC中的UAV目标跟踪与计算卸载

## 单行摘要
论文在海上目标跟踪场景中利用 USV-based MEC 分担 UAV 图像处理负载，并通过 Lyapunov 优化与 BAS-Elman 跟踪器联合平衡能耗、检测精度与队列稳定性。

## 题目驱动研究框架
- 研究场景：海上目标跟踪与空海跨域协同边缘计算。
- 研究对象：单架 UAV、多个 USV 边缘服务器、移动目标、图像处理任务队列。
- 核心问题：如何在目标运动随机、UAV 能量有限和图像处理开销高的情况下维持高成功率跟踪。
- 标题承诺的方法：UAV-assisted target tracking and computation offloading in USV-based MEC networks.
- 期望效果：兼顾推进能耗、数据处理能耗、图像检测精度与队列稳定。
- 标题与正文的偏差：正文重点不只是 offloading，而是“实时跟踪控制 + 随机卸载资源分配”两阶段联动。

## Algorithm Design 快照
论文研究海上目标跟踪中的空海协同问题。UAV 需要根据机载相机持续跟踪目标，但高分辨率图像处理会消耗大量能量和算力，因此作者引入 USV 作为海上 MEC 服务器分担处理负载。整体框架分为两阶段：先用 BAS-Elman 神经网络预测目标运动并维持实时跟踪，再用 Lyapunov 方法把随机数据处理、计算卸载与资源分配转化为逐时隙确定性问题。这样，飞行控制与边缘卸载被整合进一套跨域闭环框架。

## 图1系统框架草案
- 系统实体：单 UAV、多个 USV MEC 节点、海上移动目标、地面/岸基控制端。
- 任务/数据流：UAV 采集目标图像并决定本地处理或卸载到 USV；USV 返回处理结果以辅助下一步跟踪。
- 控制/优化变量：跟踪距离、图像分辨率、卸载比例、带宽与计算资源分配。
- 约束来源：UAV 电量、USV 资源、随机目标运动、数据队列稳定性。
- 画图提醒：图中要突出“实时跟踪环”和“数据处理/卸载环”两套耦合闭环。

## System Model
- UAV 在随机海面环境中跟踪目标，目标运动受海流等因素影响。
- UAV 采集的图像会进入数据队列，分辨率越高检测精度越好，但处理开销也越大。
- USV 作为边缘服务器承担部分计算，缓解 UAV 算力和能量受限问题。
- 优化目标同时涉及推进能耗、数据处理能耗、检测准确率和数据存储队列稳定性。

## Algorithm Design 详解
- 跟踪阶段：利用 BAS-Elman 神经网络从历史目标状态中预测下一时刻运动，实现轻量实时跟踪。
- 卸载阶段：基于 Lyapunov 把随机优化问题拆解为逐时隙决策，联合处理资源分配和计算卸载。
- JOISR：把图像分辨率、处理方式、资源分配等决策打包为统一方案。
- 方法意义：这篇论文把[[目标跟踪]]、[[USV辅助MEC]]与[[任务卸载]]真正串起来，形成空海协同的跨域 UAC 分支。
- 实验结论：所提方案在保持高跟踪成功率的同时降低推进能耗，并能动态权衡检测精度与队列长度。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成随机海上环境
- 平台与软件：未说明
- 硬件与算力：未明确披露
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文给出两阶段优化的实时性分析与多组对比曲线，但未披露实现栈。

## Introduction 写作素材
- 目标跟踪和边缘卸载在海上场景中不是两件独立事情，图像处理负担会反向影响跟踪策略。
- USV 作为海上 MEC 节点，是把空中计算扩展到跨域协同的重要基础设施。
- 这篇论文适合支撑“UAC 正从单域 UAV-MEC 走向空海协同边缘计算”的引言判断。

## Related Work 写作素材
- 与预知目标轨迹的路径规划工作相比，本文强调随机目标运动下的实时跟踪。
- 与只做视觉跟踪的工作相比，本文同时处理图像处理卸载和队列稳定。
- 与常见地面 MEC 场景相比，本文采用 USV 作为移动海上边缘节点，更强调跨域协同。

## 相关系统建模页
- [[计算卸载模型]]
- [[任务队列与时延保障模型]]

## 相关概念与主题页
- [[目标跟踪]]
- [[USV辅助MEC]]
- [[任务卸载与资源分配研究主线]]
- [[轨迹优化与协同控制]]
- [[UAC研究路线图]]

## 来源
- [原文](../raw/markdown/wang2024UAVassistedTargetTracking.md)
