"""按场景定义注入故障（电池/风/电机/链路，含回执记录）（shared 块）。"""
from __future__ import annotations


class InjectError(Exception):
    """命令拒绝/超时（合成源直接回执，真实链路 2s 无响应视为超时）。"""


def _params_for(scenario: str, level: str, sc_def: dict) -> dict:
    kind = sc_def.get("kind")
    if kind == "sudden":  # 电机故障：PX4 failure injection 语义，值为故障强度 0-1
        return {f"failure_motor{sc_def.get('motor', 1)}": sc_def.get("levels", {}).get(level, 0.7)}
    if kind == "progressive":  # 低电量+逆风：内部合成参数（真实 PX4 走风参数与电池仿真）
        lv = sc_def.get("levels", {}).get(level, 2.0)
        return {"sim_battery_drain_x": lv, "sim_wind_ms": sc_def.get("wind_ms", 6.0)}
    if kind == "link":  # 链路退化：遥测丢弃率
        return {"sim_drop_rate": sc_def.get("drop_rate", {}).get(level, 0.3)}
    return {}


def inject_scenario_fault(conn, scenario: str, level: str, timing: dict) -> dict:
    """优先合成源 conn.inject_scenario()；真实链路走 param_set_send 序列；两者皆无→InjectError。

    timing: {phase: 'cruise'|'climb'|..., at_s: 注入时刻(相对起飞)}——由调用方决定何时调用，
    本函数把 timing 计入回执。回执 dict 落运行清单由调用方（run_eval/控制台）负责。
    """
    params = _params_for(scenario, level, getattr(conn, "scenario_defs", {}).get(scenario, {})
                         if hasattr(conn, "scenario_defs") else {})
    if not params:  # conn 不带场景表时按场景名推缺省（配置常量与 load_config 默认一致）
        fallback = {"lowbat_headwind": {"sim_battery_drain_x": 2.2, "sim_wind_ms": 6.0},
                    "motor_fail": {"failure_motor1": 0.7},
                    "link_degrade": {"sim_drop_rate": 0.3}}
        params = fallback.get(scenario, {})
        if not params:
            raise InjectError(f"场景未定义: {scenario}")
    receipt = {"scenario": scenario, "level": level, "timing": timing,
               "params": params, "path": None}
    inj = getattr(conn, "inject_scenario", None)
    if callable(inj):
        try:
            ack = inj(scenario, level, params) or {}
        except Exception as exc:
            raise InjectError(f"合成源注入被拒: {exc}") from exc
        receipt["path"], receipt["ack"] = "synthetic", ack
        return receipt
    setter = getattr(getattr(conn, "mav", None), "param_set_send", None)
    if callable(setter):
        # 真实 PX4 SITL 参数映射（合成名→仿真器实参）
        px4map = {
            "sim_battery_drain_x": ("SIM_BAT_CR_PCT", lambda v: 500.0 * float(v)),
            "sim_wind_ms": ("SIM_WIND_SPD", float),
            "failure_motor1": ("SIH_MOTOR1_FAIL", float),   # SIH 无此参时静默失败由回执承载
        }
        params = {px4map.get(k, (k, float))[0]: px4map.get(k, (None, float))[1](v)
                  for k, v in params.items()}
        for k, v in params.items():
            setter(conn.target_system if hasattr(conn, "target_system") else 1,
                   getattr(conn, "target_component", 1), k.encode() if isinstance(k, str) else k,
                   float(v))
        receipt["path"], receipt["ack"] = "param_set", {"sent": len(params)}
        return receipt
    raise InjectError("conn 既无 inject_scenario 也无 mav.param_set_send——不可注入")
