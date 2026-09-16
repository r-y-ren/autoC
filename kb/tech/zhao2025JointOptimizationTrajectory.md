---
id: zhao2025JointOptimizationTrajectory
name: UAV-MEC轨迹卸载缓存迁移的Lyapunov联合优化
field: [移动边缘计算, 在线优化, 无人机轨迹]
published: 2025-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: Lyapunov 在线控制（队列稳定项 + 收益项）把长期随机调度问题拆成逐时隙决策，是任务动态到达 + 多服务主体类赛题的标准建模范式；任务在执行/缓存/迁移三态间转移的建模视角超出常规一次性卸载设定，可作为差异化模型结构
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 部署-关联-卸载-调度-迁移带宽的多层决策交替优化框架（BCD + SDR/rounding 处理调度 QCQP）可迁移到分布式任务调度与带宽分配类算法题，层间迭代结构清晰、易改写
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 基础设施缺失区域（农田/山区/灾区）多无人机算力服务组织方案——以任务生命周期（缓存等待、跨机迁移）而非单次卸载组织边缘算力，支撑申报书技术方案完整性论证
    reuse_cost: 低
sources:
  - paper_title: "Joint Optimization of Trajectory, Offloading, Caching, and Migration for UAV-assisted MEC"
    doi: 10.1109/TMC.2024.3486995
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# UAV-MEC轨迹卸载缓存迁移的Lyapunov联合优化

## 单行摘要

在基础设施缺失区域的多 UAV 协同 MEC 服务系统中，把轨迹部署、任务卸载、任务缓存与任务迁移写进同一 Lyapunov 在线控制框架，经 BCD 分解逐时隙联合决策任务交给谁、是否缓存等待、何时迁移以及 UAV 是否移向任务热点，目标是长期吞吐提升、执行时间降低与队列稳定。

## 方法快照

- 问题特征：用户任务随位置变化跨时隙进入不同 UAV 覆盖区，真正难点是任务在多时隙、多 UAV 间的持续服务组织，而非单时刻分配。
- 关键变量：UAV 部署（task-scheduling-oriented deployment）、用户关联、任务卸载比例、任务缓存决策、迁移链路带宽分配；亮点是把 task caching（区别于 content caching）作为一等主变量。
- 求解管线：Lyapunov 把长期随机问题拆为 one-slot 逐时隙问题 → BCD 在部署/关联/卸载/调度/迁移带宽间迭代 → 调度 QCQP 经 SDR + rounding 处理。
- 验证：MATLAB R2021a + CVX/YALMIP/MOSEK + PyTorch 1.12 的合成场景仿真，页内记录实验栈披露完整（复现 medium）；开源未说明。

## 比赛映射要点

- 数模赛：动态任务到达 + 队列稳定性的多期调度建模可直接套用 Lyapunov 范式，队列长度/稳定性可写进结果评价维度。
- 黑客松/算法赛：三态任务状态机（执行/缓存/迁移）+ 多层决策交替优化的求解器骨架易于改写复用。
- 双创申报：偏远农业区多机算力服务的任务全生命周期组织叙事。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Zhao2025_轨迹卸载缓存与迁移联合优化的UAV辅助MEC`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `zhao2025JointOptimizationTrajectory` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写。
- 复现性承自 vault 页自评（medium，数值仿真、实验栈披露完整但开源未说明）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
