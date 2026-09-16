---
tags: [论文, 事件相机, 无人机避障, BioDrone, FPGA]
created: 2026-04-10
updated: 2026-04-10
sources:
  - ../raw/markdown/li2025TamingEventCameras.md
venue_tier: CCF-A
literature_type: system
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - engineering_context
  - methodology
validation_type:
  - prototype
  - field_test
data_origin:
  - self_collected
platforms:
  - ArduPilot
frameworks:
  - BioDrone
  - CEF
  - LEM
  - DOT
  - FPGA co-design
datasets: []
hardware_stack:
  - Xilinx Zynq-7020
  - stereo event cameras
  - industrial drone
  - NVIDIA Jetson TX2
artifact_availability: unknown
reproducibility_level: medium
---

# Li2025_BioDrone基于事件相机的无人机避障

## 单行摘要
论文提出 `BioDrone` 事件相机避障系统，以仿生视觉通路启发的 `CEF + LEM + DOT` 管线和 FPGA 软硬协同设计，实现工业无人机在高速场景下低于 `6.4 ms` 的端到端避障感知延迟。

## 题目驱动研究框架
- 研究场景：工业与城市高速飞行环境中的无人机避障。
- 研究对象：双目事件相机、机载处理芯片、飞控系统和动态障碍物。
- 核心问题：传统帧相机和雷达在高相对速度下易受运动模糊或视场限制影响，难以同时保证检测速度与定位精度。
- 标题承诺的方法：用 bio-inspired architecture and algorithm 驯服 event cameras。
- 期望效果：在高动态场景中稳定实现高检测率、低定位误差和低延迟。
- 标题与正文的偏差：标题强调事件相机“驯服”，正文真正亮点在于“生物启发视觉管线 + FPGA 并行化 + ArduPilot 集成”的系统级共设计。

## Algorithm Design 快照
作者不是简单把事件流换成新的视觉输入，而是重构了整套避障管线。系统以双目事件相机为输入，先通过交叉神经节启发的 `CEF` 快速滤除环境触发事件，再通过 `LEM` 在时空表示上完成双目匹配，最后以 `DOT` 融合历史轨迹和实时观测，持续预测障碍位置。为了让这套管线真正跑上机，作者进一步用 `Xilinx Zynq-7020` 做软硬件协同，把像素级事件处理并行化。

## 图1系统框架草案
- 感知层：双目事件相机持续输出异步事件流。
- 处理层：`CEF -> LEM -> DOT` 三段式视觉处理。
- 执行层：与 `ArduPilot` 集成的飞行控制器根据障碍位置做规避动作。
- 评估层：检测率、跟踪误差、端到端时延、不同飞行模式对比。
- 画图提醒：把“生物视觉通路类比”与“FPGA 并行实现”同时画出来，才能体现论文的系统完整性。

## System Model
- 论文以工业无人机高速飞行中的动态避障为核心任务，输入来自双目事件相机。
- 事件相机输出不是帧，而是像素级异步事件流，因此传统图像拼帧定位会带来额外延迟。
- 系统目标是在检测率、定位精度和反应延迟之间取得更优平衡，并支撑不同飞行模式下的在线避障。
- 为实现机载实时运行，系统必须在算法复杂度、芯片实现和飞控接口之间协同设计。

## Algorithm Design 详解
- 第一步：提出仿生视觉路径式处理架构，让双目事件流尽早融合，而不是等到最后再做三角测量。
- 第二步：用 `CEF` 快速滤除环境触发事件，缓解事件爆发导致的障碍信息淹没问题。
- 第三步：用 `LEM` 构造独特时空表示完成双目事件匹配，降低事件“粘连”带来的定位延迟。
- 第四步：用 `DOT` 融合历史状态和当前观测，持续跟踪并预测障碍位置。
- 第五步：将上述模块以 FPGA 逻辑电路并行实现，并集成进 `ArduPilot` 飞控链路。

## 实验证据卡片
- 验证类型：`prototype` + `field_test`
- 数据来源：自采事件流与室内外实飞场景
- 平台与软件：`ArduPilot`
- 方法组件：`BioDrone`、`CEF`、`LEM`、`DOT`、`FPGA co-design`
- 硬件与算力：`Xilinx Zynq-7020`、双目事件相机、工业无人机；对比中使用机载 `NVIDIA Jetson TX2`
- 开源情况：未说明
- 复现判断：`medium`
- 缺失信息：未披露完整硬件 HDL/驱动代码与事件数据集发布情况

## Introduction 写作素材
- 高速飞行无人机的安全瓶颈并不只在控制策略，而在感知链路能否以毫秒级时延稳定捕捉动态障碍。
- 事件相机天生适合高动态场景，但真正难点在于如何把异步事件流转成可用的避障决策。
- 这篇论文很适合支撑“空中智能系统需要传感器、算法和硬件协同共设计”的引言论证。

## Related Work 写作素材
- 与基于帧相机的避障方法相比，本文直接围绕事件流设计系统管线。
- 与单纯的软件算法方案相比，本文把 FPGA 并行实现和飞控集成一起纳入设计。
- 与通用事件视觉工作相比，本文更强调高速无人机避障这一具身执行场景。

## 相关系统建模页
- [[无人机能耗模型]]

## 相关概念与主题页
- [[事件相机]]
- [[轨迹优化与协同控制]]
- [[大语言模型驱动无人机规划]]

## 来源
- [原文](../raw/markdown/li2025TamingEventCameras.md)
