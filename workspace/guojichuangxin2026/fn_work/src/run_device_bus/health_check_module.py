"""模块健康监测→失健降级切换/恢复切回指令（run_device_bus 块）。"""
from __future__ import annotations


def health_check_module(module_handle, thresholds: dict | None = None):
    """module_handle: 总线侧统计 {fps, errors, latency_ms}（由帧路由累计）。"""
    thr = {"fps_min": 1.0, "errors_max": 5, "latency_ms_max": 2000.0, **(thresholds or {})}
    if not module_handle:
        return {"healthy": False, "action": "degrade", "why": "无统计"}
    fps = float(module_handle.get("fps", 0.0))
    errs = int(module_handle.get("errors", 0))
    lat = float(module_handle.get("latency_ms", 0.0))
    why = []
    if fps < thr["fps_min"]:
        why.append(f"帧率 {fps:.2f} < {thr['fps_min']}")
    if errs > thr["errors_max"]:
        why.append(f"错误 {errs} > {thr['errors_max']}")
    if lat > thr["latency_ms_max"]:
        why.append(f"延迟 {lat:.0f}ms")
    healthy = not why
    return {"healthy": healthy, "action": "restore" if healthy else "degrade",
            "why": "；".join(why) or "正常"}
