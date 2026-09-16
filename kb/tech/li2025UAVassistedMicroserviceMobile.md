---
id: li2025UAVassistedMicroserviceMobile
name: 灾后医疗救援UAV微服务MEC架构（Transformer资源管理）
field: [UAV 辅助 MEC, 微服务架构, 智能资源调度]
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
  - track: 数模-数据分析与决策
    edge: 卸载比例/能耗/时延/持续服务时间联合优化的完整建模（本地-全卸载-混合卸载三类时延能耗表达式 + Lyapunov 稳定性 + Transformer 决策），适配数模资源配置与系统可持续运行类题
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 灾后应急/social-good 类赛题的系统架构参考——临时覆盖 + 边缘算力 + 前后方三层协同 + 生命周期治理闭环的整套设计语言
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 应急救援/农业灾害监测空地协同系统的架构级叙事支撑点（微服务治理 + 双数字签名身份认证 + 备用 UAV/电源保障体系）
    reuse_cost: 低
sources:
  - paper_title: "UAV-assisted Microservice Mobile Edge Computing Architecture: Addressing Post-Disaster Emergency Medical Rescue"
    doi: 10.1109/TC.2025.3566913
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 灾后医疗救援UAV微服务MEC架构（Transformer资源管理）

## 单行摘要

面向地面基础设施受损的灾后医疗救援，提出 UAV-assisted microservice MEC 架构：前线 UAV-MEC 队列提供临时通信与算力，后方移动基站卡车/临时医疗中心承接重推理，移动电源车与备用 UAV 保障长时运行；用四个覆盖 UAV 注册-入网-运行-退出全生命周期的微服务做治理闭环，并以 Transformer 驱动的资源管理（TCAG 生成卸载决策 + DROA 动态资源优化 + GOS 在线更新模型）最大化系统持续服务时间。

## 方法快照

- 三层架构：前线 UAV 搜救服务层、后方移动基站/边缘分析层、保障车队支撑层。
- 计算模型：显式给出本地执行、全卸载、混合卸载三种时延/能耗表达式；任务可按比例卸载至某一 UAV-MEC。
- 能耗模型：通信与计算之外显式纳入悬停、垂直起降、水平飞行、返航补能各阶段。
- 资源管理 TBRM：Transformer 生成卸载与信道分配决策（TCAG），DROA 做通信/计算资源动态优化，GOS 周期性更新模型参数；以持续服务时间最大化为统一目标（含 Lyapunov 优化思想）。
- 安全治理：四类微服务 + 双数字签名证书身份认证，支撑灾后 UAV 动态加入/退出下的高可用与故障隔离。
- 验证：大规模长时仿真（合成灾后任务流），未说明平台栈、未开源。

## 比赛映射要点

- 数模：资源配置类题可复用「多模式执行时延能耗表达式 + 系统持续运行时间目标 + 在线决策更新」的完整建模链；优化目标从单次任务效率换成系统寿命是差异化角度。
- 黑客松：应急/社会价值类赛题的架构设计参考，微服务生命周期治理是超出普通「无人机 + 网络」方案的系统化亮点。
- 双创申报：空地协同应急/农业监测系统的顶层设计叙事 + 安全治理细节，评审材料可直接借用其三层架构图逻辑。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Li2025_灾后医疗救援的UAV辅助微服务MEC架构`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `li2025UAVassistedMicroserviceMobile` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写。
- 复现性承自 vault 页自评（medium，大规模仿真但平台栈与代码未披露）；signal.runnable 如实标 false。
