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


---

## 【R10 增补·2026-09-23】种子迟购截断层（layer S，orderbook-L1）

## 结构概览（增补）
- build_layer_s_candidate ← R10
  - append_layer_s_block
  - _cxs_agent（运行时，注入包内）
    - _cxs_seed_truncate
      - _cxs_seed_surplus
        - _cxs_completable_plant_demand
          - _cxs_harvest_completable
- verify_layer_s_gates ← R10
  - gate_h2h_vs_verbatim
  - gate_lineage_strength
  - gate_equivalence_precision
    - replay_action_diff
    - precision_subset_check
    - constructed_invariant_cases
  - gate_launch_fourgate_l1

## 需求覆盖矩阵（增补行）
| 需求 | 顶层函数 |
|---|---|
| R10 | build_layer_s_candidate；verify_layer_s_gates |

## 功能块 build_layer_s_candidate ← R10
（块引言：layer S 是加在 round-30 orderbook 衍生版（main sha a16e0e9b / pkg sha 2838cc66）尾部的纯减法过滤层：step≥648 起对基座动作里的 BUY_SEED 订单做零误杀截断——删除充要条件=删除后"库存种子+保留订单+磁带未来购买"仍覆盖全部可完成种+收的 PLANT 机会（逐品项）；不确定即保留（宁买勿漏）。异常一律回退基座动作。产物全落 orderbook_l1_derivative/，orderbook_derivative/ 原件零改动。）

- **build_layer_s_candidate** [L0|新增]
  - 职责：构建编排——复制 orderbook_derivative/main.py 为 L1 副本 → append_layer_s_block 注入 layer S 尾块 → 确定性打包（round-30 配方：tarfile mtime0/uid0/gid0/mode644、gzip mtime0、双跑逐字节一致）→ 生成 manifest（基底 sha 链 a16e0e9b→2838cc66、layer S 块 sha、双跑哈希、描述文案 "public derivative with seed-truncation layer"）。
  - 签名意图：输入: 无（CLI） / 输出: orderbook_l1_derivative/{main.py, submission.tar.gz, build_manifest.json} / 错误: 注入校验或打包不确定即构建失败（fail-closed）。
  - 调用方：操作者（构建期）。
  - tested 策略：上游覆盖: verify_layer_s_gates。
  - 核验命令：上游覆盖: gate_launch_fourgate_l1。
  - **append_layer_s_block** [L1|新增]
    - 职责：生成 layer S 源码块（下述五运行时函数）文本追加到副本尾部；注入校验四条——py_compile 通过、AST 可解析、装载后 globals 最后 callable=_cxs_agent、对原版 diff 仅尾部追加（无既有行改动）。
    - 签名意图：输入: L1 main.py 路径 / 输出: 注入后源文件+diff 审计记录 / 错误: 任一校验红即失败。
    - 调用方：build_layer_s_candidate。
    - tested 策略：自有单测。
    - 核验命令：测试: orderbook_l1_derivative/test_build.py（注入校验组；继承 R10 验收④装载门）。
  - **_cxs_agent** [L1|新增]（运行时入口，注入包内）
    - 职责：尾块捕获最后 callable（=orderbook 版 _cxd_agent）→ 取基座动作 → step<648 或动作无 BUY_SEED → 原样返回（同对象，零足迹）；否则交 _cxs_seed_truncate 过滤后返回 dict(action, market=filtered)；任何异常→基座动作原样返回（fail-safe）；step==0 复位层内缓存（磁带解析缓存等）。
    - 签名意图：输入: observation, configuration / 输出: 基座格式 action / 错误: 一切内部异常吞掉并回退基座动作。
    - 调用方：Kaggle 官方装载（最后 callable）。
    - tested 策略：上游覆盖: verify_layer_s_gates。
    - 核验命令：上游覆盖: gate_launch_fourgate_l1。
    - **_cxs_seed_truncate** [L2|新增]
      - 职责：过滤主函数——对 action['market'] 中 step≥648 的 BUY_SEED 逐单裁决：逐品项调用 _cxs_seed_surplus 得允许删除量，只删超出部分（按订单出现序删后单），其余订单与槽位顺序原样保留；任何品项 surplus 计算返回不确定（None）→ 该品项零截断。
      - 签名意图：输入: observation, action / 输出: 过滤后 market 订单表（纯减法） / 错误: 异常向上抛（由 _cxs_agent 兜底回退）。
      - 调用方：_cxs_agent。
      - tested 策略：自有单测（三构造用例经 constructed_invariant_cases 复用）。
      - 核验命令：测试: orderbook_l1_derivative/test_layer_s.py（继承 R10 验收③(c)）。
      - **_cxs_seed_surplus** [L3|新增]
        - 职责：零误杀核心——surplus(crop)=max(0, 库存种子(crop)−当前步 PLANT 消耗(crop))+本回合保留 BUY_SEED(crop)+磁带未来 BUY_SEED(crop)−可完成种收需求(crop)（−当前步 PLANT 消耗（current_plants 未知→None）：引擎结算序 PLANT 先于买单入账，评审 2026-09-23 修正）；允许删除量=max(0, surplus) 且不超过本回合该品项购买量；需求经 _cxs_completable_plant_demand；磁带/库存任一读取失败→返回 None（不确定=不截）。种子↔格子换算按引擎 crop 常数（麦/萝卜 1 种/格）。
        - 签名意图：输入: crop, observation, 本回合保留订单集 / 输出: 允许删除量（int）或 None / 错误: 解析失败→None。
        - 调用方：_cxs_seed_truncate。
        - tested 策略：自有单测。
        - 核验命令：测试: orderbook_l1_derivative/test_layer_s.py（surplus 用例组）。
        - **_cxs_completable_plant_demand** [L4|新增]
          - 职责：逐品项统计未来 PLANT 种子需求——读选中磁带/计划未来 farmer PLANT 事件（经基座既有未来计划通道，同 RACE 扫描 tape 未来卖单的先例，只读不改），只计经 _cxs_harvest_completable 判定可完成的机会；输出需求量；通道解析失败→None。
          - 签名意图：输入: crop, observation / 输出: 需求种子数（int）或 None / 错误: 解析失败→None。
          - 调用方：_cxs_seed_surplus。
          - tested 策略：自有单测。
          - 核验命令：测试: orderbook_l1_derivative/test_layer_s.py（demand 用例组）。
          - **_cxs_harvest_completable** [L5|新增]
            - 职责：纯时间测试——step s 的 crop PLANT 可完成种+收 ⇔ s+first_harvest_steps(crop) ≤ 719（引擎天粒度，评审 2026-09-23 修正）；first_harvest_steps 取 vendored 引擎 crop 常数（麦/萝卜≈48 步）；常数缺失/异常→True（保守：不构成截断理由）。
            - 签名意图：输入: step, crop / 输出: bool / 错误: 无（异常→True）。
            - 调用方：_cxs_completable_plant_demand。
            - tested 策略：自有单测。
            - 核验命令：测试: orderbook_l1_derivative/test_layer_s.py（harvest 边界组：s671 用例）。

## 功能块 verify_layer_s_gates ← R10
- **verify_layer_s_gates** [L0|新增]
  - 职责：四门编排与台账——顺序执行 gate_h2h_vs_verbatim → gate_lineage_strength → gate_equivalence_precision → gate_launch_fourgate_l1，evidence 四件套落 orderbook_l1_derivative/（h2h/lineage/equivalence/launch JSON，格式沿 round-30）；任一门不可执行=整体 fail（fail-closed）；全绿输出 overall PASS（发射前置）。
  - 签名意图：输入: L1 包路径+26 局局集清单 / 输出: {overall, h2h, lineage, equivalence, launch} / 错误: fail-closed。
  - 调用方：操作者。
  - tested 策略：自有单测。
  - 核验命令：测试: orderbook_l1_derivative/test_gates.py（继承 R10 验收①②③④）。
  - **gate_h2h_vs_verbatim** [L1|新增]
    - 职责：门①——seated 通道双席位对 orderbook verbatim ≥16 局，互胜 ≥0.55；h2h_evidence.json 同格式台账（seed/seat/rewards/statuses/margin）。
    - 签名意图：输入: 两 callable+种子集 / 输出: {n, wins, rate, per_game} / 错误: 任一局非 DONE 即门红。
    - 调用方：verify_layer_s_gates。tested 策略：自有单测。核验命令：测试: orderbook_l1_derivative/test_gates.py（h2h 组；继承 R10 验收①）。
  - **gate_lineage_strength** [L1|新增]
    - 职责：门②——对 v48 纯件/v4b/hybrid-v2 各 ≥8 局（seated 双席位），无翻负（允许平）；对照 48-0 基线台账。
    - 签名意图：输入: L1 callable+三对手 callable / 输出: 三对手 {n, losses} / 错误: 任一负局即门红。
    - 调用方：verify_layer_s_gates。tested 策略：自有单测。核验命令：测试: orderbook_l1_derivative/test_gates.py（lineage 组；继承 R10 验收②）。
  - **gate_equivalence_precision** [L1|新增]
    - 职责：门③——三合一裁决：(a 反应面+结果面，2026-09-24 口径修订) 26 局线上局集 seated 重演：全部差异步 ≥648 且差异形态限于 {BUY_SEED 增/删、SELL 单集合变化}（基座对截断的自身经济反应），且逐局终局资金 l1 ≥ verbatim（replay_action_diff 全量差异枚举+逐形态分类裁决；原严格逐字节口径废止留档）；(b) 子集判据（precision_subset_check：逐局逐品项被截断量 ≤ 原版终局未种下量；模式甲类局截断额 ≈0）；(c) 构造用例三件（constructed_invariant_cases）。任一红即门红。
    - 签名意图：输入: 26 局回放集+L1/verbatim 两 callable / 输出: {equiv, subset, cases} / 错误: fail-closed。
    - 调用方：verify_layer_s_gates。tested 策略：自有单测。核验命令：测试: orderbook_l1_derivative/test_gates.py（equivalence 组；继承 R10 验收③）。
    - **replay_action_diff** [L2|新增]
      - 职责：逐局重演 diff——L1 与 verbatim 各驱动同一局，动作流逐字节对比；差异仅允许"BUY_SEED 订单消失"形态，出现任何其他差异（含下游 PLANT/HIRE 漂移）即报告首个异类差异位置。
      - 签名意图：输入: 单局回放+两 callable / 输出: {identical_mod_seed_drop, first_divergence} / 错误: 重演失败=该局 fail。
      - 调用方：gate_equivalence_precision。tested 策略：自有单测。核验命令：测试: orderbook_l1_derivative/test_gates.py（diff 组）。
    - **precision_subset_check** [L2|新增]
      - 职责：零误杀的可观察裁决——逐局逐品项统计"被截断购种量 vs 原版该局终局未种下量"，截断量 ≤ 未种下量（子集性质）；输出逐局明细与汇总（模式甲类局截断额应 ≈0；有效采购 $1,350 级保留）。
      - 签名意图：输入: 26 局重演产物+原版终局库存 / 输出: {per_game, per_crop, violations} / 错误: 任一 violation 即门红。
      - 调用方：gate_equivalence_precision。tested 策略：自有单测。核验命令：测试: orderbook_l1_derivative/test_gates.py（subset 组）。
    - **constructed_invariant_cases** [L2|新增]
      - 职责：构造三用例直测不变量——未来仍有 PLANT 机会的 BUY_SEED 不截；确无机会的截；s671 边界单仅当磁带确无后续种植机会才截。
      - 签名意图：输入: 构造 obs/action 夹具 / 输出: 三例 pass/fail / 错误: 夹具异常=失败。
      - 调用方：gate_equivalence_precision（并供 test_layer_s 复用）。tested 策略：自有单测。核验命令：测试: orderbook_l1_derivative/test_layer_s.py（invariant 组；继承 R10 验收③(c)）。
  - **gate_launch_fourgate_l1** [L1|新增]
    - 职责：门④——发射四门：官方 last-callable 装载（末 callable=_cxs_agent；与 _cxd_agent 基线的完整序列差异仅来自截断层）；双席自打 DONE+max 单步 <1s；确定性双跑动作流 sha256 一致；体积 <100MB 与 sha 身份链登记（manifest 同 round-30 格式）。
    - 签名意图：输入: L1 包 / 输出: 四门结果 / 错误: 任一门红。
    - 调用方：verify_layer_s_gates。tested 策略：自有单测。核验命令：测试: orderbook_l1_derivative/test_gates.py（launch 组；继承 R10 验收④）。


---

## 【R11 增补·2026-09-24】供给核算修正·净需求覆盖（L1.1）

## 结构概览（增补）
- build_l11_candidate ← R11
  - make_layer_s_v2_block
    - _cxs_seed_surplus [改造·v2]
- verify_l11_gates ← R11
  - gate_h2h_vs_l1
  - gate_equivalence_v2
    - constructed_cases_v2
  - （复用不改）：gate_lineage_strength / gate_launch_fourgate_l1 / replay_action_diff / precision_subset_check——由编排重定向参数复用 L1 实现

## 需求覆盖矩阵（增补行）
| 需求 | 顶层函数 |
|---|---|
| R11 | build_l11_candidate；verify_l11_gates |

## 功能块 build_l11_candidate ← R11
（块引言：R11 只改造一个运行时函数——_cxs_seed_surplus 供给口径改净需求覆盖式；其余四个运行时函数与常数沿 R10 逐字节继承（v2 块=L1 块源+该函数替换，AST 校验差异恰为一函数体）。产物落 orderbook_l1_1_derivative/；L1 目录零改动；打包配方与 manifest 链沿 round-30/L1 先例。）

- **build_l11_candidate** [L0|新增]
  - 职责：编排——make_layer_s_v2_block 生成 v2 块 → 复制基座原件注入（L1 append 四校验管线复用）→ 确定性打包（双跑逐字节）→ manifest（基座 a16e0e9b/2838cc66 链+L1 块 sha+v2 块 sha+双跑声明；schema orderbook_l1_1_derivative_manifest/1.0）。
  - 签名意图：输入: 无（CLI） / 输出: orderbook_l1_1_derivative/{main.py, submission.tar.gz, build_manifest.json} / 错误: 任一步不确定即抛。
  - 调用方：操作者。tested 策略：上游覆盖: verify_l11_gates。核验命令：上游覆盖: verify_l11_gates。
  - **make_layer_s_v2_block** [L1|新增]
    - 职责：从 L1 的 layer_s_block.py 源生成 v2 块——定位 `_cxs_seed_surplus` 函数体替换为净需求覆盖实现，其余文本逐字节不变；校验：AST 可解析、与 L1 块的 diff 恰为一处函数体、v2 末 callable 仍 _cxs_agent。
    - 签名意图：输入: L1 块路径 / 输出: v2 块文件+diff 审计 / 错误: 定位失败或 diff 超界即抛。
    - 调用方：build_l11_candidate。tested：自有单测。核验：测试: orderbook_l1_1_derivative/test_build_v2.py。
    - **_cxs_seed_surplus** [L2|改造·v2]
      - 职责：[2026-09-24 修订一轮]删除台账式累计口径——供给=库存−当前步 PLANT 消耗（钳 0）+本回合保留单+磁带未来购买（按实存计，台账扣已删）；删除充要条件=删后剩余累计供给 ≥ 剩余累计可完成需求（品项级）；磁带单/回买单统一授权；整单删除；不确定→None（零误杀不变）；实现前置法证=mode-B 真局 s662-663 五数实测（held/kept/tape_future/demand/allowed）。
      - 签名意图：输入: crop, observation, kept_orders, plan_view, current_plants / 输出: 允许删除量或 None / 错误: 不确定→None。
      - 调用方：_cxs_seed_truncate（v2 块内，沿 R10 调用形）。tested：自有单测。核验：测试: orderbook_l1_1_derivative/test_layer_s_v2.py（净口径矩阵+两件新构造用例）。

## 功能块 verify_l11_gates ← R11
- **verify_l11_gates** [L0|新增]
  - 职责：四门编排（沿 L1 verify 形制，evidence 落 v2 目录 evidence/）：①gate_h2h_vs_l1；②gate_lineage_strength（**复用 L1 模块重定向**：run(v2_main, 三对手, 8)）；③gate_equivalence_v2；④gate_launch_fourgate_l1（**复用重定向**：run(v2_pkg)）。任一门不可执行=整体 fail；全绿=发射前置。
  - 签名意图：输入: v2 包路径 / 输出: {overall, h2h, lineage, equivalence, launch} / 错误: fail-closed。
  - 调用方：操作者。tested：自有单测。核验：测试: orderbook_l1_1_derivative/test_verify_v2.py。
  - **gate_h2h_vs_l1** [L1|新增]
    - 职责：seated 双席位 ≥16 局 vs **L1（在飞件同字节）**互胜 ≥0.55（直量增量）；另附 vs verbatim 8 局参考面（记账不设阈）；装载身份断言沿 L1（v2 末 callable=_cxs_agent）；per_game 沿 h2h 台账格式。
    - 签名意图：输入: v2_main, l1_main, verbatim_main, seeds / 输出: {n, wins, rate, passed, ref_face} / 错误: fail-closed。
    - 调用方：verify_l11_gates。tested：自有单测。核验：测试: orderbook_l1_1_derivative/test_gate_h2h_v2.py。
  - **gate_equivalence_v2** [L1|新增]
    - 职责：26 局重演三面——(a) v2 vs verbatim 差异（沿 R10 修订口径：步界/形态有界）+ **buy_seed_appear ≤2**；(b) 结果面：逐局 v2 终局资金 ≥ L1 终局资金 + **终局死种合计 ≤$900**；净截断（dropped 含拦下回买）子集判据重验（复用 precision_subset_check 口径）；(c) constructed_cases_v2 五件（R10 三件+新增两件：净口径下回买单被拦/真需求回买单保留）。
    - 签名意图：输入: episodes_dir, v2_main, l1_main, verbatim_main / 输出: {forms, appear_count, result_face, dead_seeds_total, subset, cases, passed} / 错误: fail-closed。
    - 调用方：verify_l11_gates。tested：自有单测。核验：测试: orderbook_l1_1_derivative/test_gate_equiv_v2.py。
    - **constructed_cases_v2** [L2|新增]
      - 职责：R10 三件沿 import 复用 + 新增两件净口径用例（窗口内非磁带回买单且净供给已覆盖→删；净供给<需求（真未来种植）→保留）。
      - 签名意图：输入: 无（夹具内置） / 输出: 五例 pass/fail / 错误: 夹具异常=失败。
      - 调用方：gate_equivalence_v2。tested：自有单测。核验：测试: orderbook_l1_1_derivative/test_layer_s_v2.py（invariant v2 组）。


---

## 【R12 增补·2026-09-24】减量改单·种子回收极限（L2）

## 结构概览（增补）
- build_l2_candidate ← R12
  - make_layer_s_v3_block
    - _cxs_agent [改造·v3]
      - _cxs_reduce_orders [改造·v3]
        - _cxs_seed_balance [改造·v3]
          - _cxs_observed_plant_rate [新增]
          - _cxs_completable_plant_demand [沿 R10]
            - _cxs_harvest_completable [沿 R10]
- verify_l2_gates ← R12
  - gate_equivalence_v3
    - constructed_cases_v3
  - （复用不改）：gate_h2h_vs_l1（基线仍 L1）/ gate_lineage_strength / gate_launch_fourgate_l1 / replay_action_diff / precision_subset_check

## 需求覆盖矩阵（增补行）
| 需求 | 顶层函数 |
|---|---|
| R12 | build_l2_candidate；verify_l2_gates |

## 功能块 build_l2_candidate ← R12
（块引言：v3 块=L1 块+受控多处改造：_cxs_seed_surplus/_cxs_seed_truncate 重写为 balance/reduce、新增 _cxs_observed_plant_rate、_cxs_agent 复位钩子挂台账、[] 空槽解析归类、窗口常数参数化（648/600 双产物）。diff 纪律从"恰一函数体"泛化为"受控变更集"（AST 级：允许的函数替换/新增/常数改动白名单，白名单外任何差异即构建失败）。打包/manifest 沿先例，窗口参数入 manifest。）

- **build_l2_candidate** [L0|新增]
  - 职责：编排 make_layer_s_v3_block（两窗各一）→ 注入基座副本（四校验+三防线沿 L1 管线）→ 确定性打包（双跑）→ manifest×2（schema orderbook_l2_derivative_manifest/1.0；含 window 参数与变更集审计）。CLI：`--window 648|600|both`。
  - 签名意图：输入: 无（CLI，window 参数） / 输出: orderbook_l2_derivative/w{648,600}/{main.py, submission.tar.gz, build_manifest.json} / 错误: 任一步不确定即抛。
  - 调用方：操作者。tested：上游覆盖: verify_l2_gates。核验：上游覆盖。
  - **make_layer_s_v3_block** [L1|新增]
    - 职责：从 L1 块源生成 v3 块——受控变更集=白名单 AST 操作：重写 _cxs_seed_surplus→_cxs_seed_balance、_cxs_seed_truncate→_cxs_reduce_orders（减量语义：BUY_SEED 订单可减量至目标保有 R，只减不加，从后往前逐单减）、新增 _cxs_observed_plant_rate、_cxs_agent 复位钩子挂台账复位+窗口常数引用、解析守卫 [] 空槽归类可忽略、_CXS_FROM 参数化注入；校验：AST 可解析、变更恰落白名单、末 callable 仍 _cxs_agent。
    - 签名意图：输入: L1 块路径+window / 输出: v3 块文件+变更集审计 / 错误: 白名单外差异即抛。
    - 调用方：build_l2_candidate。tested：自有单测。核验：测试: orderbook_l2_derivative/test_build_v3.py。
    - **_cxs_agent** [改造·v3]（运行时入口）
      - 职责：沿 R10 职责面；差异=过滤调用改 _cxs_reduce_orders；step==0 复位钩子挂台账；窗口界读常数（构建期定 648/600）。
      - 签名意图：输入: observation, configuration / 输出: action / 错误: 一切异常回退基座动作。
      - 调用方：官方装载。tested：上游覆盖。核验：上游覆盖: verify_l2_gates。
      - **_cxs_reduce_orders** [改造·v3]
        - 职责：纯减法过滤升级为减量过滤——对窗口内 BUY_SEED 逐品项计算目标保有 R（_cxs_seed_balance），从后往前把该品项购买量减至 R（逐单减量、可减至 0=整单消失；订单位置与其他订单不动；R≥现有量→全保留原样[同对象零足迹]）；品项不确定→该品项原样。
        - 签名意图：输入: observation, action, plan_view / 输出: 过滤后 market 表 / 错误: 异常上抛（_cxs_agent 兜底）。
        - 调用方：_cxs_agent。tested：自有单测。核验：测试: orderbook_l2_derivative/test_layer_s_v3.py。
        - **_cxs_seed_balance** [改造·v3]
          - 职责：减量目标 R=max(0, 需求赤字)+反应层安全边；需求赤字=剩余累计可完成需求−（held−当前步消耗+本回合保留+磁带未来按实存[台账扣已减]）；安全边=观测实种速率（_cxs_observed_plant_rate）×外推窗；台账跨步累计防重复计入；任何不确定→None（该品项原样，宁多买）。
          - 签名意图：输入: crop, observation, kept_orders, plan_view, current_plants / 输出: 目标保有 R 或 None / 错误: 不确定→None。
          - 调用方：_cxs_reduce_orders。tested：自有单测。核验：测试: orderbook_l2_derivative/test_layer_s_v3.py。
          - **_cxs_observed_plant_rate** [L4|新增]
            - 职责：从 observation 的我方 farms 地块 planted_day 统计该品项近 N 步（定桩实现期，5-10）实际种植速率（法证：反应层种植磁带视不可见，670 实种 2 vs 视 1——观测边数据源）；解析失败→None（上游按不确定处理）。
            - 签名意图：输入: observation, crop, lookback / 输出: 速率或 None / 错误: 异常→None。
            - 调用方：_cxs_seed_balance。tested：自有单测。核验：测试: orderbook_l2_derivative/test_layer_s_v3.py。

## 功能块 verify_l2_gates ← R12
- **verify_l2_gates** [L0|新增]
  - 职责：**两窗各跑全套四门**（w648/w600 分别：①复用 gate_h2h_vs_l1（cand=该窗 v3，对手仍 L1）②复用 gate_lineage_strength ③gate_equivalence_v3 ④复用 gate_launch_fourgate_l1），取全绿最宽窗为 recommended；fail-closed 全跑不短路；evidence 落各窗 evidence/ + 顶层 verify_summary（两窗对比+推荐窗）。
  - 签名意图：输入: 包根目录 / 输出: {windows:{w648:{overall…}, w600:{…}}, recommended} / 错误: fail-closed。
  - 调用方：操作者。tested：自有单测。核验：测试: orderbook_l2_derivative/test_verify_v3.py。
  - **gate_equivalence_v3** [L1|新增]
    - 职责：26 局重演四面——(a) 形态面（复用 replay_action_diff，减量自然分解为 BUY_SEED 增/删对均在允许集；步界=该窗参数）；(b) 结果面：逐局终局资金 ≥ L1 + 死种合计 ≤$500 + **饿死零容忍**（重演终态产量/在田株数逐局对比 L1——减产迹象即红）+ 子集重验（净回收 ≤ 原局未种下）；(c) constructed_cases_v3 九件。
    - 签名意图：输入: episodes_dir, v3_main, l1_main, verbatim_main, window / 输出: {forms, result_face{finals_ok, dead_seeds_total, starve_free, subset}, cases, passed} / 错误: fail-closed。
    - 调用方：verify_l2_gates。tested：自有单测。核验：测试: orderbook_l2_derivative/test_gate_equiv_v3.py。
    - **constructed_cases_v3** [L2|新增]
      - 职责：九件构造用例——R10 三件（减量语义重校）+c4/c5（重校）+新四件：8→1 减量恰留真需求+安全边；反应层超种安全边兜住；[] 空槽单可忽略不误 None；600 窗滴灌局回收。
      - 签名意图：输入: 无（夹具内置） / 输出: 九例 pass/fail / 错误: 夹具异常=失败。
      - 调用方：gate_equivalence_v3。tested：自有单测。核验：测试: orderbook_l2_derivative/test_layer_s_v3.py（invariant v3 组）。


---

## 【R13 增补·2026-09-24】CARROT2 源头钳制（L3）

## 结构概览（增补）
- build_l13_candidate ← R13
  - inject_controller_clamp
    - _ca_future_plant_demand [新增·注入]
  - （复用 L1 append：layer S 尾块逐字节继承）
- verify_l13_gates ← R13
  - gate_launch_l3
  - gate_equivalence_l3
    - constructed_cases_l3
  - （复用不改）：gate_h2h_vs_l1 / gate_lineage_strength / replay_action_diff / precision_subset_check

## 需求覆盖矩阵（增补行）
| 需求 | 顶层函数 |
|---|---|
| R13 | build_l13_candidate；verify_l13_gates |

## 功能块 build_l13_candidate ← R13
（块引言：双注入构建=中部受控手术（CARROT2 §3b 行 4695 目标项）+ 尾部 layer S 追加（L1 逐字节继承）。**Divide 级精化（登记 batches 变更记录）**：钳制激活窗 step≥648（day≥27）——实测浪费带全在 652-671、day26 无观测浪费，且与门③形态步界 ≥648 对齐；day<27 目标保持原 8。R13-b 粗粒度变体=同管线 mode="coarse"（day≥27 目标 2，一常数）。diff 审计=受控变更集两层：中部恰{一 helper def 插入+一表达式替换+激活条件}、尾部恰 layer S 块追加。）

- **build_l13_candidate** [L0|新增]
  - 职责：编排——复制基座 → inject_controller_clamp（mode=fine|coarse）→ 追加 layer S 尾块（复用 L1 append 四校验）→ 确定性打包（双跑）→ manifest（schema orderbook_l3_derivative_manifest/1.0；provenance=基座链→钳制变更集→layer S 块 sha→双跑；mode 登记）。
  - 签名意图：输入: mode（CLI） / 输出: orderbook_l3_derivative/{main.py, submission.tar.gz, build_manifest.json} / 错误: 任一步不确定即抛。
  - 调用方：操作者。tested：上游覆盖。核验：上游覆盖: verify_l13_gates。
  - **inject_controller_clamp** [L1|新增]
    - 职责：中部受控注入——AST 定位 CARROT2 §3b 的 q 计算行（4695 目标项），fine 模式替换为 `q = (min(_CA_BUFFER, _ca_future_plant_demand(<上下文>)+2) if step>=648 else _CA_BUFFER) - have - buying` 语义（异常回退原式：包 try 或需求 None→原值）；coarse 模式替换目标项为 `(2 if step>=648 else _CA_BUFFER)`；在 CARROT2 层函数前插入 helper def；校验：AST 可解析、变更集恰{一 def 插入+一表达式替换}、五区零改动断言（磁带/路由/反克隆/清仓/重排区文本恒等）。
    - 签名意图：输入: 基座 main 副本路径+mode / 输出: 注入后源+变更集审计 / 错误: 定位失败/变更超界即抛。
    - 调用方：build_l13_candidate。tested：自有单测。核验：测试: orderbook_l3_derivative/test_build_l4.py。
    - **_ca_future_plant_demand** [L2|新增·注入]（helper，随钳制注入基座）
      - 职责：route2 磁带后缀（≥当前 step）PLANT,CARROT 计数 + day≤28 可 swap 小麦槽保守计数（复用基座 _ca_tape/_ca_visits 机制与命名空间；读不到/异常→返回 None→钳制回退原目标）。
      - 签名意图：输入: 基座 CARROT2 层上下文（seat/step/st） / 输出: 需求 int 或 None / 错误: 异常→None。
      - 调用方：钳制表达式。tested：自有单测。核验：测试: orderbook_l3_derivative/test_layer_l4.py。

## 功能块 verify_l13_gates ← R13
- **verify_l13_gates** [L0|新增]
  - 职责：四门编排（fail-closed 全跑）：①复用 gate_h2h_vs_l1（cand=L3，**预期真胜局**）②复用 gate_lineage_strength ③gate_equivalence_l3 ④gate_launch_l3；evidence 落 L3 目录+verify_summary。
  - 签名意图：输入: L3 包路径 / 输出: {overall, h2h, lineage, equivalence, launch} / 错误: fail-closed。
  - 调用方：操作者。tested：自有单测。核验：测试: orderbook_l3_derivative/test_verify_l4.py。
  - **gate_launch_l3** [L1|新增]
    - 职责：发射四门（复用 v48_derivative_launch_check 重定向）+ **形态检查扩展**：truncation_only_diff 接受 {BUY_SEED 整单消失、BUY_SEED 减量对（同品项 disappear≥appear）、SELL 变化} 且差异步 ≥648（修 R12 留档的门禁形态缺口）。
    - 签名意图：输入: L3 包 / 输出: 四门+扩展形态裁决 / 错误: 任一门红。
    - 调用方：verify_l13_gates。tested：自有单测。核验：测试: orderbook_l3_derivative/test_verify_l4.py。
  - **gate_equivalence_l3** [L1|新增]
    - 职责：26 局重演四面（沿 v3 骨架，窗口界 648）：形态（扩展集含减量对）；结果面=逐局 ≥L1+死种 ≤$900+饿死零容忍+子集重验；构造用例。
    - 签名意图：输入: episodes_dir, l3_main, l1_main, verbatim_main / 输出: {forms, result_face, cases, passed} / 错误: fail-closed。
    - 调用方：verify_l13_gates。tested：自有单测。核验：测试: orderbook_l3_derivative/test_gate_equiv_l4.py。
    - **constructed_cases_l3** [L2|新增]
      - 职责：R10 三件 + 新四件（钳制触发局需求+2 恰好/day28 swap 不饿死/钳计算异常回退原 q/mode-A 休眠局零足迹）。
      - 签名意图：输入: 无 / 输出: 七例 pass/fail / 错误: 夹具异常=失败。
      - 调用方：gate_equivalence_l3。tested：自有单测。核验：测试: orderbook_l3_derivative/test_layer_l4.py。


---

## 【R14 增补·2026-09-24】surge 日卖时判决实验（全量版）

## 结构概览（增补）
- run_judgment ← R14
  - phase_a_attribution
    - daily_netflow_decompose
    - mark_surge_days
    - classify_surge_composition
  - phase_b_four_arm_replay
    - build_treatment_arm
      - apply_surge_day_sells
    - replay_dual_seat
    - compare_action_stream
  - judge_verdicts
- corpus_select（共享，Phase A/B 共用）

## 需求覆盖矩阵（增补行）
| 需求 | 顶层函数 |
|---|---|
| R14 | run_judgment |

## 功能块 run_judgment ← R14
（块引言：两阶段判决实验编排——Phase A 全量 86 局回放归因（surge 日全景测绘+构成分解+不可处置分层标注）→ Phase B 四臂双席位 seated 重演（对照=L3 在飞件同字节；A1 卖空率对齐/A2 高价优先/A3 组合；对手席=回放录像动作开环重放，两臂共用同一对手脚本——判决实验口径，对手反应性损失记入解读注记）→ 逐臂独立判据（可处置显著局 ≥2/3 Δ>0+全语料无害带 Δ≥−100）+敏感度报告 → evidence JSON（orderbook_surge_lab/evidence/judgment.json）。fail-closed：任一环节不可执行=整体 fail。产物全落 orderbook_surge_lab/，零改动既有目录与在飞件，不上线。）

- **run_judgment** [L0|新增]
  - 职责：编排裁决——corpus_select 定语料 → phase_a_attribution 全量归因（若全语料零可处置 surge 日→verdict=KILLED_A 短路出 evidence）→ phase_b_four_arm_replay 四臂×双席位重演 → judge_verdicts 逐臂判据+敏感度 → 汇总 evidence JSON（source 可复跑命令/逐局逐臂双席 margin 与 Δ/surge 标注/归因表/逐臂 verdict）；两阶段产物均落盘供单独复跑。
  - 签名意图：输入: 无（CLI，参数=语料目录/阈值档） / 输出: evidence JSON+控制台摘要 / 错误: 任一环节 fail-closed 即整体 fail。
  - 调用方：操作者。
  - tested 策略：上游覆盖: phase_a_attribution/phase_b_four_arm_replay/judge_verdicts。
  - 核验命令：测试: orderbook_surge_lab/test_run_judgment.py（编排+短路+evidence schema 组）。
  - **phase_a_attribution** [L1|新增]
    - 职责：全量回放逐日归因——对语料局集逐局调 daily_netflow_decompose 得双席逐日净收入/量/价/品类表 → mark_surge_days 标注（默认 1500/1.5×，附 1000/1500/2000 三档敏感度）→ classify_surge_composition 分解每个 surge 日差距构成（量差/mix 差/价差/结构性库存差+同品类覆盖能力+不可处置标注+价格可识别性[当日品项价 vs 滚动分位]）；输出 Phase A 报告 JSON（全景分布+8 局深描集标注）。
    - 签名意图：输入: 回放目录+语料清单 / 输出: {per_game:{per_day,surge_days,composition}, panorama, sensitivity} / 错误: 单局解析失败=该局 fail 记录不中断全量。
    - 调用方：run_judgment。
    - tested 策略：自有单测。
    - 核验命令：测试: orderbook_surge_lab/test_phase_a.py。
    - **daily_netflow_decompose** [L2|新增]
      - 职责：单局逐日双席分解——每日（day d 末=step d*24+23 口径）双席 money 净收入（money_delta+seed+BUY_PRODUCT 支出）、卖出量（按品项，成交量口径=库存背书部分）、隐含均价、可卖库存（shed+当日可收）；JSON 字符串字段 json.loads、提交量≠成交量修正沿 volume_price_decomp 方法注记。
      - 签名意图：输入: 单局回放 dict / 输出: {days:[{d,my:{net,vol_by_item,avgpx,sellable},opp:{...}}]} / 错误: 解析异常→该局 fail。
      - 调用方：phase_a_attribution。
      - tested 策略：自有单测（构造小回放夹具）。
      - 核验命令：测试: orderbook_surge_lab/test_phase_a.py（decompose 组）。
    - **mark_surge_days** [L2|新增]
      - 职责：surge 日标注——净日差=对手日净收入−我方日净收入 ≥阈值 且对手当日收入≥其全程日收入中位数 ×中位倍数（默认 1500/1.5×，参数化）；输出逐局 surge 日列表+三档阈值（1000/1500/2000）对照。
      - 签名意图：输入: 单局逐日分解+阈值参数 / 输出: {surge_days:[d], sensitivity:{th1000:[...],th1500:[...],th2000:[...]}} / 错误: 无（缺数据日跳过）。
      - 调用方：phase_a_attribution。
      - tested 策略：自有单测（边界日构造）。
      - 核验命令：测试: orderbook_surge_lab/test_phase_a.py（mark 组）。
    - **classify_surge_composition** [L2|新增]
      - 职责：单 surge 日构成分解——对手当日多赚部分拆为量差（同品类量差×我方均价）/品类 mix 差（对手品类结构高价值差）/价差（同品类价差×量）/结构性库存差（对手多卖品类在我方当日可卖库存中覆盖不了的部分）；覆盖能力=我方可卖同品类量/对手品类量；不可处置标注=结构性占比 ≥70% 或覆盖 <30%；价格可识别性=surge 日各品项价在该品项全程价的分位。
      - 签名意图：输入: 该日双席分解 / 输出: {quant_gap, mix_gap, px_gap, structural_gap, coverage, treatable:bool, price_percentile} / 错误: 分解失败→记 None 不中断。
      - 调用方：phase_a_attribution。
      - tested 策略：自有单测（构造四形态各一）。
      - 核验命令：测试: orderbook_surge_lab/test_phase_a.py（composition 组）。
  - **phase_b_four_arm_replay** [L1|新增]
    - 职责：四臂×双席位重演编排——corpus_select 的 Phase B 语料（可处置败局全集+8 胜局）逐局：双席位各跑对照臂（L3 在飞件同字节）与 A1/A2/A3 处置臂（build_treatment_arm）；对手席=该局回放录像动作开环重放（R8 先例）；compare_action_stream 校验非 surge 日零足迹；replay_dual_seat 执行单局单臂单席位重演（fail 重跑一次）；输出逐局逐臂双席 margin 与动作流摘要。
    - 签名意图：输入: Phase A 报告+语料+L3 main 路径 / 输出: {per_game:{per_arm:{seat0:{margin},seat1:{margin},delta}}} / 错误: 单臂单席 fail 两次=该局该臂红、整体 fail-closed。
    - 调用方：run_judgment。
    - tested 策略：自有单测。
    - 核验命令：测试: orderbook_surge_lab/test_phase_b.py。
    - **build_treatment_arm** [L2|新增]
      - 职责：构造处置 callable——包装 L3 agent：读该局 oracle surge 日集合与对应处置参数（A1=对手当日卖空率/A2=价格×库存价值序/A3=组合）；surge 日回合交 apply_surge_day_sells 改卖单，非 surge 日原样透传（同对象）；任何异常→原 action 返回（fail-safe）；step==0 复位。
      - 签名意图：输入: L3 callable+surge 配置+arm 类型 / 输出: 包装 callable / 错误: 包装层异常吞掉回退原 action。
      - 调用方：phase_b_four_arm_replay。
      - tested 策略：自有单测。
      - 核验命令：测试: orderbook_surge_lab/test_phase_b.py（arm 组）。
      - **apply_surge_day_sells** [L3|新增]
        - 职责：surge 日卖单改造（单一功能转变）——输入基座 action 与当日处置参数：A1 卖空率对齐=把该日卖出总量提至"我方可卖库存×对手当日卖空率"（品类按我方自然卖序放量）；A2 高价优先=按当日品项价×可卖量排序重排卖单顺序与品类优先；A3=两者叠加；硬约束=只卖有的（逐品项不超过可卖量）、其余动作与槽位原样保留。
        - 签名意图：输入: action, observation, 处置参数 / 输出: 改造后 action / 错误: 异常上抛（build_treatment_arm 兜底）。
        - 调用方：build_treatment_arm。
        - tested 策略：自有单测（三臂各一+库存上限+空卖单）。
        - 核验命令：测试: orderbook_surge_lab/test_phase_b.py（sells 组）。
    - **replay_dual_seat** [L2|新增]
      - 职责：单局单臂单席位 seated 重演——twin 引擎装载我方 callable 于指定席、对手席按录像动作重放，跑全程（720 步）取终局 margin；非 DONE/超时=异常；驱动实现取材 v48_hybrid/gates 重演管线与 L3 等价面管线（只读取材不改其源）。
      - 签名意图：输入: 回放, our_callable, seat / 输出: {margin, status, steps_n} / 错误: 异常→raise 由编排层重跑一次。
      - 调用方：phase_b_four_arm_replay。
      - tested 策略：自有单测（构造小局）。
      - 核验命令：测试: orderbook_surge_lab/test_phase_b.py（replay 组）。
    - **compare_action_stream** [L2|新增]
      - 职责：零足迹校验——同局同席位对照臂与处置臂的逐回合动作流对比：非 surge 日必须逐字节一致；surge 日差异必须限于卖单集合（SELL 增/删/序变），出现其他形态即报首个异类位置。
      - 签名意图：输入: 两动作流+surge 日集合 / 输出: {identical_off_surge, first_alien_diff} / 错误: 无（结果即裁决）。
      - 调用方：phase_b_four_arm_replay。
      - tested 策略：自有单测。
      - 核验命令：测试: orderbook_surge_lab/test_phase_b.py（zerofootprint 组）。
  - **judge_verdicts** [L1|新增]
    - 职责：逐臂独立判据——每臂：可处置显著局中 Δmargin>0 的局数 ≥2/3 且全语料（含胜局）Δ≥−100 → 该臂 POSITIVE；附敏感度（Δ>0 vs Δ>50；2/3 vs 3/4）与逐臂对比表；整体 verdict=任一臂 POSITIVE→POSITIVE（记胜出臂）/全 NEGATIVE→NEGATIVE/KILLED_A 由 run_judgment 短路给定。
    - 签名意图：输入: Phase B 结果+Phase A 分层标注 / 输出: {per_arm:{positive, n_sig, n_pos, harm_violations}, overall, winning_arm, sensitivity} / 错误: 语料缺失局=fail。
    - 调用方：run_judgment。
    - tested 策略：自有单测（构造正/负/边界判例）。
    - 核验命令：测试: orderbook_surge_lab/test_judge.py。

## 共享函数（增补）
- **corpus_select**（调用方：run_judgment, phase_a_attribution, phase_b_four_arm_replay）
  - 职责：语料选择——Phase A=全量回放目录；Phase B=Phase A 检出"含可处置 surge 日"败局全集+8 抽样胜局（r32/r33 各 4，rng.Random(20260924r14)）；输出逐局清单（episode/tag/seat 归属/胜负标签）；缺回放的局=fail-closed 列出。
  - 签名意图：输入: 回放目录+Phase A 报告（Phase B 时） / 输出: {phase_a:[...], phase_b:{losses:[...], wins:[...]}} / 错误: 语料缺失=fail。
  - 调用方：见上。
  - tested 策略：自有单测（抽样种子可复现）。
  - 核验命令：测试: orderbook_surge_lab/test_corpus.py。


---

## 【R15 增补·2026-09-24】反周期产线 mix 判决实验（参数扫描+双层）

## 结构概览（增补）
- run_mix_judgment ← R15
  - phase_m_market_map
    - item_price_percentile
    - rank_swap_pairs
  - generate_mix_variants
    - build_variant_schedule
    - check_variant_feasibility
    - build_variant_main
  - openloop_replay_variants
  - closedloop_probe
  - judge_mix_verdicts
- select_corpus_r15（共享，编排/重演共用）

## 需求覆盖矩阵（增补行）
| 需求 | 顶层函数 |
|---|---|
| R15 | run_mix_judgment |

## 功能块 run_mix_judgment ← R15
（块引言：反周期 mix 判决实验编排——Phase M 市场地图法证（86 局品项价格分位×全家族供给密度全景，无合格置换对即 KILLED 短路）→ generate_mix_variants 参数扫描变体生成（≤16 个，复用 R9 giant_route 排程/可行性/磁带手术工具，产物落 orderbook_mix_lab/variants/，零改动既有目录）→ openloop_replay_variants 开环重演主判据（26 败局双席位+10 胜局无害臂，对手席=录像开环重放；重演执行复用 R14 实验室 replay_dual_seat，只调用不重写）→ closedloop_probe 闭环副证（开环 POSITIVE 变体 vs 原版 L3 对镜像近亲 5 局双席位直接对打——R9 市场耦合补丁）→ judge_mix_verdicts 三出口判据 → evidence JSON（orderbook_mix_lab/evidence/mix_judgment.json）。fail-closed：任一组件不可执行=整体 fail。不上线不提交。）

- **run_mix_judgment** [L0|新增]
  - 职责：编排裁决——select_corpus_r15 定语料 → phase_m_market_map 出市场地图与置换对排序（零合格对→KILLED 短路出 evidence）→ generate_mix_variants 扫描生成变体（全部不可行→KILLED）→ openloop_replay_variants 跑开环主判据 → closedloop_probe 对开环 POSITIVE 变体跑闭环副证 → judge_mix_verdicts 三出口 → evidence JSON（source 可复跑/市场地图/逐变体构建与可行性/开环逐局 Δ/闭环副证/verdict）。
  - 签名意图：输入: 无（CLI，参数=语料目录/幅度档/变体上限） / 输出: evidence JSON+控制台摘要 / 错误: 任一组件 fail-closed 即整体 fail。
  - 调用方：操作者。
  - tested 策略：上游覆盖: 各组件。
  - 核验命令：测试: orderbook_mix_lab/test_run_mix_judgment.py（编排+短路+evidence schema 组）。
  - **phase_m_market_map** [L1|新增]
    - 职责：市场地图——复用 R14 daily_netflow_decompose（只调用）重算 86 局逐日品项价/量/双席供给 → item_price_percentile 逐品项全程价格轨迹与分位 → rank_swap_pairs 置换对排序+产能窗图谱；输出 Phase M 报告 JSON。
    - 签名意图：输入: 回放目录 / 输出: {items:{price_pct_series, supply_density}, swap_pairs_ranked, capacity_windows} / 错误: 单局失败记录不中断。
    - 调用方：run_mix_judgment。
    - tested 策略：自有单测。
    - 核验命令：测试: orderbook_mix_lab/test_phase_m.py。
    - **item_price_percentile** [L2|新增]
      - 职责：单品项统计——该品在语料全_season 的逐日价格→全程分位轨迹（滚动分位窗口参数化）、崩价/稀缺判定阈值（低分位+高供给密度=崩价品；高分位=稀缺品）。
      - 签名意图：输入: 逐日品项价量表 / 输出: {pct_series, structural_low:bool, structural_high:bool} / 错误: 数据缺→None。
      - 调用方：phase_m_market_map。
      - tested 策略：自有单测（构造崩价/稀缺/中性三态）。
      - 核验命令：测试: orderbook_mix_lab/test_phase_m.py（percentile 组）。
    - **rank_swap_pairs** [L2|新增]
      - 职责：置换对排序——崩价品×稀缺品全组合按（价格分位差×可置换产能）排序，输出 top 对与产能窗（哪些天的哪些品项窗口可迁）；空集=KILLED 依据。
      - 签名意图：输入: 市场地图品项统计 / 输出: [{from,to,expected_gain, windows}] / 错误: 无（空集即结果）。
      - 调用方：phase_m_market_map。
      - tested 策略：自有单测（有对/无对两例）。
      - 核验命令：测试: orderbook_mix_lab/test_phase_m.py（swap 组）。
  - **generate_mix_variants** [L1|新增]
    - 职责：变体生成编排——置换对×幅度档（{10%,20%,30%}）展开参数点（上限 16）→ build_variant_schedule 逐点排程 → check_variant_feasibility 逐个校验（不可行弃并记录）→ build_variant_main 磁带手术产变体 main.py；输出变体清单与构建审计。
    - 签名意图：输入: 置换对排序+幅度档 / 输出: {variants:[{id, pair, scale, schedule, main_path, feasible}]} / 错误: 全不可行→KILLED 依据。
    - 调用方：run_mix_judgment。
    - tested 策略：自有单测。
    - 核验命令：测试: orderbook_mix_lab/test_variant_gen.py。
    - **build_variant_schedule** [L2|新增]
      - 职责：单变体排程——复用 giant_route gen_schedule（只读调用/取材）：按置换对把 from 品产能窗的 X% 迁给 to 品，产逐日买/建/雇/种计划；保持劳动/现金/棚容约束在排程层可满足。
      - 签名意图：输入: 置换对+幅度+原排程基线 / 输出: 变体逐日排程 JSON / 错误: gen_schedule 失败→该变体弃。
      - 调用方：generate_mix_variants。
      - tested 策略：自有单测（构造小排程）。
      - 核验命令：测试: orderbook_mix_lab/test_variant_gen.py（schedule 组）。
    - **check_variant_feasibility** [L2|新增]
      - 职责：可行性校验——变体排程孪生空跑（劳动 op/现金/棚容/停时逐日校验，沿 giant_route feasibility 口径），不可行日逐条报。
      - 签名意图：输入: 变体排程 / 输出: {feasible:bool, violations:[...]} / 错误: 空跑崩溃→不可行。
      - 调用方：generate_mix_variants。
      - tested 策略：自有单测（可行/不可行夹具）。
      - 核验命令：测试: orderbook_mix_lab/test_variant_gen.py（feasibility 组）。
    - **build_variant_main** [L2|新增]
      - 职责：变体 main 构建——按变体排程做磁带产线事件手术（沿 giant_route build_v6 受控变更集方法）：L3 基座副本上改写对应 BUY_SEED/PLANT 事件并保留路由/反应层/清仓结构，装载链与确定性自检；产物落 variants/（基座与在飞件零改动）。
      - 签名意图：输入: 变体排程+L3 基座路径 / 输出: 变体 main.py+diff 审计 / 错误: 手术超界即弃。
      - 调用方：generate_mix_variants。
      - tested 策略：自有单测（小磁带夹具）。
      - 核验命令：测试: orderbook_mix_lab/test_variant_gen.py（build 组）。
  - **openloop_replay_variants** [L1|新增]
    - 职责：开环重演编排——语料 26 败局×双席位+10 胜局原席位，对照臂=原版 L3（与 R14 重合局可复用其对照数据并复算抽验）；逐变体逐局逐席位调 R14 replay_dual_seat（只调用）重演，Δ=同局同席 margin(变体)−margin(对照)；异常重跑一次仍败=红。
    - 签名意图：输入: 变体清单+语料 / 输出: {per_variant:{per_game:{seats, margin, delta}}} / 错误: 单局红=该变体 fail-closed。
    - 调用方：run_mix_judgment。
    - tested 策略：自有单测（mock replay）。
    - 核验命令：测试: orderbook_mix_lab/test_openloop.py。
  - **closedloop_probe** [L1|新增]
    - 职责：闭环副证——对每个开环 POSITIVE 变体：镜像近亲 5 局做 变体 vs 原版 L3 双席位直接对打（twin 引擎，对手可反应），统计互胜与 margin 分布。
    - 签名意图：输入: POSITIVE 变体清单+镜像局集 / 输出: {per_variant:{games, wins, rate, margins}} / 错误: 引擎异常→该局重跑一次。
    - 调用方：run_mix_judgment。
    - tested 策略：自有单测（mock 引擎）。
    - 核验命令：测试: orderbook_mix_lab/test_closedloop.py。
  - **judge_mix_verdicts** [L1|新增]
    - 职责：三出口判据——逐变体：败局 ≥2/3 翻正+胜局重损违例 ≤2（Δ<−100）+败局 Δ 中位>0 → 开环 POSITIVE；开环 POSITIVE 且闭环互胜 ≥0.5 无系统性负 → 变体 POSITIVE；任一变体 POSITIVE→R15=POSITIVE（记胜出变体）；全败→NEGATIVE；KILLED 由编排短路给定。附判据敏感度（2/3 vs 3/5；中位>0 vs 均值>0）。
    - 签名意图：输入: 开环结果+闭环副证 / 输出: {per_variant, overall, winning_variant, sensitivity} / 错误: 语料缺失=fail。
    - 调用方：run_mix_judgment。
    - tested 策略：自有单测（正/负/KILLED 判例）。
    - 核验命令：测试: orderbook_mix_lab/test_judge_mix.py。

## 共享函数（增补）
- **select_corpus_r15**（调用方：run_mix_judgment, openloop_replay_variants, closedloop_probe）
  - 职责：语料选择——26 败局（29 排 3 早崩[112844424/112846785/112847952 由 d10 margin 判定]）+10 抽样胜局（r32/r33 各 5，rng.Random(20260925r15)）+5 镜像近亲局（闭环用，|margin|<400 且资金差<2% 的 r33 败局/平局池抽取，rng 同种子独立抽样）；缺回放=fail-closed 列出。
  - 签名意图：输入: 回放目录+audit 数据 / 输出: {losses26:[...], wins10:[...], mirror5:[...]} / 错误: 语料缺失=fail。
  - 调用方：见上。
  - tested 策略：自有单测（抽样可复现）。
  - 核验命令：测试: orderbook_mix_lab/test_corpus_r15.py。
