---
tags:
  - 论文
  - 协同计算
  - UAV群
  - 协同推理
  - ASAP
created: 2026-04-10
updated: 2026-04-10
sources:
  - ../raw/markdown/sun2024AllskyAutonomousComputing.md
venue_tier: CCF-A
literature_type: system
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - engineering_context
  - system_model
validation_type:
  - prototype
  - field_test
data_origin:
  - self_collected
platforms: []
frameworks:
  - ASAP
  - elastic scheduler
  - inference performance predictor
  - adaptive compressor
  - TensorRT
hardware_stack:
  - 24 airborne computers
  - 5 real-world quadrotor UAVs
  - NVIDIA Jetson Nano
  - NVIDIA Jetson TX2
  - NVIDIA Jetson Xavier NX
  - NVIDIA RTX 3060
datasets: []
artifact_availability: open
reproducibility_level: high
---

# Sun2024_ASAP无人机群全空域自主协同计算

## 单行摘要
论文提出 `ASAP` 全空域自主协同计算系统，让 UAV 群在空中完成“边传边算”的协同推理，通过弹性任务调度、推理时延预测和自适应压缩，在不依赖地面基站的情况下同时维持低时延与高精度。

## 题目驱动研究框架
- 研究场景：灾害检测、搜救和矿区探测等基站受损或条件恶劣的 UAV 群作业环境。
- 研究对象：任务 UAV、通信中继 UAV、机载计算节点和深度学习推理任务。
- 核心问题：机载单机推理算力不足，而原始数据回传地面又会造成高传输时延，如何让 UAV 群自身形成可弹性重构的协同计算系统。
- 标题承诺的方法：all-sky autonomous computing in UAV swarm。
- 期望效果：在空中自治地完成高精度低时延推理，并在部分 UAV 不可用时继续稳定运行。
- 标题与正文的偏差：标题强调 “all-sky autonomous computing”，正文真正贡献是“架构 + 调度 + 预测 + 压缩”的成套系统实现。

## Algorithm Design 快照
论文不是做传统的任务卸载，而是构造了一个 UAV 群原生的协同计算架构。系统把 DL 任务在集群层和集群内两层切分，用弹性调度器根据 UAV 可用性动态重排计算分配，再用轻量级推理性能预测器快速估计执行代价，最后通过自适应中间数据压缩器缓解机间链路瓶颈。这样，UAV 群可以在空中边传边算，而不是要么压缩模型单机跑、要么把原始数据送回地面。

## 图1系统框架草案
- 集群层：按 UAV 群层级结构组织任务 UAV 与中继 UAV。
- 计算层：模型分段与数据分块在不同 UAV 之间分配。
- 控制层：弹性调度器根据可用 UAV 集实时重构任务分配。
- 支撑层：推理性能预测器 + 机间自适应压缩器。
- 对比层：地面回传方案、模型压缩方案和 ASAP 自治协同方案对照。

## System Model
- 论文面向多 UAV 集群中的协同推理问题，任务数据由机载感知负载产生。
- 单机 UAV 在算力、内存和能耗上都无法稳定承载高精度深度模型。
- 地面站回传路径在灾害场景中常不可用，因此系统将协同计算能力上移到空中。
- 关键设计变量包括任务分段方式、UAV 任务映射、机间数据压缩比例和故障后的重调度策略。

## Algorithm Design 详解
- 第一步：提出 UAV 群原生协同计算架构，同时考虑群层级结构和 DL 推理执行特征。
- 第二步：设计弹性调度器，在集群间和集群内两层做任务分配，并在 UAV 不可用时在线更新。
- 第三步：构建轻量化推理性能预测器，把复杂模型时延估计拆成算子级预测与细粒度修正。
- 第四步：设计机间自适应压缩器，依据链路带宽变化调整中间数据压缩比例。
- 第五步：在真实 UAV 群和大量机载计算节点上进行系统验证，体现其工程可行性。

## 实验证据卡片
- 验证类型：`prototype` + `field_test`
- 数据来源：自采 UAV 群感知任务与实飞测试数据
- 平台与软件：未单独披露统一平台名称
- 方法组件：`ASAP`、`elastic scheduler`、`inference predictor`、`adaptive compressor`、`TensorRT`
- 硬件与算力：`24` 台机载计算节点、`5` 架真实四旋翼 UAV、`Jetson Nano / TX2 / Xavier NX`、地面 `RTX 3060`
- 开源情况：`open`
- 复现判断：`high`
- 缺失信息：论文未给出统一标准数据集，但系统与代码已对外开放

## Introduction 写作素材
- 传统 UAV 计算方案常在“高精度但高回传时延”和“低时延但低推理精度”之间二选一。
- 当基站不可用时，真正的突破方向不是继续压缩单机模型，而是让 UAV 群本身形成协同计算系统。
- 这篇论文非常适合支撑“空中系统开始从网络化平台走向自主 AI 计算基础设施”的叙事。

## Related Work 写作素材
- 与模型压缩路线相比，本文不牺牲模型精度，而是利用群体协同释放算力。
- 与传统边缘/地面回传方案相比，本文强调空中自治计算，不依赖固定基础设施。
- 与一般协同边缘计算相比，本文更贴近 UAV 群的层级组织和链路动态特性。

## 相关系统建模页
- [[任务队列与时延保障模型]]
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[空中自主协同计算]]
- [[空中边缘大模型前沿]]
- [[多无人机协同]]

## 来源
- [原文](../raw/markdown/sun2024AllskyAutonomousComputing.md)
