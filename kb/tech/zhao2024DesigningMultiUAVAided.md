---
id: zhao2024DesigningMultiUAVAided
name: 多UAV无线供能动态通信的分层强化学习（MAHDRL）
field: [无线供能通信, 分层强化学习, UAV 轨迹优化]
published: 2024-01-01
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
  - track: 黑客松-数据与算法
    edge: "双阈值角色切换 + 双时间尺度分层 MARL 模板（上层 SAC 学连续轨迹与供能动作、下层 DQN 学子时隙离散调度），可直接迁移到'能量受限多智能体在连续控制 + 离散调度耦合'类赛题，比单层单时间尺度 DRL 有结构差异化"
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: "无人机给田间无线节点无线充电并回收数据的能量自维持农业传感网络方案支撑点（WPCN 架构 + 节点按电量动态换角色），适合'免维护/自供能农田监测'叙事"
    reuse_cost: 低
sources:
  - paper_title: "On Designing Multi-UAV Aided Wireless Powered Dynamic Communication via Hierarchical Deep Reinforcement Learning"
    doi: 10.1109/TMC.2024.3439556
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 多UAV无线供能动态通信的分层强化学习（MAHDRL）

## 单行摘要

研究多 UAV 辅助无线供能通信网络（WPCN）中节点在能量采集与数据传输之间的动态切换：放弃固定 harvest-then-transmit 周期，提出双阈值节点类型更新规则让节点按电量在 E-node（采集）与 I-node（传输）间动态换角色；对应地用双层 MAHDRL 处理不同时间尺度决策——上层 SAC 学习 UAV 连续轨迹与二元 WET（无线能量传输）动作，下层 DQN 在给定轨迹下学习子时隙级 WDC（无线数据采集）调度，在 UAV 机载能量约束下最大化全网总传输数据量。

## 方法快照

- 建模创新：节点角色本身是系统动态的一部分（双阈值切换），而非协议固定参数。
- 分层决策：连续控制（轨迹）与离散调度（子时隙 WDC）天然不同时间尺度，拆成 SAC + DQN 两层分别学习，层间以轨迹/调度结果耦合。
- 状态演化：显式建模 UAV 电量与节点电量双动态，是长期资源管理问题而非单时隙优化。
- 可扩展性验证：不同 UAV 数量与网络规模下的训练/测试对比。
- 验证：Python 3.9.12 + PyTorch 1.12.1 仿真（合成场景，未开源，无硬件验证）。

## 比赛映射要点

- 黑客松/算法赛：能源受限的多智能体调度题（充电车 + 传感网、无人机补给 + 数据回收）可复用"角色动态切换 + 分层 RL"结构；SAC 管连续、DQN 管离散的分层模板比强行混合动作空间更容易训练与讲解。
- 双创申报：自供能农田监测网络（无人机巡田充电 + 收数）是智慧农业方向现成的技术路线素材，双阈值角色切换可作为协议层创新点写入申报书。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Zhao2024_多UAV辅助无线供能动态通信的分层强化学习设计`（4 枚举字段自 vault 页 frontmatter 迁移，reproducibility_level=medium）。
- bib 回填：citekey `zhao2024DesigningMultiUAVAided` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写。
- 复现性承自 vault 页自评（medium，框架/版本有披露但未发布代码）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
