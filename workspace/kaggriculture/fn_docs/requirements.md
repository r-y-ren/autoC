# 需求文档：kaggriculture 战役工程库重构（fn_work/ 重建）

> fn-refactor 阶段三产物（2026-09-21，三轮裁决完成）。上游：behavior_inventory.md（G1-G24）+ gap_table.md。本文是 fn-divide 及后续阶段的唯一需求依据；行为基线=fn_docs/README.md v1 + 行为清单 §1-6。

## 根本目的

把 26 轮战役积累的 workspace/kaggressulture/ 工程变成**赛后可持续维护、可交接、fresh clone 可复算核心门禁**的代码库。成功标准三条：

1. 全部保留行为在新结构下不变（阶段四快照安全网对旧代码跑绿后，对新结构同样跑绿）；
2. 已裁决缺陷在新结构中修复（验收=快照反例：旧代码失败、新代码通过）；
3. 可维护性达成（单源名册/路径变量化/死码清零/文档与代码一致/最小可复算集入库）。

## 环境与技术栈决策（用户裁决 2026-09-21）

| 项 | 决策 |
|---|---|
| 语言/运行时 | Python **3.14 钉死**（与线上提交、active_candidate 一致） |
| 测试框架 | pytest 延续（requirements.txt 锁定 9.1.1） |
| 提交 bot 依赖 | **stdlib-only 不变**（离线自主运行） |
| 评估/脚本侧依赖 | vendored wheel（kaggle_environments 1.32.7）+ locked requirements |
| 错误处理风格 | 沿用现役语义：bot 内 fail-open 三道；评估/台账链 fail-closed |
| 日志方式 | 沿用遥测影子（进程内）+ 台账 JSON（exports/） |

## 术语表

| 术语 | 精确定义 |
|---|---|
| 席位（seat） | 一局对局中的两个玩家槽位（seat0/seat1）；评估必须显式声明我方在哪个席位 |
| 席位错位 | 评估 harness 把"我方动作"恒注入 seat0 的缺陷——me_seat=1 局的数字全为伪影 |
| seated rollout | 显式按 me_seat 注入双方动作的正确回放推演（参照实现 v143_sellrace_gates.py:91-116） |
| 快照反例 | 能让**旧代码失败、新代码通过**的构造用例——缺陷修复条目的验收方式 |
| 双口径 | 同一评估的两个数字口径（如 错位口径历史值 vs seated 口径重算值）并列留档 |
| 旗关等价 | PLANNER_ENABLED=False 时与基线行为逐字节一致（黄金哈希验证） |
| 冻结面 | 终局窗口内零字节变更的旧树（现役提交链+验收引用路径+工件） |
| 最小可复算集 | 保证 fresh clone 跑通核心门禁与快照测试的最小数据入库集 |
| 双源归源 | 同一字节存在两个公开来源时，血统记录并列两源（作者/日期/许可现状），归属标未定 |
| active/dormant/dead/one-off | 行为状态四分类（见 behavior_inventory.md 图例） |

## 需求条目

### R1 行为基线保持（G-基线） [P0]
- 内容：行为清单 §1-6 全部 active 件的行为在新结构中不变（四层决策链、DTSP 全链、fail-open 三道、旗关等价、身份链、评估契约族、线上台账门、取证画像管线、语料完整性、对手认证门、活性门等）。
- 验收方式：阶段四建立的 characterization 快照测试对旧代码跑绿后，对新结构逐字节/逐键跑绿；旗关等价黄金哈希在新结构复验一致。

### R2 席位正确的 rollout 通道（G1） [P0]
- 内容：seated rollout（v143:91-116 参照实现）上提为 planner_offline_bench 唯一通道，8 处错位内联全部替换；受影响历史结论（v3 复裁 b/c、v48+ 巨人门等）以双口径重算留档。
- 验收方式：快照反例——构造 me_seat=1 注入局，旧 bench 输出与 seated 口径不一致（旧失败），新结构输出与 seated 口径一致（新通过）；重算台账落 fn_docs。

### R3 trimmed_mean 值序裁切（G2） [P0]
- 内容：select.py:42 聚合改按值序裁切，悲观模型在投影段恢复效力；v31_pressure_calibration 标注"仅 ref b4aeafb 语义成立"。
- 验收方式：快照反例——Ω=4 分数集构造名字序与值序裁切结果不同的用例，旧代码失败/新代码通过；投影段含悲观模型时聚合值改变的断言测试。

### R4 双源血统记录（G4） [P0]
- 内容：dadee25a（v48 衍生，在跑线上资产 ref 56400478）血统统一为双源：kaitofukami（2026-08-31 首拉，无显式许可）+ ahmedberatozer（2026-09-20 拉回，v48plus README 记录），原创归属标"两账号间未定"；对外引用不再单源断言。
- 验收方式：fn_docs 血统记录存在且含两源作者/日期/sha/许可现状/未定声明；全库 grep 无单源断言残留（opponents/PROVENANCE.md 与 v48plus/README.md 的物理统一随新结构落地，旧树战后改）。

### R5 第二引擎指纹看护（G5） [P0]
- 内容：replay_profile.py 内嵌 ~1050 行手写引擎复算加指纹看护（对 wheel 版本 sha 断言）或改走 twin.py 通道复算。
- 验收方式：篡改引擎常量/换 wheel 版本时看护测试变红；正常则绿。

### R6 测试基线机器无关（G6） [P0]
- 内容：索引/打包工件 LF 重建；Windows-only 断言（normcase、Path.is_absolute）改双平台兼容；基线声明机器语境（"990+2 仅主力机"历史口径与通用口径并列）。仓外 .gitattributes 不可加（范围外），靠测试双兼容。
- 验收方式：fresh Linux clone 上 0 个环境性失败（数据依赖项显式 skip 并标注缺什么）；同 commit 在 Windows 主力机基线不回退。

### R7 bc_track 文档与票账修正（G7） [P1]
- 内容：README 复现命令路径修正；issues/03/08 票面状态与 JOURNAL 对齐（03 弃牌、08 关账、04-07 标未触发关闭）。
- 验收方式：复现命令逐条可 cd；票面状态与 JOURNAL 台账一致。

### R8 校验器与对手名册单源（G10） [P0]
- 内容：异常局判定（arena._abnormal_reason vs eval_contract.game_abnormal_reason）合并单源；对手名册 5 处常量 + check_eval_contract REQUIRED_OPPONENTS 网格收敛为单一来源。
- 验收方式：单点定义、多处引用的 import 断言测试；改一处名册全链生效的一致性测试。

### R9 bots 常量看护（G11） [P0]
- 内容：kgenv/bots/ 五文件手抄 CROPS_INFO/ANIMALS_INFO 增加对 vendored wheel 常量的交叉校验测试。
- 验收方式：篡改任一常量测试变红。

### R10 死码清除（G12） [P0]
- 内容：9 处死码不进新结构（_two_opt_segment、_note_buys、V9_TOUR_BONUS/DECAY、_schedule_units 与 _dawn_crew_size 及其测试、WEED_RECLAIM=="all" 支、wave 死旋钮 WAVE_OPENING_EOD_CASH_MAX 与 WHEAT 死种子、_hands_target 11/12 死档、_SELLRACE_SHIP 死支）；stage_* 四键显式化为"保留轴"并在文档标注（不静默丢弃）。
- 验收方式：快照安全网全绿（行为不变）；上述符号在新结构 grep 零命中。

### R11 脚本三档分层（G13+G3） [P0]
- 内容：保留档（twin_fidelity、planner_flagoff_golden、v48_derivative_launch_check、v48plus_launch_check、p41_official_load_probe）；工具箱档（m4_switchover_regression --golden-only、solver_shadow_stats、sprintA_structure_probe）；归档档（round23×4、round24×3、v15×3、v143（seated 实现吸收进 R2 后）、v3、v31、planner_calibration_suite、v48plus_ab_gate/layer_ablation、v48plus_metrics、profile_v48_gap）。
- 验收方式：归档件不在主线 import 路径（grep 断言）；保留档逐件可跑（--help 或 smoke）；v143 归档前置条件=R2 完成并有吸收留痕。

### R12 大证据件归档（G14） [P1]
- 内容：bc_track/models/ 416KB 权重件移入证据归档区，不进新结构代码面。
- 验收方式：新结构代码树 grep 零命中；归档区清单登记。

### R13 半休眠件降级（G15） [P1]
- 内容：gym_env（仅冒烟续命）与 bots/llm_provider（实验件默认关）移出主线依赖，标记 dormant 实验区。
- 验收方式：主线 import 图不含两者；冒烟路径显式引用实验区。

### R14 评估链孤儿降级（G16） [P1]
- 内容：economy.py、redlines.py 降级为纯测试资产/语义对照面，README 与 CODEMAP 陈述同步修正。
- 验收方式：评估链主线 import 图不含两者；文档矛盾清零（对照 gap_table §一）。

### R15 market_ledger 归位（G17） [P1]
- 内容：库模块从 scripts/ 归位到 kgenv（或新结构等价库位）。
- 验收方式：scripts/ 无无入口库件（扫描断言）；import 链更新后全量测试绿。

### R16 文档一致性（G18+G19+G20） [P0]
- 内容：fn_docs/README v1 已按裁决回写（矛盾 8 处+补 10 项，本次完成）；CODEMAP 失准 4 处随新结构落地退役（fn_docs 已记勘误）；代码注释漂移 3 处（ANTICIPATED"已禁用"实为开、_decide_mode docstring 死门、main"九模块"）在新结构中修正。
- 验收方式：gap_table §一清单逐项对账清零；新结构注释与行为一致（抽查断言或评审）。

### R17 治理留档与降级（G9+G21） [P1]
- 内容：蓝图 2 条失效验收 cmd（docs/report.typ、check_report_metrics.py 不存在）在 fn_docs 留失效声明，战后随 /attack 修订蓝图一并处置；active_candidate.json 战后降级为历史台账（不现在补记，避免动在役身份链）。
- 验收方式：fn_docs 处置记录存在；终局收口（09-29/30）后再执行降级动作。

### R18 probes 入库策略统一（G22） [P1]
- 内容：exports/probes 规则显式化——结论 .md 全入库、数据中间物留 gitignore，与其余子目录策略统一表述。
- 验收方式：策略写入新结构 README/数据面文档；现存 6 份强制入库摘要与规则一致。

### R19 最小可复算集入库（G23） [P0]
- 内容：flagoff golden JSON、round23 灾难局回放（ep110634204）、孪生保真抽样语料 manifest+样例、对手池种子定义入库；其余 ~GB 原始语料本机保存+清单声明（哪些结论依赖主力机语料）。
- 验收方式：fresh clone + 最小集即可跑通：flagoff 等价黄金复验、灾难局接合证明、孪生保真 smoke、快照安全网全量；体积预算（单件与总量上限在 fn-divide 定桩时明确）。

### R20 路径变量化（G24） [P0]
- 内容：新结构内以单一根发现函数/常量取代字面路径；消除"仓根 CWD 假设"（114+ 处现行引用与三代并存路径不再扩散）；蓝图验收命令路径属旧树契约，战后随蓝图修订退役。
- 验收方式：新结构树 grep `workspace/kag` 字面路径零命中（豁免：旧树对接适配层、fn_docs 记录）；从任意 CWD 运行测试与门禁均通过。

## 非功能约束

| 约束 | 判据 |
|---|---|
| 确定性 | 同 obs 同动作（无集合迭代序依赖）；打包双次构建逐字节一致 |
| D14 圈禁 | 一切重构产物只落 workspace/kaggressulture/ 内（含 fn_work/、snapshot_tests/） |
| 仓外零改动 | 不碰 campaign 目录外任何文件（含仓根 .gitattributes） |
| 终局隔离 | 09-30 收口前旧树零字节变更；线上提交序列与终榜对不受重构影响 |
| 体积纪律 | 大数据不进 git 主线（R12/R19 体积预算） |

## 外部依赖

| 依赖 | 用途与边界 |
|---|---|
| vendored kaggle_environments 1.32.7 wheel | 引擎真源；升版会断 4 处直耦合+replay_profile（须先过 R5 看护） |
| pytest 9.1.1（locked） | 测试框架 |
| kaggle CLI | 线上台账件（sync_online_probe/forensic_harvest）运行前提；战后停摆件保留可跑 |
| gitignored 语料 | R19 最小集转入库；其余本机保存+依赖声明 |

## 范围外（含全部丢弃项与理由）

1. **终局窗口内旧树零变更**（09-30 收口前，含文档与工件——用户裁决五条之一）；
2. **campaign 目录外零改动**（含仓根配置）；
3. **蓝图不改**（2 条失效 cmd 战后经 /attack；本轮只在 fn_docs 留失效声明）；
4. **线上提交序列不受重构影响**（终榜对={v14.2, v48 衍生}与 09-29/30 收口不动）；
5. **G9/G21 的物理处置不在本轮**（active_candidate 补记/降级、蓝图修订=战后）；
6. **丢弃项**（理由：dead 不可达/零触发或 one-off 已完成使命，行为基线不含它们）：
   - 提交链死码 9 处（R10 清单）；
   - 归档档脚本 ~19 件（R11 清单）——理由：单次法证已完成裁决并留痕 JOURNAL/digests，可复跑价值由保留档与工具箱档承接；
   - bc models 权重件（自动生成物，结论已在 metrics/issues 留痕）；
   - gym_env/llm_provider 主线地位（降级不删除）、economy/redlines 评估链地位（降级为测试资产）；
   - wave 死旋钮/死种子、_hands_target 死档、stage_* 保留轴显式化（不丢轴、丢死值）。

## 变更记录

| 日期 | 变更 | 原因 |
|---|---|---|
| 2026-09-21 | 初版：三轮裁决（G1-G24 全按推荐；环境 3.14+pytest+stdlib；范围外五条确认；active 全保留为基线） | fn-refactor 阶段三完成 |
| 2026-09-21 | G8 当下动作已执行：merge_metrics 重跑，root=分片逐键一致（software 3438 叶子键，_generated_at 2026-09-21T19:48:44） | 裁决"跑 merge+留档" |
