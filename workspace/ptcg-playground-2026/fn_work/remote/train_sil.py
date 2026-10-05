"""自模仿学习（SIL）：自产对局→只学赢家的决策——低方差的自产数据闭环

替代 REINFORCE 的噪声梯度：CE 机器已被蒸馏验证（0.99 收敛）；
赢家轨迹=策略自己打出来的高回报路径，照着学=策略改进的自然循环。
"""
import json, os, random, sys, time
from multiprocessing import Pool

sys.path.insert(0, "src")
import numpy as np

_G = {}

def _base(deck):
    def a(obs, config=None):
        if obs.get("select") is None:
            return list(deck)
        sel = obs["select"]
        return list(range(min(sel.get("maxCount") or 0, len(sel.get("option") or []))))
    return a

def _init_worker():
    from kaggle_environments.envs.cabt import cabt
    from learn.bc_policy import MLP
    from learn.bc_policy_v3 import build_features
    from learn.eval_agent import make_agent as make_eval_agent
    from shared.play_local_match import play_local_match
    _G["deck"] = list(cabt.deck)
    _G["MLP"] = MLP
    _G["build"] = build_features
    _G["eval_agent"] = make_eval_agent()
    _G["play"] = play_local_match
    _G["v5"] = _base(_G["deck"])

def make_policy_agent(model, record, temperature=1.0, seat="a"):
    rng = random.Random(os.getpid() * 13 + hash(seat) % 9999)
    def agent(obs, config=None):
        sel = (obs or {}).get("select")
        if sel is None:
            return list(_G["deck"])
        opts = sel.get("option") or []
        mc = int(sel.get("maxCount") or 0)
        mn = int(sel.get("minCount") or 0)
        if not opts or mc <= 0:
            return []
        X = np.stack(_G["build"](obs))
        H = np.tanh(X @ model.W1.T + model.b1)
        s = (H @ model.W2.T + model.b2).ravel()
        k = mc if mn == mc else max(mn, min(1, mc))
        k = max(1, min(k, len(opts)))
        if temperature <= 0.05:
            order = sorted(range(len(opts)), key=lambda i: -s[i])
            chosen = order[:k]
        else:
            g = np.array([-np.log(max(rng.random(), 1e-12)) for _ in s])
            noisy = s / max(temperature, 1e-6) - g
            chosen = sorted(range(len(opts)), key=lambda i: -noisy[i])[:k]
        if record is not None:
            record.append({"feats": _G["build"](obs), "chosen": list(chosen)})
        return chosen
    return agent

def play_batch(args):
    model_w, n_games, opponent_mode, seed0, temperature = args
    MLP = _G["MLP"]
    m = MLP(h=96, seed=0, d=model_w["d"])
    m.W1 = np.array(model_w["W1"]); m.b1 = np.array(model_w["b1"])
    m.W2 = np.array(model_w["W2"]); m.b2 = np.array(model_w["b2"])
    play = _G["play"]; deck = _G["deck"]
    winners_rows = []
    n_win = n_loss = 0
    for g in range(n_games):
        rec_a, rec_b = [], []
        ag_a = make_policy_agent(m, rec_a, temperature, seat=f"a{os.getpid()}{g}")
        if opponent_mode == "self":
            ag_b = make_policy_agent(m, rec_b, temperature, seat=f"b{os.getpid()}{g}")
        else:
            ag_b = _G.get(opponent_mode, _G["v5"])
        try:
            r = play(ag_a, ag_b, deck, deck, seed=seed0 + g, config={"bo": 3})
        except Exception:
            continue
        rw = r["rewards"]
        if rw[0] is None or rw[1] is None:
            continue
        for rec, seat in ((rec_a, 0), (rec_b, 1)):
            if opponent_mode != "self" and rec is rec_b:
                continue
            if rw[seat] > 0:
                n_win += 1
                for step in rec:
                    for c in step["chosen"]:
                        winners_rows.append((step["feats"], c, "sil"))
            else:
                n_loss += 1
    return winners_rows, n_win, n_loss

def main():
    _init_worker()
    t0 = time.time()
    NPROC = 28  # 2026-10-06 升载：12 工人只吃 13% CPU，喂饱 32 核
    pool = Pool(NPROC, initializer=_init_worker)
    MLP = _G["MLP"]

    # 起点=蒸馏专家（BC）
    model = MLP(h=96, seed=11, d=124)
    def export_w(m):
        return {"d": 124, "W1": m.W1.tolist(), "b1": m.b1.tolist(), "W2": m.W2.tolist(), "b2": m.b2.tolist()}
    drows = [r for chunk in pool.map(_distill, [(12, 500000 + k * 100) for k in range(NPROC)]) for r in chunk]
    model.train(drows, epochs=12, lr=0.02)
    print(f"[sil] BC 起点 rows={len(drows)}", flush=True)
    best = {"fit": -1, "w": export_w(model)}
    GAMES, ITERS = 240, 60
    for it in range(1, ITERS + 1):
        temp = 0.9 if it < ITERS * 0.6 else 0.3  # 前期探索后期收敛
        batch = [
            (export_w(model), GAMES // 2, "self", 2000000 + it * 1000, temp),
            (export_w(model), GAMES // 4, "v5", 2100000 + it * 1000, temp),
            (export_w(model), GAMES // 4, "eval_agent", 2200000 + it * 1000, temp),
        ]
        chunks = pool.map(play_batch, batch)
        rows = [r for ch in chunks for r in ch[0]]
        nwin = sum(ch[1] for ch in chunks)
        nloss = sum(ch[2] for ch in chunks)
        if len(rows) > 100:
            model.train(rows, epochs=3, lr=0.01)
        if it % 5 == 0 or it == 1:
            ev = _eval(export_w(model), 12, 810000 + it)
            score = ev["v5"] + ev["eval_agent"]
            mark = ""
            if score > best["fit"]:
                best = {"fit": score, "w": export_w(model)}
                mark = " *BEST*"
                json.dump(best["w"], open("weights/sil_best.json", "w"))
            print(f"[sil] it{it}: win={nwin} loss={nloss} rows={len(rows)} eval={ev}{mark} ({time.time()-t0:.0f}s)", flush=True)
        json.dump(export_w(model), open("weights/sil_latest.json", "w"))
    fin = {"eval": _eval(best["w"], 24, 777000), "best_fit": best["fit"], "elapsed_s": round(time.time() - t0)}
    json.dump(fin, open("sil_results.json", "w"), indent=1)
    print(json.dumps(fin), flush=True)

def _distill(args):
    n_games, seed0 = args
    rows = []
    expert = _G["eval_agent"]
    deck = _G["deck"]
    def recorder(obs, config=None):
        choice = expert(obs, config)
        sel = (obs or {}).get("select")
        if sel and isinstance(choice, list) and len(choice) == 1:
            rows.append((_G["build"](obs), choice[0], "d"))
        return choice
    for g in range(n_games):
        try:
            _G["play"](recorder, expert, deck, deck, seed=seed0 + g, config={"bo": 3})
        except Exception:
            continue
    return rows

def _eval(model_w, games, seed0):
    MLP = _G["MLP"]
    m = MLP(h=96, seed=0, d=model_w["d"])
    m.W1 = np.array(model_w["W1"]); m.b1 = np.array(model_w["b1"])
    m.W2 = np.array(model_w["W2"]); m.b2 = np.array(model_w["b2"])
    play = _G["play"]; deck = _G["deck"]
    res = {}
    for name, y in (("v5", _G["v5"]), ("eval_agent", _G["eval_agent"])):
        won = 0
        for i in range(games):
            ag = make_policy_agent(m, None, temperature=0.05, seat=f"e{os.getpid()}{i}")
            swap = i % 2 == 1
            a, b = (y, ag) if swap else (ag, y)
            r = play(a, b, deck, deck, seed=seed0 + i, config={"bo": 3})
            mine = r["rewards"][1] if swap else r["rewards"][0]
            won += (mine or -1) > 0
        res[name] = won / games
    return res

if __name__ == "__main__":
    main()
