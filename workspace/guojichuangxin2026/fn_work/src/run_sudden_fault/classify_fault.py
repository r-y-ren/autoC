"""轻量分类器判故障来源（电机/电调/链路瞬断/未知）（run_sudden_fault 块）。"""
from __future__ import annotations


def classify_fault(features, classifier):
    """features: 确认窗统计 {"ch_mean": {...}, "ch_max": {...}}；classifier 可 None→规则判型。"""
    if classifier is not None and hasattr(classifier, "predict"):
        label = classifier.predict([features["ch_mean"]])[0]
        return {"fault": label, "confidence": 0.8, "path": "model"}
    m, mx = features["ch_mean"], features.get("ch_max", {})
    link = max(m.get("telem_loss", 0.0) or 0.0,
               0.75 * (mx.get("telem_loss", 0.0) or 0.0))  # 爬坡确认窗：峰值口径
    att = max(m.get("att_track", 0.0) or 0.0, m.get("motor_consistency", 0.0) or 0.0,
              m.get("pos_vel_innov", 0.0) or 0.0)
    if link > 0.6 and link >= att:
        return {"fault": "链路瞬断", "confidence": min(0.5 + 0.4 * link, 0.95), "path": "rules"}
    if att > 0.25:
        if (m.get("motor_consistency") or 0.0) > (m.get("att_track") or 0.0):
            return {"fault": "电机异常", "confidence": min(0.5 + 0.4 * att, 0.95), "path": "rules"}
        return {"fault": "电调异常" if (m.get("att_track") or 0) > 1.0 else "电机异常",
                "confidence": min(0.4 + 0.4 * att, 0.9), "path": "rules"}
    return {"fault": "未知", "confidence": 0.3, "path": "rules"}
