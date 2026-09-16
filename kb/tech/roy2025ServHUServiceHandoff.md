---
id: roy2025ServHUServiceHandoff
name: Serv-HU：UaaS 平台服务接力与最优定价机制
field: [无人机服务计算, 平台机制, 收益定价]
published: 2025-01-01
maturity: paper
directions: [创新创业大赛, 数模与时序预测]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Services Computing
  runnable: false
competition_fit:
  - track: 双创-文书与申报
    edge: UaaS 平台"单一用户入口 + 多提供者接力 + 统一计价"机制为智慧农业无人机服务平台的商业模式与收益分成设计提供机制级支撑（服务连续性论证）
    reuse_cost: 低
  - track: 数模-数据分析与决策
    edge: 两阶段建模（SSP 递归选择 + Lagrangian/KKT 最优定价）是"覆盖不足下的服务分派与定价"类优化赛题的可移植范式；仿真显示最优 SSP 选择较随机接力降低终端收费约 10.3%-12.7%
    reuse_cost: 中
sources:
  - paper_title: Serv-HU：Service Hand-off for UAV-as-a-service
    doi: 10.1109/TSC.2024.3521684
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# Serv-HU：UaaS 平台服务接力与最优定价机制

## 单行摘要

为 UaaS 平台提出 Serv-HU 服务接力机制：主服务提供者（PSP）无法独立覆盖用户请求的完整任务区域时，分两阶段完成次级提供者（SSP）最优选择与终端最优定价，使用户无需分别签约多个服务商即可获得连续服务交付。

## 方法快照

- 两阶段分解：阶段一为 SSP 选择——按服务评价、可服务区域、单位面积收费与资源能力，递归选出补足未覆盖子区域的次级提供者集合；阶段二为最优定价——在既定接力关系下用 Lagrangian + KKT 求 PSP 的最优收费区间与最优价格。
- 经济模型：平台同时核算 cash outflow / inflow / service payoff，兼顾 PSP 转包支出与终端支付上界/下界；结论为最优 SSP 选择较随机接力使最终收费降低约 10.3%-12.7%。
- 系统角色：终端用户只与 PSP 交互；服务区域划分子区域；UAV 所有者作为资源方。PSP/SSP 协同部署 UAV 完成整片区域服务。
- 通信侧延伸：讨论多 SSP 协同场景下的多跳通信成本，说明 hand-off 不只是业务逻辑切换，也影响底层通信组织。

## 比赛映射要点

- 双创申报：农业植保/巡检类无人机服务平台常被质疑"单服务商覆盖不了大田区怎么办"——Serv-HU 给出可引用的机制答案（平台内部接力+收益结算，用户体验单入口），是商业模式画布中"合作伙伴与收入流"的差异化设计点。
- 数模优化：服务分派+定价双阶段建模可整体迁移到"设施覆盖不足下的转包/协同调度"类赛题；KKT 定价推导是可复用的解析组件。
- 方法对照价值：与纯任务卸载/轨迹优化论文形成对照，把"服务连续性"写成平台机制问题，适合数模论文的创新点表述。

## 关联概念
- 服务接力（Service Hand-off）

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Roy2025_Serv-HU面向UaaS的服务接力机制`（frontmatter 带 venue_tier/evidence_tier/paper_role/reproducibility_level，已映射到本卡 4 枚举字段）。
- bib 回填：citekey `roy2025ServHUServiceHandoff` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- 留痕：bib 标题原为 ASCII 冒号「Serv-HU: Service Hand-off for UAV-as-a-service」，按分片规则改全角冒号写入 paper_title。
- `published` 仅年份已知（2025），按 2025-01-01 填写；验证类信息（simulation/synthetic/复现性 medium、开源未说明）承自 vault 页自评，如需引用请以论文原文复核。
