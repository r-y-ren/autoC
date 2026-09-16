---
id: wang2024UAVassistedTargetTracking
name: Lyapunov空海协同目标跟踪与计算卸载
field: [移动边缘计算, 目标跟踪, Lyapunov 优化]
published: 2024-01-01
maturity: paper
directions: [数模与时序预测]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-预测与评估
    edge: BAS-Elman 轻量时序预测器（天牛须搜索优化 Elman 网络参数）在目标随机运动下预测下一时刻状态，配套「精度—能耗—队列长度」多指标权衡评估，适配移动目标轨迹预测与动态系统状态评估类数模题
    reuse_cost: 中
  - track: 数模-数据分析与决策
    edge: Lyapunov 把长期能量与队列稳定性约束转化为逐时隙在线决策、再与感知任务（图像分辨率选择）联动的闭环骨架，是资源受限动态调度赛题的标准解法结构，且强调感知质量与计算负载的正反馈耦合这一常被忽略的建模点
    reuse_cost: 中
sources:
  - paper_title: "UAV-assisted Target Tracking and Computation Offloading in USV-based MEC Networks"
    doi: 10.1109/TMC.2024.3396121
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# Lyapunov空海协同目标跟踪与计算卸载

## 单行摘要

在海上目标跟踪场景中，单架 UAV 机载相机持续跟踪移动目标，但高分辨率图像处理开销大、能量受限，故引入 USV 作为海上 MEC 服务器分担计算：两阶段框架先用 BAS-Elman 神经网络从历史状态预测目标运动实现轻量实时跟踪，再用 Lyapunov 优化把随机数据处理、计算卸载与资源分配转化为逐时隙确定性问题（JOISR 统一打包图像分辨率、处理方式与资源分配决策），联合平衡推进能耗、检测精度与队列稳定性。

## 方法快照

- 系统实体：单 UAV、多个 USV MEC 节点、海上随机运动目标（受海流影响）、图像任务队列。
- 跟踪环：BAS（天牛须搜索）优化 Elman 网络参数，从历史目标状态预测下一时刻运动，支撑实时跟踪控制。
- 卸载环：Lyapunov 优化引入队列稳定性惩罚，把长期能量与稳定性约束拆为逐时隙决策；JOISR 决策向量含图像分辨率、本地处理 / 卸载 USV、带宽与算力分配。
- 关键耦合：分辨率越高检测精度越好但处理能耗越大，处理结果又反哺跟踪策略——感知与计算正反馈闭环。
- 验证：数值仿真（合成随机海上环境），给出实时性分析与多组对比曲线；实现栈未披露。

## 比赛映射要点

- 数模预测与评估类：BAS-Elman 是可手写实现的轻量时序预测器（对比 LSTM 参数更少、可解释优化过程），适合作为「随机运动目标预测 + 精度 / 开销权衡评估」类题型的预测组件。
- 数模数据分析与决策类：Lyapunov 队列化 + 逐时隙在线决策 + 感知负载联动的建模结构，可直接套用到「能耗预算下的感知—计算—通信联合调度」题型。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Wang2024_USV辅助MEC中的UAV目标跟踪与计算卸载`（4 枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `wang2024UAVassistedTargetTracking` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写；复现性 medium 与 simulation/synthetic 验证形态承自 vault 页自评（artifact_availability: unknown），如需引用请以论文原文复核。
