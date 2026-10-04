# v6 — 磁带手术候选（R9-G2 perform_tape_surgery + assemble_v6_build）

> 基底 `../../v48_derivative/main.py`（dadee25a…，只读）经`giant_route/tape_surgery.py` 产线事件手术：六路由内BUY/BUILD/HIRE/种植事件按 `giant_route/target_schedule.json` 改写；卖单面/移动骨架/事件点切换结构/反应层（反克隆/槽位重排/终局清仓/杂草修复）逐字节保留。追加块沿 v4b 旗面（P2 死价保险 on，P1/P3/P4 off）。本目录产物由 `giant_route/build_v6.py` 确定性生成。

## 身份链

| 件 | sha256 | 字节 |
|---|---|---|
| 基底（未手术原样） | `dadee25a9840313218384208c53b2c4752f82c3209cc654632e0b96c65e2664a` | 107008 |
| 手术基底（blob 替换后） | `4e89b09ca187b86de5192867c90e1cbca6b6501f25d8c90b645156defb63d891` | 107756 |
| v6 `main.py`（手术基底 + P2 追加块） | `f1decea4473d3a375805615ec0b3af5caf7822013f0e1eb7134e8515ed736c5e` | 117247 |
| `submission.tar.gz` | `da84461918d0d57bbf31e2b80d554fdd334a519c210eb96479c3c4e6b48ac304` | 88219 |

开关：P1/P3/P4 off、P2 on（v4b 接线形态）；手术差分 499 条（hires/buys/plants/land），编辑 2610 处——明细 `../giant_route/surgery_diff.json`。

## 门禁（四门冒烟结果回填）

| 门 | 判据 | 结果 |
|---|---|---|
| gate1 官方装载语义 | 干净 -I 子进程 get_last_callable 复刻一致 | PASS（干净 -I 子进程 get_last_callable 复刻，named==last（_v48hybrid_entrypoint），isolated vs local 动作流 mismatch=0，stdlib 扫描空） |
| gate2 双席自打 | seeds 101/102 双局 720 回合 DONE、每步 <1000ms | PASS（seeds 101/102 双席自打双 DONE 720 回合，seed101 statuses=['DONE', 'DONE'] rewards=[15127,15127] 720回合 max 97.65ms p99 0.51ms; seed102 statuses=['DONE', 'DONE'] rewards=[33870,33870] 720回合 max 2.92ms p99 0.37ms） |
| gate3 确定性 | seed101 重跑动作流哈希逐字节一致 | PASS（seed101 重跑动作流哈希逐字节一致（b55cb9b6d875…）） |
| gate4 体积 | tar ≤ 100MB | PASS（88,219B ≤ 100MB） |

结构性门禁（h2h/seated/胜局回归/经济面）属 R9-G4 verify_structure_gates，不在本装配器内。

