# functions.md —— 函数级实现清单（补登版）
> 2026-09-23 补登（fn-review 审计 Important 项对账修正）：本梯 F1-F3 压缩执行未留三文档，现按 commit 80b68e2 与 gates_report.json 回溯登记。代码与门禁台账为真值，本表为导航。
> 改状态前先跑核验、贴输出，绿了才许改。

| 函数 | 批次 | 状态(日期) | 核验命令+摘要 | commit |
|---|---|---|---|---|
| apply_midgame_sell_layer | F1 | wired 09-22；v2 09-22；v3 09-23 FAIL 已回退 | 27 passed（v2：tape 透传/day≥13/只补发/N=3 前瞻/基底日历重推导一致性） | 80b68e2 |
| apply_economic_guard | F1 | wired 09-22 | 14 passed（90/90/30+4 帧+day≥10 窄化；未触发同对象返回） | 80b68e2 |
| apply_milestone_monitor | F1 | wired 09-22 | 33 passed（d10-12 里程碑表/只动卖单缝/异常回退） | 80b68e2 |
| load_v48_base | F2 | wired 09-22 | audit_base PASS（前缀逐字+五零改动区分区+三注入点唯一） | 80b68e2 |
| assemble_package | F2 | wired 09-22 | 双跑逐字节一致；旗关零接线字节级；发射四门全绿 | 80b68e2 |
| run_h2h_gate | F3 | wired 09-22 | v1 0-16 → v2 4W-4L-8T 互胜 0.25（FAIL 结构性）；AB/BA 显式席位 | 80b68e2 |
| run_panel_gate | F3 | wired 09-22 | 合成语料 6 局 seated ratio 0.9994 PASS（官方语料=主力机补测） | 80b68e2 |
| check_zero_new_anomalies | F3 | wired 09-22 | kinds=[] 新增=[] PASS | 80b68e2 |
| run_launch_fourgate | F3 | wired 09-22 | 装载 719 obs 零失配/双席 DONE×2/确定性/stdlib | 80b68e2 |
| test_guard_inactive_equivalence | F3 | wired 09-22 | p000 逐字节 4/4；全开≡p100 4/4 | 80b68e2 |
| test_trigger_coverage | F3 | wired 09-22 | 触发面用例齐（v2 后 p2/p3 有效触发 0——正常局零动作实证） | 80b68e2 |
| estimate_lead_margin | F4 | wired 09-25 | patches 113P 之一（三态 basis：farms_money_direct 直读实测/代理/None） | (本批) |
| plan_protective_sells | F4 | wired 09-25 | patches 113P 之一（717-718 让位/帽 4/时点 6,12,18/异常原单） | (本批) |
| build_lead_protection | F4 | wired 09-25 | patches 113P 之一（day≥24 且 lead≥3000 门；未触发原对象） | (本批) |
| assemble_lead_protection_build | F4 | wired 09-25 | v5 包 20421986…/95,489B；四门绿；P4-off 对照≡v4b 逐字节 | (本批) |
| run_replay_gate | F4 | wired 09-25 | 真实跑 0/14（判据 ≥7/14 FAIL；8/14 重演=原值逐位=P4 零足迹自证；EOD 变体仍 0/14） | (本批) |
| run_equivalence_face | F4 | wired 09-25 | 8/8 逐字节一致（构造 4+真实 4） | (本批) |
| run_launch_recheck | F4 | wired 09-25 | 四门真复跑+patches 113P | (本批) |
| verify_lead_protection | F4 | wired 09-25 | 总裁决 FAIL（重演门）落 gates/out/lead_protection_verdict.json | (本批) |
| build_lead_protection | F5 | wired-v2 09-25 | 触发并集+峰寄存器（56 测之一）；v5 重建 042f84f0… | (本批) |
| run_replay_gate | F5 | wired-v2 09-25 | **双臂对照 28 重演：wins 0/14，Δ 正1/负4/零9（净-2642）=杠杆符号确证为负** | (本批) |
| verify_lead_protection | F5 | FAIL-v2 09-25 | gates/out/lead_protection_v2_verdict.json=FAIL；等价面 8/8+四门绿（实现无瑕） | (本批) |
| generate_giant_schedule | G1 | wired 09-23 | 排程 17羊6牛/SE d13/可行性 1 轮 0 违规/收入峰 13634@d17（favorable 情景） | (本批) |
| perform_tape_surgery | G2/G2b | wired 09-23 | 三面重生成（产线 858+卖 723+移动 180 路由日）；v6b 5a532201 四门绿 | (本批) |
| assemble_v6_build | G2/G2b | wired 09-23 | v6 da844619（中间产物）/v6b 5a532201 | (本批) |
| verify_structure_gates | G3 | FAIL 09-23 | 五线 1/5：h2h 0-16（-150k 级）/巨人 0-9/回归 8/8 翻负/四门过/经济面 16-37% | (本批) |
| _cxs_harvest_completable | S1 | wired 09-23 | pytest -k harvest + crosscheck → 6 passed；常数转录 WHEAT/CARROT=48,TOMATO=192,STRAW/MELON=240 | (本批) |
| _cxs_completable_plant_demand | S1 | wired 09-23 | pytest test_layer_s → 11 passed（demand 组 7+harvest 组 4；2 红为他批桩预期） | (本批) |
| _cxs_seed_surplus | S1 | wired 09-23 | pytest test_layer_s → 16 passed（供给三路+None 矩阵 8 组；库存字段=private.seeds 依 L6775/L4693） | (本批) |
| _cxs_seed_truncate | S1 | wired 09-23 | pytest test_layer_s → 23 passed 全绿（含三构造用例；快道同对象零足迹） | (本批) |
| _cxs_agent | S1 | tested 09-23（wired 待 S2 注入；P1 修复后复验） | pytest 全家 37 passed；注入模拟链路过；_CXS_HOST 块首捕获+独立态 None | (本批) |
| append_layer_s_block | S2 | wired 09-23 | pytest test_build → 4 passed；末callable=_cxs_agent 真exec 0.09s；三道写入前防线（拒原件/判重/纯净副本） | (本批) |
| build_layer_s_candidate | S2 | wired 09-23 | build 实跑三产物（main dc6412f5/tar 1dd87d7d/manifest）；配方复刻 round-30 重打包复现 2838cc66；test_build 8 passed | (本批) |
| replay_action_diff | S3 | wired 09-24 | 26 局全量：10 identical/16 RED（基座回买@662×12+少卖 EGG@669×4）；final_delta 26 局无负值 | (本批) |
| precision_subset_check | S3 | wired 09-24 | 26/26 all_ok 0 violation（WHEAT 21≤84/CARROT 94≤128）；模式甲金丝雀绿 | (本批) |
| constructed_invariant_cases | S3 | wired 09-24 | c3 夹具形态修正为真实链路（决策步 670+plants@671）；复用 test_layer_s 夹具零复制 | (本批) |
| gate_equivalence_precision | S3 | wired 09-24 | 新口径（反应面+结果面）26/26 game_pass：消失×77+回买×16 全形态有界、步界 652-656≥648、final_delta 全 ∈{0,+10,+30}；evidence 协议 1.1 | (本批) | (本批) |
| gate_h2h_vs_verbatim | S3 | wired 09-24；P0 修复重跑 09-24 | 16 局全量 14-0-2 绿（rate 1.0≥0.55：seeds 101-104/201-203 双席全胜 margin +10、204 双席 tie）；装载=官方 last-callable（import 复用门② _load_entry）+身份断言 _cxs_agent/_cxd_agent。初跑 0-0-16 全 tie 系装载缺陷误定性（评审 P0 纠正） | (本批) |
| gate_lineage_strength | S3 | wired 09-24 | 24 局 24-0-0 三对手零负——48-0 谱系强度保持 | (本批) |
| gate_launch_fourgate_l1 | S3 | wired 09-24 | 四门全绿 22.2s；truncation_only_diff 差异步=1（step 653）全 ≥648 | (本批) |
| verify_layer_s_gates | S3 | wired 09-24 | 全量编排 overall=PASS（四门全绿：①14-0-2 ②24-0 ③26/26 ④全绿+差异步 653）；发射前置达成 | (本批) | (本批) |
| make_layer_s_v2_block | S4 | wired 09-24 | v2 块 sha 0c130d68；diff 恰一函数体校验过 | (本批) |
| _cxs_seed_surplus | S4 | wired 09-24 | S4·v2 净需求覆盖落地+全矩阵过——但口径被门①③实证否决（见下） | (本批) |
| build_l11_candidate | S4 | wired 09-24 | 三产物 main 60b6f283/tar ae186747/manifest | (本批) |
| gate_h2h_vs_l1 | S4 | wired 09-24 | 全量 16 局 0-6-10：六败全恰 -10（seeds 103/104/203）——L1 的 +10 在净口径下丢失 | (本批) |
| gate_equivalence_v2 | S4 | wired 09-24 | appear_total=16>2（零拦截）；死种 $3,310>$900 且劣于 L1 $3,190 | (本批) |
| constructed_cases_v2 | S4 | wired 09-24 | 五件全过（单测面） | (本批) |
| verify_l11_gates | S4 | wired 09-24 | overall=FAIL（门①③红②④绿）——设计级否决，批间门裁决 | (本批) |
| make_layer_s_v3_block | S5 | wired 09-24 | 双窗块 w648 5fc4c53c/w600 c308ff26；路由边界解耦修正（_CXS_ROUTE_BOUNDARY=648 恒定+审计不变式） | (本批) |
| _cxs_agent | S5 | wired 09-24 | S5·v3 wired；h2h 16 局全平局=行为≡L1 | (本批) |
| _cxs_reduce_orders | S5 | wired 09-24 | S5·v3 wired；减量按设计精确触发（112432199：3→2@657/662）——但被基座逐步补偿 | (本批) |
| _cxs_seed_balance | S5 | wired 09-24 | S5·v3 wired；R=赤字+安全边矩阵全绿 | (本批) |
| _cxs_observed_plant_rate | S5 | wired 09-24 | S5·v3 wired；planted_day 观测源 | (本批) |
| build_l2_candidate | S5 | wired 09-24 | 两窗六产物（w648 44aaa824/w600 b5f3c522） | (本批) |
| gate_equivalence_v3 | S5 | wired 09-24 | 形态面绿/结果面红：死种 3190=L1（控制器补偿）；饿死零容忍绿；子集绿 | (本批) |
| constructed_cases_v3 | S5 | wired 09-24 | 九件全过 | (本批) |
| verify_l2_gates | S5 | wired 09-24 | 两窗 overall=FAIL recommended=None——闭环控制器实证否决 R12 价值前提 | (本批) |
| inject_controller_clamp | S6 | wired 09-24 | fine 中间件 95382180（恰 45 行受控变更+六校验+五区恒定） | (本批) |
| _ca_future_plant_demand | S6 | wired 09-24 | route2 后缀胡萝卜+保守小麦槽；None→回退原目标 | (本批) |
| build_l13_candidate | S6 | wired 09-24 | 双注入产物 main 340229db/tar f624222c/manifest | (本批) |
| gate_launch_l3 | S6 | wired 09-24 | 形态扩展过；差异步 653 | (本批) |
| gate_equivalence_l3 | S6 | wired 09-24 | form 红=空槽占位伪差异×9；死种 2090>900 帽；starve/subset/cases 全绿 | (本批) |
| constructed_cases_l3 | S6 | wired 09-24 | 七件全过 | (本批) |
| verify_l13_gates | S6 | wired 09-24 | overall=FAIL 仅门③两因：空槽分类器缺口+死种帽未达 | (本批) |
| select_corpus_r15 | B1 | wired 09-24 | pytest test_corpus_r15 → 3 passed（13c82ea 收口合并+test_seed_derivation；对账 09-25 重跑复核 3 绿——原记 5 passed 为收口前口径）；实跑 losses26=26+wins10（r32/r33 各 5）+mirror 4（池<5 取全池记 note） | (本批) |
| item_price_percentile | B1 | wired 09-24 | pytest（percentile 组）→ 3 passed（崩价/稀缺/中性三态+窗口≥8+空表）；双面分位（own-pool 趋势+Markup 截面结构），判据面偏差登记 evidence.method_notes | (本批) |
| rank_swap_pairs | B1 | wired 09-24 | pytest（swap 组）→ 2 passed（score 排序+空集）；实跑单对 MELON→WHEAT（分位差 74.7×产能 39.0=score 29.13，产能窗∩停时窗） | (本批) |
| phase_m_market_map | B1 | wired 09-24 | 实跑 86/86 ok 零 error（50s，复用 R14 daily_netflow_decompose）；crash=[MELON] scarce=[WHEAT]→非 KILLED；单局失败记录不中断面有测 | (本批) |
| build_variant_schedule | B2 | wired 09-24 | pytest（schedule 组）→ 3 passed（迁移+种子同步严格更早步+停时窗过滤；对账 09-25 重跑 3 绿——原记 4 为合并前口径）；实跑 moved=1/2/4=target（选点位移重试后零 skip） | (本批) |
| check_variant_feasibility | B2 | wired 09-24 | pytest（feasibility 组）→ 3 passed（ok/cash 击穿/停时越界）；实跑 3 变体全可行（棚容峰值 4-22≤100，现金地板=26 败局日末资金逐日最小值） | (本批) |
| build_variant_main | B2 | wired 09-24 | pytest（build 组）→ 2 passed（splice 区间外一致+拒绝覆盖基座+装载回路；对账 09-25 重跑 2 绿——原记 3 为合并前口径）；实跑 3 变体 main.py+build_audit.json（blob 重编码与原编码参数逐字节同构） | (本批) |
| generate_mix_variants | B2 | wired 09-24 | pytest end_to_end → 2 passed；实跑 3 参数点全构建零弃（sha 4e1ec1c5/c18374f6/4de93f6f） | (本批) |
| openloop_replay_variants | B3 | wired 09-24 | pytest（mock replay）→ 4 passed（Δ/复用+抽验/红/预算截断）；实跑 239 重演无红：对照复用 11 席+抽验 2 局 drift=0.0+fresh 51 | (本批) |
| closedloop_probe | B3 | tested 09-24（NEGATIVE 下未触发实跑） | pytest（mock 引擎）→ 3 passed（互胜率/中位/重跑一次/红定向）；mirror 池 4 局已备 | (本批) |
| judge_mix_verdicts | B3 | wired 09-24 | pytest → 5 passed（正/负三路/KILLED 透传+敏感度/红 fail-closed）；实跑三变体全 NEGATIVE（敏感度四门全 False） | (本批) |
| run_mix_judgment | B4 | wired 09-24 | pytest（编排 mock）→ 5 passed（全流/KILLED 双短路/S1 fail-closed/闭环触发）；实跑 322.6s → evidence/mix_judgment.json overall=NEGATIVE | (本批) |
| fetch_2965_source | B5 | wired 09-24 | gzip 载荷解码+sha 钉死（bc8f8464 双源核实）；缓存命中/失败重试 | (本批) |
| merge_increments | B5 | wired 09-24 | 真跑：三增量 222 行移植+layer S 20705B 逐字节拆解；前/后缀恒等；末 callable=_cxd_agent；_cxs_* 零残留 | (本批) |
| apply_2965_constants | B5 | wired 09-24 | 真跑：恰三处（2→3/−15→−5/8→20）+RACE [40,44] 不动断言 | (本批) |
| audit_diff_vs_2965 | B5 | wired 09-24 | 真跑：a/b 白名单归因全绿零 UNATTRIBUTED；篡改注入试验红 | (本批) |
| build_2965_adopt | B6 | wired 09-24 | 双件构建：r34a 51fc19db/r34b 15fafc6d；tar 双跑逐字节；manifest sha 链 | (本批) |
| verify_2965_gates | B7 | wired 09-25 | 真跑合计约 603s（a 291.7s+b 310.9s）：r34a overall=PASS（五门全绿）/r34b overall=FAIL（h2h 0.50+subset 红）；evidence 落 a/b 子目录+提交记录 a/evidence/submission_record.json | (本批) |
| phase_v_adjudicate | B9 | wired 09-25 | pytest（汇总/单件失败不阻断）→ 2 passed；实跑三件汇总（羊 adopt/番茄·路由否决）evidence/phase_v_summary.json | (本批) |
| probe_sheep_fertilizer_loop | B9-B10 | wired 09-25 | pytest 3 件（闭环解剖/断链/注入语料不足 3）→ 3 passed；实跑 8 高羊败局 8/8 闭环 adopt（收肥 367-435/麦施 15-37/增产 +1.77~2.60/经济性 4/4） | (本批) |
| scan_tomato_gate | B9-B10 | wired 09-25 | pytest 4 件（两行变体唯一性/网格编排+胜者/全负不并入/胜局翻负否决）→ 4 passed；实跑 14.3min：42 粗+top-3 邻域×18 局全零 Δ → NEGATIVE 保 70/12000 | (本批) |
| expand_route_table | B9-B10 | wired 09-25 | pytest 3 件（指纹+路由复算/正流并入/回归剔除）→ 3 passed；实跑唯一候选 (1042.0,9989)→116 重演翻负（−10,161/−1,789）剔除→空集 NEGATIVE | (本批) |
| build_r35 | B9,B11 | wired 09-25 | pytest 8 件（HR 块抽取+遥测拒斥/改1-only/全并入/只加表项纪律/杂散 diff 拒斥/归因/真基座集成）→ 8 passed；实跑两形态（702bbe1e 全并集/3e5d7340 改1-only）+tar 双跑逐字节 | (本批) |
| verify_r35_gates | B9,B11 | wired 09-25 | pytest 5 件（全绿/fail-closed 全跑/身份链红传导 h2h/未构建红/h2h 重定向装载身份集）→ 5 passed；实跑×2：launch·lineage·diff 绿+h2h 0.50+subset 红 → overall FAIL×2 | (本批) |
| run_r35_iteration | B9 | wired 09-25 | pytest 3 件（全流 launch_ready/失败留痕 run_summary/--skip-phase-v 复用）→ 3 passed | (本批) |
| forensic_cxtb_trigger | B13-B14 | wired 09-25 | pytest 4 件（触发/面死/结局差分组/锚幂等）→4 passed；实跑 86/86 clean 105s：call_rate 1.0 face 活、fire 9/86、触发局轨迹=BUY_SEED 10@432+SELL 26-29 天窗 | (本批) |
| scan_wheat_step91 | B13-B14 | wired 09-25 | pytest 3 件（胜者规则/全负保基线/skip 条款）→3 passed；实跑 91s：五点表全负或零（31 饱和触发送走一切麦卖）→adopt False | (本批) |
| adjudicate_cxtb_variants | B13-B15 | wired 09-25 | 阶梯化两变体均 Δ 中位 0/均 −2848；三常数 OAT 8 点×主语料+敏感带全中位 0——无胜点（内置函数，责任矩阵外辅助件） | (本批) |
| build_r36_conditional | B13,B15 | wired 09-25 | pytest 6 件（锚唯一/幂等/阶梯形态/无 adopt 拒斥/白名单归因/尾块防混入）→6 passed；判决全负→未实跑构建（B15 出口） | (本批) |
| verify_r36_gates | B13,B15 | wired 09-25 | pytest 5 件（全绿/fail-closed 全跑/身份链/未构建红/阶梯入口）→5 passed；r36 未构建→未实跑门禁（B15 出口） | (本批) |
| run_r18_iteration | B13-B16 | wired 09-25 | pytest 5 件（POSITIVE 全流/KILLED_T/惰性 NEGATIVE/门禁红 NEGATIVE/失败留痕）→5 passed；实跑 260s verdict=NEGATIVE launch_ready=false | (本批) |
| parse_episode_states | B19 | wired 09-25 | pytest test_parse_states.py → 29 passed（真 replay 结构 1440 行/双席/字段+最小件全等+缺字段 25 例+坏 JSON/缺文件+口径钉）；口径裁定：行 step=replay 原生 si（磁带 step X 动作在 X+1 行）、money=farms[seat].money 执行后值、animals_grid/tiles 从 tiles[y][x] 提取；6 局全过解析 | (本批) |
| replay_guard_verdict | B19 | wired 09-25；rev 09-26 | pytest test_judge_replay.py verdict 组 → 7 passed（+棚仓臂最小复现：钱被卖货掩蔽但 inventory 增=成交、inventory 平=仍判失败）；**09-26 修订（用户裁决）**：成交判据加棚仓臂（inventory 分物品字典按 item 计数——引擎买畜进 private.shed 不上格、钱扣被同拍卖单收入掩蔽，17 张真成交误报驱动）+对照 l1 降观测（移出 pass 门）；口径：死逃/买失败成交窗/cash_d1h0=step24 沿旧 | (本批) |
| judge_cash_guard_replay | B19 | wired 09-25；rev 09-26 | pytest test_judge_replay.py → 11 passed；**真跑 32 重演 overall=PASS（修订后 09-26）**：死牛 0 ✓/真丢单 0 ✓（原 17=判定器假阳性，逐张复核全额成交）/d1 现金 min 12.0 ✓；对照 l1 观测值（逐席 min −25,433/合计 +130,128/10 席翻负）不进红绿（用户裁决）；evidence/replay_judgment.json（含 criteria_revision 留痕） | (本批) |
| count_shearings | B20 | wired 09-26 | pytest test_judge_league.py count 组 → 7 passed（链计数/保守+产物推断两支/MILK·EGG 不认领+假认领剔除/覆盖率两分支/UNKNOWN/真样本可复算深等）；剪毛口径=同席同单元同日 HARVEST→PLACE WOOL 链认领为主+产物推断补（PLACE 12 常覆盖多次 HARVEST）+非羊格链矛盾不计；真样本 112938600 实算 124 刀/19 轮（席 65/59）；evidence/count_shearings_sample.json | (本批) |
| judge_sheep_league | B20 | wired 09-26 | pytest 12 passed（judge 4+count 7+伞面）；400 局全量真跑（修正前守卫）=主对 0-200 确诊过度扣单→守卫三修后 **60 局小联赛 h2h rate 0.6136≥0.55 达标**（种子级 5W/17T/0L、run 级 10W/34T/0L，强臂 0.75、mirror 0.5，全谱零负）；剪毛=轮次 100%≥5（8-12 轮）但每羊 4 次（R20 目标 5 未达）；evidence/judge_sheep_league.json | (本批) |
| _r37_defer_low_priority | B17 | wired 09-25；rev 09-26 | 09-26 三修（用户裁决）：①顺延线改逐单价精确丢单保护（qty×GOOSE300/COW400/SHEEP500，只拦引擎真会丢的）②投影计入同列表前序 SELL 收入（lockstep 口径，卖价=obs 市场价读不到回退保守）③BUY_SEED 入重发范围（FIFO 回填可负担空槽）；pytest test_runtime_guard.py → 17 passed（+逐单价 450 分界/卖单收入计入+位序反例/种子回填/卖单不动反例）；SELL·DROP·PLACE 差异归因=底版反应层原生改写非守卫越权（evidence/action_diff_attribution.json） | (本批) |
| _r37_cash_guard | B17 | wired 09-25；rev 09-26 | pytest 17 passed 全绿；09-26 三修随轮：floors 改 {"d0_end":12,"buy_animal":"exact_cost"}+prices 覆盖表（逐单价精确丢单线）、投影含同列表前序 SELL 收入；d0 窗[20-23]≥12/硬底线夹持/零足迹/双命中取更严维持 | (本批) |
| _r37_agent | B17 | wired 09-25；rev 09-26 | pytest 17 passed 全绿；09-26 三修随轮：顺延账回填扩 BUY_SEED（FIFO 落可负担空槽、无可负担槽不连坐低价意图）；入口 fail-safe/step0 复位/动作集合不变量维持；微探针归因=守卫只动购买槽（灾难语料 36 处干预全在购买槽、真局 0 干预） | (本批) |
| inject_cash_guard_block | B17 | wired 09-25 | pytest test_inject_guard.py → 6 passed（四条校验复核/尾部追加不变量/委托冒烟/sha 确定性/失败即抛/源同步）；**r34a 实跑**：1,038,506→1,066,974B（块 28,468B，block_sha 30dedaefe44d…），四条校验全过，evidence/inject_r34a_smoke.json；命名=纯核块内改名 _r37_guard_core+单参入口 _r37_agent+捕获行 _R37_GUARD_PARENT（避开底版 _R37_PARENT 撞名） | (本批) |
| retape_sheep_timing | B18 | wired 09-25 | pytest test_retape_sheep.py → 9 passed（解码回路/刀次公式 d11=5·d12=4 抛/只提前+target_step 标定/no-op/总量不变/资金序 V57/解剖快照可复算）；真 r34a 解剖：41 路由 231 批羊单全 ≥5 刀、仅 route 12/115 各 1 批越窗——手术=115 前移 265→264、12 供资锁 skip、229 no-op；编解码 `_decode_routes/_encode_routes` 私有真源（blob=base85(zlib(json)) 池共享写时复制+四条自检链）；evidence/sheep_tape_dissection.json | (本批) |
| retape_tail_savings | B18 | wired 09-25 | pytest test_retape_tail.py → 9 passed（窗口外不动/违抛/删净/闲置 HIRE 判据[当日 HIRE 序 m→hands[m]]/HARVEST·卖单逐类不动/池共享 CoW/饿死边界 d29 停喂≤1/真跑可复算）；真 r34a：CARE 779 删（d28 613+d29 166）、FEED 0（r34a 本就 d29 停喂）、HIRE 0（451 张全有役）——真跑结论非空转；evidence/tail_savings_realrun.json | (本批) |
| build_sellflow_library | B22 | wired 09-26 | pytest test_sellflow → 4 passed（迷你建库/无 renyxin 跳过/坏文件抛/真跑可复算）；**真跑 86 局建库**：n_used=86、SELL 事件 29,470、键数 158、库 sha acb76cfc…；键=「店对\|m钱_w麦」（OPEN1:/EARLY 档）；evidence/sellflow_library_realrun.json | (本批) |
| infer_rival_sells | B22 | tested 09-26 | pytest test_predict_runtime → 5 passed（五组全绿）；逆推=库存差分+城镇消费−自家净卖（_town_consume 口径）、$1 地板记 lower_bound、跨步账本 _ledger | (本批) |
| match_sellflow | B22 | tested 09-26 | pytest 5 passed；键命中真库集成探针 source=key（规范键=建库口径对齐，容错候选同查）；置信=min(1,n/10)×集中度，门槛 0.5 | (本批) |
| extrapolate_sells | B22 | tested 09-26 | pytest 5 passed；净卖∪库均量合成 1-2 步预测 SELL 写 plan[step]（同槽同品取 max 合并）；低置信跳过 | (本批) |
| apply_dodge | B22 | tested 09-26 | pytest 5 passed；预测集中抛售 Q≥3 且置信足→整单顺延置 []/减量改单；只动 SELL 槽；避让账带 due_step（跨步重发待裁决留档） | (本批) |
| _predict_agent | B22 | tested 09-26 | pytest 5 passed（全链串通/异常 fail-safe/step0 复位/假父层注入）；链=父层→infer→match→extrapolate→dodge；_PREDICT_PARENT/_PREDICT_LIBRARY 捕获变量注入面 | (本批) |
| inject_predict_block | B23 | wired 09-26 | pytest 7 passed（四条校验/尾部不变量/单参冒烟/sha 确定/失败即抛/库对账双向/真 r37 实跑）；真烟 1,296,398→1,324,745B（块 28,347B）；捕获 _PREDICT_PARENT=_r37_agent 真链、末 callable=_predict_agent；五函数 ast 抽取零手抄+typing 填充（B17 同款） | (本批) |
| audit_diff_vs_r37 | B23 | wired 09-26 | pytest audit 组 8/8（正路/前缀破坏/锚行缺失或双现/同文本/键稳定/装饰兼容/块外垃圾/JSON 往返）；核心短语「r38 对手预测尾块」识别；归因={ok,whitelist{predict_block},unattributed} | (本批) |
| pack_r38 | B23 | wired 09-26 | pytest pack 组 6/6（字段齐/双跑同 sha/tar 形态/区分度/坏输入/缺件 null 不造假）；manifest orderbook_r38_manifest/1.0（14 键：base_sha_chain 四节点/predict_block/library_sha AST 主链+伴生行兜底）；真源复用 build_tar_bytes；签名微调 out_dir=None | (本批) |
| build_r38 | B23 | wired 09-26 | pytest build 组 5/5+全包 37 绿（4 桩=B24）；**真跑**：main 1e07f0f2d69a/tar 51b388e5d9b3/块 292,740B（含真库）；库 sha acb76cfc…三口径对账恒等；审计零 UNATTRIBUTED；双跑恒等；r37 零改动；evidence/build_r38_realrun.json | (本批) |
| flip_stats | B24 | wired 09-26 | pytest flip 组 6 passed（晚崩判定[loss_phase 三段最负主导=晚崩，15/20 复现]/非晚崩不计/realized 价差/UNKNOWN/对照资金差/避让抢跑差分）；真跑口径=重演差分 vs 原局逐席自比 | (本批) |
| judge_predict_replay | B24 | wired 09-26 | pytest judge 组 4 passed；**真跑 36 条目/30 局 258.6s overall=NEGATIVE（如实）**：晚崩翻正 0/15、对照 final_delta min −82,919（10/10 负）、h2h vs r37 0.000（8 seed 全负 mean −146.6k）、realized 草莓 delta_px −1.75（未升反跌）、避让 3329/预测写入 9975；可信度证=r37 件重演精确复刻原局；evidence/judge_predict_realrun.json | (本批) |
| verify_r38_gates | B24 | wired 09-26 | pytest 4 passed（全绿路/红不短路/fail-closed/独立 n 不双计）；真跑 5m27s overall=FAIL（如实）：合规✓/launch✓/谱系 16-0✓、h2h 0.0<0.55✗、饿死 1/26 违例+净经济 −621,148✗；evidence/gates_r38_realrun.json 四件 | (本批) |
| run_r38_iteration | B24 | wired 09-26 | pytest 5 passed（全链 mock POSITIVE/判决红 NEGATIVE 收档不进门禁/门禁红不发射/Error 留痕/收档台账形态）；verdict 逻辑=判正才门禁+发射台账、判负收档台账（archive_note 判负留赛后）；真跑整合=收档链 | (本批) |
| audit_diff_vs_r34a | B18 | wired 09-25 | pytest test_build_r37.py audit 组 → 7 passed（三类全归因/白名单外即抛/前缀破坏即抛/同文本零归因/键稳定/blob 解码失败定罪/in_blob 未分类定罪）；归因表 {ok,whitelist{tail_guard_block,sheep_retiming,tail_savings},unattributed}；真跑 ok=True UNATTRIBUTED 0（guard 229,858B/1 move/779 removed）；断言 str 路由键裁定=代码即真值（JSON 往返 str 键） | (本批) |
| pack_r37 | B18 | wired 09-25 | pytest test_build_r37.py pack 组 → 8 passed（字段齐+文案原文/确定性双跑/tar 形态 mtime0·mode644/区分度/坏输入抛/双跑不等抛/whitelist 尽力自证/签名意图）；manifest schema orderbook_r37_manifest/1.0（base_sha_chain a16e0e9b→51fc19db→r37、三件 sha 内嵌注释自证、double_run）；单一真源复用 build_adopt.build_tar_bytes；签名微调=可选 out_dir=None（登记） | (本批) |
| build_r37 | B18 | wired 09-25 | pytest test_build_r37.py build 组+全包 → 53 passed（B17+B18 全绿；7 红=后续批次桩）；**真 r34a 构建验收实跑**：源 sha 51fc19db… 前后不变、r37 main 430a702d73cc…、tar dcbdcf9743d2…（648,327B）、归因 ok 零 UNATTRIBUTED、确定性双跑全同、manifest complete=True；流程=decode→羊手术→尾盘手术→encode→变更表注释→注入守卫块→审计→打包（tempfile 中转，失败不落半成品）；evidence/build_r37_realrun.json | (本批) |
| verify_r37_gates | B21 | wired 09-26 | pytest test_gates_r37 → 6 passed；**五门实跑 overall=PASS**：合规四轴 4/4、launch 四门（last-callable=_r37_agent/719 obs 零分歧/双席 DONE/确定性/身份链）、h2h vs r34a **0.5625≥0.55**（n=8 独立 seed）、谱系 v48/v4b 各 8-0、饿死 26/26+**净经济 +73,824 金**（09-26 判据重裁：死种降观测——L3 纯减法口径不适配经济守卫层，三轮运行时实验+源头补丁勘察证实死种差不可消）；evidence/gates_r37_realrun.json | (本批) |
| run_r37_iteration | B21 | wired 09-26 | pytest test_run_r37 → 5 passed；**全链整合实跑 6.7min**：build 确定性同 sha（4b237e412d51）、判决 A pass=true（死牛 0/真丢单 0/d1 现金 min 11）、verdict=**HOLD**——judgments_green=false 只因 judge_sheep_league 的"每羊 5 刀"未达（**已知项·用户裁决"接受现状"**：计划面每格 ≥5 达标、真局执行漂移留档），gates 段按"判决红不进门禁"短路（五门独立实跑 overall=PASS 在案）；发射已按"通过即上线"授权+已接受判决态执行（run_summary.json 留痕） | (本批) |
| detect_clone | B25 | wired 09-27 | pytest clone 组 4 用例（相似度 0.95 含界/step1 现金差 <0.5 严格/缺字段保守/异常→非克隆）；跨步快照函数属性 _stream | (本批) |
| infer_rival_sells | B25 | 改造 wired 09-27 | pytest infer v2 组 6 子用例（删失下界 max(0,D−U)/禁填 0 反例/噪声门 ≤$3·sold<2/最终动作快照） | (本批) |
| match_sellflow | B25 | 改造 wired 09-27 | pytest match v2 组 5 子用例（TOP-1 取一/历史门 3×0.70 两分支/global ×0.5 降档/旧库条目 v1 兼容） | (本批) |
| extrapolate_sells | B25 | 改造 wired 09-27 | pytest 六门逐项（窗 336-646/K=4·2×pred/每步每品 1 单/带通 4-99·min(棚存,48h 计划)/价门 min_sell_price=2+base/噪声门 skipped）+tier 三档+credit 减记禁净加卖；常量落 extrapolate 内 | (本批) |
| apply_dodge | B25 | 改造 wired 09-27 | pytest 门两分支+action 零改动反例+异常全 allow；**删除顺延/置 [] 旧语义**（公开负结果教训落地） | (本批) |
| _predict_agent | B25 | 改造 wired 09-27 | pytest 非克隆零写入/克隆走链/step0 复位全账含 credit/deny 回滚 plan 钩子+credit/异常 fail-safe | (本批) |
| build_sellflow_library | B26 | 改造 wired 09-27 | pytest 11 passed（top-30 时间序/新旧合并/hit 3×0.75/样本<3 缺省/<30 抛/真跑）；真跑 30 新(17,570 事件)+86 旧(29,470)→213 键、hit 覆盖 34/213、库 sha fd30fba3…；hit 口径=窗桶预期 ±50% 含界、条目级聚合 | (本批) |
| retape_shear_phase | B26 | wired 09-27 | pytest 5 passed（偏移+刀次≥5/越季 no-op/不动买卖 FEED CARE 反例/空槽不变/真跑）；真 r37=16 格偏移(+2 天型)/267 no-op/刀次 min 5；走位曼哈顿 ≤1 可达校验 | (本批) |
| inject_predict_block | B26 | 改造 wired 09-27 | pytest 8 passed（v2 块形态组新增）；六件抽取序+内嵌 v2 库+四条校验+库 sha 对账（canonical ensure_ascii=False）；锚行短语不动 | (本批) |
| audit_diff_vs_r37 | B26 | 改造 wired 09-27 | pytest audit 组 4 passed；两类白名单（尾块 v2 锚行+shear_phase blob 归因带变更表核对）；v1 单类路径 19 测零回退；真跑零 UNATTRIBUTED（283 行=16 偏移+267 no-op 逐条吻合） | (本批) |
| pack_r39 | B26 | wired 09-27 | pytest pack 组 5 passed；manifest orderbook_r39_manifest/1.0（链 a16e0e9b→r34a→r37 剥块→r39；predict_block/library/shear_change 三 sha 自证）；build_tar_bytes 真源复用；文案 "…(v2) and anti-counter schedule" | (本批) |
| build_r39 | B26 | wired 09-27 | pytest build 组 4 passed；**真跑构建**：main b0370ee619e7/tar b6da5f12bf52/块 a9b310a4145c/库 fd30fba3…/shear 2ebeb766…；归因 ok 零越界；双跑恒等；r37 零改动；evidence/build_r39_realrun.json | (本批) |
| make_counter_opponent | B27 | stub 09-27 | 测试: test_judge_predict.py（counter 组） | — |
| flip_stats | B27 | 改造待做 09-27（v2 动作降量面） | 测试: test_judge_predict.py（flip v2 组） | — |
| judge_predict_replay | B27 | 改造待做 09-27（v2 六判据+反制臂） | 测试: test_judge_predict.py（v2 组） | — |
| verify_r39_gates | B28 | stub 09-27 | 测试: test_gates_r39.py | — |
| run_r39_iteration | B28 | stub 09-27 | 测试: test_run_r39.py | — |
