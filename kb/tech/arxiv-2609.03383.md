---
id: arxiv-2609.03383
name: "TIGPO: Temporal Instance-Graph Policy Optimization for Long-Horizon LLM Agents"
field: [LLM agents, 强化学习, credit assignment]
directions: [黑客松与数据竞赛]
published: "2026-09-03"
maturity: paper
signal:
  venue: "arXiv v1（2026-09-03 提交，cs.LG，单作者；摘要页无代码仓库链接）"
  runnable: false
competition_fit:
  - track: "Kaggle-竞赛"
    edge: "需要自训 agent 在长程交互环境中拿分的模拟/对战类赛（Kaggle simulation 型赛制形态）的训练侧差异化武器：这类赛题的核心痛点是 rollout 昂贵、评分方差大、小算力赛队凑不大批次；TIGPO 的跨更新持久转移图 + Exploration/Revisit 槽位设计专治'小 rollout 组下相对优势估计不稳'，且显式复用旧策略版本发现的有效转移——把历史经验变成信用分配的结构参照而不进损失重放，算力受限赛队可用小批次拿到更稳的训练信号；ALFWorld/WebShop 环境开源，可先复现论文结论再迁移到赛题环境"
    reuse_cost: 高
sources:
  - url: https://arxiv.org/abs/2609.03383
    title: "TIGPO: Temporal Instance-Graph Policy Optimization for Long-Horizon LLM Agents"
    accessed: "2026-09-04"
---

# TIGPO：面向长程 LLM agent 的时序实例图策略优化

> 来源：https://arxiv.org/abs/2609.03383 （arXiv v1 提交于 2026-09-03，主分类 cs.LG，单作者 Jinwei Gan；摘要页未附代码链接）；抓取日期 2026-09-04

## 是什么

一种**长程 LLM agent 的信用分配（credit assignment）训练方法**（以下均来自本次抓取的摘要页）。现有 graph-based policy optimization 在每次策略更新内独立构建状态转移图，导致两个损失：早期策略发现的转移被丢弃；优势估计被限制在小的批内 rollout 组里。TIGPO 的核心改动：

1. **持久转移图**：为每个任务维护跨更新（cross-update）的实例图，让不同策略版本发现的有效转移共同决定信用；
2. **Exploration/Revisit 双槽位**：固定 rollout 预算切分为常规采样槽与延迟重试槽；每次 revisit 把当前 rollout 组与其更早的 Exploration 组配对，形成**跨时间参照**——既在小 rollout 组下稳定相对优势估计，又直接度量跨训练阶段的策略改进；
3. **历史脱钩**：历史转移与分数只作为结构性与脱钩（detached）的统计参照，绝不进入 policy loss 重放。

在 ALFWorld 与 WebShop 上一致超过先前的 group-based 与 graph-based 策略优化方法。

## 解决什么问题

长程 agent 的 RL 训练中，组内对比（group-based）方法要凑大 rollout 组才稳，可 LLM agent 的 rollout 极贵；图方法虽改善了组内信用分配，却把图的生命周期限制在单次更新内。TIGPO 把信用分配的时间尺度从"一个批次"拉长到"整个训练史"，使小 rollout 组也能获得稳定的相对优势信号。

## 相比前方法优势

- **跨更新经验复用**：旧策略发现的有效转移不再随批次丢弃，而是持久图为后续更新的优势估计提供参照；
- **小 rollout 组可用**：Revisit 槽位的跨时间配对设计直接对冲小组下的高方差——这正是算力受限场景的痛点解法；
- **无重放风险**：历史只作 detached 统计参照，避免 off-policy 重放带来的偏差；
- 在 ALFWorld/WebShop 两个标准长程 agent 环境一致增益。

## 局限

- **无开源实现**：摘要页无代码链接，单作者论文，maturity 如实标 paper、runnable=false；
- **复现成本高**：需要完整 LLM-RL 训练管线（rollout 采样、持久图维护、group-based 优化器），比赛时间盒内搭建风险大；
- **实验域与赛题环境的差距**：ALFWorld/WebShop 为家庭任务与购物仿真，迁移到具体竞赛环境需自行验证；
- 摘要未报告持久图的存储/计算开销规模，采用前需读正文确认。

## 如何用于比赛（比赛映射展开）

- **Kaggle-竞赛（simulation/agent 对战型赛制，需提交自训 agent）**：把 TIGPO 作为训练侧差异化点——多数赛队用朴素 PPO/GRPO 类方法硬凑大批次，本卡打法是小批次 + 持久图跨时间参照，用"同等算力下更稳的训练曲线"做评测对比叙事；WebShop/ALFWorld 开源可先复现增益曲线作为方法有效性的前置证据；
- **迁移路径**：先在开源环境按论文设置复现，再把持久图 + Revisit 槽位机制搬到赛题环境，只换任务接口；
- **复用成本评估：高**——无开源、需 RL 基建、LLM rollout 花费真实存在；适合已有 RL 训练经验的赛队作为拔高手段，不适合从零搭起；若赛题不允许重训或时间盒 <2 周，本卡仅作方法叙述引用。
