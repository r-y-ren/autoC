---
id: arxiv-2608.26385
name: "Why RAGs Hallucinate: Penalty-Aware Evaluation of Retrieval-Augmented Generation Systems with Knowledge-Gap Canaries"
field: [RAG, 评测方法, 幻觉检测]
directions: [黑客松与数据竞赛]
published: "2026-08-26"
maturity: paper
signal:
  venue: "arXiv（厂商技术报告，CustomGPT.ai）"
  stars: 0
  runnable: true
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "RAG 赛题自评与答辩方法论：knowledge-gap canary（从知识库可验证构造『答案不在库里』的问题集）+ 非对称评分（对+1/错-4/弃权0）证明『系统知道何时不该答』——实测三种商用 RAG 答题准确率聚集 97-98% 而 canary 违规率差六倍（16.7% vs 98.1%），用该指标可把『准确率差不多』的同质化对比变成『我们不瞎答』的硬差异化；失败归因管线再定位检索/生成/弃权短板"
    reuse_cost: 低
    open_source: "https://github.com/adorosario/why-rags-hallucinate"
sources:
  - url: https://arxiv.org/abs/2608.26385
    title: "Why RAGs Hallucinate: Penalty-Aware Evaluation of Retrieval-Augmented Generation Systems with Knowledge-Gap Canaries"
    accessed: "2026-08-28"
  - url: https://github.com/adorosario/why-rags-hallucinate
    title: "论文配套审计仓库（gh api 实核：Python/MIT，src+scripts+tests+results 齐备，2026-08-16 最后 push，0 stars）"
    accessed: "2026-08-28"
---

# Why RAGs Hallucinate：RAG 的罚感感知评测框架与知识缺口金丝雀

> 来源：https://arxiv.org/abs/2608.26385 （arXiv v1 提交于 2026-08-26，cs.CL 跨 cs.AI，作者 Do Rosario、Younes、Pires，机构 CustomGPT.ai；Comments"13 pages, 1 figure, 5 tables"并给出代码/日志/裁判票仓 github.com/adorosario/why-rags-hallucinate；仓库 2026-08-28 经 gh api 实核存在；抓取日期 2026-08-28）

## 是什么

arXiv 2608.26385 提出针对已部署 RAG 产品的 **penalty-aware 评测框架**（以下均来自本次抓取的摘要页与配套仓库 README）：

- 三件套：(i) **非对称评分**（对 +1、错 -4、弃权 0，弃权由 80% 置信阈值触发）；(ii) **knowledge-gap canaries**——答案可验证地不在知识库中的问题，任何回答都必为参数记忆的无 grounding 生成；(iii) **失败归因管线**，把失败分到检索、生成、弃权策略三层；
- 实测：SimpleQA-Verified 1,000 题 × 3 系统 + 1 无检索基线 × 3 重复，跨族三裁判（GPT+Claude+Gemini）盲评，98.9% 一致率；
- 结果（README 结果表，2026-08-28 实抓）：三商用 RAG **答题准确率聚集**（0.866–0.968，README 述答题时准确率 97.0–98.0%），**canary 违规率差近六倍**（CustomGPT.ai 16.7% vs Gemini 98.1%）；无检索基线 penalty-aware 得分 -1.933；penalty-aware 排名与 volume 排名相反，且 k=1..9 罚值范围内稳定；
- README 声称论文每个数字均可从仓库内审计日志重算（含 configs、transcripts、judge votes）。

## 解决什么问题

volume-based accuracy **奖励瞎猜**：一个"有问必答"的系统在传统准确率上压过"库不支持时选择弃权"的系统——摘要引 Kalai et al. (2025) 的 confidence-target 分析作为立论基础。已部署 RAG 产品缺一个把"何时不该答"计入得分的评测口径，幻觉被准确率指标系统性掩盖。

## 相比前方法优势

- **canary 是可验证构造的压力测试**：不像通用幻觉基准依赖外部真值对齐，canary 只要求"答案不在库内"这一可程序化验证的属性，任何领域的知识库都能自造；
- **非对称评分使弃权理性化**：传统 0/1 计分下弃权与答错同值或更差，该框架给出"该弃权时弃权"的量化激励，且结论对罚值鲁棒（k=1..9 重排序不变）；
- **归因到层**：检索失败/生成失败/弃权策略失败分开计账，比单一总分更可操作——知道该修检索器还是该修置信阈值。

## 局限

- **v1 无同行评审 venue**，且出品方 CustomGPT.ai 是被测商用 RAG 之一（其系统 canary 违规率 16.7% 最优）——存在利益相关的自评语境，数字宜作参考而非定论；
- **单一基准与语言**：全部实测在 SimpleQA-Verified（英文事实问答）上，中文政策库/领域库场景需自构 canary 集，框架的跨域有效性未在其内验证；
- **仓库社区验证缺位**：2026-08-28 实核 0 stars、2026-08-16 最后 push 的个人新仓（MIT，文件结构完整含 tests），无第三方复现记录；
- 评测对象为**商用 RAG 产品**而非开源自建管线，赛队自建系统的绝对数字不可直接对标。

## 如何用于比赛（比赛映射展开）

- **适用赛种**：黑客松数据与算法题中一切 RAG/知识库问答项目的自评与答辩。
- **打法**：
  (a) **赛期自造 canary 集**：从赛题知识库抽样事实，程序化扰动（替换实体/数值/时间）或选取库外事实，构造"答案可验证不在库内"的问题集，套用本仓评分脚本跑自家系统；
  (b) **答辩差异化**：放对比图——"对手系统准确率与我们相当（~97%），但 canary 违规率 60%+，我们 20% 以下"——在评审听腻了准确率数字时，"知道自己不知道"是稀缺叙事；
  (c) **迭代指引**：用归因管线区分"检索没召回"与"召回了仍编造"，分别对应改索引/改 prompt 与加置信阈值弃权。
- **成本**：reuse_cost=低——框架代码完整（src/scripts/tests/results 齐备、requirements.txt 给出），无训练，主要工作量是自构领域 canary 集（数百题量级即可支撑答辩口径）。
