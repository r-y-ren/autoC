---
id: zeng2024A3DAdaptiveAccurate
name: A3D：边缘辅助无人机的自适应高精导航服务调度
field: [边缘智能, 无人机导航, 服务调度]
published: 2024-01-01
maturity: paper
directions: [黑客松与数据竞赛, 数模与时序预测, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE/ACM Transactions on Networking
  runnable: false
competition_fit:
  - track: 黑客松-数据与算法
    edge: 把导航推理当服务调度的 DRL 调度器（联合决策执行位置、分辨率、压缩比三变量）可直接迁移到端云协同推理/算力分配类赛题，有 Jetson Nano+AirSim 原型链路支撑方案可信度
    reuse_cost: 中
  - track: 数模-预测与评估
    edge: QoN 指标把导航时延与精度合并为统一评价量，是评估类赛题「多指标合成单一度量」的直接范式，可迁移为服务质量/系统效能评价体系设计
    reuse_cost: 低
  - track: 双创-文书与申报
    edge: 低算力机载平台+边缘算力共享的农业无人机巡检架构（容器化多机边缘推理）可作为智慧农业低空感知方案的技术支撑点
    reuse_cost: 低
sources:
  - paper_title: "A3D: Adaptive, Accurate, and Autonomous Navigation for Edge-Assisted Drones"
    doi: 10.1109/TNET.2023.3297876
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# A3D：边缘辅助无人机的自适应高精导航服务调度

## 单行摘要

针对 DNN 驱动的自主无人机在机载算力有限、网络动态变化下的导航难题，提出 A3D 系统——把导航视为边缘辅助的服务调度问题，用 DRL 神经调度器联合决策模型执行位置（本地/边缘）、输入分辨率与图像压缩比，并定义导航质量 QoN 把时延与精度合并为统一目标，在真实校园路线原型与 AirSim 仿真中验证收益。

## 方法快照

- 指标设计：QoN 把导航建模为一串必须在误差阈值内及时完成的服务事件，统一时延与精度两个维度，并关联可达飞行距离。
- 调度建模：不简单做 offload 二选一，而是同时优化执行位置、输入分辨率、压缩比三类配置变量，适配带宽与环境复杂度动态。
- 状态增强：引入环境信息编码模块，提升调度器对动态环境的状态抽象能力。
- 边缘侧：容器化导航模型 + 资源分配算法，支持多无人机并发共享边缘推理能力。
- 验证链路完整：simulation + prototype + field_test 三级证据，组件含 PyTorch、stable-baselines（A2C/DQN）、DroNet，硬件为 Jetson Nano + 桌面边缘服务器。

## 比赛映射要点

- 黑客松/算法赛：端云协同推理调度赛题可直接套用其「三变量联合 DRL 调度 + QoN 目标」结构；无完整边缘环境时也可退化为仿真调度器实现。
- 数模评估题：QoN 的「误差阈值内及时完成事件」定义是复合评价指标设计的可搬运范式（如配送时效、救援响应评估）。
- 双创申报：农业巡检/植保无人机的边缘智能架构段落可直接引用其机载-边缘分工与容器化多机服务设计。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Zeng2024_A3D边缘辅助无人机自适应高精导航`（4 枚举字段承自页 frontmatter）。
- bib 回填：citekey `zeng2024A3DAdaptiveAccurate` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写。
- 复现性 medium 承自 vault 页自评：验证含真实校园原型与公开带宽 traces，但论文未给出完整工程代码与 trace 链接，如需引用请以原文复核。
