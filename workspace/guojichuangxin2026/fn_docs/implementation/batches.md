# batches.md —— 批次表（待办导航）
> fn-implement 独占更新。▶ = 下一批要完成的任务；未经批间门批准不得增删批次内容。
> **全部 17 批已完成（首轮 12+演进 5，2026-10-03）**——批次表清空，留痕见 history.md。
> 依赖序自底向上：B1 地基 → 数据接入 → 检测通道 → 决策 → 设备/平台/控制台 → 材料/评估集成。
> 单批 ≥6 函数的批次（B2/B5）建议子代理逐函数档；其余主会话连续档即可。

| 批次 | 函数/任务清单 | 验收点 | 注 |
|---|---|---|---|

| 2026-10-03 | 签名微调 | spawn_sitl 增 synthetic 备选（设备缺席等价数据面）；EventHub 增 publish_sync（会话线程侧发布）；控制台模板寄宿 run_ground_station.console_page → 归位 launch_demo_session.render_console |


## 变更记录
| 2026-10-08 | B20 实施留痕 | R26 五页统一指挥中心壳+控制台六区（canvas 航迹/仪表/色带）+事件降噪+1Hz nav 帧；R27 render_device_panel（tested）+/api/devices 真值（合成/PX4/SDR/Orin+待接入三件） | 120 tests 绿；boot_selfcheck 三步 PASS |

| 2026-10-08 | 演示链路修复（用户实跑 demo.sh 崩溃指令修复） | ①demo.sh venv 优先（系统 python 缺 uvicorn 根因）②smoke_boot 接 boot_selfcheck 三步真验收③run_ground_station 桥接 app.state.cfg（会话共享平台 hub，SSE 断线根因）——实测 SSE 92 帧事件流、三步自检 PASS | 树内既有单元一行级修复，无新函数 |

| 2026-10-06 | B19 实施留痕 | R23 _ensure_model 选优装载（probe/tcn/回退三分支+train_report 补 best 落盘）；R25 lead_s 单值+汇总聚合+export 派生键；R24 卫生核验+gitignore runs_*/+git rm --cached 336 产物（索引归零，磁盘保留） | 批内补记：train_report.json 曾漏 best 字段致 winner 不达批量（实证修复） |

| 2026-10-06 | 流程审计补账（R17-R22 执行欠账） | 用户指出 R17-R22 未经 divide/scaffold/implement 正式过门即完成——审计属实：①divide 门口未呈报+31 助手单元未入树（B12 起累积）②scaffold 纯改造豁免不成立（有新单元）③implement 无批表/四态/批间门。补账：31 助手入 responsibility 树与块（[L2|补记]）+类/垫片登记；functions.md 补行+七件改造单元状态刷新；名实漂移修复（session_control_api）；死代码 inject_at_v 删除。B18=补账批次 |
（计划层事件：签名微调、需求变更往返、放弃等）
| 日期 | 事件 | 说明 |
|---|---|---|
| 2026-10-03 | 签名微调 | open_run_dir 增可选 config_snapshot 参数（运行清单落配置快照） |
| 2026-10-03 | 实现内修正 | B3/B4 缺陷修复：dB 残差模型重构/CUSUM 零值键污染/距离参考点对齐（非结构变化） |
| 2026-10-06 | P7 实施留痕 | PX4 真源接通实施内修复集：run_eval PX4 分支（spawn/udpin 连接/定时注入/强制解锁+AUTO.TAKEOFF 模式编码修正）、replay_check 暖机豁免+rssi 降可选（PX4 SITL 无无线电消息）、spawn_sitl 进程组回收+sihsim_quadx 口径、batch_eval 归档根修正（战役 fn_docs/results）；诊断四号实证 SIH 低空限制（电机响应、爬升≈0.3m）——场景事件指标以合成源为准、PX4 源为数据面验证，如实两源口径 |
| 2026-10-03 | 演进轮记账 | divide 门预登记 functions.md stub 行与 B13-B17 批（lint 一致性要求；实现期由 fn-implement 独占续写）；run_eval 改造并入原块（唯一名约束，[改造] 标注） |
| 2026-10-03 | 预授权 | 用户字面授权"剩下的批次一并完成"→批间门不停人，核验照跑照贴 |
