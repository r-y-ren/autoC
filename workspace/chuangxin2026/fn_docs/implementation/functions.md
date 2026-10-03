# functions.md —— 函数级实现清单（唯一状态真值）

> fn-implement 独占更新。**代码是真值，本表只是导航。**
> **改任何状态前必须先跑核验命令、在对话中贴出输出，绿了才许改。**

| 函数 | 批次 | 状态(日期) | 核验命令+摘要 | commit |
|---|---|---|---|---|
| load_scenario | B1 | stub (10-03) | pytest tests/src/shared/load_scenario.py → 桩断言过 | 31106ded |
| write_sigmf | B1 | tested (10-03) | pytest tests/src/shared → 15 passed | 0c62831c |
| read_sigmf | B1 | tested (10-03) | pytest tests/src/shared → 15 passed | 0c62831c |
| EstopManager | B1 | tested (10-03) | pytest tests/src/shared → 15 passed | 0c62831c |
| make_spectrogram | B1 | tested (10-03) | pytest tests/src/shared → 15 passed | 0c62831c |
| create_instrument_backend | B2 | wired (10-03) | pytest tests/src/create_instrument_backend → 5 passed；mock 对偶实跑+b210 缺驱动提示断言 | fa9bf5f8 |
| synthesize_style | B3 | tested (10-03) | pytest tests/src/generate_jamming → 11 passed | acdfbcab |
| generate_jamming | B3 | wired (10-03) | 同批 9 passed + gen 入口 dry-run 实跑 rc=0 | acdfbcab |
| parse_serial_line | B4 | tested (10-03) | pytest tests/src/collect_dut_samples → 11 passed | 08b08193 |
| start_dut_source | B4 | tested (10-03) | 同批 11 passed（jammer 响应/失联/dead_at） | 08b08193 |
| collect_dut_samples | B4 | wired (10-03) | 同批 11 passed（双源+gap 续采+回调） | 08b08193 |
| compute_spectrum_stats | B5 | tested (10-03) | pytest tests/src/record_run_streams → 4 passed | 2c987515 |
| record_run_streams | B5 | wired (10-03) | 同批 4 passed（三路落盘+覆盖率≥0.9+extra_events） | 2c987515 |
| plot_triple_curves | B6 | tested (10-03) | pytest tests/src/build_report → 4 passed | 55e2edc6 |
| build_report | B6 | wired (10-03) | 同批 4 passed（声明+失效行+图嵌入断言） | 55e2edc6 |
| plan_steps | B7 | stub (10-03) | 桩断言过 | 31106ded |
| check_failure | B7 | stub (10-03) | 桩断言过 | 31106ded |
| execute_scenario | B7 | stub (10-03) | 桩断言过 | 31106ded |
| index_dataset | B8 | stub (10-03) | 桩断言过 | 31106ded |
| grouped_cv_split | B9 | stub (10-03) | 桩断言过 | 31106ded |
| train_classifier | B9 | stub (10-03) | 桩断言过 | 31106ded |
| predict_style | B10 | stub (10-03) | 桩断言过 | 31106ded |
| run_demo | B11 | stub (10-03) | 桩断言过 | 31106ded |
| serve_console | B12 | stub (10-03) | 桩断言过 | 31106ded |
| bridge_to_sitl | B13 | stub (10-03) | 桩断言过 | 31106ded |
| animate_link_state | B14 | stub (10-03) | 桩断言过 | 31106ded |

（状态：stub / implemented / tested / wired 日期 / blocked: 一句原因；全函数按依赖序平铺）
