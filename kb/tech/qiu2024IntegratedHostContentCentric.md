---
id: qiu2024IntegratedHostContentCentric
name: IHCR：UAV蜂群主机-内容中心融合路由
field: [FANET 路由, 内容中心网络, UAV 蜂群]
published: 2024-01-01
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
    edge: 拓扑「短时稳定 + 快速波动」混合特性下的路由机制设计——稳定期复用 host-centric 路径减少泛洪、失效时切 content-centric 失败检测与延迟转发快速恢复，动态网络路由赛题相对单一 AODV 或泛洪方案有现成差异化论证
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 无人机蜂群协同作业中「节点会话 + 内容分发」混合业务的机间组网方案支撑点，农业蜂群影像/状态数据分发场景可直接引用
    reuse_cost: 低
sources:
  - paper_title: Integrated Host- and Content-Centric Routing for Efficient and Scalable Networking of UAV Swarm
    doi: 10.1109/TMC.2023.3267451
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# IHCR：UAV蜂群主机-内容中心融合路由

## 单行摘要

针对 UAV 蜂群「拓扑并非一直剧烈变化、但也并不稳定」的网络特性，提出 IHCR 融合路由：用统一的 NID:N 命名结构同时兼容节点身份与内容标识，编队保持期按 host-centric 思路复用稳定路径减少探测泛洪，拓扑波动时切换 content-centric 失败检测与延迟转发机制快速重路由——在包级仿真中显著提升内容共享与节点通信场景的可扩展性与交付性能。

## 方法快照

- 问题定位：纯 host-centric（如 AODV）擅长利用稳定路径但高机动下恢复慢；纯 content-centric（如 LFBL）灵活但即使有稳定路径也重复泛洪；蜂群网络不适合被硬性归为稳定 MANET 或完全机会网络。
- 命名层：NID:N 结构统一生产者节点身份与内容标识，避免两种范式命名空间冲突。
- 路由层：稳定路径复用（host-centric）+ 失效时内容中心式失败检测与延迟转发（content-centric）协同。
- 承载业务：节点到节点（控制消息、认证）与内容共享（位置、图像视频、任务分发）双模式。
- 验证：OMNeT++（Ubuntu 20.04 / VMware ESXi，Intel Xeon Gold 6148 + 260GB RAM）包级仿真，指标为 PDR、时延、可支持网络规模与流量负载，对比 AODV、LFBL、AGGR；未开源仿真脚本。

## 比赛映射要点

- 黑客松/算法赛：动态网络/机会网络路由题可用「先判稳定性再选范式」的机制设计思路；「两种经典方法各抓一半、融合机制取长补短」的论证结构可直接迁移到方案答辩。
- 双创申报：蜂群作业的机间组网章节（数据分发 + 节点会话并存）可引用其混合业务建模。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Qiu2024_UAV蜂群高效可扩展网络的主机-内容中心融合路由`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `qiu2024IntegratedHostContentCentric` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写。
- 复现性承自 vault 页自评（medium，包级仿真、未披露脚本与配置）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
