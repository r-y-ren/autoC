---
tags: [论文, 多目标优化, 多UAV辅助MEC, 任务卸载, 轨迹控制]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/sun2024MultiobjectiveOptimizationMultiUAVassisted.md
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
  - MATLAB R2022b
frameworks:
  - JTORATC
  - CVX
  - distributed splitting
  - threshold rounding
  - SCA
  - KKT
datasets: []
hardware_stack:
  - Intel Core i7-8750H CPU
  - 8 GB RAM
artifact_availability: unknown
reproducibility_level: medium
---

# Sun2024 多UAV辅助MEC多目标优化

## 单行摘要
论文把多 UAV-assisted MEC 中的任务完成时延、UAV 总能耗和卸载任务总数统一为多目标优化问题，并提出 JTORATC，通过任务卸载、计算资源分配与 UAV 轨迹控制三段协同求解。

## 题目驱动研究框架
- 研究场景：多用户、资源受限的多 UAV 辅助 MEC 系统。
- 研究对象：终端用户、多架 UAV、卸载决策、计算资源与 UAV 轨迹。
- 核心问题：只优化单一目标会牺牲其他关键指标，尤其在密集场景里时延、能耗和可服务任务数天然冲突。
- 标题承诺的方法：multi-objective optimization for multi-UAV-assisted MEC。
- 期望效果：在低复杂度前提下找到较好的三目标折中解。
- 标题与正文的偏差：正文的核心不是通用多目标求解，而是如何把混合整数非凸问题拆成三个可控子问题并维持可行性。

## Algorithm Design 快照
论文研究多 UAV 辅助 MEC 中的联合决策问题，其中每个用户既关心任务是否能及时完成，也影响 UAV 的推进与计算能耗，而系统又希望尽可能服务更多卸载任务。难点在于三个目标互相冲突且决策变量混合离散与连续。为此，作者提出 JTORATC，把原问题拆为任务卸载、计算资源分配和 UAV 轨迹控制三类子问题：卸载子问题通过 distributed splitting 与 threshold rounding 处理二进制变量，资源分配子问题借助 KKT 条件求解，轨迹控制子问题用 SCA 逐步凸化。这样系统在复杂度可控的情况下获得多目标折中解，并能适配不同负载强度。

## 图1系统框架草案
- 系统实体：多个用户、多架 UAV、本地计算与空中 MEC 节点。
- 任务/数据流：用户在本地或向某架 UAV 卸载任务，UAV 边飞行边提供计算服务。
- 控制/优化变量：卸载二进制变量、UAV 计算频率、轨迹位置、任务执行时间。
- 约束来源：用户截止期、UAV 能量预算、单时隙服务能力、飞行轨迹可行域。
- 画图提醒：建议把三目标在图中直接并列写出，并用三块优化模块对应 JTORATC 的三个子问题。

## System Model
- 用户任务可以本地执行，也可以卸载给多架 UAV 中的某一台处理。
- UAV 的能量同时消耗在飞行推进和计算服务上，因此轨迹与资源分配紧密耦合。
- 系统目标不是单纯最小时延，而是在时延、能耗、卸载数量之间做折中。
- 原问题被写成混合整数非线性规划，且属于 NP-hard。

## Algorithm Design 详解
- JTORATC 先固定其余变量求卸载决策，通过 distributed splitting 将离散变量松弛，再用 threshold rounding 恢复二进制结构。
- 计算资源分配部分利用 KKT 条件获得每个 UAV 的最优资源配置。
- 轨迹控制部分通过 SCA 把非凸约束逐步逼近为可求解凸形式。
- 该文的价值在于给出了一条“多目标 UAV-MEC 低复杂度工程求解”路线，而不是只强调理论最优性。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成多 UAV、多用户任务场景
- 平台与软件：`MATLAB R2022b`、`CVX`
- 硬件与算力：`Intel Core i7-8750H CPU`、`8 GB RAM`
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文清楚披露了仿真平台和主要求解工具，适合作为多目标 UAV-MEC 的数值基线。

## Introduction 写作素材
- 多 UAV MEC 的设计往往天然是多目标问题，因为“服务更多任务”和“少耗能、低时延”不会自动一致。
- 如果只追求低时延，UAV 轨迹和能耗可能会快速失衡。
- 因而多目标优化不仅是性能修饰，而是系统设计的必要视角。

## Related Work 写作素材
- 单目标 UAV-MEC 研究已经很多，但少数工作显式把时延、能耗和服务数量放在同一目标体系下。
- 相较于纯 DRL 或纯群智能方法，该文更强调可解释的分解式优化流程。
- 它适合作为“低复杂度多目标联合优化”代表作进入综述。

## 相关系统建模页
- [[计算卸载模型]]
- [[无人机能耗模型]]

## 相关概念与主题页
- [[任务卸载]]
- [[资源分配]]
- [[轨迹优化]]
- [[任务卸载与资源分配研究主线]]
- [[UAC研究路线图]]

## 来源
- [原文](../raw/markdown/sun2024MultiobjectiveOptimizationMultiUAVassisted.md)
