# 包标记（B17 清债）：让本目录测试以 snapshot.test_* 限定名导入，
# 与 fn_work/snapshot_tests/ 的同名测试模块（snapshot_tests.test_*）区分，
# 消除 pytest 全量收集的 "import file mismatch"。不改任何测试语义。
