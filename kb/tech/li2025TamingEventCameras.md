---
id: li2025TamingEventCameras
name: BioDrone：仿生事件相机无人机避障系统（FPGA软硬协同）
field: [事件相机, 无人机避障, 软硬件协同设计]
published: 2025-01-01
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
    edge: CEF 滤除→LEM 双目时空匹配→DOT 轨迹融合的异步事件流三段式低延迟管线（端到端低于 6.4 ms），可迁移到高速流式数据实时检测/感知类赛题，区别于先拼帧再处理的常规视觉管线
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 智慧农业植保/巡检无人机高速避障感知方案的技术支撑点（事件相机低功耗毫秒级感知 + FPGA 嵌入式部署 + ArduPilot 集成的完整工程叙事）
    reuse_cost: 低
sources:
  - paper_title: "Taming Event Cameras with Bio-Inspired Architecture and Algorithm: A Case for Drone Obstacle Avoidance"
    doi: 10.1109/TMC.2024.3521044
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# BioDrone：仿生事件相机无人机避障系统（FPGA软硬协同）

## 单行摘要

提出 BioDrone 事件相机避障系统：以仿生视觉通路为蓝本设计 CEF（交叉神经节启发的事件滤除）+ LEM（时空表示双目匹配）+ DOT（历史轨迹与实时观测融合）三段管线，并在 Xilinx Zynq-7020 上做 FPGA 软硬协同并行化、集成进 ArduPilot 飞控，使工业无人机在高速场景下实现端到端低于 6.4 ms 的避障感知延迟。

## 方法快照

- 感知输入：双目事件相机输出像素级异步事件流，避开帧相机高相对速度下的运动模糊。
- CEF：仿生交叉神经节机制快速滤除环境触发事件，缓解事件爆发淹没障碍信息。
- LEM：在时空表示上完成双目事件匹配，双目融合前移以降低事件「粘连」造成的定位延迟。
- DOT：融合历史轨迹与当前观测，持续预测障碍位置供规避决策。
- 硬件实现：像素级事件处理 FPGA 并行化（Zynq-7020），对比平台含 Jetson TX2；执行层对接 ArduPilot。
- 验证：prototype + 真实室内外实飞（field_test），自采事件流；未披露完整 HDL/驱动代码与数据集。

## 比赛映射要点

- 黑客松/算法赛：流式数据低延迟检测类赛题可套用「尽早滤除 + 时空匹配 + 状态融合」的管线分工；「传感器-算法-硬件协同共设计」的问题定义是差异化论证。
- 双创申报：低空经济/植保无人机场景的感知亮点叙事——事件相机高速低功耗 + 嵌入式部署，工程完整度高、评审友好。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Li2025_BioDrone基于事件相机的无人机避障`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `li2025TamingEventCameras` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写。
- 复现性承自 vault 页自评（medium，prototype + 实飞验证但未披露完整代码与数据）；signal.runnable 如实标 false。
