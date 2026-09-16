---
id: li2025ExploringRobustnessHierarchical
name: HFL-OD：抗毁伤的UAV集群层次化联邦目标检测
field: [联邦学习, UAV 集群, 目标检测]
published: 2025-01-01
maturity: paper
directions: [黑客松与数据竞赛, 数模与时序预测, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 黑客松-数据与算法
    edge: 三维图着色打散分组 + 组内数据备份 + 信誉动态服务器重选的容错分布式训练骨架，可迁移到节点失效/通信受限下的协同训练类赛题，区别于只做 FedAvg 的常规 FL 方案
    reuse_cost: 中
  - track: 数模-数据分析与决策
    edge: 空间打散分组（图着色）+ 冗余备份 + 基于多因素信誉的角色选举，构成完整的抗毁组网决策模型，适配应急设施布置与网络抗毁类数模题
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 植保/巡检无人机集群在部分损毁场景下维持感知与训练能力的协同学习方案支撑点（VisDrone + YOLOv5 的可复现叙事）
    reuse_cost: 低
sources:
  - paper_title: "Exploring the Robustness: Hierarchical Federated Learning Framework for Object Detection of UAV Cluster"
    doi: 10.1109/TMC.2025.3562812
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# HFL-OD：抗毁伤的UAV集群层次化联邦目标检测

## 单行摘要

面向森林火灾、电磁干扰等高威胁环境下的 UAV 集群目标检测，提出两层级联邦学习框架 HFL-OD：先用三维图着色把地理上可能同时受威胁的 UAV 打散分组，组内共享备份业务数据与局部模型参数，组内聚合与全局聚合构成层次化 FL，并靠基于信誉的动态服务器重选在组/簇服务器失效时快速重组汇聚路径——把「节点毁伤导致数据与模型双重丢失」作为系统主目标正面求解。

## 方法快照

- 三维图着色分组：替代按位置就近分组，避免同组 UAV 空间聚集被一锅端；局部空域受威胁时不至于整组样本丢失。
- 组内备份：UAV 在组内共享业务数据与局部参数，单点损毁后数据可恢复。
- 两层聚合：组服务器聚合 group model，簇服务器做 global aggregation（FedAvg/SGD，检测模型 YOLOv5）。
- 动态服务器重选：信誉综合数据相似性、分布均匀性、剩余电量与能耗，定期重选使失效后重建更稳定。
- 验证：VisDrone 公共数据集仿真，对比集中训练/传统 FL/不同分组备份策略，未开源、未披露训练硬件。

## 比赛映射要点

- 黑客松/算法赛：分布式协同/容错类赛题（多节点训练、边缘协同）可直接复用「图着色打散 + 数据备份 + 角色动态选举」三件套；「鲁棒性写进系统主目标」的论证方式是差异化亮点。
- 数模：抗毁组网/应急设施布置类题的建模组件——空间分散分组目标（同组不同时受损）正是图着色的形式化表达。
- 双创申报：集群协同感知的高可用叙事（毁伤场景下精度保持率 + 通信开销权衡的量化论证）。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Li2025_层次化联邦学习增强UAV集群目标检测鲁棒性`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `li2025ExploringRobustnessHierarchical` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写。
- 复现性承自 vault 页自评（medium，公共数据集 + 常见框架组件但未开源）；signal.runnable 如实标 false。
