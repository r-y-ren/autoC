---
id: bai2024DelayAwareCooperativeTask
name: 多UAV边云协同的时延感知任务卸载
field: [移动边缘计算, 任务卸载, Lyapunov 优化]
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
  - track: 黑客松-数据与算法
    edge: 本地/集群 LAN/远端云三目的地分流 + Lyapunov 虚拟队列处理长期能量预算的在线调度范式，可迁移到负载均衡/在线决策类赛题，对比单时隙贪心有长期性能差异化
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 弱基础设施（农田、灾区）下"多机现场边缘集群 + 云端补充算力"的边缘算力协同方案支撑点
    reuse_cost: 低
sources:
  - paper_title: "Delay-Aware Cooperative Task Offloading for Multi-UAV Enabled Edge-Cloud Computing"
    doi: 10.1109/TMC.2022.3232375
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 多UAV边云协同的时延感知任务卸载

## 单行摘要

在地面基础设施薄弱的场景下，把多 UAV 边缘集群与远端云纳入同一套时延模型：任务可本机处理、经集群 LAN 并行分担，或经基站卸载远端云（含空地 LoS/NLoS 信道与 BS-云有线中继时延）；目标是在长期电池预算约束下最小化系统总时延，用 Lyapunov 优化引入虚拟队列把长期约束转化为逐时隙协同卸载决策，缓解单机过载与负载不均。

## 方法快照

- 三类处理路径：本机计算、UAV 集群内 LAN 并行协同（异构机经虚拟机/容器化实现子任务兼容）、UAV-to-Cloud 经 BS 中转。
- 时延/能耗拆解：LAN 传输 + 集群并行计算（completion time 由最慢子任务决定）+ 云卸载三段。
- 长期建模：电池有限 → 长期平均能量预算约束，而非单时隙贪心。
- Lyapunov 转化：虚拟队列把长期约束问题变为逐时隙可求控制问题，逐时隙联合决策卸载比例矩阵、CPU 频率与云传输选择。
- 验证：数值仿真 + 真实 UAV-EC 平台测试床（Pixhawk + Jetson Nano 等），vault 正文实验卡注明资产已公开。

## 比赛映射要点

- 黑客松/算法赛：任何"任务往哪放 + 机器算力/电量有限"的调度题都可复用其三目的地分流建模与 Lyapunov drift-plus-penalty 在线化套路；"并行任务完成时间取决于最慢子任务"这一结构也是负载均衡题的关键约束点。
- 双创申报：农业监测、应急通信等弱基础设施场景的机载边缘算力协同叙事支撑。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Bai2024_多UAV边云协同时延感知任务卸载`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `bai2024DelayAwareCooperativeTask` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写。
- 复现性以 vault 页 frontmatter 自评 medium 为准（正文实验卡另标 high 并注明资产公开，取保守值）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
