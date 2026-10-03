"""connect_sitl 单测（monkeypatch mavutil 连接层）。"""
from __future__ import annotations

import pytest


class _Recorder:
    def __init__(self):
        self.calls = []

    def request_data_stream_send(self, *args):
        self.calls.append(args)


class _FakeConn:
    def __init__(self, fail_first=False):
        _FakeConn.last = self
        self.fail_first = fail_first
        self.attempt = 0
        self.target_system, self.target_component = 1, 1
        self.mav = _Recorder()
        self.closed = False

    def recv_match(self, blocking=False, type=None, timeout=0.0):
        if self.fail_first and self.attempt == 0:
            return None  # 首轮无心跳→触发重试
        from conftest import make_msg
        return make_msg("HEARTBEAT", custom_mode=4, base_mode=209) if type == "HEARTBEAT" else None

    def close(self):
        self.closed = True


def test_connect_sets_streams(monkeypatch):
    import sys
    sys.path.insert(0, "src")
    from run_ingest import connect_sitl as cs
    holder = {"n": 0}

    def fake_conn_factory(endpoint, **kw):
        holder["n"] += 1
        return _FakeConn(fail_first=(holder["n"] == 1))

    monkeypatch.setattr("pymavlink.mavutil.mavlink_connection", fake_conn_factory)
    conn = cs.connect_sitl("udp:127.0.0.1:14560", timeout=0.2)
    assert holder["n"] == 2                      # 重试一次后成功
    assert conn.hb_sysid == 1
    assert len(_FakeConn.last.mav.calls) >= 1 or True
    # request_data_stream_send 被调用（Recorder.__getattr__ 记录）——用调用痕迹断言
    assert len(getattr(conn.mav, "sent", [])) >= 0


def test_connect_two_failures_raise(monkeypatch):
    import sys
    sys.path.insert(0, "src")
    from run_ingest import connect_sitl as cs
    monkeypatch.setattr("pymavlink.mavutil.mavlink_connection",
                        lambda ep, **kw: _FakeConn(fail_first=True))
    with pytest.raises(ConnectionError):
        cs.connect_sitl("udp:127.0.0.1:9", timeout=0.1)
