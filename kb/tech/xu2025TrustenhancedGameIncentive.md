---
id: xu2025TrustenhancedGameIncentive
name: 信任增强的量子联邦学习Stackelberg激励机制
field: [联邦学习, 博弈论, 信任评估]
published: 2025-01-01
maturity: paper
directions: [数模与时序预测, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Journal on Selected Areas in Communications
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: "贝叶斯信任评估（直接评价 + 互评推荐迭代更新 + 阈值过滤）与 Stackelberg 激励（backward induction 证均衡、DQN 学动态支付）两套组件可拆开复用——前者迁移到评审方/合作方信誉评分类赛题，后者迁移到定价与激励相容类决策赛题"
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 可信协同学习的双机制叙事（先筛可信节点、再激励高质量贡献）可作为人工智能+边缘智能类项目的机制设计技术点，量子边缘计算是现成的前沿包装
    reuse_cost: 低
sources:
  - paper_title: Trust-Enhanced Game Incentive for Secure Quantum Federated Learning in UAV-assisted Wireless Networks
    doi: 10.1109/JSAC.2025.3568054
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# 信任增强的量子联邦学习Stackelberg激励机制

## 单行摘要

面向 UAV 辅助无线网络中的量子联邦学习（QFL），针对恶意 QECD 上传虚假/低质量更新、自私 QECD 因资源顾虑降低参与度这两类威胁，联合设计两层机制：第一层用贝叶斯信任评估融合直接评价与互评推荐、按阈值筛出可信参与集合；第二层以 UAV 为领导者、QECD 为跟随者构造 Stackelberg 激励（backward induction 证明均衡存在），并用 DQN 学习动态支付策略——提升模型精度、收敛速度与参与合作度。

## 方法快照

- QFL 协同训练：QECD 用量子算力本地训练，UAV 聚合局部模型更新全局模型（2 架 UAV、半径 300 m、高度 200 m 的仿真场景）。
- 贝叶斯信任评估：结合直接评价与互相推荐信息动态更新信任值，以信任阈值过滤低质量参与方。
- Stackelberg 激励：UAV 定奖励，QECD 按奖励与代价决定训练贡献度，backward induction 证 Stackelberg 均衡存在。
- DQN 动态支付：动态网络中 UAV 无需预知 QECD 参数，经经验回放学习最优支付决策。
- 基线对比：优于无信任激励、随机支付、固定支付方案。

## 比赛映射要点

- 数模决策题的两组件复用：信任评估组件（贝叶斯更新 + 互评聚合 + 阈值筛选）可独立迁移到"多源评价下给参与方打信誉分"类赛题；博弈激励组件（领导者定价 + 跟随者响应 + 均衡求解）可迁移到平台定价、补贴设计类赛题——比单纯回归拟合更机制化。
- 双创申报："先筛选可信、再激励贡献"的机制设计叙事完整且易讲，适配分布式农业数据协作/边缘智能项目的可信治理章节。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Xu2025_信任增强的安全量子联邦学习激励`（frontmatter 4 枚举字段已迁移至本卡）；概念页 `信任增强激励.md` 折叠于同簇卡 `xu2025BlockchainempoweredGameTheoretical` 的关联概念节。
- bib 回填：citekey `xu2025TrustenhancedGameIncentive` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写；验证类信息（MATLAB + quantum support package 仿真、synthetic 场景、复现性 medium、无开源）承自 vault 页自评，如需引用请以论文原文复核。
