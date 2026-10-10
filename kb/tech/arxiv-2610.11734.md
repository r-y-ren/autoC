---
id: arxiv-2610.11734
name: "Timer-M1: A Multivariate Time Series Foundation Model via Learning Primitives（原语式预训练多变量 TSFM）"
field: [时序基础模型, 时序预测, 零样本预测]
directions: [数模与时序预测]
published: "2026-10-08"
maturity: paper
venue_tier: arXiv
signal:
  venue: arXiv
  runnable: false
competition_fit:
  - track: "数模-预测与评估"
    edge: "两层可用价值（模型本体未放码，勿直接复用）：(1) 零样本选型先验——当前可下载梯队为 Chronos-2/TimesFM-3（Timer-M1 在 FEV 超 Chronos-2 3.43% MASE、GIFT-Eval 次于 TimesFM-3），权重放出后多变量+协变量题型即有替换候选；(2) 协变量角色组织蓝图——episode 内 target/past-only/known-future 三角色 + 防泄漏注意力分组，正是数模题'目标变量+节假日促销日历+天气'数据结构的一等建模方式，评测协议 FEV（github.com/autogluon/fev，论文实抓载明）可作赛题自评 harness"
    reuse_cost: "高"
    open_source: "论文无代码无权重（arXiv 摘要页与 HTML 全文 2026-10-10 实抓均无 release 声明）；可复用的是评测 harness github.com/autogluon/fev"
sources:
  - url: https://arxiv.org/abs/2610.11734
    title: "Timer-M1: A Multivariate Time Series Foundation Model via Learning Primitives (arXiv:2610.11734, 摘要页实抓)"
    accessed: "2026-10-10"
  - url: https://arxiv.org/html/2610.11734v1
    title: "Timer-M1 HTML 全文（架构参数/基准数字/预训练数据规模实抓）"
    accessed: "2026-10-10"
---

# Timer-M1：学习时序原语的多变量时序基础模型

## 是什么

Timer 谱系（thuml）团队新作（作者含 Haoran Zhang、Yong Liu、Jianmin Wang、Mingsheng Long 等，2026-10-08 提交 arXiv:2610.11734，cs.LG，v1；机构页未列，谱系归属由作者构成与 thuml 官方仓族推定）发布的 121M 参数多变量 TSFM：主张跨域时序共享**初等时序/关系模式（primitives）**，据此构建"真实数据（TimeBench）+ 按原语（周期/趋势/随机依赖/状态切换/符号响应/共享驱动/协整/事件效应等关系算子）合成"的预训练管线——227 个 dataset 条目、2.143 亿持久记录、3.02 万亿标量位；以 episode 组织多变量样本，episode 内给每个变量分配角色（target / past-only 协变量 / known-future 协变量）并用掩码与注意力分组防泄漏；骨干为门控二维 Transformer（12 层 768 宽，时序注意力 + 逐层门控变量注意力，门控 α≈0.01 初始化、随深度增大、推理期固定），分解注意力（factorized）代价 O(CN²D+NC²D)。

## 解决什么问题

现有 TSFM 的零样本/任务泛化预测对**多变量结构**（变量间关系）与**协变量角色**（哪些变量只有过去、哪些未来已知）支持薄弱；Timer-M1 用原语合成+角色化 episode 让单一 checkpoint 同时覆盖单变量/多变量/两类协变量任务，无需任务专属参数更新。

## 相比前方法优势（论文实证结论）

- **FEV 榜双第一**：MASE skill 0.3771 / SQL skill 0.4887，较 Chronos-2 误差低 3.43%（MASE），较 TimesFM-3 低 0.47%；
- **TIME 榜第一**：nMASE 0.6372 / CRPS 0.5363，较 Chronos-2 低 3.75%；对 TimesFM-3 优势 <0.4%，作者自述为"competitive 而非统计确立的优越"；
- **GIFT-Eval 第二**（0.6806/0.4688，TimesFM-3 居首），胜 Chronos-2、TiRex-2、Toto 2.0（2.5B）；
- **消融支撑设计主张**：全配方 FEV SQL 0.4887 > 仅真实数据 0.4431 / 仅合成 0.4710 / 去联合目标 0.4725；自适应门控优于固定门控；目标变量缺失场景 NMAE 较 Chronos-2 低 32.5%。

## 局限（如实标注）

- **无代码、无权重**（摘要页与 HTML 全文 2026-10-10 实抓均无 release 声明；搜索亦无 Timer-M1 专属仓，thuml 谱系仓最后推送早于论文）——signal.runnable=false，**当前不可用于任何作品**；谱系既往开源惯例（Timer-XL 等有官方仓）不构成放码承诺，以实际放出为准；
- 对 TimesFM-3 的领先在作者自述的统计噪声级；GIFT-Eval（以单变量为主）上仍居次；
- 预训练数据规模的"万亿标量位"为存储计数口径（去重/采样前），引用时勿当作独特观测数。

## 如何用于比赛

1. **零样本选型先验（数模-预测与评估）**：答卷/练手今日可下载的零样本骨干仍按库内 arxiv-2608.22968 选型框架 + Chronos-2/TimesFM-3 梯队执行；Timer-M1 权重若放出，多变量+协变量题型（C 题多指标联合预测）优先纳入对比——本卡即放码后的替换触发器。
2. **协变量角色组织蓝图**：赛前整理数据时按 target / past-only（天气、滞后指标）/ known-future（节假日、促销日历、预报值）三角色分列，配 FEV 式 matching-configuration 自评（同一数据多种角色配置对比），是零成本提升答卷实验设计档次的做法；Chronos-2（库内 arxiv-2608.11359 已核验支持协变量）今日即可承载该组织方式。
3. **技术脉络定位**：库内首张"TSFM 本体"卡（此前为选型实证 2608.22968、零样本表格 2608.20024、失败模式 2608.14106、适配 2608.11359）——Timer→Timer-XL→Sundial→Timer-M1 谱系的最新一代，简报按谱系归位。
