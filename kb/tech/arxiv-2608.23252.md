---
id: arxiv-2608.23252
name: "The Laws of Context Allocation: Causal Measurement and Closed-Loop Orchestration in Generative Search"
field: [检索增强生成, 上下文工程, LLM评测]
directions: [黑客松与数据竞赛]
published: "2026-08-24"
maturity: paper
signal:
  venue: arXiv
  runnable: true
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "RAG 作品的两处即插差异化：a) 评测口径升级——用 leave-one-out 因果探针量化『生成器真实用了哪篇证据』替代相关性代理（论文称标准代理在 hard negatives 上灾难性失效，即 diagnostic illusion），评委面前的方法论故事与真实调优依据双收；b) 预算分配律——把『一次堆宽上下文』改为『窄上下文 × 多次迭代生成』，论文量化组合召回 +16.7~20.5 绝对百分点"
    reuse_cost: "低"
    open_source: "https://github.com/PeiYangLiu/ascp"
  - track: "Kaggle-竞赛"
    edge: "LLM/RAG 类赛题的 test-time 推理预算分配策略与消融证据：官方 run_experiment.py 可直接驱动（--dataset/--k/--n-generations），冻结超参配置作起点；探针测量数据可当特征重要性/证据引用类赛题的中间证据"
    reuse_cost: "中"
    open_source: "https://github.com/PeiYangLiu/ascp"
sources:
  - url: https://arxiv.org/abs/2608.23252
    title: "The Laws of Context Allocation (arXiv:2608.23252)"
    accessed: "2026-08-28"
  - url: https://github.com/PeiYangLiu/ascp
    title: "PeiYangLiu/ascp — 官方代码（MIT，含分析级统计复现与 HF 数据集链接）"
    accessed: "2026-08-28"
---

# 上下文分配律：生成式搜索的因果测量与闭环编排

## 是什么

Liu, Wang, Liang, Ye（2026-08-24 提交 arXiv，cs.LG/cs.CL/cs.IR，v1 无会议标注）针对生成式搜索/RAG 做了两件事：

1. **因果测量**：提出 leave-one-out 反事实探针，隔离生成器对每篇检索文档的真实依赖并校准注意力稀释，暴露"诊断幻觉"（diagnostic illusion）——标准相关性代理在 hard negatives 上灾难性失效；
2. **分配律**：用去混杂的因子网格证明"单次加宽上下文"是被相关性衰减惩罚的陷阱；固定推理预算下跨顺序生成的**迭代分配**带来 16.7–20.5 绝对百分点的组合召回增益（验证至 32B 模型）；统一为闭环次模调度器 + 归因引导对比解码器，优于经典开环基线。

官方工件：GitHub（MIT）+ HuggingFace 数据集 `PeiyangLiu/ascp-context-attribution` 发布探针原始测量（11,520 probe 行 / 54,100 归因行 / 1,200 利用率行）。

## 解决什么问题

RAG 系统两个瓶颈：证据利用率测量失真（业界普遍用"检索命中率/相关性"代理"生成器真用没用"）与上下文预算分配次优（盲目加宽上下文窗口）。

## 相比前方法优势

- 测量与编排**解耦且各自可独立复用**：探针只要能跑模型前传就能用（k+1 次 teacher-forced 前传/查询），调度器可在自有管线上重实现；
- 收益量化扎实：+16.7~20.5 绝对百分点召回增益、规模验证到 32B；
- 工件完整度高：论文表格/图形可用笔记本纯 CPU 复现（MIT），超参冻结于 40-query 开发集一次性确定。

## 局限（如实标注）

- LOO 探针每查询成本 k+1 次前传——评测成本随文档数线性放大，赛场只能抽样使用；
- 全管线复现（生成侧）需 GPU + torch/transformers/vllm；免 GPU 的仅是分析级统计部分；
- v1 无 venue、无 Comments（纯 arXiv 预印本，未经会议评审）；
- 实验任务集中在开放域问答组合（ASQA / QAMPARI / ELI5 / 食谱 / HotpotQA），法规、医学等领域文档 RAG 未验证；
- maturity: paper。

## 如何用于比赛

1. **黑客松-数据与算法（主用）**：任何 RAG 问答/文档作品两处即插增益：a) 把评测口径从"检索 top-k 命中"升级为 LOO 因果利用率——工程量低（k+1 次前传的脚本），既是答辩差异化叙事（"我们测量了生成器真实用了什么，而非检索器召回了什么"），又是真实调优依据（找到被稀释的关键证据）；b) 按分配律把预算从"30 篇塞一次生成"改为"窄上下文 × 多次迭代生成"，有论文级数字背书。
2. **Kaggle-竞赛**：LLM/RAG 类赛道（检索问答、证据引用）的 test-time 预算分配策略：官方 `run_experiment.py` 直接驱动，冻结超参作起点；探针输出可作证据引用类赛题的中间特征。
3. 风险控制：收益数字出自开放域 QA 语料，赛场领域分布偏移需小规模自测；探针成本在长文档集上按题抽样。
