// Kaggriculture 战役 II 方案报告（Typst）——成稿（波次 4/4，m3-polish）
// 结构：波次 1/4 冻结的六节 + 附录 A/B，结构不变、数字回填。
// 铁律：本报告一切性能数字只引 workspace/metrics.json 的 `metrics.software.<键>`（表注标键名）；
//       线上未发生与 LLM 真实 A/B 未发生的指标如实呈现 null（§4 边界框），禁止估计与派生数字；
//       赛事事实引 kb/competitions/kaggle-kaggriculture/meta.md（官方直抓，2026-08-28，URL 见附录 B）；
//       软件-文档接口契约：workspace/software/exports/schema.json（v1.1，B 组键已落盘）；
//       波次执行记录引 workspace/JOURNAL.md（2026-08-28 各波次行）。
#set page(paper: "a4", margin: 2.2cm)
#set text(lang: "zh", region: "cn", size: 11pt, font: ("Libertinus Serif", "Microsoft YaHei"))
#set heading(numbering: "1.1")
#set par(justify: true, leading: 0.85em)
#show heading.where(level: 1): it => { v(0.6em); it; v(0.3em) }

// ───────────────────────── 封面 ─────────────────────────
#align(center)[
  #v(1.2em)
  #text(size: 20pt, weight: "bold")[Kaggriculture 农场博弈 Agent 战役 II 方案报告]
  #v(0.5em)
  #text(size: 12pt)[Kaggle Simulation Competition「Kaggriculture」（Google 自办）· apply 模式 · 参赛级迭代至 09-30 终交]
  #v(0.3em)
  #text(size: 11pt)[队伍单账号提交（3 人，团队上限 5 人内） · 2026-08-28]
  #v(0.3em)
  #text(size: 10pt, fill: gray)[成稿（波次 4/4，m3-polish）：一切性能数字出自 workspace/metrics.json 实测键；线上未发生指标如实 null]
]
#v(0.8em)

= 摘要

本报告是 Kaggle Simulation Competition「Kaggriculture」*第二轮战役*（终交 2026-09-30）的方案报告。第二轮使命从第一轮的「框架闭环验证」升级为「参赛级迭代」：工程底座（可提交 bot + 本地评估基建）自归档原样复活并冻结回归线（m0），边际投入全部落在两个夺奖变量——*线上标定*（m1 对手池强化 + man-submit 天梯反馈回填）与*策略增强*（m2 失败模式驱动迭代，每项过评估矩阵才合入），m3 完成终交锁定与文档成稿。

本版为波次 4/4（m3-polish）成稿：四阶段波次（m0 资产复活 → m1 对手池强化竖切 → m2 失败模式驱动迭代 → m3 文档成稿与终交准备）已收口，六节结构与波次 1 冻结版一致；§4 实测结果全部回填自 `workspace/metrics.json`（表注标键名），未发生的线上与 LLM 真实 A/B 指标如实呈现 null 并附边界说明。合规模式 apply（官方 rules 2026-08-28 直抓，逐条映射见 §5）；人机分工：AI 全部实现与本地验证，人工报名（man-reg）/线上提交与天梯观察（man-submit）/终交锁定与裁量（man-final），留痕见附录 A。

核心实测结论（均为本地官方引擎实测，键名见 §4）：

- *全池（9 bot）Elo 第一*：重构后 submission 1500.8，其全部 36 局 W36-L0-T0，领先第二名 cow_baron 81.2 分——`m2_elo_ratings_full_pool`。
- *对 m1 新增强敌头对头翻盘*：cow_baron 10W-2L、melon_hoarder 11W-1L（seeds 101-104 与 201-208 唯一种子）——`m2_matchup_win_rates`；m1 时为 0/4 与 0/4 全负（`m1_matchup_win_rates`）。
- *关键转折——弱池假象确证*：m1 强池入局后旧 submission 对 cow_baron / melon_hoarder 双零封，第一轮「对冻结弱池 24/24 不败」确证为弱池假象，评估口径随之升级为 matchup 全矩阵 + 方差 + 审计（§3.2）。
- *工程护栏*：测试 101/101 全绿（50 → 84 → 101 三阶段递增）；评估审计 8 pass / 3 warn / 0 fail；旧弱池回归门复跑 PASS——`m2_tests_passed`、`eval_audit_pass`、`m2_regression_gate_pass`。
- *如实 null*：线上天梯三键（未提交，man-submit 人工项）、LLM 真实 A/B 胜率（待 `KG_LLM_*` key，harness 已就绪）、终交锁定 commit（man-final 待执行）——`metrics.unmeasured`。

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
#text(size: 9pt, fill: gray)[表注：本表只作定位对照、不含性能数值——第一轮实测数值以归档 metrics.json 为准，第二轮数值已回填（§4，键名见表注）。]

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

评估产出按 `workspace/software/exports/schema.json`（draft 2020-12，自第一轮归档原样复活，本轮已 bump 至 v1.1）落盘：逐局 `games`（p0 / p1 / seed / rewards / winner / turns / elapsed_seconds）、`head_to_head` 逐对战绩、`elo` 表（k / start / rating / record）、`runtime_seconds`——文档侧 metrics 键与该契约逐一对齐（清单见 `workspace/docs/metrics-keys.md`）。m1 / m2 新增口径（方差报告、审计清单、失败模式、LLM A/B、天梯回填）已随 schema v1.1 落盘（B 组键），文档引用的键均已在 `workspace/metrics.json` 中存在；未落盘数值一律不引用。

= 四阶段波次执行记录

本章按 `workspace/JOURNAL.md` 波次行逐波写实（记录时点 2026-08-28）；波次内一切数字可回溯至 metrics 键（§4 表注）。

== m0：资产复活与回归线冻结（波次 1/4）

目标：从归档复制工程 42 文件到 workspace（archive 只读不改）、依赖锁定安装（含 vendored 官方引擎 wheel）；测试全绿（第一轮基线 + 本轮新增）；固定种子复现第一轮 Elo 排序为回归断言（`run_eval.py --assert-regression`：submission > baseline_wheat > greedy_carrot > starter > random > pass，且 submission 对冻结池不败）；metrics 键清单与报告大纲（本文件）；人工项置顶发出（man-reg）。验收项：m0-deps / m0-boot / m0-test / m0-regress。

执行记录（JOURNAL 18:05 波次行）：42 文件自归档复活、逐文件 diff 验证一致（归档保持只读）；测试 50/50 通过（45 复活基线 + 5 回归门新增，`tests_passed` / `tests_total`）；冒烟自检 PASS（3.3 s，`smoke_boot_pass` / `smoke_boot_runtime_seconds`）；回归门同参两跑 PASS 且 Elo 逐位可复现（20 局、submission 12W-0L-0T，`regression_gate_pass` / `regression_gate_submission_record`）；40 局全量评估复现第一轮口径（107.36 s、单局均值 2.66 s、720 回合全长，`eval_games_total` / `eval_runtime_seconds` / `avg_episode_runtime_seconds` / `avg_turns_per_game`）；跨会话逐局比对 32/40 奖励一致（漂移 8 局全部来自引擎 random agent 的 OS 熵自播，`cross_session_replay_identical_games`）；metrics 20 键实测落盘、报告骨架编译通过；人工项置顶发出。scoped 验收 m0- / doc- 全 pass。

== m1：对手池强化竖切（波次 2/4）

目标：新增 2-3 个强启发式对手变体 + matchup 全矩阵 + 方差报告与评估审计清单（ABE-Ralph 式）；输出当前 bot 对新池的失败模式清单——后续一切策略增强的证据基础。验收项：m1-matrix。

执行记录（JOURNAL 20:10 波次行）：三强对手入库——cow_baron / melon_hoarder / expansionist，各经强度门对冻结弱池 4 对手 × 3 种子 9/9 全胜认证（`opponent_pool_names` method）；148 局全矩阵（36 对 × 4 种子 + 4 头对头 +500 偏移种子 + 4 确定性探针，346.94 s，`m1_eval_games_total` / `m1_eval_runtime_seconds`）+ Wilson / t 区间方差报告（`eval_variance_report`）+ ABE-Ralph 式 11 项审计 8 pass / 3 warn / 0 fail（`eval_audit_pass`）+ 四条失败模式清单 FM-1 至 FM-4（探针 64 局 49W-15L-0T，`failure_modes`）。

*关键转折——弱池假象确证*：旧 submission 对 cow_baron 与 melon_hoarder 均 0/4 全负（胜率 0.0、平均分差 -17772 / -5410，`m1_matchup_win_rates` / `m1_submission_margin_vs_pool`），第一轮「对冻结弱池 24/24 不败」（m0 会话 `submission_win_rate_vs_pool`）被确证为弱池假象。本波由此成为整场战役的评估口径转折点：此后一切增强以全矩阵 + 方差区间 + 审计为合入门禁。

*冻结线尾序修订留痕*：m0 冻结序子句「random > pass」经 m1 全矩阵数据复核为首轮子矩阵伪影（m0 子矩阵中 random 与 pass 从未交手，相对序是对手字典迭代顺序在 Elo 流中的伪影）；全矩阵实测 pass 对 random 100% 胜，据此把该子句修订为「pass > random」并回写蓝图留痕（`m0_regression_pass` method 注；论证全文见 `exports/eval_audit.md` 第 6 项）。*submission 相关的两条不变量（Elo 降序中 submission 居首 + 对冻结池不败）原样未动*；修订后回归门复跑 PASS（74 局 196.17 s，冻结子流 32 局 submission 0 负）。测试增至 84/84（`m1_tests_total` / `m1_tests_passed`）；schema v1.1 扩 B 组键。scoped 验收 m1- pass。

== m2：失败模式驱动迭代 + 线上闭环（波次 3/4）

目标：按失败模式清单逐项改进（市场门控升级 / 资本计划 / 劳动调度），每项过评估矩阵才合入；LLM 模块 A/B 实测落 metrics（m2-ab，含预算闸与回退生效证据）；启动线上提交节奏（man-submit）并回填天梯反馈校准本地对手池；09-15 保留 RSNA 切换决策点（strategy 第五节兜底路径）。

执行记录（JOURNAL 21:35 波次行）：按 FM 清单逐项迭代，8 轮设计迭代留下 16 条门记录（10 条实时 + 6 条自会话运行日志补录并标记 retroactive=true；最终 PASS：v2c-dairy-r8，`m2_iteration_gate_log`）。FM-1 根因级重构——动物引擎由鹅换奶牛 + 显式选择性干预市场门控（`m2_submission_engine`，stdlib-only 自包含）；FM-2 引擎级消除溢价作物敞口（瓜双波移除）；FM-3 小麦先行分期资本；FM-4 门控出货 + 自用施肥（`failure_mode_status_m2`：FM-1/2/3 已缓解、FM-4 部分缓解）。终版实测：全池（9 bot）Elo 第一 1500.8（其全部 36 局 W36-L0-T0、领先第二名 81.2 分，`m2_elo_ratings_full_pool`）；对强敌头对头 cow_baron 10W-2L、melon_hoarder 11W-1L（`m2_matchup_win_rates`）；8 种子失败探针 53W-3L-0T，3 负局均为需求枯竭类种子（`m2_probe_record`）；旧弱池回归门复跑 PASS（`m2_regression_gate_pass`）+ 冒烟 PASS（3.7 s，`m2_smoke_boot_pass`）；测试增至 101/101（`m2_tests_total` / `m2_tests_passed`）。LLM A/B harness 就绪并经 NullProvider 管道验证（`llm_ab_harness_ready` / `llm_ab_fallback_count`）——*真实 A/B 因环境无 `KG_LLM_*` key 未发生，胜率如实 null*（`llm_ab_win_rate`）；线上提交未发生（man-submit 人工项，`online_ladder_games` null）。

== m3：终交锁定（波次 4/4，本波）

目标：终交前提交管理（「最近 2 份最优」锁定，man-final）；报告与 SOP v2 定稿（消费 merge_metrics 稳定值，数字只出自 metrics.json）。验收项：doc-compile / man-final。

收口记录（本波）：报告成稿（本文件——§4 全部数字回填自 `workspace/metrics.json` 汇总生成物，消费时点快照 `_generated_at` = 2026-08-28T20:28:00）；提交 SOP v2 定稿为可执行检查单（`workspace/docs/submit-sop.md`：19 项基础 + 四组新增共 36 项——报名前置门 / 每日提交纪律逐次检查列 / 天梯反馈回填 metrics 流程 / 终交「最近 2 份最优」锁定）；doc-compile 验收执行（typst 编译 exit 0，见 §4.6 文档侧实测）。man-final 为人工项：按 SOP v2 §6 于 09-30 前执行，`final_submission_commits` 待锁定时回填（当前 null）。

= 实测结果

本节全部数字回填自 `workspace/metrics.json`（铁律 4：对局指标只出自实测值，表注标键名；消费时点快照 `_generated_at` = 2026-08-28T20:28:00）。键清单与用途见 `workspace/docs/metrics-keys.md`；波次 1 骨架所标「建议键」均已随 schema v1.1 落盘后方可引用。全部对局运行在 vendored 官方引擎（kaggle-environments 1.32.7+nodeps，引擎代码未改动，720 回合全长，`engine` 边界注：所有数字为本地实测、无线上对局）。未发生指标如实 null（§4.5 边界框与 §4.6 未测项纪律）。

== m0：回归线（复活复现）

#table(
  columns: (2.6fr, 1.3fr, 2.4fr),
  align: (x, y) => (if x == 0 { left } else { center }) + horizon,
  table.header([*指标*], [*数值*], [*metrics 键*]),
  [测试套件通过 / 总数], [50 / 50], [`tests_passed` / `tests_total`],
  [冒烟自检], [PASS（3.3 s）], [`smoke_boot_pass` / `smoke_boot_runtime_seconds`],
  [回归断言（Elo 排序复现 + 冻结池不败）], [PASS（两跑；m1 波复跑 74 局 196.17 s，冻结子流 32 局 submission 0 负）], [`regression_gate_pass`；复跑 `m0_regression_pass`；排序证据 `elo_ratings`],
  [回归门内 submission 战绩], [12W-0L-0T], [`regression_gate_submission_record`],
  [全量评估对局数 / 总耗时 / 单局均值], [40 局 / 107.36 s / 2.66 s], [`eval_games_total` / `eval_runtime_seconds` / `avg_episode_runtime_seconds`],
  [单局平均回合数（全长核查）], [720.0], [`avg_turns_per_game`],
  [对冻结弱池胜率 / 对基线头对头], [1.0（16W-0L）/ 1.0（8W-0L）], [`submission_win_rate_vs_pool` / `submission_win_rate_vs_baseline`],
  [submission 平均终局资金（对池 / 头对头）], [30631.46 / 29325.12（对手 11475.25）], [`submission_avg_final_money` / `submission_avg_final_money_h2h` / `baseline_wheat_avg_final_money_vs_submission`],
  [跨会话逐局一致（复活验证）], [32 / 40（漂移全部来自引擎 random agent）], [`cross_session_replay_identical_games`],
)
#text(size: 9pt, fill: gray)[表注：m0 会话复活复现 Elo 序 `submission` 1460.9 \> `baseline_wheat` 1245.8 \> `greedy_carrot` 1162.2 \> `starter` 1122.9 \> `random` 1111.2 \> `pass` 1097.0（`elo_ratings`，40 局、k=32、start=1200）——尾序 random/pass 为子矩阵伪影，m1 全矩阵数据修订为 pass \> random（留痕见 §3.2）。该 16W-0L / 24 局不败均为*冻结弱池*口径；m1 强池入局后对 cow_baron / melon_hoarder 胜率跌至 0.0（§4.2）——弱池假象的确证证据。]

== m1：对手池与 matchup 矩阵

#table(
  columns: (2.6fr, 1.3fr, 2.4fr),
  align: (x, y) => (if x == 0 { left } else { center }) + horizon,
  table.header([*指标*], [*数值*], [*metrics 键*]),
  [Elo 表（含新对手，9 bot 全池）], [见下表], [`m1_elo_ratings_full_pool`],
  [matchup 全矩阵逐对胜率（36 对）], [submission：cow_baron 0.0、melon_hoarder 0.0、其余 6 对手均 1.0], [`m1_matchup_win_rates`],
  [胜率 / 评级方差报告], [见下方要点], [`eval_variance_report`],
  [评估审计清单（11 项）], [8 pass / 3 warn / 0 fail（critical 全过）], [`eval_audit_pass`],
  [对手池最强 Elo（池强度标定）], [cow_baron 1460.3（m0 为 1162.2）], [`opponent_pool_max_elo`],
  [失败模式清单（探针 64 局，seeds 201-208）], [4 条；总战绩 49W-15L-0T；负局集中于 melon_hoarder（0-8）与 cow_baron（1-7）], [`failure_modes`],
  [矩阵规模 / 耗时 / 测试], [148 局 / 346.94 s / 84 通过 84], [`m1_eval_games_total` / `m1_eval_runtime_seconds` / `m1_tests_passed` / `m1_tests_total`],
)

m1 全池 Elo（148 局，k=32、start=1200；同参两跑表逐位复现，仅涉 random 对局奖励漂移——method 注）：

#table(
  columns: (1.4fr, 0.9fr, 1.4fr, 0.9fr),
  align: horizon,
  table.header([*bot*], [*Elo*], [*bot*], [*Elo*]),
  [cow_baron（新）], [1460.3], [baseline_wheat], [1170.6],
  [submission], [1422.8], [greedy_carrot], [1155.8],
  [melon_hoarder（新）], [1391.3], [starter], [1058.3],
  [expansionist（新）], [1289.6], [pass], [991.5],
  [], [], [random], [859.7],
)
#text(size: 9pt, fill: gray)[表注：`m1_elo_ratings_full_pool`——submission 居第 2（method 注：2nd of 9）；对强敌的平均分差 cow_baron -17772、melon_hoarder -5410、expansionist +10014（`m1_submission_margin_vs_pool`）。]

方差要点（`eval_variance_report`，Wilson 95% 胜率区间 + Student-t 95% 资金差区间，逐对 4 种子）：

- 最不稳对（弱池内部）：baseline_wheat vs greedy_carrot 胜率 0.75、CI95 \[0.3006, 0.9544\]、跨种子结果翻转（flips=true）。
- submission 相关对局跨种子无翻转（`no_submission_pair_flipped_outcomes_across_seeds`）；对 cow_baron / melon_hoarder 的 CI95 均为 \[0.0, 0.4899\]，失败结论另由 8 种子探针加固（0/8 与 1/8 跨 seeds 201-208 稳定——method 注）。
- 审计 3 warn 均为已声明边界：第 7 项同族对手过拟合、第 8 项单座位对局、第 9 项小样本方差——跟进责任：m2 增强判据强制区间报告、线上校准后重校池构成（§5.1 合规表注同源）。

== m2：策略迭代实测（失败模式驱动）

迭代门摘要（每项候选改动先过门、后合入）：

#table(
  columns: (2.6fr, 1.3fr, 2.4fr),
  align: (x, y) => (if x == 0 { left } else { center }) + horizon,
  table.header([*指标*], [*数值*], [*metrics 键*]),
  [门记录条数 / 设计迭代轮数], [16 条（实时 10 + 补录 6，retroactive=true 标记）/ 8 轮], [`m2_iteration_gate_log`],
  [最终门判定], [PASS（v2c-dairy-r8：黎明 HIRE 突发 + 腐烂抢救收割 + 清仓式放奶门 + 幽灵补饲料修复）], [`m2_iteration_gate_log`（final 字段）],
  [引擎重构], [鹅 + 瓜双波 → 奶牛 + 施肥小麦 + 显式选择性干预市场门控（stdlib-only 自包含，双座位 / 短局 / gym 契约测试绿）], [`m2_submission_engine`],
  [FM 状态], [FM-1 / FM-2 / FM-3 已缓解；FM-4 部分缓解], [`failure_mode_status_m2`],
)

m2 终版实测（合并后 bot 的最终产物运行，148 局矩阵 + 64 局探针）：

#table(
  columns: (2.6fr, 1.3fr, 2.4fr),
  align: (x, y) => (if x == 0 { left } else { center }) + horizon,
  table.header([*指标*], [*数值*], [*metrics 键*]),
  [全池 Elo（9 bot）], [submission 第一：1500.8（其全部 36 局 W36-L0-T0；领先第二名 81.2 分）], [`m2_elo_ratings_full_pool`],
  [矩阵胜率（seeds 101-104）], [对全部 8 对手均 1.0], [`m2_matchup_win_rates`（matrix_seeds_101_104）],
  [探针胜率（seeds 201-208）], [cow_baron 0.75、melon_hoarder 0.875、其余 1.0], [`m2_matchup_win_rates`（probe_seeds_201_208）],
  [唯一种子头对头], [cow_baron 10W-2L、melon_hoarder 11W-1L（seeds 101-104 + 201-208）], [`m2_matchup_win_rates`（unique_seed_head_to_head）],
  [探针战绩与负局画像], [53W-3L-0T；3 负局 = cow_baron seed 204（-3213）、206（-3587）、melon_hoarder seed 208（-1413）；均为需求枯竭局（城镇零奶类商铺抽取、奶价 9-40 地板）——市场随机性、非对手可针对行为], [`m2_probe_record`],
  [平均分差（对强敌）], [cow_baron +3330、melon_hoarder +12875（m1 为 -17772 / -5410）], [`m2_submission_margin_vs_pool`],
  [回归门 / 冒烟 / 测试], [PASS / PASS（3.7 s）/ 101 通过 101（进度 50 → 84 → 101）], [`m2_regression_gate_pass` / `m2_smoke_boot_pass` / `m2_tests_passed` / `m2_tests_total`（对照 `tests_total`、`m1_tests_total`）],
)

#table(
  columns: (1.4fr, 0.9fr, 1.4fr, 0.9fr),
  align: horizon,
  table.header([*bot*], [*Elo*], [*bot*], [*Elo*]),
  [submission], [1500.8], [baseline_wheat], [1177.7],
  [cow_baron], [1419.6], [greedy_carrot], [1154.1],
  [melon_hoarder], [1355.1], [starter], [1056.8],
  [expansionist], [1287.1], [pass], [990.4],
  [], [], [random], [858.4],
)
#text(size: 9pt, fill: gray)[表注：`m2_elo_ratings_full_pool`（148 局、363.11 s、k=32、start=1200）；method 注：m1 对照 submission 1422.8（第 2/9）→ m2 1500.8（第 1/9）。]

== m2：A/B 实测与天梯回填

#table(
  columns: (2.6fr, 1.3fr, 2.4fr),
  align: (x, y) => (if x == 0 { left } else { center }) + horizon,
  table.header([*指标*], [*数值*], [*metrics 键*]),
  [LLM A/B 胜率 / 对局数], [null（真实 A/B 未发生）/ 4（NullProvider 管道验证局，非 A/B 结论）], [`llm_ab_win_rate` / `llm_ab_games`],
  [预算闸触发 / 回退次数], [null（NullProvider 无预算对象，未触发）/ 1294（每次咨询均回退启发式——回退路径实测生效）], [`llm_ab_budget_gate_hits` / `llm_ab_fallback_count`],
  [线上天梯对局数 / skill rating], [null / null（man-submit 人工项未执行）], [`online_ladder_games` / `online_skill_rating`],
  [天梯反馈校准动作], [null（待线上反馈触发）], [`online_feedback_calibration`],
  [终交锁定 commit], [null（man-final 待执行）], [`final_submission_commits`],
  [A/B harness 就绪度], [true（一键双座位带 provider 计数；验证跑 4 局 13.06 s、座位对称）], [`llm_ab_harness_ready`],
)

#block(fill: rgb("#f4f4f4"), inset: 9pt, radius: 3pt)[
*边界说明——如实 null（未发生不估计、不派生）*

- *LLM 真实 A/B 未发生*：harness 已就绪（`llm_ab_harness_ready`：`run_llm_ab.py --rounds 2` 一条命令，LLM-on 侧接 `provider_from_env()`、双座位、provider 计数；NullProvider 验证实测 4 局 13.06 s、1294 次咨询全部启发式回退、0 预算阻断）。因当前环境无 `KG_LLM_*` 环境变量，A/B 两侧运行相同启发式策略，胜率实测无意义，故 `llm_ab_win_rate` 如实置 null——待用户提供 key 后按 m2-ab 验收补测（启用与否本身是人工裁量项，Reasonableness Standard）。
- *线上指标全部未发生*：Kaggle 报名与提交为队伍人工项（man-reg / man-submit），本报告成稿时点尚未执行，`online_ladder_games` / `online_skill_rating` / `online_feedback_calibration` / `final_submission_commits` 四键如实 null；回填流程见 SOP v2 新增组 3（§4 每日观察 → 三键转录 → 背离触发校准）。
- *本地结论的适用边界*：本节全部战绩与 Elo 为本地 9 bot 池结论（148 局矩阵 + 8 种子探针），天梯真实对手分布未标定；同族对手过拟合、单座位、小样本方差三条 warn 已在审计中声明（§4.2），线上标定是消除该边界的唯一路径。
]

== 未测项纪律

未发生的指标（线上提交未启动、LLM 真实 A/B 未跑、终交未锁定）如实呈现为 null（`metrics.unmeasured` 口径，共 6 键：`llm_ab_win_rate`、`llm_ab_budget_gate_hits`、`online_ladder_games`、`online_skill_rating`、`online_feedback_calibration`、`final_submission_commits`），不做估计、不做换算派生（倍率等派生数字同样禁止）；已发生的替代证据（harness 管道验证、探针加固）如实标注性质，不冒充真实 A/B 或线上结论。

== 文档侧实测（本波 m3）

#table(
  columns: (2.6fr, 1.3fr, 2.4fr),
  align: (x, y) => (if x == 0 { left } else { center }) + horizon,
  table.header([*指标*], [*数值*], [*metrics 键（document 分片）*]),
  [报告编译（doc-compile 验收）], [见 `workspace/document/metrics.json`（本波实测：exit code / 耗时 / 页数）], [`report_compile_exit_code` 等],
  [SOP v2 检查单规模], [19 项基础 + 四组新增 17 项 = 36 项], [`sop_v2_base_items` / `sop_v2_new_group_items` 等],
)
#text(size: 9pt, fill: gray)[表注：document 分片为 `merge_metrics` 汇总命名空间（`metrics.document.*`），本表引用其键名；数值以该分片落盘值为准，本节不重复抄录（避免双源不一致）。]

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
  [LLM 决策模块默认 NullProvider 关闭；本轮 A/B harness 就绪并经管道验证（1294 次回退实测生效），真实 A/B 因 `KG_LLM_*` key 未提供如实 null；内置调用次数与时长预算闸，任何失败 / 超时回退启发式；提交形态不依赖外部模型与网络。],
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
  [配套提交 SOP v2（`workspace/docs/submit-sop.md`，36 项）：提交前本地四查（冒烟 + 测试 + 矩阵评估 + 回归门）、每日提交纪律逐次检查列、天梯回填流程、终交前锁定检查单（man-final）。],
  [符合（流程保障）],
)
#text(size: 9pt, fill: gray)[表注：条款原文 2026-08-28 经 Kaggle 官方 ListPages API 直抓（附录 B）；终交前由队伍逐条复核签字（人工裁量环节，man-final 组成部分）。容器资源限额与网络政策官方未解析——本作品不依赖、不臆测线上能力。]

== 人机分工（概要）

*AI（autoC 框架）*：四阶段波次的全部工程实现与本地验证——bot 复活与回归线冻结、三强对手设计入库、matchup 全矩阵 / 方差 / 审计评估基建、16 条迭代门记录驱动的引擎重构、LLM A/B harness 及其管道验证、测试套件（50 → 84 → 101）；文档成稿（本报告与 SOP v2，数字仅引 metrics）。*人工（队伍）*：报名（man-reg）、线上提交与天梯观察回填（man-submit）、`KG_LLM_*` key 供给与 LLM 启用 / 预算裁量（Reasonableness Standard）、增强合入裁决与最优版本选择、终交锁定与 09-15 切换裁量（man-final / 决策点）、定稿审读签字。逐环节留痕表见附录 A。

= 遗留与可复用资产

== 遗留与待核

- *线上标定未发生*（最大遗留）：man-reg / man-submit 人工项截至成稿未执行，`online_ladder_games` / `online_skill_rating` / `online_feedback_calibration` 三键 null；entry_deadline 官方数值仍缺失，第 0 天人工锁定（置顶，唯一硬时点风险）。回填流程已就绪（SOP v2 新增组 3）。
- *FM-4 部分缓解*：肥料线性 glut + 零城镇消费的曲线结构下双人卖压仍单调下行，门控只能延缓（`failure_mode_status_m2`）；残留 3 负局为需求枯竭类种子（204 / 206 / 208，市场随机性，`m2_probe_record`）——不可对手级针对，接受为分布内损失。
- *LLM 真实 A/B 待 key*：`llm_ab_win_rate` / `llm_ab_budget_gate_hits` null；harness 就绪（`llm_ab_harness_ready`），用户提供 `KG_LLM_*` 后即可补测。
- *审计 warn 跟进*：第 7 项同族对手过拟合（三强对手均为我方同族设计）→ man-submit 后按线上反馈重校池构成；第 8 项单座位（探针 64 局均 p0 位）→ 下一战役 p1 位复测；第 9 项小样本方差 → 增强判据已强制区间报告。
- *agent 容器资源限额与网络政策*（FAQ 模板变量未解析）→ 提交形态保持 stdlib-only、不依赖外部网络模型，不臆测线上能力。
- *奖池双口径*（官方 rules / Prizes 双处直抓 50,000 vs 列表页 60,000）→ 不影响模式判定，如实并存待核（meta.md 待核清单）。
- *深度 RL 路线本轮不做*（投入产出比判断）→ 如线上反馈显示必须，留下一战役决策。

== 可复用资产清单（▲ = 对第一轮清单的增量）

- 官方引擎 vendored 复刻路线（同族 Kaggle 仿真赛直用，沿用）。
- 评估基建骨架：对手池 / Elo / 复盘日志 / 全量评估协议（沿用，m0 复活验证 32/40 逐局一致）。
- ▲ *强对手池 + 强度门认证协议*：三强启发式对手（cow_baron / melon_hoarder / expansionist）及「对弱池 9/9 全胜才入库」认证流程（`opponent_pool_names` method）——直接对症「对手池偏弱」。
- ▲ *迭代门*：候选 → 头对头 + 守门 → JSONL 台账（16 条记录、retroactive 如实标记），一切增强过门才合入（`m2_iteration_gate_log`）。
- ▲ *方差与审计协议*：Wilson / t 区间方差报告 + ABE-Ralph 式 11 项审计清单与 3 warn 声明边界机制（`eval_variance_report` / `eval_audit_pass`）。
- ▲ *LLM A/B harness*：一键双座位、provider 计数、预算闸与回退路径可实测（`llm_ab_harness_ready` / `llm_ab_fallback_count`）。
- 失败模式清单与迭代台账（m1 / m2 产出，即自建 patterns 的新增样本）。
- 提交 SOP 检查单（v1 19 项 → v2 36 项 = 基础 19 + 四组新增 17，见 `workspace/docs/submit-sop.md`）。
- 报告结构与 metrics 键契约（schema v1.1 驱动的文档生成流程：`metrics-keys.md` + 本报告六节骨架）。

#pagebreak()

= 附录 A：人机分工记录（合规留痕）

本作品由 AI 辅助生成、队伍主导迭代，按「AI 辅助原创」标准产出并在归档时保留本记录。下表按战役实际逐项核实（m3-polish 波次）。

#table(
  columns: (1.4fr, 2.4fr, 2.2fr),
  align: horizon,
  table.header([*环节*], [*AI（autoC 框架，GLM-5.3 驱动）*], [*人工（队伍）*]),
  [情报与决策支持], [KB 收集与赛道矩阵草拟（来源可溯）], [赛道裁决（用户闸门）、09-15 切换决策点],
  [机制量化], [收益模型 / 红线检查表实现与单测], [机制关键参数对照官方页复核],
  [bot 与评估基建], [bot、评估器、测试、评估脚本实现与执行（m0 复活 42 文件 + 回归线冻结）], [结果审读、迭代方向裁决],
  [对手池强化与策略迭代], [三强对手设计与强度认证、matchup 矩阵 / 方差 / 审计、16 条迭代门与引擎重构（奶牛引擎 + 市场门控）、101 测试全绿], [增强合入裁决、最优版本选择],
  [LLM A/B], [harness 实现与 NullProvider 管道验证（1294 次回退实测，数据落 metrics）], [`KG_LLM_*` key 供给、启用 / 预算裁量（Reasonableness Standard）],
  [线上提交], [不执行（man-reg / man-submit / man-final 列人工）；SOP v2 检查单与回填流程就绪], [Kaggle 报名、提交操作、天梯观察与记录、终交锁定与签字],
  [文档], [本报告与 SOP v2 成稿（数字仅引 metrics，null 如实呈现）], [定稿审读与签字确认（man-final 前完成）],
)
#text(size: 9pt, fill: gray)[表注：AI 侧各环节产物于 `workspace/JOURNAL.md` 波次行、`workspace/software/exports/`（含 `logs/iteration_gate_log.jsonl`）与验收记录留痕；报告内一切性能数字可经表注键名回溯至 `workspace/metrics.json`。]

= 附录 B：参考来源

赛事事实（赛程 / 奖金 / AI 政策 / 机制）均来自以下官方直抓信源（访问 / 抓取日期 2026-08-28），经 `kb/competitions/kaggle-kaggriculture/meta.md` 转引：

- Kaggle 官方 ListPages API（competitionId=147734）：rules / Prizes / Timeline / Evaluation / How to Play / Foundational Rules 全文——#link("https://www.kaggle.com/api/i/competitions.PageService/ListPages?competitionId=147734")[kaggle.com/api/i/competitions.PageService/ListPages?competitionId=147734]（2026-08-28）
- 赛站：#link("https://www.kaggle.com/competitions/kaggriculture")[kaggle.com/competitions/kaggriculture]（2026-08-28）
- 本仓知识库技术卡：`arxiv-2608.27456`（UrbanGround，评测方法论）、`arxiv-2608.26753`（ABE-Ralph，实验保真审计）、`arxiv-2608.15291`（ReasonCast，选择性干预门控）、`arxiv-2608.25992`（ProgRouter，成本路由）、`arxiv-2608.24087`（Bayesian Self-Escalation）
- 本战役工程产物与数据：`workspace/blueprint.md`、`workspace/strategy.md`、`workspace/JOURNAL.md`（波次执行记录）、`workspace/software/exports/schema.json`（软件-文档契约 v1.1）、`workspace/software/exports/eval_results.json` / `eval_audit.md` / `failure_modes.md`、`workspace/software/exports/logs/iteration_gate_log.jsonl`（迭代门台账）
- `workspace/metrics.json`（一切性能数字的唯一来源，merge_metrics 生成物；本报告消费时点快照 2026-08-28T20:28:00）与 `workspace/document/metrics.json`（文档侧实测分片）
- 第一轮归档（结构参照，只读）：`archive/2026-08_Kaggriculture-农场博弈-Agent-战役_720-回合供应链博弈-bot（agentic-RL-风向标赛，09-30-终交`/ 内 `docs/report.typ`、`docs/submit-sop.md`、`software/exports/schema.json`
