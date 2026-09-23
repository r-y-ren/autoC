# 责任文档：磁带生成管线（tape_gen）
> 由 fn-divide 产出与独占更新；fn-implement 只读。实现期结构性变化必须回本阶段改本文档。
> 上游：requirements.md（R1-R7）。批次：T1 挖掘 → T2 库+变体 → T3 搜索+选择 → T4 组装+管线。函数总数 20（预警线上，各批 ≤8）。

## 结构概览
- mine_trajectories ← R1
  - load_replay_corpus
  - extract_and_filter_seats
- build_route_library ← R2
  - elect_backbone
  - fork_routes_on_events
  - verify_replay_fidelity
- derive_market_variants ← R3
  - apply_market_edit_operators
  - assert_farmer_stream_identity
- search_reflector_configs ← R4
  - define_config_space
  - evaluate_ablation_tree
- select_on_holdout ← R5
  - split_train_holdout
  - rank_candidates_seated
- assemble_and_gate ← R6
  - build_candidate_package
  - run_m1_m2_gates
- run_pipeline ← R7

## 需求覆盖矩阵
| 需求 | 顶层函数 |
|---|---|
| R1 | mine_trajectories |
| R2 | build_route_library |
| R3 | derive_market_variants |
| R4 | search_reflector_configs |
| R5 | select_on_holdout |
| R6 | assemble_and_gate |
| R7 | run_pipeline |

## 功能块 mine_trajectories ← R1
（块引言：全量语料→逐席动作流库；剔除我方席与 v48 家族克隆席（1-51 步逐字节判定）；/tmp 缓存先持久化入库；确定性+语料哈希。）
- **load_replay_corpus** [L0|新增]：装载 round27/28+lead-collapse+/tmp 缓存（若有）；语料哈希与清单。签名意图：输入: 语料目录集 / 输出: {games:[{path, sha, seats}], corpus_hash} / 错误: 缺目录 fail-closed。
- **extract_and_filter_seats** [L1|新增]：逐席 719 步动作流提取+克隆/我方席过滤+元数据（对手/结果/边际/克隆旗）。验收：同语料同输出；过滤抽查清单 ≥10 局。
## 功能块 build_route_library ← R2
（块引言：嵌缀树路由库，格式兼容 v48 执行机制（RouteLibrary 载入即回放）；骨干+事件分叉+共享前缀约束（分叉步与商店事件对齐）。）
- **build_route_library** [L0|新增]：编排。输入: 轨迹库 / 输出: RouteLibrary / 错误: 轨迹不足 fail-closed。
- **elect_backbone** [L1|新增]：骨干选举（最多共享前缀的走位流）。
- **fork_routes_on_events** [L1|新增]：商店事件分叉（对齐 88/120/153/216 式事件步；共享前缀强制）。
- **verify_replay_fidelity** [L1|新增]：库内路由经 v48 回放器逐步回放=源轨迹逐字节（金标准）。
## 功能块 derive_market_variants ← R3
- **derive_market_variants** [L0|新增]：编排。输入: 骨干+算子集 / 输出: 变体集+差分账本 / 错误: 算子异常跳过留痕。
- **apply_market_edit_operators** [L1|新增]：时点/量/帽算子（文档化集合）生成市场编辑变体。
- **assert_farmer_stream_identity** [L1|新增]：farmer 流与骨干逐字节断言+市场单差分账本。
## 功能块 search_reflector_configs ← R4
（块引言：消融树= v48 自带反射层开关/阈值（含编译未启用 market_maker/MPC/终局强改）+新增保险层；稀疏惩罚（启用模块数计入代价，同适应度取更稀疏枝）。）
- **search_reflector_configs** [L0|新增]：编排（空间定义→树评估→稀疏优先选择）。输入: 候选库+评估预算 / 输出: 选定配置+消融账本 / 错误: 预算耗尽取已评最优并标注。
- **define_config_space** [L1|新增]：空间文档（枚举开关/阈值轴+新保险层）。
- **evaluate_ablation_tree** [L1|修订 v2]：分阶段混合适应度——粗筛=留出流 seated（保预算）；精评起=0.5×留出+0.5×对纯 v48 引擎对打；稀疏惩罚不变。
## 功能块 select_on_holdout ← R5
（块引言：训练/留出分离；**留出集对手与挖掘集不相交**（R9 镜像假阳教训内建）；选择只在留出集裁决。）
- **select_on_holdout** [L0|新增]：编排。输入: 候选集+分离 / 输出: 最终件+留出逐局边际表 / 错误: 留出局不足 fail-closed（≥30%）。
- **split_train_holdout** [L1|新增]：种子化分离（对手级不相交）。
- **rank_candidates_seated** [L1|新增]：seated 适应度表（孪生整季重演，真实对手流）。
## 功能块 assemble_and_gate ← R6
- **assemble_and_gate** [L0|新增]：编排（打包→四门→M1/M2）。输入: 库+配置 / 输出: 包+门禁报告 / 错误: 任一门红如实分档（管线不成 vs 未到五线）。
- **build_candidate_package** [L1|新增]：换 RouteLibrary/配置字节重打包（v48 外壳，机制区不动）。
- **run_m1_m2_gates** [L1|新增]：M1=seated 对纯 v48 互胜 ≥0.45；M2=五线（h2h≥0.65/巨人 seated×3/胜局回归 8/四门/经济面）。
## 功能块 run_pipeline ← R7
- **run_pipeline** [L0|新增]：全管线确定性编排+消融账本（语料/中间件/选择哈希链）；双跑逐字节一致。验收：管线产物双跑一致+账本 schema 校验。
