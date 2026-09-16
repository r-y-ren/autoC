---
id: wu2025ReconfigurableIntelligentSurface
name: TRAIL：RIS辅助UAV群智感知Transformer强化学习
field: [移动群智感知, UAV-RIS, Transformer 强化学习]
published: 2025-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Computers
  runnable: false
competition_fit:
  - track: 数模-预测与评估
    edge: Transformer 编码轨迹历史长时依赖再喂给决策网络，"历史序列特征提升在线决策稳定性"的范式可迁移到时序轨迹/需求预测类赛题，与无记忆的逐时隙决策基线形成对比
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: Transformer + PER-DDQN 处理连续轨迹与离散相位混合动作空间的模板完整（Python/PyTorch 实现路线、KAIST 公开轨迹 trace-driven 验证），可改造为序列决策类赛题组件
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 城市/山地 NLoS 环境下无人机数据采集（群智感知）与 RIS 补盲方案支撑点，契合智慧农业果园巡检、城市感知类申报的数据采集层叙事
    reuse_cost: 低
sources:
  - paper_title: "Reconfigurable Intelligent Surface Assisted UAV-MCS Based on Transformer Enhanced Deep Reinforcement Learning"
    doi: 10.1109/TC.2025.3585361
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# TRAIL：RIS辅助UAV群智感知Transformer强化学习

## 单行摘要

针对 RIS 辅助 UAV 移动群智感知（MCS）场景中 NLoS 条件下单纯优化水平轨迹难以兼顾通信质量与能耗的问题，提出 TRAIL：把联合优化写成 MDP，先用 Transformer 从 UAV 轨迹状态序列中提取长期依赖特征，再输入 PER-DDQN 学习 UAV 三维轨迹与 RIS 离散相位的联合动作策略——决策不只瞬时最优，而是显式利用历史状态序列，在城市/遮挡环境中更稳定地提升吞吐并压低能耗。

## 方法快照

- 系统设定：多 UAV 下行通信增强的 MCS 系统，RIS 部署于建筑外立面改善 NLoS，地面 PoI 分布且可有移动性。
- 信道与约束：Rician 信道，RIS 离散相位量化显式建模；目标为吞吐与 UAV 能耗的联合优化（非单一速率最大化）。
- 学习架构：Transformer 编码状态序列的长期依赖 → PER-DDQN（优先经验回放双 Q 学习）输出连续轨迹 + 离散相位的联合动作。
- 验证：Python 3.7 + PyTorch 1.7.0，合成环境 + KAIST 公开移动轨迹数据 trace-driven 双验证（Intel i9-13900K），未开源。

## 比赛映射要点

- 数模预测题：轨迹历史序列建模思想可平移到车辆/人群/需求时序预测——用序列编码器替代逐点特征是与 ARIMA/普通 NN 基线拉开差距的手段。
- 黑客松/算法赛：混合动作空间（连续控制量 + 离散选择）的 Transformer+DRL 骨架适用于路径规划与资源选择耦合类赛题；KAIST 轨迹做 trace-driven 评测的思路可复用为更可信的实验设计。
- 双创申报：无人机巡检/数据采集平台在遮挡环境下的通信保障叙事（RIS 补盲 + 长时记忆决策）。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Wu2025_TRAIL面向UAV群智感知的RIS辅助Transformer强化学习`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `wu2025ReconfigurableIntelligentSurface` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写。
- 复现性承自 vault 页自评（medium，仿真 + trace 驱动、未开源，KAIST 为公开数据集）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
