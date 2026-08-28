---
id: arxiv-2608.23011
name: 'Coarse Indexing, Fine Evidence: Decoupling Temporal Granularity in Long-Video RAG'
field: [long-video understanding, retrieval augmented generation, 高效检索]
directions: [黑客松与数据竞赛]
published: "2026-08-24"
maturity: paper
signal:
  venue: "arXiv v1（2026-08-28 实抓：无 Comments、无 venue、无代码链接）"
  runnable: false
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "长视频 QA/视频理解类赛题的免训练提速组件：粗粒度图索引定位 + 保留映射回扩原粒度证据的两级设计，节点数砍半到六成、端到端时延 1.3-1.7 倍加速而 QA 保持约 99%——限时赛中'建得完索引、跑得完检索'正是长视频题的翻车点，且 training-free 无算力门槛，赛期内可自实现复现，与堆模型参数的队伍形成工程差异化"
    reuse_cost: 中
    open_source: "无官方实现（arXiv 页 2026-08-28 实抓无代码链接；方法免训练，密度合并算法可自建）"
sources:
  - url: https://arxiv.org/abs/2608.23011
    title: 'Coarse Indexing, Fine Evidence: Decoupling Temporal Granularity in Long-Video RAG'
    accessed: "2026-08-28"
---

# 粗索引细证据：长视频 RAG 的时间粒度解耦（DAGC）

> 来源：https://arxiv.org/abs/2608.23011 （arXiv v1 提交于 2026-08-24，主分类 cs.CV 交叉 cs.AI；抓取日期 2026-08-28）

## 是什么

arXiv 2608.23011 提出 DAGC（Density-Aware Graph Construction，按摘要命名），一个 **training-free** 的长视频 RAG 索引构建方法（以下描述与数字均来自本次抓取的摘要页）。核心主张：现有 graph-based video RAG 在建索引时把**索引粒度与证据粒度耦合**在视频分割的固定时间粒度上，而这个耦合是不必要的——定位相关区域只需粗表示，支撑推理才需要细证据。做法：

1. **密度自适应合并**：把视觉内容冗余的相邻 chunk 合并，构建紧凑的密度自适应图索引；
2. **保留映射**：合并后的节点保留到原始（细粒度）时间单元的映射；
3. **回扩精化**：检索命中粗区域后，回扩到原始 chunk 粒度取细证据做推理精化。

**结果**：在 MLVU、Video-MME、LongVideoBench 三个长视频 QA 基准上，仅保留约 40-50% 的图节点，端到端 wall-clock 加速 1.3-1.7 倍，QA 性能保持约 99%；且宣称该设计可跨 LVLM backbone 与 video RAG pipeline 转移。

## 解决什么问题

长视频切 chunk 后逐段建图索引，索引规模随视频时长线性膨胀，检索与构建都贵；而其中大量 chunk 是视觉冗余的（静止镜头、过渡画面）。已有系统被迫在"索引建得细（贵）"与"证据取得细（好）"之间二选一。本文把两件事拆开：索引为定位服务（粗即可），证据为推理服务（细才好），从而同时拿到效率与质量。

## 相比前方法优势

- **免训练**：纯索引构建策略，不动模型权重，即插即用于既有 video RAG 管线；
- **效率数字扎实口径**：节点数（-50~60%）、端到端时延（1.3-1.7x）、质量（~99% 保持）三个维度同时汇报，而非只报精度；
- **跨 backbone/pipeline 可移植**：摘要明确主张粒度解耦是管线级设计原则而非绑定某模型的技巧；
- 与"更狠地压缩/摘要视频"的路线相比，它不丢证据——细粒度证据仍在，只是索引层变粗。

## 局限

- **v1 无 venue、无 Comments、无代码链接**（2026-08-28 实抓）：runnable=false，复现需自实现密度合并与回扩逻辑；
- "视觉冗余合并"的收益假设视频存在大量冗余片段——高信息密度视频（快剪、监控事件密集流）上合并率与质量保持未验证；
- QA 保持"约 99%"是摘要口径，分基准明细与统计显著性需进正文核实；
- 三个基准均为 QA 型任务，对视频摘要、时刻定位等非 QA 任务的迁移未证；
- 基线为哪些 graph-based video RAG 系统摘要未列全，"1.3-1.7x 加速"的参照系需进正文确认。

## 如何用于比赛（比赛映射展开）

- **黑客松-数据与算法**：长视频理解/多模态 RAG 是黑客松高频题型，常见的死法是索引建不完或检索超时。搬两级粒度设计：粗图索引（合并冗余 chunk）定位 + 原粒度回扩取证，把内存与时延砍半而答案质量几乎无损——评委问"为什么你的系统能处理 1 小时视频"时，这就是答案；
- **实现要点**：免训练意味着全部工作量在索引构建算法（相邻 chunk 相似度判定 + 合并 + 映射表），可用现成 embedding 模型 + 图库实现，赛期内可完成；
- **引用纪律**：论文的 1.3-1.7x/99% 是其在公开基准上的数字，对外作品必须报自测值（铁律 4），论文数字仅作方法选型佐证。
