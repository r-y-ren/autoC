---
id: wu2024BeamformingPredictionBased
name: MRDDQN：UAV-RIS辅助THz波束预测
field: [THz 通信, UAV-RIS, 深度强化学习]
published: 2024-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: Science China Information Sciences
  runnable: false
competition_fit:
  - track: 数模-预测与评估
    edge: 把"逐次搜索最优配置"重构为"公开数据集训练的离散预测问题"（少量激活单元的采样信道特征 → 最优码字标签），这一寻优问题预测化范式可迁移到各类配置寻优/评估题
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: double-reward DDQN（可达速率+RIS 功率预算双奖励）+ DeepMIMO O1-drone 生成 30000 样本（80/20 划分、Adam 训练）的完整数据驱动决策管线可直接复用为离散动作预测组件
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 低空 THz 专网与 RIS 补盲覆盖的工程化叙事（波束训练开销从在线搜索降为离线预测）
    reuse_cost: 低
sources:
  - paper_title: "Beamforming Prediction Based on the Multireward DQN Framework for UAV-RIS-assisted THz Communication Systems"
    doi: 10.1007/s11432-024-4199-y
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# MRDDQN：UAV-RIS辅助THz波束预测

## 单行摘要

在 UAV 挂载 RIS 辅助的 THz OFDM 系统中，把 RIS 反射波束选择从"码本逐次训练搜索"重构为数据驱动的预测问题：基于 DeepMIMO O1-drone 生成 30000 个宽带信道样本，用少量激活 RIS 单元的采样信道签名构造状态，MRDDQN（double-reward DDQN）同时以可达速率与 RIS 功率预算两类奖励学习最优反射码字——降低波束训练开销的同时在速率与功率约束间显式权衡。

## 方法快照

- 系统设定：地面基站经 THz-OFDM 向多用户传输，UAV 挂载 RIS 于固定高度为被遮挡用户建立反射链路。
- 码本式控制：RIS 相位从预定义码本中选择而非连续求解，目标受最大可达速率与 RIS 激活功率共同约束。
- MRDDQN：双奖励刻画速率与功率预算表现，replay buffer + double-Q learning 稳定训练。
- 数据管线：DeepMIMO O1-drone 公开数据集生成 30000 样本，80% 训练 / 20% 测试，Adam 优化。
- 验证：仿真，对比穷举训练与传统波束训练流程（未开源）。

## 比赛映射要点

- 数模预测题：`配置寻优 → 监督化预测` 的转换思路（仿真器批量造样本 + 模型预测 Top 配置）适用于任何带昂贵评估器的赛题（参数寻优、方案评估）。
- 黑客松/算法赛：多奖励 DQN 的双奖励设计（性能指标 + 资源预算）是带约束离散决策题的通用技巧；DeepMIMO 样本生成管线可复用。
- 双创申报：低空专网/复杂遮挡环境通信增强的技术点。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Wu2024_多奖励DQN驱动的UAV-RIS辅助THz波束预测`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `wu2024BeamformingPredictionBased` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写。
- 复现性承自 vault 页自评（medium，仿真级、未开源，DeepMIMO O1-drone 为公开数据）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
