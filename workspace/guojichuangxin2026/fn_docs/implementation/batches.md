# batches.md —— 批次表（待办导航）
> fn-implement 独占更新。▶ = 下一批要完成的任务；未经批间门批准不得增删批次内容。
> 依赖序自底向上：B1 地基 → 数据接入 → 检测通道 → 决策 → 设备/平台/控制台 → 材料/评估集成。
> 单批 ≥6 函数的批次（B2/B5）建议子代理逐函数档；其余主会话连续档即可。

| 批次 | 函数/任务清单 | 验收点 | 注 |
|---|---|---|---|
| B2 | connect_sitl, normalize_telemetry, aggregate_imu_features, compute_physical_margins, replay_check, run_ingest, inject_scenario_fault | run_ingest wired（SITL 短飞实跑）+ replay_check 可用 | 7 件，建议子代理档 |
| B3 | estimate_distance_trend, consistency_residual, run_link_consistency | run_link_consistency wired | 供 B4 残差通道消费 |
| B4 | build_residuals, cusum_detect, classify_fault, run_sudden_fault | run_sudden_fault wired | 残差通道含 B3 证据 |
| B5 | build_feature_window, predict_risk_tcn, calibrate_conformal, check_physical_baseline, train_tcn, run_progressive_risk | run_progressive_risk wired | 6 件，建议子代理档；train_tcn 需微型数据冒烟 |
| B6 | update_state, plan_disposal, run_safety_state_machine | run_safety_state_machine wired | 消费 B4/B5 事件 |
| B7 | discover_device_module, health_check_module, route_device_frames, run_device_bus | run_device_bus wired（拔插双态用例） | R10 模块化架构 |
| B8 | replay_spectrum_source, capture_spectrum, compute_occupancy, run_spectrum_monitor, sdr_check | sdr_check 双源自检可用 | 依赖 B7 总线 |
| B9 | pipe_events, register_pages, run_ground_station | run_ground_station wired（五页起服务） | 依赖 B8 瀑布流 |
| B10 | spawn_sitl, render_console, session_control_api, launch_demo_session | launch_demo_session wired（SIH 冒烟） | R9 演示控制台 |
| B11 | export_metrics_table, draft_revision_notes, compile_documents, build_materials | build_materials wired | 材料 |
| B12 | run_eval + 全链路 smoke（smoke_boot 实跑） | eval CLI 实跑出指标分片；sw-boot 绿 | 评估集成收官 |

## 变更记录（计划层事件：签名微调、需求变更往返、放弃等）
| 日期 | 事件 | 说明 |
|---|---|---|
| 2026-10-03 | 签名微调 | open_run_dir 增可选 config_snapshot 参数（运行清单落配置快照） |
| 2026-10-03 | 预授权 | 用户字面授权"剩下的批次一并完成"→批间门不停人，核验照跑照贴 |
