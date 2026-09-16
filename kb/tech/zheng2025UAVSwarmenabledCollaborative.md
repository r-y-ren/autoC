---
id: zheng2025UAVSwarmenabledCollaborative
name: 低空经济灾后UAV蜂群协同通信两阶段优化
field: [无人机自组网, 协同波束形成, 应急通信]
published: 2025-01-01
maturity: paper
directions: [数模与时序预测, 创新创业大赛, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 两阶段分解范式——第一阶段求最优多路径流量路由并给出网络传输率理论上界，第二阶段用 DM-PSO 联合优化参与 UAV 的激励权重与部署位置逼近上界；"上界-实际值-间隙"的结果评价结构可直接写进数模论文，比单段元启发式更有说服力
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 低空经济 + 灾后应急通信是双创高热度叙事组合——UAV 蜂群协同自组网 + HAP 高空协调枢纽 + 三类意外场景鲁棒性验证，可整体作为应急通信/低空经济项目的技术方案骨架
    reuse_cost: 低
  - track: 黑客松-数据与算法
    edge: diffusion model 增强 PSO（DM-PSO）的元启发式改造思路可移植到连续空间部署/布点优化类算法题，作为对标准 PSO 的差异化升级点
    reuse_cost: 中
sources:
  - paper_title: "UAV Swarm-Enabled Collaborative Post-Disaster Communications in Low Altitude Economy via a Two-Stage Optimization Approach"
    doi: 10.1109/TMC.2025.3583510
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 低空经济灾后UAV蜂群协同通信两阶段优化

## 单行摘要

从低空经济视角设计面向灾后长距离通信的 UAV 蜂群协同自组网（灾区设备 → 多 UAV 蜂群协同波束形成中继 → 远端 AP，HAP 作高空协调枢纽），第一阶段求最优多路径流量路由与理论传输率上界，第二阶段把实际系统写成 V-RPTRMOP 并用 DM-PSO 联合优化激励权重与部署位置使实际传输率逼近上界，并验证突发情形下的鲁棒性。

## 方法快照

- 架构分层：地面源端、多 UAV swarm 协同中继层、HAP 控制层（不直接转发数据，负责算法执行与控制策略生成）、远端 AP 目的端。
- 耦合关系：每架参与 UAV 的激励权重与部署位置共同决定链路传输率，因此路由只解决流量分配，物理层性能还取决于第二阶段部署优化——两者拆开而非揉进一个超大问题。
- 第二阶段：惩罚版变体 + diffusion model-enabled PSO，联合调整 UAV 位置与激励电流权重。
- 鲁棒性：专门评估三类 unexpected situations 对系统传输率的影响，比普通灾后覆盖工作更强调系统韧性。
- 验证：合成灾后协同通信网络场景仿真，明显优于传统单阶段或非协同方法（页内自评复现 medium）；仿真平台与 DM-PSO 代码未披露。

## 比赛映射要点

- 数模赛：先上界后逼近的两阶段结构天然适配网络设计/部署类赛题，理论上界与间隙可作结果评价与算法有效性论证。
- 双创申报：应急通信与低空经济双热点叙事，方案链完整（组网 + 协调枢纽 + 鲁棒性验证）。
- 算法赛：DM-PSO 元启发式改造套路可用于布点/部署类题目的优化器升级。

## 关联概念
- 低空经济（LAE）

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Zheng2025_低空经济灾后协同通信的两阶段优化`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `zheng2025UAVSwarmenabledCollaborative` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写。
- 复现性承自 vault 页自评（medium，仿真验证、平台与代码未披露）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
