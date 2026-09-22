---
id: arxiv-2609.22977
name: "CASP-LLM：覆盖感知的提示选择——usage 正则替代相似度 top-K 检索（官方代码已放）"
field: [时序预测, 检索增强, 提示选择, LLM]
directions: [创新创业大赛, 数模与时序预测, 黑客松与数据竞赛]
published: "2026-09-19"
maturity: demo
venue_tier: other
reproducibility_level: medium
signal:
  venue: "EMNLP 2026 Findings（论文自述 Accepted to Findings of ACL: EMNLP 2026；findings 卷非主会正刊，24页8图15表）+ 官方仓 dadaeun09/CASP-LLM（0 stars，2026-08-28 创建后未再 push，研究代码态）"
  stars: 0
  citations_90d: 0
  runnable: true
competition_fit:
  - track: "数模-预测与评估"
    edge: "用 LLM 做时序预测管线时的检索选样问题：主流 top-K 余弦相似度无冗余控制，检索回近重复提示，使预测偏向主导形态、系统性漏掉稀有但信息量大的时段——而突变段恰是数模预测题拉分点。CASP 的 usage-tracking+saturating-gate 合成覆盖正则，零新增可学参数、即插即用；论文实证口径诚实：六个长期基准+M4 多数设定 matches-or-improves 相似度基线，但 Electricity/M4-Monthly/few-shot 长程失效，且对照实验给出可省赛期试错的负结果——『跨批次锚点使用率正则有效，MMR 式多样性重排无效』。选型时先判场景（数据是否模式单一、有无稀有事件段）"
    reuse_cost: 中
    open_source: "官方仓 https://github.com/dadaeun09/CASP-LLM（GPT-2 骨干+models/prompt.py 提示池与覆盖逻辑+6 基准脚本，0 stars 单次 push 研究代码态，2026-09-22 API 实抓）"
  - track: "黑客松-数据与算法"
    edge: "可迁移洞见超出时序：一切『检索条件化 LLM』管线（RAG/ICL/agent 记忆选样）都吃相似度检索的近重复集中化亏——『按跨请求使用率做覆盖正则、比 MMR 多样性重排更有效』的结论可直接搬进黑客松 RAG 应用做检索层差异化，零参数正则实现成本低（几十行代码），评测（命中率/覆盖度对比 top-K/MMR/覆盖正则三方案）容易做出可视化对比页"
    reuse_cost: 低
    open_source: "同上官方仓，正则逻辑集中于 models/prompt.py 可移植"
sources:
  - url: https://arxiv.org/abs/2609.22977
    title: "Beyond Similarity: Coverage-Aware Prompt Selection for Time Series Forecasting with LLMs（arXiv abs 页实抓 2026-09-22：相似度检索主导且无冗余控制→偏向主导时间形态漏掉稀有信息事件；CASP-LLM=usage-tracking+saturating-gate 合成覆盖正则、无新增可学参数；六长期基准+M4 短期多数设定 matches-or-improves，例外为 Electricity/M4-Monthly/few-shot 长程；受控实验归因跨批次使用率而非单次检索冗余——MMR 式多样化无效、跨训练正则化锚点使用率有效；均出自页面摘要原文）"
    accessed: "2026-09-22"
  - url: https://github.com/dadaeun09/CASP-LLM
    title: "dadaeun09/CASP-LLM 官方仓实抓（2026-09-22 API+README：0 stars，2026-08-28 创建/末次 push，Python，全管线代码 run.py/data_provider/exp/models(CASPLLM.py,prompt.py)/scripts(ETT×4,weather,electricity)/utils；README 自述 GPT-2 backbone+adaptive prompt-based forecasting，依赖 torch 2.5.1+transformers 4.31，sh scripts/etth1.sh 即跑）"
    accessed: "2026-09-22"
---

# CASP-LLM：提示检索别只看相似度——覆盖正则比多样性重排有效

> 来源：https://arxiv.org/abs/2609.22977 （arXiv abs 页实抓，2026-09-22；v1 提交于 2026-09-19，cs.LG/cs.CL，一作 Daeun Ji）+ https://github.com/dadaeun09/CASP-LLM （官方仓 API+README 实抓，2026-09-22）

## 是什么

LLM 时序预测中的**提示（exemplar prompt）选择**方法（摘要与官方 README 口径）：

- **问题**：prompt-based forecasting 主流用 top-K 余弦相似度检索历史片段做提示，无冗余控制——检索集中在近重复候选，预测偏向主导时间形态，漏掉稀有但信息量大的时段；
- **方法**：CASP-LLM（coverage-aware semantic prompting）把 **usage-tracking（使用率追踪）+ saturating-gate（饱和门）**合成一个**覆盖正则**，加进训练目标——**零新增可学参数**；骨干为预训练 GPT-2 + 自适应提示机制（README）；
- **实证口径（摘要自述，如实转述）**：六个长期基准 + M4 短期，多数设定 matches-or-improves 相似度基线；**例外**：Electricity、M4-Monthly、few-shot 长程；
- **受控实验归因**：失效源于**跨批次使用率水平**而非单次检索冗余——**MMR 式多样性重排无效，跨训练正则化锚点使用率有效**。

发表：EMNLP 2026 Findings（24 页 8 图 15 表）。官方代码：dadaeun09/CASP-LLM（0 stars，2026-08-28 创建后未再 push）。

## 解决什么问题

相似度检索是 ICL/RAG/提示式预测的默认规则，其近重复集中化缺陷在 RAG 领域已被多样性检索研究注意到，但在其他检索条件化管线（含提示式预测）中未被检验过（摘要口径）。本文用提示式预测做试验台，证明"选什么提示"不该只看相似度，并把修正做成训练期覆盖正则而非推理期重排。

## 相比前方法优势

- **零新增参数**：覆盖正则加在训练目标上，不改架构不增推理成本；
- **消融给出可复用的负结果**：MMR 多样性重排（推理期、逐次）无效，跨批次使用率正则（训练期、全局）有效——这个对照直接否掉了一条看起来更直觉的替代方案；
- **诚实报告失效场景**：Electricity/M4-Monthly/few-shot 长程不增益，选型可先判场景；
- 官方代码全管线放出（数据管线/实验框架/六基准脚本）。

## 局限

- **改进幅度口径为 matches-or-improves**：不是全面显著超越，三个场景明确失效——这是"特定问题的修正"而非"通用涨点器"；
- 官方仓 0 stars、创建后一次 push、无 release：研究代码态，未经验证可复跑，环境依赖较旧（transformers 4.31），复现需自下数据集与 GPT-2 权重并自行调通；
- 结论建立在与"相似度基线 LLM 预测器"的对比上：与非 LLM 的轻量数值模型（DLinear 类）孰优，摘要层未给对比；
- **库内定位**（LLM×时序族去重）：Compositional Spectral Prompts（arxiv-2609.02093）管提示**内容构造**（频谱组合），本卡管提示**检索选择**（覆盖 vs 相似度），管线阶段不同；CTRL（arxiv-2609.23257）是控制器路线与本卡无叠。本卡占"检索选样+覆盖正则"位。

## 如何用于比赛（比赛映射展开）

- **适用赛种**：数模-预测与评估（LLM 预测管线选样）；黑客松-数据与算法（RAG 检索层通用洞见）。
- **打法**：
  (a) **赛题适配判断**：数据模式单一、稀有事件段重要（负荷突变、异常交易段）→ 上覆盖正则；数据本身高噪声多模式（Electricity 类）→ 论文自证不增益，别硬上；
  (b) **正则即插即用**：训练 LLM 预测器时把 usage-tracking+saturating-gate 加进损失，消融表加一行"top-K vs MMR vs 覆盖正则"三对照——论文已替你跑过这个消融的预期结论，赛内复现即得讨论章节；
  (c) **迁移到 RAG 应用**（黑客松/数模文本题）：检索层按历史查询使用率做覆盖正则替代纯相似度 top-K，与 MMR 做对比 demo，是有论文背书的差异化点。
- **成本**：reuse_cost=中（时序用法：官方代码可跑但需调通旧环境+下数据）；正则思想迁移（RAG 用法）reuse_cost=低。
