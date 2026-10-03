# 新公开策略来源审查与有限融合

2026-09-22。只解析下载的 Notebook JSON 与 Python AST，提取第 2 号单元中的压缩源码，没有运行 Notebook 安装、保存、提交或发布单元。

## 原始来源和完整性

| 来源 | 本地原始源码 | 版本 | 字节数 | SHA-256 |
|---|---|---:|---:|---|
| [Ahmed Berat Özer：V56](https://www.kaggle.com/code/ahmedberatozer/kaggriculture-v56-smarter-seeds-and-fertilizer) | `external/ahmed_v56.py` | 1 | 1056142 | `a1ad0fd1d174477ee2cbdd561a812bcb7029647ce34599e79d6b79e9057eff6c` |
| [shiiin9：Orderbook](https://www.kaggle.com/code/shiiin9/your-market-list-is-an-order-book) | `external/orderbook.py` | 2 | 1026965 | `a16e0e9b40c489972630a0b9d04f30e9c1cab03159fa78676db74277d84d82ab` |

两个结果均与各自 Notebook 声明的 EXPECTED_SHA256 精确一致。原始字节和所有署名保留。公开 Apache-2.0 祖先包括 Thomas Tschinkel、Yusuke Hayashi、Dmitrii Gluzdov、Ahmed Berat Özer 等，Orderbook 新层署名为 shiiin9。

## 静态检查

对两份源码分别递归解出 3 个 Python 单元。只观察到标准库导入；未观察到网络请求、子进程或文件写操作。

两处 `exec` 执行的内容都是源码内固定字符串，分别为官方物理动作规则和七步终局模拟器。二者在两个版本中逐字相同，已递归检查。唯一 `open(path)` 在可选销售预测库函数中，而该函数将 `path` 固定为 `None`，对应分支不执行。运行不依赖这个外部文件。

可重复提取与检查脚本：`extract_round7_candidates.py`。详细导入与敏感调用位置记录：`research/round7/source_audit.json`。这是静态检查结果，不是运行表现结论。

## 融合边界

以 Orderbook 完整源码作为不变前缀，保留其市场排序、番茄投资判断和原作者已经选择的常数。仅追加 V56 的两项输入节省机制：按剩余种植机会限制末期种子采购；预计不会增加计划收成时避免再次施肥。

兼容性检查确认 `_ca_visits`、`_ca_yield_path`、`_v219_native_day` 的 AST 相同，内嵌物理模拟器源码相同。V56 追加段中的父入口从 `final_price_guard` 改接 `_cxd_agent`，避免绕过 Orderbook 新层。其余 V56 机制代码保持不变；额外入口只汇总错误和命中计数，未再调参。

生成候选：`experiments/round7_orderbook_v56.py`，1033333 字节，SHA-256 为 `273ca38d83d110166af4e2f2c6748892328488d5292f39fdbe4ef87b11350197`。

构建脚本：`build_round7_orderbook_v56.py`；来源与哈希清单：`research/round7/orderbook_v56_manifest.json`。此处仅完成静态构建及接口检查，是否采用取决于主任务的独立完整对局结果；未运行比赛或上传。

## 融合发布前复审

复审对象为上面的固定 SHA-256，候选文件未因审查而改写。

- **调用链**：`round7_orderbook_v56_agent → e410_agent → e402_agent → _cxd_agent → _cxtb_agent → V55`。D 层和番茄投资门控均保留，未被新增父入口绕过。
- **接口**：新增机制使用的三项路线/产量助手函数与 Orderbook 版本 AST 相同，两份内嵌物理模拟源码完全一致。Orderbook 较积极的胡萝卜替换常量不改变这些接口；种子预算对麦与胡萝卜各保留全部剩余二者种植机会总数，是偏保守的上限。
- **市场槽位**：种子层仅缩减固定价格种子购买数量，完全取消时留下空槽；它不重新排列已由 D 层选择的出售。施肥层只改单位动作，不再重排市场。两项节省机制仍需真实对局确认，源码兼容不等同于收益叠加。
- **施肥预测前提**：已覆盖三天的情形直接保留肥料；其他情形按当前可见作物与原计划的后续浇水/收获比较产量。已识别的反应式专职工人不采用这项计划预测。未来路线可能因杂草或缺货而偏离，因此“本次预测相同”不保证所有未来情形收成相同；有限独立对局与回放核对仍是必要证据。
- **重置**：新种子缓存、种子计数、施肥计数、D 层计数均在 step 0 重置。继承的 `_CXTB_REPORT` 是跨局累计诊断，原版本就不逐局清零；其数值不用于决策。不要把其累计调用次数误判为决策状态泄漏。
- **真实入口**：最后新定义的 callable 是 `round7_orderbook_v56_agent`；最终 `agent` 指向同一函数。隔离验证应选择最后 callable，不能使用之前的 `kaggle_submission_agent`，后者仍指向种子层并会跳过施肥层。
- **沉默错误**：必须检查入口的 `seed_errors`、`fertilizer_errors`、`cxd_errors`、`cxtb_errors`。还应遍历顶层名称含 REPORT/STATS 的字典中的 error 字段，以及 `_IMPL.chassis.diagnostics` 的 error/fallback。仅看到 DONE 与空 stderr 不够。
- **时限**：主任务现有 6 局融合对 Orderbook 报告的最大动作耗时为 0.216226 秒。D 层每回合最多评分 800 个排序；新增种子层仅末期工作且有缓存，施肥层仅在实际有施肥请求时工作。这些是本机观察和结构约束，不是所有输入、所有硬件的一秒上界。

独立发布脚本 `build_release_v7.py` 已编写并通过语法检查，尚未运行。它固定候选哈希，验证实际压缩包成员；运行后会创建两局 1438 步的连续隔离核对，分别测试原始观测键序和排序键序，保留完整 stderr 和所有错误计数快照。它不更新主入口或默认构建脚本。
