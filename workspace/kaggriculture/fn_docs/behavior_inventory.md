# 行为清单（fn-refactor 阶段二产物）

> 2026-09-21，六分片并行只读审查汇总（A 提交链 / B kgenv / C 身份门禁评估脚本 / D Track-B 与线上工件 / E 测试与 bc_track / F 治理数据面）。旧代码零改动。
> 状态图例：active=在役｜dormant=开关关闭/仅测试续命｜dead=不可达/零触发｜one-off=单次历史件。
> **用途**：§0 裁决候选总表是阶段三（行为裁决 grill）的输入，逐条由用户裁决 保留/修复/丢弃。修复=写入新结构的需求数条目（旧代码验收前一字节不动，一切变更发生在 fn_work/ 重建时）。

## 0. 裁决候选总表（G1-G24，含推荐）

### 缺陷类（推荐=修复：作为新结构需求条目）

| # | 事项 | 证据锚 | 推荐 |
|---|---|---|---|
| G1 | **席位错位通道未回流**：planner_offline_bench.py:319 rollout_with_replay_opponent 恒 mine→seat0，me_seat=1 局数字全为伪影；内联同构扩散至 v3_readmission:98、v15_d0:61、v15_regression:103、v48plus_ab_gate:254、calibration:256/425、round23_engagement:58、round24_d0:55、round24_cf:88；**正确实现仅存 v143_sellrace_gates.py:91-116** | D/E 分片；session-findings 工程#5、遗留#2 | 修复（seated 版上提进 bench 并全面重算受影响历史数字） |
| G2 | **select.py:42 trimmed_mean 按名字序裁切**（悲观模型恒被裁=投影段折扣零效力）；连带 v31_pressure_calibration 在 HEAD 语义失效（其 value 档恢复的正是未修实现，只在 ref b4aeafb 成立=复现性陷阱） | A/D 分片；session-findings 工程#6、遗留#4 | 修复（值序裁切；v31 加 ref 标注） |
| G3 | profile_v48_gap.py 路径双拼损坏（REPO_ROOT 再拼 workspace/… → workspace/workspace/…，必崩）；CODEMAP 标"在役"不实 | D 分片 | 修复或归档 |
| G4 | **dadee25a 血统双 PROVENANCE 冲突**：opponents/PROVENANCE.md:7-15（kaitofukami、未附开源许可）vs v48plus/README.md:52-54（Ahmed Berat Ozer、Apache-2.0）；该字节衍生版=在跑线上资产（ref 56400478） | D 分片 | 修复（归源统一，合规链敏感） |
| G5 | **replay_profile.py 内藏 ~1050 行手写第二引擎且无指纹看护**（:629-1685）：与 twin.py 的 fail-closed 指纹链形成对照，wheel 语义变更时静默漂移 | B 分片 | 修复（sha 断言或改走 twin 通道） |
| G6 | 测试基线机器依赖：本 Linux 机实测 976P/8F/8S 全环境性（CRLF 工件×3、gitignored 数据缺机×3、Windows-only 断言×2）；"990+2"仅在 Windows 主力机+数据在机成立 | E 分片 | 修复（LF 归一 + POSIX 断言修正 + 机器语境记录） |
| G7 | bc_track/README.md:10 复现命令路径拼错（kaggressure）；issues/08 票面已关账未回写、04-07 未标关闭 | E 分片 | 修复 |
| G8 | 根 metrics.json 落后 software 分片 14 键（bc_*、v48_derivative_launch 等未进权威面） | F 分片 | 修复（跑 merge_metrics + 补合并纪律） |
| G9 | 蓝图 2 条验收 cmd 指向不存在文件（docs/report.typ、docs/check_report_metrics.py）；/accept 链 09-01 后静默、m6/m7 无验收记录 | F 分片 | 处置受限（铁律禁改蓝图→战后经 /attack 修订或留档声明） |
| G10 | arena._abnormal_reason vs eval_contract.game_abnormal_reason 双校验器已分叉；对手池名册 5 处常量重复（bots/__init__×2、STANDARD_MATRIX_ORDER、regression.EXPECTED_ELO_ORDER、holdout_matrix_order）+ check_eval_contract REQUIRED_OPPONENTS 与 iterate_gate 池双维护 | B/C 分片 | 修复（合并到单一来源） |
| G11 | kgenv/bots/ 五文件手抄 CROPS_INFO/ANIMALS_INFO 零交叉校验（漂移会污染对手池强度标定） | B 分片 | 修复（对 wheel 常量断言） |

### 死码/归档类（推荐=丢弃/归档）

| # | 事项 | 推荐 |
|---|---|---|
| G12 | 提交链死代码簇：_two_opt_segment(solver:128)、_note_buys(market:216)、V9_TOUR_BONUS/DECAY(constants:500-501)、_schedule_units/_dawn_crew_size(仅测试)、WEED_RECLAIM=="all"支、stage_* 四键发射未接线(plans.py:803 显式保留轴)、WAVE_OPENING_EOD_CASH_MAX 零消费+WHEAT 种子死值(wave:50/199)、_hands_target 帽 10 使 11/12 死档(strategy:170-181)、_SELLRACE_SHIP 死支(main:102) | 丢弃（stage_* 若为保留轴则显式化） |
| G13 | 一次性法证脚本归档：C 族 9 件（quickwin_probe/kill_table/r3_trajectory_probe/probe_v9_wheat_gate/analyze_failure_modes/verify_milk_economics/sell_plan_reconciliation/observer_v0_validator/capacity_calibration）+ D 族 ~17 件（round23×4/round24×3/v15×3/v143/v3/v31/calibration/p41/v48plus_ab_gate/layer_ablation/metrics 等） | 归档（保留可复跑的 permanent-gate：twin_fidelity/flagoff_golden/v48 两 launch_check） |
| G14 | bc_track/models/ 416KB 权重证据件（自动生成物） | 归档为证据（不进新结构代码面） |
| G15 | gym_env（仅冒烟+5 测试续命）、bots/llm_provider（实验件默认关） | 降级 dormant 或移出主线 |
| G16 | economy.py / redlines.py 评估链孤儿（0 脚本消费；CODEMAP/docstring 两处陈述过期） | 降级纯测试资产或并入对照面 |
| G17 | market_ledger.py 是库模块误置 scripts/（无入口） | 归位 kgenv 或库目录 |

### 文档修正类（推荐=随阶段三裁决后统一回写）

| # | 事项 | 推荐 |
|---|---|---|
| G18 | README v0 修订：单文件自包含→多模块包、"九模块"→十模块、Elo"顺序无关"表述失准、红线清单实际无接线、对手血统库"四套解码版"实际入库仅 v48+v72、corpus 族与对手认证门未提及、活性门未提及 | 修订（清单见 gap_table §一） |
| G19 | CODEMAP 4 处失准（profile_v48_gap"在役"、economy"market.py 消费"、53→51 测试文件、opponents 清单） | 修正或随 fn_work 落地退役 |
| G20 | strategy.py:81-84/419-421 注释宣称 ANTICIPATED"已禁用"实为 True；_decide_mode docstring 列已删门；main.py 头注释"九模块"过期 | 新结构中修正（旧码不动） |

### 治理与数据归宿类

| # | 事项 | 推荐 |
|---|---|---|
| G21 | active_candidate.json 停在 v72 时代（online_submission_refs 空、v14.3 标 development），身份链权威名存实亡，实际以 JOURNAL+git 为准 | 降级历史台账或补记终局对 |
| G22 | exports/probes 混合入库策略（gitignore+6 份强制入库摘要）与其余子目录全入库不一致 | 统一策略 |
| G23 | 原始回放证据（references/data ~GB 语料、线上回放）gitignored：21/27 Track-B 脚本与 corpus/observer 族本机不可跑、8 skip 同因——fresh clone 不可复算画像与法证结论 | 数据归宿裁决（本机留存声明/小体积入库/接受不可复算） |
| G24 | 三代硬编码路径并存（workspace/software 旧布局 manifest×6、workspace/kaggressulture 现行 ~114 处、仓根 CWD 假设）；run_holdout 已付过双前缀兼容成本 | 新结构内路径变量化（fn-divide 取材） |

## 1. 分片 A：提交链 bot 本体（kaggle_simulations/agent/，18 文件全读）

| 行为 | 位置 | 状态 | 备注 |
|---|---|---|---|
| 薄装载：定位包根+无条件 sys.path.insert（P4.1 腰带）+exec 10 模块同 globals+重绑 agent 为最后 callable | main.py:1-52 | active | _MODULE_ORDER=10 模块（wave 加入后）；头注释"九模块"过期 |
| DTSP_RUNTIME_CONFIG（enabled/seed/0.85s 帽/悲观单模型/阶梯）+装载窗内急切 import planner.runtime | main.py:114-117 | active | P4.1 修复，tests/test_p41 把守 |
| agent() 编排：observer 旁路→DTSP 黎明钩子→宏计划→任务→四层求解→市场→雇工→排序（wave flush 先卖钩子）→预算截断 | entry.py:187 等 | active | 整体 try/except→PASS |
| fail-open 三道：entry 旗关+清寄存器 / runtime restore_pristine+sticky_off+记因 / 指纹不符走同通道 | entry.py:93-100、runtime.py:787 | active | 已知⑤属实 |
| 旋钮面 _plan_knob 旗关恒回默认（29+ 键，PLANNER_ENABLED=False=冻结值） | constants.py:770-778 | active | 已知③成立，黄金测试在场 |
| 观察器四通道日账（精确流发布/残差/钱账/tile）+est_* getter | observer.py | active | _opp_note_fills 仅离线 |
| L1 宏观：三模式+WHEAT_FARM 关+_plan_rollout 偿付门+阶段寄存器 P0-P5/d1/d6/d10/d14/d22/fuse/backfill+_field_alloc 分区轮作 | strategy.py | active | 注释漂移见 G20 |
| L2 任务包+末日清算+黎明影子包（D1-D4/deps/EOD/容量前馈/mission_hash） | mission.py:692 等 | active | |
| L3：EDF+价值密度+2-opt+载货腿+D1 兜尾+自适应 REPLAN | solver.py | active | _two_opt_segment/_dawn_crew_size/_schedule_units 死/测试件（G12） |
| L4：沿线执行+F4 跳过+D1/EOD 断言+幂等 REPLAN+d29 DROP→SELL | executor.py | active | |
| 市场层：引擎镜像定价/三门卖出/MK-3 批次/MK-5 载体/sellrace 前移（旗关）/买地饲料种子畜群四重门 | market.py | active | _note_buys 死 shim（G12） |
| 遥测影子+sink 注入，异常全吞 | telemetry.py | active(旁路) | |
| wave 波次日历剧本：全部消费点经 _plan_knob/globals() 钩子旗关零足迹，但 DTSP 每黎明恒排比较集首位（选中即激活） | wave.py、runtime.py:697 | dormant(线上可达) | 已知④修正：非纯休眠；死旋钮/死种子见 G12 |
| 黎明规划：预算治理→摘要→枚举≤120→投影×Ω4→robust_select→rollout 阶梯→τ 双闸→注入/快照/幂等缓存 | planner/runtime.py | active | |
| PlanSpec 轴/枚举 R1-R9/54 键 override/project_season | planner/plans.py | active | stage_* 四键未接线（G12） |
| Ω=4 对手模型（被动/两内置画像/悲观 0.75） | planner/opponents.py | active | 悲观在投影段零效力（G2） |
| 聚合+argmax+identity tie-break（τ=0.5%） | planner/select.py:42 | active(带缺陷) | G2 |
| 孪生：指纹链装载 fail-closed/回放重建/推进/克隆/规范投影 | planner/twin.py | active | |
| WaveCandidate 鸭类型+尾段投影镜像（与 wave.py 双份日历常量，测试钉） | planner/wave_script.py | active | 双份常量=重构合并点 |
| 候选档案头（谱系声明） | src/_archive_header.py | one-off | 建议=保留（身份史） |
| 确定性打包（拓扑序/零时间戳/--check）+precheck | build.py | active(工具) | MODULE_ORDER 须与 main 逐字一致 |

## 2. 分片 B：kgenv 引擎与评估基建

| 行为 | 状态 | 备注 |
|---|---|---|
| engine.py：wheel 驱动单局+ActivityPolicy 活性门+episode 契约（16 脚本/9 测试消费） | active 承重墙 | 活性门 README 未提 |
| arena.py：提交装载/run_match/异常局拒收/复盘 jsonl（16s/15t） | active 承重墙 | _abnormal_reason 与 eval_contract 分叉（G10） |
| eval_contract.py：种子域/AB-BA/异常局/sha+git 身份/原子发布（8s/5t，契约族基座） | active 基座 | |
| replay_profile.py：画像+_s_* 手写引擎复算（~1050 行）+成功指标（6s/2t） | active 承重墙 | G5 首险 |
| holdout_contract.py：一次性考卷状态机，4 代历史种子黑名单（:34-90） | active | |
| online_probe.py：采样台账 fail-closed 门（replays_are_local_selfplay→拒 :425） | active（SOP 唯一门） | |
| bots/：冻结弱池+强池+画像池 11 对手（11s/5t） | active | 手抄常量零校验（G11）；名册 5 处重复（G10） |
| elo（顺序敏感）/bradley_terry（批量顺序无关）/variance（Wilson+t）/regression（冻结回归线） | active | Elo 序敏感是回归门依据 |
| candidate_identity/external_h2h_contract/dna_forensics+dna_integrity | active | external_h2h 钉 wheel 版本+8 文件清单 |
| gym_env.py：gym 式单席封装 | 半 dormant | 仅 1 one-off 脚本+冒烟+5 测试（G15） |
| bots/llm_provider.py：OpenAI 兼容顾问（默认关，预算护栏） | dormant 实验件 | G15 |
| economy.py/redlines.py：经济/红线语义镜像 | 孤儿 | 0 脚本消费；docstring 陈述过期（G16） |
| vendor wheel 耦合 4 处：engine/gym_env 直 import、economy re-export（好样板）、twin 三重 sha、external_h2h 清单 | — | 升版 wheel 全断+replay_profile 静默 |

## 3. 分片 C：身份/门禁/评估/语料画像脚本（29 件）

recurring（机制常驻）：check_candidate_identity、check_eval_contract（import run_eval/run_holdout 子进程）、run_holdout（.flow 私有+exports 发布态）、run_eval、iterate_gate、ablate/quickwin_probe（灾难诊断口径纪律件）、run_llm_ab（env 门控条件件）、sync_online_probe（SOP 唯一门，需 kaggle CLI）、fit_bradley_terry、forensic_harvest（战后停摆）、replay_deep_stats、corpus_integrity、analyze/check_dna_forensics、h2h_external_probe/check_external_h2h、check_opponent_strength（验收 cmd）。

one-off：kill_table（曲线轴可跑）、sell_plan_reconciliation、capacity_calibration、observer_v0_validator、analyze_failure_modes、verify_milk_economics、probe_v9_wheat_gate、r3_trajectory_probe。库件误置：market_ledger（G17）。数据通道：corpus_build/corpus_fetch（依赖 gitignored 语料）。

关键事实：**corpus_integrity（蓝图验收 cmd）本机实测 exit=1**（references/data/replay-corpus/manifest.json gitignored 缺失）——验收绿灯只在持数据机器成立（G23）。

## 4. 分片 D：Track-B 门与法证族（27 件）+ 线上工件

permanent-gate：twin_fidelity（m6 验收）、planner_flagoff_golden（--check 本机退化 skip，golden JSON gitignored）、planner_offline_bench（m7 判据 a，席位错位 G1）、v48_derivative_launch_check / v48plus_launch_check（线上资产复验；后者靠 monkeypatch 复用前者模块全局）。

forensic-one-off：calibration_suite、p41_official_load_probe、v3_readmission_suite、v31_pressure_calibration（G2）、v15 三件、v143_sellrace_gates（含唯一正确的 seated rollout:91-116）、v48plus_ab_gate/layer_ablation/metrics、round23 四件、round24 三件。历史 utility：m4_switchover_regression（--golden-only 仍可用）、solver_shadow_stats、sprintA_structure_probe。已死：profile_v48_gap（G3）。

线上工件：v48_derivative（tar 01de7c27=原作者公开件逐字节；发射证据 JSON 在 gitignored probes 已消失）、v48plus（manifest 三 sha 核验一致；构建依赖 gitignored references→fresh clone 不可复现）、opponents（v48_main+v72+PROVENANCE；血统冲突 G4）。**2945/island-ga/kaggri 在 machine-local references/intel-notebooks，不在库内**（README"四套解码版"失准，G18）。

## 5. 分片 E：测试基线（实测）+ bc_track

**本机实测：976 passed / 8 failed / 8 skipped（992 collected，64s，工作树 clean）**。8F 全环境性：CRLF 工件×3（test_build_determinism/test_p3::TestPackaging/test_artifact_indexes——Windows autocrlf 机构建的提交件）、gitignored 数据缺机×3、Windows-only 断言×2（normcase/Path.is_absolute 语义）。8S 全为语料缺机。→"990+2"基线=Windows 主力机+数据在机口径（G6/G23）。

测试→行为钉住：51 文件；提交链契约 5（身份/打包/索引）钉 live 件；策略族 10+调度市场 7+观测器 1 **全部 import 现 main.py**（历史波命名、钉现役行为）；评估/语料 10；门禁 10（holdout 系钉 6 代 frozen b64=唯一历史代钉住）；Track-B 8。conftest.py 把 software/ 插 sys.path 总根——搬移 kgenv 断全部 51 文件（G24）；17 测试按文件名引用根级 frozen 工件。

bc_track（全 dormant，弃牌核实）：harvest/extract/schema/policy/eval 五件工装价值高（bc_eval 已是席位修正版 :172-191），train/opening/seed 中低，models 416KB 证据件（G14）。3,272 行零测试覆盖；复现链步骤 1-3 依赖 gitignored 语料；README 路径拼错+票 08 未回写（G7）。

## 6. 分片 F：治理与数据面

| 机制 | 现状 | 状态 |
|---|---|---|
| 蓝图验收 | 17 项（14 cmd+3 人工）；2 cmd 指向不存在文件（G9） | 部分失效 |
| /accept 记录 | 31 run 止于 09-01；m6/m7 与终交冲刺无验收记录 | 静默（实际治理已转 JOURNAL+metrics 分片直写） |
| 冻结快照 | 6 组 b64+manifest；manifest 内 candidate.path 记旧布局路径 | retired（历史身份链） |
| active_candidate.json | working=v14.3(dev)/frozen=v72/online_refs=[]——与 09-21 真实终局对脱节 | 滞后（G21） |
| metrics 合并 | 根 284 键@09-20 vs 分片 298 键@09-21，差 14 键 | 断裂（G8）；合并器在仓外 scripts/verify/ |
| JOURNAL | 270 行/190 条/08-28→09-21 连续 | active 健康（事实权威源） |
| references | README+INDEX 台账+digests 7 份；data/ 整目录 gitignore（~GB） | active；数据归宿=G23 |
| exports | 8 类正式产物入库（5 子目录 index.json，无根 index）；probes 混合策略（G22）；logs 9 件入库 | 基本健康 |
| 硬编码路径 | 三代并存（G24）：旧布局 manifest×6、现行 114 处（scripts 40/tests 10/blueprint 16/README 40/docs 8）、仓根 CWD 假设 | 重构最大雷区 |
