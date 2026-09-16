---
id: chen2024AdaptiveBitrateVideo
name: UAV辅助MEC的码率视频鲁棒缓存（DRO）
field: [移动边缘计算, 边缘缓存, 分布鲁棒优化]
published: 2024-01-01
maturity: paper
directions: [创新创业大赛, 数模与时序预测, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: low
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 请求分布不确定时用模糊集（Kantorovich/TV 等距离构造）做最坏情形期望优化的 DRO 建模，可迁移到需求不确定的库存/资源预置类数模赛题，比经验分布最优更稳健
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 缓存命中/转码命中/回源 miss 三种交付模式统一进一阶段混合整数优化的建模方式，可迁移到内容分发与多级资源调度类赛题
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 乡村/农田热点区域监测数据与媒体内容的空中边缘缓存-回传调度方案支撑点
    reuse_cost: 低
sources:
  - paper_title: "Adaptive Bitrate Video Caching in UAV-Assisted MEC Networks Based on Distributionally Robust Optimization"
    doi: 10.1109/TMC.2023.3304624
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# UAV辅助MEC的码率视频鲁棒缓存（DRO）

## 单行摘要

面向热点区域的自适应码率视频业务，在 UAV 辅助 MEC 中联合建模缓存放置、转码调度与回源交付三种模式（cache hit / transcoding hit / backhaul miss）：缓存二元决策与三类交付量共同构成一阶段混合整数非线性问题，并在内容流行度分布不确定时引入 distributionally robust optimization，在由历史请求数据构造的模糊集上优化最坏情形期望时延，得到抗分布偏差的稳健缓存与交付策略。

## 方法快照

- 交付三模式：直接命中缓存、由高码率版本转码得到目标版本、经基站回源，各自时延/能耗结构不同。
- 联合问题：缓存变量 x_f 与交付量 y_c/y_t/y_b 同置一阶段 MINLP，受 UAV 存储、码率层级关系与系统能耗预算约束。
- DRO 框架：不假设唯一真实分布，用经验分布 + Kantorovich / Fortet-Mourier / TV 等距离度量构造 confidence set，目标为最坏分布下的期望时延最优。
- 适用洞察：请求分布越不稳定、历史样本越有限，DRO 相对经验分布优化的收益越大。
- 验证：合成场景数值仿真，未开源。

## 比赛映射要点

- 数模赛：需求/流行度分布不确定时的决策题（库存、缓存、容量预置）可复用"模糊集 + 最坏情形期望"建模与多距离度量的容忍度设置，作为超越"直接用经验分布"的差异化论证。
- 黑客松/算法赛：多级交付（本地命中/加工转换/远端回源）的统一 MINLP 建模可迁移到 CDN、多级缓存调度类题。
- 双创申报：农业监测数据在空中边缘节点的缓存与回传调度叙事。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Chen2024_面向自适应码率视频的UAV辅助MEC鲁棒缓存`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `chen2024AdaptiveBitrateVideo` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写。
- 复现性承自 vault 页自评（low，实验资产链条说明有限，当前定位为方法理解支撑）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
