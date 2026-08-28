---
id: arxiv-2608.11359
name: "Market-Information-Aware Gated-LoRA of Foundation Models for Transferable Day-Ahead Electricity Price Forecasting"
field: [时序预测, 电力市场, 参数高效微调]
directions: [数模与时序预测]
published: "2026-08-11"
maturity: paper
signal:
  venue: arXiv
  runnable: false
competition_fit:
  - track: "数模-预测与评估"
    edge: "电价/现货出清价预测类赛题（电工杯、研赛能源题）的结构性打法：以开源 Chronos-2 为骨干（pip 可装、支持协变量），按论文 MSMI 接口组织'7 天价格上下文 + 供需/备用/检修/机组容量/联络线'协变量先跑零样本基线（低成本高性价比组件），赛期允许再加 ~1% 参数的源域 Gated-LoRA 做目标市场零标签适配；门控以备用紧张度/运行状态为条件，恰好针对赛题中最难压误差的尖峰紧张时段；验证协议照搬 leave-one-market-out + 分时段误差分解"
    reuse_cost: "中"
    open_source: "https://github.com/amazon-science/chronos-forecasting（被适配骨干 Chronos-2 官方仓，Apache-2.0，HF 权重 amazon/chronos-2；论文自身无代码）"
  - track: "黑客松-数据与算法"
    edge: "能源数据黑客松（公开日前市场价格+系统变量数据集）：'冻结 TSFM + 门控 LoRA 参数高效适配'对常见 GBM 堆叠基线是结构性差异点，且论文场景（数据稀缺新市场）与黑客松小样本题面天然对齐"
    reuse_cost: "高"
sources:
  - url: https://arxiv.org/abs/2608.11359
    title: "Market-Information-Aware Gated-LoRA of Foundation Models for Transferable Day-Ahead Electricity Price Forecasting (arXiv:2608.11359)"
    accessed: "2026-08-28"
  - url: https://github.com/amazon-science/chronos-forecasting
    title: "amazon-science/chronos-forecasting——Chronos/Chronos-2 官方实现（复用骨干，非论文代码；2026-08-28 实抓核验含 Chronos-2 与 HF 权重）"
    accessed: "2026-08-28"
---

# 市场信息感知 Gated-LoRA：可迁移的日前电价预测

## 是什么

Fan、Wei、Mei 三人（2026-08-11 提交 arXiv:2608.11359，cs.LG，v1）提出的电价预测适配框架：以 **Chronos-2** 时序基础模型为骨干，构造**多源市场信息接口（MSMI）**——7 天价格上下文 + 出清前供需、备用、检修、机组容量、联络线等变量——再用**源域门控 LoRA**（约 1% 参数、目标市场零标签）做参数高效迁移；门控以备用紧张度与运行状态信号对冻结的源适配器做缩放。在四个中国省级日前现货市场上以 leave-one-market-out 协议评测。

## 解决什么问题

日前电价波动大、强市场特异性、与预期系统状态强耦合；既有监督方法依赖市场专属历史数据，在新建或数据稀缺市场难以落地——这正是"赛题只给有限历史、测试期市场状态/分布变化"场景的原型。

## 相比前方法优势（论文实证结论）

- 相对"市场信息感知零样本 Chronos-2"：平均 MAE/RMSE 降低 6.24%/7.99%；
- 相对朴素 Source-LoRA：再降 3.05%/3.52%（论文自述该增量有限，如实计）；
- 消融表明门控设计不可替代：学习型全局标量门控或随机初始化门控均无法复现增益——**按运行状态条件的门控**是误差改善的来源。

## 局限（如实标注）

- 论文**无代码**（arXiv 页 2026-08-28 实抓，无 Comments 与代码链接），Gated-LoRA 与 MSMI 接口需按论文自建；signal.runnable 记 false（骨干开源但论文方法本体无实现）；
- 四个中国省级现货市场的出清前供需/备用等细粒度数据未公开，赛队复用只能依赖赛题提供的类比协变量，接口需重新对齐；
- 对 Source-LoRA 的增量约 3%，赛期紧张时"MSMI 零样本 Chronos-2"部分才是性价比最高的可搬组件，完整 Gated-LoRA 属锦上添花；
- 所有数值仅在其 leave-one-market-out 数据集上成立，引用必须注明出处，不得挪用为通用性能声明。

## 如何用于比赛

1. **电价/出清价预测类赛题（数模-预测与评估，主用）**：骨干直接用开源 Chronos-2（`pip install chronos-forecasting`，HF 权重 amazon/chronos-2，120M，支持协变量输入），按 MSMI 思路组织"价格史 + 系统状态协变量"先跑零样本基线；赛期允许时冻结骨干、加约 1% 参数的源域 LoRA（全量训练集当源域）做测试期零标签适配。
2. **紧张时段针对性建模**：门控条件（备用紧张度/运行状态）对应电价尖峰时段的误差集中区，可发展为答卷中"针对性设计"的论证点与分时段误差分析章节。
3. **验证协议复用**：leave-one-market-out（或等价的滚动留出）+ 分时段误差分解直接作为实验设计骨架，比单一全局 MAE 的答卷高一档。
4. **能源数据黑客松**：公开市场数据场景下"冻结 TSFM + PEFT 适配"对 GBM 堆叠基线是结构性差异，且小样本新市场题面与论文设定天然对齐（注意完整方法需自建训练回路，成本高）。
