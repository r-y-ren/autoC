"""export_metrics_table 单测。"""
from __future__ import annotations

import json

import pytest

from build_materials.export_metrics_table import MaterialError, export_metrics_table


def _run(tmp, rows):
    d = tmp / f"r{len(list(tmp.iterdir()))}"
    d.mkdir()
    with open(d / "metrics.jsonl", "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps({"key": r[0], "value": r[1], "ts": "t"}) + "\n")
    return str(d)


def test_aggregate_and_conflict(tmp_path):
    runs = [_run(tmp_path, [("sc/lead_p10_s", 5.2), ("sc/frames", 240)]),
            _run(tmp_path, [("sc/lead_p10_s", 4.9), ("sc/frames", 238)])]
    t = export_metrics_table(runs)
    assert t["n_runs"] == 2 and "sc/lead_p10_s" in t["keys"]
    assert not t["conflicts_final"]                      # 非终值键多值合法
    with pytest.raises(MaterialError):
        export_metrics_table([str(tmp_path / "nope")])   # 缺分片阻断
    bad = tmp_path / "bad"; bad.mkdir()
    (bad / "metrics.jsonl").write_text('{"value": 1}\n', encoding="utf-8")
    with pytest.raises(MaterialError, match="无 key"):
        export_metrics_table([str(bad)])


def test_r25_derived_aggregates(tmp_path):
    """R25：lead_s 单值列派生 P10/中位数/达标率（汇总口径供模板）。"""
    runs = [_run(tmp_path, [("sc/lead_s", 6.0)]), _run(tmp_path, [("sc/lead_s", 4.0)])]
    t = export_metrics_table(runs)
    assert t["by_key"]["sc/lead_p10_s"][0]["value"] == 4.2   # M8：P10 线性插值单口径（4.2 非取整 4.0）
    assert t["by_key"]["sc/lead_median_s"][0]["value"] == 5.0
    assert t["by_key"]["sc/lead_hit_rate"][0]["value"] == 0.5      # 6.0 达标/4.0 不达标
    assert t["by_key"]["sc/lead_p10_s"][0]["run"] == "(aggregate)"
