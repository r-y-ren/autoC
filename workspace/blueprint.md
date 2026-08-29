---
campaign:
  competition_id: kaggle-kaggriculture
  name: Kaggriculture 农场博弈 Agent 战役 II（审计修订版）
  theme: 720 回合供应链 bot 的评估可信度重建、策略修复与 09-30 终交

scope:
  deliverables:
    - 可提交的 stdlib-only Kaggle bot（/kaggle_simulations/agent/），修复末日资本支出、末日现收产物处置、失败购买状态预记、重复库存承诺和零数量订单
    - 评估保真 v2：每个配对与种子强制 AB/BA 双座位，开发种子与独立 holdout 隔离，异常局 fail-closed，完整门禁不可被自定义子集绕过
    - 可审计正式证据链：候选文件哈希与 git ref、预期赛程语义校验、quick/dev/失败产物隔离、通过后临时文件原子替换正式 export
    - 冻结候选的一次性独立 holdout 全矩阵与确认性统计（逐对 W/L/T、座位分层、Wilson 区间、顺序无关汇总；顺序敏感 Elo 仅作附录）
    - 合并后的 workspace/metrics.json、重生成的 Typst 报告与提交 SOP v3；旧 1500.8/36-0 明确标为固定 p0 开发集基线
  out_of_scope:
    - 获奖、天梯名次或线上胜率承诺
    - Kaggle 账号操作与线上提交（团队人工执行，列 manual 验收）
    - 继续使用 101-104、201-208 作为确认性 holdout
    - 在 holdout 结果揭晓后继续调同一候选并复用该 holdout
    - 线上提交形态依赖外部 LLM 或网络 API
    - 端到端深度 RL 训练管线与硬件交付

tech_stack:
  - name: 可执行实验保真审计与证据身份
    kb_tech_ids: [arxiv-2608.26753]
    rationale: 将 ABE-Ralph 的实验保真审计机械化为候选哈希、完整赛程、异常 fail-closed、跨字段语义一致性和原子发布门
    reuse_cost: 低
  - name: 开发集与确认集隔离的 runnable 沙盒
    kb_tech_ids: [arxiv-2608.27456]
    rationale: 延续 UrbanGround 的 runnable 沙盒和失败模式清单，但将开发种子、回归种子与一次性 holdout 严格分层，防止调参泄漏
    reuse_cost: 中
  - name: 动态市场选择性干预与终局回收
    kb_tech_ids: [arxiv-2608.15291]
    rationale: 保留选择性市场门控，并把末日零回收期、库存压力与无效资本支出改成可测试策略约束
    reuse_cost: 中
  - name: LLM 辅助决策的逐局预算隔离
    kb_tech_ids: [arxiv-2608.25992, arxiv-2608.24087]
    rationale: 若提供 KG_LLM_*，每局重建 provider/budget 并记录有效调用；未配置或零有效调用不产生真实 A/B 结论
    reuse_cost: 中

interface_contracts:
  - between: [software, document]
    contract_file: workspace/software/exports/schema.json

milestones:
  - id: m2a-eval-hardening
    task: 修复评估器和门禁：AB/BA 双座位；开发/回归/holdout 种子域隔离；非 DONE/INVALID/超时/contract 失败整批 fail-closed；正式门强制完整 gate+guard 对手和预期局数，自定义子集仅 exploratory；quick/dev/失败输出隔离；正式 export 经 schema+语义校验后原子替换；记录候选 SHA-256、git ref、dirty 状态和输入哈希；修复 t 区间与 acceptance 夹具 run-N 误读；补对应测试
    owner_role: software
    depends_on: []
  - id: m2b-strategy-repair
    task: 仅使用开发种子修复 bot：第 29 天禁止无回收期 BUY_LAND/HIRE/BUY_ANIMAL，保证末日现收产物可在终局前变现或不做无效收获；购买状态只按下一观察的实际资产变化确认；任务构建预扣 shed 库存；所有数量订单严格正数；逐项通过完整开发门后冻结候选文件与 SHA-256
    owner_role: software
    depends_on: [m2a-eval-hardening]
  - id: m2c-holdout-confirm
    task: 对冻结候选生成此前未使用的系统随机 holdout 种子清单并只运行一次全池 AB/BA 矩阵；运行前锁定候选哈希，运行后公开种子；任何代码变化使结果失效并要求新 holdout；输出座位分层与合并 W/L/T、Wilson 区间、顺序无关 Bradley-Terry/配对统计、完整性与异常局断言；merge_metrics 汇总稳定值
    owner_role: software
    depends_on: [m2b-strategy-repair]
  - id: m3-redocument
    task: 基于新 workspace/metrics.json 重生成报告与 SOP v3；数字只引用 metrics 键；旧 1500.8/36-0 只作为固定 p0 开发集历史基线并紧邻限制；不得把本地 holdout 外推为天梯实力；报告编译、键引用和 PDF 视觉验收通过
    owner_role: document
    depends_on: [m2c-holdout-confirm]

acceptance:
  checklist:
    - {id: m2a-test, category: software, item: 全部软件测试通过，覆盖双座位、holdout 隔离、异常 fail-closed、门禁完整性、原子写入、统计边界和验收夹具, method: 自动,
       cmd: "python -m pytest workspace/software/tests -q && python scripts/verify/test_acceptance.py"}
    - {id: m2a-smoke, category: software, item: 提交 bot 在官方引擎完成短局和 720 回合自博弈且 contract 全绿, method: 自动,
       cmd: "python workspace/software/smoke_boot.py"}
    - {id: m2a-gate-contract, category: software, item: 正式迭代门拒绝缺失必测对手、异常局和单座位赛程；exploratory 子集不得返回 PASS, method: 自动,
       cmd: "python workspace/software/scripts/check_eval_contract.py --mode gate"}
    - {id: m2a-export-safety, category: software, item: quick/dev/失败运行不覆盖正式 export，正式发布仅在 schema 与语义校验后原子替换, method: 自动,
       cmd: "python workspace/software/scripts/check_eval_contract.py --mode export"}
    - {id: m2b-strategy, category: software, item: 末日零资本支出与可变现、购买确认、库存预留、正数量订单策略回归测试通过, method: 自动,
       cmd: "python -m pytest workspace/software/tests/test_strategy_m2.py workspace/software/tests/test_agent_contract.py -q"}
    - {id: m2b-dev-gate, category: software, item: 冻结候选在完整开发门上通过且日志含全部 gate/guard 对手、双座位、候选哈希与零异常局, method: 自动,
       cmd: "python workspace/software/scripts/iterate_gate.py --candidate workspace/software/kaggle_simulations/agent/main.py --label m2b-frozen --rounds 4 --require-complete"}
    - {id: m2c-holdout, category: software, item: 冻结候选的一次性独立 holdout 全池 AB/BA 矩阵已经发布且通过完整性检查；验收不得重跑或换种子, method: 自动,
       cmd: "python workspace/software/scripts/run_holdout.py --verify-published --require-frozen"}
    - {id: m2c-identity, category: software, item: 正式 export 的候选哈希、git ref、种子域、预期局数、AB/BA 对称性、零异常局与跨字段语义一致, method: 自动,
       cmd: "python workspace/software/scripts/check_eval_contract.py --mode official --input workspace/software/exports/eval_results.json"}
    - {id: m2c-metrics, category: software, item: metrics 分片合并成功且确认性数字全部可追溯到正式 export, method: 自动,
       cmd: "python scripts/verify/merge_metrics.py"}
    - {id: m2-ab, category: software, item: LLM 真实 A/B 仅在 KG_LLM_* 完整配置时执行且逐局预算隔离；未配置时保持 null 并通过通路自检, method: 自动}
    - {id: doc-compile, category: document, item: 修订报告编译通过, method: 自动,
       cmd: "typst compile --root workspace workspace/docs/report.typ workspace/docs/report.pdf"}
    - {id: doc-consistency, category: document, item: 报告数字键零悬空、旧开发基线限制紧邻披露、无天梯或获奖外推, method: 自动,
       cmd: "python workspace/docs/check_report_metrics.py"}
    - {id: doc-visual, category: document, item: 报告 PDF 渲染后逐页视觉验收通过，无溢出、重叠、断页或不可读图表, method: agent 视觉验收}
    - {id: man-reg, category: manual, item: Kaggle 报名状态已由 userHasEntered=True 证据闭环，终验人工复核账号仍在队, method: 人工手册}
    - {id: man-submit, category: manual, item: 按 SOP v3 线上提交并回填天梯反馈，遵守每日最多 5 次且最近 2 次规则, method: 人工手册}
    - {id: man-final, category: manual, item: 09-30 前锁定最近 2 份最优提交并记录 commit/hash 与 Validation Episode 状态, method: 人工手册}

compliance:
  ai_policy_reviewed: true
  mode: apply
  policy_basis: >-
    Kaggle 官方 Rules（2026-08-28 实抓）："The use of external data and models is acceptable unless specifically prohibited by the Host"；"a small subscription charge to use additional elements of a large language model such as Gemini Advanced are acceptable if meeting the Reasonableness Standard"；"Individual Participants and Teams may use automated machine learning tool(s) ('AMLT') ... provided that ... they have an appropriate license"。
  notes: >-
    单账号与团队上限纪律不变；提交 bot 保持 stdlib-only、离线自主运行，外部 LLM 只用于本地可选 A/B 且默认关闭。竞赛数据 Apache 2.0，Winner License CC-BY 4.0。所有公开性能数字只来自 workspace/metrics.json 对应的正式、完整、身份锁定 export；本地 holdout 不等于线上天梯。
---

# 正文（人读）

## 选型依据摘要

- 本次不是重做 m0/m1，而是对审计推翻的 m2/m3 证据链重开。旧 bot 可运行、101 项测试与强对手池仍是资产；旧 `1500.8 / 36-0` 因固定 p0、开发种子复用和顺序敏感 Elo，仅保留为历史开发基线。
- 评估治理优先于继续调策略：没有完整门、异常 fail-closed、候选身份和独立 holdout，任何新增胜率都不可作为交付结论。
- 用户要求的五项硬约束全部进入机检：AB/BA、独立 holdout、异常 fail-closed、正式产物原子写入、完整门禁。

## 里程碑展开

1. **m2a** 先修测量工具与验收框架，建立不可绕过的正确性基础。
2. **m2b** 只在开发种子上修已证实的策略 bug，完整开发门通过后冻结候选哈希。
3. **m2c** 对冻结候选生成新 holdout 并只运行一次 AB/BA 全矩阵；结果无论好坏都如实进入 metrics，不在同一 holdout 上继续调参。
4. **m3** 只消费合并后的新 metrics，重写报告和 SOP；旧结论降格并披露边界。

## 风险与缓解

1. holdout 揭晓后表现下降：接受结果，不复用该 holdout调参；若继续迭代，必须冻结新候选并生成全新 holdout。
2. AB/BA 使局数翻倍：开发门保持 4 seeds，确认性 holdout 8 seeds；以可审计性优先，不用单座位换速度。
3. 对手池仍为同族启发式：holdout 只控制种子/座位，不消除对手分布偏差；线上反馈仍是最终校准来源。
4. LLM key 缺失：不阻塞 bot 与评估主线；相关指标保持 null，禁止把 NullProvider 通路自检写成真实 A/B。
5. 数字纪律：任何失败、quick、exploratory 产物不得进入正式 metrics；报告只引用通过身份和语义校验的正式 export。
