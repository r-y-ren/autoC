---
id: shen2024SlicingBasedTaskOffloading
name: SAGIN车联网切片式任务卸载
field: [网络切片, 车联网, 深度强化学习]
published: 2024-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 黑客松-数据与算法
    edge: 「自适应切片窗口 + 资源切片 + DDQN 窗口内调度」的双层闭环可整体迁移为时变负载下的资源调度 demo；实验用的 OpenITS 交通流 trace 公开可得，trace 驱动评测链路可直接复用
    reuse_cost: 中
  - track: 数模-数据分析与决策
    edge: 把控制周期（切片窗口长度）本身作为决策变量的双时间尺度建模，适用于负载波动的调度类赛题——大尺度定周期配资源、小尺度做实时调度，比固定周期基线多一层论证维度
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 车路协同/智慧农业园区车辆作业场景中，时延敏感（避障）与时延容忍（数据回传）业务差异化保障的服务隔离叙事，有 CCF-A 系统框架背书
    reuse_cost: 低
sources:
  - paper_title: Slicing-Based Task Offloading in Space-Air-Ground Integrated Vehicular Networks
    doi: 10.1109/TMC.2023.3283852
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# SAGIN 车联网切片式任务卸载

## 单行摘要

面向空天地一体车联网（卫星 + 地面基站 + 无人机基站异构接入），提出服务导向的 RAN 切片任务卸载框架：大时间尺度上按业务流波动自适应调整切片窗口长度并做通信/计算资源切片，小时间尺度上由 DDQN 在窗口内完成任务调度，最大化长期任务完成数，同时平衡时延敏感/时延容忍业务的差异化 QoS 与切片控制信令开销。

## 方法快照

- 异构接入：卫星、地面 BS、无人机 BS 共同服务高速车辆；任务分时延敏感/时延容忍两类，用队列模型刻画到达与完成过程。
- 双层闭环：窗口到来时 MEC 控制器重新配置切片资源（窗口长度与各切片份额均为决策变量）；窗口内部 DDQN 学习不同任务与链路状态下的调度动作。
- 窗口自适应：切片窗口长度是连接长期负载波动与短期调度决策的显式建模对象，避免固定周期控制在高峰期失灵。
- 开销权衡：切片重配置带来控制信令开销，框架在 QoS 保障与开销之间显式平衡。
- 验证：数值仿真 + OpenITS 交通流 trace 驱动仿真（混合来源）；硬件为 Ryzen5 3500X + GTX 1660 SUPER；交通流数据平台公开但论文未放出完整代码（artifact partial）。

## 比赛映射要点

- 黑客松：DDQN 窗口内调度 + 外层周期性资源重配的分层结构，适合实时调度类赛题快速实现；公开 trace（OpenITS）让评测天然贴近真实负载，区别于纯随机负载 demo。
- 数模：交通/负载波动类赛题中"决策控制周期"这一变量本身值得显式建模（窗口过短开销大、过长失灵），该论文提供了完整的变量化与权衡论证模板。
- 双创：智慧农业园区/冷链车队等多业务并存场景，引用其差异化 QoS 切片叙事（实测数字需自建）。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Shen2024_空天地一体车联网中的切片式任务卸载`（frontmatter 4 枚举字段已迁移到本卡：venue_tier/evidence_tier/paper_role/reproducibility_level）。
- bib 回填：citekey `shen2024SlicingBasedTaskOffloading` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写；验证类信息（simulation + trace-driven/OpenITS/复现性 medium）承自 vault 页自评，如需引用请以论文原文复核。
