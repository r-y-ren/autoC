# G1 受影响历史结论重算台账（recalculation_ledger）

- 生成时间: 2026-09-21T14:48:04Z
- 生成入口: fn_work/src/run_official_bench/recalculate_affected_history.py::recalculate_affected_history
- 结论清单来源: fn_docs/behavior_inventory.md §0 缺陷 G1（席位错位通道未回流——受影响历史结论）
- 条目: 5 条 = RECALC 0 + SKIP 5
- 本台账与既有 JOURNAL 并列留痕（不改 JOURNAL）。

## 口径定义

- **原值（错位口径）**: 旧 planner_offline_bench 内联通道——`deps["step"](state, [mine, theirs])` 恒把"我方动作"注入 seat0（G1：planner_offline_bench.py:319 及其内联同构扩散），me_seat=1 局终局数字为双席互换伪影。
- **重算值（seated 口径）**: fn_work/src/run_official_bench/rollout_with_replay_opponent.py——显式 me_seat 注入（mine→seats[me]、回放对手动作→对席），返回序=(seat0, seat1)；正确参照 software/scripts/v143_sellrace_gates.py:91-116。
- **是否翻转**: 重算值与原值在结论自身判据语义下不等价（默认值级不等；语义级判定由条目 flip 谓词给出）。
- **状态**: RECALC=已用 seated 通道重算；SKIP(<原因>)=本条未重算、原因留档——单条失败不中断整批（契约）。

## 重跑前提

- 官方回放语料 `references/data/online-replays/**`（gitignored）须在位：缺失条目记 SKIP(replay_data_missing)，在持有语料的主力机上重跑 `recalculate_affected_history(default_affected_conclusions())` 即回填真值并重新落盘本台账。
- 各结论须注入与原脚本同源的决策 persona（条目 agent_callable/agent_factory；缺 persona 记 SKIP(persona_missing)，persona_note 注明出处）。
- 引擎指纹链 fail-closed：wheel/场景 sha256 不符即抛，不静默降级（该类失败记 SKIP(recalc_error)）。

## 台账

| 结论标识 | 局号 | 原值（错位口径） | 重算值（seated 口径） | 是否翻转 | 状态 |
|---|---|---|---|---|---|
| v3_readmission:criterion_b_giants | 110687913、110677576、110684532、110694473、110702221、110699710、110685617、110841464、110701172 | 5/9（判据 b 九巨人败局回归，阈值 ≥4/9 判 PASS；错位通道口径） | — | — | SKIP(replay_data_missing) |
| v3_readmission:criterion_c_wins | 110681129、110682284、110683437、110686759、110690133、110691193、110692292、110693383、110695554、110696787、110697778、110698875 …（共 13 局） | 7/13（判据 c 十三胜局回归，损伤 >5% 局数 ≤2 判 PASS、实测 7 局判 FAIL；错位通道口径） | — | — | SKIP(replay_data_missing) |
| v48plus_ab_gate:giants_d0 | 110687913、110677576、110684532、110694473、110702221、110699710、110685617、110841464、110701172 | 9 巨人局 v48plus−v48 挽回方向判据（direction_ok/improved 计数；历史明细 exports/probes/v48plus/ gitignored 未随库） | — | — | SKIP(replay_data_missing) |
| round24_d0_counterfactual | 110687913、110677576、110684532、110694473、110702221、110699710、110685617、110841464、110701172、110681129、110682284、110683437 …（共 22 局） | 22 局 d0 反事实 base/V_LAND/V_WALLET/V_COMB 四臂终局与 ≥5/9 挽回门（错位通道口径） | — | — | SKIP(replay_data_missing) |
| planner_official_bench:history | — | m7 判据 a 等离线基准历史数字（planner_offline_bench.py:319 恒 mine→seat0） | — | — | SKIP(replay_data_missing) |

## SKIP 详情

- **v3_readmission:criterion_b_giants** [SKIP(replay_data_missing)] 回放缺失 9/9 局: references/data/online-replays/round24/episode-110687913-replay.json、references/data/online-replays/round24/episode-110677576-replay.json、references/data/online-replays/round24/episode-110684532-replay.json、references/data/online-replays/round24/episode-110694473-replay.json、references/data/online-replays/round24/episode-110702221-replay.json、references/data/online-replays/round24/episode-110699710-replay.json、references/data/online-replays/round24/episode-110685617-replay.json、references/data/online-replays/round24/episode-110841464-replay.json、references/data/online-replays/round24/episode-110701172-replay.json
- **v3_readmission:criterion_c_wins** [SKIP(replay_data_missing)] 回放缺失 13/13 局: references/data/online-replays/round24/episode-110681129-replay.json、references/data/online-replays/round24/episode-110682284-replay.json、references/data/online-replays/round24/episode-110683437-replay.json、references/data/online-replays/round24/episode-110686759-replay.json、references/data/online-replays/round24/episode-110690133-replay.json、references/data/online-replays/round24/episode-110691193-replay.json、references/data/online-replays/round24/episode-110692292-replay.json、references/data/online-replays/round24/episode-110693383-replay.json、references/data/online-replays/round24/episode-110695554-replay.json、references/data/online-replays/round24/episode-110696787-replay.json、references/data/online-replays/round24/episode-110697778-replay.json、references/data/online-replays/round24/episode-110698875-replay.json、references/data/online-replays/round24/episode-110790899-replay.json
- **v48plus_ab_gate:giants_d0** [SKIP(replay_data_missing)] 回放缺失 9/9 局: references/data/online-replays/round24/episode-110687913-replay.json、references/data/online-replays/round24/episode-110677576-replay.json、references/data/online-replays/round24/episode-110684532-replay.json、references/data/online-replays/round24/episode-110694473-replay.json、references/data/online-replays/round24/episode-110702221-replay.json、references/data/online-replays/round24/episode-110699710-replay.json、references/data/online-replays/round24/episode-110685617-replay.json、references/data/online-replays/round24/episode-110841464-replay.json、references/data/online-replays/round24/episode-110701172-replay.json
- **round24_d0_counterfactual** [SKIP(replay_data_missing)] 回放缺失 22/22 局: references/data/online-replays/round24/episode-110687913-replay.json、references/data/online-replays/round24/episode-110677576-replay.json、references/data/online-replays/round24/episode-110684532-replay.json、references/data/online-replays/round24/episode-110694473-replay.json、references/data/online-replays/round24/episode-110702221-replay.json、references/data/online-replays/round24/episode-110699710-replay.json、references/data/online-replays/round24/episode-110685617-replay.json、references/data/online-replays/round24/episode-110841464-replay.json、references/data/online-replays/round24/episode-110701172-replay.json、references/data/online-replays/round24/episode-110681129-replay.json、references/data/online-replays/round24/episode-110682284-replay.json、references/data/online-replays/round24/episode-110683437-replay.json、references/data/online-replays/round24/episode-110686759-replay.json、references/data/online-replays/round24/episode-110690133-replay.json、references/data/online-replays/round24/episode-110691193-replay.json、references/data/online-replays/round24/episode-110692292-replay.json、references/data/online-replays/round24/episode-110693383-replay.json、references/data/online-replays/round24/episode-110695554-replay.json、references/data/online-replays/round24/episode-110696787-replay.json、references/data/online-replays/round24/episode-110697778-replay.json、references/data/online-replays/round24/episode-110698875-replay.json、references/data/online-replays/round24/episode-110790899-replay.json
- **planner_official_bench:history** [SKIP(replay_data_missing)] 回放根缺失: references/data/online-replays
