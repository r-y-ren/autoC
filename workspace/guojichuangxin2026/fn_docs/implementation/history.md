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
