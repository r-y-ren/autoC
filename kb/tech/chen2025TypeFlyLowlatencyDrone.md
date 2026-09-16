---
id: chen2025TypeFlyLowlatencyDrone
name: TypeFly：低时延大模型无人机规划
field: [大语言模型, 无人机规划, 具身智能系统]
published: 2025-01-01
maturity: paper
directions: [创新创业大赛, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: high
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 黑客松-数据与算法
    edge: LLM agent 时延优化的三板斧（轻量 DSL MiniSpec 压缩 token + 流式解释边生成边执行 + probe 短查询代替重规划），可直接用于黑客松 LLM/机器人 agent 的首响应延迟优化，vault 页注明代码已公开
    reuse_cost: 低
  - track: 双创-文书与申报
    edge: 自然语言操控无人机执行植保/巡检任务的演示亮点与低空经济叙事支撑（真实 Tello 原型验证）
    reuse_cost: 低
sources:
  - paper_title: "TypeFly: Low-latency Drone Planning with Large Language Models"
    doi: 10.1109/TMC.2025.3561282
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# TypeFly：低时延大模型无人机规划

## 单行摘要

针对 LLM 逐 token 生成计划导致的响应过慢问题，TypeFly 把 LLM 定位为 plan generator 而非完整控制器，设计面向 token 效率与流式解释的轻量规划语言 MiniSpec（相比 Python/PDDL 更短），配套 runtime 在计划尚未生成完时就识别并执行可执行片段，对依赖运行时场景信息的分支用 probe 机制向 LLM 发起极短回复查询——显著降低首个动作启动延迟，并在技能失败或环境变化时触发 replan。

## 方法快照

- 延迟洞察：规划延迟与输出 token 长度高度相关；等整段计划生成完再执行是首响应慢的根因。
- MiniSpec 语言：为无人机任务定制的轻量 DSL，压缩语法减少计划长度。
- 流式执行：plan 生成与执行重叠（stream interpreting），先到先执行。
- probe 机制：运行时分支不让 LLM 重新完整规划，只回答一个极短问题，省 token。
- 技能分层：少量高频高层技能降低 LLM 编程负担，同时避免技能库过大推高 prompt 成本。
- 输入融合：用户自然语言任务 + 视觉编码器（YOLOv8）场景描述经 Prompt Generator 合成规划提示。
- 验证：真实室内飞行原型（Ryze Tello + RTX 4090），vault 页注明代码/资产已公开（artifact_availability: open）。

## 比赛映射要点

- 黑客松/数据与算法：LLM agent 赛题普遍被首 token/首动作延迟拖累，本篇的 DSL 压缩 + 流式执行 + 选择性追问组合是可落地的工程模板（有公开代码，改造成本低）。
- 双创申报：低空经济 + 大模型的展示型亮点——自然语言指挥无人机完成巡检/植保任务的真实原型，申报书与路演演示双适配。

## 关联概念
- 大语言模型驱动无人机规划

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Chen2025_TypeFly低时延大模型无人机规划`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `chen2025TypeFlyLowlatencyDrone` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写。
- 复现性承自 vault 页自评（high，真实原型 + 自评代码已公开），但本次跑批未实测该开源仓库可用性，signal.runnable 按跑批口径如实标 false，引用前请复核仓库。
