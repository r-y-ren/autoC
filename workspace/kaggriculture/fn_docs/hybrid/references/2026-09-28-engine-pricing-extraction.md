# 引擎定价公式与结算语义抽取（2026-09-28）

来源：kaggle-environments 官方包 `kaggle_environments/envs/kaggriculture/kaggriculture.py`
（1.32.7 本地安装件；GitHub 官方仓库同源，Apache-2.0）。抓取日期 2026-09-28。A 级（源码直读）。

## 一、市场定价公式（源码 L28-96, L192-205）

`price(inv) = max(1, round(base ± amp × shape(|inv − I0|, T)))`
- I0=10000（全品折点）、PRICE_FLOOR=1；inv<I0 走 below 支（稀缺溢价 +）、inv≥I0 走 above 支（过剩折价 −）；
- `amp = target × base / shape(func, T, T)`（幅度按 T 处形状值归一）；
- 形状函数：linear/sqrt/log/sq（平方）/hinge（过 T 折点前线性 x/T、之后陡升）。

逐品参数表（base, T, below_func→target, above_func→target）：

| 品 | base | T | 稀缺支 | 过剩支 |
|---|---|---|---|---|
| WHEAT | 25 | 400 | sqrt→0.80 | log→0.20 |
| CARROT | 35 | 450 | hinge→1.00 | sqrt→0.70 |
| TOMATO | 60 | 200 | hinge→0.40 | sqrt→0.60 |
| STRAWBERRY | 120 | 100 | sqrt→0.70 | linear→1.60 |
| MELON | 250 | 300 | log→0.20 | sq→3.60 |
| EGG | 50 | 332 | hinge→0.40 | log→0.20 |
| MILK | 160 | 122 | sqrt→0.60 | linear→1.60 |
| WOOL | 200 | 105 | log→0.20 | sq→3.20 |
| FERTILIZER | 100 | 200 | linear→0.40 | linear→0.40 |

**结构性要点**：WOOL/MILK/STRAWBERRY 的 T 最小（100-122）=对库存最敏感；
WOOL/MELON 过剩支是平方崩塌（sq 3.2-3.6）——**牲畜品抛售自伤是二次方级**，
"少而大+择时"的收益来源就是这条曲线；这也定量解释 d21-28 变现窗差距。

## 二、已证结算语义（同文件；详见 2026-09-28-execution-faces-scan.md 一-1~5）

同槽 lockstep 1:1 交错 / 逐单位按共享库存重报价（BUY_PRODUCT 按 inv−1 使同拍对倒净零）/
单列表 10 单硬截断 / 死单占槽后移 / $1 地板成交不加库存 / abort 全废剩余单位。

## 三、可利用点（每条=确定性，源码直读）

1. **精确价格预测**：给定库存轨迹可精确算出每单位成交价与价格漂移——订单簿回放
   择优可完全精确化（不再需要近似衰减模型）。
2. **卖量最优停止**：曲线已知→自抛售的边际损失可解析求解（尤其 WOOL/MILK 平方支），
   "每拍该卖多少"是可计算的优化问题。
3. **结算序套利**：同拍动作次序（收成/买单/卖单结算序）决定单位进库存的时点——
   精确排程有确定收益面。
4. **对倒零和确认**：BUY_PRODUCT(inv−1) 语义=同拍买卖对倒净零，tape 的对倒设计
   是规则级安全的（不动它）。
