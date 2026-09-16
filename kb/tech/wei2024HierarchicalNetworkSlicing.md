---
id: wei2024HierarchicalNetworkSlicing
name: UAV无线网络两时间尺度分层切片
field: [网络切片, UAV 通信, 随机博弈]
published: 2024-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Journal on Selected Areas in Communications
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 大时间尺度粗粒度配额+小时间尺度博弈调整的两时间尺度分解范式，直接映射"长周期规划+短周期动态调整"类多层资源分配赛题，且纳什均衡存在性证明给出可解释的决策层
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 切片内资源竞争建模为随机博弈并用轻量分布式学习 FDLA 逼近纯策略均衡，是多主体资源竞争类赛题的差异化建模范式（对比集中式重学习框架更轻量）
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 低空 6G 网络差异化服务保障叙事的技术支撑点（uRLLC/eMBB 多业务并行、UAV 高度本身成为切片质量变量）
    reuse_cost: 低
sources:
  - paper_title: "Hierarchical Network Slicing for UAV-assisted Wireless Networks with Deployment Optimization"
    doi: 10.1109/JSAC.2024.3459055
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# UAV无线网络两时间尺度分层切片

## 单行摘要

针对动态环境与不确定流量下 UAV 辅助无线网络难以同时满足 uRLLC 与 eMBB 等差异化业务的问题，提出两时间尺度分层切片框架：大时间尺度以粗粒度联合决定跨切片资源配额与 UAV 高度部署（MINLP，用分解技术+动态规划求近优），小时间尺度把切片内子信道竞争建模为随机博弈，证明纯策略纳什均衡存在并用轻量分布式学习 FDLA 求解——既避免频繁全局重切片，又能实时适应环境变化。

## 方法快照

- 系统设定：地面 BS + 一个可调高度 UAV 共同覆盖圆形区域，多业务切片并行，各切片用户有不同 QoS 偏好。
- 上层 RSP：大时间尺度联合决定切片资源份额与 UAV 高度，表述为 MINLP，分解技术求近优。
- 下层 SAP：小时间尺度切片内子信道/物理资源竞争建模为随机博弈，动态衰落与随机到达下在线适应。
- FDLA：轻量分布式学习逼近纯策略纳什均衡（证明存在性），避免在资源受限 UAV 上跑重型 DRL。
- 验证：仿真（合成动态无线环境），给出收敛、utility、throughput 与 delay 对比，未开源。

## 比赛映射要点

- 数模决策题：任何"长周期容量规划 + 短周期动态调度"双层结构（如共享算力配额、应急物资预置+调拨）都可套用两时间尺度分解；博弈层"均衡存在性 + 轻量学习"的写法比拍脑袋的启发式分配更有论证力。
- 黑客松/算法赛：多用户竞争资源时，随机博弈建模 + 分布式学习求解是与集中式优化/贪心基线拉开差距的路径。
- 双创申报：低空通信基础设施多业务保障的方案支撑点。

## 关联概念
- 层次化网络切片

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Wei2024_带部署优化的UAV辅助无线网络分层切片`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `wei2024HierarchicalNetworkSlicing` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写。
- 复现性承自 vault 页自评（medium，仿真级、未开源）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
