---
id: arxiv-2609.16309
name: 'Agentic Search Spaces for Tabular Machine Learning'
field: [LLM agents, 表格机器学习, 超参数优化, AutoML]
directions: [黑客松与数据竞赛]
published: "2026-09-14"
maturity: paper
signal:
  venue: "arXiv v1（cs.LG，页内无 venue/comments 标注）"
  runnable: false
competition_fit:
  - track: "Kaggle-竞赛"
    edge: "固定调参与集成预算下多挤出 0.6–2%（中小型回归集 2.0%）——Kaggle 决胜恰在此量级；'最强 agentic 集成超过 AutoGluon 最佳常规集成'给出可对标的集成叙事；底座公开（autogluon/tabarena 307★ 活跃维护，2026-09-16 实核），复用=自实现'LLM 逐模块提候选代码+经典 HPO 联合优化'回路"
    reuse_cost: 中
    open_source: "官方代码无（arXiv 页无链接、GitHub 检索 0 命中，2026-09-16 实抓）；复用底座 https://github.com/autogluon/tabarena 公开"
  - track: "黑客松-数据与算法"
    edge: "'让 agent 设计搜索空间而非人手调参'的管线级差异化叙事：五模块拆解（预处理/嵌入/架构/训练/推理）可直接当表格管线重构清单；现场演示 LLM agent 向 AutoGluon/TabArena 注入候选模块并在同预算下打平或超越默认空间，工程量适中且评审可见"
    reuse_cost: 中
    open_source: "同上（官方代码无，底座 autogluon/tabarena 公开）"
sources:
  - url: https://arxiv.org/abs/2609.16309
    title: 'Agentic Search Spaces for Tabular Machine Learning'
    accessed: "2026-09-16"
  - url: https://github.com/autogluon/tabarena
    title: "autogluon/tabarena——TabArena 表格 ML 活跃基准（复用底座，非论文官方代码）"
    accessed: "2026-09-16"
---

# Agentic Search Spaces for Tabular Machine Learning

> 来源：https://arxiv.org/abs/2609.16309 （arXiv v1 提交于 2026-09-14，cs.LG，作者 Renat Sergazinov、Artem Chistyakov、Sergey Pankevich、Artem Babenko；抓取日期 2026-09-16）；底座仓库 https://github.com/autogluon/tabarena （307 stars，2026-09-16 实核活跃维护）

## 是什么

arXiv 2609.16309 研究一个具体问题：**SOTA agentic AI 系统能否为成熟表格模型设计出超过模型作者默认搜索空间的扩展 HPO 搜索空间**（以下描述与数字均来自本次抓取的摘要页）：

- **方法**：把每个表格模型框成模块化管线——预处理、嵌入、架构、训练、推理五模块；agent 为每模块提出候选代码实现；经典 HPO 算法在"agent 候选 + 默认超参"的并集上**联合优化**；
- **实验**：45 数据集套件 + TabArena 基准做迁移评测；
- **结果**：平均相对增益 0.6%，中小型回归数据集升至 2.0%；增益在**相同调参与集成预算**下成立（不额外花算力）；TabArena 上 5 个模型族中 4 个 Elo 提升；两个最强 agentic 集成**超过常规模型的最佳 AutoGluon 集成**；
- **开源状态**：官方未放代码（arXiv 页无链接，GitHub 检索 0 命中，2026-09-16 实抓，runnable=false）；摘要未点名具体 agent 系统与表格模型族。

## 解决什么问题

表格 AutoML 的搜索空间由模型作者手工圈定，LLM agent 的价值长期停留在"替人写代码/调参"。本文把 agent 的贡献点**上移一层**：扩展的不是默认网格里的采样点，而是可调空间的结构边界本身（模块级候选实现），再用经典 HPO 收敛——agent 出题、HPO 判卷。

## 相比前方法优势

- **增益与预算解耦**：相同 HPO/集成预算下对比，0.6–2% 是净增益而非堆算力；
- **鲁棒于 agent 幻觉**：失败的候选实现被 HPO 联合优化自然淘汰，坏提案不致命；
- **空间可迁移**：TabArena 迁移评测表明设计出的搜索空间跨数据集有效，非逐集过拟合；
- 有"agentic 集成 > 最佳 AutoGluon 常规集成"的强对标结论，叙事直接可用。

## 局限

- **无官方代码**：复现需自建 agent 提案回路（提示工程 + 候选沙箱执行 + HPO 接线），非开箱即用；
- 平均增益 0.6% 偏薄，2.0% 仅在中小型回归子集成立——分类与大数据集上的期望要压低；
- 摘要未披露具体 agent 系统与模型族名、agent 提案的 LLM 调用成本，细节需进正文核实；
- v1 无 venue/comments，未过同行评审；
- 增益前提是作者默认空间偏保守；若底座模型空间本已放开，边际收益缩水。

## 如何用于比赛（比赛映射展开）

- **Kaggle-竞赛**：把"agent 扩搜索空间"接进自家表格工作流——LLM 对 AutoGluon/自建管线五模块各提 3–5 个候选实现，Optuna 类工具在候选+默认超参并集上联合搜索；金区（0.1–1% 分差）场景里 0.6–2% 净增益值得这份工程量；论文结论可作方案书先验依据，赛场分数必须自测（铁律 4：metrics.json）；
- **黑客松-数据与算法**：五模块拆解当表格管线重构清单；"同预算下 agentic 集成胜 AutoGluon 最佳集成"是现场可演示、评审可感知的差异化故事；
- **成本核算**：reuse_cost=中——底座公开（TabArena 活跃维护），缺的是论文的接线层；LLM 提案费与沙箱执行时间是隐藏成本，赛前先在 2–3 个公开小数据集试跑校准再上正赛。
