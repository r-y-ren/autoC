---
id: arxiv-2608.23965
name: "RAGSentinel: Certifiable Geometric Consensus for Robust Retrieval-Augmented Generation"
field: [retrieval augmented generation, LLM 安全与鲁棒性]
directions: [黑客松与数据竞赛]
published: "2026-08-25"
maturity: paper
signal:
  venue: "EMNLP 2026 Main"
  runnable: false
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "LLM 安全主题黑客松的『带证书的防御』组件：training-free/label-free/黑盒适用（只需一个代理编码器，不碰 RAG 系统内部），现场可演示『语料投毒 → 隐态几何离群 → 拦截 + 恢复证书』闭环；在诚实多数 + 表征分离条件下可证明精确恢复无毒多数上下文——『有理论保证的防御』比启发式过滤是硬差异化，且对抗已知流水线的自适应攻击者仍稳"
    reuse_cost: 中
sources:
  - url: https://arxiv.org/abs/2608.23965
    title: "RAGSentinel: Certifiable Geometric Consensus for Robust Retrieval-Augmented Generation（arXiv abs 页，v1 2026-08-25）"
    accessed: "2026-08-28"
---

# RAGSentinel：RAG 投毒防御的可认证几何共识

> 来源：https://arxiv.org/abs/2608.23965 （v1 提交 2026-08-25，cs.CR/cs.AI/cs.IR/cs.LG；Comments：To appear in EMNLP 2026 Main；arXiv 页无代码链接，2026-08-28 网络检索亦未发现官方开源仓；抓取日期 2026-08-28。本卡内容均出自本次抓取的摘要页与检索结果。）

## 是什么

arXiv 2608.23965（Quan、Gao、Xia、Fang、Liu）针对 RAG 的知识投毒攻击（攻击者向知识库注入恶意文档，混入上下文窗口诱导模型给出定向错误答案）提出 **RAGSentinel**：

- **training-free、label-free、对黑盒 RAG 系统适用**的检索后防御；
- 机制：用一个**代理编码器**度量检索文档引起的查询条件化隐态偏移，**剥离共享主题方向**后，把中毒文档识别为相对**鲁棒多数共识**的几何离群点；
- **可认证保证**：在诚实多数假设 + 表征级分离条件下，**证明能精确恢复出无毒的多数规模上下文**；
- 实验：3 个 QA 数据集 × 3 个 LLM 家族 × 多种投毒攻击，攻击成功率持续压低、干净精度有竞争力，且对**完全知悉流水线的自适应攻击者**仍具韧性。

## 解决什么问题

现有检索后防御（基于指令遵从、参数知识或文本级一致性）会被自适应攻击者模仿或绕过——RAGSentinel 换到几何/共识视角，给出无法靠"模仿防御风格"攻破的可认证防线。

## 相比前方法优势

- 防御信号从"文本行为"换到"隐态几何"：文本级一致性可被攻击者仿造，隐态偏移的表征分离更难绕过（实验含全知自适应攻击者）；
- **证书式保证**是质的差异：多数现有防御只有经验攻击成功率，RAGSentinel 在明确假设下给恢复性证明；
- 黑盒 + 免训练 + 免标签：部署面比需要微调或白盒访问的防御宽得多。

## 局限

- **无官方代码**：arXiv 页无链接，本次网络检索未发现公开实现——runnable=false，复用需自行实现（代理编码器 + 主题方向剥离 + 鲁棒共识，均无需训练，工程量中等）；
- 保证依赖两个前提：**诚实多数**（中毒文档不过半）与**表征级分离**条件——不满足时证书不成立，实际语料库是否满足需自验；
- 防的是检索后投毒一类威胁，不覆盖综述（arXiv 2608.24977）里隐私泄露/公平性等其他目标；
- EMNLP 2026 Main 接收，但摘要口径为作者自报。

## 如何用于比赛（比赛映射展开）

- **黑客松（数据与算法）**：LLM 安全主题（prompt injection / 语料投毒防线）作品的核心组件。演示脚本：现场向知识库注入定向投毒文档 → 基线 RAG 被带偏 → RAGSentinel 以几何共识拦截并输出"恢复证书"。评审叙事的差异化有两层：**(1) 免训练/免标签/黑盒适用**意味着接任意现成 RAG 即可，赛期工程量可控；**(2) 可认证保证**——"我们的防御在 X 条件下有恢复性证明"远比"我们过滤掉了一些坏文档"硬。论文自带的"对抗全知自适应攻击者仍稳"的实验设计也可直接抄成现场的对抗评测环节（reuse_cost=中：无官方实现，但全程无需训练，代理编码器可用现成句子编码器替）。
