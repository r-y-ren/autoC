#!/usr/bin/env bash
# 一键启动（R7 验收）：冒烟自检→起平台服务，浏览器开 http://127.0.0.1:8000
set -euo pipefail
cd "$(dirname "$0")"
PY=.venv/bin/python          # venv 优先：系统 python 缺 uvicorn 等依赖
[ -x "$PY" ] || PY=python3
"$PY" smoke_boot.py
exec "$PY" server.py "$@"
