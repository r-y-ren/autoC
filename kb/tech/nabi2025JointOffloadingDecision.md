---
id: nabi2025JointOffloadingDecision
name: JOUR：UAV与HAP层次化空中计算的匹配-卸载联合决策
field: [层次化空中计算, 匹配博弈, 深度强化学习]
published: 2025-01-01
maturity: paper
directions: [创新创业大赛, 黑客松与数据竞赛, 数模与时序预测]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: GU-UAV 二元关联与 UAV-HAP 部分卸载拆成两层分别求解（离散匹配博弈+连续动作 SAC）的层次化分解，适配多级设施、混合决策变量的分级调度决策题；能耗/时延/负载均衡三目标奖励设计可复用
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 匹配博弈稳定关联+增强 SAC 连续资源控制的分层流水线，可迁移到分配+连续调度两段式算法题，比端到端混合动作 RL 更可解释、训练更稳
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 偏远农村与灾害场景空中算力补位平台的技术方案支撑（TMC 2025，HAP 稳定算力层+UAV 灵活接入层+负载调节）
    reuse_cost: 低
sources:
  - paper_title: "Joint Offloading Decision, User Association, and Resource Allocation in Hierarchical Aerial Computing: Collaboration of UAVs and HAP"
    doi: 10.1109/TMC.2025.3548668
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# JOUR：UAV与HAP层次化空中计算的匹配-卸载联合决策

## 单行摘要

面向偏远地区与灾害场景的层次化空中计算平台，构建地面接入层-UAV 边缘层-HAP 稳定算力层三级结构：地面用户先与某架 UAV 建立关联并做二元卸载决策，UAV 再决定任务本机处理还是部分转发到 HAP；JOUR 方案先用匹配博弈（GOUA）完成 GU 卸载决策与 GU-UAV 关联，再用增强版 Soft Actor-Critic（ESAC）处理 UAV 部分卸载比例与 UAV/HAP 计算资源分配，奖励同时编码能耗、时延与负载均衡，使 HAP 成为负载调节器而非单纯兜底算力。

## 方法快照

- 问题结构：GU-UAV 离散关联与 UAV-HAP 连续资源分配紧密耦合，且目标同时涉及时延、能耗与负载均衡。
- 两层粒度：GU 到 UAV 为二元决策，UAV 到 HAP 允许部分卸载，体现层次化控制差异。
- 求解分层：离散匹配问题先由匹配博弈稳定下来，连续动作空间交给 ESAC；避免端到端混合动作 RL 的训练不稳定。
- 验证：数值仿真（合成层次化空中计算场景，设置较完整）；实现平台、训练框架与代码开放情况未披露。

## 比赛映射要点

- 数模决策题：离散关联+连续分配的两层分解套路，可直接套到多级设施（站点-枢纽-中心）联合调度题；负载均衡进奖励的写法可复用。
- 黑客松算法题：匹配博弈+ actor-critic 的分层流水线在分配/调度类题中训练收敛与可解释性占优。
- 双创申报：农村/灾害应急场景的空地协同算力平台方案支撑。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Nabi2025_UAV与HAP协同层次化空中计算联合卸载`（venue_tier/evidence_tier/paper_role/reproducibility_level 承自该页 frontmatter）。
- bib 回填：citekey `nabi2025JointOffloadingDecision` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2025），按年-01-01 填写；验证类信息（simulation/synthetic/复现性 medium）承自 vault 页自评，如需引用请以论文原文复核。
