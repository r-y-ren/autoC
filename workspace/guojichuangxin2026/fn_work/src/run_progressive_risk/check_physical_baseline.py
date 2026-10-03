"""四类余量持续收窄判定（独立降级判据）（run_progressive_risk 块）。"""
from __future__ import annotations


def check_physical_baseline(margins, thresholds: dict) -> dict:
    """margins: 帧余量序列（含 norm）；逐类判"低于阈值且持续 persist_s"。

    输出四类 {triggered, evidence_span_s, last_norm}；无模型时它独立产保守告警。
    """
    persist = float(thresholds.get("baseline_persist_s", 5.0))
    names = ("energy", "nav", "link", "control")
    out = {}
    for name in names:
        thr = float(thresholds.get(name, 0.4))
        seq = [(m.get("t"), (m.get(name) or {}).get("norm"))
               for m in margins
               if (m.get(name) or {}).get("norm") == (m.get(name) or {}).get("norm")]
        trig, span, last = False, 0.0, None
        run = []
        for t, v in seq:
            last = v
            if v is not None and v < thr:
                run.append(t)
                if run and t - run[0] >= persist:
                    trig, span = True, t - run[0]
            else:
                run = []
        out[name] = {"triggered": trig, "evidence_span_s": span, "last_norm": last}
    return out
