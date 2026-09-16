---
tags: [论文, LoRa, UAV辅助通信, 实地实验, 数据采集]
created: 2026-04-09
updated: 2026-04-09
sources:
  - ../raw/markdown/zhang2025ImprovingDataCollection.md
venue_tier: CCF-A
literature_type: system
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - methodology
  - engineering_context
validation_type:
  - prototype
  - field_test
data_origin:
  - self_collected
platforms:
  - commercial LoRa platform
frameworks:
  - PreLoRa
  - annulus model
  - SF backoff
datasets: []
hardware_stack:
  - STM32 Nucleo-64
  - Semtech SX1262
  - Z410 UAV
  - Raspberry Pi 4B
  - Semtech SX1301 gateway
artifact_availability: unknown
reproducibility_level: medium
---

# Zhang2025 基于定向性感知链路模型的UAV-LoRa高效数据采集

## 单行摘要
论文通过实地测量发现 UAV-LoRa 空地链路存在“头顶数据采集空洞”，并据此提出 `annulus model + PreLoRa` 主动配置调度机制，以显著提升空地数据采集吞吐。

## 题目驱动研究框架
- 研究场景：基础设施稀缺环境下的 UAV 辅助 LoRa 数据采集网络。
- 研究对象：UAV 网关、LoRa 地面节点、空地链路定向性损耗、传输配置切换。
- 核心问题：UAV 越靠近节点并不一定越好，天线辐射方向不对齐会导致近距离反而吞吐下降。
- 标题承诺的方法：directivity-aware link model。
- 期望效果：根据空地链路质量变化主动安排发送时段和配置，提高短暂驻留时间内的数据上传效率。
- 标题与正文的偏差：正文最大的价值其实是“先发现真实空地链路反直觉现象，再围绕它做系统设计”。

## Algorithm Design 快照
作者先通过野外实验发现 UAV 在节点正上方附近会因为天线直向性失配而经历明显的信号衰减空洞。为量化这一现象，论文提出 `annulus model`，把空地链路质量写成与相对位置有关的环带结构；然后在此基础上设计 `PreLoRa`，预测 UAV 在各个配置区域内的驻留时长，并提前下发最优发送计划与参数配置。这样，节点不必被动等链路变差后重传，而是能主动在最佳窗口上传数据。

## 图1系统框架草案
- 节点层：稀疏分布的 LoRa 传感节点。
- 空中层：携带网关的 UAV 按路径经过采集区域。
- 模型层：`annulus model` 将直向性导致的链路质量变化映射到空间环带。
- 协议层：`PreLoRa` 基于模型做时序与参数调度。
- 画图提醒：把“node 上方的 data collection void”明确画出来，会非常有辨识度。

## System Model
- 地面节点在 UAV 经过期间利用短暂窗口上传缓存数据。
- 由于收发天线主辐射方向失配，空地链路质量不是随距离单调改善。
- LoRa 配置如 `SF`、`BW` 和包长会影响链路可靠性与有效吞吐。
- 系统目标是在短驻留时间内最大化可靠上传量，而非只提高单次包成功率。

## Algorithm Design 详解
- 通过实地测量建立 `annulus model`，量化直向性对空地链路的影响。
- 网关持续更新 RSS/SNR 估计与模型参数，并为节点下发未来 ping 周期内的发送计划。
- 节点根据预测的 UAV 飞行状态切换最优 `SF`、发送时段和包长度。
- 多节点场景下再引入 `SF backoff`，缓解并发冲突并提升全网吞吐。

## 实验证据卡片
- 验证类型：`prototype` + `field_test`
- 数据来源：作者实地测试链路与多节点部署数据
- 平台与软件：商业 `LoRa` 平台
- 硬件与算力：`STM32 Nucleo-64`、`Semtech SX1262`、`Z410 UAV`、`Raspberry Pi 4B`、`Semtech SX1301`
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：该文具备非常强的工程证据层，链路模型直接建立在野外测量之上。

## Introduction 写作素材
- UAV 辅助 LPWAN 的困难不只是覆盖不够，而是空地链路的几何关系会改变链路本身的物理特性。
- 如果忽略天线直向性，系统会在“看起来最近、实际上最差”的位置浪费掉宝贵上传机会。
- 因而 UAV-LoRa 数据采集应从“距离感知”升级到“定向性感知”。

## Related Work 写作素材
- 既有 UAV-LoRa 文献多聚焦 MAC、调度或轨迹，较少真正从空地物理链路实测出发。
- 既有地面 LoRa 自适应配置方法难以直接适用于高速空地移动场景。
- `PreLoRa` 是“实测链路现象驱动协议设计”的代表页。

## 相关系统建模页
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[定向性感知空地链路模型]]
- [[空中通信与协同传输]]
- [[无人机辅助群智感知与持续作业]]

## 来源
- [原文](../raw/markdown/zhang2025ImprovingDataCollection.md)
