---
campaign:
  competition_id: kaggle-kaggriculture
  name: Kaggriculture 农场博弈 Agent 战役
  theme: 720 回合供应链博弈 bot（agentic RL 风向标赛，09-30 终交）

scope:
  deliverables:
    - 可提交的 Kaggle bot（workspace/software/kaggle_simulations/agent/：官方 Python kit 结构，本地 kit 自博弈可跑、Validation Episode 校验通过）
    - 本地评估基建（环境 gym 化封装 + 自博弈对局器 + 对手池 + Elo 式评估脚本 + 复盘日志）
    - 博弈机制量化工具（作物/动物/市场收益模型 + 机制红线检查表：浇水/喂养/产出次数约束）
    - 方案报告（typst）与提交 SOP（每日 ≤5 提交、最近 2 次计入的迭代纪律 + 终交前检查单）
  out_of_scope:
    - 获奖结果承诺（天梯高方差，如实呈现）
    - Kaggle 账号注册与线上提交操作（队伍人工完成，列入 manual 验收）
    - 多账号等违规手段（rules 明文禁止）
    - RSNA/其他赛事作品（属备选与支线，不在本战役范围）
    - 硬件类交付（无 hardware 里程碑）

tech_stack:
  - name: 启发式基线与本地评估基建（主力）
    kb_tech_ids: [arxiv-2608.27456]
    rationale: UrbanGround（runnable 沙盒）的评测方法论与 agent 失败模式清单直接迁移——本地自博弈评估器/compare_models 式量化对比，先规则基线后增强，每步迭代有据
    reuse_cost: 低
  - name: LLM 辅助决策模块（可选增强，A/B 验证）
    kb_tech_ids: [arxiv-2608.25992, arxiv-2608.24087]
    rationale: ProgRouter 质量-成本路由 + Bayesian Self-Escalation 控制 LLM 调用的回合时延与费用（符合 rules 的 Reasonableness Standard——Gemini Advanced 级订阅可接受）
    reuse_cost: 中
  - name: 策略技能库
    kb_tech_ids: [arxiv-2608.25500]
    rationale: CaSKG 式技能检索组织启发式策略库（开局/中期/终局策略分段复用），方法论级落地
    reuse_cost: 中

interface_contracts:
  - between: [software, document]
    contract_file: workspace/software/exports/schema.json

milestones:
  - id: m1
    task: 环境复刻与机制量化（收益模型、红线检查表、gym 化封装）
    owner_role: software
    depends_on: []
  - id: m2
    task: 启发式基线 bot（官方 kit 结构跑通本地自博弈与 Validation Episode 格式校验）
    owner_role: software
    depends_on: [m1]
  - id: m3
    task: 评估基建（对手池/Elo 脚本/复盘日志）与首轮线上提交（队伍协作）
    owner_role: software
    depends_on: [m2]
  - id: m4
    task: 增强迭代（搜索/学习策略 与 LLM 辅助决策 A/B，按评估器择优）
    owner_role: software
    depends_on: [m3]
  - id: m5
    task: 方案报告（typst）与提交 SOP 定稿
    owner_role: document
    depends_on: [m3]

acceptance:
  checklist:
    - {id: sw-deps, category: software, item: 依赖锁定安装通过, method: 自动,
       cmd: "python -m pip install -q -r workspace/software/requirements.txt"}
    - {id: sw-boot, category: software, item: bot 本地自博弈冒烟（起环境、跑 N 局、校验输出契约）, method: 自动,
       cmd: "python workspace/software/smoke_boot.py"}
    - {id: sw-test, category: software, item: 测试套件全过（收益模型单测 + agent 接口契约测试）, method: 自动,
       cmd: "python -m pytest workspace/software/tests -q"}
    - {id: doc-compile, category: document, item: 方案报告编译通过, method: 自动,
       cmd: "typst compile workspace/docs/report.typ workspace/docs/report.pdf"}
    - {id: man-reg, category: manual, item: Kaggle 报名完成（entry_deadline 官方数值缺失，第 0 天人工核对赛站并尽早锁定）, method: 人工手册}
    - {id: man-submit, category: manual, item: 线上提交与天梯观察（每日 ≤5 次、最近 2 次计入；按 SOP 检查单执行）, method: 人工手册}

compliance:
  ai_policy_reviewed: true
  mode: apply
  policy_basis: >-
    官方 rules（2026-08-28 经 Kaggle ListPages API 直抓）："The use of external data and models is
    acceptable unless specifically prohibited by the Host"；LLM 费用按 Reasonableness Standard 放行
    （"a small subscription charge to use additional elements of a large language model such as
    Gemini Advanced are acceptable"）；"Individual Participants and Teams may use automated machine
    learning tool(s) ('AMLT') ... provided that ... they have an appropriate license"。Winner License
    CC-BY 4.0；Competition Data Apache 2.0。
  notes: >-
    单账号纪律（rules 明文禁多账号报名/提交）；团队上限 5 人（画像 3 人合规）。每日提交 ≤5 次、仅最近 2 次
    计入评估——SOP 检查单防终交前误操作。agent 运行环境资源限额为 FAQ 模板变量未解析：bot 内存/时长占用
    预留裕量。

---

# 正文（人读）

## 选型依据摘要

- 用户闸门指定主攻（2026-08-28，CUMCM 因学校报名门槛后置）；时间窗 33 天最优区，收官（09-30）后 RSNA（10-22 终交）可无缝接力。
- 技术路线三段式：启发式基线先行（规则可解释、迭代快）→ 评估基建量化（Elo 对手池，UrbanGround `arxiv-2608.27456` 评测方法论迁移）→ 增强模块 A/B（搜索/学习策略 与 LLM 辅助决策，ProgRouter `arxiv-2608.25992` 控成本）。无 patterns（首届未放榜）——机制量化工具（m1）即是自建 patterns 的过程。

## 里程碑展开

m1-m2 为最小可提交闭环（第 1 周）；m3 评估基建上线即启动首轮线上提交拿天梯反馈（第 2 周）；m4 按评估器数据迭代至终交（第 3-4 周，09-30 收官）；m5 报告与 SOP 与 m3 并行启动、终交前定稿。RSNA 备选切换决策点：09-15 前 若评估器显示投入产出比不佳，切 RSNA 且评估基建通用。

## 风险与缓解

1. entry_deadline 官方数值缺失 → man-reg 第 0 天人工核对并完成报名（唯一硬时点风险）。
2. RL/博弈新领域 → 基线先行 + 全程量化评估，每步有据；09-15 切换决策点兜底。
3. 天梯高方差（Elo + Bradley-Terry）→ 对手池多轮评估降方差，不追单局结论。
4. 数字纪律：报告中一切对局指标只能来自 workspace/metrics.json 实测。
