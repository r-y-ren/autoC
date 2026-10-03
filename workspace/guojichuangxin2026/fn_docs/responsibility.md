# 责任文档：安航云盾演示系统（材料冲刺版）
> 由 fn-divide 产出与独占更新；fn-implement 只读。进度与状态见 implementation/。
> 职责字段是**重写规约**：凭职责详述 + 签名意图（输入/输出），必须能完美复现该函数功能。
> ⚠ 实现期发现结构性变化（函数增/删/拆/并/职责或调用关系变化）必须停下回本阶段改本文档。
> ⚠ 函数总数 43 > 20 预警线（scaffold 落桩实测 43，此前文档误记 34/38 已修正）：本任务为 9 需求口的系统级工程（数据/双通道模型/SDR/状态机/Web/演示控制台/材料），非单一算法任务；收缩建议见文末，门口裁决。

## 结构概览（纯结构，不带职责）
- run_ingest ← R1
  - connect_sitl
  - normalize_telemetry
  - aggregate_imu_features
  - compute_physical_margins
  - replay_check
- run_progressive_risk ← R2
  - build_feature_window
  - predict_risk_tcn
  - calibrate_conformal
  - check_physical_baseline
  - train_tcn
- run_sudden_fault ← R3
  - build_residuals
  - cusum_detect
  - classify_fault
- run_link_consistency ← R4
  - estimate_distance_trend
  - consistency_residual
- run_spectrum_monitor ← R5
  - capture_spectrum
  - compute_occupancy
  - sdr_check
- run_safety_state_machine ← R6
  - update_state
  - plan_disposal
- run_ground_station ← R7
  - pipe_events
  - register_pages
- launch_demo_session ← R9
  - spawn_sitl
  - session_control_api
  - render_console
- build_materials ← R8
  - export_metrics_table
  - compile_documents
  - draft_revision_notes
- load_config
- open_run_dir
- append_record
- load_model_artifact
- run_eval
- inject_scenario_fault

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

## 共享函数（shared：多顶层共用；矩阵挂全部受益需求）
- **load_config**（调用方：程序入口, run_ingest, run_progressive_risk, run_sudden_fault, run_link_consistency, run_spectrum_monitor, run_safety_state_machine, run_ground_station, build_materials, run_eval, train_tcn, replay_check, sdr_check, launch_demo_session）
  - 职责：读取场景定义、阈值、模型路径、运行参数的 YAML 配置，做模式校验（缺字段/类型错/取值域越界即报错），返回冻结配置对象；默认值集中在默认配置文件，不散落代码。
  - 签名意图：输入: 配置文件路径（可选，缺省读包内默认） / 输出: 冻结配置对象（dataclass 树） / 错误: 配置缺失或校验失败抛 ConfigError 并指明字段
  - tested 策略：自有单测
  - 核验命令：测试: tests/test_load_config.py
- **open_run_dir**（调用方：run_eval, run_ingest, run_spectrum_monitor, launch_demo_session）
  - 职责：创建带时间戳与场景标签的运行目录，落运行清单（配置快照+随机种子+机器信息），返回目录路径句柄；同秒冲突自动加序号。
  - 签名意图：输入: 根目录, 场景名, 种子 / 输出: 运行目录路径 / 错误: 根目录不可写抛 IOError
  - tested 策略：自有单测
  - 核验命令：测试: tests/test_open_run_dir.py
- **append_record**（调用方：run_ingest, run_progressive_risk, run_sudden_fault, run_spectrum_monitor, run_safety_state_machine, run_eval, launch_demo_session）
  - 职责：把一条事件或度量记录以 JSON 行追加写入运行目录的 events.jsonl / metrics 分片文件，保证进程内写序；度量键带场景与时间戳前缀。
  - 签名意图：输入: 运行目录, 记录类型（event|metric）, 载荷 dict / 输出: 无（副作用=落盘） / 错误: 磁盘失败抛 IOError
  - tested 策略：自有单测
  - 核验命令：测试: tests/test_append_record.py
- **load_model_artifact**（调用方：predict_risk_tcn, classify_fault）
  - 职责：按配置加载模型工件（PyTorch checkpoint 或轻量分类器 pickle），校验版本戳与输入特征名匹配，返回就绪模型对象；文件缺失给出明确指引（先跑 train_tcn）。
  - 签名意图：输入: 模型路径, 期望特征名清单 / 输出: 模型对象 / 错误: 文件缺失/特征不匹配抛 ModelArtifactError
  - tested 策略：自有单测
  - 核验命令：测试: tests/test_load_model_artifact.py
- **run_eval**（调用方：程序入口）
  - 职责：批量评估执行器（R2/R3/R4 验收命令本体）——按场景名与次数循环：open_run_dir → run_ingest（inject_scenario_fault 注入）→ 风险管线 → 按失控判据计时出指标（提前量 P10/中位数/达标率、确认时延 P90、类型正确率、误报数）→ append_record 汇总；输出每场景指标汇总表并落运行目录。**只读运行目录写分片，不写战役顶层 metrics.json**（那是 merge_metrics 的领地）。
  - 签名意图：输入: 场景名, 次数, 可选种子清单 / 输出: 指标汇总 dict + 运行目录清单 / 错误: 场景未定义/仿真启动失败即报错退出（非零退出码）
  - tested 策略：自有单测（回放模式跑通最小次数）
  - 核验命令：继承 R2/R3/R4 验收方式（demo.eval 本体）
- **inject_scenario_fault**（调用方：run_eval, session_control_api）
  - 职责：按场景定义在指定飞行阶段注入故障——低电量+逆风（PX4 电池参数/风参数）、电机故障（PX4 failure injection 命令）、链路退化（遥测丢弃/延迟注入）；注入时刻与参数记录进运行清单。
  - 签名意图：输入: MAVLink 控制连接, 场景名, 强度档（低/中/高）, 注入时机 / 输出: 注入回执 dict / 错误: 命令拒绝/超时抛 InjectError
  - tested 策略：自有单测（SITL 起飞注入一次）
  - 核验命令：测试: tests/test_inject_scenario_fault.py

## 功能块 run_ingest ← R1
（R1：从 PX4 SITL 读多源遥测，产 20 Hz 统一状态序列——字段字典对齐计划书 4.1，质量掩码+时间戳+缺失标记，含失控判据字段；原始遥测全量落运行目录。）

- **run_ingest** [L0|新增]
  - 职责：统一数据接入主循环——connect_sitl 建链后按 20 Hz 节拍收消息，normalize_telemetry 归一，aggregate_imu_features 压高频 IMU，compute_physical_margins 出四类物理余量，append_record 落统一状态序列与原始遥测；Ctrl-C/仿真退出时干净收尾并落清单。供 run_eval 与演示实时流两种调用形态。
  - 签名意图：输入: 配置（连接参数/速率/字段字典）, 运行目录, 可选停止条件 / 输出: 统一状态流（生成器或回调）+ 运行目录产物 / 错误: 连接失败/持续超时抛 IngestError 并落部分数据
  - 调用方：程序入口, run_eval
  - tested 策略：自有单测（SITL 短飞）+ 上游覆盖: run_eval
  - 核验命令：继承 R1 验收方式（`python -m demo.replay_check --run <目录>`）
  - **connect_sitl** [L1|新增]
    - 职责：建立 pymavlink 连接（udp/tcp/uds 可配），请求消息速率与数据流，等到心跳与首帧姿态即认为就绪；带超时与一次重试。
    - 签名意图：输入: 连接串, 超时 / 输出: 连接对象（含心跳元数据） / 错误: 超时抛 ConnectionError
    - 调用方：run_ingest
    - tested 策略：上游覆盖: run_ingest
    - 核验命令：上游覆盖: run_ingest
  - **normalize_telemetry** [L1|新增]
    - 职责：原始 MAVLink 消息批 → StateFrame（统一字段/量纲/时间戳/来源标记）；同时生成质量掩码：字段新鲜度（距上次更新时长）、取值域越界、跨源一致性（如 GNSS 与 EKF 位置差）三项合成 per-field 质量位；缺失字段置 NaN+掩码位，绝不插值冒充实测。
    - 签名意图：输入: 20 Hz 节拍内的原始消息批 / 输出: StateFrame（含 quality_mask） / 错误: 无（内部消化，异常只影响掩码）
    - 调用方：run_ingest
    - tested 策略：自有单测
    - 核验命令：测试: tests/test_normalize_telemetry.py
  - **aggregate_imu_features** [L1|新增]
    - 职责：短窗口（可配，默认 1 s）高频 IMU 原始采样 → 均方根、峰值、频带能量、偏置变化四特征，附加到对应节拍的 StateFrame；窗口样本不足时特征置 NaN+掩码。
    - 签名意图：输入: IMU 原始缓冲, 窗口参数 / 输出: 特征 dict（四键） / 错误: 无（不足即 NaN）
    - 调用方：run_ingest
    - tested 策略：自有单测
    - 核验命令：测试: tests/test_aggregate_imu_features.py
  - **compute_physical_margins** [L1|新增]
    - 职责：由 StateFrame 计算四类可解释物理余量：返航能源余量（当前电量→返航能耗估算，含逆风修正系数）、GNSS/EKF 导航可信度、链路健康度（到达间隔/序号丢包/信号质量+R4 一致性证据）、控制余量（姿态跟踪误差/振动/执行器饱和）；输出归一余量与原始量双份。产物流入 check_physical_baseline 与 update_state 消费。
    - 签名意图：输入: StateFrame 序列（需返航点配置） / 输出: margins dict（四类，各含 raw 与 normalized） / 错误: 依赖字段缺失时该类余量置 NaN+掩码
    - 调用方：run_ingest
    - tested 策略：自有单测
    - 核验命令：测试: tests/test_compute_physical_margins.py
  - **replay_check** [L1|新增]
    - 职责：R1 验收命令本体——读运行目录，统计统一帧率（≥20 Hz 判 PASS）、字段覆盖率清单（逐字段有效帧占比）、掩码分布，输出 PASS/FAIL 与明细。
    - 签名意图：输入: 运行目录（--run） / 输出: 检查报告（stdout + 报告文件）, 退出码 0/1 / 错误: 目录结构不合法报错退出
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
  - 核验命令：继承 R2 验收方式（demo.eval --scenario lowbat_headwind）
  - **build_feature_window** [L1|新增]
    - 职责：最近 10 s（可配）StateFrame+margins → 模型特征张量（定长列，掩码位转 NaN 指示列）；窗口不满时返回 None（不预测）。
    - 签名意图：输入: 帧缓冲, 窗口参数 / 输出: 特征张量或 None / 错误: 无
    - 调用方：run_progressive_risk
    - tested 策略：自有单测
    - 核验命令：测试: tests/test_build_feature_window.py
  - **predict_risk_tcn** [L1|新增]
    - 职责：TCN 前向——特征窗口 → 未来 1/3/5/10 s 进入危险状态的概率与剩余安全时间估计（多任务头）；纯函数，模型经 load_model_artifact 注入。
    - 签名意图：输入: 特征张量, 模型对象 / 输出: 概率 dict + 剩余安全时间 / 错误: 形状不匹配抛 ValueError
    - 调用方：run_progressive_risk
    - tested 策略：自有单测（小模型前向）
    - 核验命令：测试: tests/test_predict_risk_tcn.py
  - **calibrate_conformal** [L1|新增]
    - 职责：共形校准——用留出校准集的非一致性分数分位数，把点概率包装为 90% 覆盖率区间；输出区间宽度一并给出（覆盖率-宽度权衡可报告）；校准集经配置注入，运行期纯查表。
    - 签名意图：输入: 点预测 dict, 校准分位数表 / 输出: 带区间预测 dict（含上下界与宽度） / 错误: 校准表缺失抛 ConformalError
    - 调用方：run_progressive_risk
    - tested 策略：自有单测（合成数据覆盖率断言）
    - 核验命令：测试: tests/test_calibrate_conformal.py
  - **check_physical_baseline** [L1|新增]
    - 职责：物理基线判定——四类余量逐类做"持续收窄"判断（阈值+持续时长），输出基线告警与所依据余量序列；它是 TCN 之外独立的降级判据（模型不可用时仍可告警）。
    - 签名意图：输入: margins 流, 阈值配置 / 输出: 基线状态 dict（四类各自触发与否+证据窗） / 错误: 无
    - 调用方：run_progressive_risk
    - tested 策略：自有单测
    - 核验命令：测试: tests/test_check_physical_baseline.py
  - **train_tcn** [L1|新增]
    - 职责：离线训练管线——从运行目录/回放数据生成监督样本（事件标注=失控判据时刻；按架次/日期分组切分防泄漏，内联完成），训练轻量 TCN（参数量≤200 万），出验证曲线与 checkpoint+特征名清单+版本戳。
    - 签名意图：输入: 数据目录清单, 训练配置 / 输出: checkpoint+元数据+验证报告路径 / 错误: 数据不足/标注缺失抛 TrainError
    - 调用方：程序入口
    - tested 策略：自有单测（微型数据冒烟一轮）
    - 核验命令：测试: tests/test_train_tcn.py

## 功能块 run_sudden_fault ← R3
（R3：残差构造+CUSUM 变化检测+轻量分类——面向电机/电调异常与通信瞬断，考核确认时延 P90 与类型正确率。）

- **run_sudden_fault** [L0|新增]
  - 职责：突发故障主循环——build_residuals 出多通道残差，cusum_detect 确认突变，classify_fault 判来源；输出统一突发事件对象（含首触发时间、检测时延自记录）；未确认期静默。
  - 签名意图：输入: StateFrame 流, 原始遥测补充流 / 输出: 突发事件流 / 错误: 运行期错误降级为事件标注
  - 调用方：程序入口, run_eval
  - tested 策略：上游覆盖: run_eval
  - 核验命令：继承 R3 验收方式（demo.eval --scenario motor_fail）
  - **build_residuals** [L1|新增]
    - 职责：构造四类残差通道——惯导创新残差（EKF innovation）、姿态跟踪残差（设定值 vs 实测量）、转速-电流一致性残差（电机模型预期 vs 实测，缺转速时掩码）、遥测到达间隔/序号丢包序列；逐通道归一。
    - 签名意图：输入: StateFrame 流+原始遥测 / 输出: 残差通道帧流 / 错误: 无（缺源即掩码）
    - 调用方：run_sudden_fault
    - tested 策略：自有单测
    - 核验命令：测试: tests/test_build_residuals.py
  - **cusum_detect** [L1|新增]
    - 职责：多通道累积和变化检测——每通道 CUSUM 统计量越阈且持续 N 拍即确认突变，输出突变通道集与确认时刻；参数（阈值/漂移/持续拍数）入配置。
    - 签名意图：输入: 残差通道帧流, 参数配置 / 输出: 突变确认事件（通道集+时刻）或 None / 错误: 无
    - 调用方：run_sudden_fault
    - tested 策略：自有单测（阶跃注入检出时延断言）
    - 核验命令：测试: tests/test_cusum_detect.py
  - **classify_fault** [L1|新增]
    - 职责：突变确认后用轻量分类器（梯度提升树）按确认窗内通道模式判故障来源：电机异常/电调异常/链路瞬断/未知；输出类型+置信度。
    - 签名意图：输入: 确认窗内残差特征, 分类器对象 / 输出: 类型+置信度 / 错误: 模型缺失时退化为规则判型（电机类/链路类二分）并标注
    - 调用方：run_sudden_fault
    - tested 策略：自有单测
    - 核验命令：测试: tests/test_classify_fault.py

## 功能块 run_link_consistency ← R4
（R4：RSSI 时序与 GNSS 真实距离互检——统计基线版（IQR 自适应阈值），一致性残差并入 R3 特征与链路健康度。）

- **run_link_consistency** [L0|新增]
  - 职责：链路一致性主循环——estimate_distance_trend 由 RSSI 时序推距离趋势，consistency_residual 与 GNSS 距离互检出一致性残差与异常证据；证据双送：进 build_residuals 的链路通道 + 进 compute_physical_margins 的链路健康度。
  - 签名意图：输入: StateFrame 流（含 RSSI 与 GNSS 距离） / 输出: 一致性证据流 / 错误: 无（缺源即静默+掩码）
  - 调用方：程序入口, run_eval
  - tested 策略：上游覆盖: run_eval
  - 核验命令：继承 R4 验收方式（demo.eval --scenario link_degrade）
  - **estimate_distance_trend** [L1|新增]
    - 职责：滑窗内由 RSSI 时序估计距离变化趋势（对数距离路径模型的差分统计版，不假设绝对距离准确，只取趋势方向与变化率）；窗口样本不足返回 None。
    - 签名意图：输入: RSSI/时间戳缓冲, 窗口参数 / 输出: 趋势估计（变化率+置信）或 None / 错误: 无
    - 调用方：run_link_consistency
    - tested 策略：自有单测
    - 核验命令：测试: tests/test_estimate_distance_trend.py
  - **consistency_residual** [L1|新增]
    - 职责：RSSI 推距趋势与 GNSS 距离变化率的互检残差，IQR 自适应阈值判异常（仅用正常样本定阈）；输出残差值+异常位。
    - 签名意图：输入: 趋势估计, GNSS 距离序列 / 输出: 残差+异常标志 / 错误: 无
    - 调用方：run_link_consistency
    - tested 策略：自有单测
    - 核验命令：测试: tests/test_consistency_residual.py

## 功能块 run_spectrum_monitor ← R5
（R5：USRP B210 只收不发采谱 2.4G ISM——占用率/能量特征+瀑布流 WebSocket 推送；设备不可用降级回放模式。）

- **run_spectrum_monitor** [L0|新增]
  - 职责：频谱站主循环——capture_spectrum 按 RTSA 参数（中心频率/带宽/帧率）连续采谱帧，compute_occupancy 出目标信道占用率与告警，帧流经回调送 pipe_events（瀑布页）；--replay 时从回放文件读帧（设备不可用降级，输出标注 replay 模式）。
  - 签名意图：输入: 配置（频率/带宽/信道表/告警阈）, 可选设备句柄 / 输出: 占用率流+瀑布帧流 / 错误: 设备打开失败自动转回放或抛 SpectrumError（无回放源时）
  - 调用方：程序入口
  - tested 策略：上游覆盖: sdr_check
  - 核验命令：继承 R5 验收方式（demo.sdr_check + 占用率响应判据）
  - **capture_spectrum** [L1|新增]
    - 职责：UHD 采样+FFT → 功率谱帧（dBm 标定经配置的增益/校准表）；帧率与带宽参数化；设备不可用返回 None 触发上层降级。
    - 签名意图：输入: 设备参数 / 输出: 功率谱帧生成器（频率轴+功率数组） / 错误: 设备错误抛 USRPError
    - 调用方：run_spectrum_monitor
    - tested 策略：自有单测（回放文件模拟帧）
    - 核验命令：测试: tests/test_capture_spectrum.py
  - **compute_occupancy** [L1|新增]
    - 职责：功率谱帧 → 目标信道集占用率（能量占比+过阈子载波占比双口径）与帧级告警位（相对基线抬升超阈）。
    - 签名意图：输入: 功率谱帧, 信道表, 基线与阈值 / 输出: 信道占用率 dict+告警位 / 错误: 无
    - 调用方：run_spectrum_monitor
    - tested 策略：自有单测
    - 核验命令：测试: tests/test_compute_occupancy.py
  - **sdr_check** [L1|新增]
    - 职责：R5 自检命令本体——设备枚举/采样带宽/帧率自检，占用率响应检查（对比回放基线与拥塞段差异需可辨）；输出 PASS/FAIL 与明细，退出码判定。
    - 签名意图：输入: 无（读配置） / 输出: 自检报告, 退出码 0/1 / 错误: 报告内呈现（不抛）
    - 调用方：程序入口
    - tested 策略：自有单测
    - 核验命令：继承 R5 验收方式（自身即验收命令）

## 功能块 run_safety_state_machine ← R6
（R6：S0-S4 确定性状态机+处置建议——阈值+持续时间+证据完整性+迟滞；三方案能源校验出建议动作，不执行。）

- **run_safety_state_machine** [L0|新增]
  - 职责：状态机主循环——消费双通道事件+margins：update_state 出当前 S 态与转换记录（含证据链），plan_disposal 出建议动作与理由；输出统一处置建议对象（动作/理由/依据事件 ID/能源校验明细），append_record 落状态轨迹；人工接管与原飞控保护声明为独立通道（本机不重叠）。
  - 签名意图：输入: 事件流（渐进+突发）, margins 流, 任务上下文（返航点/备降点表/地理围栏） / 输出: 状态轨迹流+建议流 / 错误: 无（内部消化）
  - 调用方：程序入口, run_eval
  - tested 策略：上游覆盖: run_eval
  - 核验命令：继承 R6 验收判据（回放日志证据链+迟滞生效——demo.eval 全场景输出内含）
  - **update_state** [L1|新增]
    - 职责：单步状态转换判定——风险分值/事件严重度满足阈值+持续时间+证据完整性三条件才迁移；阈值邻域设迟滞带防抖动；输出新态+触发证据（事件 ID 清单+各项条件读数）。
    - 签名意图：输入: 当前态, 事件窗, 阈值与迟滞配置 / 输出: 新态+迁移记录（或保持） / 错误: 无
    - 调用方：run_safety_state_machine
    - tested 策略：自有单测（迁移/迟滞/证据不全不升三级用例）
    - 核验命令：测试: tests/test_update_state.py
  - **plan_disposal** [L1|新增]
    - 职责：处置建议——对返航/备降（逐备降点）/原地降落三方案算能源需求（含逆风修正），检查 GNSS/链路可用性、地理围栏、落点条件、平台权限；低电量逆风时返航须能源高于保留裕量才允许，GNSS+链路同退时禁依赖远程连续控制的策略；输出建议+全部方案校验明细（被否方案附理由）。
    - 签名意图：输入: 当前态, margins, 任务上下文 / 输出: 建议对象（动作/理由/方案明细） / 错误: 无
    - 调用方：run_safety_state_machine
    - tested 策略：自有单测（低电量逆风禁返航/双退化禁远程两用例）
    - 核验命令：测试: tests/test_plan_disposal.py

## 功能块 run_ground_station ← R7
（R7：FastAPI+WebSocket 单机服务——仪表盘/事件时间线/频谱瀑布/回放四页+控制台页，一键启动断网可用。）

- **run_ground_station** [L0|新增]
  - 职责：平台主入口——组装 FastAPI app（register_pages 挂五页路由含控制台页与 session_control_api 控制端点，pipe_events 接实时流），uvicorn 起服务（localhost 可配端口），提供静态资源与运行目录索引；`./demo.sh` 与 smoke_boot 的服务端本体；浏览器打开即进入控制台页（演示主入口）。
  - 签名意图：输入: 配置（端口/运行目录根）, 可选实时流源 / 输出: 运行中的服务（阻塞） / 错误: 端口占用抛 SystemExit 带提示
  - 调用方：程序入口
  - tested 策略：上游覆盖: sw-boot 验收
  - 核验命令：继承 R7 验收方式（`./demo.sh` 一键启动五页可看）
  - **pipe_events** [L1|新增]
    - 职责：实时流分发——订阅 run_ingest/双通道事件/状态轨迹/频谱帧的发布端，维护 WebSocket 订阅者集合并广播（JSON 序列化，背压丢帧保序策略：事件全发、频谱帧可抽稀）。
    - 签名意图：输入: 各发布端回调注册, WebSocket 连接管理 / 输出: 无（副作用=广播） / 错误: 单订阅者异常剔除不影响其余
    - 调用方：run_ground_station
    - tested 策略：自有单测（本地 WebSocket 客户端收帧）
    - 核验命令：测试: tests/test_pipe_events.py
  - **register_pages** [L1|新增]
    - 职责：挂载五个页面路由与 API——仪表盘（风险等级/剩余安全时间/能源实时）、事件时间线（含证据链展开）、频谱瀑布（历史环+实时帧）、回放页（选运行目录→时间线重放）、控制台页（render_console 的载体，含 session_control_api 控制端点挂载）；页面模板与静态资源随包分发，无外网依赖。
    - 签名意图：输入: FastAPI app, 运行目录根 / 输出: 无（副作用=路由注册） / 错误: 模板缺失启动即报
    - 调用方：run_ground_station
    - tested 策略：自有单测（五路由 GET 200 + 关键元素存在）
    - 核验命令：测试: tests/test_register_pages.py

## 功能块 build_materials ← R8
（R8：材料包——实测数字引用表（每数字带 metrics 键）、计划书逐节修订建议+可粘贴段落、材料编译入口；对外数字唯一来源=metrics 分片。）

- **build_materials** [L0|新增]
  - 职责：材料构建总入口——汇总各运行目录 metrics 分片，export_metrics_table 出数字引用表，draft_revision_notes 出计划书修订建议稿，compile_documents 编译材料（docs/build.py 本体）；供 m3 文档冲刺消费。
  - 签名意图：输入: 运行目录清单, 材料配置 / 输出: 数字引用表+修订建议稿+编译产物路径 / 错误: 分片缺失/数字不一致抛 MaterialError（阻断编译）
  - 调用方：程序入口
  - tested 策略：上游覆盖: doc-compile 验收
  - 核验命令：继承 R8 验收方式（doc-compile + doc-numbers）
  - **export_metrics_table** [L1|新增]
    - 职责：读全部 metrics 分片 → 汇总表（指标×场景×运行批次，含统计口径列与来源运行目录），并做一致性校验（同键不同值冲突即报）；不写战役顶层 metrics.json（merge_metrics 领地），只产引用表。
    - 签名意图：输入: 运行目录清单 / 输出: 引用表（Markdown+JSON 双格式） / 错误: 冲突/缺失键抛 MaterialError
    - 调用方：build_materials
    - tested 策略：自有单测
    - 核验命令：测试: tests/test_export_metrics_table.py
  - **draft_revision_notes** [L1|新增]
    - 职责：组装计划书逐节修订建议——输入=frontier-tech.md 三补强落点+实测数字引用表+演示形态描述，输出=按计划书章节组织的修订建议稿（每节：原文摘要/修订建议/可直接粘贴段落/数字占位符带 metrics 键）；团队消化改写用，含人机分工记录模板头。
    - 签名意图：输入: 引用表, 补强方案路径 / 输出: 修订建议稿（Markdown） / 错误: 引用键缺失抛 MaterialError
    - 调用方：build_materials
    - tested 策略：自有单测（占位符全闭合断言）
    - 核验命令：测试: tests/test_draft_revision_notes.py
  - **compile_documents** [L1|新增]
    - 职责：材料编译——把修订建议稿+数字回填模板编译为计划书 v2 草稿与路演 PPT（Marp）产物；编译前跑数字一致性预检（与引用表逐键对照），不过即失败退出。
    - 签名意图：输入: 材料源目录, 编译配置 / 输出: 编译产物（PDF/PPTX/MD）路径清单 / 错误: 编译器失败/数字不一致抛 MaterialError
    - 调用方：build_materials
    - tested 策略：上游覆盖: build_materials
    - 核验命令：继承 doc-compile 验收方式（docs/build.py 本体）

## 功能块 launch_demo_session ← R9
（R9：演示控制台后端——演示会话全流程 UI 化：选场景一键起飞、飞行中注入故障/调强度、中止归档、时间轴回放；演示零终端零代码。2D 指挥中心风；手动接管模式为 P1 范围外。）

- **launch_demo_session** [L0|新增]
  - 职责：演示会话编排——从控制台请求发起一次演示：open_run_dir 建运行目录 → spawn_sitl 按场景拉起仿真 → 装配 run_ingest 与风险管线/状态机（复用各顶层函数）→ 事件流接 pipe_events → 返回会话句柄（会话表：id→句柄/运行目录/控制端点）；会话中止或正常结束时归档运行清单（append_record）；同机多会话互不串流。
  - 签名意图：输入: 会话请求（场景名/强度档/可选种子）, 配置 / 输出: 会话句柄（id, 运行目录, 控制端点） / 错误: 场景未定义/SITL 拉起失败抛 SessionError（含可读原因给 UI 展示）
  - 调用方：程序入口, session_control_api
  - tested 策略：自有单测（SIH 最小场景会话冒烟：发起→收帧→中止归档）
  - 核验命令：继承 R9 验收方式（浏览器全流程判据；单测=tests/test_launch_demo_session.py）
  - **spawn_sitl** [L1|新增]
    - 职责：按场景定义拉起 PX4 SITL 进程（Gazebo 主/SIH 备选可配），等心跳就绪并做健康检查，管理进程句柄与日志文件；会话结束/异常时干净回收；同机多会话的端口/MavLink 端点分配。
    - 签名意图：输入: 场景定义, 仿真器选择 / 输出: 仿真进程句柄（含连接端点） / 错误: 拉起超时/心跳不至抛 SitlError
    - 调用方：launch_demo_session
    - tested 策略：自有单测（SIH 拉起→心跳→回收）
    - 核验命令：测试: tests/test_spawn_sitl.py
  - **session_control_api** [L1|新增]
    - 职责：控制台后端 API——UI 动作全映射：发起/中止会话（桥 launch_demo_session）、飞行中注入故障与调强度（桥 inject_scenario_fault）、回放请求（指定运行目录+时间窗）、会话状态查询；按钮按下到后端受理的响应保持演示节奏（≤2 s 目标）。
    - 签名意图：输入: HTTP/WS 控制请求 / 输出: 动作回执（含受理结果与会话状态） / 错误: 无会话/动作非法返回结构化错误给 UI 展示（不抛裸异常）
    - 调用方：register_pages
    - tested 策略：自有单测（FastAPI TestClient 打全控制端点）
    - 核验命令：测试: tests/test_session_control_api.py
  - **render_console** [L1|新增]
    - 职责：控制台页——2D 指挥中心风前端（深色主题）：地图+飞行器航迹、姿态/电量/链路仪表组、频谱瀑布嵌入、事件时间轴、故障注入面板（按钮+强度滑杆 低/中/高）、回放时间轴（暂停/加速/拖动）；模板与静态资源随包分发，无外网依赖；为答辩投屏优化（大字号/高对比）。
    - 签名意图：输入: 页面路由上下文 / 输出: 控制台页（HTML+静态资源） / 错误: 资源缺失启动即报
    - 调用方：register_pages
    - tested 策略：自有单测（路由 GET 200 + 关键元素存在：地图容器/注入面板/时间轴）
    - 核验命令：测试: tests/test_render_console.py

## 产出前自检
- 矩阵正向：R1-R9 每条恰好一个顶层函数负责 ✓（9/9，无漏实现；R9 变更后新增 launch_demo_session 块）
- 矩阵反向+树：全部 43 函数经调用链可达顶层入口 ✓（程序入口：run_eval / replay_check / sdr_check / run_ground_station / build_materials / train_tcn / launch_demo_session 及各顶层函数自身；shared 六件均被多顶层引用；无死代码；scaffold 落桩 43 与本计数一致）
- 单一功能转变：逐函数复核 ✓（compute_physical_margins 四类余量=同一转变"帧→余量"；register_pages 五路由=同一转变"挂路由"；session_control_api 多端点=同一转变"UI 动作→后端受理"）
- 函数总数 43 > 20 预警线：**已预警**——成因=9 需求口的系统级工程（接入/双通道/SDR/状态机/Web/演示控制台/材料）；可选收缩项（若要逼近 20）：①砍 train_tcn 独立函数（并入脚本，-1）②R4 两叶子合并为 consistency_check（-1）③R8 的 draft_revision_notes 并入 build_materials 主体（-1）——即便全采纳仍 ~40，低于 20 需砍需求口（不建议；R9 为用户明确要求的面向用户能力，不可砍）。门口裁决：接受 43 或指定收缩项。
