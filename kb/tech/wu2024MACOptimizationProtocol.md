---
id: wu2024MACOptimizationProtocol
name: EC-CMAC：双感知协作UAV-MAC协议
field: [FANET, MAC 协议, 协作传输]
published: 2024-01-01
maturity: paper
directions: [创新创业大赛, 数模与时序预测]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 双创-文书与申报
    edge: 恶劣环境（重雾浓烟/高速机动）与灾后应急通信下无人机自组网的链路层方案支撑点，网络寿命与包投递率双指标叙事契合山地果园巡检、应急救援类申报
    reuse_cost: 低
  - track: 数模-数据分析与决策
    edge: 剩余能量/信道增益/方位多因素加权的中继选择与直接/协作传输自适应切换，可抽象为带多目标权衡（寿命-时延-投递率）的决策子问题嵌入网络优化赛题
    reuse_cost: 中
sources:
  - paper_title: "MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy Consumption and Channel Gain"
    doi: 10.1109/TMC.2024.3372253
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# EC-CMAC：双感知协作UAV-MAC协议

## 单行摘要

面向重雾、浓烟和高速机动等恶劣环境下的 FANET，提出兼顾能耗与信道增益的协作 MAC 协议 EC-CMAC：先用信道传播模型估计所需发射功率，再综合节点剩余能量、信道增益、方向与位置从一跳邻居中选择中继，并在直接传输与协作传输之间自适应切换——把性能优化从常见的网络层路由下沉到链路层，以较小吞吐和时延代价换取网络寿命与包投递率提升。

## 方法快照

- 感知层：依据传播模型估计链路信道增益与所需发射功率（发送功率估计）。
- 节点状态层：感知候选中继的残余能量、方向与位置，多因素加权选中继。
- MAC 决策层：直接传输与协作转发自适应切换，恶劣链路下一跳邻居协作降低丢包。
- 评测指标：网络寿命、端到端时延、吞吐、包传输率；对比传统 MAC 与非协作转发协议。
- 验证：MATLAB 仿真（合成恶劣传输环境与高速机动场景，未开源）。

## 比赛映射要点

- 双创申报：应急救灾通信、山地/果园无人机巡检组网的方案支撑点——"链路层协作比单纯增大发射功率更可持续"是能耗论证的关键句。
- 数模决策题：中继选择本质是带能量/信道/几何多约束的加权选择问题，可嵌入无人机网络寿命最大化或多目标通信保障类赛题的求解框架。

## 关联概念
- 协作MAC协议

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Wu2024_双感知能耗与信道增益的协作UAV-MAC优化协议`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `wu2024MACOptimizationProtocol` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写。
- 复现性承自 vault 页自评（medium，仿真级、未开源）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
