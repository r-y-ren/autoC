---
id: arxiv-2609.17895
name: "TabPFN-3.5：表格基础模型新旗舰（时序/非i.i.d./多模态列全面扩张）"
field: [表格基础模型, 时序预测, AutoML]
directions: [数模与时序预测]
published: "2026-09-15"
maturity: product
venue_tier: arXiv
reproducibility_level: high
signal:
  venue: "arXiv（技术报告，Prior Labs）+ GitHub PriorLabs/TabPFN（7993 stars，Apache-2.0，2026-09-20 API 实抓）"
  stars: 7993
  runnable: true
competition_fit:
  - track: "数模-预测与评估"
    edge: "国赛/研赛/电工杯表格类预测题（分类/回归/小样本/缺失值）的默认强基线：TabArena 标准表格预测 SOTA，且明确扩张到赛题数据的真实形态——非 i.i.d. 的时序/分组划分、字符串/文本/图像列、高基数类别特征、宽表；TabPFN-3.5-Fast 推理提速至 3 倍适配赛期算力。免调参出强结果，把省下的时间投给特征工程与论文写作"
    reuse_cost: 低
    open_source: "https://github.com/PriorLabs/TabPFN（pip install tabpfn，README 已文档化 v3.5 与 v3.5-fast 用法，2026-09-20 实抓）"
  - track: "Kaggle-竞赛"
    edge: "表格赛与部分时序任务（论文自述 time-series forecasting 增益延续到任务专用 harness）的零样本/低成本成员模型；小数据场景下与 GBDT 集成互补，是其相对 XGBoost/LightGBM 栈的核心差异点"
    reuse_cost: 低
    open_source: "https://github.com/PriorLabs/TabPFN"
sources:
  - url: https://arxiv.org/abs/2609.17895
    title: "TabPFN-3.5: Technical Report（arXiv export API 实抓：2026-09-15 提交，摘要+无 Comments；TabArena SOTA、非i.i.d.扩张、Fast/Plus/Thinking 三变体口径均出自摘要原文）"
    accessed: "2026-09-20"
  - url: https://github.com/PriorLabs/TabPFN
    title: "PriorLabs/TabPFN 仓库实抓（GitHub API 2026-09-20：7993 stars，Apache-2.0，README 含 TabPFN-3.5 架构图与 ModelVersion.V3_5_FAST 用法，PyPI badge 在列）"
    accessed: "2026-09-20"
---

# TabPFN-3.5：表格基础模型新旗舰，把"非 i.i.d.、宽表、多模态列"纳入默认能力

> 来源：https://arxiv.org/abs/2609.17895 （arXiv export API 实抓，抓取日期 2026-09-20；开源状态经 https://github.com/PriorLabs/TabPFN GitHub API 实抓核实。以下分析基于本次抓取的摘要与仓库元数据）

## 是什么

Prior Labs 的新一代表格基础模型技术报告（摘要口径）：TabPFN-3.5 显著超越前代 TabPFN-3 与全部现有基线，在 TabArena 标准表格预测上刷新 SOTA，并把能力边界扩张到实践数据的真实形态——**非 i.i.d. 数据（时序/分组划分）、含字符串/文本/图像的表、高基数类别特征、多特征宽表**。增益延续到任务专用 harness：关系数据 SOTA 与更强的时序预测。四个变体：标准版、推理提速至 3 倍的 **TabPFN-3.5-Fast**、多模态/文本/日期处理更强但含专有推理优化的 **TabPFN-3.5-Plus**、推理时算力扩展的 **TabPFN-3.5-Thinking**（较 3-Thinking 快至 12 倍）。

## 解决什么问题

表格类赛题/业务数据极少满足 i.i.d. 假设：时序泄漏、分组依赖、混杂列型、宽表高维是常态，此前表格基础模型在这些"脏形态"上不可靠，赛队只能退回 GBDT 手工栈。TabPFN-3.5 把这些形态纳入 SOTA 能力圈，等于给"不调参直接出强预测"的默认基线升级了一代。

## 相比前方法优势

- 相比 TabPFN-3：标准预测 SOTA + 四类真实形态扩张 + Fast 3 倍推理提速（保持大部分精度）；
- 相比 GBDT（XGBoost/LightGBM）路线：零训练免调参、小样本强、可作异质集成成员——但其对超大数据的适用边界需按官方文档核实（README 载明 CPU 上 TabPFN-3/3.5 限 5000 样本，2026-09-20 实抓）；
- 开发生态成熟：pip install tabpfn，Apache-2.0，7993 stars，3.5/3.5-fast 已进 README 用法文档。

## 局限

- **性能口径为厂商自报**：TabArena 排行由 Prior Labs 关联方维护发布，第三方独立复验尚未见（本卡止于摘要层，未读正文实验表）；
- TabPFN-3.5-Plus 含**专有推理优化**（闭源部分），Thinking 变体推理时算力开销高——赛期预算内主要可用的是标准版与 Fast；
- 技术报告无同行评审 venue（Comments 无，2026-09-20 实抓）；
- CPU 上 5000 样本上限意味着中大数据集仍需 GBDT 或 GPU。

## 如何用于比赛（比赛映射展开）

- **适用赛种**：数模-预测与评估（一切表格回归/分类/评价类题）；Kaggle-竞赛（表格赛、概率型时序赛）。
- **打法**：
  (a) **默认基线位**：拿到表格数据先 `pip install tabpfn` 出 TabPFN-3.5(-Fast) 基线，再决定要不要上手工栈——把 GBDT 调参时间换成特征工程与消融；
  (b) **非 i.i.d. 场景**：赛题要求按时间/分组划分验证时，直接用其官方支持而非自行防泄漏改造；
  (c) **集成成员**：与 LightGBM/XGBoost 异质集成，通常稳定提升——答辩时"参数化先验 + 梯度提升"两条路线互补是成熟叙事。
- **成本**：reuse_cost=低——pip 安装即用；注意事项仅一条：超样本上限时切换 Fast 或退回 GBDT。
