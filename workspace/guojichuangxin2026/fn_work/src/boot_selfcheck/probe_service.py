"""平台服务 GET 探活（可达性+延迟）（boot_selfcheck 块）。"""
from __future__ import annotations


def probe_service(base_url: str, timeout_s: float = 2.0, retries: int = 3) -> dict:
    """探测 /api/state 与 /api/runs；返回 {reachable, latency_ms, endpoints}。"""
    import time
    import urllib.error
    import urllib.request

    endpoints, ok_all, lat = {}, True, 0.0
    for ep in ("/api/state", "/api/runs"):
        got, err = False, None
        for _ in range(retries):
            t0 = time.monotonic()
            try:
                with urllib.request.urlopen(base_url + ep, timeout=timeout_s) as r:
                    r.read(64)
                got, lat = True, (time.monotonic() - t0) * 1000
                break
            except (urllib.error.URLError, OSError, TimeoutError) as exc:
                err = str(exc)
                time.sleep(0.2)
        endpoints[ep] = {"ok": got, "error": err}
        ok_all = ok_all and got
    return {"reachable": ok_all, "latency_ms": round(lat, 1), "endpoints": endpoints}
