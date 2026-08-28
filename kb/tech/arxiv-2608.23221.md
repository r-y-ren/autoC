---
id: arxiv-2608.23221
name: "Which Histories Matter for Time Series Forecasting? Learning Predictive Relevance with Future Supervision"
field: [时序预测, 信息检索, 检索增强预测]
directions: [数模与时序预测]
published: "2026-08-24"
maturity: paper
signal:
  venue: "arXiv"
  runnable: false
competition_fit:
  - track: "数模-预测与评估"
    edge: "相似日/类比检索类题（负荷、气象、交通）的升级件：用历史折内『已实现未来』作特权监督训练 listwise 兼容性重排器，叠在经典相似日检索上提升近邻质量；其域诊断结论（查询特定相关性存在与否）兼作赛前『检索式 vs 末值锚定』的选型依据"
    reuse_cost: 中
sources:
  - url: https://arxiv.org/abs/2608.23221
    title: "Which Histories Matter for Time Series Forecasting? Learning Predictive Relevance with Future Supervision"
    accessed: "2026-08-28"
---

# Which Histories Matter?：用未来监督学习历史样本的预测相关性

> 来源：https://arxiv.org/abs/2608.23221 （arXiv v1 提交于 2026-08-24，cs.IR 主分类 / cs.LG；抓取日期 2026-08-28）

## 是什么

arXiv 2608.23221（Choi & Cho）研究"预测查询到底该检索哪些历史样本"（以下机制描述来自本次抓取的摘要页）：

- 定义**预测相关性** = 在推理时信息条件下的期望未来效用；**已实现的未来只在训练期作为特权监督**（privileged supervision），推理时仅用过去数据——部署合法；
- 方法两段式：**归一化模式检索器**（normalized-pattern retriever）构建粗候选集 + **轻量残差 MLP** 学习 listwise 未来兼容性目标做重排；
- 理论分解：最优相关性 = 候选级效用 + 查询特定兼容性，并设计 Candidate-Prior / Shuffled-Future 两个控制实验分离两者；
- 实验：6 个基准 × 12 个确认性任务——重排器改进 Pattern 检索、同协议下胜过 SARAF 检索规则；消融把增益归于未来监督本身。

## 解决什么问题

历史检索增强预测普遍拿"过去相似"当"有用"的代理，但相似不等于对当前查询的预测有帮助；缺少一套"哪些历史该被检索"的学习目标。

## 相比前方法优势

- 直接以"对预测的期望未来效用"为监督目标，对齐预测而非检索相似度；
- 特权信息只在训练期使用，推理不依赖未来数据；
- 控制实验设计（两分解 + 两对照）严谨，把增益归因到未来监督而非 MLP 容量或附加上下文。

## 局限（含作者自陈）

- **没有普适最优的检索规则**：末值锚定的 L2 规则在部分域仍占优，未来监督重排的优势集中在诊断显示存在查询特定相关性的域（摘要举例 Solar）——这既是诚实结论也是适用性上限；
- 无代码（arXiv 页面未见作者仓库，runnable=false）、无 venue 信号，摘要层面增益幅度未量化，需全文核实；
- 主分类为 cs.IR，评审语境是检索而非预测竞赛，移植时需自行验证。

## 如何用于比赛（比赛映射展开）

- **适用赛种**：相似日/类比法是常规武器的数模预测题——电力负荷、气象要素、交通流量（"找历史相似日加权预测"是这类题的经典解法）。
- **打法（检索重排升级）**：在传统相似日检索上加一层"未来监督重排器"——训练期在历史折内用已实现的未来给候选集打 listwise 兼容性标签，训练残差 MLP；推理时检索 + 重排 + 加权融合。
- **赛前选型（诊断用法）**：先验证题目的查询特定相关性（不同查询的最优近邻集合差异是否够大）再决定是否上重排——该文的域诊断思路直接可搬。
- **诚实建议**：该文自己的结论是域依赖且简单规则常胜——比赛务必三方 A/B（朴素末值锚定 / 相似日 / 重排相似日）择优入论文，重排器只在诊断支持时作为差异化亮点，避免为复杂而复杂。
- **成本**：检索器 + 残差 MLP 均为轻量组件，按论文描述可在比赛周期内实现（reuse_cost=中）。
