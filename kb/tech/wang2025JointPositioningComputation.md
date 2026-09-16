---
id: wang2025JointPositioningComputation
name: PPO联合优化的多UAV放置与计算卸载
field: [移动边缘计算, UAV部署优化, 近端策略优化]
published: 2025-01-01
maturity: paper
directions: [黑客松与数据竞赛, 数模与时序预测, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 黑客松-数据与算法
    edge: PPO 统一学习「接入服务 UAV + 回传桥接 UAV」的角色化放置与卸载比例，策略能在随机 UAV 故障下快速重构网络——应急组网 / 容错调度类赛题的可迁移方案，超越「把 UAV 放到热点上方」的静态最优思路
    reuse_cost: 中
  - track: 数模-数据分析与决策
    edge: 双层优化（上层定位置与网络形成、下层定任务卸载）转单阶段 RL 策略求解的范式，加上二维高斯簇用户分布与连通性约束的建模，适配设施选址 + 任务分配类数模题
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 灾后 / 偏远地区等基础设施稀缺场景下临时低时延网络服务方案的技术支撑点（TMC 2025，故障韧性有实验实证）
    reuse_cost: 低
sources:
  - paper_title: "Joint Positioning and Computation Offloading in Multi-UAV MEC for Low Latency Applications：A Proximal Policy Optimization Approach"
    doi: 10.1109/TMC.2025.3562806
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# PPO联合优化的多UAV放置与计算卸载

## 单行摘要

在缺乏蜂窝基础设施的动态多 UAV MEC 网络中，UAV 既要贴近用户簇降低接入时延，又要保持与基站及彼此的连通以形成回传网络——位置与卸载比例彼此影响，不能分开优化。论文先构建双层基线优化（上层决定 UAV 网络形成与位置，下层决定任务卸载），再用 PPO 统一学习放置与卸载决策：部分 UAV 服务用户、部分承担回传桥接，训练后的策略可按不同初始位置快速重构网络，并在随机 UAV 故障下维持恢复能力，降低低时延应用端到端时延。

## 方法快照

- 场景设定：用户按二维高斯簇分布（对应灾后 / 偏远热点），UAV 固定高度运行，角色分为接入层与回传桥接层。
- 求解路线：双层优化基线 → PPO 统一策略（放置 + 卸载联合动作空间）。
- 韧性验证：随机 UAV 故障实验表明学到的是可恢复策略而非单场景静态最优解；任务拆分在 BS 与不同 UAV 间快速收敛。
- 验证：Python 3.9 + TensorFlow 2.11.0 数值仿真、合成用户簇场景，训练参数披露较全；代码未公开。

## 比赛映射要点

- 黑客松算法类：应急通信 / 无人机组网赛题中，「角色分工 + 故障恢复」是差异化考核点，PPO 联合策略思路与故障实验设计可直接迁移。
- 数模决策类：选址-分配双层模型的 RL 化求解路径与用户簇建模方式可借鉴。
- 双创申报：应急通信保障 / 偏远地区网络覆盖类项目书的技术方案支撑。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Wang2025_PPO驱动的多UAV_MEC联合定位与计算卸载`（4 枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `wang2025JointPositioningComputation` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）；标题中「: 」按本跑批 YAML 约定改写为全角冒号。
- `published` 仅年份已知（2025），按 2025-01-01 填写；复现性 medium 与 simulation/synthetic 验证形态承自 vault 页自评（artifact_availability: unknown），如需引用请以论文原文复核。
