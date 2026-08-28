# 战役 II metrics 键清单（工程角色积累指引）

> 用途：本文件是蓝图 m0 交付物「metrics 键清单」，定义 software 侧须在 `workspace/metrics.json`（`software` 分片）积累的键，供报告（`workspace/docs/report.typ` §4）与 SOP v2 引用。
> 对齐依据：`workspace/software/exports/schema.json`（draft 2020-12，自第一轮归档原样复活——games / head_to_head / elo / runtime_seconds 顶层字段）+ 蓝图 10 项验收（m0-deps / m0-boot / m0-test / m0-regress / m1-matrix / m2-ab / doc-compile / man-reg / man-submit / man-final）。
> 纪律（铁律 4）：一切键值必须实测落盘；文档引用形如 `metrics.software.<键>` 并在表注标键名；未测 = null 如实呈现，禁止占位数字与换算派生值。

## A. 既有键（schema v1.0 派生，m0 复活后即可回填）

| 键 | 用途（一句） | 验收对齐 |
|---|---|---|
| `metrics.software.tests_total` / `tests_passed` | 测试套件规模与通过数，复活后须覆盖第一轮基线加本轮新增 | m0-test |
| `metrics.software.smoke_boot_pass` / `smoke_boot_runtime_seconds` | 冒烟自检通过与耗时（起环境、跑局、契约校验、看门狗） | m0-boot |
| `metrics.software.eval_games_total` | 全量评估对局总数（m0 回归复现与 m1 矩阵共用口径） | m0-regress / m1-matrix |
| `metrics.software.eval_runtime_seconds` / `avg_episode_runtime_seconds` | 评估总耗时与平均单局耗时，SOP v2 资源裕量自查引用 | man-submit（提交前检查） |
| `metrics.software.avg_turns_per_game` | 平均单局回合数，核查 720 回合全长度对局完整性 | m0-boot（口径核查） |
| `metrics.software.elo_ratings` | Elo 表（k / start / 各 bot rating + W-L-T record）——m0 作回归排序断言证据，m1 起新对手入表 | m0-regress / m1-matrix |
| `metrics.software.submission_win_rate_vs_pool` / `submission_win_rate_vs_baseline` | 提交 bot 对池 / 对基线头对头胜率（schema head_to_head 派生） | m0-regress（不败断言） |
| `metrics.software.submission_avg_final_money` / `submission_avg_final_money_h2h` | 提交 bot 终局资金均值（对池 / 头对头两口径，A/B 对照基线） | m1-matrix 参照 |

## B. 本轮新增键（建议——需 software 侧扩展 schema v1.1 后落盘，文档在落盘前不得引用其数值）

### m0（回归线）

| 键 | 用途（一句） | 验收对齐 |
|---|---|---|
| `metrics.software.m0_regression_pass` | `run_eval.py --assert-regression` 回归断言布尔（固定种子 Elo 排序复现 + 冻结池不败），复活是否成功的直接证据 | m0-regress |

### m1（对手池 / 矩阵 / 方差）

| 键 | 用途（一句） | 验收对齐 |
|---|---|---|
| `metrics.software.opponent_pool_names` | 对手池构成清单（含新变体命名），矩阵与天梯校准的基准描述 | m1-matrix |
| `metrics.software.opponent_pool_max_elo` | 对手池最强 Elo——量化「对手池偏弱」问题的改善程度 | m1-matrix |
| `metrics.software.matchup_win_rates` | matchup 全矩阵逐对胜率（schema head_to_head 数组按 contender × opponent 展开），一切增强合入的判据 | m1-matrix |
| `metrics.software.eval_variance_report` | 胜率 / 评级的种子间方差与区间估计——方差控制证据，防小样本自欺 | m1-matrix（方差报告） |
| `metrics.software.eval_audit_pass` | ABE-Ralph 式评估审计清单逐项通过记录（配置 / 种子 / 引擎版本留痕） | m1-matrix（审计清单） |
| `metrics.software.failure_modes` | 当前 bot 对新池的失败模式清单（条目 + 计数）——m2 迭代的证据基础 | m1-matrix（输出物） |

### m2（A/B 与线上闭环）

| 键 | 用途（一句） | 验收对齐 |
|---|---|---|
| `metrics.software.llm_ab_win_rate` | LLM 模块开启与否的对局胜率差（A/B 主指标） | m2-ab |
| `metrics.software.llm_ab_games` | A/B 对局数（样本量说明） | m2-ab |
| `metrics.software.llm_ab_budget_gate_hits` / `llm_ab_fallback_count` | 预算闸触发与失败回退次数——「预算闸与回退生效证据」验收的量化物证 | m2-ab |
| `metrics.software.iteration_gate_log` | m2 每项增强的过闸记录（假设 → 矩阵证据 → 合入结论），迭代可追溯台账 | m2-full（合入纪律） |
| `metrics.software.online_ladder_games` / `online_skill_rating` | 天梯反馈回填（人工记录转录；未发生时如实 null） | man-submit |
| `metrics.software.online_feedback_calibration` | 天梯反馈触发的对手池校准动作记录（替换 / 引入了谁），线上标定闭环证据 | man-submit / m2-full |

### m3（终交锁定）

| 键 | 用途（一句） | 验收对齐 |
|---|---|---|
| `metrics.software.final_submission_commits` | 终交锁定的最近 2 份提交 commit hash——man-final 台账对账与报告收官记录 | man-final |

## C. 变更纪律

- B 组键属软件-文档接口扩展：由 software 侧在 `exports/schema.json` 同步新增字段并 bump `schema_version`，经 document 侧确认后本清单随之更新（文档不单方面造键）。
- 报告引用规则：A 组键 m0 后可引用；B 组键其所属里程碑收口后方可引用；一律标注键名，未落盘不引用。
