---
id: arxiv-2609.21573
name: "Micro-Collaborative Poisoning: A Distributed Attack on RAG Systems"
field: [retrieval augmented generation, RAG 安全, 对抗攻击]
directions: [创新创业大赛, 黑客松与数据竞赛]
published: "2026-09-18"
maturity: paper
venue_tier: workshop
reproducibility_level: medium
signal:
  venue: "arXiv（ESORICS 2026 LLM4CyberSecurity Workshop 录用）"
  runnable: false
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "RAG 攻防类题目的进攻方方法论：把『假主张拆成多篇局部可信文档、靠弱对抗信号累积生效』的攻击在标准 RAG 栈上复现（19 页论文方法可照做），现场演示『逐篇审查全干净、合在一起答案被带偏』——比单文档投毒的常规演示高一个认知档位；论文 108 配置的结论直接当防御清单用：控制 top-k、提高干净库多样性、换强检索器都能压攻击成功率"
    reuse_cost: 中
  - track: "双创-文书与申报"
    edge: "企业知识库/RAG 产品数据安全的供应链叙事：知识库内容源若被低质/恶意内容分片渗透，文档级人工审查挡不住（可见性分析：分布式投毒的显式投毒特征比直接投毒更弱）；ESORICS 2026 workshop 录用给出同行评审背书，支撑『语料库级审计而非文档级审查』的产品差异化主张——企业 RAG 落地叙事里少见的具体威胁模型"
    reuse_cost: 低
sources:
  - url: https://arxiv.org/abs/2609.21573
    title: "Micro-Collaborative Poisoning: A Distributed Attack on RAG Systems（arXiv abs 页，v1 2026-09-18，Pereira/Maia/Praça，Comments：19 pages，ESORICS 2026 LLMs for Cybersecurity Workshop）"
    accessed: "2026-09-22"
---

# Micro-Collaborative Poisoning：把一条假主张拆散进多篇"局部可信"文档的 RAG 分布式投毒

> 来源：https://arxiv.org/abs/2609.21573 （v1 提交 2026-09-18，cs.CR/cs.AI；Comments：19 pages, 3 images, 4 tables，录用于 ESORICS 2026（第 31 届欧洲计算机安全研究 Symposium）的 2nd Workshop on the Use of Large Language Models for Cybersecurity；页面无代码链接；抓取日期 2026-09-22。本卡内容出自本次抓取的摘要页。）

## 是什么

arXiv 2609.21573（Pedro Pereira、Eva Maia、Isabel Praça）提出 **Micro-Collaborative Poisoning**——针对 RAG 系统的分布式投毒攻击：不把假主张集中塞进单篇恶意段落，而是**拆散到多篇各自看起来局部可信的文档**里，每篇只携带一块弱对抗信号，靠检索时多篇同时入 context 的**信号累积**让模型输出假目标主张。评测覆盖 **108 种 RAG 配置**（数据集、检索器架构、检索深度 top-k、数据库组成、被投毒数据库数量、生成模型的组合网格），发现：

- 攻击生效靠弱信号的累积而非"单篇毒文主导"；
- **top-k 越大、投毒库越多，攻击越容易成功**；干净数据库多样性越高、检索器越强，攻击被削弱越多；
- 可见性分析：**逐篇隔离审查难以发现**——分布式投毒留下的显式投毒特征比直接投毒更弱。

## 解决什么问题

现有 RAG 投毒防御与审计大多按"找出那篇毒文"的单点威胁模型设计（文档级过滤、异常段落检测）。本文给出反例：攻击者根本不需要任何一篇文档可疑——每篇单独审都干净，危害产生于检索组合层面的共现。这把 RAG 安全的审查单位从"文档"推向"语料库组合"，也为防御侧给出可操作的杠杆（top-k 纪律、库多样性、检索器强度）。

## 相比前方法优势

- 威胁模型升级：单文档投毒 → 分布式累积投毒，逐篇审查天然失效，比常见"塞一篇毒段落"的演示更贴近真实供应链渗透（多条低质来源各自合规）；
- 证据是网格化的：108 配置系统变化六个因子，结论是趋势性的（top-k/库数正向、多样性/检索器强度负向），不是单点 cherry-pick；
- 同行评审背书：ESORICS 2026 workshop 录用（安全主流会议的 workshop），在 RAG 攻击类 arXiv 预印本里证据等级偏高；
- 防御结论直接可用：文献同时给出四个能压攻击成功率的工程旋钮，攻击与防御一体两面。

## 局限

- 无代码发布（arXiv 页无仓库链接，GitHub 检索无官方实现，2026-09-22 实查），复现需按论文自行搭建 108 配置级别的评测或其小子集；
- workshop 短文级录用，攻击目标限于"让假主张被采信"类知识篡改，未覆盖指令注入型 RAG 攻击；库内亦无直接同题卡可比（agent 记忆投毒线是另一攻击面）；
- 摘要未报告绝对成功率数值与防御的具体代价（压攻击的旋钮对正常检索召回的损失需读正文确认）；
- "弱信号如何写才局部可信"的对抗文案构造依赖人工/模型辅助，规模化成本论文未充分讨论。

## 如何用于比赛（比赛映射展开）

- **黑客松（数据与算法）**：做 RAG 应用赛题时的攻防自证——先用论文方法在小语料上复现分布式投毒（把一条假事实拆进 5-10 篇正常文风文档），再逐项启用防御（top-k 从大收小、混入多样干净库、换 bge/强检索器、语料来源审计），现场展示攻击成功率随防御旋钮衰减的曲线；相比只演示"RAG 能答对"的作品，带着已知攻击模式做防御闭环的队伍在安全向评审里差异化明显（reuse_cost=中：方法可照做，需自建评测集）。
- **双创（文书与申报）**：企业知识库/RAG 产品的数据安全章节——用"每篇文档都过审 ≠ 语料库安全"的威胁模型论证产品需要语料供应链审计（来源白名单、库多样性、检索组合监控），引用 ESORICS workshop 录用与 108 配置实证增加说服力；对教育、政务、医疗等强合规行业的 RAG 落地方向，这是少有的具名威胁证据（reuse_cost=低：叙事直接引用，无需复现）。
