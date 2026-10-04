# 🌾 Kaggriculture Silver Medal Solution: The Master Hybrid Engine

<div align="center">

[![Kaggle Silver Medal](https://img.shields.io/badge/Kaggle%20Competition-Silver%20Medal%20%F0%9F%A5%88-silver?style=for-the-badge&logo=kaggle)](https://www.kaggle.com/competitions/kaggriculture)
[![Framework](https://img.shields.io/badge/Architecture-Tri--Modal%20Hybrid%20Engine-orange?style=for-the-badge)](https://github.com/sunyuxiang136/kaggriculture-silver-agent)
[![Runtime](https://img.shields.io/badge/Dependencies-Pure%20Python%20Stdlib-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Decision Time](https://img.shields.io/badge/Step%20Latency-%3C%203ms%20%2F%20step-brightgreen?style=for-the-badge)](https://github.com/sunyuxiang136/kaggriculture-silver-agent)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow?style=for-the-badge)](LICENSE)

**Kaggle 模拟博弈对抗赛 Kaggriculture 银牌方案完整源码**  
**融合“离线确定性最优录像带 + 在线 DSM 动态规划器 + 泊松博弈截胡调度器”的高性能三模态自主智能体**

[English Overview](#english-overview) | [中文深度解析](#chinese-deep-dive) | [📚 完整源码大白话解析手册](CODEBASE_GUIDE.md)

</div>

---

<a name="chinese-deep-dive"></a>
## 🌟 方案全景与真实系统架构

Kaggle **Kaggriculture** 是一个双人同台对抗的 $10 \times 10$ 网格农场经营仿真模拟博弈比赛。比赛周期严格运行 **720 步（30 天 $\times$ 每天 24 小时）**。终局时只有手头现金计分，所有未收获作物、未出栏牲畜在第 719 步全部归零。

在 720 步的长程博弈中，纯规则（IF-ELSE）极其容易在后期复杂局面下死锁，而纯强化学习（RL）收敛慢且极难在非线性价格衰减与斐波那契雇工成本下保证稳定性。

本项目派生自 Kaggle 开源社区经典的 **The 2965 Master Hybrid Engine（V39/V46 经典谱系）**，由 **Shawn404** 深度重构并演化为一套**高弹性三模态自适应切换智能体**：

```
                              ┌─────────────────────────────────────────┐
                              │           Kaggle Observation            │
                              └────────────────────┬────────────────────┘
                                                   │
                  ┌────────────────────────────────┴────────────────────────────────┐
                  ▼                                                                 ▼
      [Step 2 & Step 47 特征监测]                                       [Step 0 ~ 215: 前 9 天]
      • Step 2: 记录对手资金 m2                                          • 运行离线极值录像带 (hy_opening.py)
      • Step 47: 统计对手西瓜数 mel1                                     • 启用 8 大防御护盾防卡死
                  │                                                                 │
                  └────────────────────────────────┬────────────────────────────────┘
                                                   │
                                     [Step 215 (Day 9 末尾) 决策门]
                                                   │
                         ┌─────────────────────────┴─────────────────────────┐
                         ▼ (对手异常: m2 < 1000 & mel1 != 12)                 ▼ (常规主流对手)
               【模态一：早期特异分流规划器】                            【模态二：离线最优录像带继续巡航】
               Day 9 ~ Day 29 (Step 216 ~ 719)                     Day 9 ~ Day 20 (Step 216 ~ 503)
               • hy_eplanner.py (pd_modules_early)                 • 稳定复现高精经济扩张路线
               • 提前在线自适应接管，反制非主流打法                                   │
                                                                   [Step 503 (Day 21 末尾) 常规交接]
                                                                                     │
                                                                                     ▼
                                                                        【模态三：后期自适应动态规划器】
                                                                        Day 21 ~ Day 29 (Step 504 ~ 719)
                                                                        • hy_planner.py (pd_modules_late)
                                                                        • 毫秒级状态重放热启动 (_catch)
                                                                        • DSM R1-R8 视窗回归决策系统
                                                   ┌─────────────────────────────────┘
                                                   ▼
                                       【终局大甩卖：Step 718】
                                       • 触发全局清仓中断，仓库物料 100% 折现
```

---

## 🔬 核心代码实现与硬核算法模块

### 1. 真实的三模态自适应换挡机制（`main.py`）
整个系统在 `main.py` 中通过精密的全局控制器 `_S` 实现三模态调度：
- **前 21 天黄金录像带（`hy_opening.py`）**：默认在 **Day 0 ~ Day 20（Step 0 ~ 503）** 执行离线经过数万次搜索验证的最优宏观路线。单步决策 $< 1\text{ms}$，绝不超时。
- **开局特征扫描与早期分流（Early Fallback）**：
  - 在 `Step 2` 捕获对手资金：`self.m2 = rival['money']`
  - 在 `Step 47` 统计对手地块西瓜数：`self.mel1 = melons(rival)`
  - 若在 `Step 215`（Day 9 结束时）发现 `self.m2 < 1000 and self.mel1 != 12`（对手没有走主流 12 西瓜流，且资金处于异常状态），控制器判定对手为怪异非主流流派，立刻在第 9 天提前换挡切换至 **`hy_eplanner.py`（早期规划器）**！
- **无缝状态迁移与热启动（`_catch` & `_pd_fp_replay`）**：
  - 在录像带运行期间，`self.buf` 全程缓存历史对局。
  - 一旦触发模式切换（无论是 Day 9 还是 Day 21），系统在几毫秒内将数百步的历史动作全速注入规划器，实现**全状态无缝热交接**！

### 2. 离线底盘内置的 8 大高可靠护卫盾（`hy_opening.py`）
录像带并非僵硬的死板脚本，其底盘内置了 8 大响应式护盾层：
1. **`hand_align`**：工人数目动态对齐与自动截断，防止工人状态不同步。
2. **`weed_repair`**：当系统随机长出的杂草阻挡了建筑或播种时，毫秒级插入 `DIG` 拔草任务并恢复录像带。
3. **`sell_lead`**：提前一拍挂单销售，锁定前瞻流动性。
4. **`front_run`**：抢跑拦截 Hook，在对手预定卖单前提前出清压价。
5. **`budget_guard`**：以 72 步（3天）为周期的滚动斐波那契雇工预算守卫。
6. **`room_guard`**：每日 23:00 强制检查仓库容量 $\le 99$，杜绝爆仓丢失产出。
7. **`clamp_sells`**：根据预期仓库容量实时修正裁剪卖单，防止超卖废单。
8. **`dead_stock`**：自动出清路线永远不会再使用的废料死库存。
9. **`terminal_liquidation`**：在 Step 718 执行全局资产清仓折现。

### 3. DSM (Data-driven State Model) 宏观规划大脑（`pd_plan.py`）
核心规划器实现了一套严密的 **DSM 视窗加性回归规则库（R1 ~ R8）**：
- **产物生命窗口规划**：
  - **草莓（Strawberries, S）**：高单价（$120）多轮收获，严格限制在 `Day 12 ~ Day 17` 窗口加性前载种植；
  - **番茄（Tomatoes, T）**：`Day 9 ~ Day 20` 窗口，结合披萨店（PIZ）、农贸市场（FRM）数量动态求解配额；
  - **胡萝卜（Carrots, C）**：3 天成熟周期，在 `Day 20 ~ Day 27` 填补后期闲置农田；
  - **小麦（Wheat, W）**：饲料基石，全天候保障牲畜供应，严禁盲目贱卖生小麦。
- **畜牧业扩张蓝图**：
  - 构建以 **9 头奶牛（产奶 $160） + 8 只绵羊（产毛 $200）** 为主力的大型双牧场；
  - 奶牛采购截止日为 Day 20，绵羊采购截止日为 Day 23。中后期形成强大的每日破万元现金流。
- **R8 动态用工配比**：根据全场工单所需工时（task-turns）精确求解当日招工数，避免雇佣费用斐波那契级爆炸。

### 4. 非线性市场操盘手与分级出货机制（`pd_market.py`）
- **小镇商店周期节拍套利（Market Beat: `Step % 4 == 1`）**：小镇商店每 4 步清空一次收购库存（`Step % 4 == 0`）。操盘手锁定在刚刷新后的第 1 拍（`hours 1, 5, 9, 13, 17, 21`）集中交易，锁定顶格收购溢价。
- **分级出货策略（Flat vs Steep Goods）**：
  - **Flat Goods（平缓商品）**：番茄、鸡蛋、胡萝卜、小麦、肥料等价格弹性低的商品，在套利窗口全量出清；
  - **Steep Goods（敏感商品）**：草莓、牛奶、羊毛、西瓜等商品，单次砸盘 50 单位会导致市价暴跌至 11%~28%。算法通过参数 `cfg['lot']` 严格按配额分批平滑挂单。
- **Hour-23 仓库容量守门员 & Step 718 全局清仓**：防止爆仓丢失物资，并在终局倒数第 2 步将 100% 物理实物转化为有效分值。

### 5. 运筹学执行器：Morning Kit 与 LNS 防撞车调度（`pd_exec.py`）
- **早间工具箱（Morning Kit）**：工人在每天 Hour 0 优先规划仓库门前路径，一次性领齐全天作业所需物料，减少 70% 往返奔波。
- **破环与重建局部搜索（Ruin & Recreate, LNS）**：内置大邻域局部搜索算法与自适应时间预算（Adaptive Search Budget），实时处理多工人路径冲突，确保 720 步 0 撞车。

### 6. 泊松博弈论对手预测与抢跑截胡（`fp_rival.py` & `fp_sched.py`）
- **对手销售模型（IPF Poisson Hazard）**：通过迭代比例拟合（IPF）建模对手的销售危害率（Hazard Rate），结合朴素贝叶斯先验预测对手出货时间表。
- **零和博弈优化目标函数（`fp_sched.py`）**：
  $$\max \quad J = \sum_t \text{OurRevenue}(t) - \lambda \sum_t \text{RivalRevenue}(t)$$
  在预测出对手的大规模清仓时段前，通过 Hook 机制**提前 1 步微量砸盘（Front-running）**，压低对手卖出时的市场收购价，实现对同台竞争对手的精准价格压制。

---

<a name="english-overview"></a>
## 🌐 English Overview

**The Master Hybrid Engine** is a battle-tested autonomous farming agent designed for the Kaggle Kaggriculture competition, achieving a prestigious **Silver Medal**. Engineered by **Shawn404** on top of the renowned *The 2965 Master Hybrid Engine (V39/V46 lineage)*, it merges offline deterministic optimization with online dynamic adaptation:

1. **Tri-Modal State Switching (`main.py`)**:
   - **Default Route**: Replays an optimal offline route (`hy_opening.py`) through **Day 20 (Step 503)**, then hands over control to the online planner (`hy_planner.py` / `pd_modules_late`) from **Day 21 to Day 29**.
   - **Early Fallback**: Continuously tracks opponent telemetry (`m2` balance at Step 2, melon count `mel1` at Step 47). If an anomalous rival is detected at Step 215 (`m2 < 1000 and mel1 != 12`), the agent switches early to `hy_eplanner.py` on Day 9.
   - **Zero-Latency State Handover**: Historical observations and market actions cached in `self.buf` are replayed instantly via `_pd_fp_replay` in $< 5\text{ms}$ upon planner activation.
2. **DSM Rule Book Planning (`pd_plan.py`)**: Incorporates multi-window additive regression rules (R1-R8) across crops and animals, front-loading high-yield investments while capping Fibonacci labor scaling.
3. **Game-Theoretic Interception (`fp_sched.py`)**: Leverages an IPF-fitted Poisson hazard model to project opponent liquidation timings, optimizing a penalized objective $\max J = \sum \text{Revenue} - \lambda \sum \text{RivalRevenue}$ to front-run competitor sell orders.
4. **Operations Research Execution (`pd_exec.py`)**: Utilizes Morning Kits and Ruin-and-Recreate Large Neighborhood Search (LNS) for collision-free multi-worker task execution.

---

## 📁 目录架构与源码映射

本项目兼顾 **Kaggle 单文件提交规范** 与 **本地模块化二次开发**：

```text
kaggriculture/
├── README.md                      # 本文档：架构全景、技术亮点与使用指南
├── CODEBASE_GUIDE.md              # 📚 强烈推荐：9000字全中文“大白话”逐文件深度解析手册
├── LICENSE                        # Apache-2.0 开源许可证
├── requirements.txt               # 运行环境依赖（纯 Python 标准库，可选 kaggle-environments）
├── main.py                        # 【Kaggle 提交文件】单文件提交 Bundle（包含压缩的 3 模态核心）
└── decompressed/                  # 【模块化工程源码】可完全阅读、调试与二次开发的核心源码
    ├── hy_opening.py              # 模态一：离线极值路线重放引擎（含 8 大防御护盾）
    ├── hy_planner.py              # 模态二：后期动态规划器包装入口
    ├── hy_eplanner.py             # 模态三：早期特异分流规划器包装入口
    ├── pd_modules_late/           # 后期在线规划器纯净源码（14 个核心生产模块，Shawn404 原创重构）
    │   ├── pd_state.py            # 状态建模、网格图表示、作物牲畜参数
    │   ├── pd_tasks.py            # 任务原语生成车间 (PLANT, WATER, FEED, DIG 等)
    │   ├── pd_exec.py             # Morning Kit 早间工具箱与 LNS 防撞车路径调度
    │   ├── pd_market.py           # 非线性价格拟合、Flat/Steep 分级与 Step % 4 == 1 套利
    │   ├── pd_plan.py             # DSM 视窗加性回归规则库 (R1-R8) 宏观经营规划器
    │   ├── pd_replant.py          # 农田轮作与老化作物铲除
    │   ├── pd_supply.py           # 仓库饲料储备与防牲畜叛逃系统
    │   ├── fp_rival.py            # 泊松速率对手销售模型与朴素贝叶斯分类器
    │   ├── fp_sched.py            # 零和博弈惩罚调度器 (J = Revenue - λ RivalRevenue)
    │   ├── fp_sched_hook.py       # 对手出单提前抢跑拦截 Hook
    │   └── ownfc_lags.py          # 自身产出时序滞后衰减表
    └── pd_modules_early/          # 早期特异分流对应的一套独立模块
```

> 💡 **想要深入研读代码？**  
> 强烈推荐打开本仓库根目录下的 [**`CODEBASE_GUIDE.md`**](CODEBASE_GUIDE.md)。这份文档没有晦涩的术语，而是把所有模块通俗比喻为“农场公司的各个部门”，带你轻松读懂每一个 Python 文件的具体职责！

---

## ⚡ 快速上手

### 1. 直接提交至 Kaggle
根目录的 `main.py` 是自包含的独立提交包，已内嵌解压与调度引擎。可直接上传至 Kaggle Kaggriculture 比赛页面进行评测。

### 2. 本地模拟对战与回放可视化

```bash
# 1. 安装可选本地环境
pip install -r requirements.txt

# 2. 运行本地对战并生成可视化 HTML 回放
python3 -c "
from kaggle_environments import make

env = make('kaggriculture', debug=True)
env.run(['main.py', 'main.py'])

with open('match_replay.html', 'w') as f:
    f.write(env.render(mode='html'))
print('对战完成，回放已保存至 match_replay.html')
"
```

---

## 💡 技术规格与性能指标

- **编程语言**：Python 3.10+
- **第三方库依赖**：**纯标准库（0 外部重度依赖）**，仅使用 `json`, `time`, `zlib`, `base64`, `hashlib`, `collections`
- **运行内存**：live 运行时峰值内存 $< 50\text{ MB}$
- **单步决策时延**：平均 $< 1.5\text{ ms}$（远低于 Kaggle 官方每步 1000ms 的硬性限制）
- **算力需求**：纯 CPU 执行，**无需任何 GPU**

---

## 📜 许可证与致谢

- 本项目遵循 [Apache-2.0 License](LICENSE) 开源协议。
- 模块核心作者：**Shawn404**（DSM 规划器、Morning Kit 执行器、泊松博弈调度器）。
- 基础架构承袭并致敬 Kaggle 开源社区的杰出贡献者：
  `haideptry` ("The 2965 Master Hybrid Engine"), `Thomas Tschinkel`, `yhay81`, `destbreso`, `aurax7`, `tetsutani`, `prvsiyan`, `Dmitrii Gluzdov`, `Ahmed Berat Ozer` 及更多社区拓荒者。

---

<div align="center">
<b>⭐ 如果这套架构对你的游戏 AI 或算法设计有所启发，欢迎给仓库点个 Star！ ⭐</b>
</div>
