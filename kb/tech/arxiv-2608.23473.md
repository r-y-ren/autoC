---
id: arxiv-2608.23473
name: "MetaCaster: Meta-Harness-Optimized Agent for End-to-End Few-Shot Learning of Lightweight Time Series Forecasters"
field: [时序预测, 智能体, 小样本学习]
directions: [数模与时序预测]
published: "2026-08-24"
maturity: paper
signal:
  venue: "arXiv (EMNLP 2026)"
  runnable: false
competition_fit:
  - track: "数模-预测与评估"
    edge: "小样本预测题破局流水线：LLM agent 从极少量真实样本+题面文本上下文合成增广训练数据，自动训练轻量专用预测器，应对新品销量/新站点负荷类『历史只有十几个点』的题；EMNLP 2026 接收可引为 agentic 数据增广的方法论背书，18 数据集×23 轻量模型×14 基线的评估规模可引"
    reuse_cost: 高
  - track: "黑客松-数据与算法"
    edge: "限时场景取其内核：LLM 数据增广+自动模型选型流水线 24 小时内出可用基线，不搬整套 meta-harness 系统"
    reuse_cost: 中
sources:
  - url: https://arxiv.org/abs/2608.23473
    title: "MetaCaster: Meta-Harness-Optimized Agent for End-to-End Few-Shot Learning of Lightweight Time Series Forecasters"
    accessed: "2026-08-28"
---

# MetaCaster：元测试床优化智能体，端到端少样本训练轻量时序预测器

> 来源：https://arxiv.org/abs/2608.23473 （arXiv v1 提交于 2026-08-24，cs.LG/cs.AI，**EMNLP 2026 接收**；抓取日期 2026-08-28）

## 是什么

arXiv 2608.23473（Shen 等 9 人）提出 MetaCaster：多智能体框架 + meta-harness 优化，端到端地"从极少样本训练轻量专用预测器"（以下机制描述来自本次抓取的摘要页）：

- **智能体定位为中间工程师**：不直接做预测，而是准备/训练任务专用的轻量预测器；
- **agentic 数据生成**：从极少量真实样本 + 文本上下文自动构造训练数据，供专用轻量预测器训练；
- **评估规模**：18 个数据集 × 23 个 SOTA 轻量预测器 × 14 个基线，报告数据效率、计算效率与预测质量俱佳。

## 解决什么问题

时序预测走向多模态与 agentic 化，但基础模型在资源受限场景不经济，需要紧凑专用预测器；而轻量预测器通常要大量训练数据——在数据稀缺、缓慢积累或隐私敏感的领域（少样本）难以落地。

## 相比前方法优势

- 同时把"少样本"与"轻量"两个约束作为一级目标，而非只顾一边；
- 数据生成 + 模型准备的端到端自动化，降低人工特征工程与调参负担；
- EMNLP 2026 接收构成 venue 信号；18×23×14 的评估矩阵在同类 agentic 工作中规模可观。

## 局限

- **无代码**：arXiv 页面未见作者仓库（runnable=false）；整套多智能体 + meta-harness 系统复杂，比赛语境更可能移植其"agentic 数据生成"思想而非复刻系统；
- 摘要未给出具体 few-shot 设置（几 shot）与量化增益，需查全文核实后再引数字；
- 智能体合成数据的分布偏差与信息泄漏风险需自行把关（合成数据放大偏差时轻量模型反而受损）。

## 如何用于比赛（比赛映射展开）

- **适用赛种**：数模小样本预测题（新品销量、新站点负荷、新装机传感器——历史序列只有十几个点、常规深度模型欠拟合的题）；黑客松数据与算法赛道的限时出模型场景。
- **打法（数模）**：面对超短历史序列，用 LLM 按题面领域知识生成"伪历史样本"（依产品文案/站点描述合成销量曲线族等），扩充训练集后训轻量模型（DLinear/NLinear 级），与"朴素外推"和"全局模型迁移"三方对照写入论文；可引 MetaCaster 作为 agentic 数据增广的方法论出处。
- **打法（黑客松）**：不搬 meta-harness，取其内核——LLM 合成增广 + 自动模型选型脚本，24 小时内出可用基线，剩余时间打磨特征与集成。
- **成本**：完整口径（多智能体+meta-harness）reuse_cost=高；轻量内核版（LLM 增广+自动选型）中等。
