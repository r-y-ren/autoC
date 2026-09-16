---
tags: [论文, 空中计算, 隐私保护, 数据存储, 数据共享]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/wang2024LSPSSConstructingLightweight.md
venue_tier: CCF-A
literature_type: system
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - system_model
  - related_work
validation_type:
  - trace_driven
data_origin:
  - unknown
platforms: []
frameworks:
  - ASPE
  - IPC
  - G-tree
  - Merkle tree
hardware_stack: []
datasets: []
artifact_availability: unknown
reproducibility_level: medium
---

# Wang2024_LSPSS空中计算中的轻量级隐私存储与共享

## 单行摘要
论文面向空中计算中的低空平台数据共享需求，提出 `LSPSS` 方案，通过多维数据转换、ASPE/IPC 加密索引和 G-tree + Merkle tree 完整性验证，实现轻量级隐私存储与范围查询。

## 题目驱动研究框架
- 研究场景：6G 空中计算框架下，LAC 平台承担数据收集与存储任务。
- 研究对象：UAV、区域服务器、区域管理员、KGA、LAC 平台与用户。
- 核心问题：长距离传输和多实体协作下，多维敏感数据难以安全共享。
- 标题承诺的方法：构建轻量级且安全的私有数据存储与共享方案。
- 期望效果：在不暴露隐私的条件下支持多维范围查询与结果完整性验证。

## Algorithm Design 快照
这篇论文更像一套“空中计算数据基础设施方案”，而不是单纯的加密算法。作者围绕位置数据和日志数据两类多维数据，设计转换、索引、加密和结果验证全链路，使 UAV 采集的数据在 LAC 场景中可以被安全检索和可信共享。

## 图1系统框架草案
- 架构层：IoT、地面计算、LAC、HAC、卫星计算五层空中计算架构。
- 数据层：位置数据与日志数据被转换为可安全匹配的多维向量。
- 索引层：为位置和日志分别构建安全索引。
- 验证层：结合 G-tree 与 Merkle tree 做结果完整性验证。
- 服务层：用户发起密文范围查询并解密结果。

## System Model
### 1. 六实体系统模型
- UAV 负责采集并上传数据。
- 区域服务器和 LAC 平台分别承担位置索引和日志索引服务。
- 区域管理员、KGA 与用户共同组成可信控制与查询方。

### 2. 数据对象
- UAV 位置数据。
- 带多维属性的 UAV 日志文件。

### 3. 安全目标
- 多维数据范围查询。
- 单维隐私与 query unlinkability。
- 查询结果的完整性验证。

## Algorithm Design 详解
### 1. 多维数据转换
- 针对位置特征和日志特征分别设计数据转换方法。
- 把原始多维数据重写为便于 IPC 匹配和加密存储的向量形式。

### 2. 轻量级密文索引
- 基于 `ASPE` 与 `IPC` 设计多维密文索引。
- 通过置换与扰动式矩阵加密降低多维范围查询的隐私泄露风险。

### 3. 结果验证
- 利用 `G-tree` 与 `Merkle tree` 组合支持查询完整性验证。
- 论文强调在 `25000` 个文件规模下，结果验证约 `400 ms`，查询约 `2.5 s`。

## 实验证据卡片
- 验证类型：`trace_driven`
- 数据来源：真实数据库，但未明确给出公开数据名
- 平台与软件：未明确说明
- 方法组件：`ASPE`、`IPC`、`G-tree`、`Merkle tree`
- 评测指标：查询时延、结果验证时延、安全性与可用性
- 对比对象：现有隐私范围查询与多维索引方案
- 开源情况：未说明
- 复现判断：`medium`
- 缺失信息：未公开平台栈、数据集名称和实现代码

## Introduction 写作素材
- 空中计算不只需要算力和链路，还需要可信的数据存储与共享基础设施。
- 相比单纯链上或重密码学方案，资源受限的低空平台更需要轻量级多维密文查询机制。
- 这篇论文很适合支撑“UAC 研究应从任务优化延伸到数据基础设施”的论述。

## Related Work 写作素材
- 现有区块链、全同态或差分隐私路线在资源受限空中平台上往往代价较高。
- 传统多维范围查询大多面向三方模型，不直接适配空中计算多层架构。
- 这篇论文把空中计算框架、轻量级密文索引和结果可验证性结合起来，形成了更系统的方案。

## 相关系统建模页
- 当前更偏隐私存储与共享协议，尚未形成稳定的专用系统建模页。

## 相关概念与主题页
- [[安全隐私共享]]
- [[空中计算]]
- [[无人机即服务（DaaS）与空中计算的关系]]
- [[安全与服务保障]]
- [[任务卸载与资源分配研究主线]]

## 来源
- [原文](../raw/markdown/wang2024LSPSSConstructingLightweight.md)
