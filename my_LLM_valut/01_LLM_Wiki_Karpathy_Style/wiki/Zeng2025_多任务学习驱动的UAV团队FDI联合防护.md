---
tags: [论文, UAV团队安全, FDI攻击, 多任务学习, 真实飞行]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/zeng2025JointSecureMechanism.md
venue_tier: CCF-A
literature_type: system
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - methodology
  - engineering_context
validation_type:
  - simulation
  - field_test
data_origin:
  - mixed
platforms:
  - Windows 11
frameworks:
  - CNN
  - LSTM
  - multi-task learning
  - experience replay
hardware_stack:
  - AMD Ryzen 7 CPU
  - 16GB RAM
  - NVIDIA GeForce RTX 3060 GPU
  - 3 x DJI Tello Robomaster TT
datasets: []
artifact_availability: unknown
reproducibility_level: medium
---

# Zeng2025_多任务学习驱动的UAV团队FDI联合防护

## 单行摘要
论文面向多 UAV 团队在同时上下行 FDI 攻击下的飞行安全问题，提出融合 `CNN + LSTM + 分层多任务学习` 的联合安全框架，实现攻击检测、定位与控制补偿三任务一体化防护。

## 题目驱动研究框架
- 研究场景：多 UAV 团队沿指定轨迹执行协同任务。
- 研究对象：UAV 团队、GCS、上下行控制与状态链路、FDI 攻击者。
- 核心问题：现有方法多只处理单 UAV 或单一子任务，难以同时完成检测、定位与补偿。
- 标题承诺的方法：joint secure mechanism of multi-task learning。
- 期望效果：在严格攻击假设下仍维持 UAV 团队稳定跟踪目标轨迹。

## Algorithm Design 快照
这篇论文的亮点是把原本分散的“攻击检测、受损部件定位、控制补偿”合并为一个共享时空特征的联合任务。作者不再假设只有传感器或执行器被单独攻击，而是正面处理上下行同时遭受 FDI 的实战场景，并用 experience replay 缓解长时训练的 knowledge decay。

## 图1系统框架草案
- 任务层：GCS 向 UAV 团队下发协同控制目标。
- 威胁层：上下行链路同时遭受 FDI 攻击。
- 特征层：`CNN + LSTM` 联合提取 UAV 团队时空特征。
- 多任务层：同时输出检测、定位和补偿结果。
- 执行层：补偿控制信号驱动 UAV 回归既定轨迹。

## System Model
### 1. 多 UAV 团队模型
- 多架 UAV 通过共享 GCS 沿预定轨迹协同飞行。
- 上行链路传输控制指令，下行链路回传状态数据。

### 2. 攻击模型
- 同时考虑 uplink 与 downlink FDI 攻击。
- 攻击可针对多个 UAV、多个部件持续发生，并可绕过传统 BDD。

### 3. 设计目标
- 检测攻击是否发生。
- 定位受攻击组件。
- 对控制信号进行补偿，维持团队飞行安全。

## Algorithm Design 详解
### 1. 时空特征挖掘
- `CNN` 提取空间关联模式。
- `LSTM` 提取跨时间步演化特征。

### 2. 分层多任务学习
- 共享特征骨干支撑三个子任务联合训练。
- 通过分层结构维持检测、定位、补偿之间的逻辑关联。

### 3. 经验回放式迭代学习
- 借鉴 reinforcement learning 中的 `experience replay`。
- 用迭代学习缓解长期任务中的知识遗忘与性能衰减。

## 实验证据卡片
- 验证类型：`simulation`、`field_test`
- 数据来源：仿真实验 + 真实飞行演示
- 平台与软件：`Windows 11`
- 硬件与算力：`AMD Ryzen 7 CPU`、`16GB RAM`、`NVIDIA GeForce RTX 3060 GPU`
- 飞行平台：`3 x DJI Tello Robomaster TT`
- 方法组件：`CNN`、`LSTM`、`multi-task learning`、`experience replay`
- 评测指标：检测性能、定位性能、偏差面积、补偿效果
- 对比对象：六类基线与既有 observer/learning 防御方法
- 开源情况：未说明
- 复现判断：`medium`
- 缺失信息：未公开训练代码、攻击注入脚本与标注数据

## Introduction 写作素材
- UAV 团队安全问题不能继续停留在“单机 + 单类攻击 + 单一任务”的设定上。
- 当上下行同时遭受 FDI，传统依赖单侧正确信息的防御逻辑会直接失效。
- 这篇论文适合支撑“安全控制必须从单点检测走向团队级联合防护”的研究动机。

## Related Work 写作素材
- 既有 FDI 防御多依赖 Kalman filter、observer 或残差分析。
- 深度学习方案通常聚焦单一检测任务，较少把定位和补偿纳入统一模型。
- 本文把时空特征、多任务学习和真实飞行验证同时带进 UAV 团队安全研究。

## 相关系统建模页
- [[故障与攻击检测模型]]
- [[容错控制与碰撞规避模型]]

## 相关概念与主题页
- [[虚假数据注入攻击（FDI）]]
- [[多无人机协同]]
- [[安全与服务保障]]
- [[轨迹优化与协同控制]]
- [[空中通信与协同传输]]

## 来源
- [原文](../raw/markdown/zeng2025JointSecureMechanism.md)
