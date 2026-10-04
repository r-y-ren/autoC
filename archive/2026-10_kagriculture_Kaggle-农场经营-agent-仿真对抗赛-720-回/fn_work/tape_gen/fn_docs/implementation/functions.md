# functions.md —— 函数级实现清单（唯一状态真值）
> 改状态前先跑核验、贴输出，绿了才许改。

| 函数 | 批次 | 状态(日期) | 核验命令+摘要 | commit |
|---|---|---|---|---|
| load_replay_corpus | T1 | done 2026-09-22 | `python -m pytest tests/mine_trajectories -q`（14 passed）；真实语料 182 局装载（full 182+projection 14 全被 full 压制去重），corpus_hash=7a77a51a…；缺目录 fail-closed/projection 可选 | — |
| extract_and_filter_seats | T1 | done 2026-09-22 | 同上；364 席：保留 162/剔我方 185+克隆 17+其他 0；本队名实测=renyxin；克隆判定 turns1-51 sha256 对 routes.json 六路由（合并 1 签名）；独立复核 3 克隆匹配+2 保留不匹配+1 席全流 719 步逐字节一致 | — |
| mine_trajectories | T1 | done 2026-09-22 | 同上；corpus/trajectory_store.jsonl（364 行，18.8MB）+mining_summary.json+filter_audit.md（12 局抽查）落盘；双跑（含异目录）逐字节一致，store sha=2e337c72… | — |
| elect_backbone | T2 | wired 2026-09-23 | 74 passed 之一；42/161 席共享≥51 步；8 席全季走位全同；medoid 并列首取最高胜局边际 | (本批) |
| fork_routes_on_events | T2 | wired 2026-09-23 | 74 passed 之一；12 组分叉裁决：1 事件对齐（73↔72 首店，25 席）成路由，深层分叉单例/无对齐 excluded（账本） | (本批) |
| verify_replay_fidelity | T2 | wired 2026-09-23 | 74 passed 之一；两路由 719 步 0 失配；v48 真值解码件载入回放逐字；对称校验过其六路由 | (本批) |
| build_route_library | T2 | wired 2026-09-23 | 74 passed 之一；2 路由（default+fork_s73_e72）v48 纯基格式+manifest；shared_prefix=73≥72 不变量 | (本批) |
| apply_market_edit_operators | T2 | wired 2026-09-23 | 74 passed 之一；3 算子（shift±1/2 天 502 单守恒/scale 426/日帽 277） | (本批) |
| assert_farmer_stream_identity | T2 | wired 2026-09-23 | 74 passed 之一；8 变体 farmer 流恒等全过+差分账本 | (本批) |
| derive_market_variants | T2 | wired 2026-09-23 | 74 passed 之一；8/8 变体（≤8 稀疏上限）market_variants.json+ledger | (本批) |
| define_config_space | T3 | done 2026-09-23 | `python -m pytest tests -q`（97 passed 之一）；空间=10 件×2^5=320 全枚举+微轴扇出 2 登记；config_space.json/md 落 search/；同库面同输出 | (本批) |
| evaluate_ablation_tree | T3 | done 2026-09-23 | `python -m pytest tests -q`（97 passed 之一）；反射层真值=深读档 modules 只读组装（含 seat1 obs.step=None 计数器补步修复）；粗筛 320×8→精评 top6×111→微轴 1；score=winrate−0.02×模块数 | (本批) |
| search_reflector_configs | T3 | done 2026-09-23 | `python -m pytest tests -q`（97 passed 之一）；真实搜索 852s/3490 rollouts 预算未耗尽；账本 22 行 JSONL content_sha256 自证；最终件 route:default+clone_preempt 留出 0.4706/+440 | (本批) |
| split_train_holdout | T3 | done 2026-09-23 | `python -m pytest tests -q`（97 passed 之一）；157 对手→训练 109/留出 48（30.6%≥30%）局 111/51 不相交证明；挖掘源 Anton Tikhonov+Yuzu 圈禁训练侧 | (本批) |
| rank_candidates_seated | T3 | done 2026-09-23 | `python -m pytest tests -q`（97 passed 之一）；seated 表（winrate 平局 0.5+逐局明细）；排序 (-score, modules, id) 同分取稀疏；评估器可注入 | (本批) |
| select_on_holdout | T3 | done 2026-09-23 | `python -m pytest tests -q`（97 passed 之一）；裁决只在留出（训练成绩仅入报告）；fail-closed 留出<30%；final_selection.json+holdout_margin_table.csv 落盘 | (本批) |
| build_candidate_package | T4 | wired 2026-09-23 | 127 passed 之一；只换 _V48_ROUTES blob（span 前后缀逐字节自证）；6 槽别名填充语义登记；包 e8e8fbdf/79,569B | (本批) |
| run_m1_m2_gates | T4 | wired 2026-09-23 | 127 passed 之一；M1=0/16 互胜 0.0<0.45 FAIL（均 -13,022）；M2：四门 PASS+巨人 seated 部分+，余四线 FAIL | (本批) |
| assemble_and_gate | T4 | wired 2026-09-23 | 127 passed 之一；分档 BELOW_LINE（管线通/结构线未到）；双跑计时遥测剥离修复+回归测试 | (本批) |
| run_pipeline | T4 | wired 2026-09-23 | 127 passed 之一；全管线 1309s+1362s 双跑逐字节；链哈希 db9c1476（T1 7a77a51a→T2 85e76389→T3 67007777 咬合） | (本批) |
