---
campaign:
  competition_id: kaggle-kaggriculture
  name: Kaggriculture 农场博弈 Agent 战役 II（参赛级迭代）
  theme: 720 回合供应链博弈 bot 第二轮：天梯标定与策略增强（09-30 终交）

scope:
  deliverables:
    - 复活并迭代的可提交 Kaggle bot（官方 kit 结构 /kaggle_simulations/agent/；本地自博弈 + Validation Episode 校验通过；每项相对第一轮基线的增强经评估矩阵量化后才合入）
    - 对手池强化与评估保真基建（更强启发式对手变体 × matchup 全矩阵 × 方差控制 + 评估审计清单，对症"对手池偏弱"）
    - 天梯反馈回填与迭代记录（线上对局结论录入 metrics；本地对手池按线上反馈校准）
    - LLM 辅助决策模块 A/B 实测（默认关闭、预算闸、失败回退；仅本地实测，提交形态不依赖外部模型）
    - 方案报告（typst）与提交 SOP v2（终交前"最近 2 份最优"锁定检查单）
  out_of_scope:
    - 获奖结果承诺（天梯高方差，如实呈现）
    - Kaggle 账号注册与线上提交操作（队伍人工完成，列 manual 验收）
    - 多账号等违规手段（rules 明文禁止）
    - 端到端深度 RL 训练管线（第一轮已验证启发式路线投入产出比；队内无 RL 实绩 + 8GB 显存约束——如线上反馈显示必须，留下一战役决策）
    - 硬件类交付（无 hardware 里程碑）

tech_stack:
  - name: 对手池强化与评估保真（主力迭代引擎）
    kb_tech_ids: [arxiv-2608.27456, arxiv-2608.26753]
    rationale: UrbanGround 的 runnable 沙盒评测方法论（失败模式清单驱动迭代）+ ABE-Ralph 的实验保真审计——把第一轮已知边界（对手池 Elo 1162 封顶）工程化为 matchup 矩阵/方差控制/审计清单，防自欺
    reuse_cost: 低
  - name: 动态市场出货门控升级
    kb_tech_ids: [arxiv-2608.15291]
    rationale: ReasonCast 选择性干预门控方法论迁移——"何时不卖"的价格闸门决策（glut 曲线护盘，稳定期不干预），对齐官方动态市场机制（价格随自身出货反应）
    reuse_cost: 中
  - name: LLM 辅助决策模块 A/B（默认关闭）
    kb_tech_ids: [arxiv-2608.25992, arxiv-2608.24087]
    rationale: ProgRouter 质量-成本路由 + Bayesian Self-Escalation 求助升级——第一轮已落地预算闸接口（NullProvider/OpenAICompatProvider），本轮完成真实 A/B 实测；Reasonableness Standard 机械化（订阅级费用）
    reuse_cost: 中

interface_contracts:
  - between: [software, document]
    contract_file: workspace/software/exports/schema.json

milestones:
  # ── 四阶段依赖链（D12 波次化）──
  - id: m0-skeleton        # 骨架层：资产复活 + 回归线冻结
    task: 从归档复制工程 42 文件到 workspace（archive 只读不改）、45 测试全绿、固定种子复现第一轮 Elo 排序为回归断言（run_eval 增加 --assert-regression）、metrics 键清单与报告大纲；人工项置顶发出（报名核对 man-reg）
    owner_role: software
    depends_on: []
  - id: m1-vertical        # 竖切层：对手池强化一条线打通
    task: 新增 2-3 个强启发式对手变体 + matchup 全矩阵 + 方差报告与评估审计清单（ABE-Ralph 式）；输出当前 bot 对新池的失败模式清单
    owner_role: software
    depends_on: [m0-skeleton]
  - id: m2-full            # 完整层：策略增强全量迭代 + 线上闭环启动
    task: 按失败模式清单逐项改进（市场门控升级/资本计划/劳动调度），每项过评估矩阵才合入；LLM 模块 A/B 实测落 metrics；启动线上提交节奏（man-submit）并回填天梯反馈校准对手池
    owner_role: software
    depends_on: [m1-vertical]
  - id: m3-polish          # 打磨层：终局提交管理与文档成稿
    task: 终交前提交管理（"最近 2 份最优"锁定，man-final）；报告/SOP v2 定稿（消费 merge_metrics 稳定值，数字只出自 metrics.json）
    owner_role: document
    depends_on: [m2-full]

acceptance:
  checklist:
    - {id: m0-deps, category: software, item: 依赖锁定安装通过（含 vendored 官方引擎 wheel）, method: 自动,
       cmd: "python -m pip install -q -r workspace/software/requirements.txt"}
    - {id: m0-boot, category: software, item: bot 本地自博弈冒烟（起环境、跑局、契约校验、超时看门狗）, method: 自动,
       cmd: "python workspace/software/smoke_boot.py"}
    - {id: m0-test, category: software, item: 测试套件全过（第一轮 45 项基线 + 本轮新增）, method: 自动,
       cmd: "python -m pytest workspace/software/tests -q"}
    - {id: m0-regress, category: software, item: 回归线复现（固定种子：Elo 排序 submission > baseline_wheat > greedy_carrot > starter > random > pass 且 submission 对冻结池不败）, method: 自动,
       cmd: "python workspace/software/scripts/run_eval.py --rounds 2 --assert-regression"}
    - {id: m1-matrix, category: software, item: 对手池扩充后 matchup 全矩阵与 Elo 表产出（含新对手、方差报告、审计清单）, method: 自动,
       cmd: "python workspace/software/scripts/run_eval.py --rounds 4"}
    - {id: m2-ab, category: software, item: LLM 模块 A/B 实测数据落 metrics（需 KG_LLM_* 环境变量；预算闸与回退生效证据）, method: 自动}
    - {id: doc-compile, category: document, item: 方案报告编译通过, method: 自动,
       cmd: "typst compile workspace/docs/report.typ workspace/docs/report.pdf"}
    - {id: man-reg, category: manual, item: Kaggle 报名核对与完成（entry_deadline 官方数值缺失，第 0 天人工核对赛站锁定——第一轮遗留，置顶）, method: 人工手册}
    - {id: man-submit, category: manual, item: 线上提交与天梯观察（每日 ≤5 次、最近 2 次计入；按 SOP v2 检查单；天梯结论回填 metrics）, method: 人工手册}
    - {id: man-final, category: manual, item: 终交前提交锁定检查（09-30 前确认最近 2 份提交为最优版本）, method: 人工手册}

compliance:
  ai_policy_reviewed: true
  mode: apply
  policy_basis: >-
    官方 rules（2026-08-28 经 Kaggle ListPages API 直抓）："The use of external data and models is
    acceptable unless specifically prohibited by the Host"；"a small subscription charge to use
    additional elements of a large language model such as Gemini Advanced are acceptable if meeting
    the Reasonableness Standard"；"Individual Participants and Teams may use automated machine
    learning tool(s) ('AMLT') ... provided that ... they have an appropriate license"。Winner License
    CC-BY 4.0；Competition Data Apache 2.0。
  notes: >-
    单账号纪律（rules 明文禁多账号报名/提交）；团队上限 5 人（画像 3 人合规）；每日提交 ≤5 次、仅最近
    2 次计入。agent 容器资源限额与网络政策为 FAQ 模板变量未解析——提交形态保持 stdlib-only、不依赖
    外部网络模型（LLM 模块仅本地 A/B 且默认关闭），不臆测线上能力。人机分工记录随归档保留。
---

# 正文（人读）

## 选型依据摘要

- 用户闸门指定主攻（第二场同赛战役）；第一轮归档资产实测：bot 本地 24/24 胜、Elo 1460.9、A/B 2.56×、45 测试——第二轮全部边际投入落在两个真正的夺奖变量：**线上标定**（对手池校准 + 天梯反馈回填）与**策略增强**（失败模式驱动迭代）。
- 技术三件套：评估保真（`arxiv-2608.27456` + `arxiv-2608.26753`，reuse 低——基建已在归档）为迭代引擎；市场门控升级（`arxiv-2608.15291` 选择性干预方法论）为策略主增量；LLM 模块 A/B（`arxiv-2608.25992` + `arxiv-2608.24087`）为受控增强。无 patterns（首届未放榜）——m1 失败模式清单即自建 patterns 的过程（延续第一轮判断）。

## 里程碑展开

- m0（第 1-2 天）：复活 + 回归线冻结 + 报名核对置顶（entry_deadline 缺失为唯一硬时点风险）。
- m1（第 1 周）：对手池强化竖切，暴露当前 bot 失败模式——这是后续一切增强的证据基础。
- m2（第 2-4 周）：失败模式驱动迭代，每项过评估矩阵才合入；线上提交尽早启动（man-submit），天梯反馈回填校准本地池；09-15 保留 RSNA 切换决策点（strategy 第五节）。
- m3（终交周）：提交锁定 + 报告/SOP v2 定稿，收官 09-30。

## 风险与缓解

1. entry_deadline 缺失 → man-reg 第 0 天人工核对并完成报名。
2. 线上天梯未标定 → m1 强对手池 + 首轮线上提交尽早拿反馈；09-15 决策点兜底切 RSNA（评估基建通用）。
3. 提交纪律（每日 ≤5、最近 2 次计入）→ SOP v2 检查单 + man-final 锁定检查。
4. 容器限额/网络政策未解析 → 提交形态 stdlib-only，LLM 仅本地 A/B 默认关闭。
5. 数字纪律：报告一切对局指标只出自 workspace/metrics.json 实测；线上未发生时如实 null。
