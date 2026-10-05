"""严判入口(layer-change-protocol 判决口径):尺子健康检查→四线 30 局双席判决电池。

用法: cd fn_work && .venv/bin/python entries/strict_judge.py [weights.json] [标签]
受测体=SIL 权重装载的策略网;锚={在梯版 submission_v9, v5 引擎原序, teacher eval_es_v1};
自镜像 n_mirror=30,每锚 n_anchor=30(双席),bo=3。
fna-013:判决电池前必跑尺子健康检查(单局决策数>20+真赢一局),不过即中止。
"""
import json
import os
import sys

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, _ROOT)
sys.path.insert(0, os.path.join(_ROOT, "src"))
sys.path.insert(0, os.path.join(_ROOT, "remote"))
os.chdir(_ROOT)  # 权重/references 相对路径解析与远程 ~/ptcg-train 布局一致(勿信调用方 cwd)

from kaggle_environments.envs.cabt import cabt

from learn.bc_policy import MLP
from learn.bc_policy_v3 import build_features
from learn.eval_agent import make_agent as make_eval_agent
from shared.load_agent_callable import load_agent_callable
from shared.play_local_match import play_local_match
from src.run_judge_pool.run_judge_pool import run_judge_pool
import train_sil as ts


def load_policy(path):
    w = json.load(open(path))
    m = MLP(h=96, seed=0, d=w["d"])
    m.W1 = __import__("numpy").array(w["W1"])
    m.b1 = __import__("numpy").array(w["b1"])
    m.W2 = __import__("numpy").array(w["W2"])
    m.b2 = __import__("numpy").array(w["b2"])
    ts._G["build"] = build_features
    ts._G["deck"] = list(cabt.deck)
    return ts.make_policy_agent(m, None, temperature=0.05, seat="judge")


def ruler_health(agent, deck):
    """fna-013:单局决策数>20+真赢一局,双过才许开判决电池。"""
    max_dec = 0
    wins = 0
    for opp_name, opp in (("random", cabt.random_agent), ("first", cabt.first_agent)):
        for i in range(2):
            r = play_local_match(agent, opp, deck, deck, seed=5000 + i, config={"bo": 3})
            dec = len(r.get("steps") or [])
            max_dec = max(max_dec, dec)
            wins += (r["rewards"][0] or -1) > 0
    ok = max_dec > 20 and wins >= 1
    print(f"[ruler] max_decisions={max_dec} wins={wins}/4 -> {'PASS' if ok else 'FAIL'}")
    return ok


def main():
    weights = sys.argv[1] if len(sys.argv) > 1 else "weights/sil_best_new.json"
    label = sys.argv[2] if len(sys.argv) > 2 else "sil_best_new"
    deck = list(cabt.deck)

    agent = load_policy(weights)
    if not ruler_health(agent, deck):
        print("RULER UNHEALTHY — 判决电池中止(先修尺子)")
        sys.exit(2)

    anchors = {
        "ladder": load_agent_callable("submission_v9", "agent"),
        "v5": ts._base(deck),
        "teacher": make_eval_agent(weights=json.load(open("weights/eval_es_v1.json"))),
    }
    rep = run_judge_pool({
        "agent": agent, "n_mirror": 30, "n_anchor": 30,
        "anchors": anchors, "deck": deck, "seed0": 7000, "bo": 3,
    })

    mir = rep["self_mirror_h2h"]
    vs = {k: v["loss"] / v["n"] for k, v in rep["members"].items() if k != "self"}
    gate = vs.get("ladder", 0) >= 0.60 and vs.get("v5", 0) >= 0.65 and 0.35 <= mir <= 0.65
    print(json.dumps({
        "label": label, "weights": weights,
        "self_mirror": mir, "vs_ladder": round(vs.get("ladder", 0), 4),
        "vs_v5": round(vs.get("v5", 0), 4), "vs_teacher": round(vs.get("teacher", 0), 4),
        "breakthrough_gate": gate,
    }, ensure_ascii=False, indent=1))
    return gate


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
