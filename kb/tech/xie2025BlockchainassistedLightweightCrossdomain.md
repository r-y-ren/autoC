---
id: xie2025BlockchainassistedLightweightCrossdomain
name: 双区块链轻量级跨域认证（多 UAV 网络）
field: [区块链认证, 跨域信任, 无人机网络安全]
published: 2025-01-01
maturity: paper
directions: [黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 黑客松-数据与算法
    edge: "双链分工（私有链域内身份治理 + 联盟链跨域信誉传递）+ 无证书签密 + 信用信任模型是多主体可信协作类赛题的现成安全架构；验证环境 Hyperledger Fabric 1.4.1 + Docker 工具链成熟，可低成本搭认证 demo"
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 智慧农业多主体协同（农户-服务商-监管域间）的可信身份基础设施论证支撑，回应跨域数据与作业授权互信的评审质询
    reuse_cost: 低
sources:
  - paper_title: Blockchain-Assisted Lightweight Cross-Domain Authentication for Multi-UAV Wireless Networks
    doi: 10.1109/TMC.2025.3582833
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 双区块链轻量级跨域认证（多 UAV 网络）

## 单行摘要

面向多 UAV 网络跨域访问场景，提出私有链 + 联盟链组成的双区块链认证框架：每域私有链管理域内 UAV 身份与许可，联盟链维护跨域信誉与信任传递，结合无证书签密与信用信任模型实现轻量级、去中心化的跨域认证。

## 方法快照

- 双链分工：私有链承担域内注册、许可与身份参数维护；联盟链承担跨域信誉共享与信任传递——保留隐私边界的同时摆脱单点控制器。
- 轻量级认证：certificateless signcryption 免除传统证书管理开销；EdDSA 提升签名效率与安全性；KGC 负责系统初始化与部分私钥生成，域边缘服务实体（DES）负责域内授权与跨域交互。
- 信任驱动授权：认证前联合评估 UAV 自身信誉、原域信誉、目标域信誉与域间特征相似度；仅获本地域许可的 UAV 才进入目标域认证流程。
- 实测环境：Docker 20.10.7 + Hyperledger Fabric 1.4.1 + Fabric Java SDK + Go，Ubuntu 16.04 虚机；指标覆盖计算/通信开销、链上时延、吞吐与 UAV 能耗，对比现有跨域认证与 UAV 认证方案；代码与链码未公开。

## 比赛映射要点

- 黑客松：凡赛题涉及"多组织/多智能体数据互信"（跨链身份、联邦准入、设备跨域接入），双链分工 + 信誉迁移是可直接复述并落地的安全架构；Fabric 工具链让 48 小时内搭出最小认证闭环可行。
- 双创申报：农业无人机作业涉及农户、飞防服务商、监管部门多个信任域，本框架支撑"可信跨域协作"基础设施论述；把认证从身份核验升级为"身份 + 信誉 + 域间信任迁移"的联合治理是差异化叙事点。
- 数模延伸：信用信任模型的多因子信誉加权（UAV/原域/目标域/相似度）可迁移为多主体协同评价类赛题的指标设计。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Xie2025_区块链辅助轻量级跨域认证`（frontmatter 带 venue_tier/evidence_tier/paper_role/reproducibility_level，已映射到本卡 4 枚举字段）。
- bib 回填：citekey `xie2025BlockchainassistedLightweightCrossdomain` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写；验证类信息（simulation/synthetic/复现性 medium、链码与部署脚本未披露）承自 vault 页自评，如需引用请以论文原文复核。
