---
tags: [论文, WRSN, 目标覆盖, 充电调度, 多目标优化]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/xue2024MaximizingCoverageTargets.md
venue_tier: CCF-A
literature_type: method
evidence_tier: core
paper_role: supporting
use_for:
  - methodology
  - related_work
  - idea_seed
validation_type:
  - simulation
data_origin:
  - synthetic
platforms: []
frameworks:
  - MaxCov
  - MaxCov-RG
  - cooperative game
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Xue2024 面向WRSN目标覆盖最大化的多充电器调度

## 单行摘要
论文在多移动充电器 WRSN 中把“目标覆盖”而非“节点存活率”作为首要目标，并通过 MaxCov 与 MaxCov-RG 联合优化平均覆盖和能效。

## 题目驱动研究框架
- 研究场景：面向特定目标监测任务的无线可充电传感器网络。
- 研究对象：传感器节点、目标集合、多个移动充电器 MC、基站。
- 核心问题：充电调度若只最大化节点生存率，未必能最大化目标覆盖质量。
- 标题承诺的方法：maximizing coverage of targets by multiple chargers scheduling。
- 期望效果：在按需充电架构中提升平均覆盖率与能效，并兼顾计算复杂度。
- 标题与正文的偏差：正文真正亮点是把 request grouping 与 cooperative scheduling 结合起来，而不仅是简单多充电器扩展。

## Algorithm Design 快照
论文研究按需充电架构下的 CoT 最大化问题。网络包含多个移动充电器和多个基站，传感器节点因电量动态变化而不断离开或回到工作状态，网络拓扑持续演化。难点在于“谁先被充电”会直接改变目标覆盖率，而不仅影响节点寿命。为此，作者提出 MaxCov 和 MaxCov-RG：前者围绕请求池、请求优先级和匹配过程优化覆盖；后者进一步用分组机制在性能和实时性之间折中。虽然这篇论文不属于标准 UAV-MEC，但它为持续服务系统中的“覆盖优先级 + 补能调度”提供了很强的建模参考。

## 图1系统框架草案
- 系统实体：传感器节点、目标点、移动充电器、基站。
- 任务/数据流：节点上报充电请求；充电器从基站出发执行充电任务；节点恢复后继续覆盖目标。
- 控制/优化变量：请求池构造、请求匹配、请求分组、充电器路径。
- 约束来源：目标覆盖要求、节点剩余能量、充电器移动时间、基站数量。
- 画图提醒：图中应突出“覆盖目标”与“保持节点存活”是不同层级目标。

## System Model
- WRSN 由静态可充电传感器、多个移动充电器和多个基站组成。
- 目标覆盖率 CoT 是主评价指标，节点生存率只是支撑指标。
- 充电请求以池化方式进入系统，充电器按风险-收益比与路径成本选择下一个任务。
- 多充电器之间通过请求分组和协同机制减少冲突与计算负担。

## Algorithm Design 详解
- MaxCov：构建请求池、计算优先级并做匹配，以直接优化目标覆盖。
- MaxCov-RG：对请求做分组，再在组级别上求解，减少计算复杂度并提升多充电器协同效率。
- 理论分析：将问题证明为 NP-hard，并借助 M/M/n 与多个 M/M/1 的对比讨论协同优势。
- 实验结论：在平均覆盖率、覆盖率曲线、能效和节点生存率上，MaxCov-RG 都优于对比基线。
- 对当前 wiki 的意义：它更像[[覆盖与部署优化主线]]与持续补能系统之间的一条跨域桥梁。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成 WRSN 网络规模与目标分布
- 平台与软件：未说明
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文系统给出了多种网络规模、基站数量与路径深度参数分析，但未披露实现平台。

## Introduction 写作素材
- 在持续服务系统中，维持“关键目标是否被持续覆盖”往往比单纯延长节点寿命更重要。
- 多补能主体的调度问题天然包含覆盖收益与移动成本之间的权衡。
- 这篇论文适合支撑“补能调度应围绕任务目标而不是只围绕设备存活”的写作判断。

## Related Work 写作素材
- 与传统移动充电研究相比，本文把目标覆盖而非节点生存作为主目标。
- 与单充电器算法相比，本文显式处理多充电器协同与请求分组。
- 与 UAV 持续作业研究相比，本文提供了一个很有价值的跨域参考：补能策略如何被任务层目标重写。

## 相关系统建模页
- [[区域覆盖与部署模型]]

## 相关概念与主题页
- [[无线可充电传感器网络（WRSN）]]
- [[目标覆盖最大化]]
- [[覆盖与部署优化主线]]
- [[无线供能移动边缘计算]]
- [[UAC研究路线图]]

## 来源
- [原文](../raw/markdown/xue2024MaximizingCoverageTargets.md)
