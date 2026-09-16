---
id: chen2025JointTrajectoryOptimization
name: Lyapunov辅助DRL的UAV轨迹与资源联合优化（JTORA）
field: [无人机轨迹优化, 资源分配, 深度强化学习]
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
  - track: 黑客松-数据与算法
    edge: Lyapunov 处理长期约束 + SAC 管连续控制 + 凸优化求结构化子问题解析解的混合求解范式，可直接迁移到带长期预算的在线调度/连续控制类赛题，避免纯 DRL 或纯解析法单打独斗
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 智慧农业无人机在用户/目标移动、任务随机到达条件下的长期能耗与服务稳定性方案支撑点
    reuse_cost: 低
sources:
  - paper_title: "Joint Trajectory Optimization and Resource Allocation in UAV-MEC Systems: A Lyapunov-Assisted DRL Approach"
    doi: 10.1109/TSC.2025.3544124
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# Lyapunov辅助DRL的UAV轨迹与资源联合优化（JTORA）

## 单行摘要

面向带用户移动（Gauss-Markov）与随机任务到达的单 UAV-MEC 系统，JTORA 用 Lyapunov 优化把长期能量与队列稳定性约束转化为逐时隙问题，再拆分求解：轨迹与通信资源（发射功率）交给 SAC 学习连续控制策略，计算资源分配（本地 CPU 频率与 UAV 侧算力）由凸优化给解析解——在保证 UAV 续航与队列稳定的同时最小化移动用户总能耗。

## 方法快照

- 系统建模：等长时隙；概率 LoS 信道使 UAV 位置直接影响卸载收益；任务随机到达进入用户队列，可本地处理或卸载 UAV。
- Lyapunov 转化：drift-plus-penalty 把多阶段 MINLP 的长期约束写入逐时隙目标（任务队列 + 虚拟能量队列）。
- 混合求解：SAC 负责 UAV 位置策略；凸优化负责给定位置下的功率与 CPU 分配——不让 DRL 独自承担全部求解压力。
- 理论边界：给出算法复杂度与长期性能分析，非纯经验性工程拼接。
- 验证：Python 3.8 + PyTorch 1.10.0 数值仿真（RTX 4070 Ti），未开源。

## 比赛映射要点

- 黑客松/算法赛：凡是"长期资源预算 + 每时隙决策 + 部分变量有解析结构"的题都可套用该三段式框架（Lyapunov 在线化 → 学习型控制 → 解析子问题），是相对端到端 DRL 基线的差异化与稳定性论证。
- 双创申报：农情巡检等场景下无人机长期作业的能耗-服务稳定性权衡叙事。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Chen2025_Lyapunov辅助DRL的轨迹与资源联合优化`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `chen2025JointTrajectoryOptimization` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写。
- 复现性承自 vault 页自评（medium，仿真级、实验资产信息部分给出但未开源）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
