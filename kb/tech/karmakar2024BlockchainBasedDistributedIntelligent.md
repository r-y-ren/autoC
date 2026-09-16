---
id: karmakar2024BlockchainBasedDistributedIntelligent
name: SwarmAuth：区块链+动态聚类的UAV蜂群分布式认证
field: [无人机蜂群安全, 区块链认证, 动态聚类]
published: 2024-01-01
maturity: paper
directions: [创新创业大赛, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 双创-文书与申报
    edge: 植保巡检类无人机集群的可信管控方案支撑——PUF 硬件互认证、区块链存证与智能合约访问控制构成完整的集群身份与准入技术叙事，NS-3/以太坊仿真数据可直接支撑申报书安全章节
    reuse_cost: 低
  - track: 黑客松-数据与算法
    edge: 动态 K-means 位置聚类把认证流量局部化（簇内转发+簇规模随移动性自适应），可迁移为移动节点自组织与通信开销控制类赛题组件，对比静态聚类有明确差异化
    reuse_cost: 中
sources:
  - paper_title: "A Blockchain-Based Distributed and Intelligent Clustering-Enabled Authentication Protocol for UAV Swarms"
    doi: 10.1109/TMC.2023.3319544
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# SwarmAuth：区块链+动态聚类的UAV蜂群分布式认证

## 单行摘要

针对高动态 UAV 蜂群在不可信环境中缺乏统一身份认证、中心化认证又存在单点失效的问题，提出 SwarmAuth：用 PUF 完成 GSC 与 UAV 的互认证，用区块链不可篡改账本存证注册与认证信息，用智能合约执行访问控制，并用基于 K-means 的动态位置聚类把认证流程局部化以适应蜂群移动——认证目标从加密算法正确性扩展到身份、状态与访问控制随移动性共同演化的系统问题。

## 方法快照

- PUF 互认证：GSC 与 UAV 基于物理不可克隆函数完成注册与双向认证，减轻密钥存储与泄露风险。
- 链上存证与合约控制：注册/认证信息写入区块链，智能合约负责访问控制与状态更新，记录可追溯。
- 动态 K-means 聚类：按位置动态成簇，认证消息在簇内转发，控制传播时延与消息开销，簇规模随移动性调整。
- 验证：Scyther 协议安全分析 + NS-3.36 与以太坊虚拟机仿真，在通信/计算开销、吞吐与时延上优于多种基线。

## 比赛映射要点

- 黑客松/算法赛：带移动性的动态成簇与认证开销权衡，可作为自组织网络/蜂群协同类赛题的差异化组件（对比静态 K-means）。
- 双创申报：智慧农业植保、巡检无人机集群的身份认证与准入管控方案；叙事点是自治蜂群需要可信基础设施而非仅链路加密。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Karmakar2024_区块链与聚类驱动的UAV蜂群认证协议`（4 枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `karmakar2024BlockchainBasedDistributedIntelligent` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写；复现性 medium 与 NS-3/以太坊合成场景仿真形态承自 vault 页自评（artifact_availability: unknown），如需引用请以论文原文复核。
