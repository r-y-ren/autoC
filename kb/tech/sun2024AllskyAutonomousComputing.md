---
id: sun2024AllskyAutonomousComputing
name: ASAP 无人机群全空域自主协同计算系统
field: [UAV 集群系统, 协同推理, 弹性调度]
published: 2024-01-01
maturity: paper
directions: [黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: high
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: true
competition_fit:
  - track: 黑客松-数据与算法
    edge: 「两层任务切分 + 弹性调度 + 算子级推理时延预测 + 机间自适应压缩」的边传边算成套系统模板，且系统与代码开放，是分布式推理/算力调度类赛题可直接落地的高复现参考
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 灾害监测/搜救/矿区探测等无基站场景的「空中自治 AI 计算基础设施」叙事，24 台机载节点 + 5 架真机（Jetson 系列实测）工程背书强，避开了「高精度高回传时延 vs 低时延低精度」二选一的旧框架
    reuse_cost: 低
sources:
  - paper_title: "All-Sky Autonomous Computing in UAV Swarm"
    doi: 10.1109/TMC.2024.3427420
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# ASAP 无人机群全空域自主协同计算系统

## 单行摘要

针对灾害/搜救/矿区等地面基站不可用场景中「单机算力不够、回传地面时延高」的矛盾，提出 ASAP 系统：不做传统任务卸载，而是让 UAV 群自身成为可弹性重构的协同计算体——把 DL 推理任务在集群间与集群内两层切分，弹性调度器按 UAV 可用性在线重排计算分配，轻量推理性能预测器快速估计执行代价，自适应压缩器依机间链路带宽调整中间数据压缩比例，实现空中边传边算且部分 UAV 失效仍稳定运行。

## 方法快照

- 架构：集群层（任务 UAV + 中继 UAV 按群层级组织）→ 计算层（模型分段 + 数据分块）→ 控制层（弹性调度在线重构）→ 支撑层（性能预测 + 自适应压缩）。
- 弹性调度器：UAV 不可用时在线更新任务映射，维持服务连续性。
- 推理性能预测器：复杂模型时延估计拆成算子级预测 + 细粒度修正，降低估计开销。
- 自适应压缩器：按链路带宽动态调整中间特征压缩比例，缓解机间瓶颈。
- 验证：原型 + 实飞（24 台机载计算节点、5 架四旋翼、Jetson Nano/TX2/Xavier NX、地面 RTX 3060、TensorRT）；vault 自评系统与代码已对外开放，复现性 high。

## 比赛映射要点

- 黑客松：多机/多节点协同推理、算力调度类赛题可直接参照其「切分-调度-预测-压缩」四件套；「不牺牲精度、用群体协同换算力」的问题定义方式本身是差异化论证。
- 双创申报：应急场景空中算力平台、无人机集群智能感知等项目的技术方案与可行性论证素材（真实硬件清单与实测结果可直接复述）。

## 关联概念
- 空中自主协同计算

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Sun2024_ASAP无人机群全空域自主协同计算`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `sun2024AllskyAutonomousComputing` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写。
- signal.runnable 标 true 的依据：vault 页自评 artifact_availability=open（「系统与代码已对外开放」），本次跑批未另行核验仓库地址，引用前建议以论文原文复核开源入口。
