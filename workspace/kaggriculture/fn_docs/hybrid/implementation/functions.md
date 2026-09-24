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
| select_corpus_r15 | B1 | wired 09-24 | pytest test_corpus_r15 → 5 passed（抽样可复现/早崩排除/镜像池边界两例/缺回放 fail-closed）；实跑 losses26=26+wins10（r32/r33 各 5）+mirror 4（池<5 取全池记 note） | (本批) |
| item_price_percentile | B1 | wired 09-24 | pytest（percentile 组）→ 3 passed（崩价/稀缺/中性三态+窗口≥8+空表）；双面分位（own-pool 趋势+Markup 截面结构），判据面偏差登记 evidence.method_notes | (本批) |
| rank_swap_pairs | B1 | wired 09-24 | pytest（swap 组）→ 2 passed（score 排序+空集）；实跑单对 MELON→WHEAT（分位差 74.7×产能 39.0=score 29.13，产能窗∩停时窗） | (本批) |
| phase_m_market_map | B1 | wired 09-24 | 实跑 86/86 ok 零 error（50s，复用 R14 daily_netflow_decompose）；crash=[MELON] scarce=[WHEAT]→非 KILLED；单局失败记录不中断面有测 | (本批) |
| build_variant_schedule | B2 | wired 09-24 | pytest（schedule 组）→ 4 passed（迁移+种子同步严格更早步+停时窗过滤）；实跑 moved=1/2/4=target（选点位移重试后零 skip） | (本批) |
| check_variant_feasibility | B2 | wired 09-24 | pytest（feasibility 组）→ 3 passed（ok/cash 击穿/停时越界）；实跑 3 变体全可行（棚容峰值 4-22≤100，现金地板=26 败局日末资金逐日最小值） | (本批) |
| build_variant_main | B2 | wired 09-24 | pytest（build 组）→ 3 passed（splice 区间外一致+拒绝覆盖基座+装载回路）；实跑 3 变体 main.py+build_audit.json（blob 重编码与原编码参数逐字节同构） | (本批) |
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
