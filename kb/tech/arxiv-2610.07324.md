---
id: arxiv-2610.07324
name: "Scale-Invariant Training for Time Series Foundation Models（ScaleIn：损失侧尺度不变训练）"
field: [时序预测, 时序基础模型, 训练技巧]
directions: [数模与时序预测]
published: "2026-10-05"
maturity: paper
venue_tier: arXiv
signal:
  venue: arXiv
  runnable: false
competition_fit:
  - track: "数模-预测与评估"
    edge: "配方级免费精度：凡赛题用到 TSFM 微调（Chronos/TimesFM 等）或从头训练监督预测器，把损失从反归一化后的原尺度目标改到缩放后目标上计算即为一行改动——论文实证 24 组 TSFM×基准全降 MASE（GIFT-Eval 平均 -18.8%、M-competitions -21.9%），直接消灭'实例归一化尺度污染梯度'这一隐性误差源；答卷中可作'训练配方改进'章节的消融点（开/关 ScaleIn 各跑一遍）"
    reuse_cost: "低"
    open_source: "无官方仓；改动一行即可在任一开源 TSFM 训练循环落地（如 Chronos 官方框架 github.com/amazon-science/chronos-forecasting，库内 arxiv-2608.11359 卡 2026-08-28 实抓核验含 Chronos-2 与 HF 权重）"
  - track: "Kaggle-竞赛"
    edge: "时序赛题微调基础模型时的默认训练技巧：异构 scale（不同门店/序列量级差异大）正是 Kaggle 时序赛数据常态，ScaleIn 消融实验可作方案鲁棒性论证"
    reuse_cost: "低"
sources:
  - url: https://arxiv.org/abs/2610.07324
    title: "Scale-Invariant Training for Time Series Foundation Models (arXiv:2610.07324, 摘要页实抓)"
    accessed: "2026-10-10"
---

# ScaleIn：时序基础模型的尺度不变训练（损失算在缩放后目标上）

## 是什么

Stepka、Potosnak、Olivares、Dubrawski 等（2026-10-05 提交 arXiv:2610.07324，cs.LG，v1）提出的训练配方修正：TSFM 训练语料中各序列 scale（数值量级）差异巨大，主流做法 ReVIN 类仿射归一化在**损失计算前**把模型输出反归一化回原尺度——论文证明这使每条序列的梯度被乘上 b^p（缩放因子的幂次），优化轨迹被各序列 scale 污染，作者称之为 **ScaleCon（scale-contaminated training）**；修正方案 **ScaleIn（scale-invariant training）** 是把损失直接算在缩放后的目标上，使每个 mini-batch 梯度与整条优化轨迹对训练序列的独立重缩放严格不变。落地只需**一行代码改动**。

## 解决什么问题

实例归一化（ReVIN 及其后继）解决了"输入尺度对齐"，但损失侧的反归一化把尺度敏感性重新引入梯度——同一模型对不同量级的同构序列学到的更新方向不同，训练被大批量级序列主导。这一问题此前未见系统刻画。

## 相比前方法优势（论文实证结论）

- **24 组 TSFM 架构×基准对比中 MASE 全部下降**，平均降幅 GIFT-Eval 18.8%、M-competitions 21.9%（摘要页实抓载明）；
- 20 个监督（supervised）设定中 16 个改善；
- 改动成本一行，无推理期开销（损失计算位置移动，不新增参数）。

## 局限（如实标注）

- **无官方代码仓**（arXiv 摘要页 2026-10-10 实抓，无 Comments 无链接）；signal.runnable 记 false——但改动本身一行，可在任一开源 TSFM 训练循环上自行落地，复现门槛极低；
- 收益依赖"仿射缩放"这一归一化族；监督设定 4/20 未改善，非普适免费午餐；
- 所有数字限于论文自报评测协议，引用时注明出处，不得挪作通用声明。

## 如何用于比赛

1. **数模-预测与评估（主用，配方级默认项）**：赛题微调 Chronos-2/TimesFM 或训练 N-HiTS/PatchTST 类监督预测器时，检查损失是否在反归一化后计算——若是，改为缩放域计算损失。多门店/多区域量级差异大的数据（C 题销量、交通流量常态）预期收益最大。
2. **消融论证模板**："开/关 ScaleIn 各跑一遍 + 逐序列 scale 分桶误差分解"可直接作为答卷训练细节章节与鲁棒性讨论，一行改动的成本换来完整消融故事。
3. **Kaggle/黑客松**：作为 TSFM 微调 pipeline 的默认开关；与库内 arxiv-2608.11359（Gated-LoRA 适配）同管线互补——一个管"参数怎么加"，一个管"损失怎么算"。
