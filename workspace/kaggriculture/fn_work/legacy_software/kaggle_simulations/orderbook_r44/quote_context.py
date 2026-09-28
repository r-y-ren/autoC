# 市场报价上下文（共享；调用方: detect_dayhigh / gate_added_sells / select_advanceable[R28]）
def quote_context(observations, tracker=None):
    """day=step//24；逐品当日迄今最高价跟踪（换日复位）；quote_of/base_of（引擎 base 表）。输入: observation 序列/当前 obs+跟踪器 / 输出: {day, day_highs, quote, base} / 错误: 缺字段→None"""
    raise NotImplementedError("unimplemented:fn:quote_context")
