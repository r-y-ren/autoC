---
id: arxiv-2608.24977
name: "Retrieved But Not Reliable: A Survey on Attacks, and Defenses in Retrieval-Augmented Generation"
field: [retrieval augmented generation, LLM 安全与鲁棒性]
directions: [黑客松与数据竞赛]
published: "2026-08-25"
maturity: paper
signal:
  venue: "Findings of EMNLP 2026 (ARR)"
  runnable: false
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "LLM 安全/鲁棒性主题黑客松的『作战地图』：按攻击目标（accuracy/privacy/fairness）× 防御阶段（retrieval/rerank/generation/traceback）的流水线感知分类法可直接转化为红蓝对抗作品的威胁模型章节与防御功能清单，附带的鲁棒性基准菜单免去赛期选型调研——地图型资源的价值在『省时间』而非『复现』"
    reuse_cost: 低
  - track: "Kaggle-竞赛"
    edge: "LLM 鲁棒性/安全类赛题的评估设计参考：综述把威胁模型形式化到 corpus/retriever/generator 三层并汇总鲁棒性基准与可解释性方法，可用于给防御型 submission 设计评测维度与消融口径"
    reuse_cost: 低
sources:
  - url: https://arxiv.org/abs/2608.24977
    title: "Retrieved But Not Reliable: A Survey on Attacks, and Defenses in Retrieval-Augmented Generation（arXiv abs 页，v1 2026-08-25 / v2 2026-08-27）"
    accessed: "2026-08-28"
---

# Retrieved But Not Reliable：RAG 攻击与防御综述（EMNLP 2026 Findings）

> 来源：https://arxiv.org/abs/2608.24977 （v1 提交 2026-08-25，v2 2026-08-27；cs.CR/cs.CL/cs.LG；Comments：24 页 6 图，Accepted to Findings of ACL: EMNLP 2026，经 ARR 同行评审；arXiv 页无代码链接；抓取日期 2026-08-28。本卡内容均出自本次抓取的摘要页。）

## 是什么

arXiv 2608.24977（Tran、Dang、Nguyen 等 13 人，宾州州立 Suhang Wang 挂尾）是一篇 **pipeline-aware 的 RAG 安全综述**，主张既有综述对攻击者目标、威胁模型与分阶段防御的覆盖不足，其贡献是把整个攻防地图统一到一条流水线上：

- **威胁模型形式化**：覆盖 corpus（语料库）、retriever（检索器）、generator（生成器）三层；
- **攻击按三目标组织**：accuracy（准确率破坏）、privacy（隐私泄露）、fairness（公平性侵害）——含 corpus poisoning、后门攻击等；
- **防御按四阶段组织**：retrieval → rerank → generation → traceback；
- 汇总 RAG 鲁棒性**基准**与**可解释性**方法，用于评估与解释鲁棒性。

## 解决什么问题

RAG 提升事实性、降低幻觉的同时引入了新的鲁棒性与安全风险，但攻防文献散落、口径不一；本综述提供一张"攻击目标 × 流水线阶段"的统一地图，让防御方知道自己在防什么、在哪一层防、用什么基准验证。

## 相比前方法优势

- 相对既往 RAG 安全综述（作者自述其覆盖面不足）：首次按攻击者三类目标 × 四个防御阶段做交叉组织，且威胁模型显式分层到 corpus/retriever/generator；
- 经 ARR 评审进入 **Findings of EMNLP 2026**，非单纯预印本；
- 地图型产出的复用方式是"查阅"而非"复现"——对赛队的边际成本几乎为零。

## 局限

- 综述本身无可运行代码（runnable=false 属常态而非缺陷），文中方法的可用性需逐条核到原始论文；
- 摘要页未给出收录文献数量与时效截止日，覆盖完整性无法从本次抓取确认；
- 防御证据以文献汇总为主，各防御在统一基准上的横向强弱需读者自行比对。

## 如何用于比赛（比赛映射展开）

- **黑客松（数据与算法）**：做 LLM 安全/鲁棒性主题作品时，直接以本综述的"攻击目标 × 防御阶段"矩阵为威胁模型骨架——作品文档引用一张已被同行评审背书的分类法来论证防御设计的系统性，再从其基准清单中挑一个做现场演示（如语料投毒攻击 + 分阶段拦截）。差异化不在技术复现，而在**叙事与选型的完备性**：评委看到的是全地图上的一格，而非孤立的 hack（reuse_cost=低）。
- **Kaggle**：若遇到 LLM 鲁棒性/安全 flavored 赛题，用其三层威胁模型设计评测维度与消融口径，比自造 taxonomy 更站得住（reuse_cost=低）。
