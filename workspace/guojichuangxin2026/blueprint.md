---
campaign:
  competition_id: cy-innovation-2026
  name: 安航云盾——乡村物流无人机主动安全保障平台
  theme: 高教主赛道·新工科类（低空经济）·本科生创意组（总决赛 2026-11 江苏主场）

scope:
  deliverables:
    - 商业计划书修订稿（docs/安航云盾_计划书_v2.md：采纳 strategy/frontier-tech.md 三补强项落点，按国创评审维度组织，数字全部回填 metrics）
    - 路演 PPT（校赛网评+路演 10 分钟口径，Marp 产线）
    - 演示视频（≥3 分钟：三场景 SITL 实录+边缘设备实拍+频谱联动画面）
    - 可运行演示原型 v1（PX4 SITL 三风险场景 + Jetson Orin NX 边缘推理 + USRP B210 频谱感知站 + FastAPI 地面 Web 平台，一键启动）
    - 实测数字包（软件/硬件 metrics 分片 → merge_metrics 汇总，对外材料数字唯一来源）
  out_of_scope:
    - 真实飞行与飞控硬件在环（待导师批准硬件后另立阶段，本轮只 SITL+边缘设备）
    - A2/A3 级自动处置执行（只输出建议+模拟回执，不接管控制权）
    - ArduPilot 第二飞控适配与跨品牌 A0-A3 覆盖率承诺（二期）
    - 深度相机备降点评估与 Livox 感知（二期，frontier-tech.md 存档）
    - 多机/集群场景；地面平台多用户与权限系统
    - 商业化落地与工商注册动作（创意组资格红线：未注册公司）

tech_stack:
  - name: 渐进风险预测（物理基线+TCN+共形校准层）
    kb_tech_ids: [arxiv-2608.17333, arxiv-2609.13345]
    rationale: SPACE 共形椭球给 TCN 危险概率输出有限样本覆盖率保证——"校准概率"升级为"带统计保证的风险区间"，正面回应评审对误报/可信度的追问；13345 提供不确定性量化选型总纲
    reuse_cost: 低
  - name: 突发故障识别（CUSUM 变化检测+轻量分类）
    kb_tech_ids: [arxiv-2608.22968]
    rationale: 2608.22968 的"轻量模型 vs 大模型边缘成本实证"为 Jetson 上选轻量方案提供评测协议与论证模板（AUROC+资源计量三件套），支撑 200ms 确认时延口径
    reuse_cost: 低
  - name: 链路一致性检测（RSSI-距离一致性，DroneMA 式统计基线起步）
    kb_tech_ids: [li2025DroneMADroneMobility]
    rationale: KB 卡与本项目硬件栈完全同构（Jetson+MAVLink 实飞验证），仅正样本训练适配攻击样本稀缺现实；把链路健康度从协议层（丢包/RSSI）扩展到物理层一致性证据
    reuse_cost: 低
  - name: SDR 频谱感知站（USRP B210，只收不发）
    kb_tech_ids: [rizvi2025MonitoringInterdroneService]
    rationale: 地面端第二证据源（占用率/能量+瀑布图），与机载链路遥测交叉验证；KB 卡提供干扰监测叙事锚点，方法学主源为外部论文（Saber 2026/MDPI Drones 2026，见 frontier-tech.md T3）；与隔壁电磁干扰平台战役共用设备与 GNU Radio 栈互为攻防测试环境
    reuse_cost: 中
  - name: 安全状态机与处置决策（S0-S4+能源校验+迟滞）
    kb_tech_ids: [liu2025DelaysensitiveGoodsDelivery, gao2025CSMAACMultiagentReinforcement]
    rationale: FH-MDP 的阈值结构证明与状态机降级逻辑同构（剩余续航 vs 备降点阈值触发）；CSMAAC 的"动作投影回安全域"为二期 runtime assurance 演进路线背书
    reuse_cost: 低
  - name: 边缘部署与评测协议（Orin NX Python 推理，TensorRT 后置）
    kb_tech_ids: [arxiv-2609.01126]
    rationale: 免泄漏在线评测协议直接复用为 Orin NX 部署期的评测规范（warmup 预算/资源计量），官方代码可跑；支撑"边缘实测口径"工程可信度
    reuse_cost: 低

interface_contracts:
  - between: [software, document]
    contract_file: workspace/guojichuangxin2026/contracts/sw-doc-interface.md
  - between: [software, hardware]
    contract_file: workspace/guojichuangxin2026/contracts/sw-hw-interface.md

milestones:
  - id: m0-skeleton
    task: 工程骨架（SITL 一键环境脚本+smoke_boot+统一数据字典 v1+metrics 键清单+两份接口契约实体化+材料大纲；含 B210/Orin 借用排期确认）
    owner_role: software
    depends_on: []
  - id: m1-vertical
    task: 场景1 竖切（SITL 低电量+逆风：20Hz 统一状态流→物理基线+TCN 最小版→S0-S4 状态机→Web 实时仪表盘端到端）
    owner_role: software
    depends_on: [m0-skeleton]
  - id: m2-full
    task: 全量（场景2 电机故障 CUSUM+场景3 链路退化注入+共形校准层+RSSI 一致性检测+事件回放页；三场景各 30 次评估跑批入 metrics 分片）
    owner_role: software
    depends_on: [m1-vertical]
  - id: m2b-edge
    task: 边缘与频谱（Orin NX 推理移植+P95 时延实测；USRP B210 标定+占用率响应检查；设备不可用时降级回放模式并如实注记）
    owner_role: hardware
    depends_on: [m2-full]
  - id: m3-polish
    task: 材料冲刺（计划书 v2 数字回填+路演 PPT+演示视频脚本与成片+答辩模拟人工项；按国创评审维度组织叙事）
    owner_role: document
    depends_on: [m2b-edge]

acceptance:
  checklist:
    - {id: sw-boot, category: software, item: 一键启动冒烟（SITL 场景起+Web 服务+回放页可用）, method: 自动,
       cmd: "python workspace/guojichuangxin2026/fn_work/smoke_boot.py"}
    - {id: sw-test, category: software, item: 测试套件全过, method: 自动,
       cmd: "python -m pytest workspace/guojichuangxin2026/fn_work/tests -q"}
    - {id: sw-eval-progressive, category: software, item: 渐进场景 30 次评估（提前量 P10/中位数/达标率+共形覆盖率入 metrics）, method: 自动,
       cmd: "python workspace/guojichuangxin2026/fn_work/eval.py --scenario lowbat_headwind --runs 30"}
    - {id: sw-eval-sudden, category: software, item: 突发场景 30 次评估（确认时延 P90+类型正确率入 metrics）, method: 自动,
       cmd: "python workspace/guojichuangxin2026/fn_work/eval.py --scenario motor_fail --runs 30"}
    - {id: sw-eval-link, category: software, item: 链路退化注入评估（一致性检测触发+正常段误报计数入 metrics）, method: 自动,
       cmd: "python workspace/guojichuangxin2026/fn_work/eval.py --scenario link_degrade --runs 30"}
    - {id: hw-edge, category: hardware, item: Orin NX 端到端推理 P95 时延实测入 metrics（设备不可用时降级回放模式并注记）, method: 自动,
       cmd: "python workspace/guojichuangxin2026/hardware/bench_edge.py"}
    - {id: hw-sdr, category: hardware, item: SDR 占用率响应自检（2.4G 拥塞前后占用率差异+告警触发）, method: 自动,
       cmd: "python workspace/guojichuangxin2026/fn_work/sdr_check.py"}
    - {id: doc-compile, category: document, item: 计划书 v2 与路演 PPT 编译通过, method: 自动,
       cmd: "python workspace/guojichuangxin2026/docs/build.py"}
    - {id: doc-numbers, category: document, item: 材料性能数字与 metrics 一致, method: 自动,
       cmd: "python scripts/kb/lint_kb.py --file workspace/guojichuangxin2026/docs/安航云盾_计划书_v2.md"}
    - {id: man-video, category: manual, item: 演示视频成片（三场景+整体叙事 ≥3 分钟）, method: 人工手册}
    - {id: man-rehearsal, category: manual, item: 答辩模拟 ≥1 次并按反馈迭代 PPT, method: 人工手册}

workflow:
  auto_chain: false   # 用户确认闸门翻转（2026-10-03）：手动波次编排，不开自动规格链

compliance:
  ai_policy_reviewed: true
  mode: apply
  policy_basis: >-
    官方文件无 AI 专项条款（2026-09-04 对教高函〔2026〕26号通知 38 页与评审规则 19 页核对，"AIGC/生成式/大模型/AI生成"关键词零命中）。
    红线原文："不准将核心工作外包代做。商业计划书、技术文档等核心参赛材料必须由团队成员独立完成。严禁委托第三方机构或个人进行'代工'包装或撰写。"（附件 8 参赛学生"十不准"之五）；
    "若项目材料存在弄虚作假、抄袭剽窃等违规情况，则一票否决"（评审规则必要条件）。
    来源：cy-innovation-2026 条目 ai_policy（2026-09-04 核对，2026-09-20 复验）
  notes: >-
    apply 口径执行：AI 辅助（代码脚手架/资料检索/语言润色），核心创意、决策与文本由团队独立完成并保留人机分工记录（归档移交）；
    材料性能数字只出自本战役 metrics 实测，论文数字一律标"论文报告值"；创意组资格红线=通知发布前未注册工商。
---

# 蓝图：安航云盾演示系统与申报材料（国创赛 2026 创意组）

# 正文（人读）

## 选型依据摘要

见 strategy.md 六节（大显身手信号 4 张 90 天新卡直接映射三大补强项；该赛 patterns 未建已如实降权；推荐结论=材料冲刺+演示级原型立即执行）。三大补强项全带源（strategy/frontier-tech.md）：共形校准（SPACE+NeurIPS/ICML/ICLR 2025-26）、链路一致性检测（DroneMA，KB 同构硬件栈）、SDR 频谱感知站（USRP B210 现有设备）。与隔壁无人机电磁干扰平台战役（同属用户）互为攻防测试环境：一攻一防组成"低空链路安全"叙事，共用 B210（错峰）与 GNU Radio 栈。

## 里程碑展开（一人成军节奏，10-25 省复赛线倒排）

- m0（本周末前）：骨架+冒烟+数据字典+契约；确认 B210/Orin 借用排期（与隔壁战役错峰）。
- m1（第 1 周）：场景 1 竖切——此后所有迭代都在真实 SITL 数据流上，Web 仪表盘同步可见（答辩演示的骨架）。
- m2（第 2 周）：三场景全量+共形校准+一致性检测+回放页；30 次评估跑批，metrics 开始积累真实数字。
- m2b（第 2-3 周交叠）：Orin NX 时延实测+B210 标定（设备到位即插即测；不可用则回放模式降级，如实注记）。
- m3（第 3 周起，与 m2 尾部并行启动）：计划书 v2 数字回填、路演 PPT、演示视频；预留排位赛通知发布后的格式微调窗口。

## 风险与缓解

见 strategy.md 第五节五项（时间/一人成军/指标/设备/赛制合规），关键两条：材料窗口按"10 月中旬交"倒排不等通知；指标差距如实报告并区分设计目标与当前实测。
