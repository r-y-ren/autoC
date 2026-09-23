# batches.md —— 批次表（待办导航）【R10 周期】
> fn-implement 独占更新。▶ = 下一批；未经批间门批准不得增删批次内容。
> 本梯批次前缀沿 F/G 惯例：R10 用 S 系列续号。

| 批次 | 函数/任务清单 | 验收点 | 注 |
|---|---|---|---|
| ▶ S1 | 运行时纯函数层：_cxs_harvest_completable → _cxs_completable_plant_demand → _cxs_seed_surplus → _cxs_seed_truncate → _cxs_agent；+FIRST_HARVEST_STEPS 常数转录（vendored wheel+交叉校验）；+侦察任务：plan_view 契约定形（读基座磁带未来 PLANT/BUY_SEED 通道，RACE 扫描先例） | test_layer_s.py 全绿（含构造用例三件=门③(c) 单测面；surplus 不确定→None；s671 边界） | 零误杀语义的落点批——每层失败方向必须朝"不截" |
| S2 | 构建面：append_layer_s_block → build_layer_s_candidate | build 实跑产出注入版 main.py+submission.tar.gz+build_manifest.json；双跑逐字节；diff 仅尾部追加 | round-30 打包配方复用 |
| S3 | 验证面：replay_action_diff → precision_subset_check → constructed_invariant_cases → gate_equivalence_precision → gate_h2h_vs_verbatim → gate_lineage_strength → gate_launch_fourgate_l1 → verify_layer_s_gates；+语料备制：strip 26 局 /tmp/r30 回放→最小重演形态归档 fn_docs/hybrid/results/replays-r30-26/（体积预算 <10MB，R8 先例） | verify_layer_s_gates 实跑四门 evidence 四件套全绿（=发射前置达成） | 8 函数=单批上限；语料是门③输入 |

## 变更记录（计划层事件）
| 日期 | 事件 | 说明 |
|---|---|---|
| 2026-09-23 | S1-S3 批次计划立表 | R10 周期开启；语料备制入 S3（实测 /tmp/r30 全量 1.3GB 不可入库，strip 后归档） |
