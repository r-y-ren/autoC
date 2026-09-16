---
id: zhang2025OptimizingMonitoringUtility
name: 兼顾监测效用与负效应的多UAV布设优化（PEACE）
field: [UAV 部署优化, 次模优化, 监测效用建模]
published: 2025-01-01
maturity: paper
directions: [创新创业大赛, 数模与时序预测, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: "效用-负效应双目标布设问题经分段常数近似 + 区域划分离散化后，转化为 uniform matroid 约束下单调次模函数最大化，取得 1-1/e-ε 可证明近似——为选址/布点/覆盖类数模题提供带近似保证的求解框架，超越普通贪心与启发式"
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: "'收益随距离/朝向各向异性变化 + 负效应随距离上升'的双曲线权衡建模 + 候选策略离散化 + 次模组合算法，适用于摄像头布设、传感点选址、资源覆盖类赛题，且有人因约束的少见差异化角度"
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: "无人机巡监/安防监测服务方案中'监测质量 - 靠得过近的扰民/隐私/安全负效应'权衡设计点，5 架 Mavic Air 2 实地飞测背书，适合写进社会效益与合规性论证"
    reuse_cost: 低
sources:
  - paper_title: "Optimizing Monitoring Utility of Uncrewed Aerial Vehicles Considering Adverse Effects"
    doi: 10.1109/TMC.2025.3543399
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 兼顾监测效用与负效应的多UAV布设优化（PEACE）

## 单行摘要

针对多 UAV 对人、车流等对象的临时监测部署，首次把"靠得过近带来的安全、噪声与隐私不适"作为负效应与监测质量（各向异性 QoM）联合建模：通过分段常数近似与区域划分把连续布设空间离散为有限候选策略集，将原问题近似为 uniform matroid 约束下的单调次模最大化（MSMUM），提出 PEACE 算法取得 1-1/e-ε 近似保证；相较对比方法综合目标提升 9.0% 至 1434.5%，并以 5 架 Mavic Air 2 实地文本识别实验验证。

## 方法快照

- 建模创新：监测效用用各向异性 QoM（兼顾距离与朝向），每个对象叠加 adverse effect 函数——UAV 部署从 coverage-aware 推进到 utility-aware + impact-aware。
- 连续转离散：分段常数近似 + 二维平面等价子区域划分 + 候选策略提取，构成有限 ground set。
- 近似求解：MSMUM 上的 PEACE 组合算法，整体 1-1/e-ε 近似，内部子问题 1-1/e 与 O(n log n)。
- 实验证据：数值仿真（随机拓扑）+ 真实场地飞行测试（5 x Mavic Air 2，外接开源文本识别模型评测），混合来源，在库内少见的"人因/安全约束 + 实地验证"证据组合。
- 局限：负效应函数依赖人工设定，代码未开源。

## 比赛映射要点

- 数模决策题：布点/选址/覆盖类问题的标准升级路径——先证明目标次模性，再上带近似保证的组合算法，近优比 "1-1/e" 是论文里现成的论证素材。
- 黑客松/算法赛：带容量约束的效用最大化选点题可直接复用"离散化候选集 + 次模贪心/组合算法"管线；效用-负效应权衡是少见的差异化建模角度。
- 双创申报：巡检监测类产品的"低打扰监测"卖点（减少对人群/牲畜的噪声与隐私干扰），有实地实验支撑。

## 关联概念
- 监测负效应

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Zhang2025_兼顾监测效用与负效应的无人机布设优化`（4 枚举字段自 vault 页 frontmatter 迁移，reproducibility_level=medium）。
- bib 回填：citekey `zhang2025OptimizingMonitoringUtility` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写。
- 复现性承自 vault 页自评（medium，有实地实验但代码未开源）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
