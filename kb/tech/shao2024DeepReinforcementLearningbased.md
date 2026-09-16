---
id: shao2024DeepReinforcementLearningbased
name: 抗干扰UAV辅助MEC的PER-MATD3联合资源管理
field: [多智能体强化学习, 移动边缘计算, 抗干扰通信]
published: 2024-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: CPU 频率调节+带宽分配+信道选择三域联合的资源管理建模（时延能耗加权成本最小化），为"通信-计算联合调度"类赛题提供完整系统模型与基线设置，JSC 干扰感知把对抗条件显式写进约束
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: MATD3+优先经验回放（PER-MATD3）处理多智能体连续动作空间是可迁移的 RL 工程组件；附 DJI Tello+Raspberry Pi 4B+USRP 室内原型路线，适合快速搭出可演示的干扰规避调度 demo
    reuse_cost: 中
sources:
  - paper_title: "Deep Reinforcement Learning-Based Resource Management for UAV-assisted Mobile Edge Computing against Jamming"
    doi: 10.1109/TMC.2024.3432491
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 抗干扰UAV辅助MEC的PER-MATD3联合资源管理

## 单行摘要

面向恶意干扰下的多 UAV 辅助 MEC，论文把 CPU 频率调节、带宽分配与信道选择同时写入多智能体连续控制问题，提出带优先经验回放的 PER-MATD3 与干扰感知的 JSC 机制，在仿真与室内原型实验中同时降低系统时延、能耗与综合成本。

## 方法快照

- 问题建模：多 UAV 既算又传，状态含 CPU 频率、CSI、带宽占用、jammer 状态与用户负载；动作覆盖频率调节、带宽分配、信道选择三域；目标是时延与能耗的加权系统成本最小化。
- 干扰感知（JSC）：显式感知被 jammer 占据的信道，信道选择从普通资源分配升级为带感知的防御动作，同时规避多 UAV 共信道干扰。
- 学习算法：MATD3 处理多智能体高维连续动作，prioritized experience replay 提升关键经验利用率、加快收敛。
- 验证：1000m×1000m 区域、4-12 架 UAV、5MHz 带宽仿真；PER-MATD3-JSC 在成本/时延/能耗上优于 MATD3、单智能体 TD3、静态频率与随机策略；室内原型用 DJI Tello + Raspberry Pi 4B + USRP N210/X310 验证频谱感知与信道规避。

## 比赛映射要点

- 数模：抗干扰条件下的"计算+通信"联合资源分配是少见的复合题型；把对抗写进约束、把三域决策合成一个成本函数的建模路径可直接迁移，基线设置（静态频率、随机策略、单智能体 TD3）现成可对照。
- 黑客松/算法赛：PER-MATD3 与 JSC 是两个可独立拆用的组件；硬件清单与室内五信道实验设计给"仿真+实物"双轨原型提供了低成本参考。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Shao2024_抗干扰UAV辅助MEC资源管理`（四枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `shao2024DeepReinforcementLearningbased` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写；复现性 medium 与"仿真+原型"验证形态承自 vault 页自评（artifact_availability: unknown，未给出完整代码），如需引用请以论文原文复核。
