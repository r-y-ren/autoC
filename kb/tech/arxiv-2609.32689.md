---
id: arxiv-2609.32689
name: "FASE：情景记忆+在线策略学习的自进化时序预测 agent（GIFT-Eval nMAE -9.1%）"
field: [时序预测, LLM agent, 持续学习]
directions: [数模与时序预测]
published: "2026-09-26"
maturity: paper
signal:
  venue: "arXiv"
  runnable: false
competition_fit:
  - track: "数模-预测与评估"
    edge: "滚动预测赛题中真值逐期揭晓=天然在线反馈流，本卡给出利用它的完整范式（反馈→情景记忆检索→排序引导浓缩），且**不更新 LLM 参数**即可自进化；比赛尺度可降级借鉴：不必复现完整 agent，把『哪类模型在哪类段位预测准』的反馈写成排序备忘并逐轮调整模型组合，即得其核心收益的轻量版；论文自报 GIFT-Eval 29 配置聚合最优、较最强单 FM 基线 nMAE 降 9.1%，是目前 LLM×时序 agent 中较扎实的量化证据"
    reuse_cost: 高
sources:
  - url: https://arxiv.org/abs/2609.32689
    title: "Self-Evolving Time-Series Forecasting Agents with Episodic Memory and Online Policy Learning"
    accessed: "2026-10-03"
---

# FASE：情景记忆与在线策略学习的自进化时序预测 agent

> 来源：https://arxiv.org/abs/2609.32689 （arXiv v1 提交于 2026-09-26，Wang、Wang、Wu、Zhang；抓取日期 2026-10-03）

## 是什么

arXiv 2609.32689 提出 **FASE**（Feedback-Aware Self-Evolving forecasting agent）（以下机制描述均来自本次抓取的摘要页）：

- **问题起点**：LLM 预测 agent 多数只处理当前预测实例；而真实部署是**在线**的——新预测不断从当前时间发出，早先预测的真值逐步到位，这些反馈被现有 agent 浪费；
- **机制两件套**：
  1. **情景记忆（episodic memory）**：存取过往已完成的预测实例供检索；
  2. **在线策略学习（online policy learning）**：把累积反馈浓缩成**排序引导（ranking guidance）**，指导后续预测决策；
- **实证**：GIFT-Eval 29 个配置上取得受测方法中最优聚合点预测结果，较最强单基础模型基线**归一化 MAE 降低 9.1%**；收益随反馈累积而增长，表明 agent 能在**不更新 LLM 参数**的前提下自进化。

## 解决什么问题

把「预测做完即弃」的一次性 agent 变成「预测—验证—复盘—改进」的闭环：让历史错误（与偶然命中）成为后续预测的可检索经验，而不是等模型重训。

## 相比前方法优势

- 相比静态 LLM 预测 agent：有跨实例的记忆与策略积累，在线场景下收益单调增长；
- 相比在线微调路线：不更新模型权重，避免灾难遗忘与算力开销，反馈以记忆+排序引导的轻量形态积累；
- 量化结果较具体（29 配置聚合最优、-9.1% nMAE），不是单一数据集的 cherry-pick 叙事。

## 局限

- **无代码、无 venue**（2026-10-03 实抓 arXiv 页无仓库链接与 Comments），runnable=false；完整复现需自建 LLM 编排+记忆库+在线策略学习三件，比赛尺度工程量高；
- 收益与「反馈可累积」绑定：一次性预测任务（无滚动验证窗口）无收益空间；
- 依赖 LLM API 的多步编排，赛期成本与时延需评估；摘要未报告与「简单持续学习基线」（如指数加权模型池）的对照，自进化收益中多少来自 LLM 本身待原文核验。

## 比赛映射

- **数模-预测与评估**：数模赛滚动预测题（逐期提交、真值逐步揭晓）与本卡的在线设定同构；**可行落地是降级版**——不搭 agent，只借其数据结构：维护「(预测轮次, 模型/配置, 段位, 误差)」的情景记录表 + 跨轮次的模型组合排序调整；完整 agent 复现成本高（LLM 编排+记忆+策略学习，无代码），作为方法论卡入库而非即用工具。

## 关联

- 库内「LLM×时序」族第三分支：arxiv-2609.22977 CASP-LLM（覆盖感知提示选择，检索机制层）、arxiv-2609.23257 CTRL（LLM 控制器+残差修正，控制层）、本卡（记忆+策略学习，自进化层）——三者机制互不重叠，可组成 LLM 增强预测的方法论谱系。
