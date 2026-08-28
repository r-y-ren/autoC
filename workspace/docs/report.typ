// Kaggriculture 战役方案报告（Typst）｜结构：通用六节科技报告（封面/摘要/方法/实现/实验结果/结论与展望）+ 附录
// 铁律：本报告中一切性能数字只引 workspace/metrics.json 的 `metrics.software.<键>`，表注标键名；
//       赛事事实引 kb/competitions/kaggle-kaggriculture/meta.md（官方直抓，2026-08-28，带 URL）；
//       禁编造/换算 metrics 中不存在的数字（如倍率、未测项的估计值）。
#set page(paper: "a4", margin: 2.2cm)
#set text(lang: "zh", region: "cn", size: 11pt, font: ("Libertinus Serif", "Microsoft YaHei"))
#set heading(numbering: "1.1")
#set par(justify: true, leading: 0.85em)
#show heading.where(level: 1): it => { v(0.6em); it; v(0.3em) }

// ───────────────────────── 封面 ─────────────────────────
#align(center)[
  #v(1.2em)
  #text(size: 20pt, weight: "bold")[Kaggriculture 农场博弈 Agent 方案报告]
  #v(0.5em)
  #text(size: 12pt)[Kaggle Simulation Competition「Kaggriculture」（Google 自办）· apply 模式]
  #v(0.3em)
  #text(size: 11pt)[队伍单账号提交（3 人，团队上限 5 人内） · 2026-08-28]
  #v(0.3em)
  #text(size: 10pt, fill: gray)[本地评估基于官方引擎 kaggle-environments 1.32.7（vendored，引擎代码未改动）；线上天梯指标未测（见 §5.1）]
]
#v(0.8em)

= 摘要

本报告是 Kaggle Simulation Competition「Kaggriculture」战役（终交 2026-09-30）的方案报告。赛事为 720 回合（30 游戏日 × 24 回合）双人对局农场经营博弈，以赛季末银行存款定胜负，Elo 式天梯排位、终局 Bradley-Terry 锦标赛定榜（官方 Evaluation 页，2026-08-28 直抓）。

技术上采用三段式路线：启发式基线先行 → 本地评估基建（gym 化封装、对手池、Elo 评级、复盘日志）→ 增强模块 A/B（LLM 可插拔决策接口，默认关闭）。全部工程产物在官方引擎（PyPI `kaggle-environments` 1.32.7，本仓 vendored 重打包、引擎代码未改动）上完成本地实测：

- 测试套件 45/45 通过（`metrics.software.tests_total` / `tests_passed`），冒烟自检通过（`smoke_boot_pass`）；
- 全量评估 40 局完整对局（`eval_games_total`），总耗时 110.19 s（`eval_runtime_seconds`），平均 2.729 s/局（`avg_episode_runtime_seconds`）；
- 提交 bot 参与 24 局（`submission_games_played`）：对弱对手池胜率 1.0（`submission_win_rate_vs_pool`，16W-0L-0T）、对基线头对头胜率 1.0（`submission_win_rate_vs_baseline`，8W-0L-0T）；
- Elo（k=32）：提交 bot 1460.9 居首（`elo_ratings`）；终局资金均值 30548.5（`submission_avg_final_money`）。

边界如实声明：对手池偏弱（最强对手本地 Elo 1162.2，`elo_ratings`），未做 Kaggle 线上提交，线上指标（`online_ladder_games` / `online_skill_rating`）与 LLM A/B（`llm_ab_win_rate`）均为 null（未测）。合规方面本赛 AI 政策为全库最宽松一档（apply 模式），本作品的外部依赖、LLM 使用与单账号纪律逐条映射见附录 A；人机分工留痕见附录 B。配套提交 SOP 见 `workspace/docs/submit-sop.md`。

= 方法

== 战役定位与选型依据

本战役由用户闸门指定为主攻（2026-08-28 决策变更：报名门槛高的赛事后置，`workspace/strategy.md`），核心依据：

- *时间窗*：2026-07-29 开赛 → 09-30 终交（官方 Timeline 页直抓），33 天处于「2--10 周」投入最优区；收官后可无缝接力备选赛 RSNA（10-22 终交），构成一鱼多吃主线。
- *技术契合*：agent 仿真博弈方向与本仓知识库技术卡群直接对口——UrbanGround（`arxiv-2608.27456`）的城市 agent 沙盒评测方法论与失败模式清单迁移为本地评估基建；CaSKG（`arxiv-2608.25500`）技能检索思想用于策略库组织；ProgRouter（`arxiv-2608.25992`）质量-成本路由与 Bayesian Self-Escalation（`arxiv-2608.24087`）用于 LLM 调用的回合预算控制。
- *合规成本*：AI 政策全库最宽松（外部数据/模型默认允许、LLM 按费用合理性标准放行、数据 Apache 2.0、获奖 CC-BY 4.0，官方 rules 2026-08-28 直抓），apply 模式成立。
- *如实降权项*：该赛首届未放榜、无获奖模式样本（patterns 库 coverage 为空）；队内无 RL/博弈竞赛实绩。策略上以启发式基线先行 + 全程量化评估对冲，09-15 设切换 RSNA 决策点兜底。

== 博弈机制量化摘要

赛制与评分（官方 How-to-Play / Evaluation / rules 直抓，经 `kb/competitions/kaggle-kaggriculture/meta.md` 转引，访问日期 2026-08-28，URL 见附录 C）：

- *对局形态*：两名玩家各自经营农场 30 个游戏日（每日 24 回合，共 720 回合），赛季结束*银行存款多者胜*；官方定位其为「现实供应链、动态定价与不确定下资源分配」的沙盒（agentic RL 风向标赛事）。
- *评分机制*：Elo 式天梯（只看胜负平，净胜金币数不影响评分）；终交后约两周继续跑对局降方差，最终以 Bradley-Terry 锦标赛定榜；Simulation 赛*无 Private Leaderboard*。
- *提交机制*：每日至多 5 次提交，仅*最近 2 次*提交被跟踪并用于最终评估；提交须先通过 Validation Episode（自博弈跑通校验）。

机制红线（How-to-Play 直抓，工程侧固化为红线检查表 `kgenv/redlines.py`）：作物两天不浇水变杂草（产出清零）；动物两天不喂（小麦）逃跑不可找回（投资全损）；番茄/草莓为有限次产出（4 次）后衰败；西瓜加肥 8 天达产上限。产出-占用效率序列（官方表，经 patterns 库转引）：蛋 1.00 > 小麦 0.80 > 胡萝卜 0.75 > 奶 0.50（Yield/tile/day 口径）。市场为动态市场：价格对自身出货量与小镇需求作出反应，倾销存在砸价风险。

上述机制经工程侧量化为可执行模型（收益模型 `kgenv/economy.py`：价格曲线/作物周期/动物产出/雇佣/地价），并对照官方价格表逐项断言（纳入 45 项测试，见 §4）。

== 三段式技术路线

*阶段一：启发式基线*。`kaggle_simulations/agent/main.py` 为官方 kit 结构的自包含 bot（stdlib-only，提交形态不依赖任何外部模型），策略为「鹅引擎 + 瓜波段」三段式（机制全部来自官方 How-to-Play/engine 源码，详见 `workspace/software/README.md`）：近区建 coop 养鹅（每日 FEED/CARE/COLLECT_FERTILIZER 的蛋与肥料现金流）、第 0--2 天西瓜进窗口期按价格闸门分批出货、剩余格小麦基座自给鹅粮，配合晨间按负载雇佣、资金闸门买地，以及第 28--29 天的终局清算调度（银行存款为唯一计分项）。

*阶段二：评估基建*。官方引擎单局对局器（`kgenv/engine.py`，结构化结果与每日资金曲线）、gym 风格封装（`kgenv/gym_env.py`，可插拔对手）、对手池（pass / random / starter / greedy_carrot / baseline_wheat）、Elo 评级（`kgenv/elo.py`，只按胜负平，对齐官方天梯语义）与逐局复盘日志。方法论迁移自 UrbanGround（`arxiv-2608.27456`）：先规则基线后增强、每步迭代以本地评估器量化对比为据。

*阶段三：增强 A/B*。LLM 可插拔决策接口（`kgenv/bots/llm_provider.py`）：默认 `NullProvider`（关闭），启用需显式环境变量（`OpenAICompatProvider`）；内置调用次数与时长预算闸（Reasonableness Standard 的机械化落地，参照 ProgRouter 成本路由与 Bayesian Self-Escalation 思路），任何失败/超时回退启发式决策、绝不阻塞回合。提交形态 `LLM_PROVIDER=None` 默认关闭，不依赖任何外部模型。

= 实现

== 工程结构

交付物位于 `workspace/software/`：可提交 bot（`kaggle_simulations/agent/main.py`，官方部署路径）、本地评估包 `kgenv/`（engine / gym_env / economy / redlines / elo / arena / bots）、评估入口 `scripts/run_eval.py`、冒烟自检 `smoke_boot.py`、测试套件 `tests/`、接口导出 `exports/`（schema.json + eval_results.json + logs/replay_log.jsonl）、锁定依赖 `requirements.txt` 与 vendor wheel。

*引擎边界声明*：本地对局运行在官方引擎上——PyPI `kaggle-environments` 1.32.7 的 `kaggriculture` 场景（本仓 vendor 了去依赖元数据、去可视化资源的重打包 wheel，引擎代码未改动，出处与重打包细节见 `workspace/software/vendor/WHEEL_PROVENANCE.md`；上游 Apache-2.0，重分发合规）。本地评估结果代表官方规则语义，但*不等价于* Kaggle 线上天梯（对手分布不同、未做线上提交）。

== 一键命令（仓库根执行）

```bash
python -m pip install -q -r workspace/software/requirements.txt   # 依赖安装（锁定）
python workspace/software/smoke_boot.py                            # 冒烟自检（exit 0 判定）
python -m pytest workspace/software/tests -q                       # 测试套件
python workspace/software/scripts/run_eval.py --rounds 4           # 全量评估（40 局）+ Elo + exports
```

测试覆盖：收益模型对照官方价格表逐项断言、机制红线检查、agent 接口契约、对局器与 Elo（实测 45 项全过，`metrics.software.tests_total` / `tests_passed`）。

== 软件-文档接口契约

评估产出按 `workspace/software/exports/schema.json`（draft 2020-12 JSON Schema）落盘为 `eval_results.json`（40 局逐局记录 + head-to-head + Elo 表）与逐局复盘日志，供本报告与后续迭代引用；顶层汇总指标汇入 `workspace/metrics.json`，本报告全部性能数字即引自该文件的 `software` 分片。

= 实验结果

全部数字引自 `workspace/metrics.json`（实测日期 2026-08-28，键名标注于各表），未做任何换算或估计。

== 评估设置与运行时

#table(
  columns: (2.4fr, 1fr, 0.9fr, 1.9fr),
  align: (x, y) => (if x == 0 { left } else { center }) + horizon,
  table.header([*指标*], [*数值*], [*单位*], [*metrics 键*]),
  [全量评估对局总数], [40], [games], [`eval_games_total`],
  [评估总耗时], [110.19], [s], [`eval_runtime_seconds`],
  [平均单局耗时], [2.729], [s/game], [`avg_episode_runtime_seconds`],
  [平均单局回合数（全长度对局）], [720.0], [turns], [`avg_turns_per_game`],
  [冒烟自检耗时], [3.2], [s], [`smoke_boot_runtime_seconds`],
)
#text(size: 9pt, fill: gray)[表注：评估矩阵为 2 主打 × 4 对手 × 4 种子 + 8 局头对头（`eval_games_total` 方法域原文）；引擎 kaggle-environments 1.32.7+nodeps（vendored），场景 kaggriculture，720 回合/局（`engine.version` / `engine.scenario` / `engine.episode_steps`）。]

== 胜率与 Elo

#table(
  columns: (2.4fr, 1.2fr, 2.6fr),
  align: (x, y) => (if x == 0 { left } else { center }) + horizon,
  table.header([*指标*], [*数值*], [*metrics 键*]),
  [提交 bot 参与对局数], [24], [`submission_games_played`],
  [对弱对手池胜率], [1.0], [`submission_win_rate_vs_pool`],
  [对基线头对头胜率], [1.0], [`submission_win_rate_vs_baseline`],
)
#text(size: 9pt, fill: gray)[表注：胜率 1.0 的方法域原文——vs 池 16W-0L-0T（pass/random/starter/greedy_carrot 各 4 种子）；vs `baseline_wheat` 8W-0L-0T（seeds 101--104, 601--604）。]

#table(
  columns: (1fr, 1fr),
  align: center + horizon,
  table.header([*bot*], [*Elo 评级*]),
  [submission（提交 bot）], [1460.9],
  [baseline_wheat], [1245.8],
  [greedy_carrot], [1162.2],
  [starter], [1122.9],
  [random], [1111.2],
  [pass], [1097.0],
)
#text(size: 9pt, fill: gray)[表注：`elo_ratings`——EloTable k=32、初始 1200，基于 40 局记录、只按胜负平（对齐官方天梯语义），方法域原文见该键。]

== 终局资金 A/B

#table(
  columns: (2.9fr, 1.3fr, 2.6fr),
  align: (x, y) => (if x == 0 { left } else { center }) + horizon,
  table.header([*指标*], [*均值（coins）*], [*metrics 键*]),
  [提交 bot 全部 24 局终局资金均值], [30548.5], [`submission_avg_final_money`],
  [提交 bot 头对头 8 局终局资金均值], [29325.13], [`submission_avg_final_money_h2h`],
  [基线 `baseline_wheat` 同 8 局头对头终局资金均值], [11475.25], [`baseline_wheat_avg_final_money_vs_submission`],
)
#text(size: 9pt, fill: gray)[表注：三项均为 metrics.json 原值并列呈现，倍率等派生数字不在此列（数字纪律：不换算 metrics 之外的值）。]

== 测试与未测项

#table(
  columns: (2.4fr, 1.2fr, 2.6fr),
  align: (x, y) => (if x == 0 { left } else { center }) + horizon,
  table.header([*指标*], [*数值*], [*metrics 键*]),
  [测试套件总数 / 通过数], [45 / 45], [`tests_total` / `tests_passed`],
  [冒烟自检通过], [true（exit 0）], [`smoke_boot_pass`],
)
#text(size: 9pt, fill: gray)[表注：测试方法域原文——`python -m pytest workspace/software/tests -q`（2026-08-28，45 passed 0 failed）。]

*未测项（metrics.unmeasured，如实呈现为 null，不做估计）*：

#table(
  columns: (2.2fr, 0.9fr, 3.1fr),
  align: (x, y) => (if x == 0 { left } else { center }) + horizon,
  table.header([*指标*], [*数值*], [*状态说明（metrics 原文转述）*]),
  [`llm_ab_win_rate`], [null], [LLM provider 默认关闭（NullProvider），未跑 LLM 对局，不主张任何 LLM 收益数字],
  [`online_ladder_games`], [null], [未做 Kaggle 线上提交（队伍人工步骤，蓝图 man-submit）],
  [`online_skill_rating`], [null], [依赖线上提交，待天梯反馈],
)

= 结论与展望

== 边界与遗留

- *对手池强度声明*：本地对手池为 pass / random / starter / greedy_carrot（最强者本地 Elo 1162.2，`elo_ratings`），整体弱于天梯真实分布；24 胜 0 负与 Elo 1460.9 为*本地池内结论*，不可外推为线上排名（天梯另有高方差特性，官方以持续对局 + Bradley-Terry 锦标赛降方差定榜）。
- *LLM 模块默认关*：提交形态不依赖外部模型；`llm_ab_win_rate` 为 null（未测）。启用属可选项且受预算闸约束（附录 A）。
- *线上指标待补*：`online_ladder_games` / `online_skill_rating` 均为 null，待队伍按 SOP 完成首轮线上提交后回填。
- *引擎版本边界*：本地为官方 1.32.7；若 Kaggle 线上 kit 升级机制，需以官方页面直抓为准复核（software 侧已声明）。
- *硬时点风险*：entry_deadline 官方数值缺失（API Timeline 模板变量未解析）——SOP 第 0 天人工核对赛站并尽早完成报名。

== 展望

近期（至 09-30 终交）：按 SOP 完成报名核对与首轮线上提交，以天梯反馈校准本地对手池（替换为线上同类评级 bot），继续增强迭代并在 09-15 做主攻/备选（RSNA）投入产出比裁决；终交前执行检查单（最近 2 份提交为最优版本）。中期：本地评估基建（gym 封装 + Elo + 复盘日志）为通用资产，可直接复用于 RSNA 的实验管理支线与后续 agent 类赛事。

#pagebreak()

= 附录 A：AI 使用与合规声明（apply 模式必附件）

本节依据赛事 rules（2026-08-28 经 Kaggle 官方 ListPages API 直抓，URL 见附录 C）逐条映射本作品实际用法。

#table(
  columns: (1.7fr, 2.6fr, 0.9fr),
  align: horizon,
  table.header([*官方政策条款（rules 直抓）*], [*本作品实际用法*], [*判定*]),
  [外部数据与模型允许："The use of external data and models is acceptable unless specifically prohibited by the Host."],
  [外部依赖仅官方引擎 `kaggle-environments` 1.32.7（上游 Apache-2.0；本仓 vendor 重打包仅去依赖元数据与可视化资源，引擎代码未改动，出处 `vendor/WHEEL_PROVENANCE.md`，重分发附署名合规）。提交形态 bot 为 stdlib-only、自包含，不使用任何外部数据集或外部模型。],
  [符合],
  [LLM 费用按 Reasonableness Standard 放行："a small subscription charge to use additional elements of a large language model such as Gemini Advanced are acceptable if meeting the Reasonableness Standard."],
  [LLM 决策模块为可插拔接口（`kgenv/bots/llm_provider.py`），*默认 NullProvider 关闭*，启用须显式配置环境变量；内置调用次数与时长预算闸，任何失败/超时回退启发式、不阻塞回合。A/B 未跑（`llm_ab_win_rate` = null），不主张 LLM 收益。],
  [符合（保守启用）],
  [AMLT 放行："Individual Participants and Teams may use automated machine learning tool(s) ('AMLT') ... provided that ... they have an appropriate license."],
  [未使用 AutoML 工具链。本作品按「AI 辅助原创」标准产出：AI 辅助生成代码与文档草稿，队伍主导迭代与裁决（人机分工见附录 B）。],
  [符合],
  [单账号纪律："You cannot sign up to Kaggle from multiple accounts and therefore you cannot enter or submit from multiple accounts."],
  [队伍 3 人（团队上限 5 人内），单一 Kaggle 账号报名与提交；SOP 内嵌防多账号检查项。],
  [符合],
  [数据许可 Apache 2.0（"You may access and use the Competition Data for any purpose, whether commercial or non-commercial"）；获奖许可 CC-BY 4.0（Winner License Type）],
  [仅使用竞赛提供的官方引擎与规则文本；知悉获奖情形下方案按 CC-BY 4.0 开源的义务。],
  [符合],
  [提交纪律：每日至多 5 次提交，仅最近 2 次计入最终评估；提交先过 Validation Episode],
  [配套《提交 SOP》（`workspace/docs/submit-sop.md`）：提交前本地回归（冒烟 + 测试 + 40 局评估）、每日提交节奏约束、终交前检查单（09-30）。],
  [符合（流程保障）],
)

补充说明：未见任何「禁用 LLM/生成式 AI」条款；本赛目标即 agentic AI（官方 abstract："design, build, and deploy an autonomous AI agent"）。API 型 LLM 在 Kaggle 仿真容器内是否可用取决于容器网络策略（官方页未载明，列待核，本作品不依赖）。

= 附录 B：人机分工记录（合规留痕）

本作品由 AI 辅助生成、队伍主导迭代，按「AI 辅助原创」标准产出并在归档时保留本记录。

#table(
  columns: (1.4fr, 2.4fr, 2.2fr),
  align: horizon,
  table.header([*环节*], [*AI（autoC 框架，GLM-5.3 驱动）*], [*人工（队伍）*]),
  [情报与决策支持], [KB 收集与赛道矩阵草拟（来源可溯）], [赛道裁决（用户闸门指定主攻、切换决策点）],
  [机制量化], [收益模型/红线检查表实现与单测], [机制关键参数对照官方页复核],
  [bot 与评估基建], [bot、评估器、测试、评估脚本实现与执行], [结果审读、迭代方向与提交版本裁决],
  [线上提交], [不执行（蓝图 man-reg / man-submit 列人工）], [Kaggle 报名、提交操作、天梯观察与记录],
  [文档], [本报告与 SOP 草拟（数字仅引 metrics）], [定稿审读与签字确认],
)

= 附录 C：参考来源

赛事事实（赛程/奖金/AI 政策/机制）均来自以下官方直抓信源（访问/抓取日期 2026-08-28），经 `kb/competitions/kaggle-kaggriculture/meta.md` 与 `patterns.md` 转引：

- Kaggle 官方 ListPages API（competitionId=147734）：rules / Prizes / Timeline / Evaluation / How to Play / Foundational Rules 全文——#link("https://www.kaggle.com/api/i/competitions.PageService/ListPages?competitionId=147734")[kaggle.com/api/i/competitions.PageService/ListPages?competitionId=147734]（2026-08-28）
- 赛站：#link("https://www.kaggle.com/competitions/kaggriculture")[kaggle.com/competitions/kaggriculture]（2026-08-28）
- 本仓知识库技术卡：`arxiv-2608.27456`（UrbanGround，评测方法论）、`arxiv-2608.25500`（CaSKG，技能检索）、`arxiv-2608.25992`（ProgRouter，成本路由）、`arxiv-2608.24087`（Bayesian Self-Escalation）
- 工程产物与实测数据：`workspace/software/README.md`、`workspace/software/exports/schema.json`、`workspace/software/exports/eval_results.json`、`workspace/metrics.json`（全部性能数字的唯一来源，实测日期 2026-08-28）

奖金口径备注：官方 rules §5 与 Prizes 页双处直抓「TOTAL PRIZES AVAILABLE: \$50,000」（1st--10th 各 \$5,000）为当前采信口径；列表页 \$60,000 口径未获官方页证实，双口径并存待核（meta.md 待核清单）。
