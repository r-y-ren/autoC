---
id: arxiv-2608.26747
name: "AgentFold: Closed-Loop Agentic Search for Protein Folding Model Design"
field: [LLM agents, agentic search, 多智能体, 蛋白质折叠]
directions: [黑客松与数据竞赛]
published: "2026-08-27"
maturity: paper
signal:
  venue: "arXiv（无 Comments/venue 字段，2026-08-28 实抓；官方代码仓库已实测可达）"
  stars: 0
  runnable: true
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "『agent 自动迭代改代码刷分』的完整开源参考实现：假设→改码→调试→评测→结构化记忆（成功+失败干预均入库）→MCTS 式分支配额的闭环搜索骨架，配 matched-budget 对照法（同等算力下 +7.5% lDDT 胜独立 Codex 提案）——做 Kaggle-agent/自动调参/自改进 agent 类赛题时，失败记忆防重复探索与算力预算分配是压过『反复重跑瞎试』队伍的答辩差异化点"
    reuse_cost: 中
    open_source: "https://github.com/lmqfly/AgentFold"
sources:
  - url: https://arxiv.org/abs/2608.26747
    title: "AgentFold: Closed-Loop Agentic Search for Protein Folding Model Design"
    accessed: "2026-08-28"
  - url: https://github.com/lmqfly/AgentFold
    title: "lmqfly/AgentFold（GitHub API 实核：public、Python、约 16.5MB、agent/folding_runtime/variants 等目录齐全，created 2026-08-24 / pushed 2026-08-26）"
    accessed: "2026-08-28"
---

# AgentFold：把"改进科学 ML 系统"做成闭环代码变体搜索的多 agent 框架

> 来源：https://arxiv.org/abs/2608.26747 （arXiv v1 提交于 2026-08-27，Liu、Chen、Cao 等 11 位作者；摘要页无 Comments 字段、无 venue；代码链接在摘要中给出并经 GitHub API 实测可达；抓取日期 2026-08-28）

## 是什么

arXiv 2608.26747 提出 **AgentFold**——一个把蛋白折叠模型开发形式化为"可执行代码变体上的闭环搜索"的多 agent 框架（以下描述均来自本次抓取的摘要页）：

- **闭环流程**：从 ESMFold 出发，agent 团队提出假设 → 实现并调试代码级修改 → 评测模型变体 → 分析实验结果 → 把**成功与失败的干预都写入结构化记忆**；
- **搜索策略**：MCTS 式策略在高分搜索分支间分配算力资源；
- **规模与结果**：在一个 2,000+ 行的工程级折叠代码库上，探索约 80 个模型变体，消耗约 5,000 GPU 小时与 1.7 亿 LLM token；同等算力预算下最佳 lDDT 比独立 Codex 提案高 **7.5%**，并胜过随机搜索对照；
- **经验性设计模式**：干预轨迹揭示——稳定增益多来自"早期、软性、可学习的先验 + 门控式精炼"；直接的几何扰动与几何条件化反馈常使训练失稳。

## 解决什么问题

科学 LLM agent 此前多停留在文献推理、工具调用与实验规划，能否让它们**自主改进大型紧耦合科学 ML 系统**（需要协调式架构修改、多目标评测、领域感知解读）是悬而未决的问题。AgentFold 给出一个可执行的肯定答案路径：把模型开发本身当作搜索问题，用 agent 闭环驱动。

## 相比前方法优势

- **不是"问 LLM 要点子再人工实现"**：假设、实现、调试、评测、归档全在闭环内，产出可直接执行的代码变体；
- **结构化记忆含失败干预**：后续搜索不重复踩坑——这是相对"独立 LLM 提案"基线的核心增益来源之一；
- **MCTS 式分支配额**：算力向高分分支倾斜，优于随机搜索对照（同等预算）；
- **matched-budget 评测法**：结论建立在等算力对照上，而非"我们跑得多"；
- **附带可迁移经验**：什么样的修改在紧耦合科学系统里稳定增益、什么样的会失稳，有实证模式归纳。

## 局限

- **算力门槛如实标注**：论文规模约 5,000 GPU 小时（约 80 变体），变体评估依赖"可训练模型 + 程序化评测指标（lDDT）"；换域复用需自配可负担的 verifier，赛队只能缩到数十变体量级；
- **领域绑定**：verifier 是蛋白折叠专属（ESMFold/lDDT），骨架可迁移但折叠本体不可复用；
- **仓库刚放出**（created 2026-08-26，stars=0），无第三方复现、无 venue（arXiv 页无 Comments），学术权重未定；runnable=true 仅指"代码实测存在且内容充实"，非"开箱即用于新域"；
- "设计模式"发现（软先验>几何扰动）目前只在折叠域内成立，外推需自证。

## 如何用于比赛（比赛映射展开）

- **适用赛种**：黑客松数据与算法题中"agent 自动改进代码/基线"类赛题——Kaggle-agent 式自动刷分 agent、自动特征工程/自动调参 agent、自改进实验 agent。
- **打法（骨架平移）**：(a) 把 verifier 换成赛题的程序化评分（CV 分/评测集分），改动对象换成特征代码、模型配置或 pipeline 代码；(b) **失败也入库**：每轮尝试的 diff+得分+失败原因写结构化记忆，检索后再提议——这是与"让 GPT 反复试"队伍拉开差距的核心；(c) 变体数量按赛期算力缩放（数十个即可成立论），保留 MCTS 式"高分分支多花预算"的分配逻辑；(d) 答辩用 matched-budget 叙事：同token预算下对比"独立提案 vs 闭环记忆搜索"。
- **答辩差异化**：论文给了两条可引用证据链——闭环+失败记忆+MCTS 配额优于独立提案与随机搜索（等预算），以及"软先验+门控精炼稳定、几何硬扰动失稳"的实证模式；可将其作为自己消融实验的设计模板。
- **成本**：reuse_cost=中——Python 参考实现开源（agent/记忆/搜索分层清晰，实测仓库含 folding_runtime 与 variants 目录），但需自换 verifier 与被改对象；算力按赛期裁剪后可行，不可照搬论文规模。
