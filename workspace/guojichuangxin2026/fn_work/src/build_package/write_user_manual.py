"""零术语用户手册四节（安装/演示/操作/排障）（build_package 块）。"""
from __future__ import annotations

_TEMPLATE = """# 安航云盾 使用手册（零术语版）

## 一、安装
1. 电脑需装 Python 3.11 或更新（Linux/Mac/Win 均可，演示推荐 Linux）。
2. 把安装包（.whl 文件）放到任意目录，执行：`pip install 安航云盾-*.whl`
3. 装好后终端输入 `ahyd-demo` 能看到服务启动即成功。

## 二、一键演示
1. 执行 `ahyd-demo`（或包内 demo.sh）。
2. 浏览器打开 http://127.0.0.1:8000 —— 不需要联网。
3. 看到"演示控制台"页面即成功。

## 三、控制台操作
1. 左上选危险场景（慢危险=电量+逆风 / 快危险=电机故障 / 链路=频谱被挤占）。
2. 点"起飞"——地图上飞机沿航线飞。
3. 飞行中点"注入故障"、拖强度滑杆——看右侧风险等级和处置建议变化。
4. 点"回放最近会话"回看全程。

## 四、常见故障排查
| 现象 | 处理 |
|---|---|
| 打不开页面 | 等服务打印 started 再刷新；检查端口没被占用 |
| 点起飞没反应 | 看 /api/session/start 返回的错误文字；重启 ahyd-demo |
| 频谱图不动 | 正常——频谱设备未接入时用录好的数据，画面来源会标注 replay |
| 数字和材料不一致 | 一切数字以 fn_docs/results 下的运行记录为准 |
"""


def write_user_manual(out_path: str) -> str:
    from pathlib import Path
    p = Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(_TEMPLATE, encoding="utf-8")
    return str(p)
