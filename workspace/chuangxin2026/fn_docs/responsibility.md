# 责任文档：无人机链路抗干扰测评台（STITP 一期）

> 由 fn-divide 产出与独占更新；fn-implement 只读。进度与状态见 implementation.md。
> 职责字段是**重写规约**：凭职责详述 + 签名意图（输入/输出），必须能完美复现该函数功能。
> **实现期发现结构性变化（函数增/删/拆/并/职责或调用关系变化）必须回到本阶段改本文档**（快速确认通道除外，须留变更说明）。
> 产出依据：fn_docs/requirements.md（2026-10-03 严格重跑版，R1–R12，用户门口确认）。

## 结构概览（纯结构，不带职责）

- generate_jamming ← R1
  - synthesize_style
- calibrate_power ← R2
- collect_dut_samples ← R3
  - start_dut_source
    - parse_serial_line
- record_run_streams ← R4
  - compute_spectrum_stats
- execute_scenario ← R5
  - plan_steps
  - check_failure
- index_dataset ← R6
- train_classifier ← R7
  - make_spectrogram
  - grouped_cv_split
- predict_style ← R7
- run_demo ← R8
- build_report ← R8
  - plot_triple_curves
- create_instrument_backend ← R9
- serve_console ← R10
- bridge_to_sitl ← R11 [P1]
- animate_link_state ← R12 [P1]
# ── 演进轮一增量（R13–R16，2026-10-03）──
- launch_console ← R13
- build_mid_material ← R16
- serve_console ← R10+R13 [改造：+render_static_pages]
- execute_scenario ← R5+R14+R15 [改造：+scaled_criteria/+apply_calibration/+resume_from]
- shared 增：register_cjk_font

## 需求覆盖矩阵（P1 在 R 号后标注；非功能约束不进矩阵，fn-close 终检对照 requirements 非功能节）

| 需求 | 顶层函数 |
|---|---|
| R1 | generate_jamming |
| R2 | calibrate_power |
| R3 | collect_dut_samples |
| R4 | record_run_streams |
| R5 | execute_scenario |
| R6 | index_dataset |
| R7 | train_classifier, predict_style（训练与推理两个程序入口） |
| R8 | run_demo, build_report（演示编排与报告生成两个程序入口） |
| R9 | create_instrument_backend（仪表插槽工厂；链路插槽=start_dut_source、样式插槽=synthesize_style 注册表——三插槽契约见 R9 块引言） |
| R10 | serve_console |
| R11 [P1] | bridge_to_sitl |
| R12 [P1] | animate_link_state |
| R13 | launch_console；serve_console [改造]（报告中心/帮助页，经 render_static_pages） |
| R14 | execute_scenario [改造]（scaled_criteria 判据同步缩放+倍率入 run 目录，build_report 出脚注） |
| R15 | execute_scenario [改造]（apply_calibration 功率换算+resume_from 断点续跑）；build_report [改造]（标定状态行） |
| R16 | build_mid_material |

## 共享函数（shared/：多顶层共用；矩阵挂全部受益需求）

- **load_scenario**（调用方：generate_jamming, record_run_streams, execute_scenario, serve_console, run_demo）
  - 职责：把场景 YAML 的唯一输入格式解析为强类型场景对象（注入段/判据/安全顶/记录开关）；做语义校验（频段范围 2400–2483.5MHz、样式名在注册表内、功率不超过安全顶 0dB、判据参数非负），任何一项不合法即拒载。
  - 签名意图：输入: 场景 YAML 路径 / 输出: 场景对象（含全部段落） / 错误: 文件缺失或 schema/语义不合法→抛异常并指明字段名。
  - tested 策略：自有单测
  - 核验命令：测试: test_load_scenario（合法卡载入+四类非法卡各拒一）
- **write_sigmf**（调用方：generate_jamming, record_run_streams）
  - 职责：把一段复基带 IQ 与真值标注（样式/功率档/时间窗）写为一对 sigmf-data/sigmf-meta 文件，符合 SigMF v1.2.0；标注字段完整（后续 dataset 分组与训练真值的唯一来源）。
  - 签名意图：输入: 输出基名, IQ 数组, 标注列表 / 输出: 两个文件路径 / 错误: 写入失败抛异常。
  - tested 策略：自有单测
  - 核验命令：测试: test_write_read_sigmf（写后 sigmf 库校验通过且标注可读回）
- **read_sigmf**（调用方：train_classifier, predict_style, index_dataset）
  - 职责：读一对 SigMF 文件为 (IQ, meta)；校验格式合法与标注齐全，缺失即报错（供数据集校验与推理输入共用）。
  - 签名意图：输入: 录制基名 / 输出: (IQ 数组, meta 字典) / 错误: 文件缺失/校验不过抛异常并含原因。
  - tested 策略：自有单测
  - 核验命令：测试: test_write_read_sigmf（与 write 成对往返）
- **EstopManager**（类；调用方：execute_scenario, record_run_streams, serve_console）
  - 职责：全局急停管理。arm(callback) 注册停发射回调；fire(reason) 按注册序同步触发全部回调并置位（本次运行内状态只升不降）；state 报 armed/fired 与原因摘要。任何异常退出路径先经它停发射。
  - 签名意图：输入: arm=回调函数, fire=原因字符串 / 输出: state 属性 / 错误: 回调抛错不阻断其余回调执行。
  - tested 策略：自有单测
  - 核验命令：测试: test_estop（注册两回调→fire→按序都执行且幂等）

## 功能块 generate_jamming ← R1

（块引言：R1 六类干扰样式生成引擎。按场景注入段参数化生成单音/扫频/啁啾/带限噪声/部分频带/脉冲六类复基带波形，经仪表后端发射并同步 SigMF 归档；dry-run 只产参数表不出射频。样式集为插件注册表——新样式=注册新构建函数，本引擎主体零改动。）

- **generate_jamming** [L0|新增]
  - 职责：接收注入段，逐样式合成波形→经仪表后端发射（dry-run 则跳过）→录制归档 SigMF（真值标注=样式/功率档/时间窗）→返回结果对象（路径+样式元数据+错误清单）。参数越界或设备失联：立即停发射、errors 非空、ok=False。
  - 签名意图：输入: 注入段对象, {dry_run, 输出目录, 后端名} / 输出: 结果对象（ok/dry_run/sigmf 路径/样式元数据/错误清单） / 错误: 越界/失联→先停发再返回失败结果。
  - 调用方：程序入口（gen 命令）
  - tested 策略：自有单测（dry-run 路径+mock 后端）
  - 核验命令：测试: R1 冒烟（dry-run 参数表+短时发射 SigMF 标注+瀑布目视）——继承 R1 验收方式
  - **synthesize_style** [L1|新增]
    - 职责：按样式名从注册表分发到对应构建器，合成一段复基带 IQ。样式名不在注册表→明确报错。注册表即样式插槽（新样式=注册新构建函数，不改调用方）。
    - 签名意图：输入: 样式名, 参数（频率/带宽/时长/采样率/样式专有参数） / 输出: 复基带 IQ 数组+样式元数据 / 错误: 未知样式/参数非法抛异常。
    - 调用方：generate_jamming
    - tested 策略：自有单测
    - 核验命令：测试: test_synthesize_style（六样式各出非零 IQ+未知样式拒）

## 功能块 calibrate_power ← R2

（块引言：R2 功率标定与步进。建立"软件增益细档×衰减器粗档→注入功率"的标定表，供执行器把场景功率档换算为后端可执行值；单调性检查保证步进可信。）

- **calibrate_power** [L0|新增]
  - 职责：对频点×增益档组合逐档实测（或按后端提供的传递函数计算），产出 calibration.json（频点×档位→注入功率表），并做单调性检查：相邻档差值与设定步距偏差>1dB 即在结果中告警。首版实测偏差如实入表。
  - 签名意图：输入: 频点列表, 增益档列表, 输出目录 / 输出: 标定结果（表路径/单调性是否通过/最大偏差/条目数） / 错误: 后端失联→中止并报错。
  - 调用方：程序入口（calibrate 命令）、execute_scenario（内部取表）
  - tested 策略：自有单测（mock 后端传递函数）
  - 核验命令：测试: R2 标定（产表+单调性检查打印）——继承 R2 验收方式

## 功能块 collect_dut_samples ← R3

（块引言：R3 被测双链路采集。真实链路（ESP32 WiFi/NRF24，串口 JSON 行 1Hz）与合成链路同接口——统一样本流是链路插槽的契约形态；串口异常记事件不中断采集。）

- **collect_dut_samples** [L0|新增]
  - 职责：按场景声明的链路清单启动样本源，在给定时长内（或直到回调停止）持续收集样本并逐条回调；串口断连/序号跳变记 gap 事件继续采集；返回样本与事件清单。
  - 签名意图：输入: 链路清单, 时长, 逐条回调 / 输出: (样本列表, gap/异常事件列表) / 错误: 全部链路失联→返回已收内容并报错。
  - 调用方：程序入口（dut --watch）、record_run_streams
  - tested 策略：自有单测（合成源路径）
  - 核验命令：测试: R3 空跑（5 分钟本底 PER/拔线 gap/合成与真实同接口）——继承 R3 验收方式
  - **start_dut_source** [L1|新增]
    - 职责：链路插槽工厂——按配置返回真实串口源或合成源，两者产出同构样本流（合成源按 jam_profile 生成指定 PER 台阶，供无硬件演示与开发）。未知链路类型拒启。
    - 签名意图：输入: 链路配置（类型/串口名或合成档案/种子） / 输出: 样本流对象（可迭代+可关闭） / 错误: 串口打不开/未知类型抛异常。
    - 调用方：collect_dut_samples
    - tested 策略：自有单测（合成源）；真实源上游覆盖
    - 核验命令：测试: test_start_dut_source（合成源出流+未知类型拒）
    - **parse_serial_line** [L2|新增]
      - 职责：一行串口 JSON→样本对象（字段与串口契约一致：link/seq/ts/per/计数/RSSI 或 NRF 计数/fw）；字段缺失或 seq 回退跳变抛出携带字段名的异常（上层转 gap 事件）。
      - 签名意图：输入: 一行字节 / 输出: 样本对象 / 错误: 非法 JSON/字段缺失/seq 异常→异常含字段名。
      - 调用方：start_dut_source（真实源分支）
      - tested 策略：自有单测
      - 核验命令：测试: test_parse_serial_line（合法行/缺字段行/seq 跳变行三分支）

## 功能块 record_run_streams ← R4

（块引言：R4 三路统一采集与时间对齐。DUT 样本∥监测谱统计∥注入事件三路汇流，统一打主机单调钟时间戳，落 run 目录标准产物；时间轴覆盖率≥99%。）

- **record_run_streams** [L0|新增]
  - 职责：一次运行期间并行采集三路（复用 collect_dut_samples 取 DUT 流；驱动监测通道取谱统计；接收执行器注入事件），统一时间戳，按 run 目录标准布局落盘（kpi.csv/events.jsonl/monitor.csv）；异常先经 EstopManager 停发射再抛出；结束时计算覆盖率。
  - 签名意图：输入: 场景对象, 时长, run 目录, {是否带注入} / 输出: 记录结果（各产物路径/覆盖率） / 错误: 设备失联→急停后抛异常。
  - 调用方：程序入口（record 命令）、execute_scenario
  - tested 策略：自有单测（合成源+mock 后端）
  - 核验命令：测试: R4 对齐（60s 三路行数一致率≥99%+事件±50ms 判定）——继承 R4 验收方式
  - **compute_spectrum_stats** [L1|新增]
    - 职责：一段监测 IQ→谱统计（峰值频率/占用度/平坦度/总功率），供 JSR 实测估计与带限噪声平坦度自检。
    - 签名意图：输入: IQ 数组, 采样率 / 输出: 统计字典 / 错误: 空输入抛异常。
    - 调用方：record_run_streams
    - tested 策略：自有单测（合成正弦+带限噪声）
    - 核验命令：测试: test_compute_spectrum_stats

## 功能块 execute_scenario ← R5

（块引言：R5 国标步进执行器。GB 42590 §5.11 协议的编排主体：读场景→取标定→按"样式外层×功率内层"步进注入→每步判失效→记录失效电平→交 record/build_report 出产物；断点续跑；执行器与仪表后端解耦（后端由 R9 工厂注入）。）

- **execute_scenario** [L0|新增]
  - 职责：完整执行一张场景卡：装载→校验→建步进计划→逐步（设样式/设功率/开→采集→判失效→关）→失效即停该样式记录电平→全部样式完成后产出 run 目录（KPI/事件/监测/SigMF）并调报告生成；对照卡（无注入）跑完须报告"未失效"；支持从 run 目录进度断点续跑；任何异常先急停。
  - 签名意图：输入: 场景路径（或断点 run 目录） / 输出: 执行结果（各步结果/各样式失效电平表/对照误报标志/报告路径） / 错误: 装载或后端失败→急停并返回失败。
  - 调用方：程序入口（run 命令）、serve_console（卡片一键测）、run_demo
  - tested 策略：自有单测（mock 后端+合成链路全流程）
  - 核验命令：测试: R5 双卡（国标卡产失效电平表+三元曲线+报告；对照卡不误报）——继承 R5 验收方式
  - **plan_steps** [L1|新增]
    - 职责：注入段→有序步进清单（样式外层循环×功率内层自 power_start 起按 step 递增至 power_stop 封顶）；纯计算无副作用，断点续跑据此切片。
    - 签名意图：输入: 注入段对象 / 输出: 步进列表（序号/样式/功率/时长） / 错误: 注入段为空（对照卡）→返回空表。
    - 调用方：execute_scenario
    - tested 策略：自有单测
    - 核验命令：测试: test_plan_steps（六样式×阶梯展开+对照空表）
  - **check_failure** [L1|新增]
    - 职责：按判据（PER≥阈值持续 sustain_s，或断连≥disconnect_s）判定最近 KPI 窗口是否失效并给出类型；纯函数。
    - 签名意图：输入: KPI 窗口样本列表, 判据对象 / 输出: (是否失效, 失效类型) / 错误: 空窗口→(False, "")。
    - 调用方：execute_scenario
    - tested 策略：自有单测
    - 核验命令：测试: test_check_failure（越界/未持续/断连/空窗四分支）

## 功能块 index_dataset ← R6

（块引言：R6 SigMF 真值数据集。扫描 run 产物→逐录制校验（格式+真值标注齐全）→按录制分组产 dataset_index.json——分组是训练分组 CV 的划分单位，也是对外发布的清单。）

- **index_dataset** [L0|新增]
  - 职责：遍历 runs 目录下全部 SigMF 录制，逐条校验（复用 read_sigmf 的校验语义：格式合法+annotations 含样式/功率档/时间窗），汇总错误清单；按录制组织分组并写 dataset_index.json（每条含 group 字段，非空硬要求）。
  - 签名意图：输入: runs 目录 / 输出: 索引结果（录制数/分组列表/错误清单/索引路径） / 错误: 任一录制不合法→计入错误清单（不中断整体），索引仍产出但命令以非零退出。
  - 调用方：程序入口（dataset --check）、train_classifier
  - tested 策略：自有单测（含一条坏录制的夹具目录）
  - 核验命令：测试: R6 校验（全部通过且 group 非空；坏录制被点名）——继承 R6 验收方式

## 功能块 train_classifier ← R7

（块引言：R7 训练侧。谱图七分类（六样式+无干扰），分组 CV 评测；算力后端自动选择：/toolbox 远程可用则派发，否则本地 CPU——对调用方透明。性能数字只如实记录。）

- **train_classifier** [L0|新增]
  - 职责：读数据集索引→按分组划分→逐录制生成谱图样本（真值取自标注）→训练分类模型（谱图 CNN 基线）→分组 CV 评测（混淆矩阵+Macro-F1）→模型与评测报告落盘；远程算力不可达自动降级本地并如实标注 backend。
  - 签名意图：输入: 数据集目录, 输出目录, {backend=auto/toolbox/local} / 输出: 训练结果（模型路径/backend/Macro-F1/混淆矩阵图/报告路径） / 错误: 数据集为空或索引缺失→拒训。
  - 调用方：程序入口（train 命令）、run_demo
  - tested 策略：自有单测（小合成数据集端到端）
  - 核验命令：测试: R7 训练端到端（产模型+分组 CV 报告）——继承 R7 验收方式
  - **make_spectrogram** [L1|新增]
    - 职责：复基带 IQ→幅度谱图矩阵（频率×时间）；训练与推理共用的唯一谱图口径。
    - 签名意图：输入: IQ 数组, {nfft, hop} / 输出: 谱图矩阵 / 错误: 空输入抛异常。
    - 调用方：train_classifier, predict_style
    - tested 策略：自有单测
    - 核验命令：测试: test_make_spectrogram（形状+能量非零）
  - **grouped_cv_split** [L1|新增]
    - 职责：数据集索引→n 折分组划分（同组同侧，杜绝段级泄漏）；纯函数。
    - 签名意图：输入: 索引路径, 折数 / 输出: [(训练组列表, 测试组列表)] / 错误: 组数<折数→抛异常。
    - 调用方：train_classifier
    - tested 策略：自有单测
    - 核验命令：测试: test_grouped_cv_split（无交集+全覆盖）

## 功能块 predict_style ← R7

（块引言：R7 推理侧。对单条录制分段预测样式并与真值并列输出——验收演示与报告"识别样例"的来源。）

- **predict_style** [L0|新增]
  - 职责：载入模型→读录制→分段谱图→逐段预测样式与概率→与标注真值并列返回。
  - 签名意图：输入: 模型路径, 录制基名 / 输出: 预测列表（段/预测样式/真值/概率表） / 错误: 模型或录制缺失→异常。
  - 调用方：程序入口（predict 命令）、build_report、run_demo
  - tested 策略：自有单测（合成模型+合成录制）
  - 核验命令：测试: R7 预测（输出与真值并列打印）——继承 R7 验收方式

## 功能块 run_demo ← R8

（块引言：R8 一键演示编排。一条命令串起短场景→小样本推理→报告；与操控台"一键演示"按钮同底层；quick 路径走合成数据（无硬件可演示）。）

- **run_demo** [L0|新增]
  - 职责：编排：选短场景（quick=合成链路+mock 或真实后端按可用性）→execute_scenario→（可选）predict_style 小样本→build_report；返回报告路径，退出码即成败。
  - 签名意图：输入: {quick} / 输出: report.md 路径 / 错误: 任一环节失败→返回失败并保留现场 run 目录。
  - 调用方：程序入口（demo 命令）、serve_console（演示按钮）
  - tested 策略：自有单测（quick 合成路径）
  - 核验命令：测试: R8 demo --quick（一条命令退出码 0+report 生成+数字可溯源）——继承 R8 验收方式

## 功能块 build_report ← R8

（块引言：R8 自动报告。run 目录→report.md：场景/标定表/三元曲线/失效电平表/识别样例+固定仪器局限声明；一切数字取自本 run 产物。）

- **build_report** [L0|新增]
  - 职责：读 run 目录全部产物→绘图（三元曲线）→汇总失效电平表→（有模型则附识别样例）→生成 report.md（含固定声明：非 CISPR 测量接收机、GB 42590 §5.11 方法学预研、EN 300 328 传导等效口径）；数字仅引用本 run 实测。
  - 签名意图：输入: run 目录 / 输出: report.md 路径（+figs） / 错误: 产物缺失→缺什么报什么。
  - 调用方：execute_scenario, run_demo, 程序入口（report 命令）
  - tested 策略：自有单测（合成 run 夹具）
  - 核验命令：测试: R8 报告（report 生成+内嵌图有效+数字溯源抽查）——继承 R8 验收方式
  - **plot_triple_curves** [L1|新增]
    - 职责：KPI CSV→标准三图（PER-vs-JSR、吞吐/时延-vs-JSR、失效事件时间线）PNG 落 figs/。
    - 签名意图：输入: kpi.csv 路径, 输出目录 / 输出: PNG 路径列表 / 错误: 数据不足以成图→跳过该图并说明。
    - 调用方：build_report
    - tested 策略：自有单测
    - 核验命令：测试: test_plot_triple_curves（三图产出）

## 功能块 create_instrument_backend ← R9

（块引言：R9 插件式扩展层·仪表插槽。全平台仪表访问的唯一入口：按配置返回干扰源/分析仪后端对象，接口固定（set_style/set_power_db/on/off、get_spectrum）。B210 为首个实现；未来 SCPI 仪表=PyVISA 新实现同接口注册进来；mock 后端供测试与无硬件演示。**可扩展性硬约束的落点**：新仪表=新后端实现，场景格式与执行器主体零改动——三插槽分布：仪表=本工厂，链路=start_dut_source，样式=synthesize_style 注册表。）

- **create_instrument_backend** [L0|新增]
  - 职责：后端工厂——按名称（b210/pyvisa/mock）构造并返回 (干扰源对象, 分析仪对象)；对象实现固定接口；未知名称或驱动不可用（如未装 UHD/PyVISA）→构造失败并给出可操作提示。
  - 签名意图：输入: 后端名, {设备参数} / 输出: (干扰源, 分析仪) 对象对 / 错误: 未知后端/驱动缺失/设备打开失败→异常含提示。
  - 调用方：generate_jamming, calibrate_power, execute_scenario, run_demo
  - tested 策略：自有单测（mock 后端；b210 分支在无驱动环境下验证"失败提示"路径）
  - 核验命令：测试: R9 双证（mock 后端跑通同一场景卡=执行器不感知具体仪表；三类插槽注册与替换接口测试）——继承 R9 验收方式

## 功能块 serve_console ← R10

（块引言：R10 Web 操控台。本地服务+浏览器单页：驾驶舱（选卡/滑杆/开始-暂停-急停）+实时仪表盘+场景卡片一键测+历史对比+报告中心；WS 实时推送；急停端点直接触发 EstopManager；后端异常→全局告警+自动急停。无头自检覆盖服务/健康/心跳/急停四点。）

- **serve_console** [L0|新增]
  - 职责：构建并启动操控台服务（REST 端点：健康/场景清单/开始/停止/急停/历史/报告/演示；WS：kpi/事件/状态推送；静态单页托管）；内部调用 execute_scenario/run_demo 复用编排；急停=立即停发射的硬通道；自检模式完成四点检查后退出。
  - 签名意图：输入: {host, port, selftest} / 输出: 服务运行（或自检退出码） / 错误: 端口占用/依赖缺失→异常；运行中异常→告警+自动急停。
  - 调用方：程序入口（ui 命令、自检脚本）
  - tested 策略：自有单测（自检模式，TestClient 无头）
  - 核验命令：测试: R10 自检（服务起/健康 200/WS 心跳/急停生效）+人工零代码走查——继承 R10 验收方式

## 功能块 bridge_to_sitl ← R11 [P1]

（块引言：R11 SITL 链路退化注入预研（姊妹项目联动，单向输出）。把实测 PER-功率台阶映射为 ArduPilot SITL 丢包/时延注入，产出联调记录。）

- **bridge_to_sitl** [L0|新增|P1]
  - 职责：读 run 的 KPI 台阶→换算为注入时间线→经 pymavlink 注入 SITL→验证 SITL 日志出现对应链路质量变化→联调截图与记录入 run 目录。
  - 签名意图：输入: run 目录, SITL 地址 / 输出: 无（产物入 run 目录） / 错误: SITL 不可达→报错留待人工。
  - 调用方：程序入口（sitl_bridge 命令）
  - tested 策略：自有单测（mock SITL）
  - 核验命令：测试: R11 联调（SITL 日志台阶对应+截图入档）——继承 R11 验收方式

## 功能块 animate_link_state ← R12 [P1]

（块引言：R12 2D 示意动画（非重点，不阻塞验收）。链路光带变色/断裂、干扰波纹随实测/合成数据驱动；有余力再做，R10 验收不含动画硬项。）

- **animate_link_state** [L0|新增|P1]
  - 职责：订阅样本流→驱动 Canvas 场景状态机（光带颜色/断裂按 PER 阈值分级；波纹形态按样式映射）；提供演示模式（合成 jam_profile 播放）。
  - 签名意图：输入: 样本流（或演示档案）, 画布 / 输出: 动画状态（与 KPI 数值联动） / 错误: 数据断流→保持末态并标注。
  - 调用方：serve_console（前端引入）
  - tested 策略：上游覆盖: serve_console（联动一致性为人工判据）
  - 核验命令：上游覆盖: serve_console——继承 R12 验收方式（若实现：演示模式联动判据三要素）

---

## 产出前自检（双向拦截假完成）

- **矩阵正向**：R1–R12 每条至少一个顶层函数负责 ✓（R7/R8 各两入口=各自两条验收命令；R9 三插槽分布：create_instrument_backend+start_dut_source+synthesize_style）。
- **矩阵反向 + 树**：全部 27 个函数均有调用链抵达程序入口 ✓（parse_serial_line→start_dut_source→collect_dut_samples→入口；共享函数调用方各标 3–5 个顶层；无死代码）。
- **单一功能转变**：逐块复核 ✓——每块职责只做一件事；"发射+归档"是同一转变的两面（一次受控注入的完整产出），未再出现复合不相干转变。
- **函数总数 27 > 20 → 预警**（已向用户呈现，见门口报告；收缩选项待用户裁决）。


---

## 演进轮一增量块（R13–R16，2026-10-03；受影响旧块以 [改造] 说明目标态，旧块原文未动）

## 功能块 launch_console ← R13

（块引言：产品最后一公里的入口件——双击即用。start.sh/start.bat 与 scripts/launch.py 的核心：起操控台服务、自动打开浏览器、失败给可操作提示；--selfcheck 自检模式供验收。）

- **launch_console** [L0|新增]
  - 职责：以子进程/线程启动操控台服务（复用 serve_console），等待 /api/health 就绪后用系统默认浏览器打开操控台地址；端口被占/依赖缺失→打印可操作提示（装依赖/换端口）退出非 0；--selfcheck 只验证"服务起+健康检查过+URL 打印"不起浏览器，返回退出码。
  - 签名意图：输入: {host, port, selfcheck, no_browser} / 输出: 退出码（0=成功拉起） / 错误: 服务起不来→提示后非 0 退出。
  - 调用方：程序入口（scripts/launch.py；start.sh/start.bat 包装）
  - tested 策略：自有单测（selfcheck 路径，无头）
  - 核验命令：测试: R13 启动器自检（start.sh --selfcheck rc=0，URL 打印）——继承 R13 验收方式

## 功能块 build_mid_material ← R16

（块引言：中期材料编译线。docs/build.py 的核心：定位最新 run 目录→汇编失效电平表/三元曲线/识别指标/仪器局限声明为 Markdown 材料稿；数字仅引自 runs 产物与 metrics.json。）

- **build_mid_material** [L0|新增]
  - 职责：扫描 runs/ 取最新完整 run（含 report.md 与 steps.jsonl）→读取失效电平/步进记录/识别指标（train_report.md 若在）→按模板生成材料稿（含图相对链接、固定仪器局限声明、数字来源注记）；--final 走同模板加深版（结题轮用）。任何稿内数字必须能在所引 run 产物中找到，否则生成失败并指明。
  - 签名意图：输入: {mode: mid|final, runs_dir, out_path} / 输出: 材料稿路径 / 错误: 无可用 run/数字溯源失败→非 0 退出并列出失败数字。
  - 调用方：程序入口（docs/build.py）
  - tested 策略：自有单测（夹具 run 目录）
  - 核验命令：测试: R16 编译（build.py --mid 产 mid_draft.md+数字溯源断言）——继承 R16 验收方式

## 增量子函数块

- **render_static_pages** [L1|新增]（挂 serve_console 子树，R13）
  - 职责：操控台静态页渲染——/reports 报告中心（历史 run 列表+单报告 Markdown→HTML 渲染，复用既有 /api/runs 与 /api/runs/{name}/report 数据）与 /help 快速上手页（零术语：五步走查流程+急停说明）。
  - 签名意图：输入: HTTP 请求（路径参数 run 名） / 输出: HTML 响应 / 错误: run 不存在→404 页。
  - 调用方：serve_console
  - tested 策略：上游覆盖: serve_console
  - 核验命令：上游覆盖: serve_console——继承 R13 验收（零代码走查含"点开历史报告"）
- **register_cjk_font**（shared 增，R13）
  - 职责：把仓库内置 OFL 中文字体注册进 matplotlib（font_manager），幂等；注册后全平台渲染中文标签零 findfont fallback 告警。
  - 签名意图：输入: 无（字体文件路径内定于包内资源） / 输出: 注册后的字体名 / 错误: 字体文件缺失→异常（属打包错误，立即暴露）。
  - 调用方：plot_triple_curves, train_classifier
  - tested 策略：自有单测
  - 核验命令：测试: R13 字体测试（渲染三图断言无 fallback 告警）
- **scaled_criteria** [L1|新增]（挂 execute_scenario 子树，R14）
  - 职责：纯函数——按速度因子返回同步缩放后的判据（sustain_s/disconnect_s 除以倍速，等效真实时间口径；safety 顶不动）与倍率信息（供写 run 目录 speed.json）。
  - 签名意图：输入: 判据对象, speed: float / 输出: (缩放后判据, {speed, note}) / 错误: speed<=0→ValueError。
  - 调用方：execute_scenario
  - tested 策略：自有单测
  - 核验命令：测试: R14（40 速国标卡 fail_levels 非空+报告脚注 grep）——继承 R14 验收
- **apply_calibration** [L1|新增]（挂 execute_scenario 子树，R15）
  - 职责：纯函数——读 calibration.json（存在）→对给定功率档按频点查表/内插换算后端增益并返回来源标注；文件缺省→恒等映射+"未标定"标注。
  - 签名意图：输入: 功率档 dB, 频点 Hz, calibration 路径 / 输出: (后端增益 dB, 来源: "calibrated|identity") / 错误: 表损坏→按 identity 降级并附告警。
  - 调用方：execute_scenario
  - tested 策略：自有单测（有表/无表两分支）
  - 核验命令：测试: R15（标定存在时 report 含"标定表已应用"）——继承 R15 验收
- **resume_from** [L1|新增]（挂 execute_scenario 子树，R15）
  - 职责：纯函数——读 run 目录 steps.jsonl 进度→返回（起跑步索引, 已完成步记录清单, kpi 追加模式标志）；无进度/已完成→(0, [], False)/完成态。
  - 签名意图：输入: run 目录, 完整步进计划 / 输出: (start_index, done_records, finished: bool) / 错误: 进度文件损坏→从 0 重跑并记事件。
  - 调用方：execute_scenario
  - tested 策略：自有单测（半程夹具）
  - 核验命令：测试: R15（半程 run 重跑 steps 总数=计划数且不重复）——继承 R15 验收

## 受影响旧块 [改造] 目标态（原文未动，实现期经快速通道）

- **serve_console** [改造 ← R13]：职责在原范围内补足"报告中心页+帮助页"（经新子 render_static_pages 挂载 /reports 与 /help），其余行为不变。
- **execute_scenario** [改造 ← R14/R15]：步进循环改为消费 scaled_criteria 判据与 apply_calibration 换算后的增益；启动时经 resume_from 断点续跑（同 run 目录续写）；倍率信息写 run 目录 speed.json。
- **build_report** [改造 ← R14/R15]：读 run 目录 speed.json→追加"加速倍率 N×（判据同步缩放）"脚注；读标定应用状态→"标定表已应用/未标定"行。

## 演进轮一自检

- 矩阵正向：R13–R16 各有顶层负责 ✓（R13=launch_console+serve_console 改造；R14/R15=execute_scenario 改造；R16=build_mid_material）。
- 反向：launch_console→程序入口 ✓；build_mid_material→程序入口 ✓；render_static_pages→serve_console→入口 ✓；register_cjk_font 调用方两顶层 ✓；scaled_criteria/apply_calibration/resume_from→execute_scenario→入口 ✓。无死代码。
- 单一转变：逐块复核 ✓。
- 函数总数 27+7=34（>20 预警延续——12+4 需求口的系统广度所致，门内已两轮确认接受）。
