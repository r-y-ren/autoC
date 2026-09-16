---
tags: [论文, UAV辅助MEC, 轨迹优化, 任务卸载, 缓存, 迁移]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/zhao2025JointOptimizationTrajectory.md
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
  - MATLAB R2021a
  - Pycharm 2023.2.3
frameworks:
  - Lyapunov optimization
  - BCD
  - SDR
  - CVX
  - YALMIP
  - MOSEK
  - PyTorch 1.12.0
datasets: []
hardware_stack:
  - Intel i7-12700F 2.1 GHz
  - 32 GB RAM
artifact_availability: unknown
reproducibility_level: medium
---

# Zhao2025 轨迹卸载缓存与迁移联合优化的UAV辅助MEC

## 单行摘要
论文在 UAV-assisted MEC 中把轨迹、卸载、任务缓存和任务迁移写进同一 Lyapunov 在线控制框架，通过 BCD 联合优化逐时隙调度与 UAV 部署。

## 题目驱动研究框架
- 研究场景：基础设施缺失区域中的多 UAV 协同 MEC 服务系统。
- 研究对象：移动用户、多架 UAV、任务队列、缓存队列、迁移链路和带宽分配。
- 核心问题：只优化轨迹或只优化卸载都无法解释任务在多时隙、多 UAV 间的持续处理过程。
- 标题承诺的方法：joint optimization of trajectory, offloading, caching, and migration。
- 期望效果：提升系统吞吐、降低执行时间，并让队列在长期上保持稳定。
- 标题与正文的偏差：正文亮点在于把 task caching 明确提出为和 content caching 不同的一类主变量。

## Algorithm Design 快照
论文研究多 UAV 辅助 MEC 中的在线服务组织问题。用户任务会随位置变化跨时隙进入不同 UAV 覆盖区，因此系统必须同时决定任务最初卸载到哪台 UAV、任务是否缓存等待后续处理、何时迁移给其他 UAV，以及 UAV 是否移动到任务热点区域。难点在于这些决策会共同影响系统吞吐、队列长度和调度成本。为此，作者使用 Lyapunov 优化把长期随机问题分解为逐时隙优化问题，再用 BCD 在 UAV 部署、用户关联、任务卸载、调度和迁移带宽分配之间迭代求解。

## 图1系统框架草案
- 系统实体：移动用户、多 UAV、缓存队列、迁移链路、无线回传带宽。
- 任务/数据流：用户产生任务 -> 卸载至某 UAV -> 直接执行/缓存等待/迁移到其他 UAV -> 完成处理。
- 控制/优化变量：UAV 部署、用户关联、任务卸载比例、任务缓存决策、迁移带宽分配。
- 约束来源：系统队列稳定、计算资源、带宽资源、迁移链路时延、缓存能力。
- 画图提醒：建议明确画出“offloading / caching / migration / computing”四个状态转换，而不是只画一个卸载箭头。

## System Model
- 多个移动用户在不同时隙生成任务，多架 UAV 提供机动边缘计算服务。
- 任务可以被直接执行、缓存等待未来时隙处理，或迁移到另一台 UAV。
- UAV 位置会随任务分布变化而重新部署，系统目标是长期提升吞吐并降低调度成本。
- Lyapunov 框架通过队列稳定项与收益项平衡长期性能与瞬时拥塞。

## Algorithm Design 详解
- 第一步：将长期随机优化问题拆成 one-slot per-slot 问题。
- 第二步：初始化 UAV 部署与用户关联，并通过 task-scheduling-oriented deployment 更新 UAV 位置。
- 第三步：设计任务卸载与调度策略，把 scheduling QCQP 通过 SDR 和 rounding 处理。
- 第四步：为迁移链路分配带宽，并在缓存、迁移和计算三者之间形成稳定的长期调度机制。
- 论文意义：这篇工作把[[任务迁移]]从辅助机制推进成主决策变量，并正式把[[任务缓存]]接入 UAV-MEC 主线。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成移动用户与多 UAV MEC 场景
- 平台与软件：`MATLAB R2021a`、`CVX`、`YALMIP`、`MOSEK`、`Pycharm 2023.2.3`、`PyTorch 1.12.0`
- 硬件与算力：`Intel i7-12700F 2.1 GHz`、`32 GB RAM`
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文完整给出求解器与开发环境配置，是当前 Batch_03 中实验栈披露最完整的论文之一。

## Introduction 写作素材
- UAV-assisted MEC 中真正困难的不是“这一时刻任务交给谁”，而是“任务在多时隙、多 UAV 之间如何被持续服务”。
- 内容缓存并不能替代任务缓存，因为待处理任务本身会占用计算和调度资源。
- 这篇论文适合支撑“UAV-MEC 正从一次性卸载走向面向任务生命周期的服务组织”的引言判断。

## Related Work 写作素材
- 与只做轨迹+卸载的研究相比，本文把 caching 和 migration 明确拉入主问题。
- 与传统内容缓存研究相比，本文强调的是 task caching 而非 content caching。
- 与纯 RL 在线调度相比，本文用 Lyapunov + BCD 构造可解释的长期稳定性控制框架。

## 相关系统建模页
- [[计算卸载模型]]
- [[任务队列与时延保障模型]]

## 相关概念与主题页
- [[任务迁移]]
- [[任务缓存]]
- [[边缘缓存]]
- [[任务卸载与资源分配研究主线]]
- [[轨迹优化与协同控制]]

## 来源
- [原文](../raw/markdown/zhao2025JointOptimizationTrajectory.md)
