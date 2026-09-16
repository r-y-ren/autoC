---
tags: [论文, 可靠性, 空地通信, 运动控制, 资源分配]
created: 2026-04-09
updated: 2026-04-09
sources:
  - ../raw/markdown/zhou2024JointOptimizationMobility.md
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
  - bi-level optimization
  - epsilon-constraint
  - sequential quadratic programming
  - KKT
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Zhou2024 UAV移动性与可靠性保障空地通信联合优化

## 单行摘要
论文研究单 UAV 空地通信中的“移动性-可靠性”耦合问题，通过双层优化联合控制加速度、发射功率和数据调度，在满足可靠性约束下最小化总能耗。

## 题目驱动研究框架
- 研究场景：单 UAV 为多个地面基站执行空地数据卸载任务。
- 研究对象：UAV 运动状态、发射功率、数据调度、地面基站和 A2G 可靠性。
- 核心问题：若只追求最短飞行或最低传输功率，往往无法保证通信可靠性；而严格可靠性又会改变 UAV 的最优轨迹。
- 标题承诺的方法：joint optimization of mobility and reliability-guaranteed A2G communication。
- 期望效果：在同等可靠性要求下尽可能降低 UAV 运动与通信联合能耗。
- 标题与正文的偏差：正文的一个关键亮点是把“可靠性约束”放进双层最优控制框架，而不只是补一个链路约束项。

## Algorithm Design 快照
作者先从 A2G 可靠性出发，将传输功率、调度比例与 UAV 运动状态联立，构造可靠性表达式。随后，用 `epsilon-constraint` 将“可靠性下界”嵌入能耗最小化目标中，形成双层优化问题。求解时，作者基于 `Lagrangian` 与顺序二次规划思想，迭代求解 UAV 加速度控制、发射功率与数据调度，使 UAV 在飞行轨迹、通信动作与可靠性目标之间取得平衡。

## 图1系统框架草案
- 空中层：单 UAV 沿任务时域飞行并执行数据卸载。
- 地面层：多个基站分布在道路周边，提供 A2G 连接机会。
- 控制层：同时决定 UAV 加速度、发射功率和各时隙数据量。
- 约束层：可靠性下界、任务时限、飞行高度与运动学约束。
- 画图提醒：应把“可靠性约束反推轨迹”这一点画出来，而不只是普通的 UAV 飞行示意图。

## System Model
- UAV 在给定起终状态与时间窗内飞行，向多个地面基站执行空地数据传输。
- 系统假设 UAV 高度固定，控制主要发生在二维平面运动上。
- 可靠性由发射功率、链路距离、数据调度和路径损耗共同决定，并被设为显式约束。
- 总能耗包含飞行能耗与通信能耗，因此轨迹与通信策略天然耦合。

## Algorithm Design 详解
- 首先建立可靠性约束下的联合能耗优化模型，变量包括 UAV 加速度、发射功率和数据调度向量。
- 然后通过 `epsilon-constraint` 将可靠性要求转为可控阈值，使问题能够在不同可靠性等级下生成 Pareto 前沿。
- 接着基于 `Lagrangian` 与顺序二次规划构造可迭代求解的数值算法，并证明收敛到 `KKT` 点。
- 论文还系统分析了飞行高度、任务时长、数据负载和路径损耗指数对能耗-可靠性折中的影响。
- 这篇工作适合作为“可靠性导向空地通信”而非“纯速率导向通信”分支的代表论文。

## 实验证据卡片
- 验证类型：`simulation`
- 数据来源：合成道路基站布局与 A2G 参数
- 平台与软件：未明确说明
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文给出了算法收敛、性能比较和 Pareto 折中分析，但暂无真实飞行或公开代码支撑。

## Introduction 写作素材
- 空地通信里的可靠性不能被平均吞吐替代，因为很多任务真正关心的是“能否稳定完成”。
- 一旦把可靠性显式化，UAV 的最优飞行路径和功率策略都会被改写。
- 因此，移动性控制与通信调度不应分开设计。

## Related Work 写作素材
- 既有 UAV 通信优化多聚焦吞吐、能效或覆盖，而本文把可靠性保障作为一等目标。
- 与随机 LoS/NLoS 型可靠性论文相比，这篇更偏最优控制和能耗折中视角。
- 若后续你要组织“可靠性保障空地通信”分支，这篇适合放在方法层入口。

## 相关系统建模页
- [[信道与通信速率模型]]
- [[无人机能耗模型]]

## 相关概念与主题页
- [[可靠性保障空地通信]]
- [[空中通信与协同传输]]
- [[安全与服务保障]]

## 来源
- [原文](../raw/markdown/zhou2024JointOptimizationMobility.md)
