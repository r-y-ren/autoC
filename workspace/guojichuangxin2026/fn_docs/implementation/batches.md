# batches.md —— 批次表（待办导航）
> fn-implement 独占更新。▶ = 下一批要完成的任务；未经批间门批准不得增删批次内容。
> **全部 12 批已完成（2026-10-03）**——批次表清空，留痕见 history.md。
> 依赖序自底向上：B1 地基 → 数据接入 → 检测通道 → 决策 → 设备/平台/控制台 → 材料/评估集成。
> 单批 ≥6 函数的批次（B2/B5）建议子代理逐函数档；其余主会话连续档即可。

| 批次 | 函数/任务清单 | 验收点 | 注 |
|---|---|---|---|

| 2026-10-03 | 签名微调 | spawn_sitl 增 synthetic 备选（设备缺席等价数据面）；EventHub 增 publish_sync（会话线程侧发布）；控制台模板寄宿 run_ground_station.console_page → 归位 launch_demo_session.render_console |

| ▶ B14 | boot_selfcheck, probe_service（smoke_boot 壳接线） | smoke_boot 三步 PASS | R13 |
| B15 | bench_edge, calibrate_usrp | 两脚本 dry-run PASS | R14；真机项列 manual |
| B16 | build_package, write_user_manual | wheel 产+干净 venv 装后 demo 起 | R15 |
| B17 | soak_test, make_portable_bundle | --quick 长跑留痕+tar 包 SHA 过 | R16；1h 全量与目标机解压属 manual |

## 变更记录（计划层事件：签名微调、需求变更往返、放弃等）
| 日期 | 事件 | 说明 |
|---|---|---|
| 2026-10-03 | 签名微调 | open_run_dir 增可选 config_snapshot 参数（运行清单落配置快照） |
| 2026-10-03 | 实现内修正 | B3/B4 缺陷修复：dB 残差模型重构/CUSUM 零值键污染/距离参考点对齐（非结构变化） |
| 2026-10-03 | 演进轮记账 | divide 门预登记 functions.md stub 行与 B13-B17 批（lint 一致性要求；实现期由 fn-implement 独占续写）；run_eval 改造并入原块（唯一名约束，[改造] 标注） |
| 2026-10-03 | 预授权 | 用户字面授权"剩下的批次一并完成"→批间门不停人，核验照跑照贴 |
