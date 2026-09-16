---
id: ning2025JointOptimizationData
name: MCDRL：无线供能IoT的UAV数据采集与轨迹联合优化
field: [无线供能物联网, 轨迹规划, 多智能体强化学习]
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
    edge: 农田/野外低功耗传感网「UAV 空中补能 + 数据回收」运维方案——智慧农业物联网节点换电难痛点的直接技术支撑，安全飞行约束显式建模增强方案可信度
    reuse_cost: 低
  - track: 黑客松-数据与算法
    edge: CMDP 安全惩罚约束 + 奖励/惩罚双 critic + 个性化注意力的 MARL 骨架，再叠 matching 理论做连接分配的两级决策结构，可迁移到带安全约束的多智能体调度赛题
    reuse_cost: 中
sources:
  - paper_title: Joint Optimization of Data Acquisition and Trajectory Planning for UAV-assisted Wireless Powered Internet of Things
    doi: 10.1109/TMC.2024.3470831
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# MCDRL：无线供能IoT的UAV数据采集与轨迹联合优化

## 单行摘要

面向多 UAV 辅助的无线供能物联网，联合优化三维轨迹与 ISD-UAV 连接分配：先把轨迹规划写成带安全惩罚约束的 CMDP，用 MCDRL（actor-critic + 奖励/惩罚双 critic + 个性化注意力）学习每架 UAV 的三维机动策略，再用匹配理论算法为覆盖范围内设备分配服务 UAV，在飞行安全、设备 QoS 与任务完成约束下最大化系统能效。

## 方法快照

- 场景：多 UAV 为大量低电量智能感知设备（ISD）先供能再回收数据，UAV 位置为三维变量且须满足最小安全间距防空中碰撞。
- 轨迹子问题：CMDP 把安全距离违反显式写成惩罚约束（区别于把安全作为隐含奖励的既有 RL 轨迹方法）。
- MCDRL：每个 UAV 维护奖励 critic 与惩罚 critic；个性化注意力机制动态关注更关键的邻居状态，提升多机协同与可扩展性。
- 连接分配：轨迹确定后用基于匹配理论的算法按能效优先级为覆盖范围内 ISD 匹配 UAV。
- 验证：Melbourne CBD 真实地理位置 + YouTube 视频服务数据集驱动的仿真（Python 3.7 + PyTorch 1.1.0，Intel Xeon Silver 4210R）；未开源。

## 比赛映射要点

- 双创申报：农业物联网/环境监测传感网的「无人机巡检补能 + 数据采集」一体化运维叙事有直接落点；「轨迹 + 匹配 + 约束」分层联合优化的方案结构可直接写进申报书技术路线。
- 黑客松/算法赛：约束型多智能体调度题（避碰、任务时限、能量预算）可复用双 critic 拆分目标与惩罚约束的建模技巧，两级决策链（先轨迹后匹配）本身就是清晰的算法分层。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Ning2025 无线供能物联网中的UAV数据采集与轨迹联合优化`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `ning2025JointOptimizationData` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写。
- 复现性承自 vault 页自评（medium，仿真 + trace 驱动、未开源）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
