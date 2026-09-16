---
tags: [论文, 监测效用, 负效应, UAV布设, 近似算法]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/zhang2025OptimizingMonitoringUtility.md
venue_tier: CCF-A
literature_type: method
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - methodology
  - related_work
validation_type:
  - simulation
  - field_test
data_origin:
  - mixed
platforms: []
frameworks:
  - PEACE
  - submodular optimization
  - uniform matroid
  - anisotropic QoM
datasets: []
hardware_stack:
  - 5 x Mavic Air 2 UAV
artifact_availability: unknown
reproducibility_level: medium
---

# Zhang2025 兼顾监测效用与负效应的无人机布设优化

## 单行摘要
论文提出 PEACE 问题，在多 UAV 监测布设中同时优化监测效用与负效应，并用 submodular + uniform matroid 近似框架获得可证明的近优解。

## 题目驱动研究框架
- 研究场景：面向人、车流或公共目标的 UAV 临时监测部署。
- 研究对象：多个被监测对象、若干可部署 UAV、摄像头朝向、二维部署区域。
- 核心问题：如何在提高监测质量的同时避免过近接触、噪声与隐私不适等负效应。
- 标题承诺的方法：optimizing monitoring utility considering adverse effects.
- 期望效果：在给定 UAV 数量约束下，获得兼顾高质量监测与较低负面影响的布设策略。
- 标题与正文的偏差：正文真正的亮点不在 placement 本身，而在把效用与负效应联合近似为 submodular maximization 问题。

## Algorithm Design 快照
论文研究多 UAV 对多对象的监测部署问题。传统工作通常只最大化图像质量或 QoM，但忽略了无人机靠得过近可能带来的安全、噪声和隐私负担。作者首先构建各向异性的 QoM 模型与 adverse effect 模型，并通过分段常数近似和区域划分把连续部署空间离散为有限候选策略集；随后把原问题近似为单调子模函数在 uniform matroid 约束下的最大化问题，并设计 PEACE 算法组合求解。这样，监测质量与负效应首次在统一的可证明近似框架下被处理。

## 图1系统框架草案
- 系统实体：多个监测对象、若干 UAV、候选部署区域、摄像头朝向。
- 任务/数据流：UAV 选择位置与朝向去覆盖对象，并输出整体监测效用。
- 控制/优化变量：UAV 位置、相机朝向、候选策略子集。
- 约束来源：UAV 数量上限、监测距离、有效监测角度、负效应半径。
- 画图提醒：图中要同时显示“收益随角度和距离变化”与“负效应随距离上升”的双曲线关系。

## System Model
- 监测效用采用 anisotropic QoM 建模，兼顾距离与朝向对识别质量的影响。
- 每个对象还对应 adverse effect 函数，刻画近距离监测带来的风险/不适。
- 通过区域划分与候选策略提取，把连续 UAV 布设空间离散成有限候选策略集合。
- 在给定 UAV 数量上限下，目标是最大化融合监测效用并最小化总体负效应。

## Algorithm Design 详解
- 目标近似：先对 reward/QoM 等连续函数做分段常数近似，为离散化做准备。
- 区域划分：把二维平面切成若干等价子区域，使每个区域内效用与负效应近似恒定。
- 候选策略提取：从子区域中抽取代表性部署策略，构成有限 ground set。
- 子模求解：将问题转化为 MSMUM，并用 PEACE 算法组合达到 `1 - 1/e - ε` 近似；内部子问题达到 `1 - 1/e` 与 `O(n log n)`。
- 实验表现：相较对比方法，综合目标提升范围为 `9.0%` 到 `1434.5%`，并在实地文本识别实验中取得更高准确率。

## 实验证据卡片
- 验证类型：数值仿真；真实场地飞行测试
- 数据来源：混合来源；随机拓扑仿真 + 实地文本监测实验
- 平台与软件：未说明；使用开源文本识别模型做外部评测
- 硬件与算力：`5 x Mavic Air 2 UAV`
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：这篇论文把“实地监测负效应”引入 UAV 部署评估，是当前库里较少见的人因/安全约束证据。

## Introduction 写作素材
- 无人机监测不应只追求拍得更清楚，还需要考虑靠得太近带来的风险和干扰。
- 这类“效用-负效应”权衡正在把 UAV 部署问题从纯几何覆盖推进到人因感知优化。
- 这篇论文适合支撑“监测部署正在从 coverage-aware 走向 utility-aware + impact-aware”的引言判断。

## Related Work 写作素材
- 与传统 QoM 监测工作相比，本文首次系统加入 adverse effect 约束。
- 与普通 coverage/placement 工作相比，本文把连续部署空间转化为可求解的子模优化。
- 与纯理论子模最大化问题相比，本文有真实 UAV 场地实验支撑。

## 相关系统建模页
- [[区域覆盖与部署模型]]

## 相关概念与主题页
- [[监测负效应]]
- [[覆盖与部署优化主线]]
- [[无人机辅助群智感知与持续作业]]
- [[UAC研究路线图]]

## 来源
- [原文](../raw/markdown/zhang2025OptimizingMonitoringUtility.md)
