# functions.md —— 函数级实现清单（唯一状态真值）
> fn-implement 独占更新。**代码是真值，本表只是导航。**
> **改任何状态前必须先跑核验命令、在对话中贴出输出，绿了才许改。**

| 函数 | 批次 | 状态(日期) | 核验命令+摘要 | commit |
|---|---|---|---|---|
| load_config | B1 | tested | 测试: tests/shared/test_load_config.py → 4 passed | 36178fc6 |
| open_run_dir | B1 | tested | 测试: tests/shared/test_open_run_dir.py → 2 passed | 36178fc6 |
| append_record | B1 | tested | 测试: tests/shared/test_append_record.py → 2 passed | 36178fc6 |
| load_model_artifact | B1 | tested | 测试: tests/shared/test_load_model_artifact.py → 3 passed | 36178fc6 |
| inject_scenario_fault | B2 | tested | 测试: tests/shared/test_inject_scenario_fault.py | 59252ced |
| run_eval | B12→B18→B19 | wired 10-06 | 继承 R2/R3/R4 验收（eval CLI 本体） | a419a834 |
| connect_sitl | B2 | tested | 上游覆盖: run_ingest | 59252ced |
| normalize_telemetry | B2 | tested | 测试: tests/run_ingest/test_normalize_telemetry.py | 59252ced |
| aggregate_imu_features | B2 | tested | 测试: tests/run_ingest/test_aggregate_imu_features.py | 59252ced |
| compute_physical_margins | B2 | tested | 测试: tests/run_ingest/test_compute_physical_margins.py | 59252ced |
| replay_check | B2 | wired 10-03 | 继承 R1 验收（自身即验收命令） | 59252ced |
| run_ingest | B2 | wired 10-03 | 继承 R1 验收（replay_check CLI 本体） | 59252ced |
| estimate_distance_trend | B3 | tested | 测试: tests/run_link_consistency/test_estimate_distance_trend.py | 2c5f0884 |
| consistency_residual | B3 | tested | 测试: tests/run_link_consistency/test_consistency_residual.py | 2c5f0884 |
| run_link_consistency | B3 | wired 10-03 | 继承 R4 验收（eval --scenario link_degrade） | 2c5f0884 |
| build_residuals | B4 | tested | 测试: tests/run_sudden_fault/test_build_residuals.py | 2c5f0884 |
| cusum_detect | B4 | tested | 测试: tests/run_sudden_fault/test_cusum_detect.py | 2c5f0884 |
| classify_fault | B4 | tested | 测试: tests/run_sudden_fault/test_classify_fault.py | 2c5f0884 |
| run_sudden_fault | B4 | wired 10-03 | 继承 R3 验收（eval --scenario motor_fail） | 2c5f0884 |
| build_feature_window | B5 | tested | 测试: tests/run_progressive_risk/test_build_feature_window.py | fd00472b |
| predict_risk_tcn | B5 | tested | 测试: tests/run_progressive_risk/test_predict_risk_tcn.py | fd00472b |
| calibrate_conformal | B5→B18 | wired 10-06 | 测试: tests/run_progressive_risk/test_calibrate_conformal.py | fd00472b |
| check_physical_baseline | B5 | tested | 测试: tests/run_progressive_risk/test_check_physical_baseline.py | fd00472b |
| train_tcn | B5→B18 | wired 10-06 | 测试: tests/run_progressive_risk/test_train_tcn.py | fd00472b |
| run_progressive_risk | B5 | wired 10-03 | 继承 R2 验收（eval --scenario lowbat_headwind） | fd00472b |
| update_state | B6 | tested | 测试: tests/run_safety_state_machine/test_update_state.py | eede9a3c |
| plan_disposal | B6 | tested | 测试: tests/run_safety_state_machine/test_plan_disposal.py | eede9a3c |
| run_safety_state_machine | B6 | wired 10-03 | 继承 R6 验收判据（eval 全场景证据链+迟滞） | eede9a3c |
| discover_device_module | B7 | tested | 测试: tests/run_device_bus/test_discover_device_module.py | eede9a3c |
| health_check_module | B7 | tested | 测试: tests/run_device_bus/test_health_check_module.py | eede9a3c |
| route_device_frames | B7 | tested | 测试: tests/run_device_bus/test_route_device_frames.py | eede9a3c |
| run_device_bus | B7 | wired 10-03 | 继承 R10 验收（拔插模块判据；单测同左） | eede9a3c |
| replay_spectrum_source | B8 | tested | 测试: tests/run_spectrum_monitor/test_replay_spectrum_source.py | 3d6d6f53 |
| capture_spectrum | B8 | tested | 测试: tests/run_spectrum_monitor/test_capture_spectrum.py | 3d6d6f53 |
| compute_occupancy | B8 | tested | 测试: tests/run_spectrum_monitor/test_compute_occupancy.py | 3d6d6f53 |
| run_spectrum_monitor | B8 | wired 10-03 | 继承 R5 验收（sdr_check 双源自检） | 3d6d6f53 |
| sdr_check | B8 | wired 10-03 | 继承 R5 验收（自身即验收命令） | 3d6d6f53 |
| pipe_events | B9 | tested | 测试: tests/run_ground_station/test_pipe_events.py | 2f17e43a |
| register_pages | B9→B18 | wired 10-06 | 测试: tests/run_ground_station/test_register_pages.py | 2f17e43a |
| run_ground_station | B9 | wired 10-03 | 继承 R7 验收（一键启动五页可看） | 2f17e43a |
| spawn_sitl | B10 | tested | 测试: tests/launch_demo_session/test_spawn_sitl.py | 2f17e43a |
| render_console | B10→B18 | wired 10-06 | 测试: tests/launch_demo_session/test_render_console.py | 2f17e43a |
| session_control_api | B10→B18 | wired 10-06 | 测试: tests/launch_demo_session/test_session_control_api.py | 2f17e43a |
| launch_demo_session | B10 | wired 10-03 | 继承 R9 验收（浏览器全流程判据） | 2f17e43a |
| export_metrics_table | B11→B19 | wired 10-06 | 测试: tests/build_materials/test_export_metrics_table.py | a419a834 |
| draft_revision_notes | B11→B18 | wired 10-06 | 测试: tests/build_materials/test_draft_revision_notes.py | a419a834 |
| compile_documents | B11 | wired 10-03 | 继承 doc-compile 验收（docs/build.py 本体） | a419a834 |
| build_materials | B11 | wired 10-03 | 继承 R8 验收（doc-compile + doc-numbers） | a419a834 |
| archive_run | B13 | tested | 测试: tests/shared/test_archive_run.py | — |
| batch_eval | B13→B19 | wired 10-06 | 继承 R11 验收（runs≥90 归档+data_source 标注） | — |
| probe_px4_env | B13 | tested | 测试: tests/batch_eval/test_probe_px4_env.py | — |
| boot_selfcheck | B14 | wired 10-03 | 继承 R13 验收（三步 PASS） | — |
| probe_service | B14 | tested | 测试: tests/boot_selfcheck/test_probe_service.py | — |
| bench_edge | B15 | wired 10-03 | 继承 R14 验收（dry-run PASS） | — |
| calibrate_usrp | B15 | wired 10-03 | 继承 R14 验收（dry-run 参考表） | — |
| build_package | B16→B19 | wired 10-06 | 继承 R15 验收（干净 venv pip install+demo 起） | — |
| write_user_manual | B16 | tested | 测试: tests/build_package/test_write_user_manual.py | — |
| soak_test | B17 | wired 10-03 | 继承 R16 验收（--quick 微缩+留痕） | — |
| make_portable_bundle | B17 | wired 10-03 | 继承 R16 验收（tar 结构+SHA256） | — |
| _deep_merge | B18 | tested | 上游覆盖: 宿主函数（2026-10-06 审计补记） | 083be0cc |
| _validate | B18 | tested | 上游覆盖: 宿主函数（2026-10-06 审计补记） | 083be0cc |
| _percentile | B18 | tested | 上游覆盖: 宿主函数（2026-10-06 审计补记） | 083be0cc |
| _crit_frame | B18 | tested | 上游覆盖: 宿主函数（2026-10-06 审计补记） | 083be0cc |
| _lead_metrics | B18 | tested | 上游覆盖: 宿主函数（2026-10-06 审计补记） | 083be0cc |
| _arm_takeoff | B18 | tested | 上游覆盖: 宿主函数（2026-10-06 审计补记） | 083be0cc |
| _get | B18 | tested | 上游覆盖: 宿主函数（2026-10-06 审计补记） | 083be0cc |
| _put | B18 | tested | 上游覆盖: 宿主函数（2026-10-06 审计补记） | 083be0cc |
| _nan | B18 | tested | 上游覆盖: 宿主函数（2026-10-06 审计补记） | 083be0cc |
| _clamp01 | B18 | tested | 上游覆盖: 宿主函数（2026-10-06 审计补记） | 083be0cc |
| _home_dist_m | B18 | tested | 上游覆盖: 宿主函数（2026-10-06 审计补记） | 083be0cc |
| _load_run | B18 | tested | 上游覆盖: 宿主函数（2026-10-06 审计补记） | 083be0cc |
| _labels_for | B18 | tested | 上游覆盖: 宿主函数（2026-10-06 审计补记） | 083be0cc |
| make_dataset | B18 | tested | 上游覆盖: 宿主函数（2026-10-06 审计补记） | 083be0cc |
| _probe_fit | B18 | tested | 上游覆盖: 宿主函数（2026-10-06 审计补记） | 083be0cc |
| _window_summary | B18 | tested | 上游覆盖: 宿主函数（2026-10-06 审计补记） | 083be0cc |
| _sparse_recall | B18 | tested | 上游覆盖: 宿主函数（2026-10-06 审计补记） | 083be0cc |
| _dist | B18 | tested | 上游覆盖: 宿主函数（2026-10-06 审计补记） | 083be0cc |
| _dist_from_ref | B18 | tested | 上游覆盖: 宿主函数（2026-10-06 审计补记） | 083be0cc |
| _score | B18 | tested | 上游覆盖: 宿主函数（2026-10-06 审计补记） | 083be0cc |
| _params_for | B18 | tested | 上游覆盖: 宿主函数（2026-10-06 审计补记） | 083be0cc |
| _probe_usrp | B18 | tested | 上游覆盖: 宿主函数（2026-10-06 审计补记） | 083be0cc |
| _probe_ssh | B18 | tested | 上游覆盖: 宿主函数（2026-10-06 审计补记） | 083be0cc |
| _build | B18 | tested | 上游覆盖: 宿主函数（2026-10-06 审计补记） | 083be0cc |
| make_usrp_stream | B18 | tested | 上游覆盖: 宿主函数（2026-10-06 审计补记） | 083be0cc |
| _freq_axis | B18 | tested | 上游覆盖: 宿主函数（2026-10-06 审计补记） | 083be0cc |
| _lift | B18 | tested | 上游覆盖: 宿主函数（2026-10-06 审计补记） | 083be0cc |
| _make_fixture | B18 | tested | 上游覆盖: 宿主函数（2026-10-06 审计补记） | 083be0cc |
| _page | B18 | tested | 上游覆盖: 宿主函数（2026-10-06 审计补记） | 083be0cc |
| _ensure_model | B18→B19 | wired 10-06 | 上游覆盖: 宿主函数（2026-10-06 审计补记） | 083be0cc |
| _already_archived | B18 | tested | 上游覆盖: 宿主函数（2026-10-06 审计补记） | 083be0cc |
| render_device_panel | B20 | stub | 测试: tests/shared/test_render_device_panel.py | — |