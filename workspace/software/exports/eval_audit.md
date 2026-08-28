# 评估保真度审计清单（ABE-Ralph 式，m1-vertical 波次 2）

> 审计对象：`scripts/run_eval.py` 全池 matchup 矩阵 + `scripts/analyze_failure_modes.py` 失败模式探针 + `scripts/check_opponent_strength.py` 强度门。
> 每项标注 pass / warn / fail 并给出可复核证据（命令 + 产物路径 + 实测数字）。本文件是 `metrics.software.eval_audit_pass` 与 `eval_results.json.eval_audit_pass` 的证据源。
> 结论先行：**8 pass / 3 warn / 0 fail**；3 条 warn 均为已声明边界（同族过拟合、单座位、小样本），不阻塞验收，但 m2 与线上校准必须回应。

## 1. 种子控制与可复现性 — PASS（含如实声明的 random 边界）

- 种子固定：矩阵种子 `101..100+rounds`、头对头加播 `+500` 偏移（seeds 601..604）、失败探针 `201..208`，全部写入 `eval_results.json.config.seeds` 与 `failure_probe_summary.json.probe_seeds`。
- 确定性探针（每次运行实测，同配对同种子连打两遍）：
  - `greedy_carrot vs starter seed=101` → 奖励逐位一致（rounds=4 运行：`[[9899,3440],[9899,3440]]`）。
  - `greedy_carrot vs random seed=101` → 奖励漂移（`[[6326,0],[6869,0]]`，rounds=2 运行漂移为 `[[6012,0],[8465,0]]`）——**如实声明**：引擎内置 `random` agent 用 OS 熵源自播，未被 episode seed 完全钉死；凡涉 random 的对局奖励跨会话漂移，胜负判定在本池强度差下不受影响（random 对任何对手 0 胜，W0 L32）。
- m0 交叉会话证据（沿用）：40 局中 32 局与第一轮归档逐局奖励一致，8 局漂移全部来自 random 对局。
- 方差统计（`kgenv/variance.py`）：Wilson 95% 区间（非 Wald，4 种子样本不适用正态近似）+ t 分布资金差区间，均已落盘 `eval_results.json.eval_variance_report`。

## 2. 对局长度全长 720 — PASS

- rounds=4 全量运行：148/148 局 `turns == 720`（min=max=720，均值 720.0）；episodeSteps 由 `FULL_EPISODE_STEPS=720` 显式注入引擎配置。证据：`eval_results.json.games[*].turns`。

## 3. 对手池构成与强度谱系 — PASS

- 池构成（9 bot，`opponent_pool_names`）：cow_baron / melon_hoarder / expansionist（新）+ baseline_wheat / greedy_carrot / starter / random / pass（冻结弱池）+ submission 本体。
- 强度认证（硬性要求）：`python scripts/check_opponent_strength.py --rounds 3` → 三新对手对弱池 4 对手 × 3 种子 **9/9 全胜 each**（对 greedy_carrot 平均分差 cow_baron +37k+、melon_hoarder +30.6k、expansionist +10.9k），退出码 0。
- 谱系（rounds=4 全池 Elo，k=32）：cow_baron 1460.3 > submission 1422.8 > melon_hoarder 1391.3 > expansionist 1289.6 > baseline_wheat 1170.6 > greedy_carrot 1155.8 > starter 1058.3 > pass 991.5 > random 859.7——池最高 Elo 从 m0 的 1162.2（greedy_carrot）提高到 1460.3，「对手池偏弱」问题已量化改善（`pool_max_elo`）。

## 4. Elo 计算参数 — PASS

- k=32、start=1200、**只按胜负平计分**（tie=0.5），对齐官方天梯语义；流按实际对局顺序回放（顺序敏感，如实记录于 `kgenv/elo.py` 与结果 `elo` 字段）。参数原样写入 `eval_results.json.elo`。

## 5. 共享市场与对局保真 — PASS

- 对局运行在官方引擎（vendored 1.32.7，引擎代码未改动，`vendor/WHEEL_PROVENANCE.md`），市场为**共享**逐单 lockstep——本波失败模式 FM-2/FM-4 正是共享市场干预的直接证据（MELON 267→165 于 day 15 对手倾销；FERT 94→41 双卖压），证明评估环境捕获了真实博弈干预而非孤岛农场模拟。
- 每日市场价格曲线已入复盘日志（`replay_log.jsonl.daily_prices`，m1 新增），供失败分析复核。

## 6. 冻结回归线独立于强池 — PASS（含一次数据驱动的修订，如实记录）

- 语义：`--assert-regression` 只在**冻结子流**（六冻结成员之间的对局）上断言两条 m0 不变量：Elo 严格降序 + submission 对冻结池 0 负。强对手对 submission 的胜负属于失败模式分析（`failure_modes.md`），不进回归门——m0 冻结线语义保持。
- 实测：`python scripts/run_eval.py --rounds 2 --assert-regression` → **PASS**（74 局 196.17s；冻结子流 32 局：submission=1355.0 > baseline_wheat=1252.4 > greedy_carrot=1227.5 > starter=1175.3 > pass=1128.9 > random=1061.0；submission 0 负）。
- **修订记录（透明呈报）**：m0 冻结序写作 `... > starter > random > pass`，但 m0 子矩阵中 random 与 pass 从未互相交手（对手只打主打），其相对序是对手字典迭代顺序在 Elo 流中的伪影。m1 全矩阵补上了该对局，pass 对 random 100% 胜（random 稳定 ~$0 vs pass 保底 $3000；冻结子流实测 pass W2 L14 > random W0 L16）。据此把该子句修订为 `pass > random`（`kgenv/regression.py` 模块 docstring 有完整论证 + 单测 `test_pass_beats_random_on_merit_in_elo`）。**提交 bot 相关的一切不变量原样未动。**

## 7. 已知威胁：对手同族变体过拟合 — WARN

- 三新对手均由我方基于同一引擎知识库设计（鹅引擎/瓜波段/小麦基线的变体），与 submission 同族。Elo 表现强（1460/1391/1290）不代表天梯多样性；对手池对 submission 的 0% / 0% 胜率（对 cow_baron / melon_hoarder）可能是族内特化打击。
- 缓解：失败模式 FM-1/FM-2 的根因（动物单位经济、共享价格闸门）是**机制级**而非对手特化的，改进方向天然泛化；m2 迭代闸门要求每项增强对全池矩阵取证，且 man-submit 后需用线上反馈重校池构成（`online_feedback_calibration` 键已预留）。

## 8. 已知威胁：单座位对局 — WARN

- 矩阵每对只以 p0 视角打 N 种子，未做座位对换。引擎市场逐单 lockstep 且双方对称报价，预计座位不对称可忽略，但**未实测**。缓解：失败探针的 64 局全部 submission p0 位，若存在座位效应则失败模式估计偏保守/偏乐观未知；m2 可加一轮 p1 位复测。

## 9. 已知威胁：小样本方差 — WARN

- 默认 4 种子/对：Wilson 区间宽（4/4 胜的 95% 下界仅 0.51）。实测最不稳对局：`baseline_wheat vs greedy_carrot`（弱池内部）win_rate 0.75、CI95 [0.30, 0.95]、跨种子结果翻转（flips=True）；submission 相关对局无翻转（对强敌 0/4 与 0/8 一致、对弱池 4/4 与 8/8 一致），失败结论的种子稳定性已在失败探针中用 8 种子加固。
- 缓解：一切增强合入判据（m2 迭代闸门）须同时看区间与样本量，禁止只看点估计。

## 10. 引擎出处与运行参数 — PASS

- 引擎：vendored `kaggle_environments-1.32.7+nodeps`（去依赖元数据/去可视化资源，引擎代码未改动）；`official_engine_version()` 写入每次结果。actTimeout=60s/回合；全部 bot 为纯启发式（单回合毫秒级），无超时风险。评估产物写入前先过 `exports/schema.json` v1.1 校验（`jsonschema.validate`，失败即拒写盘）。

## 11. 产物契约 — PASS

- `eval_results.json` 通过 schema v1.1（pytest `test_eval_results_sample_matches_schema` 常驻把关）；B 组 m1 键（opponent_pool_names / pool_max_elo / matchup_win_rates / eval_variance_report / eval_audit_pass / failure_modes）与 m2 占位键（9 个，全 null 待测）齐备；v1.0 字段原样保留（向后兼容）。

---

## 汇总

| # | 项 | 判定 |
|---|---|---|
| 1 | 种子控制与可复现性（random 边界如实声明） | pass |
| 2 | 全长 720 回合（148/148） | pass |
| 3 | 对手池构成与强度谱系（强度门 9/9×3） | pass |
| 4 | Elo 参数（k=32 只按胜负平） | pass |
| 5 | 共享市场保真（干预实测可复现） | pass |
| 6 | 冻结回归线独立（gate PASS；random/pass 修订已呈报） | pass |
| 7 | 对手同族过拟合 | warn |
| 8 | 单座位对局未换位 | warn |
| 9 | 小样本方差（CI 已落盘） | warn |
| 10 | 引擎出处与超时 | pass |
| 11 | 产物契约 schema v1.1 | pass |

**8 pass / 3 warn / 0 fail**。三条 warn 的跟进责任：#7、#8 → m2 波次（迭代闸门 + p1 位复测）；#9 → m2 增强判据强制区间报告；线上校准 → man-submit 后回填。
