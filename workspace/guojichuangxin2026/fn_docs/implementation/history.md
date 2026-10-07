# history.md —— 历史表（已完成批次队列，只追加不删改）
> fn-implement 独占更新。每批次完成后尾部追加留痕。

| 完成日期 | 批次 | 任务/函数清单（含操作与来源说明） | 验收摘要 |
|---|---|---|---|
| 2026-10-03 | B1 | load_config, open_run_dir, append_record, load_model_artifact | pytest tests/shared → 11 passed 2 skipped（B1 四件单测全绿；2 skip=B2/B12 占位） |
| 2026-10-03 | B2 | connect_sitl, normalize_telemetry, aggregate_imu_features, compute_physical_margins, replay_check(wired), run_ingest(wired), inject_scenario_fault | pytest → 28 passed 1 skipped；run_ingest 实跑 20Hz×30 帧落盘；缺陷修复 4 处（mkdir/def def/state 假值/IMU 时戳） |
| 2026-10-03 | B3 | estimate_distance_trend, consistency_residual, run_link_consistency(wired) | 7 passed；正常零误报+欺骗检出；远距限界记录 |
| 2026-10-03 | B4 | build_residuals, cusum_detect, classify_fault, run_sudden_fault(wired) | 6 passed；电机时延≤0.6s+链路事件+正常静默 |
| 2026-10-03 | B5 | build_feature_window, predict_risk_tcn, calibrate_conformal, check_physical_baseline, train_tcn(wired), run_progressive_risk(wired) | 9 passed；缺陷修复 3（指示位维度/批内窗长不定/训练梯度断链） |
| 2026-10-03 | B6 | update_state, plan_disposal, run_safety_state_machine(wired) | 6 passed；升级直达路径缺陷修复 |
| 2026-10-03 | B7 | discover_device_module, health_check_module, route_device_frames, run_device_bus(wired) | 5 passed；拔插双态切换实证 |
| 2026-10-03 | B8 | replay_spectrum_source, capture_spectrum, compute_occupancy, run_spectrum_monitor(wired), sdr_check(wired) | 7 passed；缺席自动回放+双源同管线 |
| 2026-10-03 | B9 | pipe_events, register_pages, run_ground_station(wired) | 5 passed；五页+分页 API |
| 2026-10-03 | B10 | spawn_sitl, render_console, session_control_api, launch_demo_session(wired) | 5 passed；会话端到端冒烟（tee 分流缺陷修复） |
| 2026-10-03 | B11 | export_metrics_table, draft_revision_notes, compile_documents(wired), build_materials(wired) | 5 passed；端到端两运行目录→三件套产物 |
| 2026-10-03 | B12 | run_eval(wired)+全链 smoke | 2 passed；motor_fail×2/lowbat×1 批量指标分片；smoke_boot 桩清零 |
| 2026-10-03 | B13 | archive_run(t), run_eval(wired 改造复走), batch_eval(wired), probe_px4_env(t) | 全套 98 passed；confirm=注入→首确认 0.5s 实测；纬度 cos 误乘 5 处修复 | 
| 2026-10-03 | B14 | boot_selfcheck(wired), probe_service(t) | 6 passed；三步自检实跑全 PASS |
| 2026-10-03 | B15 | bench_edge(wired), calibrate_usrp(wired) | 4 passed；dryrun 基准+参考表落档 |
| 2026-10-03 | B16 | build_package(wired), write_user_manual(t) | 4 passed+真构建：wheel 产+干净 venv 装后自测 passed（ahyd_cli 垫片入包） |
| 2026-10-03 | B17 | soak_test(wired), make_portable_bundle(wired) | 4 passed+实产：quick 长跑报告留痕+459MB full 便携包（dist/ 已 gitignore） |
| 2026-10-06 | B18 | R17-R22 执行（train_tcn[改]/calibrate_conformal[改]/draft_revision_notes[改]/register_pages[改]/render_console[改]/run_eval[改]/session_control_api[改]）+31 助手审计补账 | 112 tests 绿；7 提案 achieved；流程欠账由审计补账记录（见 batches 变更记录） |
| 2026-10-06 | B19 | _ensure_model(wired), run_eval[改](wired), export_metrics_table[改](wired), build_package[改](wired), batch_eval[改](wired) | 113 tests 绿；批量实证 note=probe-sel+lead_s=15.5+分片无误导键；索引产物归零 |
