# Kaggriculture 软件交付（workspace/software）

Kaggle Simulation Competition **Kaggriculture**（Google/Kaggle 农场经营 720 回合博弈）的
bot、本地评估基建、机制量化工具与增强策略 A/B。

**引擎边界声明**：本地对局运行在**官方引擎**上——PyPI `kaggle-environments` 1.32.7 的
`kaggriculture` 场景（本仓 vendor 了去依赖元数据/去可视化资源的重打包 wheel，引擎代码未改动，
见 `vendor/WHEEL_PROVENANCE.md`）。本地评估结果代表官方规则语义，但**不等价于** Kaggle 线上
天梯（对手分布不同、未做线上提交）。

## 一键命令（仓库根目录执行）

```bash
# 1) 依赖安装（锁定）
python -m pip install -q -r workspace/software/requirements.txt

# 2) 冒烟自检（起环境 -> 自博弈 -> 契约校验 -> 退出码判定，超时看门狗 300s）
python workspace/software/smoke_boot.py

# 3) 测试套件
python -m pytest workspace/software/tests -q

# 4) 强度门（m1 新对手须对冻结弱池 >=50% 胜率，不达标退出码 1）
python workspace/software/scripts/check_opponent_strength.py --rounds 3

# 5) 全量评估（m1 起为全池两两矩阵：9 bot x 36 对 x 4 种子 + 4 局 A/B + 4 局确定性探针，
#    共 152 局，约 7 分钟；产出矩阵/胜率表/Elo/方差报告/eval_results.json schema v1.1）
python workspace/software/scripts/run_eval.py --rounds 4

# 6) 回归门（冻结回归线在冻结子流上断言，快速档约 3.5 分钟；失败退出码 1 并打印差异表）
python workspace/software/scripts/run_eval.py --rounds 2 --assert-regression

# 7) 失败模式探针（submission 对全池多种子深记录，产出 failure_modes.md 的证据层）
python workspace/software/scripts/analyze_failure_modes.py --rounds 8
```

## 目录

```
workspace/software/
├── kaggle_simulations/agent/main.py   可提交 bot（官方 kit 结构，自包含 stdlib-only；
│                                      上传：kaggle competitions submit kaggriculture -f main.py）
├── kgenv/                             本地评估包
│   ├── engine.py                      官方引擎单局对局器（结构化结果/每日资金曲线）
│   ├── gym_env.py                     gym 风格单智能体封装（可插拔对手策略）
│   ├── economy.py                     收益模型（价格曲线/作物周期/动物产出/雇佣/地价）
│   ├── redlines.py                    机制红线检查表（浇水/喂养/产出上限/shed/期限）
│   ├── elo.py                         Elo 评级（只按胜负平，对齐官方天梯语义）
│   ├── arena.py                       对局编排 + 复盘日志 + 提交 bot 加载
│   ├── regression.py                  冻结回归线断言（--assert-regression 的纯逻辑核心；
│   │                                  m1 起只在冻结池子流上断言，强对手不改变冻结线）
│   ├── variance.py                    种子方差统计（Wilson 胜率区间 / t 分数资金差区间）
│   └── bots/                          baseline_wheat / greedy_carrot / cow_baron /
│                                       melon_hoarder / expansionist / LLM provider（默认关）
├── scripts/run_eval.py                全池 matchup 矩阵 + Elo + 方差报告 + 确定性探针 +
│                                       exports 产出（schema v1.1）+ 回归门旗标
├── scripts/check_opponent_strength.py 强度门：新对手对冻结弱池 >=50% 胜率断言
├── scripts/analyze_failure_modes.py   失败模式探针（多种子深记录 + 证据报告生成）
├── smoke_boot.py                      冒烟自检（验收命令）
├── tests/                             pytest：收益模型/红线/agent 契约/对局器/回归门/
│                                       新对手单测/方差统计
├── exports/
│   ├── schema.json                    软件->文档接口契约（评估结果 JSON Schema v1.1）
│   ├── eval_results.json              实测评估样例（全池矩阵 + 方差报告）
│   ├── eval_audit.md(+summary.json)   评估保真度审计清单（ABE-Ralph 式，逐项 pass/warn）
│   ├── failure_modes.md(+summary)     失败模式清单（FM-1..4，含证据局号）
│   ├── failure_probe_report.md        失败探针自动证据层（分差曲线/价格轨迹）
│   └── logs/                          replay_log.jsonl / failure_probe_log.jsonl
│                                       （每局一行的对局记录 + 每日资金 + 共享市场价格）
├── metrics.json                       实测指标分片（只写实测值，禁编造）
├── requirements.txt                   锁定依赖（含 vendor wheel，需从仓库根安装）
└── vendor/                            官方引擎 nodeps 重打包 wheel + 出处说明
```

## 对手池（m1-vertical 波次 2 强化后）

| bot | 风格一句话 | solo 终局资金(vs pass, seed 101) |
|---|---|---|
| cow_baron | 奶牛男爵：6 牛近栏每日喂养+照护（照护银行化 3 奶/2 天），小麦自给饲料，牛奶 130 闸门分批放货 | 48962 |
| melon_hoarder | 囤瓜波段：12+12 双波西瓜、无动物，190 高闸门囤货-放货节奏 | 36751 |
| expansionist | 扩张流：全四象限买地 + 7-8 雇工的工业化小麦庄园 + 6 鹅肥料院（自施肥 6 单/块） | 22007 |
| baseline_wheat / greedy_carrot / starter / random / pass | 第一轮冻结弱池（Elo 1245.8 以下） | 10506 / 6704 / … |

强度认证：三新对手对冻结弱池 3 种子全胜（`check_opponent_strength.py --rounds 3`，9/9 each）；
对 submission 的威胁见 `exports/failure_modes.md`（cow_baron 7/8、melon_hoarder 8/8 胜 submission——
第一轮"24/24 全胜"的弱池假象已被打破，失败模式成为 m2 迭代的输入）。

## Bot 策略（kaggle_simulations/agent/main.py）

"鹅引擎 + 瓜波段"三段式（全部机制来自官方 How-to-Play/engine 源码）：

1. **鹅引擎**：shed 近区建 coop 养鹅；每日 FEED（小麦）+ CARE（喂养日照护银行化 +1 蛋/日，
   即每日照护使产蛋翻倍）+ COLLECT_FERTILIZER（每只存活动物每日 1 肥料，~$100）+ 批量 HARVEST。
   蛋与肥料的价格曲线对抛压耐受（log 上行目标 0.2），可每日倾销。
2. **瓜波段**：第 0-2 天 6 块西瓜进窗口期浇水（6-12 天龄，1+6=6 果/块），第 12-13 天收获，
   按价格闸门分批出货（西瓜 glut 曲线 sq 3.6，乱抛直接砸穿到 $1）；价格仍在 $180 以上时第
   13-16 天续第二波。
3. **小麦基座**：剩余格种小麦（自给鹅粮 + 现金），max_yield_day 收获，只卖喂养储备外的盈余。
4. **劳动与土地**：晨间按负载雇佣（fib 成本 1,1,2,3,...）、资金闸门下买地（NE 早期/SW/SE）。
5. **终局清算**：第 28 天起停 CARE（银行奖金要下个产出日才付），第 29 天清仓一切——只计银行存款。

### LLM 可插拔决策接口（默认关闭）

`kgenv/bots/llm_provider.py`：`NullProvider`（默认）/ `OpenAICompatProvider`
（读 `KG_LLM_PROVIDER` / `KG_LLM_BASE_URL` / `KG_LLM_API_KEY` / `KG_LLM_MODEL` 环境变量）。
带调用次数与时长预算闸（Reasonableness Standard 的机械化落地，参照 ProgRouter 成本路由与
Bayesian Self-Escalation 思路），任何失败超时都回退启发式决策，绝不阻塞回合。
main.py 中的 `LLM_PROVIDER=None` 钩子同样默认关闭——提交形态不依赖任何外部模型。
（规则依据：赛事 rules 允许外部模型，LLM 订阅级费用符合 Reasonableness Standard。）

## 实测结果摘要

**m0 复活会话（2026-08-28，弱池时代）**：40 局全长评估 107.36s；submission 24/24 全胜
（弱池+baseline），平均终局资金 30631.46；Elo submission 1460.9 > baseline_wheat 1245.8 >
greedy_carrot 1162.2；回归门 PASS（20 局 55.49s）。

**m1 波次 2（2026-08-28，对手池强化 + 失败模式证据）**：

- 全池矩阵（9 bot × 36 对 × 4 种子 + A/B + 探针 = 148 局 + 4 探针，346.94s），
  148/148 局恰好 720 回合；两次同配置独立运行 Elo 表完全一致（仅涉 random 对手的奖励漂移）
- Elo（k=32）：cow_baron 1460.3 > **submission 1422.8** > melon_hoarder 1391.3 >
  expansionist 1289.6 > baseline_wheat 1170.6 > greedy_carrot 1155.8 > starter 1058.3 >
  pass 991.5 > random 859.7；池最高 Elo 1162.2 → **1460.3**
- submission 对池：对 cow_baron **0/4**（均差 -17772）、对 melon_hoarder **0/4**（-5410）——
  第一轮"全胜"被强池打破；对 expansionist 4/4（+10014）、对弱池与 baseline 全胜
- 失败探针（种子 201-208 × 8 对手 = 64 局）：submission 49W-15L；失败模式 4 条
  （`exports/failure_modes.md`：奶牛引擎经济压制 / 二波瓜重植被锁死 / 开局爬坡被压制 /
  共享肥料贬值）
- 方差报告：最不稳对局 baseline_wheat vs greedy_carrot（0.75，CI95 [0.30,0.95]，跨种子
  翻转）；submission 相关对局无翻转
- 评估审计：**8 pass / 3 warn / 0 fail**（`exports/eval_audit.md`）
- 回归门：PASS（74 局 196.17s，冻结子流上断言；含一次数据驱动的冻结序修订
  random/pass 对调，见 `kgenv/regression.py` docstring 与审计第 6 项）
- 测试：**84 passed**（新增新对手单测 / 方差统计 / 冻结池门语义 / 复盘价格日志）
- 复现性：确定性对手同配对同种子奖励逐位一致；引擎 `random` 对手奖励漂移（未被子完全
  钉死，已声明边界）

## 已知边界

- 未做 Kaggle 线上提交（队伍人工步骤，蓝图 man-submit）；线上指标在 metrics.json 中为 null。
- 引擎为官方 1.32.7；若 Kaggle 线上 kit 升级机制，需以官方页面直抓为准复核。
- 对手池在 m1 波次 2 已强化（最强 Elo 见 metrics `opponent_pool_max_elo`），但强对手与
  submission 同属启发式家族，存在"同族变体过拟合"风险（eval_audit.md 第 7 项 warn）；天梯
  真实对手分布仍需线上反馈校准。
- 引擎 `random` 对手的奖励未被子完全钉死（种子外熵源），跨会话漂移；矩阵中涉 random 的
  对局奖励可能逐会话漂移，胜负判定与 Elo 序在本池强度差下稳定（eval_audit.md 第 1 项）。
- 矩阵每对只打单座位（p0 视角 × N 种子），未做座位对换；引擎市场为逐单 lockstep，座位
  不对称性预计可忽略（eval_audit.md 第 8 项 warn）。
