# -*- coding: utf-8 -*-
# 【中文】R8 前置探针：驱动一局官方真引擎（kaggle_environments.make
# "kaggriculture"，vendored wheel 1.32.7 先例），dump 喂给 agent 的 obs
# 键结构，确认对手资金（farms[1-seat].money）可见性。临时件，不入 manifest。
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HYB = os.path.dirname(HERE)
KSIM = os.path.dirname(HYB)
SOFTWARE = os.path.dirname(KSIM)
for _p in (SOFTWARE,):
    if _p not in sys.path:
        sys.path.insert(0, _p)
sys.dont_write_bytecode = True

CAPTURE = {"n": 0}


def probe_agent(obs):
    # obs 为 kaggle Struct（属性视图）；转 dict 检查键
    d = obs.__dict__ if hasattr(obs, "__dict__") else dict(obs)
    if CAPTURE["n"] < 40:   # 逐步采样前 40 帧足够判键结构
        try:
            keys = sorted(d.keys())
            farms = d.get("farms")
            farm_info = None
            if isinstance(farms, (list, tuple)):
                farm_info = []
                for i, f in enumerate(farms):
                    if isinstance(f, dict):
                        farm_info.append({"seat": i, "keys": sorted(f.keys()),
                                          "money": f.get("money", "<ABSENT>")})
                    else:
                        farm_info.append({"seat": i, "type": type(f).__name__,
                                          "keys": sorted(getattr(f, "__dict__", {}).keys()),
                                          "money": getattr(f, "money", "<ABSENT>")})
            rec = {"frame": CAPTURE["n"], "obs_keys": keys,
                   "farm_info": farm_info,
                   "player": d.get("player"), "step": d.get("step"),
                   "town_keys": sorted((d.get("town") or {}).__dict__.keys())
                   if hasattr(d.get("town") or {}, "__dict__")
                   else sorted((d.get("town") or {}).keys()),
                   "market_keys": sorted((d.get("market") or {}).keys()),
                   "private_keys": sorted((d.get("private") or {}).keys())}
            print(json.dumps(rec, ensure_ascii=False, default=str))
        except Exception as e:  # noqa: BLE001
            print("PROBE_ERR", repr(e))
        CAPTURE["n"] += 1
    return {"market": []}


def main():
    from kaggle_environments import make
    env = make("kaggriculture",
               configuration={"episodeSteps": 720, "seed": 20260922,
                              "actTimeout": 60},
               debug=True)
    env.run([probe_agent, probe_agent])
    print("FINAL_REWARDS", [float(s["reward"]) for s in env.steps[-1]])


if __name__ == "__main__":
    main()
