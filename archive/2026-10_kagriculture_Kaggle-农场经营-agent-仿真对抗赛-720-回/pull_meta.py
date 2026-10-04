#!/usr/bin/env python3
"""r32/r33 loss-audit step 1: submissions + episodes metadata pull.
Auth pattern follows fn_docs/hybrid/results/2026-09-23-round30-read.json source node.
Slug extracted programmatically from that file's recorded commands (not hand-typed).
"""
import json, os, re, subprocess, sys, time

KAGGLE = "/home/renyxin/.local/bin/kaggle"
WD = None  # campaign root resolved by glob in __main__
REFS = {"r30": 56491673, "r31": 56508268, "r32": 56517593, "r33": 56517991}
OUT = "/tmp/kagr_root"


def sh(args, tries=3):
    for i in range(tries):
        p = subprocess.run(args, capture_output=True, text=True, timeout=300)
        if p.returncode == 0:
            return p.stdout
        time.sleep(3 * (i + 1))
    raise RuntimeError(f"cmd failed rc={p.returncode}: {p.stderr[-400:]}")


def raw_decode_list(out):
    # CLI tails a usage line after the JSON array
    idx = out.rfind("]")
    return json.JSONDecoder().raw_decode(out[: idx + 1])[0]


def main():
    # 1) slug from prior snapshot (programmatic, no hand-splicing)
    src = json.load(open(f"{WD}/fn_docs/hybrid/results/2026-09-23-round30-read.json"))
    cmds = src["source"]["commands"]
    slugs = set()
    for c in cmds:
        m = re.search(r"competitions (?:submissions|episodes|replay) (\S+)", c)
        if m and not m.group(1).isdigit() and re.fullmatch(r"[a-z0-9-]+", m.group(1)):
            slugs.add(m.group(1))
    assert len(slugs) == 1, slugs
    slug = slugs.pop()
    # cross-check live
    live = sh([KAGGLE, "competitions", "list", "-s", slug, "--csv"])
    assert f"/competitions/{slug}" in live, f"slug {slug} not live"
    print("slug:", slug)

    # 2) token injection per source node (429-tolerant)
    tok = subprocess.run([KAGGLE, "auth", "print-access-token"],
                         capture_output=True, text=True)
    tok = tok.stdout.strip() if tok.returncode == 0 else ""
    if tok:
        os.environ["KAGGLE_API_TOKEN"] = tok
        print("token injected, len", len(tok))
    else:
        print("token unavailable (print-access-token 429); proceeding on default kaggle.json creds")

    # 3) submissions
    subs = raw_decode_list(sh([KAGGLE, "competitions", "submissions", slug, "--format", "json"]))
    json.dump(subs, open(f"{OUT}/submissions.json", "w"), indent=1)
    now_rows = {}
    for s in subs:
        ref = s.get("ref") or s.get("id")
        if ref in REFS.values():
            now_rows[str(ref)] = {
                "ref": ref, "date": str(s.get("date")),
                "description": s.get("description"),
                "status": str(s.get("status")),
                "publicScore": s.get("publicScore"),
            }
    print(json.dumps(now_rows, ensure_ascii=False, indent=1))

    # 4) episodes per ref
    eps_out = {}
    for tag, ref in REFS.items():
        lst = raw_decode_list(sh([KAGGLE, "competitions", "episodes", str(ref), "--format", "json"]))
        json.dump(lst, open(f"{OUT}/episodes-{tag}-{ref}.json", "w"))
        types = {}
        ids_by_type = {}
        pend = []
        for e in lst:
            t = e.get("type", "?")
            types[t] = types.get(t, 0) + 1
            ids_by_type.setdefault(t, []).append(e["id"])
            if e.get("state") not in ("DONE", "COMPLETE", None):
                pend.append((e["id"], e.get("state")))
        eps_out[tag] = {"ref": ref, "n_total": len(lst), "types": types,
                        "pending_states": pend,
                        "ids_public": sorted(ids_by_type.get("PublicLeaderboard", []))}
        print(tag, ref, "total", len(lst), types, "pending", len(pend))
        if not ids_by_type.get("PublicLeaderboard") and types:
            print("  type keys sample:", lst[-1])
    json.dump(eps_out, open(f"{OUT}/meta_summary.json", "w"), indent=1)
    print("done")


if __name__ == "__main__":
    WD = sys.argv[1]
    main()
