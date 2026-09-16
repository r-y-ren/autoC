---
tags: [论文, 多UAV协同, 任务调度, 吞吐最大化]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/zhao2025MultiUAVCooperativeTask.md
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
  - Windows 10 21H2
frameworks:
  - TF-PPO
  - MOGS
datasets: []
hardware_stack:
  - NVIDIA RTX 3090 GPU
  - Intel Xeon Gold 6226R CPU
artifact_availability: unknown
reproducibility_level: medium
---

# Zhao2025_动态环境中的多UAV协同任务调度

## 单行摘要
论文把动态环境中的多 UAV 协作计算统一写成吞吐最大化问题，并通过 TF-PPO 优化 UAV 协同部署，再用 Many-to-One Gale-Shapley 机制处理异构任务与 UAV 的快速关联。

## 题目驱动研究框架
- 研究场景：多架 UAV 在动态环境中为移动设备提供协同计算服务。
- 研究对象：执行协同机动的 UAV、持续移动的 MD 以及随机到达的异构任务。
- 核心问题：任务集和用户位置持续变化时，既要保持 UAV 协同覆盖，又要快速完成任务关联与调度。
- 标题承诺的方法：a multi-UAV cooperative task scheduling in dynamic environments。
- 期望效果：提升系统吞吐、已完成任务数并降低任务处理时延。

## Algorithm Design 快照
作者先把完成任务数、时延和吞吐统一压到一个核心目标上：吞吐最大化。随后把问题拆成两部分求：一部分由 TF-PPO 学习多 UAV 的协同部署与动作选择，另一部分由改造后的 Gale-Shapley 机制 MOGS 近似求解动态任务-无人机关联。这样就把“怎么飞”和“接谁的任务”分层耦合起来，尤其适合任务到达和用户移动都很强随机的环境。

## 图1系统框架草案
- 环境层：移动设备在连续时间内产生依赖任务和独立任务。
- 协同层：多 UAV 调整部署位置与协作关系以覆盖更多设备。
- 调度层：MOGS 完成任务与 UAV 的快速多对一匹配。
- 学习层：TF-PPO 通过任务因子化改善多 UAV 协作训练稳定性。
- 目标层：吞吐最大化。

## System Model
### 1. 动态计算服务场景
- UAV 为移动设备提供计算服务，用户位置与任务属性持续变化。
- 系统同时存在依赖任务和独立任务。

### 2. 双层决策结构
- 上层是 UAV 协同部署与动作选择。
- 下层是任务与 UAV 的多对一关联调度。

### 3. 核心指标
- 吞吐量。
- 完成任务数。
- 任务完成时延。

## Algorithm Design 详解
### 1. TF-PPO
- 在 PPO 上叠加 task factorization 网络，提高多 UAV 全局动作选择质量。
- 目标是在动态环境中保持更稳定的协同性能。

### 2. MOGS
- 基于 Gale-Shapley 稳定匹配思想改造而来。
- 支持多对一关联，且不需要额外中心服务器介入。

### 3. 研究意义
- 这篇论文把“动态任务集 + 动态用户位置 + 多 UAV 协同”一起考虑。
- 对写“连续时间环境中的空中计算调度”很有价值。

## 实验证据卡片
- 验证类型：`simulation`
- 数据来源：合成动态移动设备和任务流
- 平台与软件：`Windows 10 21H2`
- 硬件与算力：`RTX 3090 GPU`、`Intel Xeon Gold 6226R CPU`
- 方法组件：`TF-PPO`、`MOGS`
- 对比对象：不同协同与调度策略
- 开源情况：未说明
- 复现判断：`medium`
- 缺失信息：未给出标准化代码与统一环境封装

## Introduction 写作素材
- 动态环境中的 UAV 协同计算不能再依赖静态用户和固定任务集假设。
- 协同部署和任务调度必须被统一考虑，否则任何一端都会成为系统瓶颈。
- 这篇论文适合支撑“空中计算研究正从静态时隙优化走向连续时间动态调度”的引言论述。

## Related Work 写作素材
- 轨迹优化研究常忽略任务异质性。
- 任务调度研究又常把 UAV 部署当成已知条件。
- 这篇论文通过 TF-PPO + MOGS 把两类问题真正联起来。

## 相关系统建模页
- [[计算卸载模型]]
- [[无人机能耗模型]]

## 相关概念与主题页
- [[多无人机协同]]
- [[任务卸载与资源分配研究主线]]
- [[近端策略优化（PPO）]]
- [[稳定匹配]]

## 来源
- [原文](../raw/markdown/zhao2025MultiUAVCooperativeTask.md)
