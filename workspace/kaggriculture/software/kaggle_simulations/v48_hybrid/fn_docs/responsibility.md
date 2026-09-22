# 责任文档：v48 混合候选（方案甲）
> 由 fn-divide 产出与独占更新；fn-implement 只读。实现期结构性变化必须回本阶段改本文档。
> 上游：fn_docs/requirements.md（R1-R7）。批次：F1=三补丁叶（可并行）→ F2=基底审计+装配打包 → F3=离线四门。

## 结构概览
- build_hybrid_package ← R1,R2,R3,R4,R5
  - load_v48_base
  - apply_midgame_sell_layer
  - apply_economic_guard
  - apply_milestone_monitor
  - assemble_package
- verify_offline_gates ← R5,R6
  - run_h2h_gate
  - run_panel_gate
  - check_zero_new_anomalies
  - run_launch_fourgate
- verify_patch_safety ← R3,R4
  - test_guard_inactive_equivalence
  - test_trigger_coverage

## 需求覆盖矩阵
| 需求 | 顶层函数 |
|---|---|
| R1 | build_hybrid_package（load_v48_base 审计） |
| R2 | build_hybrid_package（apply_midgame_sell_layer）+ verify_offline_gates（h2h/panel） |
| R3 | build_hybrid_package（apply_economic_guard）+ verify_patch_safety |
| R4 | build_hybrid_package（apply_milestone_monitor）+ verify_patch_safety |
| R5 | build_hybrid_package（assemble_package）+ verify_offline_gates（launch_fourgate） |
| R6 | verify_offline_gates（全门+台账） |
| R7 | assemble_package（README 交接面） |

## 功能块 build_hybrid_package ← R1-R5
（块引言：基底五区零改动（磁带/路由/反克隆/槽位重排/终局清仓），补丁经窄缝注入；补丁失败回退 v48 原生（fail-safe）。）
- **load_v48_base** [L0|新增]：装载基底字节+sha 校验（dadee25a）+五区零改动审计接口（对最终混合件 diff 做分区归因）。签名意图：输入: 基底路径 / 输出: {main_source, sha256, zones} / 错误: sha 不符即抛。
- **apply_midgame_sell_layer** [L1|改造 v3]：三门卖出计划器语义（v3=近克隆帧仍透传 tape 全部卖单，但**允许补发清线加卖**——与 gold_floor 抢卖同向；镜像共振风险由 A/B 门裁决）：输入=回合观测（价格/库存/资金/剧本预期卖单）/输出=中期卖单/错误=异常→回退剧本默认卖单。
- **apply_economic_guard** [L1|新增]：双死价检测（阈值文档化）→否决买畜/建棚；未触发=零动作。
- **apply_milestone_monitor** [L1|新增]：点火里程碑偏离监测（d10-12 窗口）→偏离超阈只调卖单时点。
- **assemble_package** [L0|新增]：把三补丁注入基底 main.py（窄缝集成）+确定性打包+manifest（基底 sha/补丁清单/门结果占位）+README 交接文档（R7）。

## 功能块 verify_offline_gates ← R5,R6
- **run_h2h_gate** [L1|新增]：seated 通道对 {纯 v48, v72, 画像池≥2} ≥16 局，对 v48 互胜≥0.65；席位显式。
- **run_panel_gate** [L1|新增]：孪生 d0 反事实资金 ratio≥0.98（vs 纯 v48，同席位）。
- **check_zero_new_anomalies** [L1|新增]：全部对局 DONE、异常集对照纯 v48 基线零新增。
- **run_launch_fourgate** [L1|新增]：官方装载语义/双席自打 DONE/确定性双跑/体积与身份链。

## 功能块 verify_patch_safety ← R3,R4
- **test_guard_inactive_equivalence** [L1|新增]：P2/P3 未触发局与纯 v48 行为一致（构造正常局驱动对比）。
- **test_trigger_coverage** [L1|新增]：构造双死价局/里程碑偏离局必触发（P2 否决买畜建棚、P3 调卖单）。


---

## 【R8 增补·2026-09-25】功能块（演进模式追加，旧块不动）

## 结构概览（增补）
- build_lead_protection ← R8
  - estimate_lead_margin
  - plan_protective_sells
  - assemble_lead_protection_build
- verify_lead_protection ← R8
  - run_replay_gate
  - run_equivalence_face
  - run_launch_recheck

## 需求覆盖矩阵（增补行）
| 需求 | 顶层函数 |
|---|---|
| R8 | build_lead_protection；verify_lead_protection |

## 功能块 build_lead_protection ← R8
（块引言：终局保果补丁（P4 家族）——d24+ 且领先差 ≥3k 形态启用保守卖时锁胜；不触发形态与 v4b 逐字节一致；注入缝=卖单干预（P1 先例），基底五区零改动；fail-safe 任何异常回退 v4b 行为。产出为独立纯函数补丁模块 + 旗面构建，战后资产不上线。）

- **build_lead_protection** [L0|新增]
  - 职责：保果补丁的编排入口——逐回合：estimate_lead_margin 算领先 → 触发形态判定【R8-v2：day≥15 且峰回撤 peak−lead≥2000 且 lead≥1500；或 day≥24 且 lead≥3000（原条件保留为并集）；峰值经运行峰寄存器跟踪】→ plan_protective_sells 调整卖单 → 返回；未触发/异常→原卖单原样返回（同对象）。
  - 签名意图：输入: 回合观测（价格/库存/资金/当日卖单计划）+ day / 输出: 调整后卖单（未触发=原对象） / 错误: 内部异常吞掉并回退原单。
  - 调用方：装配后的混合 agent（v5 构建形态）。
  - tested 策略：自有单测。
  - 核验命令：测试: patches/test_lead_protection.py（继承 R8 验收②③的单测面）。
  - **estimate_lead_margin** [L1|新增]
    - 职责：领先差计算——优先 obs 可得的对手机金/资金字段；不可得时用可观测代理（我方资金+库存估值 vs 对手产出估计），代理口径文档化并在实现期登记。
    - 签名意图：输入: 回合观测 / 输出: {lead: float, basis: str} / 错误: 不可估→lead=None（视为未触发）。
    - 调用方：build_lead_protection。
    - tested 策略：自有单测。
    - 核验命令：测试: patches/test_lead_protection.py（estimate 用例组）。
  - **plan_protective_sells** [L1|新增]
    - 职责：保守卖时生成——把计划卖单前移/拆批以确保成交（对冲对手低价倾倒反超）；只动卖时与批量，不新增产线动作；与反克隆抢卖/终局清仓的仲裁=清仓窗内让位（717-718 逐字保留，调整只发生在其前）。
    - 签名意图：输入: 库存/价格投影/当前卖单/领先差 / 输出: 调整后卖单 / 错误: 异常→原单。
    - 调用方：build_lead_protection。
    - tested 策略：自有单测。
    - 核验命令：测试: patches/test_lead_protection.py（plan 用例组）。
  - **assemble_lead_protection_build** [L1|新增]
    - 职责：旗面构建 v5（P4 on，P1/P3 off，P2 on 沿 v4b）——包装 build.py 既有旗面机制新增 P4 旗（零接线字节级验证沿用）；产物落 v48_hybrid/v5/。
    - 签名意图：输入: 无（CLI） / 输出: v5 包+manifest / 错误: 构建不确定即失败。
    - 调用方：操作者（构建期）。
    - tested 策略：上游覆盖: verify_lead_protection。
    - 核验命令：上游覆盖: run_launch_recheck。

## 功能块 verify_lead_protection ← R8
- **verify_lead_protection** [L0|新增]
  - 职责：验收编排——重演门+等价面+发射复检三件汇总裁决 dict。
  - 签名意图：输入: v5 包路径+14 局语料清单 / 输出: {overall, replay_gate, equivalence, launch} / 错误: 任一门不可执行=整体 fail（fail-closed）。
  - 调用方：操作者。
  - tested 策略：自有单测。
  - 核验命令：测试: gates/test_lead_protection_gates.py（继承 R8 验收①②③）。
  - **run_replay_gate** [L1|新增]
    - 职责：14 局领先崩塌局孪生重演**双臂对照**（seated 通道；注入点=领先峰值日；每局两臂=P4 臂（v5）与对照臂（v4b）同点注入）；逐局 Δ=margin(P4)−margin(对照)（杠杆符号直测）；成功=重演终局 margin>0；≥7/14 PASS；Δ 分布随裁决 JSON 落盘。语料=14 局回放归档入 fn_docs/results/replays-lead-collapse/（体积预算沿最小集先例）。
    - 签名意图：输入: 归档语料+v5 callable / 输出: {wins, n, per_game} / 错误: 语料缺失 fail-closed。
    - 调用方：verify_lead_protection。
    - tested 策略：自有单测（tmp 语料）。
    - 核验命令：测试: gates/test_lead_protection_gates.py（replay 用例组）+真实跑 ≥7/14。
  - **run_equivalence_face** [L1|新增]
    - 职责：非触发局等价面——构造 ≥4 局+真实回放采样 ≥4 局，v5 与 v4b 动作流逐字节一致（未触发形态保果层零足迹）。
    - 签名意图：输入: 局集+两 callable / 输出: {n_identical, n} / 错误: 任一分叉即 fail。
    - 调用方：verify_lead_protection。
    - tested 策略：自有单测。
    - 核验命令：测试: gates/test_lead_protection_gates.py（等价用例组）。
  - **run_launch_recheck** [L1|新增]
    - 职责：v5 发射四门复检（装载语义/自打 DONE/确定性/体积身份）+patches 单测全绿确认。
    - 签名意图：输入: v5 包 / 输出: 四门结果 / 错误: 任一门红。
    - 调用方：verify_lead_protection。
    - tested 策略：上游覆盖。
    - 核验命令：上游覆盖: verify_lead_protection。


---

## 【R9 增补·2026-09-23】结构重构梯（G 批次）
## 结构概览（增补）
- generate_giant_schedule ← R9
  - validate_schedule_feasibility
- perform_tape_surgery ← R9
  - map_events_to_tape
  - rebuild_tape_routes
- assemble_v6_build ← R9
- verify_structure_gates ← R9
  - run_h2h_v48_gate
  - run_giant_seated_gate
  - run_win_regression_gate
  - run_economic_face

## 需求覆盖矩阵（增补行）
| 需求 | 顶层函数 |
|---|---|
| R9 | generate_giant_schedule；perform_tape_surgery；assemble_v6_build；verify_structure_gates |

## 功能块 generate_giant_schedule ← R9
（块引言：从 M0 经济模型+M4 巨人画像生成羊重仓目标产线排程——逐日买/建/雇/种计划+现金流预算；画像锚=statma 卡。）
- **generate_giant_schedule** [L0|新增]：排程生成（目标：羊~17/羊毛占比~0.52/SE@d11/收入峰 d14-17≥17k 级）；输入 M0 模型+画像 / 输出 逐日计划 JSON / 错误：不可行约束即报。
  - **validate_schedule_feasibility** [L1|新增]：孪生空跑可行性（劳动 op/现金/棚容/停时约束逐日校验）；不可行日逐条报。
## 功能块 perform_tape_surgery ← R9
- **perform_tape_surgery** [L0|新增]：把目标排程映射为 v48 磁带产线事件手术（解码路由的 BUY/BUILD/HIRE 事件改写；反应层/市场层/终局清仓不动）。
  - **derive_sell_schedule** [L1|新增]：按 M1 吸收节律最优（卖速≈吸收率+末日清仓）从新产线推导逐日卖序（羊毛/奶/麦/西瓜线各排程）。
  - **allocate_labor_plan** [L1|新增]：op 容量可行性分配（CARE/FEED/收割/种植 op 预算逐日；畜群规模受照护容量约束回传排程）。
  - **map_events_to_tape** [L1|修订]：排程+卖序+劳动 → 磁带全事件差分集（产线/卖/移动三面）。
  - **rebuild_tape_routes** [L1|新增]：重编码受影响路由段并保一致性（事件点/路由切换结构不变）。
## 功能块 assemble_v6_build ← R9
- **assemble_v6_build** [L0|新增]：v6 构建（手术磁带+P2 保险沿 v4b 旗面形态；四门冒烟；产物 v6/）。
## 功能块 verify_structure_gates ← R9
- **verify_structure_gates** [L0|新增]：五线编排裁决。
  - **run_h2h_v48_gate** [L1|新增]：v6 vs 纯 v48 ≥16 局互胜 ≥0.65。
  - **run_giant_seated_gate** [L1|新增]：对 statma/fuxi/42 回放流各 ≥3 局 seated 对照（打平或更好）。
  - **run_win_regression_gate** [L1|新增]：胜局回归 ≥8 局不翻负。
  - **run_economic_face** [L1|新增]：收入峰 ≥12.7k 级@d14-17（孪生计量）。
