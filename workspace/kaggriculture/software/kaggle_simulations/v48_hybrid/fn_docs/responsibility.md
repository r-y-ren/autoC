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
- **apply_midgame_sell_layer** [L1|新增]：三门卖出计划器语义实现（从旧树 market.py 取材改写为独立模块）：输入=回合观测（价格/库存/资金/剧本预期卖单）/输出=中期卖单/错误=异常→回退剧本默认卖单。含与反克隆/槽位重排的仲裁规则（v48 优先）。
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
