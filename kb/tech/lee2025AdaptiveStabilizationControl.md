---
id: lee2025AdaptiveStabilizationControl
name: BAASC：浮力辅助四旋翼的DRL自适应稳定控制
field: [深度强化学习, 姿态控制, 原型验证]
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
    edge: 长航时悬停监测硬件方案——氦气球净浮力抵消大容量电池增重、DRL 抑制阵风倒立摆效应，真实户外原型与微风/阵风对照实验为智慧农业长时驻留监测类申报提供实机验证背书（TMC 2025）
    reuse_cost: 高
  - track: 黑客松-数据与算法
    edge: 倒立摆效应线性化模型+姿态偏差奖励函数+多机在线采集/服务器离线 RNN-DQN 训练再回灌的安全训练范式，可迁移到机器人与飞行器稳定控制类赛题（9 维状态、4 旋翼转速动作的接口清晰）
    reuse_cost: 中
sources:
  - paper_title: "Adaptive Stabilization Control by Deep Reinforcement Learning for Hovering Drone Surveillance"
    doi: 10.1109/TMC.2025.3548421
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# BAASC：浮力辅助四旋翼的DRL自适应稳定控制

## 单行摘要

面向长航时悬停监视任务，设计带四个 24 英寸氦气球的浮力辅助四旋翼（净浮力约抵消 5000 mAh 电池相对 2600 mAh 的增重），并针对气球带来的阵风「倒立摆效应」提出 BAASC：以位置、roll/pitch、期望姿态与摆动加速度为 9 维状态、四旋翼转速为动作、姿态偏差构造奖励，用多机在线采集经验 + 服务器离线 RNN/DQN 训练再回灌微调的方式训练稳定策略；真实户外实验中 BAASC 在阵风下相对非浮力辅助 PID 方案飞行时间提升 112.8%，而浮力辅助+PID 基线 47 秒即坠机。

## 方法快照

- 浮力辅助结构：H380 V4 机体 + Pixhawk 飞控 + AIRGEAR450/KV880 电机，78 cm 碳纤管挂 4 个氦气球；飞行时间模型 T = C×D/((m_b+m_f)×I)×3600，说明「增大电池+浮力抵消增重」比单纯加电池有效。
- 倒立摆建模：气球受风拖动机体摆动，线性化得水平面摆动方程（含 3g/4L 项）；roll/pitch 超 30 度坠毁作为安全边界。
- BAASC 训练范式：多台真机并行在线采集 (s,a,r) → 服务器端 RNN 组织时序 + Q 值/策略更新 → 策略回灌在线微调，规避真机端到端长时训练的坠机风险。
- 对照实验：BAASC / BAPID（浮力+PID）/ NBAPID（非浮力+PID）三组拆分验证「浮力是否有用」与「DRL 是否必要」；阵风下 BAASC 姿态偏差标准差 2.523°，远优于 BAPID 的 10.29°，接近非浮力方案。

## 比赛映射要点

- 双创申报：长航时驻留监测（农田长时巡查、悬停监测）的硬件+控制一体化方案，有真机与户外风场实验数据支撑；硬件复现成本高（气球选型、挂载结构、风场测试），适合作为申报方案的技术亮点而非直接落地组件。
- 黑客松/算法赛：DRL 稳定控制的状态/动作/奖励接口与「在线采集+离线训练」安全范式可迁移到仿真环境下的机器人控制类赛题；倒立摆线性化模型可作物理建模素材。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Lee2025_基于深度强化学习的浮力辅助无人机自适应稳定控制`（4 枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `lee2025AdaptiveStabilizationControl` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写；复现性 medium 与 prototype+field_test（真实户外飞行）形态承自 vault 页自评（artifact_availability: unknown），如需引用请以论文原文复核。
