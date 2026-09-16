---
tags: [论文, AoI, MEC, 多目标强化学习, HAP]
created: 2026-04-09
updated: 2026-04-09
sources:
  - ../raw/markdown/song2024AoIEnergyTradeoff.md
venue_tier: CCF-A
literature_type: method
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - methodology
  - related_work
validation_type:
  - simulation
data_origin:
  - synthetic
platforms: []
frameworks:
  - MOMDP
  - MOPPO
  - evolutionary refinement
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Song2024 空地协同MEC中的AoI与能耗权衡学习

## 单行摘要
论文在 `HAP + UAV` 空地协同 MEC 中联合优化 UAV 飞行路径与任务卸载比例，利用 `MOPPO + 进化算子` 学习一组 `AoI-能耗` 折中策略而非单一固定偏好解。

## 题目驱动研究框架
- 研究场景：高空平台与 UAV 协同提供边缘计算服务的空地协同 MEC 网络。
- 研究对象：UAV 轨迹、地面设备任务、任务卸载比例、AoI 与 UAV 能耗。
- 核心问题：AoI 和能耗天然冲突，固定加权的单目标化方法难以表达动态偏好。
- 标题承诺的方法：AoI and energy tradeoff with a multi-objective learning approach。
- 期望效果：得到一组高质量非支配策略，供不同偏好下的系统按需选择。
- 标题与正文的偏差：正文真正重要的是“输出一组 Pareto 策略”，而不是某一个唯一最优策略。

## Algorithm Design 快照
论文首先把 `AoI-能耗权衡` 写成带向量奖励的多目标 MDP，使 AoI 与能耗分别对应奖励向量的不同维度。随后使用 `MOPPO` 训练多个带不同权重偏好的学习个体，获得非支配策略集合；再用参数级交叉与变异对策略网络做进一步进化增强，避免局部最优和过早收敛。这样，系统不再输出一个固定权衡点，而是输出随用户偏好可切换的策略前沿。

## 图1系统框架草案
- 基础设施层：HAP、UAV、地面设备 GD。
- 任务流：GD 产生任务，UAV 采集后本地处理或协同卸载。
- 状态层：GD 位置与 AoI、UAV 坐标、任务队列状态。
- 决策层：飞行方向、飞行距离、卸载比例。
- 画图提醒：要把“训练阶段得到 Pareto 策略集”单独画出来，体现多目标学习特色。

## System Model
- HAP 与 UAV 共同为地面设备提供计算支持，UAV 负责机动接入与任务收集。
- 每个地面设备的数据新鲜度用 AoI 描述，而 UAV 飞行会引入显著推进能耗。
- 系统同时优化 UAV 飞行路径和任务卸载比例，以降低总 AoI 与总能耗。
- 用户偏好可随时间变化，因此系统更适合输出策略集合而非单一固定权重解。

## Algorithm Design 详解
- 把问题形式化为向量奖励的多目标 MDP，使每个目标保持独立语义。
- 采用 `MOPPO` 训练多个学习个体，每个个体对应一种偏好权重向量。
- 用进化算子在参数层面继续改良策略网络，增强全局探索能力。
- 该文很适合支撑“为什么空地协同 MEC 需要 Pareto 策略而不是单一加权最优”的写作论证。

## 实验证据卡片
- 验证类型：`simulation`
- 数据来源：合成场景参数
- 平台与软件：未明确披露
- 硬件与算力：未明确披露
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：方法链条清晰，但实验仍属于标准数值仿真范畴。

## Introduction 写作素材
- 在空地协同 MEC 中，AoI 与能耗并不是一个可被固定权重永久折中的静态关系。
- 当用户偏好会变化时，系统更需要一组可切换策略，而不是单一点最优解。
- 因而多目标学习比传统加权和方法更贴近实际服务系统。

## Related Work 写作素材
- 既有 AoI-energy 研究常用线性加权，把多目标压扁成单目标。
- 既有 UAV-MEC 强化学习方法常直接求单策略，难以支持动态偏好。
- 该文是 `AoI + 能耗 + Pareto 策略集` 这条线的关键代表。

## 相关系统建模页
- [[计算卸载模型]]
- [[任务队列与时延保障模型]]

## 相关概念与主题页
- [[信息年龄（AoI）]]
- [[高空平台（HAP）]]
- [[多目标强化学习（MORL）]]
- [[任务卸载与资源分配研究主线]]
- [[轨迹优化与协同控制]]

## 来源
- [原文](../raw/markdown/song2024AoIEnergyTradeoff.md)
