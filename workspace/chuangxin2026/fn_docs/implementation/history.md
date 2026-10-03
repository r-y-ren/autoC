# history.md —— 历史表（已完成批次队列，只追加不删改）

> fn-implement 独占更新。每批次完成后尾部追加留痕。

| 完成日期 | 批次 | 任务/函数清单（含操作与来源说明） | 验收摘要 |
|---|---|---|---|
| 10-03 | B1 | load_scenario, write_sigmf, read_sigmf, EstopManager, make_spectrogram | 15 单测绿；四张场景卡真实载入（含 nojam 注入为 None、国标卡 -5/5 口径断言） |
| 10-03 | B2 | create_instrument_backend（含 backends.py 子树：Mock/B210/PyVisa 三后端） | 5 单测绿；mock 后端工厂实跑、未知名拒绝、b210 缺 UHD 给可操作提示 |
| 10-03 | B3 | synthesize_style, generate_jamming（styles 注册表=样式插槽；gen.py 入口实装） | 11 单测绿；dry-run 不发射断言、mock 全路径 SigMF 真值可读回、注册表与 KNOWN_STYLES 一致性 |
| 10-03 | B4 | parse_serial_line, start_dut_source, collect_dut_samples | 11 单测绿；合成源台阶与 jammer 功率响应、失联 gap 不中断、真实/合成同接口 |
| 10-03 | B5 | compute_spectrum_stats, record_run_streams（kw jammer/extra_events 签名微调已登记） | 4 单测绿；谱峰位断言、三路文件齐、注入事件入 JSONL、覆盖率≥0.9 |
