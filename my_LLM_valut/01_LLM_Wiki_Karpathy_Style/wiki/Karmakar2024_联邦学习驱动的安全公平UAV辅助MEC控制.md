---
tags: [论文, 联邦学习, 公平性优化, 安全MEC, 3D轨迹]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/karmakar2024NovelFederatedLearningBased.md
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
  - NS-3.35
frameworks: []
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---


# Karmakar2024 联邦学习驱动的安全公平UAV辅助MEC控制

## 单行摘要
论文提出 FairLearn，通过联邦学习和 3D 轨迹-功率联合控制，在存在窃听者的 UAV-MEC 中提升保密速率公平性。

## 题目驱动研究框架
- 研究场景：存在窃听威胁的 UAV 辅助 MEC 服务网络。
- 研究对象：执行任务的合法 UAV、干扰 UAV、移动用户、窃听者、FL 协作学习框架。
- 核心问题：如何在保证安全的同时，让不同用户获得更公平的保密 MEC 服务机会。
- 标题承诺的方法：federated learning-based smart power and 3D trajectory control for fairness optimization。
- 期望效果：最大化安全服务公平性，同时改善吞吐、包丢失和轨迹适应性。
- 标题与正文的偏差：正文真正的特色是“联邦学习 + RL 生成数据 + 双 UAV 角色分工”的系统设计。

## Algorithm Design 快照
论文针对 UAV 辅助 MEC 中“安全性、公平性和轨迹控制”三者难以兼顾的问题，设计了 FairLearn 框架。系统由成对 UAV 组成，一架负责执行用户卸载任务，另一架作为干扰机压制窃听者。算法上，作者首先用 RL 模块在不同场景下生成训练数据，再用 DNN 模块预测 3D 轨迹、功率和调度时间，并通过联邦学习在多个 UAV 之间协同更新模型参数。最终方法在 NS-3 仿真中显著提升保密速率、平均吞吐和公平性指标。

## 图1系统框架草案
- 系统实体：合法 UAV、干扰 UAV、移动 GUs、窃听者、地面站。
- 任务/数据流：用户向合法 UAV 卸载任务，干扰 UAV 对窃听链路施加抑制，联邦学习聚合多 UAV 训练结果。
- 控制/优化变量：3D 轨迹、发射功率、调度时间、联邦学习参数更新。
- 约束来源：安全速率、公平性目标、移动性、功率预算与时隙结构。
- 画图提醒：图里建议画成“安全服务面”和“联邦学习面”两个并行层。

## System Model
- 系统使用“合法 UAV + 干扰 UAV”的成对结构，将执行和安全保护解耦。
- 移动用户和窃听者同时存在，导致轨迹、功率与安全速率高度耦合。
- 公平性通过长期保密速率或吞吐公平指标来刻画，而非只追求总和吞吐。
- 训练样本由 RL 在线生成，再通过联邦学习在不同 UAV 间共享知识。

## Algorithm Design 详解
- 第一步用 RL 模块在多样网络状态下生成用于监督训练的数据集。
- 第二步训练 DNN 模块预测轨迹、功率和调度时间。
- 第三步通过联邦学习聚合各 UAV 的局部模型，提高泛化和适应性。
- 第四步在 NS-3 中比较 FairLearn 与多种安全 MEC 基线的保密速率与公平性。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成安全 UAV-MEC 场景
- 平台与软件：`NS-3.35`
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：系统假设和指标定义明确，但尚未给出真实部署或公开代码证据。

## Introduction 写作素材
- UAV-MEC 中的“公平”不能只看吞吐或时延，还要看不同用户能否公平获得安全服务。
- 安全控制与轨迹控制并不是两个独立层次，窃听威胁会反过来改变最优飞行行为。
- 这篇论文适合支撑“从性能最优走向安全公平服务”的写作过渡。

## Related Work 写作素材
- 与传统安全 MEC 工作相比，本文将公平性显式纳入目标。
- 与只做 2D 轨迹控制的工作不同，本文面向 3D 轨迹与功率联合设计。
- 与集中训练方式不同，本文用联邦学习整合多 UAV 的经验。

## 相关系统建模页
- [[计算卸载模型]]
- [[信道与通信速率模型]]
- [[无人机能耗模型]]

## 相关概念与主题页
- [[联邦学习]]
- [[公平性优化]]
- [[任务卸载与资源分配研究主线]]
- [[安全与服务保障]]

## 来源
- [原文](../raw/markdown/karmakar2024NovelFederatedLearningBased.md)
