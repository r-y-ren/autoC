---
id: arxiv-2610.00906
name: "ActiveSaddler：harness 自动优化的课程层——失败模式臂 + 非平稳 bandit 场景调度"
field: [LLM agents, agent harness 工程, curriculum learning]
directions: [创新创业大赛, 黑客松与数据竞赛]
published: "2026-10-01"
maturity: demo
venue_tier: arXiv
reproducibility_level: medium
signal:
  venue: "arXiv"
  stars: 233
  runnable: true
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "agent 自进化管线的『课程调度』组件：已开源 harness 优化器（AutoSaddler，微软，MIT）上加一层 bandit 课程即可复用——失败聚类成可复用臂、按严重度/可修性/覆盖面/副作用打分择臂、开发集收益驱动 exploit/explore 切换。论文实测同优化器下仅换课程选择就白拿 GAIA2 +4.4pp / Terminal-Bench 2.0 +7.5pp test Pass@1，且到同 dev 分省 4.6x/1.7x 算力——对按 API 预算掐表的赛期是直接的成本武器，也是与库内 RRSI 卡拼装『课程选择+更新正则』双层自进化的另一半"
    reuse_cost: "中"
    open_source: "https://github.com/microsoft/AutoSaddler/tree/feat/activesaddler（MIT，233 stars）"
  - track: "双创-文书与申报"
    edge: "AgentOps/自动评测运营类项目的成本-效果论据：『该拿哪些场景养 agent』被形式化为非平稳 bandit，给出可写进申报书技术路线的完整组件图（失败模式抽取器/臂优先级器/探索控制器），引用省 4.6x 优化成本与两大 agent 基准增益说明可持续自我改进产品的经济性"
    reuse_cost: "中"
    open_source: "https://github.com/microsoft/AutoSaddler/tree/feat/activesaddler（MIT，233 stars）"
sources:
  - url: https://arxiv.org/abs/2610.00906
    title: "ActiveSaddler: Automated Curriculum Learning for Agent Harness Optimization（arXiv abs 页，v1 2026-10-01，Comments: 37 pages 16 figures，附项目页与代码链接）"
    accessed: "2026-10-03"
  - url: https://autosaddler-projectpage.github.io/activesaddler/
    title: "ActiveSaddler 项目页（方法组件、GAIA2/Terminal-Bench 2.0 结果、AutoSaddler feat/activesaddler 分支代码链接，2026-10-03 实抓）"
    accessed: "2026-10-03"
  - url: https://github.com/microsoft/AutoSaddler
    title: "microsoft/AutoSaddler — 官方代码底座（MIT，Python，233 stars，2026-10-02 有推送，feat/activesaddler 分支存在 commit 93f39390，2026-10-03 GitHub API 实查）"
    accessed: "2026-10-03"
---

# ActiveSaddler：harness 优化的瓶颈在"喂什么场景"，不在"怎么改"

> 来源：https://arxiv.org/abs/2610.00906 （v1 2026-10-01，cs.AI/cs.CL/cs.LG/cs.MA/cs.SE）；项目页 https://autosaddler-projectpage.github.io/activesaddler/ ；代码 https://github.com/microsoft/AutoSaddler/tree/feat/activesaddler ；抓取日期 2026-10-03。本卡内容出自本次抓取的 arXiv 摘要页、项目页与 GitHub API 仓库元数据。

## 是什么

arXiv 2610.00906（Sungho Park、Wonjoong Kim 等 11 人，含微软 Qingwei Lin/Victor Rühle）指出自动化 harness 优化（迭代改 prompt/工具接口/控制逻辑）的盲区：现有方法都在优化"怎么改 harness"，却把"**用哪些训练场景产生反馈**"固定死。而 harness 在进化，对它最有信息量的场景也在变。ActiveSaddler 把课程选择建成**非平稳多臂 bandit**，优化器本身一行不动（与 AutoSaddler 同底座）：

- **Failure-Pattern Extractor**：把反复出现的失败抽象为可复用"失败模式臂"，臂池在线增长；
- **Arm Prioritizer**：LLM 按严重度、可修性、覆盖面、副作用风险给每个臂打分；
- **Exploration Controller**：在"回头练已知弱点（exploit）"与"探索未见场景（explore）"间平衡，臂随 harness 进化动态实例化。

效果（摘要+项目页自报，任务 agent 与优化器均用 gpt-5.5）：test Pass@1 相比固定场景顺序 **GAIA2 59.8% vs 55.4%（+4.4pp）、Terminal-Bench 2.0 80.0% vs 72.5%（+7.5pp）**；达到给定 dev 分的优化成本 **GAIA2 省 4.6x、TB2.0 省 1.7x**；dev 精度 63.1%/89.5% 亦超最优基线（58.5%/78.9%）。对比对象含 GEPA、Meta-Harness、Terminus。

## 解决什么问题

harness 自进化循环的"教材选择"问题：固定场景顺序会让优化器在已治好的失败上空转、对还没暴露的失败视而不见。ActiveSaddler 让课程与 harness 共进化——失败模式即课程单元，bandit 保证每一轮优化预算花在当前最有学习价值的场景上。

## 相比前方法优势

- 与库内 harness 族严格互补：RRSI（arxiv-2609.24972）管"更新端正则"（防改歪/防过拟合），本卡管"课程端调度"（防喂错料）——两者可拼成双层自进化管线，无重叠；EDGEGEN（arxiv-2609.24115）是静态合成边界用例扩场景池，本卡是按学习进度动态择场景，一个供料一个选料；
- 相比固定顺序/随机顺序的课程基线：同优化器同预算下两大 agent 基准白拿 4.4~7.5pp，这是"换调度策略"级别的增量而非换架构，工程上可直接叠加到任何已有 harness 优化回路；
- 微软官方开源（AutoSaddler 233 stars，MIT，feat/activesaddler 分支 2026-10-03 实查存在），37 页论文 + 项目页，方法组件披露完整。

## 局限

- 基础设施重：跑通全套需要场景库、失败聚类、LLM 臂打分与完整优化回路，任务/优化器均按 gpt-5.5 计费，比赛尺度复刻全套成本高，实用姿势是借"臂+bandit"思想轻量自建；
- 结果为作者自报的 v1 预印本（Comments 无 venue），基线与自建消融均出自同一团队；
- 增益依赖失败模式抽取质量：失败聚类错了臂就错，论文未报告聚类错误率的影响面；
- 论文自述仅优化课程层、优化器不动——harness 本身的改进上限仍由所配优化器决定。

## 如何用于比赛（比赛映射展开）

- **黑客松（数据与算法）**：赛前/赛期迭代 agent 的正确姿势不是"想到什么改什么"，而是把踩过的失败记成模式卡（臂），按"严重度 x 可修性 x 复现成本"排序决定下一轮迭代喂哪个场景——bandit 调度思想可脱开微软全套基建，用一个 YAML 场景清单 + 简单 UCB 在半天内自建（reuse_cost=中）；若直接用官方仓，AutoSaddler MIT 底座 + feat 分支可跑，把"省 4.6x 优化成本"变成现场迭代速度优势。
- **双创（文书与申报）**：agent 产品类申报书的技术路线图可直接引用其组件划分（失败模式抽取/臂优先级/探索控制）与成本数字，论证"产品能以有界的评测预算持续自改进"——相比"人工 prompt 调优"叙事有论文级背书（reuse_cost=中，需把研究管线翻译成产品语言）。
