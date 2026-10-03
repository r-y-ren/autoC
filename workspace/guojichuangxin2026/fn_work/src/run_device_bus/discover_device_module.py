"""枚举装载在场设备模块→注册表（缺席记 None 不阻塞）（run_device_bus 块）。"""
from __future__ import annotations

_PROBES = {
    "usrp": lambda cfg: _probe_usrp(cfg),
    "ssh": lambda cfg: _probe_ssh(cfg),
}


def _probe_usrp(cfg):
    try:
        import uhd  # 设备模块依赖：缺席=模块不可用，非总线错误
    except ImportError:
        return None
    try:
        usrp = uhd.usrp.MultiUSRP(cfg.get("args", ""))
        return {"name": cfg.get("name", "sdr"), "type": "usrp", "handle": usrp,
                "info": str(usrp.get_usrp_rx_info().get("mboard", ""))}
    except Exception:
        return None


def _probe_ssh(cfg):
    import socket
    host, port = cfg.get("host", ""), int(cfg.get("port", 22))
    if not host:
        return None
    try:
        with socket.create_connection((host, port), timeout=float(cfg.get("timeout", 1.0))):
            return {"name": cfg.get("name", "jetson"), "type": "ssh",
                    "handle": (host, port), "info": f"tcp可达 {host}:{port}"}
    except OSError:
        return None


def discover_device_module(module_configs: list, timeout: float = 2.0):
    """module_configs: [{name, type, ...探测参数}]→{name: 注册项|None}。探测异常按缺席处理。"""
    registry = {}
    for cfg in module_configs or []:
        name = cfg.get("name", "?")
        probe = _PROBES.get(cfg.get("type"))
        try:
            hit = probe(cfg) if probe else None
        except Exception:
            hit = None
        registry[name] = {"module": hit, "configured": True,
                          "present": hit is not None}
    return registry
