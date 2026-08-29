---
campaign:
  competition_id: kaggle-kaggriculture
  name: Kaggriculture 农场博弈 Agent 战役 III（线上反馈重构版）
  theme: 批量回放画像与线上风格对手池驱动的市场自适应引擎重构、一次性 holdout v2 与 09-30 终交前天梯爬升

scope:
  deliverables:
    - 回放语料与画像管线：官方 episodes index 解析、按需日分片/单局下载器、语料完整性校验（双方 DONE、720 步、异常局剔除留痕）、逐局结构化画像（资金曲线、畜群轨迹、作物轮替、雇佣强度、外购饲料、卖出价格门控、终局行为）、分层抽样画像档案（top-20 / top-100 / 500-900 近段），每档案携带数据集 URL 与抓取日期
    - 线上风格对手池：依据跨局复核（同选手不少于 3 局一致）后的画像参数实现 2-4 个本地对手（如作物轮作 bot、重劳动麦作 bot、混合畜群 bot、终局囤倾 bot），对冻结弱池认证强度后纳入 run_eval 对手池与完整门禁必测名单
    - 市场自适应候选引擎：作物轮作主引擎 + 小规模混合畜群 + 常态外购饲料（带价格护栏）+ 劳动扩容 + 第三象限扩张 + 终局囤积-倾销与末日停喂；保留 m2b 全部修复（末日无 capex、购买观察确认、shed 预留、正数量订单、跨座位跨局隔离）；stdlib-only 单文件自包含
    - 一次性独立 holdout v2：系统随机全新种子（与全部历史种子 27 个开发/回归 + 8 个已公布 holdout + 3 个线上实测 seed 无交集）、全池 AB/BA 双座位、候选身份冻结、异常 fail-closed、通过语义校验后原子发布，merge_metrics 汇总
    - 报告与提交 SOP v4 重生成：纳入线上 round-1 复盘与 round-2 天梯采样-回拉-复盘循环协议（每日至多 5 次、最近 2 次跟踪、每候选至多 2 次/日、Error 即停）；旧 92.9% holdout 结论明确标注为前代候选 sha 7c482921 的实测，不外推新候选
  out_of_scope:
    - 获奖、天梯名次或线上胜率承诺
    - 复用已公布 holdout 种子或在该 holdout 上继续调参
    - 端到端深度 RL 或模仿学习训练管线（列为后续战役方向，本轮仅离线画像驱动的显式策略工程）
    - Kaggle 账号操作与线上提交执行（团队人工执行，列 manual 验收）
    - 提交 bot 运行时依赖外部数据集、LLM 或网络 API（画像只用于离线设计）
    - 在旧同族对手池上单独调参并宣称策略提升

tech_stack:
  - name: 可执行实验保真审计与证据身份（扩展至回放语料）
    kb_tech_ids: [arxiv-2608.26753]
    rationale: 把语料来源（数据集 URL+抓取日期）、画像档案哈希、异常局剔除规则与候选身份链统一纳入 ABE-Ralph 式可执行审计，防止画像污染策略结论
    reuse_cost: 低
  - name: 开发/确认隔离的 runnable 沙盒与失败模式驱动迭代
    kb_tech_ids: [arxiv-2608.27456]
    rationale: 线上风格对手进入同一沙盒、完整门禁与失败模式闭环；画像产出先变失败模式清单再变修复，延续 UrbanGround 方法
    reuse_cost: 中
  - name: 动态市场选择性干预与终局回收（升级为生产结构自适应）
    kb_tech_ids: [arxiv-2608.15291]
    rationale: 选择性干预从卖出 timing 门控扩展为按价格曲线重构生产结构（轮作、畜群、饲料来源），终局回收升级为囤积-倾销与停喂决策
    reuse_cost: 中
  - name: LLM 辅助决策的逐局预算隔离（可选）
    kb_tech_ids: [arxiv-2608.25992, arxiv-2608.24087]
    rationale: KG_LLM_* 完整配置时才执行真实 A/B；未配置保持 null 并通过通路自检，不阻塞主线
    reuse_cost: 中

interface_contracts:
  - between: [software, document]
    contract_file: workspace/software/exports/schema.json

milestones:
  - id: m1-replay-corpus
    task: 建回放语料与画像管线：解析官方 episodes index，按需下载指定日分片或单局回放到 gitignored 数据目录（仅小体积画像档案入库）；语料完整性校验（双方 DONE、720 步、异常剔除留痕）；实现逐局画像提取器（资金曲线、畜群轨迹、作物轮替、雇佣强度、外购饲料、卖出价格分布、终局抛售构成）；产出分层画像档案（top-20/top-100/500-900 近段），同选手跨局一致性复核，单局结论标 exploratory；全部档案携带来源 URL 与抓取日期
    owner_role: software
    depends_on: []
  - id: m2-online-pool
    task: 依据复核后的画像参数实现 2-4 个线上风格对手 bot，经 check_opponent_strength 对冻结弱池认证（不低于 50%）后纳入 run_eval 对手池与完整门禁必测名单；更新 gate contract 必测集合与对手单测；旧池成员全部保留
    owner_role: software
    depends_on: [m1-replay-corpus]
  - id: m3-adaptive-candidate
    task: 在新完整开发门（含线上风格对手）上重构候选：作物轮作主引擎（按实时价格在麦/草莓/西瓜/胡萝卜间轮换地块）、小规模混合畜群（羊为主）、常态外购饲料（价格护栏）、劳动扩容至画像实证强度、第三象限扩张、终局囤积-倾销与末日停喂；保留 m2b 全部修复与既有测试；新增策略回归测试；开发门通过后冻结候选与 SHA-256
    owner_role: software
    depends_on: [m2-online-pool]
  - id: m4-holdout-v2
    task: 对冻结候选生成与全部历史种子无交集的系统随机 holdout 种子并只运行一次全池 AB/BA 矩阵；运行前锁定候选哈希，运行后公开种子；输出逐对 W/L/T、座位分层、Wilson 区间、顺序无关统计与完整性断言；merge_metrics 汇总；禁止复用任何已公布种子
    owner_role: software
    depends_on: [m3-adaptive-candidate]
  - id: m5-redocument
    task: 基于新 metrics 重生成报告与 SOP v4（含 round-1 线上复盘、round-2 天梯采样协议与止损线）；数字只引用 metrics 键；旧 92.9% 标注为前代候选实测并紧邻限制；不得把本地 holdout 外推为天梯实力；报告编译、键引用与 PDF 视觉验收通过
    owner_role: document
    depends_on: [m4-holdout-v2]

acceptance:
  checklist:
    - {id: m1-tests, category: software, item: 全部软件测试通过，覆盖语料校验、画像提取、异常局剔除与画像档案 schema, method: 自动,
       cmd: "python -m pytest workspace/software/tests -q && python scripts/verify/test_acceptance.py"}
    - {id: m1-corpus, category: software, item: 画像产物过完整性校验（每档案含数据集 URL 与抓取日期、异常局剔除留痕、分层抽样齐备、跨局复核标注）, method: 自动,
       cmd: "python workspace/software/scripts/corpus_integrity.py --mode official"}
    - {id: m1-smoke, category: software, item: 提交 bot 在官方引擎完成短局与 720 回合自博弈且 contract 全绿, method: 自动,
       cmd: "python workspace/software/smoke_boot.py"}
    - {id: m2-pool, category: software, item: 新线上风格对手对冻结弱池认证强度不低于 50% 且跨局画像参数一致才入库，对手单测通过, method: 自动,
       cmd: "python workspace/software/scripts/check_opponent_strength.py --rounds 3"}
    - {id: m2-gate, category: software, item: 完整门禁必测名单包含全部新对手，拒绝缺失必测对手、异常局与单座位赛程, method: 自动,
       cmd: "python workspace/software/scripts/check_eval_contract.py --mode gate"}
    - {id: m2-ab, category: software, item: LLM 真实 A/B 仅在 KG_LLM_* 完整配置时执行且逐局预算隔离；未配置时保持 null 并通过通路自检, method: 自动}
    - {id: m3-strategy, category: software, item: 轮作、外购饲料护栏、劳动扩容、象限扩张、终局囤倾与停喂的策略回归测试通过，m2b 修复项测试不回退, method: 自动,
       cmd: "python -m pytest workspace/software/tests/test_strategy_m3.py workspace/software/tests/test_strategy_m2.py workspace/software/tests/test_agent_contract.py -q"}
    - {id: m3-dev-gate, category: software, item: 冻结候选在含线上风格对手的完整开发门通过且日志含全部 gate/guard 对手、双座位、候选哈希与零异常局, method: 自动,
       cmd: "python workspace/software/scripts/iterate_gate.py --candidate workspace/software/kaggle_simulations/agent/main.py --label m3-frozen --rounds 4 --require-complete"}
    - {id: m4-holdout, category: software, item: 冻结候选的一次性独立 holdout v2 已发布且通过完整性检查；验收不得重跑或换种子, method: 自动,
       cmd: "python workspace/software/scripts/run_holdout.py --verify-published --require-frozen"}
    - {id: m4-identity, category: software, item: 正式 export 的候选哈希、git ref、种子域隔离、预期局数、AB/BA 对称性、零异常局与跨字段语义一致, method: 自动,
       cmd: "python workspace/software/scripts/check_eval_contract.py --mode official --input workspace/software/exports/eval_results.json"}
    - {id: m4-metrics, category: software, item: metrics 分片合并成功且确认性数字全部可追溯到正式 export, method: 自动,
       cmd: "python scripts/verify/merge_metrics.py"}
    - {id: doc-compile, category: document, item: 修订报告编译通过, method: 自动,
       cmd: "typst compile --root workspace workspace/docs/report.typ workspace/docs/report.pdf"}
    - {id: doc-consistency, category: document, item: 报告数字键零悬空、旧基线与旧 holdout 限制紧邻披露、无天梯或获奖外推, method: 自动,
       cmd: "python workspace/docs/check_report_metrics.py"}
    - {id: doc-visual, category: document, item: 报告 PDF 渲染后逐页视觉验收通过，无溢出、重叠、断页或不可读图表, method: agent 视觉验收}
    - {id: man-submit-r2, category: manual, item: 按 SOP v4 提交新候选并回拉不少于 3 局公共天梯回放完成 round-2 复盘（每日至多 5 次、每候选至多 2 次/日、Error 即停）, method: 人工手册}
    - {id: man-final, category: manual, item: 09-30 前锁定最近 2 份最优提交并记录 commit/hash 与 Validation Episode 状态, method: 人工手册}

compliance:
  ai_policy_reviewed: true
  mode: apply
  policy_basis: >-
    Kaggle 官方 Rules（2026-08-28 实抓）："The use of external data and models is acceptable unless
    specifically prohibited by the Host"；"a small subscription charge to use additional elements
    of a large language model such as Gemini Advanced are acceptable if meeting the Reasonableness
    Standard"；"Individual Participants and Teams may use automated machine learning tool(s)
    ('AMLT') ... provided that ... they have an appropriate license"。
  notes: >-
    单账号与团队上限纪律不变；提交 bot 保持 stdlib-only、离线自主运行，回放画像只用于离线设计不进入运行时依赖。
    竞赛数据 Apache 2.0、获奖许可 CC-BY 4.0；官方 episodes 数据集与网页 episode 下载为平台公开通道。
    所有公开性能数字只来自 workspace/metrics.json 对应的正式、完整、身份锁定 export；本地 holdout 不等于线上天梯。
---

# 正文（人读）

## 选型依据摘要

- 战役 II 已闭环：评估治理（AB/BA、fail-closed、身份冻结、原子发布）与一次性 holdout 92.9% 均为可复用资产；但线上首轮 1W-2L（rank 4550/6806，skill 549.9）证明同族对手池的分布偏移未被种子/座位隔离消除，这正是战役 II 蓝图风险第 3 条的应验。
- 线上证据链完整：两位胜者（3629/3978 名）的多物种+外购饲料+高价值作物结构（FM-O1..O4）与榜首单局解构（作物轮作引擎、牛奶崩盘即停产转产）共同指向"市场自适应生产结构"为顶部核心能力。
- 官方回放数据集（index + 每日快照）与网页 episode 下载通道实测可用，使对手分布偏移首次可工程化消除：分层画像 → 线上风格对手池 → 含新对手的完整门禁与一次性 holdout。
- 用户五项新要求（画像、对手池、候选重构、holdout v2、SOP v4）全部进入里程碑与机检。

## 里程碑展开

1. **m1** 语料与画像先行：没有跨局复核的画像不进对手池（防单局过拟合），没有来源标注的档案不进正式产物（引用纪律）。
2. **m2** 对手池：画像参数 → 2-4 个显式实现的风格 bot，认证强度后进入必测名单；旧池保留防能力回退。
3. **m3** 候选重构：只在新完整门上迭代；每项新能力（轮作/饲料/劳动/象限/终局）配回归测试；通过后冻结。
4. **m4** holdout v2：全新种子一次性运行，结果无论好坏如实入 metrics。
5. **m5** 文档：SOP v4 把"提交-回拉-复盘"固化为循环，并写入止损线。

## 风险与缓解

1. 分段偏差：画像分层抽样覆盖近段与榜首；爬升先胜近段。
2. 单局应激误读：同选手 ≥3 局一致才进对手池参数，单局结论 exploratory。
3. 数据量：原始回放仅落 gitignored 目录，画像档案小体积入库；按需下载不全量镜像。
4. holdout 纪律：候选变更即作废，必须全新种子；旧 8+27+3 全部排除。
5. 同族偏移复发风险：SOP v4 每轮线上复盘滚动更新画像；本地结论不外推天梯。
6. 提交预算：每日 5 次上限内每候选 ≤2 次/日；Validation Error 即停当日提交。
7. 止损：新候选线上 ≥6 局公共局胜率 <50% 时停止本方向调参，转 RSNA 接力。
