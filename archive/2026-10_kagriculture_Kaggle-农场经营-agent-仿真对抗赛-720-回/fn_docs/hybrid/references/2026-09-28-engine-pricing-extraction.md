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

## 四、生产/消耗/成本全表（2026-09-28 补，源码 L11-22, L99-108, L728-755）

**作物**（seed 价, 首产日, 最大日, 间隔, 单次量/持有, ongoing）：
- WHEAT（10, d2, d4, —, 6, 一次性）；CARROT（20, d2, d3, —, 4, 一次性）；
- TOMATO（50, d8, —, 1 天, 4, 续产）；STRAWBERRY（100, d10, —, 2 天, 4, 续产）；
- MELON（80, d10-12, —, 6, 一次性）。
**牲畜**（cost, 建筑型, 首产日, 间隔, 持有上限, 产品）：
- GOOSE（300, COOP, d4, 1 天, 4, EGG）；COW（400, PASTURE, d8, 2 天, 6, MILK）；
- SHEEP（500, PASTURE, d6, 3 天, 6, WOOL）。
**雇工成本**：当日第 n 次雇=1×fib(n)（1,1,2,3,5,8,13…）。
**城镇排水（确定性价格支撑）**：
- 每 4 步：**每家已解锁商店各排其每个产品 1 件**（单品店 ×2：YARN_STORE 排 2 WOOL、
  PET_CAFE 排 2 CARROT；同名多实例独立排水）；
- 每 24 步：城镇中心排全品各 1（除 FERTILIZER）；排完即刷新全品价格。
**SHOPS 表**：BAKERY(EGG,WHEAT)/PIZZA(MILK,TOMATO,WHEAT)/BRUNCH(EGG,WHEAT,STRAW)
/YARN(WOOL)/ICE_CREAM(STRAW,MILK,WHEAT)/PET_CAFE(CARROT)/SMOOTHIE(STRAW,MILK)
/FARMERS_MARKET(WHEAT,CARROT,TOMATO,STRAW)；商店有放回抽签、实例上限 8。

**合成要点（"卖多少"的解析口径）**：排水表+定价曲线+双方卖单 → **价格轨迹完全可
预测**；最优卖速≈"按城镇吸收速率出清"（尤其 WOOL/MILK 这类 T 小、过剩支陡的品，
库存压在 I0=10000 下方=吃稀缺溢价，冲过折点=平方/线性崩价）。MILK 过剩支 linear
vs WOOL 平方 —— 与行为面"重牛轻羊"互证：**牛线可规模化的曲线原因**。
