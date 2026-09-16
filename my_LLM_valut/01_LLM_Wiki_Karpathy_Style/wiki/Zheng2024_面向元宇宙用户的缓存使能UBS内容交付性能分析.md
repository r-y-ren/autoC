---
tags: [论文, 元宇宙, 内容交付, 缓存, 无人机基站, 性能分析]
created: 2026-04-09
updated: 2026-04-09
sources:
  - ../raw/markdown/zheng2024ContentDeliveryPerformance.md
venue_tier: CCF-A
literature_type: theory
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - methodology
  - related_work
validation_type:
  - theory
  - simulation
data_origin:
  - synthetic
platforms:
  - MATLAB
frameworks:
  - MHCPP
  - BPP
  - probabilistic caching
  - Monte Carlo
hardware_stack: []
datasets: []
artifact_availability: unknown
reproducibility_level: medium
---

# Zheng2024_面向元宇宙用户的缓存使能UBS内容交付性能分析

## 单行摘要
论文针对时延敏感的元宇宙用户，构建缓存使能 `UBS-assisted` 蜂窝网络的解析模型，从内容交付成功概率和平均内容交付时延两个维度评估 UAV 基站部署、缓存命中和关联策略对系统性能的影响。

## 题目驱动研究框架
- 研究场景：缓存使能的 UAV 基站辅助蜂窝网络服务元宇宙用户。
- 研究对象：`MBSs`、`UBSs`、时延敏感用户、缓存内容库。
- 核心问题：元宇宙业务对时延更敏感，传统最近基站关联无法充分利用 UAV 缓存优势。
- 标题承诺的方法：分析 content delivery performance。
- 期望效果：给出成功概率和平均时延的理论界，并指导 `UBS` 高度和数量部署。

## Algorithm Design 快照
这篇论文不直接做控制算法，而是先把 `cache hit` 和 `BS association` 写成解析概率模型，再从理论上解释 UAV 缓存基站为何能帮助元宇宙内容交付。作者的关键处理是：在 `cache miss` 和 `cache hit` 两种情况下采用不同的关联逻辑，并用 `MHCPP` 更真实地建模地面宏基站的排斥分布，使结果更接近实际蜂窝部署。

## 图1系统框架草案
- 地面层：`MBSs` 通过光纤接入核心网并可提供全部内容。
- 空中层：`UBSs` 近用户部署并缓存部分热门内容。
- 请求层：元宇宙用户发起对时延敏感的内容请求。
- 关联层：在 cache hit / miss 情况下采取不同 BS 关联策略。
- 评估层：分析成功概率和平均交付时延。

## System Model
### 1. 空地缓存网络模型
- `MBS` 位置服从 `MHCPP`，`UBS` 位置服从 `BPP`。
- `UBS` 采用概率缓存策略，能直接命中部分热门内容。

### 2. 关联策略
- `cache miss`：用户仅关联最近 `MBS`。
- `cache hit`：用户按最强平均接收功率在 `MBS/LBS/NBS` 间选择关联对象。

### 3. 性能指标
- 内容交付成功概率。
- 平均内容交付时延。

## Algorithm Design 详解
### 1. 解析建模
- 推导不同类型基站的关联概率、服务距离分布和 `SINR` 表达式。
- 给出内容交付成功概率的下界和平均内容交付时延的上界。

### 2. 缓存与部署分析
- 研究 `UBS` 高度、数量、缓存容量和 Zipf 热度参数的影响。
- 识别最优 UAV 高度和最优 `UBS` 数量。

### 3. 研究意义
- 论文把“空中缓存是否真的改善用户体验”从经验判断推进成可解析量化问题，很适合做内容交付方向的理论锚点。

## 实验证据卡片
- 验证类型：`theory`、`simulation`
- 数据来源：合成元宇宙内容请求与 UAV 基站部署场景
- 平台与软件：`MATLAB`
- 方法组件：`MHCPP`、`BPP`、`probabilistic caching`、`Monte Carlo`
- 评测指标：内容交付成功概率、平均内容交付时延
- 对比对象：不同关联策略与系统参数设置
- 开源情况：未说明
- 复现判断：`medium`
- 缺失信息：未披露完整仿真代码与参数生成脚本

## Introduction 写作素材
- 元宇宙内容交付比传统内容业务更强调低时延和近用户分发。
- UAV 基站的真正优势不仅是 LoS 传播，还包括把内容缓存搬到更靠近用户的位置。
- 这篇论文适合支撑“缓存 UAV 基站能否真正改善人本交互体验”的写作问题。

## Related Work 写作素材
- 既有 UAV 缓存网络多关注一般用户而非时延敏感元宇宙用户。
- 既有内容交付分析往往采用更理想化的地面基站空间分布模型。
- 本文的特色在于同时考虑更真实的 `MHCPP` 和 `cache hit` 驱动的关联策略。

## 相关系统建模页
- [[服务放置模型]]
- [[编码缓存与内容命中模型]]

## 相关概念与主题页
- [[内容交付性能]]
- [[内容缓存]]
- [[元宇宙内容交付]]
- [[空中通信与协同传输]]
- [[安全与服务保障]]

## 来源
- [原文](../raw/markdown/zheng2024ContentDeliveryPerformance.md)
