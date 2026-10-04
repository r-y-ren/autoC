# v6b — 计划层三面一致重生成候选（R9-G2b tape_surgery_v2 + assemble_v6b_build）

> 基底 `../../v48_derivative/main.py`（dadee25a…，只读）经`giant_route/tape_surgery_v2.py` 三面手术：产线（买/建/雇/种）、卖序（M1 吸收节律+峰日寻优）、移动动词（tile 组任务+精确计步）全部重生成；六路由 trunk/branch 前缀恒等（88/120/153/216/160 切换点前逐字节同 default），事件点切换结构与反应层（反克隆/槽位重排/终局清仓/杂草修复）在 blob 外逐字节保留。追加块沿 v4b 旗面（P2 死价保险 on，P1/P3/P4 off）。本目录产物由 `giant_route/build_v6b.py` 确定性生成。

## 身份链

| 件 | sha256 | 字节 |
|---|---|---|
| 基底（未手术原样） | `dadee25a9840313218384208c53b2c4752f82c3209cc654632e0b96c65e2664a` | 107008 |
| 手术基底（blob 替换后） | `9810f78def3e7b203de9d59f3ac02472dce9dde175f907b3f698bb66a430d87c` | 81009 |
| v6b `main.py`（手术基底 + P2 追加块） | `62b4fea99c6a4fbfd35fc0147e5ba4ed9ae844e9946bbd7c83c7ebff3036a522` | 90500 |
| `submission.tar.gz` | `5a532201c285a853db065e2d7f0f4a9cb7cef16b19fdc0d496b781e86759201b` | 67406 |

三面差分：产线 858 条；卖面 723 条（6 路由重排）；移动面 180 路由日全重排——明细 `../giant_route/surgery_v2_diff.json`。

## 门禁（四门冒烟结果回填）

| 门 | 判据 | 结果 |
|---|---|---|
| gate1 官方装载语义 | 干净 -I 子进程 get_last_callable 复刻一致 | PASS（干净 -I 子进程 get_last_callable 复刻，named==last（_v48hybrid_entrypoint），isolated vs local 动作流 mismatch=0，stdlib 扫描空） |
| gate2 双席自打 | seeds 101/102 双局 720 回合 DONE、每步 <1000ms | PASS（seeds 101/102 双席自打双 DONE 720 回合，seed101 statuses=['DONE', 'DONE'] rewards=[10657,10657] 720回合 max 2.4ms p99 0.36ms; seed102 statuses=['DONE', 'DONE'] rewards=[32340,32340] 720回合 max 3.45ms p99 0.35ms） |
| gate3 确定性 | seed101 重跑动作流哈希逐字节一致 | PASS（seed101 重跑动作流哈希逐字节一致（eb2503257232…）） |
| gate4 体积 | tar ≤ 100MB | PASS（67,406B ≤ 100MB） |

结构性门禁（h2h/seated/胜局回归/经济面）属 R9-G4 verify_structure_gates，不在本装配器内。

