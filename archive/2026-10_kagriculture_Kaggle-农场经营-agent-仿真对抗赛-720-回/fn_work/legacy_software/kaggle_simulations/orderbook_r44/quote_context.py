# 市场报价上下文（共享；调用方: detect_dayhigh / gate_added_sells / select_advanceable[R28]）
# stdlib-only 自含；构建时被文本拼接进提交包（本文件源码在层源码之前、同一命名空间）。

# 引擎 base 表（口径=fn_docs/hybrid/references/2026-09-28-engine-pricing-extraction.md
# 逐品参数表 base 列；FERT100 即品名 FERTILIZER 的 base=100）。
_BASE_TABLE = {
    "WHEAT": 25.0,
    "CARROT": 35.0,
    "TOMATO": 60.0,
    "STRAWBERRY": 120.0,
    "MELON": 250.0,
    "EGG": 50.0,
    "MILK": 160.0,
    "WOOL": 200.0,
    "FERTILIZER": 100.0,
}


def quote_context(observations, tracker=None):
    """day=step//24；逐品当日迄今最高价跟踪（换日复位）；quote_of/base_of（引擎 base 表）。输入: observation 序列/当前 obs+跟踪器 / 输出: {day, day_highs, quote, base} / 错误: 缺字段→None

    语义固化（R27 判新高的唯一口径）：
    - observations：单个 observation（dict）或其序列（list/tuple），按步序处理；
    - tracker：跨调用持久的可变跟踪器 {"day": int|None, "day_highs": {item: float}}，
      None=一次用临时跟踪器；缺键自动补；
    - day_highs=**判新高基线**——截至上一步的当日迄今最高（换日清空）；当前 obs 的
      报价在返回快照之后才 fold 进 tracker（严格新高=quote>day_highs，若基线含当前
      报价则永无新高）；当日/跟踪首见无基线 → 该品无基线条目（调用方按不触发处理）；
    - quote=当前 obs 公开市场报价 {item: float}（非数值价目跳过）；
    - base=引擎 base 全表快照（常量，逐调用复制返回）；
    - 错误：任一 obs 非 dict/缺 step/缺 market/缺 prices/step 非数值 → None
      （先全量解析后才动跟踪器，报错零副作用）。
    """
    if isinstance(observations, dict):
        obs_seq = [observations]
    elif isinstance(observations, (list, tuple)):
        obs_seq = list(observations)
    else:
        return None
    if not obs_seq:
        return None

    # 全量解析（缺字段→None，解析期不动跟踪器）
    parsed = []
    for obs in obs_seq:
        if not isinstance(obs, dict):
            return None
        step = obs.get("step")
        if isinstance(step, bool) or not isinstance(step, (int, float)):
            return None
        if isinstance(step, float):
            if not step.is_integer():
                return None
            step = int(step)
        market = obs.get("market")
        if not isinstance(market, dict):
            return None
        prices = market.get("prices")
        if not isinstance(prices, dict):
            return None
        quotes = {}
        for item, price in list(prices.items()):
            if isinstance(price, bool) or not isinstance(price, (int, float)):
                continue  # 非数值价目跳过（不属"缺字段"）
            quotes[item] = float(price)
        parsed.append((step, step // 24, quotes))

    if not isinstance(tracker, dict):
        tracker = {"day": None, "day_highs": {}}
    highs = tracker.get("day_highs")
    if not isinstance(highs, dict):
        highs = {}
        tracker["day_highs"] = highs

    # 除末步外全部 fold；末步先取基线快照再 fold（换日复位先于两者）
    for step, day, quotes in parsed[:-1]:
        if tracker.get("day") != day:
            tracker["day"] = day
            highs.clear()  # 换日复位
        for item, price in quotes.items():
            prev = highs.get(item)
            if prev is None or price > prev:
                highs[item] = price
    step, day, quotes = parsed[-1]
    if tracker.get("day") != day:
        tracker["day"] = day
        highs.clear()  # 换日复位
    baseline = dict(highs)  # 判新高基线=截至上一步（不含当前 obs 报价）
    for item, price in quotes.items():
        prev = highs.get(item)
        if prev is None or price > prev:
            highs[item] = price
    return {"day": day, "day_highs": baseline, "quote": quotes,
            "base": dict(_BASE_TABLE)}
