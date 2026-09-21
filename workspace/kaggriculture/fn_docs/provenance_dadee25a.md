# dadee25a 双源血统记录（R4）

## 血统对象

- artifact sha256: `dadee25a9840313218384208c53b2c4752f82c3209cc654632e0b96c65e2664a`
- 字节数: 107008（源A 记录方公布口径）
- 定性: v48 公开衍生；在跑线上资产 ref 56400478

## 源 A（首拉）

- 账号: kaitofukami
- notebook: 40/40 Early Floor | 39/46 Top-10 | v48 Fast Routes
- 拉取日期: 2026-08-31
- 来源通道: kaggle kernels pull（首拉，自解包 cell 执行重建）
- sha: dadee25a9840313218384208c53b2c4752f82c3209cc654632e0b96c65e2664a（与 notebook §7 公布值逐字节一致）
- 记录文件: software/kaggle_simulations/opponents/PROVENANCE.md
- 许可现状: 无显式许可（notebook 未附开源许可；只作对手重放，不挖实现）
- 备注: 作者自报面板: first-20 40/40、Top-10 holdout 39/46、Top-30 97/140（冻结动作流重放，非天梯分）

## 源 B（拉回）

- 账号: ahmedberatozer
- notebook: kaggriculture-v48-clear-the-queue（Kaggriculture V48 — Clear the Queue）
- 拉取日期: 2026-09-20
- 来源通道: kaggle kernels pull（终局期 fresh-sweep 拉回）
- sha: base=其提交包解码真源码 dadee25a…（notebook 内嵌源 sha 4b540288…）
- 记录文件: software/kaggle_simulations/v48plus/README.md
- 许可现状: Apache-2.0（notebook 声明，待核）
- 备注: 实证: references/INDEX.md L38（fresh-20260920 批次含 ahmedberatozer/v48-clear-the-queue）

## 原创归属

- **两账号间未定**（两账号通道各自独立入库同 sha；无证据裁断唯一原创方，对外不得断言任一账号为唯一作者。）

## 在跑线上资产引用规则

- 在跑线上资产 ref 56400478（dadee25a 衍生）的一切对外引用=双源并列（kaitofukami 2026-08-31 首拉 + ahmedberatozer 2026-09-20 拉回），禁止单源断言任一账号为唯一来源。

## 全库单源断言扫描（两记录文件+对外文档面）

- 扫描规则: 文件内提及两账号标记（大小写不敏感）恰一个=单源断言残留；两个=双源；零个=与血统无关。扫描面=两记录文件 + `docs/**/*.md`。
- 扫描目标 11 件：双源 0、单源残留 2、无关/缺失 9。

### 残留清单（旧树冻结，战后处置）

| 文件（战役根相对） | 仅提及 | 缺失源 |
|---|---|---|
| software/kaggle_simulations/opponents/PROVENANCE.md | A(kaitofukami) | B(ahmedberatozer) |
| software/kaggle_simulations/v48plus/README.md | B(ahmedberatozer) | A(kaitofukami) |

- 处置: 残留文件属旧树（冻结），其单源表述的物理统一随新结构迁移副本落地执行（迁移副本按本记录双源化改写），旧树本体战后修改；新结构对外文档自即日起按上方【在跑线上资产引用规则】节双源引用。

### 对外文档面（docs/）结论

- docs/final_sprint_plan.md: unrelated
- docs/market_strategy_design.md: unrelated
- docs/online_probe_sop.md: unrelated
- docs/opp_supply_observer_design.md: unrelated
- docs/phase_branch_plan.md: unrelated
- docs/session-findings-20260921.md: unrelated
- docs/track-B-digital-twin-planner.md: unrelated
- docs/track-C-bc-spec.md: unrelated
- docs/worker_route_scheduler_design.md: unrelated

## 记录元信息

- 生成器: fn_work/src/record_governance_dispositions/write_dual_source_provenance.py（record_governance_dispositions 编排叶）
- 引用纪律: 本记录一切源事实来自入库证据（opponents/PROVENANCE.md、v48plus/README、references/INDEX.md L38），不凭记忆撰写。
