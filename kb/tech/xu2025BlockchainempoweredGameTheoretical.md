---
id: xu2025BlockchainempoweredGameTheoretical
name: 区块链赋能的UAV带宽分配Stackelberg博弈激励
field: [区块链, 博弈论, 资源分配]
published: 2025-01-01
maturity: paper
directions: [数模与时序预测, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 带宽定价 Stackelberg 博弈（领导者定价、跟随者按价请求、backward induction 求均衡）加信誉加权 DPoS 的组合，可迁移到共享资源定价与分配类赛题（运力/算力/频谱），并把安全性、效率、公平性放进同一评价体系
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 农业无人机共享服务平台（植保/物流无人机向农户出租通信与算力）的可信交易治理外壳——区块链账本记录恶意行为 + 智能合约自动押金结算惩罚，直接支撑平台机制设计章节
    reuse_cost: 低
sources:
  - paper_title: Blockchain-Empowered Game Theoretical Incentive for Secure Bandwidth Allocation in UAV-assisted Wireless Networks
    doi: 10.1109/TMC.2025.3579505
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# 区块链赋能的UAV带宽分配Stackelberg博弈激励

## 单行摘要

针对地面基础设施受损或过载时 UAV 辅助无线网络中的带宽交易问题，先搭一层可信交易外壳——区块链不可篡改账本记录交易与恶意行为、智能合约自动执行押金/结算/惩罚、带信誉约束的 DPoS 维护共识防恶意实体主导——再把 UAV（带宽提供方）与移动用户（请求方）的交互建模为 Stackelberg 博弈：UAV 定价，用户按价格决定请求量，backward induction 求取均衡，在安全、效率与公平之间取得平衡。

## 方法快照

- 分层框架：服务层（UAV 供带宽）、治理层（区块链记账）、合约层（智能合约自动押金/结算/惩罚）、共识层（信誉驱动 DPoS）、决策层（定价-请求互动）。
- 威胁模型：拒付、伪装、数据篡改等恶意行为风险，需要自动支付与可追责机制维持长期合作。
- Stackelberg 激励：UAV 作为领导者决定带宽价格，用户作为跟随者选择请求量，backward induction 求均衡。
- 基线对比：优于传统带宽分配与无区块链激励方案（安全性、效率、公平性、双方效用）。

## 比赛映射要点

- 数模决策题：把定价博弈（均衡求解）与信誉机制（历史行为记账加权）组合使用，适合共享经济类资源分配赛题；"安全 + 效率 + 公平"三目标评价体系可直接搬用。
- 双创申报：无人机共享服务平台的治理叙事——资源交易不能只谈稀缺还要谈可信，本文提供区块链从身份认证走向资源交易治理的完整案例。

## 关联概念（vault 枢纽页折叠于此，不独立成卡）

- **信任增强激励**：把参与者可信度评估与收益分配机制联合设计——先筛选可信节点、再激励高质量贡献，以稳定长期协作；本卡以区块链账本 + 信誉 DPoS 承担信任底座、Stackelberg 博弈承担激励层。该概念页同时锚定本片姊妹卡 `xu2025TrustenhancedGameIncentive`（QFL 信任 + 博弈激励）与 Xie2025 跨域认证（不在本片）。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Xu2025_区块链赋能的安全带宽分配博弈激励`（frontmatter 4 枚举字段已迁移至本卡）；枢纽页 `信任增强激励.md` 已折叠进上文关联概念节。
- bib 回填：citekey `xu2025BlockchainempoweredGameTheoretical` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写；验证类信息（simulation、synthetic 场景、复现性 medium、无开源）承自 vault 页自评，如需引用请以论文原文复核。
