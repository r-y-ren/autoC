---
id: arxiv-2610.01256
name: "DeFA：依赖图引导的 LLM Agent 失败归因——事件依赖图+失败传播图定位决定性错误"
field: [LLM agents, 失败归因, 多智能体系统调试]
directions: [创新创业大赛, 黑客松与数据竞赛]
published: "2026-10-01"
maturity: paper
venue_tier: arXiv
reproducibility_level: low
signal:
  venue: "arXiv"
  runnable: false
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "agent 赛道的可靠性/可调试性差异化模块：多数队伍只演示成功路径，'失败后能自动定位哪个 agent 哪一步犯的错'是评委可感知的工程成熟度信号。DeFA 的两件套可降级自实现——轨迹建事件依赖图、沿失败传播图回溯决定性错误；其'分段详情+他段摘要'的长轨迹处理技巧是低成本可抄的工程要点。论文给出闭环证据：归因诊断喂给 Trace2Skill 后下游任务准确率 +6~15pp，说明归因不是分析玩具而是改进回路的前置件"
    reuse_cost: "高"
sources:
  - url: https://arxiv.org/abs/2610.01256
    title: "DeFA: Dependency-Guided Failure Attribution for LLM Agents（arXiv abs 页，v1 2026-10-01，cs.AI，Comments 无 venue 无代码链接）"
    accessed: "2026-10-03"
---

# DeFA：agent 失败归因不能只读步骤文本，要读步骤依赖

> 来源：https://arxiv.org/abs/2610.01256 （v1 2026-10-01，cs.AI；abs 页无代码链接，GitHub 检索 0 命中（2026-10-03 API 实查 q=DeFA failure attribution）；抓取日期 2026-10-03。本卡内容出自本次抓取的 arXiv 摘要页。）

## 是什么

arXiv 2610.01256（Bo Deng、Xinlei Zheng 等 9 人）做 LLM agent（含多 agent）执行的**失败归因**：错误发生步与其可见后果之间可能隔着很多步，定位"决定性错误"必须同时理解步骤内容与步骤间依赖。DeFA 框架三步：

1. 把协议关系（protocol relations）与语义依赖合成覆盖整条轨迹的**事件依赖图**；
2. 在其上构造**失败传播图**，定位决定性错误、责任 agent 与错误类别；
3. 长轨迹按**分段处理**——每段的详情与其余各段的摘要配对，控制上下文又不丢全局。

效果（摘要自报）：Who and When 基准（含 Pro 文本子集）跨骨干取得最高准确率；支持图像/视频轨迹；归因诊断喂给 Trace2Skill 后**下游任务准确率提升 6~15 个百分点**。

## 解决什么问题

"哪个 agent、哪一步、什么错"的事后归因是 agent 系统迭代的瓶颈：日志回放靠人眼，LLM 直接读长轨迹会被上下文淹没且忽略"步骤 B 的失败其实是步骤 A 埋的雷"这类依赖结构。DeFA 把归因从文本阅读问题变成图上的传播定位问题。

## 相比前方法优势

- 相比纯 LLM 判卷式归因：显式建模步骤依赖，能抓"错在早处、显在晚处"的因果错位，Who&When 上跨骨干 SOTA；
- 相比库内近邻卡无重叠：AttnLocate（arxiv-2608.24022）做安全侧的"行为引导指令定位"，TraceBench（arxiv-2608.27182）做时序根因的受控评测——"多 agent 失败归因"在 kb/tech 是空位，本卡占位；
- 与本仓库 harness 工程线（RRSI/ActiveSaddler）同链条：自进化回路需要"知道上一轮为什么败"，DeFA 提供的是回路里归因环节的方法论，且 Trace2Skill 闭环证明归因产物可兑现为下游分数。

## 局限

- **无开源实现**：abs 页无代码链接，GitHub 检索 0 命中（2026-10-03 实查），复现=按论文自建依赖图抽取+传播定位管线；
- 结果为作者自报 v1 预印本，Comments 无 venue；
- 依赖图质量决定归因上限：协议关系与语义依赖的抽取本身可能出错，摘要未给错误依赖对结果的影响分析；
- 下游 +6~15pp 依赖 Trace2Skill 这一外部系统，归因→改进的闭环在比赛尺度需自行搭建。

## 如何用于比赛（比赛映射展开）

- **黑客松（数据与算法）**：两个可落地的降级用法——其一，调试利器：多 agent 项目现场联调时，把轨迹按"工具调用=事件、消息传递=依赖边"建简易有向图，失败后沿图回溯而非从头人读日志，定位速度就是迭代速度；其二，答辩卖点：演示"失败自动归因+修复建议"环节，与只放成功 demo 的队伍拉开工程成熟度差距。论文的"分段详情+他段摘要"是长轨迹塞进上下文的直接可抄技巧。注意 reusable 的是方法论（reuse_cost=高：无代码，全部自行实现），勿在材料中声称使用了 DeFA 系统。
