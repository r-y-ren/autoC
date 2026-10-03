---
id: arxiv-2610.02002
name: "Mem++：组织级 LLM Agent 的非破坏式记忆——写时零压缩、读时按时间线选择"
field: [LLM agents, agent memory, 时序知识问答]
directions: [创新创业大赛, 黑客松与数据竞赛]
published: "2026-10-01"
maturity: demo
venue_tier: arXiv
reproducibility_level: high
signal:
  venue: "arXiv"
  runnable: true
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "agent 赛道的『时间线问答/组织记忆』题型可直接套：方法零训练、写时只存原文+日期+作者，读时做『截至时点过滤+词法/语义融合排序』，一个下午可实现；官方 Apache-2.0 Python 实现可跑（2026-10-03 实查，仓库 2026-10-02 仍有提交）。相比带记忆层的通用 agent 框架，差异化卖点是把『哪个版本的决策在时刻 T 有效』做对——这是 RAG 朴素 top-K 检索必翻车、评委一听就懂的考点"
    reuse_cost: "低"
    open_source: "https://github.com/AIDAChip-Inc/mem-plus-plus（Apache-2.0，Python）"
  - track: "双创-文书与申报"
    edge: "企业知识管理/合规问答类『人工智能+』项目的架构论据：组织里修订过的决策以新文档而非编辑到达，写时压缩型记忆产品（蒸馏成事实/笔记/图边的 Mem0 类方案）在写入时就锁死了能回答什么；Mem++ 的非破坏式存储+读时选择给出可引用的反方案叙事，且 OrgMemBench 上超最强记忆基线 8.0-13.1 分的数字可作技术可行性锚点"
    reuse_cost: "低"
    open_source: "https://github.com/AIDAChip-Inc/mem-plus-plus（Apache-2.0，Python）"
sources:
  - url: https://arxiv.org/abs/2610.02002
    title: "Mem++: Non-Destructive Memory for Long-Term Organizational LLM Agents（arXiv abs 页，v1 2026-10-01，Comments: 15 pages 4 figures）"
    accessed: "2026-10-03"
  - url: https://github.com/AIDAChip-Inc/mem-plus-plus
    title: "AIDAChip-Inc/mem-plus-plus — 官方代码仓（Apache-2.0，Python，1 star，2026-10-02 有推送，2026-10-03 GitHub API 实查）"
    accessed: "2026-10-03"
---

# Mem++：把组织记忆存成"带时间戳的原文"，把智能挪到读时

> 来源：https://arxiv.org/abs/2610.02002 （v1 2026-10-01，cs.CL/cs.AI；官方代码 https://github.com/AIDAChip-Inc/mem-plus-plus ；抓取日期 2026-10-03。本卡内容出自本次抓取的 arXiv 摘要页与 GitHub API 仓库元数据。）

## 是什么

arXiv 2610.02002（Ahmad Yehia、Aly O. Abdelkareem 等 7 人）研究**组织场景下 LLM agent 的长期记忆**：决策由多人跨文档、跨月记录，修订以"新文档"而非"编辑"到达，回答问题需要知道**给定时间点上哪个版本有效**。Mem++ 的主张是把记忆的智能从写时挪到读时：

- **写时零生成**：不做事实蒸馏、不建笔记/图边，每篇文档原文整体入库，只附日期与作者两个元数据——没有 generative model 参与写入；
- **读时选择**：检索时只取日期早于/等于问题时间点的文档，融合词法与语义两路排序，把"截至 T 时刻的事实状态"交给模型现场综合。

效果（摘要自报）：OrgMemBench 上跨两个回答模型超最强记忆基线 **8.0-13.1 分**；gpt-4.1-mini 下整体超 RAG **2.6 分**；LoCoMo 上平均 LLM-judge 分最高；LongMemEval-S 上排第二。

## 解决什么问题

写时压缩型记忆系统（把文档蒸馏成 facts/notes/graph edges）在**写入时就固定了日后能回答什么**——对组织决策记录这种"版本随时间演化"的语料，压缩会丢掉"某决策何时被推翻、被谁推翻"的时间线结构，导致时点问答（as-of-date QA）系统性出错。Mem++ 用"存一切+按时间线过滤"换取零信息损失。

## 相比前方法优势

- 对比写时压缩记忆基线：OrgMemBench +8.0~13.1 分，且赢在时间敏感题上而非靠总分类；
- 对比朴素 RAG：同样读时融合检索，差距 2.6 分的核心是**按问题时间点过滤文档**这一步——不需要训练、不需要图构建，是一条纯工程可迁移的流水线；
- 对比库内记忆族卡（Dynamics-memory arxiv-2609.03340 的矛盾裁决、Lemmalog gh-JordyZomer_lemmalog 的演绎数据库）：本卡解决的是**时间版本有效性**这一正交维度——那两卡裁"说法冲突"，本卡裁"哪个说法在何时有效"，可组合不可互替；
- 官方代码 Apache-2.0 已放（Python，2026-10-02 仍有提交），复现门槛低。

## 局限

- OrgMemBench 为作者方自建基准，主结果属自报；LoCoMo 仅"平均 judge 分最高"、LongMemEval-S 仅第二，跨基准并非全面碾压；
- 非破坏式存储把成本转嫁给读时上下文：文档量大时"全部原文入库+读时重排"的 token 与延迟开销随语料线性涨，论文摘要未给成本曲线；
- 官方仓极新且冷清（1 star，2026-10-03 快照），无文档与社区生态，遇坑需自己啃；
- v1 预印本无 venue 信号（Comments 仅 15 pages 4 figures）。

## 如何用于比赛（比赛映射展开）

- **黑客松（数据与算法）**：遇到"文档集+时间点提问"类赛题（会议纪要、合同修订、合规审计、多版本 wiki），固定流水线三步走：文档原文+日期入库 → 按问题时点过滤 → BM25+向量双路融合重排。相比直接上 LangChain 记忆模块或 Mem0 的队伍，差异点是时间过滤——恰好是这类题的失分主因；官方代码可作对照实现（reuse_cost=低，纯文本工程零训练）。
- **双创（文书与申报）**：做企业 agent/知识库产品的项目书里，"写时压缩 vs 读时选择"是现成的技术路线对比章节素材：可引用 Mem++ 数字论证非破坏式记忆在组织决策场景的必要性与可行性；Apache-2.0 许可对商业化叙事无障碍（reuse_cost=低）。
