# 差距表（fn-refactor 阶段二产物）

> 对照基线：fn_docs/README.md v0（用户叙述=docs 底稿模式）。2026-09-21 六分片只读审查汇总。
> 用途：§一/§二 经阶段三裁决后回写 README；§三 供 fn-divide 结构取材。所有"修改"都发生在新结构（fn_work/）重建时，旧代码不动。

## 一、README 与代码的矛盾（README 需修订）

| # | README 表述 | 代码实际 | 证据 |
|---|---|---|---|
| 1 | 功能表#1"stdlib-only **单文件**自包含程序" | tar.gz 多模块包（main+src 10+planner 6）；"薄装载器"表述（流程 A#1）反而正确 | main.py:1-52、build.py |
| 2 | 流程 A#1"**九个**功能模块" | `_MODULE_ORDER`=**10** 模块（wave 加入后）；main.py 头注释同样过期 | main.py:51-52 |
| 3 | 功能表#3"Elo/BT 评级（顺序无关批量）" | Elo 顺序敏感（且其序恰是冻结回归门依据）、仅 BT 批量顺序无关 | elo.py:33 |
| 4 | 功能表#3"红线清单"为本地评估体系组成 | redlines.py 零 gate/arena 消费，孤儿模块 | redlines.py:24 陈述过期 |
| 5 | 功能表#7"四套公开顶级 bot 的**解码版**"（v48/2945/island-ga/kaggri） | 库内 opponents/ 仅 v48_main+v72；2945/island-ga/kaggri 在 machine-local references/intel-notebooks | opponents/、PROVENANCE.md |
| 6 | 功能表#2/流程隐含"孪生与 d0 反事实=可信计算" | 孪生本身逐位保真成立；但 harness 层席位错位使 me_seat=1 局的 d0 反事实/离线基准数字系伪影（已知勘误） | planner_offline_bench.py:319 及 8 文件 |
| 7 | 工作流程 D"每波过查→/accept 全量验收→分片汇总入 metrics" | /accept 链 09-01 静默（m6/m7 无验收记录）；根 metrics 落后 14 键；实际治理=JOURNAL 详记+分片直写 | acceptance/、metrics.json |
| 8 | （CODEMAP，非 README）"economy.py market.py 消费"/"profile_v48_gap 在役"/"53 tests"/"opponents 三套" | economy 零消费；profile_v48_gap 路径损坏必崩；51 tests；入库仅两套 | 各分片实证 |

## 二、README 未提及的重要行为（裁决后决定是否入 README / 进需求）

1. **语料管线全族**（corpus_build/fetch/integrity，m1 top-20 语料与完整性校验）——corpus_integrity 是蓝图验收命令，README 任何节未提；
2. **对手池认证门**（check_opponent_strength ≥50% vs greedy_carrot）与 11 对手三级池结构；
3. **活性门**（ActivityPolicy，engine.py:26-123，独立测试+冒烟把守）；
4. **replay_profile 内藏第二引擎**（~1050 行手写复算，无指纹看护——G5）；
5. **LLM 顾问实验件**（llm_provider，env 门控默认关）与 run_llm_ab 条件件；
6. **holdout 已历 4 代**种子域状态机（HISTORICAL_SEEDS_V1→V4）；
7. **市场层对账件**（market_ledger 库件+sell_plan_reconciliation）；
8. **波次日历剧本**（wave.py）非纯休眠——DTSP 每黎明把它排比较集首位，选中即激活；
9. **测试基线的机器语境**（990+2 仅 Windows 主力机+数据在机；本机 976P/8F/8S 全环境性）；
10. **原始证据的数据归宿**（references/data ~GB gitignored：线上回放、回放语料、golden JSON——fresh clone 不可复算画像/法证/部分测试）。

## 三、结构与复现性风险地图（fn-divide 取材）

### 3.1 身份与等价性锚点（搬移即断）

- main.py sha = 候选身份（check_candidate_identity 三方一致）；
- build.py MODULE_ORDER 必须与 main._MODULE_ORDER 逐字一致；
- runtime.agent_dir() 相对 `../src`；twin wheel 相对 `../../../vendor`；
- 黄金哈希套件按固定成员名 exec src（flagoff equivalence）；
- tests 17 处按文件名引用 software 根 frozen b64/manifest。

### 3.2 路径硬编码三代并存（G24）

①旧布局 `workspace/software/...`（6 份冻结 manifest、acceptance/report.md）；②现行 `workspace/kaggriculture/...`（scripts 40/tests 10/blueprint 16/software README 40/docs 8，全部假设 CWD=仓根）；③仓外 `scripts/verify/*`（merge_metrics/build_indexes/test_acceptance——重构不可触碰）。run_holdout.py:64 的双前缀兼容（SOFTWARE_REPO_PREFIXES）=上次搬移已付的补偿成本。

### 3.3 依赖方向（可安全独立单元）

- constants 被全员共享；planner 永不 import src（纪律）；runtime 经 exec 反向驱动 src 沙盒并写 main globals=唯一反向边；
- 可独立：twin/plans/select/opponents/wave_script/build（纯函数无 src 耦合）；
- planner_offline_bench 是事实共享库（calibration/v3/v31/v15×2/round23×2/round24×2/v143 import）——席位 bug 居其核心（G1）；build_v13_namespace 有 3 份近似拷贝（bench:216/flagoff:116/v15_h2h:85）；TARGET9/WINS13 局号元组 ≥5 文件重复。

### 3.4 全局状态

提交链 ~16 个按 player 分键 dict（_PLAN_MEM/_STAGE_MEM/_MISSION_SHADOW/_SELL_*/_MARKET_MEM/_OPP_OBSERVER/_TELEMETRY 等），各自手写"时钟倒退=重置"惯用法——重复逻辑重灾区，重构高价值合并点。

### 3.5 复现性断层（跨 C/D/E/F 汇总）

- 数据孤儿：references/data 整目录 gitignored 且本机不存在→21/27 Track-B 脚本+corpus/observer 族不可跑、8 测试 skip、corpus_integrity 验收 cmd exit=1；
- 工件不可移植：CRLF 变体 index sha（Windows 主力机 autocrlf 构建）→3 测试在 POSIX 必挂；
- Windows-only 断言 ×2；v31 只在历史 ref 语义成立；
- v48+ 构建依赖 gitignored references 源→fresh clone 不可复现；v48_derivative 发射证据 JSON 已随 probes 清理消失。

### 3.6 合规链注意

dadee25a（v48 衍生=在跑线上资产 56400478）的 PROVENANCE 双记录冲突（kaitofukami/无许可 vs Ozer/Apache-2.0）——统一归源前，对外引用该资产时不得二选一断言（G4）。
