"""classify_fault 单测。"""
from __future__ import annotations


def test_rules_link_vs_motor_vs_unknown():
    from run_sudden_fault.classify_fault import classify_fault
    link = classify_fault({"ch_mean": {"telem_loss": 1.2, "att_track": 0.1,
                                       "motor_consistency": 0.0, "pos_vel_innov": 0.1}}, None)
    motor = classify_fault({"ch_mean": {"telem_loss": 0.1, "att_track": 0.2,
                                        "motor_consistency": 0.9, "pos_vel_innov": 0.1}}, None)
    unknown = classify_fault({"ch_mean": {"telem_loss": 0.0, "att_track": 0.05,
                                          "motor_consistency": 0.0, "pos_vel_innov": 0.02}}, None)
    assert link["fault"] == "链路瞬断" and link["path"] == "rules"
    assert motor["fault"] == "电机异常"
    assert unknown["fault"] == "未知"


def test_model_path():
    from run_sudden_fault.classify_fault import classify_fault
    class Clf:
        def predict(self, rows):
            return ["电调异常"]
    r = classify_fault({"ch_mean": {"x": 1}}, Clf())
    assert r["fault"] == "电调异常" and r["path"] == "model"
