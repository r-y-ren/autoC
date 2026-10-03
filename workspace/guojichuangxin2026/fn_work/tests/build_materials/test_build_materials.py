"""build_materials 总入口单测（上游覆盖）。"""
from __future__ import annotations

import json


def test_end_to_end_from_runs(tmp_path):
    from build_materials.build_materials import build_materials
    for i in range(2):
        rd = tmp_path / f"run{i}"; rd.mkdir()
        with open(rd / "metrics.jsonl", "w", encoding="utf-8") as fh:
            for k, v in {"lowbat_headwind/conformal_coverage": 0.91,
                         "lowbat_headwind/lead_p10_s": 5.6 + i * 0.1,
                         "lowbat_headwind/lead_median_s": 7.1,
                         "lowbat_headwind/lead_hit_rate": 0.8,
                         "link_degrade/detected": 1, "link_degrade/false_alarms": 0,
                         "motor_fail/confirm_p90_s": 0.18,
                         "motor_fail/type_accuracy": 1.0,
                         "sdr_check/pass": 1}.items():
                fh.write(json.dumps({"key": k, "value": v, "ts": "t"}) + "\n")
    out = build_materials([str(tmp_path / "run0"), str(tmp_path / "run1")],
                          {"work_dir": str(tmp_path / "mat")})
    assert out["n_runs"] == 2 and len(out["compiled"]) == 2
