---
id: arxiv-2608.26829
name: "SAGE: Variate-Wise Semantic Augmentation for Vision-Language Time Series Forecasting"
field: [time series forecasting, vision-language models, 语义增强]
directions: [数模与时序预测]
published: "2026-08-27"
maturity: paper
signal:
  venue: "arXiv"
  runnable: false
competition_fit:
  - track: "数模-预测与评估"
    edge: "多变量时序题的语义先验注入：把每个变量的文字描述+统计描述子经门控残差注入频域 patch 表示，视觉对齐只在训练期（推理环内零 LLM 成本）——负荷/气象/空气质量/交通类赛题变量有明确物理含义，『变量粒度语义注入』是数模队讲得清、可消融的建模创新点；作者自报 8 个长程基准+M4 SOTA（v1 未经同行评审，引用需谨慎）"
    reuse_cost: 高
sources:
  - url: https://arxiv.org/abs/2608.26829
    title: "SAGE: Variate-Wise Semantic Augmentation for Vision-Language Time Series Forecasting"
    accessed: "2026-08-28"
---

# SAGE：变量粒度语义增强的视觉-语言时序预测

> 来源：https://arxiv.org/abs/2608.26829 （arXiv v1 提交于 2026-08-27，cs.LG 跨 cs.CV，comments: 10 pages, 2 figures；作者 Haizhao Fan、Xinyi Le；抓取日期 2026-08-28）

## 是什么

arXiv 2608.26829 提出 **SAGE**：端到端基于 CLIP 的视觉-语言时序预测框架（以下描述均来自本次抓取的摘要页）：

- CLIP 文本编码器处理**频域增强 patch 与变量 token**，经**门控残差通路**注入每个变量专属的文字描述与统计描述子（variate-wise，而非数据集级统一提示）；
- **冻结的 CLIP 视觉编码器**通过**仅训练期的对比目标**把"渲染成图的序列"与时间表示对齐——推理环内没有任何 LLM；
- 作者自报在 **8 个长程预测基准 + M4** 上取得 SOTA，消融显示多模态对齐与变量级知识增益互补。

## 解决什么问题

纯数值时序模型缺少领域专家隐式使用的语义知识（变量物理含义、统计行为、时序动态）。已有补法两派皆有痛点：推理期挂 LLM（算力贵）；数据集级统一文本提示（忽略变量间异质性——不同变量的语义/统计特性差异被抹平）。SAGE 把语义注入做到**变量粒度**且推理期零 LLM 成本。

## 相比前方法优势

- **变量级 vs 数据集级**：逐变量描述+统计描述子，保留变量异质性；
- **门控残差注入**：语义通路的贡献可控、可消融（数模写作友好）；
- **训练期视觉对齐**：对比目标只出现在训练，推理成本≈常规前向传播，避开"推理挂 LLM"的算力账；
- 时间、跨变量、文本、视觉四路信息联合建模。

## 局限

- **无代码发布**（arXiv 页 comments 仅"10 pages, 2 figures"，runnable=false），CLIP 文本+视觉双编码、频域 patch、对比训练管线从零复现工程量大；
- SOTA 数字为作者自报的 v1 预印本结果，无同行评审信号；
- 对变量无自然语言语义可写的赛题（匿名传感器通道类 Kaggle 题）增益存疑——卖点依赖"变量含义可描述"；
- 摘要未报训练成本与推理延迟的量化对比，"零 LLM 推理"省下多少需自行验证。

## 如何用于比赛（比赛映射展开）

- **适用赛种**：数模预测与评估类时序题（负荷/气象/环境/交通等变量物理含义明确的场景）。
- **打法**：给每个变量写一句领域描述 + 计算统计描述子，经冻结文本编码器→投影→门控残差注入骨干预测器——相对纯数值基线多出"领域知识显式进模型"的可解释创新层，且可做有/无语义注入、逐变量开关的消融，支撑论文写作的方法章节。
- **降本路径**：完整复现 SAGE 成本高（reuse_cost=高，无代码）；可拆出核心思想做简化版（冻结 CLIP 文本编码器 + 门控残差注入，跳过视觉对比对齐），工程量降为中，但 SOTA 数字不可迁移，只借方法论。
- **Kaggle 侧提醒**：匿名通道赛题写不出变量描述，此路不通；有元数据/变量名可读的赛题（如能源类）适用。
