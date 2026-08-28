---
id: arxiv-2608.20761
name: "Fuzzy-MoE: Interpretable Regime-Conditioned Expert Routing for Non-Stationary Multivariate Time Series Forecasting"
field: [时序预测, 机器学习, 可解释AI]
directions: [数模与时序预测]
published: "2026-08-21"
maturity: paper
signal:
  venue: arXiv
  runnable: false
competition_fit:
  - track: "数模-预测与评估"
    edge: "非平稳多变量预测题（负荷/交通/销量类，带政策切换或工况突变）用『模糊规则路由的专家混合』替代单一端到端黑箱：IF-THEN 规则+高斯隶属度曲线直接构成机理解释章节，回应数模评审对可解释性的常见质疑；不同变量激活不同专家的隶属度热力图本身就是现成的结果分析图"
    reuse_cost: "中"
    open_source: "无官方实现（arXiv 摘要页无代码链接，2026-08-28 检索确认未发布仓库）；模糊隶属度原型可借 PYFTS 库起步，但完整双视角路由需自建"
  - track: "黑客松-数据与算法"
    edge: "regime 识别+专家路由透明化是 demo 叙事卖点：现场可展示『当前处于哪个潜在动态状态、哪个专家被激活、置信多少』，比黑箱 MoE 的路由权重可讲性强"
    reuse_cost: "中"
sources:
  - url: https://arxiv.org/abs/2608.20761
    title: "Fuzzy-MoE: Interpretable Regime-Conditioned Expert Routing for Non-Stationary Multivariate Time Series Forecasting (arXiv:2608.20761, cs.LG cross cs.AI)"
    accessed: "2026-08-28"
---

# Fuzzy-MoE：可解释的 regime 条件专家路由预测

## 是什么

Guo Lan、Xiao Jie 等（2026-08-21 提交 arXiv，cs.LG/cs.AI）提出的 **Fuzzy-MoE**：基于模糊逻辑的动态混合专家（MoE）架构，面向非平稳多变量时序预测。结构为并行专家映射网络 + 双视角模糊路由器——路由器同时利用局部卷积动态与全局分段统计推断潜在动态状态（regime），通过可学习高斯隶属函数计算专家激活强度，实现显式 IF-THEN 规则式专家选择；同一序列中不同变量可激活不同专家。

## 解决什么问题

非平稳多变量序列中，不同变量、不同样本呈现异质的潜在动态状态；主流深度预测模型把它们压缩进一个统一端到端映射，导致两点损失：时变动态建模不佳（一套权重伺候所有 regime），以及不透明——说不清当前预测由哪种机制主导。传统 MoE 虽分工但路由是黑箱学习值，无法解释"为什么此刻选这个专家"。

## 相比前方法优势（论文自报）

- **可解释路由**：模糊隶属度+规则激活提供透明的路由诊断，专家选择可追溯——与黑箱 MoE 路由形成直接对比；
- **细粒度异质性建模**：变量级而非样本级的专家激活，同一序列不同变量走不同专家；
- **精度**：论文自报在多个公开基准上准确率优于主流预测方法（摘要页未附具体数值表）。

## 局限（如实标注）

- **无官方代码**：arXiv 摘要页无代码链接，2026-08-28 web 检索确认未发布官方仓库，完整复现需按论文自建（signal.runnable 记 false）；检索到的 pyFTS、zaai-ai/mixture_of_experts_time_series 仅为相邻工具，非本文实现；
- 摘要级信息未给出基准清单与误差数值，"优于主流方法"是作者自报主张，引用须注明出处；
- 模糊规则的可解释性依赖隶属函数设计合理性，规则数与专家数的选择未在摘要中说明，实战需自行调参；
- 新投稿（v1，2026-08-21），未经同行评审与社区复现检验。

## 如何用于比赛

1. **数模-非平稳预测题主用**：负荷/交通/销量等带 regime 切换的预测题，把"单一模型"升级为"模糊规则门控的多专家"：局部卷积统计+全局分段统计算隶属度 → 门控两三个互补专家（如线性专家+非线性专家）。答辩时用隶属度曲线解释"何时切换机制"，直接命中评审对黑箱的扣分点。
2. **轻量移植版（推荐路线）**：不完整复现架构，只借"双视角统计特征 + 高斯隶属度软门控"思想叠加在 DLinear/PatchTST 等成熟骨干上，工程量小、故事完整——论文思想标注出处即可。
3. **黑客松 demo**：路由可视化（变量×专家激活热力图）做"透明 AI"叙事组件。
