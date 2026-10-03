# functions.md —— 函数级实现清单（唯一状态真值）
> fn-implement 独占更新。**代码是真值，本表只是导航。**
> **改任何状态前必须先跑核验命令、在对话中贴出输出，绿了才许改。**

| 函数 | 批次 | 状态(日期) | 核验命令+摘要 | commit |
|---|---|---|---|---|
| load_config | B1 | stub | 测试: tests/shared/test_load_config.py | — |
| open_run_dir | B1 | stub | 测试: tests/shared/test_open_run_dir.py | — |
| append_record | B1 | stub | 测试: tests/shared/test_append_record.py | — |
| load_model_artifact | B1 | stub | 测试: tests/shared/test_load_model_artifact.py | — |
| inject_scenario_fault | B2 | stub | 测试: tests/shared/test_inject_scenario_fault.py | — |
| run_eval | B12 | stub | 继承 R2/R3/R4 验收（eval CLI 本体） | — |
| connect_sitl | B2 | stub | 上游覆盖: run_ingest | — |
| normalize_telemetry | B2 | stub | 测试: tests/run_ingest/test_normalize_telemetry.py | — |
| aggregate_imu_features | B2 | stub | 测试: tests/run_ingest/test_aggregate_imu_features.py | — |
| compute_physical_margins | B2 | stub | 测试: tests/run_ingest/test_compute_physical_margins.py | — |
| replay_check | B2 | stub | 继承 R1 验收（自身即验收命令） | — |
| run_ingest | B2 | stub | 继承 R1 验收（replay_check CLI 本体） | — |
| estimate_distance_trend | B3 | stub | 测试: tests/run_link_consistency/test_estimate_distance_trend.py | — |
| consistency_residual | B3 | stub | 测试: tests/run_link_consistency/test_consistency_residual.py | — |
| run_link_consistency | B3 | stub | 继承 R4 验收（eval --scenario link_degrade） | — |
| build_residuals | B4 | stub | 测试: tests/run_sudden_fault/test_build_residuals.py | — |
| cusum_detect | B4 | stub | 测试: tests/run_sudden_fault/test_cusum_detect.py | — |
| classify_fault | B4 | stub | 测试: tests/run_sudden_fault/test_classify_fault.py | — |
| run_sudden_fault | B4 | stub | 继承 R3 验收（eval --scenario motor_fail） | — |
| build_feature_window | B5 | stub | 测试: tests/run_progressive_risk/test_build_feature_window.py | — |
| predict_risk_tcn | B5 | stub | 测试: tests/run_progressive_risk/test_predict_risk_tcn.py | — |
| calibrate_conformal | B5 | stub | 测试: tests/run_progressive_risk/test_calibrate_conformal.py | — |
| check_physical_baseline | B5 | stub | 测试: tests/run_progressive_risk/test_check_physical_baseline.py | — |
| train_tcn | B5 | stub | 测试: tests/run_progressive_risk/test_train_tcn.py | — |
| run_progressive_risk | B5 | stub | 继承 R2 验收（eval --scenario lowbat_headwind） | — |
| update_state | B6 | stub | 测试: tests/run_safety_state_machine/test_update_state.py | — |
| plan_disposal | B6 | stub | 测试: tests/run_safety_state_machine/test_plan_disposal.py | — |
| run_safety_state_machine | B6 | stub | 继承 R6 验收判据（eval 全场景证据链+迟滞） | — |
| discover_device_module | B7 | stub | 测试: tests/run_device_bus/test_discover_device_module.py | — |
| health_check_module | B7 | stub | 测试: tests/run_device_bus/test_health_check_module.py | — |
| route_device_frames | B7 | stub | 测试: tests/run_device_bus/test_route_device_frames.py | — |
| run_device_bus | B7 | stub | 继承 R10 验收（拔插模块判据；单测同左） | — |
| replay_spectrum_source | B8 | stub | 测试: tests/run_spectrum_monitor/test_replay_spectrum_source.py | — |
| capture_spectrum | B8 | stub | 测试: tests/run_spectrum_monitor/test_capture_spectrum.py | — |
| compute_occupancy | B8 | stub | 测试: tests/run_spectrum_monitor/test_compute_occupancy.py | — |
| run_spectrum_monitor | B8 | stub | 继承 R5 验收（sdr_check 双源自检） | — |
| sdr_check | B8 | stub | 继承 R5 验收（自身即验收命令） | — |
| pipe_events | B9 | stub | 测试: tests/run_ground_station/test_pipe_events.py | — |
| register_pages | B9 | stub | 测试: tests/run_ground_station/test_register_pages.py | — |
| run_ground_station | B9 | stub | 继承 R7 验收（一键启动五页可看） | — |
| spawn_sitl | B10 | stub | 测试: tests/launch_demo_session/test_spawn_sitl.py | — |
| render_console | B10 | stub | 测试: tests/launch_demo_session/test_render_console.py | — |
| session_control_api | B10 | stub | 测试: tests/launch_demo_session/test_session_control_api.py | — |
| launch_demo_session | B10 | stub | 继承 R9 验收（浏览器全流程判据） | — |
| export_metrics_table | B11 | stub | 测试: tests/build_materials/test_export_metrics_table.py | — |
| draft_revision_notes | B11 | stub | 测试: tests/build_materials/test_draft_revision_notes.py | — |
| compile_documents | B11 | stub | 继承 doc-compile 验收（docs/build.py 本体） | — |
| build_materials | B11 | stub | 继承 R8 验收（doc-compile + doc-numbers） | — |
