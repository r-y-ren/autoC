---
id: arxiv-2609.13956
name: "Tabby：全开源配方时序基础模型（145M 三合一骨干+冻结prompt-tuning）"
field: [时序基础模型, 概率预测, 开源配方]
directions: [数模与时序预测]
published: "2026-09-12"
maturity: demo
venue_tier: arXiv
reproducibility_level: high
signal:
  venue: "arXiv（43页技术报告）+ GitHub huawei-noah/trustworthyAI（1142 stars，Apache-2.0；Tabby 于顶层 TabbyTSFM 目录发布，2026-09-20 API 实抓）"
  stars: 1142
  runnable: true
competition_fit:
  - track: "数模-预测与评估"
    edge: "赛题要『带区间的预测』或『预测+异常检测』二合一时的免训练选项：145M 参数 encoder-only patch Transformer、8192 长上下文、概率（分位数）输出，单卡可跑；prompt-tuning 模块在冻结预训练权重上做域内适配，是赛期数据量小、从头训练不可行时最现实的 TSFM 定制路径；GIFT-Eval/TIME 零样本 competitive 口径给了选型安全垫"
    reuse_cost: 中
    open_source: "https://github.com/huawei-noah/trustworthyAI（TabbyTSFM 目录：训练管线+权重，论文 comment 自述 release）"
  - track: "Kaggle-竞赛"
    edge: "MASE/CRPS 类概率时序赛的集成成员与 anomaly detection 辅助任务复用——同一骨干三任务（预测/UCR 分类/TSB-AD-U 零样本异常检测）切换，省赛期工程量"
    reuse_cost: 中
sources:
  - url: https://arxiv.org/abs/2609.13956
    title: "Tabby: An Open Pretraining Recipe for Time Series Foundation Models（arXiv export API 实抓：2026-09-12，Comments『43 pages, 3 figures, 32 tables. Technical report』；架构/语料/训练目标/145M/8192 上下文/开源声明均出自摘要原文）"
    accessed: "2026-09-20"
  - url: https://github.com/huawei-noah/trustworthyAI
    title: "huawei-noah/trustworthyAI 仓库实抓（GitHub API 2026-09-20：1142 stars，Apache-2.0，顶层目录含 TabbyTSFM）"
    accessed: "2026-09-20"
---

# Tabby：把时序基础模型的完整配方开源出来

> 来源：https://arxiv.org/abs/2609.13956 （arXiv export API 实抓，抓取日期 2026-09-20；开源状态经 GitHub API 核实 trustworthyAI 顶层 TabbyTSFM 目录。以下分析基于本次抓取的摘要原文）

## 是什么

华为诺亚的开源时序基础模型技术报告：Tabby = 长上下文概率时序基础模型 + **完整开放的建设配方**。架构采用 encoder-only patch Transformer，贡献集中在数据与训练流程：预训练语料 = 扩充真实语料（GIFT-Eval-Pretrain+ 与 BLAST）+ 合成数据（KernelSynth 与 CauKerV2——后者是基于随机采样结构因果模型的在线生成器）；训练 = 渐进收敛调度（产出可复用的中间 checkpoint）+ 中间层深分位数监督目标。145M 骨干支持 8192 观测长度上下文，一个骨干服务预测、分类、异常检测三任务；prompt-tuning 模块在冻结权重上进一步提升域内预测。GIFT-Eval 与分布外 TIME 基准上零样本预测 competitive。训练管线与模型开源在 huawei-noah/trustworthyAI（2026-09-20 API 实抓确认顶层 TabbyTSFM 目录存在，Apache-2.0）。

## 解决什么问题

TSFM 领域普遍"只放权重不放配方"，社区无法复现或审计预训练过程；同时多数 TSFM 只做预测单一任务。Tabby 用全开源配方回答"一个可复现的 TSFM 是怎么造出来的"，并让单一骨干覆盖三类时序任务。

## 相比前方法优势

- **配方级开源**（数据构成+训练调度+监督目标全部披露）而非仅权重发布——同代 TSFM 报告中少见；
- **一骨干三任务**：预测 + UCR 分类 + TSB-AD-U 零样本异常检测，赛队学一次 API 覆盖多题型；
- **prompt-tuning 冻结适配**：域内提升不需要微调整骨干，显存与算力门槛低；
- 145M 规模单卡可部署，8192 长上下文覆盖多数赛题窗口。

## 局限

- 零样本性能口径是 **competitive（有竞争力）而非 SOTA**——输给 Chronos-2/TimesFM 等头部模型的场景需赛内自测；
- 1142 stars 属 trustworthyAI 多项目混合仓库，非 Tabby 专属热度信号（2026-09-20 实抓口径）；
- 预训练配方对赛队价值有限（赛期内不可能预训练），真正可用的是权重+prompt-tuning；
- 本卡止于摘要层，TabbyTSFM 目录内的许可与权重文件完整性未逐项核验。

## 如何用于比赛（比赛映射展开）

- **适用赛种**：数模-预测与评估（要预测区间的题：发电/负荷/环境/客流）；Kaggle-竞赛（概率时序赛、含异常检测的混合题）。
- **打法**：
  (a) **零样本先行**：赛题数据下载后先跑 Tabby 零样本分位数预测作基线，再决定是否值得训练专用模型；
  (b) **prompt-tuning 定制**：数据量中等、域性强（如某省负荷）时，冻结骨干+prompt-tuning 是赛期内唯一可完成的"定制 TSFM"路径——这是它相对闭源 TSFM 的核心差异化；
  (c) **异常检测搭车**：预测题里评委常追问异常点处理，同一骨干直接出零样本异常检测作论文附加分析。
- **成本**：reuse_cost=中——权重与管线可得，但需自行部署环境、验证权重完整性并调 prompt-tuning；不像 pip 库那样开箱即用。
