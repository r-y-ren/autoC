---
tags: [论文, 任务卸载, UAV辅助MEC, THz, IRS辅助通信]
created: 2026-04-10
updated: 2026-04-10
sources:
  - ../raw/markdown/wu2025TwostageDeepEnergy.md
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
  - IOPO
  - OPPO
  - DNN
datasets: []
hardware_stack: []
artifact_availability: open
reproducibility_level: medium
---

# Wu2025_IOPO面向THz多UAV-MEC的IRS辅助卸载优化

## 单行摘要
论文面向 THz 多用户多 UAV MEC 场景，引入 IRS 改善传播环境，并提出两阶段深度学习框架 `IOPO`，联合优化二元任务卸载矩阵与 IRS 相位，以降低系统能耗并满足时延约束。

## 题目驱动研究框架
- 研究场景：THz 通信下的多用户多 UAV MEC，链路容易受阻、传播衰减强。
- 研究对象：用户、多个 UAV、单个 IRS、THz 传输链路。
- 核心问题：如何在 IRS 相位与卸载矩阵耦合的条件下生成低能耗且不过期的卸载决策。
- 标题承诺的方法：two-stage deep learning energy optimization。
- 期望效果：让多 UAV MEC 在 THz+IRS 环境中获得更低能耗和更好可行解质量。

## Algorithm Design 快照
作者没有采用“一次性同时预测卸载和相位”的单阶段策略，而是提出两阶段 `IOPO`。第一阶段生成较优二元卸载决策，第二阶段在此基础上进一步优化 IRS 相位。与此同时，`OPPO` 会持续搜索顺序保持的更优卸载分配，使模型在迭代中不断逼近最优并减少过期用户。

## 图1系统框架草案
- 实体：多用户、多 UAV、单 IRS、THz 链路。
- 决策：二元卸载矩阵、IRS 相位。
- 目标：最小化用户和 UAV 的总能耗，同时满足 no-overdue 约束。
- 画图提醒：把“直接链路 + IRS 重定向链路 + 卸载矩阵”三层一起画出。

## System Model
- 用户任务可在本地执行，也可卸载到多个 UAV 中的某一个。
- IRS 作为中间传播控制层，辅助用户到 UAV 的 THz 上传。
- 系统同时建模本地计算能耗、上传能耗和 UAV 处理能耗。
- 约束重点不是单纯速率，而是每个用户任务都不能超过可接受时延。

## Algorithm Design 详解
- 第一步：建立多用户多 UAV MEC 系统的二元卸载矩阵模型。
- 第二步：把 IRS 相位配置与卸载矩阵联合写成混合整数非线性问题。
- 第三步：设计 `IOPO` 两阶段框架，先找卸载、再调相位。
- 第四步：利用 `OPPO` 在迭代过程中持续挖掘更优卸载方案，提高解质量与收敛速度。
- 第五步：比较 LOCAL、GREEDY、DDPG 等基线，验证能耗与准最优性。

## 实验证据卡片
- 验证类型：`simulation`
- 数据来源：合成场景参数
- 平台与软件：未明确说明
- 方法组件：`IOPO`、`OPPO`、DNN
- 开源情况：`open`
- 复现判断：`medium`
- 缺失信息：未给出统一硬件环境与完整工程脚本说明

## Introduction 写作素材
- THz 场景下的 MEC 卸载不能只继承 5G 设定，因为遮挡与传播损耗会直接改变卸载可行域。
- IRS 把传播控制变量引入后，卸载问题从资源分配升级为“卸载 + 相位”耦合问题。

## Related Work 写作素材
- 与只做 THz 通信增强的工作相比，本文明确建模了 MEC 卸载。
- 与单阶段学习不同，本文强调两阶段求解和顺序保持搜索机制。

## 相关系统建模页
- [[计算卸载模型]]
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[THz-IRS辅助卸载]]
- [[任务卸载与资源分配研究主线]]
- [[空中通信与协同传输]]

## 来源
- [原文](../raw/markdown/wu2025TwostageDeepEnergy.md)
