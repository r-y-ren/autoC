// Kaggriculture 战役 II 方案报告（Typst）——大纲包（波次 1/4，m0 阶段产出）
// 结构参照：归档第一轮 report 六节 + 附录；成稿于 m3（终交周）。
// 铁律：本报告一切性能数字只引 workspace/metrics.json 的 `metrics.software.<键>`（表注标键名）；
//       本版全部数字位为占位引用，终波消费 merge_metrics 稳定值回填，严禁提前写死数值；
//       赛事事实引 kb/competitions/kaggle-kaggriculture/meta.md（官方直抓，2026-08-28，URL 见附录 B）；
//       软件-文档接口契约：workspace/software/exports/schema.json（自第一轮归档原样复活）。
#set page(paper: "a4", margin: 2.2cm)
#set text(lang: "zh", region: "cn", size: 11pt, font: ("Libertinus Serif", "Microsoft YaHei"))
#set heading(numbering: "1.1")
#set par(justify: true, leading: 0.85em)
#show heading.where(level: 1): it => { v(0.6em); it; v(0.3em) }

#let ph = text(fill: gray)[待回填]

// ───────────────────────── 封面 ─────────────────────────
#align(center)[
  #v(1.2em)
  #text(size: 20pt, weight: "bold")[Kaggriculture 农场博弈 Agent 战役 II 方案报告]
  #v(0.5em)
  #text(size: 12pt)[Kaggle Simulation Competition「Kaggriculture」（Google 自办）· apply 模式 · 参赛级迭代至 09-30 终交]
  #v(0.3em)
  #text(size: 11pt)[队伍单账号提交（3 人，团队上限 5 人内） · 2026-08-28]
  #v(0.3em)
  #text(size: 10pt, fill: gray)[大纲包（波次 1/4）：结构冻结、数字占位——成稿于 m3，一切性能数字以 workspace/metrics.json 终值为准]
]
#v(0.8em)

= 摘要

本报告是 Kaggle Simulation Competition「Kaggriculture」*第二轮战役*（终交 2026-09-30）的方案报告。第二轮使命从第一轮的「框架闭环验证」升级为「参赛级迭代」：工程底座（可提交 bot + 本地评估基建）自归档原样复活并冻结回归线（m0），边际投入全部落在两个夺奖变量——*线上标定*（m1 对手池强化 + man-submit 天梯反馈回填）与*策略增强*（m2 失败模式驱动迭代，每项过评估矩阵才合入），m3 完成终交锁定与文档成稿。

本版为波次 1/4 产出的大纲包：六节结构冻结、metrics 数字位全部以 `metrics.software.<键>` 占位（键清单见 `workspace/docs/metrics-keys.md`），终波消费 `workspace/metrics.json` 稳定值回填；线上未发生的指标将如实呈现为 null。合规模式 apply（官方 rules 2026-08-28 直抓，逐条映射见 §5）；人机分工：AI 全部实现与本地验证，人工报名（man-reg）/线上提交与天梯观察（man-submit）/终交锁定与裁量（man-final），留痕见附录 A。

= 战役定位与范围

== 第二轮 vs 第一轮：从闭环验证到参赛级迭代

第一轮（已归档）完成了从零到可提交 bot 的闭环验证：本地对全对手池不败、Elo 居首（均为本地池内结论，数值见归档 `elo_ratings`），但 Kaggle 报名与线上提交均未发生，对手池偏弱且天梯真实分布未标定。第二轮把同一工程底座复活为迭代平台，边际投入全部转向夺奖变量：

#table(
  columns: (1.1fr, 2.3fr, 2.6fr),
  align: horizon,
  table.header([*维度*], [*第一轮（已归档）*], [*第二轮（本战役）*]),
  [使命], [框架闭环验证：从零到可提交 bot + 评估基建], [参赛级迭代至 09-30 终交：线上标定 + 策略增强],
  [评估口径], [固定对手池、单轮全量评估], [m1 起 matchup 全矩阵 + 方差控制 + 评估审计清单（ABE-Ralph 式）],
  [线上参与], [未报名、未提交（人工项遗留）], [man-reg 第 0 天锁定报名；man-submit 尽早启动并按天梯反馈校准对手池],
  [增强验证], [增强模块接口落地、A/B 未跑], [LLM 模块真实 A/B 实测落 metrics（m2-ab）；策略增强逐项过评估矩阵才合入],
  [工程底座], [42 文件 + 测试基线（蓝图 m0-test 口径）], [原样复活 + 固定种子回归线冻结（m0-regress 为合入门禁）],
)
#text(size: 9pt, fill: gray)[表注：本表只作定位对照、不含性能数值——第一轮实测数值以归档 metrics.json 为准，第二轮数值待本战役 metrics 回填（§4）。]

== 交付物与范围边界

交付物（蓝图 scope.deliverables）：① 复活并迭代的可提交 Kaggle bot（官方 kit 结构，本地自博弈 + Validation Episode 校验通过，每项相对第一轮基线的增强经评估矩阵量化后才合入）；② 对手池强化与评估保真基建（更强启发式对手变体 × matchup 全矩阵 × 方差控制 + 评估审计清单，对症「对手池偏弱」）；③ 天梯反馈回填与迭代记录（线上对局结论录入 metrics，本地对手池按线上反馈校准）；④ LLM 辅助决策模块 A/B 实测（默认关闭、预算闸、失败回退；仅本地实测，提交形态不依赖外部模型）；⑤ 本报告与提交 SOP v2（终交前「最近 2 份最优」锁定检查单）。

范围外（如实声明）：获奖结果承诺（天梯高方差，如实呈现）；Kaggle 账号注册与线上提交操作（队伍人工完成）；多账号等违规手段（rules 明文禁止）；端到端深度 RL 训练管线（第一轮已验证启发式路线投入产出比，队内无 RL 实绩 + 显存约束——如线上反馈显示必须，留下一战役决策）；硬件类交付。

== 遗留人工项（置顶）

- *man-reg*：Kaggle 报名核对与完成——entry_deadline 官方数值缺失（API Timeline 模板变量未解析），第 0 天人工核对赛站锁定（第一轮遗留，唯一硬时点风险）。
- *man-submit*：线上提交与天梯观察（每日 ≤5 次、最近 2 次计入；按 SOP v2 检查单执行，天梯结论回填 metrics）。
- *man-final*：终交前提交锁定检查（09-30 前确认最近 2 份提交为最优版本）。

= 方法与选型

== 技术三件套（每项一句差异化逻辑）

#table(
  columns: (1.5fr, 1.7fr, 3.0fr, 0.8fr),
  align: horizon,
  table.header([*选型*], [*kb 技术卡*], [*一句差异化逻辑*], [*复用成本*]),
  [评估保真（主力迭代引擎）], [`arxiv-2608.27456` + `arxiv-2608.26753`], [UrbanGround 的 runnable 沙盒评测与失败模式清单 + ABE-Ralph 的实验保真审计——把第一轮「对手池偏弱」的自欺风险工程化为 matchup 矩阵 / 方差控制 / 审计清单，一切增强必须过矩阵才合入], [低（基建已在归档）],
  [动态市场出货门控升级], [`arxiv-2608.15291`], [ReasonCast 选择性干预门控迁移为「何时不卖」的价格闸——glut 曲线护盘、稳定期不干预，对齐官方动态市场机制（价格随自身出货反应）], [中],
  [LLM 辅助决策模块 A/B（默认关闭）], [`arxiv-2608.25992` + `arxiv-2608.24087`], [ProgRouter 质量-成本路由 + Bayesian Self-Escalation 求助升级——第一轮已落地预算闸接口，本轮完成真实 A/B 实测并将 Reasonableness Standard 机械化（订阅级费用）], [中],
)
#text(size: 9pt, fill: gray)[表注：本赛首届未放榜、patterns 方法论分布无数据——m1 失败模式清单即自建 patterns 的过程（延续第一轮判断，如实降权声明）。]

== 软件-文档接口契约

评估产出按 `workspace/software/exports/schema.json`（draft 2020-12，自第一轮归档原样复活）落盘：逐局 `games`（p0 / p1 / seed / rewards / winner / turns / elapsed_seconds）、`head_to_head` 逐对战绩、`elo` 表（k / start / rating / record）、`runtime_seconds`——文档侧 metrics 键与该契约逐一对齐（清单见 `workspace/docs/metrics-keys.md`）。m1 / m2 新增口径（方差报告、审计清单、LLM A/B、天梯回填）需契约扩展时由 software 侧 bump schema_version 并同步文档侧，文档不得引用未落盘的键值。

= 四阶段波次执行记录

== m0：资产复活与回归线冻结（第 1-2 天）

目标：从归档复制工程 42 文件到 workspace（archive 只读不改）、依赖锁定安装（含 vendored 官方引擎 wheel）；测试全绿（第一轮基线 + 本轮新增）；固定种子复现第一轮 Elo 排序为回归断言（`run_eval.py --assert-regression`：submission > baseline_wheat > greedy_carrot > starter > random > pass，且 submission 对冻结池不败）；metrics 键清单与报告大纲（本文件）；人工项置顶发出（man-reg）。验收项：m0-deps / m0-boot / m0-test / m0-regress。

#text(fill: gray)[（占位：m0 执行记录——软件侧产物清单、验收结果、回归线断言证据，待 m0 收口回填。）]

== m1：对手池强化竖切（第 1 周）

目标：新增 2-3 个强启发式对手变体 + matchup 全矩阵 + 方差报告与评估审计清单（ABE-Ralph 式）；输出当前 bot 对新池的失败模式清单——后续一切策略增强的证据基础。验收项：m1-matrix。

#text(fill: gray)[（占位：m1 执行记录——新对手变体清单、矩阵与方差报告、失败模式清单条目，待 m1 收口回填。）]

== m2：失败模式驱动迭代 + 线上闭环（第 2-4 周）

目标：按失败模式清单逐项改进（市场门控升级 / 资本计划 / 劳动调度），每项过评估矩阵才合入；LLM 模块 A/B 实测落 metrics（m2-ab，含预算闸与回退生效证据）；启动线上提交节奏（man-submit）并回填天梯反馈校准本地对手池；09-15 保留 RSNA 切换决策点（strategy 第五节兜底路径）。

#text(fill: gray)[（占位：m2 执行记录——迭代台账（假设 → 矩阵证据 → 合入结论）、LLM A/B 数据、天梯回填时间线，待 m2 收口回填。）]

== m3：终交锁定（终交周）

目标：终交前提交管理（「最近 2 份最优」锁定，man-final）；报告与 SOP v2 定稿（消费 merge_metrics 稳定值，数字只出自 metrics.json）。验收项：doc-compile / man-final。

#text(fill: gray)[（占位：m3 收口记录——锁定版本台账、终版 metrics 快照、人机分工记录核实，待终交周回填。）]

= 实测结果

本节全部数字位为占位引用（铁律 4：对局指标只出自 `workspace/metrics.json` 实测值，表注标键名）。键清单与用途见 `workspace/docs/metrics-keys.md`；标注「建议键」者为 m1 / m2 契约扩展项，落盘前不得在正文引用其数值。

== m0：回归线（复活复现）

#table(
  columns: (2.6fr, 1.0fr, 2.6fr),
  align: (x, y) => (if x == 0 { left } else { center }) + horizon,
  table.header([*指标*], [*数值*], [*metrics 键*]),
  [测试套件通过 / 总数], [#ph], [`tests_passed` / `tests_total`],
  [冒烟自检], [#ph], [`smoke_boot_pass`],
  [回归断言（Elo 排序复现 + 冻结池不败）], [#ph], [`m0_regression_pass`（建议键）；排序证据 `elo_ratings`],
  [全量评估对局数 / 总耗时 / 单局均值], [#ph], [`eval_games_total` / `eval_runtime_seconds` / `avg_episode_runtime_seconds`],
)

== m1：对手池与 matchup 矩阵

#table(
  columns: (2.6fr, 1.0fr, 2.6fr),
  align: (x, y) => (if x == 0 { left } else { center }) + horizon,
  table.header([*指标*], [*数值*], [*metrics 键*]),
  [Elo 表（含新对手）], [#ph], [`elo_ratings`],
  [matchup 全矩阵逐对胜率], [#ph], [`matchup_win_rates`（建议键，schema head_to_head 派生）],
  [胜率 / 评级方差报告], [#ph], [`eval_variance_report`（建议键）],
  [评估审计清单], [#ph], [`eval_audit_pass`（建议键）],
  [对手池最强 Elo（池强度标定）], [#ph], [`opponent_pool_max_elo`（建议键）],
)

== m2：A/B 实测与天梯回填

#table(
  columns: (2.6fr, 1.0fr, 2.6fr),
  align: (x, y) => (if x == 0 { left } else { center }) + horizon,
  table.header([*指标*], [*数值*], [*metrics 键*]),
  [LLM A/B 胜率 / 对局数], [#ph], [`llm_ab_win_rate` / `llm_ab_games`（建议键）],
  [预算闸触发 / 回退次数], [#ph], [`llm_ab_budget_gate_hits` / `llm_ab_fallback_count`（建议键）],
  [线上天梯对局数 / skill rating], [#ph], [`online_ladder_games` / `online_skill_rating`（人工回填）],
  [天梯反馈校准动作], [#ph], [`online_feedback_calibration`（建议键）],
)

== 未测项纪律

未发生的指标（如线上提交未启动、A/B 未跑）在终稿中如实呈现为 null（`metrics.unmeasured` 口径），不做估计、不做换算派生（倍率等派生数字同样禁止）。

= 合规与人机分工

== apply 模式合规映射

#table(
  columns: (1.9fr, 2.9fr, 1.0fr),
  align: horizon,
  table.header([*官方政策条款（rules 直抓）*], [*本作品实际用法*], [*判定*]),
  [外部数据与模型允许："The use of external data and models is acceptable unless specifically prohibited by the Host."],
  [提交形态 stdlib-only 自包含；仅依赖官方引擎 vendored 重打包（上游 Apache-2.0，出处 vendor/WHEEL_PROVENANCE.md，引擎代码未改动）。],
  [符合],
  [LLM 费用按 Reasonableness Standard 放行："a small subscription charge to use additional elements of a large language model such as Gemini Advanced are acceptable if meeting the Reasonableness Standard."],
  [LLM 决策模块默认 NullProvider 关闭，仅本地 A/B 实测；内置调用次数与时长预算闸，任何失败 / 超时回退启发式；提交形态不依赖外部模型与网络。],
  [符合（保守启用）],
  [AMLT 放行："Individual Participants and Teams may use automated machine learning tool(s) ('AMLT') ... provided that ... they have an appropriate license."],
  [未使用 AutoML 工具链；按「AI 辅助原创」标准产出：AI 辅助生成代码与文档草稿，队伍主导迭代与裁决（附录 A）。],
  [符合],
  [单账号纪律："You cannot sign up to Kaggle from multiple accounts..."],
  [队伍 3 人（上限 5 人内），单一 Kaggle 账号报名与提交；SOP v2 内嵌防多账号检查项。],
  [符合],
  [数据许可 Apache 2.0；获奖许可 CC-BY 4.0（Winner License Type）],
  [仅使用竞赛提供的官方引擎与规则文本；知悉获奖情形下方案按 CC-BY 4.0 开源的义务。],
  [符合],
  [提交纪律：每日至多 5 次提交、仅最近 2 次计入最终评估；提交先过 Validation Episode],
  [配套提交 SOP v2（`workspace/docs/submit-sop.md`）：提交前本地回归（冒烟 + 测试 + 评估矩阵）、每日提交节奏约束、天梯回填流程、终交前锁定检查单（man-final）。],
  [符合（流程保障）],
)
#text(size: 9pt, fill: gray)[表注：条款原文 2026-08-28 经 Kaggle 官方 ListPages API 直抓（附录 B）；终波由队伍逐条复核签字（人工裁量环节）。容器资源限额与网络政策官方未解析——本作品不依赖、不臆测线上能力。]

== 人机分工（概要）

*AI（autoC 框架）*：全部工程实现（bot / 评估基建 / 对手池强化 / 逐项策略迭代）与本地验证；文档草拟（数字仅引 metrics）。*人工（队伍）*：报名（man-reg）、线上提交与天梯观察回填（man-submit）、终交锁定与切换裁量（man-final / 09-15 决策点）、定稿审读签字。逐环节留痕表见附录 A。

= 遗留与可复用资产

== 遗留与待核

- entry_deadline 官方数值缺失（API Timeline 模板变量未解析）→ man-reg 第 0 天人工核对赛站锁定（置顶，唯一硬时点风险）。
- agent 容器资源限额与网络政策（FAQ 模板变量未解析）→ 提交形态保持 stdlib-only、不依赖外部网络模型，不臆测线上能力。
- 奖池双口径（官方 rules / Prizes 双处直抓口径 vs 列表页口径）→ 不影响模式判定，如实并存待核（meta.md 待核清单）。
- 深度 RL 路线本轮不做（投入产出比判断）→ 如线上反馈显示必须，留下一战役决策。

== 可复用资产清单

- 官方引擎 vendored 复刻路线（同族 Kaggle 仿真赛直用）。
- 评估基建骨架：对手池 / Elo / 复盘日志 / 全量评估协议——本轮升级为 matchup 矩阵 + 方差控制 + 审计清单（增量资产，m1 产出）。
- 失败模式清单与迭代台账（m1 / m2 产出，即自建 patterns 的新增样本）。
- 提交 SOP 检查单（v1 19 项 → v2 新增四类项，见 `workspace/docs/submit-sop.md`）。
- 报告结构与 metrics 键契约（本骨架 + `metrics-keys.md`：schema 驱动的文档生成流程）。

#text(fill: gray)[（占位：终波按实际产出核对清单并补漏。）]

#pagebreak()

= 附录 A：人机分工记录（合规留痕）

本作品由 AI 辅助生成、队伍主导迭代，按「AI 辅助原创」标准产出并在归档时保留本记录。

#table(
  columns: (1.4fr, 2.4fr, 2.2fr),
  align: horizon,
  table.header([*环节*], [*AI（autoC 框架，GLM-5.3 驱动）*], [*人工（队伍）*]),
  [情报与决策支持], [KB 收集与赛道矩阵草拟（来源可溯）], [赛道裁决（用户闸门）、09-15 切换决策点],
  [机制量化], [收益模型 / 红线检查表实现与单测], [机制关键参数对照官方页复核],
  [bot 与评估基建], [bot、评估器、测试、评估脚本实现与执行], [结果审读、迭代方向裁决],
  [对手池强化与策略迭代], [新对手变体、matchup 矩阵、失败模式清单、逐项增强实现与本地验证], [增强合入裁决、最优版本选择],
  [LLM A/B], [模块 A/B 实测执行与数据落 metrics], [启用 / 预算裁量（Reasonableness Standard）],
  [线上提交], [不执行（man-reg / man-submit / man-final 列人工）], [Kaggle 报名、提交操作、天梯观察与记录、终交锁定],
  [文档], [本报告与 SOP v2 草拟（数字仅引 metrics）], [定稿审读与签字确认],
)
#text(size: 9pt, fill: gray)[（占位：终波按战役实际逐项核实修订。）]

= 附录 B：参考来源

赛事事实（赛程 / 奖金 / AI 政策 / 机制）均来自以下官方直抓信源（访问 / 抓取日期 2026-08-28），经 `kb/competitions/kaggle-kaggriculture/meta.md` 转引：

- Kaggle 官方 ListPages API（competitionId=147734）：rules / Prizes / Timeline / Evaluation / How to Play / Foundational Rules 全文——#link("https://www.kaggle.com/api/i/competitions.PageService/ListPages?competitionId=147734")[kaggle.com/api/i/competitions.PageService/ListPages?competitionId=147734]（2026-08-28）
- 赛站：#link("https://www.kaggle.com/competitions/kaggriculture")[kaggle.com/competitions/kaggriculture]（2026-08-28）
- 本仓知识库技术卡：`arxiv-2608.27456`（UrbanGround，评测方法论）、`arxiv-2608.26753`（ABE-Ralph，实验保真审计）、`arxiv-2608.15291`（ReasonCast，选择性干预门控）、`arxiv-2608.25992`（ProgRouter，成本路由）、`arxiv-2608.24087`（Bayesian Self-Escalation）
- 本战役工程产物与数据：`workspace/blueprint.md`、`workspace/strategy.md`、`workspace/software/exports/schema.json`（软件-文档契约）、`workspace/metrics.json`（一切性能数字的唯一来源，终波生成）
- 第一轮归档（结构参照，只读）：`archive/2026-08_Kaggriculture-农场博弈-Agent-战役_720-回合供应链博弈-bot（agentic-RL-风向标赛，09-30-终交`/ 内 `docs/report.typ`、`docs/submit-sop.md`、`software/exports/schema.json`
