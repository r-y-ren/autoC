---
tags: [论文, 视觉雷达融合, 无人机定位, 多模态感知, 小目标检测]
created: 2026-04-10
updated: 2026-04-10
sources:
  - ../raw/markdown/wan2025MultimodalScaleNormalization.md
venue_tier: CCF-A
literature_type: method
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - system_model
  - engineering_context
validation_type:
  - field_test
data_origin:
  - self_collected
platforms: []
frameworks:
  - multimodal scale normalization
  - distance-aware image slicing
  - modal fusion network
  - MMDetection
  - YOLOv5
datasets:
  - self-built vision-radar UAV positioning dataset
hardware_stack:
  - phased-array radar
  - Hikvision DS-2DC4223IW-D camera
  - rotary table
  - single GPU workstation
artifact_availability: unknown
reproducibility_level: medium
---

# Wan2025_视觉雷达融合的小型UAV定位尺度归一化框架

## 单行摘要
论文面向远距离小型 UAV 精确定位问题，提出视觉-雷达多模态尺度归一化框架，通过距离感知图像切片、尺度归一化和模态融合，在 `150 m` 到 `1300 m` 的尺度剧烈变化条件下提升小目标定位稳定性。

## 题目驱动研究框架
- 研究场景：复杂空域中小型 UAV 的宽域探测与定位。
- 研究对象：视觉传感器、相控阵雷达、远距离小目标和多模态融合网络。
- 核心问题：随着距离增大，小型 UAV 的视觉尺度迅速缩小，而雷达回波与视觉表征又存在模态差异，导致远距离定位精度显著下降。
- 标题承诺的方法：multimodal scale normalization。
- 期望效果：在远距离和尺度剧烈变化条件下保持稳定的小型 UAV 定位性能。
- 标题与正文的偏差：标题突出尺度归一化，正文的完整亮点是“距离感知切片 + 尺度归一化 + 视觉雷达融合”的成体系设计。

## Algorithm Design 快照
论文把“小目标越来越小”看成跨模态尺度漂移问题，而不是单纯更换检测器。作者先根据距离信息自适应切分图像，保留远距离小目标可分辨区域，再对视觉与雷达分支分别做尺度归一化，最后通过模态融合网络完成联合定位。这样一来，系统能够在大范围距离变化下维持更稳定的表征一致性。

## 图1系统框架草案
- 感知层：相控阵雷达 + 可见光摄像头同步观测小型 UAV。
- 预处理层：距离感知图像切片与跨模态尺度标准化。
- 融合层：视觉分支、雷达分支与模态融合网络。
- 输出层：小型 UAV 的检测与定位结果。
- 画图提醒：一定要把 `150 m -> 1300 m` 的尺度变化画出来，否则这篇论文的痛点不够直观。

## System Model
- 系统由视觉摄像头和相控阵雷达共同构成，目标是远距离小型 UAV 定位。
- 随着目标距离变化，视觉目标尺度发生显著压缩，而雷达特征与视觉特征又存在模态差异。
- 作者通过距离感知切片与尺度归一化削弱这种跨模态尺度漂移。
- 最终定位性能由感知质量、归一化效果和多模态融合能力共同决定。

## Algorithm Design 详解
- 第一步：根据目标距离设计自适应图像切片，避免远距离下小目标被过大背景淹没。
- 第二步：提出多模态尺度归一化机制，使视觉与雷达表征在不同观测距离下保持更可对齐的尺度。
- 第三步：构建融合网络，把归一化后的视觉与雷达特征联合起来完成定位。
- 第四步：在实测平台和自建数据集上验证框架对尺度变化的鲁棒性。

## 实验证据卡片
- 验证类型：`field_test`
- 数据来源：自采视觉-雷达定位数据
- 平台与软件：未单独披露平台；训练使用 `MMDetection`
- 方法组件：`distance-aware image slicing`、`multimodal scale normalization`、`modal fusion network`、`YOLOv5`
- 硬件与算力：相控阵雷达、`Hikvision DS-2DC4223IW-D` 摄像头、旋转台、单 GPU 工作站
- 开源情况：未说明
- 复现判断：`medium`
- 缺失信息：未给出数据集与训练代码的公开方式

## Introduction 写作素材
- 小型 UAV 的远距离定位并不只是“小目标检测难”，而是跨模态尺度失配导致表征难以稳定融合。
- 视觉和雷达互补，但互补要成立，前提是先解决距离变化带来的尺度漂移。
- 这篇论文适合支撑“真实空域感知正在从单模态检测走向多模态尺度建模”的引言逻辑。

## Related Work 写作素材
- 与只改进视觉检测器的工作相比，本文更强调视觉-雷达融合与尺度标准化。
- 与普通多模态融合工作相比，本文把距离变化引起的尺度漂移作为一等问题处理。
- 与只做目标检测的工作相比，本文更直接服务于精确定位场景。

## 相关系统建模页
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[视觉雷达融合定位]]
- [[多模态尺度归一化]]
- [[无人机定位]]

## 来源
- [原文](../raw/markdown/wan2025MultimodalScaleNormalization.md)
