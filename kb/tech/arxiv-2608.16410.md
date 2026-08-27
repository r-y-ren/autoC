---
id: arxiv-2608.16410
name: "TRACE-CASH: Trial-History-Conditioned Reinforcement Learning for Adaptive Configuration Exploration in Time-Series CASH"
field: [时序预测, 自动机器学习, 超参数优化]
directions: [数模与时序预测]
published: "2026-08-17"
maturity: paper
signal:
  venue: arXiv
  citations_90d: 0
  runnable: false
competition_fit:
  - track: "数模-数据分析与决策"
    edge: "方法论迁移：把'模型×时间粒度×架构×训练动作'的配置搜索组织成按时间顺序验证驱动的序贯决策（利用试验历史、停滞时切换探索），替代'试几个挑最好'——41 个任务变体上 MASE/WQL 平均排名最优的背书可直接引用，直击数模评审必问的'模型与参数如何选定'章节"
    reuse_cost: "高"
  - track: "数模-预测与评估"
    edge: "'搜索过程即证据'叙事：把配置搜索的试验历史可视化（探索-利用轨迹、按时间验证的滚动对比），将调参从黑箱劳动变成可写进论文的严谨实验设计章节；工程上可将 actor-critic 降级为 bandit/序贯贝叶斯搜索实现同类思想"
    reuse_cost: "高"
sources:
  - url: https://arxiv.org/abs/2608.16410
    title: "TRACE-CASH: Trial-History-Conditioned Reinforcement Learning for Adaptive Configuration Exploration in Time-Series CASH (arXiv:2608.16410)"
    accessed: "2026-08-28"
---

# TRACE-CASH：试验历史条件化的时序预测 CASH 求解器

## 是什么

Huang、Wu 与 Tseng（2026-08-17 提交 arXiv，cs.LG）处理时序预测中的 **CASH（联合算法选择与超参数优化）**问题：时间相关选择、按时间顺序的验证与昂贵评估使搜索比常规 AutoML 更难。**TRACE-CASH** 是任务局部混合序贯优化器：分组 actor-critic 候选生成，配合模型覆盖、验证引导利用、停滞时探索的固定规则；结构上由一个**模型 actor**提出初始预测模型、三个**模型条件化 actor**分别产生时间/架构/训练动作、一个**模型特定解码器**组装最终配置。在 41 个数据集-频率任务变体上，对比随机、贝叶斯、进化、多目标与语言模型辅助六类搜索，取得 **MASE 与 WQL 双指标最低平均排名**及预定全窗口/晚窗口的最低窗口平均测试 MASE 排名（来源：https://arxiv.org/abs/2608.16410，抓取 2026-08-28）。

## 解决什么问题

时序预测的模型与超参联合搜索空间里，随机/网格搜索浪费昂贵评估、贝叶斯优化又不感知时序验证的特殊性——需要"记得试过什么"且按时间顺序验证的搜索策略。

## 相比前方法优势

- 六类搜索基线（随机/贝叶斯/进化/多目标/LLM 辅助）上的双指标平均排名最优，验证面广（41 任务变体）；
- 显式处理时序 AutoML 的独有约束（时间相关动作、按时间顺序验证）；
- 混合设计（学习 + 规则）使停滞时的探索有保底，避免纯 RL 的不稳定。

## 局限（如实标注）

- **未找到开源实现**：arXiv 页（2026-08-28 实抓）无任何代码链接，runnable=false，复现需自建；
- 完整复刻分组 actor-critic + 多 actor 解码器的工程量大，赛期现实路径是**借思想不借架构**（序贯搜索 + 按时间验证 + 试验历史条件化）；
- maturity: paper；单篇 arXiv 无同行评审信号标注于摘要页。

## 如何用于比赛

1. **数模-数据分析与决策类（主用）**：预测类赛题的"模型选择与调参"章节按此文方法论重写——配置空间显式定义为"模型×时间粒度×架构×训练"四层、验证严格按时间切分、记录完整试验历史并展示探索-利用过程；引用其 41 任务平均排名结论作方法学背书（reuse_cost 高：无代码，思想级复用）。
2. **数模-预测/评估类**：工程落地取降级实现——以序贯贝叶斯/bandit 搜索承载"试验历史条件化"内核，Optuna 等现成框架 + 自定义按时间验证即可近似，成本低一个量级；
3. 落地注意：不要在论文里声称复现 TRACE-CASH 本身（无代码），如实写"受其启发的搜索策略设计"。
