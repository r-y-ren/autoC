# history.md —— 历史表（已完成批次队列，只追加不删改）

> fn-implement 独占更新。每批次完成后尾部追加留痕。

| 完成日期 | 批次 | 任务/函数清单（含操作与来源说明） | 验收摘要 |
|---|---|---|---|
| 10-03 | B1 | load_scenario, write_sigmf, read_sigmf, EstopManager, make_spectrogram | 15 单测绿；四张场景卡真实载入（含 nojam 注入为 None、国标卡 -5/5 口径断言） |
| 10-03 | B2 | create_instrument_backend（含 backends.py 子树：Mock/B210/PyVisa 三后端） | 5 单测绿；mock 后端工厂实跑、未知名拒绝、b210 缺 UHD 给可操作提示 |
