# 责任划分（fn-divide 产物·由已确认的 R1–R13 派生）

> 2026-10-03 随 fn-scaffold 生成；包名 `linkbench`（弃用 `platform`——遮蔽标准库）。
> 顶层函数=文件、子函数就近、共享子函数进 shared/；tests/ 按模块镜像（扁平文件）；环境文件在 software/ 根。

## R → 顶层函数 → 文件 → 测试 → 验收命令

| R | 顶层函数/类 | 文件（software/ 下） | 测试 | 验收命令（蓝图） |
|---|---|---|---|---|
| R1 | generate_interference | linkbench/gen/generator.py（子：styles.py 六构建器） | tests/test_gen.py | sw-boot / `python -m linkbench.gen` |
| R2 | run_calibration | linkbench/calibrate/calibrate.py（子：gain_map.py） | tests/test_calibrate.py | （m1 内部门：monotonic_ok） |
| R3 | watch_links | linkbench/dut/collector.py（子：serial_link/fake_dut） | tests/test_dut.py | sw-boot（DUT 空跑并入冒烟） |
| R4 | record_run | linkbench/record/recorder.py（子：monitor.py） | tests/test_record.py | sw-loop |
| R5 | run_scenario | linkbench/runner/runner.py（子：stepper/fail_criteria） | tests/test_runner.py | sw-loop / sw-gb42590（scripts/run_scenario.py） |
| R6 | check_dataset | linkbench/dataset/indexer.py（子：sigmf_validate） | tests/test_dataset.py | sw-dataset（scripts/check_dataset.py） |
| R7 | train_model / evaluate / predict_styles | linkbench/train/trainer.py + predict/predictor.py（子：spectrogram/cv_grouped/remote） | tests/test_train.py / test_predict.py | sw-ai（scripts/eval_jamming_cls.py） |
| R8 | demo / build_report / plot_triple_curves | linkbench/demo/demo.py + report/{builder,curves}.py | tests/test_demo_report.py | sw-demo（scripts/demo.py） |
| R9 | JammerSource / SpectrumAnalyzer（+B210/PyVISA 后端） | linkbench/instruments/{base,b210_backend,pyvisa_backend}.py | tests/test_sitl_instruments.py | 代码审查（无旁路调用） |
| R10 | inject_profile | linkbench/sitl/bridge.py | tests/test_sitl_instruments.py | 联调记录（人工+自动混合） |
| R11 | create_app / serve / register_api / WsHub | linkbench/ui/{server,api,ws_hub}.py + static/ | tests/test_ui.py | sw-ui-boot（ui_selftest.py） |
| R12 | （并入 register_api 的卡片/报告端点） | linkbench/ui/api.py | tests/test_ui.py | man-ui-demo + sw-ui-boot |
| R13 | initAnim / driveAnim / styleToWave | linkbench/ui/static/anim.js（app.js 配套） | tests/test_ui.py（资源+标记扫描） | man-ui-demo（联动判据） |
| 共享 | load_scenario / write|read_sigmf / now_ms / EstopManager | linkbench/shared/{scenario,sigmf_io,clock,safety}.py | tests/test_shared.py | sw-boot 内含 |
| 固件 | emit_sample（×2 链路） | hardware/firmware/{esp32_link,nrf24_link}/src/main.cpp | （PlatformIO 编译） | hw-fw（build_all.py） |

## 桩标记约定

- Python：`raise NotImplementedError("unimplemented:fn:<名>")`；JS：`throw new Error("unimplemented:fn:<名>")`；C++：`// unimplemented:fn:<名>` 注释 + 空实现。
- hw-fw 验收命令调整为 `python3 workspace/chuangxin2026/hardware/firmware/build_all.py`（双工程顺序编译；蓝图随本次变更）。
