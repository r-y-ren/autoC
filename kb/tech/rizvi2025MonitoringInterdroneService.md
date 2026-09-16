---
id: rizvi2025MonitoringInterdroneService
name: 面向韧性运行的无人机间服务干扰监测（PIS 评估）
field: [无人机服务系统, 时空数据分析, 服务韧性]
published: 2025-01-01
maturity: paper
directions: [创新创业大赛, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Services Computing
  runnable: false
competition_fit:
  - track: 双创-文书与申报
    edge: 低空经济与无人机配送运行监测的技术支撑点——干扰 taxonomy + PIS 严重度量化可写成"共享空域服务韧性管理"模块，嵌入智慧物流/农业植保多机调度类申报（TSC 2025，真实配送数据验证）
    reuse_cost: 低
  - track: 黑客松-数据与算法
    edge: 轨迹时空重叠判据 + 启发式干扰检测 + 影响评分（PIS）是可独立复用的轨迹数据分析管线，可迁移到轨迹异常/事件检测类数据赛题，快于穷举与 K-Means 基线且检测准确率约 95%
    reuse_cost: 中
sources:
  - paper_title: "Monitoring Inter-Drone Service Interference for Resilient Operations"
    doi: 10.1109/TSC.2025.3568245
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 面向韧性运行的无人机间服务干扰监测（PIS 评估）

## 单行摘要

针对多服务提供方共享 skyway 网络的无人机配送场景，论文提出节点级/航段级干扰 taxonomy、基于时空邻近性的启发式检测算法与 PIS（Percentage Impact Score）严重度评估，把"不会撞却拖慢配送"的效率型干扰正式写进服务系统 QoS 语义，为改航、限流与充电调度等韧性控制提供前瞻依据。

## 方法快照

- 系统建模：无人机配送建模为服务系统（功能属性=包裹在 skyway 节点间交付，非功能属性=能耗/成本/交付时间）；super-provider 拥有全局航迹视图，可在服务执行前做干扰监测。
- 干扰 taxonomy：区分节点级干扰（如充电桩拥塞）与航段级干扰（共享航段时空近距飞行，经气动作用恶化实际能耗）；本文聚焦航段级负干扰。
- 检测：以三维空间时间重叠、垂直间距与相对位置构造启发式规则，快速筛出疑似干扰事件。
- 严重度评估：PIS 衡量干扰对电池消耗、额外充电时间与到达时刻的影响，避免把所有近距事件一视同仁。
- 验证：trace-driven，真实配送/skyway 数据，检测准确率约 95%，显著快于穷举与 K-Means 基线。

## 比赛映射要点

- 双创申报：低空经济是当前申报热词；"运行监测-干扰识别-严重度评估"三层可写成多机协同调度项目的韧性管理子系统，区分度高于单纯讲航线规划。
- 黑客松/数据赛：时空重叠判据 + 事件评分的管线可直接搬到轨迹异常检测、交通事件识别类赛题；"检测 + 定量影响评分"的两步式输出比纯分类更有说服力。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Rizvi2025_面向韧性运行的无人机间服务干扰监测`（venue_tier/evidence_tier/paper_role/reproducibility_level 四枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `rizvi2025MonitoringInterdroneService` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写；复现性 medium 与 trace-driven 验证形态承自 vault 页自评（artifact_availability: unknown，开源情况未说明），如需引用请以论文原文复核。
