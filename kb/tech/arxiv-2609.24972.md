---
id: arxiv-2609.24972
name: "RRSI: Regularized Recursive Self-Improvement of Agent Harnesses"
field: [LLM agents, 智能体自我改进, agent harness 工程]
directions: [创新创业大赛, 黑客松与数据竞赛]
published: "2026-09-21"
maturity: demo
venue_tier: arXiv
reproducibility_level: high
signal:
  venue: "arXiv"
  stars: 33
  runnable: true
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "agent 开发类黑客松的『防过拟合自进化』引擎：官方 Python 包（rrsi 包 + tests + domains，pyproject 可安装）fork 即跑，把『在自建评测集上越改越强』做成现场可见的进化曲线；其降噪地板/成本规则直接回应评委最锋利的质疑——『增益是不是只在你的演示任务上成立』（OOD 基准仍 +4.7）且省 30% policy token，对按 API 预算掐表的赛期是硬通货"
    reuse_cost: 低
    open_source: "https://github.com/google-research/rrsi"
  - track: "双创-文书与申报"
    edge: "『AgentOps/自动进化运维』题材的技术底座与风险章节背书：相比人工调 prompt 的 agent SaaS 叙事，可引用 Google Research 的正则化 RSI 证据（8 基准 in-dist 最高 +14.1、5 个 OOD 基准 +4.7、token -30%）论证产品能持续自我改进且不过拟合单一客户场景——同行评审级证据比自测截图有说服力"
    reuse_cost: 中
    open_source: "https://github.com/google-research/rrsi"
sources:
  - url: https://arxiv.org/abs/2609.24972
    title: "RRSI: Regularized Recursive Self-Improvement of Agent Harnesses（arXiv abs 页，v1 2026-09-21，Google Research 团队）"
    accessed: "2026-09-22"
  - url: https://github.com/google-research/rrsi
    title: "google-research/rrsi — 官方代码（README 方法说明与 rrsi 包/tests/domains 结构，33 stars，2026-09-22 快照）"
    accessed: "2026-09-22"
---

# RRSI：给 agent harness 递归自改进加正则（Google Research）

> 来源：https://arxiv.org/abs/2609.24972 （v1 提交 2026-09-21，cs.LG/cs.AI/cs.CL；官方代码 https://github.com/google-research/rrsi 与项目页 regularized-rsi.com；抓取日期 2026-09-22。本卡内容出自本次抓取的摘要页与官方仓库 README。）

## 是什么

arXiv 2609.24972（Peng Xia、Rujun Han、Zifeng Wang 等 15 人，Google Research 阵容）研究 **harness 级递归自改进（RSI）的过拟合治理**。出发点：agent 能力很大程度由 harness（冻结骨干模型外围的 prompt、控制流、工具、记忆与上下文管理）放大；近期方法自动迭代地提出并筛选 harness 组件级编辑，形成 agent 系统层的 RSI——但这种进化**对进化集过拟合**：分布内大涨、换基准就缩水甚至消失。RRSI 保持编辑空间开放，改为对搜索轨迹做两侧正则：

- **提议侧**：温度退火预算（annealed budget）限制单个候选可捆绑的独立编辑数；proposer 以完整编辑历史为条件，被证伪的假设不再重画；停滞时把搜索重定向到从未动过的组件；
- **筛选侧**：critic 在评估前拦截带套件特异逻辑的候选；噪声调整地板拦截落在评估方差内的"增益"；成本规则要求新增推理 token 必须由实测增益买单；失效组件定期剪除。

效果：跨 8 个基准（coding、agentic workspace、engineering design 三类），分布内最高 **+14.1** 分，5 个 OOD 基准上最高 **+4.7** 分，同时比无正则进化**少用 30% policy token**。

## 解决什么问题

harness 进化方法的"刷进化集"病：无约束的组件编辑会把套件特异逻辑写进 harness，评测分虚高、泛化能力没涨。RRSI 把"防止过拟合"从人工把关变成进化循环内建的五道闸门，让自改进的产物是可复用机制而非基准特化补丁。

## 相比前方法优势

- 相比无正则的 harness 进化基线（论文的直接对照）：同样编辑空间下 OOD 不缩水（+4.7）、token 成本降 30%，是"搜索正则化"而非"换搜索算法"的增量改良，工程上可直接叠加；
- 与库内 Meta^n（arxiv-2608.24735，元操作递归沉淀技能库）互补而非重叠：Meta^n 解决"改进深度受稳定性封顶"，RRSI 解决"改进方向被进化集带偏"——前者沉淀什么、后者防止沉淀错；
- Google Research 出品且**官方开源可跑**（rrsi 包 + tests + domains 目录，pyproject 安装结构，README 与论文同期发布），相比多数仅纸面的自改进工作，复现路径明确。

## 局限

- v1 预印本，无 venue 信号，结果为作者自报；
- 正则是"缓解"不是"消除"过拟合：OOD 增益（+4.7）远小于分布内（+14.1），跨任务泛化仍是开放问题；
- 进化循环本身吃 LLM 预算（proposal/critic/评估多路调用），适合赛前/离线沉淀，赛程中途在线进化不现实；
- 官方仓刚发布（33 stars，2026-09-22 快照），文档与社区生态薄，跑通官方域之外的场景需自建进化集与评估 harness。

## 如何用于比赛（比赛映射展开）

- **黑客松（数据与算法）**：agent 类赛题的胜负手常在"评委现场加试"环节——用 RRSI 的官方包在自建任务集上离线进化 harness，把进化曲线与 OOD 保留成绩放进 demo：评委随手出题时 agent 不崩，这正是五道闸门（critic 拦特异逻辑、噪声地板拦假增益、成本规则控 token）的可视化卖点；相比手工调 prompt 的队伍，差异化是"有纪律的自进化"且有 Google 开源背书（reuse_cost=低，fork 即跑）。
- **双创（文书与申报）**："AI+"申报里做 agent 运维/自动优化工具方向时，RRSI 提供两个现成论据：一是市场痛点（harness 过拟合 = 产品换客户场景就失效），二是技术方案的正则化五件套可作为产品架构图的骨架，引用其实测数字说明可行性与成本优势（reuse_cost=中，需把研究代码包装成产品化故事）。
