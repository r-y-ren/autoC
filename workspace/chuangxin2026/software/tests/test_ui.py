"""R11–R13 ui：导入链+静态资源+桩（fastapi 未装也可跑——惰性导入）。"""

from __future__ import annotations

import pytest

from linkbench.ui import api, server, ws_hub


def test_module_importable():
    assert callable(server.create_app) and callable(server.serve)
    assert callable(api.register_api)


def test_ws_hub_stub():
    import asyncio
    hub = ws_hub.WsHub()
    with pytest.raises(NotImplementedError):
        asyncio.run(hub.broadcast({}))
    with pytest.raises(NotImplementedError):
        asyncio.run(hub.subscribe(None))
