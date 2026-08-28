---
id: arxiv-2608.22652
name: Evaluating Inference-Time Defenses Against Package Hallucination in LLM-Generated Code
field: [LLM 代码生成, 软件供应链安全, 评测方法]
directions: [黑客松与数据竞赛]
published: "2026-08-23"
maturity: paper
signal:
  venue: "ASE 2026（arXiv comments: Accepted ASE 2026；页挂 citation DOI 10.1145/3832783.3837555）"
  runnable: false
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "LLM 生成代码类作品（数据分析 agent/自动写脚本/代码助手）的现场翻车点防御：给出防御-威胁模型匹配的选型先验——常规场景 Greedy 解码 + 生成后包存在性校验的权衡最好，不可信/对抗输入场景换 RAG 或 Self-Refine 迭代自校验；另附评测口径修正（把标准库模块误判为幻觉使 Python 幻觉率高估 9.4pp），可直接用于作品自评章节，避免自报数字被同样的度量错误污染"
    reuse_cost: 低
    open_source: "无（arXiv 页 2026-08-28 实抓无代码链接；但 Greedy 解码/Self-Refine/包存在性校验均为轻量推理时手段，无需论文代码即可按摘要结论落地）"
sources:
  - url: https://arxiv.org/abs/2608.22652
    title: Evaluating Inference-Time Defenses Against Package Hallucination in LLM-Generated Code
    accessed: "2026-08-28"
---

# LLM 生成代码包幻觉的推理时防御评测

> 来源：https://arxiv.org/abs/2608.22652 （arXiv 提交于 2026-08-23，cs.SE 交叉 cs.AI；comments: Accepted ASE 2026；页挂 citation DOI 10.1145/3832783.3837555；抓取日期 2026-08-28）

## 是什么

arXiv 2608.22652 对"LLM 生成代码时的包幻觉"（hallucinate 不存在的软件包，构成软件供应链攻击入口）的推理时防御做了系统评测，摘要列出四项贡献（以下均来自本次抓取的摘要页）：

1. **度量修正**：先前评测方法系统性高估幻觉率——部分语言中把标准库模块误分类为幻觉（Python 高估 9.4 个百分点）；
2. **七种推理时防御横向评测**：五种引导解码策略（Greedy、Contrastive、DoLa、Nudging、ALCD）加 Self-Refine 与 RAG 两类防御，覆盖 8 个模型、5 个家族、4 种语言（Python/JS/Ruby/Rust）共 32 个模型-语言配置；RAG 在 18/32 配置中降低包幻觉率（PHR）；
3. **提出 Package Utility（PU）度量**：衡量防御是否保留有效且任务相关的包推荐（防"防御把正常推荐也砍掉"）；综合权衡下 Greedy 解码平均表现最好；
4. **对抗压力测试**：提示注入下 PHR 飙升（最高 +45pp），Ruby 最脆弱（80.9-95.2% 模型-语言配置受影响）；对抗条件下 RAG 与 Self-Refine 优于纯解码策略。

## 解决什么问题

两个此前没对齐的问题：一是幻觉率测不准（评测器本身把标准库当幻觉，数字失真）；二是防御怎么选没有依据——引导解码、自修正、检索增强三类防御在什么威胁模型下该用哪个，缺少跨模型跨语言的横向证据。本文补上度量与选型两张表。

## 相比前方法优势

- **先修度量再评防御**：9.4pp 的标准库误判修正使后续所有对比数字可信；
- **PU 度量补盲区**：以往只看"幻觉少了没有"，不看"有用推荐是否被误杀"，PU 把两方面放进同一权衡；
- **威胁模型分层结论**：常规 vs 对抗两种条件下最优防御不同（Greedy vs RAG/Self-Refine），比"某防御全面更优"式结论更可操作；
- 覆盖面宽：8 模型 5 家族 4 语言 32 配置，含开源闭源。

## 局限

- **arXiv 页无代码链接**（2026-08-28 实抓；comments 确认 Accepted ASE 2026，但 artifact/代码仓库未见），runnable=false；
- 引导解码类防御（DoLa/ALCD 等）需访问模型 logits，闭源 API 模型上不可用——赛场若用 API 模型，实际可选防御只剩 Greedy 解码切换、Self-Refine、RAG 三类；
- Ruby 最脆弱的结论对国内赛场（以 Python 生态为主）相关性弱；
- PU 需自实现；对抗测试的攻击面限于提示注入一种；
- 摘要未给出防御带来的时延/成本代价数字，工程落地开销需进正文核实。

## 如何用于比赛（比赛映射展开）

- **黑客松-数据与算法**：任何"让 LLM 写代码"的作品（数据分析 agent、自动建模管线、代码补丁助手）演示现场最尴尬的事故之一就是 `pip install` 一个不存在的包。按本文结论搭两层防御：默认 Greedy 解码 + 生成后包存在性校验（查 PyPI/本地环境）；输入不可信或对抗主题赛道时叠加 Self-Refine 自校验或 RAG（接真实包索引文档）。成本极低、差异化明确——别人现场翻车，你有防御层且能引用论文级依据说明选型；
- **自评章节**：用本文的度量修正口径统计自己作品的包幻觉率（排除标准库误判），自报数字更可信，也更经得起评委追问；
- **引用纪律**：9.4pp/45pp 等数字仅作方法佐证，作品自报数字必须来自自测（铁律 4）。
