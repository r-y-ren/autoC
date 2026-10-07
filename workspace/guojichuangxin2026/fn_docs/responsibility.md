# 责任文档：安航云盾演示系统（材料冲刺版·重开版）
> 由 fn-divide 产出与独占更新；fn-implement 只读。进度与状态见 implementation/。
> 职责字段是**重写规约**：凭职责详述 + 签名意图（输入/输出），必须能完美复现该函数功能。
> ⚠ 实现期发现结构性变化（函数增/删/拆/并/职责或调用关系变化）必须停下回本阶段改本文档。
> ⚠ 函数总数 48 > 20 预警线（计数经命令实测，见自检节）：10 需求口的系统级工程（数据/双通道模型/频谱设备模块/设备总线/状态机/Web/演示控制台/材料），非单一算法任务；门口裁决。

## 结构概览（纯结构，不带职责）
- run_ingest ← R1
  - connect_sitl
  - normalize_telemetry
    - _get
    - _put
  - aggregate_imu_features
  - compute_physical_margins
    - _nan
    - _clamp01
    - _home_dist_m
  - replay_check
- run_progressive_risk ← R2
  - build_feature_window
  - predict_risk_tcn
    - _build
  - calibrate_conformal
  - check_physical_baseline
  - train_tcn
    - _load_run
    - _labels_for
    - make_dataset
    - _probe_fit
    - _window_summary
    - _sparse_recall
- run_sudden_fault ← R3
  - build_residuals
  - cusum_detect
  - classify_fault
- run_link_consistency ← R4
  - _dist_from_ref
  - estimate_distance_trend
  - consistency_residual
- run_spectrum_monitor ← R5
  - _freq_axis
  - capture_spectrum
    - make_usrp_stream
  - replay_spectrum_source
  - compute_occupancy
  - sdr_check
    - _lift
    - _make_fixture
- run_safety_state_machine ← R6
  - update_state
    - _score
  - plan_disposal
    - _dist
- run_ground_station ← R7
  - pipe_events
  - register_pages
    - _page
- build_materials ← R8
  - export_metrics_table
  - draft_revision_notes
  - compile_documents
- launch_demo_session ← R9
  - spawn_sitl
  - session_control_api
  - render_console
- run_device_bus ← R10
  - discover_device_module
    - _probe_usrp
    - _probe_ssh
  - health_check_module
  - route_device_frames
- batch_eval ← R11
  - _ensure_model
  - _already_archived
  - probe_px4_env
- boot_selfcheck ← R13
  - probe_service
- bench_edge ← R14
- calibrate_usrp ← R14
- build_package ← R15
  - write_user_manual
- soak_test ← R16
- make_portable_bundle ← R16
- load_config
  - _deep_merge
  - _validate
- open_run_dir
- append_record
- load_model_artifact
- run_eval
  - _percentile
  - _crit_frame
  - _lead_metrics
  - _arm_takeoff
- inject_scenario_fault
  - _params_for
- archive_run

## 需求覆盖矩阵
| 需求 | 顶层函数 |
|---|---|
| R1 | run_ingest |
| R2 | run_progressive_risk |
| R3 | run_sudden_fault |
| R4 | run_link_consistency |
| R5 | run_spectrum_monitor |
| R6 | run_safety_state_machine |
| R7 | run_ground_station |
| R8 | build_materials |
| R9 | launch_demo_session |
| R10 | run_device_bus |
| R11 | batch_eval |
| R12 | run_eval |
| R13 | boot_selfcheck |
| R14 | bench_edge |
| R15 | build_package |
| R16 | soak_test |
| R17 | run_progressive_risk |
| R18 | run_progressive_risk |
| R19 | build_materials |
| R20 | build_materials |
| R21 | run_ground_station |
| R22 | build_materials |
| R23 | batch_eval |
| R24 | build_package |
| R25 | run_eval |

## 共享函数（shared：多顶层共用；矩阵挂全部受益需求）
- **load_config**（调用方：程序入口, run_ingest, run_progressive_risk, run_sudden_fault, run_link_consistency, run_spectrum_monitor, run_safety_state_machine, run_ground_station, build_materials, launch_demo_session, run_device_bus, run_eval, train_tcn, replay_check, sdr_check）
  - 职责：读取场景定义、阈值、模型路径、运行参数、设备模块清单的 YAML 配置，做模式校验（缺字段/类型错/取值域越界即报错），返回冻结配置对象；默认值集中在默认配置文件，不散落代码。
  - 签名意图：输入: 配置文件路径（可选，缺省读包内默认） / 输出: 冻结配置对象（dataclass 树） / 错误: 配置缺失或校验失败抛 ConfigError 并指明字段
  - tested 策略：自有单测
  - 核验命令：测试: tests/shared/test_load_config.py
- **open_run_dir**（调用方：run_eval, run_ingest, run_spectrum_monitor, launch_demo_session）
  - 职责：创建带时间戳与场景标签的运行目录，落运行清单（配置快照+随机种子+机器信息+设备在场清单），返回目录路径句柄；同秒冲突自动加序号。
  - 签名意图：输入: 根目录, 场景名, 种子 / 输出: 运行目录路径 / 错误: 根目录不可写抛 IOError
  - tested 策略：自有单测
  - 核验命令：测试: tests/shared/test_open_run_dir.py
- **append_record**（调用方：run_ingest, run_progressive_risk, run_sudden_fault, run_spectrum_monitor, run_safety_state_machine, run_eval, launch_demo_session）
  - 职责：把一条事件或度量记录以 JSON 行追加写入运行目录的 events.jsonl / metrics 分片文件，保证进程内写序；度量键带场景与时间戳前缀。
  - 签名意图：输入: 运行目录, 记录类型（event|metric）, 载荷 dict / 输出: 无（副作用=落盘） / 错误: 磁盘失败抛 IOError
  - tested 策略：自有单测
  - 核验命令：测试: tests/shared/test_append_record.py
- **load_model_artifact**（调用方：predict_risk_tcn, classify_fault）
  - 职责：按配置加载模型工件（PyTorch checkpoint 或轻量分类器 pickle），校验版本戳与输入特征名匹配，返回就绪模型对象；文件缺失给出明确指引（先跑 train_tcn）。
  - 签名意图：输入: 模型路径, 期望特征名清单 / 输出: 模型对象 / 错误: 文件缺失/特征不匹配抛 ModelArtifactError
  - tested 策略：自有单测
  - 核验命令：测试: tests/shared/test_load_model_artifact.py
- **run_eval**（调用方：程序入口, batch_eval）
  - [改造 10-06 R25] 分片键改单值 lead_s（删 per-run lead_p10_s/lead_median_s 误导键）；补录 10-06 语义注记（首次告警提前量口径/conformal_coverage+detected+false_alarms 指标键/link_evs 采集）。核验=继承 R25（分片无 lead_p10_s 有 lead_s）
  - 职责：批量评估执行器（R2/R3/R4 验收命令本体）——按场景名与次数循环：open_run_dir → run_ingest（inject_scenario_fault 注入）→ 风险管线 → 按失控判据计时出指标（提前量 P10/中位数/达标率、确认时延 P90、类型正确率、误报数）→ append_record 汇总；输出每场景指标汇总表并落运行目录。只写运行目录分片，不写战役顶层 metrics.json（那是 merge_metrics 的领地）。
  - [改造 10-03 演进轮] R12 口径增量：manifest 记 inject_at_s；突发时延=确认−inject_at；hit_rate 仅渐进场景输出。R11 通道增量：接受 model/quantiles 注入（模型缺席自动回退降级通道并在分片 note 标 degraded）；分片附 data_source（px4|synthetic）。CLI 壳 eval.py 不变。
  - 签名意图：输入: 场景名, 次数, 可选种子清单 / 输出: 指标汇总 dict + 运行目录清单 / 错误: 场景未定义/仿真启动失败即报错退出（非零退出码）
  - tested 策略：自有单测（回放模式跑通最小次数）
  - 核验命令：继承 R2/R3/R4 验收方式（eval CLI 本体）
- **archive_run**（调用方：batch_eval, boot_selfcheck, soak_test, run_eval）
  - 职责：把 fn_work/runs 下的运行目录整体归档到 fn_docs/results/<场景>/<目录名>/（含 manifest/metrics/events/frames），保持只拷不移（原件留在工程运行区），返回归档路径；同名冲突加序号；归档清单回写 manifest。
  - 签名意图：输入: 运行目录路径, 归档根（缺省 fn_docs/results） / 输出: 归档目标路径 / 错误: 源目录缺失抛 FileNotFoundError
  - tested 策略：自有单测
  - 核验命令：测试: tests/shared/test_archive_run.py
- **inject_scenario_fault**（调用方：run_eval, session_control_api）
  - 职责：按场景定义在指定飞行阶段注入故障——低电量+逆风（PX4 电池/风参数）、电机故障（PX4 failure injection 命令）、链路退化（遥测丢弃/延迟注入）；注入时刻与参数记录进运行清单。
  - 签名意图：输入: MAVLink 控制连接, 场景名, 强度档（低/中/高）, 注入时机 / 输出: 注入回执 dict / 错误: 命令拒绝/超时抛 InjectError
  - tested 策略：自有单测（SITL 起飞注入一次）
  - 核验命令：测试: tests/shared/test_inject_scenario_fault.py

## 功能块 run_ingest ← R1
（R1：从 PX4 SITL 读多源遥测，产 20 Hz 统一状态序列——字段字典对齐计划书 4.1，质量掩码+时间戳+缺失标记，含失控判据字段；原始遥测全量落运行目录。）

- **run_ingest** [L0|新增]
  - 职责：统一数据接入主循环——connect_sitl 建链后按 20 Hz 节拍收消息，normalize_telemetry 归一，aggregate_imu_features 压高频 IMU，compute_physical_margins 出四类物理余量，append_record 落统一状态序列与原始遥测；Ctrl-C/仿真退出时干净收尾并落清单。供 run_eval 与演示实时流两种调用形态。
  - 签名意图：输入: 配置（连接参数/速率/字段字典）, 运行目录, 可选停止条件 / 输出: 统一状态流（生成器或回调）+ 运行目录产物 / 错误: 连接失败/持续超时抛 IngestError 并落部分数据
  - 调用方：程序入口, run_eval
  - tested 策略：自有单测（SITL 短飞）+ 上游覆盖: run_eval
  - 核验命令：继承 R1 验收方式（replay_check CLI 本体）
  - **connect_sitl** [L1|新增]
    - 职责：建立 pymavlink 连接（udp/tcp/uds 可配），请求消息速率与数据流，等到心跳与首帧姿态即认为就绪；带超时与一次重试。
    - 签名意图：输入: 连接串, 超时 / 输出: 连接对象（含心跳元数据） / 错误: 超时抛 ConnectionError
    - 调用方：run_ingest
    - tested 策略：上游覆盖: run_ingest
    - 核验命令：上游覆盖: run_ingest
  - **normalize_telemetry** [L1|新增]
    - 职责：原始 MAVLink 消息批 → StateFrame（统一字段/量纲/时间戳/来源标记）；同时生成质量掩码：字段新鲜度、取值域越界、跨源一致性三项合成 per-field 质量位；缺失字段置 NaN+掩码位，绝不插值冒充实测。
    - 签名意图：输入: 20 Hz 节拍内的原始消息批 / 输出: StateFrame（含 quality_mask） / 错误: 无（内部消化，异常只影响掩码）
    - 调用方：run_ingest
    - tested 策略：自有单测
    - 核验命令：测试: tests/run_ingest/test_normalize_telemetry.py
  - **aggregate_imu_features** [L1|新增]
    - 职责：短窗口（可配，默认 1 s）高频 IMU 原始采样 → 均方根、峰值、频带能量、偏置变化四特征，附加到对应节拍的 StateFrame；窗口样本不足时特征置 NaN+掩码。
    - 签名意图：输入: IMU 原始缓冲, 窗口参数 / 输出: 特征 dict（四键） / 错误: 无（不足即 NaN）
    - 调用方：run_ingest
    - tested 策略：自有单测
    - 核验命令：测试: tests/run_ingest/test_aggregate_imu_features.py
  - **compute_physical_margins** [L1|新增]
    - 职责：由 StateFrame 计算四类可解释物理余量：返航能源余量（含逆风修正）、GNSS/EKF 导航可信度、链路健康度（到达间隔/序号丢包/信号质量+R4 一致性证据）、控制余量（姿态跟踪误差/振动/执行器饱和）；输出归一余量与原始量双份。产物流入 check_physical_baseline 与 update_state 消费。
    - 签名意图：输入: StateFrame 序列（需返航点配置） / 输出: margins dict（四类，各含 raw 与 normalized） / 错误: 依赖字段缺失时该类余量置 NaN+掩码
    - 调用方：run_ingest
    - tested 策略：自有单测
    - 核验命令：测试: tests/run_ingest/test_compute_physical_margins.py
  - **replay_check** [L1|新增]
  - [改造 10-06 R25·语义补录] 覆盖率口径注记：2s GPS 暖机段豁免；rssi 为可选字段（PX4 SITL 无无线电消息，链路健康退化为遥测间隔证据）
    - 职责：R1 验收命令本体——读运行目录，统计统一帧率（≥20 Hz 判 PASS）、字段覆盖率清单（逐字段有效帧占比）、掩码分布，输出 PASS/FAIL 与明细。
    - 签名意图：输入: 运行目录（--run） / 输出: 检查报告, 退出码 0/1 / 错误: 目录结构不合法报错退出
    - 调用方：程序入口
    - tested 策略：自有单测
    - 核验命令：继承 R1 验收方式（自身即验收命令）

## 功能块 run_progressive_risk ← R2
（R2：物理基线+轻量 TCN+共形校准三层——10 s 窗口出 1/3/5/10 s 危险概率与剩余安全时间，概率经 90% 覆盖率共形区间包装成渐进事件对象。）

- **run_progressive_risk** [L0|新增]
  - 职责：渐进风险主循环——消费 StateFrame 流：check_physical_baseline 先判物理余量持续收窄，build_feature_window 组窗，predict_risk_tcn 出概率，calibrate_conformal 包区间；输出统一渐进事件对象（风险类型/严重度/置信区间/证据字段/剩余安全时间/首触发时间），append_record 落事件流；数据质量不足时输出保守告警事件（不升级处置）。
  - 签名意图：输入: StateFrame 流, margins 流, 模型配置 / 输出: 渐进事件流（生成器） / 错误: 模型加载失败抛 ModelArtifactError；运行期错误降级为事件标注
  - 调用方：程序入口, run_eval
  - tested 策略：上游覆盖: run_eval
  - 核验命令：继承 R2 验收方式（eval --scenario lowbat_headwind）
  - **build_feature_window** [L1|新增]
    - 职责：最近 10 s（可配）StateFrame+margins → 模型特征张量（定长列，掩码位转 NaN 指示列）；窗口不满时返回 None（不预测）。
    - 签名意图：输入: 帧缓冲, 窗口参数 / 输出: 特征张量或 None / 错误: 无
    - 调用方：run_progressive_risk
    - tested 策略：自有单测
    - 核验命令：测试: tests/run_progressive_risk/test_build_feature_window.py
  - **predict_risk_tcn** [L1|新增]
    - 职责：TCN 前向——特征窗口 → 未来 1/3/5/10 s 进入危险状态的概率与剩余安全时间估计（多任务头）；纯函数，模型经 load_model_artifact 注入；目标设备（Jetson 设备模块）到场时同一函数在设备侧执行并带来源标注。
    - 签名意图：输入: 特征张量, 模型对象 / 输出: 概率 dict + 剩余安全时间 / 错误: 形状不匹配抛 ValueError
    - 调用方：run_progressive_risk
    - tested 策略：自有单测（小模型前向）
    - 核验命令：测试: tests/run_progressive_risk/test_predict_risk_tcn.py
  - **calibrate_conformal** [L1|新增]
    - 职责：共形校准——用留出校准集的非一致性分数分位数，把点概率包装为 90% 覆盖率区间；输出区间宽度一并给出；校准集经配置注入，运行期纯查表。
    - 签名意图：输入: 点预测 dict, 校准分位数表 / 输出: 带区间预测 dict（含上下界与宽度） / 错误: 校准表缺失抛 ConformalError
    - 调用方：run_progressive_risk
    - tested 策略：自有单测（合成数据覆盖率断言）
    - 核验命令：测试: tests/run_progressive_risk/test_calibrate_conformal.py
  - **check_physical_baseline** [L1|新增]
    - 职责：物理基线判定——四类余量逐类做"持续收窄"判断（阈值+持续时长），输出基线告警与所依据余量序列；它是 TCN 之外独立的降级判据（模型不可用时仍可告警）。
    - 签名意图：输入: margins 流, 阈值配置 / 输出: 基线状态 dict（四类各自触发与否+证据窗） / 错误: 无
    - 调用方：run_progressive_risk
    - tested 策略：自有单测
    - 核验命令：测试: tests/run_progressive_risk/test_check_physical_baseline.py
  - **train_tcn** [L1|新增]
  - [改造 10-06 R23·补记] train_report.json 必含 best 字段（选优结果落盘，供 _ensure_model 消费；曾漏致批量装载断链——回归测试守护）
    - 职责：离线训练管线——从运行目录/回放数据生成监督样本（事件标注=失控判据时刻；按架次/日期分组切分防泄漏，内联完成），训练轻量 TCN（参数量≤200 万），出验证曲线与 checkpoint+特征名清单+版本戳。
    - 签名意图：输入: 数据目录清单, 训练配置 / 输出: checkpoint+元数据+验证报告路径 / 错误: 数据不足/标注缺失抛 TrainError
    - 调用方：程序入口
    - tested 策略：自有单测（微型数据冒烟一轮）
    - 核验命令：测试: tests/run_progressive_risk/test_train_tcn.py

## 功能块 run_sudden_fault ← R3
（R3：残差构造+CUSUM 变化检测+轻量分类——面向电机/电调异常与通信瞬断，考核确认时延 P90 与类型正确率。）

- **run_sudden_fault** [L0|新增]
  - 职责：突发故障主循环——build_residuals 出多通道残差，cusum_detect 确认突变，classify_fault 判来源；输出统一突发事件对象（含首触发时间、检测时延自记录）；未确认期静默。
  - 签名意图：输入: StateFrame 流, 原始遥测补充流 / 输出: 突发事件流 / 错误: 运行期错误降级为事件标注
  - 调用方：程序入口, run_eval
  - tested 策略：上游覆盖: run_eval
  - 核验命令：继承 R3 验收方式（eval --scenario motor_fail）
  - **build_residuals** [L1|新增]
    - 职责：构造四类残差通道——惯导创新残差（EKF innovation）、姿态跟踪残差（设定值 vs 实测量）、转速-电流一致性残差（电机模型预期 vs 实测，缺转速时掩码）、遥测到达间隔/序号丢包序列；逐通道归一；R4 一致性残差经链路通道并入。
    - 签名意图：输入: StateFrame 流+原始遥测 / 输出: 残差通道帧流 / 错误: 无（缺源即掩码）
    - 调用方：run_sudden_fault
    - tested 策略：自有单测
    - 核验命令：测试: tests/run_sudden_fault/test_build_residuals.py
  - **cusum_detect** [L1|新增]
    - 职责：多通道累积和变化检测——每通道 CUSUM 统计量越阈且持续 N 拍即确认突变，输出突变通道集与确认时刻；参数（阈值/漂移/持续拍数）入配置。
    - 签名意图：输入: 残差通道帧流, 参数配置 / 输出: 突变确认事件（通道集+时刻）或 None / 错误: 无
    - 调用方：run_sudden_fault
    - tested 策略：自有单测（阶跃注入检出时延断言）
    - 核验命令：测试: tests/run_sudden_fault/test_cusum_detect.py
  - **classify_fault** [L1|新增]
    - 职责：突变确认后用轻量分类器（梯度提升树）按确认窗内通道模式判故障来源：电机异常/电调异常/链路瞬断/未知；输出类型+置信度。
    - 签名意图：输入: 确认窗内残差特征, 分类器对象 / 输出: 类型+置信度 / 错误: 模型缺失时退化为规则判型（电机类/链路类二分）并标注
    - 调用方：run_sudden_fault
    - tested 策略：自有单测
    - 核验命令：测试: tests/run_sudden_fault/test_classify_fault.py

## 功能块 run_link_consistency ← R4
（R4：RSSI 时序与 GNSS 真实距离互检——统计基线版（IQR 自适应阈值），一致性残差并入 R3 特征与链路健康度。）

- **run_link_consistency** [L0|新增]
  - 职责：链路一致性主循环——estimate_distance_trend 由 RSSI 时序推距离趋势，consistency_residual 与 GNSS 距离互检出一致性残差与异常证据；证据双送：进 build_residuals 的链路通道 + 进 compute_physical_margins 的链路健康度。
  - 签名意图：输入: StateFrame 流（含 RSSI 与 GNSS 距离） / 输出: 一致性证据流 / 错误: 无（缺源即静默+掩码）
  - 调用方：程序入口, run_eval
  - tested 策略：上游覆盖: run_eval
  - 核验命令：继承 R4 验收方式（eval --scenario link_degrade）
  - **estimate_distance_trend** [L1|新增]
    - 职责：滑窗内由 RSSI 时序估计距离变化趋势（对数距离路径模型的差分统计版，只取趋势方向与变化率）；窗口样本不足返回 None。
    - 签名意图：输入: RSSI/时间戳缓冲, 窗口参数 / 输出: 趋势估计（变化率+置信）或 None / 错误: 无
    - 调用方：run_link_consistency
    - tested 策略：自有单测
    - 核验命令：测试: tests/run_link_consistency/test_estimate_distance_trend.py
  - **consistency_residual** [L1|新增]
    - 职责：RSSI 推距趋势与 GNSS 距离变化率的互检残差，IQR 自适应阈值判异常（仅用正常样本定阈）；输出残差值+异常位。
    - 签名意图：输入: 趋势估计, GNSS 距离序列 / 输出: 残差+异常标志 / 错误: 无
    - 调用方：run_link_consistency
    - tested 策略：自有单测
    - 核验命令：测试: tests/run_link_consistency/test_consistency_residual.py

## 功能块 run_spectrum_monitor ← R5
（R5 频谱感知站=设备模块：USRP B210 只收不发；设备缺席自动回放模式（帧等价、来源标注），到位即测真数据——双源经同一占用率管线，实证"即插即测不重构"。）

- **run_spectrum_monitor** [L0|新增]
  - 职责：频谱站主循环——经 run_device_bus 获知 SDR 模块在场与否：在场走 capture_spectrum（设备实采），缺席走 replay_spectrum_source（回放帧，source=replay）；帧经 route_device_frames 分发，compute_occupancy 出占用率与告警；全程同一管线，仅数据来源不同。
  - 签名意图：输入: 配置（频率/带宽/信道表/告警阈）, 设备总线句柄 / 输出: 占用率流+瀑布帧流（帧头带 source 标注） / 错误: 设备打开失败自动转回放或抛 SpectrumError（无回放源时）
  - 调用方：程序入口, sdr_check
  - tested 策略：上游覆盖: sdr_check
  - 核验命令：继承 R5 验收方式（sdr_check 双源自检）
  - **capture_spectrum** [L1|新增]
    - 职责：设备模式——经设备总线从 SDR 模块取 IQ 采样+FFT → 功率谱帧（dBm 标定经配置增益/校准表）；帧率与带宽参数化；设备错误经总线健康通道上报。
    - 签名意图：输入: 设备采样流, 参数 / 输出: 功率谱帧生成器（source=device） / 错误: 设备错误抛 USRPError（上层转回放）
    - 调用方：run_spectrum_monitor
    - tested 策略：自有单测（回放文件模拟 IQ）
    - 核验命令：测试: tests/run_spectrum_monitor/test_capture_spectrum.py
  - **replay_spectrum_source** [L1|新增]
    - 职责：回放模式——从回放文件读预录功率谱/IQ → 与设备模式**帧格式完全等价**的帧流（source=replay），供同一占用率管线消费；支持循环与时间窗定位。
    - 签名意图：输入: 回放文件路径, 参数 / 输出: 功率谱帧生成器（source=replay） / 错误: 文件缺失/格式不符抛 ReplayError
    - 调用方：run_spectrum_monitor
    - tested 策略：自有单测
    - 核验命令：测试: tests/run_spectrum_monitor/test_replay_spectrum_source.py
  - **compute_occupancy** [L1|新增]
    - 职责：功率谱帧（不关心来源）→ 目标信道集占用率（能量占比+过阈子载波占比双口径）与帧级告警位（相对基线抬升超阈）。
    - 签名意图：输入: 功率谱帧, 信道表, 基线与阈值 / 输出: 信道占用率 dict+告警位 / 错误: 无
    - 调用方：run_spectrum_monitor
    - tested 策略：自有单测
    - 核验命令：测试: tests/run_spectrum_monitor/test_compute_occupancy.py
  - **sdr_check** [L1|新增]
    - 职责：R5 自检命令本体=模块化实证——同一 compute_occupancy 管线分别跑设备帧与回放帧：回放模式出带宽/帧率/占用率响应自检；设备在场时加跑实采并比对两源口径一致性；输出 PASS/FAIL 与明细。
    - 签名意图：输入: 无（读配置） / 输出: 自检报告, 退出码 0/1 / 错误: 报告内呈现（不抛）
    - 调用方：程序入口
    - tested 策略：自有单测
    - 核验命令：继承 R5 验收方式（自身即验收命令）

## 功能块 run_safety_state_machine ← R6
（R6：S0-S4 确定性状态机+处置建议——阈值+持续时间+证据完整性+迟滞；三方案能源校验出建议动作，不执行。）

- **run_safety_state_machine** [L0|新增]
  - 职责：状态机主循环——消费双通道事件+margins：update_state 出当前 S 态与转换记录（含证据链），plan_disposal 出建议动作与理由；输出统一处置建议对象（动作/理由/依据事件 ID/能源校验明细），append_record 落状态轨迹；人工接管与原飞控保护为独立通道（本机不重叠）。
  - 签名意图：输入: 事件流（渐进+突发）, margins 流, 任务上下文（返航点/备降点表/地理围栏） / 输出: 状态轨迹流+建议流 / 错误: 无（内部消化）
  - 调用方：程序入口, run_eval
  - tested 策略：上游覆盖: run_eval
  - 核验命令：继承 R6 验收判据（回放日志证据链+迟滞生效，eval 全场景输出内含）
  - **update_state** [L1|新增]
    - 职责：单步状态转换判定——风险分值/事件严重度满足阈值+持续时间+证据完整性三条件才迁移；阈值邻域设迟滞带防抖动；输出新态+触发证据（事件 ID 清单+各项条件读数）。
    - 签名意图：输入: 当前态, 事件窗, 阈值与迟滞配置 / 输出: 新态+迁移记录（或保持） / 错误: 无
    - 调用方：run_safety_state_machine
    - tested 策略：自有单测（迁移/迟滞/证据不全不升三级用例）
    - 核验命令：测试: tests/run_safety_state_machine/test_update_state.py
  - **plan_disposal** [L1|新增]
    - 职责：处置建议——对返航/备降（逐备降点）/原地降落三方案算能源需求（含逆风修正），检查 GNSS/链路可用性、地理围栏、落点条件、平台权限；低电量逆风时返航须能源高于保留裕量才允许，GNSS+链路同退时禁依赖远程连续控制的策略；输出建议+全部方案校验明细（被否方案附理由）。
    - 签名意图：输入: 当前态, margins, 任务上下文 / 输出: 建议对象（动作/理由/方案明细） / 错误: 无
    - 调用方：run_safety_state_machine
    - tested 策略：自有单测（低电量逆风禁返航/双退化禁远程两用例）
    - 核验命令：测试: tests/run_safety_state_machine/test_plan_disposal.py

## 功能块 run_ground_station ← R7
（R7：FastAPI+WebSocket 单机服务——仪表盘/事件时间线/频谱瀑布/回放四页+控制台页；一键启动断网可用；功能完整性优先，界面精致度为加分项。）

- **run_ground_station** [L0|新增]
  - 职责：平台主入口——组装 FastAPI app（register_pages 挂五页路由含控制台页与 session_control_api 控制端点，pipe_events 接实时流），uvicorn 起服务（localhost 可配端口），提供静态资源与运行目录索引；`demo.sh` 与 smoke_boot 的服务端本体；浏览器打开即进入控制台页（演示主入口）。
  - 签名意图：输入: 配置（端口/运行目录根）, 可选实时流源 / 输出: 运行中的服务（阻塞） / 错误: 端口占用抛 SystemExit 带提示
  - 调用方：程序入口
  - tested 策略：上游覆盖: sw-boot 验收
  - 核验命令：继承 R7 验收方式（一键启动五页可看）
  - **pipe_events** [L1|新增]
    - 职责：实时流分发——订阅 run_ingest/双通道事件/状态轨迹/频谱帧（经 route_device_frames）的发布端，维护 WebSocket 订阅者集合并广播（背压策略：事件全发、频谱帧可抽稀）。
    - 签名意图：输入: 各发布端回调注册, WebSocket 连接管理 / 输出: 无（副作用=广播） / 错误: 单订阅者异常剔除不影响其余
    - 调用方：run_ground_station
    - tested 策略：自有单测（本地 WebSocket 客户端收帧）
    - 核验命令：测试: tests/run_ground_station/test_pipe_events.py
  - **register_pages** [L1|新增]
    - 职责：挂载五个页面路由与 API——仪表盘、事件时间线（证据链展开）、频谱瀑布、回放页、控制台页（render_console 载体，含 session_control_api 控制端点挂载）；页面模板与静态资源随包分发，无外网依赖；界面以功能完整与稳定为验收线，视觉打磨不阻塞交付。
    - 签名意图：输入: FastAPI app, 运行目录根 / 输出: 无（副作用=路由注册） / 错误: 模板缺失启动即报
    - 调用方：run_ground_station
    - tested 策略：自有单测（五路由 GET 200 + 关键元素存在）
    - 核验命令：测试: tests/run_ground_station/test_register_pages.py

## 功能块 build_materials ← R8
（R8：材料包——实测数字引用表（每数字带 metrics 键）、计划书逐节修订建议+可粘贴段落、材料编译入口；对外数字唯一来源=metrics 分片。）

- **build_materials** [L0|新增]
  - 职责：材料构建总入口——汇总各运行目录 metrics 分片，export_metrics_table 出数字引用表，draft_revision_notes 出计划书修订建议稿，compile_documents 编译材料（docs/build.py 本体）；供材料冲刺消费。
  - 签名意图：输入: 运行目录清单, 材料配置 / 输出: 数字引用表+修订建议稿+编译产物路径 / 错误: 分片缺失/数字不一致抛 MaterialError（阻断编译）
  - 调用方：程序入口
  - tested 策略：上游覆盖: doc-compile 验收
  - 核验命令：继承 R8 验收方式（doc-compile + doc-numbers）
  - **export_metrics_table** [L1|新增]
  - [改造 10-06 R25·补记] lead_s 列派生汇总键（P10/中位数/达标率，(aggregate) 注记）；P10 口径唯一源=run_eval._percentile（线性插值）
    - 职责：读全部 metrics 分片 → 汇总表（指标×场景×运行批次，含统计口径列与来源运行目录），并做一致性校验（同键不同值冲突即报）；不写战役顶层 metrics.json，只产引用表。
    - 签名意图：输入: 运行目录清单 / 输出: 引用表（Markdown+JSON 双格式） / 错误: 冲突/缺失键抛 MaterialError
    - 调用方：build_materials
    - tested 策略：自有单测
    - 核验命令：测试: tests/build_materials/test_export_metrics_table.py
  - **draft_revision_notes** [L1|新增]
    - 职责：组装计划书逐节修订建议——输入=补强方案（三补强落点）+实测数字引用表+演示形态描述，输出=按计划书章节组织的修订建议稿（每节：原文摘要/修订建议/可直接粘贴段落/数字占位符带 metrics 键）；团队消化改写用，含人机分工记录模板头。
    - 签名意图：输入: 引用表, 补强方案路径 / 输出: 修订建议稿（Markdown） / 错误: 引用键缺失抛 MaterialError
    - 调用方：build_materials
    - tested 策略：自有单测（占位符全闭合断言）
    - 核验命令：测试: tests/build_materials/test_draft_revision_notes.py
  - **compile_documents** [L1|新增]
    - 职责：材料编译——把修订建议稿+数字回填模板编译为计划书 v2 草稿与路演 PPT（Marp）产物；编译前跑数字一致性预检（与引用表逐键对照），不过即失败退出。
    - 签名意图：输入: 材料源目录, 编译配置 / 输出: 编译产物路径清单 / 错误: 编译器失败/数字不一致抛 MaterialError
    - 调用方：build_materials
    - tested 策略：上游覆盖: build_materials
    - 核验命令：继承 doc-compile 验收方式（docs/build.py 本体）

## 功能块 launch_demo_session ← R9
（R9 演示控制台后端——演示会话全流程 UI 化：选场景一键起飞、飞行中注入故障/调强度、中止归档、时间轴回放；零终端零代码；功能完整 P0，UI 精致度加分项；手动接管为 P1 范围外。）

- **launch_demo_session** [L0|新增]
  - 职责：演示会话编排——从控制台请求发起一次演示：open_run_dir 建运行目录 → spawn_sitl 按场景拉起仿真 → 装配 run_device_bus（设备模块自动发现/降级）与 run_ingest 及风险管线/状态机 → 事件流接 pipe_events → 返回会话句柄（会话表：id→句柄/运行目录/控制端点）；会话中止或正常结束时归档运行清单；同机多会话互不串流。
  - 签名意图：输入: 会话请求（场景名/强度档/可选种子）, 配置 / 输出: 会话句柄（id, 运行目录, 控制端点） / 错误: 场景未定义/SITL 拉起失败抛 SessionError（含可读原因给 UI 展示）
  - 调用方：程序入口, session_control_api
  - tested 策略：自有单测（SIH 最小场景会话冒烟：发起→收帧→中止归档）
  - 核验命令：继承 R9 验收方式（浏览器全流程判据；单测=tests/launch_demo_session/test_launch_demo_session.py）
  - **spawn_sitl** [L1|新增]
    - 职责：按场景定义拉起 PX4 SITL 进程（Gazebo 主/SIH 备选可配），等心跳就绪并做健康检查，管理进程句柄与日志文件；会话结束/异常时干净回收；同机多会话的端口/MAVLink 端点分配。
    - 签名意图：输入: 场景定义, 仿真器选择 / 输出: 仿真进程句柄（含连接端点） / 错误: 拉起超时/心跳不至抛 SitlError
    - 调用方：launch_demo_session
    - tested 策略：自有单测（SIH 拉起→心跳→回收）
    - 核验命令：测试: tests/launch_demo_session/test_spawn_sitl.py
  - **session_control_api** [L1|新增]
  - [改造 10-06 R25·签名意图修正] 签名意图正名：输入: FastAPI app（挂载控制路由与端点） / 输出: 无（副作用=路由注册）——stub 期 payload 语义作废（名实已于审计对齐）
    - 职责：控制台后端 API——UI 动作全映射：发起/中止会话（桥 launch_demo_session）、飞行中注入故障与调强度（桥 inject_scenario_fault）、回放请求（指定运行目录+时间窗）、会话状态查询（含设备模块在场状态展示）；按钮按下到后端受理保持演示节奏（≤2 s 目标）。
    - 签名意图：输入: HTTP/WS 控制请求 / 输出: 动作回执（含受理结果与会话状态） / 错误: 无会话/动作非法返回结构化错误给 UI 展示（不抛裸异常）
    - 调用方：register_pages
    - tested 策略：自有单测（FastAPI TestClient 打全控制端点）
    - 核验命令：测试: tests/launch_demo_session/test_session_control_api.py
  - **render_console** [L1|新增]
    - 职责：控制台页——功能完整性优先的演示操控前端：场景选择/起飞/注入面板（按钮+强度滑杆 低/中/高）/实时状态区（风险等级/剩余安全时间/建议动作）/频谱瀑布嵌入/事件时间轴/回放时间轴（暂停/加速/拖动）；深色主题基线（视觉打磨为加分项不阻塞交付）；模板与静态资源随包分发、无外网依赖。
    - 签名意图：输入: 页面路由上下文 / 输出: 控制台页（HTML+静态资源） / 错误: 资源缺失启动即报
    - 调用方：register_pages
    - tested 策略：自有单测（路由 GET 200 + 关键元素存在：注入面板/时间轴/状态区）
    - 核验命令：测试: tests/launch_demo_session/test_render_console.py

## 功能块 run_device_bus ← R10
（R10 设备模块化架构——统一设备接口：发现/健康/数据帧路由/降级；模块缺席自动回放顶替，到位即插即测，核心不因设备变化重构。SDR 与 Jetson 边缘为首批模块。）

- **run_device_bus** [L0|新增]
  - 职责：设备总线主循环——启动时 discover_device_module 枚举在场设备模块（按配置清单：sdr/jetson/…），运行期 health_check_module 持续监测（采样率/错误率），route_device_frames 把模块数据帧（频谱帧/边缘样本）按订阅分发并统一帧头（source=device|replay）；模块缺席或失健时自动挂对应回放源并标注，消费方（如 run_spectrum_monitor）无感知切换。
  - 签名意图：输入: 设备模块配置清单, 回放源配置 / 输出: 总线句柄（注册/订阅/健康查询接口） / 错误: 模块初始化失败不阻断总线（降级+日志）
  - 调用方：程序入口, launch_demo_session
  - tested 策略：自有单测（双模块注入/拔除切换用例）
  - 核验命令：继承 R10 验收方式（拔插模块判据；单测=tests/run_device_bus/test_run_device_bus.py）
  - **discover_device_module** [L1|新增]
    - 职责：按配置清单枚举并装载在场设备模块（USRP 在场探测、Jetson SSH/USB 探测等），返回模块注册表（在场模块+缺席标记）；探测只做发现不阻塞，缺席即记 None。
    - 签名意图：输入: 模块配置清单, 探测超时 / 输出: 模块注册表 dict（模块名→句柄或 None） / 错误: 探测异常按缺席处理并记日志
    - 调用方：run_device_bus
    - tested 策略：自有单测（模拟在场/缺席两态）
    - 核验命令：测试: tests/run_device_bus/test_discover_device_module.py
  - **health_check_module** [L1|新增]
    - 职责：模块健康监测——周期采样模块指标（帧率/错误计数/延迟），越阈判定失健并产出降级切换指令（挂回放源+标注），恢复后自动切回设备源。
    - 签名意图：输入: 模块句柄, 健康阈值 / 输出: 健康状态+切换动作 / 错误: 无（异常按失健处理）
    - 调用方：run_device_bus
    - tested 策略：自有单测（失健→降级→恢复用例）
    - 核验命令：测试: tests/run_device_bus/test_health_check_module.py
  - **route_device_frames** [L1|新增]
    - 职责：设备帧路由——把模块/回放源产出的数据帧按主题（spectrum/edge/…）分发给订阅者（pipe_events、run_spectrum_monitor），帧头统一携带来源标记（source=device|replay）与时间戳；背压时频谱类帧可抽稀。
    - 签名意图：输入: 帧流, 订阅表 / 输出: 无（副作用=分发） / 错误: 单订阅者异常剔除不影响其余
    - 调用方：run_device_bus
    - tested 策略：自有单测（双源同管线等价断言）
    - 核验命令：测试: tests/run_device_bus/test_route_device_frames.py

## 产出前自检（R23-R25 演进轮，2026-10-06）
- 矩阵正向：R1-R25 全覆盖（25/25）✓（R24 以 build_package"交付卫生"职责承接；一次性 git ops 为 B19 批内动作）
- 矩阵反向：R23-R25 无新函数——均为既有单元 [改造]（batch_eval/run_eval/build_package）+文档修正（session_control_api 签名/replay_check 注记）✓
- 纯改造无新单元 → fn-scaffold 依演进链规则合法跳过
- 函数总数 89（31 补账后）不变 ✓

## 产出前自检
- 矩阵正向：R1-R10 每条恰好一个顶层函数负责 ✓（10/10，无漏实现）
- 矩阵反向+树：全部函数经调用链可达顶层入口 ✓（程序入口：十个顶层函数 + run_eval / replay_check / sdr_check / train_tcn；shared 六件均被多顶层引用；无死代码）
- 单一功能转变：逐函数复核 ✓（双源（capture/replay）各自单一、总线三件（发现/健康/路由）各自单一）
- 函数总数 48 > 20 预警线：**已预警并命令实测**（计数方式：概览树函数行数=功能块与共享节的函数条目数，两者一致才算数）——成因=10 需求口的系统级工程，其中 R10 模块化（4 函数）与 R5 双源（+1）为用户本轮明确要求的即插即测能力，不在可砍之列。门口裁决：接受 48 或指定收缩项。


## 功能块 batch_eval ← R11
（R11：真数据面+批量跑批——PX4 工具链探测（用户 sudo 安装后可用），三场景×N 次批量，产物归档 fn_docs/results，模型经 train_tcn 重训接入。）

- **batch_eval** [L0|新增]
  - [改造 10-06 R23/R25] R23：_ensure_model 消费 train_tcn best/selection（winner=probe→probe.pkl 重建探针装载；winner=tcn→tcn.pt；缺失/失败回退重训并注记原因）。R25：汇总层增跨运行聚合（lead P10/中位数/达标率入快照）。核验=继承 R23/R25（批量 note 含 probe-sel+hit_rate≥0.9；快照含聚合值）
  - 职责：跨场景批量评估总控——probe_px4_env 定数据面（px4 就绪→spawn_sitl px4 模式；否则 synthetic 兜底并标注）；保证风险模型工件存在（缺则调 train_tcn 合成重训，标 synthetic-trained）；逐场景调 run_eval（注入模型与口径参数）×N 次；逐运行 archive_run 归档；产快照 JSON（runs 数、data_source、按场景口径分列的汇总）写 fn_docs/results/。
  - 签名意图：输入: scenarios 清单（缺省三场景）, runs_per_scenario（缺省 30）, config / 输出: 快照 dict+归档路径清单 / 错误: PX4 模式拉起失败自动降级 synthetic 并在快照 note 记原因（不中断批量）
  - 调用方：程序入口
  - tested 策略：自有单测（synthetic 模式 1×1 微量跑通+归档断言）
  - 核验命令：继承 R11 验收方式（runs≥90 分片落 fn_docs/results；事件带共形区间；data_source 标注）
  - **probe_px4_env** [L1|新增]
    - 职责：探测 PX4 真跑条件——必需命令（make/cmake/arm 工具链）与 sitl.px4_dir 源码树是否可用；输出 {ready, missing:[...], px4_dir}；不做安装（安装属用户 sudo 动作）。
    - 签名意图：输入: config（sitl 节） / 输出: 就绪报告 dict / 错误: 无（探测失败=not ready）
    - 调用方：batch_eval
    - tested 策略：自有单测（缺 px4_dir→not ready；假目录+PATH 注入→ready 路径）
    - 核验命令：测试: tests/batch_eval/test_probe_px4_env.py

## 功能块 boot_selfcheck ← R13
（R13：一键自检升三步真验收——合成会话起→服务探活→回放探活。）

- **boot_selfcheck** [L0|新增]
  - 职责：sw-boot 验收本体三步——①launch_demo_session 起一个短合成会话并等到首帧/首事件；②probe_service 探活平台服务（起 uvicorn 线程后 GET /api/state）；③回放探活（GET /api/runs 对刚归档运行可用，或 frames API 返回非空）；三步全过输出三项 PASS 与汇总退出码；smoke_boot.py 为其 CLI 壳。
  - 签名意图：输入: 无（读配置；端口可配） / 输出: {step1, step2, step3, pass} 与退出码 0/1 / 错误: 各步失败记入报告不抛
  - 调用方：程序入口
  - tested 策略：自有单测（三步微缩版）
  - 核验命令：继承 R13 验收方式（smoke_boot 单命令三 PASS）
  - **probe_service** [L1|新增]
    - 职责：对 localhost 平台服务发 GET 探活（/api/state 与 /api/runs），带重试与超时；返回可达性与延迟 ms。
    - 签名意图：输入: base_url, 超时, 重试次数 / 输出: {reachable, latency_ms, endpoints} / 错误: 无（不可达=reachable False）
    - 调用方：boot_selfcheck
    - tested 策略：自有单测（本地起服务线程探活+拒绝端口反例）
    - 核验命令：测试: tests/boot_selfcheck/test_probe_service.py

## 功能块 bench_edge ← R14
（R14 设备就绪：Jetson 侧时延基准——真机执行列 manual，脚本侧 dry-run 自测过。）

- **bench_edge** [L0|新增]
  - 职责：边缘推理时延基准——dry-run 模式在本机以合成帧测 predict_risk_tcn 端到端 P50/P95（标口径 host-dryrun）；deploy 模式输出 Jetson 部署清单与执行脚本（rsync 包+运行命令），真机结果回读并入 metrics 分片（真机项 manual：设备到位执行）。
  - 签名意图：输入: mode（dryrun|deploy）, config / 输出: 基准报告 dict（dryrun）或部署指令清单（deploy） / 错误: deploy 无目标配置抛 BenchError 提示设备待接入
  - 调用方：程序入口
  - tested 策略：自有单测（dryrun 出有限 P50/P95）
  - 核验命令：继承 R14 验收方式（dry-run 自检 PASS；真机列 manual）

## 功能块 calibrate_usrp ← R14
（R14 设备就绪：B210 标定——增益/底噪/频轴核对，dry-run 用回放谱自测。）

- **calibrate_usrp** [L0|新增]
  - 职责：B210 标定流水——设备在场：扫增益阶梯记录底噪曲线与频轴偏差，产标定表（JSON，capture_spectrum 的 cal 参数消费）；设备缺席：--dry-run 用回放谱走同一流水出参考表并标注 replay；标定表落 fn_docs/results/calibration/。
  - 签名意图：输入: mode（dryrun|device）, config / 输出: 标定表路径+摘要 / 错误: device 模式无 uhd 抛 CalibError（提示设备待接入）
  - 调用方：程序入口
  - tested 策略：自有单测（dryrun 参考表）
  - 核验命令：继承 R14 验收方式（dry-run 自检 PASS）

## 功能块 build_package ← R15
（R15 打包与安装：pyproject、pip 可装、用户手册。）

- **build_package** [L0|新增]
  - [改造 10-06 R24·签名意图补记] 输出含 hygiene 报告字段（ignore_runs/tracked_artifacts）；卫生扫描 cwd=战役根（评审 C1 修正：原 pathspec 落空致假守卫）
  - [改造 10-06 R24] 打包前置卫生核验：ignore 覆盖 runs_* 规约+产物入库扫描（发现即失败并列清单）；一次性 git rm --cached 与 ignore 补写为 B19 批内 ops 动作留痕。核验=继承 R24（git ls-files 计数 0+打包自检）
  - 职责：产 pyproject.toml（src 布局映射+入口点 console_scripts：demo/eval/replay-check/sdr-check）并构建 wheel；装后自测——干净 venv pip install 轮子后以入口点起 demo.sh 等价服务探活；write_user_manual 产零术语手册（演示操作/安装/故障排查三节）随包分发。
  - 签名意图：输入: out_dir / 输出: wheel 路径+自测报告 / 错误: 构建失败抛 BuildError（贴 stderr 摘要）
  - 调用方：程序入口
  - tested 策略：自有单测（pyproject 生成+手册内容断言；构建走 subprocess 受 --skip-build 保护）
  - 核验命令：继承 R15 验收方式（干净 venv pip install 后 demo 起服务）
  - **write_user_manual** [L1|新增]
    - 职责：生成零术语用户手册 Markdown（安装/一键演示/控制台操作/常见故障四节，中文），内容从 README 项目功能节派生+安装实测步骤；不做排版美化。
    - 签名意图：输入: out_path / 输出: 手册路径 / 错误: 无
    - 调用方：build_package
    - tested 策略：自有单测（四节齐全断言）
    - 核验命令：测试: tests/build_package/test_write_user_manual.py

## 功能块 soak_test ← R16
（R16 长跑稳定性：连续会话+健康记录。）

- **soak_test** [L0|新增]
  - 职责：长跑稳定性——循环起 launch_demo_session（时长可配，默认连跑至 1h：会话串行直至总时长到），每会话记录帧数/事件数/线程存活/RSS 采样；结束产健康报告（会话数/总帧/内存曲线摘要/异常列表）入 fn_docs/results/soak/；--quick 模式压缩总时长供测试。
  - 签名意图：输入: duration_s（缺省 3600）, quick / 输出: 健康报告 dict+路径 / 错误: 单会话异常计入报告继续下一会话（崩溃率>50% 提前终止并标注）
  - 调用方：程序入口
  - tested 策略：自有单测（--quick 微缩长跑）
  - 核验命令：继承 R16 验收方式（长跑留痕入 fn_docs/results）

## 功能块 make_portable_bundle ← R16
（R16 免 root 便携交付包：tar 布局自含环境+数据+手册，解压即跑。）

- **make_portable_bundle** [L0|新增]
  - 职责：组装便携包——复制 venv（可迁移前缀修正脚本随包）+源码+fixtures+手册+入口脚本（portable_demo.sh：解压后设置 VIRTUAL_ENV 与 PATH 再 exec demo 链）；产 .tar.gz 与 SHA256SUMS；目标机口径 Linux x86_64；不做 ISO（需 root，口径注记于包内 README）。
  - 签名意图：输入: out_dir / 输出: 包路径+SHA256 / 错误: 环境不可复制（venv 缺）抛 BundleError
  - 调用方：程序入口
  - tested 策略：自有单测（tar 结构与 SHA 校验，不解压目标机）
  - 核验命令：继承 R16 验收方式（解压即跑属目标机人工项，包结构与校验和命令化）

## 辅助单元补账（2026-10-06 审计回填；[L2|补记] 为实现期随宿主交付、本次登记）

- **_deep_merge** [L2|补记]
  - 职责：配置树深合并（默认值+YAML 覆盖）
  - 签名意图：输入: base/override 两 dict / 输出: 合并 dict / 错误: 无
  - 调用方：load_config
  - tested 策略：上游覆盖: load_config
  - 核验命令：上游覆盖: load_config
- **_validate** [L2|补记]
  - 职责：配置模式校验（节/类型/取值域）
  - 签名意图：输入: 合并后 dict / 输出: 无 / 错误: ConfigError 带字段名
  - 调用方：load_config
  - tested 策略：上游覆盖: load_config
  - 核验命令：上游覆盖: load_config
- **_percentile** [L2|补记]
  - 职责：序列分位数（P10/P90 口径）
  - 签名意图：输入: 数值列表, q / 输出: float / 错误: 空表返 NaN
  - 调用方：run_eval
  - tested 策略：上游覆盖: run_eval
  - 核验命令：上游覆盖: run_eval
- **_crit_frame** [L2|补记]
  - 职责：失控判据判定（三场景各自尺子）
  - 签名意图：输入: 帧, 场景名 / 输出: bool / 错误: 无
  - 调用方：run_eval
  - tested 策略：上游覆盖: run_eval
  - 核验命令：上游覆盖: run_eval
- **_lead_metrics** [L2|补记]
  - 职责：首次告警提前量指标（规格口径）
  - 签名意图：输入: 帧列, 事件列, 场景 / 输出: 指标 dict / 错误: 无
  - 调用方：run_eval
  - tested 策略：上游覆盖: run_eval
  - 核验命令：上游覆盖: run_eval
- **_arm_takeoff** [L2|补记]
  - 职责：GPS 等锁→解锁（含强制）→AUTO.TAKEOFF 起飞
  - 签名意图：输入: MAVLink 连接 / 输出: bool / 错误: best-effort 不抛
  - 调用方：run_eval
  - tested 策略：上游覆盖: run_eval
  - 核验命令：上游覆盖: run_eval
- **_get** [L2|补记]
  - 职责：消息属性安全取值
  - 签名意图：输入: 消息, 名 / 输出: 值或 None / 错误: 无
  - 调用方：normalize_telemetry
  - tested 策略：上游覆盖: normalize_telemetry
  - 核验命令：上游覆盖: normalize_telemetry
- **_put** [L2|补记]
  - 职责：单字段写入+掩码+携带表登记
  - 签名意图：输入: 帧/掩码/状态, 键值, 时刻 / 输出: 无 / 错误: 无
  - 调用方：normalize_telemetry
  - tested 策略：上游覆盖: normalize_telemetry
  - 核验命令：上游覆盖: normalize_telemetry
- **_nan** [L2|补记]
  - 职责：空余量占位（raw/norm 双 NaN）
  - 签名意图：输入: 无 / 输出: dict / 错误: 无
  - 调用方：compute_physical_margins
  - tested 策略：上游覆盖: compute_physical_margins
  - 核验命令：上游覆盖: compute_physical_margins
- **_clamp01** [L2|补记]
  - 职责：0-1 截断（NaN 透传）
  - 签名意图：输入: float / 输出: float / 错误: 无
  - 调用方：compute_physical_margins
  - tested 策略：上游覆盖: compute_physical_margins
  - 核验命令：上游覆盖: compute_physical_margins
- **_home_dist_m** [L2|补记]
  - 职责：帧到返航点平面距离（m）
  - 签名意图：输入: 帧, 返航点 / 输出: float 或 None / 错误: 无
  - 调用方：compute_physical_margins
  - tested 策略：上游覆盖: compute_physical_margins
  - 核验命令：上游覆盖: compute_physical_margins
- **_load_run** [L2|补记]
  - 职责：运行目录载入（frames+manifest，兼容 results 归档）
  - 签名意图：输入: 目录 / 输出: (帧列, manifest) / 错误: TrainError
  - 调用方：train_tcn
  - tested 策略：上游覆盖: train_tcn
  - 核验命令：上游覆盖: train_tcn
- **_labels_for** [L2|补记]
  - 职责：危险标签抽取（失控判据时刻）
  - 签名意图：输入: 帧列, manifest / 输出: t_danger 或 None / 错误: 无
  - 调用方：train_tcn
  - tested 策略：上游覆盖: train_tcn
  - 核验命令：上游覆盖: train_tcn
- **make_dataset** [L2|补记]
  - 职责：监督样本生成（按架次分组防泄漏）
  - 签名意图：输入: 目录列, 配置 / 输出: (窗, y, 组) 三元组列 / 错误: TrainError
  - 调用方：train_tcn
  - tested 策略：上游覆盖: train_tcn
  - 核验命令：上游覆盖: train_tcn
- **_probe_fit** [L2|补记]
  - 职责：岭正则最小二乘拟合探针
  - 签名意图：输入: X[N,3F], y / 输出: (w, b) / 错误: 无
  - 调用方：train_tcn
  - tested 策略：上游覆盖: train_tcn
  - 核验命令：上游覆盖: train_tcn
- **_window_summary** [L2|补记]
  - 职责：窗→[3F] 统计摘要（末值/均值/斜率，NaN 安全）
  - 签名意图：输入: [T,F] / 输出: (摘要, 填充列) / 错误: 无
  - 调用方：train_tcn
  - tested 策略：上游覆盖: train_tcn
  - 核验命令：上游覆盖: train_tcn
- **_sparse_recall** [L2|补记]
  - 职责：稀疏事件召回口径（选优判据）
  - 签名意图：输入: 预测列, 标签列 / 输出: float / 错误: 无
  - 调用方：train_tcn
  - tested 策略：上游覆盖: train_tcn
  - 核验命令：上游覆盖: train_tcn
- **_dist** [L2|补记]
  - 职责：两点平面距离（m）
  - 签名意图：输入: 两点 / 输出: float / 错误: 无
  - 调用方：plan_disposal
  - tested 策略：上游覆盖: plan_disposal
  - 核验命令：上游覆盖: plan_disposal
- **_dist_from_ref** [L2|补记]
  - 职责：帧到参考点距离（m）
  - 签名意图：输入: 帧, 参考点 / 输出: float 或 None / 错误: 无
  - 调用方：run_link_consistency
  - tested 策略：上游覆盖: run_link_consistency
  - 核验命令：上游覆盖: run_link_consistency
- **_score** [L2|补记]
  - 职责：窗口严重度打分+证据完整性
  - 签名意图：输入: 事件窗 / 输出: (分值, 证据列, 完整) / 错误: 无
  - 调用方：update_state
  - tested 策略：上游覆盖: update_state
  - 核验命令：上游覆盖: update_state
- **_params_for** [L2|补记]
  - 职责：场景+档位→注入参数映射
  - 签名意图：输入: 场景/档位/定义 / 输出: 参数 dict / 错误: 无
  - 调用方：inject_scenario_fault
  - tested 策略：上游覆盖: inject_scenario_fault
  - 核验命令：上游覆盖: inject_scenario_fault
- **_probe_usrp** [L2|补记]
  - 职责：USRP 在场探测（uhd 延迟导入）
  - 签名意图：输入: 配置 / 输出: 注册项或 None / 错误: 异常按缺席
  - 调用方：discover_device_module
  - tested 策略：上游覆盖: discover_device_module
  - 核验命令：上游覆盖: discover_device_module
- **_probe_ssh** [L2|补记]
  - 职责：TCP 可达探测（Jetson）
  - 签名意图：输入: 配置 / 输出: 注册项或 None / 错误: 异常按缺席
  - 调用方：discover_device_module
  - tested 策略：上游覆盖: discover_device_module
  - 核验命令：上游覆盖: discover_device_module
- **_build** [L2|补记]
  - 职责：TinyTCN 网络工厂（块+双头）
  - 签名意图：输入: 通道/层数 / 输出: Net / 错误: 无
  - 调用方：predict_risk_tcn
  - tested 策略：上游覆盖: predict_risk_tcn
  - 核验命令：上游覆盖: predict_risk_tcn
- **make_usrp_stream** [L2|补记]
  - 职责：UHD 采样流构造（设备侧，uhd 延迟导入）
  - 签名意图：输入: 模块句柄, 参数 / 输出: IQ 生成器 / 错误: USRPError
  - 调用方：capture_spectrum
  - tested 策略：上游覆盖: capture_spectrum
  - 核验命令：上游覆盖: capture_spectrum
- **_freq_axis** [L2|补记]
  - 职责：频轴生成（中心/带宽/点数）
  - 签名意图：输入: 配置 / 输出: ndarray / 错误: 无
  - 调用方：run_spectrum_monitor
  - tested 策略：上游覆盖: run_spectrum_monitor
  - 核验命令：上游覆盖: run_spectrum_monitor
- **_lift** [L2|补记]
  - 职责：占用率抬升均值（自检口径）
  - 签名意图：输入: 帧列 / 输出: float / 错误: 无
  - 调用方：sdr_check
  - tested 策略：上游覆盖: sdr_check
  - 核验命令：上游覆盖: sdr_check
- **_make_fixture** [L2|补记]
  - 职责：合成回放夹具（空闲→拥塞）
  - 签名意图：输入: 路径 / 输出: 无（落 npz） / 错误: 无
  - 调用方：sdr_check
  - tested 策略：上游覆盖: sdr_check
  - 核验命令：上游覆盖: sdr_check
- **_page** [L2|补记]
  - 职责：五页 HTML 模板壳
  - 签名意图：输入: 标题/正文 / 输出: str / 错误: 无
  - 调用方：register_pages
  - tested 策略：上游覆盖: register_pages
  - 核验命令：上游覆盖: register_pages
- **_ensure_model** [L2|补记]
  - 职责：模型工件保障（缺则合成重训）
  - 签名意图：输入: 配置 / 输出: (model, quantiles, note) / 错误: TrainError
  - 调用方：batch_eval
  - tested 策略：上游覆盖: batch_eval
  - 核验命令：上游覆盖: batch_eval
- **_already_archived** [L2|补记]
  - 职责：归档去重判定（manifest.archived_to）
  - 签名意图：输入: 运行目录 / 输出: bool / 错误: 无
  - 调用方：batch_eval
  - tested 策略：上游覆盖: batch_eval
  - 核验命令：上游覆盖: batch_eval

## 内嵌类型与交付垫片登记（随宿主单元交付，不单列函数）
- 异常类型（各宿主签名意图已含）：ConfigError/IngestError/TrainError/ConformalError/ModelArtifactError/InjectError/SitlError/SessionError/ReplayError/USRPError/BenchError/CalibError/BuildError/BundleError/MaterialError
- 承载类（职责见宿主块）：Config(load_config), SyntheticSITL(spawn_sitl), DeviceBus(run_device_bus), EventHub(pipe_events), OnlineCalibrator(calibrate_conformal), _LinearProbe(train_tcn)
- console_scripts 垫片（build_package 交付物）：ahyd_cli.shims 的 demo_main/eval_main/replay_main/sdr_main/_boot_ok
- 名实对齐记录：session_control_api 契约名与代码名 mount_control_api 曾漂移，2026-10-06 审计统一为 session_control_api（mount_control_api 保留为兼容别名）；死代码 inject_at_v 已删（无调用方）
