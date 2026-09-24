# batches.md —— 批次表（待办导航）【R10 周期】
> fn-implement 独占更新。▶ = 下一批；未经批间门批准不得增删批次内容。
> 本梯批次前缀沿 F/G 惯例：R10 用 S 系列续号。

| 批次 | 函数/任务清单 | 验收点 | 注 |
|---|---|---|---|
| S1(完成 09-23) | 运行时纯函数层：_cxs_harvest_completable → _cxs_completable_plant_demand → _cxs_seed_surplus → _cxs_seed_truncate → _cxs_agent；+FIRST_HARVEST_STEPS 常数转录（vendored wheel+交叉校验）；+侦察任务：plan_view 契约定形（读基座磁带未来 PLANT/BUY_SEED 通道，RACE 扫描先例） | test_layer_s.py 全绿（含构造用例三件=门③(c) 单测面；surplus 不确定→None；s671 边界） | 零误杀语义的落点批——每层失败方向必须朝"不截" |
| S2(完成 09-23) | 构建面：append_layer_s_block → build_layer_s_candidate | build 实跑产出注入版 main.py+submission.tar.gz+build_manifest.json；双跑逐字节；diff 仅尾部追加 | round-30 打包配方复用 |
| S3(完成 09-24) | 验证面：replay_action_diff → precision_subset_check → constructed_invariant_cases → gate_equivalence_precision → gate_h2h_vs_verbatim → gate_lineage_strength → gate_launch_fourgate_l1 → verify_layer_s_gates；+语料备制：strip 26 局 /tmp/r30 回放→最小重演形态归档 fn_docs/hybrid/results/replays-r30-26/（体积预算 <10MB，R8 先例） | verify_layer_s_gates 实跑四门 evidence 四件套全绿（=发射前置达成） | 8 函数=单批上限；语料是门③输入 |
| S4(完成 09-24) | R11：make_layer_s_v2_block（净需求覆盖 v2 块生成+AST 校验）→ build_l11_candidate → gate_h2h_vs_l1 → gate_equivalence_v2(+constructed_cases_v2) → verify_l11_gates；全量四门真跑 | verify_l11_gates 实跑 overall（门绿=round-32 发射前置） | R10 管线复用重定向；L1 目录零改动 |

## 变更记录（计划层事件）
| 日期 | 事件 | 说明 |
|---|---|---|
| 2026-09-24 | S4 全量门禁 FAIL=净需求覆盖口径实证否决 | 门① 0-6-10（六败全恰 -10：L1 净赚的 +10 在净口径下丢）+门③ appear 16>2（回买全数穿透：被剩余磁带种植需求局部正当化）+死种 $3,310 劣于 L1 $3,190——**任何步局部判定都缺跨步信息认证回买为废**；正确机制=累计台账式（品项级 跨窗累计供给 vs 累计可完成需求，对磁带单/回买单统一授权）。批间评审顺延至修订批（FAIL 归因=设计级，实现语义矩阵已验无误） |
| 2026-09-24 | S3 评审 P0/P1 批内修复（用户授权批内） | ①P0 门①装载缺陷：gate_h2h_vs_verbatim 仍用 kgenv.arena.load_submission_agent（具名 agent 优先对两 main 均装到内层基座、L1 漏层 S）→16 局实为基座互打全 tie、证据无效；修复=装载改官方 last-callable 桌面复刻（import 复用门② _load_entry，不制第四份）+装载身份断言（l1=_cxs_agent/verbatim=_cxd_agent，不符抛 GateH2HError"装载身份不符" fail-closed，门④同款先例）+docstring 更正+全量重跑 16 局 **14-0-2 绿**（margin +10×14、204 双席 tie；rate 1.0≥0.55）。②P1 测试台账隔离：h2h/launch run 加 evidence_path=None（门③同款口径），test_gate_h2h/test_gate_launch 台账全走 tmp（+装载身份断言/装载失败 fail-closed 用例×3）——修复前测试真跑曾把真 h2h_evidence.json 覆写回 4 局（HEAD 即该脏态入库）；重跑后复验 pytest 不再打回（n_games=16 与 verify_summary 一致）。③留痕更正：三文档"两红均规格口径"表述更正为"门③红系规格口径裁决项；门①红系装载缺陷（已修复重跑）"；115 passed |
| 2026-09-24 | S3 计划层事件四件（②③子项经 P0 修复更正） | ①测试文件按函数拆分（test_gate_h2h/test_gate_lineage/test_gate_launch/test_replay_action_diff/test_precision_subset_check/test_gate_equivalence/test_verify_gates——并行实现防冲突；原 test_gates.py 桩按重复删除）；②门②③④装载器改官方 last-callable 桌面复刻（kgenv.arena 命名优先分支对 L1 会漏层 S——两子代理独立同发现，与 round-30 gate_note 203/719 分歧同源；**门①漏改，评审 P0 纠正后补齐**）；③门①实测 0-0-16 全 tie 翻红+门③(a) 16/26 基座反应形态红（回买@662/少卖@669；final_delta 无负值、subset 26/26 绿）——门③红系规格口径裁决项；门①红系装载缺陷（已修复重跑，"截断在该种子域不触发"系误定性），批间门裁决；④26 局语料归档 fn_docs/hybrid/results/replays-r30-26/（5.09MB<10MB 预算，seed 真值在 info.seed，26/26 孪生复现） |
| 2026-09-23 | S2 批间评审 PASS-with-notes | 双轴无 P0/P1：P1×2 修复经引擎源独立证实（719 界等价性五作物严格成立；PLANT 先于买单属实）；配方对 round-30 复现独立复核；产物 sha 三方一致。P2×4 备查：a) plants_now>held 角落钳 0 系规格明文（基座不自记超种不触发）；b) manifest generated 挂钟行跨日重建会脏树（S3 知悉）；c) 双跑哈希=单 sha+断言口径；d) 测试注释两处小疵（S3 顺修） |
| 2026-09-23 | S1 批间评审 FAIL（两阻断） | ①P0：c63f5eb 误夹带会话前已存在的本地改动（.zcode/config.json 三钩子 enabled→false——按 D14 授权边界记忆系用户有意关闭勿恢复；.gitignore 两行路径迁移——对应 09-23 大整合后的正确新路径）；处置=补留痕不回滚，主会话此后弃用 git add -u 改显式路径。②P1×2（误杀向公式缺口，S2 注入前必须修）：_cxs_harvest_completable off-by-one（引擎天粒度 day-planted>=fyd 且 718 为最后动作步 ⇒ 边界应为 s+fh≤719/天粒度 s//24+fyd≤29，现式把 s=671 判不可完成）；_cxs_seed_surplus 缺当前步 PLANT 消耗扣减（同步单位先于市场结算，紧平衡时可超删至多 p 量）；修复方案=公式改天粒度+demand 纳入当前步 plants（签名加 current_plants 参数=微调级） |
| 2026-09-23 | S1-S3 批次计划立表 | R10 周期开启；语料备制入 S3（实测 /tmp/r30 全量 1.3GB 不可入库，strip 后归档） |
