# batches.md —— 批次表（待办导航）
> fn-implement 独占更新。▶ = 下一批要完成的任务；未经批间门批准不得增删批次内容。
> 波序对齐 responsibility.md 四波（W1 评估修复 → W2 基线数据 → W3 契约结构 → W4 文档治理+bot 整体迁移）；唯一波间依赖：B9 的 v143 归档前置 B3（bench 吸收 seated 完成）。
> 旧树冻结纪律：一切实现只落 fn_work/ 与 fn_docs/implementation/；[改造] 件的修复发生在 fn_work 副本，旧树零字节变更直至战后 fn-close。

| 批次 | 函数/任务清单 | 验收点 | 注 |
|---|---|---|---|
| ▶ B9 | archive_forensic_assets 子树: partition_script_tiers, archive_bc_models, archive_forensic_assets | 归档区落位 + 主线 import 断言 + 保留档可跑 | W3；R11/R12；前置 B3 |
| B10 | relocate_library_modules 子树: scan_for_library_misplacement, relocate_library_modules | 顶层 wired + 库件误置扫描绿 | W3；R15 |
| B11 | downgrade_dormant_assets 子树: prune_mainline_import_graph, downgrade_dormant_assets | 主线 import 图断言绿 | W3；R13/R14 |
| B12 | run_submission_agent 下半（迁移核心 5 件）: observe_opponent_state, decide_macro_mode, build_mission_pack, solve_worker_routes, execute_along_route | 五件 implemented+tested（对旧模块语义随迁测试绿） | W4；子树 10 函数超 8 上限切半；死码不迁（R10） |
| B13 | run_submission_agent 上半: load_agent_modules, plan_market_orders, run_dawn_planner, record_shadow_telemetry, run_submission_agent | 顶层 wired=agent 整链实跑 + run_equivalence_gate 全 pass（快照整局冻结值+黄金哈希） | W4 收口；R1 主体 |
| B14 | sync_documentation 子树: fix_bc_track_records, retire_codemap_with_errata, codify_probes_policy, sync_documentation | 顶层 wired + gap_table §一清单对账清零 | W4；R7/R16/R18 |
| B15 | record_governance_dispositions 子树: write_dual_source_provenance, declare_blueprint_cmd_invalidation, demote_active_candidate_ledger, record_governance_dispositions | 顶层 wired + 处置记录键完整 | W4；R4/R17/R21（R21 物理动作留时点闸） |

## 变更记录（计划层事件：签名微调、需求变更往返、放弃等）
| 日期 | 事件 | 说明 |
|---|---|---|
| 2026-09-22 | B6/B7 评审登记 | B6：Windows 断言语义收窄为"工具+扫描器 0 命中"（旧树冻结不可改，fn_work 从未含此模式）；生成文档内嵌绝对路径属实跑记录（可接受，报告 output_root 同机幂等）。B7：spec"任一类缺失即失败"实改为"missing 登记回填+ok/complete 分离"（本机 gitignored 语料缺失常态）；两处应修（manifest 自指字段/声明绝对路径）随补丁批处理 |
| 2026-09-21 | B6 体积修正（协调者） | artifacts 全量镜像（100 文件/54 万行）属可再生成派生数据，违反体积纪律——撤出 git 只留报告×2+LF 索引×5+锚例 1；机制保留按需重建（regenerate_artifacts_lf 随时可重放） |
| 2026-09-21 | B5 评审文档同步 | responsibility.md migrate 块"反例 XPASS"字面与实现"转常规 PASSED+零 xfail 残留"口径差——实现自洽（旧套件 README 迁移时转正规定），裁决键 xpassed_counterexamples 名遗留待下次契约触及改名 |
| 2026-09-21 | B3 签名登记（评审补登） | evaluate_plan_portfolio 实参扩为 +replay/+me_seat/+聚合四参+plan_cap（模块 docstring 已载，补表）；gate_eps/twin_noise_eps 为解析未接线死旋钮（语义同旧码常量 1.0，W1 不动留档） |
| 2026-09-21 | 快照套件口径修正（B3 期发现） | 根因=planner-on 整局含时间治理器（0.85s 帽读真实墙钟）→负载抖动跨决策边界即漂移（实测两跑 [81108,70273]/[78199,63920]）；整局逐位冻结改旗关面（三遍逐字节一致 [59730.0,59835.0]），planner-on 改 DONE/零异常/engaged 冒烟；旧 planner-on 冻结值文件头留档已废；门默认口径 62P+4xf 不变（commit dfcf476） |
| 2026-09-21 | B2 签名登记 | robust_select→robust_selection（对齐责任文档命名）；返回结构 dict{best,ranking,strategy,tie_break,aggregates}（旧码同构） |
| 2026-09-21 | 批次计划建立 | 15 批（B1 共享基座 → B15 治理层）；波序对齐 responsibility.md 四波；run_submission_agent 因 10 函数超 8 切 B12/B13 两批 |
