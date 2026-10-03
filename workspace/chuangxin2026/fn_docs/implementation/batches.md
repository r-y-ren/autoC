# batches.md —— 批次表（待办导航）

> fn-implement 独占更新。▶ = 下一批要完成的任务；未经批间门批准不得增删批次内容。
> wired 验收一律先走 mock 后端+合成链路（模块化插槽使然）；真实射频/真实串口/浏览器走查=蓝图人工项。

| 批次 | 函数/任务清单 | 验收点 | 注 |
|---|---|---|---|
| B1 | shared×5：load_scenario, write_sigmf, read_sigmf, EstopManager, make_spectrogram | 五函数 tested 自有单测绿；四张场景卡真实载入通过 | 共享基座，服务全部顶层 |
| B2 | create_instrument_backend | wired：mock 后端工厂实跑；b210/pyvisa 惰性分支+缺驱动报错路径 | 仪表插槽；后端类实现于本包内 |
| B3 | synthesize_style → generate_jamming | generate_jamming wired：mock 后端 dry-run 参数表+短跑落 SigMF（合成路径） | 真实射频=人工项 man-lab |
| B4 | parse_serial_line → start_dut_source → collect_dut_samples | collect_dut_samples wired：合成源连续流+gap 事件+真实/合成同接口 | 链路插槽；真实串口=人工项 |
| B5 | compute_spectrum_stats → record_run_streams | record_run_streams wired：合成三路 60s 落盘+覆盖率≥99% | |
| B6 | plot_triple_curves → build_report | build_report wired：合成 run 夹具→report.md+三图 | |
| B7 | calibrate_power(并批), plan_steps, check_failure → execute_scenario | execute_scenario wired：mock+合成链路双卡实跑（国标卡失效电平+对照不误报） | R5 主验收 |
| B8 | index_dataset | wired：夹具目录（含一条坏录制）校验+索引 | |
| B9 | grouped_cv_split → train_classifier | wired：小合成数据集端到端（分组 CV 报告；本地 CPU 路径） | /toolbox 远程路径另测 |
| B10 | predict_style | wired：合成模型+录制预测与真值并列 | |
| B11 | run_demo | wired：quick 合成路径一条命令 | |
| B12 | serve_console | wired：selftest 四点（TestClient 无头） | 浏览器零代码走查=人工项 man-ui-demo |
| B13 | bridge_to_sitl [P1] | wired：mock SITL 注入台阶对应 | 预研深度可裁 |
| B14 | animate_link_state [P1] | 上游覆盖（serve_console 联动判据） | 非阻塞，有余力做 |

| ▶ B16 | scaled_criteria, apply_calibration, resume_from + execute_scenario/build_report 改造 | 40 速国标卡出失效电平+脚注；半程续跑；标定入报告 | 演进轮一 |
| B17 | build_mid_material + docs/build.py | build --mid 产材料稿+数字溯源断言 | 演进轮一 |

## 变更记录（计划层事件：签名微调、需求变更往返、放弃等）

| 日期 | 事件 | 说明 |
|---|---|---|
| 2026-10-03 | 计划补洞 | calibrate_power（R2 顶层）原漏于批次表，并入 B7 一并实现 |
| 2026-10-03 | 评审修复+签名微调 | execute_scenario 增 kw estop（操控台急停联通）；calibrate_power 增 warnings（步距偏差>1dB）；补 scripts/record·calibrate·sitl_bridge 三入口（消除死代码 FAIL）；serial seq 记忆改会话级；sitl note 如实化 |
| 2026-10-03 | 签名微调 | record_run_streams 增 kw jammer/extra_events（执行器联动监测与事件注入，意图级签名不变） |
| 2026-10-03 | 批次计划立表 | 入口对账：fn-check 残留桩 31（=scaffold 真值）、全量测试 27/27 PASS、镜像齐全；14 批垂直切片覆盖全部 27 函数 |
