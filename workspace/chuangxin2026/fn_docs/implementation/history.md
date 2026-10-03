# history.md —— 历史表（已完成批次队列，只追加不删改）

> fn-implement 独占更新。每批次完成后尾部追加留痕。

| 完成日期 | 批次 | 任务/函数清单（含操作与来源说明） | 验收摘要 |
|---|---|---|---|
| 10-03 | B1 | load_scenario, write_sigmf, read_sigmf, EstopManager, make_spectrogram | 15 单测绿；四张场景卡真实载入（含 nojam 注入为 None、国标卡 -5/5 口径断言） |
| 10-03 | B2 | create_instrument_backend（含 backends.py 子树：Mock/B210/PyVisa 三后端） | 5 单测绿；mock 后端工厂实跑、未知名拒绝、b210 缺 UHD 给可操作提示 |
| 10-03 | B3 | synthesize_style, generate_jamming（styles 注册表=样式插槽；gen.py 入口实装） | 11 单测绿；dry-run 不发射断言、mock 全路径 SigMF 真值可读回、注册表与 KNOWN_STYLES 一致性 |
| 10-03 | B4 | parse_serial_line, start_dut_source, collect_dut_samples | 11 单测绿；合成源台阶与 jammer 功率响应、失联 gap 不中断、真实/合成同接口 |
| 10-03 | B5 | compute_spectrum_stats, record_run_streams（kw jammer/extra_events 签名微调已登记） | 4 单测绿；谱峰位断言、三路文件齐、注入事件入 JSONL、覆盖率≥0.9 |
| 10-03 | B6 | plot_triple_curves, build_report（steps.jsonl 联表=JSR 轴；缺表时间轴兜底） | 4 单测绿；三图产出+无步进兜底+报告含固定声明与失效电平行 |
| 10-03 | B7 | calibrate_power(并批补洞)+plan_steps+check_failure+execute_scenario；夹具判据修正+增益排序 bug 修复 | 10 单测绿（executor 8+calibrate 2）；国标卡实测出失效电平、对照卡零误报、报告自动生成 |
| 10-03 | B8+B10 | index_dataset, predict_style（npz 模型契约键与训练侧一致；修测试 fftshift 半区权重笔误） | 2 单测绿 |
| 10-03 | B9 | grouped_cv_split, train_classifier（本地 softmax 降级路径；toolbox 派发占位） | 3 单测绿；分组 CV 同组同侧、端到端 F1≥0.9、npz 模型跨模块契约 |
| 10-03 | B11+B12 | run_demo, serve_console（内嵌单页+急停硬通道）；顺修 generate_jamming out_dir 拼层 bug（树内函数、B3 回归同批跑） | 4 单测绿+ui_selftest rc=0；demo 一条命令三件产出 |
| 10-03 | B13+B14 | bridge_to_sitl [P1], animate_link_state [P1] | 3 单测绿；**27/27 函数全部 wired——fn-implement 全批次完成** |
| 10-03 | 评审修复轮 | 双轴评审 4 项需修中 4 项当场闭环（三 CLI 入口/estop 联通/serial seq/步距告警+弱断言与文档行修正）；2 项结构性留批间门裁决（execute 复用 record/标定、断点续跑） | 全量测试绿复跑 |
| 10-03 | B15（演进一） | launch_console/render_static_pages/register_cjk_font + serve_console 改造落位 + 字体接入两绘图方 + legend 守卫 | 全量 77 绿；start --selfcheck rc=0；-W error 三图零告警 |
| 10-03 | B16（演进一） | scaled_criteria/apply_calibration/resume_from 三叶 + execute_scenario 与 build_report [改造] 落位 | 全量 83 绿；40 速国标卡报出失效电平+加速脚注、半程 run 续跑补齐且首步保留、标定表已应用入报告 |
