---
id: song2024MethodsAssignUAVs
name: IoT网络K覆盖与补能的UAV多时隙分配（MPC-MILP与MCTS）
field: [覆盖调度, 能量管理, 滚动优化]
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
  - track: 数模-数据分析与决策
    edge: 「MILP 全知基准 → GMM 预测+MPC 滚动求解 → MCTS 轻量在线」的三级求解阶梯是未来不确定条件下调度决策类数模题的现成方法论，含完整近似比对标（MPC 与 MCTS 的 coverage lifetime 分别为 MILP 的 81.04% 与 67.07%）
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 太阳能充电平台+多 UAV 监测/回充换班的持续覆盖系统，直接支撑农田 IoT 持续监测与光伏补能调度的智慧农业申报场景（附 DJI Mavic 3+HEISHA C300 充电桩的实测组件清单）
    reuse_cost: 低
sources:
  - paper_title: "Methods to Assign UAVs for K-Coverage and Recharging in IoT Networks"
    doi: 10.1109/TMC.2023.3259461
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# IoT网络K覆盖与补能的UAV多时隙分配（MPC-MILP与MCTS）

## 单行摘要

在太阳能充电平台支持的 IoT 监测网络中，论文按离散时隙联合决定每架 UAV 去监测点（维持 K 覆盖）还是回充电平台（补能），目标最大化连续满足 K-coverage 的时隙数（K-coverage lifetime）：先建需要非因果信息的 MILP 作最优基准，再用 GMM 预测未来充电能量把 MPC-MILP 变成可在线执行方案，并设计 MCTS 启发式降低计算开销。

## 方法快照

- 系统状态：充电平台储能受太阳能随机到达影响且有电量溢出损失；UAV 电量同时受飞行距离、悬停监测与充电影响——能量在时间上强耦合。
- MILP 基准：已知未来能量到达的理想条件下求全局最优分配（上界）。
- MPC-MILP：控制器用 GMM 预测未来一段时间的平台能量到达，滚动求解 MILP（可部署近似，约达 MILP 的 81.04% coverage lifetime）。
- MCTS：把每时隙的替换/回充决策组织为树搜索，靠 rollout 评估 coverage lifetime（更轻量的在线启发式，约 67.07%）。
- 验证：Python + Gurobi 数值仿真，合成监测拓扑 + 测量驱动太阳能模型，含复杂度分析与多组参数扫描；i5 2.4GHz/8GB 可运行，未公开完整代码。

## 比赛映射要点

- 数模：三阶梯求解（上界-滚动优化-在线启发式）几乎可模板化套进任何"预测+优化"题：先给全知最优解定界，再给可执行近似并量化差距；"预测器+MILP"的组合是数模答卷的高分结构。
- 双创申报：持续监测系统的核心痛点是"谁监测、谁补能、何时换班"的时间耦合；光伏补能+换班调度叙事贴合农业长期监测项目，硬件组件均有市售对应，落地感强。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Song2024_面向IoT网络K覆盖与补能的UAV分配方法`（四枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `song2024MethodsAssignUAVs` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写；复现性 medium 与 Python/Gurobi 数值仿真形态承自 vault 页自评（artifact_availability: unknown，未公开完整代码），如需引用请以论文原文复核。
