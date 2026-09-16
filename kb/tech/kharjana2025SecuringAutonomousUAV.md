---
id: kharjana2025SecuringAutonomousUAV
name: 链上阈值多签密钥管理的自主UAV集群安全
field: [无人机集群安全, 区块链, 密钥管理]
published: 2025-01-01
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
    edge: 远程自主作业无人机集群的密钥全生命周期治理方案——密钥建模为链上 crypto-asset、多重签名阈值授权，覆盖重编队/子集群/跨簇迁移场景，是申报书中集群自治安全基础设施的直接技术支撑（TMC 2025）
    reuse_cost: 低
  - track: 黑客松-数据与算法
    edge: 多签阈值授权可用智能合约 multisignature 模式快速原型化，叠加 OMNET++/Crypto++ 的网络与链上负载指标即可形成可演示的端到端集群密钥治理 demo
    reuse_cost: 中
sources:
  - paper_title: "Securing Autonomous UAV Cluster with Blockchain-Based Threshold Key Management System Utilizing Crypto-Asset and Multisignature"
    doi: 10.1109/TMC.2025.3538462
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# 链上阈值多签密钥管理的自主UAV集群安全

## 单行摘要

针对自治 UAV 集群在远程部署中缺乏可信密钥管理基础设施、集中式 CA 与单机密钥持有者都构成单点故障的问题，提出基于区块链的阈值密钥管理系统：把密钥抽象为链上 crypto-asset 完成登记、更新、撤销与迁移管理，用多重签名实现可配置阈值的协同授权，使集群在重编队、子聚类、重合并与跨簇迁移等过程中仍能自治且安全地管理密钥。

## 方法快照

- 密钥资产化：密钥生命周期操作（更新/撤销/迁移）建模为链上 crypto-asset 的状态变更，账本不可篡改。
- 阈值多签授权：每个关键操作需达到阈值数量（参数 M）的协作 UAV 签名才能被链上接受，消除单点信任。
- 生命周期场景化：显式覆盖最佳/最差拓扑与集群增强、子聚类、跨簇迁移等操作流程。
- 验证：OMNET++ 结合 AODV/DSDV 路由协议与 Crypto++ 密码库，分析响应时延、丢包、带宽、链上交易（区块/UTXO）负载与 UAV 能耗。

## 比赛映射要点

- 双创申报：智慧农业远程作业集群（植保、巡检编队）的密钥治理与集群自治安全方案；叙事点是安全基础设施（密钥如何随重组与迁移演化）而非单次认证。
- 黑客松/算法赛：链上多签阈值授权 + 网络层性能联动分析可做成可演示原型；AODV/DSDV 路由选择对签名收集时延的影响是可量化的实验设计点。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Kharjana2025_基于区块链阈值密钥管理的自主UAV集群安全`（4 枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `kharjana2025SecuringAutonomousUAV` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写；复现性 medium 与 OMNET++/Crypto++ 合成拓扑仿真形态承自 vault 页自评（artifact_availability: unknown），如需引用请以论文原文复核。
