# v5 — v48 混合战后资产包（R8-v2 F5：经济保险 + 终局保果层 v2）

> **public derivative with economic-guard + lead-protection layers (post-war build, not for current competition)**

> 战后资产（R8-v2）：只构建 + 离线验证，不上线——零提交冻结 ba1b44c。旗面 `P1/P3 off、P2/P4 on`：在 v4b 形态（行为级≡纯 v48 + P2 死价保险）之上叠加 P4 终局保果层 v2——触发=双条件并集【day≥15 且峰回撤 peak−lead≥2000 且 lead≥1500】∪【day≥24 且 lead≥3000】，峰值经运行峰寄存器跟踪（编排处持有 `_V48H_P4_REGISTER`，跨回合注入，补丁模块保持纯函数）；未触发形态零足迹=原对象返回。由 `python build.py --p4 on --p1 off --p3 off` 的装配函数经 `tmp/build_v5_v2.py` 确定性驱动生成。

## 身份链（identity chain）

| 件 | sha256 | 字节 |
|---|---|---|
| 基底 `../v48_derivative/main.py` | `dadee25a9840313218384208c53b2c4752f82c3209cc654632e0b96c65e2664a` | 107008 |
| P1 `patches/midgame_sell_layer.py` | `1b9f235e9824c6b0c38c362ca53133869be1dcd126fe6bf7fd33dcfcd4de9f94` | 23676 |
| P2 `patches/economic_guard.py` | `e7206b734451cb08a5d9cbbba5f4cf16a88f17dfcf8a3b34cd1f99201ad98713` | 10168 |
| P3 `patches/milestone_monitor.py` | `b0ef3c90380d9de079a6efb0d90462546336e196bd12732ddbb7287f5b0d6caf` | 16760 |
| P4 `patches/lead_protection.py` | `edb7100fed82f8dd5541f0fb0c8be67217b2ab951c31bced61fa09291e8953bb` | 25454 |
| 混合 `main.py`（基底逐字前缀 + 追加块） | `042f84f090fde48c4d51a0f7aa8ca9fe2f4bce5aef993f3001b747ad4e12e8b1` | 130088 |
| `submission.tar.gz`（单成员 main.py，确定性 tar） | `ad698d0189d859f28ca378720add264073198d115f0f1788319b2bb7c32f2e68` | 97655 |

P4-off 无扰动对照：同装配器以 v4b 旗面（P4 off）重建与 `../v4b/` 包逐字节一致（含 tar）；P1-P3 全开（P4 off）重建与根提交件 `../main.py` 逐字节一致——旗面增量对既有构建零扰动（`build_manifest.json` 的 `p4_off_no_disturbance`）。

## 接线与仲裁

卖单面次序：P2 产线否决（死价 BUY/建棚→PASS）→ P4 `build_lead_protection(obs, day=step//24, market, register=_V48H_P4_REGISTER)`（P4 自带门栈：双条件并集触发——回撤臂 day≥15 且 peak−lead≥2000 且 lead≥1500 ∪ 原臂 day≥24 且 lead≥3000；保护时点 6/12/18；step≥717 清仓窗让位；透传现有卖单、仅分批前移补发，量帽 split_qty_cap=4/线数帽 4；未触发/异常=原对象零足迹）；P1/P3 零接线。基底五零改动区以前缀构造保持字节一致（`../audit_base.py` 分区审计）。

## 提交（冻结：不提交）

战后资产不进当前赛事（零提交冻结 ba1b44c）；描述文案留档：`public derivative with economic-guard + lead-protection layers (post-war build, not for current competition)`

## 门禁结果（发射冒烟四门，tmp/fourgate_v5.py 回填）

| 门 | 判据 | 结果 |
|---|---|---|
| gate1 官方装载语义 | 干净 -I 子进程 get_last_callable 复刻一致 | PASS（干净 -I 子进程 get_last_callable 复刻，named==last（_v48hybrid_entrypoint），isolated vs local 动作流 mismatch=0，stdlib 扫描空） |
| gate2 双席自打 | seeds 101/102 双局 720 回合 DONE、每步 <1000ms | PASS（seeds 101/102 双席自打双 DONE 720 回合，seed101 statuses=['DONE', 'DONE'] rewards=[92750,92750] 720回合 max 2.77ms p99 1.2ms; seed102 statuses=['DONE', 'DONE'] rewards=[86550,86550] 720回合 max 3.98ms p99 1.09ms） |
| gate3 确定性 | seed101 重跑动作流哈希逐字节一致 | PASS（seed101 重跑动作流哈希逐字节一致（a009ad5e6fb4…）） |
| gate4 体积 | tar ≤ 100MB | PASS（97,655B ≤ 100MB） |

