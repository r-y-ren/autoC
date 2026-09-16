---
tags: [论文, 内容缓存, 服务放置, 任务卸载, QoE, UAV-MEC]
created: 2026-04-09
updated: 2026-04-09
sources:
  - ../raw/markdown/zhao2025JointContentCaching.md
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
  - Gibbs sampling
  - matching game
  - QoE maximization
hardware_stack: []
datasets: []
artifact_availability: unknown
reproducibility_level: medium
---

# Zhao2025_UAV-MEC中的内容缓存服务放置与任务卸载联合优化

## 单行摘要
论文面向同时存在内容请求和服务请求的 `UAV-enabled MEC` 网络，提出把内容缓存、服务放置和任务卸载一起优化，并用“内容命中率 + 服务时延缩减率”的加权和定义平均 `QoE`。

## 题目驱动研究框架
- 研究场景：带缓存和计算能力的多 UAV-MEC 网络。
- 研究对象：UAV、地面用户、内容库、服务库与任务卸载决策。
- 核心问题：仅优化缓存或仅优化卸载都无法完整刻画系统满足异构请求的能力。
- 标题承诺的方法：联合优化 content caching、service placement 与 task offloading。
- 期望效果：在存储和计算资源受限时尽可能提升系统平均 QoE。

## Algorithm Design 快照
这篇论文很重要的一点是，它把“内容请求”和“服务请求”放进同一网络模型中。也就是说，UAV 不仅要决定缓存哪些文件，还要决定预装哪些服务，并在服务请求到来时协调任务是否本地处理或卸载。作者因此提出以平均 `QoE` 为核心指标，将 `cache hit ratio` 和 `service delay shrinkage ratio` 统一起来，这比单纯时延或能耗更接近真实服务系统目标。

## 图1系统框架草案
- 请求层：用户可能发起内容请求，也可能发起服务请求。
- 资源层：每架 UAV 同时具备存储空间和计算能力。
- 决策层：联合决定内容缓存、服务放置和任务卸载。
- 求解层：缓存/放置由 `Gibbs sampling` 优化，卸载由 `matching game` 优化。
- 目标层：最大化平均 `QoE`。

## System Model
### 1. 异构请求模型
- 内容请求：用户从覆盖范围内缓存了目标内容的 UAV 获取文件。
- 服务请求：用户可本地计算或将多个任务卸载给部署了相应服务的 UAV。

### 2. 缓存与放置模型
- UAV 存储同时容纳内容和服务，两者共享有限存储预算。
- 服务放置决定可执行服务集合，内容缓存决定可直接命中的文件集合。

### 3. QoE 目标
- 用 `content cache hit ratio` 衡量内容请求满足能力。
- 用 `service delay shrinkage ratio` 衡量服务请求加速能力。
- 以两者加权和作为平均 QoE。

## Algorithm Design 详解
### 1. 缓存与放置优化
- 将内容缓存和服务放置写成联合组合优化问题。
- 用 `Gibbs sampling` 迭代寻找高 QoE 的缓存-放置配置。

### 2. 卸载优化
- 对服务请求中的多个独立任务，用 `matching game` 决定是否及向哪架 UAV 卸载。
- 同时考虑 UAV 的 CPU 核心数和计算能量限制。

### 3. 研究意义
- 论文把 `cache + placement + offloading` 三者真正绑成一个系统问题，是服务化 UAV-MEC 很典型的骨架文献。

## 实验证据卡片
- 验证类型：`simulation`
- 数据来源：合成 UAV 与 UE 空间部署及异构请求场景
- 平台与软件：未明确说明
- 方法组件：`Gibbs sampling`、`matching game`、`QoE maximization`
- 评测指标：平均 `QoE`、内容命中率、服务时延缩减率
- 对比对象：贪心缓存、随机方案、上界穷举等基线
- 开源情况：未说明
- 复现判断：`medium`
- 缺失信息：未披露完整代码和平台配置

## Introduction 写作素材
- UAV-MEC 系统已经不只是“算力卸载”，而是在同时处理内容分发和服务执行。
- 若只优化缓存或只优化卸载，都会丢失系统对异构请求的真实服务能力。
- 这篇论文非常适合支撑“从任务卸载走向服务组织”的写作主线。

## Related Work 写作素材
- 既有 MEC 工作常把任务卸载与服务放置分开。
- 既有 UAV 缓存工作多聚焦内容而非服务执行。
- 本文通过统一 `QoE` 指标把内容与服务两个视角真正并到一起。

## 相关系统建模页
- [[计算卸载模型]]
- [[服务放置模型]]
- [[编码缓存与内容命中模型]]

## 相关概念与主题页
- [[内容缓存]]
- [[服务放置]]
- [[任务卸载]]
- [[任务卸载与资源分配研究主线]]
- [[空中通信与协同传输]]

## 来源
- [原文](../raw/markdown/zhao2025JointContentCaching.md)
